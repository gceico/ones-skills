#!/usr/bin/env python3
"""Lay out a print-ready photobook PDF from <work_dir>/graded + <work_dir>/book.json.

Usage: python build_book.py <work_dir>

Output (in <work_dir>):
  <output>.pdf          one PDF, single pages (not spreads), trim + bleed, page 1 = front cover,
                        last page = back cover, photos as 300 dpi images, all text as embedded vector fonts
  preview/pNNN.jpg      small previews with text, for checking
  plan.txt              page-by-page plan (what is on every page)
  dpi_log.json          effective print resolution of every placed photo (used by quality_report.py)

Layout rules (why they exist):
  - 1-2 photos per page; low-res phone photos are never enlarged past print.min_dpi so they stay sharp.
  - High-res photos sometimes get a full-bleed page for rhythm; never two message pages in a row.
  - Text and photos on the inner side stay `binding_margin_mm` from the spine (glued books don't open flat).
  - New folders in graded/ that are not in book.json become chapters automatically (before the "last" one).
"""
import glob, json, os, re, sys, urllib.request
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

WORK = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
cfg = json.load(open(os.path.join(WORK, 'book.json')))
P = {'width_mm': 300, 'height_mm': 300, 'bleed_mm': 3, 'binding_margin_mm': 22, 'outer_margin_mm': 20, 'gap_mm': 6}
P.update(cfg.get('page', {}))
PR = {'min_dpi': 170, 'hero_min_dpi': 125}
PR.update(cfg.get('print', {}))
DPI = 300
MM = DPI / 25.4
TW, TH, BLEED = P['width_mm'], P['height_mm'], P['bleed_mm']
PW, PH = TW + 2 * BLEED, TH + 2 * BLEED            # page incl. bleed, mm
PXW, PXH = round(PW * MM), round(PH * MM)
BIND, OUT_M, GAP = P['binding_margin_mm'], P['outer_margin_mm'], P['gap_mm']
S = min(TW, TH) / 300                              # type scale: designed on 300 mm, scales to A5..A3

def hexrgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
ST = {'paper': '#FCFAF6', 'ink': '#282624', 'muted': '#78726A', 'accent': '#C4807C', 'quote': '#C8BEAF'}
ST.update(cfg.get('style', {}))
PAPER, INK, MUTED, ACCENT, QUOTE = (hexrgb(ST[k]) for k in ('paper', 'ink', 'muted', 'accent', 'quote'))
FD = os.path.join(WORK, 'fonts')

def font(file, size_pt):
    f = ImageFont.truetype(os.path.join(FD, file), round(size_pt * S / 72 * DPI))
    f.file, f.pt = file, size_pt * S
    return f
TITLE, SERIF_I, BODY_I, LABEL, LABEL_L = 'CG-Light.ttf', 'CGI-Regular.ttf', 'CGI-Medium.ttf', 'Jost-Regular.ttf', 'Jost-Light.ttf'

def mm(v): return round(v * MM)
def pref(name, keys): return any(name.startswith(k) for k in keys)

# ---------- photos ----------
inv = json.load(open(os.path.join(WORK, 'inventory.json'))) if os.path.exists(os.path.join(WORK, 'inventory.json')) else {}

class Photo:
    def __init__(self, path):
        self.path = path
        self.group = os.path.basename(os.path.dirname(path))
        self.name = os.path.basename(path)[:-4]
        with Image.open(path) as im: self.w, self.h = im.size
        self.ar = self.w / self.h
    @property
    def hires(self): return min(self.w, self.h) >= 2800
    def max_mm(self, dpi=None):
        d = dpi or PR['min_dpi']; return self.w / d * 25.4, self.h / d * 25.4
    def key(self):
        d = (inv.get(f'{self.group}/{self.name}') or {}).get('date')
        return (1, d) if d else (0, self.name)       # undated first, then chronological

def find(prefix):
    if not prefix: return None
    hits = sorted(glob.glob(os.path.join(WORK, 'graded', prefix + '*.jpg')) + glob.glob(os.path.join(WORK, 'graded', '*', prefix + '*.jpg')))
    exact = [h for h in hits if os.path.basename(h)[:-4] == os.path.basename(prefix)]
    return Photo((exact or hits)[0]) if hits else None

COVER = find(cfg.get('cover', {}).get('photo'))

def load_group(folder):
    moves, ex = cfg.get('moves', {}), cfg.get('exclude', [])
    moved = lambda p: next((t for k, t in moves.items() if os.path.basename(p).startswith(k)), None)
    paths = [p for p in glob.glob(os.path.join(WORK, 'graded', folder, '*.jpg')) if moved(p) in (None, folder)]
    paths += [p for p in glob.glob(os.path.join(WORK, 'graded', '*', '*.jpg')) if moved(p) == folder and os.path.basename(os.path.dirname(p)) != folder]
    ps = [Photo(p) for p in paths if not pref(os.path.basename(p), ex)]
    if COVER and not cfg.get('cover', {}).get('repeat_inside'): ps = [p for p in ps if p.path != COVER.path]
    order = cfg.get('order', {}).get(folder)
    if order:   # explicit order wins; unlisted photos keep date order after the listed ones
        rank = lambda p: next((i for i, k in enumerate(order) if p.name.startswith(k)), len(order))
        return sorted(ps, key=lambda p: (rank(p), p.key()))
    return sorted(ps, key=Photo.key)

HAAR = os.path.join(WORK, 'haar_face.xml')
if not os.path.exists(HAAR):
    try: urllib.request.urlretrieve('https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml', HAAR)
    except Exception: pass
FACES = cv2.CascadeClassifier(HAAR) if os.path.exists(HAAR) else None

def face_center(im):
    if FACES is None or FACES.empty(): return 0.5, 0.4
    small = im.copy(); small.thumbnail((800, 800))
    fs = FACES.detectMultiScale(cv2.cvtColor(np.asarray(small), cv2.COLOR_RGB2GRAY), 1.1, 5, minSize=(30, 30))
    if len(fs) == 0: return 0.5, 0.4
    return (np.mean([a + c / 2 for a, b, c, d in fs]) / small.width, np.mean([b + d / 2 for a, b, c, d in fs]) / small.height)

def cover_crop(im, ar):
    cx, cy = face_center(im); W, H = im.size
    if W / H > ar:
        nw = H * ar; x0 = min(max(cx * W - nw / 2, 0), W - nw); return im.crop((round(x0), 0, round(x0 + nw), H))
    nh = W / ar; y0 = min(max(cy * H - nh / 2, 0), H - nh); return im.crop((0, round(y0), W, round(y0 + nh)))

LOG, CUR, PAGE_TEXT = [], [0], []
def draw_photo(pg, photo, x, y, w, h, crop=False):
    im = Image.open(photo.path).convert('RGB')
    if crop: im = cover_crop(im, w / h)
    used_w = im.width
    pg.paste(im.resize((mm(w), mm(h)), Image.LANCZOS), (mm(x), mm(y)))
    LOG.append((photo.group + '/' + photo.name, round(used_w / (w / 25.4)), CUR[0], photo.path))

# ---------- geometry ----------
def content_box(right):
    """right-hand (odd) pages have the spine on the left"""
    l = BLEED + (BIND if right else OUT_M); r = BLEED + TW - (OUT_M if right else BIND)
    return l, BLEED + OUT_M, r, BLEED + TH - OUT_M

def new_page(): return Image.new('RGB', (PXW, PXH), PAPER)
def fit(ar, bw, bh): return (bw, bw / ar) if ar > bw / bh else (bh * ar, bh)
def limit(photo, w, h, dpi=None):
    mw, mh = photo.max_mm(dpi); s = min(1, mw / w, mh / h); return w * s, h * s

def text_center(y, txt, f, fill, cx=None):
    PAGE_TEXT.append((PXW / 2 if cx is None else cx, y, txt, f, fill))

def _greedy(words, f, maxw):
    lines, cur = [], ''
    for word in words:
        t = (cur + ' ' + word).strip()
        if not cur or f.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = word
    return lines + [cur]

def wrap(text, f, maxw):
    """balanced wrapping: as few lines as greedy wrapping, but evenly long (no lonely last word);
    numbers like '1 000' never break"""
    out = []
    for para in text.split('\n'):
        para = re.sub(r'(\d) (\d{3})', '\\1\u00a0\\2', para)
        words = [w for w in para.split(' ') if w]
        if not words: out.append([]); continue
        n = len(_greedy(words, f, maxw)); lo, hi = maxw * 0.4, maxw
        for _ in range(18):
            mid = (lo + hi) / 2
            if len(_greedy(words, f, mid)) <= n: hi = mid
            else: lo = mid
        out.append(_greedy(words, f, hi))
    return out

def heart(d, cx, cy, s, fill):
    r = s / 2
    d.ellipse((cx - s, cy - r, cx, cy + r), fill=fill); d.ellipse((cx, cy - r, cx + s, cy + r), fill=fill)
    d.polygon([(cx - s + r * 0.06, cy + r * 0.35), (cx + s - r * 0.06, cy + r * 0.35), (cx, cy + s * 1.35)], fill=fill)

# ---------- pages ----------
def page_full(photo, right):
    pg = new_page(); draw_photo(pg, photo, 0, 0, PW, PH, crop=True); return pg

def page_single(photo, right, scale=1.0):
    pg = new_page(); l, t, r, b = content_box(right)
    w, h = limit(photo, *fit(photo.ar, (r - l) * scale, (b - t) * scale))
    draw_photo(pg, photo, (l + r) / 2 - w / 2, (t + b) / 2 - h / 2 - 4 * S, w, h); return pg

def page_pair(a, b, right):
    pg = new_page(); l, t, r, b_ = content_box(right); bw, bh = r - l, b_ - t
    h = min(bh, (bw - GAP) / (a.ar + b.ar)); row = (h * a.ar, h, b.ar * h, h)
    w = min(bw, (bh - GAP) / (1 / a.ar + 1 / b.ar)); col = (w, w / a.ar, w, w / b.ar)
    mode, (w1, h1, w2, h2) = ('row', row) if row[0] * row[1] + row[2] * row[3] >= col[0] * col[1] + col[2] * col[3] else ('col', col)
    s = min(1, *[m / v for p, dims in ((a, (w1, h1)), (b, (w2, h2))) for m, v in zip(p.max_mm(), dims)])
    s = max(s, 0.78)          # keep pairs from getting tiny; worst case stays ~160 dpi
    w1, h1, w2, h2 = w1 * s, h1 * s, w2 * s, h2 * s
    cx, cy = (l + r) / 2, (t + b_) / 2
    if mode == 'row':
        x = cx - (w1 + GAP + w2) / 2
        draw_photo(pg, a, x, cy - h1 / 2, w1, h1); draw_photo(pg, b, x + w1 + GAP, cy - h2 / 2, w2, h2)
    else:
        y = cy - (h1 + GAP + h2) / 2
        draw_photo(pg, a, cx - w1 / 2, y, w1, h1); draw_photo(pg, b, cx - w2 / 2, y + h1 + GAP, w2, h2)
    return pg

def page_opener(ch, num, hero, right):
    pg = new_page(); l, t, r, b = content_box(right)
    text_center(mm(t + 6 * S), f'{num:02d}', font(LABEL_L, 13), MUTED)
    text_center(mm(t + 18 * S), ch['title'], font(TITLE, 76), INK)
    extra = 0
    if ch.get('subtitle'):
        sf = font(SERIF_I, 26); sub = wrap(ch['subtitle'], sf, mm(TW * 0.73))[0]
        for i, ln in enumerate(sub): text_center(mm(t + (46 + i * 11) * S), ln, sf, MUTED)
        extra = (len(sub) - 1) * 11 * S
    if hero:
        t += extra; top = t + 60 * S
        w, h = fit(hero.ar, r - l, b - top)
        w, h = limit(hero, w, h, PR['hero_min_dpi'])
        draw_photo(pg, hero, (l + r) / 2 - w / 2, top + 2 * S + max(0, (b - top - h) / 2 - 22 * S), w, h)
    return pg

def page_message(msg, right):
    pg = new_page(); d = ImageDraw.Draw(pg)
    n = len(msg['text'])
    f = font(BODY_I, 28 if n < 300 else 25 if n < 500 else 22 if n < 800 else 19)
    paras = wrap(msg['text'], f, mm(TW * 0.57))
    lh = f.size * 1.5; pgap = lh * 0.55
    lines = []
    for i, p in enumerate(paras):
        if i: lines.append(None)
        lines += p
    total = sum(lh if ln is not None else pgap for ln in lines)
    y = (PXH - total) / 2 - mm(8 * S)
    text_center(y - mm(34 * S), '\u201c', font(TITLE, 90), QUOTE)
    for ln in lines:
        if ln is None: y += pgap; continue
        text_center(y, ln, f, INK); y += lh
    y += mm(6 * S); heart(d, PXW / 2, y + mm(2 * S), mm(2.4 * S), ACCENT); y += mm(12 * S)
    text_center(y, '\u2014  ' + msg['author'], font(LABEL, 15), INK)
    if msg.get('relation'): text_center(y + mm(9 * S), msg['relation'], font(LABEL_L, 12), MUTED)
    return pg

def page_title(right, p):
    pg = new_page()
    text_center(PXH * 0.36, cfg['title'], font(TITLE, 120), INK)
    if cfg.get('subtitle'): text_center(PXH * 0.36 + mm(53 * S), cfg['subtitle'], font(SERIF_I, 34), MUTED)
    return pg

def page_stats(right, p):
    pg = new_page(); rows = p.get('rows', []); y = (PXH - len(rows) * mm(42 * S)) / 2
    for big, small in rows:
        text_center(y, big, font(TITLE, 54), INK); text_center(y + mm(24 * S), small, font(LABEL_L, 14), MUTED); y += mm(42 * S)
    return pg

def page_text(right, p):
    pg = new_page(); f = font(SERIF_I, p.get('size', 40))
    text_center(PXH * 0.44, p.get('text', ''), f, INK)
    if p.get('subtext'): text_center(PXH * 0.44 + mm(24 * S), p['subtext'], font(LABEL_L, 12), MUTED)
    return pg

def page_cover():
    pg = new_page(); c = cfg.get('cover', {})
    y = BLEED + 34 * S
    if COVER:
        w = TW * c.get('photo_width', 0.7); h = w / COVER.ar
        if h > TH * 0.55: w, h = w * TH * 0.55 / h, TH * 0.55     # leave room for the title
        w, h = limit(COVER, w, h, PR['hero_min_dpi'])
        draw_photo(pg, COVER, BLEED + (TW - w) / 2, y, w, h); y += h + 18 * S
    else:
        y = BLEED + TH * 0.38
    text_center(mm(y), c.get('title', cfg['title']), font(TITLE, 96), INK)
    sub = c.get('subtitle', cfg.get('subtitle'))
    if sub: text_center(mm(y + 38 * S), sub, font(SERIF_I, 30), MUTED)
    return pg

def page_back():
    pg = new_page()
    if cfg.get('cover', {}).get('back_text'): text_center(mm(BLEED + TH - 40 * S), cfg['cover']['back_text'], font(LABEL_L, 10), MUTED)
    return pg

# ---------- sequencing ----------
def chapter_pages(photos, hero_name):
    hero = next((p for p in photos if p.name == hero_name), None) or next((p for p in photos if hero_name and p.name.startswith(hero_name)), None) or photos[0]
    rest = [p for p in photos if p is not hero]
    feat, nofull = cfg.get('feature', []), cfg.get('nofull', []) + cfg.get('secondary', [])
    seq, i, since_big = [], 0, 9
    while i < len(rest):
        p = rest[i]
        if pref(p.name, feat): seq.append(('full', [p])); i += 1; since_big = 0; continue
        if cfg.get('auto_full', True) and p.hires and since_big >= 3 and not pref(p.name, nofull):
            seq.append(('full' if 0.7 <= p.ar <= 1.4 else 'single', [p])); i += 1; since_big = 0; continue
        if i + 1 < len(rest):
            if pref(rest[i + 1].name, feat): seq.append(('full', [rest.pop(i + 1)])); since_big = 0; continue
            seq.append(('pair', [p, rest[i + 1]])); i += 2
        else:
            seq.append(('single', [p])); i += 1
        since_big += 1
    return hero, seq

def plan_book():
    chapters_cfg = cfg.get('chapters', [])
    known = [c['folder'] for c in chapters_cfg]
    extra = sorted(set(os.path.basename(p) for p in glob.glob(os.path.join(WORK, 'graded', '*'))) - set(known))
    chapters = [c for c in chapters_cfg if not c.get('last')]
    chapters += [{'folder': f, 'title': f.replace('-', ' ').title()} for f in extra]
    chapters += [c for c in chapters_cfg if c.get('last')]
    msgs = cfg.get('messages', [])
    plan = [('cover', None), ('blank', None)]
    for p in cfg.get('intro_pages', [{'type': 'title'}]): plan.append((p['type'], p))
    for n, ch in enumerate(chapters, 1):
        photos = load_group(ch['folder'])
        if not photos: continue
        hero, seq = chapter_pages(photos, ch.get('hero'))
        plan.append(('opener', (ch, n, hero)))
        mine = [m for m in msgs if m.get('after') == ch['folder']]
        for m in sorted([m for m in mine if 'pos' in m], key=lambda m: -m['pos']): seq.insert(min(m['pos'], len(seq)), ('message', m))
        for k, m in enumerate([m for m in mine if 'pos' not in m]): seq.insert(len(seq) - 2 * k if k else len(seq), ('message', m))
        plan += seq
    plan += [('message', m) for m in msgs if not m.get('after')]
    for _ in range(100):   # never two message pages in a row
        bad = next((i for i in range(1, len(plan)) if plan[i][0] == 'message' and plan[i - 1][0] == 'message'), None)
        if bad is None: break
        j = next((k for k in range(bad + 1, len(plan)) if plan[k][0] in ('pair', 'single', 'full')), None)
        if j is None: break
        plan.insert(j, plan.pop(bad))
    if cfg.get('closing'): plan.append(('text', cfg['closing']))
    if len(plan) % 2 == 0: plan.append(('blank', None))      # total page count stays even
    plan.append(('back', None))
    return plan

def render(kind, data, right):
    if kind == 'cover': return page_cover()
    if kind == 'back': return page_back()
    if kind == 'blank': return new_page()
    if kind == 'title': return page_title(right, data)
    if kind == 'stats': return page_stats(right, data)
    if kind == 'text': return page_text(right, data)
    if kind == 'opener': return page_opener(*data, right)
    if kind == 'full': return page_full(data[0], right)
    if kind == 'single': return page_single(data[0], right, 0.6 if pref(data[0].name, cfg.get('secondary', [])) else 1.0)
    if kind == 'pair': return page_pair(*data, right)
    if kind == 'message': return page_message(data, right)
    raise ValueError(kind)

def main():
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm as RMM
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for fn in (TITLE, SERIF_I, BODY_I, LABEL, LABEL_L): pdfmetrics.registerFont(TTFont(fn[:-4], os.path.join(FD, fn)))
    for dd in ('pages', 'preview'):
        os.makedirs(os.path.join(WORK, dd), exist_ok=True)
        for f in glob.glob(os.path.join(WORK, dd, '*.jpg')): os.remove(f)
    plan = plan_book()
    out = os.path.join(WORK, cfg.get('output', 'photobook_print.pdf'))
    c = canvas.Canvas(out, pagesize=(PW * RMM, PH * RMM), initialFontName=LABEL_L[:-4], initialFontSize=10)
    c.setTitle(cfg['title'] + (' - ' + cfg['subtitle'] if cfg.get('subtitle') else ''))
    PT = 72 / DPI; lines = []
    for idx, (kind, data) in enumerate(plan, 1):
        PAGE_TEXT.clear(); CUR[0] = idx
        pg = render(kind, data, idx % 2 == 1)
        fn = os.path.join(WORK, 'pages', f'p{idx:03d}.jpg'); pg.save(fn, quality=93, dpi=(DPI, DPI))
        c.drawImage(fn, 0, 0, PW * RMM, PH * RMM)
        pv = pg.copy(); d = ImageDraw.Draw(pv)
        for cx, y, txt, f, fill in PAGE_TEXT:            # vector text in the PDF, burned-in text in the preview
            c.setFillColorRGB(*[v / 255 for v in fill]); c.setFont(f.file[:-4], f.pt)
            c.drawCentredString(cx * PT, PH * RMM - (y + f.getmetrics()[0]) * PT, txt)
            d.text((cx - f.getlength(txt) / 2, y), txt, font=f, fill=fill)
        c.showPage()
        pv.thumbnail((1200, 1200)); pv.save(os.path.join(WORK, 'preview', f'p{idx:03d}.jpg'), quality=88)
        what = ', '.join(p.group + '/' + p.name for p in data) if kind in ('pair', 'single', 'full') else \
            (data[0]['title'] if kind == 'opener' else data.get('author', '') if kind == 'message' and isinstance(data, dict) else '')
        lines.append(f'{idx:3d}  {"R" if idx % 2 else "L"}  {kind:8s} {what}')
    c.save()
    open(os.path.join(WORK, 'plan.txt'), 'w').write('\n'.join(lines) + '\n')
    json.dump(LOG, open(os.path.join(WORK, 'dpi_log.json'), 'w'))
    print(f'{len(plan)} pages -> {out}  ({os.path.getsize(out) / 1e6:.0f} MB)')
    print(f'page size {PW} x {PH} mm incl. {BLEED} mm bleed (trim {TW} x {TH} mm)')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Flag photos that may look bad in print. Run after build_book.py.

Usage: python quality_report.py <work_dir>
Writes <work_dir>/quality_report.md and crops/ (each flagged photo at true print scale, ~5 cm square),
so you can look at the crops before telling the user. Metrics are heuristics: always look before judging.

Flags:
  LOW-RES   printed below 150 dpi (soft/pixelated up close); 150-170 = borderline
  SOFT      little fine detail (motion blur, out of focus, heavy WhatsApp compression)
  DARK      most of the photo is near black (night/club shots print darker than they look on screens)
  NOISY     strong grain
"""
import json, os, sys
import numpy as np, cv2

def main(work):
    log = json.load(open(os.path.join(work, 'dpi_log.json')))
    rows = []
    for name, dpi, page, path in log:
        g = cv2.imread(path, 0)
        s = 1200 / max(g.shape); sm = cv2.resize(g, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        sharp = cv2.Laplacian(sm, cv2.CV_64F).var()
        noise = float(np.median(np.abs(sm.astype(float) - cv2.GaussianBlur(sm, (0, 0), 1.5))))
        dark = float((g < 25).mean())
        flags = []
        if dpi < 150: flags.append(f'LOW-RES ({dpi} dpi)')
        elif dpi < 170: flags.append(f'borderline res ({dpi} dpi)')
        if sharp < 120: flags.append(f'SOFT (detail {sharp:.0f})')
        if dark > 0.35 and g.mean() < 75: flags.append(f'DARK ({dark*100:.0f}% near-black)')
        if noise > 6: flags.append(f'NOISY ({noise:.0f})')
        severity = sum(3 if f.startswith(('LOW-RES', 'SOFT')) else 1 for f in flags)
        if sharp < 40: severity += 3
        rows.append((severity, page, name, dpi, flags, path))
    flagged = sorted([r for r in rows if r[4]], key=lambda r: (-r[0], r[1]))
    os.makedirs(os.path.join(work, 'crops'), exist_ok=True)
    from PIL import Image
    out = ['# Print quality check', '', f'{len(rows)} placed photos, {len(flagged)} flagged. Look at crops/ before deciding.', '',
           '| Risk | Page | Photo | Print dpi | Why |', '|---|---|---|---|---|']
    for sev, page, name, dpi, flags, path in flagged:
        risk = 'high' if sev >= 6 else 'medium' if sev >= 3 else 'low'
        out.append(f'| {risk} | {page} | {name} | {dpi} | {"; ".join(flags)} |')
        im = Image.open(path); cw = int(dpi / 25.4 * 50)   # ~5 cm of print
        cx, cy = im.width // 2, im.height // 2
        im.crop((cx - cw // 2, cy - cw // 2, cx + cw // 2, cy + cw // 2)).resize((600, 600)).save(
            os.path.join(work, 'crops', f'p{page:03d}_{os.path.basename(name)[:20]}.jpg'), quality=85)
    open(os.path.join(work, 'quality_report.md'), 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])

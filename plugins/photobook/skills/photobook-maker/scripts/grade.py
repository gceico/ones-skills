#!/usr/bin/env python3
"""Give every photo the same print-ready look. src/ -> graded/

Usage: python grade.py <work_dir> [--force]

Per photo: rotate/crop fixes from book.json, partial white balance, luminance stretch, gentle local
contrast, soft S-curve, saturation normalised towards a shared target, a slight shared warmth, soft
matte blacks and resolution-aware sharpening. Optional black & white conversion.

book.json "grade" block (all optional; keys are photo-name prefixes or group names):
  "rotate": {"img_0012": 90}            degrees counter-clockwise
  "crop":   {"scan-03": [0, 0.16, 0.99, 0.905]}   fractions x0,y0,x1,y1 (applied after rotation)
  "bw":     ["img_0420", "club-night-2"]    convert to black & white
  "old_photos": ["childhood"]           stronger colour-cast correction (scans of prints)
  "warmth": 1.0                         0 = neutral, 1 = default, 2 = warmer
"""
import glob, json, os, sys
import numpy as np, cv2
from PIL import Image

def match(name, group, keys):
    return any(name.startswith(k) or group == k for k in keys)

def curve(x):
    return ((0.5 + 0.5 * np.tanh(2.2 * (x - 0.5)) / np.tanh(1.1)) * 0.35 + x * 0.65).astype(np.float32)

def grade(img, wb_strength=0.4, bw=False, warmth=1.0):
    a = img.astype(np.float32) / 255
    lum = a.mean(2); m = (lum > 0.15) & (lum < 0.9)
    means = a[m].mean(0) if m.sum() > 100 else a.reshape(-1, 3).mean(0)
    g = np.clip(1 + (means.mean() / means - 1) * wb_strength, 0.85, 1.18)
    a = (a * g).astype(np.float32)
    L = a @ np.array([0.299, 0.587, 0.114], np.float32)
    lo, hi = np.percentile(L, [0.4, 99.6]); hi = max(hi, lo + 0.3)
    a = np.clip((a - lo) / (hi - lo), 0, 1).astype(np.float32)
    lab = cv2.cvtColor((a * 255).astype(np.uint8), cv2.COLOR_RGB2LAB)
    cl = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8)).apply(lab[..., 0])
    lab[..., 0] = (0.65 * lab[..., 0] + 0.35 * cl).astype(np.uint8)
    a = curve(cv2.cvtColor(lab, cv2.COLOR_LAB2RGB).astype(np.float32) / 255)
    if bw:
        y = curve(a @ np.array([0.3, 0.59, 0.11], np.float32))
        a = np.stack([y * 1.01, y, y * 0.985], 2)
    else:
        hsv = cv2.cvtColor(np.clip(a, 0, 1).astype(np.float32), cv2.COLOR_RGB2HSV)
        s = hsv[..., 1]; f = np.clip(0.38 / max(float(s.mean()), 0.05), 0.88, 1.18)
        hsv[..., 1] = np.clip(s * f, 0, 1).astype(np.float32)
        a = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        a = a * np.array([1 + 0.02 * warmth, 1.0, 1 - 0.025 * warmth], np.float32)
    a = np.clip(0.025 + a * 0.965, 0, 1)
    u = (a * 255).astype(np.uint8)
    r = max(u.shape[:2]) / 1600
    blur = cv2.GaussianBlur(u, (0, 0), 1.2 * r)
    return cv2.addWeighted(u, 1.35, blur, -0.35, 0)

def main(work, force=False):
    cfg = json.load(open(os.path.join(work, 'book.json'))) if os.path.exists(os.path.join(work, 'book.json')) else {}
    G = cfg.get('grade', {})
    import hashlib
    h = hashlib.md5(json.dumps(G, sort_keys=True).encode()).hexdigest()
    hp = os.path.join(work, 'graded', '.grade_settings')
    if not os.path.exists(hp) or open(hp).read() != h: force = True   # settings changed -> regrade all
    n = 0
    for f in sorted(glob.glob(os.path.join(work, 'src', '*', '*.jpg'))):
        group = os.path.basename(os.path.dirname(f)); name = os.path.basename(f)[:-4]
        out = os.path.join(work, 'graded', group, name + '.jpg')
        if os.path.exists(out) and not force and os.path.getmtime(out) > os.path.getmtime(f): continue
        im = Image.open(f)
        for k, deg in G.get('rotate', {}).items():
            if name.startswith(k): im = im.rotate(deg, expand=True)
        for k, box in G.get('crop', {}).items():
            if name.startswith(k):
                W, H = im.size; im = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
        old = match(name, group, G.get('old_photos', []))
        res = grade(np.asarray(im.convert('RGB')), 0.7 if old else 0.4, match(name, group, G.get('bw', [])), G.get('warmth', 1.0))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        Image.fromarray(res).save(out, quality=94); n += 1
    os.makedirs(os.path.dirname(hp), exist_ok=True); open(hp, 'w').write(h)
    print(f'graded {n} photos')

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(sys.argv[1], '--force' in sys.argv)

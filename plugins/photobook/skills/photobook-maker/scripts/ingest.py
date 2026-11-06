#!/usr/bin/env python3
"""Ingest a photo folder into a photobook work directory.

Usage: python ingest.py <input_dir> <work_dir>

- Every sub-folder of <input_dir> becomes a group (chapter candidate); loose files go to "misc".
- HEIC/HEIF/PNG/JPG/WEBP are converted to upright RGB JPEGs in <work_dir>/src/<group>/<name>.jpg
- File and folder names are slugified (spaces, brackets and accents removed).
- Already-ingested files are skipped, so you can re-run it when the user adds photos.
- Writes <work_dir>/inventory.json: size, orientation, colour/B&W, capture date (EXIF DateTimeOriginal only).
"""
import json, os, re, sys, unicodedata
from PIL import Image, ImageOps
import numpy as np
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except ImportError:
    print('warning: pillow-heif missing, HEIC files will be skipped', file=sys.stderr)

EXT = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp', '.tif', '.tiff'}

def slug(s, maxlen=60):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'\(.*?\)', '', s)                 # drop "(notes in brackets)"
    s = re.sub(r'[^A-Za-z0-9_-]+', '-', s).strip('-').lower()
    return s[:maxlen].strip('-') or 'misc'

def main(inp, work):
    src = os.path.join(work, 'src'); os.makedirs(src, exist_ok=True)
    inv_path = os.path.join(work, 'inventory.json')
    inv = json.load(open(inv_path)) if os.path.exists(inv_path) else {}
    new = 0
    for root, _, files in os.walk(inp):
        rel = os.path.relpath(root, inp)
        group = 'misc' if rel == '.' else slug(rel.split(os.sep)[0])
        for f in sorted(files):
            if os.path.splitext(f)[1].lower() not in EXT: continue
            name = slug(os.path.splitext(f)[0], 80)
            out = os.path.join(src, group, name + '.jpg')
            key = f'{group}/{name}'
            if os.path.exists(out) and key in inv: continue
            try:
                im = Image.open(os.path.join(root, f))
                exif = im.getexif()
                date = exif.get_ifd(0x8769).get(36867)  # DateTimeOriginal only; WhatsApp copies carry receive time
                im = ImageOps.exif_transpose(im).convert('RGB')
            except Exception as e:
                print('skip', f, e, file=sys.stderr); continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            im.save(out, quality=95)
            a = np.asarray(im.resize((64, 64))).astype(float)
            sat = float((a.max(2) - a.min(2)).mean())
            inv[key] = {'w': im.width, 'h': im.height,
                        'orientation': 'portrait' if im.height > im.width else 'landscape' if im.width > im.height else 'square',
                        'bw': sat < 6, 'date': date, 'source': os.path.join(root, f)}
            new += 1
    json.dump(inv, open(inv_path, 'w'), indent=1)
    groups = {}
    for k, v in inv.items(): groups.setdefault(k.split('/')[0], []).append(v)
    print(f'{new} new photos, {len(inv)} total')
    for g, vs in sorted(groups.items()):
        p = sum(v['orientation'] == 'portrait' for v in vs); bw = sum(v['bw'] for v in vs)
        small = sum(min(v['w'], v['h']) < 1300 for v in vs)
        print(f'  {g}: {len(vs)} photos ({p} portrait, {len(vs)-p} landscape/square, {bw} b&w, {small} low-res)')

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

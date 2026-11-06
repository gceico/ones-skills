#!/usr/bin/env python3
"""Make one labelled contact sheet per group so the agent (and user) can look at the photos.

Usage: python contact_sheets.py <work_dir> [src|graded]
Writes <work_dir>/sheets/<group>.jpg. Labels are the photo-name prefixes used in book.json.
"""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont

def main(work, which='src'):
    out = os.path.join(work, 'sheets'); os.makedirs(out, exist_ok=True)
    try: font = ImageFont.truetype('DejaVuSans-Bold.ttf', 20)
    except OSError: font = ImageFont.load_default()
    for d in sorted(glob.glob(os.path.join(work, which, '*'))):
        fs = sorted(glob.glob(d + '/*.jpg'))
        if not fs: continue
        cols, T = 4, 340; rows = (len(fs) + cols - 1) // cols
        S = Image.new('RGB', (cols * T, rows * (T + 28)), 'white'); dr = ImageDraw.Draw(S)
        for i, f in enumerate(fs):
            im = Image.open(f); im.thumbnail((T - 8, T - 8))
            x, y = (i % cols) * T, (i // cols) * (T + 28)
            S.paste(im, (x + 4, y + 4))
            dr.text((x + 6, y + T), f'{i+1}: {os.path.basename(f)[:-4][:26]}', fill='red', font=font)
        S.save(os.path.join(out, os.path.basename(d) + '.jpg'), quality=80)
        print('sheet', os.path.basename(d), len(fs))

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(*sys.argv[1:3])

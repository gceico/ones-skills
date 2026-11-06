#!/usr/bin/env python3
"""One image with every spread of the book (cover alone, then left|right pairs), for a fast visual check.

Usage: python preview_spreads.py <work_dir>   -> <work_dir>/preview-spreads.jpg
"""
import glob, os, sys
from PIL import Image, ImageDraw

def main(work):
    ps = sorted(glob.glob(os.path.join(work, 'preview', 'p*.jpg')))
    first = Image.open(ps[0]); ar = first.width / first.height
    T = 260; TW = round(T * ar)
    spreads = [[ps[0]]] + [ps[i:i + 2] for i in range(1, len(ps), 2)]
    cols = 4; rows = (len(spreads) + cols - 1) // cols
    S = Image.new('RGB', (cols * (2 * TW + 30), rows * (T + 40)), (70, 70, 70)); d = ImageDraw.Draw(S)
    for i, sp in enumerate(spreads):
        x, y = (i % cols) * (2 * TW + 30) + 10, (i // cols) * (T + 40) + 10
        for j, p in enumerate(sp):
            S.paste(Image.open(p).resize((TW, T)), (x + (TW if len(sp) == 1 else j * TW), y))
        a, b = ps.index(sp[0]) + 1, ps.index(sp[-1]) + 1
        d.text((x, y + T + 6), f'p{a}' + (f'-{b}' if len(sp) > 1 else (' (cover)' if a in (1, len(ps)) else '')), fill='white')
    out = os.path.join(work, 'preview-spreads.jpg'); S.save(out, quality=82); print(out)

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])

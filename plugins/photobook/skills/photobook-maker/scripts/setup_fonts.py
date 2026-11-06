#!/usr/bin/env python3
"""Download the default book fonts (OFL, Google Fonts) and make static instances.

Usage: python setup_fonts.py <work_dir>
Creates <work_dir>/fonts/{CG-Light,CG-Regular,CGI-Regular,CGI-Medium,Jost-Light,Jost-Regular}.ttf
Cormorant Garamond (titles, messages) + Jost (small labels). Both cover Romanian, German, French,
Polish, Dutch, Spanish diacritics. Swap fonts by placing other static TTFs with the same file names.
"""
import os, sys, urllib.request
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

BASE = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'
SRC = {'CG.ttf': 'cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf',
       'CGI.ttf': 'cormorantgaramond/CormorantGaramond-Italic%5Bwght%5D.ttf',
       'Jost.ttf': 'jost/Jost%5Bwght%5D.ttf'}
OUT = {'CG-Light.ttf': ('CG.ttf', 300), 'CG-Regular.ttf': ('CG.ttf', 400),
       'CGI-Regular.ttf': ('CGI.ttf', 400), 'CGI-Medium.ttf': ('CGI.ttf', 500),
       'Jost-Light.ttf': ('Jost.ttf', 300), 'Jost-Regular.ttf': ('Jost.ttf', 400)}

def main(work):
    d = os.path.join(work, 'fonts'); os.makedirs(d, exist_ok=True)
    for out, (src, w) in OUT.items():
        if os.path.exists(os.path.join(d, out)): continue
        p = os.path.join(d, src)
        if not os.path.exists(p): urllib.request.urlretrieve(BASE + SRC[src], p)
        instantiateVariableFont(TTFont(p), {'wght': w}).save(os.path.join(d, out))
    print('fonts ready in', d)

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])

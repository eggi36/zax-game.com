#!/usr/bin/env python3
"""Ordnet gefundene Bilder den archivierten Vorschauen der Screenshot-Galerie von reflexive.net (2003) zu.

Vorschauen: tools/archive/finds_src/www.reflexive.net/zax/images/Screen Shots/*Small.jpg (150x113, Internet Archive).
Jedes Bild wird auf 150x113 verkleinert und mit jeder Vorschau verglichen (mittlere Abweichung je Farbkanal, 0-255).
Erfahrungswert: dieselbe Datei 3-6, ein anderes Bild über 18; dazwischen genauer ansehen (gleiche Szene, anderes
Einzelbild oder nachbearbeitet). Siehe tools/archive/RECHERCHE.md.

Aufruf: python3 tools/archive/match_thumbs.py BILD_ODER_ORDNER ...   (Pillow)
"""
import glob, os, sys
from PIL import Image, ImageChops, ImageStat

THUMBS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'finds_src', 'www.reflexive.net', 'zax', 'images', 'Screen Shots')

def diff(a, b): return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3

def main(args):
    thumbs = {os.path.basename(p): Image.open(p).convert('RGB') for p in sorted(glob.glob(os.path.join(THUMBS, '*mall.jpg')))}
    files = []
    for a in args:
        files += sorted(p for p in glob.glob(os.path.join(a, '**', '*'), recursive=True) if os.path.isfile(p)) if os.path.isdir(a) else [a]
    for p in files:
        try: im = Image.open(p).convert('RGB')
        except Exception: continue
        if im.size[0] < 300: continue
        small = im.resize((150, 113), Image.LANCZOS)
        best = sorted((diff(small, t), n) for n, t in thumbs.items())[:2]
        mark = 'TREFFER ' if best[0][0] < 8 else '        '
        print(f'{mark}{p} {im.size[0]}x{im.size[1]}: ' + ', '.join(f'{n} {e:.1f}' for e, n in best))

if __name__ == '__main__':
    main(sys.argv[1:] or ['.'])

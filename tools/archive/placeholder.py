#!/usr/bin/env python3
"""Rot schraffierter „MISSING: <Dateiname>“-Platzhalter für nie archivierte Bilder.

Gleiches Aussehen wie alle Platzhalter im Archiv: Grund #280000, 1-px-Diagonale #6E0000 alle 8 px,
Rahmen #FF3C3C, Text Arial 9 px #FFC8C8 bei x=4, senkrecht mittig. Das Format folgt der Endung
(.jpg → JPEG, sonst GIF), damit Inhalt und Content-Type zusammenpassen. Braucht Pillow.

Aufruf: python3 tools/archive/placeholder.py <pfad> <breite> <höhe>
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

FONTS = ['/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/Arial.ttf',
         '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf']

def font():
    for f in FONTS:
        if os.path.exists(f): return ImageFont.truetype(f, 9)
    return ImageFont.load_default()

def make(path, w, h):
    im = Image.new('RGB', (w, h), (40, 0, 0)); px = im.load()
    for y in range(h):
        for x in range(w):
            if (x + y) % 8 == 0: px[x, y] = (110, 0, 0)
    d = ImageDraw.Draw(im); f = font(); t = 'MISSING: ' + os.path.basename(path)
    bb = d.textbbox((0, 0), t, font=f)
    d.text((4, (h - (bb[3] - bb[1])) // 2 - bb[1]), t, font=f, fill=(255, 200, 200))
    d.rectangle([0, 0, w - 1, h - 1], outline=(255, 60, 60))
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    if path.lower().endswith(('.jpg', '.jpeg')):
        im.save(path, 'JPEG', quality=92, subsampling=0)
    else:
        im.convert('P', palette=Image.ADAPTIVE, colors=64).save(path, 'GIF')

if __name__ == '__main__':
    make(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

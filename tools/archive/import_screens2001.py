#!/usr/bin/env python3
"""Setzt die Screenshot-Serie vom Januar 2001 (7 Motive) ein: reflexive.net/Zax 2001 (ZSS01-07); die Archivseite der Fan-Seite zeigt sie (archive.html#screens-2001).

Die Bilder der Screenshot-Seite von reflexive.net (Images/BigScreens/ZSS01-07.jpg, 640x480) wurden nie archiviert.
Dieselbe Serie zeigte GameSpot ("First Look: Zax", 05.01.2001, zax_screen001-007.jpg); die Fassungen hier sind
logofrei aus mehreren Kopien zusammengesetzt (GameSpot-Bild, nur der Bereich des eingeblendeten Logos aus einer
anderen Kopie; Motiv 7 aus zwei Kopien ohne GameSpot-Datei; Motiv 1 behält das GameSpot-"G").
Entscheidung des Seitenbetreibers: Zuordnung GameSpot 001-007 -> ZSS01-07 (nicht belegt), die Vorschauen
ZSS01-07small.gif (150x113, nie archiviert) werden aus den großen Bildern verkleinert. Die Seiten erhalten einen
Kommentar im Quelltext.

Aufruf: python3 tools/archive/import_screens2001.py SRC   (SRC: Ordner mit zax_screen001-007.png; Pillow)
"""
import os, sys
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
VERSIONS = ['2001-01_Version1', '2001-04_Version2', '2001-12_Version3']
NOTE_BIG = ('<!-- fan-site archive: the picture of this page was never archived; it is the picture of the same series '
            'that GameSpot showed on 5 January 2001 (First Look: Zax){what}. The order of the series on this site '
            'is not known. -->')
NOTE_SMALL = ('<!-- fan-site archive: the thumbnails were never archived; they are scaled down from the pictures of the '
              'same series that GameSpot showed on 5 January 2001 (First Look: Zax), in the order of GameSpot. -->')

def what(n):
    if n == 1: return ', zax_screen001.jpg'
    if n == 7: return '; GameSpot\'s zax_screen007.jpg was never archived, so the picture is put together from two other copies without logo'
    return f', zax_screen{n:03d}.jpg, with the area of the GameSpot logo taken from another copy'

def images_dir(z):
    """Bilderordner in genau der vorhandenen Schreibweise (2001-01/-04: Images, 2001-12: images)."""
    return next(d for d in os.listdir(z) if d.lower() == 'images')

def note(path, text):
    s = open(path, encoding='ascii', newline='').read()
    if 'fan-site archive' in s: s = s[:s.index('<!-- fan-site archive')] + s[s.index('-->', s.index('<!-- fan-site archive')) + 3:].lstrip('\r\n')
    nl = '\r\n' if '\r\n' in s else '\n'
    i = s.lower().index('<head>') + len('<head>')
    open(path, 'w', encoding='ascii', newline='').write(s[:i] + nl + text + nl + s[i:].lstrip('\r\n'))

def main(src):
    for n in range(1, 8):
        im = Image.open(os.path.join(src, f'zax_screen{n:03d}.png')).convert('RGB')
        assert im.size == (640, 480), im.size
        small = im.resize((150, 113), Image.LANCZOS).quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        for v in VERSIONS:
            z = os.path.join(ROOT, 'archive', v, 'Zax')
            imgs = os.path.join(z, images_dir(z))
            im.save(os.path.join(imgs, 'BigScreens', f'ZSS{n:02d}.jpg'), quality=95, subsampling=0)
            small.save(os.path.join(imgs, 'SmallScreens', f'ZSS{n:02d}small.gif'))
            note(os.path.join(z, 'ScreenHtms', f'Screen{n}.htm'), NOTE_BIG.format(what=what(n)))
    for v in VERSIONS:
        note(os.path.join(ROOT, 'archive', v, 'Zax', 'Screens.htm'), NOTE_SMALL)
    print('ok')

if __name__ == '__main__':
    main(sys.argv[1])

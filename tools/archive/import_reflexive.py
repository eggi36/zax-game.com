#!/usr/bin/env python3
"""Baut die Fassungen 1998 und 2003 von reflexive.net/Zax aus den Funden in tools/archive/finds_src/www.reflexive.net/.

- archive/1998-12_Version0/: die erste Zax-Seite (zaxintro.html, Dezember 1998) mit ihren Bildseiten. Die zehn
  großen Bilder wurden nie archiviert; es sind die Bilder der Score-Heft-CD (archive/score_1998-11/), die Seiten
  zeigen sie mit Kommentar (Entscheidung des Seitenbetreibers).
- archive/2003-06_Version4/: reflexive.net/zax.htm (2003) mit FAQ, Characters, Weapons, Demo, French Patch und den
  Screenshot-Seiten. Die Übersicht der Screenshots (Screens.htm) war 2003 eine Fehlerseite, die Galerie-Übersicht
  nie archiviert: beides zeigt archive/missing.html.

Bilder: schon vorhandene bleiben; sonst aus dem Fundordner FOUND_IMAGES (nur beim ersten Lauf nötig), aus einer
anderen Fassung (gleicher Pfad unter Zax/), Score-CD-Bild (auch die Vorschauen von 1998, verkleinert), oder ein MISSING-Platzhalter in Originalgröße.
Bilder fremder Server werden aus einer lokalen Kopie unter archive/*/external/<Server>/ genommen.
Seitenlinks, die nicht im Archiv liegen, zeigen ins Internet Archive (Aufnahme der Startseite); nie
archivierte Rahmen zeigen archive/missing.html.

Aufruf: python3 tools/archive/import_reflexive.py [FOUND_IMAGES]   (Pillow; danach archive_entities.py,
check_links.py --fix)
"""
import glob, os, re, shutil, sys
from urllib.parse import unquote, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from placeholder import make
from PIL import Image

ARCHIVE = os.path.normpath(os.path.join(HERE, '..', '..', 'archive'))
SRC = os.path.join(HERE, 'finds_src', 'www.reflexive.net')
FOUND = os.path.join(sys.argv[1], 'archive_org', 'www.reflexive.net') if len(sys.argv) > 1 else None
found = {os.path.relpath(p, SRC).lower(): p for p in glob.glob(SRC + '/**/*', recursive=True) if os.path.isfile(p)}
if FOUND:
    found.update({os.path.relpath(p, FOUND).lower(): p for p in glob.glob(FOUND + '/**/*', recursive=True)
                  if os.path.isfile(p) and not p.lower().endswith(('.htm', '.html'))})
known = {}   # Dateien der anderen Fassungen: zax/<pfad klein> -> Datei
for v in sorted(glob.glob(os.path.join(ARCHIVE, '2001-*_Version*', 'Zax'))):
    for p in glob.glob(v + '/**/*', recursive=True):
        if os.path.isfile(p): known.setdefault('zax/' + os.path.relpath(p, v).lower(), p)
external = {}   # lokale Kopien von Bildern fremder Server: (server, dateiname) -> Datei
for p in glob.glob(os.path.join(ARCHIVE, '*', 'external', '*', '*')):
    external.setdefault((os.path.basename(os.path.dirname(p)).lower(), os.path.basename(p).lower()), p)
# Die großen Bilder der Seite von 1998 = Bilder der Score-CD (nur bei 640×480)
SCORE = {'om illustration.jpg': 'ZAX01', 'zax illustration.jpg': 'ZAX03', 'sentinel illustration.jpg': 'ZAX06',
         'the crutch.jpg': 'ZAX07', 'the zelon.jpg': 'ZAX08', 'zelon interior.jpg': 'ZAX09', 'korbo illustration.jpg': 'ZAX10',
         'screen shot of village.gif': 'ZAX02', 'screen shot in cave.gif': 'ZAX04', 'screen shot of temple.gif': 'ZAX05'}
# Die Vorschauen (380 breit, Zelon-Innenraum 330x246) daneben wurden auch nie archiviert: aus denselben Bildern verkleinert. Die breiten
# Vorschauen (380x208) zeigen nur den Bildausschnitt ohne Rand, Logo und Bildunterschrift (Zeilen 62-415).
BAND = (0, 62, 640, 416)
THUMBS = {'zax by ship illustration.jpg': ('ZAX03', BAND), 'sentinel illustration.jpg': ('ZAX06', BAND),
          'crutch illustration.jpg': ('ZAX07', BAND), 'the zelon.jpg': ('ZAX08', BAND),
          'om rendering.jpg': ('ZAX01', None), 'korbo village.jpg': ('ZAX10', None),
          'screen shot of village 380.jpg': ('ZAX02', None), 'screen shot in cave 380.jpg': ('ZAX04', None),
          'screen shot of temple 380.jpg': ('ZAX05', None), "zax's ship interior.jpg": ('ZAX09', None)}
# Screenshots von 2003, die dort nie archiviert wurden, aber als dieselbe Datei bei jowood.com liegen. Zuordnung über die
# archivierten Vorschauen (reflexive.net/Zax/images/Screen Shots/Screen Shot NNSmall.jpg, Internet Archive 2002/2003):
# mittlere Abweichung 3,6-5,3 gegenüber über 18 bei allen anderen Bildern. Bei 16 und 20 nennt die Seite 640x480,
# die jowood-Datei ist 800x600 (wird von width/height der Seite verkleinert).
JOWOOD_SS = os.path.join(ARCHIVE, 'jowood.com_2003', 'gamers', 'en', 'games', 'zax', 'ss')
SAME_PICTURE = {'screen shot 05.jpg': 'zax_1.jpg', 'screen shot 13.jpg': 'zax_6.jpg',
                'screen shot 16.jpg': 'zax_3.jpg', 'screen shot 20.jpg': 'zax_2.jpg'}
# "…" darf ' enthalten (Zax's Ship Interior.jpg), '…' darf " enthalten
LINK = re.compile(r'''(?i)\b(src|href|background)=(?:(")([^"]+)"|(')([^']+)'|()([^"'\s>]+))''')
MISSING_HTML = os.path.join(ARCHIVE, 'missing.html')

def url_path(t): return '/'.join(p.replace(' ', '%20') for p in t.split('/'))
def tag_of(m, s): return s[s.rfind('<', 0, m.start()):s.find('>', m.end())]
def size_of(m, s):
    t = tag_of(m, s); w = re.search(r'(?i)width="?(\d+)', t); h = re.search(r'(?i)height="?(\d+)', t)
    return (int(w.group(1)), int(h.group(1))) if w and h else None

def build(root, ts, start, extra=(), gone=()):
    """root: Zielordner; ts: Internet-Archive-Aufnahme für fremde Seitenlinks; gone: Seiten, die zur Zeit
    dieser Fassung Fehlerseiten waren (zeigen missing.html)."""
    todo, done = [start, *extra], set()
    while todo:
        page = todo.pop(0)
        if page.lower() in done or page.lower() not in found: continue
        done.add(page.lower())
        s = open(found[page.lower()], 'rb').read().decode('latin-1').replace('\r\n', '\n')
        base, notes = os.path.dirname(page), []
        here = os.path.dirname(os.path.join(root, page))
        def missing(target): return os.path.relpath(MISSING_HTML, here).replace(os.sep, '/') + '?' + url_path(target)
        def fix(m):
            g = m.groups(); attr = g[0]; q, url = next((g[i], g[i + 1]) for i in (1, 3, 5) if g[i + 1] is not None)
            if re.match(r'(?i)(mailto:|javascript:|#)', url): return m.group(0)
            if re.match(r'(?i)https?:', url):
                if attr.lower() == 'href': return m.group(0)
                u = urlsplit(url); copy = external.get((u.netloc.lower(), os.path.basename(u.path).lower()))
                if not copy: return m.group(0)
                dst = os.path.join(root, 'external', u.netloc.lower(), os.path.basename(copy))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.abspath(copy) != os.path.abspath(dst): shutil.copyfile(copy, dst)
                notes.append(f'local copy of {url}')
                return f'{attr}={q}{os.path.relpath(dst, here).replace(os.sep, "/")}{q}'
            target = os.path.normpath(os.path.join(base, unquote(url.split('#')[0]))).replace(os.sep, '/')
            if target.startswith('..'): return m.group(0)
            low = target.lower()
            if low.endswith(('.htm', '.html')):
                if low in gone: return f'{attr}={q}{missing(os.path.basename(target))}{q}'
                if low in found and low.startswith('zax'): todo.append(target); return m.group(0)
                if os.path.exists(os.path.join(root, target)): return m.group(0)
                if attr.lower() == 'src': return f'{attr}={q}{missing(target)}{q}'      # Rahmen
                return f'{attr}={q}https://web.archive.org/web/{ts}/http://www.reflexive.net/{url_path(target)}{q}'
            if low.endswith(('.zip', '.exe')):
                return f'{attr}={q}https://web.archive.org/web/{ts}/http://www.reflexive.net/{url_path(target)}{q}'
            dst = os.path.join(root, target)
            name = os.path.basename(low)
            if name in SCORE and size_of(m, s) == (640, 480):
                notes.append(f'the picture of this page was never archived; it is the same picture from the cover CD of Score 59 (November 1998), {SCORE[name]}.png')
                return f'{attr}={q}{os.path.relpath(os.path.join(ARCHIVE, "score_1998-11", SCORE[name] + ".png"), here).replace(os.sep, "/")}{q}'
            if name in THUMBS and size_of(m, s):
                z, box = THUMBS[name]; im = Image.open(os.path.join(ARCHIVE, 'score_1998-11', z + '.png')).convert('RGB')
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                (im.crop(box) if box else im).resize(size_of(m, s), Image.LANCZOS).save(dst, quality=92, subsampling=0)
                notes.append('the small pictures of this page were never archived; they are scaled down from the pictures of the cover CD of Score 59 (November 1998)')
                return m.group(0)
            if name in SAME_PICTURE and root.endswith('2003-06_Version4'):
                os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(os.path.join(JOWOOD_SS, SAME_PICTURE[name]), dst)
                notes.append(f'the picture of this page was never archived here; it is the same picture as jowood.com/gamers/en/games/zax/ss/{SAME_PICTURE[name]} (matched with the archived thumbnail of this site)')
                return m.group(0)
            if os.path.exists(dst): return m.group(0)
            src = found.get(low) or known.get(low)
            if src:
                os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(src, dst)
            elif size_of(m, s) and min(size_of(m, s)) >= 2:
                make(dst, *size_of(m, s))
            return m.group(0)
        s = LINK.sub(fix, s)
        if notes:
            s = s.replace('<head>', '<head>' + ''.join(f'\n<!-- fan-site archive: {n} -->' for n in dict.fromkeys(notes)), 1)
        dst = os.path.join(root, page)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'w', encoding='latin-1').write(s)
        print('page', os.path.relpath(dst, ARCHIVE))

def main():
    build(os.path.join(ARCHIVE, '1998-12_Version0'), '19990221113005', 'zax/zaxintro.html')
    build(os.path.join(ARCHIVE, '2003-06_Version4'), '20030620084750', 'zax.htm',
          ['zax/screensmain.htm', 'zax/frenchfix.htm']
          + [f'zax/screenhtms/ss{n:02d}.htm' for n in range(26)] + [f'zax/screenhtms/multiplayer {n:02d}.htm' for n in range(1, 10)],
          gone={'zax/screens.htm'})
    print('ok')

if __name__ == '__main__':
    main()

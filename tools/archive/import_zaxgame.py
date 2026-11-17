#!/usr/bin/env python3
"""Ergänzt archive/zax-game.com_2004/ um die Funde vom November 2026 (Seiten in tools/archive/finds_src/).

Quellen: www.zax-game.com (archive.org) und zax.jowood.com, JoWooD's Spiegel derselben Seite; was auf
zax-game.com nie archiviert wurde, kommt vom Spiegel (SOURCES.txt im Archivordner hält es fest).
Bilder: schon im Archiv vorhandene bleiben; sonst aus FOUND_IMAGES (Ordner mit den geladenen Bildern, nur
beim ersten Lauf nötig) oder ein MISSING-Platzhalter (tools/archive/placeholder.py) in Originalgröße.

Was das Skript an den Originalseiten ändert (mit Kommentar im Quelltext):
- nie archivierte Flash-Filme zeigen archive/missing.html?<Pfad>
- news.php/links.php heißen news_php.html/links_php.html (GitHub Pages liefert .php nicht als Seite aus);
  ihr Stil und ihre Rahmengrafiken lagen auf admin.jowood.de und zeigen auf die gleichnamigen Dateien der Seite
- die Rahmen von News & Links, Top Secret und dem deutschen Cargo Hold zeigen auf die gefundenen Seiten
- der Demo-Link der deutschen Download-Seite zeigt wie der englische ins Internet Archive

Aufruf: python3 tools/archive/import_zaxgame.py [FOUND_IMAGES]   (Pillow; danach archive_entities.py,
check_links.py --fix)
"""
import os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from placeholder import make

SRC = os.path.join(HERE, 'finds_src')
SOURCES = [os.path.join(SRC, 'www.zax-game.com'), os.path.join(SRC, 'zax.jowood.com')]   # Reihenfolge = Vorrang
OUT = os.path.join(HERE, '..', '..', 'archive', 'zax-game.com_2004')
FOUND = sys.argv[1] if len(sys.argv) > 1 else None
# Originale, die vorher Platzhalter waren (vom Spiegel); werden aus FOUND_IMAGES überschrieben
REPLACE = ['images/home_zax2.jpg', 'images/missionb_mineral.jpg', 'images/missionb_ore.jpg']
DEMO = 'https://web.archive.org/web/20041012034327/http://www.zax-game.com/demo/zaxdemo.exe'   # wie english/downloads.html

def found_image(rel):
    """Bild aus dem Fundordner (beide Quellen), oder None."""
    if not FOUND: return None
    for host in ('archive_org/www.zax-game.com', 'jowood/zax.jowood.com'):
        p = os.path.join(FOUND, host, rel)
        if os.path.exists(p): return p
    return None

def missing_flash(m, dst, depth):
    mv = re.search(r'value="?([^" >]+\.swf)', m.group(0)); wh = re.search(r'width="?(\d+)"?\s+height="?(\d+)', m.group(0))
    target = os.path.normpath(os.path.join(os.path.dirname(dst), mv.group(1)))
    if os.path.exists(target): return m.group(0)
    path = os.path.relpath(target, OUT)
    return (f'<!-- fan-site archive: {path} was never archived --><iframe src="{"../" * (depth + 1)}../missing.html?{path}" '
            f'width="{wh.group(1)}" height="{wh.group(2)}" frameborder="0" scrolling="no" title="missing: {path}"></iframe>')

def import_page(rel, src):
    dst_rel = rel.replace('.php', '_php.html')
    dst = os.path.join(OUT, dst_rel)
    depth = dst_rel.count('/') - 1
    s = open(src, 'rb').read().decode('latin-1').replace('\r\n', '\n')
    s = re.sub(r'<object.*?</object>', lambda m: missing_flash(m, dst, depth), s, flags=re.S | re.I)
    if rel.endswith('.php'):
        s = s.replace('href="zaxtext.css"', 'href="styles/zaxtext.css"')
        s = re.sub(r'(src|background)="(table_[a-z_]+\.gif)"', r'\1="../images/\2"', s)
        s = s.replace('<head>', '<head>\n<!-- fan-site archive: style sheet and frame graphics point to the files of the same name on zax-game.com -->', 1)
    if rel == 'german/downloads.html':
        s = s.replace('href="../demo/zaxdemo.exe"', f'href="{DEMO}"')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='latin-1').write(s)
    for m in re.finditer(r'<img[^>]*src="([^"]+)"[^>]*width="(\d+)"[^>]*height="(\d+)"', s, re.I):
        t = os.path.normpath(os.path.join(os.path.dirname(dst), m.group(1)))
        if os.path.exists(t): continue
        f = found_image(os.path.relpath(t, OUT))
        if f: shutil.copyfile(f, t)
        else: make(t, int(m.group(2)), int(m.group(3)))
    return dst_rel

def main():
    pages = {}
    for base in SOURCES:
        for root, _, files in os.walk(base):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), base).replace(os.sep, '/')
                if rel.startswith(('english/', 'german/')) and not f.startswith('_') and not rel.endswith('.css'):
                    pages.setdefault(rel, os.path.join(root, f))
    for rel, src in sorted(pages.items()):
        if not os.path.exists(os.path.join(OUT, rel.replace('.php', '_php.html'))):
            print('page', import_page(rel, src))
    # die leere Seite des Top-Secret-Rahmens gibt es nur auf Deutsch
    blank = os.path.join(OUT, 'english', 'blank.html')
    if not os.path.exists(blank): shutil.copyfile(os.path.join(OUT, 'german', 'blank.html'), blank)
    for rel in REPLACE:
        f = found_image(rel)
        if f: shutil.copyfile(f, os.path.join(OUT, rel))
    frames = {'english/news_and_links.html': [('../../missing.html?news_nav.html', 'news_nav.html'),
                                              ('../../missing.html?admin.jowood.de/zax/news.php', 'news_php.html')],
              'english/top_secret.html': [('../../missing.html?blank.html', 'blank.html'), ('../../missing.html?bottom_nav.html', 'bottom_nav.html')],
              'german/cargo_hold.html': [('../../missing.html?downloads.html', 'downloads.html')]}
    for rel, subs in frames.items():
        p = os.path.join(OUT, rel); s = open(p, encoding='latin-1', newline='').read()   # Zeilenenden wie im Original
        for old, new in subs: s = s.replace(f'src="{old}"', f'src="{new}"')
        open(p, 'w', encoding='latin-1', newline='').write(s)
    print('ok')

if __name__ == '__main__':
    main()

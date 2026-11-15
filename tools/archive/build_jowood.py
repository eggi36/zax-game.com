#!/usr/bin/env python3
"""Baut archive/jowood.com_2003/gamers/*.html aus den Originalseiten in tools/archive/jowood_src/.

Die Bilder, CSS- und JS-Dateien liegen bereits unter archive/jowood.com_2003/ (aus dem Internet
Archive geladen); jowood_captures.json hält fest, aus welcher Aufnahme jede Datei und Seite stammt.

Was das Skript an den Originalseiten ändert (jeweils mit Kommentar im Quelltext):
- Links zwischen den archivierten Seiten zeigen lokal aufeinander, alle anderen JoWooD-Links
  ins Internet Archive; Links auf fremde Server bleiben, wie sie waren.
- Formulare sind abgeschaltet (sie würden Daten an Server schicken, die es nicht mehr gibt).
- Nie archivierte Bilder bekommen MISSING-Platzhalter (tools/archive/placeholder.py).
- Bilder aus deutlich späteren Aufnahmen als die Seite werden im Kopf der Seite aufgelistet.
- Sonderzeichen werden zu HTML-Entities (tools/archive_entities.py).

Aufruf: python3 tools/archive/build_jowood.py   (braucht Pillow für die Platzhalter)
"""
import json, os, re, sys
from datetime import datetime
from urllib.parse import urljoin, urlsplit, parse_qsl

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'jowood_src')
OUT = os.path.join(HERE, '..', '..', 'archive', 'jowood.com_2003')
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from placeholder import make as placeholder
from archive_entities import convert, raw_pages

SITE = 'http://www.jowood.com/'
IA = 'https://web.archive.org/web/20030110210508/'
CAP = json.load(open(os.path.join(HERE, 'jowood_captures.json')))

# Quelle -> (Original-URL, lokale Datei unter gamers/)
PAGES = {
 'en_index': (SITE + 'gamers/index.php?lang=en&site=2&ScreenID=4265&GameID=zax', 'index.html'),
 **{f'en_{n}': (SITE + f'gamers/index.php?lang=en&site=2&ScreenID={n}&GameID=zax', f'zax_{n}.html') for n in (4266, 4490, 4491, 4492, 4493)},
 'en_reg54': (SITE + 'gamers/index.php?lang=en&site=3&gamenr=54', 'register_54.html'),
 **{f'en_ss{i}': (SITE + f'gamers/screenshot.php?lang=en&GameID=zax&ss={i}', f'screenshot_{i}.html') for i in range(1, 7)},
 'de_main': (SITE + 'gamers/index.php?lang=de&site=2&GameID=zax', 'index_de.html'),
 **{f'de_{n}': (SITE + f'gamers/index.php?lang=de&site=2&ScreenID={n}&GameID=zax', f'zax_de_{n}.html') for n in (345, 346, 347)},
 'de_reg19': (SITE + 'gamers/index.php?lang=de&site=3&gamenr=19', 'register_de_19.html'),
 **{f'de_ss{i}': (SITE + f'gamers/screenshot.php?lang=de&GameID=zax&ss={i}', f'screenshot_de_{i}.html') for i in range(1, 7)},
}
ALIASES = {  # weitere Adressen derselben Seiten (Sprachumschalter, Eintrag „The Game“)
 SITE + 'gamers/index.php?lang=en&site=2&GameID=zax': 'index.html',
 SITE + 'gamers/index.php?lang=de&site=2&ScreenID=344&GameID=zax': 'index_de.html',
}
# Nie archiviert: Pfad -> (Breite, Höhe, Herkunft der Größe)
MISSING = {
 'gamers/en/images/logos/gamelogo_zax.gif': (218, 60, 'unknown; column width, height estimated'),
 'gamers/de/images/logos/gamelogo_zax.gif': (218, 60, 'unknown; column width, height estimated'),
 'gamers/en/games/industrygiant2/link_industrygiant2.gif': (136, 76, 'as the other game banners'),
 'gamers/de/games/diegilde_addon/link_diegilde_addon.gif': (136, 76, 'as the other game banners'),
 'gamers/de/games/echelon/link_echelon.gif': (136, 76, 'as the other game banners'),
 **{f'gamers/en/games/zax/ss/tn_zax_{i}.jpg': (120, 90, 'as the archived thumbnail tn_zax_6.jpg') for i in range(1, 6)},
 'gamers/de/games/zax/ss/tn_zax_4.jpg': (120, 90, 'as the other archived thumbnails'),
 **{f'gamers/en/games/zax/ss/zax_{i}.jpg': (800, 600, 'as the archived German screenshots') for i in range(1, 7)},
 'gamers/de/games/zax/ss/zax_6.jpg': (800, 600, 'as the other archived screenshots'),
}
LATE_DAYS = 60   # ab so vielen Tagen nach der Seite gilt eine Bildaufnahme als „später“

def key(u):
    p = urlsplit(u.strip())
    return (p.netloc.lower().replace(':80', ''), p.path, frozenset((k, v.strip()) for k, v in parse_qsl(p.query)))
LOCAL = {key(u): f for u, f in PAGES.values()}
LOCAL.update({key(u): f for u, f in ALIASES.items()})

def day(ts): return datetime.strptime(ts[:8], '%Y%m%d')
def fmt(ts): return f'{ts[:4]}-{ts[4:6]}-{ts[6:8]}'

def resources(s, url):
    refs = re.findall(r"(?i)\b(?:src|background)=['\"]?([^'\" >]+)", s) + re.findall(r"'([^'\s]+\.(?:gif|jpg))'", s)
    out = set()
    for r in refs:
        a = urljoin(url, r)
        if a.startswith(SITE): out.add(a[len(SITE):])
    return out

def build(src, url, name):
    s = open(os.path.join(SRC, src + '.html'), 'rb').read().decode('cp1252')
    def target(u):
        if re.match(r'(?i)(javascript:|mailto:|#)', u) or u.lower().endswith(('.css', '.js')): return None
        a = urljoin(url, u.strip())
        if not a.startswith(SITE): return None
        return LOCAL.get(key(a)) or IA + a
    def link(m):
        t = target(m.group(3))
        return m.group(0) if t is None else f'{m.group(1)}={m.group(2)}{t}{m.group(2)}'
    s = re.sub(r"(?i)\b(href)=(['\"]?)([^'\">]+?)\2(?=[\s>])", link, s)
    s = re.sub(r"(?i)\b(action)=(['\"]?)([^'\" >]+)\2", link, s)
    s = re.sub(r"(?i)(<option[^>]*\bvalue)=(['\"]?)(index\.php[^'\" >]*)\2", link, s)
    s = re.sub(r"MM_openBrWindow\('(\.\./send\.php[^']*)'", lambda m: "MM_openBrWindow('" + IA + urljoin(url, m.group(1)) + "'", s)
    s, forms = re.subn(r'(?i)<form\b', '<form onsubmit="return false"', s)
    # Kopf-Kommentar: Herkunft, Formulare, fehlende und spätere Bilder
    page_ts = CAP['pages'][src]
    used = resources(s, url)
    notes = [f'fan-site archive: {url} as captured by the Internet Archive on {fmt(page_ts)}.']
    if forms: notes.append('Forms are disabled; they would send data to servers that no longer exist.')
    gone = sorted(p for p in used if p in MISSING)
    if gone: notes.append('Never archived (MISSING placeholders): ' + '; '.join(f'{p} (size {MISSING[p][2]})' for p in gone) + '.')
    late = sorted(p for p in used if p in CAP['files'] and (day(CAP['files'][p]) - day(page_ts)).days > LATE_DAYS)
    if late: notes.append('From later captures, may differ from this date: ' + '; '.join(f'{p} ({fmt(CAP["files"][p])})' for p in late) + '.')
    comment = '<!-- ' + '\n     '.join(notes) + ' -->\n'
    m = re.search(r'(?i)<html', s)
    s = s[:m.start()] + comment + s[m.start():] if m else comment + s
    path = os.path.join(OUT, 'gamers', name)
    open(path, 'wb').write(s.encode('cp1252'))
    convert(path)
    return len(gone), len(late)

if __name__ == '__main__':
    for p, (w, h, _) in MISSING.items():
        placeholder(os.path.join(OUT, p), w, h)
    for src, (url, name) in PAGES.items():
        g, l = build(src, url, name)
        print(f'{name}: {g} missing, {l} from later captures')
    lines = ['Internet Archive capture date of every file in this folder (fan-site archive).', '']
    lines += [f'{fmt(ts)}  gamers/{name}' for src, (u, name) in PAGES.items() for ts in [CAP["pages"][src]]]
    lines += [f'{fmt(ts)}  {p}' for p, ts in CAP['files'].items()]
    lines += [f'never archived  {p}  (placeholder, size {v[2]})' for p, v in MISSING.items()]
    open(os.path.join(OUT, 'CAPTURES.txt'), 'w').write('\n'.join(lines) + '\n')
    assert not [p for p in raw_pages() if 'jowood' in p]
    print('ok')

#!/usr/bin/env python3
"""Wandelt rohe Sonderzeichen in den Archivseiten in HTML-Entities um.

GitHub Pages liefert jede .htm/.html-Datei mit `charset=utf-8` aus; das schlägt das
<meta charset=iso-8859-1> der Originalseiten. Rohe Latin-1/Windows-1252-Bytes (ä, ö, ü, ß,
„ “ –) würden online als � erscheinen. Als &#NNN; sind sie in jeder Kodierung richtig.

Aufruf: python3 tools/archive_entities.py          (ändert die Dateien)
        python3 tools/archive_entities.py --check  (meldet nur, Exit-Code 1 bei Funden)
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'archive')

def pages():
    for d, _, files in os.walk(ROOT):
        for f in files:
            if f.lower().endswith(('.htm', '.html')):
                yield os.path.join(d, f)

def raw_pages():
    return [p for p in pages() if any(b > 127 for b in open(p, 'rb').read())]

def convert(path):
    data = open(path, 'rb').read()
    try:
        text = data.decode('utf-8')          # vom Fan-Projekt selbst geschriebene Seiten
    except UnicodeDecodeError:
        text = data.decode('cp1252', errors='strict')   # Originalseiten (Windows-1252 ⊃ Latin-1)
    out = ''.join(c if ord(c) < 128 else '&#%d;' % ord(c) for c in text)
    open(path, 'wb').write(out.encode('ascii'))
    return sum(1 for c in text if ord(c) >= 128)

if __name__ == '__main__':
    found = raw_pages()
    if '--check' in sys.argv:
        for p in found: print('raw non-ASCII:', os.path.relpath(p, os.path.dirname(ROOT)))
        sys.exit(1 if found else 0)
    for p in found:
        print(os.path.relpath(p, os.path.dirname(ROOT)), convert(p), 'characters')

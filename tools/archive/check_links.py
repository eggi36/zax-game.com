#!/usr/bin/env python3
"""Prüft alle Archivseiten auf lokale Verweise (src, href, background), die auf GitHub Pages ins Leere gehen.

GitHub Pages unterscheidet Groß- und Kleinschreibung, die alten Server (IIS) nicht: `Images/x.gif` und
`images/x.gif` waren dort dieselbe Datei. Mit --fix werden Verweise, die nur in der Schreibweise abweichen,
auf die tatsächliche Schreibweise der Datei gesetzt. Verweise auf fehlende Dateien werden nur gemeldet.

Aufruf: python3 tools/archive/check_links.py [--fix]
"""
import os, re, sys
from urllib.parse import unquote, quote
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'archive')
# "…" darf ' enthalten (z. B. Zax's Ship.jpg), '…' darf " enthalten, ohne Anführungszeichen bis zum Leerzeichen
LINK = re.compile(r'''(?i)\b(src|href|background|value)=(?:(")([^"]+)"|(')([^']+)'|()([^"'\s>]+))''')

def exact(path):
    """Tatsächlicher Pfad mit der Schreibweise auf der Platte, oder None."""
    parts = os.path.relpath(path, ROOT).split(os.sep); cur = ROOT; out = []
    for p in parts:
        if p == '..': return None
        try: names = os.listdir(cur)
        except NotADirectoryError: return None
        hit = p if p in names else next((n for n in names if n.lower() == p.lower()), None)
        if hit is None: return None
        out.append(hit); cur = os.path.join(cur, hit)
    return out

def main(fix):
    bad = 0
    for d, _, files in os.walk(ROOT):
        for f in files:
            if not f.lower().endswith(('.htm', '.html')): continue
            page = os.path.join(d, f); s = open(page, 'rb').read().decode('latin-1'); changed = False
            def check(m):
                nonlocal bad, changed
                g = m.groups(); attr = g[0]; q, url = next((g[i], g[i + 1]) for i in (1, 3, 5) if g[i + 1] is not None)
                if re.match(r'(?i)([a-z]+:|#|/|\?)', url) or attr.lower() == 'value' and not url.lower().endswith('.swf'): return m.group(0)
                path = unquote(url.split('#')[0].split('?')[0])
                if not path or re.search(r'[;\[\]{}]', path): return m.group(0)   # Skriptcode, kein Verweis
                target = os.path.normpath(os.path.join(d, path))
                if not os.path.abspath(target).startswith(os.path.abspath(ROOT)): return m.group(0)
                if exact(target) is None:
                    bad += 1; print(f'MISSING  {os.path.relpath(page, ROOT)}: {url}'); return m.group(0)
                # Schreibweise Teil für Teil an die Dateien anpassen; '..' und '.' bleiben, Prozentkodierung wie im Original
                cur = d; parts = []
                for part in path.split('/'):
                    if part in ('', '.', '..'):
                        parts.append(part); cur = os.path.normpath(os.path.join(cur, part or '.')); continue
                    names = os.listdir(cur); real = part if part in names else next(n for n in names if n.lower() == part.lower())
                    parts.append(real); cur = os.path.join(cur, real)
                fixed = '/'.join(parts)
                if fixed == path: return m.group(0)
                new = quote(fixed, safe="/:'()&=+,;!~*") if '%' in url else fixed
                bad += 1; print(f'CASE     {os.path.relpath(page, ROOT)}: {url} -> {new}')
                if fix: changed = True; return f'{attr}={q}{new}{q}'
                return m.group(0)
            s2 = LINK.sub(check, s)
            if changed: open(page, 'wb').write(s2.encode('latin-1'))
    return bad

if __name__ == '__main__':
    n = main('--fix' in sys.argv)
    print(f'{n} problem(s)' if n else 'all links ok')

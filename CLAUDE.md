# Zax: The Alien Hunter – Fan-Website

Statische Fan-Seite (GitHub Pages) im Stil der offiziellen zax-game.com (2002–2004).
Kommunikation mit dem Nutzer auf Deutsch; die Website selbst ist nur auf Englisch.

## Arbeitsweise
- Alle HTML-Seiten im Wurzelordner werden von `tools/gen.py` erzeugt. Nicht von Hand bearbeiten,
  sondern `tools/gen.py` ändern und `python3 tools/gen.py` ausführen (braucht Pillow).
- Menü: Liste `MENU` in `tools/gen.py` (bis zu 7 Einträge passen in den Monitor der Leiste).
  Schrift und Zeilenhöhe des Menüs skalieren mit der Zahl der Einträge (CSS `--n`), die Fläche ist immer gefüllt.
  „The Game“ (`the-game.html`) fasst Mission Briefing, Profiles, Weapons und Unused Content als Abschnitte zusammen (`GAME_SECTIONS`).
  Unused Content: Daten aus der Modellübersicht (Artefakt) in `tools/unused_environments.json`, Bilder in `assets/img/unused/environments/`.
- Logbücher: `tools/logs.json`.
- CSS/JS werden mit `?v=<Inhalts-Hash>` eingebunden (`asset()` in `tools/gen.py`), damit Browser keine alten Dateien aus dem Cache nehmen.
- Vor dem Commit die geänderten Seiten im Browser prüfen (lokal: `python3 -m http.server`).

## Aufbau
- `assets/css/zax.css` – Layout; `.navbar` (797×107) ist der Nachbau von `top_nav.swf`.
- `assets/js/nav.js` – kleiner Flash-Zeitleisten-Player + Menüverhalten:
  Bootsequenz einmal pro Sitzung (Inhalt erst danach sichtbar), Anzeige zeigt beim Überfahren
  den Menüpunkt, Klick lädt sofort, Dauer-Knistern (Sprite 64) bewusst entfernt.
- `assets/js/nav-data.js` – aus `top_nav.swf` exportierte Formen/Zeitleisten (generiert, nicht von Hand ändern).
- `assets/fonts/` – „Zelon Dots“ (Punktmatrix) und „Zelon Bold“, aus den SWF-Schriften nachgebaut;
  Bau-Skripte in `tools/fonts/`.
- `assets/snd/` – Original-Töne aus top_nav.swf (hover, typing, zap, crackle).

## Archiv (`archive/`)
- Originalseiten aus dem Internet Archive: reflexive.net/Zax (Jan/Apr/Dez 2001), zax-game.com und die Zax-Seite auf jowood.com (Jan 2003).
- Regel: nur echtes archiviertes Material. Nie archivierte Bilder bleiben als rot schraffierte
  „MISSING“-Platzhalter in Originalgröße stehen; keine selbst rekonstruierten Grafiken einfügen.
- zax-game.com: Flash läuft über Ruffle (lokal in `assets/ruffle/`) in `index_flash.html` und `*/top_nav.html`.
- Archivseiten nur in ASCII speichern: GitHub Pages sendet `charset=utf-8`, rohe Latin-1-Umlaute werden zu �.
  Nach dem Import `python3 tools/archive_entities.py`; `tools/gen.py` bricht sonst ab.
- jowood.com-Archiv: nicht von Hand ändern, sondern `tools/archive/build_jowood.py` (Quellen in `tools/archive/jowood_src/`).
  Platzhalter immer mit `tools/archive/placeholder.py` erzeugen.
- Alte zax-game.com-Adressen leitet `REDIRECTS` in `tools/gen.py` um (`index_flash.html`, `english/…`, `german/…`).
- Nichts von fremden Servern einbinden (Datenschutz). Nie archivierte Frames/Flash-Filme zeigen `archive/missing.html?<name>`.

## Projekte des Nutzers (Seite projects.html)
zax-launcher (C), zax-decomp (C++), zax-editor (Python), zax-formats (Python) – alle unter github.com/eggi36.

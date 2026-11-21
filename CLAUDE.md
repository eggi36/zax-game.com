# Zax: The Alien Hunter – Fan-Website

Statische Fan-Seite (GitHub Pages) im Stil der offiziellen zax-game.com (2002–2004).
Kommunikation mit dem Nutzer auf Deutsch; die Website selbst ist nur auf Englisch.

## Arbeitsweise
- Alle HTML-Seiten im Wurzelordner werden von `tools/gen.py` erzeugt. Nicht von Hand bearbeiten,
  sondern `tools/gen.py` ändern und `python3 tools/gen.py` ausführen (braucht Pillow).
- Menü: Liste `MENU` in `tools/gen.py` (bis zu 7 Einträge passen in den Monitor der Leiste).
  Schrift und Zeilenhöhe des Menüs skalieren mit der Zahl der Einträge (CSS `--n`), die Fläche ist immer gefüllt.
  „The Game“ (`the-game.html`) ist wie ein Handbuch gegliedert (`GAME_SECTIONS`): Overview, Story, Characters, Weapons, Interface, Screenshots, FAQ. Figuren und Waffen führen die Texte von reflexive.net (2001) und zax-game.com (2002–2004) je Eintrag zusammen.
  Unused Content (Abschnitt im Archiv, `archive.html#unused-content`): Daten aus der Modellübersicht (Artefakt) in `tools/unused_models.json` (je Kategorie), Bilder in `assets/img/unused/<kategorie>/`.
- Logbücher: `tools/logs.json`.
- `tools/gen.py` bricht ab, wenn eine erzeugte Seite auf eine Datei verweist, die es in genau dieser Schreibweise nicht gibt
  (macOS ignoriert Groß-/Kleinschreibung, GitHub Pages nicht).
- CSS/JS werden mit `?v=<Inhalts-Hash>` eingebunden (`asset()` in `tools/gen.py`), damit Browser keine alten Dateien aus dem Cache nehmen.
- Vor dem Commit die geänderten Seiten im Browser prüfen (lokal: `python3 -m http.server`).

## Aufbau
- `assets/css/zax.css` – Layout; `.navbar` (797×107) ist der Nachbau von `top_nav.swf`.
- `assets/js/nav.js` – kleiner Flash-Zeitleisten-Player + Menüverhalten:
  keine Bootsequenz (Leiste und Inhalt sofort im Endzustand), Anzeige zeigt beim Überfahren
  den Menüpunkt, Klick lädt sofort, Dauer-Knistern (Sprite 64) bewusst entfernt.
- `assets/js/cdkey.js` – CD-Key-Generator der Download-Seite (Prüfung wie in Zax.exe 0x46b540, läuft nur im Browser).
- `assets/js/nav-data.js` – aus `top_nav.swf` exportierte Formen/Zeitleisten (generiert, nicht von Hand ändern).
- `assets/fonts/` – „Zelon Dots“ (Punktmatrix) und „Zelon Bold“, aus den SWF-Schriften nachgebaut;
  Bau-Skripte in `tools/fonts/`.
- `assets/snd/` – Original-Töne aus top_nav.swf (hover, typing, zap, crackle).

## Archiv (`archive/`)
- Originalseiten aus dem Internet Archive: reflexive.net/Zax (Dez 1998, Jan/Apr/Dez 2001, 2003), zax-game.com und die Zax-Seite auf jowood.com (Jan 2003).
- Regel: nur echtes archiviertes Material. Nie archivierte Bilder bleiben als rot schraffierte
  „MISSING“-Platzhalter in Originalgröße stehen; keine selbst rekonstruierten Grafiken einfügen.
  Vom Nutzer freigegebene Ausnahmen (immer mit Herkunftskommentar `<!-- fan-site archive: … -->` in der Seite):
  dasselbe Bild von einer anderen Adresse (pixelgleich bzw. über archivierte Vorschauen belegt, z. B. jowood.com, Score-CD);
  Vorschauen, die aus einem vorhandenen großen Bild verkleinert sind; die Januar-2001-Serie ZSS01–07 (aus GameSpot-Kopien
  ohne Logo zusammengesetzt); die Multiplayer-Bilder 2003 (GameStar-Kopien derselben Aufnahmen, auf Seitengröße verkleinert und
  je Farbkanal an die archivierte Vorschau angeglichen, `GAMESTAR_MP` in `import_reflexive.py`). Nicht erlaubt bleibt: nachgezeichnete, gespiegelte oder ähnliche, aber nicht gleiche Bilder.
- zax-game.com: Flash läuft über Ruffle (lokal in `assets/ruffle/`) in `index_flash.html` und `*/top_nav.html`.
- GitHub Pages unterscheidet Groß-/Kleinschreibung, die alten Server nicht: nach Änderungen im Archiv `python3 tools/archive/check_links.py --fix`
  (Rückgabe 1 bei neuen Problemen; hingenommene Lücken in `tools/archive/known_missing.txt`).
- Funde vom Nov. 2026: Quellseiten in `tools/archive/finds_src/`; reflexive.net 1998/2003 baut `tools/archive/import_reflexive.py`,
  die neuen zax-game.com-Seiten `tools/archive/import_zaxgame.py` (nicht von Hand ändern).
- Suche nach fehlenden Archivbildern: Stand, Treffer und noch nicht geprüfte Quellen in `tools/archive/RECHERCHE.md`;
  Funde für die 2003er-Galerie mit `tools/archive/match_thumbs.py` gegen die archivierten Vorschauen prüfen.
- Screenshots ZSS01–07 (2001, auch Abschnitt `archive.html#screens-2001`): `tools/archive/import_screens2001.py` (Serie vom Jan. 2001, GameSpot; Quelle nicht im Repo).
- zax-game.com: was dort nie archiviert ist, kommt vom Spiegel zax.jowood.com (`archive/zax-game.com_2004/SOURCES.txt`).
- Archivseiten nur in ASCII speichern: GitHub Pages sendet `charset=utf-8`, rohe Latin-1-Umlaute werden zu �.
  Nach dem Import `python3 tools/archive_entities.py`; `tools/gen.py` bricht sonst ab.
- jowood.com-Archiv: nicht von Hand ändern, sondern `tools/archive/build_jowood.py` (Quellen in `tools/archive/jowood_src/`).
  Platzhalter immer mit `tools/archive/placeholder.py` erzeugen.
- Alte zax-game.com-Adressen leitet `REDIRECTS` in `tools/gen.py` um (`index_flash.html`, `english/…`, `german/…`).
- Nichts von fremden Servern einbinden (Datenschutz). Nie archivierte Frames/Flash-Filme zeigen `archive/missing.html?<name>`.

## Projekte des Nutzers (Seite projects.html)
zax-launcher (C), zax-decomp (C++), zax-editor (Python), zax-formats (Python) – alle unter github.com/eggi36.

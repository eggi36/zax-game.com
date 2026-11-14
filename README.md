# Zax: The Alien Hunter – Fan Site

Fan-Website zu *Zax: The Alien Hunter* (Reflexive Entertainment / JoWooD, 2001) im Stil der offiziellen Seite **zax-game.com**.
Statisches HTML/CSS, ein kleines Skript für die Navigation – läuft direkt auf GitHub Pages.

## Seiten
| Datei | Inhalt |
|---|---|
| `index.html` | Homepage |
| `mission-briefing.html` | Story + offizielles FAQ |
| `profiles.html` | Charaktere |
| `weapons.html` | Waffen |
| `downloads.html` | Demo-Mirrors, verlorene Dateien |
| `news-links.html`, `logs.html` | Neuigkeiten, Entwickler-Logs 2000/2001, Links |
| `projects.html` | eigene Projekte (zax-formats, zax-editor, zax-launcher, zax-decomp) |
| `archive.html`, `archive/` | die vier Original-Websites aus dem Internet Archive, nur mit archiviertem Material |

## Bearbeiten
Kopf, Menü und Fußzeile stehen in **`tools/gen.py`**, ebenso die Texte der Seiten. Nach Änderungen:
```
python3 tools/gen.py        # benötigt Python 3 + Pillow
```
Das Menü steht oben in `MENU` (Datei, Menütext, Text der Punktmatrix-Anzeige). Im Monitor der Leiste haben **höchstens 7 Einträge** Platz;
auf schmalen Bildschirmen erscheint stattdessen eine Menüzeile unter der Leiste.
Die Seiten im Ordner `archive/` werden vom Generator nicht angefasst.

Inhaltsbausteine:
```html
<div class="box"><p class="title">Überschrift</p><p>Text …</p></div>
<div class="item"><img …><h3>Name</h3><p>Text …</p></div>   <!-- in einer Box, Bild links -->
<span class="dots">Text in Punktmatrix-Schrift</span>
```

## Schriften
- **Zelon Dots** (`assets/fonts/ZelonDots.*`) – Punktmatrix-Schrift der Anzeige, aus der Flash-Navigation ausgelesen (5×5-Raster).
  Original: A–I, K–P, R–U, W, Z, &. Ergänzt: J Q V X Y, Ziffern, Satzzeichen, Ä Ö Ü ß.
- **Zelon Bold** (`assets/fonts/ZelonBold.*`) – Menüschrift, aus der Flash-Navigation ausgelesen.
  Original: A–I, K–P, R–Z, Ä, &, Komma, Punkt; ergänzt: J und Q aus U/O gebaut, Ö Ü, Ziffern und Satzzeichen nach DejaVu Sans Condensed Bold.
- Neu erzeugen: `tools/fonts/build_dotfont.py`, `tools/fonts/build_boldfont.py` (Python + fontTools; Bold zusätzlich numpy, OpenCV und DejaVu Sans Condensed Bold).

## Zu prüfen
- **Projekttexte** in `tools/gen.py` (`repos`) sind aus den Repo-Namen abgeleitet – bitte durch eigene Beschreibungen ersetzen.
- Datum unter „Site news“ anpassen.

## Herkunft und Rechte
Fan-Projekt ohne Verbindung zu den Rechteinhabern. Spielinhalte, Grafiken, Texte und Sounds © Reflexive Entertainment / JoWooD Productions bzw. deren Rechtsnachfolger.
Navigationsleiste, Rahmen, Schriften und Hover-Ton stammen aus den Originaldateien von zax-game.com; die Originalseiten wurden aus Kopien des Internet Archive rekonstruiert.
Bilder, die nie archiviert wurden, sind in den Archivseiten als rot schraffierte Platzhalter („FEHLT“) in Originalgröße markiert; selbst rekonstruierte Grafiken sind nicht enthalten. Die Flash-Dateien von zax-game.com laufen über Ruffle (per CDN von unpkg.com eingebunden; funktioniert nur online bzw. über einen Webserver, nicht per file://).

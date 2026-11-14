# Zax: The Alien Hunter – Fan Site

Fan website for *Zax: The Alien Hunter* (Reflexive Entertainment / JoWooD, 2001), in the style of the official site **zax-game.com**.
Static HTML/CSS plus a small navigation script – runs directly on GitHub Pages.

**Live:** https://zax-game.com/

## Pages
| File | Content |
|---|---|
| `index.html` | Homepage |
| `mission-briefing.html` | Story + official FAQ |
| `profiles.html` | Characters |
| `weapons.html` | Weapons |
| `downloads.html` | Demo mirrors, lost files |
| `news-links.html`, `logs.html` | News, developer logs 2000/2001, links |
| `projects.html` | Related projects (zax-formats, zax-editor, zax-launcher, zax-decomp) |
| `index_flash.html` | Redirect from the old zax-game.com start address to the homepage |
| `archive.html`, `archive/` | The original websites (reflexive.net 2001, zax-game.com 2002–2004, jowood.com 2003) from the Internet Archive, archived material only |

## Editing
Header, menu and footer live in **`tools/gen.py`**, as do the page texts. After making changes:
```
python3 tools/gen.py        # requires Python 3 + Pillow
```
The menu is defined at the top in `MENU` (file, menu label, dot-matrix display text). The monitor in the navigation bar fits **at most 7 entries**;
on narrow screens a menu row appears below the bar instead.
The pages in `archive/` are not touched by the generator.

To preview locally, run `python3 -m http.server` in the repository root (the Flash pages need a web server, not `file://`).

Content building blocks:
```html
<div class="box"><p class="title">Heading</p><p>Text …</p></div>
<div class="item"><img …><h3>Name</h3><p>Text …</p></div>   <!-- inside a box, image on the left -->
<span class="dots">Text in dot-matrix font</span>
```

## Fonts
- **Zelon Dots** (`assets/fonts/ZelonDots.*`) – dot-matrix font of the display, extracted from the Flash navigation (5×5 grid).
  Original: A–I, K–P, R–U, W, Z, &. Added: J Q V X Y, digits, punctuation, Ä Ö Ü ß.
- **Zelon Bold** (`assets/fonts/ZelonBold.*`) – menu font, extracted from the Flash navigation.
  Original: A–I, K–P, R–Z, Ä, &, comma, period; added: J and Q built from U/O, Ö Ü, digits and punctuation based on DejaVu Sans Condensed Bold.
- To rebuild: `tools/fonts/build_dotfont.py`, `tools/fonts/build_boldfont.py` (Python + fontTools; Bold additionally needs numpy, OpenCV and DejaVu Sans Condensed Bold).

## Origin and rights
Fan project with no affiliation to the rights holders. Game content, graphics, texts and sounds © Reflexive Entertainment / JoWooD Productions or their legal successors.
Navigation bar, frames, fonts and hover sound come from the original zax-game.com files; the original pages were reconstructed from Internet Archive copies.
Images that were never archived are marked in the archive pages as red-hatched "MISSING" placeholders at their original size; no self-made reconstructions of graphics are included. The zax-game.com Flash files run via Ruffle 0.7.1, bundled in `assets/ruffle/` (MIT/Apache-2.0; works only through a web server, not via `file://`). The site loads nothing from third-party servers.

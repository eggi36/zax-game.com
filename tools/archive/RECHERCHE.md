# Recherche: fehlende Archivbilder

Stand 19.11.2026 (drei Suchrunden). Hält fest, was gesucht wurde, was gefunden wurde und welche Quellen noch nicht geprüft sind.

## Screenshot-Galerie reflexive.net 2003 (`archive/2003-06_Version4/zax/images/Screen Shots/`)

Die Galerie hatte 26 Einzelspieler-Bilder (`Screen Shot 00–25.jpg`, ohne 03) und 9 Multiplayer-Bilder
(`Multiplayer01–09.jpg`), je 640×480 oder 800×600. Die Übersichtsseiten wurden nie archiviert.

### Vorschauen (Belege für die Zuordnung)

`tools/archive/finds_src/www.reflexive.net/zax/images/Screen Shots/*Small.jpg`, 150×113. 33 Vorschauen sind
gesichert; `Screen Shot 15Small.jpg` ist nur als Fehlerseite (2014) archiviert. Alle stammen aus dem Internet Archive,
Adresse `http://reflexive.net/Zax/images/Screen%20Shots/<Name>`. Die verwendeten Aufnahmen sind vom 30.12.2002,
außer diesen: 01 vom 06.05.2003, 05 und 14 vom 06.04.2003.

Abgleich: `python3 tools/archive/match_thumbs.py <Bild oder Ordner>` liefert die mittlere Abweichung zu jeder Vorschau.
- Dieselbe Datei: 3–6.
- Ein anderes Bild: über 18.

### Stand der großen Bilder

| Bild | Zustand | Quelle |
|---|---|---|
| 00, 02, 04, 07, 12, 22, Multiplayer07 | archiviert | reflexive.net |
| 05, 13, 16, 20 | eingesetzt (`import_reflexive.py`, `SAME_PICTURE`) | jowood.com `ss/zax_1`, `zax_6`, `zax_3`, `zax_2` |
| 01, 06, 08–11, 14, 15, 17–19, 21, 23–25 | fehlt | – |
| Multiplayer01–06, 08, 09 | eingesetzt, angeglichen (`import_reflexive.py`, `GAMESTAR_MP`) | gamestar.de, Galerie 52251 |

Ohne Zuordnung bleibt jowoods `zax_5.jpg` (800×600): Abweichung über 18, es ist also keins der Bilder mit erhaltener
Vorschau. Möglich wären noch 03 und 15, die keine Vorschau haben.

### Geprüft, ohne gesicherten Treffer

- **GameSpot** (`gamespot.com/pc/action/zaxthealienhunter/screenindex*.html`, Internet Archive) mit drei Serien:
  - **05.01.2001:** `screenshots/gs/news/010105/zax_screen001–007` – das ist die Januar-Serie, ZSS01–07 der Fassungen von 2001.
  - **22.08.2001:** `screenshots/gs/news/010822/zax_screen001–009`; archiviert sind nur 003–005 (640×480).
    - Sie zeigen dieselbe Szene im selben Ausschnitt wie die Vorschauen Multiplayer03, 04 und 05 (Abweichung 8,5–12,5;
      Korrelation 0,88–0,93 gegenüber 0,97–0,99 bei echten Treffern).
    - Die Bilder sind aber deutlich heller und haben das GameSpot-„G“.
    - Damit ist nicht belegt, dass es dieselbe Datei ist; sie sind nicht eingesetzt.
    - Adressen: `http://gamespot.com/gamespot/images/screenshots/gs/news/010822/zax_screen00N.jpg`
      (Aufnahmen 20020307160437, 20020227152418, 20020315094727).
  - **Oktober 2001:** `2001/pc/act/zax/zax_1002_screen001–022`; archiviert sind 001–003, 005–007, 009–011 und 015–019.
    Es gab keinen Treffer; das sind GameSpots eigene Bilder.
- **Impress Forest Watch** (forest.watch.impress.co.jp/article/2001/08/22/game145.html): 8 Bilder, 800×600. Andere Bilder.
- **gameswelt.de/zax-the-alien-hunter:** 17 Vorschauen vom August 2001. Andere Bilder.
- **gamepressure.com (GRY OnLine):** nur die Januar-Serie.
- **reflexive.net selbst:** alle archivierten Dateien unter `Zax/images/Screen Shots/` (CDX-Abfrage) sind verwendet.

- **Zweite Runde (18.11.2026), ohne Treffer:**
  - **GameSpot:** von der August-Serie sind auch unter `image.com.com` nur 003–005 archiviert; die 38 Einzelseiten
    `screens.html?page=N` zeigen die drei bekannten Serien (7 + 9 + 22). `zax_boxshot.jpg` (100×119) ist kein fehlendes Bild.
  - **IGN** (Review `pc.ign.com/articles/167/167008p1.html`): Bilder `pcmedia.ign.com/media/reviews/image/zax_sept28_*`,
    eigene Aufnahmen der Redaktion (Abweichung über 17).
  - **GameSpy** (Review `gamespy.com/reviews/october01/zax/`, Bilder 1–5): eigene Aufnahmen.
  - **jowood.com/.de/.at** (alle archivierten Bilder mit „zax“ im Namen): nur die schon verwendeten Screenshots,
    Packshots und `en/news/zax.jpg` (120×136, nicht das fehlende `news_zax.jpg` 177×236 von zax-game.com).
  - **zax-game.com und zax.jowood.com** (alle archivierten Bilder): von den fehlenden Figuren-, Waffen- und
    Produktbildern (`enemy_*`, `heroic_*`, `weapon_*`, `game_download.jpg`, `news_zax.jpg`, `links_zax.jpg`, `ss01`, `ss25`)
    ist keines archiviert, auch `ss02–24` nicht.
  - **gameswelt.de** (35 Bilder in 640×480), **pcgames.de** (Test 11/2001, 4 Bilder), **LaunchBox** (15 Bilder, meist
    Packungen und Fan-Bilder): andere Bilder.
- **Gefunden:** `reflexive.net/images/ZaxMain.jpg` (193×74, Aufnahme 2004-12-13) – dieselbe Adresse wie das fehlende Bild
  der Fassung von 2003; liegt in `finds_src/www.reflexive.net/images/` und wird von `import_reflexive.py` eingesetzt.

- **Dritte Runde (19.11.2026):**
  - **GameStar** (Galerie `gamestar.de/galerien/zax_the_alien_hunter,52251.html`, 9 Bilder, 800×600,
    `images.cgames.de/images/gamestar/4/zax-the-alien-hunter-105N_10725xx.jpg`, N = 1–9): das ist die ganze
    **Multiplayer-Reihe 01–09** derselben Aufnahmen, aber heller und in 800×600 statt 640×480.
    - Zuordnung: 1051→MP03, 1052→MP06, 1053→MP05, 1054→MP02, 1055→MP01, 1056→MP08, 1057→MP07, 1058→MP04, 1059→MP09.
    - Ohne Tonwertausgleich Abweichung 30–57; mit Ausgleich je Farbkanal 3,4–4,7, das nächstbeste Bild 8,5 oder mehr.
    - Gegenprobe mit dem archivierten `Multiplayer07.jpg` (640×480): gleiches Einzelbild (Uhr 00:05:28, gleiche Meldungen),
      Restabweichung 3,6, Korrelation 0,96.
    - Also dasselbe Bild, aber **nicht dieselbe Datei** (andere Größe und Helligkeit). Vom Nutzer als Ausnahme freigegeben
      (19.11.2026): `import_reflexive.py` verkleinert auf 640×480 und gleicht jedes Bild je Farbkanal an seine archivierte
      Vorschau an (Kurve aus den 150×113-Pixeln, geglättet, monoton). Probe am echten Multiplayer07: Abweichung 4,4 statt 39.
      Quellen in `finds_src/images.cgames.de/`. Das erklärt auch die helleren GameSpot-Bilder vom August 2001 (MP03–05).
  - **4Gamer.net** (Review `4gamer.net/review/live/zax.html`, `img/zax/zax01–09.jpg`, 800×600): eigene Aufnahmen der
    japanischen Fassung (Abweichung über 31).
  - **MobyGames** (Spiel-ID 5954): Live-Seite hinter Cloudflare, auch von Hand nicht passierbar. Über das Internet Archive:
    13 Nutzer-Screenshots (587×440, `cdn.mobygames.com/<id>.webp`) ohne Treffer; die Promo-Gruppe enthält nur
    Zeitschriftenanzeigen (CD-Action, NextGen, PC Games).
  - **Eurogamer** (Review `eurogamer.net/r-zax`, 4 Bilder, 800×600): eigene Aufnahmen.
  - **spaziogames.it** (Review): keine Zax-Bilder. **4players.de, pcaction.de:** keine Zax-Bilder im Internet Archive
    (pcaction nur der Demo-Download), keine Galerie live gefunden.
  - **Vom Nutzer gefunden (19.11.2026, Quelle nicht im Repo):** zwei Fassungen der Januar-Serie 2001 in 600×450.
    - Eine entspricht ZSS05 (Abweichung 1,4), die andere ZSS04 (2,7). Es ist jeweils dasselbe Einzelbild, aber mit anderer
      Anzeige unten rechts: ZSS05 ohne den Munitionszähler „27“, ZSS04 ohne den blauen Balken und mit verschobenem Waffensymbol.
    - Genau dort liegt in unseren Fassungen das aus einer anderen GameSpot-Kopie eingesetzte Stück (Logo-Bereich). Es gab
      also zwei veröffentlichte Fassungen dieser Bilder; welche reflexive.net zeigte, ist ohne archivierte Vorschau nicht
      zu entscheiden. Kleiner und nicht dieselbe Datei: nicht eingesetzt.

### Noch nicht geprüft

- **MobyGames live** (falls die Cloudflare-Prüfung einmal durchgeht): große Fassungen der Nutzer-Screenshots.
- **Hinweis zur CDX-Abfrage:** eckige Klammern im Filter müssen kodiert werden (`filter=original:.*%5BZz%5Dax.*`),
  sonst kommt stillschweigend eine leere Liste zurück.

## Navigation reflexive.net April 2001 (Hover-Bilder `*2.gif` und Randstücke)

Die Navigation vom Dezember 2001 ist dasselbe Motiv, aber neu gerendert, kleiner und anders angeordnet; sie ist nicht
gespiegelt. Ein Pixelvergleich der Kugeln ergibt eine mittlere Abweichung von 12–29, also keine gleichen Pixel.
Ohne Nachbau ist das nicht wiederherzustellen.

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

## Japanische Vollversion (Downloads-Seite)

Gesucht am 20.11.2026, ohne Download-Fund.
- **Titel:** 「ザックス 〜エイリアンハンター〜 完全日本語版」 (4Gamer: „ZAX ～エイリアンハンター～ 完全日本語版“).
- **Verlag:** Media Quest (メディアクエスト, auch „Kids Station“). Erschienen am 13.12.2001, 8800 Yen (mit Steuer 9240 Yen).
- **Belege:** die Kritik `4gamer.net/review/live/zax.html` vom 12.01.2002. Impress Forest Watch schrieb am 15.08.2001 noch,
  dass keine japanische Fassung angekündigt sei.
- **Geprüft, ohne Treffer:**
  - Internet Archive, Suche nach „zax“ mit japanisch/jpn, ザックス, エイリアンハンター, メディアクエスト und mediaquest.
    Andere Media-Quest-Titel liegen dort im Namensschema `(Win)(Media Quest, …)(JP)(ja)`, Zax nicht.
  - Websuche (englisch und japanisch), Zomb's Lair, MyAbandonware.
- **Händler und Auktionen (Stand 20.11.2026):**
  - **Amazon.co.jp:** ASIN B00005REZ0, Marke マイピック (MyPick), Artikelnummer **MJD-1090**, erschienen 2001/12/13.
    Derzeit nicht erhältlich, auch kein Marketplace-Angebot.
  - **Mercari:** ein Exemplar vom Shop Suruga-ya, gebraucht für 3450 Yen, ausverkauft. Laut Anzeige für Windows
    95/98/Me/2000/XP; die Seriennummer steht auf der CD-Hülle.
  - **Yahoo! Auctions** (über Buyee, aus der EU gesperrt): kein Angebot.
  - **Suruga-ya direkt:** hinter einer Cloudflare-Prüfung; dort nach „MJD-1090“ suchen.
  - **Ergebnis:** weder neu noch als Download erhältlich, nur gebraucht. Im Internet Archive und bei Zomb's Lair
    gibt es nur die englische Fassung.
- **Noch offen:** Suruga-ya direkt. Für die Downloads-Seite gibt es ohne Download nichts zu verlinken.

## Brasilianische und taiwanesische Fassung (Downloads-Seite)

Gesucht am 20.11.2026, ohne Download-Fund.
- **Brasilien:** Die Fassung gab es.
  - Titel „Zax: O Caçador de Alienígenas“, Verlag JoWooD, Vertrieb Infogrames do Brasil Ltda., 2002 (MobyGames, Releases;
    der dort genannte 23.11.2001 gehört zur russischen Ausgabe von Russobit-M), Box, EAN 7898172881199.
  - Belege: MobyGames-Seiten Releases und Covers (über das Internet Archive) sowie GameFAQs.
  - MobyGames hat Scans von Box, Medium und Handbuch; die Credits nennen eine Übersetzung und das Team von Infogrames Brasil.
    **Sprache (geklärt 20.11.2026 an den Packungsbildern bei MobyGames): Spiel englisch, nur das Handbuch portugiesisch.**
    Unterseite der Box: „Conteúdo: 01 CD-ROM / Software em inglês – 01 Manual em português“ und rot
    „É necessário proficiência no idioma inglês para a correta utilização deste produto“; Rückseite mit dem Siegel
    „Manual em português / Software em inglês“. Hersteller der Box Videolar (Barueri), Herausgeber Infogrames do Brasil.
    Die CD trägt dieselbe Nummer wie die britische (`ROZAX00003LAB`).
  - Im Internet Archive gibt es keine Fassung auf Portugiesisch (Suche nach Titel, Sprache por, brasil/brazil).
- **Taiwan:** angekündigt, aber keine Veröffentlichung belegt.
  - Die Reflexive-News nennen die Fassung als in Arbeit:
    - 17.10.2001: „Zax is also currently being translated into Japanese and Taiwanese“
      (`archive/2001-12_Version3/Frames/Archived News/10-01.htm`);
    - 01.11.2001: Japanese, Taiwanese, Polish, French, Spanish;
    - 21.11.2001: zusätzlich Russian und Chinese (`archive/2001-12_Version3/News.htm`).
  - Alle anderen Fassungen dieser Liste sind erschienen, die taiwanesische nicht nachweisbar.
  - Ohne Treffer gesucht wurde so:
    - Websuche nach 異形獵人, Bahamut und üblichen Verlagen (第三波, 英特衛, 松崗, 美商藝電).
    - Internet Archive.
    - MobyGames: listet keine Veröffentlichung in Taiwan.
    - Alle chinesischen Quellen beziehen sich auf die vereinfachte chinesische Fassung (archive.org `ZTAHChs`).
  - Möglicher Rest der Arbeit: In der vereinfachten chinesischen Fassung stehen drei Menütexte in Langzeichen, und
    `Multiplayer.RDS` besteht aus GBK-Bytes, die als Big5 gelesen wurden (zax-packs `chinese/INFO.txt`).

## Polnische Fassung im Handel (20.11.2026)

- **Veröffentlichungen** (MobyGames, gry-online.pl, dubbingpedia.pl):
  - Handel: „Zax: Galaktyczny Wojownik“, Übersetzung und Vertrieb CD Projekt, 49,90 zł, Datum unsicher:
    MobyGames nennt den 12.12.2002, gry-online den 12.12.2001. Die Reflexive-News vom 21.11.2001 führen Polnisch noch
    als in Arbeit; beide Daten sind damit möglich. Synchronisation von Start International Polska;
    Zelon wird von Agnieszka Kunikowska gesprochen.
  - Billig-Ausgabe „Tanie Granie“ (28.02.2003).
  - Beilage zu Świat Gier Komputerowych 10/2002 (Vertrieb Egmont).
- **Vollversionen in Zeitschriften** (zapach-papieru.pl, Baza gier z czasopism): „Zax: Galaktyczny wojownik“ in
  Komputer Świat GRY 20 und CD-Action 71; „Zax: The Alien Hunter“ in CDA 67, CDA 70 und GK 83 (vermutlich Demos).
- **Internet Archive:**
  - `zax_20210926` (unser polnischer Link) ist die Beilage zu Komputer Świat Gry 04/2004 mit Freischaltcode,
    nicht die Ausgabe aus dem Handel.
  - `cdrom-cdaction-71` und `-71-2`: Auf beiden CDs ist kein Zax; die Vollversion lag wohl auf einer dritten,
    nicht archivierten CD.
  - `play-07-2004-cd-3` („Zax & Beach Volley“, Zeitschrift Play 07/2004, Vollversion; Sprache ungeprüft).
  - Ein Abbild der CD-Projekt-Ausgabe aus dem Handel ist nicht archiviert (Suche nach Titel, Sprache pol, CD Projekt,
    Tanie Granie).

## Weitere Hinweise auf Sprachfassungen (20.11.2026)

- **Reflexive-News 2001** (`archive/2001-12_Version3/`): genannt werden nur Fassungen, die Reflexive selbst übersetzen
  ließ (Vermutung). Deutsch fehlt vermutlich, weil JoWooD (Österreich) die deutsche Fassung selbst machte; sie erschien
  schon am 28.09.2001, also vor den Meldungen.
- **zax-game.com 2004:** nur Englisch und Deutsch als Sprachen der Seite, dazu der Patch für die französische Fassung.
- **Exe der chinesischen Fassung (Build 1314):** voreingestellte Schrift `MSGOTHIC.TTC` / „MS UI Gothic“, also japanisch
  (zax-decomp `docs/EXE_FINDINGS.md`, `CUnicodeTrueTypeFontInfo`). Die Unicode-Fassung des Programms stammt also
  wahrscheinlich aus der japanischen Übersetzung. Die Exes der anderen Fassungen nennen keine Sprachen.
- **MobyGames, Packungen** (Covers-Seite über das Internet Archive, Vorschaubilder direkt von `cdn.mobygames.com`):
  USA, Großbritannien, Deutschland (dazu Oranzzsoft-Budget), Brasilien, Russland, Polen, Italien und der JoWooD-Shop.
  - **Italien:** Keep Case, Rückseite auf Italienisch, „Exclusively distributed in Italy by Koch Media“.
    Die CD ist nur englisch beschriftet („Made in EU“).
    - EAN 9006113065036 (Rückseite). Die Websuche nach der EAN ergab nichts.
    - Auf den CD-Bildern bei MobyGames hat die CD dieselbe Gestaltung wie die anderen JoWooD-CDs, aber eine eigene Nummer:
      Italien anscheinend `ROZAX00006LAB`, Großbritannien `ROZAX00003LAB`, Deutschland (beide Ausgaben) `ROZAX00004LAB`.
      Die Nummern sind aus kleinen Bildern abgelesen; die deutsche CD mit deutschen Daten trägt eine eigene Nummer.
      Wofür die eigene Nummer steht (anderes Presswerk, anderer Build, zusätzliche Dateien wie ein italienisches
      Handbuch als PDF?), ist offen. Laut spaziogames ist das Spiel selbst englisch; den Inhalt der CD prüft das bestellte Exemplar.
    - **Sprache: Englisch.** Die Kritik bei spaziogames in der Fassung vom 27.03.2009 (Internet Archive,
      `spaziogames.it/recensioni_videogiochi/console_pc/645/zax-the-alien-hunter.aspx`) nennt im Infokasten
      „Distributore: Koch Media – Versione: Europea – Lingua: Inglese“. Die heutige Fassung der Seite hat den Kasten nicht mehr.
    - Ein Exemplar ist bestellt (Stand 20.11.2026); daran Handbuch und CD-Inhalt prüfen.
    - Sonst gibt es keine Belege. Gesucht wurde im Internet Archive (Sprache ita, italiano/italia, italienische Zeitschriften)
      und im Netz (Koch Media, „in italiano“, Kritiken).
    - multiplayer.it (Kritik vom 30.09.2001, `multiplayer.it/recensioni/zax-the-alien-hunter.html`, 13 Bilder 640×480 unter
      `multiplayer.net-cdn.it/images/2001/09/30/199NN.zax.*.jpg`): nur 19928 passt zu einer Vorschau (Screen Shot 20, 3,3),
      und das ist schon eingesetzt; die übrigen liegen über 18.
  - **Brasilien:** englisches Spiel mit portugiesischem Handbuch, Vertrieb Infogrames (siehe oben).
- **Tschechisch:** keine Ausgabe im Handel, sondern eine Übersetzung von Fans aus dem Jahr 2004 (zax-packs `czech`).
  Das Spiel lag als Vollversion der Score-CD 114 bei (August 2003). Quelle: archive.org `score114cd`, Beschreibung
  „Plná hra Zax the Alien Hunter“. Laut dem mitgelieferten Abbild-Protokoll (`*_cd2_volDesc.txt`) heißt die zweite CD
  „Zax“ und enthält einen InstallShield-Installer (`SETUP.EXE`, `DATA1.CAB`, `DATA2.CAB`, `DATA.EXE`) sowie das Handbuch
  als PDF (`ZAX_MA~1.PDF`). Geprüft am 20.11.2026: Das Spiel ist die englische Fassung, nur das Handbuch
  ist tschechisch.
- **Bekannte Fassungen damit:**
  - übersetzt erschienen: Englisch, Deutsch, Französisch, Spanisch, Polnisch, Russisch, Chinesisch (vereinfacht), Japanisch;
  - englisches Spiel in eigener Packung (Handbuch übersetzt oder vermutlich übersetzt): Brasilien, Italien (Handbuch
    noch zu prüfen);
  - englisches Spiel als Heft-Beilage mit übersetztem Handbuch: Tschechien (Score-CD 114);
  - angekündigt, aber nicht nachgewiesen: Taiwan (Langzeichen).

## Navigation reflexive.net April 2001 (Hover-Bilder `*2.gif` und Randstücke)

Die Navigation vom Dezember 2001 ist dasselbe Motiv, aber neu gerendert, kleiner und anders angeordnet; sie ist nicht
gespiegelt. Ein Pixelvergleich der Kugeln ergibt eine mittlere Abweichung von 12–29, also keine gleichen Pixel.
Ohne Nachbau ist das nicht wiederherzustellen.

#!/usr/bin/env python3
"""Erzeugt die Zax-Fan-Website (Stil zax-game.com). Inhalte stehen in diesem Skript bzw. in logs.json.
Aufruf: python3 tools/gen.py   -> schreibt die HTML-Seiten ins Repo-Verzeichnis"""
import json, html, os, re
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Repo-Wurzel

# Menü im Monitor (max. 7 Einträge). (Datei, Menütext, Text für die Punktmatrix-Anzeige)
MENU = [
    ('the-game.html',         'The Game',         'The Game'),
    ('downloads.html',        'Downloads',        'Downloads'),
    ('news-links.html',       'News & Links',     'News & Links'),
    ('projects.html',         'Projects',         'Projects'),
    ('archive.html',          'Archive',          'Archive'),
    ('sitemap.html',          'Sitemap',          'Sitemap'),
]

import hashlib
def asset(path):
    """Pfad mit Inhalts-Kennung (?v=…), damit Browser nach Änderungen nicht die alte Datei aus dem Cache nehmen."""
    return path + '?v=' + hashlib.sha1(open(os.path.join(SITE, path), 'rb').read()).hexdigest()[:10]

def img(src, alt='', cls=None):
    w, h = Image.open(os.path.join(SITE, src)).size
    c = f' class="{cls}"' if cls else ''
    return f'<img src="{src}" width="{w}" height="{h}" alt="{html.escape(alt)}"{c}>'

def page(filename, display, title, body, current=None):
    items = ''
    for href, label, disp in MENU:
        cur = ' aria-current="page"' if href == current else ''
        items += (f'      <li><a href="{href}" data-label="{html.escape(disp)}"{cur}>'
                  f'<img class="cursor" src="assets/ui/cursor.svg" alt="">{html.escape(label)}</a></li>\n')
    mobile = ' '.join(f'<a href="{href}"' + (' aria-current="page"' if href == current else '') + f'>{html.escape(label)}</a>' for href, label, disp in [('index.html','Home','Homepage')] + MENU)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} – Zax: The Alien Hunter</title>
<link rel="stylesheet" href="{asset('assets/css/zax.css')}">
<script>(function(){{try{{if(sessionStorage.getItem('zaxBooted')!=='1'&&!matchMedia('(prefers-reduced-motion: reduce)').matches){{var d=document.documentElement;d.classList.add('zax-boot');setTimeout(function(){{d.classList.remove('zax-boot');}},10000);}}}}catch(e){{}}}})();</script>
</head>
<body>
<div class="page">
<div class="navbar-wrap">
  <nav class="navbar" aria-label="Main menu">
    <a class="home-link" href="index.html" data-label="Homepage" aria-label="Homepage"></a>
    <h1 class="display"><span class="page-text">{html.escape(display)}</span></h1>
    <ul class="menu" style="--n:{len(MENU)}">
{items}    </ul>
  </nav>
</div>
<nav class="mobile-menu" aria-label="Menu">{mobile}</nav>
<main>
{body}
</main>
<footer>
  Fan project – not affiliated with the rights holders. Zax: The Alien Hunter &copy; 2001 Reflexive Entertainment / JoWooD Productions.
  All trademarks and original material belong to their respective owners.<br>
  Design based on the official site zax-game.com (2001–2004), rebuilt from copies at the <a href="https://web.archive.org/">Internet Archive</a>.<br>
  <button type="button" class="sound-toggle" hidden>Sound: on</button>
</footer>
</div>
<script src="{asset('assets/js/nav-data.js')}"></script>
<script src="{asset('assets/js/nav.js')}"></script>
</body>
</html>
'''
    open(os.path.join(SITE, filename), 'w', encoding='utf-8').write(doc)

def box(inner, title=None, id=None):
    t = f'  <p class="title">{title}</p>\n' if title else ''
    i = f' id="{id}"' if id else ''
    return f'<div class="box"{i}>\n{t}{inner}\n</div>'

def row(side, content):
    return f'<div class="row">\n  <div class="side">{side}</div>\n  <div class="content">\n{content}\n  </div>\n</div>'

def ps(*paras):
    return '\n'.join(f'  <p>{p}</p>' for p in paras)

# ---------------------------------------------------------------- Homepage
home = row(img('assets/img/missionb_zelon.jpg', 'Zelon'), box(ps(
    'Welcome to a fan site for <b>Zax: The Alien Hunter</b>, the isometric action adventure by Reflexive Entertainment, published by JoWooD Productions in 2001.',
    'The look of this site is rebuilt from the official zax-game.com – the navigation bar, the fonts of Zelon\'s ship computer and the blue frames are taken from the original files. The original websites themselves can be visited in the <a href="archive.html">Archive</a>.',
    'Besides the game information you will find my own <a href="projects.html">projects</a> around the game: tools for the file formats, a level editor, a launcher and a decompilation project.'), 'Welcome, hunter'))
home += '\n' + row(img('assets/img/missionb_zax.jpg', 'Zax'), box(ps(
    '"Zax – The Alien Hunter" is a futuristic explorer on a solitary mission of wealth acquisition when he crash lands on a hostile, uncharted planet. With his ship suffering from rampant system failures due to the crash, Zax has no choice but to try and navigate this backwater world until he can acquire the necessary resources to repair his ship and escape with his life.',
    'With no military training and only his wit and determination to sustain him, Zax relies heavily on the help of his ship\'s artificial intelligence, Zelon, to serve as his second set of eyes and ears and to supply him with the items he needs to survive.',
    'He soon discovers that this is a place of ancient religion and wondrous magic and that he has but one potential ally – a downtrodden race that is desperate for help themselves. These people, known as the Korbo, live in a primitive agrarian society and worship an angry god.',
    'A powerful and terrifying god that walks among them.',
    'A god that is very unhappy with Zax\'s presence.'), 'You\'re in for the adventure of your life…'))
home += '\n' + box('''  <div class="credits">
    <div>Developed by<a href="https://web.archive.org/web/2001/http://www.reflexive.net/">''' + img('assets/img/reflexive_logo.gif', 'Reflexive Entertainment') + '''</a></div>
    <div>Published by<a href="https://web.archive.org/web/2002/http://www.jowood.com/">''' + img('assets/img/jowood_logo.gif', 'JoWooD Productions') + '''</a></div>
  </div>''')
page('index.html', 'Homepage', 'Homepage', home)

# ---------------------------------------------------------------- Mission Briefing
story = [
 ('assets/img/missionb_zax.jpg', 'Zax', 'Story', [
  'Caranthian Ore and Crystals were once common commodities. Now they are the most rare, precious and priceless substances in existence. They were the foundation of a fortune, the life blood of an economy and a lifelong obsession.',
  'As a youth, Zax had listened with interest in history class about the year his society changed forever – the year that the pioneer Oleus Caranth journeyed to a nearby planet.',
  'There Caranth found a staggering concentration of minerals he called Caranthian Ore and Crystals. He discovered that the unique molecular structure of these minerals made them perfect for use in Materials Generators – machines that converted raw materials into other more useful objects.',
  'Whereas most minerals could only produce a few rudimentary objects, Caranthian Ore could be converted into virtually anything imaginable. His discovery soon became an integral part of daily life and made him a very wealthy man.',
  'The Ore and Crystals were in such demand that Oleus\' company, Oleus Mining, soon strip-mined the nearby planet of all obtainable ore.']),
 (None, None, None, [
  'A devastating economic depression resulted when the Ore supply dwindled and its price began to skyrocket. Oleus Mining sent out several new ships to the reaches of space to find more ore, but none ever returned. As the society slowly returned to using other minerals in their materials generators and toward a more traditional economy, Caranthian Ore became exorbitantly valuable and a symbol of the “Good Old Days”. It became so rare that it was virtually priceless.',
  'Zax grew up at the tail end of this 40-year depression dreaming about being the next Oleus Caranth. His lifelong ambition was to explore the universe and seek his fortune exactly the way Caranth had. Others had tried and failed of course, but Zax knew that he would be different.']),
 ('assets/img/missionb_zelon.jpg', 'Zelon', None, [
  'He had tasted poverty enough to know that he hated it. He had never known wealth, but its allure was all encompassing to him. So he worked long and hard to acquire his very own space ship. The one he finally found was veteran of other failed explorer missions. It was old, beat up, and nothing to brag about – but it was for sale. He bought it, fixed it up the best he could, and named it “Zelon” after a famous actress from the “Good Old Days” who once had a ‘relationship’ with Oleus Caranth.',
  'Zelon\'s best feature was its commonplace, but very sophisticated, onboard artificial intelligence. The AI was capable of thinking, performing research, and had a rudimentary personality. Zax reprogrammed its speaking voice to be that of the real life Zelon, or “Babe”, as Caranth had called his mistress.',
  'Finally, when the onboard materials generator was repaired, Zax set off to make his dream a reality. He knew there was more Caranthian Ore out there somewhere, and he would find it.',
  'Ten long years later, he was about to set down on what he thought was an uncharted and unclaimed planet in deep space.']),
]
mb = ''
for src, alt, title, paras in story:
    b = box(ps(*paras), title)
    mb += (row(img(src, alt), b) if src else row('<div style="width:177px"></div>', b)) + '\n'
faq = [
 ('What kind of game is Zax: The Alien Hunter?', 'Zax: The Alien Hunter is an Action / Adventure game, with heavy emphasis on the action. We have spent a great deal of time and effort making sure that the player always has a goal and plenty of enemies to deal with. The adventure side comes in with an involving storyline that unfolds over one hundred maps.'),
 ('How many missions does Zax: The Alien Hunter have?', 'There are 22 missions in the game. Many of these missions have several maps, which means that some of the missions can be completed in a non-linear fashion. That is, what you choose to do first in a given scenario, impacts which order you finish the missions.'),
 ('Is there multi-player in Zax: The Alien Hunter?', 'Yes, Zax has multiplayer capabilities. Death Match, Capture The Flag, and our new addition to multi-player called Salvage King, which is our company favorite!'),
 ('Will Zax: The Alien Hunter ship with a level editor?', 'There are no plans to ship any of the developing tools with Zax.'),
 ('Is there a story in Zax: The Alien Hunter, or is it just kill all the bad guys?', 'There is a very compelling story that drives the player throughout the game. We have spent a lot of time developing and scripting special events throughout the game to facilitate telling the story to the player. At the same time, we have tried not to overwhelm the player with a billion sub-plots.'),
 ('What are the minimum specs?', 'Pentium II 233 compatible processor with 32 megs of RAM. Of course if you have a faster machine with more RAM, we won\'t complain.'),
 ('Can Zax: The Alien Hunter be played over the Internet?', 'Yes, Zax is playable over the internet. We are estimating a maximum of 16 players per game. However, that will depend on the system specs of the machine running the server.'),
 ('Is it fun?', 'It rocks! We think it\'ll keep you in front of your PC for hours at a time just so you can see what happens around the next corner. (and there are a lot of corners!)'),
]
mb += box('  <p class="small">From the official FAQ by Reflexive Entertainment (2001). Note: the Zax CD-Key is found on the back of the jewel case, not the back of the manual as indicated in the manual.</p>\n  <dl class="faq">\n' +
          ''.join(f'    <dt>{q}</dt><dd>{a}</dd>\n' for q, a in faq) + '  </dl>', 'Frequently asked questions')

# ---------------------------------------------------------------- Profiles
chars = [
 ('zax.jpg', 'Zax', 'Rollin Triskin “Zax”: Born 2318 son of Tallis and Marion Triskin. His parents, fearing that they would not be able to get him out of the system, were forced to place him with his uncle. They hugged their boy and promised they would come for him as soon as they could. Months turned into years and the years turned into his life. Zax never saw or heard from his parents again.'),
 ('cave_dweller.jpg', 'Cave Dweller', 'This soft-shelled four-legged arachnid resides deep in the wet caverns of LV-42-3. Though very slow moving, they can kill enemy and prey alike with the venomous spray shot from their mouths.'),
 ('jungle_creature.jpg', 'Jungle Creature', 'These creatures can usually be found in packs throughout the jungle regions. These speedy two-legged beasts use their powerful jaws to feast upon the native wild boar and any unsuspecting Korbo.'),
 ('higher_orb_slayer.jpg', 'Higher Orb Slayer', 'These Bots are like their lower counterparts but with one exception. The Higher Orb Slayer wields a more powerful orb that is fired from a cannon on its right arm.'),
 ('oversier.jpg', 'Lord Om Overseers', 'Lord Overseers are similar to Master Overseers but do not take part in the daily routines of the Korbo slave camps. Their job is to serve the needs of Om. Lords can be found mostly near the inner chambers of the facilities to which Om itself resides. They are darker in color than the Masters and pack a much more powerful projectile. A Companion Drone is usually found with these evil Bots.'),
 ('parascope.jpg', 'Master Om Overseers', 'These highly intelligent Bots are the right hand of Om. Master Overseers control other Bots and coordinate their activities in gathering resources for the construction of facilities. Their other purpose involves the gathering and enslaving of Korbo. Master Overseers are equipped with shields and a powerful right gun.'),
 ('rogcoil.jpg', 'Rogcoil', 'These Cyborg are lightly armed and are directly controlled by Om. Rogcoil often patrol in groups. They can be seen around Korbo villages, herding the Korbo to their doom. Although they are not heavily armored, they can still put up a fight and are extremely effective at intimidating the Korbo.'),
 ('scorpio.jpg', 'Scorpio Flyer', 'The Scorpio Flyer is a larger Bot that hovers about a foot over the ground. These Bots can be found near Om\'s strongholds to fend off large groups of Korbo rebels. They are equipped with large lasers and an energy grenade thrower.'),
]
pr = box('\n'.join(f'  <div class="item">{img("assets/img/profiles/"+f, n)}<h3>{n}</h3><p>{t}</p></div>' for f, n, t in chars),
         'Profiles')

# ---------------------------------------------------------------- Weapons
weapons = [
 ('light_pistol_ill.gif', 'Light Pistol', 'This pistol is the standard emergency weapon that Crater carries in his boot holster or has strapped under his seat. Its small, tough frame has been proven time and again to be ideal in dealing with surprise problems – though it is typically used as a backup when the regular primary weapon has been disabled. Although its disruptive power is actually weaker than that of the Modified Laser Welder, the laser blast emitted from the Light Pistol has a far greater range.'),
 ('twin_disruptor_ill.gif', 'Twin Disrupter', 'This weapon has twin-mounted disruptive lasers that feed asynchronously off of the power source, reducing the power leakage and increasing the damage potential. It provides a good punch for the Mega-Joule usage.'),
 ('full_auto_pistol.gif', 'Full Automatic Pistol', 'This weapon fires slugs at an ungodly rate, reducing the enemies in front of it to pieces. However, it uses bullets like there is no tomorrow, and should only be used in the most dire of situations or when a bullet stockpile has just been located. Blocked by: the Inertia shield.'),
 ('impaction_cannon.jpg', 'Impaction Cannon', 'A weapon of untested strength and power, the Impaction Cannon is a mish-mash of ancient alien technology and Imperium ingenuity. It emits a highly focused laser pulse surrounded by a phase-dampened sub-nuclear envelope, perfect for punching through albedo shields and robotic matter. Its Mega-Joule cost is very high, but the show is well worth the wait.'),
 ('tri_gun_detail.jpg', 'Tri-Spread Gun', 'This is the level 3 version of the Light Pistol. The only difference other than doing more damage is that the Tri-Spread gun emits 3 lasers. Blocked by: the Albedo shield.'),
 ('nucleardisbeauty.jpg', 'Autonomous Nuclear Disrupter', 'This large weapon spits forth a translucent, glowing cloud that emits massively duped electrons at enemy targets. What makes this weapon especially devastating is the intelligence that the cloud exhibits. It follows its target through hallways and around corners until it consumes itself or its target. The cloud does move slowly, so if the target runs away (and keeps running) the cloud (perhaps) can be avoided.'),
]
wp = box('\n'.join(f'  <div class="item">{img("assets/img/weapons/"+f, n)}<h3>{n}</h3><p>{t}</p></div>' for f, n, t in weapons)
         + '\n  <p class="small">“Crater” in the first description was the working name of the hero during development.</p>', 'Weapons')

# ---------------------------------------------------------------- The Game (Mission Briefing, Profiles, Weapons)
GAME_SECTIONS = [('mission-briefing', 'Mission Briefing', mb), ('profiles', 'Profiles', pr), ('weapons', 'Weapons', wp)]
game = '<nav class="subnav" aria-label="The Game">' + ''.join(f'<a href="#{a}">{html.escape(t)}</a>' for a, t, _ in GAME_SECTIONS) + '</nav>\n'
game += '\n'.join(f'<section id="{a}" aria-labelledby="{a}-h">\n<h2 class="section-title" id="{a}-h"><span class="dots">{html.escape(t)}</span></h2>\n{body}\n</section>'
                  for a, t, body in GAME_SECTIONS)
page('the-game.html', 'The Game', 'The Game', game, 'the-game.html')

# ---------------------------------------------------------------- Downloads
REL = 'https://github.com/eggi36/zax-game.com/releases/download/downloads/'
# Dateigrößen aus dem Release lesen (GitHub-API); offline gilt der zuletzt gespeicherte Stand.
SIZES_CACHE = os.path.join(SITE, 'tools', 'downloads.json')
def release_sizes():
    import urllib.request
    try:
        req = urllib.request.Request('https://api.github.com/repos/eggi36/zax-game.com/releases/tags/downloads',
                                     headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'zax-site-gen'})
        with urllib.request.urlopen(req, timeout=15) as r:
            sizes = {a['name']: a['size'] for a in json.load(r)['assets']}
        json.dump(sizes, open(SIZES_CACHE, 'w'), indent=1, sort_keys=True)
        return sizes
    except Exception as e:
        print('Release nicht erreichbar, nehme', os.path.basename(SIZES_CACHE), '-', e)
        return json.load(open(SIZES_CACHE))
SIZES = release_sizes()
def size(name):
    b = SIZES[name]   # KeyError = Datei fehlt im Release
    return f'{b / 1e6:.1f} MB' if b >= 1e6 else f'{max(1, round(b / 1e3))} KB'
demos = [
 ('ZaxDemo_2001-07-01_Build890.exe', '1 July 2001', '890', '30 June 2001',
  'The earliest demo, from an older stage of the engine. It is the only build with 3D positional sound via DirectSound3D and EAX.'),
 ('ZaxDemo_2001-07-19_Build950.exe', '19 July 2001', '950', '18 July 2001',
  'An intermediate build shortly before the full version, without the positional sound of the first demo.'),
 ('ZaxDemo_2001-08-06_Build1308.exe', '6 August 2001', '1308', '1 August 2001',
  'Technically the EXE of the full version without copy protection – only its smaller data set makes it a demo.'),
]
official = box('''  <h3>Playable demos (2001)</h3>
  <p>Three demo versions were released in the summer of 2001. All three contain the same five levels. Each download is the original Windows installer.</p>
  <ul class="downloads">
''' + ''.join(f'''    <li><a href="{REL}{f}"><b>Demo of {d}</b></a> – build {b}, EXE dated {e} ({size(f)})<br>{t}</li>
''' for f, d, b, e, t in demos) + '''  </ul>
  <p class="small">Minimum system requirements: Pentium II 233 MHz, 32 MB RAM. File list and SHA-256 checksums: <a href="https://github.com/eggi36/zax-game.com/releases/tag/downloads">release page</a>.</p>
  <h3>French patch</h3>
  <p><a href="''' + REL + '''Zax_French_Patch.zip"><b>Zax_French_Patch.zip</b></a> (''' + size('Zax_French_Patch.zip') + ''', February 2002) – fixes the crash in mission 10 of the French version. Copy <code>1French.RED</code> into the Zax folder (where <code>Zax.exe</code> is); save games keep working.</p>
  <h3>Wallpapers</h3>
  <p>The wallpaper section of the official site was a Flash file that has not been preserved.</p>
''', 'Official downloads', 'official')
packs = [
 ('Zax_Fix_Levels.zip', 'Level fixes', '<code>DataFixes.RED</code> – fixes script errors in ten levels: Valeth\'s ore cave in mission 7, misspelt trigger targets in missions 5, 14 and 21, the mission log in the Mining maps, the Sun key in the Assimilate Temple and more. Works with every language. Note: the Slave Main key door now raises the alarm, so that level is harder than in the original.'),
 ('Zax_Fix_English.zip', 'English fix', '<code>EnglishFix.RED</code> – spelling, grammar and wrong names in menus, objectives, dialogue and item texts; dialogue matches the spoken voice.'),
 ('Zax_Fix_German.zip', 'German fix', '<code>GermanFix.RED</code> – wrong translations, duplicate menu shortcuts, 28 missing texts and 5 multiplayer map names, 37 broken item labels. Needs <code>GERMAN.RED</code>.'),
 ('Zax_Fix_French.zip', 'French fix', '<code>0FrenchFix.RED</code> – fixes the mission 10 crash like the official patch, adds 33 missing texts and corrects about 30 translations. Needs <code>0French.RED</code>. Not yet tested in the game.'),
 ('Zax_Fix_Spanish.zip', 'Spanish fix', '<code>0SpanishFix.RED</code> – a broken weapon text, three voice lines that played in English, missing item and weapon names. Needs <code>0Spanish.RED</code>.'),
 ('Zax_Fix_Polish.zip', 'Polish fix', '<code>PolishFix.RED</code> – Polish voice lines that never played, a speaker without portrait, missing texts and misspellings. Needs <code>Polish.red</code>.'),
 ('Zax_Fix_Chinese.zip', 'Chinese fix', '<code>0ChineseFix.RED</code> – readable multiplayer texts (they were garbled), a missing item description and weapon name. Chinese Simplified edition only.'),
 ('Zax_LanguagePack_Russian.zip', 'Russian language pack', '<code>RUSSIAN.RED</code> – the Russian texts and voices of the Russian edition for the standard game data, with repaired voice files and missing texts added.'),
 ('Zax_LanguagePack_Czech.zip', 'Czech language pack', '<code>Czech.RED</code> – the Czech community translation of 2004 (translation: Dr. Mephisto, technique: Blackbird) for the standard game data; no patched <code>Zax.exe</code> needed, mission 18 no longer ends the game.'),
]
community = box('''  <h3>Tools</h3>
  <ul class="downloads">
    <li><a href="https://github.com/eggi36/zax-launcher/releases"><b>Zax-Launcher</b></a> – a launcher for the original <code>Zax.exe</code>: start directly into any map with a start point and difficulty of your choice, a “Load Map” button in the game menu, and the developer switches still hidden in the exe (debug log, frame rate, cheats and more). The exe itself is not modified; full support for build 1308/1309 without copy protection.</li>
    <li><a href="https://github.com/eggi36/zax-editor/releases"><b>Zax Editor</b></a> – a level editor for Zax maps: objects, polygons, ground, surfaces, mini map, transitions and dialogue scripts, own graphics, a model viewer and a “Test in game” button. English with a German translation.</li>
  </ul>
  <h3>Fix packs and language packs</h3>
  <p>Each ZIP holds one <code>.RED</code> file and a README. Put the <code>.RED</code> file into the game folder next to <code>Zax.exe</code> and <code>DATA.dat</code> – the game loads every <code>.RED</code> file there in alphabetical order. Use one language at a time; the level fixes combine with any of them. All packs need the original game.</p>
  <ul class="downloads">
''' + ''.join(f'''    <li><a href="{REL}{f}"><b>{n}</b></a> ({size(f)}) – {t}</li>
''' for f, n, t in packs) + '''  </ul>
  <p class="small">Fan-made tools and packs, not affiliated with the rights holders. Checksums: <a href="https://github.com/eggi36/zax-game.com/releases/tag/downloads">release page</a>. More projects around the game are listed on the <a href="projects.html">Projects</a> page.</p>''', 'Community downloads', 'community')
dl = community + '\n' + official
page('downloads.html', 'Downloads', 'Downloads', dl, 'downloads.html')

# ---------------------------------------------------------------- News & Links (+ Developer Logs)
news_site = [('11/14/26', 'This fan site goes online: navigation and fonts rebuilt from the original Flash files of zax-game.com, the original websites restored in the <a href="archive.html">Archive</a>.')]
news_orig = [
 ('04/03/01', 'Zax&trade; has a brand new name! "Zax the Alien Hunter" is now the official title of the Zax title that has been under construction for the past year. The team is currently working on multi-player maps, AI\'s and optimizations. The game is looking beautiful if I do say so myself.'),
 ('02/15/01', 'Hmmm, I wonder what\'s new? You guessed it! The Zax page has been redesigned yet again. However this time it is for good reason. There is now a Zax message board that will be moderated by members of Reflexive. There will be a major update to the Logs section soon.'),
 ('01/03/01', 'Well, the Zax Team is back at work after a nice relaxing vacation! There have been many changes, you just can\'t see most of them. There is a new screen shot, and the Logs section has been redone. There is also a new Weapon revealed, so have fun checking out all the new stuff.'),
 ('12/07/00', 'The website has just about been completed. All of the sections will be updated on a continuous basis. So checkout what is new and come back often for updates!'),
 ('11/12/00', 'The Zax website is going through some major changes. It should now be updated every week with the latest and greatest information on the Epic adventure Zax. Stay tuned for more information.'),
]
links = [
 ('About the game', [
  ('https://www.mobygames.com/game/5954/zax-the-alien-hunter/', 'MobyGames', 'credits, screenshots, releases'),
  ('https://en.wikipedia.org/wiki/Zax:_The_Alien_Hunter', 'Wikipedia', 'overview and reviews'),
  ('https://www.myabandonware.com/game/zax-the-alien-hunter-du5', 'My Abandonware', 'game page')]),
 ('Original websites', [
  ('archive.html', 'Archive on this site', 'reflexive.net/Zax (2001), jowood.com (2003) and zax-game.com (2002–2004), restored'),
  ('https://web.archive.org/web/2001/http://www.reflexive.net/Zax/', 'reflexive.net/Zax at the Internet Archive', ''),
  ('https://web.archive.org/web/2004/http://www.zax-game.com/', 'zax-game.com at the Internet Archive', '')]),
]
nl = box(''.join(f'  <p><span class="date">{d}</span>{t}</p>\n' for d, t in news_site), 'Site news', 'site-news')
nl += '\n' + box(''.join(f'  <p><span class="date">{d}</span>{t}</p>\n' for d, t in news_orig)
                 + '  <p class="small">News from the official site by Reflexive Entertainment, 2000–2001.</p>', 'Development news 2000–2001', 'development-news')
nl += '\n' + box('  <p>Every week the Reflexive team posted what they had been working on – programmers, artists and level designers. Three of these logs have survived: 12/08/00, 12/15/00 and 01/05/01.</p>\n  <p><a href="logs.html">Read the developer logs</a></p>', 'Developer logs', 'developer-logs')
lk = ''
for head, entries in links:
    lk += f'  <h3>{head}</h3>\n  <ul>\n' + ''.join(
        f'    <li><a href="{u}">{n}</a>{" – " + d if d else ""}</li>\n' for u, n, d in entries) + '  </ul>\n'
nl += '\n' + box(lk, 'Links', 'links')
page('news-links.html', 'News & Links', 'News & Links', nl, 'news-links.html')

logs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs.json'), encoding='utf-8'))
lg = box('  <p>The weekly logs of the Zax team at Reflexive Entertainment, as published on reflexive.net/Zax. Text unchanged, apart from layout.</p>\n  <p><a href="news-links.html">&larr; back to News &amp; Links</a></p>', 'Developer logs')
for l in logs:
    inner = ''
    for sec in l['sections']:
        inner += f'  <h3>{html.escape(sec["name"])}</h3>\n'
        for p in sec['people']:
            inner += f'  <p class="small" style="margin:.6em 0 .2em;color:#fff">{html.escape(p["name"])}</p>\n  <ul>\n' + ''.join(
                f'    <li>{html.escape(i)}</li>\n' for i in p['items']) + '  </ul>\n'
    lg += '\n' + box(inner, f'Log {l["date"]}', 'log-' + re.sub(r'\W+', '-', l['date']).strip('-'))
page('logs.html', 'Developer Logs', 'Developer Logs', lg, 'news-links.html')

# ---------------------------------------------------------------- Projects
repos = [
 ('zax-formats', 'Python', 'Documentation and Python tools for the file formats of the game: level files (.zax), waypoint files (.way) and the Data.dat archive.'),
 ('zax-editor', 'Python', 'A level editor for Zax maps.'),
 ('zax-launcher', 'C', 'A launcher for Zax: The Alien Hunter.'),
 ('zax-decomp', 'C++', 'Decompilation project of the game executable.'),
]
pj = box('  <p>Projects around the game, all open source on GitHub.</p>\n' + ''.join(
    f'  <div class="item"><h3><a class="repo" href="https://github.com/eggi36/{n}">{n}</a><span class="tag">{lang}</span></h3><p>{d}</p></div>\n'
    for n, lang, d in repos), 'Projects', 'my-projects')
community_projects = [
 ('https://github.com/zar9roc/ZaxEd', 'ZaxEd', 'A map viewer in the browser, an editor is planned.'),
 ('https://github.com/zar9roc/ZaxHiRes', 'ZaxHiRes', 'A patch for high resolutions.'),
 ('https://github.com/dubstabber/Zax-The-Alien-Hunter-Rebooted', 'Zax – The Alien Hunter Rebooted', 'A remake in Godot 4.'),
 ('https://github.com/dubstabber/Zax-bot', 'Zax-bot', 'Bots for multiplayer.'),
]
pj += '\n' + box('  <p>Projects by other fans.</p>\n' + ''.join(
    f'  <div class="item"><h3><a class="repo" href="{u}">{html.escape(n)}</a></h3><p>{d}</p></div>\n'
    for u, n, d in community_projects), 'Community projects', 'community-projects')
page('projects.html', 'Projects', 'Projects', pj, 'projects.html')

# ---------------------------------------------------------------- Archive
arch = [
 ('archive/2001-01_Version1/Zax/index.html', 'archive/shot_2001-01_Version1.png', 'reflexive.net/Zax – January 2001',
  'The developer\'s site during production. Most of the layout graphics were not preserved; missing images are marked.'),
 ('archive/2001-04_Version2/Zax/index.html', 'archive/shot_2001-04_Version2.png', 'reflexive.net/Zax – April 2001',
  'The stone medallion design with Zax and the rune chain. Some frame graphics were not preserved; missing images are marked.'),
 ('archive/2001-12_Version3/Zax/index.html', 'archive/shot_2001-12_Version3.png', 'reflexive.net/Zax – December 2001',
  'The release version with FAQ, demo page and the mirrored navigation.'),
 ('archive/zax-game.com_2004/index_flash.html', 'archive/shot_zax-game.com_gateway.png', 'zax-game.com – 2002 to 2004',
  'The official JoWooD site in English and German. Navigation and banner are the original Flash files, played with the Ruffle emulator.'),
 ('archive/jowood.com_2003/gamers/index.html', 'archive/shot_jowood.com_2003.jpg', 'jowood.com – January 2003',
  'The game\'s pages on the publisher\'s site in English and German: the game, screenshots, demo, patches, reviews, system requirements and registration. Links to other JoWooD pages lead to the Internet Archive; the Zax logo and most English screenshots were not preserved, the forms are disabled.'),
]
ar = box('  <p>The original websites, restored from copies at the Internet Archive. They are shown as they were – with frames, period HTML and, where noted, Flash. Only archived material is shown: images that were never preserved are marked as missing.</p>', 'Archive')
ar += '\n<div class="cards">\n' + ''.join(
    f'<div class="box card"><p class="title">{t}</p><a href="{u}" target="_blank" rel="noopener">{img(s, t, "shot")}</a><p>{d}</p><p><a href="{u}" target="_blank" rel="noopener">Open</a></p></div>\n'
    for u, s, t, d in arch) + '</div>'
page('archive.html', 'Archive', 'Archive', ar, 'archive.html')

# ---------------------------------------------------------------- Sitemap (Seite im Menü + sitemap.xml)
def sm_list(items):
    return '<ul>\n' + ''.join(f'<li><a href="{h}">{html.escape(t)}</a>' + (sm_list(c) if c else '') + '</li>\n' for h, t, c in items) + '</ul>\n'
SITEMAP = [
 ('index.html', 'Homepage', []),
 ('the-game.html', 'The Game', [(f'the-game.html#{a}', t, []) for a, t, _ in GAME_SECTIONS]),
 ('downloads.html', 'Downloads', [('downloads.html#community', 'Community downloads – tools, fix packs and language packs', []),
                                   ('downloads.html#official', 'Official downloads – demos and the French patch', []),
                                   ('https://github.com/eggi36/zax-game.com/releases/tag/downloads', 'Release page with all files and checksums', [])]),
 ('news-links.html', 'News & Links', [('news-links.html#site-news', 'Site news', []),
                                       ('news-links.html#development-news', 'Development news 2000–2001', []),
                                       ('logs.html', 'Developer logs', [('logs.html#log-' + re.sub(r'\W+', '-', l['date']).strip('-'), 'Log ' + l['date'], []) for l in logs]),
                                       ('news-links.html#links', 'Links', [])]),
 ('projects.html', 'Projects', [('projects.html#my-projects', 'Projects of this site', []), ('projects.html#community-projects', 'Community projects', [])]),
 ('archive.html', 'Archive', [(u, t, []) for u, s_, t, d in arch]
                              + [('archive/jowood.com_2003/gamers/index_de.html', 'jowood.com – January 2003, German pages', [])]),
]
smap = box('  <div class="sitemap">\n' + sm_list(SITEMAP) + '  </div>', 'Sitemap')
page('sitemap.html', 'Sitemap', 'Sitemap', smap, 'sitemap.html')
# Für Suchmaschinen: alle eigenen Seiten (ohne Weiterleitungen) und die Einstiegsseiten des Archivs
urls = [h for h, _, _ in MENU] + ['index.html', 'logs.html'] + [u for u, *_ in arch] + ['archive/jowood.com_2003/gamers/index_de.html']
urls = sorted(set(urls), key=lambda u: (u != 'index.html', u))
open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>https://zax-game.com/{"" if u == "index.html" else u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(SITE, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://zax-game.com/sitemap.xml\n')

# ---------------------------------------------------------------- Weiterleitungen alter Adressen
# GitHub Pages kann keine Server-Weiterleitungen: Meta-Refresh + JS + Link.
# Alte Adressen -> passende Seite der Fan-Site: frühere Einzelseiten dieser Site und zax-game.com (2002–2004;
# deutsche -> Startseite).
REDIRECTS = {
    'mission-briefing.html': 'the-game.html#mission-briefing', 'profiles.html': 'the-game.html#profiles',
    'weapons.html': 'the-game.html#weapons',
    'index_flash.html': 'index.html', 'index_no_flash.html': 'index.html', 'gateway.html': 'index.html',
    **{f'english/{p}.html': 'index.html' for p in ('index', 'homepage', 'top_nav', 'top_secret')},
    **{f'english/{p}.html': 'the-game.html#mission-briefing' for p in ('mission_briefing', 'missionb_nav', 'story', 'mission_shots')},
    **{f'english/{p}.html': 'downloads.html' for p in ('downloads', 'downloads_nav', 'cargo_hold')},
    'english/news_and_links.html': 'news-links.html',
    **{f'german/{p}.html': 'index.html' for p in ('index', 'homepage', 'top_nav', 'mission_briefing', 'missionb_nav', 'story', 'cargo_hold')},
}
for old, target in REDIRECTS.items():
    new = os.path.relpath(target, os.path.dirname(old) or '.')
    os.makedirs(os.path.join(SITE, os.path.dirname(old)), exist_ok=True)
    open(os.path.join(SITE, old), 'w', encoding='utf-8').write(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Zax: The Alien Hunter</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="https://zax-game.com/{'' if target == 'index.html' else target}">
<meta http-equiv="refresh" content="0;url={new}">
<script>location.replace('{new}'{'' if '#' in new else ' + location.hash'});</script>
</head>
<body><a href="{new}">Continue to the Zax fan site</a></body>
</html>
''')

# ---------------------------------------------------------------- Archiv: keine rohen Sonderzeichen
# GitHub Pages sendet charset=utf-8; rohe Latin-1-Bytes der Originalseiten würden zu �.
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archive_entities import raw_pages
raw = raw_pages()
if raw:
    sys.exit('Archivseiten mit rohen Sonderzeichen – erst `python3 tools/archive_entities.py` ausführen:\n  '
             + '\n  '.join(os.path.relpath(p, SITE) for p in raw))
print('ok')

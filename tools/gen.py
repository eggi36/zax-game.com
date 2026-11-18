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

def sections(label, secs, intro=''):
    """Seite aus Abschnitten wie „The Game“: Unterleiste mit Sprungmarken, je Abschnitt eine Punktmatrix-Überschrift.
    secs: [(id, Titel, HTML)]; intro steht zwischen Leiste und erstem Abschnitt."""
    out = f'<nav class="subnav" aria-label="{html.escape(label)}">' + ''.join(f'<a href="#{a}">{html.escape(t)}</a>' for a, t, _ in secs) + '</nav>\n'
    out += (intro + '\n') if intro else ''
    return out + '\n'.join(f'<section id="{a}" aria-labelledby="{a}-h">\n<h2 class="section-title" id="{a}-h"><span class="dots">{html.escape(t)}</span></h2>\n{body}\n</section>'
                            for a, t, body in secs)

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

# ---------------------------------------------------------------- The Game
# Eine Seite in der Reihenfolge eines Handbuchs: Overview → Story → Characters → Weapons → Interface → Screenshots → FAQ. (Unused Content steht im Archiv.)
# Texte aus den archivierten Seiten: reflexive.net (2001) und zax-game.com (2002–2004); je Eintrag beide Quellen zusammengeführt.
R1 = 'archive/2001-12_Version3/Zax/'          # reflexive.net, Dezember 2001
ZG = 'archive/zax-game.com_2004/english/'     # zax-game.com
SRC_NAMES = {'r': 'reflexive.net, 2001', 'z': 'zax-game.com, 2002–2004'}
def src_links(srcs):
    return '<p class="srcline">Source: ' + ' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{SRC_NAMES[k]}</a>' for k, u in srcs) + '</p>'
def thumb(path, alt):
    return f'<div class="thumb">{img(path, alt)}</div>' if path else '<div class="thumb none">picture not preserved</div>'
def entry(name, pic, texts, srcs, id=None):
    i = f' id="{id}"' if id else ''
    return f'  <div class="item entry"{i}>{thumb(pic, name)}<h3>{html.escape(name)}</h3>{ps(*texts)}{src_links(srcs)}</div>'

# ---- Overview
features_sp = ['Nonstop action', 'More than 100 challenging maps', '7 unique environment types', 'Tons of cool special effects',
               'Frequent weapon upgrades throughout your adventure', 'Hundreds and hundreds of robots to decimate',
               'Interesting puzzles, tricks, and traps around just about every corner', 'A captivating and involving story']
features_mp = [('Salvage King', 'You have to try this! Your goal is to collect and protect your crystals from other marauding players intent on cashing in on your hard work. Should you collect your own, or forcibly take your opponents\' from him? Well, that\'s up to you.'),
               ('Capture the Flag', 'Team up for some classic style flag retrieval in our trap-infested environments.'),
               ('Deathmatch', 'It\'s survival of the fittest in the alien world! Can you adapt?')]
facts = [('Developer', 'Reflexive Entertainment'), ('Publisher', 'JoWooD Productions'), ('Released', '2001, for Windows'),
         ('Genre', 'Action/adventure in isometric view'), ('Single player', '22 missions on more than 100 maps in 7 environment types'),
         ('Multiplayer', 'Deathmatch, Capture the Flag and Salvage King, over the Internet or a LAN for up to 16 players'),
         ('Minimum system', 'Pentium II 233 MHz, 32 MB RAM')]
ov = row(img('assets/img/gallery/jowood_packshot.jpg', 'Zax: The Alien Hunter, PC CD-ROM'), box(ps(
    'Zax – The Alien Hunter is a non-stop action/adventure game that crash-lands you onto an alien world where everything has been turned upside down. A proud people have been enslaved, their world of ancient magic wrested from them by a mysterious god of metal. Your fiery entrance onto their planet has given them hope for a release from their torment, but you are in sad shape yourself. With no military training and a heavily-damaged ship, your obstacles are clear.',
    'Unprepared as you are, you represent the final hope for the Korbo. Are you up to the challenge? Can you defeat the minions of Om? No one said being a hero was easy.')
    + '\n  <dl class="facts">\n' + ''.join(f'    <dt>{k}</dt><dd>{v}</dd>\n' for k, v in facts) + '  </dl>', 'Zax: The Alien Hunter'))
ov += '\n' + box('  <h3>Single player</h3>\n  <ul>\n' + ''.join(f'    <li>{f}</li>\n' for f in features_sp) + '  </ul>\n'
                 '  <h3>Multiplayer</h3>\n  <dl class="faq">\n' + ''.join(f'    <dt>{n}</dt><dd>{t}</dd>\n' for n, t in features_mp) + '  </dl>\n'
                 + src_links([('z', ZG + 'features.html')]), 'Features')

# ---- Story
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
st = ''
for src, alt, title, paras in story:
    b = box(ps(*paras), title)
    st += (row(img(src, alt), b) if src else row('<div style="width:177px"></div>', b)) + '\n'
st += box('  <p>How the story was told before the release: in 1998 Zax was still a soldier of the “Galactic Imperium” on a planet about to be destroyed by a supernova (<a href="archive/1998-12_Version0/zax/zaxintro.html" target="_blank" rel="noopener">reflexive.net, December 1998</a>), and during development the hero was called “Crater”.</p>', 'Earlier versions')

# ---- Characters (Bild: zax-game.com, sonst reflexive.net; Texte beider Seiten)
P, PO = 'assets/img/profiles/', 'assets/img/profiles/official/'
RC, ZE, ZH = R1 + 'Characters.htm', ZG + 'enemy/', ZG + 'heroic/'
characters = [
 ('Heroes', [
  ('Zax', PO + 'heroic_zax.jpg', ['On a quest to get rich has his priorities rearranged when discovering the plight of the Korbo.',
    'Rollin Triskin “Zax”: Born 2318 son of Tallis and Marion Triskin. His parents, fearing that they would not be able to get him out of the system, were forced to place him with his uncle. They hugged their boy and promised they would come for him as soon as they could. Months turned into years and the years turned into his life. Zax never saw or heard from his parents again.'],
   [('z', ZH + 'zax.html'), ('r', RC)]),
  ('Zelon', None, ['The onboard artificial intelligence of Zax\'s ship. He fondly refers to her as Babe. She is his second set of eyes and ears as he discovers this alien environment. She also develops new items for Zax to use on his adventure.'], [('z', ZH + 'zelon.html')]),
  ('The Korbo', None, ['The Korbo are a native race to the planet Zax has discovered. They are an intelligent, yet somewhat primitive people that has been overwhelmed and enslaved by the robots on the planet. They have been praying to their true gods for a saviour. Many of them view Zax as that saviour.'], [('z', ZH + 'korbo.html')]),
  ('Mindaza', None, ['A Korbo Shaman, wise, but not as learned as Valeth.'], [('z', ZH + 'mindaza.html')])]),
 ('Om and his servants', [
  ('Om', None, ['This robot has convinced the Korbo that he is an angry god that should be obeyed and worshipped. His robotic minions are the chief obstacles for Zax.'], [('z', ZE + 'om.html')]),
  ('Azah-Pan', PO + 'enemy_azah_pon.jpg', ['This mysterious spirit is capable of possessing and controlling robots. A fiercely loyal servant of Om. His assignment is to remove the threat presented by Zax.'], [('z', ZE + 'azah_pan.html')]),
  ('Altered Korbo', PO + 'enemy_altered_korbo.jpg', ['Once loyal Korbo citizens, Altered Korbo are part flesh, part machine and have been programmed to be servants of Om. These unfortunate beings have been injected with what the Korbo call the Virus of Metal. They are Om\'s ultimate means of fear creation and population control. They are aggressive but not very durable or strong.'], [('z', ZE + 'altered_korbo.html')]),
  ('Rogcoil', PO + 'enemy_rogcoil.jpg', ['Quick moving, lightly armoured patrol robots using energy pulse weapons a bit stronger than the altered Korbo. Assigned to guard the jungle and caves and supervise the enslaved Korbo.',
    'These Cyborg are lightly armed and are directly controlled by Om. Rogcoil often patrol in groups. They can be seen around Korbo villages, herding the Korbo to their doom. Although they are not heavily armored, they can still put up a fight and are extremely effective at intimidating the Korbo.'], [('z', ZE + 'rogcoil.html'), ('r', RC)]),
  ('Crutch', PO + 'enemy_crutch.jpg', ['Derives its name from its means of propulsion. It is heavily armoured with very accurate energy pulse weaponry.'], [('z', ZE + 'crutch.html')]),
  ('Om Overseer', PO + 'enemy_om_overseer.jpg', ['Heavily armoured biped robot that has a missile launcher for a right arm. Bears decorations from a time when the Korbo believed Om\'s minions were deities.'], [('z', ZE + 'om_overseer.html')]),
  ('Master Om Overseer', P + 'parascope.jpg', ['These highly intelligent Bots are the right hand of Om. Master Overseers control other Bots and coordinate their activities in gathering resources for the construction of facilities. Their other purpose involves the gathering and enslaving of Korbo. Master Overseers are equipped with shields and a powerful right gun.'], [('r', RC)]),
  ('Lord Om Overseer', PO + 'enemy_lord_om_overseer.jpg', ['The most devastating robot in Om\'s service. Capable of discharging missiles in tandem from either of its two \'arms\'. Korbo have seldom seen this most feared robot.',
    'Lord Overseers are similar to Master Overseers but do not take part in the daily routines of the Korbo slave camps. Their job is to serve the needs of Om. Lords can be found mostly near the inner chambers of the facilities to which Om itself resides. They are darker in color than the Masters and pack a much more powerful projectile. A Companion Drone is usually found with these evil Bots.'], [('z', ZE + 'lord_om_overseer.html'), ('r', RC)]),
  ('Orb Slayer', None, ['Originally created to carry much smaller ordinance, this robot has been overloaded with a heavy explosive ball-bomb. Despite the limp, it presents formidable opposition.'], [('z', ZE + 'orb_slayer.html')]),
  ('Higher Orb Slayer', PO + 'enemy_higher_orb_slayer.jpg', ['This improvement of the Orb Slayer has no trouble carrying, or delivering, its even more devastating spheric bomb.',
    'These Bots are like their lower counterparts but with one exception. The Higher Orb Slayer wields a more powerful orb that is fired from a cannon on its right arm.'], [('z', ZE + 'higher_orb_slayer.html'), ('r', RC)]),
  ('Skynuk', None, ['This flying bot is nimble and very aggressive. It shoots explosive tip bullets that are extremely deadly.'], [('z', ZE + 'skynuk.html')]),
  ('Scorpio Flyer', P + 'scorpio.jpg', ['Bigger, stronger and more intimidating than the Skynuk. Watch out!',
    'The Scorpio Flyer is a larger Bot that hovers about a foot over the ground. These Bots can be found near Om\'s strongholds to fend off large groups of Korbo rebels. They are equipped with large lasers and an energy grenade thrower.'], [('z', ZE + 'scorpio_flyer.html'), ('r', RC)]),
  ('Talon', None, ['This spider-like robot is slow moving but equipped with a grenade launcher that will keep intruders on alert.'], [('z', ZE + 'talon.html')]),
  ('Sentinon', None, ['Created to guard high security areas, these robots lie harmless underground until a would-be trespasser is detected. They then arm themselves in a startling manner.'], [('z', ZE + 'sentinon.html')])]),
 ('Creatures', [
  ('Cave Dweller', P + 'cave_dweller.jpg', ['This soft-shelled four-legged arachnid resides deep in the wet caverns of LV-42-3. Though very slow moving, they can kill enemy and prey alike with the venomous spray shot from their mouths.'], [('r', RC)]),
  ('Jungle Creature', P + 'jungle_creature.jpg', ['These creatures can usually be found in packs throughout the jungle regions. These speedy two-legged beasts use their powerful jaws to feast upon the native wild boar and any unsuspecting Korbo.'], [('r', RC)])]),
]
def ch_id(group): return 'ch-' + re.sub(r'[^a-z]+', '-', group.lower()).strip('-')   # Sprungmarke einer Figurengruppe
ch = box('  <p>The heroes, the robots of Om and the creatures of the planet, as the developer (reflexive.net, 2001) and the official site (zax-game.com, 2002–2004) described them. Where both sites wrote about the same character, both texts are given; pictures were only partly preserved.</p>\n'
         '  <nav class="toc">' + ' · '.join(f'<a href="#{ch_id(g)}">{g}</a>' for g, _ in characters) + '</nav>')
for g, items in characters:
    ch += '\n' + box('\n'.join(entry(*c) for c in items), g, ch_id(g))

# ---- Weapons (Reihenfolge und Texte von zax-game.com – meist Zelons Worte –, Bilder und längere Texte von reflexive.net)
W, RW, ZW = 'assets/img/weapons/', R1 + 'Weapons.htm', ZG + 'weapons/'
weapons = [
 ('Modified Laser Welder', None, ['I designed this weapon for you when it became apparent you would need to defend yourself. Its low power laser pulse is being drawn from a fusion reactor meant to weld and repair metallic components. I will work on a replacement immediately.'], [('z', ZW + 'laser_welder.html')]),
 ('Light Pistol', W + 'light_pistol_ill.gif', ['Much more powerful than the modified laser welder, it can be fired frequently to spray damage in numerous directions.',
   'This pistol is the standard emergency weapon that Crater carries in his boot holster or has strapped under his seat. Its small, tough frame has been proven time and again to be ideal in dealing with surprise problems – though it is typically used as a backup when the regular primary weapon has been disabled. Although its disruptive power is actually weaker than that of the Modified Laser Welder, the laser blast emitted from the Light Pistol has a far greater range.'], [('z', ZW + 'light_pistol.html'), ('r', RW)]),
 ('Semi Automatic Pistol', None, ['Designed for use with metal piercing projectiles. To be used at your discretion. I suspect it will be most valuable when the power supply of your battery is low.'], [('z', ZW + 'semi_auto.html')]),
 ('Full Automatic Pistol', W + 'full_auto_pistol.gif', ['Capable of discharging bullets at a far greater rate than the semi-auto version. Created after optimizing the firing mechanism of the Semi-Auto Pistol.',
   'This weapon fires slugs at an ungodly rate, reducing the enemies in front of it to pieces. However, it uses bullets like there is no tomorrow, and should only be used in the most dire of situations or when a bullet stockpile has just been located. Blocked by: the Inertia shield.'], [('z', ZW + 'full_auto.html'), ('r', RW)]),
 ('Twin Disruptor', W + 'twin_disruptor_ill.gif', ['Twin mounted disruptive lasers for increased damage ability.',
   'This weapon has twin-mounted disruptive lasers that feed asynchronously off of the power source, reducing the power leakage and increasing the damage potential. It provides a good punch for the Mega-Joule usage.'], [('z', ZW + 'twin_disruptor.html'), ('r', RW)]),
 ('Tri-Spread Gun', W + 'tri_gun_detail.jpg', ['This is the Tri-Spread Gun. A very damaging energy based weapon capable of dispersing energy pulses in three different directions.',
   'This is the level 3 version of the Light Pistol. The only difference other than doing more damage is that the Tri-Spread gun emits 3 lasers. Blocked by: the Albedo shield.'], [('z', ZW + 'tri_spread.html'), ('r', RW)]),
 ('Grenade Launcher', None, ['Ejects grenades so that you may reduce the number of robots in an area prior to entering it yourself.'], [('z', ZW + 'grenade_launcher.html')]),
 ('Proximity Mine', None, ['Great care should be taken using these mines. Once placed, there are only a few seconds to clear the area before it arms itself with a hair trigger. Its proximity detectors will cause the explosives to detonate when anything or anyone comes close to it.'], [('z', ZW + 'proximity_mine.html')]),
 ('Plasma Thrower', None, ['Akin to a flamethrower, this weapon expels material that is not liquid and not solid – Plasma – that causes large amounts of damage to whatever it touches.'], [('z', ZW + 'plasma_thrower.html')]),
 ('Psyonic Wave Glove', None, ['This glove will send out a stream of psyonic electricity that will expand and encompass the first object it comes in contact with.'], [('z', ZW + 'psionic_wave.html')]),
 ('Missile Launcher', None, ['Typically too expensive to use under normal conditions, Zelon is devising a model that is compatible with the rockets “available” from the robots.'], [('z', ZW + 'missile_launcher.html')]),
 ('Impaction Cannon', W + 'impaction_cannon.jpg', ['This weapon emits an energy pulse fused with a sub-nucleonic charge.',
   'A weapon of untested strength and power, the Impaction Cannon is a mish-mash of ancient alien technology and Imperium ingenuity. It emits a highly focused laser pulse surrounded by a phase-dampened sub-nuclear envelope, perfect for punching through albedo shields and robotic matter. Its Mega-Joule cost is very high, but the show is well worth the wait.'], [('z', ZW + 'impaction_cannon.html'), ('r', RW)]),
 ('Nuclear Disruptor', W + 'nucleardisbeauty.jpg', ['Emits a small radioactive cloud that is devastating to its targets.',
   'This large weapon spits forth a translucent, glowing cloud that emits massively duped electrons at enemy targets. What makes this weapon especially devastating is the intelligence that the cloud exhibits. It follows its target through hallways and around corners until it consumes itself or its target. The cloud does move slowly, so if the target runs away (and keeps running) the cloud (perhaps) can be avoided.'], [('z', ZW + 'nuclear_disruptor.html'), ('r', RW)]),
]
wp = box('  <p>The thirteen weapons in the order Zax gets them. Zelon builds each one in the materials generator on board the ship (see <a href="#interface">Interface</a>); the first text of each weapon is hers, from the official site. “Crater” in the longer texts of the developer\'s site was the working name of the hero.</p>\n'
         + '\n'.join(entry(*w) for w in weapons))

# ---- Interface (Features-Seite von zax-game.com)
hud = [('Health', 'If you allow Zax\'s health to go to 0% he dies and the game is over. You will want to keep his health as high as possible at all times.'),
       ('Shield Charge', 'Zax\'s current shield charge is displayed as a graphical representation of the fraction of the current charge over the total possible charge. Generating a higher level shield will increase total possible charge.'),
       ('Ore & Crystals', 'The number of ore and crystals are displayed as a fraction of how many Zax currently has – compared to how many he has collected over the course of his adventure.'),
       ('Sphere of Zin', 'This sphere detects evil in the general vicinity of its carrier.'),
       ('Game Time Elapsed', 'Zelon will keep a running clock of how long Zax\'s adventure has taken him. Useful for the mission log.'),
       ('Secondary weapon', 'Proximity Mines are displayed here (if Zax has them). The number below the icon represents the number of mines that Zax has in his possession. By default, weapons in this window are activated by clicking the right mouse button.'),
       ('Battery charge', 'Zax\'s current battery charge is displayed as a graphical representation of the fraction of current over total possible charge. Generating a higher-level battery will increase total possible charge.'),
       ('Primary Weapon', 'The primary weapon that Zax is currently using. By default, weapons in this window are fired by clicking the left mouse button.')]
gen_steps = ['Find your way to the Materials Generator onboard Zelon. It is towards the front of the ship.',
             'When the Generator appears, click on the Weapons tab (note the three other tabs as well).',
             'Click on the bar featuring the Modified Laser Welder (note that its background becomes highlighted).',
             'Click the Generate Button. If the item is not generated, you do not possess enough Ore or Crystals to create it. The quantity of ore or crystals required to create an item are listed to the far right of the item.']
it = box(f'  <p>{img("assets/img/gallery/features_hud.jpg", "The heads up display")}</p>\n  <p>At all times during gameplay, you will see the HUD at the bottom of the screen. There, useful information is constantly displayed – from left to right:</p>\n  <dl class="faq">\n'
         + ''.join(f'    <dt>{n}</dt><dd>{t}</dd>\n' for n, t in hud) + '  </dl>\n' + src_links([('z', ZG + 'features.html')]), 'The heads up display (HUD)')
it += '\n' + box(f'  <p>{img("assets/img/gallery/features_materials.jpg", "The materials generator")}</p>\n'
         + ps('Common back on Zax\'s home planet, Materials Generators convert raw materials into other items. As Zelon develops new items for Zax to use on his quest, she will let him know of their availability.',
              'Each item requires a specific number of Caranthian Ore and Crystal deposits. It is up to Zax to find the required amount in the world around him. Items available in the Materials Generator are divided into Weapons, Shields, Power Generators and Miscellaneous. How to create an item – for example the Modified Laser Welder:')
         + '\n  <ol>\n' + ''.join(f'    <li>{s}</li>\n' for s in gen_steps) + '  </ol>\n' + src_links([('z', ZG + 'features.html')]), 'The materials generator')

# ---- Screenshots
shots = [('reflexive_ss00.jpg', 'Pipes and machinery', 'r'), ('reflexive_ss02.jpg', 'In the caves', 'r'), ('jowood_zax_1.jpg', 'Laser barriers in a cave', 'j'),
         ('reflexive_ss22.jpg', 'Lava and pipes', 'r'), ('jowood_zax_2.jpg', 'A pool of lava', 'j'), ('reflexive_ss12.jpg', 'Jungle clearing', 'r'),
         ('jowood_zax_6.jpg', 'Jungle ruins', 'j'), ('reflexive_ss07.jpg', 'Temple floor', 'r'), ('jowood_zax_5.jpg', 'Metal halls', 'j'),
         ('jowood_zax_3.jpg', 'Snow and ice', 'j'), ('reflexive_ss04.jpg', 'Mission statistics', 'r'), ('reflexive_multiplayer07.jpg', 'Multiplayer', 'r')]
SHOT_SRC = {'r': 'reflexive.net', 'j': 'jowood.com'}
sc = box('  <p>Screenshots from the developer\'s site (reflexive.net, 2001–2003) and the publisher\'s game pages (jowood.com, 2004–2010). Earlier pictures of the game, from 1998 and January 2001, are in the <a href="archive.html">Archive</a>.</p>\n  <div class="gallery renders">\n' + ''.join(
    f'    <figure><a class="pic" href="assets/img/gallery/{f}" target="_blank" rel="noopener">{img("assets/img/gallery/" + f, t)}</a><figcaption>{html.escape(t)} <span class="srcline">{SHOT_SRC[k]}</span></figcaption></figure>\n'
    for f, t, k in shots) + '  </div>')

# ---- FAQ
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
fq = box('  <p class="small">From the official FAQ by Reflexive Entertainment (2001). Note: the Zax CD-Key is found on the back of the jewel case, not the back of the manual as indicated in the manual.</p>\n  <dl class="faq">\n' +
         ''.join(f'    <dt>{q}</dt><dd>{a}</dd>\n' for q, a in faq) + '  </dl>\n' + src_links([('r', R1 + 'FAQ.htm')]))

# ---------------------------------------------------------------- Unused Content (Modelle, die das Spiel nie benutzt)
# Daten: tools/unused_models.json ({Kategorie: [Modelle]}) + Vorschaubilder in assets/img/unused/<kategorie>/
# (aus der Modellübersicht der Verweisanalyse der DATA.dat: kein Level, Skript, keine Definition und nicht Zax.exe nennt sie).
unused_models = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unused_models.json'), encoding='utf-8'))
def unused_box(cat, models):
    groups = {}
    for m in models:
        area, _, rest = m['name'].partition('/')
        groups.setdefault(area, []).append((rest or area, m))
    out = ''
    for area in sorted(groups):
        out += f'  <h3>{html.escape(area)}</h3>\n  <div class="gallery">\n'
        for label, m in groups[area]:
            note = ' <span class="maybe">possibly used</span>' if m['status'] != 'unused' else ''
            out += (f'    <figure><div class="pic">{img(f"assets/img/unused/{cat.lower()}/" + m["file"], label)}</div>'
                    f'<figcaption>{html.escape(label.replace("/", " / "))}{note}</figcaption></figure>\n')
        out += '  </div>\n'
    n_maybe = sum(m['status'] != 'unused' for m in models)
    out += (f'  <p class="small">{len(models)} models of the category {cat}' +
            (f'; {len(models) - n_maybe} are never used, {n_maybe} only by other files that are themselves possibly unused (marked “possibly used”).'
             if n_maybe else ', none of them used by the game.') + '</p>')
    return box(out, cat, 'unused-' + cat.lower())
uc = box('  <p>Models in the game data (<code>DATA.dat</code>) that the game never uses: no level, script, object definition or the executable refers to them. Each picture is the first frame of the model, rendered straight from the game files.</p>')
uc += ''.join('\n' + unused_box(cat, models) for cat, models in unused_models.items())
GAME_SECTIONS = [('overview', 'Overview', ov), ('story', 'Story', st), ('characters', 'Characters', ch), ('weapons', 'Weapons', wp),
                 ('interface', 'Interface', it), ('screenshots', 'Screenshots', sc), ('faq', 'FAQ', fq)]
game = sections('The Game', GAME_SECTIONS)
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
 ('ZaxDemo_2001-06-01.exe', '1 June 2001', None, '1 June 2001',
  'The earliest known build, from a much older stage of the engine. It runs in 8-bit colour only, offers any 4:3 resolution from 640×480 upwards, shows still images instead of the intro videos and still has working cheat codes. Only a third-party repack of its installer has survived.'),
 ('ZaxDemo_2001-07-01_Build890.exe', '1 July 2001', '890', '30 June 2001',
  'The first demo with 16-bit graphics and the intro videos. Like the June demo, it still has 3D positional sound via DirectSound3D and EAX.'),
 ('ZaxDemo_2001-07-19_Build950.exe', '19 July 2001', '950', '18 July 2001',
  'An intermediate build shortly before the full version, without the positional sound of the earlier demos.'),
 ('ZaxDemo_2001-08-06_Build1308.exe', '6 August 2001', '1308', '1 August 2001',
  'Technically the EXE of the full version without copy protection – only its smaller data set makes it a demo.'),
]
official = box('''  <h3>Playable demos (2001)</h3>
  <p>Four demo versions from the summer of 2001 are known. All four contain the same five levels. The three later downloads are the original Windows installers; the earliest demo survives only as a later repack.</p>
  <ul class="downloads">
''' + ''.join(f'''    <li><a href="{REL}{f}"><b>Demo of {d}</b></a> – {f"build {b}" if b else "no build number"}, EXE dated {e} ({size(f)})<br>{t}</li>
''' for f, d, b, e, t in demos) + '''  </ul>
  <p class="small">Minimum system requirements: Pentium II 233 MHz, 32 MB RAM. File list and SHA-256 checksums: <a href="https://github.com/eggi36/zax-game.com/releases/tag/downloads">release page</a>.</p>
  <h3>French patch</h3>
  <p><a href="''' + REL + '''Zax_French_Patch.zip"><b>Zax_French_Patch.zip</b></a> (''' + size('Zax_French_Patch.zip') + ''', February 2002) – fixes the crash in mission 10 of the French version. Copy <code>1French.RED</code> into the Zax folder (where <code>Zax.exe</code> is); save games keep working.</p>
  <h3>Wallpapers</h3>
  <p>The wallpaper section of the official site was a Flash file that has not been preserved.</p>
''')
packs = [
 ('Zax_Fix_Levels.zip', 'Level fixes', '<code>DataFixes.RED</code> – fixes script errors in eleven levels: Valeth\'s ore cave in mission 7, misspelt trigger targets in missions 5, 14 and 21, the mission log in the Mining maps and in the Cave of Souls (mission 8), the Sun key in the Assimilate Temple and more; also Zax\'s footsteps on metal floors. Works with every language. Note: the Slave Main key door now raises the alarm, so that level is harder than in the original. A fix only takes effect in a level the game enters for the first time with the pack installed – levels already visited in a save game stay as they were.'),
 ('Zax_Fix_English.zip', 'English fix', '<code>EnglishFix.RED</code> – spelling, grammar and wrong names in menus, objectives, dialogue and item texts; dialogue matches the spoken voice.'),
 ('Zax_Fix_Chinese.zip', 'Chinese fix', '<code>0ChineseFix.RED</code> – readable multiplayer texts (they were garbled), a missing item description and weapon name. Chinese Simplified edition only.'),
 ('Zax_Fix_French.zip', 'French fix', '<code>0FrenchFix.RED</code> – fixes the mission 10 crash like the official patch, adds 33 missing texts and corrects about 30 translations. Needs <code>0French.RED</code>. Not yet tested in the game.'),
 ('Zax_Fix_German.zip', 'German fix', '<code>GermanFix.RED</code> – wrong translations, duplicate menu shortcuts, 28 missing texts and 5 multiplayer map names, 37 broken item labels. Needs <code>GERMAN.RED</code>.'),
 ('Zax_Fix_Polish.zip', 'Polish fix', '<code>PolishFix.RED</code> – Polish voice lines that never played, a speaker without portrait, missing texts and misspellings. Needs <code>Polish.red</code>.'),
 ('Zax_Fix_Russian.zip', 'Russian fix', '<code>RussianFix.RED</code> – repairs for the original Russian edition with its own Russian <code>DATA.dat</code> and <code>local.txt</code>: damaged voice files and data files, a speaker portrait that was never found, an untranslated speaker name, a missing item description and two missing weapon names, dialogue text that did not match the spoken line. Keep the loose <code>local.txt</code>. For Russian over the standard game data use the Russian language pack below, which already holds these repairs.'),
 ('Zax_Fix_Spanish.zip', 'Spanish fix', '<code>0SpanishFix.RED</code> – a broken weapon text, three voice lines that played in English, missing item and weapon names. Needs <code>0Spanish.RED</code>.'),
 ('Zax_LanguagePack_Czech.zip', 'Czech language pack', '<code>Czech.RED</code> – the Czech community translation of 2004 (translation: Dr. Mephisto, technique: Blackbird) for the standard game data; no patched <code>Zax.exe</code> needed, mission 18 no longer ends the game.'),
 ('Zax_LanguagePack_Russian.zip', 'Russian language pack', '<code>RUSSIAN.RED</code> – the Russian texts and voices of the Russian edition for the standard game data, with repaired voice files and missing texts added.'),
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
  <p class="small">Fan-made tools and packs, not affiliated with the rights holders. Checksums: <a href="https://github.com/eggi36/zax-game.com/releases/tag/downloads">release page</a>. More projects around the game are listed on the <a href="projects.html">Projects</a> page.</p>''')
# Vollversionen des Spiels: nur externe Links, nichts davon liegt auf dieser Seite oder im Release.
# Je Eintrag: (Sprache, Flagge in assets/img/flags/ oder None, Adresse, Anbieter, Beschreibung); Englisch zuerst, dann alphabetisch.
game_downloads = [
 ('English', 'en', 'https://archive.org/details/zax-the-alien-hunter-flt', 'archive.org', ''),
 ('Chinese', 'zh', 'https://archive.org/details/ZTAHChs', 'archive.org', ''),
 ('French', 'fr', 'https://www.abandonware-france.org/ltf_abandon/ltf_jeu.php?id=4014&fic=liens', 'abandonware-france.org', ''),
 ('German', 'de', 'https://archive.org/details/Zax_DE', 'archive.org', ''),
 ('Polish', 'pl', 'https://archive.org/details/zax_20210926', 'archive.org', ''),
 ('Russian', 'ru', 'https://www.old-games.ru/game/download/2011.html', 'old-games.ru', ''),
 ('Spanish', 'es', 'https://archive.org/details/Zax_ES', 'archive.org', ''),
]
# Flaggen im Stil der Sprachwahl von zax-game.com (en.gif = flag_uk.gif dort); ohne Flagge bleibt der Platz frei
def flag(code):
    return img(f'assets/img/flags/{code}.gif', '') if code else '<span class="noflag"></span>'
def game_item(lang, code, u, h, t):
    u, n = html.escape(u), f'Zax: The Alien Hunter – {html.escape(lang)}'
    return (f'    <li><a class="flag" href="{u}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">{flag(code)}</a>'
            f'<span><a href="{u}" target="_blank" rel="noopener"><b>{n}</b></a> <span class="srcline">({html.escape(h)}, external)</span>{"<br>" + t if t else ""}</span></li>\n')
gd_list = ('  <ul class="downloads flags">\n' + ''.join(game_item(*g) for g in game_downloads) + '  </ul>\n') if game_downloads else '  <p><i>No links yet.</i></p>\n'
# CD-Key-Generator (assets/js/cdkey.js, nach der Prüfung in Zax.exe 0x46b540; läuft nur im Browser)
cdkey_html = ('  <h3 id="cdkey-generator">CD key generator</h3>\n  <p>The game asks for a CD key. If yours is lost, this generator makes a valid one – right here in your browser, nothing is sent anywhere.</p>\n'
    '  <p class="cdkey-row"><output id="cdkey" class="cdkey" aria-live="polite">····-····-····-····-····</output>'
    '<button type="button" id="cdkey-new">New key</button><button type="button" id="cdkey-copy">Copy</button></p>\n'
    '  <noscript><p class="small">The generator needs JavaScript.</p></noscript>\n'
    f'<script src="{asset("assets/js/cdkey.js")}" defer></script>\n')
game_dl = box('  <p>The full versions of the game in its different editions. They are not hosted here: the links lead to other sites, which are responsible for their downloads.</p>\n'
              + gd_list
              + f'  <p>Problems with the copy protection? Use the <code>Zax.exe</code> of the <a href="{REL}ZaxDemo_2001-08-06_Build1308.exe">demo of 6 August 2001</a> (build 1308) – it is the full version\'s EXE without copy protection: install the demo, back up or rename the <code>Zax.exe</code> in the game folder of the full version, then copy the demo\'s <code>Zax.exe</code> there. This does not work with the Chinese edition.</p>\n'
              + cdkey_html
              + '  <p class="small">You need the full version for the fix packs and language packs below.</p>')
dl = sections('Downloads', [('game', 'Game Downloads', game_dl), ('community', 'Community Downloads', community), ('official', 'Official Downloads', official)])
page('downloads.html', 'Downloads', 'Downloads', dl, 'downloads.html')

# ---------------------------------------------------------------- News & Links (+ Developer Logs)
news_site = [('11/18/26', 'Seven early screenshots of January 2001 – the series of the developer\'s site, also shown by GameSpot – are now in the <a href="archive.html#screens-2001">Archive</a>, also on the screenshot pages of the 2001 versions. The first Zax page of 1998 shows its small pictures again, scaled down from the Score cover CD pictures, and the screenshot gallery of 2003 has four more pictures, found on jowood.com.'),
             ('11/17/26', 'New in <a href="downloads.html">Downloads</a>: <a href="downloads.html#game">links to the full version</a> of the game in seven languages with a tip for copy protection problems, a <a href="downloads.html#cdkey-generator">CD key generator</a> and a fix pack for the original Russian edition.'),
             ('11/17/26', 'New finds from the Internet Archive: the first Zax page of 1998 and the reflexive.net page of 2003 in the <a href="archive.html">Archive</a>, many more pages and pictures of zax-game.com and jowood.com, and a new <a href="the-game.html">The Game</a> page that brings together everything the developer\'s and the official site said about the game: story, characters, weapons, interface and screenshots.'),
             ('11/16/26', 'New in <a href="downloads.html#official">Downloads</a>: the demo of 1 June 2001, the earliest known build of the game, in 8-bit colour and with still images instead of the intro videos.'),
             ('11/16/26', 'New in the <a href="archive.html#score-1998">Archive</a>: ten early pictures of the game from the cover CD of the Czech magazine <i>Score</i>, issue 59 (November 1998), with the text that came with them.'),
             ('11/14/26', 'This fan site goes online: navigation and fonts rebuilt from the original Flash files of zax-game.com, the original websites restored in the <a href="archive.html">Archive</a>.')]
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
nl_site = box(''.join(f'  <p><span class="date">{d}</span>{t}</p>\n' for d, t in news_site))
nl_dev = box(''.join(f'  <p><span class="date">{d}</span>{t}</p>\n' for d, t in news_orig)
                 + '  <p class="small">News from the official site by Reflexive Entertainment, 2000–2001.</p>', )
nl_logs = box('  <p>Every week the Reflexive team posted what they had been working on – programmers, artists and level designers. Three of these logs have survived: 12/08/00, 12/15/00 and 01/05/01.</p>\n  <p><a href="logs.html">Read the developer logs</a></p>', )
lk = ''
for head, entries in links:
    lk += f'  <h3>{head}</h3>\n  <ul>\n' + ''.join(
        f'    <li><a href="{u}">{n}</a>{" – " + d if d else ""}</li>\n' for u, n, d in entries) + '  </ul>\n'
nl = sections('News & Links', [('site-news', 'Site News', nl_site), ('development-news', 'Development News 2000–2001', nl_dev),
                               ('developer-logs', 'Developer Logs', nl_logs), ('links', 'Links', box(lk))])
page('news-links.html', 'News & Links', 'News & Links', nl, 'news-links.html')

logs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs.json'), encoding='utf-8'))
lg_intro = box('  <p>The weekly logs of the Zax team at Reflexive Entertainment, as published on reflexive.net/Zax. Text unchanged, apart from layout.</p>\n  <p><a href="news-links.html">&larr; back to News &amp; Links</a></p>')
log_secs = []
for l in logs:
    inner = ''
    for sec in l['sections']:
        inner += f'  <h3>{html.escape(sec["name"])}</h3>\n'
        for p in sec['people']:
            inner += f'  <p class="small" style="margin:.6em 0 .2em;color:#fff">{html.escape(p["name"])}</p>\n  <ul>\n' + ''.join(
                f'    <li>{html.escape(i)}</li>\n' for i in p['items']) + '  </ul>\n'
    log_secs.append(('log-' + re.sub(r'\W+', '-', l['date']).strip('-'), f'Log {l["date"]}', box(inner)))
lg = sections('Developer Logs', log_secs, lg_intro)
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
    for n, lang, d in repos))
community_projects = [
 ('https://github.com/zar9roc/ZaxEd', 'ZaxEd', 'A map viewer in the browser, an editor is planned.'),
 ('https://github.com/zar9roc/ZaxHiRes', 'ZaxHiRes', 'A patch for high resolutions.'),
 ('https://github.com/dubstabber/Zax-The-Alien-Hunter-Rebooted', 'Zax – The Alien Hunter Rebooted', 'A remake in Godot 4.'),
 ('https://github.com/dubstabber/Zax-bot', 'Zax-bot', 'Bots for multiplayer.'),
]
pj_c = box('  <p>Projects by other fans.</p>\n' + ''.join(
    f'  <div class="item"><h3><a class="repo" href="{u}">{html.escape(n)}</a></h3><p>{d}</p></div>\n'
    for u, n, d in community_projects))
pj = sections('Projects', [('my-projects', 'My Projects', pj), ('community-projects', 'Community Projects', pj_c)])
page('projects.html', 'Projects', 'Projects', pj, 'projects.html')

# ---------------------------------------------------------------- Archive
ZGA = 'archive/zax-game.com_2004/english/'
def link_list(items): return ', '.join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for u, t in items)
zg_more = ('<br>Pages that were reached through Flash menus that were not preserved: '
    + link_list([(ZGA + 'features.html', 'features'), ('archive/zax-game.com_2004/german/features.html', 'Features (German)'),
             (ZGA + 'heroic/zax.html', 'heroes'), (ZGA + 'enemy/om.html', 'enemies'), (ZGA + 'weapons/laser_welder.html', 'weapons'),
             (ZGA + 'screenshots/00.html', 'screenshots'), (ZGA + 'links_php.html', 'links')])
    + '. All heroes, enemies and weapons are linked from <a href="the-game.html#characters">The Game</a>.')
R4 = 'archive/2003-06_Version4/zax/screenhtms/'
r4_shots = ('<br>Screenshot pages (their overview page was not preserved): '
    + link_list([(R4 + f'ss{n:02d}.htm', f'{n:02d}') for n in range(26) if n not in (3,)] + [(R4 + f'multiplayer%20{n:02d}.htm', f'MP{n:02d}') for n in range(1, 10)]) + '.')
arch = [
 ('archive/1998-12_Version0/zax/zaxintro.html', 'archive/shot_1998-12_Version0.png', 'reflexive.net/Zax – December 1998',
  'The first Zax page of the developer: “Zax, Coming 1999-2000”, with the early story of a soldier of the Galactic Imperium. Only the text was preserved; its ten large pictures – seven illustrations and three screenshots – are the ones found on the <a href="#score-1998">Score cover CD</a>, and its small pictures are scaled down from them; the other images are marked as missing.'),
 ('archive/2001-01_Version1/Zax/index.html', 'archive/shot_2001-01_Version1.png', 'reflexive.net/Zax – January 2001',
  'The developer\'s site during production. Most of the layout graphics were not preserved; missing images are marked. The seven screenshots were not preserved either: they are shown from the same series on GameSpot (5 January 2001), the order is not known.'),
 ('archive/2001-04_Version2/Zax/index.html', 'archive/shot_2001-04_Version2.png', 'reflexive.net/Zax – April 2001',
  'The stone medallion design with Zax and the rune chain. Some frame graphics were not preserved; missing images are marked.'),
 ('archive/2001-12_Version3/Zax/index.html', 'archive/shot_2001-12_Version3.png', 'reflexive.net/Zax – December 2001',
  'The release version with FAQ, demo page and the mirrored navigation.'),
 ('archive/2003-06_Version4/zax.htm', 'archive/shot_2003-06_Version4.png', 'reflexive.net – 2002 to 2003',
  'The short Zax page on the developer\'s site after the release, with FAQ, characters, weapons, demo and the French patch. Of its screenshot gallery seven full-size pictures were preserved; four more are shown from jowood.com, which used the same files.' + r4_shots),
 ('archive/zax-game.com_2004/index_flash.html', 'archive/shot_zax-game.com_gateway.png', 'zax-game.com – 2002 to 2004',
  'The official JoWooD site in English and German. Navigation and banner are the original Flash files, played with the Ruffle emulator. Files that were never archived on zax-game.com come from JoWooD\'s mirror zax.jowood.com.' + zg_more),
 ('archive/jowood.com_2003/gamers/index.html', 'archive/shot_jowood.com_2003.jpg', 'jowood.com – January 2003',
  'The game\'s pages on the publisher\'s site in English and German: the game, screenshots, demo, patches, reviews, system requirements and registration. Links to other JoWooD pages lead to the Internet Archive; the Zax logo was not preserved, the forms are disabled. Screenshots never archived at their own address come from the files of the same name elsewhere on jowood.com.'),
]
ar_intro = box('  <p>Early pictures of the game from a 1998 magazine cover CD and from January 2001, the original websites, restored from copies at the Internet Archive, and the models that were left unused in the game data. The websites are shown as they were – with frames, period HTML and, where noted, Flash. Only archived material is shown: images that were never preserved are marked as missing.</p>')
# Score 59 (CZ, November 1998): Bilder von der Heft-CD (NGF-Format, verlustfrei als PNG). Es sind die zehn großen Bilder der
# reflexive.net-Seite von 1998 (nie archiviert); Reihenfolge und Unterschriften wie dort (sonst die Unterschrift im Bild).
R0 = 'archive/1998-12_Version0/zax/'
score = [('ZAX03', 'Zax discovers a new world', 'Zax640Images/ZaxIllustration.htm'),
         ('ZAX02', 'Zax finds huts of The Korbo.', 'ZaxScreenShots/SSVillage.htm'),
         ('ZAX04', 'Deep underground in the Korbo Cave Temples.', 'ZaxScreenShots/SSCave.htm'),
         ('ZAX05', 'Zax at the gate of Korbo ruins.', 'ZaxScreenShots/SSTemple.htm'),
         ('ZAX06', 'Sentinel at the Temple', 'Zax640Images/Sentinel%20Illustration.htm'),
         ('ZAX07', 'The Crutch', 'Zax640Images/Crutch%20Illustration.htm'),
         ('ZAX01', 'The Throne of Om.', 'Zax640Images/Om%20Illustration.htm'),
         ('ZAX10', 'Malak of the Korbo', 'Zax640Images/Korbo%20Illustration.htm'),
         ('ZAX08', 'The Zelon', 'Zax640Images/Zelon%20Illustration.htm'),
         ('ZAX09', 'The Zelon Interior', 'Zax640Images/Zelon%20Interior%20Illustration.htm')]
ar_score = box(
    '  <p>Ten pictures from the cover CD of the Czech games magazine <i>Score</i>, issue 59 (November 1998) – almost three years before the release. '
    'They are the large pictures of the developer\'s <a href="' + R0 + 'zaxintro.html" target="_blank" rel="noopener">first Zax page</a> on reflexive.net (December 1998): seven illustrations and three early screenshots. '
    'The Internet Archive kept that page, but not these pictures. On the disc they are stored in the NGF image format, which the CD also uses for its other pictures; here they are converted to PNG without loss, in their original size of 640×480.</p>\n'
    '  <div class="gallery renders">\n' + ''.join(
        f'    <figure><a class="pic" href="archive/score_1998-11/{f}.png" target="_blank" rel="noopener">{img(f"archive/score_1998-11/{f}.png", t)}</a>'
        f'<figcaption>{html.escape(t)}</figcaption></figure>\n' for f, t, pg in score) +
    '  </div>\n'
    '  <p>The text that came with the pictures:</p>\n'
    '  <blockquote lang="cs">Velmi nadějně vyhlížející sci-fi adventuru ZAX prezentovali na Internetu před nedávnem marketingoví odborníci firmy Reflexive Entertainment. '
    'Její vydání je sice naplánované až na konec příštího roku,při spatření těch úchvatných renderovaných - a přece tak reálných - obrázků ze hry mi všk srdce napovídá, '
    'že tady by se mohl skrývat jeden z nejpotencionálnějších produktů příští zimy. Když budeme všichni společně věřit a doufat, třeba se ZAX dostane na herní trh dříve '
    'a my tak budeme moci konečně odložit slintátko, uchopit myš a dát se do hraní. Už aby to bylo.</blockquote>\n'
    '  <p class="small">In English: “The very promising-looking sci-fi adventure ZAX was recently presented on the Internet by the marketing experts of Reflexive Entertainment. '
    'Its release is planned for the end of next year, but seeing these stunning rendered – and yet so realistic – pictures from the game, my heart tells me this could be one of the most promising products of next winter. '
    'If we all believe and hope together, maybe ZAX will reach the shops sooner, and we can finally put away the bib, grab the mouse and start playing. Can\'t wait.”</p>',
    )
# Screenshot-Serie Januar 2001: die Bilder ZSS01-07 der reflexive.net-Seite 2001 (nie archiviert), dieselbe Serie wie bei
# GameSpot (First Look, 05.01.2001); eingesetzt von tools/archive/import_screens2001.py. Reihenfolge wie bei GameSpot.
R3 = 'archive/2001-12_Version3/Zax/'
shots2001 = ['Laser maze in a cave', 'Wooden bridge in the jungle', 'Jungle path', 'Fight at the temple statue',
             'Deep in the caves', 'Korbo village with fires', 'Village square']
ar_2001 = box(
    '  <p>Seven early screenshots, with the old status bar: the pictures of the developer\'s <a href="' + R3 + 'Screens.htm" target="_blank" rel="noopener">screenshot page</a> on reflexive.net in 2001. '
    'The Internet Archive kept the page, but not the pictures. The same series was shown by GameSpot in its First Look of 5 January 2001; the pictures here are put together from several copies of it, '
    'without logos (the first still shows GameSpot\'s “G”, no GameSpot copy of the seventh was preserved). The order on the developer\'s page is not known; this is the order of GameSpot.</p>\n'
    '  <div class="gallery renders">\n' + ''.join(
        f'    <figure><a class="pic" href="{R3}Images/BigScreens/ZSS{n:02d}.jpg" target="_blank" rel="noopener">{img(f"{R3}Images/BigScreens/ZSS{n:02d}.jpg", t)}</a>'
        f'<figcaption>{html.escape(t)}</figcaption></figure>\n' for n, t in enumerate(shots2001, 1)) +
    '  </div>')
ar_web = '<div class="cards">\n' + ''.join(
    f'<div class="box card"><p class="title">{t}</p><a href="{u}" target="_blank" rel="noopener">{img(s, t, "shot")}</a><p>{d}</p><p><a href="{u}" target="_blank" rel="noopener">Open</a></p></div>\n'
    for u, s, t, d in arch) + '</div>'
ar = sections('Archive', [('score-1998', 'Score CD Finds 1998', ar_score), ('screens-2001', 'Screenshots January 2001', ar_2001), ('websites', 'Websites', ar_web), ('unused-content', 'Unused Content', uc)], ar_intro)
page('archive.html', 'Archive', 'Archive', ar, 'archive.html')

# ---------------------------------------------------------------- Sitemap (Seite im Menü + sitemap.xml)
def sm_list(items):
    return '<ul>\n' + ''.join(f'<li><a href="{h}">{html.escape(t)}</a>' + (sm_list(c) if c else '') + '</li>\n' for h, t, c in items) + '</ul>\n'
SITEMAP = [
 ('index.html', 'Homepage', []),
 ('the-game.html', 'The Game', [(f'the-game.html#{a}', t, []) for a, t, _ in GAME_SECTIONS]),
 ('downloads.html', 'Downloads', [('downloads.html#game', 'Game downloads – full versions (external links)', []), ('downloads.html#cdkey-generator', 'CD key generator', []), ('downloads.html#community', 'Community downloads – tools, fix packs and language packs', []),
                                   ('downloads.html#official', 'Official downloads – demos and the French patch', []),
                                   ('https://github.com/eggi36/zax-game.com/releases/tag/downloads', 'Release page with all files and checksums', [])]),
 ('news-links.html', 'News & Links', [('news-links.html#site-news', 'Site news', []),
                                       ('news-links.html#development-news', 'Development news 2000–2001', []),
                                       ('logs.html', 'Developer logs', [('logs.html#log-' + re.sub(r'\W+', '-', l['date']).strip('-'), 'Log ' + l['date'], []) for l in logs]),
                                       ('news-links.html#links', 'Links', [])]),
 ('projects.html', 'Projects', [('projects.html#my-projects', 'My projects', []), ('projects.html#community-projects', 'Community projects', [])]),
 ('archive.html', 'Archive', [('archive.html#score-1998', 'Finds from the Score cover CD – 1998', []), ('archive.html#screens-2001', 'Screenshots of January 2001', [])] + [(u, t, []) for u, s_, t, d in arch]
                              + [('archive/jowood.com_2003/gamers/index_de.html', 'jowood.com – January 2003, German pages', [])]
                              + [('archive.html#unused-content', 'Unused Content – models the game never uses', [])]),
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
    'mission-briefing.html': 'the-game.html#story', 'profiles.html': 'the-game.html#characters',
    'weapons.html': 'the-game.html#weapons',
    'index_flash.html': 'index.html', 'index_no_flash.html': 'index.html', 'gateway.html': 'index.html',
    **{f'english/{p}.html': 'index.html' for p in ('index', 'homepage', 'top_nav', 'top_secret')},
    **{f'english/{p}.html': 'the-game.html#story' for p in ('mission_briefing', 'missionb_nav', 'story', 'mission_shots')},
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

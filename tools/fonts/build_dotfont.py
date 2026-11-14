"""Erzeugt die Webschrift 'Zelon Dots' aus der Punktmatrix-Schrift von zax-game.com (top_nav.swf, Font 12)
und ergänzt fehlende Zeichen im selben 5x5-Raster."""
import json, math, os
HERE=os.path.dirname(os.path.abspath(__file__))
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
G=json.load(open(os.path.join(HERE,'dotfont_grid.json')))
SX,SY=G['SX'],G['SY']; X0=G['X0']; TOP=-G['Y0']      # Mitte der obersten Punktreihe über der Grundlinie
R=70                                                 # Punktradius (gemessen an den Kurvenpunkten der Original-Glyphen)
orig={k:v for k,v in json.load(open(os.path.join(HERE,'dotfont_bitmaps.json'))).items()}
def B(s): return [[1 if c=='#' else 0 for c in row] for row in s.split('/')]
new={
 'J':B('....#/....#/....#/#...#/.###.'),
 'Q':B('.###./#...#/#.#.#/#..#./.##.#'),
 'V':B('#...#/#...#/#...#/.#.#./..#..'),
 'X':B('#...#/.#.#./..#../.#.#./#...#'),
 'Y':B('#...#/.#.#./..#../..#../..#..'),
 'C':B('.####/#..../#..../#..../.####'),   # nur falls nicht vorhanden
 'Z':B('#####/...#./..#../.#.../#####'),
 '0':B('.###./#..##/#.#.#/##..#/.###.'),
 '1':B('.#./##./.#./.#./###'),
 '2':B('####./....#/.###./#..../#####'),
 '3':B('####./....#/.###./....#/####.'),
 '4':B('#..#./#..#./#####/...#./...#.'),
 '5':B('#####/#..../####./....#/####.'),
 '6':B('.###./#..../####./#...#/.###.'),
 '7':B('#####/...#./..#../.#.../.#...'),
 '8':B('.###./#...#/.###./#...#/.###.'),
 '9':B('.###./#...#/.####/....#/.###.'),
 '.':B('./././././#'.replace('/','/',)) if False else B('././././#'),
 ',':B('./././#/#'),
 ':':B('./#/./#/.'),
 ';':B('./#/./#/#'),
 '!':B('#/#/#/./#'),
 '?':B('###./...#/.##./..../.#..'),
 '-':B('.../.../###/.../...'),
 '+':B('.../.#./###/.#./...'),
 "'":B('#/#/./././'.rstrip('/')),
 '"':B('#.#/#.#/.../.../...'),
 '/':B('....#/...#./..#../.#.../#....'),
 '(':B('.#/#./#./#./.#'),
 ')':B('#./.#/.#/.#/#.'),
 '_':B('...../...../...../...../#####'),
 '#':B('.#.#./#####/.#.#./#####/.#.#.'),
 '>':B('#../.#./..#/.#./#..'),
 '<':B('..#/.#./#../.#./..#'),
 '=':B('.../###/.../###/...'),
 '%':B('#...#/...#./..#../.#.../#...#'),
}
glyphs={}
for k,v in orig.items(): glyphs[k]=v
for k,v in new.items():
  if k not in glyphs: glyphs[k]=v
# Umlaute: Grundbuchstabe + zwei Punkte eine Reihe darüber
for u,base in [('Ä','A'),('Ö','O'),('Ü','U')]:
  glyphs[u]=[[0,1,0,1,0]]+glyphs[base]
glyphs['ß']=B('###./#..#/#.#./#..#/#.##.')
glyphs['·']=B('./././#/.')
def advance(w): return round(956-(5-w)*155.5)
fb=FontBuilder(1024,isTTF=True)
names=['.notdef','space']+[f'g{ord(c):04X}' for c in glyphs]
fb.setupGlyphOrder(names)
cmap={32:'space'}
for c in glyphs:
  cmap[ord(c)]=f'g{ord(c):04X}'
  if c.isalpha() and c.lower()!=c and ord(c.lower())<0x250: cmap[ord(c.lower())]=f'g{ord(c):04X}'
fb.setupCharacterMap(cmap)
def circle(pen,cx,cy,r):
  n=8; k=r/math.cos(math.pi/n)
  pts=[(cx+r*math.cos(2*math.pi*i/n),cy+r*math.sin(2*math.pi*i/n)) for i in range(n)]
  ctl=[(cx+k*math.cos(2*math.pi*(i+.5)/n),cy+k*math.sin(2*math.pi*(i+.5)/n)) for i in range(n)]
  pen.moveTo((round(pts[0][0]),round(pts[0][1])))
  for i in range(n):
    pen.qCurveTo((round(ctl[i][0]),round(ctl[i][1])),(round(pts[(i+1)%n][0]),round(pts[(i+1)%n][1])))
  pen.closePath()
gl={}; metrics={}
p=TTGlyphPen(None); p.moveTo((0,0)); p.lineTo((0,700)); p.lineTo((500,700)); p.lineTo((500,0)); p.closePath(); gl['.notdef']=p.glyph(); metrics['.notdef']=(600,0)
gl['space']=TTGlyphPen(None).glyph(); metrics['space']=(495,0)
for c,bm in glyphs.items():
  pen=TTGlyphPen(None); rows=len(bm); extra=rows-5  # Umlaute: eine Reihe mehr oben
  w=max(len(r) for r in bm)
  for ri,row in enumerate(bm):
    for ci,v in enumerate(row):
      if v:
        cx=X0+ci*SX; cy=TOP-(ri-extra)*SY
        circle(pen,cx,cy,R)
  gl[f'g{ord(c):04X}']=pen.glyph(); metrics[f'g{ord(c):04X}']=(advance(w),0)
fb.setupGlyf(gl); fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=1000,descent=-120)
fb.setupNameTable({'familyName':'Zelon Dots','styleName':'Regular','copyright':'Glyphen nach der Flash-Navigation von zax-game.com (JoWooD/Reflexive 2001); ergänzt für ein Fan-Projekt'})
fb.setupOS2(sTypoAscender=1000,sTypoDescender=-120,usWinAscent=1000,usWinDescent=120)
fb.setupPost()
fb.save('ZelonDots.ttf')
fb.font.flavor='woff'; fb.font.save('ZelonDots.woff')
json.dump({'original':sorted(orig),'neu':sorted(set(glyphs)-set(orig))},open('glyphs.json','w'),ensure_ascii=False,indent=1)
print('Zeichen:',''.join(sorted(glyphs)))

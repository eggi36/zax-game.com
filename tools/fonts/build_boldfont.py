"""Erzeugt die Webschrift 'Zelon Bold' aus Font 1 der Flash-Navigation von zax-game.com.
Originalglyphen als Vektoren; J, Q, Ö, Ü aus Originalteilen; Ziffern/Satzzeichen aus DejaVu Sans Condensed Bold angepasst."""
import json, math, os, numpy as np, cv2
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'..','..','assets','fonts')
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
G=json.load(open(os.path.join(HERE,'font1_glyphs.json'))); ADV=json.load(open(os.path.join(HERE,'font1_adv.json')))
CAP=729
def contours_of(paths):
  """SWF-Pfade -> Liste von Konturen [(typ,pts...)] in TT-Koordinaten (y nach oben)"""
  out=[]
  for p in paths:
    segs=[]
    for c in p:
      if c[0]=='M': start=(c[1],-c[2]); segs=[('M',start)]
      elif c[0]=='L': segs.append(('L',(c[1],-c[2])))
      else: segs.append(('Q',(c[1],-c[2]),(c[3],-c[4])))
    out.append(segs)
  return out
def flatten(segs,n=8):
  pts=[segs[0][1]]; cur=segs[0][1]
  for s in segs[1:]:
    if s[0]=='L': pts.append(s[1]); cur=s[1]
    else:
      (cx,cy),(ax,ay)=s[1],s[2]
      for i in range(1,n+1):
        t=i/n; pts.append(((1-t)**2*cur[0]+2*(1-t)*t*cx+t*t*ax,(1-t)**2*cur[1]+2*(1-t)*t*cy+t*t*ay))
      cur=s[2]
  return np.array(pts)
def area(poly): x,y=poly[:,0],poly[:,1]; return 0.5*np.sum(x*np.roll(y,-1)-np.roll(x,-1)*y)
def inside(pt,poly): return cv2.pointPolygonTest(poly.astype(np.float32).reshape(-1,1,2),(float(pt[0]),float(pt[1])),False)>0
def reverse(segs):
  # Kontur umkehren
  pts=[segs[0][1]]; kinds=[]
  for s in segs[1:]:
    kinds.append(s); 
  # Liste der Punkte mit Segmenttyp
  nodes=[('M',segs[0][1])]
  out=[]; cur=segs[0][1]; items=[]
  for s in segs[1:]:
    if s[0]=='L': items.append(('L',cur,s[1])); cur=s[1]
    else: items.append(('Q',cur,s[1],s[2])); cur=s[2]
  rev=[('M',cur)]
  for it in reversed(items):
    if it[0]=='L': rev.append(('L',it[1]))
    else: rev.append(('Q',it[2],it[1]))
  return rev
def oriented(conts):
  polys=[flatten(c) for c in conts]; res=[]
  for i,c in enumerate(conts):
    depth=sum(1 for j,q in enumerate(polys) if j!=i and inside(polys[i][0],q))
    a=area(polys[i])
    want_cw=(depth%2==0)          # TrueType: außen im Uhrzeigersinn
    is_cw=a<0
    res.append(c if is_cw==want_cw else reverse(c))
  return res
def draw(pen,conts,dx=0,sx=1):
  for c in conts:
    pen.moveTo((round(c[0][1][0]*sx+dx),round(c[0][1][1])))
    for s in c[1:]:
      if s[0]=='L': pen.lineTo((round(s[1][0]*sx+dx),round(s[1][1])))
      else: pen.qCurveTo((round(s[1][0]*sx+dx),round(s[1][1])),(round(s[2][0]*sx+dx),round(s[2][1])))
    pen.closePath()
# ---------- Raster-Hilfen für J, Q ----------
S=1  # 1 Einheit = 1 px
def raster(conts,W=1200,H=1300,ox=50,oy=1100):
  img=np.zeros((H,W),np.uint8)
  for c in conts:
    poly=flatten(c,16); pts=np.c_[poly[:,0]+ox, oy-poly[:,1]].astype(np.int32)
    tmp=np.zeros_like(img); cv2.fillPoly(tmp,[pts],255); img^=tmp
  return img
def vectorize(img,ox=50,oy=1100):
  cs,hier=cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
  out=[]
  for c,h in zip(cs,hier[0]):
    c=cv2.approxPolyDP(c,1.2,True).reshape(-1,2).astype(float)
    pts=np.c_[c[:,0]-ox, oy-c[:,1]]
    segs=[('M',tuple(pts[0]))]+[('L',tuple(p)) for p in pts[1:]]
    out.append(segs)
  return oriented(out)
base={k:oriented(contours_of(v)) for k,v in G.items() if k not in ('\x85',)}
glyph_conts=dict(base); adv=dict(ADV)
# J: aus U – linken Schaft oben entfernen, unten kurzen Haken lassen
U=raster(base['U']); j=U.copy(); ox,oy=50,1100
j[0:oy-260, ox+0:ox+60+173+2]=0
cs=vectorize(j); 
# nach links schieben
xs=[p[1][0] for c in cs for p in c]; shift=40-min(xs)
cs=[[ (s[0],(s[1][0]+shift,s[1][1])) for s in c] for c in cs]
glyph_conts['J']=cs; adv['J']=round(595+shift+60)
# Q: O plus schräger Strich unten rechts
O=raster(base['O']); q=O.copy()
p1=(ox+380,oy-210); p2=(ox+640,oy+70)
cv2.line(q,p1,p2,255,int(173*0.9))
q[oy+75:,:]=0
glyph_conts['Q']=vectorize(q); adv['Q']=700
# Ö, Ü: Punkte von Ä übernehmen
dots=[c for c in base['Ä'] if min(p[1][1] for p in c)>CAP+10]
def shifted(conts,dx): return [[(s[0],)+tuple((pt[0]+dx,pt[1]) for pt in s[1:]) for s in c] for c in conts]
glyph_conts['Ö']=base['O']+shifted(dots,(586+49)/2-648/2)
glyph_conts['Ü']=base['U']+shifted(dots,(595+60)/2-648/2)
adv['Ö']=adv['O']; adv['Ü']=adv['U']
# ---------- Ziffern / Satzzeichen aus DejaVu Sans Condensed Bold ----------
dv=TTFont('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'); dgs=dv.getGlyphSet(); dcmap=dv.getBestCmap()
dcap=1493; sc=CAP/dcap
extra='0123456789-:/!?()+\'"#%_;<>=ß@*'
fb=FontBuilder(1024,isTTF=True)
chars=sorted(set(glyph_conts)|set(extra)|{' '})
names=['.notdef']+['space' if c==' ' else f'u{ord(c):04X}' for c in chars if c!=' ']+['space']
names=list(dict.fromkeys(names))
fb.setupGlyphOrder(names)
cmap={}
for c in chars:
  n='space' if c==' ' else f'u{ord(c):04X}'; cmap[ord(c)]=n
  if c.isalpha() and c.lower()!=c: cmap[ord(c.lower())]=n
fb.setupCharacterMap(cmap)
glyf={}; met={}
p=TTGlyphPen(None); p.moveTo((50,0)); p.lineTo((50,700)); p.lineTo((450,700)); p.lineTo((450,0)); p.closePath(); glyf['.notdef']=p.glyph(); met['.notdef']=(500,0)
glyf['space']=TTGlyphPen(None).glyph(); met['space']=(adv.get(' ',220),0)
for c in chars:
  if c==' ': continue
  n=f'u{ord(c):04X}'; pen=TTGlyphPen(None)
  if c in glyph_conts:
    draw(pen,glyph_conts[c]); 
    xs=[pt[0] for cc in glyph_conts[c] for s in cc for pt in s[1:]]
    met[n]=(adv.get(c, round(max(xs)+60)),0)
  else:
    dn=dcmap[ord(c)]; g=dgs[dn]
    tp=TransformPen(pen,(sc*0.92,0,0,sc,0,0)); g.draw(tp)
    met[n]=(round(g.width*sc*0.92),0)
  glyf[n]=pen.glyph()
fb.setupGlyf(glyf); fb.setupHorizontalMetrics(met)
fb.setupHorizontalHeader(ascent=960,descent=-200)
fb.setupNameTable({'familyName':'Zelon Bold','styleName':'Regular','copyright':'Glyphen nach der Flash-Navigation von zax-game.com (2001); Ziffern/Satzzeichen nach DejaVu Sans Condensed Bold (Bitstream Vera Lizenz); Fan-Projekt'})
fb.setupOS2(sTypoAscender=960,sTypoDescender=-200,usWinAscent=1000,usWinDescent=220)
fb.setupPost()
fb.save(os.path.join(OUT,'ZelonBold.ttf')); fb.font.flavor='woff'; fb.font.save(os.path.join(OUT,'ZelonBold.woff'))
print(''.join(c for c in chars))

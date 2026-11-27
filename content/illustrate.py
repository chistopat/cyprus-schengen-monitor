from PIL import Image, ImageDraw, ImageFont
import numpy as np, json, math, argparse
from scipy.ndimage import distance_transform_edt, gaussian_filter, zoom
from pathlib import Path
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--language',choices=['ru','en','el'],default='ru')
lang=parser.parse_args().language
labels={
 'ru':['К И П Р','Средиземное море','Никосия','Пафос','Ларнака','С','50 км'],
 'en':['C Y P R U S','Mediterranean Sea','Nicosia','Paphos','Larnaca','N','50 km'],
 'el':['Κ Υ Π Ρ Ο Σ','Μεσόγειος Θάλασσα','Λευκωσία','Πάφος','Λάρνακα','Β','50 χλμ.']
}[lang]
W,H=1400,800
rng=np.random.default_rng(311)
scale=477
def xy(lon,lat): return (int((lon-33.43)*scale+W*.49),int((35.14-lat)*scale/.818+H*.49))
coords=json.loads((root/'content/island.json').read_text())['coordinates'][0]
mask=Image.new('L',(W,H))
ImageDraw.Draw(mask).polygon([xy(*p[:2]) for p in coords],fill=255)
land=np.asarray(mask)>0
y,x=np.mgrid[:H,:W]
lon=(x-W*.49)/scale+33.43; lat=35.14-(y-H*.49)*.818/scale
def noise(freq):
 a=rng.standard_normal((max(3,int(freq*H/W)),freq))
 im=Image.fromarray(a.astype('float32')).resize((W,H),Image.Resampling.BICUBIC)
 return np.asarray(im)
micro=noise(115); small=noise(55); med=noise(26); large=noise(12)
grain=rng.normal(0,2.8,(H,W))
d=distance_transform_edt(~land)
dl=distance_transform_edt(land)
# Subtle plate tone, concentric coastline engraving and paper tooth.
paper=np.stack([np.full((H,W),v) for v in [220.,226.,205.]],axis=-1)
sea_stain=3.7*large+1.8*med+1.3*micro+grain
sea_stain+=6*(x/W-.5)-.7*small
edgefade=np.clip(d/120,0,1)
wave=np.minimum.reduce([abs(d-(g+.75*small+.6*med)) for g in [5,10,16,23,31,41,53,67,82,100,121,145,171]])
sea_stain-=20*np.exp(-wave**2/1.1)*np.exp(-d/86)
paper+=sea_stain[:,:,None]
paper+=np.array([-3,-2,0])[None,None,:]*(1-edgefade[:,:,None])
# Line engraving for the two mountain belts; relief is illustrative.
troodos=np.exp(-(((lon-32.91)/.47)**2+((lat-34.91+.10*(lon-32.91))/.161)**2))
kyrenia=np.exp(-((lat-(35.33+.17*(lon-33.35)))/.048)**2-((lon-33.67)/.64)**2)
h=(troodos*.94+kyrenia*.84)*(.85+.11*large+.17*med+.12*small+.082*micro+.035*noise(210))
gy,gx=np.gradient(gaussian_filter(h,1))
rel=np.clip((gy*1.6+gx)*850,-28,28)
ink=12*np.clip(h,0,1.6)+rel
# Fine engraved hatching follows the relief and fades into the coastal plain.
strokes=np.exp(-((np.sin((y*.80+x*.29+4.5*small+7*med+h*62)*.90))/.38)**2)
ink+=strokes*(6+20*np.clip(h,0,1))+5*np.exp(-((np.sin(h*117))/.31)**2)*np.clip(h,0,1)
tint=grain+.9*micro+2.8*med+2.1*large-ink
isle=np.array([226.,210.,162.])[None,None,:]+tint[:,:,None]
coast=24*np.exp(-((dl-1.0)/1.45)**2)+8*np.exp(-((dl-5)/1.25)**2)
isle-=coast[:,:,None]
paper[land]=isle[land]
im=Image.fromarray(np.clip(paper,0,255).astype('uint8')).convert('RGBA')
overlay=Image.new('RGBA',im.size); draw=ImageDraw.Draw(overlay)
for lng in np.arange(31.5,36,.25):
 px,_=xy(lng,35)
 col=(71,94,72,42 if lng%1==0 else 19)
 draw.line((px,0,px,H),fill=col,width=1)
for lt in np.arange(33,37,.25):
 _,py=xy(33,lt);draw.line((0,py,W,py),fill=(71,94,72,42 if lt%1==0 else 19),width=1)
im=Image.alpha_composite(im,overlay);draw=ImageDraw.Draw(im)
def font(name,size):
 linux=Path('/usr/share/fonts')/name
 mac={'opentype/urw-base35/NimbusRoman-Regular.otf':'Times New Roman.ttf','opentype/urw-base35/NimbusRoman-Italic.otf':'Times New Roman Italic.ttf','truetype/dejavu/DejaVuSansMono.ttf':'Courier New.ttf','truetype/liberation/LiberationSans-Regular.ttf':'Arial.ttf'}
 return ImageFont.truetype(str(linux if linux.exists() else Path('/System/Library/Fonts/Supplemental')/mac[name]),size)
roman='opentype/urw-base35/NimbusRoman-Regular.otf'
italic='opentype/urw-base35/NimbusRoman-Italic.otf'
mono='truetype/dejavu/DejaVuSansMono.ttf'
sans='truetype/liberation/LiberationSans-Regular.ttf'
def spaced(txt,pos,size,spacing,face,color):
 f=font(face,size); lengths=[draw.textlength(c,font=f) for c in txt]; total=sum(lengths)+spacing*(len(txt)-1)
 px,py=pos;px-=total/2
 for c,adv in zip(txt,lengths):
  draw.text((px,py),c,font=f,fill=color,anchor='lm');px+=adv+spacing
spaced(labels[0],xy(33.12,35.015),41,4,roman,'#605c3c')
spaced(labels[1],(W*.65,H*.82),30,2.2,italic,'#687d71')
for txt,lon0,lat0,dx,dy in [(labels[2],33.38,35.185,9,-21),(labels[3],32.42,34.78,-15,19),(labels[4],33.62,34.92,15,12)]:
 px,py=xy(lon0,lat0); r=7 if txt==labels[2] else 5
 draw.ellipse((px-r-2,py-r-2,px+r+2,py+r+2),fill='#f0e6bd')
 draw.ellipse((px-r,py-r,px+r,py+r),fill='#805534' if txt==labels[2] else '#545e47')
 draw.text((px+dx,py+dy),txt,font=font(sans,23),fill='#333e30',anchor='rm' if dx<0 else 'lm',stroke_width=2,stroke_fill='#dfd9b9')
# Compass rose, scale and border ticks.
cx,cy=W-95,108
draw.ellipse((cx-30,cy-30,cx+30,cy+30),outline='#71806a',width=1)
for i in range(8):
 a=i*math.pi/4-math.pi/2
 radius=47 if i%2==0 else 24
 width=7 if i%2==0 else 4
 tip=(cx+math.cos(a)*radius,cy+math.sin(a)*radius)
 left=(cx-math.sin(a)*width,cy+math.cos(a)*width);right=(2*cx-left[0],2*cy-left[1])
 draw.polygon([tip,(cx,cy),left],fill='#53624e');draw.polygon([tip,(cx,cy),right],fill='#b9bda0',outline='#62715c')
draw.text((cx,cy-55),labels[5],font=font(roman,22),fill='#4c5b4e',anchor='mb')
xx,yy=47,H-54;sc=int(50/(111.2*.818)*scale)
for i in range(4):
 draw.rectangle((xx+sc*i/4,yy,xx+sc*(i+1)/4,yy+5),fill='#5d6957' if i%2==0 else '#ece9d3',outline='#687660',width=1)
draw.text((xx,yy-9),'0',font=font(mono,16),fill='#4d604e',anchor='lb')
draw.text((xx+sc,yy-9),labels[6],font=font(mono,16),fill='#4d604e',anchor='rb')
for lng in [32.5,33,33.5,34,34.5]:
 px,_=xy(lng,35)
 if 30<px<W-30:
  draw.line((px,0,px,10),fill='#849780',width=2)
  label=('%g'%lng).replace('.5','°30′')+('°' if lng%1==0 else '')
  draw.text((px,H-12),label,font=font(mono,15),fill='#6b7e6a',anchor='mb')
for lt in [34.5,35,35.5]:
 _,py=xy(33,lt);draw.line((0,py,11,py),fill='#849780',width=2)
im.convert('RGB').save(root/('dist/assets/cyprus-atlas'+('' if lang=='ru' else '-'+lang)+'.webp'),quality=88,method=6)

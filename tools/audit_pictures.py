"""Contact sheets that pair every picture with its page title, branch and era, so a person (or Claude) can
check that each picture matches its title. Usage: python3 tools/audit_pictures.py [outdir]
Entries without a picture and variants are included. Open the sheets and compare tile by tile."""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
OUT=sys.argv[1] if len(sys.argv)>1 else '/tmp/audit'; os.makedirs(OUT,exist_ok=True)
IM='app/src/main/assets/images/'
d=json.load(open('app/src/main/assets/data/entries.json'))['entries']
tiles=[]
for e in d:
    br=','.join(b[:3] for b in e['branches'])
    tiles.append((e['id'],e['name'],br,e.get('image')))
    for v in e.get('variants',[]):
        if v.get('image'): tiles.append((e['id']+':'+v['label'],e['name']+' / '+v['label'],br,v['image']))
COLS,ROWS,TW,TH=6,4,250,190
try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
except Exception: F=ImageFont.load_default()
per=COLS*ROWS; n=0
for s in range(0,len(tiles),per):
    sh=Image.new('RGB',(COLS*TW,ROWS*(TH+46)),'#202020'); dr=ImageDraw.Draw(sh)
    for k,(i,name,br,img) in enumerate(tiles[s:s+per]):
        x=(k%COLS)*TW; y=(k//COLS)*(TH+46)
        try:
            im=Image.open(IM+img).convert('RGB'); im.thumbnail((TW-8,TH-4)); sh.paste(im,(x+4,y+2))
        except Exception: dr.text((x+10,y+80),'NO PICTURE' if not img or img=='none' else 'MISSING FILE',fill='#888',font=F)
        dr.text((x+4,y+TH),name[:40],fill='#ffd84d',font=F)
        dr.text((x+4,y+TH+15),(name[40:80] if len(name)>40 else '')+'',fill='#ffd84d',font=F)
        dr.text((x+4,y+TH+30),f'{i[:26]} | {br}',fill='#9fb0c9',font=F)
    sh.save(f'{OUT}/audit_{n:02d}.png'); n+=1
print(len(tiles),'tiles',n,'sheets in',OUT)

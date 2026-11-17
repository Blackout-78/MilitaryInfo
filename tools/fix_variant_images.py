"""Give variants their own picture, or an explicit blank, so a variant page never shows the parent's picture by mistake."""
import json
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); by={e['id']:e for e in d['entries']}
def setv(i,label,img):
    for v in by[i]['variants']:
        if v['label']==label: v['image']=img
NONE='none'
setv('u-woodland-bdu','Woodland BDU (four-color)','badges/u-woodland-bdu.png')
setv('u-woodland-bdu','Desert BDU (six-color)',NONE)
setv('u-pinks-greens','WWII officer service combination','badges/u-pinks-greens.png')
setv('u-pinks-greens','Army Green Service Uniform','badges/u-agsu.png')
setv('m-dev-star','Bronze service star','badges/m-dev-star.png')
setv('m-dev-star','Silver service star','badges/m-dev-star-silver.png')
setv('m-dev-olc','Bronze oak leaf cluster',NONE)
setv('m-dev-olc','Silver oak leaf cluster',NONE)
setv('u-asu','Male','badges/u-asu.png')
setv('u-asu','Female',NONE)
# note on the desert BDU: no free picture of the six-color pattern found yet
e=by['u-woodland-bdu']
t='UNVERIFIED: the Desert BDU (six-color) variant has no source and no picture yet; the page shows a blank rather than the woodland photo'
if t not in e['facts']: e['facts'].append(t)
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False)

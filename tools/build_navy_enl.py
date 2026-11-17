import json
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); by={e['id']:e for e in d['entries']}
SRC='U.S. Navy Uniform Regulations (NAVPERS 15665 series), Chapter 4, mynavyhr.navy.mil, article '
ED=' (web page read 17 Nov 2026; the page does not state its edition)'
U='UNVERIFIED, not stated in the regulation text (figures only): '
def upd(i,add,art,unv):
    e=by[i]
    keep=[f for f in e['facts'] if f.startswith(('Grade','Insignia'))]
    e['facts']=keep+add+[U+unv]
    e['sources']=[SRC+art+ED]+[s for s in e['sources'] if 'Rank names' in s]
cpo=['Rating badge: perched eagle, wings raised, head turned to the right, on a pentagonal background; chevrons, rocker and stars as authorized show the rate, and a specialty mark shows the rating (art. 4211)',
 'Chevrons on CPO rating badges are 3-1/4 inches wide for men (art. 4211)',
 'On Service Dress Blue and Dinner Dress Blue Jacket the eagle, specialty mark and stars are silver on navy blue; on the Dinner Dress White Jacket the background is white (art. 4211)']
for i,star in [('n-e7',''),('n-e8','Collar anchor carries one, two or three silver stars for Senior Chief, Master Chief and MCPON (art. 4211); which rank wears which count is not in the text. '),('n-e9','Collar anchor carries one, two or three silver stars for Senior Chief, Master Chief and MCPON (art. 4211); which rank wears which count is not in the text. ')]:
    upd(i,cpo+([star.strip()] if star else []),'4211','number of chevrons, rockers and stars for this grade')
po=['Rating badge on the left sleeve, centered between the shoulder seam and the elbow (art. 4221)',
    'Background: navy blue on navy uniforms; the badge colors follow a per-uniform chart; on the peacoat the eagle is white and the chevrons are cardinal (art. 4221)']
for i in ['n-e4','n-e5','n-e6']:
    upd(i,po,'4221','number of chevrons for this grade and the eagle pose')
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False)

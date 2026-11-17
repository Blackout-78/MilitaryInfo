"""Coverage matrix for MilitaryInfo: branch x era per tab, plus pictures and proof. Usage: python3 tools/coverage.py"""
import json,collections
d=json.load(open('app/src/main/assets/data/entries.json'));es=d['entries']
B=['Army','Navy','Marine Corps','Air Force','Space Force','Coast Guard']
E=['ww1','interwar','ww2','korea','vietnam','coldwar','gulf','modern']
WANT={'uniforms':'dress, service, mess, utility/BDU/camo, flight, PT, per era',
      'medals':'decorations, service medals, unit awards, ribbons, devices',
      'badges':'combat, skill, qualification, identification, marksmanship, warfare',
      'ranks':'enlisted, warrant, officer, per era; unit/SSI patches'}
print('entries',len(es),'dataVersion',d.get('dataVersion'))
print('era order',E)
for t in WANT:
    print('\n==',t,'| need:',WANT[t])
    for b in B:
        sub=[e for e in es if e['tab']==t and b in e['branches']]
        row=[sum(1 for e in sub if x in e['eras']) for x in E]
        pic=sum(1 for e in sub if e.get('image')); unv=sum(1 for e in sub if e['proof']!='official')
        print(f'{b:13}{row} total {len(sub):3} pics {pic:3} unverified {unv:3} no-era {sum(1 for e in sub if not e["eras"])}')
print('\nno picture:',collections.Counter(e['tab'] for e in es if not e.get('image')))
print('EMPTY cells (tab,branch,era):')
for t in WANT:
    for b in B:
        z=[x for x in E if not any(e['tab']==t and b in e['branches'] and x in e['eras'] for e in es)]
        if z: print(' ',t,b,z)

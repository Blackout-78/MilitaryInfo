"""Text cards for entries with no accurate free picture. Shows only the entry's own name, branch and first summary sentence."""
import json, os, subprocess, textwrap
from xml.sax.saxutils import escape
P='app/src/main/assets/data/entries.json'; OUT='app/src/main/assets/images/badges'; TMP='/tmp/cards'; os.makedirs(TMP,exist_ok=True)
d=json.load(open(P)); n=0
for e in d['entries']:
    im=e.get('image')
    if im=='none': continue
    if im and os.path.exists('app/src/main/assets/images/'+im): continue
    k=e['id']; first=(e.get('summary') or '').split('. ')[0][:170]
    name=textwrap.wrap(e['name'],26)[:3]; body=textwrap.wrap(first,44)[:4]
    t=''.join(f'<text x="200" y="{70+i*26}" font-size="22" font-weight="700" fill="#e6edf7" text-anchor="middle">{escape(l)}</text>' for i,l in enumerate(name))
    y0=70+len(name)*26+14
    t+=f'<text x="200" y="{y0}" font-size="13" fill="#9fb0c9" text-anchor="middle">{escape(", ".join(e.get("branches",[])))}</text>'
    t+=''.join(f'<text x="200" y="{y0+28+i*18}" font-size="13" fill="#c9d4e6" text-anchor="middle">{escape(l)}</text>' for i,l in enumerate(body))
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="384" viewBox="0 0 400 300" font-family="DejaVu Sans, Arial, sans-serif"><rect width="400" height="300" fill="#1b2230"/>'
         f'<rect x="12" y="12" width="376" height="276" rx="12" fill="none" stroke="#4a5c80" stroke-width="2" stroke-dasharray="8 6"/>{t}'
         f'<text x="200" y="280" font-size="12" fill="#9fb0c9" text-anchor="middle">NO PICTURE AVAILABLE - TEXT CARD</text></svg>')
    open(f'{TMP}/{k}.svg','w').write(svg)
    subprocess.check_call(['rsvg-convert','-w','512',f'{TMP}/{k}.svg','-o',f'{OUT}/{k}.png'])
    e['image']=f'badges/{k}.png'; n+=1
    open('CREDITS.md','a').write(f'| {k} | Own text card (tools/make_cards.py) | CC0 | |\n')
json.dump(d,open(P,'w'),indent=2,ensure_ascii=False); print(n,'cards')

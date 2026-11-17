"""Draw schematic illustrations (not official artwork) from the wording of official manuals.
Each picture shows ONLY elements named in the manual text, carries the caption 'ILLUSTRATION - NOT OFFICIAL',
and is credited as own work, CC0. Output: app/src/main/assets/images/badges/<id>.png (512 px wide)."""
import math, os, subprocess, json, sys
OUT='app/src/main/assets/images/badges'
TMP='/tmp/illus'; os.makedirs(TMP,exist_ok=True)
GOLD='#d4a72c'; GOLD2='#f2d36b'; GOLDD='#8c6a12'; PEW='#9aa3ad'; PEWD='#5d6670'; PEWL='#cfd5db'; SIL='#d9dde2'
NAVY='#1f3a6e'; RED='#b3202b'; BG='#1b2230'
def star(cx,cy,r,fill,stroke='none',n=5,inner=0.4,rot=-90):
    pts=[]
    for i in range(n*2):
        a=math.radians(rot+i*180/n); rr=r if i%2==0 else r*inner
        pts.append(f'{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def wings(cx,cy,span,color,dark):
    s=''
    for sgn in (-1,1):
        for k in range(4):
            y0=cy-18+k*9; L=span*(1-0.12*k)
            x1=cx+sgn*L; 
            s+=f'<path d="M{cx+sgn*30},{y0-6} Q{cx+sgn*L*0.6},{y0-24-k*2} {x1},{y0-2+k*3} Q{cx+sgn*L*0.6},{y0+10} {cx+sgn*30},{y0+8} Z" fill="{color}" stroke="{dark}" stroke-width="2"/>'
    return s
def shield(cx,cy,w,h,fill=SIL,stroke=NAVY,stripes=True):
    x=cx-w/2; y=cy-h/2
    d=f'M{x},{y} H{x+w} V{y+h*0.55} Q{x+w},{y+h} {cx},{y+h} Q{x},{y+h} {x},{y+h*0.55} Z'
    s=f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
    s+=f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h*0.22}" fill="{NAVY}"/>'
    if stripes:
        for i in range(1,5): s+=f'<line x1="{x+i*w/5}" y1="{y+h*0.24}" x2="{x+i*w/5}" y2="{y+h*0.88}" stroke="{RED}" stroke-width="3"/>'
    return s
def anchor(cx,cy,s,color,dark,tilt=0):
    g=f'<g transform="rotate({tilt} {cx} {cy})" stroke="{dark}" stroke-width="2" fill="{color}">'
    g+=f'<circle cx="{cx}" cy="{cy-s}" r="{s*0.16}" fill="none" stroke="{color}" stroke-width="{s*0.07}"/>'
    g+=f'<rect x="{cx-s*0.05}" y="{cy-s*0.85}" width="{s*0.1}" height="{s*1.8}"/>'
    g+=f'<rect x="{cx-s*0.4}" y="{cy-s*0.6}" width="{s*0.8}" height="{s*0.09}"/>'
    g+=f'<path d="M{cx-s*0.7},{cy+s*0.3} Q{cx-s*0.6},{cy+s*0.95} {cx},{cy+s*0.95} Q{cx+s*0.6},{cy+s*0.95} {cx+s*0.7},{cy+s*0.3}" fill="none" stroke="{color}" stroke-width="{s*0.09}"/>'
    g+=f'<polygon points="{cx-s*0.8},{cy+s*0.2} {cx-s*0.55},{cy+s*0.2} {cx-s*0.7},{cy+s*0.45}"/><polygon points="{cx+s*0.8},{cy+s*0.2} {cx+s*0.55},{cy+s*0.2} {cx+s*0.7},{cy+s*0.45}"/></g>'
    return g
def compass(cx,cy,r,fill,dark):
    return star(cx,cy,r,fill,dark,n=8,inner=0.38)+f'<circle cx="{cx}" cy="{cy}" r="{r*0.14}" fill="{dark}"/>'
def oars(cx,cy,L,color,dark):
    s=''
    for a in (35,-35):
        s+=f'<g transform="rotate({a} {cx} {cy})"><rect x="{cx-4}" y="{cy-L/2}" width="8" height="{L}" fill="{color}" stroke="{dark}" stroke-width="2"/><ellipse cx="{cx}" cy="{cy-L/2-8}" rx="12" ry="26" fill="{color}" stroke="{dark}" stroke-width="2"/></g>'
    return s
def oar_hook(cx,cy,L,color,dark):
    s=f'<g transform="rotate(35 {cx} {cy})"><rect x="{cx-4}" y="{cy-L/2}" width="8" height="{L}" fill="{color}" stroke="{dark}" stroke-width="2"/><ellipse cx="{cx}" cy="{cy-L/2-8}" rx="12" ry="26" fill="{color}" stroke="{dark}" stroke-width="2"/></g>'
    s+=f'<g transform="rotate(-35 {cx} {cy})"><rect x="{cx-4}" y="{cy-L/2}" width="8" height="{L}" fill="{color}" stroke="{dark}" stroke-width="2"/><path d="M{cx},{cy-L/2} q22,-6 12,-26 q-4,-6 -12,-2" fill="none" stroke="{color}" stroke-width="7"/></g>'
    return s
def waves(cx,cy,w,color):
    s=''
    for j in range(2):
        d=f'M{cx-w/2},{cy+j*14} '
        for i in range(8): d+=f'q{w/16},-12 {w/8},0 '
        s+=f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
    return s
def helmet(cx,cy,s,color,dark,knot=False):
    g=f'<g fill="{color}" stroke="{dark}" stroke-width="2">'
    g+=f'<circle cx="{cx}" cy="{cy-s*0.35}" r="{s*0.42}"/>'
    g+=f'<rect x="{cx-s*0.14}" y="{cy-s*0.95}" width="{s*0.28}" height="{s*0.14}"/>'
    g+=f'<circle cx="{cx}" cy="{cy-s*0.32}" r="{s*0.16}" fill="{dark}"/>'
    g+=f'<polygon points="{cx-s*0.5},{cy+s*0.05} {cx+s*0.5},{cy+s*0.05} {cx+s*0.62},{cy+s*0.75} {cx-s*0.62},{cy+s*0.75}"/>'
    g+=f'<circle cx="{cx-s*0.26}" cy="{cy+s*0.35}" r="{s*0.06}" fill="{dark}"/><circle cx="{cx+s*0.26}" cy="{cy+s*0.35}" r="{s*0.06}" fill="{dark}"/>'
    if knot: g+=f'<ellipse cx="{cx}" cy="{cy+s*0.42}" rx="{s*0.2}" ry="{s*0.11}" fill="none" stroke="{dark}" stroke-width="3"/><ellipse cx="{cx}" cy="{cy+s*0.42}" rx="{s*0.11}" ry="{s*0.2}" fill="none" stroke="{dark}" stroke-width="3"/>'
    return g+'</g>'
def seahorses(cx,cy,s,color,dark):
    g=''
    for sgn in (-1,1):
        x=cx+sgn*s*0.9
        g+=f'<path d="M{x},{cy-s*0.8} q{-sgn*s*0.25},{s*0.2} 0,{s*0.5} q{sgn*s*0.3},{s*0.4} 0,{s*0.8} q{-sgn*s*0.2},{s*0.3} {-sgn*s*0.05},{s*0.5}" fill="none" stroke="{color}" stroke-width="{s*0.2}" stroke-linecap="round"/>'
        g+=f'<circle cx="{x-sgn*s*0.1}" cy="{cy-s*0.85}" r="{s*0.15}" fill="{color}" stroke="{dark}" stroke-width="2"/>'
        g+=f'<line x1="{x+sgn*s*0.1}" y1="{cy-s*1.0}" x2="{x+sgn*s*0.1}" y2="{cy-s*1.5}" stroke="{color}" stroke-width="5"/><path d="M{x+sgn*s*0.1-12},{cy-s*1.3} L{x+sgn*s*0.1},{cy-s*1.55} L{x+sgn*s*0.1+12},{cy-s*1.3}" fill="none" stroke="{color}" stroke-width="5"/>'
    return g
def caduceus(cx,cy,s,color,dark):
    g=f'<line x1="{cx}" y1="{cy-s}" x2="{cx}" y2="{cy+s}" stroke="{color}" stroke-width="{s*0.12}"/>'
    for sgn in (1,-1):
        d=f'M{cx},{cy-s*0.8} '
        for i in range(4): d+=f'q{sgn*s*0.5},{s*0.2} 0,{s*0.4} '
        g+=f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{s*0.1}"/>'
    return g
def eagle(cx,cy,s,color,dark):
    g=f'<g fill="{color}" stroke="{dark}" stroke-width="2">'
    for sgn in (-1,1):
        g+=f'<path d="M{cx+sgn*s*0.08},{cy-s*0.15} Q{cx+sgn*s*0.7},{cy-s*0.75} {cx+sgn*s*1.15},{cy-s*0.35} Q{cx+sgn*s*0.9},{cy-s*0.2} {cx+sgn*s*1.0},{cy+s*0.1} Q{cx+sgn*s*0.7},{cy} {cx+sgn*s*0.75},{cy+s*0.3} Q{cx+sgn*s*0.45},{cy+s*0.15} {cx+sgn*s*0.1},{cy+s*0.25} Z"/>'
    g+=f'<path d="M{cx-s*0.14},{cy-s*0.2} Q{cx},{cy-s*0.35} {cx+s*0.14},{cy-s*0.2} L{cx+s*0.2},{cy+s*0.35} L{cx+s*0.3},{cy+s*0.75} L{cx-s*0.3},{cy+s*0.75} L{cx-s*0.2},{cy+s*0.35} Z"/>'
    g+=f'<circle cx="{cx}" cy="{cy-s*0.4}" r="{s*0.15}"/><polygon points="{cx+s*0.12},{cy-s*0.42} {cx+s*0.3},{cy-s*0.35} {cx+s*0.12},{cy-s*0.3}" fill="{dark}"/>'
    return g+'</g>'
def oakwreath(cx,cy,r,color,dark,open_top=False,gold2=None):
    g=''
    for i in range(14):
        a=math.radians(-90+ (i*360/14))
        if open_top and abs(((i*360/14)+360)%360)<30 or (open_top and abs(i*360/14-360)<30): continue
        x=cx+r*math.cos(a); y=cy+r*math.sin(a)
        g+=f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r*0.17:.1f}" ry="{r*0.09:.1f}" transform="rotate({math.degrees(a)+90:.0f} {x:.1f} {y:.1f})" fill="{color}" stroke="{dark}" stroke-width="1.5"/>'
    return g
def rope(cx,cy,r,color,dark):
    g=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{dark}" stroke-width="16"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="11" stroke-dasharray="10 6"/>'
    return g
def pennant(cx,cy,w,color,dark):
    return f'<path d="M{cx-w/2},{cy-18} L{cx+w/2},{cy-8} L{cx+w/2-30},{cy+2} L{cx+w/2},{cy+12} L{cx-w/2},{cy+22} Z" fill="{color}" stroke="{dark}" stroke-width="2"/>'
def letter(ch,cx,cy,s,fill):
    return f'<text x="{cx}" y="{cy+s*0.36}" font-family="DejaVu Sans, Arial, sans-serif" font-weight="700" font-size="{s}" text-anchor="middle" fill="{fill}">{ch}</text>'
def hourglass(cx,cy,s,fill,dark):
    return (f'<polygon points="{cx-s*0.5},{cy-s*0.9} {cx+s*0.5},{cy-s*0.9} {cx+s*0.06},{cy} {cx+s*0.5},{cy+s*0.9} {cx-s*0.5},{cy+s*0.9} {cx-s*0.06},{cy}" fill="{fill}" stroke="{dark}" stroke-width="3"/>'
            f'<rect x="{cx-s*0.6}" y="{cy-s*1.0}" width="{s*1.2}" height="{s*0.12}" fill="{fill}" stroke="{dark}" stroke-width="2"/><rect x="{cx-s*0.6}" y="{cy+s*0.88}" width="{s*1.2}" height="{s*0.12}" fill="{fill}" stroke="{dark}" stroke-width="2"/>')
def arrowhead(cx,cy,s,fill,dark):
    return f'<path d="M{cx},{cy-s} L{cx+s*0.55},{cy+s*0.7} L{cx},{cy+s*0.35} L{cx-s*0.55},{cy+s*0.7} Z" fill="{fill}" stroke="{dark}" stroke-width="3"/>'
BRONZE='#a9743a'; BRONZED='#5e3b17'; SILV='#cfd3d8'; SILVD='#6b7078'
def card(body,label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="384" viewBox="0 0 400 300"><rect width="400" height="300" fill="{BG}"/>'
            f'<g>{body}</g>'+''.join(f'<text x="200" y="{y}" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#9fb0c9" text-anchor="middle">{t}</text>' for y,t in zip((268,286) if ' - ' in label else (286,),label.rsplit(' - ',1) if ' - ' in label else (label,)))+'</svg>')
ILL='ILLUSTRATION - NOT OFFICIAL'
D={}
def wing_badge(extra): return wings(200,125,150,GOLD,GOLDD)+extra
D['b-cg-aviator']=wing_badge(anchor(200,125,40,GOLDD,GOLDD,0)+shield(200,125,44,52))
D['b-cg-aircrew']=wing_badge(anchor(200,128,42,GOLD2,GOLDD)+letter('AC',200,150,26,'#ffffff'))
D['b-cg-astronaut']=wing_badge(anchor(185,125,40,GOLD2,GOLDD,-30)+anchor(215,125,40,GOLD2,GOLDD,30)+shield(200,128,40,46)+star(238,98,13,'#ffffff',GOLDD))
D['b-cg-aviationms']=wing_badge(f'<circle cx="200" cy="125" r="42" fill="{GOLD}" stroke="{SIL}" stroke-width="7"/>'+anchor(200,125,30,SIL,PEWD))
D['b-cg-boatforce']=oar_hook(200,140,130,PEW,PEWD)+waves(200,210,220,PEW)+compass(200,128,58,PEWL,PEWD)
D['b-cg-diver2']=helmet(200,135,120,PEW,PEWD)
D['b-cg-diver1']=helmet(200,135,110,PEW,PEWD)+waves(200,75,130,PEW).replace('stroke-width="5"','stroke-width="4"')+waves(200,215,130,PEW)
D['b-cg-masterdiver']=seahorses(200,130,60,PEW,PEWD)+helmet(200,140,100,PEW,PEWD,knot=True)
D['b-cg-dmt']=seahorses(200,130,60,PEW,PEWD)+helmet(200,140,100,PEW,PEWD)+caduceus(200,172,30,PEWD,PEWD)
D['b-cg-honorguard']=f'<ellipse cx="200" cy="130" rx="110" ry="80" fill="{GOLD}" stroke="{GOLDD}" stroke-width="6"/>'
D['b-cg-cmdafloat']=pennant(200,150,260,GOLD,GOLDD)+eagle(200,110,70,SIL,PEWD)
D['b-cg-cmdashore']=oakwreath(200,130,78,GOLD,GOLDD)+eagle(200,118,60,SIL,PEWD)
D['b-cg-oicafloat']=rope(200,130,72,PEW,PEWD)+anchor(200,128,44,PEWD,PEWD)+shield(200,128,34,40)
D['b-cg-oicashore']=oakwreath(200,130,78,PEW,PEWD,open_top=True)+shield(200,132,50,60)
# Army/Air Force/Coast Guard devices (shape and metal as named in the entries)
D['m-dev-star']=star(200,125,70,BRONZE,BRONZED)
D['m-dev-campaign-star']=star(200,125,70,BRONZE,BRONZED)
D['m-dev-star516']=star(200,125,70,GOLD,GOLDD)
D['m-dev-star-silver']=star(200,125,70,SILV,SILVD)
D['m-dev-gold-star']=star(200,125,70,GOLD,GOLDD)
D['m-dev-numeral']=letter('2',200,125,150,SILV)
D['m-dev-c']=letter('C',200,125,150,BRONZE)
D['m-dev-r']=letter('R',200,125,150,BRONZE)
D['m-dev-m']=letter('M',200,125,150,BRONZE)
D['m-dev-arctic-a']=letter('A',200,125,150,BRONZE)
D['m-dev-nuclear-n']=letter('N',200,125,150,BRONZE)
D['m-dev-cg-o']=letter('O',200,125,150,GOLD)
D['m-dev-cg-m']=letter('M',200,125,150,GOLD)
D['m-dev-hourglass']=hourglass(200,125,70,BRONZE,BRONZED)
D['m-dev-arrowhead']=arrowhead(200,125,75,BRONZE,BRONZED)
CAP={'m-dev-numeral':'numeral 2 (shape only; metal not shown)','m-dev-hourglass':'bronze hourglass (silver, gold also)','m-dev-campaign-star':'bronze star (also silver)','m-dev-star':'bronze star (also silver)','m-dev-star-silver':'silver star','m-dev-star516':'gold star (also silver)'}
if __name__=='__main__':
    for k,body in D.items():
        svg=card(body,(CAP.get(k)+' - ' if k in CAP else '')+ILL) if k in CAP else card(body,ILL)
        p=f'{TMP}/{k}.svg'; open(p,'w').write(svg)
        subprocess.check_call(['rsvg-convert','-w','512',p,'-o',f'{OUT}/{k}.png'])
    print(len(D),'drawn')

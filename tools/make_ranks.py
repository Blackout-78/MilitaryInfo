"""Draw SCHEMATIC Army rank pictures from the written descriptions in DA Pam 670-1 ch 21.
Not to scale, not exact insignia shapes. Colors: enlisted golden-light on Army blue (ASU); officers per para 21-5/21-6."""
import math, os, json
from PIL import Image, ImageDraw, ImageFont
W = 600; H = 450
BLUE = (24, 40, 78); GOLD = (222, 184, 70); SILVER = (205, 208, 214); BLACK = (20, 20, 20); GRAY = (40, 44, 52)
SS = 2
def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi/2 + i*math.pi/5; rr = r if i % 2 == 0 else r*0.42
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    d.polygon(pts, fill=fill)
def chevron(d, cx, y, w=200, th=26, fill=GOLD):
    # V shape: apex at top
    d.polygon([(cx-w, y+w*0.45), (cx, y), (cx+w, y+w*0.45), (cx+w, y+w*0.45+th), (cx, y+th), (cx-w, y+w*0.45+th)], fill=fill)
def arc(d, cx, y, w=200, th=20, fill=GOLD):
    # rocker: curve opening upward
    pts = [(cx-w+ (2*w*i/40), y + 0.0 + 28*math.sin(math.pi*i/40)*-1 + 28) for i in range(41)]
    top = [(x, yy) for x, yy in pts]; bot = [(x, yy+th) for x, yy in reversed(pts)]
    d.polygon(top+bot, fill=fill)
def eagle(d, cx, cy, s, fill):
    # simplified spread eagle: body, head, tail, and two wings of stepped feathers
    for sg in (-1, 1):
        for i in range(5):
            x0 = cx + sg*s*(0.18 + i*0.2); y0 = cy - s*(0.35 + i*0.06)
            d.polygon([(cx+sg*s*0.15, cy-s*0.3), (x0+sg*s*0.2, y0), (x0+sg*s*0.2, y0+s*(0.55 - i*0.04)), (x0, y0+s*(0.75 - i*0.04)), (cx+sg*s*0.15, cy+s*0.1)], fill=fill)
    d.ellipse([cx-s*0.2, cy-s*0.45, cx+s*0.2, cy+s*0.5], fill=fill)
    d.ellipse([cx-s*0.12, cy-s*0.72, cx+s*0.12, cy-s*0.42], fill=fill)
    d.polygon([(cx-s*0.18, cy+s*0.4), (cx+s*0.18, cy+s*0.4), (cx+s*0.28, cy+s*0.85), (cx-s*0.28, cy+s*0.85)], fill=fill)
def lozenge(d, cx, cy, s, fill):
    d.polygon([(cx, cy-s), (cx+s*0.6, cy), (cx, cy+s), (cx-s*0.6, cy)], fill=fill)
def _lf(d, x, y, ang, L, T, fill):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for t in range(0, 21):
        u = t/20; w = T*math.sin(math.pi*u)
        pts.append((x+ca*L*u - sa*w, y+sa*L*u + ca*w))
    for t in range(20, -1, -1):
        u = t/20; w = T*math.sin(math.pi*u)
        pts.append((x+ca*L*u + sa*w, y+sa*L*u - ca*w))
    d.polygon(pts, fill=fill)
def wreath(d, cx, cy, r, fill):
    for sg in (-1, 1):
        for i in range(9):
            a = math.pi/2 + sg*(0.35 + i*0.3)
            x, y = cx + r*math.cos(a), cy - r*math.sin(a)*-1*-1
            _lf(d, x, y, a + sg*math.pi/2 + (math.pi if sg > 0 else 0)*0, 30, 8, fill)
def leaf(d, cx, cy, s, fill):
    # oak leaf: stem, central lobe, three lobes per side
    d.rectangle([cx-3, cy+s*0.7, cx+3, cy+s*1.15], fill=fill)
    d.ellipse([cx-s*0.28, cy-s*1.0, cx+s*0.28, cy+s*0.3], fill=fill)
    for sg in (-1, 1):
        for k, (dx, dy, rr) in enumerate([(0.38, -0.55, 0.28), (0.5, -0.05, 0.3), (0.4, 0.45, 0.26)]):
            d.ellipse([cx+sg*s*dx-s*rr, cy+s*dy-s*rr, cx+sg*s*dx+s*rr, cy+s*dy+s*rr], fill=fill)
    d.ellipse([cx-s*0.45, cy-s*0.6, cx+s*0.45, cy+s*0.7], fill=fill)
def bar(d, cx, cy, w, h, fill): d.rectangle([cx-w/2, cy-h/2, cx+w/2, cy+h/2], fill=fill)
def draw(spec):
    kind = spec[0]
    im = Image.new("RGB", (W*SS, H*SS), BLUE if kind == "enl" else GRAY); d = ImageDraw.Draw(im)
    s = SS; cx = W*s/2
    if kind == "enl":
        _, n_chev, n_arc, dev, spc = spec
        top = 70*s; step = 40*s
        if spc: 
            chevron(d, cx, top+60*s, 170*s, 24*s); eagle(d, cx, top+50*s, 40*s, GOLD)  # inverted: eagle above
        else:
            for i in range(n_chev): chevron(d, cx, top+i*step, 170*s, 24*s)
            for j in range(n_arc): arc(d, cx, top+n_chev*step+60*s+j*34*s-20*s, 170*s, 18*s)
            ey = top+ (n_chev-1)*step + 170*s*0.45*0.5 + 30*s
            if dev == "lozenge": lozenge(d, cx, top+n_chev*step+30*s, 28*s, GOLD)
            if dev == "star": star(d, cx, top+n_chev*step+30*s, 30*s, GOLD)
        if dev == "wreathstar":
            wreath(d, cx, 200*s, 120*s, GOLD); star(d, cx, 200*s, 70*s, GOLD)
        if dev == "sma":
            eagle(d, cx, 190*s, 70*s, GOLD); star(d, cx-150*s, 190*s, 40*s, GOLD); star(d, cx+150*s, 190*s, 40*s, GOLD)
    elif kind == "wo":
        _, n, line = spec
        bar(d, cx, 220*s, 320*s, 90*s, SILVER)
        if line: bar(d, cx, 220*s, 300*s, 8*s, BLACK)
        for i in range(n): bar(d, cx-(n-1)*45*s/2*1 + i*45*s - ((n-1)*45*s/2 - (n-1)*45*s/2), 220*s, 28*s, 28*s, BLACK) if False else None
        if not line:
            x0 = cx - (n-1)*60*s/2
            for i in range(n): bar(d, x0+i*60*s, 220*s, 32*s, 32*s, BLACK)
    elif kind == "bars":
        _, n, col = spec
        x0 = cx - (n-1)*100*s/2
        for i in range(n): bar(d, x0+i*100*s, 220*s, 70*s, 190*s, col)
    elif kind == "leaf": leaf(d, cx, 200*s, 90*s, spec[1])
    elif kind == "eagle": eagle(d, cx, 210*s, 130*s, SILVER)
    elif kind == "stars":
        n = spec[1]; x0 = cx - (n-1)*130*s/2
        for i in range(n): star(d, x0+i*130*s, 215*s, 62*s, SILVER)
    im = im.resize((W, H), Image.LANCZOS); d = ImageDraw.Draw(im)
    f = ImageFont.load_default(size=18)
    d.text((W/2, H-18), "SCHEMATIC - not to scale, not the exact insignia", fill=(170, 176, 190), font=f, anchor="mm")
    return im
SPEC = {
 "pv2": ("enl",1,0,None,False), "pfc": ("enl",1,1,None,False), "spc": ("enl",1,0,None,True), "cpl": ("enl",2,0,None,False), "sgt": ("enl",3,0,None,False),
 "ssg": ("enl",3,1,None,False), "sfc": ("enl",3,2,None,False), "msg": ("enl",3,3,None,False), "1sg": ("enl",3,3,"lozenge",False),
 "sgm": ("enl",3,3,"star",False), "csm": ("enl",0,0,"wreathstar",False), "sma": ("enl",0,0,"sma",False),
 "wo1": ("wo",1,False), "cw2": ("wo",2,False), "cw3": ("wo",3,False), "cw4": ("wo",4,False), "cw5": ("wo",0,True),
 "2lt": ("bars",1,GOLD), "1lt": ("bars",1,SILVER), "cpt": ("bars",2,SILVER), "maj": ("leaf",GOLD), "ltc": ("leaf",SILVER), "col": ("eagle",),
 "bg": ("stars",1), "mg": ("stars",2), "lg": ("stars",3), "gen": ("stars",4),
}
if __name__ == "__main__":
    os.makedirs("app/src/main/assets/images/ranks", exist_ok=True)
    for k, sp in SPEC.items(): draw(sp).save(f"app/src/main/assets/images/ranks/r-{k}.png", optimize=True)

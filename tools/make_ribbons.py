"""Draw Army ribbon PNGs from the official stripe widths (inches) and color names.
Source text: veteranmedals.army.mil, "U.S. Army Service, Campaign Medals and Foreign Awards Information".
Rule: stripe widths must add up to the 1 3/8 inch ribbon, or the ribbon is not drawn.
Hex values are approximations of the named Federal colors (the source gives names and numbers only)."""
import json, sys
from fractions import Fraction as F
from PIL import Image, ImageDraw

H = {"W":"#FFFFFF","R":"#BF0A30","S":"#C8102E","CR":"#A6192E","SR":"#B3202B","OGB":"#0A2A6B","UB":"#1C3F94",
 "IB":"#1B2A6B","P":"#5B2A86","GO":"#F2A900","MG":"#00695C","G":"#1E7A3C","BK":"#111111","OG":"#C9A227",
 "GY":"#F5B700","Y":"#FFD100","MOS":"#7C8F4E","OB":"#2F62B0","BR":"#5A3A22","IG":"#009A44","BB":"#5DADE2",
 "TL":"#2A8C9B","SP":"#8B5A2B","PG":"#4B5320","AFY":"#FDB913","CH":"#D8B77A","EM":"#0E8F5A","GL":"#F3D55B",
 "JG":"#2E5A3A","FB":"#1F3E8C","O":"#F26B21","GR":"#2C8FC9","BRK":"#9C3B2E","SC":"#C8102E"}
def f(x): return F(x)
def tri(a,b,c): return [(F(1,24),a),(F(1,24),b),(F(1,24),c)]
def sym(half, center):
    return half + [center] + half[::-1]

R = {}
R["m-dsc"]=[(F(1,8),"R"),(F(1,16),"W"),(F(1),"IB"),(F(1,16),"W"),(F(1,8),"R")]
R["m-dsm"]=sym([(F(5,16),"S"),(F(1,16),"UB")],(F(5,8),"W"))
R["m-silver-star"]=sym([(F(3,32),"UB"),(F(3,64),"W"),(F(7,32),"UB"),(F(7,32),"W")],(F(7,32),"R"))
R["m-lom"]=[(F(1,16),"W"),(F(5,4),"CR"),(F(1,16),"W")]
R["m-soldiers-medal"]=[(F(3,8),"UB")]+[(F(5,104),"W" if i%2==0 else "R") for i in range(13)]+[(F(3,8),"UB")]
R["m-bsm"]=sym([(F(1,32),"W"),(F(9,16),"S"),(F(1,32),"W")],(F(1,8),"UB"))
R["m-purple-heart"]=[(F(1,8),"W"),(F(9,8),"P"),(F(1,8),"W")]
R["m-msm"]=sym([(F(1,8),"CR"),(F(1,4),"W")],(F(5,8),"CR"))
R["m-air-medal"]=sym([(F(1,8),"UB"),(F(1,4),"GO")],(F(5,8),"UB"))
R["m-jscm"]=sym([(F(1,4),"BB"),(F(1,8),"W"),(F(3,32),"MG"),(F(1,8),"W")],(F(3,16),"MG"))
R["m-arcom"]=sym([(F(3,32),"W"),(F(25,64),"MG"),(F(1,32),"W"),(F(1,16),"MG"),(F(1,32),"W"),(F(1,16),"MG")],(F(1,32),"W"))
R["m-aam"]=sym([(F(1,8),"G"),(F(1,16),"W"),(F(1,8),"G"),(F(1,16),"W"),(F(9,32),"UB")],(F(1,16),"W"))
R["m-pow"]=sym([(F(1,16),"R"),(F(3,32),"W"),(F(1,16),"OGB"),(F(1,8),"W")],(F(11,16),"BK"))
R["m-agcm"]=sym([(F(1,16),"SR" if i%2==0 else "W") for i in range(6)],(F(5,8),"SR"))
# mirrored order for Good Conduct: left SR,W,SR,W,SR,W / right W,SR,W,SR,W,SR (mirror of left)
R["m-arcam"]=sym([(F(5,16),"OG"),(F(1,8),"UB"),(F(1,16),"W")],(F(3,8),"S"))
R["m-aoo-germany"]=sym([(F(1,16),"UB"),(F(1,16),"S"),(F(3,16),"W")],(F(3,4),"BK"))
R["m-adsm"]=[(F(3,16),"GY")]+tri("OGB","W","S")+[(F(3,4),"GY")]+tri("S","W","OGB")+[(F(3,16),"GY")]
R["m-wac"]=[(F(1,8),"OG"),(F(9,8),"MOS"),(F(1,8),"OG")]
R["m-american-campaign"]=([(F(3,16),"OB"),(F(1,16),"W"),(F(1,16),"BK"),(F(1,16),"S"),(F(1,16),"W"),(F(3,16),"OB")]+tri("OGB","W","S")
  +[(F(3,16),"OB"),(F(1,16),"W"),(F(1,16),"S"),(F(1,16),"BK"),(F(1,16),"W"),(F(3,16),"OB")])
R["m-apc"]=([(F(3,16),"Y"),(F(1,16),"W"),(F(1,16),"S"),(F(1,16),"W"),(F(1,4),"Y")]+tri("OGB","W","S")
  +[(F(1,4),"Y"),(F(1,16),"W"),(F(1,16),"S"),(F(1,16),"W"),(F(3,16),"Y")])
R["m-eame"]=([(F(3,16),"BR"),(F(1,16),"IG"),(F(1,16),"W"),(F(1,16),"S"),(F(1,4),"IG")]+tri("OGB","W","S")
  +[(F(1,4),"IG"),(F(1,16),"W"),(F(1,16),"BK"),(F(1,16),"W"),(F(3,16),"BR")])
R["m-humane-action"]=sym([(F(9,32),"BK"),(F(1,16),"W"),(F(9,32),"TL"),(F(3,64),"W")],(F(1,32),"S"))
R["m-ndsm"]=sym([(F(7,16),"S"),(F(1,32),"W"),(F(1,32),"OGB"),(F(1,32),"W"),(F(1,32),"S")],(F(1,4),"GY"))
R["m-ksm"]=sym([(F(1,32),"W"),(F(19,32),"BB")],(F(1,8),"W"))
R["m-afem"]=[(F(3,32),c) for c in ("G","GY","SP","BK")]+[(F(7,32),"BB"),(F(1,16),"UB"),(F(1,16),"W"),(F(1,16),"S"),(F(7,32),"BB")]+[(F(3,32),c) for c in ("BK","SP","GY","G")]
R["m-vsm"]=sym([(F(1,8),"PG"),(F(5,16),"AFY"),(F(1,16),"R"),(F(5,32),"AFY")],(F(1,16),"R"))
R["m-swasm"]=sym([(F(1,16),"BK"),(F(1,8),"CH"),(F(1,16),"OGB"),(F(1,16),"W"),(F(1,16),"R"),(F(3,16),"CH"),(F(3,32),"MG")],(F(1,16),"BK"))
R["m-acm"]=sym([(F(5,64),"EM"),(F(3,16),"S"),(F(1,8),"BK"),(F(7,32),"W"),(F(1,32),"S"),(F(1,32),"W")],(F(1,32),"OGB"))
R["m-icm"]=sym([(F(5,32),"S"),(F(1,16),"W"),(F(1,32),"G"),(F(1,16),"W"),(F(5,32),"BK")],(F(7,16),"CH"))
R["m-afsm"]=sym([(F(1,16),"GL"),(F(1,8),"JG"),(F(1,8),"G"),(F(1,8),"MOS"),(F(1,8),"GL")],(F(1,4),"BB"))
R["m-ncopdr"]=([(F(3,16),"G"),(F(1,8),"Y"),(F(3,16),"G"),(F(1,16),"Y"),(F(1,4),"FB"),(F(1,16),"Y"),(F(3,16),"G"),(F(1,8),"Y"),(F(3,16),"G")])
R["m-asr"]=sym([(F(7,32),"S"),(F(5,32),"O"),(F(3,32),"GY"),(F(1,8),"EM")],(F(3,16),"UB"))  # centre width = remainder
R["m-osr"]=[(F(3,16),"FB"),(F(5,16),"GR"),(F(1,16),"GY"),(F(1,4),"BRK"),(F(1,16),"GY"),(F(5,16),"GR"),(F(3,16),"FB")]
R["m-arcotr"]=[(F(19,32),"UB"),(F(3,64),"W"),(F(3,32),"R"),(F(3,64),"W"),(F(19,32),"UB")]
R["m-vua"]=sym([(F(3,8),"R"),(F(1,16),"UB"),(F(1,64),"W"),(F(3,32),"UB"),(F(3,32),"W")],(F(3,32),"R"))
R["m-asua"]=sym([(F(17,32),"S"),(F(1,32),"Y")],(F(1,4),"G"))

# Good Conduct: left half starts SR; right half is the mirror image.
W = F(11,8)
bad = {k: float(sum(w for w,_ in v)) for k,v in R.items() if sum(w for w,_ in v) != W}
print("sum check:", "all 1 3/8 in" if not bad else bad)
if bad: sys.exit(1)

out = "app/src/main/assets/images/ribbons/"
S = 2; PW, PH = 1375, 375
for k, st in R.items():
    im = Image.new("RGB", (PW*S, PH*S), "#000000"); d = ImageDraw.Draw(im); x = F(0)
    for w, c in st:
        x0 = round(float(x)/1.375*PW*S); x += w; x1 = round(float(x)/1.375*PW*S)
        d.rectangle([x0,0,x1-1,PH*S-1], fill=H[c])
    im = im.resize((PW//2, PH//2), Image.LANCZOS); im.save(out+k+".png", optimize=True)
json.dump(sorted(R), open("/tmp/ribbon_ids.json","w"))
print(len(R), "ribbons drawn")

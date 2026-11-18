"""Fetch picked unit insignia from Commons (900px, trimmed) + Wikipedia intro text. Runs on GitHub Actions."""
import json, os, re, time, urllib.parse, urllib.request, io
from PIL import Image, ImageChops
UA="MilitaryInfo-image-finder/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
def get(api,p):
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(api+"?"+urllib.parse.urlencode(p),headers={"User-Agent":UA}),timeout=40))
        except Exception as e: err=e; time.sleep(2)
    raise err
PICKS=json.load(open("tools/unit_picks.json")); os.makedirs("out/badges",exist_ok=True); meta={}
for k in PICKS:
    i=k["id"]; m={"name":k["name"]}
    try:
        d=get("https://commons.wikimedia.org/w/api.php",{"action":"query","format":"json","titles":k["file"],"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":900})
        ii=list(d["query"]["pages"].values())[0]["imageinfo"][0]; x=ii["extmetadata"]
        raw=urllib.request.urlopen(urllib.request.Request(ii.get("thumburl") or ii["url"],headers={"User-Agent":UA}),timeout=60).read()
        im=Image.open(io.BytesIO(raw)).convert("RGBA"); bg=Image.new("RGBA",im.size,"#ffffff"); bg.alpha_composite(im); im=bg.convert("RGB")
        bb=ImageChops.difference(im,Image.new("RGB",im.size,"white")).point(lambda v:255 if v>14 else 0).convert("L").getbbox()
        if bb: im=im.crop((max(0,bb[0]-10),max(0,bb[1]-10),min(im.width,bb[2]+10),min(im.height,bb[3]+10)))
        im.save(f"out/badges/{i}.png")
        m.update(title=k["file"],license=(x.get("LicenseShortName",{}) or {}).get("value",""),page=ii["descriptionurl"],filedesc=re.sub("<[^>]+>","",(x.get("ImageDescription",{}) or {}).get("value",""))[:300])
    except Exception as e: m["img_error"]=str(e)
    try:
        d=get("https://en.wikipedia.org/w/api.php",{"action":"query","format":"json","prop":"extracts","exintro":1,"explaintext":1,"redirects":1,"titles":k["wiki"]})
        p=list(d["query"]["pages"].values())[0]; m["wiki_title"]=p.get("title"); m["extract"]=(p.get("extract") or "")[:1200]
    except Exception as e: m["wiki_error"]=str(e)
    meta[i]=m; print("ok" if "img_error" not in m and "wiki_error" not in m else "PARTIAL",i); time.sleep(0.5)
json.dump(meta,open("out/badges/meta.json","w"),indent=1)

"""Download chosen tier badge images from Commons at 900px width, trim white borders, save PNGs. Runs on GitHub Actions."""
import json, os, re, time, urllib.parse, urllib.request, io
from PIL import Image, ImageChops
API="https://commons.wikimedia.org/w/api.php"; UA="MilitaryInfo-image-finder/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
L={"avr-senior":"File:Army Senior Aviator.png"}
for q in ("Army Master Aviator","Master Army Aviator badge","Army Aviator Badge Master"):
    d=json.load(urllib.request.urlopen(urllib.request.Request(API+"?"+urllib.parse.urlencode({"action":"query","format":"json","list":"search","srnamespace":6,"srsearch":q,"srlimit":8}),headers={"User-Agent":UA}),timeout=40))
    print(q,[x["title"] for x in d["query"]["search"]])
os.makedirs("out/tier",exist_ok=True); meta={}
for k,t in L.items():
    try:
        u=API+"?"+urllib.parse.urlencode({"action":"query","format":"json","titles":t,"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":900})
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=40))
        p=list(d["query"]["pages"].values())[0]; ii=p["imageinfo"][0]; m=ii["extmetadata"]
        src=ii.get("thumburl") or ii["url"]
        raw=urllib.request.urlopen(urllib.request.Request(src,headers={"User-Agent":UA}),timeout=60).read()
        im=Image.open(io.BytesIO(raw)).convert("RGBA"); bg=Image.new("RGBA",im.size,"#ffffff"); bg.alpha_composite(im); im=bg.convert("RGB")
        if k=="ins-basic":  # photo: crop to the badge in the middle
            w,h=im.size; im=im.crop((int(w*.2),int(h*.05),int(w*.8),int(h*.95)))
        bb=ImageChops.difference(im,Image.new("RGB",im.size,"white")).point(lambda v:255 if v>14 else 0).convert("L").getbbox()
        if bb and k!="ins-basic":
            pad=10; im=im.crop((max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad)))
        im.save(f"out/tier/{k}.png"); meta[k]={"title":t,"license":(m.get("LicenseShortName",{}) or {}).get("value",""),"artist":re.sub("<[^>]+>","",(m.get("Artist",{}) or {}).get("value","")),"page":ii["descriptionurl"],"size":im.size}
        print("ok",k,im.size)
    except Exception as e: print("FAIL",k,e)
    time.sleep(0.5)
json.dump(meta,open("out/tier/meta.json","w"),indent=1)

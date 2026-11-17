"""List image file names used on Wikipedia articles (candidate names only; each is vetted later on Commons)."""
import json, os, urllib.parse, urllib.request, time
UA="MilitaryInfo-image-finder/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
PAGES=json.load(open("tools/wiki_pages.json"))
os.makedirs("cands",exist_ok=True); out={}
for p in PAGES:
    try:
        u="https://en.wikipedia.org/w/api.php?"+urllib.parse.urlencode({"action":"parse","format":"json","prop":"images","page":p,"redirects":1})
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=40))
        out[p]=[i for i in d["parse"]["images"] if i.lower().endswith((".svg",".png",".jpg",".jpeg"))]
        print("ok",p,len(out[p]))
    except Exception as e: print("FAIL",p,e)
    time.sleep(1)
json.dump(out,open("cands/wiki_images.json","w"),indent=1)

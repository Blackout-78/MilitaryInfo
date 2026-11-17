"""List files in Commons categories (depth-limited) with license + description. Runs on GitHub Actions."""
import json, os, re, time, urllib.parse, urllib.request
API="https://commons.wikimedia.org/w/api.php"; UA="MilitaryInfo-image-finder/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
CFG=json.load(open("tools/units_cats.json"))
def get(p):
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(API+"?"+urllib.parse.urlencode(p),headers={"User-Agent":UA}),timeout=40))
        except Exception as e: err=e; time.sleep(2)
    print("FAIL",p.get("gcmtitle") or p.get("cmtitle"),err); return {}
def members(cat,typ):
    out=[]; cont={}
    while True:
        d=get({"action":"query","format":"json","list":"categorymembers","cmtitle":cat,"cmtype":typ,"cmlimit":500,**cont})
        out+=[m["title"] for m in d.get("query",{}).get("categorymembers",[])]
        if "continue" in d: cont=d["continue"]
        else: return out
def info(titles):
    res={}
    for i in range(0,len(titles),40):
        d=get({"action":"query","format":"json","titles":"|".join(titles[i:i+40]),"prop":"imageinfo","iiprop":"extmetadata|size"})
        for p in d.get("query",{}).get("pages",{}).values():
            ii=(p.get("imageinfo") or [{}])[0]; m=ii.get("extmetadata",{})
            res[p["title"]]={"lic":(m.get("LicenseShortName",{}) or {}).get("value",""),"desc":re.sub("<[^>]+>","",(m.get("ImageDescription",{}) or {}).get("value",""))[:160],"w":ii.get("width"),"h":ii.get("height")}
        time.sleep(0.3)
    return res
os.makedirs("cands",exist_ok=True); out={}
for key,c in CFG.items():
    files=[]; cats=[c["cat"]]; seen=set(cats)
    for depth in range(c.get("depth",1)+1):
        nxt=[]
        for cat in cats:
            files+=[(cat,f) for f in members(cat,"file")]
            if depth<c.get("depth",1):
                for s in members(cat,"subcat"):
                    if s not in seen: seen.add(s); nxt.append(s)
        cats=nxt
    uniq={f:cat for cat,f in files}
    inf=info(list(uniq))
    out[key]=[{"t":f,"cat":uniq[f],**inf.get(f,{})} for f in uniq]
    print("ok",key,len(out[key]))
json.dump(out,open("cands/units.json","w"),indent=0)

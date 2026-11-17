"""Find free-licensed Commons images for the badges tab. Runs on GitHub Actions. Writes
cands/<id>_<n>.jpg thumbnails, cands/candidates.json, and contact sheets cands/sheet_<k>.png."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image, ImageDraw
API = "https://commons.wikimedia.org/w/api.php"
UA = "MilitaryInfo-image-finder/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
OK = re.compile(r"public domain|^pd[- ]|cc0", re.I)
Q = {
 "r-pv2": ["Private E-2 United States Army insignia"], "r-pfc": ["Private First Class United States Army insignia"],
 "r-spc": ["Specialist United States Army insignia"], "r-cpl": ["Corporal United States Army insignia"], "r-sgt": ["Sergeant United States Army insignia"],
 "r-ssg": ["Staff Sergeant United States Army insignia"], "r-sfc": ["Sergeant First Class United States Army insignia"],
 "r-msg": ["Master Sergeant United States Army insignia"], "r-1sg": ["First Sergeant United States Army insignia"],
 "r-sgm": ["Sergeant Major United States Army insignia"], "r-csm": ["Command Sergeant Major United States Army insignia"],
 "r-sma": ["Sergeant Major of the Army insignia"], "r-wo1": ["Warrant Officer 1 United States Army insignia"], "r-cw2": ["Chief Warrant Officer 2 United States Army insignia"],
 "r-cw3": ["Chief Warrant Officer 3 United States Army insignia"], "r-cw4": ["Chief Warrant Officer 4 United States Army insignia"], "r-cw5": ["Chief Warrant Officer 5 United States Army insignia"],
 "r-2lt": ["Second Lieutenant United States Army insignia"], "r-1lt": ["First Lieutenant United States Army insignia"], "r-cpt": ["Captain United States Army insignia"],
 "r-maj": ["Major United States Army insignia"], "r-ltc": ["Lieutenant Colonel United States Army insignia"], "r-col": ["Colonel United States Army insignia"],
 "r-bg": ["Brigadier General United States Army insignia"], "r-mg": ["Major General United States Army insignia"], "r-lg": ["Lieutenant General United States Army insignia"], "r-gen": ["General United States Army insignia four star"],
}
def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r: return json.load(r)
        except Exception as e: time.sleep(2)
    return {}
def search(term):
    d = get({"action":"query","format":"json","generator":"search","gsrnamespace":6,"gsrsearch":term,"gsrlimit":10,
             "prop":"imageinfo","iiprop":"url|size|mime|extmetadata","iiurlwidth":360})
    r = []
    for p in (d.get("query",{}).get("pages",{}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata",{})
        lic = (m.get("LicenseShortName",{}) or {}).get("value","")
        if not OK.search(lic) or ii.get("mime") not in ("image/png","image/jpeg","image/svg+xml"): continue
        r.append({"title":p["title"],"license":lic,"w":ii.get("width"),"h":ii.get("height"),"thumb":ii.get("thumburl"),
                  "page":ii.get("descriptionurl"),"url":ii.get("url"),"mime":ii.get("mime")})
    return r
os.makedirs("cands", exist_ok=True); out = {}; sheets = []
for eid, qs in Q.items():
    seen = {}; 
    for q in qs:
        for c in search(q):
            if c["title"] not in seen and not re.search(r"\.pdf|ribbon|ceremony|awarded|presents|receives", c["title"], re.I): seen[c["title"]] = c
        time.sleep(0.5)
    cs = list(seen.values())[:6]; out[eid] = cs
    for i, c in enumerate(cs):
        try:
            req = urllib.request.Request(c["thumb"], headers={"User-Agent": UA})
            open(f"cands/{eid}_{i}.img", "wb").write(urllib.request.urlopen(req, timeout=40).read()); time.sleep(0.3)
        except Exception as e: c["err"] = str(e)
    print(f"== {eid}: {len(cs)}"); [print("  ", c["license"], c["w"], "x", c["h"], c["title"][:80]) for c in cs]
json.dump(out, open("cands/candidates.json","w"), indent=1)
# contact sheets: 3 entries per sheet, up to 6 thumbs each
ids = list(out); 
for k in range(0, len(ids), 3):
    im = Image.new("RGB", (1500, 3*300), "#222"); d = ImageDraw.Draw(im)
    for r, eid in enumerate(ids[k:k+3]):
        d.text((6, r*300+4), eid, fill="yellow")
        for i, c in enumerate(out[eid]):
            try:
                t = Image.open(f"cands/{eid}_{i}.img").convert("RGBA"); bg = Image.new("RGBA", t.size, "#ffffff"); bg.alpha_composite(t)
                t = bg.convert("RGB"); t.thumbnail((240, 240)); im.paste(t, (i*250+5, r*300+20))
                d.text((i*250+5, r*300+264), f"{i} {c['license'][:14]} {c['w']}x{c['h']}", fill="white")
            except Exception: pass
    im.save(f"cands/sheet_{k//3:02d}.png")

"""Find free-licensed Commons images for the badges tab. Runs on GitHub Actions. Writes
cands/<id>_<n>.jpg thumbnails, cands/candidates.json, and contact sheets cands/sheet_<k>.png."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image, ImageDraw
API = "https://commons.wikimedia.org/w/api.php"
UA = "MilitaryInfo-image-finder/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
OK = re.compile(r"public domain|^pd[- ]|cc0", re.I)
Q = {
 "b-cib": ["Combat Infantryman Badge"], "b-cmb": ["Combat Medical Badge"], "b-cab": ["Combat Action Badge"],
 "b-eib": ["Expert Infantryman Badge"], "b-efmb": ["Expert Field Medical Badge"], "b-esb": ["Expert Soldier Badge"],
 "b-aviator": ["Army Aviator Badge", "Basic Army Aviator Badge"], "b-flight-surgeon": ["Army Flight Surgeon Badge"],
 "b-aviation": ["Army Aviation Badge", "Aircraft Crew Member Badge"], "b-eod": ["Explosive Ordnance Disposal Badge", "EOD badge Army"],
 "b-parachutist": ["Parachutist Badge United States Army", "Master Parachutist Badge"], "b-freefall": ["Military Freefall Parachutist Badge"],
 "b-pathfinder": ["Pathfinder Badge"], "b-air-assault": ["Air Assault Badge"], "b-space": ["Army Space Badge"],
 "b-driver-tech": ["Driver and Mechanic Badge", "Driver badge United States Army"], "b-diver": ["Army Diver Badge", "Master Diver Badge"],
 "b-rigger": ["Parachute Rigger Badge"], "b-instructor": ["Army Instructor Badge"],
 "b-presidential": ["Presidential Service Badge"], "b-vice-presidential": ["Vice Presidential Service Badge"],
 "b-osd-id": ["Office of the Secretary of Defense Identification Badge"], "b-jcs-id": ["Joint Chiefs of Staff Identification Badge"],
 "b-army-staff-id": ["Army Staff Identification Badge"], "b-tomb-guard-id": ["Tomb of the Unknown Soldier Identification Badge", "Tomb Guard Badge"],
 "b-horseman-id": ["Military Horseman Identification Badge"],
 "b-marksmanship": ["Marksmanship Qualification Badge Expert", "Sharpshooter badge Army", "Marksman badge Army"],
 "b-ranger-tab": ["Ranger tab"], "b-sf-tab": ["Special Forces tab"], "b-sapper-tab": ["Sapper tab"], "b-presidents-hundred-tab": ["President's Hundred tab"],
 "b-airborne-trim": ["Airborne background trimming", "Airborne oval parachutist badge background"],
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

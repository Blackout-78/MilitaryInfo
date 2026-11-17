"""Fetch the picked Commons badge images (public domain / CC0 only) as PNG, <=600 px wide.
Writes app/src/main/assets/images/badges/<id>.png and CREDITS.md. Runs on GitHub Actions."""
import io, json, re, time, urllib.parse, urllib.request, os
from PIL import Image
API = "https://commons.wikimedia.org/w/api.php"
UA = "MilitaryInfo-image-fetch/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
OK = re.compile(r"public domain|^pd[- ]|cc0", re.I)
def get(url):
    for _ in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r: return r.read()
        except Exception as e: err = e; time.sleep(3)
    raise err
picks = json.load(open("tools/navy_picks.json"))
os.makedirs("out/navy", exist_ok=True); rows = []
for eid, title in picks.items():
    q = urllib.parse.urlencode({"action":"query","format":"json","titles":title,"prop":"imageinfo","iiprop":"url|size|extmetadata","iiurlwidth":600})
    p = list(json.loads(get(API+"?"+q))["query"]["pages"].values())[0]; ii = p["imageinfo"][0]; m = ii["extmetadata"]
    lic = m.get("LicenseShortName",{}).get("value","")
    if not OK.search(lic): print("SKIP license", eid, lic); continue
    url = ii.get("thumburl") if ii["width"] > 600 or title.lower().endswith(".svg") else ii["url"]
    im = Image.open(io.BytesIO(get(url))).convert("RGBA")
    if im.width > 600: im = im.resize((600, round(im.height*600/im.width)), Image.LANCZOS)
    im.save(f"out/navy/{eid}.png", optimize=True)
    art = re.sub(r"<[^>]+>", "", m.get("Artist",{}).get("value","")).strip()[:80]
    rows.append(f"| {eid} | {title[5:]} | {lic} | {art or 'n/a'} | {ii['descriptionurl']} |")
    print("ok", eid, im.size, lic); time.sleep(0.5)
open("out/CREDITS_navy.md","w").write("# Image credits\n\nBundled badge pictures, all public domain or CC0 per their Wikimedia Commons file pages.\n\n| Entry | File | License | Author field | Source page |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")

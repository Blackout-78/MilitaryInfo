"""List Wikimedia Commons image candidates (with license) for every medals entry.
Runs on GitHub Actions (the build session has no route to Commons). Read-only: downloads nothing."""
import json, re, sys, time, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "MilitaryInfo-image-finder/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
OK = re.compile(r"public domain|pd[- ]|cc0|cc[- ]by", re.I)

def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                return json.load(r)
        except Exception as e:
            err = e; time.sleep(2)
    return {"error": str(err)}

def search(term):
    d = get({"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
             "gsrsearch": term, "gsrlimit": 8, "prop": "imageinfo",
             "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 400})
    out = []
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata", {})
        lic = (m.get("LicenseShortName", {}) or {}).get("value", "")
        out.append({"title": p.get("title"), "license": lic, "ok": bool(OK.search(lic)),
                    "w": ii.get("width"), "h": ii.get("height"), "mime": ii.get("mime"),
                    "thumb": ii.get("thumburl"), "page": ii.get("descriptionurl"),
                    "artist": re.sub("<[^>]+>", "", (m.get("Artist", {}) or {}).get("value", ""))[:60]})
    return out

entries = json.load(open("app/src/main/assets/data/entries.json"))
entries = entries["entries"] if isinstance(entries, dict) else entries
res = {}
for e in entries:
    if e.get("tab") != "medals" or e.get("proof") != "official":
        continue
    name = e["name"]
    c = [x for x in search(name + " United States Army") if x["ok"]]
    if not c:
        c = [x for x in search(name) if x["ok"]]
    res[e["id"]] = c
    print(f"== {e['id']} | {name}")
    for x in c[:4]:
        print(f"   {x['license']:<14} {x['w']}x{x['h']} {x['title']}")
json.dump(res, open("candidates.json", "w"), indent=1)

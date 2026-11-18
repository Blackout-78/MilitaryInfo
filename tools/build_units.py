"""Idempotent: build Patches-tab entries from tools/unit_picks.json + tools/units_meta.json (+ images in badge-final style folder).
Usage: python3 tools/build_units.py <dir with <id>.png>"""
import json, re, shutil, sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
ENT=ROOT/"app/src/main/assets/data/entries.json"; IMG=ROOT/"app/src/main/assets/images/badges"
SRC=pathlib.Path(sys.argv[1]); META=json.load(open(ROOT/"tools/units_meta.json")); PICKS=json.load(open(ROOT/"tools/unit_picks.json"))
DROP={"u-ssi-marksman","u-af-afspc","u-ssi-80abn","u-ssi-artb","u-ssi-53sig","u-cg-cyber","u-ssi-15sust","u-ssi-108sust","u-ssi-56fa","u-ssi-44med","u-ssi-75id","u-ssi-88id","u-af-aflc","u-cg-d1","u-cg-d5","u-cg-d7","u-cg-d11","u-cg-d14","u-cg-d17"}  # + text did not match the unit, or no source text   # picture could not be confirmed against the name
MANUAL={ # eras not stated in the Wikipedia intro: written from general knowledge, so marked Unverified
 "u-ssi-4id":["ww1","ww2","vietnam","coldwar","gulf","modern"],"u-ssi-35id":["ww1","ww2"],"u-ssi-usarj":["coldwar","gulf","modern"],
 "u-ssi-recruiting":["vietnam","coldwar","gulf","modern"],"u-ssi-parachute":["coldwar","vietnam","gulf","modern"],
 "u-mc-1mardiv":["ww2","korea","vietnam","coldwar","gulf","modern"],"u-af-aetc":["modern"],"u-af-afmc":["modern"],"u-af-afrc":["modern"],
 "u-af-ang":["korea","vietnam","coldwar","gulf","modern"],"u-af-adc":["korea","vietnam","coldwar"],"u-af-afsc":["vietnam","coldwar"]}
RANGES={"ww1":(1914,1918),"interwar":(1919,1938),"ww2":(1939,1945),"korea":(1950,1953),"vietnam":(1955,1975),"coldwar":(1946,1991),"gulf":(1990,1991),"modern":(1992,2100)}
def eras_from(text):
    """Eras only when the source text states a formation year (formed/activated/established/...): that year to now (active) or to the last year in the text (ended). Else [] = unknown."""
    mm=re.search(r"\b(formed|activated|established|constituted|created|organized|founded|stood up|reactivated|designated)\b[^.]{0,70}?\b(19[0-9]{2}|20[0-2][0-9])\b",text)
    if not mm: return []
    lo=int(mm.group(2)); ys=[int(y) for y in re.findall(r"\b(19[0-9]{2}|20[0-2][0-9])\b",text)]
    if lo!=min(ys): return []   # an earlier year in the text means this is a later re-formation, not the start
    first=sents(text)[0] if sents(text) else ""
    active=not re.search(r"\b(was|were|former|formerly|inactive|disbanded|deactivated)\b",first)
    hi=2100 if active else max(ys)
    return [k for k,(x,y) in RANGES.items() if x<=hi and y>=lo]
def sents(t):
    t=re.sub(r"\s+"," ",t.replace("\n"," ")); return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"(])",t) if s.strip()]
def cut(t,n):
    if len(t)<=n: return t
    t=t[:n].rsplit(" ",1)[0].rstrip(",;:(")
    return t+" ..."
def clip(ss,n):
    out=""
    for s in ss:
        if out and len(out)+len(s)>n: break
        out+=(" " if out else "")+s
    return cut(out,n)
HER=json.load(open(ROOT/"tools/heraldry_data.json"))
doc=json.load(open(ENT)); keep=[e for e in doc["entries"] if not e["id"].startswith("u-")]
credits=[]; new=[]
for p in PICKS:
    i=p["id"]
    if i in DROP: continue
    m=META[i]
    if i=="u-ssi-78id": p=dict(p,name="78th Division (now 78th Training Division)")
    if i=="u-ssi-100id": p=dict(p,name="100th Infantry Division (now 100th Training Division)")
    if i=="u-ssi-173abn": p=dict(p,name="173rd Airborne Brigade (Sky Soldiers)")
    if not m.get("extract"): print("skip (no text)",i); continue
    ss=sents(m["extract"]); manual=i in MANUAL
    eras=MANUAL.get(i) or ([] if i in ("u-ssi-100id",) else eras_from(m["extract"]))
    if not eras: eras=list(RANGES); manual=True
    summary=clip(ss,300); used=len(sents(summary)) if not summary.endswith(" ...") else 1
    facts=[cut(x,230) for x in ss[used:used+2]]
    facts.append("Picture file on Wikimedia Commons: "+m["title"][5:])
    if p["branch"]=="Army" and "Ranger Regiment" not in p["name"]: facts.insert(0,"Patch type: Army shoulder sleeve insignia (SSI).")
    srcs=None
    if i in HER:
        h=HER[i]; facts=h["facts"]+facts; eras=h["eras"]; manual=False
        srcs=[f"Heraldry of the World (heraldry-wiki.com), \"{h['page']}\" - reproduces the US Army Institute of Heraldry record; {h['url']}"]
    shutil.copy(SRC/f"{i}.png",IMG/f"{i}.png")
    new.append({"id":i,"tab":"patches","group":p["group"],"name":p["name"],"branches":[p["branch"]],"eras":eras,
      "summary":summary,"facts":facts,"variants":[],"swatches":[],"attachments":[],"proof":"unverified" if manual else "historical",
      "remember":p["name"]+": "+p["group"].split(" (")[0].lower()+".","image":f"badges/{i}.png",
      "sources":[f"Wikipedia, \"{m['wiki_title']}\" (introduction text; a secondary source, not an official record)",
                 "Picture: Wikimedia Commons (public domain/CC0) - see CREDITS.md"]+(srcs or [])+(["Eras: the source text gives no formation year, so the era filter is not reliable for this unit (not yet checked)"] if manual else []),
      "yearFrom":None,"yearTo":None})
    credits.append(f"| {i} | {m['title'][5:]} | {m['license']} | {m['page']} |")
doc["entries"]=keep+new; json.dump(doc,open(ENT,"w"),indent=2,ensure_ascii=False)
cr=ROOT/"CREDITS.md"; lines=[l for l in cr.read_text().splitlines() if not l.startswith("| u-")]
cr.write_text("\n".join(lines)+"\n"+"\n".join(credits)+"\n"); print(len(new),"unit entries")

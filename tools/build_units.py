"""Idempotent: build Patches-tab entries from tools/unit_picks.json + tools/units_meta.json (+ images in badge-final style folder).
Usage: python3 tools/build_units.py <dir with <id>.png>"""
import json, re, shutil, sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
ENT=ROOT/"app/src/main/assets/data/entries.json"; IMG=ROOT/"app/src/main/assets/images/badges"
SRC=pathlib.Path(sys.argv[1]); META=json.load(open(ROOT/"tools/units_meta.json")); PICKS=json.load(open(ROOT/"tools/unit_picks.json"))
DROP={"u-ssi-marksman","u-af-afspc"}   # picture could not be confirmed against the name
MANUAL={ # eras not stated in the Wikipedia intro: written from general knowledge, so marked Unverified
 "u-ssi-4id":["ww1","ww2","vietnam","coldwar","gulf","modern"],"u-ssi-35id":["ww1","ww2"],"u-ssi-usarj":["coldwar","gulf","modern"],
 "u-ssi-recruiting":["vietnam","coldwar","gulf","modern"],"u-ssi-parachute":["coldwar","vietnam","gulf","modern"],
 "u-mc-1mardiv":["ww2","korea","vietnam","coldwar","gulf","modern"],"u-af-aetc":["modern"],"u-af-afmc":["modern"],"u-af-afrc":["modern"],
 "u-af-ang":["korea","vietnam","coldwar","gulf","modern"],"u-af-adc":["korea","vietnam","coldwar"],"u-af-afsc":["vietnam","coldwar"],"u-af-aflc":["vietnam","coldwar"]}
K={'ww1':r'World War I\b|First World War|1917|1918','ww2':r'World War II|Second World War|194[2345]','korea':r'Korean War|Korea\b','vietnam':r'Vietnam','coldwar':r'Cold War','gulf':r'Gulf War|Desert Storm|Desert Shield','modern':r'Iraq|Afghanistan|2001|20[012]\d'}
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
doc=json.load(open(ENT)); keep=[e for e in doc["entries"] if not e["id"].startswith("u-")]
credits=[]; new=[]
for p in PICKS:
    i=p["id"]
    if i in DROP: continue
    m=META[i]; ss=sents(m["extract"]); manual=i in MANUAL
    eras=MANUAL.get(i) or [a for a,r in K.items() if re.search(r,m["extract"])]
    if not eras: continue
    summary=clip(ss,300); used=len(sents(summary)) if not summary.endswith(" ...") else 1
    facts=[cut(x,230) for x in ss[used:used+2]]
    facts.append("Picture file on Wikimedia Commons: "+m["title"][5:])
    if p["branch"]=="Army" and "Ranger Regiment" not in p["name"]: facts.insert(0,"Patch type: Army shoulder sleeve insignia (SSI).")
    shutil.copy(SRC/f"{i}.png",IMG/f"{i}.png")
    new.append({"id":i,"tab":"patches","group":p["group"],"name":p["name"],"branches":[p["branch"]],"eras":eras,
      "summary":summary,"facts":facts,"variants":[],"swatches":[],"attachments":[],"proof":"unverified" if manual else "historical",
      "remember":p["name"]+": "+p["group"].split(" (")[0].lower()+".","image":f"badges/{i}.png",
      "sources":[f"Wikipedia, \"{m['wiki_title']}\" (introduction text; a secondary source, not an official record)",
                 "Picture: Wikimedia Commons (public domain/CC0) - see CREDITS.md"]+(["Eras for this unit are not in the source text; they are from general knowledge and not yet checked"] if manual else []),
      "yearFrom":None,"yearTo":None})
    credits.append(f"| {i} | {m['title'][5:]} | {m['license']} | {m['page']} |")
doc["entries"]=keep+new; json.dump(doc,open(ENT,"w"),indent=2,ensure_ascii=False)
cr=ROOT/"CREDITS.md"; lines=[l for l in cr.read_text().splitlines() if not l.startswith("| u-")]
cr.write_text("\n".join(lines)+"\n"+"\n".join(credits)+"\n"); print(len(new),"unit entries")

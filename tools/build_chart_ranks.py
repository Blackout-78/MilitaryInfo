"""Marine Corps, Air Force, Coast Guard enlisted rank entries. Names and grades: marines.mil/Ranks (Marines, official), mymilitarylifestyle.com and militaryfactory.com
(all, cross-check). Insignia pictures cropped from a user-supplied enlisted chart (author and license unknown). Insignia descriptions: mymilitarylifestyle.com, checked against the chart."""
import json, os
import numpy as np
from PIL import Image
CH = "tools/chart_source.jpg"
im = Image.open(CH).convert("RGB"); a = np.array(im).astype(int)
BANDS = {"mc": (234, 300), "af": (503, 560), "cg": (628, 692)}
def segs(k):
    y0, y1 = BANDS[k]; sub = a[y0:y1]
    sat = (sub.max(2) - sub.min(2) > 40) | (sub.sum(2) < 250); cols = sat.sum(0) > 1
    out = []; s = None
    for x, v in enumerate(list(cols) + [False]):
        if v and s is None: s = x
        if not v and s is not None:
            if x - s > 6: out.append((s, x))
            s = None
    m = []
    for sg in out:
        if m and sg[0] - m[-1][1] < 5: m[-1] = (m[-1][0], sg[1])
        else: m.append(sg)
    return m
def crop(k, box, path):
    y0, y1 = BANDS[k]; x0, x1 = box
    c = im.crop((x0 - 3, y0 - 4, x1 + 3, y1 + 4)); n = np.array(c).astype(int)
    mask = (n.max(2) - n.min(2) > 30) | (n.sum(2) < 300); ys, xs = np.where(mask)
    rows = sorted(set(ys.tolist())); end = rows[0]
    for r in rows[1:]:
        if r - end > 1 and r - rows[0] > 20: break   # gap after the insignia: what follows is label text
        end = r
    keep = ys <= end; xs, ys = xs[keep], ys[keep]
    c = c.crop((xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3))
    s = 280 / max(c.size); c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS); c.save(path, optimize=True)
P = "app/src/main/assets/data/entries.json"; d = json.load(open(P))
es = [e for e in d["entries"] if not e["id"].startswith(("mc-", "af-", "cg-"))]
SRC_N = ["Rank names and grades: mymilitarylifestyle.com and militaryfactory.com (commercial sites, cross-checked)", "Insignia read from a user-supplied enlisted insignia chart (author and license unknown). Not an official source"]
def add(i, branch, name, grade, desc, rem, image, srcs, group="Enlisted"):
    es.append({"id": i, "tab": "ranks", "group": group, "name": name, "branches": [branch], "eras": ["modern"], "yearFrom": None, "yearTo": None,
      "summary": f"{branch} {grade}. {desc}", "facts": [f"Grade: {grade}", f"Insignia: {desc}", "Unverified: no official insignia text was read for this entry"],
      "remember": rem, "swatches": [], "variants": [], "attachments": [], "proof": "unverified", "sources": srcs, "image": image})
os.makedirs("app/src/main/assets/images/marines", exist_ok=True); os.makedirs("app/src/main/assets/images/airforce", exist_ok=True); os.makedirs("app/src/main/assets/images/coastguard", exist_ok=True)
# Marines: cells = segs minus first stray mark
S = segs("mc")[1:]; assert len(S) == 11, len(S)
MC = [("pvt","Private","E-1","No insignia.","None."),("pfc","Private First Class","E-2","One chevron.","One chevron."),("lcpl","Lance Corporal","E-3","One chevron with crossed rifles.","Chevron plus rifles."),
 ("cpl","Corporal","E-4","Two chevrons with crossed rifles.","Two chevrons."),("sgt","Sergeant","E-5","Three chevrons with crossed rifles.","Three chevrons."),
 ("ssgt","Staff Sergeant","E-6","Three chevrons, one rocker, crossed rifles.","Three over one."),("gysgt","Gunnery Sergeant","E-7","Three chevrons, two rockers, crossed rifles.","Three over two."),
 ("msgt","Master Sergeant","E-8","Three chevrons, three rockers, crossed rifles.","Three over three."),("1stsgt","First Sergeant","E-8","Three chevrons, three rockers, and a diamond.","Diamond in the middle."),
 ("mgysgt","Master Gunnery Sergeant","E-9","Chevrons, four rockers, and a bursting bomb.","Bursting bomb."),("sgtmaj","Sergeant Major","E-9","Three chevrons, four rockers, and a star.","Star."),
 ("smmc","Sergeant Major of the Marine Corps","E-9","Chevrons and rockers with the eagle, globe, and anchor.","Eagle, globe, anchor.")]
for n, (i, name, g, desc, rem) in enumerate(MC):
    img = None
    if i != "pvt":
        crop("mc", S[n-1], f"app/src/main/assets/images/marines/mc-{i}.png"); img = f"marines/mc-{i}.png"
    add("mc-"+i, "Marine Corps", name, g, desc, rem, img, ["Rank names and grades: marines.mil/Ranks (official list)"] + SRC_N)
S = segs("af")[1:]; assert len(S) == 13, len(S)
AF = [("ab","Airman Basic","E-1","No insignia.",None),("amn","Airman","E-2","One chevron with a star in a circle.",0),("a1c","Airman First Class","E-3","Two chevrons with a star in a circle.",1),
 ("sra","Senior Airman","E-4","Three chevrons with a star in a circle.",2),("ssgt","Staff Sergeant","E-5","Four chevrons with a star in a circle.",3),("tsgt","Technical Sergeant","E-6","Five chevrons with a star in a circle.",4),
 ("msgt","Master Sergeant","E-7","Five chevrons down, one up, star in a circle.",5),("1sg-e7","First Sergeant (E-7)","E-7","Master Sergeant chevrons with a diamond.",6),
 ("smsgt","Senior Master Sergeant","E-8","Five chevrons down, two up, star in a circle.",7),("1sg-e8","First Sergeant (E-8)","E-8","Senior Master Sergeant chevrons with a diamond.",8),
 ("cmsgt","Chief Master Sergeant","E-9","Five chevrons down, three up, star in a circle.",9),("1sg-e9","First Sergeant (E-9)","E-9","Chief Master Sergeant chevrons with a diamond.",10),
 ("ccm","Command Chief Master Sergeant","E-9","Chief chevrons with a star in the upper field.",11),("cmsaf","Chief Master Sergeant of the Air Force","E-9","Chevrons with the Great Seal in a wreath.",12)]
for i, name, g, desc, idx in AF:
    img = None
    if idx is not None: crop("af", S[idx], f"app/src/main/assets/images/airforce/af-{i}.png"); img = f"airforce/af-{i}.png"
    add("af-"+i, "Air Force", name, g, desc, desc.split(".")[0], img, SRC_N + ["Chevron stripe counts E-1 to E-7 agree with the Air Force history paper 'A Chronology of the Enlisted Rank Chevron of the U.S. Air Force' (dafhistory.af.mil, February 1992)"])
S = segs("cg"); assert len(S) == 11, len(S)
CG = [("sr","Seaman Recruit","E-1","A plain blue field, one stripe per the chart."),("sa","Seaman Apprentice","E-2","Two diagonal stripes."),("sn","Seaman","E-3","Three diagonal stripes."),
 ("po3","Petty Officer Third Class","E-4","Eagle above one chevron."),("po2","Petty Officer Second Class","E-5","Eagle above two chevrons."),("po1","Petty Officer First Class","E-6","Eagle above three chevrons."),
 ("cpo","Chief Petty Officer","E-7","Eagle above three chevrons and a rocker."),("scpo","Senior Chief Petty Officer","E-8","One star above the eagle, chevrons, and rocker."),
 ("mcpo","Master Chief Petty Officer","E-9","Two stars above the eagle, chevrons, and rocker."),("cmc","Command Master Chief","E-9","Two stars above the eagle with a shield."),
 ("mcpocg","Master Chief Petty Officer of the Coast Guard","E-9","Three stars above the eagle and shield.")]
for n, (i, name, g, desc) in enumerate(CG):
    crop("cg", S[n], f"app/src/main/assets/images/coastguard/cg-{i}.png")
    add("cg-"+i, "Coast Guard", name, g, desc, desc.split(".")[0], f"coastguard/cg-{i}.png", SRC_N)
d["entries"] = es; d["dataVersion"] = "0.12.0-chart-ranks"
json.dump(d, open(P, "w"), indent=1, ensure_ascii=False); print(len(es))

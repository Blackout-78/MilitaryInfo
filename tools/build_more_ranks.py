"""Officer and warrant ranks for the Marine Corps, Air Force, Space Force, and Coast Guard; Space Force enlisted.
Names/grades: marines.mil/Ranks (Marines), mymilitarylifestyle.com and militaryfactory.com (all). Insignia text: mymilitarylifestyle.com. Officer pictures: the Army's
army.mil/ranks pictures, because the bar, leaf, eagle, and star insignia are the same design (collar insignia)."""
import json
P = "app/src/main/assets/data/entries.json"; d = json.load(open(P)); es = d["entries"]
es[:] = [e for e in es if not e["id"].startswith(("mo-", "ao-", "so-", "co-", "se-", "mw-", "cw-"))]
OFF = [("2lt","O-1","one gold bar","r-2lt"),("1lt","O-2","one silver bar","r-1lt"),("cpt","O-3","two silver bars","r-cpt"),("maj","O-4","a gold oak leaf","r-maj"),
 ("ltc","O-5","a silver oak leaf","r-ltc"),("col","O-6","a silver eagle","r-col"),("bg","O-7","one silver star","r-bg"),("mg","O-8","two silver stars","r-mg"),
 ("lg","O-9","three silver stars","r-lg"),("gen","O-10","four silver stars","r-gen")]
NAMES = {
 "Marine Corps": ["Second Lieutenant","First Lieutenant","Captain","Major","Lieutenant Colonel","Colonel","Brigadier General","Major General","Lieutenant General","General"],
 "Air Force": ["Second Lieutenant","First Lieutenant","Captain","Major","Lieutenant Colonel","Colonel","Brigadier General","Major General","Lieutenant General","General"],
 "Space Force": ["Second Lieutenant","First Lieutenant","Captain","Major","Lieutenant Colonel","Colonel","Brigadier General","Major General","Lieutenant General","General"],
 "Coast Guard": ["Ensign","Lieutenant Junior Grade","Lieutenant","Lieutenant Commander","Commander","Captain","Rear Admiral (Lower Half)","Rear Admiral (Upper Half)","Vice Admiral","Admiral"]}
PFX = {"Marine Corps": "mo-", "Air Force": "ao-", "Space Force": "so-", "Coast Guard": "co-"}
def names_src(b):
    s = ["Rank names and grades: mymilitarylifestyle.com and militaryfactory.com (commercial sites, cross-checked)"]
    if b == "Marine Corps": s.insert(0, "Rank names and grades: marines.mil/Ranks (official list)")
    return s + ["Insignia description: mymilitarylifestyle.com (commercial site). Not an official text"]
def add(i, b, name, g, group, desc, rem, img, extra=()):
    es.append({"id": i, "tab": "ranks", "group": group, "name": name, "branches": [b], "eras": ["modern"], "yearFrom": None, "yearTo": None,
      "summary": f"{b} {g}. {desc}", "facts": [f"Grade: {g}", f"Insignia: {desc}", "Unverified: no official insignia text was read for this entry"] + list(extra),
      "remember": rem, "swatches": [], "variants": [], "attachments": [], "proof": "unverified",
      "sources": names_src(b) + (["Picture: the Army's rank picture from army.mil/ranks. The bar, leaf, eagle, and star insignia are the same design"] if img else []), "image": img})
for b, nm in NAMES.items():
    for (k, g, desc, rid), name in zip(OFF, nm):
        cg = b == "Coast Guard"
        add(PFX[b] + k, b, name, g, "General officers" if g in ("O-7","O-8","O-9","O-10") else "Officers", desc[0].upper() + desc[1:] + ".", desc.split(" ", 1)[1].capitalize() + ".", f"ranks/{rid}.png",
            ["Coast Guard collar insignia matches the Navy's; dress uniforms also use sleeve stripes and shoulder boards"] if cg else [])
MW = [("w1","Warrant Officer","W-1","a gold bar with scarlet enamel"),("w2","Chief Warrant Officer 2","W-2","a gold bar with scarlet blocks"),
 ("w3","Chief Warrant Officer 3","W-3","a silver bar with scarlet blocks"),("w4","Chief Warrant Officer 4","W-4","a silver bar with scarlet blocks"),("w5","Chief Warrant Officer 5","W-5","a silver bar with a scarlet stripe")]
for k, name, g, desc in MW:
    add("mw-"+k, "Marine Corps", name, g, "Warrant officers", desc[0].upper() + desc[1:] + ".", None, None, ["A Marine gunner replaces the chief warrant officer insignia on the left collar with a bursting bomb insignia (marines.mil/Ranks)"])
for k, name, g in [("w2","Chief Warrant Officer 2","W-2"),("w3","Chief Warrant Officer 3","W-3"),("w4","Chief Warrant Officer 4","W-4")]:
    add("cw-"+k, "Coast Guard", name, g, "Warrant officers", "Collar bar and shoulder board.", None, None, ["Coast Guard warrant officers run W-2 to W-4 only, per the pages read"])
SF = [("spc1","Specialist 1","E-1","No insignia."),("spc2","Specialist 2","E-2","Space Force Delta above one bar."),("spc3","Specialist 3","E-3","Space Force Delta above two bars."),
 ("spc4","Specialist 4","E-4","Space Force Delta above three bars."),("sgt","Sergeant","E-5","Space Force Delta and globe above chevrons."),("tsgt","Technical Sergeant","E-6","Space Force Delta and globe above chevrons."),
 ("msgt","Master Sergeant","E-7","Space Force Delta and globe with chevrons."),("smsgt","Senior Master Sergeant","E-8","Space Force Delta and globe with chevrons."),
 ("cmsgt","Chief Master Sergeant","E-9","Space Force Delta and globe with chevrons."),("cmssf","Chief Master Sergeant of the Space Force","E-9","Space Force Delta and globe with chevrons.")]
for k, name, g, desc in SF:
    add("se-"+k, "Space Force", name, g, "Enlisted", desc, None, None, ["Space Force E-5 is Sergeant, not Staff Sergeant. The Space Force has no warrant officers, per the pages read"])
d["dataVersion"] = "0.13.0-more-ranks"; json.dump(d, open(P, "w"), indent=1, ensure_ascii=False)
print(sum(1 for e in es if e["id"].startswith(("mo-","ao-","so-","co-","se-","mw-","cw-"))), len(es))

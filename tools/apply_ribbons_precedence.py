"""Attach ribbon images and DA Pam 670-1 para 22-5 order-of-wear numbers to medals entries."""
import json, os
P = "app/src/main/assets/data/entries.json"
d = json.load(open(P)); E = {e["id"]: e for e in d["entries"]}
SRC_P = "DA Pam 670-1, Guide to the Wear and Appearance of Army Uniforms and Insignia, 26 Jan 2021, para 22-5 (read from the copy hosted at home.army.mil/jackson)"
SRC_R = "Ribbon stripes: U.S. Army, 'U.S. Army Service, Campaign Medals and Foreign Awards Information' (veteranmedals.army.mil, text dated 19 Mar 2003). Ribbon drawn by this app; color values are approximations of the named Federal colors"
SRC_M = "Ribbon: MIL-DTL-11589/92E, Ribbon, Meritorious Unit Commendation, U.S. Army, 31 May 2010 (solid Scarlet 67111, 1 3/8 inch). Color value is an approximation"
SRC_G = "Ribbon stripes cross-checked or measured against S. G. Haskin, Illustrated Guide - United States Military Specification MIL-DTL-11589 Ribbons, 7 Dec 2018 (private guide to the TIOH spec sheets, not endorsed by TIOH); widths to 1/64 inch, +/-1/64, colors are its Pantone matches"
import json as _j
GN = _j.load(open("tools/guide_fit.json"))["new"]
prec = {
 "Decorations": {"m-moh":1,"m-dsc":2,"m-defense-dsm":6,"m-dsm":7,"m-silver-star":8,"m-defense-superior":9,"m-lom":10,"m-dfc":11,"m-soldiers-medal":12,"m-bsm":16,"m-purple-heart":17,"m-defense-meritorious":18,"m-msm":19,"m-air-medal":20,"m-jscm":22,"m-arcom":23,"m-jsam":27,"m-aam":28},
 "Unit awards": {"m-puc":1,"m-vua":5,"m-muc":9,"m-asua":13},
 "Service medals and ribbons": {"m-pow":1,"m-agcm":2,"m-adsm":3,"m-wac":4,"m-american-campaign":5,"m-apc":6,"m-eame":7,"m-wwii-victory":8,"m-aom":9,"m-humane-action":10,"m-ndsm":11,"m-ksm":12,"m-antarctica":13,"m-afem":14,"m-vsm":15,"m-swasm":16,"m-kcm":17,"m-acm":18,"m-icm":19,"m-ircm":20,"m-gwotem":21,"m-gwotsm":22,"m-kdsm":23,"m-afsm":24,"m-hsm":25,"m-movsm":26,"m-asdr":27,"m-afrm":28,"m-ncopdr":29,"m-asr":30,"m-osr":31,"m-arcotr":32},
}
n = 0
for cat, m in prec.items():
    for i, no in m.items():
        e = E[i]; e["facts"] = [f for f in e["facts"] if not f.startswith("Order of wear:")]
        e["facts"].append(f"Order of wear: No. {no} in the Army table for {cat.lower()}. Lower numbers are worn first (higher).")
        if SRC_P not in e["sources"]: e["sources"].append(SRC_P)
        n += 1
r = 0
for f in sorted(os.listdir("app/src/main/assets/images/ribbons")):
    i = f[:-4]; e = E[i]; e["image"] = "ribbons/" + f
    if i == "m-muc": src = SRC_M
    elif i in GN: src = SRC_G + f" (sheet MIL-DTL-11589/{GN[i]['sheet']})"
    else: src = SRC_R
    e["sources"] = [x for x in e["sources"] if not x.startswith("Ribbon") or x == src]
    if src not in e["sources"]: e["sources"].append(src)
    if i not in GN and i != "m-muc" and SRC_G not in e["sources"]: e["sources"].append(SRC_G)
    r += 1
d["dataVersion"] = "0.3.0-army-ribbons"
json.dump(d, open(P, "w"), indent=1, ensure_ascii=False)
print("precedence on", n, "entries; ribbons on", r)

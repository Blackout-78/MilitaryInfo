"""Download the official Army rank insignia SVGs from army.mil/ranks and render PNGs. Runs on GitHub Actions."""
import os, re, time, urllib.request, cairosvg
B = "https://www.army.mil/e2/images/rv7/ranks/badges/"
L = [("enlisted","private_noimage","r-pvt"),("enlisted","private","r-pv2"),("enlisted","private_first_class","r-pfc"),("enlisted","specialist","r-spc"),("enlisted","corporal","r-cpl"),
 ("enlisted","sergeant","r-sgt"),("enlisted","staff_sergeant","r-ssg"),("enlisted","sergeant_first_class","r-sfc"),("enlisted","master_sergeant","r-msg"),("enlisted","first_sergeant","r-1sg"),
 ("enlisted","sergeant_major","r-sgm"),("enlisted","command_sergeant_major","r-csm"),("enlisted","sergeant_major_of_the_army","r-sma"),
 ("warrant_officer","cw1","r-wo1"),("warrant_officer","cw2","r-cw2"),("warrant_officer","cw3","r-cw3"),("warrant_officer","cw4","r-cw4"),("warrant_officer","cw5","r-cw5"),
 ("officer","second_lieutenant","r-2lt"),("officer","first_lieutenant","r-1lt"),("officer","captain","r-cpt"),("officer","major","r-maj"),("officer","lieutenant_colonel","r-ltc"),
 ("officer","colonel","r-col"),("officer","brigadier_general","r-bg"),("officer","major_general","r-mg"),("officer","lieutenant_general","r-lg"),("officer","general","r-gen"),("officer","general_of_the_army","r-goa")]
os.makedirs("out/ranks", exist_ok=True)
for grp, name, rid in L:
    url = f"{B}{grp}/sm/{name}.svg"
    try:
        svg = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 MilitaryInfo-fetch"}), timeout=40).read()
        open(f"out/ranks/{rid}.svg", "wb").write(svg)
        cairosvg.svg2png(bytestring=svg, write_to=f"out/ranks/{rid}.png", output_width=400)
        print("ok", rid, len(svg))
    except Exception as e: print("FAIL", rid, url, e)
    time.sleep(0.4)

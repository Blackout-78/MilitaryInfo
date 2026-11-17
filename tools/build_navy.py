"""Navy entries (insignia) from the Navy Uniform Regulations (NAVPERS 15665), mynavyhr.navy.mil chapter 4:
4101 sleeve insignia, 4104 collar grade insignia, 4211 CPO rating badges, 4221 E-1..E-6 rate insignia, 4231 service stripes.
Officer sleeve pictures are drawn to the stripe widths in 4101 (60 px per inch)."""
import json, os
from PIL import Image, ImageDraw, ImageFont
P = "app/src/main/assets/data/entries.json"
d = json.load(open(P)); es = [e for e in d["entries"] if e.get("branches") != ["Navy"]]
B = "https://www.mynavyhr.navy.mil/References/US-Navy-Uniforms/Uniform-Regulations/Chapter-4/"
def src(*paras): return ["U.S. Navy Uniform Regulations (NAVPERS 15665), mynavyhr.navy.mil, " + p + " (" + B + p.split()[0] + "/)" for p in paras]
NAVY = (14, 24, 52); GOLD = (214, 176, 64)
PX = 60
def pic(path, parts, note):
    im = Image.new("RGB", (600, 450), NAVY); d_ = ImageDraw.Draw(im)
    total = sum(h for h, _ in parts) * PX
    y = (450 - 40 - total) / 2 + total  # build from bottom up
    for h, col in parts:  # bottom first
        y -= h*PX; d_.rectangle([60, y, 540, y+h*PX], fill=col); 
    im2 = im; f = ImageFont.load_default(size=17)
    d_.text((300, 428), note, fill=(170, 176, 190), anchor="mm", font=f); im.save(path, optimize=True)
    return path
OFF = [ # id, name, grade, stripes bottom-up in inches (None = gap 0.25), description
 ("ens","Ensign","O-1",[0.5],"One 1/2-inch stripe."),
 ("ltjg","Lieutenant Junior Grade","O-2",[0.5,None,0.25],"One 1/2-inch stripe with a 1/4-inch stripe above it."),
 ("lt","Lieutenant","O-3",[0.5,None,0.5],"Two 1/2-inch stripes."),
 ("lcdr","Lieutenant Commander","O-4",[0.5,None,0.25,None,0.5],"Two 1/2-inch stripes with a 1/4-inch stripe between."),
 ("cdr","Commander","O-5",[0.5,None,0.5,None,0.5],"Three 1/2-inch stripes."),
 ("capt","Captain","O-6",[0.5,None,0.5,None,0.5,None,0.5],"Four 1/2-inch stripes."),
 ("radm-lh","Rear Admiral (lower half)","O-7",[2],"One 2-inch stripe."),
 ("radm","Rear Admiral (upper half)","O-8",[2,None,0.5],"One 2-inch stripe with one 1/2-inch stripe above."),
 ("vadm","Vice Admiral","O-9",[2,None,0.5,None,0.5],"One 2-inch stripe with two 1/2-inch stripes above."),
 ("adm","Admiral","O-10",[2,None,0.5,None,0.5,None,0.5],"One 2-inch stripe with three 1/2-inch stripes above."),
 ("fadm","Fleet Admiral","Special",[2,None,0.5,None,0.5,None,0.5,None,0.5],"One 2-inch stripe with four 1/2-inch stripes above."),
]
os.makedirs("app/src/main/assets/images/navy", exist_ok=True)
def add(i, name, group, grade, summary, facts, rem, sources, image=None, variants=()):
    es.append({"id": i, "tab": "ranks", "group": group, "name": name, "branches": ["Navy"], "eras": ["modern"], "yearFrom": None, "yearTo": None,
      "summary": summary, "facts": facts, "remember": rem, "swatches": [], "variants": list(variants), "attachments": [], "proof": "official", "sources": sources, "image": image})
for i, n, g, st, desc in OFF:
    parts = []
    for s in st: parts.append((0.25, NAVY) if s is None else (s, GOLD))
    img = pic(f"app/src/main/assets/images/navy/n-{i}.png", parts, "Sleeve stripes drawn to 4101 widths. Star and corps device not shown.")
    add("n-"+i, n, "Officers" if g.startswith("O") else "Flag officers", g, f"Navy {g}. Sleeve insignia: {desc}",
        [f"Grade: {g}", f"Sleeve stripes: {desc}", "Gold stripes encircle the sleeve, with 1/4-inch intervals between multiple stripes (para 4101)",
         "Flag officers wear collar stars (4 Admiral, 3 Vice, 2 Rear, 1 Rear lower half, per image names in 4104)" if g in ("O-7","O-8","O-9","O-10") else "Line officers wear grade insignia on both collar points (para 4104)"],
        None, src("4101 Sleeve Insignia", "4104 Collar Grade Insignia"), f"navy/n-{i}.png")
WO = [("w5","Chief Warrant Officer 5","W-5","One 1/2-inch stripe with a 1/8-inch blue strip broken by one hash mark"),
 ("w4","Chief Warrant Officer 4","W-4","One 1/2-inch stripe with one break"),("w3","Chief Warrant Officer 3","W-3","One 1/2-inch stripe with two breaks"),
 ("w2","Chief Warrant Officer 2","W-2","One 1/2-inch stripe with three breaks"),("w1","Warrant Officer 1","W-1","One 1/4-inch stripe with three breaks")]
for i, n, g, desc in WO:
    add("n-"+i, n, "Warrant officers", g, f"Navy {g}. Sleeve insignia: {desc}.", [f"Grade: {g}", f"Sleeve stripe (para 4101.3.b): {desc}", "Warrant officer breaks are bright blue",
        "Warrant officers wear grade insignia on the right collar point and staff insignia on the left (para 4104)"], None, src("4101 Sleeve Insignia", "4104 Collar Grade Insignia"))
add("n-e1","Seaman Recruit","Enlisted","E-1","Navy E-1. Wears the striker mark only, no group rate mark.",
  ["E-1 wears the striker mark only, centered 2 inches above the midway point between shoulder and elbow (para 4221)"], None, src("4221 E-1 to E-6 Rate Insignia"))
add("n-e2","Seaman Apprentice","Enlisted","E-2","Navy E-2. Two group rate stripes, with the striker mark above.",
  ["E-2 personnel wear two stripes (para 4221)","Group rate marks are 3 inches long, angled at 30 degrees","Striker mark is worn above the stripes, on Service Dress uniforms only"], "Two stripes.", src("4221 E-1 to E-6 Rate Insignia"))
add("n-e3","Seaman","Enlisted","E-3","Navy E-3. Three group rate stripes, with the striker mark above.",
  ["E-3 personnel wear three stripes (para 4221)","Group rate marks are 3 inches long, angled at 30 degrees","Striker mark is worn above the stripes, on Service Dress uniforms only"], "Three stripes.", src("4221 E-1 to E-6 Rate Insignia"))
add("n-cpo-badge","Chief Petty Officer rating badge","Enlisted","E-7 to E-9","The rating badge worn by Chief Petty Officers: a perched eagle with chevrons.",
  ["Rating badges consist of a perched eagle with expanded wings pointing upward and the eagle's head to its right (para 4211)","Chevrons are 3-1/4 inches wide for male CPOs and 2-1/2 inches wide for female CPOs",
   "Service Dress Blue: navy background, silver eagle and specialty mark, gold/scarlet chevrons and service stripes","Dinner Dress White Jacket: white background, silver eagle and specialty mark, gold/blue chevrons and stripes",
   "Sewn on the left sleeve of the Service Dress Blue jacket, centered between shoulder seam and elbow","CPO collar insignia: a gold fouled anchor with silver block letters USN (para 4212)"],
  "Chief: eagle on the sleeve, anchor on the collar.", src("4211 CPO Rating Badges", "4212 CPO Collar Insignia"))
add("n-service-stripes","Service stripes","Service marks","","One stripe for each four years of active duty service.",
  ["One stripe for each four years of active duty service. Active reserve time in an active status also counts (para 4231)","Stripes are cardinal, gold, or blue as specified",
   "Male CPO: 7-inch stripes, 3/8 inch wide. Male E-1 to E-6: 5-1/4 inch, 3/8 inch wide. Women: 5-1/4 inch, 1/4 inch wide",
   "Left sleeve; lower end of the first stripe 2 inches from the end of the sleeve; angled 45 degrees; spaced 1/4 inch apart","Enlisted Sailors with 12 cumulative years of service may wear gold stripes instead of red"],
  "One stripe, four years.", src("4231 Service Stripes"))
d["entries"] = es; d["dataVersion"] = "0.8.0-navy-ranks"
json.dump(d, open(P, "w"), indent=1, ensure_ascii=False); print(len(es))

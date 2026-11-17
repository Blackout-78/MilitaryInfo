"""Replace the two sample rank entries with Army rank insignia and service marks.
Source: DA Pam 670-1 (26 Jan 2021) ch 21, paras 21-5, 21-6, 21-7, 21-28, 21-29 (read from home.army.mil/jackson copy)."""
import json
P = "app/src/main/assets/data/entries.json"
d = json.load(open(P)); es = d["entries"]
es[:] = [e for e in es if e["id"] not in ("r-service-stripes", "r-sergeant-e5")]
SRC = ["DA Pam 670-1, Guide to the Wear and Appearance of Army Uniforms and Insignia, 26 Jan 2021, ch 21 (read from the copy hosted at home.army.mil/jackson)"]
ENL = [  # id, name, grade, para, description, remember
 ("pvt","Private","E-1","21-7a(14)","The private wears no grade insignia.","No insignia at all."),
 ("pv2","Private (E-2)","E-2","21-7a(13)","One chevron.","One chevron."),
 ("pfc","Private First Class","E-3","21-7a(12)","One chevron above one arc.","Chevron over one arc."),
 ("spc","Specialist","E-4","21-7a(11)","Shaped like an inverted chevron at the bottom with an eagle device in the center.","Eagle in the middle."),
 ("cpl","Corporal","E-4","21-7a(10)","Two chevrons.","Two chevrons, no arc."),
 ("sgt","Sergeant","E-5","21-7a(9)","Three chevrons.","Three chevrons, no arc."),
 ("ssg","Staff Sergeant","E-6","21-7a(8)","Three chevrons above one arc.","Three over one."),
 ("sfc","Sergeant First Class","E-7","21-7a(7)","Three chevrons above two arcs.","Three over two."),
 ("msg","Master Sergeant","E-8","21-7a(6)","Three chevrons above three arcs.","Three over three."),
 ("1sg","First Sergeant","E-8","21-7a(5)","Three chevrons above three arcs with a pierced lozenge.","Three over three, lozenge in the middle."),
 ("sgm","Sergeant Major","E-9","21-7a(4)","Three chevrons above three arcs with a five-pointed star.","Three over three, star."),
 ("csm","Command Sergeant Major","E-9","21-7a(3)","A five-pointed star within a wreath.","Star inside a wreath."),
 ("sma","Sergeant Major of the Army","E-9","21-7a(2)","The eagle from the Great Seal of the United States between two stars.","Eagle between two stars."),
]
OFF = [  # id, name, grade, group, para, description, remember
 ("wo1","Warrant Officer 1","WO1","Warrant officers","21-6a(11)","One black enamel square on a silver bar.","One square."),
 ("cw2","Chief Warrant Officer 2","CW2","Warrant officers","21-6a(10)","Two black enamel squares on a silver bar.","Two squares."),
 ("cw3","Chief Warrant Officer 3","CW3","Warrant officers","21-6a(9)","Three black enamel squares on a silver bar.","Three squares."),
 ("cw4","Chief Warrant Officer 4","CW4","Warrant officers","21-6a(8)","Four black enamel squares on a silver bar.","Four squares."),
 ("cw5","Chief Warrant Officer 5","CW5","Warrant officers","21-6a(7)","A black line in the center of the bar.","One line down the middle."),
 ("2lt","Second Lieutenant","O-1","Officers","21-6a(6)","One gold-colored bar.","One gold bar."),
 ("1lt","First Lieutenant","O-2","Officers","21-6a(5)","One silver-colored bar.","One silver bar."),
 ("cpt","Captain","O-3","Officers","21-6a(4)","Two silver-colored bars.","Two silver bars."),
 ("maj","Major","O-4","Officers","21-6a(3)","Gold-colored oak leaf.","Gold leaf."),
 ("ltc","Lieutenant Colonel","O-5","Officers","21-6a(2)","Silver-colored oak leaf.","Silver leaf."),
 ("col","Colonel","O-6","Officers","21-6a(1)","Silver-colored spread eagle.","Silver eagle."),
 ("bg","Brigadier General","O-7","General officers","21-5a(4)","One silver-colored, five-pointed star.","One star."),
 ("mg","Major General","O-8","General officers","21-5a(3)","Two silver-colored, five-pointed stars.","Two stars."),
 ("lg","Lieutenant General","O-9","General officers","21-5a(2)","Three silver-colored, five-pointed stars.","Three stars."),
 ("gen","General","O-10","General officers","21-5a(1)","Four silver-colored, five-pointed stars.","Four stars."),
]
def add(i, name, grade, group, para, desc, rem, facts, variants):
    es.append({"id": "r-"+i, "tab": "ranks", "group": group, "name": name, "branches": ["Army"], "eras": ["modern"], "yearFrom": None, "yearTo": None,
      "summary": f"Army grade {grade}. {desc}", "facts": [f"Grade: {grade}", f"Insignia: {desc}"] + facts, "remember": rem, "swatches": [],
      "variants": variants, "attachments": [], "proof": "official", "sources": SRC + [f"Para {para}"], "image": None})
EV = [
 {"label":"Sew-on, Army Service Uniform","era":"modern","uniform":"ASU","gender":"male","note":"Golden-light on Army blue (or white cloth). Large size. Para 21-7b(1)."},
 {"label":"Sew-on, Army Service Uniform","era":"modern","uniform":"ASU","gender":"female","note":"Golden-light on Army blue (or white cloth). Small size. Para 21-7b(2)."},
 {"label":"Sew-on, Army Green Service Uniform","era":"modern","uniform":"AGSU","gender":"any","note":"Heritage tan 566 on heritage green 564. Para 21-7b."},
 {"label":"Pin-on, polished","era":"modern","uniform":"Service","gender":"any","note":"Polished brass. Para 21-7c."},
 {"label":"Pin-on, subdued","era":"modern","uniform":"Utility","gender":"any","note":"Dull, flat black finish. Worn centered on the hook-and-loop pad on utility uniforms. Paras 21-7d, 21-7e(4)."},
]
for i,n,g,p,desc,rem in ENL:
    f = ["Enlisted personnel wear subdued grade insignia on utility uniforms"]
    if i == "pvt": f = ["Wears no grade insignia"]
    add(i,n,g,"Enlisted",p,desc,rem,f if i!="pvt" else f,[] if i=="pvt" else EV)
OV = [
 {"label":"Subdued","era":"modern","uniform":"Utility","gender":"any","note":"Generally black (para 21-6). Worn centered on the front hook-and-loop pad (21-6b(2))."},
]
for i,n,g,grp,p,desc,rem in OFF:
    add(i,n,g,grp,p,desc,rem,["Subdued officer insignia is generally black (para 21-6)"] if grp!="General officers" else ["Subdued general officer insignia has hook-and-loop backing (para 21-5a)"],OV)
es.append({"id":"r-service-stripes","tab":"ranks","group":"Service marks","name":"Service stripes","branches":["Army"],"eras":["modern"],"yearFrom":None,"yearTo":None,
 "summary":"Diagonal stripes on the left sleeve of the dress coat. One stripe for each 3 years of honorable active Federal service.",
 "facts":["Authorized: one stripe for each 3 years of honorable active Federal service (AR 670-1 para 21-28, text from an unofficial copy)",
  "Male ASU: golden-lite stripe, 3/16 in wide, 1-5/16 in long, on blue, 3/32 in border; left sleeve, first stripe 4 in from the bottom; each added stripe 1/16 in higher; 45 degree angle",
  "Male AGSU: heritage tan 566 on heritage green 564; both sleeves; each added stripe 1/8 in higher; 30 degree angle",
  "Female ASU and AGSU: stripe 5/32 in wide, 1-1/4 in long, 5/64 in border",
  "Mess uniforms: gold braid, male 1/2 in wide, female 1/4 in wide, variable length"],
 "remember":"One stripe, three years.","swatches":[],"variants":[],"attachments":[],"proof":"official",
 "sources":SRC+["Paras 21-28a to 21-28c. The 3-year rule is from AR 670-1 para 21-28 as quoted at ar670.com (unofficial copy); DA Pam text read did not state it"],"image":None})
es.append({"id":"r-overseas-bars","tab":"ranks","group":"Service marks","name":"Overseas service bars","branches":["Army"],"eras":["modern"],"yearFrom":None,"yearTo":None,
 "summary":"Small bars on the right sleeve of the dress coat. One bar for each 6-month period of overseas service.",
 "facts":["Authorized: one bar for each 6-month period (AR 670-1 para 21-29a, text from an unofficial copy)",
  "Male: golden-lite bar, 3/16 in wide, 1-5/16 in long, on blue, 3/32 in border",
  "Female: golden-lite bar, 5/32 in wide, 13/32 in long, on blue, 5/64 in border",
  "AGSU: heritage tan 566 on heritage green 564",
  "Worn centered on the outside bottom half of the right sleeve; first bar 1/4 in above the sleeve braid (officers) or 4 in above the bottom of the sleeve (enlisted); each added bar 1/16 in higher"],
 "remember":"One bar, six months.","swatches":[],"variants":[],"attachments":[],"proof":"official",
 "sources":SRC+["Para 21-29a to 21-29d. The 6-month rule is from AR 670-1 para 21-29a as quoted at ar670.com (unofficial copy); DA Pam text read did not state it"],"image":None})
d["dataVersion"] = "0.5.0-army-ranks"
json.dump(d, open(P, "w"), indent=1, ensure_ascii=False)
print(sum(1 for e in es if e["tab"]=="ranks"))

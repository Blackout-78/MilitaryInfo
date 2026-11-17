"""Add current Army uniform entries from DA Pam 670-1 (26 Jan 2021). Replaces the u-army-blue sample.
Historical samples (u-woodland-bdu, u-pinks-greens) stay Unverified."""
import json
P = "app/src/main/assets/data/entries.json"
d = json.load(open(P)); es = d["entries"]
es[:] = [e for e in es if e["id"] != "u-army-blue"]
S = "DA Pam 670-1, Guide to the Wear and Appearance of Army Uniforms and Insignia, 26 Jan 2021 (read from the copy hosted at home.army.mil/jackson)"
def add(i, name, group, summary, facts, remember, srcs, variants=()):
    es.append({"id": i, "tab": "uniforms", "group": group, "name": name, "branches": ["Army"], "eras": ["modern"], "yearFrom": None, "yearTo": None,
      "summary": summary, "facts": facts, "remember": remember, "swatches": [], "variants": list(variants), "attachments": [], "proof": "official",
      "sources": [S] + srcs, "image": None})
add("u-acu-ocp", "Army Combat Uniform (OCP)", "Field", "The daily work, utility, and field uniform, in the Operational Camouflage Pattern.",
 ["Includes a coat, trousers, tan 499 undershirt, tan 499 rigger belt, socks, coyote leather combat boots, and headgear (para 4-2)",
  "Patrol cap is the standard garrison headgear (para 4-10a(1))",
  "Coat has hook-and-loop fasteners for the flag, insignia, and tapes (para 4-8a)",
  "OCP items replace UCP items as those become unserviceable and on-hand stock runs out (para 4-1b)"],
 "OCP: the daily work and field uniform.", ["Paras 4-1, 4-2, 4-7f, 4-8a, 4-10"],
 [{"label":"Maternity work uniform (OCP)","era":"modern","note":"A daily work and utility uniform for pregnant Soldiers (para 5-1)."}])
add("u-agsu", "Army Green Service Uniform (AGSU)", "Service", "Service uniform in heritage colors. The pamphlet's 2021 revision added it.",
 ["Coat: heritage green 564", "Trousers or slacks: heritage taupe 565", "Shirt: heritage tan 566, short- or long-sleeved", "Necktie: four-in-hand, heritage green",
  "A clothing bag issue item for enlisted personnel (para 14-1)", "Sew-on grade insignia: heritage tan 566 on heritage green 564 (para 21-7b)"],
 "Green coat 564, taupe trousers 565, tan shirt 566.", ["Paras 14-1, 14-2a, 21-7b"],
 [{"label":"Maternity version","era":"modern","note":"Covered in chapter 15."}])
add("u-asu", "Army Service Uniform (Army Blue)", "Dress", "Army blue service and dress uniform for men and women.",
 ["Male Class A: Army blue coat, low-waist trousers, white short- or long-sleeved shirt (para 11-2b(1))",
  "Male Class B: low-waist trousers and white short- or long-sleeved shirt, no coat (para 11-2b(2))",
  "Coat color: Army blue 450 or 150 (para 11-2a(1))",
  "Private through specialist wear no ornamentation on the trousers (para 11-8c(4))",
  "Male is chapter 11, female is chapter 12, maternity is chapter 13",
  "Service stripes go on the left sleeve and overseas service bars on the right sleeve (paras 21-28, 21-29)"],
 "Blue coat is Class A. Drop the coat for Class B.", ["Paras 1-7a, 11-1, 11-2, 11-8c(4), 12-1, 21-28, 21-29"],
 [{"label":"Male","era":"modern","gender":"male","note":"Chapter 11."},{"label":"Female","era":"modern","gender":"female","note":"Chapter 12."}])
add("u-mess-blue", "Army Blue Mess uniform", "Formal", "Black-tie uniform that corresponds to a civilian tuxedo. The Blue Evening Mess is the most formal.",
 ["Male blue mess uniform is worn for black-tie functions and corresponds to a civilian tuxedo (para 16-6a)",
  "Male blue evening mess uniform is the most formal uniform worn by Army personnel (para 16-6a)",
  "Female: blue mess jacket, blue skirt (knee- or full-length), white formal blouse, black dress neck tab, black cummerbund, black pumps, sheer stockings (para 17-2)"],
 "Blue mess is Army black tie.", ["Paras 16-6a, 17-1, 17-2"],
 [{"label":"Male","era":"modern","gender":"male","note":"Chapter 16."},{"label":"Female","era":"modern","gender":"female","note":"Chapter 17."}])
add("u-mess-white", "Army White Mess uniform", "Formal", "Seasonal black-tie uniform in white. The White Evening Mess is the most formal.",
 ["Normally worn from April to October. Clothing zones I and II may wear it year-round (paras 18-1, 19-1)",
  "Male: white mess jacket, black high-waist trousers, white shirt, necktie, white vest (evening only), black cummerbund, black oxford shoes, black socks, white undershirt (para 18-2)",
  "Female: white mess jacket, black or white skirt, white formal blouse, black neck tab, black or white cummerbund, pumps, sheer stockings (para 19-2)",
  "Male white mess is worn for black-tie functions, like the blue mess (para 18-6a)"],
 "White mess: April to October.", ["Paras 18-1, 18-2, 18-6a, 19-1, 19-2"],
 [{"label":"Male","era":"modern","gender":"male","note":"Chapter 18."},{"label":"Female","era":"modern","gender":"female","note":"Chapter 19."}])
add("u-apfu", "Army Physical Fitness Uniform (APFU)", "Fitness", "The authorized physical fitness uniform.",
 ["The physical fitness uniform authorized for wear is classified as the Army physical fitness uniform (para 10-1)"],
 None, ["Chapter 10, para 10-1. Components were not read"])
d["dataVersion"] = "0.6.0-army-uniforms"
json.dump(d, open(P, "w"), indent=1, ensure_ascii=False)

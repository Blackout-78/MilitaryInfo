"""Navy warfare insignia entries. Sources: MILPERSMAN 1210-090, 1210-010, 1210-220, 1220-050, 1220-060, 1220-070, 1220-080 (mynavyhr.navy.mil, read 2026-11)
and the Naval History and Heritage Command dolphins article."""
import json, re
P = "app/src/main/assets/data/entries.json"
d = json.load(open(P)); es = [e for e in d["entries"] if not e["id"].startswith("nb-")]
M = "https://www.mynavyhr.navy.mil/Portals/55/Reference/MILPERSMAN/1000/1200Classification/"
def m(n): return f"MILPERSMAN {n}, mynavyhr.navy.mil ({M}{n}.pdf)"
def add(i, name, summary, facts, rem, srcs, img):
    es.append({"id": i, "tab": "badges", "group": "Warfare insignia", "name": name, "branches": ["Navy"], "eras": [], "yearFrom": None, "yearTo": None,
      "summary": summary, "facts": facts, "remember": rem, "swatches": [], "variants": [], "attachments": [], "proof": "official",
      "sources": srcs + (["Picture: Wikimedia Commons (public domain/CC0) - see CREDITS.md"] if img else []), "image": f"navy/{i}.png" if img else None})
add("nb-swo", "Surface Warfare Officer insignia", "Breast insignia for officers qualified as Surface Warfare Officers.",
 ["Officers get the 111X/114X designation, or additional qualification designator LA9 if their designator does not change","That designation entitles an officer to wear the SWO insignia under the uniform regulations (NAVPERS 15665I)",
  "An SWO keeps the designation until NAVPERSCOM revokes it","An officer who needs more than 18 months to qualify triggers a report or extension notice to NAVPERSCOM"],
 "Qualified at sea: 111X.", [m("1210-090") + ", CH-16, 27 Sep 2006"], True)
add("nb-sub", "Submarine Warfare insignia (Dolphins)", "The Dolphins: bow view of a surfaced submarine with two dolphinfish. Gold for officers, silver for enlisted.",
 ["Final design approved for wear on 24 March 1924. Captain Ernest J. King proposed it in summer 1923","Shows a bow view of a surfaced O-class submarine with two dolphinfish resting their heads on its bow planes",
  "Officers wore a gold-plated metal pin on the left breast above their ribbons and medals","Enlisted first wore an embroidered cloth version on the right sleeve (1924-47), then on the left breast from 1947. From 1950 they could wear a silver-plated metal pin"],
 "Dolphins on a sub. Gold officer, silver enlisted.", ["Naval History and Heritage Command, Submarine Warfare Insignia (Dolphins), history.navy.mil"], True)
add("nb-aviator", "Naval Aviator and Naval Flight Officer wings", "Wings for officers designated as naval aviators or naval flight officers.",
 ["Eligible officers may be designated by the Chief of Naval Personnel or the Chief of Naval Air Training as naval aviators or naval flight officers","Designation requires completing the course of instruction. Designators are 131X (naval aviator) and 132X (naval flight officer)",
  "Officers must be commissioned line officers in the Navy, Marine Corps, or Coast Guard","The right to wear aviation insignia may be revoked on the recommendation of a naval aviation evaluation board","Picture shows the Naval Aviator badge. The Naval Flight Officer badge is not pictured"],
 "131X pilot, 132X flight officer.", [m("1210-010")], True)
add("nb-nsw", "Naval Special Warfare insignia (SEAL)", "Insignia for officers qualified in special warfare.",
 ["After required courses, a 118X officer is reported as qualified in special warfare and the designator changes from 118X to 113X","The officer is authorized to wear the NSW insignia, with a 4-year active-duty service obligation from the qualification date",
  "Selection by the SEAL Officer Selection Panel is required. Waivers are not approved for previous in-service drug use","The official text does not describe the insignia design"],
 "118X becomes 113X.", [m("1210-220")], True)
add("nb-esws", "Enlisted Surface Warfare Specialist (ESWS) insignia", "Enlisted surface warfare qualification insignia.",
 ["Enlisted members may voluntarily obtain ESWS qualification while assigned to a surface ship or afloat staff","Worn with the Surface Warfare designation","Requirements are in OPNAVINST 1414.1D (reference b of the article)"],
 "Enlisted surface qualification, voluntary.", [m("1220-050") + ", 27 Sep 2006 (CH-16)"], True)
add("nb-eaws", "Enlisted Aviation Warfare Specialist (EAWS) insignia", "Enlisted aviation qualification insignia. Add (AW) after the rating.",
 ["Enlisted personnel can voluntarily obtain EAWS qualification under OPNAVINST 1414.2A","Qualified members may wear the EAWS insignia and add (AW) after their rating, as in AD3(AW)","Needs command recommendation and commanding officer approval"],
 "(AW) after the rating.", [m("1220-060")], True)
add("nb-ews", "Enlisted EOD Warfare Specialist (EWS) insignia", "Enlisted explosive ordnance disposal warfare qualification insignia.",
 ["Enlisted EOD members shall obtain the EWS qualification under OPNAVINST 1414.8","Qualified members may wear the EWS insignia and use the EWS designator in parentheses after the rate, as in EOD2(EWS)",
  "Members whose NEC is removed for disciplinary or administrative action, or voluntarily, may not wear it","Picture shows the Basic EOD badge"],
 "(EWS) after the rate.", [m("1220-070")], True)
add("nb-dws", "Enlisted Diving Warfare Specialist (DWS) insignia", "Enlisted diving warfare qualification insignia.",
 ["Enlisted divers and corpsmen with certain classifications must obtain DWS qualification","Qualification entitles the member to wear the DWS insignia","Applies to Navy divers (ND) and hospital corpsmen (HM) holding NEC M2DV, M1DV, L27A, or L28A","The member loses authorization if the NEC is removed voluntarily or through disciplinary or administrative action"],
 "Divers and corpsmen with a dive NEC.", [m("1220-080")], False)
d["entries"] = es; d["dataVersion"] = "0.10.0-navy-warfare"
json.dump(d, open(P, "w"), indent=1, ensure_ascii=False); print(len(es))

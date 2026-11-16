#!/usr/bin/env python3
"""Add Army badges and tabs to entries.json from AR 600-8-22 ch 8 (19 Jan 2024) and DA Pam 670-1 ch 22 (26 Jan 2021).
Every fact is taken from quoted text as read. Usage: build_army_badges.py <entries.json>"""
import json, sys
ERA = [("ww1",1914,1918),("interwar",1919,1938),("ww2",1939,1945),("korea",1950,1953),("vietnam",1961,1975),("coldwar",1946,1991),("gulf",1990,1991),("modern",1992,2026)]
def eras(yf, yt=None):
    if yf is None: return []          # no dates in the sources: leave out of the era filter
    end = yt or 2026
    return [k for k,a,b in ERA if yf<=b and end>=a]
AR="AR 600-8-22, Military Awards, 19 Jan 2024, "
DP="DA Pam 670-1, Guide to the Wear and Appearance of Army Uniforms and Insignia, 26 Jan 2021, "
NOTE_AR="Text read from the copy hosted at ri.ng.mil (Rhode Island National Guard)"
NOTE_DP="Text read from the copy hosted at home.army.mil/jackson"
def A(name, note=None, variants=None): return {"name":name,"note":note,"variants":variants or []}
def V(label, note=None): return {"label":label,"note":note}
def B(eid, group, name, yf, summary, facts, remember, srcs, attachments=None, variants=None, yt=None):
    return {"id":eid,"tab":"badges","group":group,"name":name,"branches":["Army"],"eras":eras(yf,yt),
      "yearFrom":yf,"yearTo":yt,"summary":summary,"facts":facts,"remember":remember,"swatches":[],
      "variants":variants or [],"attachments":attachments or [],"proof":"official",
      "sources":srcs+[NOTE_AR if any(s.startswith("AR") for s in srcs) else NOTE_DP]+([NOTE_DP] if any(s.startswith("AR") for s in srcs) and any(s.startswith("DA") for s in srcs) else []),"image":None}
def g(n): return f"Badge group {n} for order of wear (DA Pam 670-1, para 22-16a)"
STAR2="Second and third awards are shown by one and two stars superimposed on the badge"
out=[]; add=out.append
# ---------------- Combat badges
add(B("b-cib","Combat badges","Combat Infantryman Badge (CIB)",1941,
 "Awarded to infantry Soldiers who actively take part in ground combat while assigned to an infantry unit in combat.",
 ["Established by the War Department, 27 Oct 1943 (para 8-6a)","Be an infantry Soldier performing infantry duties, assigned to an infantry unit in active ground combat, and take part in that combat (para 8-6b)",STAR2+" (para 8-6c)",g(1)],
 "Infantry plus ground combat. Established 27 Oct 1943.",[AR+"para 8-6",DP+"para 22-16a"]))
add(B("b-cmb","Combat badges","Combat Medical Badge (CMB)",1941,
 "Awarded to medical personnel assigned or attached to an infantry unit while it is in actual ground combat.",
 ["Originally the Medical Badge; created by the War Department, 1 Mar 1945 (para 8-7a)","The infantry unit must have been in contact with the enemy (para 8-7b)",STAR2+" (para 8-7d)",g(1)],
 "Medics with the infantry in combat. Created 1 Mar 1945.",[AR+"para 8-7",DP+"para 22-16a"]))
add(B("b-cab","Combat badges","Combat Action Badge (CAB)",2001,
 "Awarded to any Soldier personally present and under hostile fire while performing satisfactorily.",
 ["The Chief of Staff of the Army approved the CAB on 2 May 2005 (para 8-8a)","May be awarded to any Soldier; must be personally present and under hostile fire (para 8-8d)","Retroactive awards are not authorized before 18 Sep 2001 (para 8-8f)",g(1)],
 "Any Soldier under fire. Approved 2005, counts back to 18 Sep 2001.",[AR+"para 8-8",DP+"para 22-16a"]))
# ---------------- Special skill badges
add(B("b-eib","Special skill badges","Expert Infantryman Badge (EIB)",None,
 "Earned by passing the test given by an infantry unit; open to active duty infantry-field Soldiers.",
 ["Candidates must be on active duty orders with a primary MOS in CMF 11 or CMF 18 (para 8-9a)","Test is taken with an infantry unit of at least battalion size (para 8-9a)","Prerequisites and tests are set by the U.S. Army Infantry Center (para 8-9)",g(2)],
 "Expert tests: infantry EIB, medical EFMB, everyone else ESB.",[AR+"para 8-9",DP+"para 22-16a"]))
add(B("b-efmb","Special skill badges","Expert Field Medical Badge (EFMB)",None,
 "Earned by passing the Army medical field test.",
 ["Open to Soldiers on active duty, or assigned to a troop program unit in a Reserve Component unit or an AMEDD mobilization augmentation agency (para 8-10)","Officers must be assigned or detailed to an AMEDD corps (para 8-10)","Commanders of grade LTC/O-5 or above conduct the test and award the badge (para 8-10)",g(2)],
 "Medical field test: EFMB.",[AR+"para 8-10",DP+"para 22-16a"]))
add(B("b-esb","Special skill badges","Expert Soldier Badge (ESB)",None,
 "Earned by Soldiers outside the infantry, special forces, and medical career fields.",
 ["Regular Army, Army National Guard, and Army Reserve Soldiers except those in infantry, SF, and medical CMFs can compete (para 8-11)","The CG, U.S. Army Center for Initial Military Training is the sole authority (para 8-11)",g(2)],
 "ESB is for everyone not covered by EIB or EFMB.",[AR+"para 8-11",DP+"para 22-16a"]))
GR3=["Basic","Senior","Master"]
add(B("b-aviator","Special skill badges","Army Aviator Badges",None,
 "Aeronautical rating badges for Army aviators, in three degrees.",
 ["Three degrees: Basic, Senior, and Master Army Aviator Badge (para 8-12)","U.S. officers must have attained an aeronautical rating of Army aviator, senior Army aviator, or master Army aviator (para 8-12)",g(3)],
 "Three degrees: Basic, Senior, Master.",[AR+"para 8-12",DP+"para 22-16a"],
 variants=[V(f"{d} Army Aviator Badge") for d in GR3]))
add(B("b-flight-surgeon","Special skill badges","Flight Surgeon Badges",None,
 "Badges for Army Medical Corps officers who complete flight surgeon training, in three levels.",
 ["Three levels: Basic, Senior, and Master Flight Surgeon Badge (para 8-13)","Any Army Medical Corps officer who satisfactorily completes the training is eligible (para 8-13)","The Basic Flight Surgeon Badge may be awarded by the CG, USAACE (para 8-13)",g(3)],
 "Doctors who fly: Basic, Senior, Master.",[AR+"para 8-13",DP+"para 22-16a"],
 variants=[V(f"{d} Flight Surgeon Badge") for d in GR3]))
add(B("b-aviation","Special skill badges","Aviation Badges",None,
 "Badges for aircrew, in three degrees; they were formerly called Aircraft Crew Member badges.",
 ["Basic Aviation Badge (formerly Aircraft Crew Member Badge)","Senior Aviation Badge (formerly Senior Aircraft Crew Member Badge)","Master Aviation Badge (formerly Master Aircraft Crew Member Badge)","Must be on flying status under AR 600-106 or have a waiver (para 8-14)",g(3)],
 "Aviation badges used to be Aircraft Crew Member badges.",[AR+"para 8-14",DP+"para 22-16a"],
 variants=[V(f"{d} Aviation Badge") for d in GR3]))
add(B("b-eod","Special skill badges","Explosive Ordnance Disposal (EOD) Badges",None,
 "Badges for explosive ordnance disposal technicians, in three types.",
 ["Three types: Basic, Senior, Master (para 8-15)","Any commissioned officer or enlisted Soldier may be awarded the Basic EOD Badge (para 8-15)","Senior: 36 months cumulative service in a TOE or TDA EOD position after the basic badge (para 8-15)","Master: 60 months cumulative service in an EOD position since the Senior badge (para 8-15)",g(3)],
 "EOD: 36 months to Senior, 60 more to Master.",[AR+"para 8-15",DP+"para 22-16a"],
 variants=[V(f"{d} EOD Badge") for d in GR3]))
add(B("b-parachutist","Special skill badges","Parachutist Badges",None,
 "Awarded for completing the Airborne course, in three degrees by number of jumps.",
 ["Three degrees: Basic, Senior, Master (para 8-16)","Basic: satisfactorily complete the Airborne course (para 8-16)","Senior: a minimum of 30 jumps, with additional conditions (para 8-16)","Master: a minimum of 65 jumps, with additional conditions (para 8-16)","A bronze service star on the badge shows a combat parachute jump (para 8-16)","The wreath and star on the Master and Senior badges project slightly above the background trimming (DA Pam 670-1, para 21-32b)",g(4)],
 "Basic, then 30 jumps for Senior, 65 for Master. Bronze star = combat jump.",[AR+"para 8-16",DP+"paras 21-32b, 22-16a"],
 attachments=[A("Bronze service star","Combat parachute jump (para 8-16)"),A("Airborne background trimming","Oval worn beneath the badge (DA Pam 670-1, para 21-32b)")],
 variants=[V(f"{d} Parachutist Badge") for d in GR3]))
add(B("b-freefall","Special skill badges","Military Freefall Parachutist Badge",None,
 "Awarded for completing the military freefall program, in two degrees.",
 ["Complete a program of instruction in military freefall approved by USAJFKSWCS (para 8-17)","Two degrees: basic and jumpmaster (para 8-17)","A bronze service star may be worn on all degrees to show a military freefall combat jump (para 8-17)",g(4)],
 "Freefall: two degrees, basic and jumpmaster.",[AR+"para 8-17",DP+"para 22-16a"],
 attachments=[A("Bronze service star","Military freefall combat jump (para 8-17)")],
 variants=[V("Basic Military Freefall Parachutist Badge"),V("Jumpmaster Military Freefall Parachutist Badge")]))
add(B("b-pathfinder","Special skill badges","Pathfinder Badge",None,
 "Awarded for completing the Pathfinder Course.",
 ["Complete the Pathfinder Course conducted under the auspices of the U.S. Army Infantry School (para 8-18)",g(4)],
 "Pathfinder Course at the Infantry School.",[AR+"para 8-18",DP+"para 22-16a"]))
add(B("b-air-assault","Special skill badges","Air Assault Badge",None,
 "Awarded for completing an air assault training course.",
 ["Basic eligibility: satisfactory completion of an air assault training course (para 8-19)","Background trimming is worn beneath the badge (DA Pam 670-1, para 21-32b)",g(4)],
 "Air assault course = Air Assault Badge.",[AR+"para 8-19",DP+"paras 21-32b, 22-16a"],
 attachments=[A("Airborne background trimming","Oval worn beneath the badge (DA Pam 670-1, para 21-32b)")]))
add(B("b-space","Special skill badges","Space Badges",None,
 "Awarded for space-related education or training, in three degrees.",
 ["Three degrees: Basic, Senior, Master (para 8-20)","Basic eligibility: completion of the appropriate space-related education or training (para 8-20)",g(4)],
 "Space badge: Basic, Senior, Master.",[AR+"para 8-20",DP+"para 22-16a"],
 variants=[V(f"{d} Space Badge") for d in GR3]))
add(B("b-driver-tech","Special skill badges","Driver and Technician Badge",None,
 "Awarded to drivers, maintainers, technicians, specialists, and repairers, with bars for each vehicle or skill type.",
 ["Called the driver and mechanic badge in DA Pam 670-1 (2021); AR 600-8-22 (2024) calls it the Driver and Technician Badge","A commander of LTC/O-5 or higher may approve the Driver Badge (para 8-21)","No more than three clasps may be attached (DA Pam 670-1, para 22-16b(3)(b))","Worn only on the left pocket flap; not authorized on utility uniforms (DA Pam 670-1, paras 22-16b, 22-16d)",g(5)],
 "Bars on it: W wheels, T tracks, M motorcycles, A amphibious.",[AR+"para 8-21",DP+"para 22-16"],
 attachments=[A("Component bars","Authorized only for these types (para 8-21); AR 600-8-22 calls them component bars, DA Pam 670-1 calls them clasps",
   [V("Driver-W","Wheeled vehicles"),V("Driver-T","Tracked vehicles"),V("Driver-M","Motorcycles"),V("Driver-A","Amphibious vehicles"),
    V("Technician-S","Technician Senior: munitions, mechanical, or electrical equipment"),V("Technician-M","Technician Master: munitions, mechanical, or electrical equipment"),V("Operator-S","Special mechanical equipment")])]))
add(B("b-diver","Special skill badges","Diver Badges",None,
 "Five types of diver badges are authorized.",
 ["Master Diver Badge","First-Class Diver Badge","Salvage Diver Badge","Second-Class Diver Badge","Special Operations Divers Badge (formerly the Scuba Diver Badge)","Qualification and approval are set by AR 611-75 (para 8-22)",g(4)],
 "Five diver badges, top is Master Diver.",[AR+"para 8-22",DP+"para 22-16a"],
 variants=[V(n) for n in ("Master Diver Badge","First-Class Diver Badge","Salvage Diver Badge","Second-Class Diver Badge","Special Operations Divers Badge")]))
add(B("b-rigger","Special skill badges","Parachute Rigger Badge",None,
 "Awarded for completing the Parachute Rigger course.",
 ["Complete the Parachute Rigger course conducted by the U.S. Army Quartermaster School (para 8-23)","Officers qualify by completing one of the courses listed in para 8-23",g(3)],
 "Rigger course at the Quartermaster School.",[AR+"para 8-23",DP+"para 22-16a"]))
add(B("b-instructor","Special skill badges","Army Instructor Badges (AIB)",None,
 "Awarded to qualified instructors, in three levels.",
 ["Three levels: Basic, Senior, Master AIB (para 8-24)","Criteria are set by the CG, TRADOC; awarding authority is the first COL or GS-15 in the chain of command (para 8-24)","Civilian instructors may wear the AIB Lapel Pin (para 8-24)"],
 "AIB: Basic, Senior, Master. Civilians get a lapel pin.",[AR+"para 8-24"],
 variants=[V(f"{d} Army Instructor Badge") for d in GR3]))
# ---------------- Identification badges
add(B("b-presidential","Identification badges","Presidential Service Badge",1964,
 "Awarded to Soldiers assigned to the White House Office.",
 ["Badge and certificate established by EO 11174, 1 Sep 1964 (para 8-26)","Assignment of at least 1 year after 21 Jan 1989 (para 8-26)","Once awarded, may be worn as a permanent part of the uniform (para 8-26)"],
 "EO 11174, 1964. White House, one year.",[AR+"para 8-26"]))
add(B("b-vice-presidential","Identification badges","Vice Presidential Service Badge",1976,
 "Awarded to Soldiers assigned to the Office of the Vice President.",
 ["Established by EO 11926, 19 Jul 1976 (para 8-27)","At least 1 year of duty in the Office of the Vice President after 19 Dec 1974 (para 8-27)","Once awarded, may be worn as a permanent part of the uniform (para 8-27)"],
 "EO 11926, 1976. Vice President's office, one year.",[AR+"para 8-27"]))
add(B("b-osd-id","Identification badges","Office of the Secretary of Defense Identification Badge",None,
 "Shows satisfactory service on the Secretary of Defense's staff.",
 ["Authorized under 10 USC (para 8-28)","Indicates the Servicemember satisfactorily served on the SECDEF's staff (para 8-28)"],
 "SECDEF staff badge.",[AR+"para 8-28"]))
add(B("b-jcs-id","Identification badges","Joint Chiefs of Staff Identification Badge",1963,
 "Worn by members who served on the Joint Staff.",
 ["Established by Joint Chiefs of Staff Memorandum Policy No. 142, 3 Apr 1963 (para 8-29)","Regular Army and Reserve Component members are authorized to wear it (para 8-29)","Permanent award is prescribed in CJCSI 1100.01E (para 8-29)"],
 "JCS memo 142, 3 Apr 1963.",[AR+"para 8-29"]))
add(B("b-army-staff-id","Identification badges","Army Staff Identification Badge",1931,
 "Awarded to military personnel serving on the staff of HQDA principal officials.",
 ["First proposed by General Douglas MacArthur, 28 Dec 1931 (para 8-30)","Awarded by HQDA principal officials to personnel serving on their staff (para 8-30)","Permanent issue must be authorized by the principal officials (para 8-30)"],
 "MacArthur proposed it, 28 Dec 1931.",[AR+"para 8-30"]))
add(B("b-tomb-guard-id","Identification badges","Guard, Tomb of the Unknown Soldier Identification Badge",1958,
 "Earned by Soldiers who serve as Tomb guards.",
 ["Retroactive to 1 Feb 1958 for Regular Army personnel (para 8-31)","Honorable service of at least 9 months, not necessarily continuous (para 8-31)","Permanent or temporary wear may be authorized (para 8-31)"],
 "9 months of honorable Tomb service; back to 1 Feb 1958.",[AR+"para 8-31"]))
add(B("b-horseman-id","Identification badges","Military Horseman Identification Badge",None,
 "Earned by completing 100 Armed Forces Full Honors Funerals at Arlington National Cemetery.",
 ["Complete 100 Armed Forces Full Honors Funerals in Arlington National Cemetery (para 8-32)","Permanent or temporary wear may be authorized (para 8-32)"],
 "100 full honors funerals at Arlington.",[AR+"para 8-32"]))
# ---------------- Marksmanship
add(B("b-marksmanship","Marksmanship","Marksmanship qualification badges",None,
 "Expert, Sharpshooter, and Marksman badges; up to three qualification clasps can be worn on each badge.",
 ["Three levels: expert, sharpshooter, marksman (DA Pam 670-1, para 22-15a)","No more than three marksmanship qualification clasps may be worn on each badge (para 22-15c)","Other marksmanship badges listed: distinguished international shooter, distinguished rifleman, distinguished pistol shot, national trophy match, Inter-Service competition, U.S. Army excellence in competition rifleman and pistol shot (para 22-15a)",g(5),"Clasp weapon names were not found in the sources read, so they are not listed here"],
 "Expert, Sharpshooter, Marksman. Max three clasps.",[DP+"para 22-15"],
 variants=[V("Expert badge"),V("Sharpshooter badge"),V("Marksman badge")],
 attachments=[A("Qualification clasps","No more than three per badge (para 22-15c)")]))
# ---------------- Skill tabs
add(B("b-ranger-tab","Skill tabs","Ranger Tab",None,
 "Skill tab worn on the left sleeve above the unit patch.",
 ["Full-color tab, 2-3/8 inches long and 11/16 inch wide, with a 1/8-inch yellow border (DA Pam 670-1, para 22-16e)","Special skill tabs are centered 1/4 inch above the SSI on the left sleeve (para 22-16f)","One of four authorized skill tabs: Ranger, SF, Sapper, President's Hundred (AR 600-8-22, para 8-2d)",g(4)],
 "Ranger tab: yellow border, 2-3/8 inches.",[DP+"para 22-16e-f",AR+"para 8-2d"]))
add(B("b-sf-tab","Skill tabs","Special Forces Tab",None,
 "Teal blue skill tab worn on the left sleeve above the unit patch.",
 ["Full-color teal blue arc, 3-1/4 inches wide and 11/16 inch high (DA Pam 670-1, para 22-16e)","Special skill tabs are centered 1/4 inch above the SSI on the left sleeve (para 22-16f)",g(4)],
 "SF tab is teal blue, 3-1/4 inches.",[DP+"para 22-16e-f",AR+"para 8-2d"]))
add(B("b-sapper-tab","Skill tabs","Sapper Tab",None,
 "Red skill tab worn on the left sleeve above the unit patch.",
 ["Full-color red arc, 2-3/8 inches long and 11/16 inch wide, with a 1/8-inch red border (DA Pam 670-1, para 22-16e)","Special skill tabs are centered 1/4 inch above the SSI on the left sleeve (para 22-16f)",g(4)],
 "Sapper tab is red, 2-3/8 inches.",[DP+"para 22-16e-f",AR+"para 8-2d"]))
add(B("b-presidents-hundred-tab","Skill tabs","President's Hundred Tab",None,
 "Marksmanship tab of yellow cloth worn on the left sleeve of the AGSU.",
 ["Full-color tab of yellow cloth, 4-1/4 inches long and 5/8 inch high (DA Pam 670-1, para 22-15e)","Centered 1/4 inch above the SSI on the left sleeve of the AGSU (para 22-15e)","The bronze metallic brassard is not authorized for wear on the Army uniform (para 22-15e)","Tabs do not count toward the three-badge limit (para 22-15c)"],
 "President's Hundred: yellow, 4-1/4 inches.",[DP+"para 22-15e",AR+"para 8-2d"]))
add(B("b-airborne-trim","Skill tabs","Airborne background trimming",None,
 "Oval embroidered backing worn beneath parachutist or air assault badges.",
 ["Oval-shaped embroidered device in distinctive colors, 1-3/8 inches high and 2-1/4 inches wide (DA Pam 670-1, para 21-32b)","Worn beneath any authorized parachutist or air assault badge (para 21-32b)","The basic badge is centered on the trimming; the wreath and star project slightly above it (para 21-32b)","See AR 670-1 for who may wear it (para 21-32b)"],
 "Oval under the wings: 1-3/8 by 2-1/4 inches.",[DP+"para 21-32b"]))
# ---------------- Wear rules
add(B("b-wear-rules","Wear rules","Where badges are worn (ASU and AGSU)",None,
 "Badge limits and positions on the service uniforms.",
 ["Badges go 1/4 inch above the ribbons, or above the top of the pocket (DA Pam 670-1, para 22-16b(3)(d))","Only one combat or special skill badge from group 1 or group 2 above the ribbons (para 22-16b(3)(a))","Up to three badges above the ribbons or pocket flap (para 22-16b(3)(e))","Only three badges from groups 3, 4, or 5, including marksmanship, below the ribbons (para 22-16b(3)(b))","AGSU: a total of four badges at one time (para 22-16b(2))","Group 1: CIB, CMB, CAB. Group 2: EIB, EFMB, ESB. Group 3: astronaut device, aviator, flight surgeon, aviation, EOD, parachute rigger. Group 4: parachutist, pathfinder, freefall, air assault, diver, space, and Ranger, SF, Sapper tabs. Group 5: driver and mechanic, marksmanship. Group 6: physical fitness (APFU only) (para 22-16a)"],
 "Groups 1 and 2 on top, max three above and three below.",[DP+"para 22-16"]))
if __name__ == "__main__":
    p = sys.argv[1]; d = json.load(open(p))
    drop = {"b-sharpshooter","b-parachutist","r-ranger-tab","r-airborne-tab"}
    keep = [e for e in d["entries"] if e["id"] not in drop and not e["id"].startswith("b-") ]
    ids = [e["id"] for e in out]; assert len(ids)==len(set(ids))
    d["entries"] = keep + out; d["dataVersion"] = "0.4.0-army-badges"
    json.dump(d, open(p,"w"), indent=1, ensure_ascii=False); print("added", len(out), "kept", len(keep))

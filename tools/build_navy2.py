"""Navy uniforms (mynavyhr chapter 3 pages), medals (SECNAVINST 1650.1H arts 230/330, App B ch 1), and E-7..E-9 notes."""
import json
P = "app/src/main/assets/data/entries.json"
d = json.load(open(P)); es = [e for e in d["entries"] if not (e.get("branches") == ["Navy"] and e["id"].startswith(("nu-", "nm-", "n-e7", "n-e8", "n-e9", "n-e1x")))]
U = "https://www.mynavyhr.navy.mil/References/US-Navy-Uniforms/Uniform-Regulations/Chapter-3/"
SRC_U = "U.S. Navy Uniform Regulations (NAVPERS 15665), mynavyhr.navy.mil, chapter 3 page: "
SRC_A = "SECNAVINST 1650.1H, Navy and Marine Corps Awards Manual (read from the copy hosted at trngcmd.marines.mil), "
def uni(i, name, group, summary, comp, worn, page, extra=()):
    es.append({"id": i, "tab": "uniforms", "group": group, "name": name, "branches": ["Navy"], "eras": ["modern"], "yearFrom": None, "yearTo": None,
      "summary": summary, "facts": ["Basic components: " + "; ".join(comp), "When worn: " + worn] + list(extra), "remember": None, "swatches": [], "variants": [],
      "attachments": [], "proof": "official", "sources": [SRC_U + page + " (" + U + page + ")"], "image": None})
uni("nu-sdb-enl", "Service Dress Blue (male enlisted E-1 to E-6)", "Dress", "Blue dress jumper uniform for male E-1 to E-6.",
    ["Jumper, Blue Dress","Trousers, Blue, Broadfall","Hat, White","Shoes, Dress, Black","Socks, Black","Undershirt, White Crew Neck","Neckerchief","Rating Badge/Service Stripes","Ribbons"],
    "May be prescribed for wear year-round to all official functions when Dinner Dress or Full Dress uniforms are not prescribed",
    "Male-Enlisted/Service-Dress/Service-Dress-Blue/", ["Prescribable items: All Weather Parka, Black Leather Gloves, Mockneck"])
uni("nu-khaki-off", "Service Khaki (male officer)", "Service", "Khaki shirt and trousers service uniform for male officers.",
    ["Shirt, Khaki","Trousers, Khaki, Service","Cap, Combination, Khaki","Shoes, Dress, Black","Socks, Black","Undershirt, White","Belt, Khaki, w/Gold Clip","Buckle, Gold","Collar Insignia","Ribbons"],
    "Summer/Winter for office work, watchstanding, liberty, or business ashore when prescribed as uniform of the day", "Male-Officer/Service/Service-Khaki/")
uni("nu-sdw-off", "Service Dress White (male officer)", "Dress", "White dress coat uniform for male officers.",
    ["Coat, Service Dress White","Trousers, White","Cap, Combination, White","Shoes, Dress, White","Socks, White","Undershirt, White","Belt, White, w/Gold Clip","Buckle, Gold","Shoulder Boards (Hard)","Ribbons"],
    "May be prescribed for Summer wear when Formal Dress, Dinner Dress, or Full Dress", "Male-Officer/Service-Dress/-Service-Dress-White")
uni("nu-nwu3", "Navy Working Uniform Type III (male officer)", "Field", "Working uniform worn at all locations, before, during, and after the workday.",
    ["Shirt, NWU III","Trousers, NWU III","Cap, Eight Point, with ACE Logo","Boot, Black, Leather 9 inch","Socks, Black, Boot","Undershirt, Coyote Brown, Crewneck","Belt, Khaki, Cotton or Nylon w/Gold Clip","Buckle, Gold","Insignia, Chest (Embroidered)","Name/U.S. NAVY Service Tapes","Straps, Blousing"],
    "Authorized for wear at all locations, commuting and all normal task associated stops",
    "Male-Officer/Working/NWU-III", ["Not a liberty uniform. Alcohol consumption in NWUs off-base is prohibited","Prescribable items: Cap Knit Watch 8, NWU Type III Parka, black leather gloves, black mockneck"])
PREC = ["Medal of Honor","Navy Cross","Defense Distinguished Service Medal","Distinguished Service Medal","Silver Star Medal","Defense Superior Service Medal","Legion of Merit","Distinguished Flying Cross","Navy and Marine Corps Medal","Bronze Star Medal","Purple Heart Medal","Defense Meritorious Service Medal","Meritorious Service Medal","Air Medal","Joint Service Commendation Medal","Navy and Marine Corps Commendation Medal","Joint Service Achievement Medal","Navy and Marine Corps Achievement Medal","Combat Action Ribbon"]
def med(i, name, group, summary, facts, rem, para, name_in_prec, eras=None, yf=None):
    pos = PREC.index(name_in_prec) + 1
    es.append({"id": i, "tab": "medals", "group": group, "name": name, "branches": ["Navy"], "eras": eras or [], "yearFrom": yf, "yearTo": None,
      "summary": summary, "facts": facts + [f"Order of precedence among U.S. military personal decorations: number {pos} of {len(PREC)} (SECNAVINST 1650.1H, Appendix B to Chapter 1)"],
      "remember": rem, "swatches": [], "variants": [], "attachments": [], "proof": "official", "sources": [SRC_A + para], "image": None})
med("nm-navy-cross","Navy Cross","Decorations","Navy award for extraordinary heroism not justifying the Medal of Honor.",
    ["Awarded to those who distinguish themselves by extraordinary heroism, not justifying the award of the Medal of Honor (art 230, para 2.b.(1))","Citation opens: 'For extraordinary heroism . . .' (para 220.3.a)"],"Second only to the Medal of Honor in precedence.","Art 230 para 2; para 220.3.a","Navy Cross")
med("nm-dsm","Distinguished Service Medal (Navy)","Decorations","Award for exceptionally meritorious service in a duty of great responsibility.",
    ["Awarded to those who distinguish themselves by exceptionally meritorious service to the United States, in a duty of great responsibility (art 230, para 3.b)"],None,"Art 230 para 3; para 220.3.a","Distinguished Service Medal")
med("nm-nmcm","Navy and Marine Corps Medal","Decorations","Award for heroism not involving actual conflict with the enemy.",
    ["Awarded to those who distinguish themselves by heroism not involving actual conflict with the enemy (art 230, para 7.b.(1))"],"Heroism, not against the enemy.","Art 230 para 7","Navy and Marine Corps Medal")
med("nm-ncm","Navy and Marine Corps Commendation Medal","Decorations","Award for heroic or meritorious achievement or service.",
    ["Awarded to individuals, including foreign military personnel, who distinguish themselves on or after 7 December 1941 by heroic or meritorious achievement or service (art 230, para 12.b)"],None,"Art 230 para 12","Navy and Marine Corps Commendation Medal",["ww2","korea","vietnam","coldwar","gulf","modern"],1941)
med("nm-nam","Navy and Marine Corps Achievement Medal","Decorations","Award for professional or heroic achievement in superior performance of duties.",
    ["Awarded to members of the Armed Forces of the grade of lieutenant commander or major and junior thereto (art 230, para 13.b)"],"Lieutenant commander and below.","Art 230 para 13","Navy and Marine Corps Achievement Medal")
med("nm-car","Combat Action Ribbon","Decorations","Ribbon for active participation in ground or surface combat.",
    ["Awarded to members of the Navy, Marine Corps, and Coast Guard in the grade of captain/colonel and junior thereto who have actively participated in ground or surface combat (art 230, para 14.b.(1))"],"Captain and below, in ground or surface combat.","Art 230 para 14","Combat Action Ribbon")
es.append({"id":"nm-e-ribbon","tab":"medals","group":"Unit awards","name":"Navy \"E\" Ribbon","branches":["Navy"],"eras":["coldwar","gulf","modern"],"yearFrom":1974,"yearTo":None,
  "summary":"Ribbon for permanent duty on ships or in squadrons that won Battle Efficiency competitions.",
  "facts":["Denotes permanent duty on ships or in squadrons that won Battle Efficiency competitions after 1 July 1974 (art 330, para 4.b)","Navy personnel permanently attached to and serving with cited ships and units during the competitive cycle (para 4.b.(1)(a))"],
  "remember":"E for efficiency, after 1 July 1974.","swatches":[],"variants":[],"attachments":[],"proof":"official","sources":[SRC_A+"Art 330 para 4"],"image":None})
def enl(i, name, grade, summary, facts, rem):
    es.append({"id":i,"tab":"ranks","group":"Enlisted","name":name,"branches":["Navy"],"eras":["modern"],"yearFrom":None,"yearTo":None,"summary":summary,"facts":facts+["Secondary source: the official Navy text read did not state this insignia. Verify before relying on it"],
      "remember":rem,"swatches":[],"variants":[],"attachments":[],"proof":"unverified","sources":["Wikipedia, 'List of United States Navy enlisted rates' (secondary source, not official)"],"image":None})
enl("n-e7","Chief Petty Officer","E-7","Navy E-7. Dress blue rating badge: three chevrons and one rocker above the rating mark.",["Dress blue insignia has three chevrons and one rocker above the rating mark"],"Three chevrons and a rocker.")
enl("n-e8","Senior Chief Petty Officer","E-8","Navy E-8. One inverted star above the eagle.",["One inverted five-point star denotes senior chief"],"One star.")
enl("n-e9","Master Chief Petty Officer","E-9","Navy E-9. Two inverted stars above the eagle.",["Two inverted five-point stars denote master chief","The Master Chief Petty Officer of the Navy wears a third star above the eagle (per an undated copy of NAVPERS 15665 chapter 4: three gold stars above the eagle and one gold star in place of the specialty mark)"],"Two stars.")
d["entries"] = es; d["dataVersion"] = "0.9.0-navy-uniforms-medals"
json.dump(d, open(P, "w"), indent=1, ensure_ascii=False); print(len(es))

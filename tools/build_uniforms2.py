"""Marine Corps, Air Force/Space Force and Coast Guard uniform entries from the three uniform regulations. Idempotent."""
import json
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
MC='MCO 1020.34H, Marine Corps Uniform Regulations, 1 May 2018, para %s (PDF supplied by the app owner; later changes not checked)'
AF='DAFI 36-2903, Dress and Personal Appearance of Department of the Air Force Personnel, 29 Feb 2024 (corrective actions 13 Mar 2024), para %s (PDF supplied by the app owner)'
CG='COMDTINST M1020.6K, Coast Guard Uniform Regulations, 7 Jul 2020, para %s (PDF supplied by the app owner)'
def u(id_,group,name,br,summary,facts,src):
    e=by.get(id_) or {}
    e.update(id=id_,tab='uniforms',group=group,name=name,branches=br,eras=['modern'],yearFrom=None,yearTo=None,summary=summary,facts=facts,
      remember=None,swatches=[],variants=[],attachments=[],proof='official',sources=[src],image=e.get('image'))
    if id_ not in by: es.append(e); by[id_]=e
M=['Marine Corps']; A=['Air Force','Space Force']; C=['Coast Guard']
# --- Marine Corps
u('mu-evening','Formal','Evening Dress "A" and "B"',M,'Officer evening dress: "A" is white tie, "B" is black tie. SNCOs may wear a SNCO evening dress in place of blue dress.',
 ['"A" with white waistcoat (male) or long skirt (female) is for white tie occasions such as state occasions and formal dinners (2001.1)','"B" with scarlet cummerbund, or scarlet waistcoat for general officers, is for black tie occasions such as club affairs and the Marine Corps Birthday (2001.2)','Officers without evening dress wear blue dress "A" or blue-white dress "A" instead (2001.3)'],MC%'2001')
u('mu-blue-dress','Dress','Blue Dress "A", "B", "C" and "D"',M,'The Marine blue dress uniform family.',
 ['"A": blue coat with large medals; not worn on leave or liberty (2002.3a)','"B": same as "A" with ribbons instead of medals; authorized for leave and liberty (2002.3b)','"C": blue dress with long-sleeve khaki shirt, no coat (2002.3c)','"D": blue dress with short-sleeve khaki shirt, no coat (2002.3d)','Used for parades, ceremonies and formal or semiformal functions; NCOs and below year-round, officers and SNCOs by season (2002.1)'],MC%'2002')
u('mu-blue-white','Dress','Blue-White Dress "A" and "B"',M,'Blue dress coat with white trousers, skirt or slacks, for officers and SNCOs in the warm season.',
 ['"A" is the blue dress "A" with white trousers, skirt or slacks; not worn on leave or liberty (2003.1-2)','"B" is the same with ribbons in place of medals; can be worn on leave and liberty (2003.4)','Officers wear the scarlet necktab; SNCOs wear the black necktab (2003.2)','Not worn in ceremonies with enlisted Marines who are not authorized white trousers (2003.1)'],MC%'2003')
u('mu-service','Service','Service "A", "B" and "C"',M,'Green service coat and khaki shirt uniform, the Marine daily dress.',
 ['"A": service coat; may be worn on leave and liberty (2004.2a)','"B": service "A" without the coat, long-sleeve khaki shirt with tie (2004.2b)','"C": short-sleeve khaki shirt with service trousers or skirt (2004.2c)','Service "A" is normally worn when reporting for duty and at courts-martial or visits to civil officials (2004.1)'],MC%'2004')
u('mu-mccuu','Field','Marine Corps Combat Utility Uniform (MCCUU)',M,'The MARPAT camouflage working uniform.',
 ['Woodland MARPAT; sleeves rolled up in summer and down in winter (2005.1)','A working uniform, not for civilian settings; commuting is allowed but off-base stops are not, except emergencies and drive-through services (2005.2)'],MC%'2005')
u('mu-pt','Fitness','Marine Corps Physical Training Uniforms',M,'Green trunks and olive green undershirt, with cold weather and running suit options.',
 ['Standard: green general purpose trunks and olive green undershirt (2006.1)','Cold weather: olive green sweat shirt and pants lettered "USMC" with the Marine Corps emblem (2006.2)','Running suit: green jacket and trousers with reflective piping (2006.3)'],MC%'2006')
# --- Air Force / Space Force
note='The instruction covers Airmen and Guardians; references to Airmen also apply to Guardians unless it says otherwise (scope)'
u('au-mess','Formal','Formal and Mess Dress',A,'Evening functions where a black or white tie tuxedo or gown is the civilian match.',
 ['Formal dress is worn by officers only; mess dress is mandatory for officers and optional for enlisted (4.1)','Enlisted without mess dress may wear the semi-formal service dress (4.1)','No name tag on either; saluting is not required (4.1)',note],AF%'4.1')
u('au-semi','Formal','Semi-Formal Dress (enlisted)',A,'Enlisted semi-formal uniform: the service dress coat without a name tag.',
 ['Worn for semi-formal or official social functions as the commander prescribes (4.3)','White long-sleeve shirt and service dress trousers; ties mandatory (4.3.1)','Saluting is not required (4.3)',note],AF%'4.3')
u('au-service','Service','Service Dress (Class A and Class B)',A,'Blue service dress: Class A with the coat, Class B without it.',
 ['Class A: service dress coat, three buttons, single-breasted (4.5.1.1)','Class B: the service blue uniform without the coat (4.5.1)','Officer coats have epaulets; enlisted coats do not (4.5.1.1)',note],AF%'4.5')
u('au-ocp','Field','Operational Camouflage Pattern (OCP)',A,'The Air Force and Space Force duty and field uniform.',
 ['May be worn off base for short convenience stops and at restaurants where comparable casual wear is common (5.1)','Not worn off base at restaurants where most diners wear business attire or at places that mainly serve alcohol (5.1)','Do not starch or hot press; light ironing only (5.1)',note],AF%'5.1')
u('au-ptg','Fitness','Physical Training Gear (PTG)',A,'Required for fitness assessments and organized PT.',
 ['Worn during physical fitness assessments and organized PT events (8.1.2)','Authorized for retired personnel as well (8.1)',note],AF%'8.1')
u('au-fdu','Field','Flight Duty Uniform (FDU) and Desert FDU',A,'Flight duty uniforms for aircrew and other flight roles.',
 ['Both meet unique organizational and functional work requirements (9.1)','Members sew Velcro on the uniform and equipment so patches can be removed in contingencies (9.1)',note],AF%'9.1')
# --- Coast Guard
def cg(id_,grp,name,summary,facts,para): u(id_,grp,name,C,summary,facts,CG%para)
cg('cu-formal','Formal','Formal Dress Blue (Evening Dress or White Tie)','The most formal Coast Guard evening uniform.',['Worn year-round for official evening functions with white tie and tails, such as diplomatic service, ceremonial events and formal weddings','Prescribed for flag officers, captains, the MCPOCG, gold badge CMCs and those assigned where protocol requires it'],'3.B.1')
cg('cu-ddbj','Formal','Dinner Dress Blue Jacket (DDBJ)','Cold weather black tie jacket uniform.',['Cold weather; official evening functions with black tie','Prescribed for O-4 and above, the MCPOCG and gold badge CMCs; optional for O-3 and below'],'3.B.2')
cg('cu-ddwj','Formal','Dinner Dress White Jacket (DDWJ)','Warm weather black tie jacket uniform.',['Warm weather; official evening functions with black tie','Prescribed for O-4 and above, the MCPOCG and gold badge CMCs; optional for O-3 and below'],'3.B.3')
cg('cu-ddb','Formal','Dinner Dress Blue (DDB)','Cold weather black tie uniform, less formal than the dinner jackets.',['Cold weather; dinners, dances, receptions, weddings and ceremonies','Worn by all personnel'],'3.B.4')
cg('cu-ddw','Formal','Dinner Dress White (DDW)','Warm weather black tie uniform for officers.',['Warm weather; same functions as Dinner Dress Blue','Prescribed for O-3 and below (officers only)'],'3.B.5')
cg('cu-fdb','Dress','Full Dress Blue (FDB)','Ceremonial dress with large medals.',['Year-round: assuming or relinquishing command, change of command ceremonies, official visits with honors, occasions of state, weddings','All personnel; large medals over the left pocket'],'3.B.6')
cg('cu-fdw','Dress','Full Dress White (FDW)','Warm weather full dress for officers.',['Same occasions as Full Dress Blue, in warm weather','Officers only'],'3.B.7')
cg('cu-sdba','Service','Service Dress Blue "Alpha" (SDB "A")','Blue service dress with the coat for functions needing more formality than Bravo.',['Worn year-round by all personnel when prescribed','More formal than SDB "Bravo", less than full dress or dinner dress','Ribbons over the left pocket'],'3.B.8')
cg('cu-sdbb','Service','Service Dress Blue "Bravo" (SDB)','The everyday coat-and-tie blue service dress.',['Worn year-round by all personnel for business and social occasions where civilians would wear a coat and tie','Light blue shirt; enlisted collar insignia and shoulder boards are worn on the shirt'],'3.B.9')
cg('cu-sdw','Service','Service Dress White (SDW)','Warm weather white service dress for officers.',['Warm weather: official and business functions, ceremonies, parades, reviews and evening socials','Officers only'],'3.B.10')
cg('cu-tb','Service','Tropical Blue (short sleeve)','Short-sleeve blue shirt uniform.',['Worn year-round where a coat and tie are not required or expected'],'3.B.11')
cg('cu-tbls','Service','Tropical Blue (long sleeve)','Long-sleeve blue shirt uniform.',['Worn year-round where the SDB coat is relaxed'],'3.B.11.a')
cg('cu-wdb','Service','Winter Dress Blue (WDB)','Optional cold weather blue uniform.',['Optional, worn in place of SDB, authorized 1 Nov to 31 Mar','Not worn to functions where civilians would wear a coat and tie'],'3.B.12')
cg('cu-odu','Field','Operational Dress Uniform (ODU)','The Coast Guard working uniform.',['Worn year-round; appropriate when visiting other DoD agencies where the ODU is the comparable uniform','Allowed when traveling on TDY with the ball cap','Not a liberty uniform'],'3.B.13')
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False); print('ok',len(es))

import json
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
DOC='DAFI 36-2903, Dress and Personal Appearance of Department of the Air Force Personnel (29 Feb 2024)'
D=[
('pres','Presidential Service Badge and Vice-Presidential Service Badge','12.4.1','Worn during and after an assignment to White House duty. Worn only on the right side; no other badge removes them from the right side of the uniform. OPR: Military Assistant to the President.'),
('osd','Office of the Secretary of Defense (OSD) badge','12.4.2','Worn during and after assignment to specific duty in the OSD. OPR: OSD Deputy Chief Management Officer.'),
('jcs','Joint Chiefs of Staff (JCS) badge','12.4.3','Worn during and after assignment to specific duty in the JCS. OPR: JCS Manpower and Personnel Directorate (J1).'),
('haf','Headquarters Air Force (HAF) badge','12.4.4','Worn during assignment to the HAF or SecAF staff within the National Capital Region; permanent wear after at least 365 consecutive days in a qualifying position. The OSD and JCS badges take priority over it.'),
('aetc','AETC Instructor badge','12.4.5.1','May be worn with any blues combination; the AETC Instructor/Master badge may be worn during and after an assignment as an AETC instructor.'),
('jrotc','AFJROTC Instructor badge','12.4.5.2','Worn only while performing assigned duties; continue to wear while attending PME.'),
('dli','Defense Language Instructor badge','12.4.5.3','Worn only while performing assigned duties; continue to wear while attending PME. OPR: Defense Language Institute Foreign Language Center.'),
('recruit','Air Force Recruiting Service badge (AETC, AFRC and ANG versions)','12.4.6-12.4.8','Earned recruiting service badge is authorized for permanent wear by Airmen with an 8R special duty identifier in their records; continue to wear while attending PME. Separate badges exist for AETC, AFRC and the Air National Guard.'),
('uc','Unified Command badge','12.4.9','Worn only for the duration of assignment to a Combatant Commander\'s staff.'),
('army','Army Staff identification badge','12.4.10','Worn only while performing duties for the duration of the assignment. OPR: Army Military Personnel Center.'),
('nato','NATO badge','12.4.11','Worn only while performing duties for the duration of the assignment.'),
('un','United Nations (UN) badge','12.4.12','Worn only while performing duties for the duration of the assignment.'),
('sf','Security Forces shield','12.4.13','Worn while performing duties in control AFSC 31PX or 3P0XX billets only; wear with the beret continues while attending PME and on joint, instructor and recruiter duties.'),
('fire','Fire protection shield','12.4.14','Worn while performing fire protection duties; continues while attending PME or on joint, instructor, recruiter or other developmental special duty assignments.'),
('osi','Air Force Office of Special Investigations (AFOSI) shield','12.4.15','Worn as directed by the AFOSI commander.'),
('epme','Air Force Enlisted Professional Military Education (EPME) badge','12.4.16','Airmen and Guardians with the 8T000 special duty identifier, and Joint and Foreign EPME instructors, may permanently wear their awarded badge.'),
('deca','Defense Commissary Agency (DeCA) badge','12.4.17','Worn only while performing duties for the duration of the assignment.'),
('disa','Defense Information Systems Agency (DISA) badge','12.4.18','Worn only while performing duties for the duration of the assignment.'),
('dfas','Defense Finance and Accounting Service (DFAS) badge','12.4.19','Worn only while performing duties for the duration of the assignment.'),
('mps','Military Postal Service (MPS) badge','12.4.20','Worn only while performing postal duty.'),
('hg','USAF Honor Guard badge','12.4.21','Earned badge is permanent for Airmen with 8G000 (enlisted) or 85G0 (officer) special duty identifiers. Base Honor Guard badges are worn only while performing honor guard duties.'),
('ndu','National Defense University (NDU) badge','12.4.22','Worn only while assigned to the NDU faculty or staff.'),
('usafa','USAF Academy Permanent Professor badge','12.4.23','Worn during and after assignment to the specific duty.'),
('ig','Inspector General (IG) badge','12.4.24','Worn while performing duties in authorized IG billets; continue to wear while attending PME; may be worn upon retirement per para 14.3.'),
('iaafa','IAAFA badge','12.4.26','Worn after receiving SEI HJ (officer) or 450 (enlisted) during and after assignment to the Inter-American Air Forces Academy.'),
('dcma','Defense Contract Management Agency (DCMA) badge','12.4.27','Authorized during and after assignment to a qualifying position.'),
('nro','National Reconnaissance Office (NRO) badge','12.4.28','Worn only while performing duties for the duration of the assignment.'),
('dla','Defense Logistics Agency (DLA) badge','12.4.29','Worn only while performing duties for the duration of the assignment.'),
('gold','Gold Star Lapel Button','12.4.30','Authorized under 10 U.S.C. 1126 for issued Airmen on Air Force dress uniform coats; centered below the U.S. insignia on the widest part of the left lapel of the service coat, and centered on the left lapel of the mess dress coat even with the top row of medals.'),
('nok','Next of Kin Lapel Button','12.4.31','Authorized under 10 U.S.C. 1126 for issued Airmen on Air Force dress uniform coats; worn in the same place as the Gold Star Lapel Button, side by side with it if both are authorized, with no order of precedence between them.'),
]
new=[]
for k,n,p,t in D:
    new.append({'id':'b-af-'+k,'tab':'badges','group':'Duty badges','name':n,'branches':['Air Force','Space Force'],'eras':['modern'],
      'yearFrom':None,'yearTo':None,'summary':'Air Force and Space Force duty badge. '+t.split('. ')[0].rstrip('.')+'.',
      'facts':[f'Wear rule: {t} (para {p})','Duty badges reflect current and previous positions; wear is optional (para 12.4)','Design is not described in DAFI 36-2903; picture not yet added'],
      'remember':n,'swatches':[],'variants':[],'attachments':[],'proof':'official',
      'sources':[f'{DOC}, para {p}','Scope: the instruction covers Department of the Air Force personnel, Air Force and Space Force'],'image':None})
for e in new:
    if e['id'] in by:
        e['image']=by[e['id']].get('image'); es[es.index(by[e['id']])]=e
    else: es.append(e)
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False); print(len(new))

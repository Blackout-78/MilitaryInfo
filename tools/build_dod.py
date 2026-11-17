"""Applies DoD manual (DoDM 1348.33 Vol 2 Change 4; DoWM 1348.33 Vol 3 Change 6) findings. Idempotent."""
import json, copy
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
V2='DoDM 1348.33, Volume 2, Change 4, 7 May 2021, para %s (PDF supplied by the app owner)'
V3='DoWM 1348.33, Volume 3, Change 6, 14 Jul 2026, para %s (PDF supplied by the app owner)'
FIVE=['Army','Navy','Marine Corps','Air Force','Space Force']
TAG='DoD manual: '
def att(name,note,link=None):
    a={'name':name,'note':note,'variants':[]}
    if link: a['link']=link
    return a
def put(id_,branches,facts,src,attachments=None):
    e=by[id_]
    e['branches']=branches
    e['facts']=[f for f in e['facts'] if not f.startswith(TAG)]+[TAG+f for f in facts]
    e['sources']=[s for s in e['sources'] if not s.startswith(('DoDM 1348.33','DoWM 1348.33'))]+[src]
    if attachments is not None: e['attachments']=attachments
    e['proof']='official'

# --- new device entries
base=by['m-dev-star']
def dev(id_,name,branches,summary,facts,src):
    e=by.get(id_) or copy.deepcopy(base); e['id']=id_; e['name']=name; e['branches']=branches
    e['summary']=summary; e['facts']=facts; e['sources']=[src]; e['attachments']=[]; e['variants']=[]; e['remember']=None
    e['image']=None; e['swatches']=[]; e['proof']='official'
    if id_ not in by: es.append(e); by[id_]=e
S2=V2
dev('m-dev-campaign-star','Campaign star',FIVE,'Bronze or silver five-pointed star, 3/16 inch, worn for each designated campaign phase on a campaign medal.',
    ['Worn on the suspension and campaign ribbon of the Afghanistan, Iraq, Inherent Resolve, Southwest Asia Service and Kosovo Campaign Medals','A silver campaign star is worn in place of five bronze ones','The Southwest Asia Service Medal uses the bronze star only'],V2%'4.1, 4.9, 4.10, 4.12, 4.16')
dev('m-dev-fmf','Fleet Marine Force Combat Operations Insignia',['Navy'],'Miniature bronze Marine Corps emblem for Navy members assigned to Marine Corps units that take part in combat.',
    ['May be authorized by the Secretary of the Navy','Listed for the Afghanistan, Iraq, Inherent Resolve, Kosovo and Southwest Asia Service Medals, and for the Armed Forces Expeditionary and Global War on Terrorism Expeditionary Medals'],V2%'4.1, 4.3, 4.6, 4.9, 4.10, 4.12, 4.16')
dev('m-dev-hourglass','Hourglass device',FIVE+['Coast Guard'],'Bronze, silver or gold hourglass on the Armed Forces Reserve Medal for 10-year periods of Reserve service.',
    ['Bronze is 10 years, silver 20 years, gold 30 years','A gold and a bronze together mean 40 years','Shown first (the wearer\'s right), then the M device, when both are worn'],V2%'4.5.j')
dev('m-dev-star516','5/16 inch star',FIVE,'Gold or silver 5/16 inch star worn for later awards of several DoD-wide decorations.',
    ['Listed for the Military Service Crosses, Department DSMs, Silver Star, Legion of Merit, DFC, Bronze Star, Purple Heart, Meritorious Service Medal and Air Medal','Each military department sets the wear rules (Army uses oak leaf clusters; see the department regulation)'],V3%'3.1 to 3.9')
by['m-dev-arrowhead']['facts']=[f for f in by['m-dev-arrowhead']['facts'] if not f.startswith(TAG)]+[TAG+'Authorized for the Afghanistan, Iraq and Inherent Resolve Campaign Medals and the Armed Forces Expeditionary and Global War on Terrorism Expeditionary Medals, as authorized by the Secretary of the Army or the Secretary of the Air Force']
by['m-dev-arrowhead']['branches']=['Army','Air Force','Space Force']
by['m-dev-arrowhead']['sources']+= [V2%'4.1, 4.3, 4.6, 4.9, 4.10']
by['m-dev-star']['branches']=FIVE
by['m-dev-star']['facts']+= [TAG+'Service stars are bronze or silver, 3/16 inch; campaign medals use the campaign star instead']
by['m-dev-star']['sources']+= [V2%'4.3 to 4.15']

CAMP=att('Campaign star','Bronze for each designated campaign phase; a silver star replaces five bronze (DoD manual).','m-dev-campaign-star')
ARROW=att('Arrowhead','Bronze, 1/4 inch; may be authorized by the Secretary of the Army or the Secretary of the Air Force.','m-dev-arrowhead')
FMF=att('Fleet Marine Force Combat Operations Insignia','Navy members assigned to Marine Corps units in combat, if authorized by the Secretary of the Navy.','m-dev-fmf')
STAR=att('Service star','Bronze for each later award; a silver star replaces five bronze (DoD manual).','m-dev-star')

put('m-acm',FIVE,['Campaign medal; period begins 11 Sep 2001, end date to be set by the Secretary of Defense','Worn after the Kosovo Campaign Medal and before the Iraq Campaign Medal','Awarded once; a campaign star marks each campaign phase'],V2%'4.1',[CAMP,ARROW,FMF])
put('m-icm',FIVE,['Campaign medal; period 19 Mar 2003 to 31 Dec 2011','Worn after the Afghanistan Campaign Medal and before the Inherent Resolve Campaign Medal'],V2%'4.10',[CAMP,ARROW,FMF])
put('m-ircm',FIVE,['Campaign medal; period begins 15 Jun 2014 (Iraq, Syria and contiguous waters and airspace)','Worn after the Iraq Campaign Medal and before the GWOT Expeditionary Medal'],V2%'4.9',[CAMP,ARROW,FMF])
put('m-kcm',FIVE,['Campaign medal; period 24 Mar 1999 to 31 Dec 2013','Worn after the Southwest Asia Service Medal and before the Afghanistan Campaign Medal','Authorized device: campaign star (no arrowhead is listed)'],V2%'4.12',[CAMP,FMF])
put('m-swasm',FIVE,['Campaign medal; period 2 Aug 1990 to 30 Nov 1995','Worn after the Vietnam Service Medal and before the Kosovo Campaign Medal','Campaign star is bronze only'],V2%'4.16',[CAMP,FMF])
put('m-afem',FIVE,['Expeditionary medal; for operations after 1 Jul 1958 with foreign armed opposition or imminent hostile action','Worn after the Antarctica Service Medal and before the Vietnam Service Medal','One award per designated operation; a service star marks each later operation'],V2%'4.3',[STAR,ARROW,FMF])
put('m-gwotem',FIVE,['Expeditionary medal; for operations on or after 11 Sep 2001; each operation has its own period of award','Worn after the Inherent Resolve Campaign Medal and before the GWOT Service Medal'],V2%'4.6',[STAR,ARROW,FMF])
put('m-gwotsm',FIVE,['Individual service medal; non-deployed support on or after 11 Sep 2001','Worn after the GWOT Expeditionary Medal and before the Korea Defense Service Medal','No devices, no later awards'],V2%'4.7',[])
put('m-kdsm',FIVE,['Deployed service medal; period begins 28 Jul 1954','Worn after the GWOT Service Medal and before the Armed Forces Service Medal','No devices are authorized'],V2%'4.11',[])
put('m-afsm',FIVE,['Deployed service medal; for designated operations on or after 1 Jun 1992 with no foreign armed opposition (the non-combat match to the AFEM)','Worn after the Korea Defense Service Medal and before the Humanitarian Service Medal','One award per designated operation; service star is the only device'],V2%'4.4',[STAR])
put('m-hsm',FIVE,['Individual service medal; humanitarian operations after 1 Apr 1975','Worn after the Armed Forces Service Medal and before the Military Outstanding Volunteer Service Medal','Service star is the only device'],V2%'4.8',[STAR])
put('m-movsm',FIVE,['Individual service medal; outstanding volunteer service after 31 Dec 1992','Worn after the Humanitarian Service Medal; Army before the Army Sea Duty Ribbon, Navy and Marine Corps before the Sea Service Deployment Ribbon, Air Force and Space Force before the Overseas Service Ribbon (Short Tour)','Service star is the only device'],V2%'4.13',[STAR])
put('m-ndsm',FIVE,['Individual service medal for periods the Secretary of Defense names; the list of periods is kept on a DoD website, not in the manual','Worn after: Army, the Army of Occupation Medal; Navy and Marine Corps, the Navy Occupation Service Medal; Air Force and Space Force, the Air Force Recognition Ribbon','Service star is the only device'],V2%'4.14',[STAR])
put('m-pow',FIVE,['Individual service medal; held captive after 5 Apr 1917 (Title 10 USC 1128)','Worn right after decorations for heroism or merit and before any other service medal or ribbon','Service star is the only device'],V2%'4.15',[STAR])
put('m-antarctica',FIVE,['Deployed service medal; period begins 1 Jan 1946; area south of 60 degrees south','Worn after the NDSM and before the AFEM','Wintered Over clasp (bronze first, gold second, silver third or later; one only) and a matching disk on the ribbon'],V2%'4.2',[att('Wintered Over clasp and disk','Clasp on the suspension ribbon and a disk on the ribbon: bronze first winter, gold second, silver third or later; only one of each (DoD manual).')])
put('m-afrm',FIVE+['Coast Guard'],['Six versions of the medal; the front is the same, the back differs by Reserve component (Army, Navy, Marine Corps, Air Force, National Guard, Coast Guard)','Qualifies: 10 years in 12 consecutive years of Reserve service, or called to active duty on or after 1 Aug 1990, or volunteer service in designated operations','Hourglass shown first, then M device and numerals (numerals start with 2)'],V2%'4.5',[att('Hourglass device','Bronze 10 years, silver 20, gold 30; gold with bronze is 40 (DoD manual).','m-dev-hourglass'),att('M device','Bronze M for mobilization; numerals mark later awards.','m-dev-m'),att('Numeral','Arabic numerals, bronze or gold; see the department regulation.','m-dev-numeral')])

# --- DoDM Vol 3, DoD-wide decorations
put('m-silver-star',FIVE,['Gallantry in action that does not warrant the Medal of Honor or a service cross','Worn after the department DSM and before the Defense Superior Service Medal','Devices: oak leaf cluster (bronze or silver) and 5/16 inch star (gold or silver)'],V3%'3.3',[att('Oak leaf cluster','Bronze or silver; Army practice (department regulation governs).','m-dev-olc'),att('5/16 inch star','Gold or silver; used instead of an oak leaf cluster by some departments.','m-dev-star516')])
put('m-lom',FIVE,['Exceptionally meritorious conduct or service; worn after the Defense Superior Service Medal and before the DFC','Devices: C, R, oak leaf cluster (bronze or silver), 5/16 inch star (gold or silver)'],V3%'3.4',None)
put('m-dfc',FIVE,['Heroism or extraordinary achievement in aerial flight','Worn after the Legion of Merit; Army before the Soldier\'s Medal, Navy and Marine Corps before the Navy and Marine Corps Medal, Air Force and Space Force before the Airman\'s Medal','Devices: V, C, oak leaf cluster (bronze or silver), 5/16 inch star (gold or silver)'],V3%'3.5',None)
put('m-bsm',FIVE,['Valor or meritorious service not in aerial flight, after 6 Dec 1941','Worn after the Soldier\'s Medal (Army), Navy and Marine Corps Medal (Navy, Marine Corps) or Airman\'s Medal (Air Force, Space Force), and before the Purple Heart','Devices: V, oak leaf cluster (bronze or silver), 5/16 inch star (gold or silver)','After 30 Oct 2000 requires hostile fire or imminent danger pay or hazardous duty pay (Title 10 USC 1133)'],V3%'3.6',None)
put('m-purple-heart',FIVE,['Worn after the Bronze Star and before the Defense Meritorious Service Medal','Devices: oak leaf cluster (bronze or silver) and 5/16 inch star (gold or silver)'],V3%'3.7',None)
put('m-msm',FIVE,['Worn after the Defense Meritorious Service Medal and before the Air Medal','Devices: R, oak leaf cluster (bronze or silver), 5/16 inch star (gold or silver)'],V3%'3.8',None)
put('m-air-medal',FIVE,['Aerial flight achievement after 8 Sep 1939; worn after the MSM and before the Joint Service Commendation Medal','Devices: V, C, oak leaf cluster, 5/16 inch star, numerals (bronze or gold)'],V3%'3.9',None)
put('m-puc',FIVE,['Established by E.O. 10694 as amended by E.O. 14085; units after 7 Dec 1941','Army: before all other unit citations. Navy and Marine Corps: after the Combat Action Ribbon and before the Joint Meritorious Unit Award. Air Force and Space Force: after the Air Force Combat Action Medal and before the Joint Meritorious Unit Award','Devices: oak leaf cluster (bronze or silver) and 3/16 inch star (bronze or silver)'],V3%'3.10',None)
# service-specific decorations: devices only
for id_,para,extra in (('m-dsc','3.1',' (all Military Service Crosses: Distinguished Service Cross, Navy Cross, Air Force Cross)'),('m-dsm','3.2',' (each department has its own DSM)')):
    e=by[id_]
    e['facts']=[f for f in e['facts'] if not f.startswith(TAG)]+[TAG+'Service-specific'+extra+'; devices: '+('C, ' if id_=='m-dsm' else '')+'oak leaf cluster (bronze or silver), 5/16 inch star (gold or silver)']
    e['sources']=[s for s in e['sources'] if not s.startswith('DoWM')]+[V3%para]
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False)
print('ok')

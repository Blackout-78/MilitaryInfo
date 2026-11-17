"""Coast Guard entries and tags from COMDTINST M1650.25D (May 2008). Idempotent."""
import json
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
SRC='COMDTINST M1650.25D, Coast Guard Medals and Awards Manual, May 2008, para %s (PDF supplied by the app owner; 2008 edition, later changes not checked)'
CG=['Coast Guard']
def eras(f,t):
    if f is None: return []
    t=t or 2100; out=[]
    for k,(a,b) in {'ww1':(1914,1918),'interwar':(1919,1938),'ww2':(1939,1945),'korea':(1950,1954),'vietnam':(1961,1975),'coldwar':(1946,1991),'gulf':(1990,1995),'modern':(2001,2100)}.items():
        if f<=b and t>=a: out.append(k)
    return out
ORDER=['ww1','interwar','ww2','korea','vietnam','coldwar','gulf','modern']
def att(n,note,link=None):
    a={'name':n,'note':note,'variants':[]}
    if link: a['link']=link
    return a
# --- tag existing awards the Coast Guard manual lists
TAG={'m-navy-cross':'2.A.2','m-silver-star':'2.A.5','m-lom':'2.A.7','m-dfc':'2.A.8','m-bsm':'2.A.10','m-purple-heart':'2.A.11',
 'm-msm':'2.A.12','m-air-medal':'2.A.13','m-nmccm':'2.A.15','m-nmcam':'2.A.17','m-car':'2.A.19','m-puc':'3.B.1','m-nuc':'3.B.4','m-nmuc':'3.B.6',
 'm-ndsm':'5.A.5','m-antarctica':'5.A.6','m-afem':'5.A.8','m-swasm':'5.A.9','m-kcm':'5.A.10','m-acm':'5.A.11','m-icm':'5.A.12',
 'm-gwotem':'5.A.13','m-gwotsm':'5.A.14','m-kdsm':'5.A.15','m-afsm':'5.A.16','m-hsm':'5.A.17','m-movsm':'5.A.19','m-afrm':'5.A.25'}
MARK='Coast Guard manual: '
for k,p in TAG.items():
    e=by[k]
    if 'Coast Guard' not in e['branches']: e['branches']=e['branches']+CG
    s=SRC%p
    if s not in e['sources']: e['sources']=[x for x in e['sources'] if not x.startswith('COMDTINST M1650.25D')]+[s]
    f=MARK+'listed as an award Coast Guard members may be given'
    if f not in e['facts']: e['facts'].append(f)
# --- devices (para 5.A.25 and Chapter 1)
by['m-dev-hourglass']['facts']=[f for f in by['m-dev-hourglass']['facts'] if not f.startswith(MARK)]+[MARK+'on the Armed Forces Reserve Medal the hourglass is bronze, silver, gold, or gold plus bronze for the 1st to 4th 10-year period (5.A.25.b.2)']
by['m-dev-hourglass']['sources']=[x for x in by['m-dev-hourglass']['sources'] if not x.startswith('COMDTINST')]+[SRC%'5.A.25.b']
# Coast Guard device entries
base=by['m-dev-star']
def dev(id_,name,summary,facts,para):
    import copy
    e=by.get(id_) or copy.deepcopy(base)
    e.update(id=id_,name=name,branches=CG,summary=summary,facts=facts,sources=[SRC%para],attachments=[],variants=[],remember=None,image=None,swatches=[],proof='official')
    if id_ not in by: es.append(e); by[id_]=e
dev('m-dev-cg-o','Operational Distinguishing Device ("O")','Coast Guard "O" device for operational personal and unit awards.',
 ['For use on personal and unit awards','The citation must specifically authorize it','Needs direct operational "hands on" work: search and rescue, firefighting, law enforcement, disaster relief, pollution response, aids to navigation','Staff or administrative service does not qualify'],'1.B (Distinguishing Devices)')
dev('m-dev-cg-m','Mobilization ("M") device (Coast Guard Reserve)','"M" device on the Armed Forces Reserve Medal for call-up or contingency service.',
 ['For members who qualify under 5.A.25.a(2) or (3): called to active duty on or after 1 Aug 1990, or volunteering for a designated contingency','Centered on the ribbon with the hourglass on the wearer\'s right and the award number on the left','No number for the first award'],'5.A.25.b')
# --- new Coast Guard entries
D,SM,RB,UN='Decorations','Service medals','Ribbons','Unit awards'
def mk(id_,g,name,f,t,summary,facts,para):
    e=by.get(id_) or {}
    e.update(id=id_,tab='medals',group=g,name=name,branches=CG,eras=sorted(eras(f,t),key=ORDER.index),yearFrom=f,yearTo=t,summary=summary,
      facts=facts,remember=None,swatches=[],variants=[],attachments=[att('"O" device','May be authorized by the citation for operational awards (Chapter 1).','m-dev-cg-o')] if g in (D,UN) and id_ not in('m-cg-hsdsm','m-cg-9','m-dot-guardian','m-cg-bicent') else [],proof='official',sources=[SRC%para],image=None)
    if id_ not in by: es.append(e); by[id_]=e
mk('m-cg-hsdsm',D,'Homeland Security Distinguished Service Medal',2003,None,'Extraordinarily meritorious service in a duty of great responsibility while assigned to the Department of Homeland Security.',
 ['Authorized by Executive Order 12824, 7 Dec 1992, for the Department of Transportation','Moved to the Department of Homeland Security by Executive Order 13286, 1 Mar 2003','Service must have contributed materially to a major command or project of national significance'],'2.A.3')
mk('m-cg-dsm',D,'Coast Guard Distinguished Service Medal',1949,None,'Exceptionally meritorious service in a duty of great responsibility.',
 ['Authorized by 14 USC 492, 4 Aug 1949','Generally awarded to flag officers in principal commands','Duty must be clearly above normal and contribute materially to a major command or project'],'2.A.4')
mk('m-dot-guardian',D,'Department of Transportation Guardian Medal',None,None,'Senior transportation officials who strengthened the protection and security of the nation.',
 ['For senior government transportation officials','New recommendations are not authorized'],'2.A.6')
mk('m-cg-medal',D,'Coast Guard Medal',1949,None,'Heroism not involving actual conflict with an enemy.',
 ['Authorized by 14 USC 493, 4 Aug 1949'],'2.A.9')
mk('m-cgcm',D,'Coast Guard Commendation Medal',1947,None,'Meritorious service or achievement, below the Bronze Star and Meritorious Service Medal.',
 ['Began as the Commendation Ribbon with Metal Pendant, authorized by the Secretary of the Treasury, 26 Aug 1947','Renamed Coast Guard Commendation Medal by the Commandant, 2 Oct 1959'],'2.A.14')
mk('m-cgam',D,'Coast Guard Achievement Medal',1968,None,'Meritorious service or achievement below the Commendation Medal.',
 ['Authorized by the Commandant, 11 Jun 1968'],'2.A.16')
mk('m-cgloc',D,'Commandant\'s Letter of Commendation Ribbon',1979,None,'Ribbon bar for a Commandant\'s Letter of Commendation.',
 ['Authorized by the Commandant','Ribbon bar established 17 Mar 1979'],'2.A.18')
mk('m-cg-gold-lsm',D,'Gold Lifesaving Medal',1874,None,'Rescue or attempted rescue at the risk of one\'s own life, showing extreme and heroic daring.',
 ['Created by Congress in 1874; authorized now by 14 USC 500, 4 Aug 1949','Awarded by the Commandant','Not classed as a military decoration but authorized for wear by Coast Guard personnel','Military personnel on duty normally get a military award instead; leave or liberty status can qualify'],'4.A.1')
mk('m-cg-silver-lsm',D,'Silver Lifesaving Medal',1874,None,'Rescue or attempted rescue with extraordinary effort that falls short of the Gold medal.',
 ['Created by Congress in 1874; authorized now by 14 USC 500, 4 Aug 1949','Awarded by the Commandant','Not classed as a military decoration but authorized for wear by Coast Guard personnel','No time limit on recommending or awarding'],'4.A.1')
mk('m-cguc',UN,'Coast Guard Unit Commendation',1963,None,'Units with valorous or extremely meritorious service in support of operations, not in combat.',
 ['Authorized by the Commandant, 1 Jan 1963','Unit service must compare to an MSM for an individual','May go to units of other branches'],'3.B.3')
mk('m-cgmuc',UN,'Coast Guard Meritorious Unit Commendation',1973,None,'Units with valorous or meritorious service in support of operations, not in combat.',
 ['Authorized by the Commandant, 13 Nov 1973','Unit service must compare to a Coast Guard Achievement Medal for an individual','May go to units of other branches'],'3.B.5')
mk('m-cgmtc',UN,'Coast Guard Meritorious Team Commendation',1993,None,'Groups or teams not identified as a Coast Guard unit.',
 ['Authorized by the Commandant, 22 Dec 1993','Team service must compare to a Commandant\'s Letter of Commendation or higher for an individual','Does not block personal awards for the same action'],'3.B.7')
mk('m-cg-e',UN,'Coast Guard "E" Ribbon',1990,None,'Cutter crews that earn the overall operational readiness "E" during Tailored Annual Cutter Training.',
 ['Authorized by the Commandant, 25 Sep 1990','Awarded by area commanders; no citation','Serving aboard more than 50 percent of the training period qualifies'],'3.B.8')
mk('m-cg-bicent',UN,'Coast Guard Bicentennial Unit Commendation',1990,None,'Unit award for the Coast Guard\'s 200th anniversary.',
 ['Authorized by the Commandant, 2 Jan 1990'],'Enclosure 1 (Historical and Statutory Notes)')
mk('m-dot-ouA',UN,'Department of Transportation Outstanding Unit Award',1994,None,'Department of Transportation unit award, listed in the Coast Guard manual.',
 ['Authorized by the Secretary of Transportation, 3 Nov 1994'],'Enclosure 1 (Historical and Statutory Notes)')
mk('m-cg-9',SM,'DOT 9/11 Medal',2003,None,'Department of Transportation employees and citizens who responded to the attacks of 11 Sep 2001.',
 ['Authorized by the Secretary of Transportation, 11 Feb 2003','New recommendations are not authorized','The ribbon is also covered under 5.A.18'],'5.A.1')
mk('m-cggcm',SM,'Coast Guard Good Conduct Medal',1921,None,'Satisfactory enlisted service: proficiency in rating, sobriety, obedience, industry, courage and neatness.',
 ['Authorized by the Commandant, 18 May 1921','Since 1 Jul 1983, three consecutive years of satisfactory service','Only enlisted service counts'],'5.A.2')
mk('m-cgrgcm',SM,'Coast Guard Reserve Good Conduct Medal',1963,None,'Reserve enlisted members with satisfactory service over three consecutive years.',
 ['Authorized by the Commandant, 1 Feb 1963','Needs at least 70 retirement points in each of three consecutive anniversary years'],'5.A.3')
mk('m-cgepoy',RB,'Coast Guard Enlisted Person of the Year Ribbon',1999,None,'The most outstanding active duty and reserve enlisted person.',
 ['Authorized by the Commandant (COMDTINST 1650.36), 16 Feb 1999','Open to pay grades E-2 through E-6','Ribbon bar only, no medal'],'5.A.4')
mk('m-cg-arctic',SM,'Coast Guard Arctic Service Medal',1976,None,'Service in Arctic waters or flights north of the Arctic Circle.',
 ['Authorized by the Commandant, 20 May 1976','Summer (1 May-31 Oct) service north of 66 33 N, or winter service on a cutter in the Bering Sea, Davis Strait or Denmark Strait','Minimum 21 consecutive days; one award per deployment'],'5.A.7')
mk('m-cgsos',RB,'Coast Guard Special Operations Service Ribbon',1987,None,'Service in designated Coast Guard special operations.',
 ['Authorized by the Commandant, 1 Jul 1987'],'5.A.20')
mk('m-cgssr',RB,'Coast Guard Sea Service Ribbon',1984,None,'12 months of cumulative sea duty.',
 ['Authorized by the Commandant, 3 Mar 1984','Duty aboard a commissioned cutter 65 feet or more, with an Afloat Training Group, or aboard certain listed vessels','Open to active and inactive Coast Guard members, Reserve and some non-Coast Guard personnel'],'5.A.21')
mk('m-cgrdr',RB,'Coast Guard Restricted Duty Ribbon',1984,None,'A permanent change of station tour at a listed restricted shore unit.',
 ['Authorized by the Commandant, 3 Mar 1984','TDY, TAD, ADT and similar assignments do not count','Units where dependents may accompany the member do not qualify'],'5.A.22')
mk('m-cgbthgr',RB,'Coast Guard Basic Training Honor Graduate Ribbon',1984,None,'Highest graduate of each recruit company.',
 ['Authorized by the Commandant, 3 Mar 1984','Effective 1 Apr 1984','Prior-service members who graduated from other than Coast Guard recruit training are not eligible'],'5.A.23')
mk('m-cgrecr',RB,'Coast Guard Recruiting Service Ribbon',1980,None,'A successful tour of two consecutive years in recruiting.',
 ['Authorized by the Commandant 2 Nov 1995, amended 1 Jan 1996','Retroactive to tours completed on or after 1 Jan 1980','Reserve members need two years drilling at or augmenting a recruiting office'],'5.A.24')
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False); print('ok',len(es))

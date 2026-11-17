"""Navy and Marine Corps entries from SECNAVINST 1650.1H (22 Aug 2006). Idempotent."""
import json, copy
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
SRC='SECNAVINST 1650.1H, 22 Aug 2006, %s (PDF supplied by the app owner; 2006 edition, later changes not checked)'
AF=['Air Force','Space Force']; NV=['Navy']; MC=['Marine Corps']; NM=['Navy','Marine Corps']
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
OLC=lambda n='Second and later awards: bronze oak leaf cluster, silver for the sixth, eleventh and so on, or instead of five bronze (para A16.13).': att('Oak leaf cluster',n,'m-dev-olc')
V=att('V device','Valor. Since 7 Jan 2016 only on the DFC, BSM, Air Medal and ASCOM (para A16.16.3).','m-dev-v')
C=att('C device','Combat: exceptionally meritorious service in combat on or after 7 Jan 2016 (para A16.8).','m-dev-c')
R=att('R device','Remote: hands-on weapon system employment, on or after 7 Jan 2016 (para A16.14).','m-dev-r')
STAR=att('Service star','Bronze or silver five-pointed star; silver replaces five bronze (para A16.15).','m-dev-star')
def make(id_,group,name,f,t,summary,facts,para,att_=None,branches=AF,remember=None):
    e=by.get(id_) or {}
    e.update(id=id_,tab='medals',group=group,name=name,branches=branches,eras=sorted(eras(f,t),key=ORDER.index),yearFrom=f,yearTo=t,
        summary=summary,facts=facts,remember=remember,swatches=[],variants=[],attachments=att_ or [],proof='official',
        sources=[SRC%para],image=None)
    if id_ not in by: es.append(e); by[id_]=e

# device lines in the original helpers are not used: this manual leaves device wear to the uniform regulations
D,SM,RB,UN='Decorations','Service medals','Ribbons','Unit awards'
NOTE='Device and wear rules are in the Navy and Marine Corps uniform regulations, not in this manual'
def mk(id_,g,name,f,t,summary,facts,para,br=NM):
    make(id_,g,name,f,t,summary,facts,para,[],br)
mk('m-navy-cross',D,'Navy Cross',None,None,'Extraordinary heroism, not enough for the Medal of Honor, for Navy and Marine Corps members.',
 ['Authorized by 10 USC 6242','Must be in the presence of great danger or at great personal risk, setting the person apart from shipmates or fellow Marines','An accumulation of minor acts does not justify the award','Worn right after the Medal of Honor'],'Chapter 2 Section 3 item 2')
mk('m-navy-dsm',D,'Navy Distinguished Service Medal',None,None,'Exceptionally meritorious service in a duty of great responsibility.',
 ['Authorized by 10 USC 6243','In general for officers in principal commands at sea or in the field','Worn after the Defense Distinguished Service Medal and before the Silver Star'],'Chapter 2 Section 3 item 3')
mk('m-nmcm',D,'Navy and Marine Corps Medal',None,None,'Heroism not involving actual conflict with the enemy; the senior peacetime heroism award.',
 ['Authorized by 10 USC 6246','Lifesaving acts must be at the risk of one\'s own life','Not a lifesaving medal: it depends on the actual life-threatening risk','Worn after the Distinguished Flying Cross and before the Bronze Star'],'Chapter 2 Section 3 item 7')
mk('m-nmccm',D,'Navy and Marine Corps Commendation Medal',1941,None,'Heroic or meritorious achievement or service on or after 7 Dec 1941, below the Bronze Star.',
 ['Navy Commendation Ribbon authorized by ALNAV 11, 11 Jan 1944; medal pendant 22 Mar 1950; renamed 19 Aug 1994','Open to foreign military personnel','Combat Distinguishing Device may be authorized','Worn after the Joint Service Commendation Medal'],'Chapter 2 Section 3 item 12')
mk('m-nmcam',D,'Navy and Marine Corps Achievement Medal',1961,None,'Meritorious service or achievement for lieutenant commander or major and below, below the Commendation Medal.',
 ['Service on or after 1 May 1961','Not for aerial flight service after 1 Jan 1969 (the Air Medal fits that)','Combat Distinguishing Device authorized for service after 17 Jul 1967, discontinued Apr 1974, reauthorized 17 Jan 1991','Renamed 19 Aug 1994'],'Chapter 2 Section 3 item 13')
mk('m-car',D,'Combat Action Ribbon',1969,None,'Active participation in ground or surface combat under enemy fire.',
 ['Authorized by SECNAVNOTE 1650, 17 Feb 1969','Navy, Marine Corps and Coast Guard (when under Navy control), captain or colonel and below','Not automatic from a combat area or a Purple Heart','Not for aerial combat; the Strike/Flight Air Medal covers that','Direct exposure to an enemy IED counts, retroactive to 7 Oct 2001'],'Chapter 2 Section 3 item 14',['Navy','Marine Corps','Coast Guard'])
mk('m-nuc',UN,'Navy Unit Commendation',1944,None,'Units with outstanding heroism in action, below the Presidential Unit Citation, or extremely meritorious service in support of operations.',
 ['Authorized by ALNAV 224, 18 Dec 1944','Awarded by the Secretary of the Navy','Level of service compares to a Silver Star or Legion of Merit for an individual','May go to units of other branches and friendly foreign forces'],'Chapter 3 Section 3 item 2')
mk('m-nmuc',UN,'Meritorious Unit Commendation (Navy and Marine Corps)',1967,None,'Valorous or meritorious unit achievement, below the Navy Unit Commendation.',
 ['Authorized by SECNAV Notice 1650, 17 Jul 1967','Awarded by the Secretary of the Navy, CNO or Commandant','Level of service compares to a Bronze Star for an individual','May go to units of other branches and friendly foreign forces'],'Chapter 3 Section 3 item 3')
mk('m-ngcm',SM,'Navy Good Conduct Medal',1869,None,'The all-around good enlisted sailor.',
 ['Established by the Secretary of the Navy, 26 Apr 1869','Three years of continuous active service as an enlisted person after 1 Jan 1996','Four years for 1 Nov 1963 through 31 Dec 1995','Commanding officers award it since 1 Feb 1971'],'Chapter 4 item 2',NV)
mk('m-mcgcm',SM,'Marine Corps Good Conduct Medal',1896,None,'Good behavior and faithful service in the Marine Corps.',
 ['Established by Special Order No. 49, 20 Jul 1896','Any three years of continuous active service after 10 Dec 1945'],'Chapter 4 item 3',MC)
mk('m-nrmsm',SM,'Naval Reserve Meritorious Service Medal',1958,None,'Navy Reservists on inactive duty who serve with distinction; the Reserve counterpart to the Good Conduct Medal.',
 ['Authorized by the Secretary of the Navy, 22 Jun 1964','Service counted from 1 Jul 1958','Four years through 31 Dec 1995'],'Chapter 4 item 4',NV)
mk('m-smcrm',SM,'Selected Marine Corps Reserve Medal',1925,None,'Service in the Selected Marine Corps Reserve.',
 ['Three-year period from 1 Jan 1996; four years from 1 Jul 1925 through 31 Dec 1995','Requires attendance at annual field training with an SMCR unit'],'Chapter 4 item 5',MC)
mk('m-nem',SM,'Navy Expeditionary Medal',1936,None,'Landing on foreign territory against armed opposition, where no other campaign or service medal was awarded.',
 ['Authorized by Navy Department General Order 84, 5 Aug 1936','Only personnel attached to an approved ship or unit who took part','The CNO keeps the list of eligible ships and units'],'Chapter 4 item 6',NV)
mk('m-mcem',SM,'Marine Corps Expeditionary Medal',1919,None,'Marine Corps counterpart to the Navy Expeditionary Medal.',
 ['Authorized by M.C.G.O. 33, 8 May 1919','Only when Navy and Marine Corps units were the sole participants','If other branches took part, the Armed Forces Expeditionary Medal is the right award'],'Chapter 4 item 7',MC)
mk('m-nasr',RB,'Navy Arctic Service Ribbon',1982,None,'28 days above the Arctic Circle after 1 Jan 1982.',
 ['Authorized by OPNAVNOTE 1650, 3 Jun 1987','Days need not be consecutive; remote ice camp and under-ice dive days count double','No subsequent award'],'Chapter 4 item 21')
mk('m-nrssr',RB,'Naval Reserve Sea Service Ribbon',1974,None,'24 months of service aboard a Navy Reserve ship or unit after 15 Aug 1974.',
 ['Authorized by SECNAV Note 5420, 28 May 1986','Any mix of active and Selected Reserve service'],'Chapter 4 item 22',NV)
mk('m-nmcosr',RB,'Navy and Marine Corps Overseas Service Ribbon',1986,None,'Overseas shore duty: 12 months for active duty, 30 consecutive or 45 cumulative days for Reserve.',
 ['Authorized by SECNAV letter 1650, 17 Sep 1986','Navy members with Marine units follow Marine Corps policy, and the reverse'],'Chapter 4 item 23')
mk('m-nrecr',RB,'Navy Recruiting Service Ribbon',1973,None,'Support of recruiting in listed Navy recruiting activities.',
 ['Established 2 Feb 1989; made retroactive to 1 Jul 1973','Second and later awards use a 3/16 inch bronze star'],'Chapter 4 item 24',NV)
mk('m-mcrecr',RB,'Marine Corps Recruiting Ribbon',1995,None,'Marines with recruiter MOS 8411 or 8412 who complete a successful recruiting tour.',
 ['Authorized by SECNAV letter 1650, 7 Jun 1995','Subsequent awards for each later tour'],'Chapter 4 item 25',MC)
mk('m-mcdir',RB,'Marine Corps Drill Instructor Ribbon',1997,None,'Marines with MOS 8511 who served in a drill instructor billet, and listed recruit training staff.',
 ['Authorized by SECNAV letter 1650, 15 Jul 1997'],'Chapter 4 item 26',MC)
mk('m-mcsgr',RB,'Marine Corps Security Guard Ribbon',1997,None,'Marines with MOS 8151 serving with the Marine Security Guard Battalion at embassies.',
 ['Authorized by SECNAV letter 1650, 15 Jul 1997','Headquarters, MSG Battalion personnel are not eligible'],'Chapter 4 item 27',MC)
mk('m-nrtsr',RB,'Navy Recruit Training Service Ribbon',1998,None,'Recruit Division Commanders at Recruit Training Command, Great Lakes, after a successful tour.',
 ['Established by the Secretary of the Navy, 13 Mar 1998','Support staff, instructors and others at the command are not eligible'],'Chapter 4 item 28',NV)
mk('m-ncgr',RB,'Navy Ceremonial Guard Ribbon',2001,None,'Service in the Navy Ceremonial Guard, Washington, DC, on or after 1 May 2001.',
 ['Authorized by SECNAV letter 0750, 12 Dec 2003','A successful tour of at least two years, with at least 18 months in drilling status'],'Chapter 4 item 29',NV)
for k in list(by):
    if by[k].get('sources') and by[k]['sources'][0].startswith('SECNAVINST'):
        if NOTE not in by[k]['facts']: by[k]['facts'].append(NOTE)
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False); print('ok',len(es))

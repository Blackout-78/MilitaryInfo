"""Air Force and Space Force entries from DAFMAN 36-2806 (Change 3, 13 Aug 2025). Idempotent."""
import json, copy
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
SRC='DAFMAN 36-2806, 27 Oct 2022, Change 3, 13 Aug 2025, para %s (PDF supplied by the app owner)'
AF=['Air Force','Space Force']
def eras(f,t):
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
D,SM,RB,UN='Decorations','Service medals','Ribbons','Unit awards'
make('m-af-cross',D,'Air Force Cross',1960,None,'Extraordinary heroism in action, not enough for the Medal of Honor, for Air Force and Space Force members.',
 ['Established by PL 88-593 (1965), effective 6 Jul 1960','Awarded to members of the Air Force or Space Force','Second highest decoration after the Medal of Honor in the military service crosses'],'A2.3',[OLC()])
make('m-af-dsm',D,'Air Force Distinguished Service Medal',1918,None,'Exceptionally meritorious service in a duty of great responsibility; limited mostly to general officers.',
 ['Established by act of Congress, 9 Jul 1918','Restricted to a minimum 18 months in a general officer position and 36 months as a general officer, and to the CMSAF and CMSSF','Authorized devices: C device and oak leaf cluster'],'A2.4',[C,OLC()])
make('m-airmans',D,"Airman's Medal",1960,None,'Heroism with voluntary risk of life not involving conflict with an armed enemy.',
 ['Established 1960 (10 USC 9280)','Saving a life is not required; the act must involve personal hazard','Not awarded for normal performance of duty'],'A2.8',[OLC()],['Air Force'])
make('m-aam',D,'Aerial Achievement Medal',1988,None,'Sustained meritorious achievement while taking part in aerial flight.',
 ['Established by the Secretary of the Air Force, 5 Feb 1988','Not for single-event flights','Since 9 Jan 2003 includes remotely piloted aircraft operators'],'A2.13',[OLC()])
make('m-ascom',D,'Air and Space Commendation Medal',1958,None,'Meritorious achievement or service, valor or heroism, for O-6 and below.',
 ['Established 24 Mar 1958; renamed from Air Force Commendation Medal on 16 Nov 2020','Not awarded to general or flag officers','Authorized devices: V, C, R and oak leaf cluster'],'A2.14',[V,C,R,OLC()])
make('m-asam',D,'Air and Space Achievement Medal',1980,None,'Outstanding achievement or meritorious service, for O-5 and below.',
 ['Established 12 Oct 1980; renamed from Air Force Achievement Medal on 16 Nov 2020','Not for aerial achievement or retirement','The V device was authorized only for acts from 11 Jan 1996 to 6 Jan 2016','Authorized devices: C, R and oak leaf cluster'],'A2.15',[C,R,OLC()])
make('m-cam',SM,'Combat Action Medal',2001,None,'Actively taking part in ground or air combat, outside the wire and under enemy fire.',
 ['Established by the Secretary of the Air Force, 15 Mar 2007 (renamed from Air Force Combat Action Medal 16 Nov 2020)','For members E-1 through O-6 on or after 11 Sep 2001','May be awarded to members of other military departments','Authorized device: gold star'],'A14.2',[att('Gold star','Authorized device (para A14.2.8; see Attachment 16).')])
make('m-crm',SM,'Combat Readiness Medal',1960,None,'Sustained individual combat mission readiness after 1 Aug 1960.',
 ['Authorized by the Secretary of the Air Force, 9 Mar 1964','Oak leaf cluster for each additional 24 months of qualifying service','From 18 Apr 2018, must be a crew member in a designated weapon system in an operational combat or combat support unit'],'A14.3',[OLC()])
make('m-afgcm',SM,'Air Force Good Conduct Medal',1963,None,'Exemplary conduct, efficiency and fidelity for enlisted Air Force members.',
 ['Established by EO 8809; service on or after 1 Jun 1963','Terminated 6 Feb 2006, reinstated 22 Nov 2008, retroactive to 6 Feb 2006','Service in a sister service is not counted'],'A14.4',[OLC()],['Air Force'])
make('m-sfgcm',SM,'Space Force Good Conduct Medal',2019,None,'Exemplary conduct for enlisted Space Force members.',
 ['Established by the Secretary of the Air Force, 30 Aug 2023, under the 3 Oct 2022 amendment to EO 8809','Service on active duty with the Space Force on or after 20 Dec 2019','Service in a sister service is not counted'],'A14.5',[OLC()],['Space Force'])
make('m-arfmsm',SM,'Air Reserve Forces Meritorious Service Medal',1964,None,'Enlisted Air National Guard and Air Force Reserve service of good behavior, efficiency and fidelity.',
 ['Established 7 Apr 1964','4 continuous years from 1 Apr 1965, or 3 continuous years from 1 Jul 1975','Creditable service ends when called to active duty'],'A14.6',[OLC()],['Air Force'])
make('m-oayr',RB,'Outstanding Airman of the Year Ribbon',1968,None,'Competitors and selectees in the Outstanding Airmen of the Year program.',
 ['Established 21 Feb 1968','Authorized devices: oak leaf cluster and bronze service star'],'A14.7',[OLC(),STAR])
make('m-asrr',RB,'Air and Space Recognition Ribbon',1980,None,'Overall winners of a headquarters or functional community award.',
 ['Established 10 Oct 1980; renamed from Air Force Recognition Ribbon on 16 Nov 2020','Not for organizations, units or activities'],'A14.8',[OLC()])
make('m-rcecm',SM,'Remote Combat Effects Campaign Medal',2001,None,'Direct participation in a DoD combat operation, mainly by remotely piloted aircraft, cyber and similar crews.',
 ['Established by the Secretary of the Air Force, 22 May 2019','For service on or after 11 Sep 2001','Worn after the MOVSM and before the Air and Space Campaign Medal','Authorized device: bronze service star'],'A14.9',[STAR])
make('m-ascm',SM,'Air and Space Campaign Medal',1999,None,'Direct support of a designated significant operation from home station or outside DoD campaign areas.',
 ['Established 24 Apr 2002, for service after 24 Mar 1999','30 consecutive or 60 non-consecutive days of direct support','Authorized device: service star'],'A14.10',[STAR])
make('m-ndosm',SM,'Nuclear Deterrence Operations Service Medal',1991,None,'Direct support of nuclear deterrence operations on or after 27 Dec 1991.',
 ['Established by the Secretary of the Air Force, 27 May 2014','Basic medal: 120 consecutive or 179 non-consecutive days in a unit supporting the nuclear enterprise','Worn right after the Air and Space Campaign Medal','Devices: oak leaf cluster and Nuclear N device'],'A14.11',[OLC(),att('Nuclear N device','Bronze N for duty in an ICBM missile complex or with nuclear-laden aircraft (para A16.11).','m-dev-nuclear-n')])
make('m-asor',RB,'Air and Space Overseas Ribbon (Short and Long Tour)',1980,None,'Completion of an overseas tour; one ribbon for short tours, one for long tours.',
 ['Established 12 Oct 1980; renamed from Air Force Overseas Ribbon on 16 Nov 2020','Devices: oak leaf cluster and Arctic A device (short tour ribbon)'],'A14.12',[OLC(),att('Arctic A device','Bronze A on the short tour ribbon for an Arctic Circle tour or Pituffik Space Base (Thule) service (para A16.3).','m-dev-arctic-a')])
make('m-asesr',RB,'Air and Space Expeditionary Service Ribbon',1999,None,'Completion of a contingency deployment after 1 Oct 1999.',
 ['Established by the Secretary of the Air Force, 18 Jun 2003; gold border added April 2004 for combat operations','Renamed from Air Force Expeditionary Service Ribbon on 16 Nov 2020','Devices: oak leaf cluster and gold border'],'A14.13',[OLC()])
make('m-aslsa',RB,'Air and Space Longevity Service Award',1957,None,'Each 4 years of honorable federal military service.',
 ['Established 25 Nov 1957; renamed from Air Force Longevity Service Award on 16 Nov 2020','Authorized device: oak leaf cluster'],'A14.14',[OLC()])
make('m-dsdr',RB,'Developmental Special Duty Ribbon',2014,None,'Completion of a developmental special duty.',
 ['Established by the Secretary of the Air Force, 4 Sep 2014; not retroactive','Worn right after the Air and Space Longevity Service Award'],'A14.15',[OLC()])
make('m-epmeg',RB,'Air and Space Forces Enlisted Professional Military Education Graduate Ribbon',1962,None,'In-residence graduates of certified enlisted professional military education schools.',
 ['Established 28 Aug 1962','Oak leaf cluster for each higher level completed'],'A14.16',[OLC()])
make('m-bmthgr',RB,'Basic Military Training Honor Graduate Ribbon',1976,None,'Honor graduates of basic military training.',
 ['Established 3 Apr 1976, effective 30 Jul 1976','No devices'],'A14.17',[])
make('m-saemr',RB,'Small Arms Expert Marksmanship Ribbon',1963,None,'Qualifying Expert with the rifle or an issued handgun.',
 ['Established 28 Aug 1962, effective 1 Jan 1963','A bronze service star shows Expert with both rifle and handgun (after 22 Jun 1972)','Open to Space Force members from 20 Dec 2019'],'A14.18',[STAR])
make('m-astr',RB,'Air and Space Training Ribbon',1974,None,'Completion of initial accession training after 14 Aug 1974.',
 ['Authorized 12 Oct 1980; renamed from Air Force Training Ribbon on 16 Nov 2020','Open to Space Force members from 20 Dec 2019'],'A14.19',[OLC()])
make('m-guc',UN,'Gallant Unit Citation',2001,None,'Units showing extraordinary heroism against an armed enemy on or after 11 Sep 2001, below the Presidential Unit Citation.',
 ['Established by the Secretary of the Air Force, March 2004'],'A9.2',[OLC()])
make('m-mua',UN,'Meritorious Unit Award',2001,None,'Exceptionally meritorious service in direct support of combat operations for at least 90 continuous days.',
 ['Established by the Secretary of the Air Force, March 2004','Awarded to squadrons, groups, deltas and wings'],'A9.3',[OLC()])
make('m-asoua',UN,'Air and Space Outstanding Unit Award',1954,None,'Numbered units with exceptionally meritorious service or outstanding achievement.',
 ['Established 6 Jan 1954; renamed from Air Force Outstanding Unit Award on 16 Nov 2020','V device no longer authorized on unit awards since 1 Jan 2014'],'A9.4',[OLC()])
make('m-asoea',UN,'Air and Space Organizational Excellence Award',1969,None,'Unnumbered Department of the Air Force organizations and activities.',
 ['Established August 1969; renamed from Air Force Organizational Excellence Award on 16 Nov 2020'],'A9.5',[OLC()])

# devices
base=copy.deepcopy(by['m-dev-star'])
def dev(id_,name,branches,summary,facts,para):
    e=by.get(id_) or copy.deepcopy(base)
    e.update(id=id_,name=name,branches=branches,summary=summary,facts=facts,sources=[SRC%para],attachments=[],variants=[],remember=None,image=None,swatches=[],proof='official')
    if id_ not in by: es.append(e); by[id_]=e
dev('m-dev-arctic-a','Arctic A device',AF,'Bronze letter A on the Air and Space Overseas Ribbon (short tour).',
 ['For a short tour above the Arctic Circle and service at Pituffik Space Base (formerly Thule), Greenland','Only one A device, however many tours','Worn to the right of any oak leaf clusters'],'A16.3')
dev('m-dev-nuclear-n','Nuclear N device',AF,'Bronze letter N on the Nuclear Deterrence Operations Service Medal.',
 ['For duty in a missile complex supporting ICBM operations or with nuclear-laden aircraft','Only one N device, however many assignments','Worn to the wearer\'s right of oak leaf clusters'],'A16.11')
AFN='Department of the Air Force: '
def addfact(id_,branches,facts,para):
    e=by[id_]
    e['branches']=sorted(set(e['branches'])|set(branches),key=['Army','Navy','Marine Corps','Air Force','Coast Guard','Space Force'].index)
    e['facts']=[f for f in e['facts'] if not f.startswith(AFN)]+[AFN+f for f in facts]
    e['sources']=[s for s in e['sources'] if not s.startswith('DAFMAN 36-2806')]+[SRC%para]
addfact('m-dev-v',AF,['Since 7 Jan 2016 only on the DFC, BSM, Air Medal and ASCOM','No longer on unit awards since 1 Jan 2014'],'A16.16')
addfact('m-dev-c',AF,['Started 7 Jan 2016 and is not retroactive','Not authorized on the Bronze Star Medal'],'A16.8')
addfact('m-dev-r',AF,['Started 7 Jan 2016 and is not retroactive; for remotely piloted aircraft, cyber, space and ISR career fields','Only on decorations for specific meritorious achievement, not end-of-tour awards'],'A16.14')
addfact('m-dev-olc',AF,['Three sizes and two colors; bronze for the 2nd to 5th award, silver for the 6th or instead of five bronze'],'A16.13')
addfact('m-dev-star',AF,['Also called a campaign star; also shows both rifle and handgun Expert on the Small Arms Expert Marksmanship Ribbon'],'A16.15')
addfact('m-dev-arrowhead',AF,['Bronze, 1/4 inch high and 1/8 inch wide; worn point up, to the wearer\'s right of all service stars; only one per ribbon'],'A16.5')
addfact('m-dev-berlin',['Air Force'],['For 90 or more consecutive days between 26 Jun 1948 and 30 Sep 1949 in a unit named for the Berlin Airlift; worn with the aircraft nose up at 30 degrees toward the wearer\'s right shoulder'],'A16.6')
addfact('m-dev-m',AF,['Bronze M for Reserve mobilization on or after 1 Aug 1990, worn on the Armed Forces Reserve Medal'],'A16.10')
addfact('m-dev-hourglass',AF,['5/16 inch hourglass with a Roman numeral X; bronze, silver and gold for each 10 years'],'A16.9')
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False); print('ok',len(es))

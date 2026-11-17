"""CMB, EFMB, Master CIB/CMB from AR 600-8-22 (30 Jul 2025). Idempotent."""
import json, copy
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
SRC='AR 600-8-22, Military Awards, 30 Jul 2025 (effective 30 Aug 2025), para %s (text read from a copy hosted at armywriter.com; the 19 Jan 2024 edition numbered the CMB 8-7 and the EFMB 8-10)'
old=lambda s:s.startswith('AR 600-8-22')
e=by['b-cmb']
e['summary']='Awarded to Army, Navy and Air Force medical personnel assigned or attached to an infantry unit while it is in actual ground combat; later widened to other ground combat units.'
e['facts']=['Originally the Medical Badge; created by the War Department, 1 Mar 1945; may be awarded retroactive to 7 Dec 1941 (para 8-10a)',
 'Medical personnel of the AMEDD, Naval Medical Department and USAF Medical Service may qualify (para 8-10b)',
 'Battle participation credit alone is not enough; the infantry unit must have been in contact with the enemy (para 8-10b)',
 'Not awarded to general or flag officers (para 8-10b)',
 'Widened to Special Forces medical sergeants from 19 Dec 1989, armor and cavalry units from 16 Jan 1991, and combat arms and combat aviation units from 11 Sep 2001 (para 8-10c)',
 'Soldiers with MOS 18D are no longer eligible from 3 Jun 2005 (para 8-10c)',
 'Second and third awards are shown by one and two stars centered at the top of the badge, between the points of the oak wreath (para 8-10d)',
 'No second award for the same qualifying period in table 8-2 (para 8-10e)',
 'Badge group 1 for order of wear (DA Pam 670-1, para 22-16a)']
e['sources']=[SRC%'8-10']+[s for s in e['sources'] if not old(s) and 'armywriter' not in s]
e['attachments']=[a for a in e['attachments'] if a.get('link')!='b-mcmb']+[{'name':'Master Combat Medical Badge','note':'Added 2024: CMB plus an expert badge (para 8-7).','variants':[],'link':'b-mcmb'}]
f=by['b-efmb']
f['facts']=[x for x in f['facts'] if not x.startswith(('Open to','Officers must','Commanders of'))]
f['facts']=['Officers must be assigned or detailed to an AMEDD corps (para 8-13a)','Enlisted Soldiers need a primary MOS in the medical career management field (para 8-13a)',
 'Commanders of grade LTC/O-5 or above conduct the test and award the badge (para 8-13b)']+[x for x in f['facts'] if x.startswith('Badge group')]
f['facts']+=['UNVERIFIED, from a screenshot an Army friend sent, not in the regulation: established 1965; same stretcher and caduceus as the CMB but no wreath']
f['sources']=[SRC%'8-13']+[s for s in f['sources'] if not old(s) and 'armywriter' not in s]
def mk(id_,name,date,summary,facts,para,base):
    n=by.get(id_) or copy.deepcopy(by[base])
    n.update(id=id_,name=name,group='Special skill badges',summary=summary,facts=facts,sources=[SRC%para],attachments=[],variants=[],remember=None,image=None,swatches=[],eras=['modern'],yearFrom=2024,yearTo=None,proof='official')
    if id_ not in by: es.append(n); by[id_]=n
mk('b-mcmb','Master Combat Medical Badge (MCMB)',None,'Combat Medical Badge holders who also hold an expert badge.',
 ['Established by the Department of the Army, 9 Oct 2024; retroactive to 11 Nov 1943','Open to AMEDD officers, warrant officers and enlisted Servicemembers','Needs the Combat Medical Badge plus the Expert Field Medical Badge, Expert Infantryman Badge or Expert Soldier Badge','Commanders of LTC/O-5 or above certify eligibility, with the original CMB orders and the expert badge orders','The text read does not describe the badge design or repeat awards'],'8-7','b-cmb')
mk('b-mcib','Master Combat Infantryman Badge (MCIB)',None,'Combat Infantryman Badge holders who also hold an expert badge.',
 ['Retroactive to 11 Nov 1943','Needs the Combat Infantryman Badge plus the Expert Infantryman Badge, Expert Field Medical Badge or Expert Soldier Badge','Commanders of LTC/O-5 or above certify eligibility','The text read does not describe the badge design or repeat awards'],'8-6','b-cib')
by['b-mcib']['facts'].insert(0,'Establishment date not read from the text')
by['b-mcmb']['yearFrom']=2024; by['b-mcib']['yearFrom']=1943; by['b-mcib']['eras']=['ww2','korea','vietnam','coldwar','gulf','modern']
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False); print('ok',len(es))

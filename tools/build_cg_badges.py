import json
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
M='COMDTINST M1020.6K, Coast Guard Uniform Manual (7 Jul 2020)'
INS=[
('aviator','Aviator','A gold-toned, winged insignia with a fouled anchor behind a shield in the center.'),
('aircrew','Air Crew','A gold-toned, winged insignia with an anchor and the letters "AC" inscribed. Enlisted members qualified for aircrew duties who advance to officer status may continue to wear it.'),
('flightofficer','Flight Officer','A gold-toned, winged insignia behind a shield in the center.'),
('flightsurgeon','Flight Surgeon','A gold-toned, winged insignia with a silver caduceus superimposed on a shield in the center.'),
('rescueswimmer','Aviation Rescue Swimmer','A gold-toned, winged insignia with the "Star of Life" and crossed scuba diver fins. Once qualified the member wears it in lieu of the aircrew insignia.'),
('astronaut','Astronaut','A gold-toned, winged insignia with crossed anchors overlaid with a shield and shooting star.'),
('aviationms','Aviation Mission Specialist','A gold-toned, winged insignia with a silver anchor on a gold background encircled in a silver ring.'),
('cutterman','Cutterman','A gold-toned (officers) or pewter-toned (enlisted) insignia with a shield on a five-pointed star superimposed on a ship\'s wheel centered over stylized waves.'),
('boatforce','Boat Force Operations','Pewter-toned insignia with an eight-point compass rose over a crossed boat hook and oar centered over stylized waves. Advanced qualification: the compass rose is polished gold and the waves and oars are pewter.'),
('coxswain','Coxswain','A pewter-toned insignia with curled stylized waves and crossed oars with a compass rose superimposed.'),
('eews','Enlisted Expeditionary Warfare Specialist','A polished silver insignia of a bow of a patrol craft on a crossed rifle and sword against a background of ocean swells.'),
('surfman','Surfman','A pewter-toned insignia of a life buoy crossed with two boat oars. A more advanced qualification, always worn in lieu of the Coxswain insignia.'),
('scuba','Scuba Diver','A gold-toned (officers) or pewter-toned (enlisted) insignia with a wet suit hood, facemask and breathing apparatus.'),
('diver2','Second Class Diver','A pewter-toned insignia with a diving helmet and breastplate.'),
('diver1','First Class Diver','A pewter-toned insignia with a diving helmet and breastplate surrounded by sea serpents.'),
('masterdiver','Master Diver','A pewter insignia with the same design as the Diving Officer insignia.'),
('divingofficer','Diving Officer','A matte gold-toned insignia with two upright sea horses facing a diving helmet and two tridents projecting upward from the helmet. A double carrick bend is superimposed on the breastplate.'),
('dmt','Diving Medical Technician','A pewter-toned insignia with two upright sea horses facing a diving helmet and two tridents projecting upward from the helmet. A caduceus is superimposed on the breastplate.'),
('portsec','Port Security','A gold-toned (officers) or pewter-toned (enlisted) insignia with two seahorses facing outward from a Coast Guard shield on two crossed swords and a trident on a background of stylized waves.'),
('marinesafety','Marine Safety','A pebble-finished rectangle with a polished gold horizontal trident and a centered compass rose, entwined by a line. A polished silver shield is centered on the compass rose.'),
('tactleo','Law Enforcement Detachment and Tactical Law Enforcement Team','A polished gold insignia with a ribbon on the top edge. A compass rose and a silver shield are centered between two crossed swords. Across the bottom it reads "TACTICAL LAW ENFORCEMENT."'),
('honorguard','Coast Guard Ceremonial Honor Guard','A gold-toned metal oval insignia, authorized for past and present members assigned to the Ceremonial Honor Guard.'),
('companycmdr','Company Commander','A gold-toned oval with the Coast Guard shield and two crossed swords on a background of stylized waves, placed between the words "Company Commander".'),
('paNP','Physician Assistant and Nurse Practitioner','A one-inch gold shield with a silver caduceus centered on the shield. There is no miniature version.'),
]
DEV=[
('cmdafloat','Command Afloat device','A gold and silver device with a miniature officer eagle superimposed on a partially unfurled commission pennant.'),
('cmdashore','Command Ashore device','A gold and silver device with a miniature officer eagle superimposed on a wreath of gold oak leaves.'),
('oicafloat','Officer in Charge Afloat device','A pewter-toned device with a Coast Guard shield and anchor superimposed on a rope grommet.'),
('oicashore','Officer in Charge Ashore device','A pewter-toned device with a wreath of oak leaves open at the top with a Coast Guard shield in its center.'),
]
def mk(i,name,desc,para,kind,extra):
    f=[f'Description: {desc} ({para})']+extra
    return {'id':i,'tab':'badges','group':'Qualification insignia','name':name+(' insignia' if kind=='ins' and not name.endswith('insignia') else ''),
      'branches':['Coast Guard'],'eras':['modern'],'yearFrom':None,'yearTo':None,'summary':f'Coast Guard {kind=="ins" and "qualification insignia" or "command device"}: '+desc.split('. ')[0].rstrip('.')+'.',
      'facts':f,'remember':name,'swatches':[],'variants':[],'attachments':[],'proof':'official','sources':[f'{M}, para {para}'],'image':None}
new=[]
INSF=['Full-size insignia on all uniforms except miniature on Dinner Dress and formal uniforms; up to two insignia may be worn with ribbons or medals (para 4.B.1)',
      'Qualification standards and awarding authority: COMDTINST M1200.1 (series), per para 4.B.1.a']
DEVF=['Devices denote command afloat and ashore experience; the afloat and ashore devices are equivalent (para 4.B.2)','Full-size on full dress, miniature on other uniforms (para 4.B.2)']
for s,n,ds in INS: new.append(mk('b-cg-'+s,n,ds,'4.B.1.a','ins',INSF))
for s,n,ds in DEV: new.append(mk('b-cg-'+s,n,ds,'4.B.2','dev',DEVF))
for e in new:
    if e['id'] in by:
        old=by[e['id']]; e['image']=old.get('image'); es[es.index(old)]=e
    else: es.append(e)
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False)
print(len(new),'CG badge entries')

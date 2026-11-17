import json
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries'] if isinstance(d,dict) else d
by={e['id']:e for e in es}
M='COMDTINST M1020.6K, Coast Guard Uniform Manual (7 Jul 2020)'
S=lambda para:f'{M}, para {para}'
UNV='UNVERIFIED, not stated in the manual text (shown only in its figures): '
def setx(i,summary,facts,srcs,proof,remember=None):
    e=by[i]; e['summary']=summary; e['facts']=facts; e['sources']=srcs; e['proof']=proof
    if remember: e['remember']=remember
# enlisted E-1..E-3 (4.A.7)
for i,n,s,grade in [('cg-sr',1,'one','E-1'),('cg-sa',2,'two','E-2'),('cg-sn',3,'three','E-3')]:
    setx(i,f'Coast Guard {grade}. {n} short diagonal stripe{"s" if n>1 else ""} on a blue background (non-rate mark).',
      [f'Grade: {grade}',f'Non-rate mark: {n} short diagonal stripe{"s" if n>1 else ""} sewn on a blue background (para 4.A.7)',
       'Stripe color shows the group: white = seaman, red = fireman, green = airman (para 4.A.7)',
       'Worn on the outer left sleeve of the blue service dress coat, midway between shoulder and elbow and between front and back crease (para 4.A.7)',
       'Pay grades E-2 and E-3 also wear a rating designator above the mark (para 4.A.7)'],[S('4.A.7')],'official',f'{n} stripe{"s" if n>1 else ""}')
# petty officers E-4..E-6 (4.A.5, 4.A.8)
for i,n,w,grade in [('cg-po3',1,'third','E-4'),('cg-po2',2,'second','E-5'),('cg-po1',3,'first','E-6')]:
    setx(i,f'Coast Guard {grade}. Collar: {n} gold chevron{"s" if n>1 else ""} under a silver shield. Sleeve: perched eagle with {n} scarlet chevron{"s" if n>1 else ""}.',
      [f'Grade: {grade}',f'Collar insignia: {n} metal gold chevron{"s" if n>1 else ""} for {w} class, mounted under a silver Coast Guard shield (para 4.A.5)',
       'Rating badge: perched eagle, wings extended upward, head to the eagle\'s right; chevrons show the pay grade (para 4.A.8)',
       'Chevron color on the badge for E-4 to E-6 is scarlet, background the same color as the jacket; on the Dinner Dress White Jacket the stripes are navy blue on white (para 4.A.8)',
       'A rating emblem sits between the eagle and the chevrons (para 4.A.8)'],[S('4.A.5'),S('4.A.8')],'official',f'{n} chevron{"s" if n>1 else ""} under the eagle')
# chiefs
setx('cg-cpo','Coast Guard E-7. Collar: gold fouled anchor with a silver shield. Sleeve: perched eagle with gold chevrons.',
  ['Grade: E-7','Collar insignia: 15/16-inch gold metal fouled anchor with a silver shield superimposed on the shank (para 4.A.5)',
   'Rating badge: perched eagle with chevrons; E-7 to E-9 chevrons are gold on a background the same color as the jacket (para 4.A.8)',
   UNV+'exact number of chevrons and rocker on the E-7 badge'],[S('4.A.5'),S('4.A.8')],'official','Gold anchor, silver shield')
for i,k,g,st in [('cg-scpo','SCPO','E-8','one'),('cg-mcpo','MCPO','E-9','two')]:
    setx(i,f'Coast Guard {g}. Collar: gold fouled anchor with a silver shield and {st} star{"s" if st=="two" else ""} on the stock.',
      [f'Grade: {g}','Collar insignia: gold fouled anchor with a silver shield on the shank; stars are attached to the stock to show senior and master chiefs (para 4.A.5)',
       f'This grade wears {st} star{"s" if st=="two" else ""} on the stock (para 4.A.5)','Rating badge chevrons are gold (para 4.A.8)',
       UNV+'exact chevron and rocker count on the sleeve badge'],[S('4.A.5'),S('4.A.8')],'official',f'{st.capitalize()} star{"s" if st=="two" else ""} on the anchor')
setx('cg-mcpocg','Coast Guard E-9. Collar: gold fouled anchor, silver shield, three stars. Gold badge with a gold shield and gold stars.',
  ['Grade: E-9, Master Chief Petty Officer of the Coast Guard','Collar insignia: gold fouled anchor with a silver shield and three stars on the stock (para 4.A.5)',
   'Rating badge: a gold shield with gold stars replaces the rating emblem; chevrons are gold (para 4.A.8)'],[S('4.A.5'),S('4.A.8')],'official','Three stars on the anchor')
setx('cg-cmc','Coast Guard E-9. Command Master Chief badge: shield with stars (silver badge; gold at Area level).',
  ['Grade: E-9','Command Master Chiefs wear a silver shield with silver stars as the rating badge; MCPOCG and Area-level Gold Badge CMCs, including the CGRF-MC, wear a gold shield with gold stars (para 4.A.8)',
   UNV+'star count and collar insignia for the CMC'],[S('4.A.8')],'unverified','Silver shield, silver stars')
# officers
common=['Sleeve stripes: O-1 to O-6 use 1/2-inch and 1/4-inch gold stripes; O-7 to O-10 use 2-inch and 1/2-inch gold stripes (para 4.A.1)',
        'Gold shield 1/4 inch above the top stripe on the sleeve; not used on dinner dress white jacket, dinner dress white, full dress white or service dress white (para 4.A.1)',
        'Shoulder boards, sleeve stripes and collar insignia all show officer grade (para 4.A.1)']
for i,leaf,txt in [('co-maj','gold','A gold oak leaf; the stem faces outboard (para 4.A.1 note).'),('co-ltc','silver','A silver oak leaf; the stem faces outboard (para 4.A.1 note).')]:
    g='O-4' if i=='co-maj' else 'O-5'
    setx(i,f'Coast Guard {g}. Collar: {leaf} oak leaf, stem outboard.',[f'Grade: {g}','Collar insignia: '+txt]+common,[S('4.A.1'),S('4.A.3')],'official',f'{leaf.capitalize()} oak leaf')
for i,g,txt in [('co-2lt','O-1','Collar bar'),('co-1lt','O-2','Collar bar'),('co-cpt','O-3','Collar bars')]:
    e=by[i]; e['facts']=[f for f in e['facts'] if 'Unverified: no official' not in f]+[UNV+'color and number of collar bars (the manual shows them only as pictures)']+common
    e['sources']=[S('4.A.1')]+[s for s in e['sources'] if 'Picture' in s]
setx('co-col','Coast Guard O-6. Collar: silver eagle, always facing forward.',['Grade: O-6','Collar insignia: an eagle; always faces forward, or to the wearer\'s right where there is no fore/aft (para 4.A.1 note)',UNV+'eagle color']+common,[S('4.A.1')]+[s for s in by['co-col']['sources'] if 'Picture' in s],'unverified','Eagle, faces forward')
for i,g in [('co-bg','O-7'),('co-mg','O-8'),('co-lg','O-9'),('co-gen','O-10')]:
    e=by[i]; e['facts']=[f for f in e['facts'] if 'Unverified: no official' not in f]+['Flag officer collar stars are metal, 9/16 inch circumference, attached point to point (para 4.A.1)','Flag officer shoulder boards: 1 1/2-inch gold lace on blue, with a silver fouled anchor and silver shield (para 4.A.1)',UNV+'number of stars (figure only)']+common
    e['sources']=[S('4.A.1')]+[s for s in e['sources'] if 'Picture' in s]
# warrants
for i,g,col in [('cw-w2','W-2','gold'),('cw-w3','W-3','silver'),('cw-w4','W-4','silver')]:
    setx(i,f'Coast Guard {g}. 1/2-inch gold sleeve stripe with blue breaks showing the grade.',
      [f'Grade: {g}','Sleeve stripe: 1/2-inch gold with blue breaks showing the grade (para 4.A.1)','Right collar shows the grade; the specialty insignia is on the left collar (para 4.A.1)','Specialty insignia is not worn on the sleeve of the Dinner Dress Blue Jacket or Formal Dress (para 4.A.1)',
       UNV+'collar and shoulder board insignia color and number of breaks per grade'],[S('4.A.1'),S('4.A.2')],'unverified','Gold stripe, blue breaks')
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False)

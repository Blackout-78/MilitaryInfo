import json
P='app/src/main/assets/data/entries.json'
d=json.load(open(P)); es=d['entries']; by={e['id']:e for e in es}
DOC='MCO 1020.34H, Marine Corps Uniform Regulations (1 May 2018)'
L=[
('psb','Presidential Service Badge (PSB)','4007.2a(1)','A blue enameled disc, 1 15/16 inches in diameter, surrounded by 27 gold rays radiating from the center. Superimposed on the disc is a gold-colored device taken from the seal of the President, encircled with 50 stars.',
 'Male Marines wear it centered on the upper right pocket of the blue dress coat, service coat and khaki shirts.'),
('vpsb','Vice-Presidential Service Badge (VPSB)','4007.2a(2)','A white enameled disc, 1 15/16 inches in diameter, surrounded by 27 gold rays radiating from the center. Superimposed on the disc is a gold-colored device taken from the seal of the Vice-President.',
 'Worn according to the same rules as the PSB.'),
('osd','Office of the Secretary of Defense Identification Badge (OSD ID)','4007.2a(3)','An eagle with wings displayed horizontally, grasping three crossed gold arrows, with an enamel shield on its breast (blue upper portion, 13 alternating red and white stripes below); a gold annulet bearing 13 gold stars above the eagle and a green enamel wreath of laurel and olive below; all on a silver sunburst of 33 rays, 2 inches in diameter.',
 'Only personnel assigned to duty in the OSD who received a certificate of eligibility may wear it. On the blue dress coat and service coat it is centered on the upper left pocket; the miniature is 1 1/2 inches in diameter.'),
('jcs','Joint Chiefs of Staff Identification Badge (JCS ID)','4007.2a(4)','The United States shield (blue upper portion, 13 red and white stripes) on four gold unsheathed swords, surrounded by a gold scroll with "JOINT" at the top and "CHIEFS OF STAFF" at the bottom in blue enamel letters, all within an oval silver laurel wreath 2 1/4 inches high by 2 inches wide.',
 'May be permanently awarded to a Marine assigned to the JCS organization who serves at least 365 consecutive days after 14 January 1961 and receives a certificate of eligibility. Worn in the same manner as the OSD ID badge; the miniature is one third smaller with nine stripes on the shield.'),
]
for i,n,p,desc,wear in L:
    e={'id':'b-mc-'+i,'tab':'badges','group':'Identification badges','name':n,'branches':['Marine Corps'],'eras':['modern'],'yearFrom':None,'yearTo':None,
      'summary':f'Marine Corps service and identification badge: {desc.split(". ")[0].rstrip(".")}.',
      'facts':[f'Design: {desc} (para {p})',f'Wear: {wear} (para {p})','No more than two service or identification badges are worn on the same side of the uniform (para 4007.1c)','Command identification badges are not worn with the utility uniforms (para 4007.1c)'],
      'remember':n,'swatches':[],'variants':[],'attachments':[],'proof':'official','sources':[f'{DOC}, para {p}'],'image':None}
    if e['id'] in by: e['image']=by[e['id']].get('image'); es[es.index(by[e['id']])]=e
    else: es.append(e)
json.dump(d,open(P,'w'),indent=1,ensure_ascii=False)

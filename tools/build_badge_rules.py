"""Idempotent: badge wear rules checked against the user-supplied DA PAM 670-1 (26 Jan 2021) PDF."""
import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent; ENT=ROOT/"app/src/main/assets/data/entries.json"
D="DA PAM 670-1, Guide to the Wear and Appearance of Army Uniforms and Insignia, 26 January 2021"
doc=json.load(open(ENT)); E={e["id"]:e for e in doc["entries"]}
def add(i,fact):
    if fact not in E[i]["facts"]: E[i]["facts"].append(fact)
w=E["b-wear-rules"]
for f in ["Army service uniform (ASU): a total of six badges at one time, counting any marksmanship badges but not tab metal replicas (para 22-16b(1))",
 "Up to three badges may be worn above the ribbons, and one badge from group 1 or group 2 counts toward those three (para 22-16b(3)(a))",
 "The driver and mechanic badge is not worn above the ribbons, only on the left pocket flap (para 22-16b(3)(a),(b))",
 "There is no precedence within a group: a Soldier with the parachutist and air assault badges chooses their order (para 22-16b(3)(c))",
 "Badges are worn one above the other, 1/2 inch apart, in group order from top to bottom (para 22-16b(3)(d))",
 "Mirror-finish commercial badges are allowed, but they cannot be mixed with badges that lack that finish (para 22-16b(3)(f))",
 "Tab metal replicas are not worn above the ribbons and are not stacked; they go on the pocket flap (para 22-16b(3)(g))"]: add("b-wear-rules",f)
w["sources"]=[s for s in w["sources"] if "home.army.mil" not in s]+[f"{D}, para 22-16b; checked against the PDF supplied by the user"] if not any("checked against" in s for s in w["sources"]) else w["sources"]
m=E["b-marksmanship"]
add("b-marksmanship","Order of precedence, highest first: distinguished international shooter, distinguished rifleman, distinguished pistol shot, national trophy match, Inter-Service competition, excellence in competition rifleman, excellence in competition pistol shot, then the qualification badges (para 22-15a)")
add("b-marksmanship","Worn on the ASU and AGSU coats and the ASU shirt; a Soldier who fails to qualify under AR 350-1, or is exempt, does not wear them (para 22-15b)")
add("b-marksmanship","Marksmanship badges are worn to the wearer's left of any special skill badges (para 22-15c)")
new=[("b-wear-combat","Badges on the combat uniform","Subdued badges go above the U.S. Army tape on the combat uniform.",
 ["Up to five badges, in group order from top to bottom and from the wearer's right to left. Only one badge from group 1 or group 2 may be worn; up to five from groups 3, 4 and 5, with the total not above five (para 22-16d(2))","Badges may be sew-on or pin-on, but Soldiers may wear them in a deployed or field environment only if sewn on (para 22-16d(1))","One badge: centered 1/8 inch above the U.S. Army tape. Two badges: one vertical column, 1/4 inch between badges (para 22-16d(2)(a),(b))","The driver and mechanic badge is not authorized on utility uniforms (para 22-16d(2))"],"22-16d, pp. 313-314"),
 ("b-wear-mess","Miniature badges on mess and evening mess uniforms","Dress miniature badges and miniature tab replicas are worn above the miniature medals.",
 ["Up to five badges or miniature tab replicas, or a combination; only one badge from group 1 or group 2 (para 22-16c(1))","One or two badges sit centered immediately above the miniature medals; a third goes 1/4 inch above the lower two; five are stacked in the same pattern. Order is by group, top to bottom and right to left (para 22-16c(1))","Dress miniatures may also be worn on the Class B service shirt, but not mixed with full-sized or miniature badges. The CIB and EIB are the only badges made in three sizes: full, miniature and dress miniature (para 22-16c(2))","Miniature badges and miniature metal tab replicas are not authorized on the AGSU (para 22-16c(3))"],"22-16c, pp. 312-313"),
 ("b-pt-badge","Physical fitness badge","Group 6 badge, a cloth badge worn only on the Army physical fitness uniform (APFU).",
 ["Authorized only as a cloth badge and worn only on the APFU (para 22-16g)","On the t-shirt: centered on the upper left front. On the APFU running jacket: sewn centered 1/2 inch above the Army logo (para 22-16g)","Group 6 in the order of group precedence (para 22-16a(6))"],"22-16g and 22-16a(6), pp. 294 and 316")]
for i,n,s,f,p in new:
    if i in E: doc["entries"].remove(E[i])
    doc["entries"].append({"id":i,"tab":"badges","group":"Wear rules","name":n,"branches":["Army"],"eras":["modern"],"summary":s,"facts":f,"variants":[],"swatches":[],"attachments":[],"proof":"official","remember":n+": see summary.","image":"none","sources":[f"{D}, para {p}; read from the PDF supplied by the user"],"yearFrom":2021,"yearTo":None})
json.dump(doc,open(ENT,"w"),indent=2,ensure_ascii=False); print("ok")

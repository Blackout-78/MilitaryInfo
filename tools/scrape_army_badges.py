"""Fetch the Army badges page and every image on it, with alt text and nearby heading. Runs on GitHub Actions."""
import os, re, json, urllib.request, urllib.parse, html
U="https://veteranmedals.army.mil/home/us-army-medals-award-badges-ribbon-and-attachments-information/us-army-badges-information"
H={"User-Agent":"Mozilla/5.0 MilitaryInfo-fetch"}
os.makedirs("cands/army",exist_ok=True)
try:
    page=urllib.request.urlopen(urllib.request.Request(U,headers=H),timeout=60).read().decode("utf8","replace")
except Exception as e:
    open("cands/army/ERROR.txt","w").write(str(e)); raise SystemExit
open("cands/army/page.html","w").write(page)
out=[]
for m in re.finditer(r"<img\b[^>]*>",page,re.I):
    tag=m.group(0); src=re.search(r'src="([^"]+)"',tag); alt=re.search(r'alt="([^"]*)"',tag)
    if not src: continue
    u=urllib.parse.urljoin(U,html.unescape(src.group(1)))
    ctx=re.sub(r"<[^>]+>"," ",page[max(0,m.start()-300):m.start()]); ctx=re.sub(r"\s+"," ",html.unescape(ctx))[-120:]
    out.append({"url":u,"alt":html.unescape(alt.group(1)) if alt else "","ctx":ctx})
for i,o in enumerate(out):
    try:
        d=urllib.request.urlopen(urllib.request.Request(o["url"],headers=H),timeout=40).read()
        ext=os.path.splitext(urllib.parse.urlparse(o["url"]).path)[1] or ".img"
        o["file"]=f"{i:03d}{ext}"; open("cands/army/"+o["file"],"wb").write(d); o["bytes"]=len(d)
    except Exception as e: o["err"]=str(e)
json.dump(out,open("cands/army/images.json","w"),indent=1)
print(len(out),"images")

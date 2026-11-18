import urllib.request, os, json
UA="MilitaryInfo-research/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
os.makedirs("cands",exist_ok=True); out={}
for k,u in {"robots":"https://www.heraldry-wiki.com/robots.txt","copyright":"https://www.heraldry-wiki.com/wiki/Heraldry_of_the_World:Copyrights","about":"https://www.heraldry-wiki.com/wiki/Heraldry_of_the_World:About","sample":"https://www.heraldry-wiki.com/wiki/1st_Infantry_Division_Big_Red_One,_US_Army","api":"https://www.heraldry-wiki.com/api.php?action=query&list=search&srsearch=Shoulder+Sleeve+Insignia+82nd+Airborne&format=json"}.items():
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=40); out[k]=r.read().decode("utf8","replace")[:6000]
    except Exception as e: out[k]="ERR "+str(e)
json.dump(out,open("cands/heraldry_probe.json","w"),indent=1)

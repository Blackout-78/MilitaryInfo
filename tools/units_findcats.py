import json, os, urllib.parse, urllib.request, time
API="https://commons.wikimedia.org/w/api.php"; UA="MilitaryInfo-image-finder/1.0 (https://github.com/Blackout-78/MilitaryInfo)"
Q=["shoulder sleeve insignia United States Army","distinctive unit insignia United States Army","United States Army divisions insignia","United States Space Force insignia","United States Coast Guard insignia","United States Air Force major command emblem","Air Force wing emblems","Marine Corps division insignia","United States Army corps insignia","United States Army brigade insignia","Combat service identification badge Army","Army regimental insignia"]
os.makedirs("cands",exist_ok=True); out={}
for q in Q:
    d=json.load(urllib.request.urlopen(urllib.request.Request(API+"?"+urllib.parse.urlencode({"action":"query","format":"json","list":"search","srsearch":q,"srnamespace":14,"srlimit":15}),headers={"User-Agent":UA}),timeout=40))
    out[q]=[x["title"] for x in d["query"]["search"]]; time.sleep(0.5)
json.dump(out,open("cands/cats.json","w"),indent=1)

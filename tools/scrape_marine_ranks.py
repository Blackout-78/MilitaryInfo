"""Scrape marines.mil/Ranks for the rank list and insignia image URLs, download them. Runs on GitHub Actions."""
import os, re, urllib.request, urllib.parse, json
U = "https://www.marines.mil/Ranks/"
H = {"User-Agent": "Mozilla/5.0 MilitaryInfo-fetch"}
html = urllib.request.urlopen(urllib.request.Request(U, headers=H), timeout=60).read().decode("utf8", "replace")
os.makedirs("out/marines", exist_ok=True); open("out/marines/page.html", "w").write(html)
imgs = re.findall(r'<img[^>]+>', html)
rows = []
for t in imgs:
    s = re.search(r'src="([^"]+)"', t); a = re.search(r'alt="([^"]*)"', t)
    if s: rows.append((urllib.parse.urljoin(U, s.group(1)), a.group(1) if a else ""))
print(len(rows)); [print(r) for r in rows]
json.dump(rows, open("out/marines/imgs.json", "w"), indent=1)
n = 0
for url, alt in rows:
    if re.search(r"rank|insignia|enlisted|officer|warrant|chevron|sergeant|general|lieut|private|corporal|captain|major|colonel", url + alt, re.I) and not url.endswith(".svg") or "rank" in url.lower():
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40).read()
            open(f"out/marines/{n:02d}_{os.path.basename(urllib.parse.urlparse(url).path)}", "wb").write(data); n += 1
        except Exception as e: print("FAIL", url, e)
print("downloaded", n)

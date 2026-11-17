import urllib.request, urllib.error
for u in ["https://www.af.mil/About-Us/The-Book/Enlisted-Ranks/?igtag=Rank+Insignia", "https://www.af.mil/About-Us/The-Book/Enlisted-Ranks/"]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "MilitaryInfo-fetch/1.0 (https://github.com/Blackout-78/MilitaryInfo)"}), timeout=40)
        h = r.read().decode("utf8", "replace"); print("OK", u, len(h))
        open("probe.html", "w").write(h); break
    except urllib.error.HTTPError as e: print("HTTP", e.code, u)
    except Exception as e: print("ERR", u, e)

#!/usr/bin/env python3
"""Check app/src/main/assets/data/entries.json against the schema.

Usage:
  python3 tools/validate_data.py            report problems, show proof counts
  python3 tools/validate_data.py --release  also fail if any entry is Unverified
"""
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "app/src/main/assets/data/entries.json"
IMAGES = DATA.parent.parent / "images"

TABS = {"uniforms", "medals", "badges", "ranks", "patches"}
BRANCHES = {"Army", "Navy", "Marine Corps", "Air Force", "Coast Guard", "Space Force"}
ERAS = {"ww1", "interwar", "ww2", "korea", "vietnam", "coldwar", "gulf", "modern"}
PROOFS = {"official", "historical", "unverified"}
FINISHES = {"polished", "subdued"}
GENDERS = {"male", "female", "any"}
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def main() -> int:
    release = "--release" in sys.argv
    problems: list[str] = []

    def bad(where: str, msg: str) -> None:
        problems.append(f"{where}: {msg}")

    def check_swatches(where: str, swatches) -> None:
        for s in swatches or []:
            for k in ("role", "name", "hex"):
                if k not in s:
                    bad(where, f"swatch missing {k}")
            if "hex" in s and not HEX.match(s["hex"]):
                bad(where, f"bad hex {s['hex']!r}")

    def check_variants(where: str, variants) -> None:
        for v in variants or []:
            if "label" not in v:
                bad(where, "variant missing label")
            if v.get("finish") and v["finish"] not in FINISHES:
                bad(where, f"unknown finish {v['finish']!r}")
            if v.get("gender") and v["gender"] not in GENDERS:
                bad(where, f"unknown gender {v['gender']!r}")
            if v.get("era") and v["era"] not in ERAS:
                bad(where, f"unknown era {v['era']!r}")
            if v.get("image") and v["image"] != "none" and not (IMAGES / v["image"]).exists():
                bad(where, f"image file missing: {v['image']}")
            check_swatches(where, v.get("swatches"))

    try:
        doc = json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Cannot read data file: {e}")
        return 1

    entries = doc.get("entries", [])
    ids = set()
    counts = {p: 0 for p in PROOFS}
    required = ("id", "tab", "group", "name", "branches", "eras", "summary", "proof")

    for e in entries:
        where = e.get("id", "<no id>")
        for k in required:
            if k not in e:
                bad(where, f"missing {k}")
        if where in ids:
            bad(where, "duplicate id")
        ids.add(where)
        if e.get("tab") not in TABS:
            bad(where, f"unknown tab {e.get('tab')!r}")
        for b in e.get("branches", []):
            if b not in BRANCHES:
                bad(where, f"unknown branch {b!r}")
        if not e.get("branches"):
            bad(where, "needs at least one branch")
        for era in e.get("eras", []):
            if era not in ERAS:
                bad(where, f"unknown era {era!r}")
        if not e.get("eras") and e.get("yearFrom") is not None:
            bad(where, "has years but no era")
        proof = e.get("proof")
        if proof not in PROOFS:
            bad(where, f"unknown proof {proof!r}")
        else:
            counts[proof] += 1
            if proof != "unverified" and not e.get("sources"):
                bad(where, "Official or Historical entries need at least one source")
        yf, yt = e.get("yearFrom"), e.get("yearTo")
        if yf is not None and yt is not None and yf > yt:
            bad(where, "yearFrom is after yearTo")
        if e.get("image") and e["image"] != "none" and not (IMAGES / e["image"]).exists():
            bad(where, f"image file missing: {e['image']}")
        check_swatches(where, e.get("swatches"))
        check_variants(where, e.get("variants"))
        for a in e.get("attachments", []):
            if "name" not in a:
                bad(where, "attachment missing name")
            check_variants(f"{where}/{a.get('name', '?')}", a.get("variants"))

    print(f"{len(entries)} entries: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    if release and counts["unverified"]:
        bad("release", f"{counts['unverified']} unverified entries must be verified or removed first")

    if problems:
        print("\nProblems:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("Data OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

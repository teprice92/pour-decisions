# Builds catalog/<console>.json title lists from No-Intro/Redump DATs and titledb.
import re, json, sys, os
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
SKIP = re.compile(r"\((?:[^)]*\b(?:Beta|Proto|Prototype|Demo|Sample|Kiosk|Debug|Program|Pirate|Aftermarket|Unl|Hack|BIOS|Test|Preview|Promo|Trial|Taikenban|Tech Demo|Competition|Not for Resale|Review|Alt|Enhancement)\b[^)]*)\)", re.I)
BAD = re.compile(r"^\[BIOS\]|\bBIOS\b|Utility|Utilities|Test Cartridge|Diagnostic|Firmware|System Update|Network Adapter|Memory Card|Demo Disc|Demo Disk|Kiosk|Jampack|Interactive Demo|Bonus Disc|Preview Disc|Sampler|Trailer|Theme\b", re.I)
def clean(name):
    t = re.sub(r"\s*[\(\[][^\)\]]*[\)\]]", "", name).strip()
    t = re.sub(r"\s+", " ", t)
    parts = t.split(" - ", 1)
    m = re.match(r"^(.*), (The|A|An)$", parts[0])
    if m: parts[0] = f"{m.group(2)} {m.group(1)}"
    t = ": ".join(parts) if len(parts) == 2 else parts[0]
    t = re.sub(r"^(.*), (The|A|An)(:|$)", lambda m: f"{m.group(2)} {m.group(1)}{m.group(3)}", t)
    return t.strip(" -:")
def key(t): return re.sub(r"[^a-z0-9]", "", t.lower().replace("&", "and"))
def from_dat(path):
    names = []
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r'^\tname "(.*)"\s*$', line)
        if m: names.append(m.group(1))
    titles = {}
    for n in names:
        if SKIP.search(n) or BAD.search(n): continue
        t = clean(n)
        if len(t) < 2: continue
        titles.setdefault(key(t), t)
    return sorted(titles.values(), key=lambda x: x.lower())
def from_titledb(path):
    d = json.load(open(path, encoding="utf-8"))
    titles = {}
    for e in d.values():
        tid, name = (e.get("id") or ""), (e.get("name") or "").strip()
        if not name or not tid.upper().endswith("000") or e.get("isDemo"): continue
        if re.search(r"\b(demo|trial|体験版)\b", name, re.I): continue
        name = re.sub(r"\s+", " ", name.replace("™", "").replace("®", "")).strip()
        titles.setdefault(key(name), name)
    return sorted(titles.values(), key=lambda x: x.lower())
files = {"atari": "atari.dat", "nes": "nes.dat", "snes": "snes.dat", "n64": "n64.dat", "gc": "gc.dat", "wii": "wii.dat", "wiiu": "wiiu.dat",
         "gb": "gb.dat", "gbc": "gbc.dat", "gba": "gba.dat", "nds": "nds.dat", "genesis": "genesis.dat", "dreamcast": "dreamcast.dat",
         "ps1": "ps1.dat", "ps2": "ps2.dat", "ps3": "ps3.dat", "xbox": "xbox.dat", "x360": "x360.dat"}
total = 0
for cid, f in files.items():
    g = from_dat(os.path.join(src, f)); total += len(g)
    json.dump(g, open(os.path.join(out, cid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(cid, len(g), os.path.getsize(os.path.join(out, cid + ".json")))
g = from_titledb(os.path.join(src, "switch.json")); total += len(g)
json.dump(g, open(os.path.join(out, "switch.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("switch", len(g), os.path.getsize(os.path.join(out, "switch.json")))
print("total", total)

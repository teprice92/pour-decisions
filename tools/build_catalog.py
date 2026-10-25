# Builds catalog/<console>.json from No-Intro/Redump DATs, libretro maxusers DATs, and titledb.
# Each entry is [title, released_in_us (1/0), max_players (0 = unknown)].
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
US = re.compile(r"\((?:[^)]*\b(?:USA|World)\b[^)]*)\)")
def max_users(path):
    users = {}
    if not path or not os.path.exists(path): return users
    cur = None
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r'^\tcomment "(.*)"\s*$', line)
        if m: cur = key(clean(m.group(1))); continue
        m = re.match(r'^\tusers (\d+)', line)
        if m and cur: users[cur] = max(users.get(cur, 0), int(m.group(1)))
    return users
def from_dat(path, users_path=None):
    names = []
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r'^\tname "(.*)"\s*$', line)
        if m: names.append(m.group(1))
    users = max_users(users_path)
    titles = {}
    for n in names:
        if SKIP.search(n) or BAD.search(n): continue
        t = clean(n)
        if len(t) < 2: continue
        k = key(t)
        e = titles.setdefault(k, [t, 0, users.get(k, 0)])
        if US.search(n): e[1] = 1
    return sorted(titles.values(), key=lambda x: x[0].lower())
# Switch 2 games: exclusives have title IDs starting 04; "Nintendo Switch 2 Edition" releases are enhanced versions.
S2_EDITION = re.compile(r"\s*[-–—:]?\s*Nintendo Switch 2 Edition\b.*$", re.I)
# well-known Switch 2 releases the eShop dump doesn't have yet
S2_EXTRA = [["Kirby Air Riders", 1, 4], ["Drag x Drive", 1, 2], ["Hyrule Warriors: Age of Imprisonment", 1, 2], ["Mario Tennis Fever", 1, 4],
            ["Split Fiction", 1, 2], ["Kirby and the Forgotten Land + Star-Crossed World", 1, 2],
            ["Pokémon Pokopia", 1, 0], ["Final Fantasy VII Remake Intergrade", 1, 1], ["Resident Evil Requiem", 1, 1],
            ["Hades II", 1, 1], ["Persona 3 Reload", 1, 1], ["EA Sports FC 26", 1, 4], ["NBA 2K26", 1, 4],
            ["Star Wars Outlaws", 1, 1], ["Assassin's Creed Shadows", 1, 1], ["Fast Fusion", 1, 4]]
def from_titledb(path):
    d = json.load(open(path, encoding="utf-8"))
    s1, s2 = {}, {}
    for e in d.values():
        tid, name = (e.get("id") or "").upper(), (e.get("name") or "").strip()
        if not name or not tid.endswith("000") or e.get("isDemo"): continue
        if re.search(r"\b(demo|trial|体験版|upgrade pack|friend's pass)\b", name, re.I): continue
        name = re.sub(r"\s+", " ", name.replace("™", "").replace("®", "")).strip()
        is_s2 = tid.startswith("04") or bool(S2_EDITION.search(name))
        name = S2_EDITION.sub("", name).strip(" -–—:")
        # the US eShop list, so every title is a US release
        (s2 if is_s2 else s1).setdefault(key(name), [name, 1, int(e.get("numberOfPlayers") or 0)])
    for t, us, pl in S2_EXTRA: s2.setdefault(key(t), [t, us, pl])
    srt = lambda m: sorted(m.values(), key=lambda x: x[0].lower())
    return srt(s1), srt(s2)
files = {"atari": "atari.dat", "nes": "nes.dat", "snes": "snes.dat", "n64": "n64.dat", "gc": "gc.dat", "wii": "wii.dat", "wiiu": "wiiu.dat",
         "gb": "gb.dat", "gbc": "gbc.dat", "gba": "gba.dat", "nds": "nds.dat", "genesis": "genesis.dat", "dreamcast": "dreamcast.dat",
         "ps1": "ps1.dat", "ps2": "ps2.dat", "ps3": "ps3.dat", "xbox": "xbox.dat", "x360": "x360.dat"}
users_files = {"atari": "Atari - 2600", "nes": "Nintendo - Nintendo Entertainment System", "snes": "Nintendo - Super Nintendo Entertainment System",
               "n64": "Nintendo - Nintendo 64", "gb": "Nintendo - Game Boy", "gbc": "Nintendo - Game Boy Color", "gba": "Nintendo - Game Boy Advance",
               "genesis": "Sega - Mega Drive - Genesis"}
total = 0
for cid, f in files.items():
    up = os.path.join(src, "maxusers", users_files[cid] + ".dat") if cid in users_files else None
    g = from_dat(os.path.join(src, f), up); total += len(g)
    json.dump(g, open(os.path.join(out, cid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(cid, len(g), "us", sum(x[1] for x in g), "players", sum(1 for x in g if x[2]), os.path.getsize(os.path.join(out, cid + ".json")))
for cid, g in zip(("switch", "switch2"), from_titledb(os.path.join(src, "switch.json"))):
    total += len(g)
    json.dump(g, open(os.path.join(out, cid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(cid, len(g), "players", sum(1 for x in g if x[2]), os.path.getsize(os.path.join(out, cid + ".json")))
print("total", total)

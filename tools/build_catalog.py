# Builds catalog/<console>.json from No-Intro/Redump DATs, libretro maxusers DATs, titledb, and PS Store title lists.
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
def key(t):
    import unicodedata
    t = "".join(ch for ch in unicodedata.normalize("NFD", t) if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", t.lower().replace("&", "and"))
# --- cleanup: things that aren't games, and tidier names ---
JUNK = re.compile(r"\b(?:Action Replay|GameShark|Game Shark|Xploder|Max Drive|Code ?Breaker (?:Vol|for|Cheat)|Cheats?\b(?! (?:Ahoy|Inc))|Code Archive|Ultimate Codes|Red Hot Codes|"
                  r"IDU|FW Update|Firmware|Test Suite|240p|Media Launcher|Instant Video|Amazon Video|Netflix|Hulu|YouTube|Crunchyroll|Bandai Channel|Nintendo TVii|"
                  r"Magazine|Dorimaga|Demo|Demos|Taikenban|Movie Disc|Movie Collection|New Lineup|Sampler|Kiosk|Preview|Hors-serie|Experience Volume|"
                  r"Best of PlayStation Network|All About PlayStation|PlayStation Underground|Welcome Pack|Add-On|Map Pack|Track Pack|Song Pack|DLC|Season Pass|"
                  r"Bonus Disc|Interactive CD|Jampack|Trial Version|Install Disc|Calibration|Rental|Beta Version|Closed Beta|Open Beta|Beta Test)\b|\bBeta$", re.I)
ACRONYM = re.compile(r"^(?:[IVX]+|FIFA|NBA|NFL|NHL|MLB|NASCAR|UEFA|WWE|WWF|ESPN|SSX|BMX|MDK|TMNT|UFC|PGA|NCAA|AFL|XXX|HD|DX|EX|VR|RPG|DLC|TV|USA|UK|XL|GT|GTA|DS|GB|GBA|NES|SNES|SD|LEGO|NEOGEO|ACA|SNK|KOF|EA|AI|OK|DJ|MX|ATV|TT|F1|R-TYPE|R-Type)$")
SMALL = {"the", "of", "and", "a", "an", "in", "on", "to", "for", "at", "by", "or", "vs", "vs."}
def tidy_caps(t):
    words = t.split(" ")
    shouty = [w for w in words if re.fullmatch(r"[^a-z]*[A-Z]{4,}[^a-z]*", w) and not ACRONYM.match(re.sub(r"[^A-Za-z0-9-]", "", w))]
    if not (t == t.upper() and re.search(r"[A-Z]{4,}", t)) and len(shouty) < 2: return t
    out = []
    for i, w in enumerate(words):
        core = re.sub(r"[^A-Za-z0-9-]", "", w)
        if not re.search(r"[A-Z]", w) or re.search(r"[a-z]", w) or ACRONYM.match(core) or re.search(r"\d", core) or len(core) <= 2:
            out.append(w); continue
        low = w.lower()
        out.append(low if i and low.strip(":,!?") in SMALL else re.sub(r"[a-z]", lambda m: m.group(0).upper(), low, count=1))
    return " ".join(out)
def polish(t, dat):
    if dat and " ~ " in t: t = t.split(" ~ ")[0]   # No-Intro joins alternate titles with ~; keep the main one
    return tidy_caps(t).strip()
US = re.compile(r"\((?:[^)]*\b(?:USA|World)\b[^)]*)\)")
def max_users(path):
    users = {}
    if not path or not os.path.exists(path): return users
    cur = None
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r'^\tcomment "(.*)"\s*$', line)
        if m: cur = key(polish(clean(m.group(1)), True)); continue
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
        if SKIP.search(n) or BAD.search(n) or JUNK.search(n): continue
        t = polish(clean(n), True)
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
            ["Star Wars Outlaws", 1, 1], ["Assassin's Creed Shadows", 1, 1], ["Fast Fusion", 1, 4],
            ["The Legend of Zelda: Breath of the Wild", 1, 1], ["The Legend of Zelda: Tears of the Kingdom", 1, 1],
            ["Metroid Prime 4: Beyond", 1, 1], ["Pokémon Legends: Z-A", 1, 1], ["Animal Crossing: New Horizons", 1, 4],
            ["Hollow Knight: Silksong", 1, 1], ["Tony Hawk's Pro Skater 3 + 4", 1, 2], ["Octopath Traveler 0", 1, 1],
            ["Dragon Quest I & II HD-2D Remake", 1, 1], ["Dragon Quest VII Reimagined", 1, 1], ["Monster Hunter Stories 3: Twisted Reflection", 1, 1],
            ["Final Fantasy Tactics: The Ivalice Chronicles", 1, 1], ["Rune Factory: Guardians of Azuma", 1, 1], ["Survival Kids", 1, 2],
            ["Daemon X Machina: Titanic Scion", 1, 1], ["Resident Evil 7 Biohazard", 1, 1], ["Resident Evil Village", 1, 1],
            ["Civilization VII", 1, 1], ["No Man's Sky", 1, 1], ["Street Fighter 6", 1, 2], ["Cyberpunk 2077: Ultimate Edition", 1, 1],
            ["Hogwarts Legacy", 1, 1], ["Sonic X Shadow Generations", 1, 2], ["Yakuza 0 Director's Cut", 1, 1], ["Deltarune", 1, 1],
            ["Story of Seasons: Grand Bazaar", 1, 1], ["Fantasy Life i: The Girl Who Steals Time", 1, 1], ["Nintendo Switch 2 Welcome Tour", 1, 1],
            ["Donkey Kong Bananza", 1, 2], ["Mario Kart World", 1, 4], ["Super Mario Party Jamboree", 1, 4], ["Puyo Puyo Tetris 2S", 1, 4]]
def from_titledb(path):
    d = json.load(open(path, encoding="utf-8"))
    s1, s2 = {}, {}
    for e in d.values():
        tid, name = (e.get("id") or "").upper(), (e.get("name") or "").strip()
        if not name or not tid.endswith("000") or e.get("isDemo"): continue
        if re.search(r"\b(demo|trial|体験版|upgrade pack|friend's pass)\b", name, re.I): continue
        name = re.sub(r"\s+", " ", name.replace("™", "").replace("®", "")).strip()
        if JUNK.search(name): continue
        name = polish(name, False)
        is_s2 = tid.startswith("04") or bool(S2_EDITION.search(name))
        name = S2_EDITION.sub("", name).strip(" -–—:")
        # the US eShop list, so every title is a US release
        (s2 if is_s2 else s1).setdefault(key(name), [name, 1, int(e.get("numberOfPlayers") or 0)])
    for t, us, pl in S2_EXTRA: s2.setdefault(key(t), [t, us, pl])
    srt = lambda m: sorted(m.values(), key=lambda x: x[0].lower())
    return srt(s1), srt(s2)
# PS4 and PS5 come from PS Store title lists (andshrew/PlayStation-Titles). Region UP/UB is the US store.
PS_APPS = re.compile(r"\b(?:Entitlement|\(Prod\)|Prod\b|Test(?:ing)?\b|Playtest|Benchmark|Share Factory|Media Player|PlayStation(?:®)? ?(?:Vue|Now|Plus|VR Worlds Demo|App)|"
                     r"Spotify|Twitch|Disney\+|Prime Video|HBO|Max\b|Apple TV|Peacock|Paramount\+|DAZN|Tubi|Pluto TV|Funimation|Vudu|Showtime|Starz|MUBI|Plex|"
                     r"Crunchyroll|Netflix|Hulu|YouTube|NFL Sunday Ticket|NBA App|MLB\.tv|NHL\.tv|Dynamic Theme|Theme\b|Avatars?\b|Soundtrack|Artbook|Art Book|"
                     r"Wallpaper|Costume|Upgrade\b|Expansion Pass|Season Pass|Character Pass|Starter Pack|Currency|Coins?\b|V-Bucks|Points\b|Credits\b|"
                     r"Trial|Demo|Prologue Demo|Beta|Tech Test|Network Test|Stress Test|Kiosk|Not for Resale|Rental|Install Disc|"
                     r"TV Player|Claro video|Crackle|iHeartRadio|Apple Music|MEGOGO|AquaTV|ClanTV|Gamepass|Fight ?pass|Tracker|Remote App|Mail App|Deluxe Edition App|Sound App|"
                     r"Art Pack|Track Compilation|Music Concert|Musical Notes|Pre-?order|Item Pack|OST|Making Of|Behind the Scenes|Digital Video|Digital Content|"
                     r"Season Update|Season Pack|Bonus|System App|Maps App|TestGame|Sound ?Track|Music Album|Official Music|Music from)|[αβ]Test|demo$|_demo|^(?:CUSA|PPSA)\d|^\d{6,}|Webmaf|_QA_|^Test\d|Themes\b|Foxtel|RMC Sport|Filmo TV|Magine TV|NOS TV|^Now TV|NRK TV|BBC Sport|BT Sport|Eurosport|francetv|Rakuten TV|Red Bull TV|UEFA\.tv|Optus Sport|"
                     r"Redbox|360Channel|Mediaset|Anghami|JOYSOUND|Wild Duck|β Version|IARC|Grada1 TV|Tennis TV|TV 2 Sumo|TV from Sky|NOS Sport|SFR Sport|Sky Sport", re.I)
# the same game listed once per region by a small publisher ("Boxed Beasts PS4 EU")
PS_REGION = re.compile(r"_(?:CUSA|PPSA)\d+$|\s+(?:PS[45]\s+)?(?:ASIA|EU|NA|JA|US|UK)$|\s*\((?:Japan|Korea Ver\.|Asia|EU|US)\)$")
# store names carry editions and platform tags; the game is the same game
PS_EDITION = re.compile(r"\s*[-–—:(]?\s*(?:(?:Digital|Standard|Deluxe|Digital Deluxe|Gold|Ultimate|Complete|Definitive|Premium|Special|Collector'?s|Legendary|Launch|Day One|Anniversary|"
                        r"Enhanced|Game of the Year|GOTY|Super Deluxe|Cross-Gen|Champions|Founder'?s|Supporter'?s|Season|Director'?s Cut|Remastered Deluxe)\s*(?:Edition|Bundle|Pack)?|"
                        r"(?:PS4|PS5)(?:™)?\s*(?:&|and|/)\s*(?:PS4|PS5)(?:™)?|PS4™?|PS5™?|PlayStation®?\s?[45]|for PS[45]|PS[45] Version|Version PS[45])\s*\)?\s*$", re.I)
# store spellings that lose a space or read oddly
PS_FIX = {"fallguysultimateknockout": "Fall Guys", "granturismosport": "Gran Turismo Sport", "watchdogs": "Watch Dogs", "watchdogs2": "Watch Dogs 2", "tekken7": "Tekken 7", "tekken8": "Tekken 8", "callofdutyblackops6": "Call of Duty: Black Ops 6", "callofdutyblackops7": "Call of Duty: Black Ops 7"}
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af\uff00-\uffef]")
def from_psstore(path):
    games = {}
    for i, line in enumerate(open(path, encoding="utf-8", errors="replace")):
        cols = line.rstrip("\n").split("\t")
        if i == 0 or len(cols) < 5: continue
        name, region = cols[2].strip(), cols[4].strip()
        # rows with no store region (or Sony-internal IP) were never on sale: placeholders, QA builds, cancelled games
        if not name or region in ("", "IP") or CJK.search(name): continue
        name = re.sub(r"\s+", " ", re.sub(r"[™®©]", "", name)).strip()
        if PS_APPS.search(name) or JUNK.search(name) or BAD.search(name): continue
        for _ in range(3): name = PS_REGION.sub("", PS_EDITION.sub("", name)).strip(" -–—:")
        name = polish(name, False)
        name = PS_FIX.get(key(name), name)
        if name != name.upper(): name = re.sub(r"(?<=\w )OF(?= \w)", "of", name)   # "Mark OF the Wolves" from shouty store names
        if len(name) < 2: continue
        e = games.setdefault(key(name), [name, 0, 0])
        if region in ("UP", "UB"):
            if not e[1]: e[0] = name   # prefer the US store's spelling
            e[1] = 1
    return sorted(games.values(), key=lambda x: x[0].lower())
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
for cid in ("ps4", "ps5"):
    g = from_psstore(os.path.join(src, "psstore", cid.upper() + "_Titles.tsv")); total += len(g)
    json.dump(g, open(os.path.join(out, cid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(cid, len(g), "us", sum(x[1] for x in g), os.path.getsize(os.path.join(out, cid + ".json")))
# Xbox One, Xbox Series X|S and PC have no game database the build can reach, so they use hand-made lists
# of well-known released games (tools/hand_lists.json, entered from knowledge). All are US releases.
hand = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_lists.json"), encoding="utf-8"))
for cid in ("xone", "xsx", "pc"):
    g = {}
    for t, pl in hand[cid]: g.setdefault(key(t), [t, 1, pl])
    g = sorted(g.values(), key=lambda x: x[0].lower()); total += len(g)
    json.dump(g, open(os.path.join(out, cid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(cid, len(g), "(hand-made)", os.path.getsize(os.path.join(out, cid + ".json")))
print("total", total)

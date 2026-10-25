# Pour Decisions

A bet-list drinking-night app. It's a single page (`index.html`) with a service worker (`sw.js`), and it's hosted on GitHub Pages from `main`. Everything is saved in the browser's localStorage. There is no build step for the app itself.

## Layout

- `index.html` holds all the HTML, CSS, and JS. The code between `<!--ARTIFACT-START-->` and `<!--ARTIFACT-END-->` is also published as the Claude preview, so keep the manifest and service-worker registration outside those markers.
- `sw.js` is the offline cache. Pages load network-first, and everything else (including `catalog/*.json`) is stale-while-revalidate.
- `catalog/<console>.json` holds the complete game list for each console that has one.
- `tools/build_catalog.py` rebuilds those lists from the source databases.
- `CATALOG` in `index.html` lists every console. Each entry has the hand-picked party games (`party`), their player counts (`pp`), party picks that weren't released in the US (`nonus`), the full-list size (`full`), and whether the full list has player counts (`pl`).

## Game catalog rules

Follow every rule here whenever you add or change games, consoles, or catalog data.

### Sources

- **Complete lists come from real databases, never from memory.** Use No-Intro and Redump DATs from `libretro/libretro-database` (`metadat/no-intro`, `metadat/redump`, `dat/` for Wii U), player counts from `metadat/maxusers`, and `blawar/titledb` `US.en.json` for Switch and Switch 2. `raw.githubusercontent.com` is reachable from cloud sessions, but Wikipedia is not.
- **Hand additions are allowed only for well-known, already released games** that a database is missing, such as `S2_EXTRA` for Switch 2. Only add a game you're confident is out, and leave out announced or unconfirmed titles. Say in your summary that hand additions come from knowledge, not a database.
- Consoles with no complete source (PS4, PS5, Xbox One, Series X|S, PC, Arcade, Cards & party) use hand-picked lists only. Don't present them as complete.

### Entry format and cleanup (all in `tools/build_catalog.py`)

- Each entry is `[title, released_in_us (1/0), max_players (0 = unknown)]`, sorted case-insensitively.
- Remove betas, protos, demos, samples, kiosk, debug, unlicensed, pirate, aftermarket, and hacks (`SKIP` for tags in parentheses, `BAD` for name patterns).
- Remove anything that isn't a game (`JUNK`): cheat devices (Action Replay, GameShark, Xploder, CodeBreaker cheat discs, "Cheats"), magazine, demo, movie, and sampler discs, firmware and updates, DLC, map, track, and song packs, season passes, test suites, streaming and video apps (Netflix, Amazon Video, Hulu, YouTube), and closed or open betas. Atari's real game "Codebreaker" must survive.
- Tidy names (`clean`, `polish`): drop region, revision, and disc tags, turn "Title, The" into "The Title", and turn `" - "` subtitles into `": "`. For No-Intro alternate titles joined with `" ~ "`, keep only the first name. Title-case ALL-CAPS store names but keep real acronyms and Roman numerals (`ACRONYM`: FIFA, NBA, NFL, II, HD, LEGO, and so on).
- Dedupe by the normalized key: lowercase, accents removed, `&` turned into "and", and only a–z and 0–9 kept. The JS `catKey` must use the same normalization. When merging variants, the game counts as US if any variant was US, and the max player count wins. Player counts are matched through the same cleaned name.
- Switch vs Switch 2: titledb entries with title IDs starting `04`, and anything named "Nintendo Switch 2 Edition", go to `switch2` only. Strip the "Nintendo Switch 2 Edition" suffix from the name. Skip Upgrade Packs, Friend's Passes, demos, and anything that isn't a base title (ID must end in `000`).

### Party picks (`CATALOG` in `index.html`)

- Every party pick needs a player count in `pp`. Use the database count when it exists, otherwise the couch count (players on one console). Use `"No"` strings such as `"15o"` for online-only games. Leave a game out rather than guess wildly.
- Use the game's US title so the US filter and player counts match, for example Jet Grind Radio rather than Jet Set Radio. Recompute `nonus` from the full list after any change, and only list picks that truly had no US release (SingStar on PS2, for example).
- Keep `full` in sync with each JSON file's length after a rebuild.

### Shipping a catalog change

1. Run `python3 -I tools/build_catalog.py <dats-dir> catalog` on fresh source files, then review the printed per-console counts.
2. **Bump `CATALOG_REV` in both `index.html` and `sw.js`**, and bump `VERSION` in `sw.js`. Without this, phones keep their old saved lists, which is how the US filter once stopped working. If you add a new console file, add it to `CATALOG_FILES` in `sw.js`.
3. Update `CATALOG` (`full`, `pp`, `nonus`, renamed picks) and the README's catalog section.

### Checks to run before pushing

Serve the folder with `python3 -m http.server` (a service worker needs http, not `file://`) and check these with Playwright:

- Search each changed console for junk ("action replay", "demo", "magazine", "netflix", "beta", "~"). It should find nothing.
- Spot-check that famous titles exist with the right US flag and player count (for example GoldenEye 007 on N64 = US, 4 players).
- Every party pick shows a 👥 count (party filter, Show all, no row without "👥").
- The US-only filter changes the count on every console with a full list, including the default All-consoles party view.
- The Players filter and Show all work, and Switch's ~19k rows render quickly.
- Upgrade path: install the previous commit, let the service worker cache it, deploy the new files, reload, and confirm the new data is used.
- Offline: after caching, go offline and confirm a console's list still loads.
- No page errors, and no horizontal scroll at a 390px width.

## Other conventions

- Saved state (`S`) must stay backward compatible. Old saves can be missing newer fields, so default them when reading.
- Avoid full re-renders on `change` or `blur` while someone may be tapping, because they swallow the next tap. Update text in place on `input` instead.
- When killing the local test server, use `pkill -f "[h]ttp.server 8765"` in its own command. A plain pattern also matches the shell running it and kills it.
- Commits go to `main` (GitHub Pages serves it) and end with the session's attribution lines.

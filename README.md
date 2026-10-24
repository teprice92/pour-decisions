# Pour Decisions

A bet list app for drink nights. Everyone picks their games, you take turns spinning the wheel to see what gets played next, and the app keeps score of who won and who drank.

Open `index.html` in any browser. No install or build step. Live at https://teprice92.github.io/pour-decisions/ once GitHub Pages is on (Settings → Pages → Deploy from a branch → `main` / root).

## How a night works

1. **Lineup**: add players and have each one pick 10 games (the number is adjustable). Shuffle the turn order if you like. Games you've played before show up in a library you can tap to fill in lists instead of typing.
2. **Spin**: the player whose turn it is spins the wheel. Choose whether the wheel holds everyone's remaining games or only the spinner's. Already played a game off the wheel? Tap **Log a game** (in the header, or next to the Spin button) at any time, even in the middle of a round. Pick the game, the winner, and the shots, and it's saved right away. The wheel, the round in progress, and whose turn it is stay exactly as they were.
3. **Record**: pick the winner (or tie), set the shots on the line (¼, ½, ¾, 1, 1½, 2, 3, or any quarter amount), and fine-tune who drinks and how much. Turn on **Winner drinks half** to have the winner pour half of what's on the line. Hit **Pour it** and the shot glass fills up.
4. **Shots**: the shot board shows each player's glass, total shots, and wins. Penalty buttons add ¼, ½, or 1 shot at any time.
5. **History**: wrap up the night to save it. The hall of fame tracks wins and shots across every night, matched by player name. **Game history** lists every game you've played, how many times, and who won it, and each past night shows its games in order with the winner.

## Games tab

A catalog of about 62,000 games across 26 consoles, including single-player one-offs as well as party games.

- **Complete libraries** for Atari 2600, NES, SNES, N64, GameCube, Wii, Wii U, Switch, Game Boy, Game Boy Color, Game Boy Advance, DS, Genesis, Dreamcast, PlayStation 1–3, Xbox, and Xbox 360.
- **Hand-picked lists** for PS4, PS5, Xbox One, Xbox Series X|S, PC, arcade, and cards & party games. For anything missing, use **Not listed? Type any game**.
- **🎉 Party friendly only** narrows any console to the multiplayer, bet-friendly picks.
- **🇺🇸 US releases only** hides Japan-only and Europe-only games.
- **Players** filters by max player count (1 player, 2+, 3+, 4+), and each game shows its count where the data has one. Counts are available for Atari 2600, NES, SNES, N64, Game Boy, Game Boy Color, Game Boy Advance, Genesis, and Switch.
- **Show all** lists every matching game at once. **Show more** pages through 300 at a time.

Search across every console, tap **+ Add** to put a game on a player's list, or fill their empty slots at random. Each console's list loads the first time you open it. The installed app saves them all in the background so the catalog works offline.

The complete lists and player counts come from the [No-Intro](https://no-intro.org) and [Redump](http://redump.org) databases (via [libretro-database](https://github.com/libretro/libretro-database)) and [titledb](https://github.com/blawar/titledb) for Switch. Betas, demos, prototypes, and regional duplicates are removed. To refresh them, run `tools/build_catalog.py` on fresh copies of those files.

## Party features

- **Wild slices**: special slices on the wheel, such as Double or nothing, Everyone drinks, Spinner picks, Reverse, and Waterfall. In Settings you can choose how many show up each round (0 to 3), read what each one does, and switch individual ones on or off.
- **Side bets**: before you record a game, anyone can bet on who wins. Wrong guesses drink the stake, and right guesses hand it out.
- **Rivalries and grudge matches**: when someone keeps beating the same person, the app points it out. One tap makes the next game a grudge match where the loser drinks double.
- **Streaks**: three wins in a row puts you "on fire" 🔥. Whoever breaks a streak of 3 or more makes the streak holder drink a bonus.
- **Water rounds**: a 💧 reminder every few shots for each player. Set it in Settings.
- **Finale bracket**: under Shots → Finale bracket, the top players by tonight's wins play a knockout. The loser of each match drinks.
- **Night recap**: MVP, most shots, biggest upset, most played game, and a funny title for each player. Share it as an image or copy it as text. It also pops up when you wrap up a night.
- **Trophy case**: achievements that carry across every night, like Hat trick, Untouchable, Perfect night, Console warrior, and Champion. "How to earn each trophy" explains every one, and tapping a trophy shows what it takes.
- **Avatars and colors**: tap a player's circle in the Lineup to give them an emoji and a color. There's also a custom drawn husky avatar (black and white fur, blue eyes).
- **TV mode**: a big-screen layout with the wheel and a live shot board. Use it on a laptop hooked to the TV, or mirror your phone.
- **Send tonight to another phone**: History → Send tonight makes a link that opens the night on another phone. It's a copy, so the two phones don't stay in sync.
- **Theme sound packs**: many themes have their own sounds, like the Zelda secret jingle, the Mario coin, a lightsaber hum, and the Metal Gear alert.

## Settings

Under **History → Settings** you can set the default shots on the line, whether the winner drinks half by default, the number of wild slices, the side bet stake, the streak-breaker bonus, and how often water rounds come up.

## Chaos roll

The **Chaos roll** button in the header opens a random number picker you can use any time for alterations, tiebreaks, or punishments. Set a min and max and roll it as a wheel, a coin, or a die.

## Themes

Xbox, PlayStation, Metal Gear, Card night, Nintendo, Castlevania, Zelda, Halo, Pokémon, Synthwave, Street Fighter, Minecraft, Fallout, Mario Kart, Mortal Kombat, Skyrim, GTA, Among Us, Dive Bar, Star Wars, Sakura, Cruise, Pride, and Wedding. Each one changes the colors, fonts, wheel, liquid in the shot glass, and the lines the app says to you.

## Saving

Everything is saved automatically in the browser you use (localStorage). Use **History → Backup** to copy or download a backup and restore it on another device.

## Install on your phone

Pour Decisions is a progressive web app, so you can install it from the live site and it works offline.

- **iPhone (Safari):** open the site, tap Share, then **Add to Home Screen**.
- **Android (Chrome):** open the site and tap **Install app** in History → Phone app, or use the browser menu's **Install app**.

When you're online, the app always loads the newest version from the site. Offline, it opens the last version it saved, with all themes and fonts.

On iPhone, the home screen app keeps its own saved data, separate from Safari. To bring nights you tracked in Safari over to the app, use **History → Backup → Copy backup** in Safari, then **Restore** in the app.

When you change the list of app files (new icons and so on), bump `VERSION` in `sw.js`. Changes to `index.html` don't need a bump.

# Pour Decisions

A bet list app for drink nights. Everyone picks their games, you take turns spinning the wheel to see what gets played next, and the app keeps score of who won and who drank.

Open `index.html` in any browser. No install or build step. Live at https://teprice92.github.io/pour-decisions/ once GitHub Pages is on (Settings → Pages → Deploy from a branch → `main` / root).

## How a night works

1. **Lineup**: add players and have each one pick 10 games (the number is adjustable). Shuffle the turn order if you like. Games you've played before show up in a library you can tap to fill in lists instead of typing.
2. **Spin**: the player whose turn it is spins the wheel. The default **Big wheel** is a Price is Right style drum where every game name runs the full width, so long titles fit. Switch to **Round wheel** under the wheel if you prefer the classic look. Choose whether the wheel holds everyone's remaining games or only the spinner's. Already played a game off the wheel? Tap **Log a game** (in the header, or next to the Spin button) at any time, even in the middle of a round. Pick the game, the winner, and the shots, and it's saved right away. The wheel, the round in progress, and whose turn it is stay exactly as they were.
   The same game can go on a list more than once, and **↺ Play again** in tonight's rounds puts a played game back on the wheel.
3. **Record**: pick the winner (or tie), set the shots on the line (¼, ½, ¾, 1, 1½, 2, 3, or any quarter amount), and fine-tune who drinks and how much. Turn on **Winner drinks half** to have the winner pour half of what's on the line. Hit **Pour it** and the shot glass fills up.
4. **Shots**: the shot board shows each player's glass, total shots, and wins. Penalty buttons add ¼, ½, or 1 shot at any time.
5. **History**: wrap up the night to save it. Pick **End night, same games & players** to go straight back to a full wheel with the same lineup, **keep crew** to keep the players and pick new games, or **new crew** to start over. The hall of fame tracks wins and shots across every night, matched by player name. **Game history** lists every game you've played, how many times, and who won it, and each past night shows its games in order with the winner.

## Games tab

A catalog of about 62,000 games across 27 consoles, including single-player one-offs as well as party games.

- **Complete libraries** for Atari 2600, NES, SNES, N64, GameCube, Wii, Wii U, Switch, Switch 2, Game Boy, Game Boy Color, Game Boy Advance, DS, Genesis, Dreamcast, PlayStation 1–3, Xbox, and Xbox 360.
- **Hand-picked lists** for PS4, PS5, Xbox One, Xbox Series X|S, PC, arcade, and cards & party games. For anything missing, use **Not listed? Type any game**.
- **🎉 Party friendly only** narrows any console to the multiplayer, bet-friendly picks.
- **🇺🇸 US releases only** hides Japan-only and Europe-only games.
- **Players** filters by max player count (1 player, 2+, 3+, 4+), and each game shows its count where the data has one. Every 🎉 party pick has a count: the number who can play on one console, or an online count for online-only games like Among Us. Beyond those, counts come from the databases for Atari 2600, NES, SNES, N64, Game Boy, Game Boy Color, Game Boy Advance, Genesis, and Switch.
- **Your own tags**: tap ⭐ on any game to favorite it, and 🎉 to mark it as a party game or unmark a built-in one. **⭐ Favorites only** shows just your favorites, which also sort to the top of every list. Tags are included in backups.
- **Show all** lists every matching game at once. **Show more** pages through 300 at a time.

Search across every console, tap **+ Add** to put a game on a player's list, or fill their empty slots at random. Each console's list loads the first time you open it. The installed app saves them all in the background so the catalog works offline.

The complete lists and player counts come from the [No-Intro](https://no-intro.org) and [Redump](http://redump.org) databases (via [libretro-database](https://github.com/libretro/libretro-database)) and [titledb](https://github.com/blawar/titledb) for Switch and Switch 2. The Switch 2 list covers the eShop data plus well-known releases it's missing, so it may lag behind brand-new games. Betas, demos, prototypes, regional duplicates, cheat discs (Action Replay, GameShark), magazine and demo discs, DLC packs, and streaming apps are removed, and ALL-CAPS store names are tidied. To refresh them, run `tools/build_catalog.py` on fresh copies of those files.

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

## Stats and bragging rights

The **Stats** tab adds up every night saved in History, plus tonight's:

- **Shots per night** for each player as a line chart (hover or tap for the numbers), and **all-time wins** as bars. Every chart has a **Table** button.
- **Player cards**: nights, games, wins, win rate, total shots, and shots per night. Each card also shows the player's **nemesis** (who beats them most), their **favorite victim**, their best and toughest games, and their win rate by console.
- **Game rankings**: every game has its own rating. Everyone starts at 1000, and beating someone takes points from them, more if they were rated higher. Pick a game to see its leaderboard, and **Champions by game** shows who's on top of each one.
- **Round photos**: tap **📷 Photo** on any recorded round to attach a picture. Photos show in the round log, the night recap, and History. They're shrunk and stored in this browser (IndexedDB), and they aren't included in backups or send-a-night links.

## Settings

Under **History → Settings** you can set the default shots on the line, whether the winner drinks half by default, the number of wild slices, the side bet stake, the streak-breaker bonus, and how often water rounds come up.

## Chaos roll

The **Chaos roll** button in the header opens a random number picker you can use any time for alterations, tiebreaks, or punishments. Set a min and max and roll it as a wheel, a coin, or a die.

## Themes

Xbox, PlayStation, Metal Gear, Card night, Nintendo, Castlevania, Zelda, Halo, Pokémon, Synthwave, Street Fighter, Minecraft, Fallout, Mario Kart, Mortal Kombat, Skyrim, GTA, Among Us, Dive Bar, Star Wars, Sakura, Cruise, Pride, Wedding, and Policenauts. Each one changes the colors, fonts, wheel, liquid in the shot glass, and the lines the app says to you.

**Build your own theme:** pick **＋ Build your own…** in the theme menu, or **History → Your themes → Build a theme**. Start from any built-in theme or tap **🎲 Surprise me**, then choose the background, card, text, button, and drink colors, the six wheel slice colors, a background pattern, the corner roundness, heading and body fonts, ALL CAPS headings, the spin button word, what the app says when the wheel lands, your own pour lines, and which built-in theme's music and sounds to borrow. The whole app shows your changes as you make them. Cancel puts everything back. It warns you if text would be hard to read. Your themes appear under "Your themes" in the theme menu, and you can edit or delete them from History. They're saved in this browser and included in backups.

## Music

Tap **♪ Music** in the header to turn on background music. Each theme has its own original loop in its style: chiptune for the Nintendo themes, gothic for Castlevania, slow synth pads for Halo and Skyrim, a 90s city-pop groove for Policenauts, and so on. The loops are generated in the browser, so they work offline and there's nothing to download. Set the volume under History → Settings.

**Your own music:** under History → Settings → *Your own music*, paste a Spotify, YouTube, or YouTube Music link (song, album, or playlist) for any theme, or for all themes. That theme then plays it in a small player in the corner instead of the built-in loop. Links are saved in this browser only. Everything loops: YouTube songs and playlists repeat, and Spotify links start over from the top when they finish. Spotify plays 30-second previews unless you're logged in to Spotify in that browser, and phones usually need one tap on play inside the player. The players only work on the hosted site, not in the Claude preview. Music gets quieter during pours and pauses when the app is in the background.

## Saving

Everything is saved automatically in the browser you use (localStorage). Use **History → Backup** to copy or download a backup and restore it on another device.

## Install on your phone

Pour Decisions is a progressive web app, so you can install it from the live site and it works offline.

- **iPhone (Safari):** open the site, tap Share, then **Add to Home Screen**.
- **Android (Chrome):** open the site and tap **Install app** in History → Phone app, or use the browser menu's **Install app**.

When you're online, the app always loads the newest version from the site. Offline, it opens the last version it saved, with all themes and fonts.

On iPhone, the home screen app keeps its own saved data, separate from Safari. To bring nights you tracked in Safari over to the app, use **History → Backup → Copy backup** in Safari, then **Restore** in the app.

When you change the list of app files (new icons and so on), bump `VERSION` in `sw.js`. When you rebuild `catalog/*.json`, bump `CATALOG_REV` in both `index.html` and `sw.js` so phones fetch the new lists instead of a saved copy. Changes to `index.html` don't need a bump.

# Pour Decisions

A bet list app for drink nights. Everyone picks their games, you take turns spinning the wheel to see what gets played next, and the app keeps score of who won and who drank.

Open `index.html` in any browser. No install or build step. Live at https://teprice92.github.io/pour-decisions/ once GitHub Pages is on (Settings → Pages → Deploy from a branch → `main` / root).

## How a night works

1. **Lineup**: add players and have each one pick 10 games (the number is adjustable). Shuffle the turn order if you like. Games you've played before show up in a library you can tap to fill in lists instead of typing.
2. **Spin**: the player whose turn it is spins the wheel. Choose whether the wheel holds everyone's remaining games or only the spinner's. Already played a game off the wheel? Tap **Log a game** (in the header, or next to the Spin button) at any time, even in the middle of a round. Pick the game, the winner, and the shots, and it's saved right away. The wheel, the round in progress, and whose turn it is stay exactly as they were.
3. **Record**: pick the winner (or tie), set the shots on the line (¼, ½, ¾, 1, 1½, 2, 3, or any quarter amount), and fine-tune who drinks and how much. Turn on **Winner drinks half** to have the winner pour half of what's on the line. Hit **Pour it** and the shot glass fills up.
4. **Shots**: the shot board shows each player's glass, total shots, and wins. Penalty buttons add ¼, ½, or 1 shot at any time.
5. **History**: wrap up the night to save it. The hall of fame tracks wins and shots across every night, matched by player name. **Game history** lists every game you've played, how many times, and who won it, and each past night shows its games in order with the winner.

## Settings

Under **History → Settings** you can set the default shots on the line for every new game, and whether the winner drinks half by default.

## Chaos roll

The **Chaos roll** button in the header opens a random number picker you can use any time for alterations, tiebreaks, or punishments. Set a min and max and roll it as a wheel, a coin, or a die.

## Themes

Xbox, PlayStation, Metal Gear, Card night, Nintendo, Castlevania, Zelda, Halo, Pokémon, Synthwave, Street Fighter, Minecraft, Fallout, Mario Kart, Mortal Kombat, Skyrim, GTA, Among Us, and Dive Bar. Each one changes the colors, fonts, wheel, liquid in the shot glass, and the lines the app says to you.

## Saving

Everything is saved automatically in the browser you use (localStorage). Use **History → Backup** to copy or download a backup and restore it on another device.

## Install on your phone

Pour Decisions is a progressive web app, so you can install it from the live site and it works offline.

- **iPhone (Safari):** open the site, tap Share, then **Add to Home Screen**.
- **Android (Chrome):** open the site and tap **Install app** in History → Phone app, or use the browser menu's **Install app**.

When you're online, the app always loads the newest version from the site. Offline, it opens the last version it saved, with all themes and fonts.

On iPhone, the home screen app keeps its own saved data, separate from Safari. To bring nights you tracked in Safari over to the app, use **History → Backup → Copy backup** in Safari, then **Restore** in the app.

When you change the list of app files (new icons and so on), bump `VERSION` in `sw.js`. Changes to `index.html` don't need a bump.

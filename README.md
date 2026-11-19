# Leonida Trophy Guide

An unofficial, offline guide and tracker for the 55 PlayStation 5 trophies of Grand Theft Auto VI, built for the make.fun bounty [gta6-trophy-guide-01](https://make.fun/bounty/gta6-trophy-guide-01).

![Bounty status](https://make.fun/badge/gta6-trophy-guide-01.svg)
![Rank](https://make.fun/badge/gta6-trophy-guide-01/emasinves0-commits/gta6-trophy-guide/rank.svg)
![Reward](https://make.fun/badge/gta6-trophy-guide-01/emasinves0-commits/gta6-trophy-guide/reward.svg)

## Run it

```
node serve.ts
```

Then open http://localhost:8080. The app is plain static files in `app/` (vanilla JS modules, CSS, no build step, no network requests), so any static server works and it runs with the network off.

Hand-in: `MAKEFUN_OUTPUT_DIR=out node main.ts` copies `app/` and `screenshots/` and writes `dossier.json`.

## What it holds

- All 55 official trophies (1 platinum, 2 gold, 6 silver, 46 bronze) with official names, descriptions and grades, kept exactly as published.
- A guide for each trophy in original words, with its kind, a missable flag, a roadmap stage and cited sources. Where the official wording is vague, the guide says the trigger is unconfirmed instead of inventing details.
- A checklist saved in localStorage, a progress bar with counts by grade, filters by kind (story, missable, collectibles, activities), grade filter, search, hide-earned.
- A spoiler setting that hides story trophy names and descriptions until earned.
- Export progress to a JSON file and import it back.
- A seven-stage roadmap to the platinum, and missable trophies flagged in the list and the roadmap.

## Files

- `app/data/trophies.json` – trophies, roadmap stages, source index
- `app/app.js` – state and wiring · `checklist.js` – cards · `filters.js` – filtering and spoilers · `progress.js` – bar and counts · `roadmap.js` – stages · `storage.js` – localStorage and files · `style.css` – neon-sunset look in pure CSS

No Rockstar logo, official artwork or game screenshots are used. Fan project, not affiliated with Rockstar Games or Sony.

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
- Every guide is a list of numbered steps in original wording; each step is one claim and carries numbered source chips. The app counts the totals live (claims cited, claims backed by 2+ sites, guides citing sources) and shows them in an audit strip under the header.
- A CLAIMS — EVERY FACT CITED section per guide, and a SOURCES FOR THIS GUIDE panel with per-source claim counts and read dates.
- Dispute boxes: 15 open points, each labelled (4 true source disagreements, plus two-targets, wording-only, uncertain and unconfirmed-trigger cases such as meditation 15 vs 18, which is two different targets), with version A, version B and our call.
- Dense tracker: filters with counts (Story, Missable, Collectibles, Activities, Disputed, At risk, PSN-hidden, Unconfirmed, Not earned), a NEXT UP roadmap-order list, search, grade filter and hide-earned.
- YOUR COUNT trackers for count trophies (for example 4/18 meditation spots), saved with progress.
- Spoiler shield that masks hidden trophies until earned and shows how many are masked.
- Tabs routed by URL hash: `#tracker` (or `#tracker/28` to open a trophy), `#roadmap`, `#missables`, `#sources`.
- Progress and counts saved in localStorage; export to a JSON file and import it back.
- A three-stage roadmap to the platinum and a missables tab with each window and last chance.

## Tools

- `tools/add-steps.py` rebuilds the steps, claims, counts and disputes in `trophies.json` (first pass: `tools/update-guides.py`); `tools/apply-polish-fixes.py` then applies the TechWiser source and the dispute labels (idempotent).
- `tools/take-screenshots.py` and `tools/browser-test.py` drive the app in headless Chrome (`node serve.ts --port 8081` first).

## Files

- `app/data/trophies.json` – trophies with steps, roadmap stages, source index, disputes
- `app/app.js` – state, hash routing, wiring · `audit.js` – live audit strip · `checklist.js` – list rows · `guide.js` – guide, sources panel, dispute boxes · `filters.js` – filters, counts, spoilers · `progress.js` – bar · `roadmap.js` – next up and stages · `missables.js` · `sources.js` · `storage.js` · `dom.js` · `style.css` – neon-sunset look in pure CSS

No Rockstar logo, official artwork or game screenshots are used. Fan project, not affiliated with Rockstar Games or Sony.

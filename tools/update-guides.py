#!/usr/bin/env python3
"""One-off data pass: rewrites guides, sources, missable flags and the roadmap in app/data/trophies.json.
Official names, descriptions and grades are never touched. Guides are original wording based on the five cited pages."""
import json, sys
path = sys.argv[1] if len(sys.argv) > 1 else 'app/data/trophies.json'
d = json.load(open(path))

d['sources'] = {
  'ppx': {'name': 'PowerPyx: GTA 6 trophy guide and roadmap', 'url': 'https://www.powerpyx.com/gta-6-grand-theft-auto-vi-trophy-guide-roadmap/'},
  'six': {'name': 'Sixshore: GTA 6 trophies and achievements', 'url': 'https://sixshore.com/gta-6/guides/trophies-and-achievements/'},
  'plan': {'name': 'PlanetGTA6: GTA 6 trophies', 'url': 'https://www.planetgta6.com/en/gta-6-trophies/'},
  'zone': {'name': 'GTA Zone: GTA 6 trophies and achievements', 'url': 'https://gta-zone.com/news/gta-6-trophies-achievements/'},
  'cg': {'name': 'CryptoGames: GTA 6 trophies full list', 'url': 'https://cryptogames.gg/gta-6-trophies-achievements-full-list/'},
}
d['list'] = 'the official 55 trophies, checked against five guide pages on 2026-11-19'
d['note'] = ("Names, descriptions and grades are the official list and are unchanged. Guides are original text written from five public guide pages "
  "(see sources). The sources agree on the totals but not on everything: where they disagree or a trigger is not confirmed, the guide says so. "
  "These are early launch-week guides (18 Nov 2026) and may change.")

d['roadmap'] = [
 {'stage': 1, 'title': 'Story and optional missions', 'hours': '60-80 hours',
  'detail': "Play the five chapters and take optional missions as they appear (100% wants any 100 of several hundred, so there is no need to chase them all). Scan new vehicles and study animals as you go. Accept Lucia's balcony meditation in Chapter 1: it is the only possibly missable trophy. There is no mission replay and no New Game+, so one playthrough does it. Keep cheats off: they disable trophies and saving."},
 {'stage': 2, 'title': '100% Completion checklist and challenges', 'hours': 'about 100 hours',
  'detail': "The checklist (Progress > Stats > 100% Completion) opens after the story. PowerPyx calls it lenient, closer to 60% of true completion: 70 of 80 challenges, 300 of 397 stunts, 15 of 18 meditations, 200 of 277 vehicles. Robberies, underwater discoveries, shooting ranges, drone races and Bret's quests must be done in full. Nothing on the checklist is missable."},
 {'stage': 3, 'title': 'Strangers & Freaks, character quests and cleanup', 'hours': 'about 10 hours',
  'detail': "Finish 8 stranger strands plus the Andy, Kenton, Billy, Randy, Tyrone and Bret lines. They are needed for trophies but not for the 100%. Then mop up one-off trophies and the unconfirmed ones, and let the platinum pop."},
]
d['roadmapNotes'] = [
 "Total: about 200 hours to the platinum, difficulty 4/10, one playthrough (PowerPyx, GTA Zone, CryptoGames). Sixshore quotes Push Square at 250+ hours, so the estimate varies.",
 "Only 1 trophy is flagged possibly missable: Positive Mental Attitude. PlanetGTA6 says it cannot tell yet whether any are missable; all other sources agree the story trophies cannot be missed.",
 "Sources disagree on a few counts: 27 vs 28 hidden trophies, 15 vs 18 meditation spots, and some one-off triggers. Those are marked UNCONFIRMED.",
 "Saving: 15 manual slots plus an autosave (Sixshore). Save at the start and end of each chapter.",
]
d['missableNote'] = ("Positive Mental Attitude is the only trophy flagged as possibly missable (PowerPyx, repeated by GTA Zone and CryptoGames). "
  "Optional missions expire, some quest givers or fences leave and some timed quests fail, but the sources say none of that affects a trophy or the 100%.")

P,S,L,Z,C = 'ppx','six','plan','zone','cg'
# id: (stage, guide, sources, unconfirmed, hidden)
G = {
1: (3, "No task of its own: it pops when the other 54 trophies are earned. Plan on about 200 hours in total (PowerPyx; Sixshore quotes 250+), one playthrough, no difficulty setting, no PS4 version. Do the Chapter 1 meditation early, finish the roadmap stages, and watch the tracker: at 54 of 54 outside the platinum it should unlock. Cheats switch trophies and saving off, so keep them out of this save.", [P,S,Z,L], False, False),
2: (1, "Finish Gone Fishing, the first mission of Chapter 1 (PowerPyx; GTA Zone says it is one of the first missions). It is story content and cannot be missed.", [P,Z,C], False, True),
3: (1, "Unlocks when the last mission of Chapter 1 ends. Nothing extra is required. While you are in Chapter 1, take the balcony meditation (see Positive Mental Attitude) before the chapter closes.", [P,Z,C], False, True),
4: (1, "The official text says to complete Chapter 2; PowerPyx words it as starting Chapter 3, i.e. it pops at the Chapter 2 to 3 handover. Either way it is plain story progress and cannot be missed.", [P,Z,C], False, True),
5: (1, "Pops at the end of Chapter 3. GTA Zone says no story trophy can be missed. Yasmani's Chapter 3 jobs are also where the Snap Gun comes from (see Sneakthief).", [P,Z,C], False, True),
6: (1, "Pops at the end of Chapter 4. Chapter 4 also opens the optional bank-vault mission used for Maximum Withdrawal, so consider that before you start Chapter 5.", [P,Z,C], False, True),
7: (1, "Complete the final mission. CryptoGames notes Beebom and CULTR word it as Chapter 5, while the official text says the final mission, so treat the two as the same moment. Save before it: you can keep playing in free roam afterwards, but mission replay does not exist, so finish the other side lines as you like. Not missable.", [P,Z,C], False, True),
8: (1, "Finish the mission Breakfast Run. GTA Zone places it in Chapter 2. Story mission, cannot be missed.", [P,Z,C], False, True),
9: (1, "Finish The Cartel Heist, a Chapter 3 mission according to GTA Zone. Story mission, cannot be missed.", [P,Z,C], False, True),
10: (1, "Finish Child's Play, a Chapter 4 mission (GTA Zone). Story mission, cannot be missed.", [P,Z,C], False, True),
11: (1, "Finish Headliners, another Chapter 4 mission (GTA Zone). Story mission, cannot be missed.", [P,Z,C], False, True),
12: (1, "Finish VCIA Takedown, a Chapter 4 mission (GTA Zone). Story mission, cannot be missed.", [P,Z,C], False, True),
13: (1, "Finish Operation Savage Glory, a Chapter 5 mission (GTA Zone). Story mission, cannot be missed.", [P,Z,C], False, True),
14: (2, "The hardest trophy by every source, mostly because of its length. The 100% checklist opens after the story and earlier progress counts; nothing on it is missable. Targets for 100%: 70 of 80 challenges, 300 of 397 stunts, 15 of 18 meditation spots, 15 of 18 card sets, 200 of 277 vehicles, 100 of 255 animals, all 8 bank vaults, all 39 gang operations, all 42 shooting gold medals, all drone races. PowerPyx reckons that is about 60% of real completion. CryptoGames lists 30 unique races for the 100% (the others only mention 20), so check the in-game list.", [P,S,Z,C], False, False),
15: (2, "Complete 250 stunts of any type, out of 397 in the world (300 are needed for 100%, so this trophy comes first). CryptoGames reports that flying under bridges is the quickest type.", [P,S,Z,C], False, False),
16: (2, "Try each of nine activity types once. PowerPyx's list: fishing, hunting, golf, shooting ranges, pool, basketball, an arcade game, winning a race or drone race, and doing a stunt. They mostly happen while chasing other trophies; check the tracker's list and fill any gap.", [P,S,Z], False, False),
17: (2, "Gold medal in every shooting range challenge: 42 challenges at 12 ranges (PowerPyx, GTA Zone). The 100% also demands all 42, so no shortcut; practise each range until gold.", [P,S,Z,C], False, False),
18: (2, "Win one Top Fun drone race at each of the 14 locations (42 races exist; all 42 count toward the 100%).", [P,S,Z,C], False, False),
19: (2, "Win 20 different races out of 40. Winning the same race twice does not add to the count (GTA Zone). CryptoGames lists 30 for the 100% checklist.", [P,S,Z,C], False, False),
20: (3, "Beat Cal in a fishing challenge. GTA Zone says he texts you after a Chapter 1 mission and marks the spot with a purple icon. Fishing is also one of the nine Master of None activities.", [P,S,Z,C], False, False),
21: (2, "Finish one arcade game, any of them (PowerPyx, Sixshore). Also counts toward Master of None.", [P,S,Z,C], False, False),
22: (3, "Finish the last mission in Andy's line, five quests in PowerPyx's count. GTA Zone notes Andy's strand does not count toward Strangers & Freaks, so it needs its own run.", [P,Z,C,S], False, True),
23: (3, "Complete Kenton's treasure-diving line, which covers seven shipwrecks (PowerPyx, Sixshore). Underwater discoveries are also fully required for the 100%.", [P,S,Z,C], False, True),
24: (3, "Finish Billy's five jobs. GTA Zone says they start at the Thrillbilly Mudclub in Kelly County after a Chapter 2 mission and stay open after the story. Does not count toward Strangers & Freaks.", [P,Z,C], False, True),
25: (3, "Complete 8 stranger strands. Not every character counts: GTA Zone confirms Kirk, Kyle, Yago and Pilot Pete do, and Moses, Tyrone, Yasmani, Andy and Billy do not. The strands are not part of the 100%. CryptoGames passes on a single-source (TechWiser) warning that some stranger chains have story-linked windows, so start them when they unlock.", [P,Z,C,S], False, False),
26: (3, "Complete Randy's wish list, 16 sports cars (PowerPyx, Sixshore). Collect them while exploring so the last few do not need a long hunt.", [P,S,Z,C], False, True),
27: (3, "Do Tyrone's labs and then his follow-up quest (PowerPyx). Tyrone's strand does not count for Strangers & Freaks (GTA Zone).", [P,Z,C], False, True),
28: (1, "POSSIBLY MISSABLE. The first meditation is at Jason's house in Chapter 1: Lucia offers it on the balcony the morning after the Down to Earth mission, and it is gone for good after the chapter. It counts toward the meditation total but is not one of the 18 marked spots, so nobody has confirmed the trophy needs it; PowerPyx earned the trophy after doing it, so just do it (about a minute). Later spots: 18 in 10 locations, and the last needs Jason and Lucia playable together after Chapter 2 (GTA Zone). The 100% only asks for 15 of 18, so this cannot cost A Long Road. Sources differ on 15 vs 18 here.", [P,S,Z,C], False, False),
29: (3, "Hunt a unique animal for Bret. His hunting quests start after Chapter 2 and are Jason-only (GTA Zone). Which animal unlocks the trophy is unconfirmed. Bret's quests must be fully completed for the 100% anyway, so finish them all.", [P,Z,C], True, True),
30: (2, "Complete 3 collectible card sets of the 18 (15 for the 100%). Pick up cards as you meet them; three full sets arrive well before the checklist demands.", [P,S,Z,C], False, False),
31: (2, "Use WAiNK on 100 locations. GTA Zone breaks the pool into Landmarks (31), Curiosities (35), Sculptures (23) and No Flusher tags, and any mix counts. PowerPyx says 100 scans are needed.", [P,S,Z,C], False, False),
32: (2, "Complete 50 of the 80 challenges (70 are needed for the 100%). Work them alongside everything else.", [P,S,Z,C], False, False),
33: (2, "Reach 4 stars with your partner and lose the heat. PowerPyx and CryptoGames both suggest a train tunnel north of Ambrosia; bank-vault jobs often hand you the wanted level. PowerPyx expects it to land during the optional bank mission.", [P,Z,C,S], False, False),
34: (2, "Rob 3 shops in a row with your partner and keep the wanted level flashing between them. The jewelry stores in north Vice City sit close together (PowerPyx, CryptoGames). CryptoGames adds: rob a fourth if it does not pop after the third.", [P,Z,C,S], False, False),
35: (1, "Discover 100 vehicles, which scanning with WAiNK does without driving them (CryptoGames, GTA Zone). The 100% wants 200 of 277 base models, so scan every new car you see from the first hours.", [P,S,Z,C], False, False),
36: (2, "Kill 5 enemies within one use of Combat Focus: fill the meter first and use an assault rifle. Gang members seem to count; police, soldiers and civilians do not.", [P,S,Z,C], False, False),
37: (3, "Steal a passenger jet that is parked at a VCIA terminal gate, take off and get about 1 km away (PowerPyx, GTA Zone, CryptoGames).", [P,Z,C], False, True),
38: (3, "Steal a tank at Mile Zero Air Station and shoot enemies from inside it (PowerPyx, GTA Zone).", [P,Z,C], False, True),
39: (2, "Rob a jewelry store without being detected. The Snap Gun comes from Yasmani's Chapter 3 jobs; use it on the back door, find the safe code and empty the safe unseen. PowerPyx suggests Richardson Jewelry & Diamonds.", [P,S,Z,C], False, False),
40: (2, "Rob 5 of the 8 bank vaults and escape (all 8 for the 100%). They open with an optional Chapter 4 mission, 'That's Where The Money Is…': follow a security van into a bank while the vault is open. Expect 4 stars, so keep a fast bike ready.", [P,S,Z,C], False, False),
41: (2, "Rob an armored truck and escape. A bank-vault robbery counts too if you get away, so it often lands with Maximum Withdrawal.", [P,S,Z,C], False, False),
42: (2, "Clear the fog from the whole map. A plane is the quickest way to uncover the dark patches (PowerPyx, GTA Zone, CryptoGames).", [P,S,Z,C], False, False),
43: (2, "Rob one illegal operation from each of the 9 gangs (39 operations exist; all of them for the 100%).", [P,S,Z,C], False, False),
44: (3, "Official hint: a cocktail with a view on Ocean Beach. PowerPyx says to drink an Apple Martini at the Ocean View Rooftop Bar; GTA Zone and CryptoGames still list the trigger as unconfirmed. Try the bar first.", [P,Z,C], True, True),
45: (3, "PowerPyx: drive the specific blue Banshee through a showroom window, which needs the Key Cloner. GTA Zone and CryptoGames call the steps unconfirmed and only suggest driving out through the window. Treat the details as unproven.", [P,Z,C], True, True),
46: (3, "Steal all three key valuables at Kingpin Bowling and escape (PowerPyx). GTA Zone puts it as robbing the Kingpin Bowling gang operation in Port Gellhorn and then losing the police; CryptoGames calls the wording unclear. Same job, different phrasing.", [P,Z,C], False, True),
47: (3, "Max out Strength for both Jason and Lucia through gym training; working out together trains both (PowerPyx, GTA Zone, CryptoGames).", [P,Z,C], False, True),
48: (2, "500 actions that count toward your Criminal Profile (GTA Zone, PowerPyx); it should come naturally. Avoid pushing toward the permanent Irredeemable profile. CryptoGames notes this detail is single-source.", [P,Z,C], False, True),
49: (3, "Trigger unconfirmed by most sources. PowerPyx suspects it relates to the Payday Loans store in the prologue. Do not rely on this.", [P,Z,C], True, True),
50: (3, "Official hint: what the hell just happened. PowerPyx says it is the UFO easter egg, seen at night near Starlet Motel after 2 AM; GTA Zone and CryptoGames still call it unconfirmed.", [P,Z,C], True, True),
51: (3, "Trigger unconfirmed. The hint is a melee drive-by; PowerPyx believes it is kicking enemies while on a motorcycle. Treat as unproven.", [P,Z,C], True, True),
52: (2, "Launder $250,000 of marked bills through fences. It is a running total. GTA Zone says Yasmani pays the most; CryptoGames says one fence does, and the total builds during the 100% robberies.", [P,S,Z,C], False, False),
53: (2, "Spend $100,000 across shops as a running total, which usually happens by itself.", [P,S,Z,C], False, False),
54: (2, "Buy all 8 garages from the Vice City Real Estate app, about $160,000 in total. The 4 story garages do not count (GTA Zone, CryptoGames). Do this before On the Spot, which needs free garage space.", [P,S,Z,C], False, False),
55: (2, "Register 10 vehicles in the Scooter Bros app, which Moses gives you in Chapter 2. You need free garage space, so buy garages first.", [P,S,Z,C], False, False),
}
assert set(G) == {t['id'] for t in d['trophies']}
for t in d['trophies']:
    stage, guide, srcs, unconf, hidden = G[t['id']]
    t['stage'] = stage; t['guide'] = guide; t['sources'] = srcs
    t['missable'] = (t['id'] == 28)
    t['unconfirmed'] = unconf; t['hidden'] = hidden
    if t['id'] in (47, 48, 50): t['kind'] = 'activities'
json.dump(d, open(path, 'w'), indent=2, ensure_ascii=False); open(path, 'a').write('\n')

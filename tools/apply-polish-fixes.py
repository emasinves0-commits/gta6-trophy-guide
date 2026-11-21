"""Second-pass corrections to app/data/trophies.json (run after tools/add-steps.py; idempotent).
- adds TechWiser (fetched 2026-11-21) to the sources index and cites it where the fetched page supports a step
- gives every dispute an honest `kind` label and corrects framing/attribution against the earlier documented data."""
import json, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'data', 'trophies.json')
d = json.load(open(P, encoding='utf-8'))

d['sources']['tw'] = {'name': 'TechWiser: All GTA 6 trophies and achievements', 'url': 'https://techwiser.com/gta-6-trophies-achievements/', 'read': '2026-11-21'}
d['list'] = 'the official 55 trophies, checked against six guide pages (five read on 2026-11-19, TechWiser on 2026-11-21)'
d['note'] = d['note'].replace('Where sources disagree or a trigger is unconfirmed, a dispute records both versions and our call.',
    'Each dispute is labelled: sources disagree, two different targets, wording only, or an unconfirmed trigger; both versions and our call are given.')

t = d['trophies'][24]  # Strangers & Freaks
assert t['name'] == 'Strangers & Freaks'
if 'tw' not in t['sources']: t['sources'].append('tw')
t['steps'][0]['refs'] = ['ppx', 'zone', 'cg', 'tw']
t['steps'][3] = {'text': 'TechWiser warns that several stranger chains have missable windows tied to story progression, and CryptoGames repeats the warning; both say to start each chain as soon as it unlocks.', 'refs': ['cg', 'tw']}
t['window'] = 'Several stranger chains have missable windows tied to story progression (TechWiser; CryptoGames repeats it).'
t['claims'] = len(t['steps'])

def dp(q, kind, trophies, a, b, call): return {'q': q, 'kind': kind, 'trophies': trophies, 'a': a, 'b': b, 'call': call}
def v(say, by): return {'say': say, 'by': by}
D = d['disputes']
D[0] = dp('Two different meditation targets: how many spots does each one want?', 'targets', [14, 28],
  v('15 of 18 spots: the target for the 100% Completion checklist (A Long Road)', ['ppx', 'zone']),
  v('All 18 marked spots: what the Positive Mental Attitude trophy asks for ("every spot")', ['ppx', 'zone', 'six', 'cg']),
  'Not a disagreement: the same sources give 15 for the 100% and 18 for the trophy. Meditate at all 18 and both are met.')
D[1] = dp('How many trophies are hidden: 27 or 28?', 'uncertain', [],
  v('28 hidden: the 27 hidden bronze plus the hidden gold, which is how the tracker marks them', []),
  v('27 hidden: the count of the hidden bronze table alone (TechWiser lists 27 hidden bronze)', ['tw']),
  'The earlier data only records that the sources give 27 and 28 without saying which source says which; a bronze-only count versus all hidden trophies is the likely cause. The tracker masks 28; the count changes no step.')
D[2] = dp('Is the Chapter 1 balcony meditation required for Positive Mental Attitude?', 'uncertain', [28],
  v('Unconfirmed: it raises the meditation counter but is not one of the 18 marked spots, so nobody has shown the trophy needs it', []),
  v('PowerPyx did it before earning the trophy, so do not skip it', ['ppx']),
  'Do it in Chapter 1: it costs about a minute and removes the risk.')
D[3]['kind'] = 'disagree'; D[3]['a']['by'] = ['ppx', 'zone', 'cg']
D[4] = dp('Does the 100% want 20 or 30 races won?', 'disagree', [14, 19],
  v('20 unique races (the trophy count; the other sources only mention 20)', ['ppx', 'zone', 'six']),
  v('30 unique races for the 100% checklist (only CryptoGames lists 30)', ['cg']),
  'Win 20 for the trophy; check the in-game 100% list before assuming the other 10.')
D[5]['kind'] = 'disagree'
D[6]['q'] = 'When does the Chapter 2 trophy pop? (wording only)'; D[6]['kind'] = 'wording'
D[7]['q'] = 'Is the last story trophy tied to Chapter 5 or to the final mission? (wording only)'; D[7]['kind'] = 'wording'
for i in (8, 9, 10, 11, 12): D[i]['kind'] = 'unconfirmed'
D[8]['q'] = 'Unconfirmed trigger: how do you trigger In The Beginning…?'
D[9]['q'] = 'Unconfirmed trigger: how do you trigger Capital Offense?'
D[10]['q'] = 'Unconfirmed trigger: what triggers The Truth Is Out There?'
D[11]['q'] = 'Unconfirmed trigger: what triggers Ten Pin?'; D[11]['b']['by'] = []; D[11]['b']['say'] = 'Trigger unconfirmed; the hint only says melee drive-by (the earlier data says only "unconfirmed" without naming sources)'
D[12]['q'] = 'Unconfirmed trigger: what triggers Bad Luck, I Guess?'; D[12]['b']['by'] = []; D[12]['b']['say'] = 'Trigger unconfirmed (most sources; not itemised in the earlier data)'
D[13]['q'] = 'How is the Bowling trophy worded? (wording only)'; D[13]['kind'] = 'wording'; D[13]['b']['by'] = ['zone']
D[14]['kind'] = 'disagree'
d['roadmapNotes'] = [n.replace('Sources disagree on a few counts: 27 vs 28 hidden trophies, 15 vs 18 meditation spots, and some one-off triggers. Those are marked UNCONFIRMED.',
  'Open points: 27 vs 28 hidden trophies (attribution unclear), 15 vs 18 meditation spots (two different targets, not a disagreement), and some one-off triggers marked UNCONFIRMED.') for n in d['roadmapNotes']]
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('ok', len(d['sources']), 'sources', len(D), 'disputes', sorted({x['kind'] for x in D}))

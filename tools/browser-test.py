"""End-to-end test of the polished app: serve it (node serve.ts --port 8081) and run
~/workspace/venv-playwright/bin/python tools/browser-test.py. Checks trophies, filters with counts, spoiler shield,
count trackers, tabs, audit numbers against the raw data, export/import round-trip, persistence, offline use."""
import json, os, tempfile
from playwright.sync_api import sync_playwright
EXE = '/home/hatch/workspace/remotion/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell'
URL = 'http://localhost:8081/'
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, '..', 'app', 'data', 'trophies.json')))
res = []
def check(name, ok, extra=''):
    res.append(bool(ok)); print(('PASS' if ok else 'FAIL'), name, extra)

def prog(pg): return pg.inner_text('.progress-text')
def rows(pg): return pg.locator('#list .row')
def row_cb(pg, i): return rows(pg).nth(i).locator('input[type=checkbox]')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    ctx = b.new_context(viewport={'width': 1280, 'height': 800}, accept_downloads=True)
    ext = []
    ctx.on('request', lambda r: ext.append(r.url) if not r.url.startswith(URL) else None)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(URL, wait_until='domcontentloaded'); pg.wait_for_selector('#list .row')
    check('55 rows', rows(pg).count() == 55)
    # official facts intact and audit computed from data
    T = DATA['trophies']
    check('55 trophies with name/description/grade', len(T) == 55 and all(t['name'] and t['description'] and t['grade'] for t in T))
    claims = sum(t['claims'] for t in T); steps = [s for t in T for s in t['steps']]
    check('claims == steps', claims == len(steps) == sum(len(t['steps']) for t in T))
    kpi = pg.inner_text('#kpi')
    multi = sum(1 for s in steps if len(s['refs']) >= 2)
    check('KPI claims cited', f"{len(steps)}/{claims}" in kpi, kpi.replace('\n', ' | '))
    check('KPI 2+ sites', str(multi) in kpi and '55/55' in kpi)
    check('KPI disputes', str(len(DATA['disputes'])) in kpi and 'disputes' in kpi)
    check('every step cites a source key that exists', all(r in DATA['sources'] for s in steps for r in s['refs']) and all(s['refs'] for s in steps))
    # shield
    pg.evaluate("localStorage.clear()"); pg.goto(URL + '#tracker'); pg.reload(); pg.wait_for_selector('#list .row')
    check('shield default on + masked count', pg.is_checked('#spoilers') and '28 masked' in pg.inner_text('.shield'), pg.inner_text('.shield'))
    pg.uncheck('#spoilers'); pg.fill('#search', '')
    row_cb(pg, 14).check(); row_cb(pg, 15).check()
    check('progress 2', '2/55' in prog(pg), prog(pg))
    row_cb(pg, 15).uncheck(); check('uncheck -> 1', '1/55' in prog(pg))
    check('ls saved', json.loads(pg.evaluate("localStorage.getItem('gta6-trophy-guide:earned')")) == [15])
    pg.reload(); pg.wait_for_selector('#list .row')
    check('survives reload', '1/55' in prog(pg) and row_cb(pg, 14).is_checked())
    check('shield setting persisted', not pg.is_checked('#spoilers'))
    # filters with counts
    def kind(k): return pg.locator(f'#kinds button[data-kind="{k}"]')
    want = {'all': 55, 'story': 21, 'missable': 1, 'collectibles': 8, 'activities': 26, 'psnhidden': 28, 'unconfirmed': 6, 'atrisk': 8, 'notearned': 54}
    want['disputed'] = len({i for d in DATA['disputes'] for i in d['trophies']})
    for k, n in want.items():
        check(f'filter {k} count label {n}', kind(k).locator('.n').inner_text() == str(n))
        kind(k).click(); check(f'filter {k} shows {n}', rows(pg).count() == n, str(rows(pg).count()))
    kind('all').click()
    pg.select_option('#grade', 'gold'); check('grade gold=2', rows(pg).count() == 2)
    pg.select_option('#grade', 'silver'); check('grade silver=6', rows(pg).count() == 6)
    pg.select_option('#grade', 'all')
    pg.fill('#search', 'shipwreck'); check('search shipwreck', rows(pg).count() >= 1)
    pg.fill('#search', 'zzzqq'); check('search empty msg', 'No trophies' in pg.inner_text('#list'))
    pg.fill('#search', '')
    pg.check('#hide-earned'); check('hide earned 54', rows(pg).count() == 54); pg.uncheck('#hide-earned')
    # spoiler shield
    pg.check('#spoilers'); txt = pg.inner_text('#list')
    check('shield masks names', 'Paradise Lost' not in txt and 'Hidden trophy' in txt)
    check('masked not searchable', (pg.fill('#search', 'Breakfast'), rows(pg).count())[1] == 0); pg.fill('#search', '')
    check('next up masks too', 'Paradise Lost' not in pg.inner_text('#nextup') and 'Breakfast' not in pg.inner_text('#nextup'))
    check('masked count shown', '27 masked' in pg.inner_text('.shield') or '28 masked' in pg.inner_text('.shield'), pg.inner_text('.shield'))
    pg.locator('#list .row-open', has_text='Hidden trophy').first.click()
    check('masked guide hides steps', pg.locator('#guide .steps').count() == 0)
    pg.uncheck('#spoilers'); check('names shown', 'Paradise Lost' in pg.inner_text('#list'))
    # guide: steps, chips, claims, sources panel, dispute box
    pg.goto(URL + '#tracker/28'); pg.wait_for_selector('#guide .steps')
    g = pg.inner_text('#guide')
    check('guide: numbered steps with chips', pg.locator('#guide .steps li').count() == 6 and pg.locator('#guide .steps .chip-src').count() >= 6)
    check('guide: claims section', 'CLAIMS — EVERY FACT CITED' in g and '6/6 claims cited' in g)
    check('guide: official quote + #N of 55', 'Meditate at every spot across Leonida.' in g and '#28 of 55' in g)
    sp = pg.inner_text('#sources-panel')
    check('sources panel + dispute box', 'SOURCES FOR THIS GUIDE' in sp and 'SOURCES DIFFER?' in sp and 'OUR CALL' in sp)
    check('source links', pg.locator('#sources-panel .src-list a').count() >= 3)
    # count tracker
    check('count tracker shown', 'YOUR COUNT — 0/18 meditation spots' in g)
    pg.click('#guide .count button[aria-label^="One more"]'); pg.click('#guide .count button[aria-label^="One more"]')
    check('count tracker +2', 'YOUR COUNT — 2/18' in pg.inner_text('#guide'))
    pg.click('#guide .count button[aria-label^="One less"]'); check('count tracker -1', 'YOUR COUNT — 1/18' in pg.inner_text('#guide'))
    check('count persisted', json.loads(pg.evaluate("localStorage.getItem('gta6-trophy-guide:counts')")) == {'28': 1})
    # open guide survives ticking (regression)
    pg.locator('#list .row.open input[type=checkbox]').check()
    check('open guide survives tick', 'Positive Mental Attitude' in pg.inner_text('#guide') and 'meditation' in pg.inner_text('#guide'))
    pg.locator('#list .row.open input[type=checkbox]').uncheck()
    # tabs
    for tab, needle in [('roadmap', 'Stage 3'), ('missables', 'LAST CHANCE'), ('sources', 'SOURCE INDEX'), ('tracker', 'FILTERS')]:
        pg.click(f'.tabs a[data-tab="{tab}"]'); pg.wait_for_selector(f'#view-{tab}', state='visible')
        check(f'tab {tab}', needle in pg.inner_text(f'#view-{tab}') or needle in pg.inner_text('body'), pg.url)
    pg.goto(URL + '#roadmap'); pg.wait_for_selector('#view-roadmap .stage')
    rt = pg.inner_text('#view-roadmap')
    check('roadmap stages in order + hours + missable callout', rt.count('Stage ') == len(DATA['roadmap']) and '60-80 hours' in rt and 'MISSABLE' in rt and 'about 200 hours' in rt)
    check('roadmap counts', all(f"{sum(1 for t in T if t['stage'] == s['stage'])} trophies" in rt for s in DATA['roadmap']))
    pg.locator('#view-roadmap .stage input').first.check(); check('roadmap checkbox syncs', '2/55' in prog(pg))
    pg.goto(URL + '#missables'); pg.wait_for_selector('#view-missables .miss')
    check('missables 8 cards', pg.locator('#view-missables .miss').count() == 8)
    pg.goto(URL + '#sources'); pg.wait_for_selector('#view-sources .src-table')
    check('sources index rows + disputes', pg.locator('#view-sources .src-table tr').count() == len(DATA['sources']) + 1 and pg.locator('#view-sources .dispute').count() == len(DATA['disputes']))
    # export / import
    pg.goto(URL + '#tracker')
    with pg.expect_download() as dl: pg.click('#export')
    f = os.path.join(tempfile.mkdtemp(), 'p.json'); dl.value.save_as(f); exp = json.load(open(f))
    check('export content', exp['earned'] == sorted(exp['earned']) and len(exp['earned']) == 2 and exp['counts'] == {'28': 1}, str(exp))
    pg.on('dialog', lambda d: d.accept()); pg.click('#reset'); check('reset', '0/55' in prog(pg))
    pg.set_input_files('#import', f); pg.wait_for_timeout(300)
    check('import restores earned + counts', '2/55' in prog(pg) and json.loads(pg.evaluate("localStorage.getItem('gta6-trophy-guide:counts')")) == {'28': 1}, pg.inner_text('#message'))
    bad = os.path.join(os.path.dirname(f), 'bad.json'); open(bad, 'w').write('not json')
    pg.set_input_files('#import', bad); pg.wait_for_timeout(300)
    check('bad import message', 'failed' in pg.inner_text('#message') and '2/55' in prog(pg), pg.inner_text('#message'))
    open(bad, 'w').write(json.dumps({'earned': [1, 2, 999, 'x']})); pg.set_input_files('#import', bad); pg.wait_for_timeout(300)
    check('import filters invalid ids', '2/55' in prog(pg), prog(pg))
    # offline
    ctx.set_offline(True)
    row_cb(pg, 20).check(); pg.fill('#search', 'tank')
    check('works with network off', '3/55' in prog(pg) and rows(pg).count() >= 1)
    check('no external requests', not ext, str(ext)); check('no console errors', not errs, str(errs))
    b.close()
print('ALL PASS' if all(res) else 'FAILURES')

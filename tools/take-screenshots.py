"""Take the four README/judge screenshots of the polished app (real renders, 1280x800, never edited).
Start the app first:  node serve.ts --port 8081   then:  python3 tools/take-screenshots.py
Progress is seeded deterministically (3 earned trophies and a few counts) so the progress bar and counters show."""
import os
from playwright.sync_api import sync_playwright
EXE = '/home/hatch/workspace/remotion/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell'
URL = 'http://localhost:8081/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'screenshots')
SEED = {'gta6-trophy-guide:earned': '[2,3,21]', 'gta6-trophy-guide:counts': '{"28":4,"30":1,"15":112}',
        'gta6-trophy-guide:settings': '{"hideStorySpoilers":true}'}

def shot(pg, name):
    pg.wait_for_timeout(250)
    pg.screenshot(path=os.path.join(OUT, name), type='jpeg', quality=82)

def go(pg, route, ready):
    pg.goto(URL + route); pg.reload(); pg.wait_for_selector(ready, state='visible')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    ctx = b.new_context(viewport={'width': 1280, 'height': 800})
    pg = ctx.new_page()
    pg.goto(URL, wait_until='domcontentloaded')
    pg.evaluate("s => { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); }", SEED)
    # 1 cover: tracker, audit strip, Positive Mental Attitude open (steps, disputes, sources), shield ON
    go(pg, '#tracker/28', '#guide .steps')
    shot(pg, '1-cover.jpg')
    # 2 roadmap: the stages in order (shield off so the trophy names read)
    pg.evaluate("localStorage.setItem('gta6-trophy-guide:settings', '{\"hideStorySpoilers\":false}')")
    go(pg, '#roadmap', '#view-roadmap .stage')
    shot(pg, '2-roadmap.jpg')
    # 3 missables: every missable / at-risk / unconfirmed trophy with window and last chance
    go(pg, '#missables', '#view-missables .miss')
    shot(pg, '3-missables.jpg')
    # 4 sources: numbered index with claim counts + disputes
    go(pg, '#sources', '#view-sources .src-table')
    shot(pg, '4-sources.jpg')
    b.close()

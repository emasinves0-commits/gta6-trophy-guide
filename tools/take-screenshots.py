"""Take the four README screenshots from the running app (node serve.ts --port 8081)."""
import os
from playwright.sync_api import sync_playwright
EXE = '/home/hatch/workspace/remotion/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell'
URL = 'http://localhost:8081/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'screenshots')

def shot(pg, name):
    pg.screenshot(path=os.path.join(OUT, name), type='jpeg', quality=85)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    pg = b.new_context(viewport={'width': 1280, 'height': 800}).new_page()
    pg.goto(URL); pg.wait_for_selector('#list .card')
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_selector('#list .card')
    for i in (1, 2, 5):
        pg.locator('#list .card').nth(i).locator('input[type=checkbox]').check()
    # 1 cover: checklist with a guide expanded
    pg.locator('#list .card').nth(0).locator('summary').click()
    pg.evaluate("window.scrollTo(0,300)")
    shot(pg, '1-cover.jpg')
    # 2 roadmap + missable flags
    pg.locator('#roadmap').scroll_into_view_if_needed()
    pg.evaluate("document.querySelector('#roadmap').scrollIntoView()")
    shot(pg, '2-roadmap.jpg')
    # 3 guide with sources
    pg.evaluate("window.scrollTo(0,0)")
    pg.locator('#list .card').nth(27).locator('summary').click()
    pg.locator('#list .card').nth(27).scroll_into_view_if_needed()
    pg.evaluate("document.querySelectorAll('#list .card')[27].scrollIntoView({block:'start'})")
    shot(pg, '3-guide.jpg')
    # 4 spoiler mode + filter
    pg.evaluate("window.scrollTo(0,0)")
    pg.check('#spoilers'); pg.click('#kinds button:text-is("Story")')
    pg.evaluate("window.scrollTo(0,560)")
    shot(pg, '4-spoiler.jpg')
    b.close()

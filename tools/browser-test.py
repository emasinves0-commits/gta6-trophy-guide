import json, sys, tempfile, os
from playwright.sync_api import sync_playwright
EXE='/home/hatch/workspace/remotion/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell'
URL='http://localhost:8081/'
res=[]
def check(name, ok, extra=''):
    res.append(ok); print(('PASS' if ok else 'FAIL'), name, extra)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=EXE)
    ctx=b.new_context(viewport={'width':1280,'height':800}, accept_downloads=True)
    ext=[]
    ctx.on('request', lambda r: ext.append(r.url) if not r.url.startswith(URL) else None)
    pg=ctx.new_page(); errs=[]
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto(URL); pg.wait_for_selector('#list .card')
    check('55 cards', pg.locator('#list .card').count()==55)
    pg.fill('#search','') ; pg.uncheck('#spoilers')
    cards=pg.locator('#list .card')
    cards.nth(14).locator('input[type=checkbox]').check()
    cards.nth(15).locator('input[type=checkbox]').check()
    check('progress 2', '2 of 55' in pg.inner_text('.progress-text'), pg.inner_text('.progress-text'))
    pg.locator('#list .card').nth(15).locator('input[type=checkbox]').uncheck()
    check('uncheck -> 1', '1 of 55' in pg.inner_text('.progress-text'))
    check('ls saved', json.loads(pg.evaluate("localStorage.getItem('gta6-trophy-guide:earned')"))==[15])
    pg.reload(); pg.wait_for_selector('#list .card')
    check('survives reload', '1 of 55' in pg.inner_text('.progress-text') and pg.locator('#list .card').nth(14).locator('input').is_checked())
    check('spoiler setting persisted', not pg.is_checked('#spoilers'))
    # filters
    for kind,exp in [('Missable',1),('Story',None),('Collectibles',None),('Activities',None)]:
        pg.click(f'#kinds button:text-is("{kind}")'); n=pg.locator('#list .card').count(); print(' kind',kind,n)
        if exp: check('kind '+kind, n==exp)
    pg.click('#kinds button:text-is("All")')
    pg.select_option('#grade','gold'); check('grade gold=2', pg.locator('#list .card').count()==2)
    pg.select_option('#grade','silver'); check('grade silver=6', pg.locator('#list .card').count()==6)
    pg.select_option('#grade','all')
    pg.fill('#search','shipwreck'); check('search shipwreck', pg.locator('#list .card').count()>=1, str(pg.locator('#list .card').count()))
    pg.fill('#search','zzzqq'); check('search empty msg', 'No trophies' in pg.inner_text('#list'))
    pg.fill('#search','')
    pg.check('#hide-earned'); check('hide earned 54', pg.locator('#list .card').count()==54); pg.uncheck('#hide-earned')
    # spoilers
    pg.check('#spoilers'); txt=pg.inner_text('#list')
    check('spoiler hides names', 'Paradise Lost' not in txt and 'Hidden trophy' in txt)
    check('hidden not searchable', (pg.fill('#search','Breakfast'), pg.locator('#list .card').count())[1]==0); pg.fill('#search','')
    check('roadmap hides too', 'Paradise Lost' not in pg.inner_text('#roadmap-body'))
    pg.uncheck('#spoilers'); check('names shown', 'Paradise Lost' in pg.inner_text('#list'))
    pg.reload(); pg.wait_for_selector('#list .card'); check('spoiler off persisted', not pg.is_checked('#spoilers'))
    # guide + sources
    pg.locator('#list .card').nth(27).locator('summary').click()
    links=pg.locator('#list .card').nth(27).locator('.sources a'); check('sources links', links.count()>=1, str([links.nth(i).get_attribute('href') for i in range(links.count())]))
    # open guide survives checkbox re-render
    pg.locator('#list .card').nth(27).locator('summary').click() if not pg.locator('#list .card').nth(27).locator('details').evaluate('d=>d.open') else None
    pg.locator('#list .card').nth(27).locator('input[type=checkbox]').check()
    check('open guide survives tick', pg.locator('#list .card').nth(27).locator('details').evaluate('d=>d.open'))
    pg.locator('#list .card').nth(27).locator('input[type=checkbox]').uncheck()
    # roadmap
    rt=pg.inner_text('#roadmap'); check('roadmap 3 stages + hours', rt.count('Stage ')==3 and '60-80 hours' in rt and 'MISSABLE' in rt)
    pg.locator('#roadmap .stage input').first.check(); check('roadmap checkbox syncs', '2 of 55' in pg.inner_text('.progress-text'))
    # export / import
    with pg.expect_download() as dl: pg.click('#export')
    f=os.path.join(tempfile.mkdtemp(),'p.json'); dl.value.save_as(f); exp=json.load(open(f)); print(' export',exp)
    check('export content', exp['earned']==sorted(exp['earned']) and len(exp['earned'])==2)
    pg.on('dialog', lambda d: d.accept()); pg.click('#reset'); check('reset', '0 of 55' in pg.inner_text('.progress-text'))
    pg.set_input_files('#import', f); pg.wait_for_timeout(300)
    check('import restores', '2 of 55' in pg.inner_text('.progress-text'), pg.inner_text('#message'))
    bad=os.path.join(os.path.dirname(f),'bad.json'); open(bad,'w').write('not json')
    pg.set_input_files('#import', bad); pg.wait_for_timeout(300); check('bad import message', 'failed' in pg.inner_text('#message') and '2 of 55' in pg.inner_text('.progress-text'), pg.inner_text('#message'))
    open(bad,'w').write(json.dumps({'earned':[1,2,999,'x']})); pg.set_input_files('#import', bad); pg.wait_for_timeout(300)
    check('import filters invalid ids', '2 of 55' in pg.inner_text('.progress-text'), pg.inner_text('.progress-text'))
    # offline
    ctx.set_offline(True)
    pg.locator('#list .card').nth(20).locator('input[type=checkbox]').check(); pg.fill('#search','tank'); pg.click('#kinds button:text-is("All")')
    check('works with network off', '3 of 55' in pg.inner_text('.progress-text') and pg.locator('#list .card').count()>=1)
    check('no external requests', not ext, str(ext)); check('no console errors', not errs, str(errs))
    b.close()
print('ALL PASS' if all(res) else 'FAILURES')

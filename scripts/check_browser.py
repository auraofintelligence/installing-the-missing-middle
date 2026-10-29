from pathlib import Path
from playwright.sync_api import sync_playwright
import json,subprocess,time
R=Path(__file__).resolve().parents[1];Q=R/'checks';Q.mkdir(exist_ok=True)
server=subprocess.Popen(['python','-m','http.server','8765','--bind','127.0.0.1'],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
errors=[];results=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for width in [320,390,1440]:
   page=browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
   page.on('pageerror',lambda e:errors.append(str(e)))
   for f in sorted(R.glob('*.html')):
    response=page.goto('http://127.0.0.1:8765/'+f.name,wait_until='networkidle')
    overflow=page.evaluate('document.documentElement.scrollWidth>window.innerWidth+1')
    bad=page.locator('img').evaluate_all('(xs)=>xs.filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.src)')
    if overflow:errors.append(f'{f.name} horizontal overflow at {width}px')
    if bad:errors.append(f'{f.name} broken images: {bad}')
    results.append({'page':f.name,'width':width,'status':response.status,'overflow':overflow,'broken_images':bad})
    if f.name in ['index.html','installation.html','sources.html','downloads.html'] and width in [390,1440]:page.screenshot(path=str(Q/f'{f.stem}-{width}.png'),full_page=True)
   page.goto('http://127.0.0.1:8765/index.html');page.locator('[data-menu]').click()
   if page.locator('#all-nav').is_hidden():errors.append('Menu did not open')
   page.keyboard.press('Escape')
   if not page.locator('#all-nav').is_hidden():errors.append('Escape did not close menu')
   page.goto('http://127.0.0.1:8765/sources.html');page.locator('[data-filter]').fill('Aura Teacher Training')
   if page.locator('[data-search]:visible').count()!=1:errors.append('Source search mismatch')
   page.locator('[data-filter]').fill('zzzz-no-result')
   if page.locator('[data-empty]').is_hidden():errors.append('Empty search state missing')
   page.goto('http://127.0.0.1:8765/economics.html')
   if '3,000' not in page.locator('#calc-result').inner_text():errors.append('Calculator baseline mismatch')
   page.locator('#population').fill('10000')
   if not page.locator('#calc-result').inner_text().startswith('1 nodes'):errors.append('Calculator input mismatch')
   page.goto('http://127.0.0.1:8765/presentation.html');page.locator('[data-present]').click();page.keyboard.press('ArrowRight')
   if page.locator('[data-slide-count]').inner_text()!='2 / 12':errors.append('Presentation navigation mismatch')
   page.keyboard.press('Escape');page.close()
  browser.close()
finally:server.terminate()
report={'viewports':[320,390,1440],'page_checks':results,'errors':errors};(Q/'browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'page_checks':len(results),'errors':errors},indent=2))
if errors:raise SystemExit(1)

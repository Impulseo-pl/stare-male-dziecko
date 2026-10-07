"""python _src/shots.py 1440|390 -> zrzuty podstron (serwer http.server 8125 z katalogu domowego)"""
import sys, os
from playwright.sync_api import sync_playwright
w=int(sys.argv[1]);h=900 if w>800 else 844
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'sh');os.makedirs(OUT,exist_ok=True)
P=['','tom-1/','czytaj/','o-serii/','dla-parafii-i-szkol/','koszyk/']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    ctx=b.new_context(viewport={'width':w,'height':h},is_mobile=w<800,has_touch=w<800)
    pg=ctx.new_page();errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    for path in P:
        if path=='koszyk/':
            pg.goto('http://127.0.0.1:8125/stare-male-dziecko/tom-1/?team=1&opcja=prezent',wait_until='networkidle')
            pg.fill('#g_email','zosia@example.com');pg.fill('#g_ded','Dla Zosi od babci');pg.click('#buy-form button[type=submit]')
            pg.wait_for_load_state('networkidle')
        else:
            pg.goto('http://127.0.0.1:8125/stare-male-dziecko/'+path+'?team=1',wait_until='networkidle')
        pg.wait_for_timeout(900)
        n=(path.strip('/') or 'home')
        pg.screenshot(path=f'{OUT}/{w}_{n}.png',full_page=True)
        pg.screenshot(path=f'{OUT}/{w}_{n}_top.png')
    print('ERR',errs)

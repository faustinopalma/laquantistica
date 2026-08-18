import uuid
from playwright.sync_api import sync_playwright
BASE="https://laquantistica.com"
SET="""([id,v])=>{const e=document.getElementById(id); e.value=v;
  e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true}));}"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(); errs=[]
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.set_viewport_size({"width":1400,"height":820})
    pg.goto("%s/it/lab-03b-deflessione-em.html?cb=%s"%(BASE,uuid.uuid4().hex), wait_until="networkidle")
    pg.wait_for_timeout(800)
    for Va in (1500, 2500, 4000):
        pg.evaluate(SET,["va",Va]); pg.evaluate(SET,["vd",150]); pg.wait_for_timeout(120)
        # si cerca il campo che riporta la macchia al centro: e' il bilanciamento v = E/B
        best=None
        for b in range(1,81):
            pg.evaluate(SET,["bb",b])
            y=pg.evaluate("()=>window.__lab.comp().y")
            if best is None or abs(y)<abs(best[1]): best=(b,y)
        pg.evaluate(SET,["bb",best[0]]); pg.wait_for_timeout(120)
        pg.evaluate("()=>document.getElementById('b1').click()"); pg.wait_for_timeout(200)
        bal=pg.evaluate("()=>window.__lab.bal")
        # tolto il campo elettrico resta solo B: si legge la deflessione
        pg.evaluate(SET,["vd",0]); pg.wait_for_timeout(150)
        pg.evaluate("()=>document.getElementById('b2').click()"); pg.wait_for_timeout(250)
        m=pg.evaluate("()=>window.__lab.misure")
        print("Va=%4d V  B bilanciante=%.2f mT (y=%.3f mm)  bilanciamento registrato: %s  misure: %d"
              %(Va,best[0]/100,best[1],bool(bal),len(m)))
        if m: print("            ultima e/m = %.4g C/kg"%(m[-1].get('em') or m[-1].get('qm') or float('nan')))
    m=pg.evaluate("()=>window.__lab.misure")
    print("\nchiavi di una misura:", list(m[-1].keys()) if m else "nessuna")
    vals=[x.get('em') or x.get('qm') for x in m if (x.get('em') or x.get('qm'))]
    if vals:
        med=sum(vals)/len(vals)
        print("media di %d determinazioni: %.4g C/kg  (accettato 1,7588e11, scarto %+.1f%%)"%(len(vals),med,(med/1.75882e11-1)*100))
    print("errori JS:", len(errs))
    br.close()

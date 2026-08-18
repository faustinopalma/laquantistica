import uuid
from playwright.sync_api import sync_playwright
BASE="https://laquantistica.com"
LABS=["lab-01-stern-gerlach","lab-02a-sg-angolo-relativo","lab-02b-sg-tre-macchine","lab-02c-sg-ricombinazione",
      "lab-02d-sg-sfasamento","lab-03a-corrente-vuoto","lab-03b-deflessione-em","lab-03c-millikan",
      "lab-04-diffrazione","lab-05-rutherford","lab-07-franck-hertz","lab-08-fotoelettrico","lab-09-spettri"]
SNAP="""() => { let s=(document.querySelector('.ctrlcol')||{}).innerText||'';
  s+=[...document.querySelectorAll('svg text')].map(e=>e.textContent).join('');
  for (const c of document.querySelectorAll('canvas')) { try {
    const d=c.getContext('2d').getImageData(0,0,Math.min(60,c.width),Math.min(60,c.height)).data;
    let h=0; for(let i=0;i<d.length;i+=97) h=(h*31+d[i])|0; s+='|'+h; } catch(e){ s+='|x'; } }
  return s; }"""
LISTA="() => [...document.querySelectorAll('button')].filter(b=>!b.closest('.con-head')).map(b=>(b.id||b.textContent.trim().slice(0,18)||b.className))"
PREMI="(i) => { const b=[...document.querySelectorAll('button')].filter(x=>!x.closest('.con-head'))[i]; b.click(); }"
with sync_playwright() as p:
    br=p.chromium.launch(); tot=0; morti=[]
    for lab in LABS:
        pg=br.new_page(); errs=[]
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.set_viewport_size({"width":1400,"height":820})
        pg.goto("%s/it/%s.html?cb=%s"%(BASE,lab,uuid.uuid4().hex), wait_until="networkidle")
        pg.wait_for_timeout(800)
        nomi=pg.evaluate(LISTA); vivi=0; inerti=[]
        for i,n in enumerate(nomi):
            prima=pg.evaluate(SNAP)
            try: pg.evaluate(PREMI,i)
            except Exception: pass
            pg.wait_for_timeout(260)
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(60)
            if pg.evaluate(SNAP)!=prima: vivi+=1
            else: inerti.append(n)
        print("%-26s pulsanti %2d, reagiscono %2d, errori JS %d %s"%(lab,len(nomi),vivi,len(errs),
              ("| senza effetto: "+", ".join(inerti[:6])) if inerti else ""))
        tot+=len(nomi)
        if errs: morti.append((lab,errs[0][:80]))
        pg.close()
    br.close()
print("\ntotale pulsanti provati:",tot)
for m in morti: print("ERRORE JS in",m)

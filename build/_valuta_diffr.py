"""Prova del laboratorio 04: la diffrazione si misura davvero?
uso: python build/_valuta_diffr.py [porta]   (server su publish/)"""
import sys, json
from playwright.sync_api import sync_playwright

PORT = sys.argv[1] if len(sys.argv) > 1 else '8099'
BASE = 'http://127.0.0.1:%s' % PORT
OUT = {}

JS_MISURA = """
() => {
  const l = window.__lab, PXMM = 208/45, out = [];
  l.setBeam(false);
  for (const V of [2500,3000,3500,4000,4500]) {
    const va = document.getElementById('va');
    va.value = V; va.dispatchEvent(new Event('input'));
    for (const p of [0,1]) {
      l.setPlane(p);
      // lettura "a occhio": il raggio vero dell'anello, portato in mm e arrotondato dal comando
      l.setRad(l.ringR(l.d) / PXMM);
      out.push({V: V, plane: p, d: l.d, r: l.rmm, delta: l.delta, lam: l.lamMis, plam: l.plam});
      l.record();
    }
  }
  return {righe: out, tab: l.rows.length,
          media: l.rows.reduce((a,b)=>a+b.pl,0)/l.rows.length,
          avgTxt: document.getElementById('rAvg').textContent,
          devTxt: document.getElementById('rDev').textContent};
}
"""

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for lang in ('it', 'en'):
        for reduce in (False, True):
            ctx = br.new_context(reduced_motion='reduce' if reduce else 'no-preference')
            pg = ctx.new_page()
            errs, bad = [], []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('response', lambda r: bad.append('%s %s' % (r.status, r.url)) if r.status >= 400 else None)
            pg.goto('%s/%s/lab-04-diffrazione.html?cb=%s%s' % (BASE, lang, lang, reduce), wait_until='networkidle')
            key = '%s%s' % (lang, '-reduce' if reduce else '')
            r = {'errori': errs, 'risorse4xx': bad}
            # il fascio deve restare acceso anche con reduced-motion
            r['fascio'] = pg.evaluate('() => window.__lab.beam')
            n0 = pg.evaluate('() => window.__lab.count')
            pg.evaluate('() => { for (let i=0;i<200;i++) window.__lab.hit(); }')
            r['accumula'] = pg.evaluate('() => window.__lab.count') - n0
            r['vmax'] = pg.eval_on_selector('#va', 'e => e.max')
            r['senza_nome'] = pg.eval_on_selector_all(
                'input,select', '''els => els.filter(e => !e.getAttribute('aria-label')).map(e => e.id)''')
            if not reduce:
                r['misura'] = pg.evaluate(JS_MISURA)
                txt = pg.inner_text('.ctrlcol')
                r['testo_pannello'] = txt
            OUT[key] = r
            ctx.close()
    br.close()

print(json.dumps(OUT, ensure_ascii=False, indent=1))

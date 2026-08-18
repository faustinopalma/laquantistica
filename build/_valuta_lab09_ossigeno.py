# -*- coding: utf-8 -*-
"""Prova di lab-09 dopo l'aggiunta dell'ossigeno: la misura di Rydberg
sull'idrogeno non deve cambiare, e le righe dell'ossigeno devono essere
raggiungibili e alle lunghezze d'onda giuste.
"""
import sys
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8099'
# righe attese, lette dalle tabelle NIST (aria), in nm
ATTESE = [391.20, 407.59, 441.49, 464.91, 615.68, 700.22, 777.19]
esito = 0


def prova(pg, lang):
    global esito
    errs, bad = [], []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('response', lambda r: bad.append('%d %s' % (r.status, r.url)) if r.status >= 400 else None)
    pg.set_viewport_size({'width': 1400, 'height': 820})
    pg.goto('%s/%s/lab-09-spettri.html' % (BASE, lang), wait_until='networkidle')
    pg.wait_for_timeout(400)

    idro = pg.evaluate("""() => {
      const l = window.__lab;
      l.setSource('h'); l.setGrating(600); l.setOrder(1);
      l.measureAll();
      return {R: l.rydberg, righe: l.rows.map(r => ({nm: r.nm, n: r.n, ref: r.ref}))};
    }""")
    oss = pg.evaluate("""() => {
      const l = window.__lab;
      l.setSource('o2');
      const vis = l.lines.filter(x => x.vis);
      l.measureAll();
      return {tot: l.lines.length, vis: vis.length,
              nm: l.lines.map(x => x.nm), mis: l.rows.map(r => r.nm)};
    }""")
    over = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")

    print('--- %s ---' % lang)
    print('  errori JS: %d   risorse 4xx: %d   sbordamento: %d px' % (len(errs), len(bad), over))
    print('  IDROGENO  R = %.4e m^-1   (accettata 1,0974e7, scarto %+.2f %%)'
          % (idro['R'], (idro['R'] / 1.0973731e7 - 1) * 100))
    print('  righe misurate: ' + ' · '.join('%.2f (n=%s)' % (r['nm'], r['n']) for r in idro['righe']))
    print('  OSSIGENO  righe raggiungibili: %d di cui visibili %d' % (oss['tot'], oss['vis']))
    print('  misurate: ' + ' · '.join('%.2f' % x for x in oss['mis'][:12]))
    for a in ATTESE:
        vicino = min((abs(x - a), x) for x in oss['nm']) if oss['nm'] else (99, 0)
        stato = 'ok' if vicino[0] < 0.02 else 'ASSENTE'
        print('    attesa %7.2f nm -> trovata %7.2f nm  %s' % (a, vicino[1], stato))
        if vicino[0] >= 0.02:
            esito = 1
    for e in errs:
        print('  ERRORE JS:', e)
    for b in bad:
        print('  RISORSA:', b)
    if errs or bad or over > 0:
        esito = 1
    if abs(idro['R'] / 1.0973731e7 - 1) > 0.003:
        print('  ATTENZIONE: la misura di Rydberg e cambiata')
        esito = 1

    pg.evaluate("() => window.__lab.setSource('o2')")
    pg.wait_for_timeout(200)
    pg.locator('#plot').screenshot(path='build/_lab09_%s_o2.png' % lang)

    for w, h in ((1024, 700), (844, 390)):
        pg.set_viewport_size({'width': w, 'height': h})
        pg.wait_for_timeout(250)
        o = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        print('  %dx%d: sbordamento %d px' % (w, h, o))
        if o > 0:
            esito = 1


with sync_playwright() as p:
    b = p.chromium.launch()
    for lang in ('it', 'en'):
        pg = b.new_page()
        prova(pg, lang)
        pg.close()
    b.close()

print('\nESITO:', 'ok' if esito == 0 else 'PROBLEMI')
sys.exit(esito)

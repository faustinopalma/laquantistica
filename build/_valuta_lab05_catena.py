# -*- coding: utf-8 -*-
"""Prova di lab-05 dopo l'aggiunta della catena di rivelazione.
Errori JS, risorse 4xx, sbordamenti, numeri della fisica invariati, ritaglio
dell'apparato per il controllo a occhio.
"""
import sys
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8099'
esito = 0


def prova(pg, lang):
    global esito
    errs, bad = [], []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('response', lambda r: bad.append('%d %s' % (r.status, r.url)) if r.status >= 400 else None)
    pg.set_viewport_size({'width': 1400, 'height': 820})
    pg.goto('%s/%s/lab-05-rutherford.html' % (BASE, lang), wait_until='networkidle')
    pg.wait_for_timeout(400)

    fisica = pg.evaluate("""() => {
      const l = window.__lab, out = {};
      out.beam = l.beam;
      for (const th of [5,10,15,20,25,30]) { l.setTheta(th); out['r'+th] = l.rate; }
      l.setTheta(0);
      return out;
    }""")
    over = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    senza_nome = pg.evaluate("""() => [...document.querySelectorAll('input,select,button')]
        .filter(e => !e.getAttribute('aria-label') && !e.textContent.trim() && !e.closest('.segrow')).length""")

    print('--- %s ---' % lang)
    print('  errori JS: %d   risorse 4xx: %d   sbordamento: %d px   comandi senza nome: %d'
          % (len(errs), len(bad), over, senza_nome))
    print('  fascio a 0: %.3f s^-1' % fisica['beam'])
    print('  ' + '  '.join('%d gradi: %.4f' % (th, fisica['r%d' % th]) for th in (5, 10, 15, 20, 25, 30)))
    print('  20 impulsi a 30 gradi: %.0f s' % (20 / fisica['r30']))
    for e in errs:
        print('  ERRORE JS:', e)
    for b in bad:
        print('  RISORSA:', b)
    if errs or bad or over > 0:
        esito = 1

    # conteggio e cronometro devono comparire nel disegno: si fa contare davvero
    pg.evaluate("() => { window.__lab.setTheta(0); window.__lab.start(); }")
    pg.wait_for_timeout(1200)
    stato = pg.evaluate("() => ({N: window.__lab.N, t: window.__lab.t})")
    print('  dopo 1,2 s di conteggio a 0 gradi: N = %d, Dt = %.1f s' % (stato['N'], stato['t']))
    if stato['N'] == 0:
        print('  ATTENZIONE: il contatore non e" salito (rAF fermo in headless?)')

    pg.locator('#stage').screenshot(path='build/_lab05_%s.png' % lang)
    pg.evaluate("() => { window.__lab.stop(); window.__lab.setTheta(120); }")
    pg.wait_for_timeout(300)
    pg.locator('#stage').screenshot(path='build/_lab05_%s_120.png' % lang)
    pg.evaluate("() => window.__lab.setTheta(0)")

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

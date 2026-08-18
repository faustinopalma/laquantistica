# -*- coding: utf-8 -*-
"""Dopo la deduplicazione di nfmt: sui tredici laboratori, in italiano e in inglese,
errori JS, risorse 4xx, presenza della nfmt condivisa e decimali col punto in italiano.
"""
import re
import sys
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8099'
LABS = ['lab-01-stern-gerlach', 'lab-02a-sg-angolo-relativo', 'lab-02b-sg-tre-macchine',
        'lab-02c-sg-ricombinazione', 'lab-02d-sg-sfasamento', 'lab-03a-corrente-vuoto',
        'lab-03b-deflessione-em', 'lab-03c-millikan', 'lab-04-diffrazione',
        'lab-05-rutherford', 'lab-07-franck-hertz', 'lab-08-fotoelettrico', 'lab-09-spettri']
PUNTO = re.compile(r'(?<![\w/])\d+\.\d+')
esito = 0

TESTO = ("() => document.body.innerText + ' | ' + "
         "[...document.querySelectorAll('svg text')].map(e => e.textContent).join(' ')")

with sync_playwright() as p:
    b = p.chromium.launch()
    for lab in LABS:
        riga = []
        for lang in ('it', 'en'):
            pg = b.new_page()
            errs, bad = [], []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('response', lambda r: bad.append('%d %s' % (r.status, r.url)) if r.status >= 400 else None)
            pg.set_viewport_size({'width': 1400, 'height': 820})
            pg.goto('%s/%s/%s.html' % (BASE, lang, lab), wait_until='networkidle')
            pg.wait_for_timeout(700)
            ok = pg.evaluate("() => typeof nfmt === 'function' && typeof dec === 'function'")
            over = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            hits = sorted(set(PUNTO.findall(pg.evaluate(TESTO)))) if lang == 'it' else []
            riga.append((lang, errs, bad, ok, over, hits))
            pg.close()
        for lang, errs, bad, ok, over, hits in riga:
            stato = 'errJS=%d 4xx=%d nfmt=%s ovf=%d' % (len(errs), len(bad), ok, over)
            print('%-26s %s  %s%s' % (lab, lang, stato,
                                      ('  PUNTI: ' + ', '.join(hits[:10])) if hits else ''))
            for e in errs[:2]:
                print('    ERRORE:', e)
            for x in bad[:2]:
                print('    RISORSA:', x)
            if errs or bad or not ok or over > 0 or hits:
                esito = 1
    b.close()

print('\nESITO:', 'ok' if esito == 0 else 'PROBLEMI')
sys.exit(esito)

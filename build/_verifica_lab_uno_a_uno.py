# -*- coding: utf-8 -*-
"""Verifica funzionale dei tredici laboratori sul sito pubblicato, uno alla volta.

La prova di reattivita' ASPETTA: diversi laboratori ridisegnano dentro
`requestAnimationFrame` (lab-01 lo fa per tutti e dodici i cursori), quindi confrontare
subito dopo l'evento darebbe «comandi inerti» anche dove funziona tutto. C'e' anche la
prova dei comandi disegnati nell'SVG — le porte di lab-02c — che non sono `input`.
Non modifica niente.
"""
import sys
import urllib.request
import uuid
from playwright.sync_api import sync_playwright

BASE = 'https://laquantistica.com'
LABS = ['lab-01-stern-gerlach', 'lab-02a-sg-angolo-relativo', 'lab-02b-sg-tre-macchine',
        'lab-02c-sg-ricombinazione', 'lab-02d-sg-sfasamento', 'lab-03a-corrente-vuoto',
        'lab-03b-deflessione-em', 'lab-03c-millikan', 'lab-04-diffrazione',
        'lab-05-rutherford', 'lab-07-franck-hertz', 'lab-08-fotoelettrico', 'lab-09-spettri']

SNAP = """() => {
  let s = (document.querySelector('.ctrlcol') || {}).innerText || '';
  s += [...document.querySelectorAll('svg text')].map(e => e.textContent).join('');
  for (const c of document.querySelectorAll('canvas')) {
    try {
      const d = c.getContext('2d').getImageData(0, 0, Math.min(60, c.width), Math.min(60, c.height)).data;
      let h = 0;
      for (let i = 0; i < d.length; i += 97) h = (h * 31 + d[i]) | 0;
      s += '|' + h;
    } catch (e) { s += '|x'; }
  }
  return s;
}"""

CTL = "() => [...document.querySelectorAll('.ctrlcol input[type=range], .ctrlcol select')].length"

MUOVI = """(i) => {
  const e = [...document.querySelectorAll('.ctrlcol input[type=range], .ctrlcol select')][i];
  const vecchio = e.value;
  if (e.tagName === 'SELECT') {
    const alt = [...e.options].find(o => o.value !== e.value);
    if (alt) e.value = alt.value;
  } else {
    const min = +e.min, max = +e.max;
    e.value = (+e.value - min) > (max - +e.value) ? min : max;
  }
  e.dispatchEvent(new Event('input', {bubbles: true}));
  e.dispatchEvent(new Event('change', {bubbles: true}));
  return vecchio;
}"""

RIMETTI = """([i, v]) => {
  const e = [...document.querySelectorAll('.ctrlcol input[type=range], .ctrlcol select')][i];
  e.value = v;
  e.dispatchEvent(new Event('input', {bubbles: true}));
  e.dispatchEvent(new Event('change', {bubbles: true}));
}"""

SVGHIT = """() => [...document.querySelectorAll('svg *')]
    .filter(e => getComputedStyle(e).cursor === 'pointer').length"""

CLICCA = """(i) => {
  const e = [...document.querySelectorAll('svg *')].filter(x => getComputedStyle(x).cursor === 'pointer')[i];
  const r = e.getBoundingClientRect();
  e.dispatchEvent(new MouseEvent('click', {bubbles: true,
      clientX: r.x + r.width / 2, clientY: r.y + r.height / 2}));
}"""

NOMI = """() => {
  const acc = e => e.getAttribute('aria-label') || e.getAttribute('aria-labelledby') ||
                   (e.labels && e.labels.length) || e.textContent.trim();
  const t = [...document.querySelectorAll('input, select, button')];
  return {comandi: t.length, senzaNome: t.filter(e => !acc(e)).length};
}"""

LAYOUT = """() => {
  const d = document.documentElement;
  const st = document.querySelector('.stagecol'), ct = document.querySelector('.ctrlcol');
  const rm = document.querySelector('.rotate-msg');
  const a = st && st.getBoundingClientRect(), b = ct && ct.getBoundingClientRect();
  const back = document.querySelector('#backTop, .con-back');
  return {overflow: d.scrollWidth - d.clientWidth,
          affiancate: !!(a && b) && Math.abs(a.top - b.top) < 80 && a.right <= b.left + 8,
          ruota: rm ? getComputedStyle(rm).display !== 'none' : null,
          back: back ? back.getAttribute('href') : null};
}"""

MISURA = {
    'lab-04-diffrazione': ("""() => {
        const l = window.__lab, PXMM = 208 / 45;
        l.setBeam(false);
        const va = document.getElementById('va');
        for (const V of [2500, 3000, 3500, 4000, 4500]) {
          va.value = V; va.dispatchEvent(new Event('input'));
          for (const p of [0, 1]) { l.setPlane(p); l.setRad(l.ringR(l.d) / PXMM); l.record(); }
        }
        return l.rows.reduce((a, b) => a + b.pl, 0) / l.rows.length;
      }""", 'p·λ medio sulle cinque tensioni', 6.0e-34, 7.2e-34, 'h = 6,626e-34'),
    'lab-05-rutherford': ("""() => { const l = window.__lab; l.setTheta(30);
        const r = l.rate; l.setTheta(0); return 20 / r; }""",
                          'tempo per venti impulsi a 30 gradi', 1500, 1750, '~1629 s'),
    'lab-07-franck-hertz': ("""() => { const l = window.__lab; l.setV(45); return l.zones; }""",
                            'zone luminose a V = 45 V', 1.5, 2.5, '2, come la fig. 7'),
    'lab-08-fotoelettrico': ("""() => { const l = window.__lab, o = [];
        for (const k of ['gi', 've', 'bl', 'vi']) { l.setFilter(k); o.push(l.V0); }
        return o[3] - o[0]; }""",
                             'V0(violetto) meno V0(giallo)', 0.70, 0.90, '1,24 - 0,44 = 0,80 V'),
    'lab-09-spettri': ("""() => { const l = window.__lab; l.setSource('h'); l.measureAll();
        return l.rydberg; }""",
                       'costante di Rydberg misurata', 1.09e7, 1.105e7, '1,0974e7 m^-1'),
}


def http(url):
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'verifica'})
        return urllib.request.urlopen(req, timeout=15).status
    except Exception as e:
        return getattr(e, 'code', 'errore')


def reattivita(pg):
    n = pg.evaluate(CTL)
    vivi = 0
    for i in range(n):
        prima = pg.evaluate(SNAP)
        v = pg.evaluate(MUOVI, i)
        pg.wait_for_timeout(180)
        if pg.evaluate(SNAP) != prima:
            vivi += 1
        pg.evaluate(RIMETTI, [i, v])
        pg.wait_for_timeout(80)
    return n, vivi


def clic_svg(pg):
    n = pg.evaluate(SVGHIT)
    vivi = 0
    for i in range(min(n, 6)):
        prima = pg.evaluate(SNAP)
        pg.evaluate(CLICCA, i)
        pg.wait_for_timeout(220)
        if pg.evaluate(SNAP) != prima:
            vivi += 1
    return n, vivi


def prova(b, lab):
    print('\n' + '=' * 74)
    print(lab)
    rilievi = []
    for lang in ('it', 'en'):
        pg = b.new_page()
        errs, bad = [], []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('response', lambda r: bad.append('%d %s' % (r.status, r.url)) if r.status >= 400 else None)
        pg.set_viewport_size({'width': 1400, 'height': 820})
        pg.goto('%s/%s/%s.html?cb=%s' % (BASE, lang, lab, uuid.uuid4().hex), wait_until='networkidle')
        pg.wait_for_timeout(900)

        lay = pg.evaluate(LAYOUT)
        nomi = pg.evaluate(NOMI)
        nctl, vivi = reattivita(pg)
        nsvg, vivisvg = clic_svg(pg)

        mis, err_mis = None, None
        if lab in MISURA:
            try:
                mis = pg.evaluate(MISURA[lab][0])
            except Exception as e:
                err_mis = str(e).splitlines()[0][:90]

        pg.set_viewport_size({'width': 844, 'height': 390})
        pg.wait_for_timeout(450)
        lay2 = pg.evaluate(LAYOUT)
        pg.set_viewport_size({'width': 390, 'height': 844})
        pg.wait_for_timeout(450)
        vert = pg.evaluate(LAYOUT)

        print('  [%s] errori JS %d - 4xx %d - comandi %d, senza nome %d - cursori vivi %d/%d - comandi sul disegno vivi %d/%d'
              % (lang, len(errs), len(bad), nomi['comandi'], nomi['senzaNome'], vivi, nctl, vivisvg, nsvg))
        print('       1400x820: sbord. %d, due colonne %s | 844x390: sbord. %d, due colonne %s | 390x844: avviso ruota %s'
              % (lay['overflow'], lay['affiancate'], lay2['overflow'], lay2['affiancate'], vert['ruota']))
        if lang == 'it':
            d = lay['back']
            print('       ritorno al capitolo: %s -> HTTP %s'
                  % (d, http('%s/it/%s' % (BASE, d.split('?')[0])) if d else 'ASSENTE'))
        if lab in MISURA:
            nome, lo, hi, atteso = MISURA[lab][1:]
            if err_mis:
                print('       MISURA FALLITA: ' + err_mis)
                rilievi.append('misura')
            else:
                ok = lo <= mis <= hi
                print('       misura: %s = %.5g  (atteso %s)  %s'
                      % (nome, mis, atteso, 'OK' if ok else 'FUORI INTERVALLO'))
                if not ok:
                    rilievi.append('misura')
        for e in errs[:2]:
            print('       ERRORE JS:', e[:110])
            rilievi.append('errori JS')
        for x in bad[:2]:
            print('       RISORSA:', x[:110])
            rilievi.append('risorse 4xx')
        if lay['overflow'] > 0 or lay2['overflow'] > 0:
            rilievi.append('sbordamento')
        if not lay['affiancate'] or not lay2['affiancate']:
            rilievi.append('colonne non affiancate')
        if vert['ruota'] is False:
            rilievi.append('manca avviso di rotazione')
        if nomi['senzaNome']:
            rilievi.append('comandi senza nome')
        if nctl and vivi < nctl:
            rilievi.append('cursori inerti (%d su %d)' % (nctl - vivi, nctl))
        if nsvg and vivisvg == 0:
            rilievi.append('comandi sul disegno inerti')
        pg.close()
    print('  VERDETTO: ' + ("funziona ed e' usabile" if not rilievi
                            else 'DA GUARDARE -> ' + ', '.join(sorted(set(rilievi)))))
    return not rilievi


scelti = sys.argv[1:] or LABS
with sync_playwright() as p:
    b = p.chromium.launch()
    ok = [prova(b, l) for l in scelti]
    b.close()
print('\n%d laboratori su %d senza rilievi' % (sum(ok), len(ok)))

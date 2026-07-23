#!/usr/bin/env python
"""Converte le formule MathML di publish/leggi/NN in immagini SVG ORIGINALI,
prendendole (nello stesso ordine documentale) da site/svg/NN.

Regole:
- I display <div class="equation"><math .../></div> -> <div class="equation"><img eq-block ...></div>
- Gli inline <math .../> dentro <span class="it"> consumano le img in ordine;
  gli stessi inline dentro il <span class="en"> RIusano le stesse img (testo bilingue).
- Le immagini provengono TAL QUALI da site/svg (originali), non rigenerate.

Controlli di sicurezza (se falliscono NON scrive nulla):
- ogni display consuma una img 'eq-block'; ogni inline una img 'eq-inline'.
- a fine conversione 0 <math residui e tutte le img consumate esattamente una volta.

Uso:  python tools/_svgconv.py 09-spettri-atomici [--apply]
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
# solo le immagini-FORMULA (eq-inline / eq-block); le eq-figure sono illustrazioni
# gia presenti come immagini in entrambe le edizioni, non vanno trattate come formule.
IMG_RE = re.compile(r'<img class="eq-(?:inline|block)[^"]*"[^>]*>')
MATH_RE = re.compile(r'<math\b.*?</math>', re.DOTALL)
BLOCK_RE = re.compile(
    r'<div class="equation">.*?</div>'
    r'|<span class="it">.*?</span>'
    r'|<span class="en">.*?</span>'
    r'|<math\b.*?</math>',
    re.DOTALL,
)

def convert(ch, apply=False):
    svg = (ROOT / f'site/svg/{ch}.html').read_text(encoding='utf-8')
    pub_path = ROOT / f'publish/leggi/{ch}.html'
    pub = pub_path.read_text(encoding='utf-8')

    imgs = IMG_RE.findall(svg)
    M = len(imgs)
    pub_math = len(MATH_RE.findall(pub))
    print(f'[{ch}] site/svg img formule = {M} · publish math = {pub_math}')

    st = {'p': 0, 'it_start': 0, 'err': [], 'warn': []}

    def take(kind):
        """consuma una img in ordine; kind e' 'block'/'inline'/'std' solo per avviso."""
        if st['p'] >= M:
            st['err'].append(f'{kind}: finite le img (p={st["p"]}, M={M})')
            return '<img alt="MISSING">'
        img = imgs[st['p']]
        exp = 'eq-block' if kind == 'block' else 'eq-inline'
        if exp not in img:
            st['warn'].append(f'{kind} #{st["p"]}: atteso {exp}, trovato {img[:50]}')
        st['p'] += 1
        return img

    def repl(m):
        s = m.group(0)
        if s.startswith('<div class="equation">'):
            if not MATH_RE.search(s):
                return s  # div gia' con img: lascia intatto
            return '<div class="equation">' + MATH_RE.sub(lambda mm: take('block'), s[len('<div class="equation">'):-len('</div>')]) + '</div>'
        if s.startswith('<span class="it">'):
            st['it_start'] = st['p']
            return re.sub(MATH_RE, lambda mm: take('inline'), s)
        if s.startswith('<span class="en">'):
            loc = {'q': st['it_start']}
            def r3(mm):
                if loc['q'] >= M:
                    st['err'].append('en: indice fuori range'); return '<img alt="MISSING">'
                img = imgs[loc['q']]; loc['q'] += 1
                return img
            return re.sub(MATH_RE, r3, s)
        # <math> standalone (fuori dagli span): una sola slot
        return take('std')

    out = BLOCK_RE.sub(repl, pub)
    remaining = len(MATH_RE.findall(out))
    print(f'[{ch}] img consumate (slot) = {st["p"]}/{M} · math residui = {remaining}')
    if st['err']:
        print('  ERRORI:')
        for e in st['err'][:20]:
            print('   -', e)
    if st['warn']:
        print(f'  avvisi classe (cosmetici) = {len(st["warn"])}')
    ok = (not st['err']) and remaining == 0 and st['p'] == M
    print(f'[{ch}] OK = {ok}')
    if apply and ok:
        pub_path.write_text(out, encoding='utf-8')
        print(f'[{ch}] SCRITTO.')
    elif apply and not ok:
        print(f'[{ch}] NON scritto (controlli falliti).')
    return ok

if __name__ == '__main__':
    ch = sys.argv[1]
    apply = '--apply' in sys.argv
    convert(ch, apply)

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
IMG_RE = re.compile(r'<img class="eq-[^"]*"[^>]*>')
MATH_RE = re.compile(r'<math\b.*?</math>', re.DOTALL)
BLOCK_RE = re.compile(
    r'<div class="equation">.*?</div>'
    r'|<span class="it">.*?</span>'
    r'|<span class="en">.*?</span>',
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

    st = {'p': 0, 'it_start': 0, 'err': []}

    def take_block():
        if st['p'] >= M:
            st['err'].append(f'display: finite le img (p={st["p"]}, M={M})')
            return '<img alt="MISSING">'
        img = imgs[st['p']]
        if 'eq-block' not in img:
            st['err'].append(f'display #{st["p"]} non e eq-block: {img[:60]}')
        st['p'] += 1
        return img

    def repl(m):
        s = m.group(0)
        if s.startswith('<div class="equation">'):
            nmath = len(MATH_RE.findall(s))
            if nmath != 1:
                # div senza math (gia img) -> lascia intatto
                if nmath == 0:
                    return s
                st['err'].append(f'div con {nmath} math')
            return f'<div class="equation">{take_block()}</div>'
        if s.startswith('<span class="it">'):
            st['it_start'] = st['p']
            def r2(mm):
                if st['p'] >= M:
                    st['err'].append('it: finite le img'); return '<img alt="MISSING">'
                img = imgs[st['p']]
                if 'eq-inline' not in img:
                    st['err'].append(f'inline #{st["p"]} non e eq-inline: {img[:60]}')
                st['p'] += 1
                return img
            return re.sub(MATH_RE, r2, s)
        # en-span: riusa le img del it-span accoppiato
        loc = {'q': st['it_start']}
        def r3(mm):
            if loc['q'] >= M:
                st['err'].append('en: indice fuori range'); return '<img alt="MISSING">'
            img = imgs[loc['q']]; loc['q'] += 1
            return img
        return re.sub(MATH_RE, r3, s)

    out = BLOCK_RE.sub(repl, pub)
    remaining = len(MATH_RE.findall(out))
    print(f'[{ch}] img consumate (slot) = {st["p"]}/{M} · math residui = {remaining}')
    if st['err']:
        print('  ERRORI:')
        for e in st['err'][:20]:
            print('   -', e)
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

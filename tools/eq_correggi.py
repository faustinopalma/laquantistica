"""Corregge nei data-tex i difetti lasciati dalla conversione da Word.

Tre correzioni, tutte sul LaTeX sorgente; il disegno si rigenera dopo con
katex_apply.py.

1. `\\{\\begin{...}` diventa `\\left\\{\\begin{...}...\\end{...}\\right.`, cosi' la
   graffa cresce fino ad abbracciare le righe invece di restare alta come una
   lettera. Trova la chiusura corrispondente contando gli annidamenti.
2. Le parole scritte lettera per lettera (`\\mathrm{I}\\mathrm{m}`) tornano
   parole: `\\operatorname{}` per le funzioni, `\\text{}` per il resto.
3. `come` dentro la versione inglese diventa `as`.

    python tools/eq_correggi.py                  # anteprima
    python tools/eq_correggi.py --write          # applica
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

FUNZIONI = {'Im', 'Re', 'sin', 'cos', 'tan', 'log', 'exp', 'max', 'min', 'det'}
APERTE = {'{': '\\{', '[': '[', '(': '(', '|': '|'}
CHIUSE = {'{': '\\}', '[': ']', '(': ')', '|': '|'}

SPEZZATA = re.compile(r'(?:\\mathrm\{([a-zA-Z])\}){2,}')
GRUPPO = re.compile(r'((?:\\mathrm\{[a-zA-Z]\}){2,})')
FISSA = re.compile(r'(?<!\\left)\\([{[(|])(\\begin\{(gathered|aligned|array|matrix)\})')


def unisci_parole(tex: str) -> tuple[str, list[str]]:
    """\\mathrm{I}\\mathrm{m} -> \\operatorname{Im} (o \\text{...})."""
    cambi = []

    def sost(m: re.Match) -> str:
        parola = ''.join(re.findall(r'\\mathrm\{([a-zA-Z])\}', m.group(1)))
        nuovo = (f'\\operatorname{{{parola}}}' if parola in FUNZIONI
                 else f'\\text{{{parola}}}')
        cambi.append(f'{parola}')
        return nuovo

    return GRUPPO.sub(sost, tex), cambi


def chiudi_parentesi(tex: str) -> tuple[str, int]:
    """Rende elastica la parentesi che apre un blocco su piu' righe."""
    fatti = 0
    while True:
        m = FISSA.search(tex)
        if not m:
            break
        simbolo, ambiente = m.group(1), m.group(3)
        # cerco il \end che chiude QUESTO ambiente, contando gli annidamenti
        i, livello = m.end(), 1
        fine = None
        for t in re.finditer(r'\\(begin|end)\{' + ambiente + r'\}', tex[m.end():]):
            livello += 1 if t.group(1) == 'begin' else -1
            if livello == 0:
                fine = m.end() + t.end()
                break
        if fine is None:
            break
        tex = (tex[:m.start()] + '\\left' + APERTE[simbolo] + m.group(2)
               + tex[m.end():fine] + '\\right.' + tex[fine:])
        fatti += 1
    return tex, fatti


def correggi(tex: str, inglese: bool) -> tuple[str, list[str]]:
    note = []
    nuovo, parole = unisci_parole(tex)
    if parole:
        note.append('parole: ' + ', '.join(sorted(set(parole))))
    if inglese:
        prima = nuovo
        nuovo = re.sub(r'\\text\{come\}', r'\\text{as}', nuovo)
        nuovo = re.sub(r'\\text\{con\}', r'\\text{with}', nuovo)
        if nuovo != prima:
            note.append('tradotta parola italiana')
    nuovo, n = chiudi_parentesi(nuovo)
    if n:
        note.append(f'parentesi elastiche: {n}')
    return nuovo, note


def lavora(path: Path, write: bool) -> int:
    src = path.read_text(encoding='utf-8')
    pezzi, pos, tocchi = [], 0, 0
    for m in re.finditer(r'data-tex="([^"]*)"', src):
        tex = html.unescape(m.group(1))
        prima = src[max(0, m.start() - 4000):m.start()]
        aperture = re.findall(r'<span class="(it|en)"', prima)
        inglese = (aperture[-1] if aperture else '') == 'en'

        nuovo, note = correggi(tex, inglese)
        if nuovo == tex:
            continue
        tocchi += 1
        riga = src[:m.start()].count('\n') + 1
        print(f'  {path.name} riga {riga}: {"; ".join(note)}')
        pezzi.append(src[pos:m.start(1)])
        pezzi.append(html.escape(nuovo, quote=True))
        pos = m.end(1)
    if tocchi and write:
        pezzi.append(src[pos:])
        path.write_text(''.join(pezzi), encoding='utf-8', newline='')
    return tocchi


if __name__ == '__main__':
    write = '--write' in sys.argv
    tot = 0
    for p in sorted(Path('publish').rglob('*.html')):
        tot += lavora(p, write)
    print(f'\n{tot} formule {"corrette" if write else "da correggere"}')

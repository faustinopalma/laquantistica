"""Rimette in ordine due formule dove la prosa aveva invaso l'allineamento.

Nel capitolo 2 le quattro proprieta' del prodotto scalare erano state schiacciate
in un unico blocco, con il primo membro di una proprieta' in coda alla riga
precedente e il secondo membro sulla riga dopo: leggendole si vedeva
`⟨α|β⟩` staccato dal suo `=⟨β|α⟩*`. Ora ogni proprieta' sta su una riga e le due
che sono uguaglianze si allineano sul segno di uguale.

Nel capitolo 5 la parola «Sostituendo» occupava la colonna di sinistra, quella
delle formule, e mandava fuori asse tutta la catena. Passa nella colonna delle
annotazioni, a destra, dove per convenzione si scrivono i passaggi.

    python tools/eq_prosa.py           # anteprima
    python tools/eq_prosa.py --write
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

# (pagina, LaTeX da sostituire, LaTeX nuovo)
CORREZIONI: list[tuple[str, str, str]] = [
    ('02-stern-gerlach-cascata.html',
     '\\begin{aligned}\n'
     '\\langle\\alpha|\\alpha\\rangle\\text{ è reale ed è }\\geq0\\ '
     '\\langle\\alpha|\\alpha\\rangle & =0\\text{ se e solo se }|\\alpha\\rangle'
     '\\text{ è il vettore nullo }\\ \\langle\\alpha|\\beta\\rangle \\\\\n'
     '& =\\langle\\beta|\\alpha\\rangle^*\\ \\langle\\alpha|\\beta_1+\\beta_2\\rangle \\\\\n'
     '& =\\langle\\alpha|\\beta_1\\rangle+\\langle\\alpha|\\beta_2\\rangle\n'
     '\\end{aligned}',
     '\\begin{aligned}\n'
     '& \\langle\\alpha|\\alpha\\rangle\\text{ è reale ed è }\\geq0 \\\\\n'
     '& \\langle\\alpha|\\alpha\\rangle=0\\text{ se e solo se }|\\alpha\\rangle'
     '\\text{ è il vettore nullo} \\\\\n'
     '\\langle\\alpha|\\beta\\rangle & =\\langle\\beta|\\alpha\\rangle^* \\\\\n'
     '\\langle\\alpha|\\beta_1+\\beta_2\\rangle & '
     '=\\langle\\alpha|\\beta_1\\rangle+\\langle\\alpha|\\beta_2\\rangle\n'
     '\\end{aligned}'),

    ('02-stern-gerlach-cascata.html',
     '\\begin{aligned}\n'
     '\\langle\\alpha|\\alpha\\rangle\\text{ is real and is }\\geq0\\ '
     '\\langle\\alpha|\\alpha\\rangle & =0\\text{ if and only if }|\\alpha\\rangle'
     '\\text{ is the null vector }\\ \\langle\\alpha|\\beta\\rangle \\\\\n'
     '& =\\langle\\beta|\\alpha\\rangle^*\\ \\langle\\alpha|\\beta_1+\\beta_2\\rangle \\\\\n'
     '& =\\langle\\alpha|\\beta_1\\rangle+\\langle\\alpha|\\beta_2\\rangle\n'
     '\\end{aligned}',
     '\\begin{aligned}\n'
     '& \\langle\\alpha|\\alpha\\rangle\\text{ is real and is }\\geq0 \\\\\n'
     '& \\langle\\alpha|\\alpha\\rangle=0\\text{ if and only if }|\\alpha\\rangle'
     '\\text{ is the null vector} \\\\\n'
     '\\langle\\alpha|\\beta\\rangle & =\\langle\\beta|\\alpha\\rangle^* \\\\\n'
     '\\langle\\alpha|\\beta_1+\\beta_2\\rangle & '
     '=\\langle\\alpha|\\beta_1\\rangle+\\langle\\alpha|\\beta_2\\rangle\n'
     '\\end{aligned}'),

    ('05-rutherford.html',
     '\\begin{aligned}\n'
     '\\Leftrightarrow\\nabla^2\\psi+\\frac{2m\\omega}{\\hbar}\\psi & '
     '=\\frac{2mq}{\\hbar^2}V\\psi\\Leftrightarrow \\\\\n'
     '\\text{Sostituendo }\\omega & =\\frac{\\hbar k^2}{2m}\\Leftrightarrow \\\\\n'
     '\\nabla^2\\psi+k^2\\psi & =\\frac{2mq}{\\hbar^2}V\\psi\n'
     '\\end{aligned}',
     '\\begin{aligned}\n'
     '\\Leftrightarrow\\nabla^2\\psi+\\frac{2m\\omega}{\\hbar}\\psi & '
     '=\\frac{2mq}{\\hbar^2}V\\psi \\\\\n'
     '\\nabla^2\\psi+k^2\\psi & =\\frac{2mq}{\\hbar^2}V\\psi '
     '&& \\text{con }\\omega=\\frac{\\hbar k^2}{2m}\n'
     '\\end{aligned}'),
    ('05-rutherford.html',
     '\\begin{aligned}\n'
     '\\Leftrightarrow\\nabla^2\\psi+\\frac{2m\\omega}{\\hbar}\\psi & '
     '=\\frac{2mq}{\\hbar^2}V\\psi\\Leftrightarrow \\\\\n'
     '\\text{Substituting }\\omega & =\\frac{\\hbar k^2}{2m}\\Leftrightarrow \\\\\n'
     '\\nabla^2\\psi+k^2\\psi & =\\frac{2mq}{\\hbar^2}V\\psi\n'
     '\\end{aligned}',
     '\\begin{aligned}\n'
     '\\Leftrightarrow\\nabla^2\\psi+\\frac{2m\\omega}{\\hbar}\\psi & '
     '=\\frac{2mq}{\\hbar^2}V\\psi \\\\\n'
     '\\nabla^2\\psi+k^2\\psi & =\\frac{2mq}{\\hbar^2}V\\psi '
     '&& \\text{with }\\omega=\\frac{\\hbar k^2}{2m}\n'
     '\\end{aligned}'),
]


def lavora(write: bool) -> int:
    fatti = 0
    for nome, vecchio, nuovo in CORREZIONI:
        p = Path('publish') / nome
        src = p.read_text(encoding='utf-8')
        v = html.escape(vecchio, quote=True)
        if v not in src:
            print(f'  {nome}: NON TROVATA -> {vecchio.splitlines()[0][:60]}')
            continue
        quante = src.count(v)
        if write:
            p.write_text(src.replace(v, html.escape(nuovo, quote=True)),
                         encoding='utf-8', newline='')
        print(f'  {nome}: {quante} occorrenza/e')
        fatti += quante
    return fatti


if __name__ == '__main__':
    write = '--write' in sys.argv
    n = lavora(write)
    print(f'\n{n} sostituzioni [{"scritte" if write else "anteprima"}]')

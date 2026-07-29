"""Separa il testo dalle formule nei punti in cui la prosa era finita dentro.

Non e' uno strumento generico: contiene l'elenco esatto dei punti concordati e li
sostituisce verificando che ognuno compaia il numero di volte previsto. Se un
conteggio non torna si ferma senza scrivere nulla.

Il testo nuovo si scrive con \\( ... \\) per le formule: le trasforma in vere
formule (data-tex + MathML) la stessa funzione usata dallo strumento di modifica.

    python tools/split_text_math.py            # anteprima
    python tools/split_text_math.py --write
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from edit_server import PUBLISH, expand_inline_tex   # noqa: E402


def eq(tex: str) -> str:
    """Espressione regolare che cattura lo <span> di una formula dato il suo LaTeX."""
    return (r'<span[^>]*data-tex="' + re.escape(html.escape(tex, quote=True))
            + r'"[^>]*>.*?</span>')


# --- capitolo 2 ---------------------------------------------------------------

ORTO_IT = r'\langle\alpha|\beta\rangle=0\Leftrightarrow\text{sono ortogonali}'
ORTO_EN = r'\langle\alpha|\beta\rangle=0\Leftrightarrow\text{they are orthogonal}'
NULLO_IT = '\\langle\\alpha_1|\\alpha_1\\rangle=0\\Rightarrow|\\alpha_1\\rangle\\text{ è nullo}'
NULLO_EN = r'\langle\alpha_1|\alpha_1\rangle=0\Rightarrow|\alpha_1\rangle\text{ is null}'

# --- capitolo 6 ---------------------------------------------------------------

ORTO6 = ('\\begin{aligned}\n'
         "|\\langle{\\overline{g}}_1\\cdots{\\overline{g}}_n|{\\overline{g}}_1'"
         "\\cdots{\\overline{g}}_n'\\rangle|^2 & =0\\Leftrightarrow \\\\\n"
         "\\langle{\\overline{g}}_1\\cdots{\\overline{g}}_n|{\\overline{g}}_1'"
         "\\cdots{\\overline{g}}_n'\\rangle & =0\\Leftrightarrow \\\\\n"
         '\\text{%s}. &\n'
         '\\end{aligned}')
ORTO6_NEW = ('\\begin{aligned}\n'
             "|\\langle{\\overline{g}}_1\\cdots{\\overline{g}}_n|{\\overline{g}}_1'"
             "\\cdots{\\overline{g}}_n'\\rangle|^2 & =0\\Leftrightarrow \\\\\n"
             "\\langle{\\overline{g}}_1\\cdots{\\overline{g}}_n|{\\overline{g}}_1'"
             "\\cdots{\\overline{g}}_n'\\rangle & =0\n"
             '\\end{aligned}')

CONG_IT = r'\overline{x},\overline{y}\ \text{e}\ \overline{z}'
CONG_EN = r'\overline{x},\overline{y}\ \text{and}\ \overline{z}'

# Gia' applicate (commit 2e04ef7): restano qui come traccia di cosa e' stato fatto.
DONE = [
    ('02-stern-gerlach-cascata.html', 1, eq(ORTO_IT),
     r'\(\langle\alpha|\beta\rangle=0\) ⇔ sono ortogonali'),
    ('02-stern-gerlach-cascata.html', 1, eq(ORTO_EN),
     r'\(\langle\alpha|\beta\rangle=0\) ⇔ they are orthogonal'),

    ('02-stern-gerlach-cascata.html', 1, eq(NULLO_IT),
     r'\(\langle\alpha_1|\alpha_1\rangle=0\Rightarrow|\alpha_1\rangle\) è nullo'),
    ('02-stern-gerlach-cascata.html', 1, eq(NULLO_EN),
     r'\(\langle\alpha_1|\alpha_1\rangle=0\Rightarrow|\alpha_1\rangle\) is null'),

    ('06-ulteriori-sviluppi.html', 1, eq(ORTO6 % 'sono ortogonali'),
     '\\[' + ORTO6_NEW + '\\] ⇔ sono ortogonali.'),
    ('06-ulteriori-sviluppi.html', 1, eq(ORTO6 % 'are orthogonal'),
     '\\[' + ORTO6_NEW + '\\] ⇔ are orthogonal.'),

    # la congiunzione dentro la formula: la coppia it/en compare due volte
    # (una nel paragrafo italiano, una in quello inglese) ed e' identica
    ('06-ulteriori-sviluppi.html', 2,
     r'<span class="it">' + eq(CONG_IT) + r'</span><span class="en">' + eq(CONG_EN) + r'</span>',
     '<span class="it">\\(\\overline{x},\\overline{y}\\) e \\(\\overline{z}\\)</span>'
     '<span class="en">\\(\\overline{x},\\overline{y}\\) and \\(\\overline{z}\\)</span>'),
]

# --- congiunzioni travestite da simbolo ---------------------------------------
# Qui la "e" non era \text{e} ma un identificatore matematico: per il file era la
# lettera e, indistinguibile dal numero di Nepero. Per questo veniva composta in
# corsivo, e per questo la stessa formula serviva entrambe le lingue — cioe' la
# versione inglese mostrava la congiunzione italiana.

COS_SIN = (r'\cos^2\frac{\vartheta_2-\vartheta_1}{2}\ e\ '
           r'\sin^2\frac{\vartheta_2-\vartheta_1}{2}')
# le stesse congiunzioni ma attaccate, senza spaziatura: sfuggono a occhio
COS_SIN_1 = r'\cos^2\frac{\vartheta}{2}e\sin^2\frac{\vartheta}{2}'
COS_SIN_3 = (r'\cos^2\frac{\vartheta_3-\vartheta_2}{2}e'
             r'\sin^2\frac{\vartheta_3-\vartheta_2}{2}')
IT_A = 'proporzionali ai termini '
EN_A = 'proportional to the terms '
XYZ = r'\overline{x},\overline{y}\ e\ \overline{z}'
ANALOG = (r'P_x=-i\hbar D_x\equiv-i\hbar\frac{\partial}{\partial x},'
          r'\ analogamente\ per\ y\ e\ z')


def anchored(text: str, tex: str):
    return re.escape(text) + eq(tex)


EDITS = [
    # (pagina, quante volte, espressione da cercare, testo nuovo)
    ('02-stern-gerlach-cascata.html', 1, anchored('proporzionali ai termini ', COS_SIN),
     r'proporzionali ai termini \(\cos^2\frac{\vartheta_2-\vartheta_1}{2}\) e '
     r'\(\sin^2\frac{\vartheta_2-\vartheta_1}{2}\)'),
    ('02-stern-gerlach-cascata.html', 1, anchored('proportional to the terms ', COS_SIN),
     r'proportional to the terms \(\cos^2\frac{\vartheta_2-\vartheta_1}{2}\) and '
     r'\(\sin^2\frac{\vartheta_2-\vartheta_1}{2}\)'),

    ('06-ulteriori-sviluppi.html', 1, anchored('una terna di valori ', XYZ),
     r'una terna di valori \(\overline{x},\overline{y}\) e \(\overline{z}\)'),
    ('06-ulteriori-sviluppi.html', 1, anchored('a triple of values ', XYZ),
     r'a triple of values \(\overline{x},\overline{y}\) and \(\overline{z}\)'),

    # frase italiana intera composta in corsivo matematico, uguale per le due lingue
    ('05-rutherford.html', 1, eq(ANALOG),
     r'\(P_x=-i\hbar D_x\equiv-i\hbar\frac{\partial}{\partial x}\)'
     r'<span class="it">, analogamente per \(y\) e \(z\)</span>'
     r'<span class="en">, similarly for \(y\) and \(z\)</span>'),

    ('02-stern-gerlach-cascata.html', 1, anchored(IT_A, COS_SIN_1),
     IT_A + r'\(\cos^2\frac{\vartheta}{2}\) e \(\sin^2\frac{\vartheta}{2}\)'),
    ('02-stern-gerlach-cascata.html', 1, anchored(EN_A, COS_SIN_1),
     EN_A + r'\(\cos^2\frac{\vartheta}{2}\) and \(\sin^2\frac{\vartheta}{2}\)'),

    ('02-stern-gerlach-cascata.html', 1, anchored(IT_A, COS_SIN_3),
     IT_A + r'\(\cos^2\frac{\vartheta_3-\vartheta_2}{2}\) e '
            r'\(\sin^2\frac{\vartheta_3-\vartheta_2}{2}\)'),
    ('02-stern-gerlach-cascata.html', 1, anchored(EN_A, COS_SIN_3),
     EN_A + r'\(\cos^2\frac{\vartheta_3-\vartheta_2}{2}\) and '
            r'\(\sin^2\frac{\vartheta_3-\vartheta_2}{2}\)'),
]


def main() -> None:
    write = '--write' in sys.argv
    changed: dict[str, str] = {}
    for name, times, pattern, new in EDITS:
        src = changed.get(name) or (PUBLISH / name).read_text(encoding='utf-8')
        hits = list(re.finditer(pattern, src, re.S))
        mark = 'OK ' if len(hits) == times else 'NO '
        print(f'{mark}{name}: {len(hits)} occorrenze (attese {times})')
        if len(hits) != times:
            print('    interrotto: nessun file e\' stato scritto')
            return
        body = expand_inline_tex(new)
        # eq-axis regola l'allineamento verticale delle formule in linea con
        # frazioni: se c'era prima, deve restare
        if 'eq-axis' in hits[0].group(0):
            body = body.replace('class="eq-inline eq-mml"',
                                'class="eq-inline eq-axis eq-mml"')
        changed[name] = re.sub(pattern, lambda m: body, src, flags=re.S)
        print(f'    prima : {hits[0].group(0)[:110]}…')
        print(f'    dopo  : {body[:110]}…')

    if not write:
        print('\n(anteprima: usa --write per scrivere)')
        return
    for name, src in changed.items():
        (PUBLISH / name).write_text(src, encoding='utf-8')
        print(f'scritto {name}')


if __name__ == '__main__':
    main()

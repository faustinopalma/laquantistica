"""Rimette in ordine la sequenza dei fasori nel capitolo 2.

I disegni erano incastrati dentro i paragrafi come se fossero lettere, e finivano
prima della frase che li annuncia invece che dopo. Qui il discorso torna nella
sua sequenza naturale: prima si dice cosa si fa, poi si vede il disegno, e la
formula chiude il passaggio.

I disegni diventano immagini centrate su riga propria, senza numerazione, e le
due formule del modulo quadrato passano da dentro la frase a blocco.

    python tools/ch2_fasori.py           # anteprima
    python tools/ch2_fasori.py --write
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PAGINA = Path('publish/02-stern-gerlach-cascata.html')
BACKUP = Path('backups/katex')
NODE = Path('tools/katexgen/tex2katex.js')

INIZIO = '<p><span class="it">Ora facciamo i seguenti calcoli matematici.'
FINE = '<p><span class="it">A questo punto sembra abbastanza chiaro'

IMG = 'img/pandoc_ch2'

# (testo italiano, testo inglese, disegno che segue, misura del disegno)
PASSI = [
    ('Ora facciamo i seguenti calcoli matematici. Prendiamo due numeri nel campo '
     'complesso, ad esempio due volte il numero uno, 1 e 1, rappresentiamoli '
     'vettorialmente.',
     'Now let us make the following mathematical calculations. Let us take two '
     'numbers in the complex field, for example the number one twice, 1 and 1, '
     'and represent them as vectors.',
     'image21.svg', 'width:2.210in'),
    ('Ora sfasiamo il secondo numero moltiplicandolo per il fasore '
     '<em>e<sup>iϕ</sup></em>, abbiamo la coppia 1 e <em>e<sup>iϕ</sup></em>.',
     'Now we phase-shift the second number by multiplying it by the phasor '
     '<em>e<sup>iϕ</sup></em>, obtaining the pair 1 and <em>e<sup>iϕ</sup></em>.',
     'image22.svg', 'width:1.710in'),
    ('Sommiamo il risultato così ottenuto e prendiamone il modulo quadrato. '
     'Otteniamo il risultato:',
     'We add the result thus obtained and take its squared modulus. '
     'We obtain the result:',
     'image23.svg', 'width:4.113in'),
    ('__FORMULA1__', '__FORMULA1__', None, None),
    ('Ora ripetiamo il tutto partendo dai due numeri 1 e –1.',
     'Now we repeat everything starting from the two numbers 1 and –1.',
     'image25.svg', 'width:3.490in'),
    ('Sfasiamo il secondo numero di ϕ ottenendo 1 e -<em>e<sup>iϕ</sup></em>.',
     'We phase-shift the second number by ϕ, obtaining 1 and -<em>e<sup>iϕ</sup></em>.',
     'image26.svg', 'width:2.187in'),
    ('Sommiamo e prendiamone il modulo quadrato. Otteniamo il risultato:',
     'We add and take the squared modulus. We obtain the result:',
     'image27.svg', 'width:2.687in'),
    ('__FORMULA2__', '__FORMULA2__', None, None),
]

FORMULE = {
    '__FORMULA1__': r'{\left|1+e^{i\varphi}\right|}^2={\left(2\cos\frac{\varphi}{2}\right)}^2=4\cos^2\frac{\varphi}{2}',
    '__FORMULA2__': r'|1-e^{i\varphi}|^2={\left(2\sin\frac{\varphi}{2}\right)}^2=4\sin^2\frac{\varphi}{2}',
}


def genera(tex_list: list[str]) -> list[str]:
    payload = json.dumps([{'i': i, 'tex': t, 'display': True}
                          for i, t in enumerate(tex_list)])
    res = subprocess.run(['node', str(NODE)], input=payload,
                         capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip()[:200])
    out = [''] * len(tex_list)
    for row in json.loads(res.stdout):
        if row.get('err'):
            raise RuntimeError(row['err'])
        out[row['i']] = row['html']
    return out


def costruisci() -> str:
    chiavi = [k for k in FORMULE]
    reso = dict(zip(chiavi, genera([FORMULE[k] for k in chiavi])))
    righe = []
    for it, en, disegno, misura in PASSI:
        if it in FORMULE:
            tex = html.escape(FORMULE[it], quote=True)
            righe.append(f'<p class="equation"><span class="eq-mml eq-mml-block" '
                         f'data-tex="{tex}">{reso[it]}</span></p>')
            continue
        righe.append(f'<p><span class="it">{it}</span>'
                     f'<span class="en">{en}</span></p>')
        if disegno:
            righe.append(f'<p class="equation"><img class="eq-figure" '
                         f'src="{IMG}/{disegno}?v=2" style="{misura}" alt=""></p>')
    return '\n'.join(righe) + '\n'


if __name__ == '__main__':
    write = '--write' in sys.argv
    src = PAGINA.read_text(encoding='utf-8')
    a, b = src.find(INIZIO), src.find(FINE)
    if a < 0 or b < 0 or b <= a:
        sys.exit('confini del passaggio non trovati')
    nuovo = costruisci()
    print(f'sostituisco {b - a} caratteri con {len(nuovo)}')
    print(f'paragrafi: {nuovo.count("<p")}  disegni: {nuovo.count("<img")}  '
          f'formule: {nuovo.count("data-tex")}')
    if write:
        BACKUP.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PAGINA, BACKUP / f'fasori-{PAGINA.name}')
        PAGINA.write_text(src[:a] + nuovo + src[b:], encoding='utf-8', newline='')
        print('scritto')

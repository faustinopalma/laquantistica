"""Sostituisce le formule ancora servite come immagini con matematica vera.

Le immagini venivano dall'editor di equazioni della tesi originale: per un
lettore di schermo dicono soltanto "formula", non scalano col testo e usano un
carattere diverso da tutte le altre. Il LaTeX qui sotto e' stato trascritto
guardandole una per una, insieme alla frase che le ospita.

Le formule che contengono parole hanno due versioni, perche' il sito e' bilingue
e l'immagine, essendo una sola, mostrava l'italiano anche agli inglesi.

    python tools/eq_images_fix.py           # anteprima
    python tools/eq_images_fix.py --write
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BACKUP = Path('backups/katex')
NODE = Path('tools/katexgen/tex2katex.js')

SISTEMA_IT = (r'\left\{\begin{gathered}'
              r'\nabla^2\psi+k^2\psi=\frac{2mq}{\hbar^2}{TERMINE} \\'
              r'\text{con }\psi(x,y,z)\underset{z\to-\infty}{\longrightarrow}e^{ikz}'
              r'\end{gathered}\right.')
SISTEMA_EN = SISTEMA_IT.replace(r'\text{con }', r'\text{with }')

FLUSSO_IT = (r'F=\left(\begin{gathered}\text{Particelle per unità} \\ '
             r'\text{di tempo in }d\Omega\end{gathered}\right)\times'
             r'\frac{\left(\begin{gathered}\text{Angolo solido} \\ '
             r'\text{totale}\end{gathered}\right)}{d\Omega}')
FLUSSO_EN = (r'F=\left(\begin{gathered}\text{Particles per unit} \\ '
             r'\text{of time in }d\Omega\end{gathered}\right)\times'
             r'\frac{\left(\begin{gathered}\text{Total solid} \\ '
             r'\text{angle}\end{gathered}\right)}{d\Omega}')

MOMENTO = (r'\overline{L}=\overline{r}\wedge\overline{p}='
           r'\begin{vmatrix}\hat{\imath} & \hat{\jmath} & \hat{k} \\ '
           r'x & y & z \\ p_x & p_y & p_z\end{vmatrix}='
           r'\hat{\imath}(yp_z-zp_y)+\hat{\jmath}(zp_x-xp_z)+\hat{k}(xp_y-yp_x)')

RIGHE_IT = (r'\begin{array}{rcl}'
            r'\text{giallo} & \to 578\,nm & 5{,}19\cdot10^{14}\,Hz \\'
            r'\text{verde} & \to 545\,nm & 5{,}49\cdot10^{14}\,Hz \\'
            r'\text{blu} & \to 436\,nm & 6{,}88\cdot10^{14}\,Hz \\'
            r'\text{violetto} & \to 405\,nm & 7{,}41\cdot10^{14}\,Hz'
            r'\end{array}')
RIGHE_EN = (r'\begin{array}{rcl}'
            r'\text{yellow} & \to 578\,nm & 5.19\cdot10^{14}\,Hz \\'
            r'\text{green} & \to 545\,nm & 5.49\cdot10^{14}\,Hz \\'
            r'\text{blue} & \to 436\,nm & 6.88\cdot10^{14}\,Hz \\'
            r'\text{violet} & \to 405\,nm & 7.41\cdot10^{14}\,Hz'
            r'\end{array}')

# nome file -> (LaTeX italiano, LaTeX inglese o None se uguale, a blocco?)
TRASCRIZIONE: dict[str, tuple[str | None, str | None, bool]] = {
    # capitolo 4 — i simboli di coniugazione e trasposizione
    'obj056.svg': (r'({}^*)', None, False),
    'obj057.svg': (r'({}^t)', None, False),
    'obj077.svg': (r'v(x)\xrightarrow{\ D\ }\frac{d}{dx}v(x)', None, True),
    'obj206.svg': (r'+\infty', None, False),
    # capitolo 5
    'obj062.svg': (SISTEMA_IT.replace('{TERMINE}', 'V\\psi'),
                   SISTEMA_EN.replace('{TERMINE}', 'V\\psi'), True),
    'obj069.svg': (SISTEMA_IT.replace('{TERMINE}', 'V(r)e^{ikz}'),
                   SISTEMA_EN.replace('{TERMINE}', 'V(r)e^{ikz}'), True),
    'obj100.svg': (None, None, False),          # immagine vuota: si toglie
    'obj118.svg': (FLUSSO_IT, FLUSSO_EN, True),
    # capitolo 6
    'obj016.svg': (r'U(t_0\to t)', None, False),
    'obj040.svg': (r'\overline{g}_1\cdots\overline{g}_n', None, False),
    'obj064.svg': (r'g_1\cdots g_n', None, False),
    'obj071.svg': (r'\overline{g}_{k_1}\cdots\overline{g}_{k_n}', None, False),
    'obj103.svg': (r'p_x', None, False),
    'obj111.svg': (r'p_x', None, False),
    'obj139.svg': (r'p_x', None, False),
    'obj141.svg': (r'p_x', None, False),
    'obj148.svg': (r'G', None, False),
    'obj152.svg': (r'G', None, False),
    'obj166.svg': (r'p_x', None, False),
    'obj168.svg': (r'p_x', None, False),
    'obj173.svg': (r'p_x', None, False),
    'obj182.svg': (r'p_x', None, False),
    'obj197.svg': (MOMENTO, None, True),
    # capitolo 8
    'obj006.svg': (RIGHE_IT, RIGHE_EN, True),
    'obj010.svg': (r'\nu', None, False),
}

IMG = re.compile(r'<img[^>]*class="[^"]*eq-[^"]*"[^>]*src="img/eq_[^"?]*/(obj\d+\.svg)[^"]*"[^>]*>')


def genera(items: list[dict]) -> dict[int, str]:
    res = subprocess.run(['node', str(NODE)], input=json.dumps(items),
                         capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        raise RuntimeError(f'tex2katex.js: {res.stderr.strip()}')
    out = {}
    for row in json.loads(res.stdout):
        if row.get('err'):
            raise RuntimeError(f'[{row["i"]}]: {row["err"]}')
        out[row['i']] = row['html']
    return out


def lingua_di(src: str, pos: int) -> str:
    aperture = re.findall(r'<span class="(it|en)"', src[max(0, pos - 6000):pos])
    return aperture[-1] if aperture else 'it'


def convert(path: Path, write: bool) -> dict:
    src = path.read_text(encoding='utf-8')
    trovate = list(IMG.finditer(src))
    if not trovate:
        return {'sostituite': 0, 'tolte': 0}

    lavoro, sconosciute = [], []
    for m in trovate:
        nome = m.group(1)
        if nome not in TRASCRIZIONE:
            sconosciute.append(nome)
            continue
        it, en, blocco = TRASCRIZIONE[nome]
        if it is None:
            lavoro.append({'m': m, 'tex': None, 'blocco': blocco})
            continue
        tex = en if (en and lingua_di(src, m.start()) == 'en') else it
        lavoro.append({'m': m, 'tex': tex, 'blocco': blocco})

    if sconosciute:
        raise RuntimeError(f'{path.name}: immagini non trascritte: {set(sconosciute)}')

    da_rendere = [{'i': i, 'tex': w['tex'], 'display': w['blocco']}
                  for i, w in enumerate(lavoro) if w['tex']]
    reso = genera(da_rendere) if da_rendere else {}

    pezzi, pos, sost, tolte = [], 0, 0, 0
    for i, w in enumerate(lavoro):
        m = w['m']
        pezzi.append(src[pos:m.start()])
        if w['tex'] is None:
            tolte += 1
        else:
            classe = 'eq-mml eq-mml-block' if w['blocco'] else 'eq-inline eq-mml'
            attr = html.escape(w['tex'], quote=True)
            pezzi.append(f'<span class="{classe}" data-tex="{attr}">{reso[i]}</span>')
            sost += 1
        pos = m.end()
    pezzi.append(src[pos:])

    if write:
        BACKUP.mkdir(parents=True, exist_ok=True)
        if not (BACKUP / f'img-{path.name}').exists():
            shutil.copy2(path, BACKUP / f'img-{path.name}')
        path.write_text(''.join(pezzi), encoding='utf-8', newline='')
    return {'sostituite': sost, 'tolte': tolte}


if __name__ == '__main__':
    write = '--write' in sys.argv
    tot = {'sostituite': 0, 'tolte': 0}
    for p in sorted(Path('publish').glob('*.html')):
        e = convert(p, write)
        if e['sostituite'] or e['tolte']:
            print(f'{p.name:34} {e["sostituite"]:3} sostituite, {e["tolte"]} tolte')
            tot['sostituite'] += e['sostituite']
            tot['tolte'] += e['tolte']
    print(f'\ntotale: {tot["sostituite"]} sostituite, {tot["tolte"]} tolte '
          f'[{"scritto" if write else "anteprima"}]')

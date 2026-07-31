"""Rende bilingui le formule che contengono parole in lingua naturale.

Ogni formula diventa due elementi fratelli con la classe di lingua aggiunta a
quelle esistenti (NON un wrapper: i selettori CSS `.equation > .eq-mml-block`
devono continuare a valere). Il KaTeX viene rigenerato dal LaTeX con la catena
gia' in uso nel progetto.
"""
import html
import json
import pathlib
import re
import subprocess

RADICE = pathlib.Path('publish')

# offset -> (latex italiano, latex inglese). Solo le PAROLE cambiano.
LAVORO = {
    '04-diffrazione.html': {
        901382: (None, lambda s: s.replace(r'\text{Costante}', r'\text{Constant}')),
    },
    '05-rutherford.html': {
        434928: (lambda s: s.replace(r'\text{with }', r'\text{con }'), None),
        462609: (lambda s: s.replace(r'\text{with }', r'\text{con }'), None),
        965690: (None, lambda s: s.replace(r'\text{Effettiva}', r'\text{Effective}')
                                  .replace(r'\text{Unitaria}', r'\text{Unit}')),
        978191: (None, lambda s: s.replace(r'\text{Effettiva}', r'\text{Effective}')),
        991305: (lambda s: s.replace(r'\text{Particles per unit}', r'\text{Particelle per unità}')
                            .replace(r'\text{of time in }', r'\text{di tempo in }')
                            .replace(r'\text{Total solid}', r'\text{Angolo solido}')
                            .replace(r'\text{angle}', r'\text{totale}'), None),
        1013929: (None, lambda s: s.replace(r'\text{Particelle per unità di tempo in }',
                                            r'\text{Particles per unit of time in }')),
        1308445: (None, lambda s: s.replace(r'\text{Verificata}', r'\text{Verified}')),
    },
    '08-effetto-fotoelettrico.html': {
        33870: (lambda s: s.replace(r'\text{yellow}', r'\text{giallo}')
                           .replace(r'\text{green}', r'\text{verde}')
                           .replace(r'\text{blue}', r'\text{blu}')
                           .replace(r'\text{violet}', r'\text{violetto}'), None),
    },
}


def fine_elemento(t, apertura):
    """Fine dello <span> aperto in `apertura`, contando gli annidamenti."""
    i, prof = apertura, 0
    for m in re.finditer(r'<span\b|</span>', t[apertura:]):
        prof += 1 if m.group(0).startswith('<span') else -1
        if prof == 0:
            return apertura + m.end()
    raise ValueError('span non chiuso')


def rendi(coppie):
    """coppie: [(chiave, tex, display)] -> {chiave: html}"""
    dentro = [{'i': k, 'tex': tex, 'display': disp} for k, tex, disp in coppie]
    p = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                       input=json.dumps(dentro), capture_output=True, text=True, encoding='utf-8')
    if p.returncode != 0:
        raise SystemExit(f'katex fallito: {p.stderr[:400]}')
    fuori = {}
    for r in json.loads(p.stdout):
        if 'err' in r:
            raise SystemExit(f'LaTeX rifiutato ({r["i"]}): {r["err"]}')
        fuori[r['i']] = r['html']
    return fuori


for nome, bersagli in LAVORO.items():
    percorso = RADICE / nome
    t = percorso.read_text(encoding='utf-8')
    pezzi = []
    for off in sorted(bersagli, reverse=True):          # dal fondo: gli offset restano validi
        m = re.match(r'data-tex="([^"]*)"', t[off:])
        if not m:
            raise SystemExit(f'{nome}: nessun data-tex a {off}')
        tex = html.unescape(m.group(1))
        apertura = t.rfind('<span', 0, off)
        chiusura = fine_elemento(t, apertura)
        classi = re.search(r'class="([^"]*)"', t[apertura:off]).group(1)
        display = 'eq-mml-block' in classi

        f_it, f_en = bersagli[off]
        tex_it = f_it(tex) if f_it else tex
        tex_en = f_en(tex) if f_en else tex
        if tex_it == tex_en:
            raise SystemExit(f'{nome}@{off}: le due versioni sono identiche')

        resa = rendi([('it', tex_it, display), ('en', tex_en, display)])
        nuovo = ''
        for l, tx in (('it', tex_it), ('en', tex_en)):
            nuovo += (f'<span class="{classi} {l}" data-tex="{html.escape(tx, quote=True)}">'
                      f'{resa[l]}</span>')
        t = t[:apertura] + nuovo + t[chiusura:]
        pezzi.append(off)
    percorso.write_text(t, encoding='utf-8')
    print(f'{nome}: {len(pezzi)} formule rese bilingui')

print('fatto')

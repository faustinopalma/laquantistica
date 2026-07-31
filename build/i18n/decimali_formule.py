"""Separatori decimali nelle formule.

Per ogni formula che contiene una virgola decimale:
  - se sta in un contesto inglese  -> il separatore diventa il punto;
  - se sta in un contesto italiano -> la virgola diventa `{,}`, che in LaTeX e' il
    modo corretto di scrivere il separatore decimale: senza le graffe KaTeX la
    tratta come punteggiatura e le mette dopo uno spazio ("6, 6");
  - se e' condivisa fra le due lingue -> si sdoppia in due varianti.
Il KaTeX viene rigenerato dal LaTeX corretto.
"""
import html
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from split import Potatore  # noqa: E402

RADICE = pathlib.Path('sorgenti')
DECIMALE = re.compile(r'(?<=\d),(?=\d)')
PUNTO = re.compile(r'(?<![\d.])(\d+)\.(\d+)(?![\d.])')


def intervalli(testo, lingua):
    p = Potatore(testo, lingua)
    p.feed(testo)
    p.close()
    return sorted(p.intervalli)


def contesto(int_it, int_en, pos):
    for a, b in int_it:
        if a <= pos < b:
            return 'it'
    for a, b in int_en:
        if a <= pos < b:
            return 'en'
    return 'condiviso'


def contenitore(t, off):
    """Tag che porta il data-tex a `off`: e' quello che si apre subito prima.
    Non basta cercare `<span`: alcune formule stanno in <div class="equation">."""
    apertura = t.rfind('<', 0, off)
    m = re.match(r'<(\w+)', t[apertura:])
    if not m or t.find('>', apertura) < off:
        raise ValueError(f'contenitore non riconosciuto a {off}')
    return apertura, m.group(1)


def fine_elemento(t, apertura, tag):
    prof = 0
    for m in re.finditer(rf'<{tag}\b|</{tag}>', t[apertura:]):
        prof += 1 if not m.group(0).startswith('</') else -1
        if prof == 0:
            return apertura + m.end()
    raise ValueError(f'<{tag}> non chiuso')


def rendi(voci):
    p = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                       input=json.dumps(voci), capture_output=True, text=True, encoding='utf-8')
    if p.returncode != 0:
        raise SystemExit(f'katex fallito: {p.stderr[:300]}')
    out = {}
    for r in json.loads(p.stdout):
        if 'err' in r:
            raise SystemExit(f'LaTeX rifiutato ({r["i"]}): {r["err"]}')
        out[r['i']] = r['html']
    return out


def punto(tex):
    return PUNTO.sub(r'\1.\2', DECIMALE.sub('.', tex.replace('{,}', ',')))


def virgola_stretta(tex):
    return DECIMALE.sub('{,}', PUNTO.sub(r'\1{,}\2', tex))


totale = 0
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'data-tex' not in t or 'class="it"' not in t:
        continue
    int_it, int_en = intervalli(t, 'it'), intervalli(t, 'en')
    bersagli = []
    for m in re.finditer(r'data-tex="([^"]*)"', t):
        tex = html.unescape(m.group(1))
        if DECIMALE.search(tex) or PUNTO.search(tex):
            c = contesto(int_it, int_en, m.start())
            # gia' a posto: inglese col punto, italiano con {,}
            if c == 'en' and not DECIMALE.search(tex):
                continue
            if c == 'it' and not PUNTO.search(tex) and not DECIMALE.search(tex):
                continue
            bersagli.append((m.start(), tex, c))
    if not bersagli:
        continue

    fatti = 0
    for off, tex, ctx in reversed(bersagli):        # dal fondo: gli offset restano validi
        apertura, tag = contenitore(t, off)
        chiusura = fine_elemento(t, apertura, tag)
        classi = re.search(r'class="([^"]*)"', t[apertura:off]).group(1)
        display = 'eq-mml-block' in classi or tag == 'div'
        if ctx == 'en':
            resa = rendi([{'i': 'x', 'tex': punto(tex), 'display': display}])
            nuovo = (f'<{tag} class="{classi}" data-tex="{html.escape(punto(tex), quote=True)}">'
                     f'{resa["x"]}</{tag}>')
        elif ctx == 'it':
            resa = rendi([{'i': 'x', 'tex': virgola_stretta(tex), 'display': display}])
            nuovo = (f'<{tag} class="{classi}" '
                     f'data-tex="{html.escape(virgola_stretta(tex), quote=True)}">'
                     f'{resa["x"]}</{tag}>')
        else:
            resa = rendi([{'i': 'it', 'tex': virgola_stretta(tex), 'display': display},
                          {'i': 'en', 'tex': punto(tex), 'display': display}])
            nuovo = ''
            for l, tx in (('it', virgola_stretta(tex)), ('en', punto(tex))):
                nuovo += (f'<{tag} class="{classi} {l}" data-tex="{html.escape(tx, quote=True)}">'
                          f'{resa[l]}</{tag}>')
        t = t[:apertura] + nuovo + t[chiusura:]
        fatti += 1

    f.write_text(t, encoding='utf-8')
    conti = {c: sum(1 for _, _, x in bersagli if x == c) for c in ('it', 'en', 'condiviso')}
    print(f'{f.name}: {fatti} formule  (italiane {conti["it"]}, inglesi {conti["en"]}, '
          f'condivise {conti["condiviso"]})')
    totale += fatti

print(f'\ntotale formule sistemate: {totale}')

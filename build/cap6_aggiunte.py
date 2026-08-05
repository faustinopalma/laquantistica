"""Due aggiunte alla scheda 6: perche' l'autoket simultaneo di x e p_y esiste
e XP_y non ha problemi di ordinamento; la verifica dell'hermitianita' di G."""
import json
import subprocess
from pathlib import Path

P = Path('sorgenti/06-ulteriori-sviluppi.html')
righe = P.read_text(encoding='utf-8').split('\n')

TEX_G = "G^+=\\iint_{g'\\:\\xi}|g',\\xi\\rangle{g'}^*\\langle g',\\xi|\\:d\\xi\\:dg'=G"

r = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps([{'i': 0, 'tex': TEX_G, 'display': True}]),
                   capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    raise SystemExit(r.stderr)
reso = json.loads(r.stdout)[0]
if 'err' in reso:
    raise SystemExit(reso['err'])
esc = TEX_G.replace('&', '&amp;').replace("'", '&#x27;')
FORMULA_G = ('<div class="equation"><span class="eq-mml eq-mml-block" data-tex="%s">%s</span></div>'
             % (esc, reso['html']))

ORDINE = (
    '<p><span class="it">Questo autoket esiste perch\u00e9 <em>x</em> e <em>p<sub>y</sub></em> sono '
    'grandezze compatibili: \u00e8 proprio l\u2019esempio con cui si \u00e8 chiuso il paragrafo precedente. '
    'Dalla stessa commutazione discende un secondo fatto che ci servir\u00e0: essendo '
    '<em>XP<sub>y</sub></em>&nbsp;=&nbsp;<em>P<sub>y</sub>X</em>, il prodotto non dipende '
    'dall\u2019ordine dei fattori ed \u00e8 hermitiano, come dev\u2019essere l\u2019operatore di una grandezza '
    'fisica. Per <em>xp<sub>x</sub></em> non sarebbe stato vero n\u00e9 l\u2019uno n\u00e9 l\u2019altro, e la '
    'costruzione avrebbe richiesto un accorgimento in pi\u00f9.</span>'
    '<span class="en">This eigenket exists because <em>x</em> and <em>p<sub>y</sub></em> are '
    'compatible quantities: it is the very example with which the previous paragraph closed. '
    'From the same commutation a second fact follows, one we shall need: since '
    '<em>XP<sub>y</sub></em>&nbsp;=&nbsp;<em>P<sub>y</sub>X</em>, the product does not depend on '
    'the order of the factors and is hermitian, as the operator of a physical quantity must be. '
    'For <em>xp<sub>x</sub></em> neither of the two would have held, and the construction would '
    'have called for a further device.</span></p>')

HERMITIANO = (
    '<p><span class="it">L\u2019hermitianit\u00e0 si vede subito: coniugando e trasponendo l\u2019integrale '
    'si scambiano il bra e il ket e si coniuga l\u2019autovalore</span>'
    '<span class="en">Hermiticity is immediate: conjugating and transposing the integral swaps '
    'the bra and the ket and conjugates the eigenvalue</span></p>')

CHIUSURA = (
    '<p><span class="it">e l\u2019ultimo passaggio vale perch\u00e9 gli autovalori <em>g\u2019</em> sono '
    'numeri reali: sono i risultati di una misura.</span>'
    '<span class="en">and the last step holds because the eigenvalues <em>g\u2019</em> are real '
    'numbers: they are the results of a measurement.</span></p>')


def indice(chiave):
    trovate = [k for k, r in enumerate(righe) if chiave in r]
    assert len(trovate) == 1, f'{len(trovate)} righe con {chiave!r}'
    k = trovate[0]
    assert righe[k].startswith('<p>') and righe[k].endswith('</p>'), righe[k][:60]
    return k


# dal fondo verso l'alto, per non spostare gli indici
k = indice('stessi passi che abbiamo seguito per l')
righe[k + 1:k + 1] = [HERMITIANO, FORMULA_G, CHIUSURA]
print('aggiunta la verifica dell\u2019hermitianit\u00e0 di G')

k = indice('un autoket rappresentativo di un autostato simultaneo')
righe[k + 1:k + 1] = [ORDINE]
print('aggiunta la nota sull\u2019ordine dei fattori in XP_y')

s = '\n'.join(righe)
assert s.count('<span') == s.count('</span>')
P.write_text(s, encoding='utf-8', newline='')

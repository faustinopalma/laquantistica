"""Rimette sulla figura 2 della scheda 7 le scritte perse nella conversione dal DWG.

Sono tutti simboli e unita', uguali nelle due lingue: basta un solo file.
Il corpo passa per una transform perche' Chrome limita font-size a 10000px.
"""
from pathlib import Path

SORGENTE = Path('publish/img/07_franck_hertz/AMPOLL~1.svg')
FONT = "'Times New Roman', Times, serif"
SCALA = 5
CORPO = 3000          # 3000 x 5 = 15000 unita' di disegno
PEDICE = 2100         # 2100 x 5 = 10500
GIU = 900             # abbassamento del pedice

# il disegno arriva a y=566490: serve spazio sotto per le tensioni
VECCHIO_VIEWBOX = 'viewBox="-17125 312505 463720 253985"'
NUOVO_VIEWBOX = 'viewBox="-17125 312505 463720 278985"'
VECCHIO_SFONDO = '<rect fill="#ffffff" x="-17125" y="312505" width="463720" height="253985"'
NUOVO_SFONDO = '<rect fill="#ffffff" x="-17125" y="312505" width="463720" height="278985"'
VECCHIA_MISURA = 'width="200.0mm" height="109.5mm"'
NUOVA_MISURA = 'width="200.0mm" height="120.3mm"'

# (x, y, ancora, testo, pedice, coda)
ETICHETTE = [
    (40000, 348000, 'middle', '5V', None, None),          # generatore del filamento
    (160000, 372000, 'middle', 'A', None, None),          # filamento
    (213000, 356000, 'start', 'B', None, None),           # prima griglia
    (290000, 356000, 'start', 'C', None, None),           # seconda griglia
    (318000, 372000, 'start', 'D', None, None),           # placca
    (408000, 381000, 'middle', 'I', None, None),          # corrente
    (154006, 568000, 'middle', 'V', 'AB', '\u22485V'),
    (244866, 568000, 'middle', 'V', 'BC', '=0..80V'),
    (355003, 568000, 'middle', 'V', 'CD', '\u22485V'),
]

s = SORGENTE.read_text(encoding='utf-8')
assert '<text' not in s, 'la figura ha gia\u2019 delle scritte'
for vecchio, nuovo in ((VECCHIO_VIEWBOX, NUOVO_VIEWBOX),
                       (VECCHIO_SFONDO, NUOVO_SFONDO),
                       (VECCHIA_MISURA, NUOVA_MISURA)):
    assert s.count(vecchio) == 1, vecchio
    s = s.replace(vecchio, nuovo)

testi = []
for x, y, ancora, testo, pedice, coda in ETICHETTE:
    dentro = testo
    if pedice:
        dentro += (f'<tspan font-size="{PEDICE}" dy="{GIU}">{pedice}</tspan>'
                   f'<tspan dy="-{GIU}">{coda}</tspan>')
    testi.append(
        f'<text transform="translate({x} {y}) scale({SCALA})" font-family="{FONT}" '
        f'font-size="{CORPO}" text-anchor="{ancora}" fill="#000000">{dentro}</text>')

SORGENTE.write_text(s.replace('</svg>', ''.join(testi) + '</svg>'), encoding='utf-8', newline='')
print(f'scritte aggiunte: {len(ETICHETTE)}')

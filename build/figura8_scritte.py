"""Rimette sulla figura 8 della scheda 5 le scritte perse nella conversione dal DWG.

Il corpo del testo passa per una transform: Chrome limita font-size a 10000px,
e in queste unita' di disegno ne servono 24000.
"""
from pathlib import Path

SORGENTE = Path('publish/img/05_rutherford/IMPULSO.svg')
FONT = "'Times New Roman', Times, serif"
SCALA = 2
CORPO = 6000                      # 6000 x 2 = 12000 unita' di disegno

# (x, y, ancora, testo_it, testo_en)
ETICHETTE = [
    (25000, 455000, 'start', 'Tensione', 'Voltage'),
    (2000, 574800, 'end', 'U', 'U'),
    (375000, 667500, 'end', 'Tempo', 'Time'),
    (150000, 490000, 'start', 'Impulso originale', 'Original pulse'),
    (25000, 762000, 'start', 'Tensione', 'Voltage'),
    (375000, 975000, 'end', 'Tempo', 'Time'),
    (200000, 880000, 'start', 'Impulso squadrato', 'Squared pulse'),
]


def scrivi(s, lingua):
    assert '<text' not in s, 'la figura ha gia\u2019 delle scritte'
    testi = []
    for x, y, ancora, it, en in ETICHETTE:
        t = it if lingua == 'it' else en
        testi.append(
            f'<text transform="translate({x} {y}) scale({SCALA})" font-family="{FONT}" '
            f'font-size="{CORPO}" text-anchor="{ancora}" fill="#000000">{t}</text>'
        )
    return s.replace('</svg>', ''.join(testi) + '</svg>')


originale = SORGENTE.read_text(encoding='utf-8')
SORGENTE.write_text(scrivi(originale, 'it'), encoding='utf-8', newline='')
SORGENTE.with_name('IMPULSO-en.svg').write_text(scrivi(originale, 'en'), encoding='utf-8', newline='')
print('scritte aggiunte: IMPULSO.svg e IMPULSO-en.svg')

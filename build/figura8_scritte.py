"""Rimette sulla figura 8 della scheda 5 le scritte perse nella conversione dal DWG.

Il corpo del testo passa per una transform: Chrome limita font-size a 10000px,
e in queste unita' di disegno ne servono 24000.
"""
from pathlib import Path

SORGENTE = Path('publish/img/05_rutherford/IMPULSO.svg')
FONT = "'Times New Roman', Times, serif"
SCALA = 4
CORPO = 6000                      # 6000 x 4 = 24000 unita' di disegno

VECCHIO_VIEWBOX = 'viewBox="-22847 405291 431129 617583"'
NUOVO_VIEWBOX = 'viewBox="-40000 405291 448282 617583"'
VECCHIO_SFONDO = '<rect fill="#ffffff" x="-22847" y="405291" width="431129" height="617583"'
NUOVO_SFONDO = '<rect fill="#ffffff" x="-40000" y="405291" width="448282" height="617583"'
VECCHIA_MISURA = 'width="200.0mm" height="286.5mm"'
NUOVA_MISURA = 'width="208.0mm" height="286.5mm"'

# (x, y, ancora, testo_it, testo_en)
ETICHETTE = [
    (25000, 455000, 'start', 'Tensione', 'Voltage'),
    (2000, 578700, 'end', 'U', 'U'),
    (375000, 667500, 'end', 'Tempo', 'Time'),
    (150000, 490000, 'start', 'Impulso originale', 'Original pulse'),
    (25000, 762000, 'start', 'Tensione', 'Voltage'),
    (375000, 975000, 'end', 'Tempo', 'Time'),
    (200000, 880000, 'start', 'Impulso squadrato', 'Squared pulse'),
]


def scrivi(s, lingua):
    assert '<text' not in s, 'la figura ha gia\u2019 delle scritte'
    for vecchio, nuovo in ((VECCHIO_VIEWBOX, NUOVO_VIEWBOX),
                           (VECCHIO_SFONDO, NUOVO_SFONDO),
                           (VECCHIA_MISURA, NUOVA_MISURA)):
        assert s.count(vecchio) == 1, vecchio
        s = s.replace(vecchio, nuovo)
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

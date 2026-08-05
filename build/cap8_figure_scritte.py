"""Rimette sulle figure 1, 2, 3, 12 e 13 della scheda 8 le scritte perse nella
conversione dal DWG. Sono parole, non simboli: serve anche la versione inglese.

Il corpo e' circa il 3,5% della larghezza del disegno: sul sito le figure sono
molto piu' grandi che sulla pagina stampata, quindi il carattere va tenuto piu'
piccolo di quanto appaia nelle scansioni.
"""
from pathlib import Path

BASE = Path('publish/img/08_effetto_fotoelettrico')
FONT = "'Times New Roman', Times, serif"

# nome: (viewBox nuovo, misure nuove, corpo, [(x, y, ancora, it, en), ...])
FIGURE = {
    'EMISSI~1.svg': {                                   # fig. 1
        'vecchio_vb': '306006 124040 241680 132444',
        'nuovo_vb': '276006 124040 271680 147444',
        'vecchia_mis': ('200.0mm', '109.6mm'),
        'nuova_mis': ('224.8mm', '122.0mm'),
        'corpo': 9500,
        'etichette': [
            (306000, 140000, 'end', 'Luce', 'Visible'),
            (306000, 152000, 'end', 'visibile', 'light'),
            (545000, 135000, 'end', 'Elettroni', 'Electrons'),
            (415000, 262000, 'middle', 'Metallo', 'Metal'),
        ],
    },
    'AMPOLL~2.svg': {                                   # fig. 2
        'vecchio_vb': '98630 -6343 171304 161319',
        'nuovo_vb': '98630 -6343 201304 161319',
        'vecchia_mis': ('200.0mm', '188.3mm'),
        'nuova_mis': ('235.0mm', '188.3mm'),
        'corpo': 7000,
        'etichette': [
            (200500, 7000, 'start', 'Anodo', 'Anode'),
            (272000, 22000, 'start', 'Luce', 'Visible'),
            (272000, 31000, 'start', 'visibile', 'light'),
            (102000, 76000, 'end', 'I', 'I'),
            (200500, 150500, 'start', 'Catodo', 'Cathode'),
        ],
    },
    'AMPOLL~1.svg': {                                   # fig. 3
        'vecchio_vb': '23010 258021 249833 167245',
        'nuovo_vb': '-1990 258021 304833 167245',
        'vecchia_mis': ('200.0mm', '133.9mm'),
        'nuova_mis': ('244.0mm', '133.9mm'),
        'corpo': 9000,
        'etichette': [
            (200500, 274000, 'start', 'Anodo', 'Anode'),
            (272000, 288000, 'start', 'Luce', 'Visible'),
            (272000, 300000, 'start', 'visibile', 'light'),
            (28000, 345000, 'end', '\u0394V', '\u0394V'),
            (200500, 417500, 'start', 'Catodo', 'Cathode'),
        ],
    },
    'SOLOVO~1.svg': {                                   # fig. 12
        'vecchio_vb': '-14097 740053 380625 177040',
        'nuovo_vb': None,
        'corpo': 13000,
        'etichette': [
            (-13000, 753000, 'start', 'Voltmetro', 'Voltmeter'),
        ],
    },
    'SEPARA~1.svg': {                                   # fig. 13
        'vecchio_vb': '531589 392743 486427 212414',
        'nuovo_vb': None,
        'corpo': 15000,
        'etichette': [
            (533000, 420000, 'start', 'Voltmetro', 'Voltmeter'),
            (684030, 478000, 'middle', 'Separatore', 'Impedance'),
            (684030, 500000, 'middle', 'di', 'buffer'),
            (684030, 522000, 'middle', 'impedenza', '', ),
        ],
    },
}


def scrivi(s, dati, lingua):
    assert '<text' not in s, 'la figura ha gia\u2019 delle scritte'
    if dati['nuovo_vb']:
        vecchio_vb, nuovo_vb = dati['vecchio_vb'], dati['nuovo_vb']
        assert s.count('viewBox="%s"' % vecchio_vb) == 1
        s = s.replace('viewBox="%s"' % vecchio_vb, 'viewBox="%s"' % nuovo_vb)
        x, y, w, h = nuovo_vb.split()
        vx, vy, vw, vh = vecchio_vb.split()
        assert s.count('x="%s" y="%s" width="%s" height="%s"' % (vx, vy, vw, vh)) == 1
        s = s.replace('x="%s" y="%s" width="%s" height="%s"' % (vx, vy, vw, vh),
                      'x="%s" y="%s" width="%s" height="%s"' % (x, y, w, h))
        vm, nm = dati['vecchia_mis'], dati['nuova_mis']
        assert s.count('width="%s" height="%s"' % vm) == 1
        s = s.replace('width="%s" height="%s"' % vm, 'width="%s" height="%s"' % nm)

    scala = 4
    corpo = dati['corpo'] // scala
    testi = []
    for x, y, ancora, it, en in dati['etichette']:
        t = it if lingua == 'it' else en
        if not t:
            continue
        testi.append(
            f'<text transform="translate({x} {y}) scale({scala})" font-family="{FONT}" '
            f'font-size="{corpo}" text-anchor="{ancora}" fill="#000000">{t}</text>')
    return s.replace('</svg>', ''.join(testi) + '</svg>')


for nome, dati in FIGURE.items():
    originale = (BASE / nome).read_text(encoding='utf-8')
    (BASE / nome).write_text(scrivi(originale, dati, 'it'), encoding='utf-8', newline='')
    en = nome.replace('.svg', '-en.svg')
    (BASE / en).write_text(scrivi(originale, dati, 'en'), encoding='utf-8', newline='')
    print(f'{nome}: {len(dati["etichette"])} scritte, con {en}')

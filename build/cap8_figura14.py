"""Ricostruisce la figura 14 della scheda 8: energia degli elettroni in funzione
della frequenza della luce. Era un grafico interno a Word, perso nella conversione;
i punti sono quelli della tabella che la precede."""
from pathlib import Path

BASE = Path('publish/img/08_effetto_fotoelettrico')
FONT = "'Times New Roman', Times, serif"

PUNTI = [(5.19, 0.44), (5.49, 0.54), (6.88, 1.05), (7.41, 1.24)]

# retta dei minimi quadrati sui quattro punti: 0,3623 eV per 10^14 Hz,
# soglia a 3,99 - sono i valori citati nel testo
PENDENZA = 0.36230
INTERCETTA = -1.44416

X0, X1 = 3.5, 7.5           # estremi degli assi
Y0, Y1 = 0.0, 1.4
SX, DX, SU, GIU = 130, 970, 60, 520      # riquadro del grafico in unita' svg
LARGO, ALTO = 1040, 620
CORPO, TITOLO = 24, 27


def px(v):
    return SX + (v - X0) / (X1 - X0) * (DX - SX)


def py(v):
    return GIU - (v - Y0) / (Y1 - Y0) * (GIU - SU)


def num(v, decimali, lingua):
    t = f'{v:.{decimali}f}'
    return t if lingua == 'en' else t.replace('.', ',')


def testo(x, y, ancora, contenuto, corpo=CORPO):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="{FONT}" font-size="{corpo}" '
            f'text-anchor="{ancora}" fill="#000">{contenuto}</text>')


def disegna(lingua):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="170mm" height="101.3mm" '
         f'viewBox="0 0 {LARGO} {ALTO}">',
         f'<rect fill="#ffffff" x="0" y="0" width="{LARGO}" height="{ALTO}"/>',
         '<g stroke="#000" stroke-width="2.2" fill="none" stroke-linecap="round">']

    # assi, con la punta di freccia
    p.append(f'<path d="M {SX} {GIU} L {DX + 18} {GIU}"/>')
    p.append(f'<path d="M {SX} {GIU} L {SX} {SU - 18}"/>')
    p.append('</g>')
    p.append(f'<path d="M {DX + 34} {GIU} l -16 -6 l 0 12 Z" fill="#000"/>')
    p.append(f'<path d="M {SX} {SU - 34} l -6 16 l 12 0 Z" fill="#000"/>')

    # tacche e numeri
    p.append('<g stroke="#000" stroke-width="2" fill="none">')
    v = X0
    while v <= X1 + 1e-9:
        p.append(f'<path d="M {px(v):.0f} {GIU} l 0 8"/>')
        v += 0.5
    v = Y0
    while v <= Y1 + 1e-9:
        p.append(f'<path d="M {SX} {py(v):.0f} l -8 0"/>')
        v += 0.2
    p.append('</g>')

    v = X0
    while v <= X1 + 1e-9:
        p.append(testo(px(v), GIU + 34, 'middle', num(v, 1, lingua)))
        v += 0.5
    v = Y0
    while v <= Y1 + 1e-9:
        p.append(testo(SX - 16, py(v) + 8, 'end', num(v, 1, lingua)))
        v += 0.2

    # la retta: tratteggiata sotto il primo punto, continua da li' in poi
    soglia = -INTERCETTA / PENDENZA
    fine = 7.55
    primo = PUNTI[0][0]
    p.append(f'<path d="M {px(soglia):.1f} {py(0):.1f} L {px(primo):.1f} '
             f'{py(PENDENZA * primo + INTERCETTA):.1f}" stroke="#000" stroke-width="2" '
             f'stroke-dasharray="5 5" fill="none"/>')
    p.append(f'<path d="M {px(primo):.1f} {py(PENDENZA * primo + INTERCETTA):.1f} L '
             f'{px(fine):.1f} {py(PENDENZA * fine + INTERCETTA):.1f}" stroke="#000" '
             f'stroke-width="2" fill="none"/>')

    # i punti misurati
    for x, y in PUNTI:
        p.append(f'<rect x="{px(x) - 7:.1f}" y="{py(y) - 7:.1f}" width="14" height="14" fill="#000"/>')

    # titoli degli assi
    p.append(testo(SX + 14, SU - 26, 'start',
                   'Energia (eV)' if lingua == 'it' else 'Energy (eV)', TITOLO))
    nome = 'Frequenza' if lingua == 'it' else 'Frequency'
    p.append(f'<text x="{DX + 60}" y="{GIU + 76}" font-family="{FONT}" font-size="{TITOLO}" '
             f'text-anchor="end" fill="#000">{nome} (10'
             f'<tspan font-size="{TITOLO * 7 // 10}" dy="-9">14</tspan>'
             f'<tspan dy="9"> Hz)</tspan></text>')

    p.append('</svg>')
    return ''.join(p)


for lingua, nome in (('it', 'GRAFICO.svg'), ('en', 'GRAFICO-en.svg')):
    (BASE / nome).write_text(disegna(lingua), encoding='utf-8', newline='')
    print('scritta', nome)

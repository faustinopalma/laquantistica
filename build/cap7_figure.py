"""Scheda 7: rimette in ordine le foto 4, 8 e 9 (erano ruotate di una posizione)
e scrive le indicazioni sulla figura 6."""
from pathlib import Path

# --- 1. le tre foto dell'apparato
# fig. 4 (neon, supporto a destra)  -> APPARA~3
# fig. 8 (mercurio, termocoppia)    -> APPARA~1
# fig. 9 (mercurio, fornetto chiuso)-> APPARA~2
p = Path('sorgenti/07-franck-hertz.html')
s = p.read_text(encoding='utf-8')
righe = s.split('\n')
for n, atteso, nuovo in ((65, '1', '3'), (85, '2', '1'), (86, '3', '2')):
    vecchio = 'src="img/07_franck_hertz/APPARA~%s.jpg"' % atteso
    assert vecchio in righe[n - 1], f'riga {n}: {vecchio} non trovato'
    righe[n - 1] = righe[n - 1].replace(vecchio, 'src="img/07_franck_hertz/APPARA~%s.jpg?v=2"' % nuovo)
p.write_text('\n'.join(righe), encoding='utf-8', newline='')
print('scheda 7: foto 4, 8 e 9 rimesse in ordine')

# --- 2. le scritte della figura 6
FIG = Path('publish/img/07_franck_hertz/DIAGRA~1.svg')
FONT = "'Times New Roman', Times, serif"
SCALA = 4
CORPO = 4000          # 16000 unita' di disegno
PEDICE = 2750
GIU = 1200

# i quattro tratti quotati stanno tra queste ascisse, a y=238134
INTERVALLI = [(685911, 738499), (753382, 805970), (820853, 873441), (888325, 940913)]

t = FIG.read_text(encoding='utf-8')
assert '<text' not in t, 'la figura ha gia\u2019 delle scritte'

etichette = [
    (688000, 42000, 'start', 'I', None, None),          # asse verticale
    (976000, 188000, 'end', 'V', 'BC', None),           # asse orizzontale
]
for a, b in INTERVALLI:
    etichette.append(((a + b) // 2, 257000, 'middle', '19V', None, None))

testi = []
for x, y, ancora, testo, pedice, coda in etichette:
    dentro = testo
    if pedice:
        dentro += f'<tspan font-size="{PEDICE}" dy="{GIU}">{pedice}</tspan>'
    testi.append(
        f'<text transform="translate({x} {y}) scale({SCALA})" font-family="{FONT}" '
        f'font-size="{CORPO}" text-anchor="{ancora}" fill="#000000">{dentro}</text>')

FIG.write_text(t.replace('</svg>', ''.join(testi) + '</svg>'), encoding='utf-8', newline='')
print(f'figura 6: {len(etichette)} scritte aggiunte')

# --- 3. il richiamo alla figura 6 deve ricaricare l'immagine
s = p.read_text(encoding='utf-8')
vecchia = 'src="img/07_franck_hertz/DIAGRA~1.svg?v=2"'
assert s.count(vecchia) == 1
p.write_text(s.replace(vecchia, 'src="img/07_franck_hertz/DIAGRA~1.svg?v=3"'),
             encoding='utf-8', newline='')
print('scheda 7: figura 6 aggiornata')

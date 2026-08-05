"""Scheda 7: corregge la tensione sull'asse X, rimette i pedici delle tensioni,
aggiorna il richiamo alla figura 2."""
from pathlib import Path
import re

p = Path('sorgenti/07-franck-hertz.html')
s = p.read_text(encoding='utf-8')

# 1. sull'oscilloscopio va la tensione variata tra le griglie, che e' VBC (righe 59, 60, 77, 78)
coppie = [
    ('porta la tensione VAB applicata tra le griglie',
     'porta la tensione VBC applicata tra le griglie'),
    ('carries the voltage VAB applied between the grids',
     'carries the voltage VBC applied between the grids'),
    ('il diagramma tensione/corrente VAB/I',
     'il diagramma tensione/corrente VBC/I'),
    ('the voltage/current diagram VAB/I',
     'the voltage/current diagram VBC/I'),
]
for vecchio, nuovo in coppie:
    assert s.count(vecchio) == 1, vecchio
    s = s.replace(vecchio, nuovo)

# 2. i pedici, persi nella conversione: V<sub>AB</sub> come nella figura
n = len(re.findall(r'\bV(AB|BC|CD)\b', s))
s = re.sub(r'\bV(AB|BC|CD)\b', lambda m: '<em>V</em><sub>%s</sub>' % m.group(1), s)

# 3. la figura 2 ora ha le scritte
vecchia = 'src="img/07_franck_hertz/AMPOLL~1.svg?v=2"'
assert s.count(vecchia) == 1
s = s.replace(vecchia, 'src="img/07_franck_hertz/AMPOLL~1.svg?v=3"')

assert s.count('<span') == s.count('</span>')
p.write_text(s, encoding='utf-8', newline='')
print(f'scheda 7: tensione sull\u2019asse X corretta, {n} pedici ripristinati')

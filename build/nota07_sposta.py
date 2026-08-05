"""Sposta il richiamo alla nota 07 dopo la formula e corregge il rinvio nella scheda 7."""
from pathlib import Path

# --- scheda 6: via il paragrafo di rinuncia, il richiamo va sotto la formula
p6 = Path('sorgenti/06-ulteriori-sviluppi.html')
righe = p6.read_text(encoding='utf-8').split('\n')

i = next(k for k, r in enumerate(righe) if 'nota-link" id="nota-7"' in r)
assert righe[i + 3].strip() == '</div>'
richiamo = righe[i:i + 4]

assert righe[i + 4].startswith('<p><span class="it">In questa scheda non risolviamo')
assert 'L\u2019energia pu\u00f2 assumere solo dei valori discreti' in righe[i + 5]
assert righe[i + 6].startswith('<div class="equation">')

nuove = righe[:i] + [righe[i + 5], righe[i + 6]] + richiamo + righe[i + 7:]
p6.write_text('\n'.join(nuove), encoding='utf-8', newline='')
print('scheda 6: paragrafo tolto, richiamo spostato dopo la formula')

# --- scheda 7: il fenomeno e' trattato nella nona scheda, non nella decima
p7 = Path('sorgenti/07-franck-hertz.html')
s7 = p7.read_text(encoding='utf-8')
for vecchio, nuovo in (('approfonditamente nella decima scheda.', 'approfonditamente nella nona scheda.'),
                       ('in detail in the tenth card.', 'in detail in the ninth card.')):
    assert s7.count(vecchio) == 1, vecchio
    s7 = s7.replace(vecchio, nuovo)
p7.write_text(s7, encoding='utf-8', newline='')
print('scheda 7: rinvio corretto alla nona scheda')

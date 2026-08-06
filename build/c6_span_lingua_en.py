"""Capitolo 6: la formula del quarto principio era avvolta nella lingua sbagliata.

Nella meta' inglese `\\overline{x},\\overline{y}` stava dentro <span class="it">: la
potatura la toglieva dall'albero inglese, e in quello italiano spariva insieme a tutto
il paragrafo .en. Risultato: la frase inglese restava monca. Si toglie il solo involucro.
"""
import re
import sys
from pathlib import Path

F = Path('sorgenti/06-ulteriori-sviluppi.html')
t = F.read_text(encoding='utf-8')

PREFISSO = ', the values '
INVOLUCRO = '<span class="it">'
apertura = t.find(PREFISSO + INVOLUCRO)
if apertura == -1:
    sys.exit('involucro gia\' tolto o testo cambiato')
apertura += len(PREFISSO)

i = t.index('>', apertura) + 1
livello = 1
for m in re.finditer(r'<span\b[^>]*>|</span>', t[i:]):
    livello += 1 if m.group(0).startswith('<span') else -1
    if livello == 0:
        fine_i, fine_f = i + m.start(), i + m.end()
        break
else:
    sys.exit('span non chiuso')

dentro = t[i:fine_i]
if 'data-tex="\\overline{x},\\overline{y}"' not in dentro:
    sys.exit('l\'involucro non contiene la formula attesa')

F.write_text(t[:apertura] + dentro + t[fine_f:], encoding='utf-8')
print('involucro .it dentro .en rimosso dalla meta\' inglese')

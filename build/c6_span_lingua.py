"""Capitolo 6: due formule erano avvolte nello span della lingua SBAGLIATA.

La formula \\overline{x},\\overline{y} stava dentro <span class="en"> nella meta'
italiana e dentro <span class="it"> in quella inglese: la potatura per lingua la
toglieva da ENTRAMBI gli alberi e la frase restava monca in tutte e due le lingue.
Si toglie il solo involucro, il contenuto resta dov'e'.
"""
import re
import sys
from pathlib import Path

F = Path('sorgenti/06-ulteriori-sviluppi.html')
t = F.read_text(encoding='utf-8')


def chiusura(testo, apertura):
    """Posizione del </span> che chiude lo <span> che inizia in `apertura`."""
    i = testo.index('>', apertura) + 1
    livello = 1
    for m in re.finditer(r'<span\b[^>]*>|</span>', testo[i:]):
        livello += 1 if m.group(0).startswith('<span') else -1
        if livello == 0:
            return i + m.start(), i + m.end()
    sys.exit('span non chiuso')


tolti = 0
for involucro in ('<span class="en"><span class="eq-inline eq-mml" data-tex="\\overline{x},\\overline{y}">',
                  '<span class="it"><span class="eq-inline eq-mml" data-tex="\\overline{x},\\overline{y}">'):
    apertura = t.find(involucro)
    if apertura == -1:
        sys.exit(f'non trovato: {involucro[:40]}')
    fine_i, fine_f = chiusura(t, apertura)
    dentro = t[t.index('>', apertura) + 1:fine_i]
    if 'data-tex' not in dentro or len(dentro) > 6000:
        sys.exit('l\'involucro contiene piu\' della formula: fermarsi')
    t = t[:apertura] + dentro + t[fine_f:]
    tolti += 1

F.write_text(t, encoding='utf-8')
print(f'involucri di lingua tolti: {tolti}')
print('occorrenze della formula nel sorgente:', t.count('\\overline{x},\\overline{y}'))

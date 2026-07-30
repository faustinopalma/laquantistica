"""Toglie il vanto da una frase che parla di un apparato mai costruito.

Diceva che «il vantaggio non e' concettuale ma pratico», come se lo sdoppiamento
piu' ampio fosse un risultato acquisito. E' invece cio' che ci si attende da una
geometria proposta sulla carta: la frase torna al condizionale, che e' il modo
in cui va detta.

    python tools/ch1_vantaggio.py
"""
from pathlib import Path

PAGINA = Path('publish/01-stern-gerlach.html')

CAMBI = [
    ('nel 1922. Il vantaggio non \u00e8 concettuale ma pratico: uno sdoppiamento di '
     'quest\u2019ordine \u00e8 visibile e misurabile direttamente, senza ricorrere alle '
     'micrografie.',
     'nel 1922: uno sdoppiamento di quest\u2019ordine si potrebbe leggere e misurare '
     'direttamente, senza ricorrere alle micrografie.'),

    ('in 1922. The advantage is not conceptual but practical: a splitting of this '
     'order is directly visible and measurable, without resorting to micrographs.',
     'in 1922: a splitting of that order could be read and measured directly, '
     'without resorting to micrographs.'),
]

src = PAGINA.read_text(encoding='utf-8')
fatti = 0
for vecchio, nuovo in CAMBI:
    if vecchio in src:
        src = src.replace(vecchio, nuovo, 1)
        fatti += 1
    else:
        print(f'  NON TROVATO: {vecchio[:60]}...')
PAGINA.write_text(src, encoding='utf-8', newline='')
print(f'{fatti} su {len(CAMBI)} corretti')

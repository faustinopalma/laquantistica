"""Rinumera in un solo passaggio le etichette di capitolo dei sorgenti.

Il capitolo di matematica entra come terzo: 1 e 2 restano, dal 3 in poi tutti slittano
di uno. Il passaggio dev'essere unico: applicando 3->4 e poi 4->5 in sequenza i numeri
si sovrascriverebbero a vicenda.
"""
import pathlib
import re

RADICE = pathlib.Path('sorgenti')
ETICHETTA = re.compile(r'\b(Cap\.|Ch\.|Capitolo|Chapter)(\s+)(\d{1,2})\b')


def nuovo(n):
    return n + 1 if n >= 3 else n


def sostituisci(m):
    parola, spazio, cifre = m.group(1), m.group(2), m.group(3)
    n = int(cifre)
    if not 1 <= n <= 12:
        raise SystemExit(f'numero fuori intervallo: {m.group(0)!r}')
    return f'{parola}{spazio}{nuovo(n):0{len(cifre)}d}'


totale = 0
for percorso in sorted(RADICE.glob('*.html')):
    testo = percorso.read_text(encoding='utf-8')
    nuovo_testo, quante = ETICHETTA.subn(sostituisci, testo)
    if quante:
        percorso.write_text(nuovo_testo, encoding='utf-8', newline='')
        totale += quante
        print(f'{percorso.name:<42} {quante:>3}')
print(f'\netichette rinumerate: {totale}')

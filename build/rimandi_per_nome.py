"""Converte i rimandi ordinali fra schede in rimandi per nome.

I rimandi per numero ("nella quarta scheda") si rompono a ogni riordino; quelli per nome no.
Lo script non scrive nulla se anche una sola stringa attesa non viene trovata esattamente una volta.
"""
import pathlib
import sys

SOSTITUZIONI = {
    '05-rutherford.html': [
        ('nella terza scheda',
         'nella scheda sugli esperimenti con gli elettroni'),
        ('in the third card',
         'in the card on experiments with electrons'),
    ],
    '06-ulteriori-sviluppi.html': [
        ('Nella scheda quattro abbiamo introdotto l’equazione di Schrödinger',
         'Nella scheda sull’hamiltoniana abbiamo introdotto l’equazione di Schrödinger'),
        ('In card four we introduced the Schrödinger equation',
         'In the card on the Hamiltonian we introduced the Schrödinger equation'),
        ('che nella scheda quattro ci ha permesso di ricavare',
         'che nella scheda sull’hamiltoniana ci ha permesso di ricavare'),
        ('that in card four allowed us to derive',
         'that in the card on the Hamiltonian allowed us to derive'),
        ('abbiamo definito nella quarta scheda',
         'abbiamo definito nella scheda sull’hamiltoniana'),
        ('we defined in the fourth card',
         'we defined in the card on the Hamiltonian'),
    ],
    '07-franck-hertz.html': [
        ('approfonditamente nella nona scheda',
         'approfonditamente nella scheda sugli spettri atomici'),
        ('in detail in the ninth card',
         'in detail in the card on atomic spectra'),
    ],
    '08-effetto-fotoelettrico.html': [
        ('è stata formulata nella quarta scheda',
         'è stata formulata nella scheda sull’hamiltoniana'),
        ('was formulated in the fourth card',
         'was formulated in the card on the Hamiltonian'),
    ],
    'nota-01-stern-gerlach.html': [
        ('nella quarta scheda l’equazione di Schrödinger non è calata dall’alto',
         'nelle schede teoriche l’equazione di Schrödinger non è calata dall’alto'),
        ('in Chapter 4 the Schrödinger equation is not handed down',
         'in the theory chapters the Schrödinger equation is not handed down'),
    ],
    'nota-04-i-principi.html': [
        ('entra in scena nella scheda quattro',
         'entra in scena nella scheda sull’hamiltoniana'),
        ('comes into play in chapter four',
         'comes into play in the chapter on the Hamiltonian'),
    ],
    'nota-07-livelli-idrogeno.html': [
        ('Come nella quarta scheda, restringere il campo',
         'Come nella scheda sull’hamiltoniana, restringere il campo'),
        ('As in the fourth chapter, narrowing the search',
         'As in the chapter on the Hamiltonian, narrowing the search'),
        ('quello che nella nona scheda compare nei salti',
         'quello che nella scheda sugli spettri compare nei salti'),
        ('appears in the ninth chapter in the jumps',
         'appears in the chapter on atomic spectra in the jumps'),
    ],
}

RADICE = pathlib.Path('sorgenti')
guasti = []
lavoro = []

for nome, coppie in SOSTITUZIONI.items():
    percorso = RADICE / nome
    testo = percorso.read_text(encoding='utf-8')
    for vecchio, nuovo in coppie:
        quante = testo.count(vecchio)
        if quante != 1:
            guasti.append(f'{nome}: {quante} occorrenze di "{vecchio[:60]}..."')
            continue
        testo = testo.replace(vecchio, nuovo)
    lavoro.append((percorso, testo))

if guasti:
    print('NESSUNA MODIFICA SCRITTA. Problemi:')
    print('\n'.join('  ' + g for g in guasti))
    sys.exit(1)

for percorso, testo in lavoro:
    percorso.write_text(testo, encoding='utf-8', newline='')
    print('aggiornato', percorso.name)
print(f'\nfile toccati: {len(lavoro)} · sostituzioni: {sum(len(v) for v in SOSTITUZIONI.values())}')

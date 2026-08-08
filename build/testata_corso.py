"""Testata nuova (corso, con la tesi come provenienza) e ritocchi minimi al testo.

Tocca solo le righe elencate qui: non riscrive prosa.
"""
import pathlib
import sys

RADICE = pathlib.Path('sorgenti')

MARCHIO_VECCHIO = ('<small class="it">Esperimenti fondamentali di Meccanica Quantistica — Tesi di Laurea</small>'
                   '<small class="en">Fundamental Experiments of Quantum Mechanics — Master\'s Thesis</small>')
MARCHIO_NUOVO = ('<small class="it">Corso introduttivo di Meccanica Quantistica — dagli esperimenti alla teoria</small>'
                 '<small class="en">An Introductory Course in Quantum Mechanics — from the experiments to the theory</small>')

PROVENIENZA_VECCHIA = ('<span class="it">Edizione web rivista rispetto all’originale del 1999.</span>\n'
                       '    <span class="en">Web edition revised from the 1999 original.</span>')
PROVENIENZA_NUOVA = ('<span class="it">Nato come tesi di laurea, Federico II, 1999 — riveduto e ampliato per il web.</span>\n'
                     '    <span class="en">Born as a master’s thesis, Federico II, 1999 — revised and expanded for the web.</span>')

# La scheda sugli spettri chiude anche il percorso sperimentale: non deve dare per letta
# la scheda teorica sui livelli.
SPETTRI_VECCHIO = ('<span class="it">Nella sesta scheda abbiamo visto che l’energia dell’atomo di idrogeno '
                   'è quantizzata; ora ci chiediamo: cosa succede quando un atomo passa da uno stato '
                   'energetico superiore a uno inferiore?</span><span class="en">In the sixth card we saw '
                   'that the energy of the hydrogen atom is quantised; we now ask what happens when an '
                   'atom passes from a higher energy state to a lower one.</span>')
SPETTRI_NUOVO = ('<span class="it">L’energia dell’atomo di idrogeno è quantizzata, e la formula dei livelli '
                 'è ricavata nella scheda sugli ulteriori sviluppi. Ora ci chiediamo: cosa succede quando '
                 'un atomo passa da uno stato energetico superiore a uno inferiore?</span><span class="en">'
                 'The energy of the hydrogen atom is quantised, and the formula for the levels is derived '
                 'in the card on further developments. We now ask what happens when an atom passes from a '
                 'higher energy state to a lower one.</span>')

guasti = []
toccati = 0

for percorso in sorted(RADICE.glob('*.html')):
    testo = percorso.read_text(encoding='utf-8')
    originale = testo
    if MARCHIO_VECCHIO in testo:
        testo = testo.replace(MARCHIO_VECCHIO, MARCHIO_NUOVO)
    if PROVENIENZA_VECCHIA in testo:
        testo = testo.replace(PROVENIENZA_VECCHIA, PROVENIENZA_NUOVA)
    if percorso.name == '09-spettri-atomici.html':
        if SPETTRI_VECCHIO not in testo:
            guasti.append('09-spettri-atomici.html: cappello non riconosciuto')
        else:
            testo = testo.replace(SPETTRI_VECCHIO, SPETTRI_NUOVO)
    if testo != originale:
        percorso.write_text(testo, encoding='utf-8', newline='')
        toccati += 1

if guasti:
    sys.exit('PROBLEMI:\n  ' + '\n  '.join(guasti))
print(f'file toccati: {toccati}')

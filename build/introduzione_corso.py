"""Ritocchi all'introduzione dopo il riordino.

Cinque sostituzioni mirate: l'occhiello, la frase che apriva il percorso con Stern-Gerlach,
i principi dichiarati come premesse, e il paragrafo su come leggere il sito con i due percorsi.
"""
import pathlib
import sys

PERCORSO = pathlib.Path('sorgenti/index.html')
testo = PERCORSO.read_text(encoding='utf-8')

COPPIE = [
    # occhiello di copertina
    ('<p class="kicker"><span class="it">Tesi di Laurea</span><span class="en">Master\'s Thesis</span></p>',
     '<p class="kicker"><span class="it">Corso introduttivo</span><span class="en">Introductory Course</span></p>'),

    # il percorso non si apre piu' con Stern-Gerlach
    ('<span class="it">Il percorso si apre con l’esperimento di Stern-Gerlach, il punto d’ingresso concettualmente più pulito nel comportamento quantistico.',
     '<span class="it">Fra questi c’è l’esperimento di Stern-Gerlach, il punto d’ingresso concettualmente più pulito nel comportamento quantistico.'),
    ('<span class="en">The path opens with the Stern–Gerlach experiment, the conceptually cleanest entry point into quantum behaviour.',
     '<span class="en">Among these is the Stern–Gerlach experiment, the conceptually cleanest entry point into quantum behaviour.'),
    ('Quella storia è raccontata nella <i>nota dietro le quinte</i> del Capitolo 1;',
     'Quella storia è raccontata nella <i>nota dietro le quinte</i> della scheda su Stern-Gerlach;'),
    ('That story is told in the <i>behind-the-scenes note</i> of Chapter 1;',
     'That story is told in the <i>behind-the-scenes note</i> of the Stern–Gerlach card;'),

    # i quattro principi sono premesse: va detto, e va detto dove nascono
    ('<p><span class="it">Da questi quattro principi, e da una misura, si deduce l’equazione di Schrödinger, senza doverla postulare e senza ricorrere alla Meccanica Analitica.</span>',
     '<p><span class="it">Da questi quattro principi, e da una misura, si deduce l’equazione di Schrödinger, senza doverla postulare e senza ricorrere alla Meccanica Analitica.</span>'
     '<span class="en">From these four principles, and one measurement, the Schrödinger equation is derived, without postulating it and without resorting to Analytical Mechanics.</span></p>\n'
     '<p><span class="it">I quattro principi sono premesse: li assumiamo perché funzionano, non li ricaviamo da altro. Gli esperimenti che li rendono naturali — Stern-Gerlach e Stern-Gerlach in cascata — stanno in fondo al percorso, nelle schede 9 e 10. Chi vuole vedere da dove nascono può leggerle prima, ma per seguire la deduzione non è necessario.</span>'),
]

# chiusura del paragrafo doppiato dalla sostituzione precedente
COPPIE.append((
    '<span class="en">From these four principles, and one measurement, the Schrödinger equation is derived, without postulating it and without resorting to Analytical Mechanics.</span></p>\n'
    '<p><span class="it">I quattro principi sono premesse: li assumiamo perché funzionano, non li ricaviamo da altro. Gli esperimenti che li rendono naturali — Stern-Gerlach e Stern-Gerlach in cascata — stanno in fondo al percorso, nelle schede 9 e 10. Chi vuole vedere da dove nascono può leggerle prima, ma per seguire la deduzione non è necessario.</span>'
    '<span class="en">From these four principles, and one measurement, the Schrödinger equation is derived, without postulating it and without resorting to Analytical Mechanics.</span></p>',
    '<span class="en">From these four principles, and one measurement, the Schrödinger equation is derived, without postulating it and without resorting to Analytical Mechanics.</span></p>\n'
    '<p><span class="it">I quattro principi sono premesse: li assumiamo perché funzionano, non li ricaviamo da altro. Gli esperimenti che li rendono naturali — Stern-Gerlach e Stern-Gerlach in cascata — stanno in fondo al percorso, nelle schede 9 e 10. Chi vuole vedere da dove nascono può leggerle prima, ma per seguire la deduzione non è necessario.</span>'
    '<span class="en">The four principles are premises: we assume them because they work, we do not derive them from anything else. The experiments that make them natural — Stern–Gerlach and cascaded Stern–Gerlach — are at the end of the path, in cards 9 and 10. Anyone who wants to see where they come from may read those first, but it is not necessary in order to follow the derivation.</span></p>'))

# come leggere il sito: dodici schede, due percorsi, il salto dichiarato
VECCHIO_LETTURA = (
    '<p><span class="it">Il lavoro è diviso in nove «schede»; ogni scheda contiene una parte sperimentale accompagnata da una parte teorica. Le schede seguono un percorso progressivo: le prime due (Stern-Gerlach e Stern-Gerlach in cascata) introducono i concetti fondamentali e i numeri complessi con rappresentazioni grafiche originali, e sono accessibili anche senza matematica avanzata. La cascata è un esperimento mentale: la sua realizzazione in laboratorio è arrivata solo di recente, e una nota della scheda due la racconta. Nelle schede successive il formalismo cresce gradualmente, fino alla deduzione dell’equazione di Schrödinger. La lettura in ordine è consigliata, ma la parte sperimentale di ogni scheda resta autonoma.</span>'
    '<span class="en">The work is divided into nine “cards”; each card contains an experimental part accompanied by a theoretical part. The cards follow a progressive path: the first two (Stern–Gerlach and cascaded Stern–Gerlach) introduce the fundamental concepts and complex numbers through original graphical representations, and are accessible even without advanced mathematics. The cascade is a thought experiment: its laboratory realisation came only recently, and a note in card two tells that story. In the later cards the formalism grows gradually, up to the derivation of the Schrödinger equation. Reading in order is recommended, but each card’s experimental part stands on its own.</span></p>')

NUOVO_LETTURA = (
    '<p><span class="it">Il lavoro è diviso in dodici «schede»: quelle sperimentali descrivono apparati e misure, quelle teoriche costruiscono la teoria a partire da esse. Nell’originale del 1999 le schede erano nove e alcune tenevano insieme le due cose: le abbiamo divise perché ognuna facesse una cosa sola.</span>'
    '<span class="en">The work is divided into twelve “cards”: the experimental ones describe apparatus and measurements, the theoretical ones build the theory starting from them. In the 1999 original there were nine cards, and some held both things together: we have split them so that each does one thing only.</span></p>\n'
    '<p><span class="it">Si legge su due livelli. Le schede sperimentali — 1, 2, 5, 7, 8, 9 e 12 — si reggono da sole e contengono in tutto un centinaio di formule. Le schede teoriche — 3, 4, 6, 10 e 11 — ricavano i risultati, e sono molto più dense: circa millecinquecento formule, quindici volte tanto. Il salto è brusco, ed è giusto saperlo prima di trovarcisi dentro: si può percorrere tutta la parte sperimentale e tornare alla teoria più tardi, senza perdere il filo. La lettura in ordine resta quella consigliata.</span>'
    '<span class="en">It can be read on two levels. The experimental cards — 1, 2, 5, 7, 8, 9 and 12 — stand on their own and contain about a hundred formulas in all. The theoretical cards — 3, 4, 6, 10 and 11 — derive the results, and are far denser: some fifteen hundred formulas, fifteen times as many. The step up is abrupt, and it is only fair to know it beforehand: you can go through the whole experimental path and come back to the theory later, without losing the thread. Reading in order remains what we recommend.</span></p>')

COPPIE.append((VECCHIO_LETTURA, NUOVO_LETTURA))

guasti = []
for vecchio, nuovo in COPPIE:
    if testo.count(vecchio) != 1:
        guasti.append(f'{testo.count(vecchio)} occorrenze di "{vecchio[:70]}..."')
        continue
    testo = testo.replace(vecchio, nuovo)

if guasti:
    sys.exit('NESSUNA MODIFICA SCRITTA:\n  ' + '\n  '.join(guasti))

PERCORSO.write_text(testo, encoding='utf-8', newline='')
print(f'introduzione aggiornata: {len(COPPIE)} sostituzioni')

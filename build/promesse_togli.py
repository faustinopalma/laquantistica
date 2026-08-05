"""Toglie i rimandi a schede mai scritte, con il minimo intervento sul testo."""
from pathlib import Path

MODIFICHE = {
    '05-rutherford.html': [
        # 1. non esiste una scheda sui raggi X
        ('in vari modi (vedi scheda sui raggi X per un esempio), e il risultato',
         'in vari modi, per esempio con la diffrazione dei raggi X, e il risultato'),
        ('in various ways (see the card on X-rays for an example), and the result',
         'in various ways, for example by X-ray diffraction, and the result'),
        # 2. e 3. non esiste una scheda sulla radioattivita'
        ('. In futuro dedicheremo una scheda alla radioattivit\u00e0, quindi ora vogliamo chiarire '
         'solo il minimo indispensabile',
         '. Qui chiariamo solo il minimo indispensabile'),
        ('. In the future we will devote a card to radioactivity, so for now we want to clarify '
         'only the bare minimum',
         '. Here we clarify only the bare minimum'),
        ('pi\u00f9 o meno complicati, che descriveremo nella scheda sulla radioattivit\u00e0. I rilevatori',
         'pi\u00f9 o meno complicati. I rilevatori'),
        ('more or less complicated, which we will describe in the card on radioactivity. The most',
         'more or less complicated. The most'),
        # 4. non esiste una scheda sui semiconduttori
        (', il meccanismo di questo fenomeno sar\u00e0 descritto approfonditamente in una scheda '
         'dedicata ai materiali semiconduttori quindi per ora non ce ne preoccupiamo.',
         ', per un meccanismo che riguarda i materiali semiconduttori e di cui qui non ci occupiamo.'),
        ('. The mechanism of this phenomenon will be described in detail in a card devoted to '
         'semiconductor materials, so for now we do not worry about it.',
         ', through a mechanism that belongs to semiconductor physics and that we do not deal with here.'),
        # 5. non esiste una scheda sulle radiazioni
        (' (la velocit\u00e0 dei raggi \u03b1 sar\u00e0 misurata nella scheda sulle radiazioni)', ''),
        (' (the speed of the \u03b1 rays will be measured in the card on radiations)', ''),
        # 6. la scheda 6 anticipa i livelli energetici, non discute l'equilibrio
        ('Nella prossima scheda studieremo un tale sistema con l\u2019equazione di Schr\u00f6dinger '
         'e mostreremo come sia possibile che si mantenga in equilibrio.',
         'Nella prossima scheda vedremo i livelli energetici di un tale sistema, ricavati '
         'dall\u2019equazione di Schr\u00f6dinger.'),
        ('In the next card we will study such a system with the Schr\u00f6dinger equation and show '
         'how it is possible for it to remain in equilibrium.',
         'In the next card we will see the energy levels of such a system, obtained from the '
         'Schr\u00f6dinger equation.'),
    ],
    '04-diffrazione.html': [
        ('pi\u00f9 avanti nella scheda sull\u2019esperimento di Rutherford e nella scheda sui raggi X.',
         'pi\u00f9 avanti, nella scheda sull\u2019esperimento di Rutherford.'),
        ('later, in the card on Rutherford\'s experiment and in the card on X-rays.',
         'later, in the card on Rutherford\'s experiment.'),
    ],
    '06-ulteriori-sviluppi.html': [
        ('In questa scheda non vogliamo risolvere questi complicati problemi matematici, e '
         'rimandiamo lo svolgimento a una scheda futura, tuttavia vogliamo anticipare i risultati '
         'per i livelli energetici:',
         'In questa scheda non risolviamo questi complicati problemi matematici; ci limitiamo a '
         'riportare i risultati per i livelli energetici:'),
        ('In this card we do not wish to solve these complicated mathematical problems, and we '
         'defer the treatment to a future card; nevertheless we wish to anticipate the results '
         'for the energy levels:',
         'In this card we do not solve these complicated mathematical problems; we simply report '
         'the results for the energy levels:'),
    ],
    '08-effetto-fotoelettrico.html': [
        ('In futuro studieremo la Meccanica Quantistica Relativistica; per ora, come risultato '
         'di questa scheda, ci ricorderemo',
         'La Meccanica Quantistica Relativistica esula da questo lavoro; come risultato di questa '
         'scheda ci ricorderemo'),
        ('In the future we will study Relativistic Quantum Mechanics; for now, as the result of '
         'this card, we will keep in mind',
         'Relativistic Quantum Mechanics lies outside this work; as the result of this card we '
         'will keep in mind'),
    ],
}

for nome, coppie in MODIFICHE.items():
    p = Path('sorgenti', nome)
    s = p.read_text(encoding='utf-8')
    for vecchio, nuovo in coppie:
        n = s.count(vecchio)
        assert n == 1, f'{nome}: {n} occorrenze di {vecchio[:60]!r}'
        s = s.replace(vecchio, nuovo)
    assert s.count('<span') == s.count('</span>')
    p.write_text(s, encoding='utf-8', newline='')
    print(f'{nome}: {len(coppie)} sostituzioni')

"""Sostituisce la cartolina con la figura pubblicata nell'articolo del 1922.

La cartolina a Bohr e' una scansione recente, che andrebbe accreditata a chi
l'ha pubblicata. La figura dell'articolo originale di Gerlach e Stern e' invece
di pubblico dominio per eta', e come riferimento in una tesi vale di piu': e' la
fonte primaria.

    python tools/ch1_figura1922.py
"""
from pathlib import Path

PAGINA = Path('publish/01-stern-gerlach.html')

VECCHIA_IMG = ('<img loading="lazy" src="img/pandoc_ch1/cartolina-gerlach-1922.png?v=1" '
               'alt="La cartolina del 1922: a sinistra il deposito senza campo, una riga '
               'sola; a destra con il campo, la riga si apre in una figura a labbra.">')
NUOVA_IMG = ('<img loading="lazy" src="img/pandoc_ch1/gerlach-stern-1922.jpg?v=1" '
             'alt="Il deposito di argento fotografato al microscopio: a sinistra senza '
             'campo, una riga sola; a destra con il campo, la riga si apre al centro.">')

VECCHIA_IT = (
    'La cartolina che Gerlach invi\u00f2 a Bohr l\u20198 febbraio 1922, con '
    'il deposito di argento fotografato al microscopio. A sinistra senza campo '
    'magnetico: una riga sola. A destra con il campo: la riga si apre al centro e '
    'torna a chiudersi alle estremit\u00e0, dove il gradiente si annulla. La scala '
    'micrometrica in basso misura un millimetro; la separazione massima \u00e8 di circa '
    'due decimi. In calce Gerlach scrive: \u00abCi congratuliamo per la conferma della '
    'sua teoria\u00bb.')
NUOVA_IT = (
    'Il risultato dell\u2019esperimento come fu pubblicato da Gerlach e Stern nel 1922: '
    'il deposito di argento fotografato al microscopio. A sinistra senza campo '
    'magnetico, una riga sola \u2014 quello che la fisica classica prevede anche con il '
    'campo acceso. A destra con il campo: la riga si apre al centro e torna a '
    'chiudersi alle estremit\u00e0. La forma a labbra e i contorni sfumati vengono dal '
    'traferro, formato da un\u2019espansione a spigolo vivo e una scanalata: una geometria '
    'che produce un gradiente intenso, ma che varia da punto a punto e si annulla ai '
    'bordi della fenditura. La separazione massima \u00e8 di circa due decimi di '
    'millimetro, un ordine di grandezza meno di quella della figura precedente. '
    '<i>Da W. Gerlach e O. Stern, Zeitschrift f\u00fcr Physik 9, 349 (1922).</i>')

VECCHIA_EN = (
    'The postcard Gerlach sent to Bohr on 8 February 1922, with the '
    'silver deposit photographed under the microscope. On the left, without the '
    'magnetic field: a single line. On the right, with the field: the line opens in '
    'the middle and closes again at the ends, where the gradient vanishes. The '
    'micrometric scale at the bottom spans one millimetre; the maximum separation is '
    'about two tenths. At the foot Gerlach writes: \u201cWe congratulate you on the '
    'confirmation of your theory\u201d.')
NUOVA_EN = (
    'The result of the experiment as published by Gerlach and Stern in 1922: the '
    'silver deposit photographed under the microscope. On the left, without the '
    'magnetic field, a single line \u2014 what classical physics predicts even with the '
    'field on. On the right, with the field: the line opens in the middle and closes '
    'again at the ends. The lip shape and the blurred edges come from the gap, formed '
    'by a knife-edge pole and a grooved one: a geometry that yields a strong gradient '
    'which however varies from point to point and vanishes at the edges of the slit. '
    'The maximum separation is about two tenths of a millimetre, an order of magnitude '
    'less than in the previous figure. '
    '<i>From W. Gerlach and O. Stern, Zeitschrift f\u00fcr Physik 9, 349 (1922).</i>')

src = PAGINA.read_text(encoding='utf-8')
fatti = 0
for vecchio, nuovo in ((VECCHIA_IMG, NUOVA_IMG), (VECCHIA_IT, NUOVA_IT),
                       (VECCHIA_EN, NUOVA_EN)):
    if vecchio in src:
        src = src.replace(vecchio, nuovo, 1)
        fatti += 1
    else:
        print(f'  NON TROVATO: {vecchio[:60]}...')
PAGINA.write_text(src, encoding='utf-8', newline='')
print(f'{fatti} su 3 sostituiti')

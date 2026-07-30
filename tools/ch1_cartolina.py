"""Inserisce nel capitolo 1 la cartolina che Gerlach mando' a Bohr.

Va subito dopo la frase che descrive la figura a labbra, cosi' il lettore la
vede mentre legge in cosa consiste. E' la prova sperimentale originale: a
sinistra il deposito senza campo, una riga sola; a destra con il campo, la riga
che si apre. Il confronto fra le due meta' dice da solo quello che il capitolo
sta sostenendo.

    python tools/ch1_cartolina.py
"""
from pathlib import Path

PAGINA = Path('publish/01-stern-gerlach.html')

ANCORA_IT = ('mentre qui le espansioni sono dimensionate per mantenerlo uniforme '
             'sull\u2019intera larghezza del fascio.')

FIGURA = (
    '\n<figure id="fig-01_stern_gerlach-10" class="fig-inline">'
    '<img loading="lazy" src="img/pandoc_ch1/cartolina-gerlach-1922.png?v=1" '
    'alt="La cartolina del 1922: a sinistra il deposito senza campo, una riga sola; '
    'a destra con il campo, la riga si apre in una figura a labbra.">'
    '<figcaption><b>Fig. 10</b> \u2014 '
    '<span class="it">La cartolina che Gerlach invi\u00f2 a Bohr l\u20198 febbraio 1922, con '
    'il deposito di argento fotografato al microscopio. A sinistra senza campo '
    'magnetico: una riga sola. A destra con il campo: la riga si apre al centro e '
    'torna a chiudersi alle estremit\u00e0, dove il gradiente si annulla. La scala '
    'micrometrica in basso misura un millimetro; la separazione massima \u00e8 di circa '
    'due decimi. In calce Gerlach scrive: \u00abCi congratuliamo per la conferma della '
    'sua teoria\u00bb.</span>'
    '<span class="en">The postcard Gerlach sent to Bohr on 8 February 1922, with the '
    'silver deposit photographed under the microscope. On the left, without the '
    'magnetic field: a single line. On the right, with the field: the line opens in '
    'the middle and closes again at the ends, where the gradient vanishes. The '
    'micrometric scale at the bottom spans one millimetre; the maximum separation is '
    'about two tenths. At the foot Gerlach writes: \u201cWe congratulate you on the '
    'confirmation of your theory\u201d.</span>'
    '</figcaption></figure>')

src = PAGINA.read_text(encoding='utf-8')
if 'cartolina-gerlach-1922' in src:
    print('gia\' inserita')
elif ANCORA_IT not in src:
    print('ATTENZIONE: punto di inserimento non trovato')
else:
    fine = src.index('</p>', src.index(ANCORA_IT)) + len('</p>')
    PAGINA.write_text(src[:fine] + FIGURA + src[fine:], encoding='utf-8', newline='')
    print('inserita come figura 10')

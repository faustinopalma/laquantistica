"""Sposta la sezione sull'algebra a tre dimensioni dal capitolo di matematica a una nota.

Rilanciabile: se la sezione nel capitolo non c'e' piu', non fa nulla.
"""
import pathlib
import re

CAPITOLO = pathlib.Path('sorgenti/bozza-matematica.html')
MODELLO = pathlib.Path('sorgenti/nota-09-perche-numeri-complessi.html')
NOTA = pathlib.Path('sorgenti/nota-14-algebra-tre-dimensioni.html')

INIZIO = ('    <h3><span class="it">Perch\u00e9 non un\u2019algebra a tre dimensioni?</span>'
          '<span class="en">Why not a three-dimensional algebra?</span></h3>\n')
FINE = ('    <h3><span class="it">Il problema agli autovalori</span>'
        '<span class="en">The eigenvalue problem</span></h3>\n')

RICHIAMO = '''    <div class="nota-link" id="nota-14">
<span class="k"><span class="it">Nota 14</span><span class="en">Note 14</span></span>
<span class="it">Nell\u2019elenco il 3 non c\u2019\u00e8, eppure lo spazio in cui viviamo ha tre dimensioni: <a href="nota-14-algebra-tre-dimensioni.html?ret=bozza-matematica.html%23nota-14">perch\u00e9 quell\u2019algebra non esiste \u2192</a></span><span class="en">The list has no 3, yet the space we live in has three dimensions: <a href="nota-14-algebra-tre-dimensioni.html?ret=bozza-matematica.html%23nota-14">why that algebra does not exist \u2192</a></span>
</div>
'''

testo = CAPITOLO.read_text(encoding='utf-8')
if INIZIO not in testo:
    print('la sezione non e\' piu\' nel capitolo: nulla da fare')
    raise SystemExit(0)

i, f = testo.index(INIZIO), testo.index(FINE)
sezione = testo[i + len(INIZIO):f]

testo = testo[:i] + testo[f:]
# il richiamo va dove nasce la domanda, subito sotto la tabella delle quattro algebre
testo = testo.replace('</table>\n', '</table>\n' + RICHIAMO, 1)
CAPITOLO.write_text(testo, encoding='utf-8')

# La nota si regge da sola: l'unico rimando al testo da cui viene e' esplicito.
sezione = sezione.replace('Di questa sezione abbiamo', 'Di questa nota abbiamo')
sezione = sezione.replace('Of this section we have', 'Of this note we have')
sezione = sezione.replace('da cui viene la tabella delle quattro algebre',
                          'da cui viene la tabella delle quattro algebre della scheda')
sezione = sezione.replace('from which the table of the four algebras comes',
                          'from which the table of the four algebras in the chapter comes')
sezione = sezione.replace('il teorema della palla pelosa, che di numeri',
                          'il teorema della palla pelosa (L. E. J. Brouwer, 1912), che di numeri')
sezione = sezione.replace('the hairy ball theorem, which does not speak',
                          'the hairy ball theorem (L. E. J. Brouwer, 1912), which does not speak')

modello = MODELLO.read_text(encoding='utf-8')
testa = modello[:modello.index('    <h1 class="doc-title">')]
coda = modello[modello.index('    <div class="doc-return">'):]

testa = testa.replace('nota-09-perche-numeri-complessi.html', 'nota-14-algebra-tre-dimensioni.html')
testa = re.sub(r'<title>.*?</title>',
               '<title>Nota 14 \u00b7 Perch\u00e9 non un\u2019algebra a tre dimensioni? '
               '\u2014 La Quantistica</title>', testa, count=1, flags=re.S)
testa = re.sub(r'<meta name="description"[^>]*>\n', '', testa, count=1)
testa = testa.replace('<span class="it">Nota 09</span><span class="en">Note 09</span>',
                      '<span class="it">Nota 14</span><span class="en">Note 14</span>')
testa = testa.replace('href="04b-forma-evoluzione.html#nota-9"',
                      'href="bozza-matematica.html#nota-14"')
testa = testa.replace(
    '<span class="cap it">Cap. 03 \u00b7 La forma dell\u2019equazione di evoluzione</span>'
    '<span class="cap en">Ch. 03 \u00b7 The Form of the Evolution Equation</span>',
    '<span class="cap it">Numeri complessi e vettori di stato</span>'
    '<span class="cap en">Complex Numbers and State Vectors</span>')

coda = coda.replace('href="04b-forma-evoluzione.html#nota-9"', 'href="bozza-matematica.html#nota-14"')
coda = coda.replace('Nota N.09', 'Nota N.14').replace('Note No. 09', 'Note No. 14')

titolo = ('    <h1 class="doc-title">\n'
          '      <span class="lead"><span class="it">Una domanda in sospeso</span>'
          '<span class="en">A question left hanging</span></span>\n'
          '      <span class="it">Perch\u00e9 non un\u2019algebra a tre dimensioni?</span>'
          '<span class="en">Why not a three-dimensional algebra?</span>\n'
          '    </h1>\n\n')

NOTA.write_text(testa + titolo + sezione + '\n' + coda, encoding='utf-8')
print(f'nota scritta: {NOTA} ({NOTA.stat().st_size} byte)')
print(f'capitolo aggiornato: {CAPITOLO} ({CAPITOLO.stat().st_size} byte)')

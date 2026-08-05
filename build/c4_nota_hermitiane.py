"""Capitolo 4: alleggerisce il passaggio su A e H e rimanda alla nota 08."""
import re
import sys
from pathlib import Path

F = Path('sorgenti/04-diffrazione.html')
t = F.read_text(encoding='utf-8')

# 1. via il paragrafo sull'analogia con i numeri complessi: il discorso passa nella nota
prima = len(t)
t = re.sub(r'<p><span class="it">La preferenza non è di gusto:.*?</span></p>\n', '', t, count=1, flags=re.S)
if len(t) == prima:
    sys.exit('paragrafo "La preferenza" non trovato')

# 2. via il rimando a K e D: resta la sola sostituzione
coppie = [
    ('è antihermitiana. Per la stessa ragione per cui abbiamo preferito <em>K</em> a <em>D</em>, sostituiamo la matrice',
     'è antihermitiana. Sostituiamo la matrice'),
    ('is anti-Hermitian. For the same reason that made us prefer <em>K</em> to <em>D</em>, we replace the matrix',
     'is anti-Hermitian. We replace the matrix'),
]
for vecchio, nuovo in coppie:
    if vecchio not in t:
        sys.exit(f'non trovato: {vecchio[:60]}')
    t = t.replace(vecchio, nuovo, 1)

# 3. richiamo alla nota dopo il nome dell'equazione
ancora = '<p><span class="it">Quest’equazione viene chiamata equazione di Schrödinger.</span><span class="en">This equation is called the Schrödinger equation.</span></p>\n'
if ancora not in t:
    sys.exit('frase di Schrödinger non trovata')
richiamo = ('<div class="nota-link" id="nota-8">\n'
            '<span class="k"><span class="it">Nota 08</span><span class="en">Note 08</span></span>\n'
            '<span class="it">Perché abbiamo preferito la matrice hermitiana <em>H</em> all’antihermitiana '
            '<em>A</em>, e che cosa sarebbe cambiato tenendo <em>A</em>: '
            '<a href="nota-08-matrici-hermitiane.html?ret=04-diffrazione.html%23nota-8">la scelta →</a></span>'
            '<span class="en">Why we preferred the Hermitian matrix <em>H</em> to the anti-Hermitian '
            '<em>A</em>, and what would have changed had we kept <em>A</em>: '
            '<a href="nota-08-matrici-hermitiane.html?ret=04-diffrazione.html%23nota-8">the choice →</a></span>\n'
            '</div>\n')
t = t.replace(ancora, ancora + richiamo, 1)

F.write_text(t, encoding='utf-8')
print('capitolo 4 aggiornato')

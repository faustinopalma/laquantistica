import re, pathlib
f = pathlib.Path('publish/04-diffrazione.html')
html = f.read_text(encoding='utf-8')

APOS = '\u2019'
def T(s):  # use curly apostrophe as in the file
    return s.replace("'", APOS)

h2 = [
 "Descrizione dell'esperimento e previsioni classiche.",
 "Descrizione dell'apparato sperimentale.",
 "Risultati sperimentali.",
 "Interpretazione dei risultati.",
 "Dualismo onda particella e relazione di De Broglie.",
 "Interpretazione probabilistica.",
 "Algebra degli operatori.",
 "Conservazione del prodotto scalare.",
 "Determinazione della matrice hamiltoniana.",
 "Conclusioni.",
]
h3 = [
 "Equazione di evoluzione temporale in forma differenziale.",
 "Matrice aggiunta e matrici hermitiane, antihermitiane ed unitarie.",
 "Rapporto tra matrici ed operatori.",
 "Funzioni di operatori o funzioni di matrici.",
 "Dimostrazione delle formule 1a, 2a, 3a e 4a.",
]

def slug(s):
    s = s.lower().replace(APOS, '').replace("'", '')
    s = s.replace(',', '')
    s = re.sub(r'[^a-z0-9. ]+', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    return 'sec-' + s

def convert(html, titles, level):
    for it in titles:
        it_c = T(it)
        pat = re.compile(r'<p><span class="it">' + re.escape(it_c) + r'</span><span class="en">(.*?)</span></p>')
        m = pat.search(html)
        if not m:
            print(f'  NOT FOUND (h{level}):', it)
            continue
        n = len(pat.findall(html))
        if n != 1:
            print(f'  WARN {n} matches:', it)
        rep = f'<h{level} id="{slug(it)}"><span class="it">{it_c}</span><span class="en">{m.group(1)}</span></h{level}>'
        html = pat.sub(lambda mm: rep, html, count=1)
        print(f'  h{level} <=', it[:50])
    return html

html = convert(html, h2, 2)
html = convert(html, h3, 3)

# existing lone h2 -> h3 (Vettori e matrici a dimensione infinita)
vt = 'Vettori e matrici a dimensione infinita'
pat = re.compile(r'<h2><span class="it">' + re.escape(vt) + r'</span><span class="en">(.*?)</span></h2>')
m = pat.search(html)
if m:
    html = pat.sub(f'<h3 id="{slug(vt)}"><span class="it">{vt}</span><span class="en">{m.group(1)}</span></h3>', html, count=1)
    print('  h3 <= Vettori e matrici a dimensione infinita (era h2)')
else:
    print('  NOT FOUND existing h2 Vettori...')

f.write_text(html, encoding='utf-8')
print('scritto', f)

"""Numeri decimali nei VERI nodi di testo (non negli attributi: i tracciati SVG
delle formule sono pieni di coppie tipo 3,-2 e non vanno toccati)."""
import collections
import pathlib
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from testo_in_formule2 import coperti, dentro  # noqa: E402

RADICE = pathlib.Path('sorgenti')
DECIMALE = re.compile(r'\d,\d')
SALTA_DENTRO = {'script', 'style', 'annotation'}


class Testi(HTMLParser):
    """Ritorna (offset, testo) di ogni nodo di testo utile."""

    def __init__(self, testo):
        super().__init__(convert_charrefs=False)
        self.testo = testo
        self.inizi = [0]
        for r in testo.splitlines(keepends=True):
            self.inizi.append(self.inizi[-1] + len(r))
        self.pila = []
        self.nodi = []

    def _off(self):
        r, c = self.getpos()
        return self.inizi[r - 1] + c

    def handle_starttag(self, tag, attrs):
        if tag not in ('br', 'img', 'meta', 'link', 'hr', 'input', 'source', 'path', 'use'):
            self.pila.append(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i] == tag:
                del self.pila[i:]
                return

    def handle_data(self, data):
        if not any(t in SALTA_DENTRO for t in self.pila):
            self.nodi.append((self._off(), data))


tot = collections.Counter()
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'class="it"' not in t:
        continue
    fusi = coperti(t)
    p = Testi(t)
    p.feed(t)
    p.close()
    conti = collections.Counter()
    esempi = collections.defaultdict(list)
    for off, dati in p.nodi:
        if not DECIMALE.search(dati):
            continue
        dove = 'dentro marcatore' if dentro(fusi, off) else 'CONDIVISO'
        conti[dove] += 1
        if len(esempi[dove]) < 6:
            esempi[dove] += re.findall(r'\d+,\d+', dati)[:2]
    if conti:
        print(f'{f.name}:')
        for k in sorted(conti):
            print(f'   {conti[k]:>4}  {k}   es. {list(dict.fromkeys(esempi[k]))[:6]}')
        tot.update(conti)

print('\n--- totale nodi di testo con virgola decimale ---')
for k in sorted(tot):
    print(f'   {tot[k]:>4}  {k}')

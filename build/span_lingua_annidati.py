"""Span di lingua annidati dentro l'altra lingua: il contenuto sparisce da entrambi gli alberi."""
from html.parser import HTMLParser
from pathlib import Path


class Potatore(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila = []
        self.annidati = []
        self.script = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.script += 1
        if tag == 'span':
            c = (dict(attrs).get('class') or '').split()
            lingua = 'it' if 'it' in c else ('en' if 'en' in c else None)
            if lingua and not self.script:
                for esterna in self.pila:
                    if esterna:
                        if esterna != lingua:
                            self.annidati.append((esterna, lingua, self.getpos()))
                        break
            self.pila.append(lingua)

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.script:
            self.script -= 1
        if tag == 'span' and self.pila:
            self.pila.pop()


tot = 0
for f in sorted(Path('sorgenti').glob('*.html')):
    p = Potatore()
    p.feed(f.read_text(encoding='utf-8'))
    if p.annidati:
        tot += len(p.annidati)
        print(f'{f.name}: {len(p.annidati)}')
        for esterna, interna, pos in p.annidati:
            print(f'    .{interna} dentro .{esterna}  riga {pos[0]} colonna {pos[1]}')
print(f'totale: {tot}')

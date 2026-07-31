"""Censimento della struttura bilingue: cosa dovra' gestire lo splitter."""
import collections
import pathlib
import re

from html.parser import HTMLParser

PAGINE = sorted(p for p in pathlib.Path('publish').glob('*.html'))


class Censimento(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.tag_lang = collections.Counter()   # (tag, lingua) -> n
        self.annidati = []                      # .it dentro .en o viceversa
        self.entrambe = []                      # elemento con class it E en
        self.profondita_max = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cls = (d.get('class') or '').split()
        lingua = None
        if 'it' in cls and 'en' in cls:
            self.entrambe.append((tag, d.get('class')))
        elif 'it' in cls:
            lingua = 'it'
        elif 'en' in cls:
            lingua = 'en'
        if lingua:
            self.tag_lang[(tag, lingua)] += 1
            for t, l in self.stack:
                if l:
                    self.annidati.append((t, l, tag, lingua))
        if tag not in ('br', 'img', 'meta', 'link', 'hr', 'input', 'source'):
            self.stack.append((tag, lingua))
            self.profondita_max = max(self.profondita_max, len(self.stack))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


tot = collections.Counter()
print(f'{"pagina":<38} {"it":>5} {"en":>5}  titolo')
for p in PAGINE:
    t = p.read_text(encoding='utf-8')
    c = Censimento()
    c.feed(t)
    n_it = sum(v for (tag, l), v in c.tag_lang.items() if l == 'it')
    n_en = sum(v for (tag, l), v in c.tag_lang.items() if l == 'en')
    tot.update({(tag, l): v for (tag, l), v in c.tag_lang.items()})
    titolo = re.search(r'<title>(.*?)</title>', t, re.S)
    titolo = titolo.group(1).strip() if titolo else '(nessuno)'
    print(f'{p.name:<38} {n_it:>5} {n_en:>5}  {titolo[:60]}')
    if c.entrambe:
        print(f'    !! class it+en insieme: {c.entrambe[:3]}')
    if c.annidati:
        print(f'    !! annidati: {c.annidati[:3]}')
    if n_it != n_en:
        print(f'    !! squilibrio it/en: {n_it} vs {n_en}')

print('\n--- tag portatori di lingua (tutte le pagine) ---')
per_tag = collections.Counter()
for (tag, l), v in tot.items():
    per_tag[tag] += v
for tag, v in per_tag.most_common():
    print(f'  <{tag}>  {v}')

print('\n--- altre cose da gestire ---')
for p in PAGINE:
    t = p.read_text(encoding='utf-8')
    note = []
    if 'lang.js' in t:
        note.append('lang.js')
    if 'lang.css' in t:
        note.append('lang.css')
    if 'langsw' in t:
        note.append('selettore')
    if 'canonical' not in t:
        note.append('SENZA canonical')
    if 'name="description"' in t:
        note.append('description')
    if '?ret=' in t:
        note.append('?ret')
    if 'hreflang' in t:
        note.append('hreflang gia presente')
    print(f'  {p.name:<38} {", ".join(note)}')

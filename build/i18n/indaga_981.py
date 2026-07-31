import html
import pathlib
import re

t = pathlib.Path('sorgenti/03-elettroni.html').read_text(encoding='utf-8')
print('elementi con 9,81 o 9.81 nel data-tex:')
for m in re.finditer(r'data-tex="([^"]*)"', t):
    tex = html.unescape(m.group(1))
    if '9,81' in tex or '9.81' in tex or '9{,}81' in tex:
        apertura = t.rfind('<span', 0, m.start())
        classi = re.search(r'class="([^"]*)"', t[apertura:m.start()])
        print(f'  offset {m.start()}  class="{classi.group(1) if classi else "?"}"')
        print(f'     {tex[:120].replace(chr(10), " ")}')
print()
i = t.find('9,81')
if i < 0:
    i = t.find('9{,}81')
apertura = t.rfind('<div class="equation"', 0, i)
print('contorno del blocco:')
print(t[apertura:apertura + 320].replace('\n', ' '))

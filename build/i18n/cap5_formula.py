import pathlib
import re

t = pathlib.Path('publish/05-rutherford.html').read_text(encoding='utf-8')
for chiave in ('Particelle per unit', 'Particles per unit'):
    i = t.find(f'\\text{{{chiave}')
    # risalgo all'inizio dell'elemento .equation o .eq-inline che la contiene
    inizio = max(t.rfind('<div class="equation"', 0, i), t.rfind('<span class="eq-', 0, i),
                 t.rfind('<p', 0, i))
    print(f'=== {chiave} (offset {i}) ===')
    print(repr(t[inizio - 260:inizio + 120]))
    print()
print('--- data-tex delle due formule ---')
for m in re.finditer(r'data-tex="([^"]*Particell?e?s? per unit[^"]*)"', t):
    print('  ', m.group(1)[:100])

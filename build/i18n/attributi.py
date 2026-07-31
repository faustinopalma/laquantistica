"""Inventario del testo che vive negli ATTRIBUTI (alt, aria-label, title...).

Non essendo elementi, non si possono sdoppiare con gli span: restano uguali in
entrambe le lingue. Qui si conta quanti sono, dove stanno e in che lingua sono.
"""
import collections
import pathlib
import re

RADICE = pathlib.Path('sorgenti')
ATTRIBUTI = ('alt', 'aria-label', 'title', 'placeholder', 'aria-description')

# parole che tradiscono la lingua
IT = re.compile(r'\b(del|della|dello|degli|delle|nel|nella|con|per|sul|sulla|una|uno|gli|dei|'
                r'che|non|piu|più|fra|tra|dopo|prima|verso|senza|come|dove|quando|esperimento|'
                r'campo|fascio|schema|figura|apparato|macchina|misura|grafico|tensione|corrente|'
                r'lingua|torna|indietro|salta|contenuto|capitolo)\b', re.I)
EN = re.compile(r'\b(the|of|with|for|from|and|but|into|onto|after|before|without|about|where|'
                r'when|experiment|field|beam|diagram|figure|apparatus|machine|measurement|chart|'
                r'voltage|current|language|back|skip|content|chapter)\b', re.I)

conta = collections.Counter()
per_pagina = collections.defaultdict(list)

for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    # gli attributi dentro <script> sono stringhe JS: li guardo a parte
    fuori_script = re.sub(r'<script\b.*?</script>', lambda m: ' ' * len(m.group(0)), t, flags=re.S)
    for a in ATTRIBUTI:
        for m in re.finditer(rf'\b{a}="([^"]*)"', fuori_script):
            v = m.group(1).strip()
            if not v:
                conta['vuoto'] += 1
                per_pagina[f.name].append((a, 'VUOTO', ''))
                continue
            it, en = bool(IT.search(v)), bool(EN.search(v))
            lingua = 'italiano' if it and not en else 'inglese' if en and not it else \
                     'ambiguo' if it and en else 'neutro'
            conta[lingua] += 1
            per_pagina[f.name].append((a, lingua, v))

print('--- riepilogo ---')
for k, v in conta.most_common():
    print(f'  {v:>4}  {k}')

print('\n--- quelli in italiano, per pagina ---')
tot = 0
for nome, voci in per_pagina.items():
    ita = [(a, v) for a, l, v in voci if l == 'italiano']
    if ita:
        tot += len(ita)
        print(f'{nome}: {len(ita)}')
        for a, v in ita[:4]:
            print(f'      {a}="{v[:78]}"')
        if len(ita) > 4:
            print(f'      ... e altri {len(ita) - 4}')
print(f'\ntotale attributi in italiano: {tot}')

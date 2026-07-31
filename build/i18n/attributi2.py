import collections
import pathlib
import re

RADICE = pathlib.Path('sorgenti')
ATTRIBUTI = ('alt', 'aria-label', 'title', 'placeholder', 'aria-description')
IT = re.compile(r'\b(del|della|dello|degli|delle|nel|nella|con|per|sul|sulla|una|uno|gli|dei|'
                r'che|non|piu|più|fra|tra|dopo|prima|verso|senza|come|dove|quando|esperimento|'
                r'campo|fascio|schema|figura|apparato|macchina|misura|grafico|tensione|corrente|'
                r'lingua|torna|indietro|salta|contenuto|capitolo)\b', re.I)
EN = re.compile(r'\b(the|of|with|for|from|and|but|into|onto|after|before|without|about|where|'
                r'when|experiment|field|beam|diagram|figure|apparatus|machine|measurement|chart|'
                r'voltage|current|language|back|skip|content|chapter)\b', re.I)

gruppi = collections.defaultdict(list)
for f in sorted(RADICE.glob('*.html')):
    t = re.sub(r'<script\b.*?</script>', lambda m: ' ' * len(m.group(0)),
               f.read_text(encoding='utf-8'), flags=re.S)
    for a in ATTRIBUTI:
        for m in re.finditer(rf'\b{a}="([^"]*)"', t):
            v = m.group(1).strip()
            if not v:
                gruppi['vuoto'].append((f.name, a, ''))
                continue
            it, en = bool(IT.search(v)), bool(EN.search(v))
            l = 'italiano' if it and not en else 'inglese' if en and not it else \
                'ambiguo' if it and en else 'neutro'
            if l != 'italiano':
                gruppi[l].append((f.name, a, v))

for l in ('ambiguo', 'neutro', 'inglese', 'vuoto'):
    print(f'===== {l} ({len(gruppi[l])}) =====')
    visti = set()
    for nome, a, v in gruppi[l]:
        k = (a, v)
        if k in visti:
            continue
        visti.add(k)
        print(f'   [{nome}] {a}="{v[:85]}"')

"""Cosa manca alle pagine per essere trovate e condivise bene."""
import collections
import pathlib
import re

conta = collections.Counter()
senza_descrizione = []

for lingua in ('it', 'en'):
    for f in sorted((pathlib.Path('publish') / lingua).glob('*.html')):
        t = f.read_text(encoding='utf-8')
        testa = t[:t.find('</head>')]
        if not re.search(r'<meta name="description"', testa):
            conta[f'{lingua}: senza descrizione'] += 1
            senza_descrizione.append(f'{lingua}/{f.name}')
        if 'og:title' not in testa:
            conta[f'{lingua}: senza anteprima social (og:)'] += 1
        if 'application/ld+json' not in testa:
            conta[f'{lingua}: senza dati strutturati'] += 1

for k in sorted(conta):
    print(f'  {conta[k]:>3}  {k}')

print(f'\npagine senza descrizione ({len(senza_descrizione)}):')
print('   ', ', '.join(n.split("/")[1].replace(".html", "") for n in senza_descrizione if n.startswith('it/')))

print('\nimmagine di anteprima disponibile?')
for c in ['publish/img/pandoc_ch1/vetrino-simulato.png', 'publish/assets']:
    p = pathlib.Path(c)
    print(f'   {c}: {"c e" if p.exists() else "assente"}')

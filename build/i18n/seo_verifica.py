"""Controlla i dati strutturati e le anteprime di condivisione."""
import html
import json
import pathlib
import re

errori = []
for lingua in ('it', 'en'):
    n_ld = n_og = 0
    for f in sorted((pathlib.Path('publish') / lingua).glob('*.html')):
        t = f.read_text(encoding='utf-8')
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            n_ld += 1
            try:
                d = json.loads(m.group(1))
            except json.JSONDecodeError as e:
                errori.append(f'{lingua}/{f.name}: JSON non valido ({e})')
                continue
            if '@context' not in d or '@type' not in d:
                errori.append(f'{lingua}/{f.name}: manca @context o @type')
            if d.get('inLanguage') not in (lingua, None):
                errori.append(f'{lingua}/{f.name}: inLanguage = {d.get("inLanguage")}')
        og = dict(re.findall(r'<meta property="(og:[^"]+)" content="([^"]*)"', t))
        if og:
            n_og += 1
            for k in ('og:title', 'og:description', 'og:url', 'og:image'):
                if not og.get(k):
                    errori.append(f'{lingua}/{f.name}: manca {k}')
            if f'/{lingua}/' not in og.get('og:url', ''):
                errori.append(f'{lingua}/{f.name}: og:url = {og["og:url"]}')
            if f'copertina-{lingua}' not in og.get('og:image', ''):
                errori.append(f'{lingua}/{f.name}: og:image = {og.get("og:image")}')
            if len(html.unescape(og.get('og:description', ''))) > 200:
                errori.append(f'{lingua}/{f.name}: descrizione troppo lunga')
    print(f'albero {lingua}: {n_ld} blocchi di dati strutturati, {n_og} pagine con anteprima')

print(f'\nerrori: {len(errori)}')
for e in errori[:12]:
    print(f'  !! {e}')

print('\n--- esempio: indice italiano ---')
t = (pathlib.Path('publish/it/index.html')).read_text(encoding='utf-8')
d = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S).group(1))
print('  @type      :', d['@type'])
print('  insegna    :', len(d['teaches']), 'argomenti')
print('  capitoli   :', len(d['hasPart']))
print('  basato su  :', d['isBasedOn']['name'], '-', d['isBasedOn']['sourceOrganization']['name'])
print('  descrizione:', d['description'][:150], '...')

"""Aggiorna publish/staticwebapp.config.json: i vecchi indirizzi (senza lingua)
devono portare alla versione italiana, che e' quella dei lettori esistenti.
"""
import json
import pathlib

CONFIG = pathlib.Path('publish/staticwebapp.config.json')
c = json.loads(CONFIG.read_text(encoding='utf-8'))

pagine = [p.name[:-5] for p in sorted(pathlib.Path('sorgenti').glob('*.html'))
          if not p.name.startswith('_') and not p.name.startswith('game-')
          and p.name != 'index.html']

teste = [r for r in c['routes'] if 'headers' in r]
# storiche = rimandi da indirizzi che non corrispondono a una pagina attuale (es. /sim-esp1):
# vanno conservati fra un'esecuzione e l'altra, altrimenti si perdono. Si scartano pero'
# quelli che puntano a una pagina non piu' esistente.
attuali = {f'/{n}' for n in pagine} | {f'/{n}.html' for n in pagine}
bersagli = {f'/it/{n}' for n in pagine} | {f'/en/{n}' for n in pagine}
storiche = [r for r in c['routes']
            if 'redirect' in r and r['route'] not in attuali and r['redirect'] in bersagli]

nuove = []
for nome in pagine:
    nuove.append({'route': f'/{nome}', 'redirect': f'/it/{nome}', 'statusCode': 301})
    nuove.append({'route': f'/{nome}.html', 'redirect': f'/it/{nome}', 'statusCode': 301})

c['routes'] = teste + storiche + nuove
c['responseOverrides'] = {'404': {'rewrite': '/index.html', 'statusCode': 404}}

CONFIG.write_text(json.dumps(c, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'regole: {len(teste)} intestazioni + {len(storiche)} storiche + {len(nuove)} per le pagine')
for r in c['routes'][:4] + c['routes'][-2:]:
    print('  ', json.dumps(r, ensure_ascii=False))

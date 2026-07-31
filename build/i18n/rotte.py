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

# tolgo eventuali regole gia' aggiunte da una esecuzione precedente
c['routes'] = [r for r in c['routes'] if not str(r.get('redirect', '')).startswith('/it/')]

vecchie = [r for r in c['routes'] if 'redirect' in r]
nuove = []
for r in vecchie:                      # i vecchi rimandi puntavano a pagine senza lingua
    bersaglio = r['redirect'].replace('.html', '').lstrip('/')
    r['redirect'] = f'/it/{bersaglio}'
for nome in pagine:
    nuove.append({'route': f'/{nome}', 'redirect': f'/it/{nome}', 'statusCode': 301})
    nuove.append({'route': f'/{nome}.html', 'redirect': f'/it/{nome}', 'statusCode': 301})

teste = [r for r in c['routes'] if 'headers' in r]
c['routes'] = teste + vecchie + nuove
c['responseOverrides'] = {'404': {'rewrite': '/index.html', 'statusCode': 404}}

CONFIG.write_text(json.dumps(c, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'regole: {len(teste)} intestazioni + {len(vecchie)} storiche + {len(nuove)} nuove')
for r in c['routes'][:4] + c['routes'][-2:]:
    print('  ', json.dumps(r, ensure_ascii=False))

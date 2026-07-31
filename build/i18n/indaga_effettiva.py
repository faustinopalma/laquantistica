import pathlib
import re

for percorso in ['publish/v2/en/05-rutherford.html', 'publish/v2/it/05-rutherford.html']:
    t = pathlib.Path(percorso).read_text(encoding='utf-8')
    print(f'=== {percorso} ===')
    for parola in ['Effettiva', 'Effective', 'Unitaria', 'Unit}', 'Verificata', 'Verified']:
        n = len(re.findall(rf'data-tex="[^"]*{parola}', t))
        print(f'   data-tex con "{parola}": {n}')
    for m in re.finditer(r'data-tex="([^"]*Effettiva[^"]*)"', t):
        i = m.start()
        apertura = t.rfind('<span', 0, i)
        print('   contesto:', t[apertura:i][:120])
        print('   tex     :', m.group(1)[:130].replace('\n', ' '))

import html
import pathlib
import re

MIGLIAIA = re.compile(r'\b\d{1,3},\d{3}\b')
DECIMALE = re.compile(r'\d,\d')

for f in sorted(pathlib.Path('sorgenti').glob('*.html')):
    t = f.read_text(encoding='utf-8')
    ripulito = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', t, flags=re.S)
    m = MIGLIAIA.findall(ripulito)
    if m:
        print(f'{f.name}: possibili separatori di migliaia {sorted(set(m))[:8]}')

print('--- controllo: virgole con piu di 2 cifre dopo (sospette) ---')
for f in sorted(pathlib.Path('sorgenti').glob('*.html')):
    t = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', f.read_text(encoding='utf-8'), flags=re.S)
    lunghe = sorted(set(re.findall(r'\b\d+,\d{3,}\b', t)))
    if lunghe:
        print(f'  {f.name}: {lunghe[:10]}')
print('(nessuna riga sopra = nessun separatore di migliaia)')

"""Confronta il numero di formule prima e dopo: deve crescere solo delle
formule condivise che sono state sdoppiate."""
import pathlib
import re
import subprocess

ATTESE = {'03-elettroni.html': 1, '05-rutherford.html': 2}   # condivise sdoppiate

ok = True
for p in sorted(pathlib.Path('sorgenti').glob('*.html')):
    ora = len(re.findall('data-tex', p.read_text(encoding='utf-8')))
    r = subprocess.run(['git', 'show', f'HEAD:sorgenti/{p.name}'],
                       capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        continue
    prima = len(re.findall('data-tex', r.stdout))
    atteso = prima + ATTESE.get(p.name, 0)
    stato = 'ok' if ora == atteso else f'!! atteso {atteso}'
    if ora != atteso:
        ok = False
    if prima or ora:
        print(f'{p.name:<38} prima {prima:>4}  ora {ora:>4}  {stato}')
print('\nesito:', 'nessuna duplicazione' if ok else 'ATTENZIONE: conteggi non tornano')

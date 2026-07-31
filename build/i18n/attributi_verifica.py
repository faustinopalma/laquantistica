"""Controlli sugli attributi per lingua nei due alberi generati."""
import collections
import pathlib
import re

USCITA = pathlib.Path('publish')
ATTRIBUTI = ('alt', 'aria-label', 'title', 'placeholder')
IT = re.compile(r'\b(del|della|dello|degli|delle|nel|nella|con|per|sul|una|uno|gli|dei|che|non|'
                r'piu|più|dopo|prima|senza|come|dove|quando|esperimento|campo|fascio|schema|'
                r'figura|apparato|macchina|misura|grafico|tensione|corrente|foto|ampolla|'
                r'immagine|schermo|angolo|reticolo|lampada|banco|vetrino|deposito)\b', re.I)

errori = []
for lingua in ('it', 'en'):
    conta = collections.Counter()
    for f in sorted((USCITA / lingua).glob('*.html')):
        t = f.read_text(encoding='utf-8')

        if '-en="' in t:
            errori.append(f'{lingua}/{f.name}: attributi -en non risolti')

        for tag in re.finditer(r'<[a-zA-Z][^>]*>', t):
            for a in ATTRIBUTI:
                if len(re.findall(rf'\s{a}="', tag.group(0))) > 1:
                    errori.append(f'{lingua}/{f.name}: attributo {a} doppio in {tag.group(0)[:70]}')

        senza_script = re.sub(r'<script\b.*?</script>', ' ', t, flags=re.S)
        for a in ATTRIBUTI:
            for m in re.finditer(rf'\s{a}="([^"]*)"', senza_script):
                v = m.group(1).strip()
                if v and IT.search(v):
                    conta[a] += 1
                    if lingua == 'en' and conta[a] <= 3:
                        print(f'   en/{f.name}: {a}="{v[:70]}"')
    print(f'albero {lingua}: attributi ancora in italiano -> {dict(conta) or "nessuno"}')

print(f'\nerrori: {len(errori)}')
for e in errori[:10]:
    print(f'  !! {e}')

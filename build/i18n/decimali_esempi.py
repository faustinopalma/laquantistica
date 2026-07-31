import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from testo_in_formule2 import coperti, dentro  # noqa: E402

RADICE = pathlib.Path('sorgenti')
DECIMALE = re.compile(r'\d[.,]\d')

for nome in ['03-elettroni.html', '04-diffrazione.html', '05-rutherford.html',
             '08-effetto-fotoelettrico.html', 'nota-tecnica-01-stern-gerlach.html',
             'lab-08-fotoelettrico.html']:
    t = (RADICE / nome).read_text(encoding='utf-8')
    fusi = coperti(t)
    ripulito = re.sub(r'<script\b.*?</script>|<style\b.*?</style>|<span class="katex".*?</span></span>',
                      lambda m: ' ' * len(m.group(0)), t, flags=re.S)
    print(f'===== {nome} =====')
    visti = 0
    for m in re.finditer(r'>([^<>]{2,})<', ripulito):
        if not DECIMALE.search(m.group(1)) or dentro(fusi, m.start()):
            continue
        visti += 1
        if visti > 4:
            continue
        pre = t[max(0, m.start() - 130):m.start()].replace('\n', ' ')
        print(f'   contesto: ...{pre[-120:]}')
        print(f'   testo   : {m.group(1)[:110].strip()}')
    print(f'   (in tutto {visti} tratti di testo)')
    for m in re.finditer(r'data-tex="([^"]*)"', t):
        tex = html.unescape(m.group(1))
        if DECIMALE.search(tex) and not dentro(fusi, m.start()):
            print(f'   FORMULA fuori: {tex[:110]}')

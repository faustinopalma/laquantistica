import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from testo_in_formule2 import coperti, dentro  # noqa: E402

RADICE = pathlib.Path('publish')
BERSAGLI = {'04-diffrazione.html': [901382],
            '05-rutherford.html': [434928, 462609, 965690, 978191, 991305, 1013929, 1308445],
            '08-effetto-fotoelettrico.html': [33870]}

for nome, offsets in BERSAGLI.items():
    t = (RADICE / nome).read_text(encoding='utf-8')
    print(f'===== {nome} =====')
    for off in offsets:
        m = re.match(r'data-tex="([^"]*)"', t[off:])
        tex = html.unescape(m.group(1))
        apertura = t.rfind('<span', 0, off)
        classi = re.search(r'class="([^"]*)"', t[apertura:off]).group(1)
        print(f'--- offset {off}  class="{classi}" ---')
        print(tex)
        print()

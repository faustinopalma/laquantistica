"""Scheda 8: le unita' della costante di Planck sono J s, non (J s)^2,
e la frequenza di soglia e' 4,0*10^14 Hz, non 10^-14."""
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

P = Path('sorgenti/08-effetto-fotoelettrico.html')
s = P.read_text(encoding='utf-8')

CAMBI = {
    '3.6\\cdot10^{-15}\\ {\\text{eV}\\:\\mathrm{s}}^2\\equiv5.8\\cdot10^{-34}\\ {\\mathrm{J}\\:\\mathrm{s}}^2':
        '3.6\\cdot10^{-15}\\ \\text{eV}\\:\\mathrm{s}\\equiv5.8\\cdot10^{-34}\\ \\mathrm{J}\\:\\mathrm{s}',
    '6{,}6\\cdot10^{-34}\\:{\\mathrm{J}\\:\\mathrm{s}}^2': '6{,}6\\cdot10^{-34}\\:\\mathrm{J}\\:\\mathrm{s}',
    '6.6\\cdot10^{-34}\\:{\\mathrm{J}\\:\\mathrm{s}}^2': '6.6\\cdot10^{-34}\\:\\mathrm{J}\\:\\mathrm{s}',
    '4{,}0\\cdot10^{-14}\\ \\text{Hz}': '4{,}0\\cdot10^{14}\\ \\text{Hz}',
    '4.0\\cdot10^{-14}\\ \\text{Hz}': '4.0\\cdot10^{14}\\ \\text{Hz}',
}

richieste = [{'i': k, 'tex': n, 'display': False} for k, n in enumerate(CAMBI.values())]
r = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps(richieste), capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    raise SystemExit(r.stderr)
reso = {}
for x in json.loads(r.stdout):
    if 'err' in x:
        raise SystemExit('%s\n%s' % (richieste[x['i']]['tex'], x['err']))
    reso[richieste[x['i']]['tex']] = x['html']

fatte = 0
for vecchio, nuovo in CAMBI.items():
    while True:
        i = s.find('data-tex="%s"' % vecchio)
        if i < 0:
            break
        a = s.rfind('<span class="', 0, i)
        b = fine_span(s, a)
        apertura = s[a:s.find('>', i) + 1].replace(vecchio, nuovo)
        s = s[:a] + apertura + reso[nuovo] + '</span>' + s[b:]
        fatte += 1

assert fatte == len(CAMBI), f'{fatte} sostituzioni su {len(CAMBI)}'
assert s.count('<span') == s.count('</span>')
P.write_text(s, encoding='utf-8', newline='')
print(f'scheda 8: {fatte} unita\u2019 corrette')

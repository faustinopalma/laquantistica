"""Immagini pubblicate ma mai richiamate da nessuna pagina.

Si guarda solo cio' che finisce online: i file di publish/ tracciati da git. Il
confronto e' sul nome del file, cosi' prende anche i richiami dentro il
JavaScript dei laboratori o nel CSS, non solo gli attributi src.
Con --togli le rimuove (git rm: restano nella cronologia).
"""
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

tracciati = [t for t in subprocess.run(['git', 'ls-files', 'publish'], cwd=BASE,
                                       capture_output=True, text=True, check=True).stdout.split('\n') if t]

IMMAGINI = {'.jpg', '.jpeg', '.png', '.svg', '.gif', '.webp', '.ico'}
TESTI = {'.html', '.css', '.js', '.xml', '.json', '.txt', '.webmanifest'}

immagini = [BASE / t for t in tracciati if Path(t).suffix.lower() in IMMAGINI]
tutto = '\n'.join((BASE / t).read_text(encoding='utf-8', errors='ignore')
                  for t in tracciati if Path(t).suffix.lower() in TESTI)

orfane = [f for f in immagini if not re.search(re.escape(f.name), tutto)]

per_cartella = defaultdict(list)
for f in orfane:
    per_cartella[f.parent.relative_to(BASE / 'publish').as_posix()].append(f)

peso = sum(f.stat().st_size for f in orfane)
print(f'immagini pubblicate: {len(immagini)} — mai richiamate: {len(orfane)} ({peso / 1024 / 1024:.1f} MB)')
for c in sorted(per_cartella):
    p = sum(f.stat().st_size for f in per_cartella[c]) / 1024
    print(f'  {c:<32}{len(per_cartella[c]):>5}{p:>8.0f} kB')

if '--togli' not in sys.argv:
    sys.exit(0)

percorsi = [f.relative_to(BASE).as_posix() for f in orfane]
for i in range(0, len(percorsi), 100):
    subprocess.run(['git', 'rm', '--quiet', '--'] + percorsi[i:i + 100], cwd=BASE, check=True)
print(f'rimosse: {len(percorsi)}')

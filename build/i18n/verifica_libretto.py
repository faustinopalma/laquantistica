"""Controlli di coerenza sulla trascrizione del libretto.

Non puo' dire se ho letto bene, ma puo' dire se cio' che ho letto sta in piedi:
date fuori dal periodo di studi, ordine cronologico, voti fuori scala.
"""
import datetime
import re
import pathlib

TESTO = pathlib.Path('librettouniversitario/trascrizione.md').read_text(encoding='utf-8')

IMMATRICOLAZIONE = datetime.date(1993, 11, 1)
LAUREA = datetime.date(1999, 5, 28)

righe = []
for m in re.finditer(r'^\| (\d+) \| (.+?) \| \*{0,2}(\d{2}/\d{2}/\d{2})\*{0,2}.*?\| (.+?) \|', TESTO, re.M):
    n, materia, data, voto = m.groups()
    g, me, a = (int(x) for x in data.split('/'))
    anno = 1900 + a if a >= 80 else 2000 + a
    righe.append((int(n), materia.strip(), datetime.date(anno, me, g), voto.strip()))

print(f'esami trascritti: {len(righe)}')

print('\n--- date fuori dal periodo di studi ---')
fuori = [r for r in righe if not (IMMATRICOLAZIONE <= r[2] <= LAUREA)]
for n, materia, d, _ in fuori:
    print(f'  !! {n:>2}. {materia[:52]:<52} {d}  (immatricolato {IMMATRICOLAZIONE}, laureato {LAUREA})')
if not fuori:
    print('  nessuna')

print('\n--- ordine non cronologico rispetto alla voce precedente ---')
for (n1, m1, d1, _), (n2, m2, d2, _) in zip(righe, righe[1:]):
    if d2 < d1:
        print(f'  .  {n2:>2}. {m2[:44]:<44} {d2}  viene dopo {m1[:26]} {d1}')

print('\n--- stessa data per piu esami ---')
per_data = {}
for n, m, d, _ in righe:
    per_data.setdefault(d, []).append(m)
for d, ms in sorted(per_data.items()):
    if len(ms) > 1:
        print(f'  .  {d}: {", ".join(x[:40] for x in ms)}')

print('\n--- voti fuori scala ---')
strani = []
for n, m, d, v in righe:
    v = v.replace('**', '').strip()
    if re.fullmatch(r'\d{2}/30', v):
        if not 18 <= int(v[:2]) <= 30:
            strani.append((n, m, v))
    elif not re.search(r'lode|ventisette|trenta', v, re.I):
        strani.append((n, m, v))
for n, m, v in strani:
    print(f'  !! {n}. {m[:50]}: "{v}"')
if not strani:
    print('  nessuno')

print('\n--- distribuzione dei voti ---')
conta = {}
for _, _, _, v in righe:
    v = v.replace('**', '').strip()
    chiave = 'lode' if 'lode' in v.lower() else v
    conta[chiave] = conta.get(chiave, 0) + 1
for k, c in sorted(conta.items(), key=lambda x: -x[1]):
    print(f'   {c:>2}x  {k}')

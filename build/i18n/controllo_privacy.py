"""Controlla cosa e' tracciato da git e non dovrebbe esserlo.

Il deposito e' PUBBLICO: tutto cio' che e' tracciato e' leggibile da chiunque.
Cerca segreti, dati personali e documenti di lavoro riservati.
"""
import re
import subprocess
from collections import defaultdict

tracciati = subprocess.run(['git', 'ls-files'], capture_output=True, text=True,
                           encoding='utf-8').stdout.splitlines()
print(f'file tracciati: {len(tracciati)}')

SOSPETTI_NOME = [
    (re.compile(r'(^|/)(privato|librettouniversitario|corrispondenza|bozze|private|personale)/', re.I),
     'cartella di lavoro o personale'),
    (re.compile(r'\.(pem|key|pfx|p12|ovpn|kdbx)$', re.I), 'file di chiavi'),
    (re.compile(r'(^|/)\.env|secrets?\.(json|ya?ml|txt)$', re.I), 'file di configurazione con segreti'),
    (re.compile(r'(^|/)\.azure', re.I), 'credenziali Azure'),
    (re.compile(r'(libretto|pergamena|laurea|certificate|carta.?identita|passaporto)', re.I),
     'documento personale'),
]

SEGRETI = [
    (re.compile(rb'(?i)\b(gh[pousr]_[A-Za-z0-9]{20,})'), 'token GitHub'),
    (re.compile(rb'(?i)\bsk-[A-Za-z0-9]{20,}'), 'chiave OpenAI'),
    (re.compile(rb'(?i)AKIA[0-9A-Z]{16}'), 'chiave AWS'),
    (re.compile(rb'(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----'), 'chiave privata'),
    (re.compile(rb'(?i)\b(password|passwd|pwd|secret|api[-_]?key|token)\s*[:=]\s*["\']?[^\s"\'<>{}]{8,}'),
     'possibile credenziale'),
    (re.compile(rb'(?i)DefaultEndpointsProtocol=.*AccountKey='), 'stringa di connessione Azure'),
    (re.compile(rb'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'), 'indirizzo email'),
]

print('\n=== file dal nome sospetto ===')
trovati = False
for f in tracciati:
    for schema, perche in SOSPETTI_NOME:
        if schema.search(f):
            print(f'  !! {f}   ({perche})')
            trovati = True
if not trovati:
    print('  nessuno')

print('\n=== contenuti sospetti nei file tracciati ===')
risultati = defaultdict(set)
for f in tracciati:
    try:
        with open(f, 'rb') as fh:
            dati = fh.read(400_000)
    except OSError:
        continue
    if b'\x00' in dati[:2000]:
        continue
    for schema, perche in SEGRETI:
        for m in schema.finditer(dati):
            testo = m.group(0).decode('utf-8', 'replace')[:70]
            risultati[perche].add((f, testo))

for perche, voci in sorted(risultati.items()):
    print(f'\n  {perche}: {len(voci)} occorrenze')
    for f, testo in sorted(voci)[:8]:
        print(f'     {f}: {testo}')
    if len(voci) > 8:
        print(f'     ... e altre {len(voci) - 8}')
if not risultati:
    print('  nessuno')

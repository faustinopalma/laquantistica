"""Allinea al nuovo ordine di lettura i numeri di capitolo citati dalle pagine
di laboratorio e dalla nota tecnica.

Quelle pagine scrivono il numero a mano ("Torna al Capitolo 1", "Lab . Cap. 3",
"Cap. 01" nel pie'), e dopo il riordino mostravano ancora la numerazione del 1999.
Qui il numero viene ricalcolato dalla lista SCHEDE, cosi' un prossimo riordino
si sistema rilanciando questo script.

    python build/numeri_lab.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ordine_schede import SCHEDE  # noqa: E402

POSIZIONE = {slug: i + 1 for i, (slug, _, _) in enumerate(SCHEDE)}

# A quale scheda appartiene ciascuna pagina secondaria. Il prefisso del nome
# conserva la numerazione del 1999, che non e' piu' quella di lettura.
APPARTENENZA = {
    'lab-01-stern-gerlach': '01-stern-gerlach.html',
    'lab-02a-sg-angolo-relativo': '02-stern-gerlach-cascata.html',
    'lab-02b-sg-tre-macchine': '02-stern-gerlach-cascata.html',
    'lab-02c-sg-ricombinazione': '02-stern-gerlach-cascata.html',
    'lab-02d-sg-sfasamento': '02-stern-gerlach-cascata.html',
    'lab-03a-corrente-vuoto': '03-elettroni.html',
    'lab-03b-deflessione-em': '03-elettroni.html',
    'lab-03c-millikan': '03-elettroni.html',
    'lab-04-diffrazione': '04-diffrazione.html',
    'lab-05-rutherford': '05-rutherford.html',
    'lab-07-franck-hertz': '07-franck-hertz.html',
    'lab-08-fotoelettrico': '08-effetto-fotoelettrico.html',
    'lab-09-spettri': '09-spettri-atomici.html',
    'nota-tecnica-01-stern-gerlach': '01-stern-gerlach.html',
}

MODELLI = [
    re.compile(r'(?P<pre>Capitolo\s+)(?P<n>\d+)'),
    re.compile(r'(?P<pre>Chapter\s+)(?P<n>\d+)'),
    re.compile(r'(?P<pre>Cap\.\s+)(?P<n>\d+)'),
    re.compile(r'(?P<pre>Ch\.\s+)(?P<n>\d+)'),
]


def rinumera(testo, n):
    """Riscrive il numero conservando l'eventuale zero iniziale gia' presente."""
    def scambia(m):
        return m.group('pre') + ('%02d' % n if len(m.group('n')) > 1 else str(n))
    for modello in MODELLI:
        testo = modello.sub(scambia, testo)
    return testo


cambiati = 0
for nome, scheda in sorted(APPARTENENZA.items()):
    percorso = Path('sorgenti/%s.html' % nome)
    if not percorso.exists():
        print('  manca', percorso)
        continue
    testo = originale = percorso.read_text(encoding='utf-8')
    n = POSIZIONE[scheda]
    testo = rinumera(testo, n)
    if testo != originale:
        percorso.write_text(testo, encoding='utf-8', newline='')
        prima = sorted({int(x) for x in re.findall(r'Cap(?:itolo)?\.?\s*0?(\d+)', originale)})
        print('%-34s %s -> %d' % (nome, prima, n))
        cambiati += 1

print('\npagine corrette:', cambiati)

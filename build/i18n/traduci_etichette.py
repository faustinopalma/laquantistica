"""Rende bilingui le etichette rimaste in italiano, seguendo lo stile gia' usato
nelle pagine dove la traduzione c'era (Lab locale/Local lab, Cap./Ch.).
"""
import pathlib
import re

RADICE = pathlib.Path('publish')


def bilingue(it, en):
    return f'<span class="it">{it}</span><span class="en">{en}</span>'


modifiche = []


def sostituisci(file_, schema, fabbrica, attese=None):
    p = RADICE / file_
    t = p.read_text(encoding='utf-8')
    n = 0

    def rimpiazza(m):
        nonlocal n
        n += 1
        return fabbrica(m)

    nuovo = re.sub(schema, rimpiazza, t)
    if n:
        p.write_text(nuovo, encoding='utf-8')
        modifiche.append((file_, schema[:38], n))
    if attese is not None and n != attese:
        raise SystemExit(f'ATTESO {attese} in {file_}, trovato {n} per {schema[:40]}')


LAB = sorted(f.name for f in RADICE.glob('lab-*.html'))

for f in LAB:
    # etichetta "Lab · Cap. N" nell'intestazione
    sostituisci(f, r'<span class="tag amber">Lab · Cap\. (\d+)</span>',
                lambda m: f'<span class="tag amber">{bilingue("Lab · Cap. " + m.group(1), "Lab · Ch. " + m.group(1))}</span>')
    # piede ancora monolingue
    sostituisci(f, r'<span>La Quantistica · Lab locale · Cap\. (\d+)</span>',
                lambda m: bilingue(f'La Quantistica · Lab locale · Cap. {m.group(1)}',
                                   f'La Quantistica · Local lab · Ch. {m.group(1)}'))

for f in ['nota-01-stern-gerlach.html', 'nota-02-prodotto-scalare.html']:
    sostituisci(f, r'<span class="tag">Nota (\d+)</span>',
                lambda m: f'<span class="tag">{bilingue("Nota " + m.group(1), "Note " + m.group(1))}</span>', 1)
    sostituisci(f, r'<span>La Quantistica · Nota tecnica N\.(\d+) · Rev\. (\d+)</span>',
                lambda m: bilingue(f'La Quantistica · Nota tecnica N.{m.group(1)} · Rev. {m.group(2)}',
                                   f'La Quantistica · Technical note No. {m.group(1)} · Rev. {m.group(2)}'), 1)

sostituisci('nota-tecnica-01-stern-gerlach.html', r'<span class="tag">Nota tecnica</span>',
            lambda m: f'<span class="tag">{bilingue("Nota tecnica", "Technical note")}</span>', 1)
sostituisci('nota-tecnica-01-stern-gerlach.html',
            r'<span>La Quantistica · Nota tecnica · Cap\. (\d+)</span>',
            lambda m: bilingue(f'La Quantistica · Nota tecnica · Cap. {m.group(1)}',
                               f'La Quantistica · Technical note · Ch. {m.group(1)}'), 1)

# richiamo alla nota dentro i capitoli
for f in sorted(RADICE.glob('0*.html')):
    sostituisci(f.name, r'<span class="k">Nota (\d+)</span>',
                lambda m: f'<span class="k">{bilingue("Nota " + m.group(1), "Note " + m.group(1))}</span>')
    sostituisci(f.name, r'<span class="k">Nota tecnica</span>',
                lambda m: f'<span class="k">{bilingue("Nota tecnica", "Technical note")}</span>')

for f, s, n in modifiche:
    print(f'{f:<38} {n}x  {s}')
print(f'\ntotale sostituzioni: {sum(n for _, _, n in modifiche)}')

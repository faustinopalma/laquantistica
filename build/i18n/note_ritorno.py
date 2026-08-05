"""Ritorno alle note: pillola sempre visibile + richiamo al capitolo in testata.

Sostituisce la freccia in alto a destra (posizione poco intuitiva) e lo script
ripetuto in ogni nota con l'unico assets/note-back.js.
Eseguire una sola volta: e' idempotente, salta le note gia' convertite.
"""
import re
import sys
from pathlib import Path

SORGENTI = Path(__file__).resolve().parents[2] / 'sorgenti'

CRUMB = ('<a class="doc-back-crumb" id="backCrumb" href="{href}">'
         '<span class="crumb-arrow" aria-hidden="true">&larr;</span>'
         '<span class="vh"><span class="it">Torna al </span><span class="en">Back to </span></span>'
         '<span class="cap it">{it}</span><span class="cap en">{en}</span></a>')

modificate = []
for f in sorted(SORGENTI.glob('nota-*.html')):
    t = f.read_text(encoding='utf-8')
    if 'doc-back-crumb' in t:
        continue

    m = re.search(r'[ \t]*<a class="doc-back-top" id="backTop" href="([^"]+)">.*?</a>\n', t, re.S)
    if not m:
        sys.exit(f'{f.name}: manca il richiamo in alto')
    href = m.group(1)
    t = t[:m.start()] + t[m.end():]

    etichetta = re.compile(
        r'<span class="it"(?: id="retLabelIt")?>((?:Cap\.|Ch\.)[^<]*)</span>'
        r'<span class="en"(?: id="retLabelEn")?>([^<]*)</span>')
    m2 = etichetta.search(t)
    if not m2:
        sys.exit(f'{f.name}: manca l\'etichetta del capitolo')
    t = t[:m2.start()] + CRUMB.format(href=href, it=m2.group(1), en=m2.group(2)) + t[m2.end():]

    m3 = re.search(r'\n<script>\n(?:(?!</script>)[\s\S])*?safeRet(?:(?!</script>)[\s\S])*?</script>\n', t)
    if not m3:
        sys.exit(f'{f.name}: manca lo script del ritorno')
    t = t[:m3.start()] + '\n' + t[m3.end():]

    t = t.replace('assets/note.css?v=5', 'assets/note.css?v=6')
    if 'note-back.js' not in t:
        t = t.replace('</head>', '<script src="assets/note-back.js?v=1" defer></script>\n</head>', 1)

    f.write_text(t, encoding='utf-8')
    modificate.append(f.name)

print(f'note convertite: {len(modificate)}')
for n in modificate:
    print(f'  {n}')

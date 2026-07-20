"""Convert all Equation Native (MTEF) objects in each OLE chapter to LaTeX,
write to build/eq/<key>.txt (UTF-8) for review."""
from pathlib import Path
from collections import Counter
import olefile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mtef2latex import convert

root = Path(__file__).resolve().parent.parent
outdir = root / 'build' / 'eq'
outdir.mkdir(parents=True, exist_ok=True)

targets = {
    '00_introduzione': 'Introduzione.docx',
    '04_diffrazione': '4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx',
    '05_rutherford': '5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD 2.docx',
    '06_ulteriori_sviluppi': '6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx',
    '08_effetto_fotoelettrico': '8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx',
    '09_spettri_atomici': '9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx',
}

for key, rel in targets.items():
    p = root / rel
    ole = olefile.OleFileIO(str(p))
    eqs = []
    for e in ole.listdir(streams=True):
        if len(e) >= 3 and e[0] == 'ObjectPool' and e[-1] == 'Equation Native':
            eqs.append((e[1], ole.openstream(e).read()))
    ole.close()
    eqs.sort(key=lambda t: t[0])
    lines = []
    hist = Counter()
    for i, (name, data) in enumerate(eqs):
        try:
            latex = convert(data, collect=hist)
        except Exception as ex:
            latex = f'<ERR {type(ex).__name__}: {ex}>'
        lines.append(f'[{i:03d}] {latex}')
    (outdir / f'{key}.txt').write_text('\n'.join(lines), encoding='utf-8')
    print(f'{key}: {len(eqs)} eqs -> build/eq/{key}.txt')

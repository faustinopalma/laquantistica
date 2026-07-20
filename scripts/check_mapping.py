"""Verify that inline-object tokens map 1:1 to extracted equation images per chapter."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_content import doc_tokens

ROOT = Path(__file__).resolve().parent.parent
CH = {
    '00_introduzione': 'Introduzione.docx',
    '04_diffrazione': '4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx',
    '05_rutherford': '5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD 2.docx',
    '06_ulteriori_sviluppi': '6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx',
    '08_effetto_fotoelettrico': '8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx',
    '09_spettri_atomici': '9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx',
}

for key, rel in CH.items():
    toks = doc_tokens(ROOT / rel)
    nobj = sum(1 for t in toks if t[0] == 'obj')
    d = ROOT / 'build' / 'eqimg' / key
    files = sorted([p.name for p in d.glob('obj*.*')]) if d.exists() else []
    # highest index present
    idxs = sorted(int(p.stem[3:]) for p in d.glob('obj*.*')) if d.exists() else []
    maxidx = idxs[-1] if idxs else -1
    print(f'{key}: tokens_obj={nobj}  files={len(files)}  max_index={maxidx}  in_range={"OK" if maxidx < nobj else "OVERFLOW"}')

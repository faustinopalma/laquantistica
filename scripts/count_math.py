"""Compare per-chapter counts: fodt <math> roots (LibreOffice equations) vs inline
object tokens (our extractor). If they match, ordinal mapping object->MathML is safe."""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_content import doc_tokens

ROOT = Path(__file__).resolve().parent.parent
# chapter key -> (source .docx, fodt filename)
CH = {
    '00_introduzione': ('Introduzione.docx', 'Introduzione.fodt'),
    '01_stern_gerlach': ('1. Esperimento di Stern-Gerlach/Esperimento di Stern-Gerlach.docx', 'Esperimento di Stern-Gerlach.fodt'),
    '02_stern_gerlach_cascata': ('2. Esperimenti di Stern-Gerlach in cascata/Esperimenti di Stern-Gerlach in cascata.docx', 'Esperimenti di Stern-Gerlach in cascata.fodt'),
    '04_diffrazione': ('4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx', 'DIFFRAZIONE DEGLI ELETTRONI.fodt'),
    '05_rutherford': ('5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD 2.docx', None),
    '06_ulteriori_sviluppi': ('6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx', 'Ulteriori sviluppi della Teoria.fodt'),
    '07_franck_hertz': ('7. Esperimento di Franck-Hertz/ESPERIMENTO DI FRANCK-HERTZ.docx', 'ESPERIMENTO DI FRANCK-HERTZ.fodt'),
    '08_effetto_fotoelettrico': ('8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx', 'EFFETTO FOTOELETTRICO.fodt'),
    '09_spettri_atomici': ('9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx', 'SPETTRI ATOMICI DI EMISSIONE.fodt'),
}

for key, (src, fodt) in CH.items():
    nobj = '-'
    try:
        toks = doc_tokens(ROOT / src)
        nobj = sum(1 for t in toks if t[0] == 'obj')
    except Exception as e:
        nobj = f'ERR {e}'
    nmath = '-'
    if fodt:
        f = ROOT / 'build' / 'fodt' / fodt
        if f.exists():
            d = f.read_text(encoding='utf-8')
            nmath = len(re.findall(r'<math[ >]', d))
    match = 'OK' if nobj == nmath else 'DIFF'
    print(f'{key}: objects={nobj}  math={nmath}  {match}')

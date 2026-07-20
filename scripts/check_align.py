"""Report per chapter: #SVG objects, #MathML, and whether any MathML gap is
mid-sequence (would misalign) vs only trailing (safe, SVG fallback)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
EQSVG = ROOT / 'build' / 'eqsvg'
MML = ROOT / 'build' / 'mml'
for key in ['00_introduzione', '04_diffrazione', '05_rutherford', '06_ulteriori_sviluppi',
            '08_effetto_fotoelettrico', '09_spettri_atomici', '02_stern_gerlach_cascata']:
    svgdir = EQSVG / key
    nsvg = (max((int(p.stem[3:]) for p in svgdir.glob('obj*.svg')), default=-1) + 1)
    mf = MML / f'{key}.json'
    maths = json.loads(mf.read_text(encoding='utf-8')) if mf.exists() else []
    nm = len(maths)
    # trailing safe if nm <= nsvg and first nm are all non-empty
    empties = [i for i, m in enumerate(maths) if not m]
    status = 'aligned (trailing fallback)' if nm <= nsvg and not empties else 'CHECK'
    print(f'{key}: svg={nsvg} mml={nm} empties={empties[:5]} -> {status}')

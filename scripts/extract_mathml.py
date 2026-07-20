"""Extract ordered MathML formulas from LibreOffice fodt exports into a per-chapter
JSON store. Each entry is the raw <math>...</math> (annotation stripped, display
attribute removed so the generator can set inline/block per context)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FODT = ROOT / 'build' / 'fodt'
OUT = ROOT / 'build' / 'mml'
OUT.mkdir(parents=True, exist_ok=True)

KEY_TO_FODT = {
    '00_introduzione': 'Introduzione.fodt',
    '01_stern_gerlach': 'Esperimento di Stern-Gerlach.fodt',
    '02_stern_gerlach_cascata': 'Esperimenti di Stern-Gerlach in cascata.fodt',
    '04_diffrazione': 'DIFFRAZIONE DEGLI ELETTRONI.fodt',
    '06_ulteriori_sviluppi': 'Ulteriori sviluppi della Teoria.fodt',
    '07_franck_hertz': 'ESPERIMENTO DI FRANCK-HERTZ.fodt',
    '08_effetto_fotoelettrico': 'EFFETTO FOTOELETTRICO.fodt',
    '09_spettri_atomici': 'SPETTRI ATOMICI DI EMISSIONE.fodt',
}

MATH = re.compile(r'<math\b.*?</math>', re.S)
ANNOT = re.compile(r'<annotation\b.*?</annotation>', re.S)
WS = re.compile(r'>\s+<')


def clean(m):
    m = ANNOT.sub('', m)
    m = WS.sub('><', m).strip()
    # remove display attr on the root so we can set it per placement
    m = re.sub(r'(<math\b[^>]*?)\s+display="[^"]*"', r'\1', m, count=1)
    return m


def main():
    summary = []
    for key, fname in KEY_TO_FODT.items():
        f = FODT / fname
        if not f.exists():
            summary.append(f'{key}: MISSING fodt'); continue
        d = f.read_text(encoding='utf-8')
        maths = [clean(m.group(0)) for m in MATH.finditer(d)]
        (OUT / f'{key}.json').write_text(json.dumps(maths, ensure_ascii=False), encoding='utf-8')
        summary.append(f'{key}: {len(maths)} formulas')
    print('\n'.join(summary))


if __name__ == '__main__':
    main()

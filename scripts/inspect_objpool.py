"""Inspect ObjectPool of legacy .doc files: list embedded object storages and their streams."""
from pathlib import Path
import olefile

root = Path(__file__).resolve().parent.parent
targets = {
    '04_diffrazione': '4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx',
    '06_ulteriori_sviluppi': '6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx',
    '07_franck_hertz': '7. Esperimento di Franck-Hertz/ESPERIMENTO DI FRANCK-HERTZ.docx',
    '08_effetto_fotoelettrico': '8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx',
    '09_spettri_atomici': '9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx',
    '00_introduzione': 'Introduzione.docx',
    '05_rutherford': '5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD 2.docx',
}

for key, rel in targets.items():
    p = root / rel
    ole = olefile.OleFileIO(str(p))
    entries = ole.listdir(streams=True, storages=True)
    # group by top-level ObjectPool child
    objs = {}
    other = []
    for e in entries:
        if e and e[0] == 'ObjectPool' and len(e) >= 2:
            objs.setdefault(e[1], []).append('/'.join(e[2:]) if len(e) > 2 else '')
        elif e and e[0] != 'ObjectPool':
            other.append('/'.join(e))
    print('=' * 70)
    print(key, '-> embedded objects:', len(objs))
    # show first few objects with their streams
    for i, (name, streams) in enumerate(list(objs.items())[:4]):
        print(f'  [{name}] streams: {streams}')
    ole.close()

"""Extract plain text from legacy Word97 (.doc, OLE2) files using olefile.
Parses the FIB + CLX piece table (handles fast-saved / complex documents).
"""
import struct, sys
from pathlib import Path
import olefile

def extract_doc_text(path):
    ole = olefile.OleFileIO(str(path))
    try:
        wd = ole.openstream('WordDocument').read()
    except OSError:
        # some use different case
        streams = ole.listdir()
        name = [s for s in streams if s and s[-1].lower() == 'worddocument']
        wd = ole.openstream(name[0]).read()

    # FIB
    wIdent = struct.unpack_from('<H', wd, 0)[0]
    flags = struct.unpack_from('<H', wd, 0x0A)[0]
    fWhichTblStm = (flags & 0x0200) != 0
    fcClx = struct.unpack_from('<I', wd, 0x01A2)[0]
    lcbClx = struct.unpack_from('<I', wd, 0x01A6)[0]

    table_name = '1Table' if fWhichTblStm else '0Table'
    try:
        table = ole.openstream(table_name).read()
    except OSError:
        # fallback: try the other
        other = '0Table' if fWhichTblStm else '1Table'
        table = ole.openstream(other).read()
    ole.close()

    clx = table[fcClx:fcClx+lcbClx]

    # Walk CLX to find Pcdt (0x02)
    i = 0
    pcdt = None
    while i < len(clx):
        clxt = clx[i]
        if clxt == 0x01:  # Prc
            cbGrpprl = struct.unpack_from('<H', clx, i+1)[0]
            i += 3 + cbGrpprl
        elif clxt == 0x02:  # Pcdt
            lcb = struct.unpack_from('<I', clx, i+1)[0]
            pcdt = clx[i+5:i+5+lcb]
            break
        else:
            i += 1
    if pcdt is None:
        return ""

    n = (len(pcdt) - 4) // (4 + 8)
    cps = [struct.unpack_from('<I', pcdt, k*4)[0] for k in range(n+1)]
    pcd_off = (n+1) * 4
    out = []
    for k in range(n):
        cp_start = cps[k]
        cp_end = cps[k+1]
        num = cp_end - cp_start
        fc_field = struct.unpack_from('<I', pcdt, pcd_off + k*8 + 2)[0]
        compressed = (fc_field & 0x40000000) != 0
        fc = fc_field & 0x3FFFFFFF
        if compressed:
            fc = fc // 2
            raw = wd[fc:fc+num]
            try:
                text = raw.decode('cp1252', errors='replace')
            except Exception:
                text = raw.decode('latin-1', errors='replace')
        else:
            raw = wd[fc:fc+num*2]
            text = raw.decode('utf-16-le', errors='replace')
        out.append(text)
    return ''.join(out)


def clean(text):
    # Word control chars -> readable
    repl = {
        '\r': '\n', '\x07': '\t', '\x0b': '\n', '\x0c': '\n',
        '\x1e': '-', '\x1f': '', '\x13': '', '\x14': '', '\x15': '',
        '\x08': '', '\x01': '[OBJ]', '\x02': '',
    }
    for a, b in repl.items():
        text = text.replace(a, b)
    return text


if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    outdir = root / 'build' / 'text_ole'
    outdir.mkdir(parents=True, exist_ok=True)
    targets = {
        '00_introduzione': 'Introduzione.docx',
        '04_diffrazione': '4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx',
        '05_rutherford': '5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD 2.docx',
        '06_ulteriori_sviluppi': '6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx',
        '07_franck_hertz': '7. Esperimento di Franck-Hertz/ESPERIMENTO DI FRANCK-HERTZ.docx',
        '08_effetto_fotoelettrico': '8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx',
        '09_spettri_atomici': '9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx',
    }
    for key, rel in targets.items():
        p = root / rel
        print('=' * 70)
        print(key, '<-', rel)
        if not p.exists():
            print('  MISSING'); continue
        try:
            txt = clean(extract_doc_text(p))
            (outdir / f'{key}.txt').write_text(txt, encoding='utf-8')
            body = txt.strip()
            print(f'  chars={len(body)}  [OBJ]count={txt.count("[OBJ]")}')
            print('  preview:', repr(body[:180]))
        except Exception as e:
            import traceback
            print('  ERROR', type(e).__name__, e)
            traceback.print_exc()

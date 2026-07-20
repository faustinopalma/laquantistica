"""Classify inline special chars (0x01) in a Word97 .doc as OLE objects (equations)
vs pictures, by parsing the CHPX (character properties) FKPs. Also returns the
main-document text as a token list interleaving text and object markers in order.
"""
import struct
from pathlib import Path
import olefile

# sprm operation codes (Word97)
SPRM_CFOLE2 = 0x080A       # bool: is OLE2 object
SPRM_CPICLOCATION = 0x6A03  # 4-byte: picture location (in Data stream)
SPRM_CFSPEC = 0x0855        # bool: special char


def _read_streams(path):
    ole = olefile.OleFileIO(str(path))
    wd = ole.openstream('WordDocument').read()
    flags = struct.unpack_from('<H', wd, 0x0A)[0]
    table_name = '1Table' if (flags & 0x0200) else '0Table'
    try:
        table = ole.openstream(table_name).read()
    except OSError:
        table = ole.openstream('0Table' if table_name == '1Table' else '1Table').read()
    ole.close()
    return wd, table


def _piece_table(wd, table):
    fcClx = struct.unpack_from('<I', wd, 0x01A2)[0]
    lcbClx = struct.unpack_from('<I', wd, 0x01A6)[0]
    clx = table[fcClx:fcClx + lcbClx]
    i = 0
    pcdt = None
    while i < len(clx):
        if clx[i] == 0x01:
            cb = struct.unpack_from('<H', clx, i + 1)[0]
            i += 3 + cb
        elif clx[i] == 0x02:
            lcb = struct.unpack_from('<I', clx, i + 1)[0]
            pcdt = clx[i + 5:i + 5 + lcb]
            break
        else:
            i += 1
    n = (len(pcdt) - 4) // 12
    cps = [struct.unpack_from('<I', pcdt, k * 4)[0] for k in range(n + 1)]
    pcd_off = (n + 1) * 4
    pieces = []
    for k in range(n):
        fc_field = struct.unpack_from('<I', pcdt, pcd_off + k * 8 + 2)[0]
        compressed = (fc_field & 0x40000000) != 0
        fc = fc_field & 0x3FFFFFFF
        if compressed:
            fc = fc // 2
        pieces.append((cps[k], cps[k + 1], fc, compressed))
    return pieces


def _parse_chpx_fkps(wd, table):
    """Return list of (fcStart, fcEnd, grpprl_bytes) sorted by fcStart."""
    fcPlcfBteChpx = struct.unpack_from('<I', wd, 0x0FA)[0]
    lcbPlcfBteChpx = struct.unpack_from('<I', wd, 0x0FE)[0]
    plc = table[fcPlcfBteChpx:fcPlcfBteChpx + lcbPlcfBteChpx]
    n = (len(plc) - 4) // 8
    aFC = [struct.unpack_from('<I', plc, k * 4)[0] for k in range(n + 1)]
    aPn = [struct.unpack_from('<I', plc, (n + 1) * 4 + k * 4)[0] & 0x003FFFFF for k in range(n)]
    runs = []
    for pn in aPn:
        off = pn * 512
        fkp = wd[off:off + 512]
        if len(fkp) < 512:
            continue
        crun = fkp[511]
        fcs = [struct.unpack_from('<I', fkp, k * 4)[0] for k in range(crun + 1)]
        for k in range(crun):
            woff = fkp[4 * (crun + 1) + k]
            if woff == 0:
                grpprl = b''
            else:
                pos = woff * 2
                cb = fkp[pos]
                grpprl = fkp[pos + 1:pos + 1 + cb]
            runs.append((fcs[k], fcs[k + 1], grpprl))
    runs.sort(key=lambda r: r[0])
    return runs


def _iter_sprms(grpprl):
    i = 0
    while i + 2 <= len(grpprl):
        sprm = struct.unpack_from('<H', grpprl, i)[0]
        i += 2
        spra = (sprm >> 13) & 0x7
        # operand size by spra
        if spra == 0 or spra == 1:
            sz = 1
        elif spra == 2 or spra == 4 or spra == 5:
            sz = 2
        elif spra == 3:
            sz = 4
        elif spra == 7:
            sz = 3
        elif spra == 6:
            if i < len(grpprl):
                sz = grpprl[i]
                i += 1
            else:
                break
        else:
            sz = 0
        operand = grpprl[i:i + sz]
        i += sz
        yield sprm, operand


def _classify_fc(fc, chpx_runs):
    # find run whose [fcStart, fcEnd) contains fc
    for a, b, grpprl in chpx_runs:
        if a <= fc < b:
            is_ole = False
            has_pic = False
            for sprm, operand in _iter_sprms(grpprl):
                if sprm == SPRM_CFOLE2 and operand and operand[0] == 1:
                    is_ole = True
                if sprm == SPRM_CPICLOCATION:
                    has_pic = True
            if is_ole:
                return 'ole'
            if has_pic:
                return 'pic'
            return 'other'
    return 'other'


def classify_objects(path):
    wd, table = _read_streams(path)
    pieces = _piece_table(wd, table)
    chpx_runs = _parse_chpx_fkps(wd, table)
    types = []  # in document order
    for cp0, cp1, fc, comp in pieces:
        num = cp1 - cp0
        if comp:
            raw = wd[fc:fc + num]
            text = raw.decode('cp1252', errors='replace')
            step = 1
        else:
            raw = wd[fc:fc + num * 2]
            text = raw.decode('utf-16-le', errors='replace')
            step = 2
        for j, ch in enumerate(text):
            if ch == '\x01':
                cfc = fc + j * step
                types.append(_classify_fc(cfc, chpx_runs))
    return types


if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    from collections import Counter
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
        try:
            types = classify_objects(root / rel)
            c = Counter(types)
            print(f'{key}: total 0x01={len(types)}  ole={c["ole"]}  pic={c["pic"]}  other={c["other"]}')
        except Exception as e:
            import traceback
            print(f'{key}: ERROR {e}')
            traceback.print_exc()

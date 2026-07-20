"""Build ordered content tokens for a legacy Word .doc: text runs interleaved with
inline-object markers (each tagged with its Data-stream object size in bytes).
Used to place MTEF equations inline in the reconstructed web pages.
"""
import struct
from pathlib import Path
import olefile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import classify_objects as C


def _ccp_text(wd):
    return struct.unpack_from('<I', wd, 0x004C)[0]


def _data_stream(path):
    ole = olefile.OleFileIO(str(path))
    data = ole.openstream('Data').read() if ole.exists('Data') else b''
    ole.close()
    return data


def _obj_lcb(data, picloc):
    if picloc is None or picloc + 6 > len(data):
        return None
    lcb = struct.unpack_from('<I', data, picloc)[0]
    return lcb


def doc_tokens(path):
    wd, table = C._read_streams(path)
    pieces = C._piece_table(wd, table)
    runs = C._parse_chpx_fkps(wd, table)
    data = _data_stream(path)
    ccp = _ccp_text(wd)

    def picloc_for(fc):
        for a, b, g in runs:
            if a <= fc < b:
                for sprm, op in C._iter_sprms(g):
                    if sprm == 0x6A03 and len(op) == 4:
                        return struct.unpack('<I', op)[0]
                return None
        return None

    tokens = []
    buf = []
    cp = 0
    in_field_instr = False  # between field-begin (0x13) and field-separator (0x14)
    ctrl = {0x07: '\t', 0x0b: '\n', 0x0c: '\n', 0x0d: '\n'}
    for cp0, cp1, fc, comp in pieces:
        num = cp1 - cp0
        step = 1 if comp else 2
        raw = wd[fc:fc + (num if comp else num * 2)]
        text = raw.decode('cp1252' if comp else 'utf-16-le', errors='replace')
        for j, ch in enumerate(text):
            if cp >= ccp:
                break
            cp += 1
            o = ord(ch)
            if o == 0x13:            # field begin -> start skipping instruction text
                in_field_instr = True
                continue
            if o == 0x14:            # field separator -> field result follows (keep it)
                in_field_instr = False
                continue
            if o == 0x15:            # field end
                in_field_instr = False
                continue
            if in_field_instr:
                # inside the field instruction (e.g. "EMBED Equation.3 \* MERGEFORMAT") -> drop
                continue
            if ch == '\x01':
                if buf:
                    tokens.append(('text', ''.join(buf))); buf = []
                pl = picloc_for(fc + j * step)
                lcb = _obj_lcb(data, pl)
                tokens.append(('obj', lcb))
            elif o in ctrl:
                buf.append(ctrl[o])
            elif o in (0x08, 0x1f, 0x02, 0x05):
                pass  # misc control chars -> drop
            elif o == 0x1e:
                buf.append('-')  # non-breaking hyphen
            elif o < 0x20 and o not in (0x09, 0x0a):
                pass
            else:
                buf.append(ch)
        if cp >= ccp:
            break
    if buf:
        tokens.append(('text', ''.join(buf)))
    return tokens


if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    rel = sys.argv[1] if len(sys.argv) > 1 else '9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx'
    toks = doc_tokens(root / rel)
    nobj = sum(1 for t in toks if t[0] == 'obj')
    lcbs = sorted(t[1] for t in toks if t[0] == 'obj' and t[1] is not None)
    print(f'tokens={len(toks)} objects={nobj}')
    print('obj lcb sorted:', lcbs)

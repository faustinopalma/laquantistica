"""Extract original equation metafiles (the exact MathType/Equation Editor rendering)
embedded in a legacy Word .doc, one per inline object, and write them as *placeable*
WMF files so they render with correct coordinates. Maps each metafile to the object's
position in the document (via the piece table), enabling perfect-fidelity inline images.
"""
import struct, zlib, sys
from pathlib import Path
import olefile
sys.path.insert(0, str(Path(__file__).resolve().parent))
import classify_objects as C


def _piclocs_in_order(wd, table, runs):
    pieces = C._piece_table(wd, table)
    ccp = struct.unpack_from('<I', wd, 0x4C)[0]
    out = []
    cp = 0
    for cp0, cp1, fc, comp in pieces:
        num = cp1 - cp0
        step = 1 if comp else 2
        raw = wd[fc:fc + (num if comp else num * 2)]
        t = raw.decode('cp1252' if comp else 'utf-16-le', errors='replace')
        infld = False
        for j, ch in enumerate(t):
            if cp >= ccp:
                break
            cp += 1
            o = ord(ch)
            if o == 0x13:
                infld = True; continue
            if o in (0x14, 0x15):
                infld = False; continue
            if infld:
                continue
            if ch == '\x01':
                pl = None
                for a, b, g in runs:
                    if a <= fc + j * step < b:
                        for sp, op in C._iter_sprms(g):
                            if sp == 0x6A03 and len(op) == 4:
                                pl = struct.unpack('<I', op)[0]
                        break
                out.append(pl)
        if cp >= ccp:
            break
    return out


def _find_blip(blob):
    off = 0
    while off + 8 <= len(blob):
        vi, rt, rl = struct.unpack_from('<HHI', blob, off)
        if rt in (0xF01A, 0xF01B):
            return _parse_blip(blob, off)
        if rt == 0xF007:  # FBSE with embedded blip after 36-byte header
            return _parse_blip(blob, off + 8 + 36)
        if (vi & 0x0F) == 0x0F:
            off += 8
        else:
            off += 8 + rl
    return None


def _scan_blip(blob):
    """Fallback: brute-force locate a WMF/EMF blip record by its type signature.
    Robust against PICF/picloc drift where the structured record walk desyncs."""
    best = None
    for sig in (b'\x1b\xf0', b'\x1a\xf0'):   # F01B (WMF), F01A (EMF) recType bytes
        p = blob.find(sig)
        while p != -1:
            start = p - 2                      # record header begins 2 bytes before recType
            if start >= 0:
                r = _parse_blip(blob, start)
                if r and len(r[1]) > 32:       # got a non-trivial raw metafile
                    if best is None or start < best[0]:
                        best = (start, r)
                    break
            p = blob.find(sig, p + 2)
    return best[1] if best else None


def _parse_blip(blob, bo):
    if bo + 8 > len(blob):
        return None
    bvi, brt, brl = struct.unpack_from('<HHI', blob, bo)
    inst = bvi >> 4
    p = bo + 8
    if brt == 0xF01B:      # WMF
        p += 16 + (16 if inst == 0x217 else 0)
        ext = 'wmf'
    elif brt == 0xF01A:    # EMF
        p += 16 + (16 if inst == 0x3D5 else 0)
        ext = 'emf'
    else:
        return None
    m_cbSize = struct.unpack_from('<I', blob, p)[0]
    rc = struct.unpack_from('<4i', blob, p + 4)          # left,top,right,bottom
    pt = struct.unpack_from('<2i', blob, p + 20)          # cx,cy in EMU
    m_cbSave = struct.unpack_from('<I', blob, p + 28)[0]
    m_comp = blob[p + 32]
    comp = blob[p + 34:p + 34 + m_cbSave]
    raw = zlib.decompress(comp) if m_comp == 0 else comp
    return ext, raw, rc, pt


def _placeable_wmf(raw, rc, pt):
    left, top, right, bottom = rc
    w = max(1, right - left)
    ptx = pt[0] if pt[0] else 914400
    inch = int(round(w * 914400.0 / ptx)) if ptx else 1440
    if inch <= 0:
        inch = 1440
    hdr = struct.pack('<IHhhhhHIH', 0x9AC6CDD7, 0, left, top, right, bottom, inch, 0, 0)
    words = struct.unpack('<10H', hdr[:20])
    chk = 0
    for wd_ in words:
        chk ^= wd_
    hdr = hdr[:20] + struct.pack('<H', chk)
    return hdr + raw


def extract(doc_path, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    wd, table = C._read_streams(Path(doc_path))
    runs = C._parse_chpx_fkps(wd, table)
    ole = olefile.OleFileIO(str(doc_path))
    data = ole.openstream('Data').read() if ole.exists('Data') else b''
    ole.close()
    piclocs = _piclocs_in_order(wd, table, runs)
    # upper bound for each object's data = the next larger picloc (so a drifted lcb
    # can't run past the next object); used by the scan fallback.
    valid = sorted(p for p in piclocs if p is not None)
    results = []
    for i, pl in enumerate(piclocs):
        if pl is None or pl + 6 > len(data):
            results.append(None); continue
        lcb = struct.unpack_from('<I', data, pl)[0]
        cbh = struct.unpack_from('<H', data, pl + 4)[0]
        end = pl + lcb
        if lcb <= 0 or end > len(data):
            # drifted/invalid length -> bound by the next object position
            nxt = next((p for p in valid if p > pl), len(data))
            end = min(nxt, pl + 8000, len(data))
        blob = data[pl + cbh:end]
        r = _find_blip(blob)
        if not r:
            # robust fallback: scan the whole object region for a blip signature
            region = data[pl:min(next((p for p in valid if p > pl), len(data)), pl + 8000)]
            r = _scan_blip(region)
        if not r:
            results.append(None); continue
        ext, raw, rc, pt = r
        if ext == 'wmf':
            out = _placeable_wmf(raw, rc, pt)
            fn = out_dir / f'obj{i:03d}.wmf'
        else:
            out = raw
            fn = out_dir / f'obj{i:03d}.emf'
        fn.write_bytes(out)
        results.append((i, fn.name, rc, pt))
    return results


if __name__ == '__main__':
    doc = sys.argv[1]
    outd = sys.argv[2]
    res = extract(doc, outd)
    ok = sum(1 for r in res if r)
    print(f'{doc}: {len(res)} objects, {ok} equation images -> {outd}')

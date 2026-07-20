"""Dump Microsoft Equation 3.0 'Equation Native' (MTEF) streams from a .doc for analysis."""
from pathlib import Path
import olefile, struct, sys

root = Path(__file__).resolve().parent.parent

def eq_streams(path):
    ole = olefile.OleFileIO(str(path))
    out = []
    for e in ole.listdir(streams=True):
        if len(e) >= 3 and e[0] == 'ObjectPool' and e[-1] == 'Equation Native':
            data = ole.openstream(e).read()
            out.append((e[1], data))
    ole.close()
    return out

def parse_header(data):
    # OLE Equation header: 28 bytes
    # cbHdr(2) version(4) cf(2) cbObject(4) reserved... then MTEF at 28
    cbHdr = struct.unpack_from('<H', data, 0)[0]
    version = struct.unpack_from('<I', data, 2)[0]
    cf = struct.unpack_from('<H', data, 6)[0]
    cbObject = struct.unpack_from('<I', data, 8)[0]
    mtef = data[cbHdr:]
    return cbHdr, version, cf, cbObject, mtef

if __name__ == '__main__':
    rel = sys.argv[1] if len(sys.argv) > 1 else '9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx'
    p = root / rel
    streams = eq_streams(p)
    print(f'{rel}: {len(streams)} equation streams')
    # MTEF version byte distribution
    from collections import Counter
    vers = Counter()
    sizes = []
    for name, data in streams:
        cbHdr, version, cf, cbObject, mtef = parse_header(data)
        mtef_ver = mtef[0] if mtef else -1
        vers[mtef_ver] += 1
        sizes.append(len(mtef))
    print('cbHdr sample:', parse_header(streams[0][1])[0])
    print('MTEF first-byte (version) distribution:', dict(vers))
    print('mtef sizes: min=%d max=%d' % (min(sizes), max(sizes)))
    # Dump the largest (most complex) and a small one
    idx_big = max(range(len(streams)), key=lambda i: sizes[i])
    idx_small = min(range(len(streams)), key=lambda i: sizes[i])
    for label, idx in [('SMALL', idx_small), ('BIG', idx_big)]:
        name, data = streams[idx]
        cbHdr, version, cf, cbObject, mtef = parse_header(data)
        print(f'--- {label} {name} mtef_len={len(mtef)} ---')
        print('header:', cbHdr, version, cf, cbObject)
        print('bytes:', mtef[:120].hex())

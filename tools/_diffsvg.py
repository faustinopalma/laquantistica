import re, sys
def paths(fn):
    d=open(fn,encoding='utf-8').read()
    return re.findall(r'<path\b[^>]*\bd="([^"]+)"', d)
a=paths(sys.argv[1]); b=paths(sys.argv[2])
print(f'{sys.argv[1]}: {len(a)} paths | {sys.argv[2]}: {len(b)} paths')
# find differing paths by position (assume same count/order)
bi=0
for i,pa in enumerate(a):
    pb=b[bi] if bi < len(b) else None
    if pb==pa:
        bi+=1; continue
    # pa was cut or removed; try to match prefix
    if pb is not None and pa.startswith(pb[:30]):
        print(f'--- path {i} CHANGED ---')
        print('  BEFORE tail:', pa[-140:])
        print('  AFTER  tail:', pb[-140:])
        bi+=1
    else:
        print(f'--- path {i} REMOVED (no match) ---')
        print('  BEFORE:', pa[:80],'...',pa[-80:])

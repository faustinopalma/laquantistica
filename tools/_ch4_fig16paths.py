import re, pathlib
t = pathlib.Path('publish/img/04_diffrazione/DIFFRA~1.svg').read_text(encoding='utf-8', errors='replace')
paths = re.findall(r'<path d="([^"]+)"\s+class="(C\d)"', t)
print('total paths:', len(paths))
def classify(d):
    # count L/l commands
    cmds = re.findall(r'[MmLlHhVvCcZzAaQq]', d)
    nums = re.findall(r'-?\d+\.?\d*', d)
    return cmds
for i,(d,cls) in enumerate(paths):
    cmds = re.findall(r'[MmLlHhVvCcZzAaQq]', d)
    # a simple straight segment: M then one l (2 cmds) 
    seg = d.strip()
    ncoords = len(re.findall(r'-?\d+', d))
    # get start
    m = re.match(r'M\s*(-?\d+)\s+(-?\d+)\s+l\s+(-?\d+)\s+(-?\d+)\s*$', seg)
    if m and cls=='C1':
        x,y,dx,dy = map(int, m.groups())
        kind = 'H' if dy==0 else ('V' if dx==0 else 'diag')
        print(f'{i:3} STRAIGHT {kind:4} start=({x},{y}) d=({dx},{dy}) end=({x+dx},{y+dy})')
    elif cls=='C1':
        print(f'{i:3} PATH   ncmds={len(cmds)} ncoords={ncoords} start={seg[:24]}')

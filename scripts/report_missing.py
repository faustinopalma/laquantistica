"""Report which inline objects in a chapter have no extractable blip (missing image),
showing the surrounding text so we can tell if an important formula was dropped."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_content import doc_tokens

ROOT = Path(__file__).resolve().parent.parent
rel = sys.argv[1]
key = sys.argv[2]
imgdir = ROOT / 'img' / f'eq_{key}'
toks = doc_tokens(ROOT / rel)
# flatten to find text context around each obj
oi = 0
missing = []
for idx, (typ, val) in enumerate(toks):
    if typ == 'obj':
        if not (imgdir / f'obj{oi:03d}.png').exists():
            before = ''
            for j in range(idx - 1, -1, -1):
                if toks[j][0] == 'text':
                    before = toks[j][1][-60:]
                    break
            after = ''
            for j in range(idx + 1, len(toks)):
                if toks[j][0] == 'text':
                    after = toks[j][1][:60]
                    break
            missing.append((oi, val, before.replace('\n', ' '), after.replace('\n', ' ')))
        oi += 1
print(f'{key}: {len(missing)} missing of {oi} objects')
for oi_, lcb, b, a in missing:
    print(f'  obj{oi_:03d} lcb={lcb} ...{b!r} [OBJ] {a!r}...')

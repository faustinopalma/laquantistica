"""Check every <img src> in the generated HTML pages points to a file that exists."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
missing = 0
total = 0
for html in sorted(ROOT.glob('*.html')):
    txt = html.read_text(encoding='utf-8', errors='replace')
    for m in re.finditer(r'<img[^>]*src="([^"]+)"', txt):
        src = m.group(1)
        if src.startswith(('http:', 'https:', 'data:')):
            continue
        total += 1
        p = (ROOT / src)
        if not p.exists():
            missing += 1
            print(f'MISSING {html.name}: {src}')
print(f'\nchecked {total} img refs, {missing} missing')

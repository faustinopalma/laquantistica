"""Quick check of equation-image classification in generated chapter HTML."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for name in sys.argv[1:]:
    t = (ROOT / name).read_text(encoding='utf-8')
    print(name)
    print('  eq-inline    :', len(re.findall(r'class="eq-inline', t)))
    print('  eq-axis      :', len(re.findall(r'eq-axis', t)))
    print('  eq-block     :', len(re.findall(r'class="eq-block', t)))
    print('  equation divs:', len(re.findall(r'<div class="equation"', t)))
    print('  leftover data-h:', len(re.findall(r'data-h', t)))
    m = re.search(r'<p[^>]*>[^<]*[A-Za-z]{4}[^<]*<img class="eq-inline[^>]*>', t)
    print('  sample inline:', (m.group(0)[-150:] if m else 'none'))

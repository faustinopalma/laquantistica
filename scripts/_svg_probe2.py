import re
import sys
from pathlib import Path
d = Path(sys.argv[1]).read_text(encoding='utf-8')
print('visibility="hidden":', d.count('visibility="hidden"'))
print('<script:', d.count('<script'))
print('Slide occurrences:', d.count('Slide'))
for x in re.findall(r'<g[^>]*visibility="hidden"[^>]*>', d)[:5]:
    print('HIDDEN G:', x[:160])
for x in re.findall(r'<g[^>]*class="[^"]*"[^>]*>', d)[:6]:
    print('G:', x[:160])

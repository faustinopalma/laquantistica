import re
import sys
from pathlib import Path
d = Path(sys.argv[1]).read_text(encoding='utf-8')
for x in re.findall(r'<g[^>]*>', d)[:12]:
    print(x[:240])
print('--- clipPath defs ---')
for x in re.findall(r'<clipPath[^>]*>.*?</clipPath>', d, re.S)[:2]:
    print(x[:240])
print('--- svg open ---')
print(re.search(r'<svg[^>]*>', d).group(0))

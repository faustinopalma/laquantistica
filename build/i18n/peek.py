import pathlib
import re

for n in ['nota-01-stern-gerlach', 'nota-tecnica-01-stern-gerlach', 'lab-01-stern-gerlach', 'index']:
    t = pathlib.Path(f'publish/{n}.html').read_text(encoding='utf-8')
    print(f'--- {n} ---')
    m = re.search(r'<div class="langsw".*?</div>', t, re.S)
    print('  langsw :', (m.group(0)[:220].replace('\n', ' | ') if m else 'ASSENTE'))
    h = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    print('  h1     :', (h.group(1)[:200].replace('\n', ' ') if h else 'assente'))
    print('  sidebar:', 'class="sidebar"' in t, '| app.js:', 'app.js' in t, '| note.css:', 'note.css' in t)
    print('  title  :', re.search(r'<title>(.*?)</title>', t, re.S).group(1).strip())

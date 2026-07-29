import re, pathlib
t = pathlib.Path('site/svg/04-diffrazione.html').read_text(encoding='utf-8')
for m in re.finditer(r'<h2([^>]*)>(.*?)</h2>', t, re.S):
    attrs = m.group(1)
    inner = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    idm = re.search(r'id="([^"]+)"', attrs)
    print((idm.group(1) if idm else '(no id)'), '|', inner)

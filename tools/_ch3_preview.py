import pathlib, re, xml.etree.ElementTree as ET
h = pathlib.Path('publish/leggi/03-elettroni.html').read_text(encoding='utf-8')
i = h.find('costanti da utilizzare')
start = h.find('<div class="equation">', i)
end = h.find('</div>', start) + 6
block = h[start:end]
math = re.search(r'<math.*?</math>', block, re.S).group(0)
try:
    ET.fromstring(math)
    print('MathML well-formed: OK')
except Exception as e:
    print('PARSE ERROR:', e)
html = ('<!doctype html><html><head><meta charset="utf-8"><style>body{font-family:sans-serif;margin:24px}'
        '.box{border:1px solid #ccc;padding:16px;max-width:420px}math{font-size:1.3rem}</style></head><body>'
        '<p>Le costanti (nuovo layout in colonna):</p><div class="box">' + block + '</div></body></html>')
pathlib.Path('build/ch3_const_preview.html').write_text(html, encoding='utf-8')
print('wrote build/ch3_const_preview.html')

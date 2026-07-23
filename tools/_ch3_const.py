import pathlib
h = pathlib.Path('publish/leggi/03-elettroni.html').read_text(encoding='utf-8')
i = h.find('costanti da utilizzare')
start = h.find('<div class="equation">', i)
end = h.find('</div>', start) + 6
block = h[start:end]
print('LEN', len(block))
pathlib.Path('build/ch3_const_block.txt').write_text(block, encoding='utf-8')
print(block)

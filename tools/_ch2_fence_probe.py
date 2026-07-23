import re, pathlib
for page in ['publish/leggi/02-stern-gerlach-cascata.html']:
    html = pathlib.Path(page).read_text(encoding='utf-8')
    # find every <mtable> and show 40 chars before / after
    tot = 0; wrapped = 0; bare = 0
    for m in re.finditer(r'<mtable>.*?</mtable>', html, re.S):
        tot += 1
        before = html[max(0,m.start()-40):m.start()]
        after  = html[m.end():m.end()+40]
        # does an <mrow> open right before the fence that precedes the table?
        ctx = before[-25:]
        if re.search(r'<mrow><mo>\(</mo>$', before) or re.search(r'<mrow>\s*<mo[^>]*>\(</mo>$', before):
            wrapped += 1
        elif re.search(r'<mo[^>]*>\(</mo>$', before):
            bare += 1
    print(f'{page}: mtable total={tot}  fence-wrapped-in-mrow={wrapped}  bare-fence(no mrow)={bare}')
    # show 3 sample contexts
    n=0
    for m in re.finditer(r'<mtable>.*?</mtable>', html, re.S):
        if n>=3: break
        print('  ...', repr(html[max(0,m.start()-30):m.start()]), '[MTABLE]', repr(html[m.end():m.end()+18]))
        n+=1

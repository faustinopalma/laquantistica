import pathlib
old = pathlib.Path('build/ch3_const_block.txt').read_text(encoding='utf-8')

# value cells (col2), each starting with "=" ; taken verbatim from the original sub-expressions
V1 = '<mo>&#x0003D;</mo><mn>9</mn><mrow><mo>&#x0002C;</mo></mrow><mn>81</mn><mtext>&#x000A0;</mtext><mrow><mi mathvariant="normal">m</mi><mo>&#x0002F;</mo><msup><mi mathvariant="normal">s</mi><mrow><mn>2</mn></mrow></msup></mrow>'
V2 = '<mo>&#x0003D;</mo><mn>875</mn><mrow><mo>&#x0002C;</mo></mrow><mn>3</mn><mtext>&#x000A0;</mtext><mrow><mi mathvariant="normal">k</mi><mi mathvariant="normal">g</mi><mo>&#x0002F;</mo><msup><mi mathvariant="normal">m</mi><mrow><mn>3</mn></mrow></msup></mrow>'
V3 = '<mo>&#x0003D;</mo><mn>1</mn><mrow><mo>&#x0002C;</mo></mrow><mn>3</mn><mtext>&#x000A0;</mtext><mrow><mi mathvariant="normal">k</mi><mi mathvariant="normal">g</mi><mo>&#x0002F;</mo><msup><mi mathvariant="normal">m</mi><mrow><mn>3</mn></mrow></msup></mrow>'
V4 = '<mo>&#x0003D;</mo><mn>1</mn><mrow><mo>&#x0002C;</mo></mrow><mn>81</mn><mo>&#x000B7;</mo><msup><mn>10</mn><mrow><mo>&#x02212;</mo><mn>5</mn></mrow></msup><mtext>&#x000A0;</mtext><mrow><mi mathvariant="normal">N</mi><mi mathvariant="normal">s</mi><mo>&#x0002F;</mo><msup><mi mathvariant="normal">m</mi><mrow><mn>2</mn></mrow></msup></mrow>'
V5 = '<mo>&#x0003D;</mo><mn>6</mn><mo>&#x000B7;</mo><msup><mn>10</mn><mrow><mo>&#x02212;</mo><mn>3</mn></mrow></msup><mtext>&#x000A0;</mtext><mi>&#x0006D;</mi>'

rho_olio = '<msub><mi>&#x003C1;</mi><mrow><mi>O</mi><mi>l</mi><mi>i</mi><mi>o</mi></mrow></msub>'
rho_aria = '<msub><mi>&#x003C1;</mi><mrow><mi>A</mi><mi>r</mi><mi>i</mi><mi>a</mi></mrow></msub>'

new = ('<div class="equation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'
       '<mtable columnalign="right left" rowspacing="0.35em">'
       '<mtr><mtd><mi>g</mi></mtd><mtd>' + V1 + '</mtd></mtr>'
       '<mtr><mtd>' + rho_olio + '</mtd><mtd>' + V2 + '</mtd></mtr>'
       '<mtr><mtd>' + rho_aria + '</mtd><mtd>' + V3 + '</mtd></mtr>'
       '<mtr><mtd><mi>&#x003B7;</mi></mtd><mtd>' + V4 + '</mtd></mtr>'
       '<mtr><mtd><mi>d</mi></mtd><mtd>' + V5 + '</mtd></mtr>'
       '</mtable></math></div>')

for f in ['publish/leggi/03-elettroni.html','site/mathml/03-elettroni.html','site/svg/03-elettroni.html']:
    p = pathlib.Path(f)
    if not p.exists():
        print('MISSING', f); continue
    t = p.read_text(encoding='utf-8')
    c = t.count(old)
    if c:
        p.write_text(t.replace(old, new), encoding='utf-8')
    print(f'{f}: replaced {c}')

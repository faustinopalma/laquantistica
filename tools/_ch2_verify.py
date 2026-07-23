import re, pathlib, xml.etree.ElementTree as ET
for page in ['publish/leggi/02-stern-gerlach-cascata.html','site/mathml/02-stern-gerlach-cascata.html']:
    html = pathlib.Path(page).read_text(encoding='utf-8')
    maths = re.findall(r'<math\b.*?</math>', html, re.S)
    bad = 0
    for i,m in enumerate(maths):
        try:
            ET.fromstring(m)
        except Exception as e:
            bad += 1
            if bad <= 5:
                print(f"  [{page}] math #{i} PARSE ERROR: {e}")
    eqimg = re.findall(r'src="img/pandoc_ch2/(image\d+\.svg)"', html)
    print(f"{page}: {len(maths)} <math> blocks, {bad} malformed, {len(set(eqimg))} eq-images remaining")

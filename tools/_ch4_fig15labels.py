import re, pathlib, subprocess
src = pathlib.Path('publish/img/04_diffrazione/FIG15.svg')
t = src.read_text(encoding='utf-8', errors='replace')
# expand viewBox to the left to make room for labels
# current: 804 7466 19956 12982
new_x0 = 804 - 2600
new_w  = 19956 + 2600
t = re.sub(r'viewBox="[^"]+"', f'viewBox="{new_x0} 7466 {new_w} 12982"', t, count=1)
t = re.sub(r'(<svg[^>]*?)\swidth="[0-9.]+mm"', rf'\1 width="{round(new_w/100,2)}mm"', t, count=1)
# labels (italic serif d with subscript)
labels = (
 '<text x="-350" y="10450" font-family="Georgia,\'Times New Roman\',serif" font-style="italic" font-size="1200" fill="#000000">d<tspan font-size="820" dy="300">1</tspan></text>'
 '<text x="-500" y="15650" font-family="Georgia,\'Times New Roman\',serif" font-style="italic" font-size="1200" fill="#000000">d<tspan font-size="820" dy="300">2</tspan></text>'
)
t = t.replace('</svg>', labels + '</svg>')
out = pathlib.Path('build/ch4_fig15_labeled.svg')
out.write_text(t, encoding='utf-8')
subprocess.run([r'C:\Program Files\LibreOffice\program\soffice.exe','--headless','--convert-to','png','--outdir','build/ch4_fig15lab',str(out)], check=False)
print('done')

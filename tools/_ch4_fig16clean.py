import re, pathlib, subprocess
src = pathlib.Path('publish/img/04_diffrazione/DIFFRA~1.svg')
t = src.read_text(encoding='utf-8', errors='replace')
remove_d = [
 "M 522557 37039 l 321799 0",
 "M 522557 105190 l 321799 0",
 "M 522557 367426 l 321799 0",
 "M 522557 435577 l 321799 0",
 "M 792453 0 l 0 472616",
]
removed = 0
for d in remove_d:
    pat = '<path d="' + re.escape(d) + '" class="C1" />'
    if pat.replace('\\','') in t or re.search(re.escape('<path d="'+d+'" class="C1" />'), t):
        new = re.sub(re.escape('<path d="'+d+'" class="C1" />'), '', t)
        if new != t:
            t = new; removed += 1
        else:
            print('NOT MATCHED exact:', d)
    else:
        print('NOT FOUND:', d)
print('removed', removed, 'of', len(remove_d))
out = pathlib.Path('build/ch4_fig16_clean.svg')
out.write_text(t, encoding='utf-8')
subprocess.run([r'C:\Program Files\LibreOffice\program\soffice.exe','--headless','--convert-to','png:draw_png_Export:{"PixelWidth":{"type":"long","value":1400},"PixelHeight":{"type":"long","value":662}}','--outdir','build/ch4_fig16clean_png',str(out)], check=False)
print('rendered')

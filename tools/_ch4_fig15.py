import re, pathlib
src = pathlib.Path('build/ch4_media_svg/image15.svg')
t = src.read_text(encoding='utf-8', errors='replace')
# crop viewBox to content + padding
x,y,w,h = 804,7466,19956,12982
t = re.sub(r'viewBox="[^"]+"', f'viewBox="{x} {y} {w} {h}"', t, count=1)
t = re.sub(r'(<svg[^>]*?)\swidth="[0-9.]+mm"\s+height="[0-9.]+mm"',
           rf'\1 width="{round(w/100,2)}mm" height="{round(h/100,2)}mm"', t, count=1)
# scale strokes for uniform on-screen weight (~0.48px at 500px display)
f = 0.447
t = re.sub(r'(stroke-width\s*[:=]\s*"?)([0-9.]+)', lambda m: f'{m.group(1)}{round(float(m.group(2))*f,3)}', t)
out = pathlib.Path('publish/img/04_diffrazione/FIG15.svg')
out.write_text(t, encoding='utf-8')
print('wrote', out)
import subprocess
subprocess.run([r'C:\Program Files\LibreOffice\program\soffice.exe','--headless','--convert-to','png','--outdir','build/ch4_fig15prev',str(out)], check=False)
print('rendered preview')

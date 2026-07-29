import re, pathlib
sx = 21590/817; sy = 27940/1057; pad = 12
MAP = {
 'image11':('FIG12.svg',(250,426,565,628)),
 'image63':('FIG18.svg',(265,436,550,618)),
 'image67':('FIG19.svg',(195,392,621,660)),
 'image65':('FIG20.svg',(250,426,565,628)),
 'image64':('FIG22.svg',(267,438,550,616)),
}
outdir = pathlib.Path('publish/img/05_rutherford')
for src,(name,bb) in MAP.items():
    t = pathlib.Path('build/ch5_svg/'+src+'.svg').read_text(encoding='utf-8', errors='replace')
    x0=(bb[0]-pad)*sx; y0=(bb[1]-pad)*sy; w=(bb[2]-bb[0]+2*pad)*sx; h=(bb[3]-bb[1]+2*pad)*sy
    x0=round(x0); y0=round(y0); w=round(w); h=round(h)
    t = re.sub(r'viewBox="[^"]+"', f'viewBox="{x0} {y0} {w} {h}"', t, count=1)
    t = re.sub(r'(<svg[^>]*?)\swidth="[0-9.]+mm"\s+height="[0-9.]+mm"',
               rf'\1 width="{round(w/100,2)}mm" height="{round(h/100,2)}mm"', t, count=1)
    (outdir/name).write_text(t, encoding='utf-8')
    print('wrote', name, 'viewBox', x0,y0,w,h)
import subprocess
subprocess.run([r'C:\Program Files\LibreOffice\program\soffice.exe','--headless','--convert-to','png','--outdir','build/ch5_fig_prev',*[str(outdir/n) for _,(n,_) in MAP.items()]], check=False)
print('rendered previews')

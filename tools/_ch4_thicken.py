import re, pathlib, subprocess, sys
SRC = {
 'FIG1~1.svg':  dict(src='publish/img/04_diffrazione/FIG1~1.svg',  factor=8.0,  crop=None),
 'AMPOLLA2.svg':dict(src='publish/img/04_diffrazione/AMPOLLA2.svg',factor=6.0,  crop=None),
 # Fig.14 graphite: crop full-page viewBox to content, gentle thicken
 'FIG14.svg':   dict(src='build/ch4_media_svg/image16.svg',        factor=2.0,  crop=(831,6752,19902,14436)),
}
outdir = pathlib.Path('build/ch4_thick'); outdir.mkdir(parents=True, exist_ok=True)

def scale_strokes(text, factor):
    def repl(m):
        pre, val = m.group(1), float(m.group(2))
        return f'{pre}{round(val*factor,3)}'
    # matches  stroke-width: 449   and  stroke-width="28.222"
    return re.sub(r'(stroke-width\s*[:=]\s*"?)([0-9.]+)', repl, text)

for name, cfg in SRC.items():
    t = pathlib.Path(cfg['src']).read_text(encoding='utf-8', errors='replace')
    if cfg['crop']:
        x,y,w,h = cfg['crop']
        t = re.sub(r'viewBox="[^"]+"', f'viewBox="{x} {y} {w} {h}"', t, count=1)
        # adjust width/height mm to new aspect (0.01mm per unit as in source)
        t = re.sub(r'(<svg[^>]*?)\swidth="[0-9.]+mm"\s+height="[0-9.]+mm"',
                   rf'\1 width="{round(w/100,2)}mm" height="{round(h/100,2)}mm"', t, count=1)
    t = scale_strokes(t, cfg['factor'])
    outp = outdir/name
    outp.write_text(t, encoding='utf-8')
    print('wrote', outp)
# render to png
subprocess.run([r'C:\Program Files\LibreOffice\program\soffice.exe','--headless','--convert-to','png','--outdir',str(outdir/'png'),*[str(outdir/n) for n in SRC]], check=False)
print('rendered')

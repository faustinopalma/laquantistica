from PIL import Image, ImageDraw
import pathlib
d = pathlib.Path('build/ch4_media_png')
files = sorted(d.glob('*.png'), key=lambda p: int(''.join(c for c in p.stem if c.isdigit())))
thumbs=[]
TW=300
for f in files:
    im=Image.open(f).convert('RGB')
    r=TW/im.width; im=im.resize((TW,int(im.height*r)))
    lab=Image.new('RGB',(TW,im.height+22),'white')
    dr=ImageDraw.Draw(lab); dr.text((4,4),f.stem,fill=(200,0,0))
    lab.paste(im,(0,22)); thumbs.append(lab)
# grid 3 cols
cols=3; rows=(len(thumbs)+cols-1)//cols
colw=TW+8; rowh=max(t.height for t in thumbs)+8
canvas=Image.new('RGB',(cols*colw, rows*rowh),'white')
for i,t in enumerate(thumbs):
    x=(i%cols)*colw; y=(i//cols)*rowh; canvas.paste(t,(x,y))
canvas.save('build/ch4_media_grid.png'); print('ok', canvas.size, [f.stem for f in files])

from PIL import Image, ImageDraw, ImageFont
import pathlib
base=pathlib.Path('publish/leggi/img/pandoc_ch2')
names=['image113','image115']
try: font=ImageFont.truetype('arial.ttf',20)
except Exception: font=ImageFont.load_default()
imgs=[]
for n in names:
    im=Image.open(base/(n+'.png')).convert('RGB')
    s=max(1.0,120/im.height)
    if im.width*s>760: s=760/im.width
    im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))))
    imgs.append((n,im))
pad=10; lh=28
W=max(500,max(im.width for _,im in imgs)+2*pad); H=sum(im.height+lh+pad for _,im in imgs)+pad
c=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c); y=pad
for n,im in imgs:
    d.rectangle([0,y,W,y+lh],fill=(230,230,240)); d.text((pad,y+4),f'{n}.svg ({im.width}x{im.height})',fill=(20,20,60),font=font)
    y+=lh; c.paste(im,(pad,y)); y+=im.height+pad
out=pathlib.Path('build/ch2_fig12.png'); c.save(out); print('saved',out,c.size)

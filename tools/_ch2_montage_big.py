from PIL import Image, ImageDraw, ImageFont
import pathlib
base = pathlib.Path('publish/leggi/img/pandoc_ch2')
names = ['image108','image114','image120']
try:
    font = ImageFont.truetype('arial.ttf', 20)
except Exception:
    font = ImageFont.load_default()
imgs = []
for n in names:
    im = Image.open(base/(n+'.png')).convert('RGB')
    scale = min(1.0, 780/im.width)
    if im.height*scale < 70:
        scale = 70/im.height
    im = im.resize((max(1,int(im.width*scale)), max(1,int(im.height*scale))))
    imgs.append((n, im))
pad=12; labelh=30
W = max(800, max(im.width for _,im in imgs)+2*pad)
H = sum(im.height+labelh+pad for _,im in imgs)+pad
c = Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c)
y=pad
for n,im in imgs:
    d.rectangle([0,y,W,y+labelh], fill=(230,230,240))
    d.text((pad,y+5), f'{n}.svg  ({im.width}x{im.height})', fill=(20,20,60), font=font)
    y+=labelh; c.paste(im,(pad,y)); y+=im.height+pad
out=pathlib.Path('build/ch2_big3.png'); c.save(out); print('saved',out,c.size)

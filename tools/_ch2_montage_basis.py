from PIL import Image, ImageDraw, ImageFont
import pathlib
base=pathlib.Path('site/svg/img/pandoc_ch2')
names=['image62','image63','image64','image65','image66','image68','image69']
try: font=ImageFont.truetype('arial.ttf',18)
except Exception: font=ImageFont.load_default()
imgs=[]
for n in names:
    try:
        im=Image.open(base/(n+'.png')).convert('RGB')
    except Exception:
        im=Image.new('RGB',(200,40),'white'); ImageDraw.Draw(im).text((4,10),n+' (no png)',fill='red')
    s=max(1.0,80/im.height)
    if im.width*s>720: s=720/im.width
    im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))))
    imgs.append((n,im))
pad=8; lh=24
W=760; H=sum(im.height+lh+pad for _,im in imgs)+pad
c=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c); y=pad
for n,im in imgs:
    d.rectangle([0,y,W,y+lh],fill=(230,230,240)); d.text((pad,y+3),n,fill=(20,20,60),font=font)
    y+=lh; c.paste(im,(pad,y)); y+=im.height+pad
out=pathlib.Path('build/ch2_basis.png'); c.save(out); print('saved',out,c.size)

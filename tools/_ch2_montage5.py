from PIL import Image, ImageDraw, ImageFont
import pathlib
base = pathlib.Path('publish/leggi/img/pandoc_ch2')
names = ['image25','image26','image49','image103','image129']
try:
    font = ImageFont.truetype('arial.ttf', 20)
except Exception:
    font = ImageFont.load_default()
imgs = []
for n in names:
    p = base/(n+'.png')
    im = Image.open(p).convert('RGB')
    # scale up small formulas for readability (target height ~90px min, cap width 900)
    scale = max(1.0, 90/im.height)
    if im.width*scale > 900:
        scale = 900/im.width
    im = im.resize((max(1,int(im.width*scale)), max(1,int(im.height*scale))))
    imgs.append((n, im))
pad = 12; labelh = 30
W = max(900, max(im.width for _,im in imgs) + 2*pad)
H = sum(im.height + labelh + pad for _,im in imgs) + pad
canvas = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(canvas)
y = pad
for n, im in imgs:
    d.rectangle([0, y, W, y+labelh], fill=(230,230,240))
    d.text((pad, y+5), f'{n}.svg   ({im.width}x{im.height})', fill=(20,20,60), font=font)
    y += labelh
    canvas.paste(im, (pad, y))
    y += im.height + pad
out = pathlib.Path('build/ch2_5formule.png')
canvas.save(out)
print('saved', out, canvas.size)

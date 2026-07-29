from PIL import Image
import pathlib
d = pathlib.Path('build/ch4_scan')
pages = [5,6,7,8]
ims = [Image.open(d/f'p{p:02d}.png').convert('RGB') for p in pages]
w = max(i.width for i in ims); h = sum(i.height for i in ims)
c = Image.new('RGB',(w,h),'white'); y=0
from PIL import ImageDraw
dr=ImageDraw.Draw(c)
for p,im in zip(pages,ims):
    c.paste(im,(0,y)); dr.text((4,y+2),f'p{p}',fill=(200,0,0)); y+=im.height
out=pathlib.Path('build/ch4_scan_5_8.png'); c.save(out); print('saved',out,c.size)

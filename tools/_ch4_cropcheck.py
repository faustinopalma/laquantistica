from PIL import Image, ImageDraw
import pathlib
b=pathlib.Path('build')
names=['ch4_fig4_crop.png','ch4_fig12_crop.png','ch4_fig13_crop.png']
ims=[Image.open(b/n).convert('RGB') for n in names]
w=max(i.width for i in ims); h=sum(i.height for i in ims)+30*len(ims)
c=Image.new('RGB',(w,h),'white'); dr=ImageDraw.Draw(c); y=0
for n,im in zip(names,ims):
    dr.text((4,y+2),n,fill=(200,0,0)); y+=24; c.paste(im,(0,y)); y+=im.height+6
c.save(b/'ch4_crops_check.png'); print('saved', c.size)

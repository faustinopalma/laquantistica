from PIL import Image
import pathlib
d = pathlib.Path('build/ch4_scan')
p3 = Image.open(d/'p03.png').convert('RGB')
p4 = Image.open(d/'p04.png').convert('RGB')
print('p03', p3.size, 'p04', p4.size)
W3,H3 = p3.size; W4,H4 = p4.size
def crop(im,W,H,x0,y0,x1,y1,name):
    box=(int(x0*W),int(y0*H),int(x1*W),int(y1*H))
    c=im.crop(box); print(name,box,c.size); c.save(pathlib.Path('build')/name)
# Fig.4 bell curve, p03 top-right
crop(p3,W3,H3, 0.63,0.055,0.99,0.20, 'ch4_fig4_crop.png')
# Fig.12 geometric diagram, p04 right-middle
crop(p4,W4,H4, 0.54,0.24,1.00,0.44, 'ch4_fig12_crop.png')
# Fig.13 two plots, p04 bottom
crop(p4,W4,H4, 0.09,0.75,0.95,0.985, 'ch4_fig13_crop.png')

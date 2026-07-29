import fitz, pathlib
pdf = pathlib.Path('scansioni/04-diffrazione.pdf')
doc = fitz.open(pdf)
out = pathlib.Path('publish/img/04_diffrazione')
zoom = fitz.Matrix(200/72, 200/72)
# page index 2 -> p03 (Fig.4), page index 3 -> p04 (Fig.12, Fig.13)
p3 = doc[2].get_pixmap(matrix=zoom)
p4 = doc[3].get_pixmap(matrix=zoom)
from PIL import Image
im3 = Image.frombytes('RGB',[p3.width,p3.height],p3.samples)
im4 = Image.frombytes('RGB',[p4.width,p4.height],p4.samples)
print('p3',im3.size,'p4',im4.size)
def crop(im,x0,y0,x1,y1,name):
    W,H=im.size; box=(int(x0*W),int(y0*H),int(x1*W),int(y1*H))
    c=im.crop(box); c.save(out/name); print(name,box,c.size)
crop(im3, 0.665,0.060,0.985,0.196, 'FIG4.png')
crop(im4, 0.545,0.255,1.000,0.415, 'FIG12.png')
crop(im4, 0.090,0.755,0.950,0.985, 'FIG13.png')

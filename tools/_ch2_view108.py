from PIL import Image
import pathlib
im = Image.open('publish/leggi/img/pandoc_ch2/image108.png').convert('RGB')
scale = 1100/im.width
im = im.resize((int(im.width*scale), int(im.height*scale)))
out = pathlib.Path('build/ch2_108.png'); im.save(out)
print('saved', out, im.size)

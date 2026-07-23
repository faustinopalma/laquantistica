import re, pathlib
html = pathlib.Path('publish/leggi/02-stern-gerlach-cascata.html').read_text(encoding='utf-8')

# all remaining eq-image srcs with class
rem = re.findall(r'<img\b[^>]*?class="(eq-[^"]*)"[^>]*?src="img/pandoc_ch2/(image\d+\.svg)"', html)
rem2 = re.findall(r'<img\b[^>]*?src="img/pandoc_ch2/(image\d+\.svg)"[^>]*?class="(eq-[^"]*)"', html)
allrem = {}
for cls,src in rem: allrem[src]=cls
for src,cls in rem2: allrem.setdefault(src,cls)
print(f"remaining eq-images: {len(allrem)}")
for src in sorted(allrem, key=lambda s:int(re.search(r'\d+',s).group())):
    print(f"  {src:16} {allrem[src]}")

# known/suspected diagrams: must still be images
diagrams = ['image1.svg','image2.svg','image3.svg','image6.svg','image16.svg','image19.svg','image27.svg','image114.svg']
print("\n-- diagram check (should be IMG) --")
for d in diagrams:
    is_img = ('src="img/pandoc_ch2/'+d+'"' in html)
    print(f"  {d:16} {'IMG(ok)' if is_img else 'CONVERTED(!!)'}")

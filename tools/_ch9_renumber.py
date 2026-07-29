import re, pathlib
p = pathlib.Path('publish/09-spettri-atomici.html')
h = p.read_text(encoding='utf-8')

# 1) shift every existing figure id/href/data-ref number +1
h = re.sub(r'fig-09_spettri_atomici-(\d+)', lambda m: 'fig-09_spettri_atomici-%d' % (int(m.group(1))+1), h)
# 2) shift caption / inline "Fig. N" +1
h = re.sub(r'Fig\. (\d+)', lambda m: 'Fig. %d' % (int(m.group(1))+1), h)
# 3) link text: set the number inside <a ...>N</a> to match the (already shifted) data-ref
h = re.sub(r'(data-ref="fig-09_spettri_atomici-(\d+)">)(\d+)(</a>)', lambda m: m.group(1)+m.group(2)+m.group(4), h)

# 4) number the RETICO figure as Fig. 1
old_ret = '<figure class="fig-inline"><img loading="lazy" src="img/09_spettri_atomici/RETICO~1.jpg" alt="Il reticolo di diffrazione."><figcaption><span class="it">Il reticolo di diffrazione utilizzato per separare le frequenze della luce.</span>'
new_ret = '<figure id="fig-09_spettri_atomici-1" class="fig-inline"><img loading="lazy" src="img/09_spettri_atomici/RETICO~1.jpg" alt="Il reticolo di diffrazione."><figcaption><b>Fig. 1</b> \u2014 <span class="it">Il reticolo di diffrazione utilizzato per separare le frequenze della luce.</span>'
assert old_ret in h, 'RETICO figure not found'
h = h.replace(old_ret, new_ret, 1)

# 5) add a text reference (Fig. 1) in the grating paragraph just before the figure
ref = ' (Fig. <a class="ref" href="#fig-09_spettri_atomici-1" data-ref="fig-09_spettri_atomici-1">1</a>)'
old_it = 'Se inviamo un fascio di luce prodotta dagli atomi verso un reticolo di diffrazione, al di l\u00e0 del reticolo'
new_it = 'Se inviamo un fascio di luce prodotta dagli atomi verso un reticolo di diffrazione' + ref + ', al di l\u00e0 del reticolo'
assert old_it in h, 'grating IT sentence not found'
h = h.replace(old_it, new_it, 1)
old_en = 'towards a diffraction grating, beyond the grating'
new_en = 'towards a diffraction grating' + ref + ', beyond the grating'
assert old_en in h, 'grating EN sentence not found'
h = h.replace(old_en, new_en, 1)

p.write_text(h, encoding='utf-8')
print('done')

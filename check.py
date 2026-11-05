from pathlib import Path
from urllib.parse import urlsplit, unquote
from lxml import html
import json

root=Path(__file__).parent/'dist'
pages=list(root.rglob('*.html'))
errors=[]
for path in pages:
    if path.name.startswith('qa-'): continue
    soup=html.fromstring(path.read_text())
    if not soup.get('lang'): errors.append(f'{path}: language missing')
    if len(soup.xpath('//h1'))!=1: errors.append(f'{path}: must have one h1')
    ids=[x.get('id') for x in soup.xpath('//*[@id]')]
    if len(ids)!=len(set(ids)): errors.append(f'{path}: duplicate ids')
    for el in soup.xpath('//a[@href]|//img[@src]|//script[@src]|//link[@href]'):
        url=el.get('href',el.get('src',''))
        parts=urlsplit(url)
        if parts.scheme or parts.netloc: continue
        if parts.path:
            target=root/unquote(parts.path.lstrip('/'))
            if not target.suffix: target=target/'index.html'
            if not target.exists(): errors.append(f'{path}: broken local URL {url}')
        elif parts.fragment and parts.fragment not in ids:
            errors.append(f'{path}: missing fragment {url}')
    for img in soup.xpath('//img'):
        if not img.get('alt'): errors.append(f'{path}: image lacks alt')
    if not soup.xpath('//meta[@name="viewport"]'): errors.append(f'{path}: viewport missing')
    if not soup.xpath('//a[@class="skip-link"]'): errors.append(f'{path}: skip link missing')
    if path.parent.parent.name=='projects' and len(soup.xpath('//section[contains(@class,"case-section ")]'))!=11:
        errors.append(f'{path}: incomplete case study')
projects=json.loads((root/'projects.json').read_text())
assert len(projects)==6 and len({p['company'] for p in projects})==5
assert all(p['skills'] and p['tools'] and p['status'] for p in projects)

def luminance(c):
    rgb=[int(c[i:i+2],16)/255 for i in (1,3,5)]
    rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(a*b for a,b in zip(rgb,[.2126,.7152,.0722]))
def contrast(a,b):
    x,y=sorted([luminance(a),luminance(b)])
    return (y+.05)/(x+.05)
for fg,bg in [('#b5cbd3','#123b4b'),('#91d1b7','#123b4b'),('#f6f5ef','#0b3041'),('#102b36','#ff6a3d')]:
    ratio=contrast(fg,bg)
    if ratio<4.5: errors.append(f'Contrast {fg}/{bg}: {ratio:.2f}')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; local links/assets, landmarks, heading and ID structure, 6 complete cases, image alternatives and core text contrast.')

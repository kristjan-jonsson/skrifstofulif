#!/usr/bin/env python3
"""Býr til deilisíðu fyrir hverja skrýtlu (s/<ID>/index.html) úr comics.json. Keyrt í pages.yml við hverja birtingu.

Hver síða hefur Open Graph-merki svo Teams, Slack, Messenger o.fl. sýni sjálfa skrýtluna í forskoðun,
og sendir gesti svo áfram á skrýtluna á forsíðunni (/#<ID>).
Forskoðunarmynd (preview.jpg, 1200×630) er skrýtlan með spássíu svo ekkert skerist af; án Pillow er upprunalega myndin notuð.
"""
import json
import os
import sys
from html import escape

from build_feed import SITE, TITLE, key

try:
    from PIL import Image
except ImportError:
    Image = None

PREVIEW_SIZE = (1200, 630)
PREVIEW_BG = (246, 243, 236)  # --bg á forsíðunni


def preview(src, dst):
    if Image is None or not os.path.exists(src):
        return None
    im = Image.open(src).convert('RGB')
    W, H = PREVIEW_SIZE
    scale = min((W - 40) / im.width, (H - 40) / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    out = Image.new('RGB', PREVIEW_SIZE, PREVIEW_BG)
    out.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    out.save(dst, quality=88, optimize=True)
    return PREVIEW_SIZE


def page(c, out_dir):
    k = key(c)
    d = os.path.join(out_dir, k)
    os.makedirs(d, exist_ok=True)
    url = f'{SITE}s/{k}/'
    target = f'{SITE}#{k}'
    size = preview(c['image'], os.path.join(d, 'preview.jpg'))
    image = url + 'preview.jpg' if size else SITE + c['image']
    title = f"{TITLE} – {c['title']}"
    desc = c.get('alt') or c['title']
    e = lambda s: escape(s, quote=True)
    dims = f'\n<meta property="og:image:width" content="{size[0]}">\n<meta property="og:image:height" content="{size[1]}">' if size else ''
    html = f"""<!doctype html>
<html lang="is">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{TITLE}">
<meta property="og:locale" content="is_IS">
<meta property="og:title" content="{e(c['title'])}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{e(image)}">{dims}
<meta property="og:image:alt" content="{e(desc)}">
<meta name="twitter:card" content="summary_large_image">
<meta http-equiv="refresh" content="0; url={e(target)}">
<script>location.replace({json.dumps(target)});</script>
</head>
<body>
<p><a href="{e(target)}">{e(title)}</a></p>
</body>
</html>
"""
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main(src, out_dir):
    with open(src, encoding='utf-8') as f:
        comics = [c for c in json.load(f).get('comics', []) if c.get('date') and c.get('image') and c.get('title')]
    for c in comics:
        page(c, out_dir)
    print(f'{len(comics)} deilisíður í {out_dir}/' + ('' if Image else ' (án Pillow: engar forskoðunarmyndir)'))


if __name__ == '__main__':
    main(*(sys.argv[1:3] or ['comics.json', 's']))

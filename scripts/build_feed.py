#!/usr/bin/env python3
"""Býr til RSS-straum (feed.xml) úr comics.json. Keyrt í pages.yml við hverja birtingu."""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

SITE = 'https://skrifstofulif.oskasteinar.is/'
TITLE = 'Skrifstofulífið'
DESCRIPTION = 'Dagleg skrýtla úr skrifstofulífinu – ný myndasaga alla daga.'
MAX_ITEMS = 50


def key(c):
    return c.get('id') or c['date']


def pub_date(c):
    # Raunverulegur birtingartími: fyrsta commit myndarinnar (þarf fetch-depth: 0 í pages.yml)
    try:
        out = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%cI', '--', c['image']],
                             capture_output=True, text=True, check=True).stdout.split()
        if out:
            return datetime.fromisoformat(out[-1]).astimezone(timezone.utc)
    except (OSError, subprocess.CalledProcessError, ValueError):
        pass
    # Annars: engin klukkustund í comics.json: birtingartíminn 07:20 (Ísland = UTC), auk mínútu fyrir hverja aukaskrýtlu sama dag (-2, -3, …)
    y, m, d = map(int, c['date'].split('-'))
    suffix = key(c)[len(c['date']):].lstrip('-')
    n = int(suffix) if suffix.isdigit() else 0
    return datetime(y, m, d, 7, 20, tzinfo=timezone.utc) + timedelta(minutes=n)


def item(c):
    # <link> er deilisíðan (s/<ID>/) svo Teams o.fl. sýni forskoðun; forskoðunarmyndin er alltaf <link> + preview.jpg
    share = f'{SITE}s/{key(c)}/'
    thumb = share + 'preview.jpg'
    image = SITE + c['image']
    alt = c.get('alt') or c['title']
    size = os.path.getsize(c['image']) if os.path.exists(c['image']) else 0
    a = lambda v: escape(v, {'"': '&quot;'})
    html = f'<p><a href="{a(share)}"><img src="{a(image)}" alt="{a(alt)}"></a></p><p>{escape(alt)}</p>'
    return f"""    <item>
      <title>{escape(c['title'])}</title>
      <link>{escape(share)}</link>
      <guid isPermaLink="false">{escape(SITE + '#' + key(c))}</guid>
      <pubDate>{format_datetime(pub_date(c))}</pubDate>
      <description>{escape(alt)}</description>
      <content:encoded><![CDATA[{html}]]></content:encoded>
      <media:thumbnail url="{a(thumb)}" width="1200" height="630"/>
      <media:content url="{a(image)}" medium="image" type="image/png"/>
      <enclosure url="{a(image)}" type="image/png" length="{size}"/>
    </item>"""


def main(src, dst):
    with open(src, encoding='utf-8') as f:
        comics = [c for c in json.load(f).get('comics', []) if c.get('date') and c.get('image') and c.get('title')]
    comics.sort(key=lambda c: (c['date'], key(c)), reverse=True)
    comics.sort(key=pub_date, reverse=True)
    comics = comics[:MAX_ITEMS]
    updated = format_datetime(pub_date(comics[0]) if comics else datetime.now(timezone.utc))
    items = '\n'.join(item(c) for c in comics)
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>{TITLE}</title>
    <link>{SITE}</link>
    <description>{escape(DESCRIPTION)}</description>
    <language>is</language>
    <copyright>© 2026 Kristján Jónsson, CC BY 4.0</copyright>
    <lastBuildDate>{updated}</lastBuildDate>
    <atom:link href="{SITE}feed.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>{SITE}{comics[0]['image'] if comics else ''}</url>
      <title>{TITLE}</title>
      <link>{SITE}</link>
    </image>
{items}
  </channel>
</rss>
"""
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(xml)


if __name__ == '__main__':
    main(*(sys.argv[1:3] or ['comics.json', 'feed.xml']))

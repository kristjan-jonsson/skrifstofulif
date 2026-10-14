#!/usr/bin/env python3
"""Býr til RSS-straum (feed.xml) úr comics.json. Keyrt í pages.yml við hverja birtingu."""
import json
import os
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
    # Engin klukkustund í comics.json: 06:00 UTC, auk mínútu fyrir hverja aukaskrýtlu sama dag (-2, -3, …)
    y, m, d = map(int, c['date'].split('-'))
    suffix = key(c)[len(c['date']):].lstrip('-')
    n = int(suffix) if suffix.isdigit() else 0
    return datetime(y, m, d, 6, 0, tzinfo=timezone.utc) + timedelta(minutes=n)


def item(c):
    link = SITE + '#' + key(c)
    image = SITE + c['image']
    alt = c.get('alt') or c['title']
    size = os.path.getsize(c['image']) if os.path.exists(c['image']) else 0
    alt_attr = escape(alt, {'"': '&quot;'})
    body = f'<p><a href="{escape(link)}"><img src="{escape(image)}" alt="{alt_attr}"></a></p>'
    if c.get('alt'):
        body += f'<p>{escape(c["alt"])}</p>'
    return f"""    <item>
      <title>{escape(c['title'])}</title>
      <link>{escape(link)}</link>
      <guid isPermaLink="true">{escape(link)}</guid>
      <pubDate>{format_datetime(pub_date(c))}</pubDate>
      <description>{escape(body)}</description>
      <enclosure url="{escape(image)}" type="image/png" length="{size}"/>
    </item>"""


def main(src, dst):
    with open(src, encoding='utf-8') as f:
        comics = [c for c in json.load(f).get('comics', []) if c.get('date') and c.get('image') and c.get('title')]
    comics.sort(key=lambda c: (c['date'], key(c)), reverse=True)
    comics = comics[:MAX_ITEMS]
    updated = format_datetime(pub_date(comics[0]) if comics else datetime.now(timezone.utc))
    items = '\n'.join(item(c) for c in comics)
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{TITLE}</title>
    <link>{SITE}</link>
    <description>{escape(DESCRIPTION)}</description>
    <language>is</language>
    <lastBuildDate>{updated}</lastBuildDate>
    <atom:link href="{SITE}feed.xml" rel="self" type="application/rss+xml"/>
{items}
  </channel>
</rss>
"""
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(xml)


if __name__ == '__main__':
    main(*(sys.argv[1:3] or ['comics.json', 'feed.xml']))

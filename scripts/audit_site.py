"""Audit the built pages, language relationships and crawl metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
SITE = json.loads((ROOT / 'site.json').read_text())
BASE = SITE['url'].rstrip('/') + '/'
EXPECTED_LANGS = {'ru', 'en', 'el-CY', 'x-default'}

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.ids = []
        self.h1s = 0
        self.title = ''
        self.text = ''
        self.scripts = []
        self.in_title = False
        self.in_schema = False
        self.schema = ''
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'h1': self.h1s += 1
        if tag == 'title': self.in_title = True
        if tag == 'script' and a.get('type') == 'application/ld+json': self.in_schema = True
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'script' and self.in_schema:
            self.in_schema = False
            self.scripts.append(json.loads(self.schema))
            self.schema = ''
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_schema: self.schema += data
        else: self.text += data
    def attrs(self, tag, key, value):
        return [a for t, a in self.tags if t == tag and a.get(key) == value]

paths = sorted(DIST.rglob('*.html'))
pages = {p: Page(p.read_text()) for p in paths}
errors = []
rows = []
urls = {}
for p in paths:
    rel = p.relative_to(DIST).as_posix()
    urls[BASE + (rel[:-10] if rel.endswith('index.html') else rel)] = p

def require(ok, p, message):
    if not ok: errors.append(f'{p.relative_to(DIST)}: {message}')

for p, page in pages.items():
    lang = next(a['lang'] for t, a in page.tags if t == 'html')
    canonical = page.attrs('link', 'rel', 'canonical')
    require(len(canonical) == 1, p, 'one canonical required')
    if not canonical: continue
    url = canonical[0]['href']
    require(urls.get(url) == p, p, 'canonical must identify this page')
    descriptions = page.attrs('meta', 'name', 'description')
    require(len(descriptions) == 1 and bool(descriptions[0].get('content')), p, 'unique description required')
    require(bool(page.title), p, 'title required')
    require(page.h1s == 1, p, 'one h1 required')
    require(len(page.ids) == len(set(page.ids)), p, 'duplicate IDs')
    require(lang in EXPECTED_LANGS - {'x-default'}, p, 'invalid lang')
    require(lang == 'ru' or not re.search('[\u0400-\u04ff]', page.text.replace('Русский', '')), p, 'untranslated Cyrillic text')
    alts = page.attrs('link', 'rel', 'alternate')
    require(len(alts) == 4 and {a.get('hreflang') for a in alts} == EXPECTED_LANGS, p, 'language alternates incomplete')
    expected_alts = {a['hreflang']: a['href'] for a in alts}
    for a in alts:
        target = urls.get(a['href'])
        require(target in pages, p, 'alternate URL missing')
        if target in pages:
            reciprocal = {a['hreflang']: a['href'] for a in pages[target].attrs('link', 'rel', 'alternate')}
            require(reciprocal == expected_alts, p, 'hreflang is not reciprocal')
    for key, expected in [('og:title', page.title), ('og:description', descriptions[0]['content']), ('og:url', url)]:
        props = page.attrs('meta', 'property', key)
        require(len(props) == 1 and props[0].get('content') == expected, p, key + ' mismatch')
    for key in ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:image:alt']:
        require(len(page.attrs('meta', 'name', key)) == 1, p, key + ' missing')
    require(bool(page.scripts), p, 'structured data missing')
    graph = page.scripts[0]['@graph'] if page.scripts else []
    webpage = next((g for g in graph if g['@type'] == 'WebPage'), {})
    require(webpage.get('url') == url and webpage.get('inLanguage') == lang, p, 'schema URL or language mismatch')
    for tag, attrs in page.tags:
        for key in ['href', 'src']:
            if key not in attrs or attrs[key].startswith(('mailto:', 'tel:', 'data:', 'javascript:')): continue
            target_url = urlparse(urljoin(url, attrs[key]))
            if target_url.netloc != urlparse(BASE).netloc: continue
            target_path = unquote(target_url.path)
            prefix = urlparse(BASE).path
            require(target_path.startswith(prefix), p, 'internal link escapes the project')
            if not target_path.startswith(prefix): continue
            target = DIST / target_path[len(prefix):]
            if target.is_dir(): target = target / 'index.html'
            require(target.is_file(), p, 'missing local target ' + str(target.relative_to(DIST)))
            if target in pages and target_url.fragment:
                require(unquote(target_url.fragment) in pages[target].ids, p, 'missing fragment ' + target_url.fragment)
    rows.append({'page': p.relative_to(DIST).as_posix(), 'lang': lang, 'canonical': url, 'title': page.title,
                 'title_characters': len(page.title), 'description': descriptions[0]['content'], 'description_characters': len(descriptions[0]['content'])})
for field in ['title', 'description', 'canonical']:
    require(len({r[field] for r in rows}) == len(rows), paths[0], 'duplicate ' + field)
sitemap = ET.parse(DIST / 'sitemap.xml')
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
entries = sitemap.findall('s:url', ns)
require({e.find('s:loc', ns).text for e in entries} == set(urls), paths[0], 'sitemap URL mismatch')
for entry in entries:
    require({a.attrib['hreflang'] for a in entry.findall('x:link', ns)} == EXPECTED_LANGS, paths[0], 'sitemap alternates incomplete')
plain_entries = ET.parse(DIST / 'sitemap-pages.xml').findall('s:url', ns)
plain_urls = [e.find('s:loc', ns).text for e in plain_entries]
require(len(plain_urls) == len(urls) and set(plain_urls) == set(urls), paths[0], 'fallback sitemap URL mismatch')
report = {'pages_checked': len(pages), 'errors': errors, 'metadata': rows}
(ROOT / 'docs/metadata-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'pages_checked': len(pages), 'errors': errors}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))

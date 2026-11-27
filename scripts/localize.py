"""Render translated static pages and their language-specific search metadata."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode, urljoin
import json
import hashlib
import re
from datetime import date
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
LANGS = {'ru': ('ru', 'ru_RU'), 'en': ('en', 'en_GB'), 'el': ('el-CY', 'el_CY')}
NAMES = {'ru': 'Кипрский монитор', 'en': 'Cyprus Monitor', 'el': 'Παρατηρητήριο Κύπρου'}
BASE_TEXT = json.loads((ROOT / 'translations/ru.json').read_text())
SEO = json.loads((ROOT / 'content/seo.json').read_text())
SITE = json.loads((ROOT / 'site.json').read_text())
PARTNER = json.loads((ROOT / 'content/partner.json').read_text())
BASE = SITE['url'].rstrip('/') + '/'
FILES = list(SEO['ru'])
MONITOR = json.loads((ROOT / 'content/monitor.json').read_text())


def chronology_mapping(lang):
    """Keep long event translations separate from the shared interface strings."""
    if lang == 'ru':
        return {}
    rows = json.loads((ROOT / f'translations/chronology-{lang}.json').read_text())
    mapping = {}
    short = {
        'ru': ['', 'ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЙ', 'ИЮН', 'ИЮЛ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯ', 'ДЕК'],
        'en': ['', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
        'el': ['', 'ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΪ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ'],
    }
    months = {
        'ru': ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'],
        'en': ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'el': ['', 'Ιανουαρίου', 'Φεβρουαρίου', 'Μαρτίου', 'Απριλίου', 'Μαΐου', 'Ιουνίου', 'Ιουλίου', 'Αυγούστου', 'Σεπτεμβρίου', 'Οκτωβρίου', 'Νοεμβρίου', 'Δεκεμβρίου'],
    }
    def full(value, language):
        d = date.fromisoformat(value)
        return f'{d.day} {months[language][d.month]} {d.year}'
    for event in MONITOR['events']:
        if 'chronology_number' not in event:
            continue
        translated = rows[str(event['chronology_number'])]
        for field in ('title', 'summary', 'impact', 'date_label'):
            if not translated.get(field):
                raise ValueError(f'Missing {lang} chronology field: {event["id"]}.{field}')
            mapping[event[field]] = translated[field]
        provenance = translated['provenance']
        if event['provenance'].startswith('Статус источника: '):
            qualifier = re.sub(r'^[A-D](?: / [A-D])*,\s*', '', translated['grade_note']).rstrip('.')
            prefix = 'Source status: ' if lang == 'en' else 'Κατάσταση πηγής: '
            provenance = prefix + qualifier + '. ' + provenance
        mapping[event['provenance']] = provenance
        ru_date = 'Событие ' + event['date_label']
        target_date = ('Event ' if lang == 'en' else 'Γεγονός ') + translated['date_label']
        if event['discovered']:
            ru_date += ' · В мониторинге с ' + full(event['discovered'], 'ru')
            target_date += (' · Tracked since ' if lang == 'en' else ' · Παρακολουθείται από ') + full(event['discovered'], lang)
        mapping[ru_date] = target_date
        d = date.fromisoformat(event['date'])
        mapping[short['ru'][d.month] + ' ' + str(d.year)] = short[lang][d.month] + ' ' + str(d.year)
    mapping.update(dict(zip(short['ru'][1:], short[lang][1:])))
    for source, translated in rows['_sources'].items():
        mapping[source] = translated
        mapping[source + ' '] = translated + ' '
    return mapping


def asset_version(filename):
    return hashlib.sha256((DIST / 'assets' / filename).read_bytes()).hexdigest()[:12]


def page_url(lang, filename):
    return BASE + ('' if lang == 'ru' else lang + '/') + ('' if filename == 'index.html' else filename)


def partner_banner(lang, filename):
    copy = PARTNER['locales'][lang]
    page = Path(filename).stem
    query = urlencode({
        'utm_source': PARTNER['utm_source'],
        'utm_medium': PARTNER['utm_medium'],
        'utm_campaign': PARTNER['utm_campaign'],
        'utm_content': LANGS[lang][0] + '_' + page,
    })
    destination = urljoin(PARTNER['url'], copy['destination_language'])
    href = destination + '?' + query + '#' + PARTNER['anchor']
    return (
        '<aside class="partner-banner container" aria-labelledby="partner-title">'
        '<div class="partner-copy"><p class="partner-label">' + escape(copy['label']) + '</p>'
        '<h2 id="partner-title">' + escape(copy['title']) + '</h2>'
        '<p class="partner-description">' + escape(copy['description']) + '</p></div>'
        '<a class="partner-action" data-partner="trawelpulse" data-partner-page="' + page + '" '
        'href="' + escape(href, quote=True) + '" rel="sponsored noopener noreferrer">'
        + escape(copy['action']) + ' <span aria-hidden="true">↗</span></a></aside>'
    )


class Translator(HTMLParser):
    def __init__(self, lang):
        super().__init__(convert_charrefs=True)
        values = json.loads((ROOT / f'translations/{lang}.json').read_text())
        if len(values) != len(BASE_TEXT):
            raise ValueError(f'Incomplete {lang} translation')
        self.mapping = dict(zip(BASE_TEXT, values))
        self.mapping.update(chronology_mapping(lang))
        self.lang = lang
        self.out = []

    def text(self, text):
        if self.lang != 'ru' and re.search('[\u0400-\u04ff]', text) and text not in self.mapping:
            raise ValueError(f'Missing {self.lang} translation: {text}')
        return self.mapping.get(text, text)

    def handle_starttag(self, tag, attrs):
        updated = []
        for key, value in attrs:
            if value is not None:
                value = self.text(value)
                if key in ('href', 'src'):
                    if value == 'index.html':
                        value = './'
                    elif self.lang != 'ru' and value.startswith('assets/'):
                        if value == 'assets/cyprus-atlas.webp': value = 'assets/cyprus-atlas-' + self.lang + '.webp'
                        value = '../' + value
            updated.append(' ' + key + ('' if value is None else '="' + escape(value, quote=True) + '"'))
        self.out.append('<' + tag + ''.join(updated) + '>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.out.append('</' + tag + '>')

    def handle_data(self, text):
        self.out.append(escape(self.text(text), quote=False))

    def handle_comment(self, text):
        self.out.append('<!--' + text + '-->')


def head(lang, filename):
    meta = SEO[lang][filename]
    code, locale = LANGS[lang]
    title, description = meta['title'], meta['description']
    canonical = page_url(lang, filename)
    asset = '' if lang == 'ru' else '../'
    image = BASE + 'assets/cyprus-atlas' + ('' if lang == 'ru' else '-' + lang) + '.webp'
    tags = ['<meta charset="utf-8">', '<meta name="viewport" content="width=device-width,initial-scale=1">',
            '<meta name="theme-color" content="#f8f7f1">', '<meta name="robots" content="index,follow,max-image-preview:large">',
            '<title>' + escape(title) + '</title>', '<meta name="description" content="' + escape(description, quote=True) + '">',
            '<link rel="canonical" href="' + canonical + '">']
    for other, (other_code, _) in LANGS.items():
        tags.append(f'<link rel="alternate" hreflang="{other_code}" href="{page_url(other, filename)}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{page_url("en", filename)}">')
    properties = {'og:type': 'website', 'og:title': title, 'og:description': description, 'og:url': canonical,
                  'og:site_name': NAMES[lang], 'og:locale': locale, 'og:image': image,
                  'og:image:type': 'image/webp', 'og:image:width': '1400', 'og:image:height': '800',
                  'og:image:alt': {'ru': 'Карта Кипра в восточном Средиземноморье', 'en': 'Map of Cyprus in the eastern Mediterranean', 'el': 'Χάρτης της Κύπρου στην ανατολική Μεσόγειο'}[lang]}
    for prop, value in properties.items():
        tags.append(f'<meta property="{prop}" content="{escape(value, quote=True)}">')
    for other, (_, other_locale) in LANGS.items():
        if other != lang:
            tags.append(f'<meta property="og:locale:alternate" content="{other_locale}">')
    for name, value in {'twitter:card': 'summary_large_image', 'twitter:title': title, 'twitter:description': description, 'twitter:image': image, 'twitter:image:alt': properties['og:image:alt']}.items():
        tags.append(f'<meta name="{name}" content="{escape(value, quote=True)}">')
    for key, config in [('google-site-verification', 'google_site_verification'), ('msvalidate.01', 'bing_site_verification')]:
        if SITE.get(config):
            tags.append(f'<meta name="{key}" content="{escape(SITE[config], quote=True)}">')
    graph = [{'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': title,
              'description': description, 'inLanguage': code, 'dateModified': '2026-11-27',
              'isPartOf': {'@id': BASE + '#website'}},
             {'@type': 'WebSite', '@id': BASE + '#website', 'url': BASE, 'name': 'Cyprus Schengen Monitor', 'inLanguage': [v[0] for v in LANGS.values()]}]
    if filename != 'index.html':
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': NAMES[lang], 'item': page_url(lang, 'index.html')},
            {'@type': 'ListItem', 'position': 2, 'name': title, 'item': canonical}]})
    tags.append('<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c') + '</script>')
    tags.extend([f'<link rel="icon" href="{asset}assets/mark.svg" type="image/svg+xml">',
                 f'<link rel="stylesheet" href="{asset}assets/site.css?v={asset_version("site.css")}">',
                 f'<script defer src="{asset}assets/site.js?v={asset_version("site.js")}"></script>',
                 f'<script defer src="{asset}assets/analytics.js?v={asset_version("analytics.js")}" data-measurement-id="{escape(SITE.get("measurement_id", ""), quote=True)}"></script>'])
    return '\n'.join(tags)


def localize():
    questions = json.loads((ROOT / 'content/questions.json').read_text())
    originals = {f: (DIST / f).read_text() for f in FILES}
    for lang, (code, _) in LANGS.items():
        output = DIST if lang == 'ru' else DIST / lang
        output.mkdir(exist_ok=True)
        for filename, html in originals.items():
            body = html.split('<body>', 1)[1].rsplit('</body>', 1)[0]
            translator = Translator(lang)
            translator.feed(body)
            body = ''.join(translator.out)
            if lang == 'ru':
                body = body.replace('Разрешить Google Analytics? Это помогает понять, какие материалы полезны. ', 'Разрешить cookies Google Analytics для статистики посещений? ')
                body = body.replace('Настройки аналитики', 'Настройки cookies')
                body = body.replace('>Разрешить</button>', '>Принять</button>').replace('>Отказаться</button>', '>Отклонить</button>')
            q = questions[lang]
            if filename == 'index.html':
                articles = ''.join('<article class="note"><h3>' + escape(title) + '</h3><div><p>' + escape(answer) + '</p><a href="' + escape(href, quote=True) + '">' + escape(label) + '</a></div></article>' for title, answer, href, label in q['items'])
                body = body.replace('</main>', '<section class="reading"><h2>' + escape(q['heading']) + '</h2>' + articles + '</section></main>')
            body = body.replace('</footer>', '<p class="container independence">' + escape(q['disclaimer']) + '</p></footer>')
            switches = []
            for other, (other_code, _) in LANGS.items():
                href = ('' if lang == 'ru' else '../') + ('' if other == 'ru' else other + '/') + filename
                label = {'ru': 'Русский', 'en': 'English', 'el': 'Ελληνικά'}[other]
                current = ' aria-current="page"' if other == lang else ''
                switches.append(f'<a href="{href}" lang="{other_code}" hreflang="{other_code}"{current}>{label}</a>')
            nav_label = {'ru': 'Язык', 'en': 'Language', 'el': 'Γλώσσα'}[lang]
            body = body.replace('</header>', f'<nav class="language-nav container" aria-label="{nav_label}">' + ' · '.join(switches) + '</nav></header>')
            if filename != 'privacy.html':
                body = body.replace('</header>', '</header>' + partner_banner(lang, filename), 1)
            (output / filename).write_text(f'<!DOCTYPE html>\n<html lang="{code}"><head>\n{head(lang, filename)}\n</head><body>{body}</body></html>\n')
    # One sitemap includes every canonical language URL and reciprocal alternates.
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    xhtml = 'http://www.w3.org/1999/xhtml'
    ET.register_namespace('', ns)
    ET.register_namespace('xhtml', xhtml)
    urlset = ET.Element(f'{{{ns}}}urlset')
    for lang in LANGS:
        for filename in FILES:
            url = ET.SubElement(urlset, f'{{{ns}}}url')
            ET.SubElement(url, f'{{{ns}}}loc').text = page_url(lang, filename)
            ET.SubElement(url, f'{{{ns}}}lastmod').text = '2026-11-27'
            for other, (other_code, _) in LANGS.items():
                ET.SubElement(url, f'{{{xhtml}}}link', {'rel': 'alternate', 'hreflang': other_code, 'href': page_url(other, filename)})
            ET.SubElement(url, f'{{{xhtml}}}link', {'rel': 'alternate', 'hreflang': 'x-default', 'href': page_url('en', filename)})
    ET.ElementTree(urlset).write(DIST / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    # Minimal protocol-only fallback, independently fetchable in Search Console.
    plain = ET.Element(f'{{{ns}}}urlset')
    for lang in LANGS:
        for filename in FILES:
            url = ET.SubElement(plain, f'{{{ns}}}url')
            ET.SubElement(url, f'{{{ns}}}loc').text = page_url(lang, filename)
            ET.SubElement(url, f'{{{ns}}}lastmod').text = '2026-11-27'
    ET.indent(plain, space='  ')
    ET.ElementTree(plain).write(DIST / 'sitemap-pages.xml', encoding='utf-8', xml_declaration=True)



if __name__ == '__main__':
    localize()

from pathlib import Path
from html import escape
from datetime import date
import json
root=Path(__file__).parent
dist=root/'dist'
data=json.loads((root/'content/monitor.json').read_text())
events=data['events']
sources=data['sources']
site=json.loads((root/'site.json').read_text())
base_url=site['url'].rstrip('/')+'/'
months=['','января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
short=['','ЯНВ','ФЕВ','МАР','АПР','МАЙ','ИЮН','ИЮЛ','АВГ','СЕН','ОКТ','НОЯ','ДЕК']
categories={'procedure':'Процедура','technical':'Техническая готовность','politics':'Политика'}
sections=[('index.html','Обзор'),('timeline.html','Хронология'),('forecast.html','Прогноз'),('participants.html','Участники'),('sources.html','Источники')]
def icon(name,size=16):
    drawings={'arrow':'<path d="M4 12h15m-6-6 6 6-6 6"/>','external':'<path d="M6 18 18 6M7 6h11v11"/>','calendar':'<rect x="3.5" y="5.5" width="17" height="15" rx="1.5"/><path d="M7.5 3v5m9-5v5M4 10h16"/>','clock':'<circle cx="12" cy="12" r="8.5"/><path d="M12 6.5V12l3.5 2"/>','pin':'<circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="1.6"/><path d="M12 1v4m0 14v4M1 12h4m14 0h4"/>','book':'<path d="M3 4h6a3 3 0 0 1 3 3v14a4 4 0 0 0-4-3H3zM21 4h-6a3 3 0 0 0-3 3v14a4 4 0 0 1 4-3h5z"/>','chevron':'<path d="m7 10 5 5 5-5"/>','search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>','menu':'<path d="M3 6h18M3 12h18M3 18h18"/>','trend':'<path d="m3 16 6-6 4 4 8-9m-6 0h6v6"/>','layers':'<path d="m12 3 9 5-9 5-9-5zm-9 9 9 5 9-5m-18 4 9 5 9-5"/>','file':'<path d="M5 3h9l5 5v13H5zM14 3v6h5M8 13h8m-8 4h6"/>','down':'<path d="M12 3v17m-6-6 6 6 6-6"/>'}
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{drawings[name]}</svg>'
def external(url,label,cls=''):
    return f'<a class="out {cls}" href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)} {icon("external",13)}</a>'
def ref(i,label=None):
    return external(sources[i]['url'],label or sources[i]['name'])
def refs(indices):
    return '<div class="reference-links">'+''.join(ref(i) for i in indices)+'</div>'
def full_date(value):
    d=date.fromisoformat(value)
    return f'{d.day} {months[d.month]} {d.year}'
def datetile(value):
    d=date.fromisoformat(value)
    return f'<span class="datetile"><strong>{d.day:02d}</strong><span>{short[d.month]} {d.year}</span></span>'
def nav(href,title,current):
    active=' aria-current="page"' if href==current else ''
    return f'<a href="{href}"{active}>{title}</a>'
brand='<img src="assets/mark.svg" alt="" width="35" height="35"><span>Кипрский монитор</span>'
def heading(label,title,intro):
    return f'<div class="page-heading"><div class="kicker"><i></i>{label}</div><h1>{title}</h1><p>{intro}</p></div>'
def page(filename,title,main):
    canonical=base_url+('' if filename=='index.html' else filename)
    seo=f'<link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Кипрский монитор"><meta property="og:title" content="{escape(title)} · Кипрский монитор"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{base_url}assets/cyprus-atlas.webp"><meta name="twitter:card" content="summary_large_image">'
    menus=''.join(nav(h,l,filename) for h,l in sections)
    foot=f'<footer><div class="container footer-in"><a class="brand small" href="index.html">{brand}</a><span>Материалы на 27 ноября 2026</span><a href="privacy.html">Конфиденциальность</a></div></footer>'
    html=f'''<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f8f7f1"><meta name="description" content="Вступление Кипра в Шенген: решения Совета ЕС, позиции стран, хронология и прогноз сроков по состоянию на 27 ноября 2026 года.">{seo}<title>{title} · Кипрский монитор</title><link rel="icon" href="assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><script defer src="assets/site.js"></script><script defer src="assets/analytics.js" data-measurement-id="{escape(site.get('measurement_id',''),quote=True)}"></script></head><body><a class="skip" href="#main">К содержанию</a><header><div class="container masthead"><a class="brand" href="index.html" aria-label="Кипрский монитор, на главную">{brand}</a><nav aria-label="Разделы">{menus}</nav><div class="edition">{icon('calendar',15)}<time datetime="2026-11-27">27 ноября 2026</time></div></div></header><main id="main" class="container">{main}</main>{foot}<div id="analytics-consent" class="analytics-consent" hidden role="region" aria-label="Настройки аналитики"><p>Разрешить Google Analytics? Это помогает понять, какие материалы полезны. <a href="privacy.html">Об аналитике</a></p><button type="button" data-consent="granted">Разрешить</button><button type="button" data-consent="denied">Отказаться</button></div></body></html>'''
    (dist/filename).write_text(html)
def tag(e):
    return f'<span class="topic {e["type"]}">{categories[e["type"]]}</span>'
def grade(e):
    return '<span class="grade">Уровень '+escape(e['grade'])+'</span>'
def news(e):
    return f'''<article class="news-row">{datetile(e["discovered"])}<div><div class="event-tags">{tag(e)}{grade(e)}</div><h3><a href="timeline.html#{e["id"]}">{e["title"]}</a></h3><p>{e["summary"]}</p><a href="timeline.html#{e["id"]}" class="small-link">Подробнее {icon('arrow',13)}</a></div></article>'''
mapcard=f'''<figure class="atlas"><img src="assets/cyprus-atlas.webp" width="1400" height="800" alt="Карта Кипра с Никосией, Пафосом и Ларнакой в восточном Средиземноморье"><figcaption><span>{icon('pin',14)} Восточное Средиземноморье</span><span>35° с. ш. &nbsp; 33° в. д.</span></figcaption></figure>'''
hero=f'''<section class="hero"><div class="hero-content"><div class="kicker"><i></i>Мониторинг вступления</div><h1>Кипр и <em>Шенген</em></h1><p>Еврокомиссия положительно оценила готовность Кипра. Совету ЕС ещё предстоит утвердить дату вступления.</p><div class="hero-actions"><a class="primary" href="timeline.html">Хронология событий {icon('arrow',16)}</a><a class="text-action" href="sources.html">Источники {icon('arrow',15)}</a></div></div>{mapcard}</section>'''
strip=f'''<section class="summary-strip" aria-label="Коротко о вступлении"><div><span class="micro">Текущий статус</span><strong><i class="status-dot"></i>В процессе вступления</strong></div><div><span class="micro">Политический ориентир</span><strong>1 июля 2027 <small>· позиция Греции</small></strong></div><div><span class="micro">Ближайшее заседание</span><strong>3–4 декабря 2026 <small>· Совет ЕС</small></strong></div></section>'''
forecast_card=f'''<aside class="aside"><div class="forecast-card"><div class="micro">{icon('trend',18)} Рабочий прогноз</div><strong class="year">2027</strong><p>Вступление возможно в течение года, если страны ЕС согласуют условия.</p><a href="forecast.html">Разобрать сценарии {icon('arrow',17)}</a></div><div class="upcoming"><div class="micro">{icon('calendar',16)} Ближайшее событие</div><h3>3–4 декабря</h3><p>Совет ЕС по юстиции и внутренним делам. Комиссия готовит сообщение по Кипру.</p>{ref(39,'Страница заседания')}</div></aside>'''
overview=hero+strip+f'''<div class="overview-grid" id="latest"><section class="feed"><div class="section-head"><h2>Последние изменения</h2><a class="sub-link" href="timeline.html">Вся хронология {icon('arrow',15)}</a></div>{''.join(news(e) for e in events[:3])}</section>{forecast_card}</div>'''
page('index.html','Кипр и Шенген',overview)
def entry(e):
    discovered=f' · В мониторинге с {full_date(e["discovered"])}' if e['discovered'] else ''
    return f'''<details id="{e['id']}" class="timeline-entry" data-category="{e['type']}"><summary>{datetile(e['date'])}<span class="entry-title"><span class="event-tags">{tag(e)}{grade(e)}</span><strong>{e['title']}</strong></span><span class="expand">{icon('chevron',18)}</span></summary><div class="details-body"><p class="entry-dates">Событие {full_date(e['date'])}{discovered}</p><p>{e['summary']} {e['detail']}</p><h3>Что это меняет</h3><p>{e['impact']}</p>{refs(e['refs'])}</div></details>'''
filters=''.join(f'<button type="button" data-filter="{k}" aria-pressed="{str(k=="all").lower()}">{s}</button>' for k,s in [('all','Все события'),('procedure','Процедура'),('technical','Техника'),('politics','Политика')])
timeline=heading('Документы и события','Хронология','События идут от новых к ранним. Раскройте запись, чтобы увидеть источник, дату публикации и влияние на прогноз.')
timeline+=f'''<div class="archive-tools" hidden><div class="chips" aria-label="Фильтр событий по теме">{filters}</div><label class="search">{icon('search',17)}<input type="search" id="query" aria-label="Поиск по событиям" placeholder="Поиск по событиям"></label></div><p id="event-count" class="count" aria-live="polite"></p><section class="entries" aria-label="События по датам">'''+''.join(entry(e) for e in sorted(events,key=lambda e:(e['date'],e['discovered']),reverse=True))+'''</section><div class="no-results" hidden><p>По этому запросу событий нет.</p><button class="primary reset" type="button">Сбросить фильтры</button></div>'''
page('timeline.html','Хронология событий',timeline)
forecast=heading('Аналитическая оценка · уровень D','Прогноз вступления','Рабочий горизонт — 2027 год. Точность прогноза зависит от закрытия планов, условий пограничного контроля и согласия государств.')
forecast+='''<div class="scenario-grid"><article class="scenario"><div class="micro">Ускоренный сценарий</div><h2>К 1 июля <em>2027</em></h2><p>Потребуются скорое закрытие планов, согласование особых режимов, консультация Европарламента и единогласное решение Совета.</p><p class="footnote">Уверенность в точной дате низкая.</p></article><article class="scenario chosen"><div class="micro">Рабочий сценарий</div><h2>В течение <em>2027</em></h2><p>Процедуры завершаются в течение года, если страны договорятся о правилах контроля и удастся избежать длительной блокировки.</p><p class="footnote">Уверенность в годовом горизонте средняя.</p></article><article class="scenario"><div class="micro">При задержке</div><h2>Конец 2027 <em>и позже</em></h2><p>Затяжные правовые или политические разногласия могут перенести вступление на конец 2027-го, 2028 год или более поздний срок.</p><p class="footnote">Резервный сценарий.</p></article></div>'''
def note(title,body,indices):
    return f'<article class="note"><h3>{title}</h3><div><p>{body}</p>{refs(indices)}</div></article>'
forecast+='<section class="reading"><h2>Что изменит прогноз</h2>'
forecast+=note('Закрытие шести планов','В проекте перечислены защита данных, возврат, внешние границы, полиция, визы и SIS. Опубликованный акт о закрытии уточнит, какие технические условия выполнены.',[19,21])
forecast+=note('Зелёная линия и базы','Предстоит согласовать учёт въездов и выездов при особом статусе Зелёной линии и порядок проверок на переходах британских баз. ЕС и Великобритания уже подтвердили работу по протоколу.',[29,3,38])
forecast+=note('Готовность аэропортов','Значение тендера в Пафосе и Ларнаке для июльского срока зависит от того, требуется ли ввод новых кабин до начала полного применения правил.',[1,2])
forecast+=note('Политическое решение','Поддержка Греции помогает переговорам. Дату и охват полного применения правил определит принятый Советом акт после консультации с Европарламентом.',[6,32])
forecast+='</section>'
page('forecast.html','Прогноз вступления',forecast)
people=heading('Политические позиции','Участники','Кто участвует в принятии решения, кто влияет на переговоры и чем подтверждается позиция каждой стороны.')
for p in data['people']:
    people+=f'''<article class="actor"><div><span class="micro">{p['role']}</span><h2>{p['name']}</h2></div><div><span class="grade">Уровень {p['grade']}</span><p>{p['summary']}</p>{refs(p['refs'])}</div></article>'''
page('participants.html','Участники и позиции',people)
directory=heading('Основания мониторинга','Источники','Шкала A–D показывает, что именно подтверждает материал. Буква описывает тип свидетельства. Вероятность вступления оценивается отдельно.')
levels=[('A','Документ','Правовой акт, запись в официальном реестре или опубликованная повестка.'),('B','Официальная позиция','Заявление должностного лица или совместное политическое обязательство.'),('C','Публикация СМИ','Репортаж, интервью или оценка, требующая атрибуции и сверки.'),('D','Аналитический вывод','Условная оценка влияния события на сроки и сценарии.')]
directory+='<section class="grade-grid" aria-label="Уровни достоверности">'+''.join(f'<div class="level"><span>{k}</span><h2>{t}</h2><p>{b}</p></div>' for k,t,b in levels)+'</section>'
groups=[('Правовой статус и документы ЕС',[8,32,9,12,15,19,21,22,0,7,23,39,40,13,29]),('Заявления государств и международных организаций',[6,33,14,11,16,17,3,4,27,24,20,10]),('Инфраструктура и независимые публикации',[1,2,5,38,30,31,18,25,26])]
for title,ids in groups:
    directory+=f'<section class="sources-group"><h2>{title}</h2><div class="documents">'+''.join(f'<div>{icon("file",17)}{ref(i)}</div>' for i in ids)+'</div></section>'
directory+='<div class="market"><div class="micro">Об этом выпуске</div><p>Сайт отражает состояние досье на 27 ноября 2026 года.</p>'+'</div>'
page('sources.html','Источники и шкала оценок',directory)

page('privacy.html','Конфиденциальность',heading('Настройки сайта','Конфиденциальность','На сайте можно разрешить или отключить статистику посещений.')+'<section class="reading"><button type="button" data-analytics-settings>Настройки аналитики</button><p>Сайт размещён на GitHub Pages. Google Analytics 4 загружается только после вашего согласия и помогает измерять просмотры страниц, переходы по ссылкам на источники, использование фильтров и раскрытие событий.</p><p>Мы не передаём в аналитику текст поисковых запросов на сайте. Рекламная персонализация и Google Signals отключены в коде счётчика. Выбор сохраняется в браузере. Изменить его можно кнопкой «Настройки cookies» на этой странице. При отключении аналитики сайт удаляет доступные ему cookies _ga.</p><p><a href="https://policies.google.com/privacy" rel="noopener noreferrer">Политика конфиденциальности Google</a> · <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener noreferrer">Политика конфиденциальности GitHub</a></p></section>')
urls=[base_url+('' if f=='index.html' else f) for f,_ in sections]+[base_url+'privacy.html']
(dist/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(u)+'</loc></url>' for u in urls)+'</urlset>\n')
(dist/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base_url+'sitemap.xml\n')
(dist/'.nojekyll').touch()

from scripts.localize import localize
localize()

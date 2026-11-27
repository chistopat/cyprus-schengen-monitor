(() => {
  const id = document.currentScript.dataset.measurementId;
  if (!/^G-[A-Z0-9]+$/.test(id)) return;
  const key = 'analytics-consent';
  const production = location.hostname === new URL(document.querySelector('link[rel=canonical]').href).hostname;
  const panel = document.getElementById(key);
  let loaded = false;
  let consent = null;
  try { consent = localStorage.getItem(key); } catch {}
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
  function enable() {
    window['ga-disable-' + id] = false;
    window.gtag('consent', 'update', {analytics_storage: 'granted'});
    if (loaded) return;
    loaded = true;
    if (!production) return;
    window.gtag('js', new Date());
    window.gtag('config', id, {allow_google_signals: false, allow_ad_personalization_signals: false, page_location: location.origin + location.pathname});
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.append(script);
  }
  function disable() {
    window.gtag('consent', 'update', {analytics_storage: 'denied'});
    window['ga-disable-' + id] = true;
    for (const cookie of document.cookie.split(';')) {
      const name = cookie.split('=')[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) continue;
      for (const domain of ['', '; domain=' + location.hostname, '; domain=.' + location.hostname]) {
        for (const path of ['/', '/cyprus-schengen-monitor/']) document.cookie = name + '=; Max-Age=0; path=' + path + domain;
      }
    }
  }
  function event(name, params) {
    if (production && consent === 'granted') window.gtag('event', name, {...params, site_language: document.documentElement.lang});
  }
  for (const button of document.querySelectorAll('[data-consent]')) button.addEventListener('click', () => {
    consent = button.dataset.consent;
    try { localStorage.setItem(key, consent); } catch {}
    if (consent === 'granted') enable(); else disable();
    panel.hidden = true;
  });
  for (const button of document.querySelectorAll('[data-analytics-settings]')) button.addEventListener('click', () => { panel.hidden = false; });
  document.addEventListener('click', e => {
    const link = e.target.closest('a[href]');
    if (link && link.dataset.partner) {
      event('partner_click', {partner: link.dataset.partner, placement: 'top_banner', source_page: link.dataset.partnerPage, link_url: link.href});
    } else if (link && link.origin !== location.origin) {
      event('source_click', {link_domain: link.hostname, link_url: link.origin + link.pathname});
    }
    const filter = e.target.closest('[data-filter]');
    if (filter) event('timeline_filter', {filter: filter.dataset.filter});
  });
  for (const entry of document.querySelectorAll('.timeline-entry')) entry.addEventListener('toggle', () => {
    if (entry.open) event('timeline_open', {event_id: entry.id});
  });
  if (consent === 'granted') enable();
  else if (consent !== 'denied') panel.hidden = false;
})();

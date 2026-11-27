(() => {
  const archive = document.querySelector('.archive-tools');
  if (!archive) return;
  const entries = [...document.querySelectorAll('.timeline-entry')];
  const buttons = [...archive.querySelectorAll('[data-filter]')];
  const search = document.getElementById('query');
  const count = document.getElementById('event-count');
  const lang = document.documentElement.lang;
  const counts = lang.startsWith('el') ? ['Εμφανίζονται γεγονότα: ', ' από '] : lang === 'en' ? ['Showing events: ', ' of '] : ['Показано событий: ', ' из '];
  const empty = document.querySelector('.no-results');
  let selected = 'all';
  const normalized = text => text.toLocaleLowerCase('ru').replaceAll('ё','е').trim();
  const searchable = new Map(entries.map(item => [item, normalized(item.textContent)]));
  function applyFilters() {
    const terms = normalized(search.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const entry of entries) {
      const matches = (selected === 'all' || entry.dataset.category === selected) &&
        terms.every(term => searchable.get(entry).includes(term));
      entry.hidden = !matches;
      if (matches) visible++;
    }
    for (const button of buttons) {
      button.setAttribute('aria-pressed', String(button.dataset.filter === selected));
    }
    count.textContent = counts[0] + visible + counts[1] + entries.length;
    empty.hidden = visible !== 0;
  }
  function followFragment() {
    const entry = entries.find(item => '#' + item.id === location.hash);
    if (!entry) return;
    if (entry.hidden) {
      search.value = '';
      selected = 'all';
      applyFilters();
    }
    entry.open = true;
    requestAnimationFrame(() => entry.scrollIntoView({block:'start'}));
  }
  for (const button of buttons) button.addEventListener('click', () => {
    selected = button.dataset.filter;
    applyFilters();
  });
  search.addEventListener('input', applyFilters);
  empty.querySelector('button').addEventListener('click', () => {
    selected = 'all';
    search.value = '';
    applyFilters();
    search.focus();
  });
  archive.hidden = false;
  applyFilters();
  followFragment();
  window.addEventListener('hashchange', followFragment);
})();

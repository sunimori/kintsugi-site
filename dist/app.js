(() => {
  'use strict';
  const copies = window.KINTSUGI_COPY;
  const normalize = value => {
    if (!value) return null;
    if (copies[value]) return value;
    const v = value.toLowerCase().replace('_', '-');
    if (v.startsWith('zh')) return /hant|tw|hk|mo/.test(v) ? 'zh-Hant' : 'zh-Hans';
    if (v.startsWith('pt')) return 'pt-BR';
    return copies[v.split('-')[0]] ? v.split('-')[0] : null;
  };
  const setLanguage = (locale, persist = false) => {
    const copy = copies[locale];
    if (!copy) return;
    document.documentElement.lang = locale;
    document.documentElement.dataset.script = /^(ja|ko|zh)/.test(locale) ? 'cjk' : 'latin';
    document.querySelectorAll('[data-t]').forEach(el => { el.textContent = copy[el.dataset.t]; });
    document.querySelectorAll('[data-label]').forEach(el => el.setAttribute('aria-label', copy[el.dataset.label]));
    document.querySelectorAll('[data-alt]').forEach(el => el.alt = copy[el.dataset.alt]);
    const select = document.querySelector('#language');
    select.value = locale;
    select.setAttribute('aria-label', copy.language);
    document.title = copy[document.body.dataset.title] + (document.body.dataset.title === 'title' ? '' : ' — 金継 KINTSUGI');
    document.querySelector('meta[name="description"]').content = copy.description;
    document.querySelector('meta[property="og:title"]').content = document.title;
    document.querySelector('meta[property="og:description"]').content = copy.description;
    document.querySelectorAll('a[href]').forEach(a => {
      const url = new URL(a.getAttribute('href'), location.href);
      if (url.origin === location.origin || url.hostname === 'sunimori.com') {
        url.searchParams.set('lang', locale);
        a.href = url.href;
      }
    });
    if (persist) {
      try { localStorage.setItem('kintsugi.language', locale); } catch {}
      const url = new URL(location.href); url.searchParams.set('lang', locale); history.replaceState(null, '', url);
    }
  };
  let saved; try { saved = localStorage.getItem('kintsugi.language'); } catch {}
  setLanguage(normalize(new URLSearchParams(location.search).get('lang')) || normalize(saved) || (navigator.languages || [navigator.language]).map(normalize).find(Boolean) || 'en');
  document.querySelector('#language').addEventListener('change', e => setLanguage(e.target.value, true));
  const menu = document.querySelector('.menu');
  const closeMenu = () => { menu.setAttribute('aria-expanded','false'); document.body.classList.remove('menu-open'); };
  menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); document.body.classList.toggle('menu-open', open); });
  document.querySelectorAll('#navigation a').forEach(a => a.addEventListener('click',closeMenu));
  document.addEventListener('keydown', e => { if(e.key === 'Escape') closeMenu(); });
  matchMedia('(min-width: 761px)').addEventListener('change', closeMenu);
  const tabs = [...document.querySelectorAll('[data-panel]')];
  const activate = tab => {
    tabs.forEach(t => { const active = t === tab; t.setAttribute('aria-selected', String(active)); t.tabIndex = active ? 0 : -1; document.querySelector('#panel-' + t.dataset.panel).hidden = !active; });
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => activate(tab));
    tab.addEventListener('keydown', e => {
      const idx = {ArrowRight:(i+1)%tabs.length, ArrowLeft:(i+tabs.length-1)%tabs.length, Home:0, End:tabs.length-1}[e.key];
      if(idx === undefined) return;
      e.preventDefault(); activate(tabs[idx]); tabs[idx].focus();
    });
  });
  const updateHeader = () => document.body.classList.toggle('scrolled', scrollY > 32);
  window.addEventListener('scroll', updateHeader, {passive:true}); updateHeader();
})();

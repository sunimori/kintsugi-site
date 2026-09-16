"""Build a dependency-free, public-only static website."""
from pathlib import Path
from html import escape
import json
from content import COPY, LANGUAGES

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
for k, v in COPY.items():
    assert len(v) == len(LANGUAGES) and all(v), k

def t(key, tag='span', cls=''):
    return f'<{tag} class="{cls}" data-t="{key}">{escape(COPY[key][0])}</{tag}>'

arrow = '<span aria-hidden="true">↗</span>'
brand = '<span class="brand-kanji" lang="ja">金継</span><span class="brand-latin">KINTSUGI</span>'
header = f'''<header class="site-header"><div class="wrap nav-wrap"><a href="/" class="brand" aria-label="金継 KINTSUGI">{brand}</a><nav id="navigation" aria-label="Main"><a href="/#craft">{t('nav_game')}</a><a href="/#world">{t('nav_world')}</a><a href="/#release">{t('nav_release')}</a></nav><div class="nav-tools"><label class="language"><span class="sr-only" data-t="language">言語</span><select id="language" aria-label="言語">{''.join(f'<option value="{c}" lang="{c}">{n}</option>' for c,n in LANGUAGES)}</select></label><button class="menu" aria-expanded="false" aria-controls="navigation" aria-label="メニュー" data-label="menu"><span></span><span></span></button></div></div></header>'''
footer = f'''<footer><div class="wrap footer-top"><a class="brand" href="/">{brand}</a>{t('footer_note','p')}<div class="footer-links"><a href="/support/">{t('support')}</a><a href="/privacy/">{t('privacy')}</a><a href="https://sunimori.com/" target="_blank" rel="noopener noreferrer">Sunimori {arrow}</a></div></div><div class="wrap footer-bottom"><span>© 2026 Sunimori</span><span>CRAFTED WITH CARE.</span></div></footer>'''

def page(route, body, title='title', home=False):
    url = 'https://playkintsugi.com' + route
    html = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(COPY[title][0])}</title><meta name="description" content="{escape(COPY['description'][0],quote=True)}"><meta name="theme-color" content="#111210"><meta name="referrer" content="strict-origin-when-cross-origin"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'"><link rel="canonical" href="{url}"><meta property="og:title" content="{escape(COPY[title][0],quote=True)}"><meta property="og:description" content="{escape(COPY['description'][0],quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:site_name" content="金継 KINTSUGI"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/icon.png"><link rel="stylesheet" href="/style.css"><script src="/locales.js" defer></script><script src="/app.js" defer></script></head><body class="{'home' if home else 'inner-page'}" data-title="{title}"><a class="skip" href="#main">{t('skip')}</a>{header}<main id="main">{body}</main>{footer}</body></html>'''
    dest = DIST / ('404.html' if route == '/404.html' else route.strip('/') + '/index.html' if route != '/' else 'index.html')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)

hero = f'''<section class="hero"><img class="hero-art" src="/assets/hero.webp" width="1672" height="941" alt="" fetchpriority="high"><div class="hero-shade"></div><div class="wrap hero-inner"><div class="hero-copy"><p class="eyebrow">{t('eyebrow')}</p><h1>{t('hero1')}<em>{t('hero2')}</em></h1>{t('hero_body','p','hero-body')}<div class="hero-actions"><a class="button cream" href="#craft">{t('explore')}<span class="button-circle" aria-hidden="true">↗</span></a>{t('coming','span','coming')}</div></div><div class="hero-bottom"><a href="#craft">{t('scroll')} <span aria-hidden="true">↓</span></a><span class="hero-edition">SUNIMORI — 金継</span></div></div></section>'''
intro = f'''<section class="intro wrap" id="craft"><div class="section-side"><p class="eyebrow">{t('intro_label')}</p><span class="seal" lang="ja" aria-hidden="true">継</span></div><div class="intro-copy">{t('intro_title','h2')}{t('intro_body','p')}</div></section>'''
panels = ''.join(f'''<section class="experience-panel" id="panel-{key}" role="tabpanel" aria-labelledby="tab-{key}" {'hidden' if i else ''}><div class="panel-text"><span class="panel-num">0{i+1}</span>{t(key+'_title','h3')}{t(key+'_body','p')}<div class="panel-rule" aria-hidden="true"></div><span class="panel-signature" lang="ja">{'修繕' if i==0 else '器の蔵' if i==1 else '工房'}</span></div><figure class="screen-frame"><img src="/assets/{key}.webp" alt="{escape(COPY[key+'_title'][0],quote=True)}" data-alt="{key}_title" width="660" height="1435" loading="lazy"></figure></section>''' for i,key in enumerate(['mend','collect','grow']))
play = f'''<section class="play-section wrap"><div class="section-heading"><div><p class="eyebrow">{t('play_label')}</p>{t('play_title','h2')}</div><div class="experience-tabs" role="tablist" aria-label="Kintsugi"><button id="tab-mend" role="tab" aria-selected="true" aria-controls="panel-mend" data-panel="mend">01 {t('mend')}</button><button id="tab-collect" role="tab" aria-selected="false" aria-controls="panel-collect" tabindex="-1" data-panel="collect">02 {t('collect')}</button><button id="tab-grow" role="tab" aria-selected="false" aria-controls="panel-grow" tabindex="-1" data-panel="grow">03 {t('grow')}</button></div></div><div class="experience-stage">{panels}</div>{t('screens_note','p','screens-note')}</section>'''
world = f'''<section id="world" class="world"><div class="wrap world-inner"><figure class="tsugi-art"><img src="/assets/spirit-tsugi.webp" width="896" height="1344" loading="lazy" alt="継 / Tsugi"><figcaption>{t('tsugi')}</figcaption></figure><div class="world-copy"><p class="eyebrow">{t('world_label')}</p>{t('world_title','h2')}{t('world_body','p','world-body')}<div class="spirit-gallery">{''.join(f'<figure><img src="/assets/spirit-{img}.webp" width="460" height="690" loading="lazy" alt="{COPY[key][0]}"><figcaption>{t(key)}</figcaption></figure>' for img,key in [('usurai','usurai'),('hido','hido'),('botanhime','botan')])}</div>{t('spirit_note','p','spirit-note')}</div></div></section>'''
release = f'''<section id="release" class="release wrap"><img class="app-icon" src="/assets/icon.webp" width="512" height="512" loading="lazy" alt="金継 KINTSUGI"><p class="eyebrow">{t('release_label')}</p>{t('release_title','h2')}{t('release_body','p','release-body')}<p class="release-status"><i aria-hidden="true"></i>{t('status')}</p><a class="text-link" href="https://sunimori.com/" target="_blank" rel="noopener noreferrer">{t('studio')} {arrow}</a></section>'''
page('/', hero+intro+play+world+release, home=True)
back = f'<a class="back" href="/">← {t("back")}</a>'
support = f'''<section class="legal wrap">{back}<p class="eyebrow">KINTSUGI / SUPPORT</p>{t('support_title','h1')}{t('support_intro','p','lead')}<div class="faq">{''.join(f'<details><summary>{t(key)}</summary>{t(body,"p")}</details>' for key,body in [('faq_release','release_body'),('faq_device','faq_device_body'),('faq_lang','faq_lang_body')])}</div>{t('contact_title','h2')}{t('contact_body','p')}<a class="contact-email" href="mailto:support@sunimori.com?subject=Kintsugi%20Support">support@sunimori.com {arrow}</a></section>'''
page('/support/', support, 'support')
privacy = f'''<section class="legal wrap">{back}<p class="eyebrow">KINTSUGI / PRIVACY</p>{t('privacy_title','h1')}{t('updated','p','updated')}{t('privacy_intro','p','lead')}{''.join(t(k,'h2')+t(k+'_body','p') for k in ['p_site','p_game','p_email'])}<p><a class="text-link" href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">{t('github_privacy')} {arrow}</a></p><a class="contact-email" href="mailto:support@sunimori.com?subject=Kintsugi%20Privacy">support@sunimori.com {arrow}</a></section>'''
page('/privacy/', privacy, 'privacy')
page('/404.html', f'<section class="legal wrap"><p class="eyebrow">404</p>{t("not_found","h1")}{back}</section>')
(DIST/'locales.js').write_text('window.KINTSUGI_COPY='+json.dumps({c:{k:v[i] for k,v in COPY.items()} for i,(c,_) in enumerate(LANGUAGES)},ensure_ascii=False,separators=(',',':'))+';\n')
(DIST/'CNAME').write_text('playkintsugi.com\n')
(DIST/'.nojekyll').touch()
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://playkintsugi.com/sitemap.xml\n')
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://playkintsugi.com{p}</loc></url>' for p in ['/','/support/','/privacy/'])+'</urlset>\n')
print(f'Built 4 pages and {len(LANGUAGES)} languages.')

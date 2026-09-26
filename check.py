"""Validate the public artifact and source before every Pages deployment."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
from content import COPY, LANGUAGES, APP_ADS, STORE_URL

ROOT = Path(__file__).resolve().parent
DIST = ROOT/'dist'
ALLOWED = {'.html','.css','.js','.svg','.webp','.png','.ttf','.txt','.xml'}
issues = []
patterns = [r'-----BEGIN [A-Z ]*PRIVATE KEY-----', r'gh[pousr]_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{40,}', r'sk-[A-Za-z0-9_-]{30,}', r'AKIA[A-Z0-9]{16}', r'AIza[A-Za-z0-9_-]{30,}']
assert len(LANGUAGES) == 11
assert all(len(values)==11 and all(v.strip() for v in values) for values in COPY.values())

class Page(HTMLParser):
    def __init__(self,path):
        super().__init__(); self.path=path; self.refs=[]; self.ids=set(); self.langs=[]; self.h1=0; self.store=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='option': self.langs.append(a.get('value'))
        if a.get('data-t') and a['data-t'] not in COPY: issues.append(f'{self.path}: missing translation')
        if tag=='img' and ('alt' not in a or not a.get('width') or not a.get('height')): issues.append(f'{self.path}: image needs alt/dimensions')
        if tag=='a' and a.get('target')=='_blank' and 'noopener' not in a.get('rel',''): issues.append(f'{self.path}: unsafe external link')
        for attr in ['href','src']:
            if a.get(attr): self.refs.append((tag,a[attr]))
        if tag=='script' and not a.get('src'): issues.append(f'{self.path}: inline script')
        if tag=='a' and 'apps.apple.com' in a.get('href',''):
            self.store+=1
            if a['href']!=STORE_URL: issues.append(f'{self.path}: store link is not the App Store page')

pages={}
for file in DIST.rglob('*'):
    if not file.is_file(): continue
    if file.name not in ['CNAME','.nojekyll'] and file.suffix not in ALLOWED: issues.append(f'Unexpected public file: {file}')
    if file.is_symlink(): issues.append(f'Symlink in public artifact: {file}')
    if file.suffix=='.html':
        p=Page(file);p.feed(file.read_text());pages[file]=p
        if p.h1!=1: issues.append(f'{file}: expected one h1')
        if p.langs!=[c for c,_ in LANGUAGES]: issues.append(f'{file}: incomplete locale picker')
for file,p in pages.items():
    for tag,ref in p.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc: continue
        target=DIST/unquote(url.path.lstrip('/')) if url.path.startswith('/') else file.parent/unquote(url.path)
        if not url.path: target=file
        if target.is_dir(): target=target/'index.html'
        if not target.exists(): issues.append(f'{file}: missing {ref}')
        if url.fragment and target in pages and url.fragment not in pages[target].ids: issues.append(f'{file}: missing anchor {ref}')
for file in ROOT.rglob('*'):
    if not file.is_file() or '.git' in file.parts or '__pycache__' in file.parts or 'qa' in file.parts: continue
    if file.suffix not in ['.py','.md','.yml','.js','.css','.html','.json','.txt','.svg','.xml']: continue
    text=file.read_text()
    if any(re.search(p,text) for p in patterns): issues.append(f'Credential pattern found: {file}')
# Released 2026-09-26: the home page (hero and release section) and the support FAQ link the store.
for route, count in [('index.html', 2), ('support/index.html', 1)]:
    if pages[DIST/route].store!=count: issues.append(f'{route}: expected {count} App Store link(s)')
assert (DIST/'CNAME').read_text().strip()=='playkintsugi.com'
assert (DIST/'app-ads.txt').read_text()==APP_ADS, 'app-ads.txt must match the AdMob publisher line'
assert not issues, '\n'.join(issues)
print(f'Passed: {len(pages)} pages, 11 complete languages, local links, assets, App Store links and public-file scan.')

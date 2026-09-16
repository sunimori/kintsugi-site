# 金継 KINTSUGI — official website

The independent, public marketing website for Sunimori's Kintsugi game. Production domain: https://playkintsugi.com/. The game is in development; no release date or App Store download link is claimed.

## Website languages

Japanese, English, Korean, Simplified Chinese, Traditional Chinese, Spanish, French, German, Italian, Brazilian Portuguese and Russian — the same 11-language set as Countdrop's app resources. The website language list does not imply that all these languages are supported in the game. The support page separately describes the current five-language game build.

## Edit and preview

Python 3.9+; no packages, framework, build-time credentials or runtime services needed.

```sh
python3 build.py
python3 check.py
python3 -m http.server 18797 --bind 127.0.0.1 --directory dist
```

- `build.py`: shared HTML layout and pages.
- `content.py`, `extra_locales.py`: complete website copy.
- `dist/style.css`, `dist/app.js`: responsive styling and interactions.
- `dist/assets/`: selected public artwork, development screenshots and local fonts.
- `check.py`: artifact boundaries, translated keys, internal routes and asset validation.

`dist/` is both the tracked static asset source and generated page output. Do not delete it as a disposable build directory. Never copy the iOS project, private documentation, development configuration, simulator saves or raw diagnostic files into this repository.

## Independent deployment

Only `main` in **sunimori/kintsugi-site** publishes this website. GitHub Actions rebuilds and validates the pages, then uploads only `dist/` to GitHub Pages. Authentication is provided by GitHub's short-lived job identity; no stored deploy credential is needed.

The private **sunimori/kintsugi** game repository is separate. Merging its work branch into its `main` cannot overwrite, rebuild or deploy this site. Website updates and fresh screenshots are reviewed and copied explicitly. Do not connect website publishing to the game's branch names.

GitHub Pages custom domain: `playkintsugi.com`. DNS stays at Squarespace: apex A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` CNAME `sunimori.github.io`. Preserve email, verification and domain-connect records. Domain binding and HTTPS enforcement live in the repository Pages settings; an Actions deployment does not configure them through the `CNAME` file alone.

## Release checklist

When the app is actually available, verify its public App Store URL, update the release wording in all 11 languages, then add the download link. Update the support information and released-app privacy policy to match the production build, including any enabled rewarded advertising. Update the Kintsugi card in `sunimori/sunimori-site` at the same time. No download button should be added for an unlisted app.

## Assets and rights

App icon, Tsugi and spirit illustrations are Sunimori product assets. The three phone screenshots were captured from the development app on 2026-09-16; the website labels them as development screens. The bowl hero is original AI-generated marketing art, not a game screenshot. Instrument Serif is distributed under the included SIL Open Font License (`dist/assets/fonts/OFL.txt`).

Copyright © 2026 Sunimori. All rights reserved to the brand, game art and website content except separately licensed fonts. Public source visibility does not grant permission to reuse product assets.

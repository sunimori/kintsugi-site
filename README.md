# 金継 KINTSUGI — official website

The independent, public marketing website for Sunimori's Kintsugi game. Production domain: https://playkintsugi.com/. The game is on the App Store since 2026-09-26: https://apps.apple.com/app/id6811162450 (`STORE_URL` in `content.py`).

## Website languages

Japanese, English, Korean, Simplified Chinese, Traditional Chinese, Spanish, French, German, Italian, Brazilian Portuguese and Russian — the same 11-language set as Countdrop's app resources. The game ships in the same 11 languages, and the support page lists them.

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

## Release (2026-09-26)

Done when the app went live: release wording in all 11 languages (description, navigation, hero note, release section, screenshot note, support FAQ); App Store links in the hero note, the release button and the download FAQ, all to `STORE_URL`, which opens each visitor's own storefront; the devices FAQ says iPhone with iOS 17 or later. `check.py` requires those three links and refuses any other App Store URL. The Kintsugi card in `sunimori/sunimori-site` switched to available now the same day.

The privacy policy describes the released game (updated 2026-09-26): local-only game data, with no play logs or diagnostics in release builds; Game Center scores and rank achievements (on by default, can be turned off in Settings); and player-initiated rewarded ads from Google AdMob with Google's consent message where required, the US-states opt-out in the same Settings entry, all-ages ad content and in-app ad reporting. Revise it in all 11 languages whenever the app's data practices change.

`dist/app-ads.txt` authorises Google AdMob to sell the app's ad space. AdMob reads it from the domain in the App Store Marketing URL, so that URL must stay `https://playkintsugi.com/`. The publisher line lives in `content.py` (`APP_ADS`) and `check.py` verifies the built file.

## Assets and rights

App icon, Tsugi and spirit illustrations are Sunimori product assets. The three phone screenshots were captured from the development app on 2026-09-16; the website labels them as development screens. The bowl hero is original AI-generated marketing art, not a game screenshot. Instrument Serif is distributed under the included SIL Open Font License (`dist/assets/fonts/OFL.txt`).

Copyright © 2026 Sunimori. All rights reserved to the brand, game art and website content except separately licensed fonts. Public source visibility does not grant permission to reuse product assets.

# מהירות האור שליחויות — notes

Zap customer 80240748 (from the brief title; not confirmed as the Dapei Zahav customer-id).

## Facts (locked; each with its source)
| field | value | source |
|---|---|---|
| name | מהירות האור שליחויות | brief |
| display phone | 072-2599648 (Zap tracking number) | brief + user confirmed 2026-10-07 |
| WhatsApp | 055-9686670 | Dapei Zahav listing https://www.d.co.il/80240748/49050/ (WhatsApp button). Brief's 050-6785822 is the contact person's mobile, not on the listing |
| lead email | shirana221@gmail.com | brief |
| public email | shirana221@gmail.com | brief |
| address | בר אילן 23, חיפה | brief; d.co.il shows "בר אילן 23, קריית חיים חיפה" |
| Dapei Zahav id | 80240748 | d.co.il listing matches name + address + phone 072-2599648 (researched 2026-10-07) |
| Google Maps | https://maps.google.com/?cid=16400963226497574796 · geo 32.833149,35.069494 | linked from the d.co.il listing |
| hours | א׳–ה׳ 08:00–18:00, ו׳ 08:00–13:00 | brief |
| years | למעלה מ-30 שנה (no founding year) | brief |
| couriers / fleet | עשרות שליחים, עשרות רכבים (קטנועים ורכבים מסחריים) | brief; "עשרות" confirmed by user |
| areas | חיפה, הקריות, הצפון, כל הארץ | brief |
| tracking link | http://37.46.35.200/Baldar/Login.aspx?ReturnUrl=%2fbaldar (returns 200, plain http) | brief |
| facebook | https://www.facebook.com/מהירות-האור-1482628425325474 | brief |

## Decisions (user, 2026-10-07)
- design.motion = lively (brief: "אתר חדשני עם אנימציות של רכבים/אופנועים זזים") + `road` section on home.
- "החברה המובילה בצפון" removed → "חברת שליחויות ותיקה בצפון הארץ".
- "טכנולוגיית WAP" → "מערכת מעקב אונליין".
- No food deliveries anywhere on the site (brief).
- No blog (brief has no SEO and no blog).

## Audience
Businesses and institutions in Haifa and the north: law and accounting offices, banks, insurance companies,
hi-tech. Fear: a document/cheque that does not arrive on time, or a courier who represents them badly.

## Assets
| file | shows | use |
|---|---|---|
| logo-original.jpg | brief logo: red wordmark on yellow, envelope + scooter, black tagline band | source |
| logo.png | top part of the logo, yellow keyed out, 2× upscaled | header |
| hero/van/checks/sameday/parcels/legal/fleet.webp | Weave Nano Banana 1K, AI, no people/text (24.5 credits approved) | hero, cards, splits |

## Gaps
- Zap privacy PDF: Zap's own is https://img.zapgroup.co.il/PrivacyPolicy.pdf; the per-client pattern could not be verified from the sandbox (zap.dbusiness.co blocks bots) → placeholder page stays
- Final domain: assumed mehiruthaor.co.il (old site 403; Wayback snapshot 2022-12-14 exists but archive.org is blocked from the sandbox)
- No registered company (בע"מ / ח.פ.) found → none shown
- Higher-res / vector logo · real photos of fleet and team
- Tracking system is plain http on a bare IP (browser "not secure"); opens in a new tab

## Research log (2026-10-07)
- Old site (via the other session's `zs grab`, Wayback): 2nd phone 04-8040404 — NOT used (brief gives 072-2599648 as display, and it is not on d.co.il); business YouTube video QhidydOUNoM ("מהירות האור שליחויות בכל הארץ", the company's own channel, verified by oEmbed) → about page.
- From this session's sandbox archive.org is blocked, so `zs grab` returns nothing here.
- Reviews: widget loads, Zap reviews API answers 500 for staging hosts → section stays hidden until the widget shows real reviews (live domain).
- d.co.il: id 80240748 confirmed, hours match the brief, services list matches; reviews come from the official Zap widget (no rating text on the site itself).
- Google Maps CID + geo from the d.co.il page. Facebook link matches the brief.

## Keyword map (no Ahrefs; volume unknown)
| page | keyword | H1 |
|---|---|---|
| home | חברת שליחויות בחיפה | חברת שליחויות בחיפה והצפון — מהירות האור שליחויות |
| /שירותי-שליחויות/ | שירותי שליחויות | שירותי שליחויות והפצה |
| …/שליחויות-לכל-הארץ/ | שליחויות לכל הארץ | שליחויות לכל הארץ |
| …/איסוף-והפקדת-צקים/ | איסוף והפקדת צ׳קים | איסוף, פיזור והפקדת צ׳קים |
| …/משלוחים-מהיום-להיום/ | משלוחים מהיום להיום | משלוחים מהיום להיום בצפון |
| …/הובלת-חבילות-ומשאות-קלים/ | הובלת חבילות ומשאות קלים | הובלת חבילות ומשאות קלים |
| …/שליחויות-משפטיות/ | שליחויות משפטיות | שליחויות משפטיות ברחבי הארץ |
| /אודות/ | חברת שליחויות בצפון | אודות מהירות האור שליחויות — חברת שליחויות בצפון |
| /צור-קשר/ | צור קשר מהירות האור שליחויות | צור קשר — מהירות האור שליחויות |

## Design decisions (benchmark pass)
- Direction A (signature, full-bleed night hero + Veo loop). Shape language: sharp (radius 2), hairlines, ↖ arrows.
- Rhythm: dark hero+stats+marquee → light split → bento → light road+features → FAQ → red CTA → light lead band → dark footer.

## Engine changes made in this session (generic)
- New section `road` (animated vehicles lane, CSS only, static under reduced motion) + icons `scooter`, `van`.
- Screenshots: tall viewport instead of full_page (Chromium dropped off-screen images in previews).
- Motion layer fix: `lively` hero photo is clipped to its frame (it overlapped the text on mobile split/centered heroes).

## Delivery (2026-10-09)
- `zs package mehirut-haor --domain https://mehiruthaor.co.il` → dist/mehirut-haor-20261009.zip (63.6 MB). Domain assumed = old site's; `deploy.sh --url` moves it.
- Install test: unzip + deploy.sh as a site user (`--owner`) into an empty docroot + empty DB, with `--url` to a test host:
  17 internal pages 200 with one H1, no leftover URLs, robots.txt + sitemap 200, admin login page, form → lead saved
  (test copy forced to staging so no client mail; test lead deleted).
- Found and fixed: deploy.sh run as root without --owner failed halfway (wp-cli refuses root) → now refuses before copying.

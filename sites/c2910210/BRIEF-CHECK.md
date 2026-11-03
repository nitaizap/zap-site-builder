# BRIEF-CHECK — מוניות כפר סבא בע״מ (2910210)

Every line of the spec sheet against the built site. ✅ = seen on the rendered page (screenshot or page
HTML), not "it is in site.json". ➖ = deliberately not built, with the reason. ⏳ = open.

## סוג הפרויקט

| line in the brief | state | where |
|---|---|---|
| אתר מלא | ✅ | 13 pages + privacy + accessibility + blog archive and 3 posts |
| אתר SEO (בלוג) — blank | ✅ added anyway | `/בלוג/`, one category, three posts. OPEN-ITEMS 6 |

## פרטי לקוח

| line | state | where |
|---|---|---|
| שם הלקוח / שם העסק: מוניות כפר סבא בע״מ | ✅ | home H1, every `<title>`, footer, schema |
| מספר לקוח 2910210 | ✅ | used as the Dapei Zahav customer id for the reviews block |
| שנות פעילות — blank | ✅ filled from the client's own sign | "פועלים משנת 1955" in the hero points, the facts card and the about page. OPEN-ITEMS 3 |
| אתר קיים www.taxi-ks.co.il | ➖ | the site would not load (connection refused) and the Wayback copy was unreachable from this session. Nothing was taken from it. NOTES.md |

## פרטי קשר

| line | state | where |
|---|---|---|
| איש קשר 052-3410799 | ➖ | a private mobile, not published on the site |
| כתובת העסק: רוטשילד 50, כפר סבא | ✅ | header area, contact page, footer (Waze link), schema |
| אזורי שירות (10 יישובים) | ✅ | the facts card on the home page, the FAQ, the service pages, schema `areaServed` |
| שעות פעילות 24/7 כולל שישי, שבת ומוצאי שבת | ✅ | hero lead, "למה נוסעים איתנו", facts card, FAQ, footer, schema |
| אימייל לאתר / מייל לטופס לידים: taxikfarsaba@bezeqint.net | ✅ | contact page and the lead-form recipient |
| טלפון לאתר 09-7661111 | ⏳ | set as `phone_regular`, shown through the "מספר מקשר" popup. The displayed number is the Zap one. OPEN-ITEMS 4 |
| מספר מקשר זאפ 072-3257979 | ✅ | the displayed phone everywhere, with `phone_is_virtual` on |

## נוכחות דיגיטלית

| line | state | where |
|---|---|---|
| וואטסאפ / פייסבוק / אינסטגרם / לינקדין — all blank | ➖ | no WhatsApp button and no social bar. Nothing invented |
| Google My Business: כן + link | ✅ | schema `sameAs` / `hasMap` |

## תוכן האתר

| line | state | where |
|---|---|---|
| תחומי עיסוק (the full paragraph) | ✅ | reproduced almost verbatim as the second paragraph of the about page; its elements drive the nine service cards |
| דף בית | ✅ | `/` |
| אודות | ✅ | `/אודות/` |
| מוניות ספיישל | ✅ | `/מוניות-ספיישל/` |
| מוניות לנתב״ג וקבלת אורחים משדה התעופה | ✅ | `/מוניות-לנתב״ג-וקבלת-אורחים/` (name shortened for the H1 and URL, OPEN-ITEMS 7) |
| הסעות עובדים והסדרי נסיעות קבועים לחברות ומוסדות | ✅ | `/הסעות-עובדים-לחברות-ומוסדות/` (shortened, OPEN-ITEMS 7) |
| הסעות תלמידים וילדים | ✅ | `/הסעות-תלמידים-וילדים/` |
| הסעות VIP והסעות אמנים | ✅ renamed | `/הסעות-יוקרה-והסעות-אמנים/`. A URL may not mix Hebrew and Latin; "VIP" stays in the page text. OPEN-ITEMS 5 |
| מוניות 6 מקומות ומעלה | ✅ | `/מוניות-6-מקומות-ומעלה/` |
| הסעות לנכים | ✅ | `/הסעות-לנכים/` |
| שירותי נהג צמוד | ✅ | `/שירותי-נהג-צמוד/` |
| שליחויות אקספרס | ✅ | `/שליחויות-אקספרס/` |
| צור קשר | ✅ | `/צור-קשר/` |
| סלוגן: אל היעד הבא עם מוניות כפר סבא! | ✅ | the site tagline; not placed in an H1 (Zap QA) |
| **כפתור חיוג בולט בכל עמוד** | ✅ | the phone button sits in the header on every page, desktop and phone, and the two hero buttons on the home page are "חייגו עכשיו" and "הזמנת מונית" |
| **הזמנת מונית בכל עמוד** | ✅ | the lead form band sits above the footer on every page except the contact page, which carries the full contact form; the home hero also has its own one-row form card |
| מאמרים — blank | ✅ three written | from the spec and the company's own Dapei Zahav text only. OPEN-ITEMS 6 |

### למה אנחנו (every line)

| line | state | where |
|---|---|---|
| שירות 24 שעות, 7 ימים בשבוע, כולל שישי, שבת ומוצאי שבת | ✅ | "מוקד 24 שעות" tile, hero lead, facts card, FAQ |
| כלי רכב חדישים ומפוארים, גדולים ומרווחים, עם מערכות GPS | ✅ | "רכבים חדישים ומרווחים" tile and the service pages |
| נהגים ללא הרשעות קודמות | ✅ | its own tile, and repeated on the תלמידים, יוקרה and נכים pages |
| הסדרי אשראי לחברות והסדרים עם ועדי עובדים | ✅ | "הסדרים לחברות ולוועדים" tile and the הסעות עובדים page |
| הזמנה דרך האתר ובאמצעות אפליקציה | ✅ | "הזמנה באתר ובאפליקציה" tile, the steps section, the about page |
| שירות גם באנגלית וברוסית | ✅ | its own tile, the facts card, the FAQ, the about page |

## עיצוב ומותג

| line | state | where |
|---|---|---|
| לוגו — blank | ✅ | taken from the client's own business card photo, IMAGE-SOURCES.md |
| צבעי מותג — blank | ✅ | sampled from that card and the station sign: deep green + taxi yellow |
| יד חופשית למעצב — blank | ✅ | read as a free hand; the direction was chosen here and recorded in NOTES.md |
| אתרים שאהבתם: nitzav-taxi.co.il, moniot.info | ✅ noted | used as a signal of taste (a direct, phone-first taxi site), not copied |

## תמונות

| line | state | where |
|---|---|---|
| תמונת בעלים — blank | ➖ | none exists in the material; no AI portrait was made |
| גלריה — blank | ✅ | ten of the client's own photographs were prepared, nine are placed. IMAGE-SOURCES.md |
| email body: "יש לייצר תמונות/לקחת ממאגר" | ✅ not needed | the client's own folder `F:\SiteContent\02910210` turned out to hold 227 files including real photographs of their taxis, station and dispatch room. 0 AI images, 0 Weave credits |

## כתבת תדמית

| line | state | where |
|---|---|---|
| כתבת תדמית — blank | ➖ | not built |

## Prohibitions and invented facts

The spec names no prohibited topic. Checked across `site.json`: no price, no rating, no review count, no
award, no "הטוב ביותר"/"מספר 1"/"המוביל", no em dash or en dash (the validator stops the build on either),
no "תמונה להמחשה", no invented staff, fleet size or case numbers. Every number that appears (1955, 24, 7,
6, the ten towns, the phone) traces to a row in NOTES.md.

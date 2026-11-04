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
| **כפתור חיוג בולט בכל עמוד** | ✅ | **Re-verified mechanically 2026-11-04** by loading all 13 pages at 1440 and at 390 and querying the DOM: a visible header call control on every page, and 3 to 6 visible `tel:` links on each. It is now genuinely בולט: a filled taxi-yellow pill with the number in it on desktop and tablet, the standard plain phone icon on phones (qa-rules). The home hero keeps "חייגו עכשיו" and "הזמנת מונית", and a yellow call band with the number inside the button sits after the service cards |
| **הזמנת מונית בכל עמוד** | ✅ | **Re-verified mechanically 2026-11-04**, same run: a taxi-ordering form present on all 13 pages at both widths. The lead form band sits above the footer on every page except the contact page, which carries the full contact form; the home hero also has its own one-row form card |
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
| לוגו — **not blank** | ✅ **corrected 2026-11-04** | the `לוגו` cell is empty in `brief.md`, but that file is a text export and drops embedded images. The `.docx` opened as a zip holds the real logo at `word/media/image1.png` (200x200), referenced from the `לוגו` cell. The site now uses it, cropped above its slogan strip per qa-rules. Decision and side-by-side: IMAGE-SOURCES.md |
| צבעי מותג — blank | ✅ | sampled from the client's own card and station sign: deep green + taxi yellow. The brief's logo is the same green and yellow, which confirms the sampling. Since 2026-11-04 the yellow does real work rather than trim: the header call button and a full-width call band |
| יד חופשית למעצב — blank | ✅ | read as a free hand; the direction was chosen here and recorded in NOTES.md |
| אתרים שאהבתם: nitzav-taxi.co.il, moniot.info | ✅ | **Both opened and studied 2026-11-04**, desktop and scrolled. Four shared signals were taken, none of their layout: the phone number written out inside a loud button; one strong accent used as a large flat fill; an ordering action high on the page and repeated; flat and direct, no ornament. What was not taken: moniot's keyword-stuffed title and footer link farm, nitzav's WhatsApp bubble (the brief leaves וואטסאפ blank). `zs pool` unchanged at 35%. NOTES.md carries the detail |

## תמונות

| line | state | where |
|---|---|---|
| תמונת בעלים — blank | ➖ | none exists in the material; no AI portrait was made |
| גלריה — blank | ✅ | ten of the client's own photographs were prepared, seven are placed (2026-11-04: the home collage band and its two weakest photos came out). IMAGE-SOURCES.md |
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


## Polish pass, 2026-11-04

Re-read against the brief after the first pass was judged to have drifted. Three brief lines moved from
"built" to "built and shown to be true":

| brief line | what changed |
|---|---|
| לוגו | the brief was not blank after all. Its `.docx` hides a 200x200 logo that the text export drops. The site now carries that artwork, cropped above its slogan strip |
| כפתור חיוג בולט בכל עמוד | "בולט" was taken seriously: the header call control is a filled taxi-yellow pill with the number in it, and a yellow call band repeats the number mid-page. Presence on all 13 pages re-verified by querying the DOM, not by reading site.json |
| אתרים שאהבתם | both sites were actually opened and what they share was written down and answered, instead of being noted and left |

Nothing on the site states a fact that is not in NOTES.md. The new call band's copy
("המוקד עונה בכל שעה, גם בשישי, בשבת ובמוצאי שבת") and the added facts paragraph are the brief's own
שעות פעילות and למה אנחנו lines reworded. No price, rating, review count, award, superlative, em dash or
en dash was introduced; `zs build`'s validator and `zs qa` both pass at 0.


## Round 2, 2026-11-04: the first screen

The user compared the site against the two named reference sites and said it looked nothing like them. The
traits were right, the placement was not. Three brief lines were re-answered where they are actually seen:

| brief line | before | after |
|---|---|---|
| אתרים שאהבתם (both lead with a saturated colour field) | first non-white element at y=1364, against a 900px fold | the hero itself is a taxi-yellow field from y=149, 801px tall |
| כפתור חיוג בולט | 16-17px in the first screen | the number is the hero's primary button at 25.6px desktop, 18px phones, and still a filled yellow pill in the header on every page |
| הזמנת מונית בכל עמוד | booking form began at y=947, below the fold | form card at y=643 at 1440x900 and y=626 at 1280x800, inside the fold; on phones the hero's "הזמנת מונית" button jumps to it |

The displayed number is **072-3257979**, the Zap tracking number the site already treats as primary.
**OPEN-ITEMS 4 is still unresolved** (the spec also gives 09-7661111 as "טלפון לאתר"); the real number
stays behind the standard "מספר מקשר" popup. Changing which one is displayed is one line in site.json,
and it now appears at display size in the hero, so the decision matters more than it did.

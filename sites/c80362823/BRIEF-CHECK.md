# BRIEF-CHECK — car service (80362823)

The spec sheet (`brief/איפיון אתר - car service - 80362823_1.docx`) line by line.
✅ = seen on the rendered page (screenshot or page HTML), not "it is in site.json". ➖ = deliberately not
built, with the reason. ⏳ = open, see OPEN-ITEMS.md.

## 1. סוג הפרויקט

| line | state | where |
|---|---|---|
| אתר מלא | ✅ | `tier: standard`: home, hub, 8 service pages, about, contact, blog, privacy, accessibility |
| אתר SEO (בלוג) | ✅ | `/בלוג/` with the category מדריכי הסעות and 3 posts |

## 2. פרטי לקוח

| line | state | where |
|---|---|---|
| שם הלקוח: רוברט מסחייב | ✅ | `author_name`, post byline, about page |
| שם העסק: car service | ✅ | H1 on the home page (the name only, per Zap QA), header, footer wordmark, every `<title>` |
| מספר לקוח 80362823 | ✅ | `dpz_customer_id` |
| שנות פעילות: קרוב לשני עשורים | ✅ | hero lead, about page, footer; never converted into a year |
| אתר קיים: (empty) | ➖ | none to migrate or keep ranking |

## 3. פרטי קשר

| line | state | where |
|---|---|---|
| רוברט מסחייב 052-8332274 | ➖ | the brief lists this as the contact person's own line; the spec's "טלפון לאתר" is 052-7980029, and that is the only number on the site |
| כתובת העסק: תל אביב | ✅ | contact page, footer, LocalBusiness schema (city only, no street in the brief) |
| אזורי שירות (long list) | ✅ | `area_served` in schema, listed in the home `prose` and on the hub |
| שעות פעילות | ✅ | contact page, footer, `opening_hours` schema |
| אימייל לאתר / מייל לטופס לידים | ✅ | `ruben.misihaev@gmail.com`, both public and leads |
| טלפון לאתר: 052-7980029 | ✅ | header button, every `tel:` link, contact page, footer |
| מספר מקשר זאפ: (empty) | ➖ | `phone_is_virtual` false; see OPEN-ITEMS #10 |

## 4. נוכחות דיגיטלית

| line | state | where |
|---|---|---|
| וואטסאפ, פייסבוק, אינסטגרם, לינקדין, GMB | ➖ | all empty in the brief and absent from the Dapei Zahav listing: no social bar, no WhatsApp button. Never invented |

## 5. תוכן האתר

| line | state | where |
|---|---|---|
| תחומי עיסוק (the long paragraph) | ✅ | rewritten as the hero lead, the home `prose` and the about page; every claim in it kept (צי רחב, מיניבוסים מפוארים וממוזגים, קצין בטיחות מורשה, לקוחות פרטיים/מוסדות/מפעלים, כל חלקי הארץ) |
| עמוד: דף בית | ✅ | `/` |
| עמוד: אודות | ✅ | `/אודות/` |
| עמוד: הסעות עובדים | ✅ | `/שירותי-הסעות/הסעות-עובדים/` |
| עמוד: הסעות תיירים | ✅ | `/שירותי-הסעות/הסעות-תיירים/` |
| עמוד: הסעות לאירועים | ✅ | `/שירותי-הסעות/הסעות-לאירועים/` |
| עמוד: הסעות לנתב״ג | ✅ | `/שירותי-הסעות/הסעות-לנמל-התעופה/` (name changed for the URL rule, keyword kept; OPEN-ITEMS #5) |
| עמוד: טיולים מאורגנים וטיולים לקברי צדיקים | ✅ | `/שירותי-הסעות/טיולים-מאורגנים/`, with קברי צדיקים as its own H2 and FAQ |
| עמוד: הסעות VIP | ✅ | `/שירותי-הסעות/הסעות-יוקרה/` (OPEN-ITEMS #4) |
| עמוד: הסעות לגיל הזהב | ✅ | `/שירותי-הסעות/הסעות-לגיל-הזהב/` |
| עמוד: הסעות ילדים ותלמידים (גנים, קייטנות, ילדים עם מוגבלויות) | ✅ | `/שירותי-הסעות/הסעות-ילדים-ותלמידים/`, all three named in the body and the FAQ |
| עמוד: צור קשר | ✅ | `/צור-קשר/` |
| נוסף: הסעות לציבור הדתי | ✅ | H2 on the הסעות לאירועים page + its FAQ |
| נוסף: הסעות לטיולים, ימי כיף | ✅ | H2 "ימי כיף וגיבוש" on טיולים מאורגנים |
| נוסף: הסעת קבוצות ספורט | ✅ | H2 "קבוצות ספורט, אמנים ולהקות" on טיולים מאורגנים |
| נוסף: הסעת אמנים ולהקות | ✅ | same H2, plus a card and FAQ on הסעות יוקרה |
| נוסף: הסעות קבועות | ✅ | הסעות עובדים (קווים קבועים, הסדרים) and הסעות לגיל הזהב (פעילות קבועה) |
| נוסף: מוניות לנתב״ג | ✅ | H2 "מוניות לנתב״ג" and a feature tile on הסעות לנמל התעופה |
| צי הרכב: אוטובוס, מיניבוס, מידיבוס | ✅ | the fleet table in the home `prose`, the gallery section intro, the about page |
| למה אנחנו: כלי רכב חדישים מפוארים וממוזגים | ✅ | `features:aside` on the home, about page |
| למה אנחנו: כלי רכב עם מערכות GPS | ✅ | `features:aside`, service pages, blog post on safety |
| למה אנחנו: פיקוח קצין בטיחות מורשה | ✅ | `features:aside`, every service page, FAQ, blog post |
| למה אנחנו: נהגים ללא הרשעות קודמות | ✅ | `features:aside`, הסעות ילדים, blog post |
| למה אנחנו: נסיעות לכל הארץ | ✅ | hero lead, `features:aside`, home `prose`, FAQ |
| למה אנחנו: הסדרים עם ועדי עובדים | ✅ | home cards, הסעות עובדים (own H2 + FAQ) |
| למה אנחנו: שירות ללקוחות פרטיים, מוסדות ומפעלים | ✅ | home `prose` ("מי נוסע אתנו"), about page |
| מאמרים: (empty) | ✅ | 3 posts written from the brief only, no invented facts (OPEN-ITEMS #15) |

## 6. עיצוב ומותג

| line | state | where |
|---|---|---|
| לוגו | ➖ | the cell holds one embedded image and nothing else was lost in the text export (the .docx was opened as a zip on 04/11/2026: one file in `word/media/`, one drawing in `document.xml`). It is the business name typed in a generic condensed italic, 97×28 px of ink, not a mark. Not used. The header and footer carry the name set in the site's own heading face; favicon is a letterform mark in the palette primary (OPEN-ITEMS #11, #18, #19) |
| צבעי מותג | ⏳ | none given; aubergine + burnt orange chosen (OPEN-ITEMS #2) |
| יד חופשית למעצב | ✅ | taken: direction chosen in automatic mode (OPEN-ITEMS #1) |
| אתרים שאהבתם | ➖ | none given |

## 7. תמונות

| line | state | where |
|---|---|---|
| תמונת בעלים | ➖ | none supplied. No AI portrait was generated: a generated "owner" would misrepresent a real person |
| גלריה | ⏳ | the client supplied no photographs at all. `F:\SiteContent\80362823` holds 11 files, every one of them a Zap internal campaign or intake template document, no image among them. 6 AI atmosphere images were generated instead, all recorded in IMAGE-SOURCES.md and marked `ai: true`, and none is presented as this client's own vehicles or premises |

## 8. כתבת תדמית

| line | state | where |
|---|---|---|
| כתבת תדמית: (empty) | ➖ | not requested |

## Prohibitions

The brief names none. Grepped `site.json` for the services it does **not** offer (food delivery, car repair,
vehicle rental/לרכב להשכרה, ride-hailing): no hits. "car service" is a passenger-transport company, and
nothing on the site suggests vehicle servicing or repair.

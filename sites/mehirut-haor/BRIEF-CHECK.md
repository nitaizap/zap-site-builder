# Brief check — מהירות האור שליחויות (customer 80240748)

Every line of the טופס איפיון against the built site. ✅ done · ➖ intentionally different (reason) · ⏳ open.

## 6. עיצוב ומיתוג

| brief | on the site |
|---|---|
| סגנון: "אתר חדשני עם אנימציות של רכבים/אופנועים זזים" | ✅ **Home hero**: night-street video loop (desktop); on phones an illustrated scooter drives along the hero's bottom edge. ✅ **Road scene** (home): scooters, a van and a truck in two lanes drive across, wheels spin, bodies bob, speed lines, moving lane marks, skyline drifting behind. ✅ **"איך זה עובד" route**: a scooter rides the route as you scroll and each stop lights up when it is reached. ✅ **Scroll progress**: a brand-colour bar at the top with a scooter riding its tip (desktop/tablet). ✅ Slogan marquee, H1 word-by-word entrance, image wipe-ins, counters, tilt + light sweep on the service tiles. Everything stops under "reduce motion" (accessibility). |
| צבעים: על בסיס הלוגו | ✅ Red #d7141c / yellow #ffe600 / black from the logo; Elementor Global Colors so one change restyles the site |
| לוגו | ✅ logo.png (keyed from the brief's logo); the original kept as logo-original.jpg |
| רכיבים: טופס יצירת קשר + מפה | ✅ Contact page: form + Google map; lead form in the footer band on every page (saved in WP; mail goes to shirana221@gmail.com only on production) |
| SEO: לא | ✅ No blog; basic Yoast titles/descriptions only (Zap standard) |

## 2. פרטי לקוח

| brief | on the site |
|---|---|
| שם העסק, כתובת בר אילן 23 חיפה | ✅ footer, contact page, schema |
| טלפון לאתר | ➖ 072-2599648 (Zap tracking number, confirmed by the user 2026-10-07) instead of 050-6785822 |
| מייל, שעות א׳–ה׳ 8–18, ו׳ 8–13 | ✅ footer + contact page + schema |
| פייסבוק | ✅ footer |
| וואטסאפ / אינסטגרם / לינקדאין / GMB | ➖ empty in the brief; WhatsApp +972559686670 and GMB found in research (NOTES.md); no Instagram/LinkedIn found |
| שנות פעילות: למעלה מ-30 | ✅ hero points, badge "30+", trust strip (no invented founding year) |

## 4. עמודי האתר ותוכן

| brief | on the site |
|---|---|
| עמוד הבית: כותרת, סלוגן, פתיח | ✅ H1 "חברת שליחויות בחיפה והצפון — מהירות האור שליחויות"; slogan in the marquee; intro text in the split section |
| 5 בלוקי שירות עם קישור | ✅ bento tiles → 5 service pages |
| "בכל זמן ובכל מקום" | ✅ features section (fleet, team, tracking) |
| כפתורים: מעקב משלוחים והזמנות · צרו קשר וקבלו הצעת מחיר | ✅ hero, features, CTA band; tracking link = the brief's Baldar URL |
| שירותי שליחויות (14-item list, technology, courtesy) | ✅ services page; "טכנולוגיית WAP" written as "מערכת מעקב אונליין" (WAP is obsolete wording) |
| אודותינו (+ client types) | ✅ about page + the company's own YouTube video |
| צרו קשר | ✅ |
| 5 עמודי שירות | ✅ one page each, with FAQ |
| אין להזכיר משלוחי אוכל | ✅ no mention anywhere (checked: 0 hits) |

## Delivery

| requirement | status |
|---|---|
| Built on WordPress + Elementor, editable in containers | ✅ every section is Elementor containers with native widgets; header/footer are Elementor Pro Theme Builder templates |
| Uploaded to the Zap staging clone through Novamira | ✅ https://mehiruthaor.ussl.co.il (staging lock: no client mail, noindex) |
| QA | ✅ `zs qa` 0 errors locally and on the live staging site |
| Launch blockers | ⏳ Zap privacy-policy URL (standards.privacy_url); client domain + `--live` push after approval |

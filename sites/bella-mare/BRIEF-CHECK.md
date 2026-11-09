# בלה מארה: brief check

Checked against the rendered pages (local build, page HTML + desktop/mobile shots), 28/10/2026.
✅ seen on the page · ➖ deliberately different (reason) · ⏳ open

## עץ אתר
| brief | status |
|---|---|
| עמוד הבית | ✅ / |
| אודות (כולל אירועים) | ✅ /אודות/ with the events section (#events) |
| תפריט ומשלוחים | ✅ /תפריט-ומשלוחים/ |
| גלריה | ✅ /גלריה/ |
| דברו איתנו (עוגן) | ✅ section on the home page, menu link /#contact |

## פרטי העסק
| brief | status |
|---|---|
| טלפון 04-8122220 | ➖ the site shows the Zap number 055-4309548 (user's decision: "use dapaz"); 04-8122220 appears in the "מספר מקשר" popup as the regular line |
| שעות: א׳–ה׳ 12:00–22:00, שישי סגור, מוצ״ש עד 24:00 | ✅ contact section, footer, FAQ |
| כתובת: השקד 47, נהריה | ✅ contact + footer, Waze link |
| כשר | ✅ (generic, no certifying body; user's decision) |
| משלוחים / טייק אווי, הזמנה אונליין | ✅ "להזמנת משלוח" → mishlohim.co.il/menu/14504 (found on rest.co.il) |
| הזמנת שולחן (טאביט) | ✅ "להזמנת שולחן" → tabitisrael.co.il/site/bellamare |
| אירועים עד 70 איש | ✅ home tiles, about #events, FAQ |
| אימייל (empty) | ➖ calls-only site: no form anywhere (user's decision); call buttons instead |
| וואטסאפ (empty) | ➖ none shown (no source) |
| פייסבוק / אינסטגרם (empty in brief) | ✅ shown: found on rest.co.il + given by the user |
| לוגו / תמונות | ✅ the client's logo (rest.co.il gallery) and the client's photos (brief's Drive folder) |

## עמוד הבית
| brief | status |
|---|---|
| SEO title "בלה מארה \| מסעדה איטלקית ופיצרייה כשרה בנהריה" | ✅ exact |
| SEO description | ✅ the brief's text, with a dash replaced by a comma (no dashes rule) + a short ending to reach 150–160 chars |
| H1 "בלה מארה – מטבח איטלקי כשר" | ➖ H1 = "בלה מארה" (Zap QA: home H1 = the client's name only, no dash); the rest is in the lead |
| פסקת פתיחה | ✅ hero lead |
| כפתור 1 להזמנת משלוח / כפתור 2 להזמנת שולחן | ✅ both, hero |
| "איטליה על השולחן, בכשרות מלאה" + פסקה | ✅ |
| "קצת עלינו" + פסקה + "לקריאה נוספת" → אודות | ✅ |
| גלריה (6 תמונות) | ✅ 8 photos (mosaic needs 4 or 8) + link to the gallery page |
| "למה בלה מארה?" + 4 יתרונות | ✅ all four, exact |
| דברו איתנו: טקסט, טלפון, כתובת, שעות | ✅ |
| טופס: שם, טלפון, הודעה | ➖ no form (no lead e-mail in the brief → calls only, user's decision) |

## אודות
| brief | status |
|---|---|
| SEO title / description | ✅ (title in Zap format "בלה מארה \| אודות ואירועים") |
| H1 "אודות בלה מארה" | ✅ |
| פסקה 1, פסקה 2 | ✅ |
| אירועים (תת-אזור) | ✅ "אירועים עד 70 איש" with the brief's text, call button |

## תפריט ומשלוחים
| brief | status |
|---|---|
| SEO title / description | ✅ (Zap title format) |
| H1 "התפריט שלנו" | ➖ "תפריט ומשלוחים" (Zap QA: inner H1 = the page name = the menu label) |
| טקסט | ✅ hero lead |
| קישור לתפריט / הזמנה | ✅ Mishlohim on every menu card + buttons |
| prices | ➖ not shown (not asked in the brief; user's decision) |

## גלריה
| brief | status |
|---|---|
| SEO title / description, H1 "גלריה" | ✅ |
| תמונות מהדרייב | ✅ 21 dish photos + an atmosphere carousel |

## Not in the brief, by rule
- Privacy policy + accessibility statement pages (Zap standard) ✅; privacy fields unconfirmed ⏳ (launch blocker)
- Blog: not in the brief's tree; added after Zap QA asked for it (01.11.2026): 3 posts, `zs seo` #5 passes
- Prohibited words: the brief has none.

## Re-check 09.11.2026 (after Zap QA 01.11 + engine updates), on the rendered pages, local and https://80392812.ussl.co.il
- Every text line of the brief found on its page (script check of the page HTML). Two deliberate differences: the
  brief's dashes are commas (no-dash rule), and the menu lead opens with the page keyword "משלוח פיצה בנהריה:" before
  the brief's sentence.
- Buttons "להזמנת משלוח" / "להזמנת שולחן" in the home hero only (Zap QA round 2: no buttons in inner-page heroes);
  both stay in the phone action bar, the menu page CTA and the footer menu (new tab).
- Blog added (Zap QA #10): 1 category, 3 posts from the brief and the client's menu; not in the brief's tree.
- Email / WhatsApp: still empty in the brief (re-read incl. tables and comments) and on every readable source → none shown.
- Fonts: one family (Noto Sans Hebrew). Text black on light grounds (incl. tile, FAQ, card and menu titles).
- Photos: wide crops for the three hero slots so nothing is shown larger than its pixels (QA check).
- zs qa 0 errors local and live (11 pages, 42 links); zs seo 0 FAIL.

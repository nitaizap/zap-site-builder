# BRIEF-CHECK — הרקולס גורקביץ (c743850)

Every line of `איפיון אתר - הרקולס-גורקביץ ... - 743850_3.docx` and of נועם's covering e-mail.
A ✅ means it was seen on the rendered page (screenshot or page HTML), never "it is in site.json".

## 1. סוג הפרויקט

| line | status | note |
|---|---|---|
| אתר מלא | ✅ | 18 pages + privacy + accessibility + blog with 3 posts |
| אתר SEO (בלוג) — empty | ✅ | a blog was added anyway: the SEO checklist needs a category with 3 posts (OPEN-ITEMS 11) |

## 2-3. פרטי לקוח וקשר

| line | status | note |
|---|---|---|
| שם העסק | ✅ | full legal name in the footer and schema; "הרקולס גורקביץ" as the display name (OPEN-ITEMS 7) |
| שנות פעילות משנת 1949 | ✅ | hero points, the about split, the profile page, the FAQ. 6 occurrences on the home |
| אתר קיים hercules.co.il | ✅ | crawled; all content and all product images taken from it |
| כתובת דרך שלמה 13, תל אביב | ✅ | footer, contact page, schema, Waze link |
| שעות פעילות | ✅ | footer and contact page |
| אימייל לאתר ולטופס לידים mirrors@zahav.net.il | ✅ | contact page; form recipient |
| טלפון לאתר 03-6828265 | ✅ | header button, footer, contact page, 6 `tel:` links on the home |
| איש קשר אסי גורקביץ 052-3909018 | ➖ | internal contact detail, not published (OPEN-ITEMS 12) |
| מספר מקשר זאפ — empty | ➖ | no tracking number, so no "מספר מקשר" popup (OPEN-ITEMS 4) |
| אזורי שירות — empty | ➖ | nothing to show |

## 4. נוכחות דיגיטלית

| line | status | note |
|---|---|---|
| וואטסאפ 052-2904020 | ✅ | floating button + mobile bar, `wa.me/972522904020` |
| פייסבוק / אינסטגרם / לינקדאין / GMB — empty | ➖ | no social bar, as the pool rules require |

## 5. תוכן האתר

| line | status | note |
|---|---|---|
| תחומי עיסוק (the long company text) | ✅ | home about split, the profile page, the dark prose band |
| עץ האתר לפי האתר הקיים | ✅ | all 11 existing categories + פרופיל + תחומי פעילות + צור קשר |
| + פנסים לכל סוגי הרכב (עמוד חדש) | ✅ | own page, in the menu, in the home card grid, in the footer |
| + מראות לרכבי אספנות (עמוד חדש) | ✅ | own page, in the menu, in the home card grid, in the footer |
| דף הבית: להציג את סוגי המראות (קטגוריות המוצרים) | ✅ | the 13-card "סוגי המראות" grid, each card its own photo |
| דף הבית: אזור וידאו (פריים) לסרטון שיופק | ✅ | **the frame is reserved and composed**, between the company story and the lead form: a full-width band at the 16:9 the player will use (measured 1440x810 at 1440, 1280x720 at 1280), holding a still from the client's own photography. Seen on the rendered page at 1440, 1280 and 390. The clip itself has not been produced; the exact JSON to paste when it arrives is in OPEN-ITEMS 1 (one paste, one rebuild) |
| סלוגן "ייצור ותיקון מראות לכל סוגי הרכב" | ✅ | hero lead and the top bar, 3 occurrences on the home |
| להדגיש: יבואני ויצרני מראות לכל סוגי הרכבים | ✅ | hero lead and the footer, 5 occurrences on the home |
| להדגיש בתפריט: פנסים, מראות לרכבי אספנות | ✅ | both under "תחומי פעילות" in the main menu and in the footer list |
| מסרים: מראות לעולם הרכב, ניסיון משנת 1949, תו תקן ISO 9001, הפצה בינלאומית | ✅ | hero points and the "למה הרקולס גורקביץ" block |
| כל התכנים והמוצרים יילקחו מהאתר הקיים | ✅ | every category text and every product list comes from the brief, which repeats the existing site |
| תמונות מוצרים — לשאוב מהאתר הקיים, כל תמונה לצד המוצר שלה | ✅ | 108 product photographs pulled from hercules.co.il, each matched to its product by catalogue number and placed on that product's card in its category page |
| אין להשתמש בתמונות מאגר או AI לתמונות מוצרים | ✅ | `grep '"ai": true' site.json` → 0. No stock image anywhere |
| תמונות אווירה — ממאגר או AI | ➖ | not needed: the client's own archive on F: covered every slot, so nothing was generated (OPEN-ITEMS 14) |
| כפתורי הנעה: ניווט, וואטסאפ, התקשרות | ✅ | Waze link on the address, WhatsApp floating button, phone in the header, all three in the phone bottom bar |
| טופס לידים "זקוקים למראה חדשה לרכב? השאירו פרטים..." | ✅ | verbatim, in the mid-page lead band and the footer form |
| חוות דעת (4.2 מתוך 15 בדפי זהב) | ⏳ | live Dapei Zahav widget, customer id 743850; a hard-coded rating is blocked by the validator and only renders once pushed (OPEN-ITEMS 2) |
| תחומי פעילות (the long text) | ✅ | the תחומי פעילות page, in full, as a list |
| each of the 11 category texts + product lists | ✅ | one page each, intro text + a card per product with its photograph + 3 FAQ |
| למה הרקולס גורקביץ (6 points) | ✅ | the "למה הרקולס גורקביץ" features block, all six |
| דף הבית: כותרת ותת-כותרת | ✅ | H1 is the client's name (Zap QA rule); the brief's headline wording is the hero lead |
| צור קשר (the text) | ✅ | the contact page |
| מאמרים — empty | ✅ | 3 posts written from the brief's own technical text |

## 6. עיצוב ומותג

| line | status | note |
|---|---|---|
| לוגו | ✅ | **the form is not empty.** `brief.md` is a text export and drops embedded images; the .docx carries one (`word/media/aa1a0db8e4c2367b079c9d7adf3e028ac19e19fb.png`), and it sits in the לוגו row: the client's official lockup, emblem + "Hercules-Gurkiewicz" + "הרקולס-גורקביץ" + a small tagline. Since 04/11/2026 the header and footer logo is cut from it (the tagline cropped off, per qa-rules) over the emblem from the client's own logo.tif. Checked on the rendered header at 1440 and 390 |
| צבעי מותג — empty | ✅ | sampled from the logo: `#BD3C42`, carried as the accent. Confirmed 04/11/2026 against the lockup embedded in the brief (its Latin wordmark is that red) and against the old site's own CSS, which sets `#bd3c42` |
| יד חופשית למעצב — empty | ✅ | direction chosen here and written up in NOTES.md |
| אתרים שאהבתם — empty | ➖ | nothing to follow |

## 7-8. תמונות וכתבת תדמית

| line | status | note |
|---|---|---|
| תמונת בעלים — empty | ➖ | none supplied |
| ללקוח אין חומרים גרפיים | ✅ | not true in the end: 2,249 files were found on `F:\SiteContent\00743850` and 396 were taken in |
| כתבת תדמית — empty | ➖ | nothing to place |

## נועם's e-mail

| line | status | note |
|---|---|---|
| "יש לוודא ששואב את כל תמונות המוצרים מהאתר הקיים" | ✅ | **verified independently on 04/11/2026**, not taken on trust: all 11 Hebrew gallery pages of hercules.co.il were fetched again and every `<img>` listed. The site carries **108** product photographs (ids 042-148 plus 726-730); `sites/c743850/assets/` holds **108**, and each one is byte for byte identical to the file the live site serves. Missing: 0. Extra: 0. The live site serves only one resolution per photograph (the lightbox links the same file), so nothing larger exists to pull. 16 of the 108 are small at source (250x188 to 338x450, mostly the משאיות set at 300x225); they are used on product cards, never as a page's lead photo |

## Gates

`bin/zs qa c743850` → 0 errors, 0 warnings (exit 0) · `bin/zs seo c743850` → 0 FAIL (exit 0) ·
`bin/zs pool c743850` → exit 0, home at most 38% like another client.

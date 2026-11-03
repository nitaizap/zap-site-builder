# BRIEF-CHECK — מרכז שירות יד מרדכי (80220135)

The spec sheet line by line against what was built.

**Legend.** ✅ = built and seen on the rendered page (a screenshot, a measurement, or the page's own HTML),
or enforced by a gate that passed. ➖ = deliberately not built, with the reason. ⏳ = open, waiting on someone.
⚠️ = built as far as the client's material allows, with a gap named.

The site was built, measured and looked at: `zs qa` 0 errors / 0 warnings, `zs seo` 0 FAIL, `zs pool` 37%
against the nearest other client. Nothing below rests on "it is in site.json".

## סוג הפרויקט

| line | status | note |
|---|---|---|
| אתר מלא, אתר תדמיתי | ✅ | 9 pages: home, אודות, 6 service pages, צרו קשר (+ privacy and accessibility from the engine) |
| אתר SEO (בלוג) | ⚠️ | empty on the spec. A blog with one category and three posts was added so `zs seo` reaches 0 FAIL; every post is written from spec material only (OPEN-ITEMS 6 and 11) |
| package | ⏳ | not named anywhere; built as `standard`, because the spec's own page list does not fit בייסיק (OPEN-ITEMS 1) |

## פרטי לקוח

| line | status | note |
|---|---|---|
| שם הלקוח: מוסך יד מרדכי | ✅ | `business.legal_name`, used in the privacy page and the contact copy |
| שם העסק: מרכז שירות יד מרדכי | ✅ | `business.name`, the home H1, every SEO title, the footer |
| מספר לקוח 80220135 | ✅ | slug `c80220135`, registered in `fingerprints/clients.json` |
| שנות פעילות: מעל 30 שנה | ➖ | contradicts the spec's own "הוקם בשנות ה-50". No number of years is claimed (OPEN-ITEMS 8) |
| אתר קיים | ⏳ | unreachable from this session; no content or slug could be carried over or 301'd |

## פרטי קשר

| line | status | note |
|---|---|---|
| איש קשר: ערן שטרנברג | ✅ | named on the about page as the manager, and set as `author_name` |
| כתובת: קיבוץ יד מרדכי, 7914500 | ✅ | NAP, schema, footer Waze link |
| אזורי שירות: אשקלון והסביבה | ✅ | `area_served`, the hero lead and every service page's first paragraph |
| שעות פעילות | ✅ | `hours` + `opening_hours` schema; also answered in the home FAQ and the contact page |
| אימייל לאתר: musach@y-m.co.il | ✅ | `email_public` |
| מייל לטופס לידים: musach@y-m.co.il | ✅ | `email_leads`; staging never mails the client |
| טלפון לאתר: 08-6720513 | ✅ | `phone_display` + `phone_e164` (+97286720513), validated as dialling the shown number |
| מספר מקשר זאפ | ➖ | empty on the spec, so `phone_is_virtual` stays false (OPEN-ITEMS 8) |

## נוכחות דיגיטלית

| line | status | note |
|---|---|---|
| וואטסאפ: 052-6758069 | ✅ | `whatsapp_e164` +972526758069, floating button and mobile bar, prefilled message |
| פייסבוק | ✅ | `business.facebook`, social bar and schema `sameAs` |
| אינסטגרם | ✅ | `business.instagram`, same |
| לינקדאין | ➖ | empty on the spec; no item invented |
| Google My Business | ⏳ | empty on the spec; no `gmb_url`, so no `hasMap` in schema (OPEN-ITEMS 8) |

## תוכן האתר

| line | status | note |
|---|---|---|
| תחומי עיסוק (the long paragraph) | ✅ | split across the home `facts` section and the about page; every sentence kept, wording modernised only where needed |
| עמוד הבית, כותרת ראשית "מרכז שירות יד מרדכי" | ✅ | the H1, the client's name only, as Zap QA requires |
| כותרת משנה "מורשה לרכבי מאזדה פורד דונגפנג ווויה באשקלון והסביבה" | ✅ | carried by the hero `lead`, which opens with the page's keyword |
| עמוד אודות | ✅ | `אודות`, H1 "אודות מרכז שירות יד מרדכי" |
| פחחות וצבע | ✅ | own page, spec text verbatim in the lead, then its own sections and FAQ |
| דיאגנוסטיקה ואבחון | ✅ | own page, same pattern |
| חשמל רכב | ✅ | own page, same pattern |
| מערכות מיזוג אוויר | ✅ | own page, same pattern |
| צמיגים | ✅ | own page, same pattern |
| מכונאות רכב | ✅ | own page, same pattern |
| צרו קשר: טופס לידים, טלפון, כתובת ומפה | ✅ | `contact` section with `map: true`, plus the NAP block |
| אזור שירותים, קוביות לכל שירות עם קישור לעמוד | ✅ | `cards` section, six cards, each linking its page, one meaningful icon each |
| באנר מבצע חלקים מקוריים | ✅ | `cta` `photo` band, the spec's wording including "רכבים מעל 3 שנים, ט.ל.ח" |
| אזור חוות דעת לקוחות | ✅ | `reviews` section on the home page, Dapei Zahav customer id 80220135, verified against the API payload (its links point at this client's own listing). Renders on the pushed site only, so it is empty in the local screenshots (OPEN-ITEMS 4) |
| לוגואים של המותגים המורשים (מאזדה, פורד, דונגפנג, וויה) | ✅ | all four shown. Mazda and Ford from the client's files; דונגפנג and וויה from dongfeng.co.il, the importer's own site (IMAGE-SOURCES.md). The המחלקה הראשונה badge follows them |
| "המחלקה הראשונה למסחריות" | ✅ | in the logos band, the band's text and the home FAQ |
| כפתורי חיוג ווואטסאפ צפים | ✅ | seen on the rendered pages: floating WhatsApp button on desktop, call + WhatsApp bar on phones, on every page |
| מבצע חלקים מקוריים (text) | ✅ | the band plus a home FAQ answer |
| מגוון רחב של שירותים במקום אחד | ✅ | `split` `frame`, spec text, workshop photo |
| למה אנחנו, הלקוח בראש סדר העדיפויות | ✅ | `split` `card` + `features` `checks` + `steps` `stack`, all from the spec's own sentences |
| מאמרים | ⚠️ | empty on the spec, so nothing was promised here. Three posts were nevertheless written from the spec's own material, because `zs seo` fails a site with no blog category (OPEN-ITEMS 6 and 11) |

## עיצוב ומותג

| line | status | note |
|---|---|---|
| לוגו: אין לוגו לעסק | ⏳ | no header or footer logo: the name renders as text. The favicon is a stand-in brand tile so the base install's icon cannot ship. Nothing drawn or traced from the sign (OPEN-ITEMS 3) |
| לוגואים בגודל אחיד ובמרווחים שווים | ✅ | measured on the rendered page: five chips at exactly 160 px wide, 174 px apart, one row. Each logo was re-cut onto a shared canvas and scaled to equal optical area, because the sources run from 7:1 to 1.8:1 |
| סדר משמאל לימין: מאזדה, פורד, דונגפנג, וויה | ✅ | measured on the rendered page: מאזדה, פורד, דונגפנג, וויה, then the badge, left to right at 1440 px. On phones the column is reversed so it reads the same top down |
| רק הלוגו המעודכן של מאזדה, לא הישן | ⚠️ | `Logo_FullColor_Horizontal.png` used. Three files show the same artwork and the spec does not say which is "המצורף" (OPEN-ITEMS 5) |
| לוגו פורד מהאתר הקיים | ✅ | the existing site is unreachable; `לוגו-פורד-ללא-רקע.png` from the client's own files was used instead |
| צבעי מותג | ➖ | none given |
| יד חופשית למעצב, צבעים לפי החלטת המעצב | ✅ | petrol `#14525e` + bronze `#8a4b0a`, taken from the building as it looks in the 2022 photos. Reasoning and measured contrast in NOTES.md |
| אתרים שאהבתם | ➖ | empty on the spec |

## תמונות

| line | status | note |
|---|---|---|
| תמונת בעלים | ➖ | empty on the spec; no portrait used or generated |
| גלריה: לקחת תמונות מהאתר הקיים | ⚠️ | the existing site is unreachable. Seven usable photographs from the F: drive are used instead; the 2020 blue-facade shots and the KIA banner are excluded (NOTES.md → Images, OPEN-ITEMS 8) |

## כתבת תדמית

| line | status | note |
|---|---|---|
| כתבת תדמית | ➖ | empty on the spec |

## Prohibitions and house rules

| rule | status | how checked |
|---|---|---|
| no em dash anywhere in copy | ✅ | grep over site.json: none |
| no en dash as punctuation | ✅ | grep: none. The 5 en dashes are ranges (07:00–16:00, ראשון–חמישי) |
| no shortcodes | ✅ | grep for `[zap_`: none. Only native sections and `zap-*` widgets |
| no invented ratings, reviews or counts | ✅ | grep + validator: none |
| no placeholders | ✅ | grep + validator: none |
| no unverifiable superlatives | ✅ | grep + validator: none |
| no invented business facts | ✅ | every fact traced to a spec line in NOTES.md's facts table |
| home H1 = the client's name only | ✅ | validator enforces it |
| `<client> \| <page>` title on every page | ✅ | validator enforces it |
| meta descriptions 150–160 chars | ✅ | all 9 measured in range |
| slug = H1 = menu label | ✅ | validator, no warnings raised |
| unique keyword per page | ✅ | validator, no cannibalisation |
| ALT on every image | ✅ | validator enforces it |
| no buttons in inner-page heroes | ✅ | validator enforces it |
| page never ends on a `cta` | ✅ | validator enforces it |
| no duplicate icons in a section | ✅ | validator enforces it |
| no photo twice in one section | ✅ | validator enforces it |

## Measured

| check | result |
|---|---|
| `zs qa` (11 URLs × 2 viewports, 19 internal links) | 0 errors, 0 warnings |
| `zs seo` (the team's checklist, row by row) | 0 FAIL; `SEO-QA-c80220135.xlsx` written |
| `zs pool` uniqueness against every other client | 37% (limit 40%) |
| hero above the fold at 1280×620 and 360×640 | passes |
| mobile menu opens full screen, Escape closes | passes |
| lead form: thank-you shown, lead saved, no mail sent from staging | passes |
| header at 1536 / 1440 / 1366 / 1280 / 1100 / 1025 | no overlap, no horizontal scroll, no wrapped labels |
| every image | converted to WebP and under 100 KB by the build |

## Looked at by eye

Home page read in full at 390 px; service, contact, blog index and a blog post shot at 390; the header and
the logos band shot at 1440 and 1280. Fixed as a result: the marque chips were different sizes and in the
wrong order, and nine menu items did not fit a laptop header (OPEN-ITEMS 11).

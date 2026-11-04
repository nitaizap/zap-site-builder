# BRIEF-CHECK — מרכז שירות יד מרדכי (80220135)

The spec sheet line by line against what was built.

**Legend.** ✅ = built and seen on the rendered page (a screenshot, a measurement, or the page's own HTML),
or enforced by a gate that passed. ➖ = deliberately not built, with the reason. ⏳ = open, waiting on someone.
⚠️ = built as far as the client's material allows, with a gap named.

The site was built, measured and looked at. Re-measured in full on 04/11, after merging `main` at `6a9a262`
(PR #86 then PR #88, the shared theme, engine and plugin fixes): `zs qa` **0 errors / 0 warnings**,
`zs seo` **0 FAIL**, `zs pool` raises nothing and the highest measured likeness to any other client is
**33%** (`mehirut-haor`, limit 40%). Every width below was measured **with a real 15px scrollbar**
(Playwright hides scrollbars by default, which hides this class of fault completely). Nothing below rests
on "it is in site.json".

## סוג הפרויקט

| line | status | note |
|---|---|---|
| אתר מלא, אתר תדמיתי | ✅ | 9 pages: home, אודות, 6 service pages, צרו קשר (+ privacy and accessibility from the engine) |
| אתר SEO (בלוג) | ✅ | the spec row is empty, so nothing was asked for; a blog with one category and three posts was built anyway, because `zs seo` fails a site with no blog category. Every post is written from spec material only, and nothing is waiting on anyone to make it work. The one thing the client should do before launch is read the three posts and say they are happy to have them (OPEN-ITEMS 6 and 11) |
| package | ⏳ | not named anywhere; built as `standard`, because the spec's own page list does not fit בייסיק (OPEN-ITEMS 1) |

## פרטי לקוח

| line | status | note |
|---|---|---|
| שם הלקוח: מוסך יד מרדכי | ✅ | `business.legal_name`, used in the privacy page and the contact copy |
| שם העסק: מרכז שירות יד מרדכי | ✅ | `business.name`, the home H1, every SEO title, the footer |
| מספר לקוח 80220135 | ✅ | slug `c80220135`, registered in `fingerprints/clients.json` |
| שנות פעילות: מעל 30 שנה | ➖ | contradicts the spec's own "הוקם בשנות ה-50". No number of years is claimed (OPEN-ITEMS 8) |
| אתר קיים | ⚠️ | ym-mazdaford.co.il was read with `bin/zs grab` (output in `research/`); every factual claim on the new site was cross-checked against it and none had to change (OPEN-ITEMS 13). **What is missing:** the 301 map from the old URLs to the new ones. It cannot be written here, because the old site is a single-page JavaScript app whose routes do not appear in the grab, and the redirects have to be installed on the live host after the domain moves. **Who supplies it:** whoever performs the launch, from the old host's URL list; it belongs on `LAUNCH-SHEET.md`, not in this build |

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
| פייסבוק | ✅ | `business.facebook`, social bar and schema `sameAs`. Read on 04/11 for identity and photographs: the page serves only its title to a logged-out reader, `מרכז שירות יד מרדכי מוסך מאזדה פורד - אזור אשקלון`, which matches what the site already says. No cover photo, About text, hours or posts are reachable without signing in, so nothing was taken from it |
| אינסטגרם | ✅ | `business.instagram`, same. Read on 04/11: public, display name `מרכז שירות יד מרדכי מאדה פורד`, 94 followers, a grid of 12 thumbnails (3 reels, 9 photos, dated 2021-2026) and two `הנבחרים` highlights. There is no bio text, no hours and no captions to a logged-out reader, and the thumbnails are thumbnails. Nothing was copied from it: an image whose origin and rights are not documented is not used (CLAUDE.md, image rights). If the client wants their Instagram photographs on the site they can say so and send the originals, and each one gets a row in `IMAGE-SOURCES.md` |
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
| צרו קשר: טופס לידים, טלפון, כתובת ומפה | ✅ | all four present. Form, phone and address in the `contact` section + NAP block; the map renders as a real `<iframe src="https://www.google.com/maps?q=קיבוץ יד מרדכי&output=embed&hl=iw">` with the title `מפת הגעה: מרכז שירות יד מרדכי`. Closed 04/11 after merging `main` at `1aa7aa2` (PR #86), which stops the part widget passing a blank control to the shortcode, so `business.address` applies. The per-client workaround that hid the empty container and collapsed the contact row to one column was **deleted** in the same pass. Measured at 1440 with a real scrollbar: map and form end on the same line (both 1599px locally, 1596px live), and at 1280 both end at 1583px, so the column is full, not half-empty |
| אזור שירותים, קוביות לכל שירות עם קישור לעמוד | ✅ | `cards` section, six cards, each linking its page, one meaningful icon each |
| באנר מבצע חלקים מקוריים | ✅ | `cta` `photo` band, the spec's wording including "רכבים מעל 3 שנים, ט.ל.ח" |
| אזור חוות דעת לקוחות | ✅ | `reviews` section on the home page, Dapei Zahav customer id 80220135, verified against the API payload (its links point at this client's own listing). Renders on the pushed site only, so it is empty in the local screenshots (OPEN-ITEMS 4) |
| לוגואים של המותגים המורשים (מאזדה, פורד, דונגפנג, וויה) | ✅ | all four shown. Mazda and Ford from the client's files; דונגפנג and וויה from dongfeng.co.il, the importer's own site (IMAGE-SOURCES.md). The המחלקה הראשונה badge follows them |
| "המחלקה הראשונה למסחריות" | ✅ | in the logos band, the band's text and the home FAQ |
| כפתורי חיוג ווואטסאפ צפים | ✅ | seen on the rendered pages: floating WhatsApp button on desktop, call + WhatsApp bar on phones, on every page |
| מבצע חלקים מקוריים (text) | ✅ | the band plus a home FAQ answer |
| מגוון רחב של שירותים במקום אחד | ✅ | `split` `frame`, spec text, workshop photo |
| למה אנחנו, הלקוח בראש סדר העדיפויות | ✅ | `split` + `steps` `cards`, from the spec's own sentences. The `features` `checks` strip was removed on 04/11: all six of its labels were already said by the `steps` block directly above it or by the hero bullets |
| מאמרים | ✅ | the spec row is empty, so nothing was promised. Three posts were written from the spec's own material and are live in the menu and on the blog index; same client sign-off as the row above (OPEN-ITEMS 6 and 11) |

## עיצוב ומותג

| line | status | note |
|---|---|---|
| לוגו: אין לוגו לעסק | ⏳ | confirmed against the `.docx` on 04/11: its three embedded images are marque logos, there is no business mark. No header or footer logo: the name renders as text. The favicon is a stand-in brand tile so the base install's icon cannot ship. Nothing drawn or traced from the sign (OPEN-ITEMS 3) |
| לוגואים בגודל אחיד ובמרווחים שווים | ✅ | five chips on one grid: the badge beside the text, the four marques in a 2x2. All five chips are now the same height (124 px desktop, 92 px phone) and share one gap, and each mark is fitted to its chip, so none floats in padding |
| סדר משמאל לימין: מאזדה, פורד, דונגפנג, וויה | ✅ | the four marques sit in a 2x2 that reads מאזדה, פורד on the top row and דונגפנג, וויה on the second, left to right, at 1440 px and on phones. The importer's המחלקה הראשונה badge is not one of the four and sits beside the text rather than in the sequence |
| רק הלוגו המעודכן של מאזדה, לא הישן | ✅ | **corrected 04/11.** "המצורף" is literally attached: the spec's `.docx` carries the updated Mazda lockup in `word/media/`, which the `brief.md` text export drops. The band had been using the old chrome-gradient wordmark from the `F:` folder, the one this line forbids. Now the client's own attachment (OPEN-ITEMS 5, 19) |
| לוגו פורד מהאתר הקיים | ✅ | the existing site was read; its only Ford artwork is a manufacturer stock composite of unclear licence, so `לוגו-פורד-ללא-רקע.png` from the client's own files was used instead (IMAGE-SOURCES.md) |
| צבעי מותג | ➖ | none given |
| יד חופשית למעצב, צבעים לפי החלטת המעצב | ✅ | petrol `#14525e` + bronze `#8a4b0a`, taken from the building as it looks in the 2022 photos. Reasoning and measured contrast in NOTES.md |
| אתרים שאהבתם | ➖ | empty on the spec. Confirmed against the `.docx` itself on 04/11, not only the text export: the row carries no text and no link |

## תמונות

| line | status | note |
|---|---|---|
| תמונת בעלים | ➖ | empty on the spec; no portrait used or generated |
| גלריה: לקחת תמונות מהאתר הקיים | ⚠️ | re-checked file by file on 04/11 against `research/img/manifest.json`. The existing site carries exactly **four photographs**, all taken on 20/05/2022 and all exteriors: three angles of the building and one of the pylon sign, at 1920px (its own alt text mislabels them `משרד קבלה`, `חדר המתנה`, `אולם עבודה`, but the pixels are facade shots). They are the same scenes already in `assets/` at 1600px, so the old site adds **nothing new** at any size; its only other artwork is a manufacturer stock composite of unclear licence, which is not usable. The three interior photographs (דלפק קבלה, חדר המתנה, אולם העבודה) exist only in the F: drive folder and only at **800×600**, which is fine in a column or a card and soft when stretched across a 1440px hero. **The gap, in one line for the client:** נשמח לקבל מכם צילומים חדשים ברוחב 1600 פיקסל ומעלה: אולם העבודה בזמן טיפול, עמדת דיאגנוסטיקה, עבודת פחחות וצבע, החלפת צמיגים, יועץ שירות מול לקוח ורכב מסחרי במחלקה הראשונה למסחריות. **Who supplies it:** the client, through the salesperson; no one else has the material (NOTES.md → Images, OPEN-ITEMS 8) |

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
| `zs qa` (16 URLs × 2 viewports, 24 internal links) | 0 errors, 0 warnings (re-measured 04/11 on `main` at `6a9a262`) |
| `zs seo` (the team's checklist, row by row) | 0 FAIL, 39 rows: 34 pass, 5 manual; `SEO-QA-c80220135.xlsx` written |
| `zs pool` uniqueness against every other client | no warning; highest measured likeness 33% against `mehirut-haor` (limit 40%). It had risen to 40% before the palette change, see OPEN-ITEMS 17 |
| hero above the fold at 1280×620 and 360×640 | passes |
| mobile menu opens full screen, Escape closes | passes |
| lead form: thank-you shown, lead saved, no mail sent from staging | passes |
| header + top strip at 1536 / 1440 / 1366 / 1280 / 1100 / 1025 | no overlap, no horizontal scroll, no wrapped labels. Re-measured 04/11 on `main` at `6a9a262` **with a real 15px scrollbar**, against the accessibility toggle (fixed in the viewport's left corner, right edge at 52px). Leftmost content, header row and top strip alike: **92 / 92 / 60 / 76 / 113 / 161px** at 1025 / 1100 / 1280 / 1366 / 1440 / 1536, i.e. clearances of 40 / 40 / 8 / 24 / 61 / 109px. The theme reserves the room from the layout width for both rows, so the per-client `.zs-topbar__in` rule this site carried was **deleted**. The same numbers on the live staging site |
| every image | converted to WebP and under 100 KB by the build |

## Looked at by eye

Home page read in full at 390 px; service, contact, blog index and a blog post shot at 390; the header and
the logos band shot at 1440 and 1280. Fixed as a result: the marque chips were different sizes and in the
wrong order, and nine menu items did not fit a laptop header (OPEN-ITEMS 11).

**Second pass, 04/11.** Every page shot full height at 1440, 1280 and 390 and read. Four things changed:

1. **The map is back** and the contact page is two full columns again (see the `צרו קשר` row). The
   workaround that collapsed it was deleted.
2. **The prose-centring workaround was deleted.** `main` now carries `margin-inline: auto` on `.zs-prose`,
   so the client rule only duplicated it. Re-measured at 1440 after deleting it: the column sits at
   `left 333px / right 348px` of a 1440px viewport on אודות and on all six service pages — centred, the
   15px being the scrollbar.
3. **The six service pages opened by saying the same sentence twice.** The hero lead and the first prose
   paragraph were near-identical, one directly under the other, on every one of them. The spec's own
   wording now stays in the hero, where a visitor actually reads it, and each page opens on a paragraph
   that says something new. On פחחות וצבע and מערכות מיזוג אוויר the spec's own punchier line
   ("עברתם תאונה? הרכב ניזוק?", "בקיץ הישראלי זה הכרחי") moved up into the hero. No new facts: every
   sentence traces to the spec's `תחומי עיסוק` paragraph or to its own service line.
4. **The service pages had no picture after the hero and a nameless FAQ strip** stretched across the full
   width. Their FAQ is now the `aside` variant: a heading (`שאלות נפוצות`) and the questions beside a tall
   photograph, so the page reads hero → text → image band → form instead of hero → text → text. The pylon
   photograph, which is 1600×2151 and was being cropped to a thin strip as a hero, is finally used at its
   own shape here.

## Covered, but thinner than Zap QA's own bar

Every service the spec names has its own page with the spec's own wording, so the brief is covered. The six
service pages are nevertheless **248–326 words** (re-counted 04/11, FAQ answers included) against the 450–800
that `qa-rules.md` asks of a trade, and no gate catches it. The 04/11 rewrite replaced a duplicated opening
rather than adding length, so the gap is essentially unchanged.

**What is missing:** for each of the six services, what the client actually does that a competitor does not.
Typical examples: the equipment in the bay, how long a job takes, what is covered by the importer's warranty,
what a commercial vehicle gets under המחלקה הראשונה. **Who supplies it:** ערן שטרנברג, in one phone call of
about twenty minutes; roughly 200 words per page come out of it. Nothing on the client's own properties closes it: the old site is
946 words in total, and the Facebook and Instagram pages were both checked on 04/11 and are unreadable
without logging in (see the `נוכחות דיגיטלית` rows). It will not be invented here. Recorded in OPEN-ITEMS 16.


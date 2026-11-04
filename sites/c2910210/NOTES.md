# NOTES — מוניות כפר סבא בע״מ (2910210)

## Facts, with a source for each

| fact | value | source |
|---|---|---|
| שם העסק / legal name | מוניות כפר סבא בע״מ | spec sheet |
| מספר לקוח | 2910210 | spec sheet |
| כתובת | רוטשילד 50, כפר סבא | spec sheet; confirmed on d.co.il/2910210 |
| geo | 32.175018, 34.908471 | d.co.il listing map |
| טלפון לאתר | 09-7661111 | spec sheet; also on the station sign in the client's own photo |
| מספר מקשר זאפ | 072-3257979 | spec sheet; shown as the contact number on d.co.il |
| אימייל | taxikfarsaba@bezeqint.net | spec sheet (both "אימייל לאתר" and "מייל לטופס לידים") |
| שעות פעילות | 24 שעות ביממה, 7 ימים בשבוע, כולל שישי, שבת ומוצאי שבת | spec sheet; d.co.il "זמינות" tags |
| אזורי שירות | כפר סבא, רעננה, הוד השרון, הרצליה, רמת השרון, פתח תקווה, ראש העין, כפר יונה, אבן יהודה, כוכב יאיר | spec sheet; identical list on d.co.il |
| שנת ייסוד | 1955 | the company's own storefront sign, photographed in their material folder (`20121225_170623.jpg`): "נוסד 1955". Not in the spec, see OPEN-ITEMS 3 |
| Google Business | https://maps.google.com/?cid=9921269185300775859 | spec sheet |
| דפי זהב customer id | 2910210 | d.co.il/2910210, verified on name + street + phone |
| תחומי עיסוק (wording) | the paragraph used on the about page | spec sheet "תחומי עיסוק"; the identical text appears as the company's own "אודות" on d.co.il |
| למה אנחנו (6 items) | 24/7, רכבים חדישים ומרווחים עם GPS, נהגים ללא הרשעות קודמות, הסדרי אשראי לחברות והסדרים עם ועדי עובדים, הזמנה באתר ובאפליקציה, שירות באנגלית וברוסית | spec sheet "למה אנחנו"; the same features are listed on d.co.il |
| סלוגן | אל היעד הבא עם מוניות כפר סבא! | spec sheet; also on the client's own mobile banner file |
| אתר קיים | www.taxi-ks.co.il | spec sheet. **Did not load** (connection refused on 212.199.115.180). The Wayback copy could not be fetched from this session either, so nothing was taken from the old site except the files already in the client's material folder |
| אתרים שאהבתם | nitzav-taxi.co.il, moniot.info | spec sheet. Looked at as references for what the client likes, not copied |
| לוגו / צבעי מותג | blank in the spec | taken from the client's own business card photo, see IMAGE-SOURCES.md |

Nothing on the site states a fact that is not in this table.

## Design brief (three lines)

- **Subject:** a taxi rank in Kfar Saba that also runs scheduled transport, courier runs and airport pickups.
- **Audience and moment:** someone who needs a car now, often at an awkward hour (a 05:00 flight, a Shabbat
  evening, a shift ending at 02:00), or an office manager setting up standing rides for a company.
- **The page's single job:** call the dispatch centre, or leave a phone number for it to call back.

## Direction (chosen in automatic mode, no gate)

Base template 5 (white + a strong colour, overlay tiles, form over a photo). Deviations: the palette is the
client's own green and taxi yellow instead of red; the kit is `panels` instead of the template's flat
sections; the home opens on the `booking` archetype, so the lead form sits under the hero rather than
further down.

- `design.kit`: **panels** (no other client branch uses it)
- `design.archetype`: **booking** (no other client branch uses it)
- `design.preset`: bold · `hero`: split · `header`: light · `radius`: 16 · `motion`: subtle
- fonts: **Rubik / Heebo** (no other client branch uses this pairing)
- colours: primary `#0C5137`, accent `#F2C200`, dark `#0A2E21`, surface `#EFF4F0`

**The one bold thing:** the yellow taxi-roof accent carried through the whole page (the eyebrow chips, the
step numerals, the buttons' counterpart) against a deep green that comes straight off their own sign.

Home order: `hero` → `features:rows` → `cards` → `overlay` → `split:frame` → `steps:stack` → `facts` →
`collage` → `reviews` → `faq:dark`. Five of those variants (`features:rows`, `overlay`, `steps:stack`,
`collage`, `faq:dark`) are used by no other client, which is what brought the uniqueness measure down.

### Uniqueness, measured

First composition measured 41% against bella-mare and 42% against white-villa (both ERROR). Redesigned:
kit `frame` → `panels`, and the shared components (`features:checks`, `gallery:mosaic`, `faq:outline`,
`marquee`, `route`) were replaced with variants no other client uses. Final: **35% white-villa,
34% kisos-beach-club, 33% patoccina**, everything else lower. `bin/zs pool c2910210` exits 0.

## Keyword map

| page | keyword | H1 |
|---|---|---|
| `/` | מוניות בכפר סבא | מוניות כפר סבא בע״מ |
| `/אודות/` | תחנת מוניות בכפר סבא | אודות מוניות כפר סבא |
| `/מוניות-ספיישל/` | מוניות ספיישל | מוניות ספיישל |
| `/מוניות-לנתב״ג-וקבלת-אורחים/` | מונית לנתב״ג | מוניות לנתב״ג וקבלת אורחים |
| `/הסעות-עובדים-לחברות-ומוסדות/` | הסעות עובדים | הסעות עובדים לחברות ומוסדות |
| `/הסעות-תלמידים-וילדים/` | הסעות תלמידים | הסעות תלמידים וילדים |
| `/הסעות-יוקרה-והסעות-אמנים/` | הסעות יוקרה | הסעות יוקרה והסעות אמנים |
| `/מוניות-6-מקומות-ומעלה/` | מוניות 6 מקומות | מוניות 6 מקומות ומעלה |
| `/הסעות-לנכים/` | הסעות לנכים | הסעות לנכים |
| `/שירותי-נהג-צמוד/` | נהג צמוד | שירותי נהג צמוד |
| `/שליחויות-אקספרס/` | שליחויות אקספרס | שליחויות אקספרס |
| `/בלוג/` | בלוג מוניות כפר סבא | בלוג |
| `/צור-קשר/` | צור קשר מוניות כפר סבא | צור קשר עם מוניות כפר סבא |

Posts: מונית לנתב״ג מהשרון · הסדר הסעות עובדים · הסעת תלמידים קבועה, all in the category נסיעות והסעות.

## Measured results

Re-measured 2026-11-03 against `main` at `8858994` (theme PR #73 merged in from the branch, no local
patch), exit codes read directly and not through a pipe:

- `bin/zs qa c2910210`: exit 0, **0 errors, 0 warnings** (38 page × viewport checks, 31 internal links, all 200)
- `bin/zs seo c2910210`: exit 0, **0 FAIL**
- `bin/zs pool c2910210`: exit 0, highest match **35% white-villa**, then 34% kisos-beach-club,
  34% c80386843, 33% patoccina. c80220135's move to the petrol palette `#14525e` left this site
  unaffected: it no longer appears among the matches at all, so it is below 33%.

## Delivery state

Pushed 2026-11-03 to https://2910210kfarsabataxis.ussl.co.il (staging, from SharonY's mail). Admin claimed with
`zs staging` (password reset through Outlook), connected with `zs connect`, `zs push` exit 0.

Re-measured on current `main` (`b954e40`) before the push: `zs pool` highest 35% white-villa (exit 0), `zs qa` 0
errors, `zs seo` 0 FAIL. Live QA (`zs qa --site`): 0 errors, 0 warnings. Live pages checked by fetching them: all 13
pages answer 200 with `<title>` = `<name> | <page>` and the real H1; no `Basic Site` / `כותרת ראשית` title anywhere;
the base's placeholder page was moved to draft by the push.


## Polish pass, 2026-11-04 (branch `pub-c2910210`, `main` merged in at 017122d)

Brief in hand again, both reference sites opened, every page looked at at 1440 and 390. The brief's own
`.docx` was opened as a zip this time: `word/media/` holds exactly one image, the logo in the `לוגו` cell.
Nothing else was hidden by the text export.

### What the two "אתרים שאהבתם" actually show

`nitzav-taxi.co.il` and `moniot.info` are not sites to copy, and they were not copied, but they agree on
four things, and the build now answers all four:

1. **The phone number is written out and loud.** nitzav puts it in the top bar at display size; moniot puts
   the digits inside the button. Here the header call control is now a filled taxi-yellow pill with the
   number in it, on every page, desktop and tablet (the phone header keeps the standard plain icon).
2. **A single strong accent used as a large flat fill**, not as trim. nitzav fills whole service tiles with
   its lime; moniot's page is yellow. Here the client's own taxi yellow now carries a full-width call band.
3. **An ordering action high on the page and repeated.** nitzav puts the booking form inside the hero;
   moniot puts a phone band directly under the header. Here the hero form stays, and the new accent band
   repeats the action right after the nine service cards, where a visitor has just found their service.
4. **Flat and direct, with no ornament.** That is what the ghost watermark and the overlapping collage were
   breaking, so both are gone.

What was deliberately *not* taken: moniot's keyword-stuffed title and footer link farm, nitzav's sticky
WhatsApp bubble (the brief leaves וואטסאפ blank), and both sites' layouts. `bin/zs pool` is unchanged at a
35% high-water mark, so nothing drifted toward another client either.

### Changes

| # | change | why |
|---|---|---|
| 1 | `logo` to `assets/logo-brief.png`: the artwork embedded in the brief's `לוגו` cell, cropped above its slogan strip | the better-sourced file, flat instead of a photographed scan, and the only one that spells the business name. Full reasoning and the side-by-side in `IMAGE-SOURCES.md` |
| 2 | header call button: filled taxi yellow inside its existing green outline, desktop only (`design.custom_css`) | the brief asks for a "כפתור חיוג בולט ... בכל עמוד" and it was a quiet white outline. The outline stays because it is what carries the 3:1 control contrast against the white header (WCAG 1.4.11); yellow on white is 1.68 and `zs qa` catches it |
| 3 | new `cta` band with `bg: accent` after the services cards, phone number inside the primary button | the client's taxi yellow had no real presence on the page, and the only call to action above the footer sat in the hero |
| 4 | home `collage` band removed | the worst band on the site: a giant pale "מוקד" ghost word that read as a rendering accident, over two overlapping photos at mismatched scales. Its content (the station at רוטשילד 50, the round-the-clock dispatch) is already carried by the `split:frame` band just above it, by the facts card, and by the about and contact pages, so nothing was lost |
| 5 | `facts` band: second paragraph added, from the brief's own `למה אנחנו` lines | the column held three short lines against a 430px card, with roughly 700px of bare ground beside it. Exactly `hero-space.md` symptom 2, in a band that is not the hero |
| 6 | `cta2` label shortened to "השאירו טלפון" | reads better, and the long label was part of what pushed the band past 390px |
| 7 | `design.custom_css`: `.zs-cta__text` takes the full row under 600px | works around the engine bug below; without it the home page scrolled sideways at 390 (434px against 390px) |

### An engine/theme bug found here and NOT fixed (out of scope on a client branch)

`wp/theme/zap-base/assets/main.css:347` sets `.elementor .e-con.zs-cta__text { flex: 1 1 420px; }`. A
420px flex-basis cannot fit a 390px viewport and the item does not shrink below it, so **any** client with
a `cta` section overflows horizontally on a phone: measured here at `document.documentElement.scrollWidth`
= 434 against a 390 viewport, which `zs qa` reports as "page scrolls sideways". Worked around in this
client's `custom_css` only. The generic fix belongs in the theme (a `min-width: 0` on the item, or a
smaller basis under the phone breakpoint) and should be made on its own branch, tested on
`examples/sample-plumber`.

### Left alone on purpose

- **The hero.** Confirmed fine; `finish.css:102` was not touched and this client needs no override.
- **The about page's dispatch photo** (`dispatch-room`, a 2006 CRT showing a street map). It is dated, but
  it is the client's own, it shows no person, and there is no better frame in the 227-file folder:
  `dispatch-night` and `dispatch-phone` are blurrier and both show identifiable staff. The real fix is new
  photographs, already OPEN-ITEMS A.
- **Palette, kit, archetype, fonts, page tree, copy, and all 13 pages' structure.** This was a polish pass.
- **The two phone numbers** (OPEN-ITEMS 4) and the privacy confirmation (OPEN-ITEMS C) still need a human.

### Gate numbers

| gate | before | after |
|---|---|---|
| `bin/zs qa c2910210` | 0 errors, 0 warnings | **0 errors, 0 warnings** (38 page x viewport checks, 31 internal links all 200) |
| `bin/zs seo c2910210` | 0 FAIL | **0 FAIL** (39 rows: 32 pass, 0 fail, 5 manual) |
| `bin/zs pool c2910210` | 35% white-villa (highest) | **35% white-villa**, then 34% c80386843, 34% kisos-beach-club, 33% patoccina |

Side effect worth recording: with `dispatch-desk` off the home page, **no identifiable person appears
anywhere on the site any more**, so OPEN-ITEMS B (consent of the people in the photos) is closed.

Mechanically verified on all 13 pages at 1440 and at 390, by loading each page and querying the DOM: a
visible header call control, 3 to 6 visible `tel:` links, and a taxi-ordering form on every one. The
brief's "כפתור חיוג בולט והזמנת מונית בכל עמוד" is true, not assumed.

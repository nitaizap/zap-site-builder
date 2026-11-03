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

Built and reviewed locally only. No staging URL exists for this client yet, so nothing was pushed and
nothing was published.

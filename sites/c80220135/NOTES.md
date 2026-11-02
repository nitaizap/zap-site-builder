# מרכז שירות יד מרדכי (80220135) — notes

Branch `site/c80220135`. Built in automatic mode from `brief/brief.md` (spec sheet
`איפיון אתר - מרכז שירות יד מרדכי - 80220135_1.docx`, dated 01/11/2026) and the 25 files in
`assets/client/` copied from `F:\SiteContent\80220135`.

## Facts table

| fact | value | source |
|---|---|---|
| business name | מרכז שירות יד מרדכי | spec, שם העסק |
| legal / client name | מוסך יד מרדכי | spec, שם הלקוח |
| client id | 80220135 | spec |
| contact person | ערן שטרנברג | spec, איש קשר |
| address | קיבוץ יד מרדכי, 7914500 | spec, כתובת העסק |
| area served | אשקלון והסביבה | spec, אזורי שירות |
| phone | 08-6720513 | spec, טלפון לאתר |
| WhatsApp | 052-6758069 | spec, וואטסאפ |
| site e-mail / leads | musach@y-m.co.il | spec, אימייל לאתר + מייל לטופס לידים |
| hours | א׳–ה׳ 07:00–16:00, ו׳ 07:00–12:30, שבת סגור | spec, שעות פעילות |
| Facebook | facebook.com/ymmazdaford | spec |
| Instagram | instagram.com/yad_mordechai_service_center | spec |
| founded | שנות ה-50 של המאה ה-20 | spec, תחומי עיסוק |
| Mazda licence | 1996, מטעם דלק מוטורס בע״מ | spec, תחומי עיסוק |
| Ford licence | 2000 | spec |
| Dongfeng + Voyah licence | 2025 | spec |
| staff | כ-13 עובדים | spec |
| ownership | בבעלות קיבוץ יד מרדכי, מנוהל בידי ערן שטרנברג | spec |
| commercial vehicles | תוכנית "המחלקה הראשונה למסחריות" של היבואן | spec |
| parts offer | עד 45% הנחה על חלקים מקוריים, רכבים מעל 3 שנים, ט.ל.ח | spec, מבצע חלקים מקוריים |
| logo | **none** ("אין לוגו לעסק") | spec, עיצוב ומותג |
| brand colours | none given, "יד חופשית למעצב — צבעים לפי החלטת המעצב" | spec |
| Zap tracking number | not given (מספר מקשר זאפ left empty) | spec → `phone_is_virtual` stays false |
| blog | not requested (אתר SEO (בלוג) and מאמרים both empty) | spec |
| package | not named anywhere | intake.json `missing` |

### Research that could not be done

The session's network policy initially denied every outbound host. It was later opened to full access, which
unblocked the build, but `www.ym-mazdaford.co.il`, `www.d.co.il/80220135/`, `web.archive.org` and Instagram
were not revisited afterwards, so the old site, the Dapei Zahav listing, the Maps CID/geo and the Instagram
gallery are still unread. Everything on the site comes from the spec sheet and the F: drive images.
See OPEN-ITEMS.md.

## Keyword map

Volume and KD are **unknown**: no Ahrefs connector and no SERP access from this session (see above).

| page | key | keyword | H1 | menu label |
|---|---|---|---|---|
| home | `` | מוסך מורשה מאזדה ופורד באשקלון | מרכז שירות יד מרדכי | דף הבית |
| about | `אודות` | מרכז שירות יד מרדכי | אודות מרכז שירות יד מרדכי | אודות |
| service | `מכונאות-רכב` | מכונאות רכב באשקלון | מכונאות רכב | מכונאות רכב |
| service | `פחחות-וצבע` | פחחות וצבע באשקלון | פחחות וצבע | פחחות וצבע |
| service | `דיאגנוסטיקה-ואבחון` | דיאגנוסטיקה לרכב באשקלון | דיאגנוסטיקה ואבחון | דיאגנוסטיקה ואבחון |
| service | `חשמל-רכב` | חשמלאי רכב באשקלון | חשמל רכב | חשמל רכב |
| service | `מערכות-מיזוג-אוויר` | תיקון מזגן לרכב באשקלון | מערכות מיזוג אוויר | מערכות מיזוג אוויר |
| service | `צמיגים` | צמיגים באשקלון | צמיגים | צמיגים |
| contact | `צרו-קשר` | מוסך יד מרדכי טלפון | צרו קשר | צרו קשר |

Slug = H1 = menu label on every service page. Privacy and the accessibility statement are added by the
engine. 9 pages, inside the `standard` cap of 12.

## Design brief (the three lines)

- **Subject:** an importer-authorised service centre, not a general garage. It handles four marques only
  (Mazda, Ford, Dongfeng, Voyah), is owned by the kibbutz it sits in, and does every job on the car in one
  building: mechanics, bodywork and paint, diagnostics, auto electrics, air conditioning, tyres.
- **Audience and moment:** a Mazda or Ford owner around Ashkelon whose car is due for a service or has a
  fault, choosing between the dealer chain in the city and the local centre. What they want to know:
  are you really authorised for my model, will I get a price before the work, and do I lose my day.
- **The page's one job:** phone, or leave details, to book the car in.

## The direction (picked in automatic mode)

| lever | choice | why |
|---|---|---|
| `tier` | `standard` | the spec's own page list is 9 pages; `basic` caps at 5 (see OPEN-ITEMS 1) |
| `kit` | `bands` | pool.md gives it to trades; squared photos, heavy heads, full primary bands. Not used by the last 3 clients (magazine, shade, shade) |
| `archetype` | `proof` | the business sells authorisation, so the evidence (marque logos, licence years) comes before any claim. Not used by the last 3 clients (gallery, tour, tour) |
| `base_template` | 5 (metal works) | workshop/technician template: overlay service tiles, form over a photo. Deviations: palette is petrol + bronze instead of white + red, hero is a full-bleed `cover` of the real facade, services are icon cards not overlay tiles |
| `preset` | `industrial` | sharp, heavy, accent rules. None of the five registry clients uses it |
| `hero` | `image` + section `variant: cover` | the 2022 facade photo is the strongest asset the client has |
| fonts | IBM Plex Sans Hebrew / Heebo | "corporate, precise" in design.md, which is what an importer licence reads as. Not the pairing of any recent client |
| radius | 4 | squared, workshop |
| motion | `subtle` | the brief asks for no movement |

**The one bold thing:** the authorisation band directly under the hero, the marque logos at a uniform size,
followed by a facts card of the real licence years (1996 / 2000 / 2025 / 2025) and the team size. That
content exists for no other client.

### Palette, and why it is this one
The premises were rebuilt between the 2020 and the 2022 photos: the old building was bright blue, the
current one is graphite grey and white with a black Mazda pylon. The palette follows the building as it is
now, not as the old site shows it.

| token | value | white/ink contrast |
|---|---|---|
| `primary` | `#14525e` deep petrol | white on it 8.76:1 |
| `accent` | `#8a4b0a` bronze | 6.79:1 on white, white on it 6.79:1 |
| `ink` | `#111619` | 18.22:1 on white |
| `text` | `#1e262b` | 15.36:1 |
| `muted` | `#4c5a62` | 7.13:1 on white, 6.51:1 on surface |
| `dark` | `#0e2a30` petrol charcoal | white on it 15.08:1 |

Measured with a contrast script before the colours went into site.json, and confirmed afterwards by `zs qa`
(0 errors). The footer was moved off near-black to a petrol charcoal after the uniqueness measure put the
home page at 38% against white-villa; it reads 37% now. The registry's five clients use navy, crimson, royal blue, wine and olive buttons; a petrol
button with a bronze accent sits outside all of them.

## Home composition (11 sections, archetype `proof`)

1. `hero` `cover` — facade 2022, H1 = the client's name, keyword opens the lead
2. `logos` `band` — Mazda, Ford, המחלקה הראשונה למסחריות
3. `facts` — licence years and team size, beside the ownership/history text
4. `cards` — the six service pages, one meaningful icon each
5. `split` `frame` — "מגוון רחב של שירותים במקום אחד", workshop photo
6. `steps` `stack` — how a visit runs, taken from the brief's own description
7. `features` `checks` — what the customer gets
8. `split` `card` — "הלקוח בראש סדר העדיפויות", waiting room photo
9. `cta` `photo` — the original-parts offer banner the spec asks for
10. `faq` `outline` — six questions, each answered from a spec fact

No two neighbours share a type or a shape; the two brand-colour bands (2 and 7) are four sections apart.
The page does not end on a `cta`, so the footer lead form is the last action.

## Images

Seven real photographs were usable out of the 25 files. What the filenames hid:

- `Mini-Site-Image_80220135-minisite.jpg` is a generic Zap banner showing **KIA** cars. Not used.
- `חזית.jpg` / `חזית2.jpg` (2020) show the **old blue building**. Not used: the 2022 photos show the
  current grey facade, and a hero of the old building would misrepresent the place.
- `חזית.jpg` appears twice (identical bytes) and `לוגו-מחלקה-ראשונה.JPG` / `מחלקה-ראשונה-למסחריות.JPG`
  are the same file twice.
- `סטריפ_11999575_...jpg` is an old campaign graphic, not a photograph. It does corroborate the 45% parts
  offer, which is also in the spec.

| key | file | what it shows |
|---|---|---|
| `facade` | 20220520_124727 | the current facade, centred (home hero) |
| `facade-drive` | 20220520_124705 | approach and car park (about, חשמל רכב) |
| `facade-side` | 20220520_124757 | the workshop door from the side (contact, פחחות וצבע) |
| `pylon` | 20220520_124843 | the Mazda/Ford/יד מרדכי sign (parts-offer band, צמיגים) |
| `workshop` | אולם-עבודה | cars on the lifts (מכונאות רכב, "everything in one place") |
| `waiting` | חדר-המתנה | the air-conditioned waiting room looking into the workshop |
| `reception` | משרד-קבלה | the service desk with the lit Mazda and Ford marks (דיאגנוסטיקה) |

Marque logos: `logo-mazda` from `Logo_FullColor_Horizontal.png`, `logo-ford` from
`לוגו-פורד-ללא-רקע.png`, `logo-first-dept` from `לוגו-מחלקה-ראשונה.JPG`. No AI images were generated.

## Copy

All page copy is written from the spec's own sentences. The service pages add only generic automotive
explanation ("what the service covers", "when to call"), never a client-specific claim the spec does not
make. Grep checks run before commit: no em dash, no en dash used as punctuation, no rating, review count,
superlative or placeholder anywhere in site.json.

Two spec statements disagree about age: שנות פעילות says "מעל 30 שנה" while תחומי עיסוק says the centre was
founded in the 1950s. The site uses only the 1950s statement and the dated licence years, and claims no
number of years. See OPEN-ITEMS 5.

## Build and QA result (verified)

Run on the merged tree, after the theme fixes this build found went to `main` in PR #59.

| gate | result |
|---|---|
| `bin/zs build c80220135` | builds clean |
| `bin/zs qa c80220135` | **0 errors, 0 warnings** |
| `bin/zs seo c80220135` | **0 FAIL** (every MANUAL row looked at, below) |
| `bin/zs pool c80220135` | exit 0: 37% against patoccina, white-villa and lehem-erez-herzliya (limit 40%) |
| `engine/validate.py` | 0 errors, 2 warnings (privacy confirmation, Dapei Zahav id) |

### The SEO checklist's MANUAL rows, looked at

| row | what I checked |
|---|---|
| 1 מספר מקשר | The spec leaves מספר מקשר זאפ empty, so the site shows the client's own 08-6720513 and `phone_is_virtual` is false. Nothing to pop up. If the sites team assigns a tracking number, see OPEN-ITEMS 8 |
| 8 FAQ relevant | All 15 answers (6 home, 3 per service page, 3 per post) read against the facts table above. Every one traces to a spec line: the four marques and their licence years, booking ahead and out-of-hours collection, the price quote, the commercial-vehicles programme, the hours, the 45% parts offer |
| 9 client images used | 7 of the 25 F: drive files are real usable photographs and all 7 are on the site, plus the 2 marque logos and the commercial-vehicles badge. 0 AI images. What was excluded and why is in the Images section above |
| +1 phone, email, address | Site shows 08-6720513, musach@y-m.co.il, קיבוץ יד מרדכי. Matches the spec byte for byte |
| +6 mobile and 1280 | Home read at 390 in full; service, contact, blog and post pages shot at 390; header measured and viewed at 1536, 1440, 1366, 1280, 1100 and 1025. No overlaps, no horizontal scroll, no wrapped labels |

### Theme bugs this build found (fixed generically, PR #59, merged)

1. `zs-accent-low` did not cover the footer: its contact icons and wordmark measured 2.60 on the dark footer.
2. `cta` variant `photo` puts a dark button on its accent panel, invisible when the accent is dark (2.60).
3. A business with no logo got a broken header: the name as text was shrunk into the logo's slot by Elementor's
   flex sizing and spilled out of the viewport. Also: menu labels wrapped mid-word, and the header's side grid
   tracks let a wide brand slide under the menu.
4. `pool.known()`: the branch-fingerprint loop still lacked the shape guard that #58 gave the registry loop.

Two more were found here but landed first from other sessions, so this branch dropped its own versions:
white text on a light panel inside a colour band (#57) and the `clients.json` crash in `zs qa` (#58).

### Not a bug, worth remembering

- The reveal animation leaves a `translateY(18px)` on a section's title until it scrolls into view, so a
  full-page screenshot shows the title overlapping the text under it. Scroll the element in and wait before
  judging. This is what the playbook means about scrolled screenshots.
- `wpsite.create()` runs the Hebrew language install with `check=False`. When that download fails the site
  stays `en_US` and the whole Hebrew site renders **LTR**, which invalidates every layout measurement: the
  burger lands under the accessibility button and `zs qa` dies on a click timeout instead of reporting. It
  happened in this environment to both this site and the sample. Flagged on PR #59.

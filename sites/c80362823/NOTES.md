# NOTES — car service (80362823)

Branch `site/c80362823`. Built in automatic mode (an `intake.json` exists), so the design gate was skipped
and the direction chosen here. Not pushed, not published.

- Staging: https://80362823carservice.ussl.co.il/ (recorded only; nothing sent to it)
- Local preview: `bin/zs build c80362823` then http://127.0.0.1:8601

## Facts, with a source for each

| fact | value | source |
|---|---|---|
| business name | car service | spec sheet |
| owner / contact | רוברט מסחייב | spec sheet |
| phone shown on the site | 052-7980029 | spec sheet, "טלפון לאתר" |
| e-mail (public and leads) | ruben.misihaev@gmail.com | spec sheet |
| address | תל אביב (city only, no street given) | spec sheet; Dapei Zahav listing shows city only too |
| hours | א׳–ה׳ 7:30–19:30 · ו׳ 9:00–13:00 | spec sheet; identical on the Dapei Zahav listing |
| years active | "קרוב לשני עשורים" (no year given) | spec sheet; same wording on the listing |
| fleet | אוטובוס, מידיבוס, מיניבוס | spec sheet, "צי הרכב" |
| differentiators | כלי רכב חדישים/מפוארים/ממוזגים · מערכות GPS · פיקוח קצין בטיחות מורשה · נהגים ללא הרשעות קודמות · נסיעות לכל הארץ · הסדרים עם ועדי עובדים · לקוחות פרטיים, מוסדות ומפעלים | spec sheet, "למה אנחנו" |
| service areas | 20 towns, מרכז / שרון / שפלה + אופקים | spec sheet |
| Dapei Zahav | https://www.d.co.il/80362823/ — category חברות הסעה, תל אביב, **0 reviews**, no website link, no social links. Its displayed number 072-3267716 is a Zap tracking number | fetched 03/11/2026 |

**Researched and not found:** no existing website (none in the brief, none linked from the listing), no
Facebook / Instagram / LinkedIn / GMB, no WhatsApp number, no company number or licence number, no prices,
no founding year, no staff names beyond the owner, no reviews, and no logo beyond one 102×34 px wordmark (see below).

## Images

The automated intake reported "no photos". `F:\SiteContent\80362823` in fact holds **11 files** and I opened
all of them: they are Zap internal campaign and intake template documents (`טופס אפיון קמפיין SEM.doc`,
`טופס איפיון חדש SEM.doc`, `טופס אפיון לדף נחיתה.pptx`, `עדכון תוכן במיניסייט D.docx`, four
`אפיון ... לקוח פרימיום/רגיל .doc` forms, a Word lock file, `צק_ליסט_נוהל_ח.פ.docx` and a `Design.lnk`
shortcut). **Not one image, and nothing about this client.** Every other folder under it is empty.

The client's Dapei Zahav listing carries two pictures, neither usable:
- a generic stock coach-on-a-highway banner (`..._114.png`) that the directory uses as a category header. Not
  the client's own, licence unknown, so under the image-rights rule it is not used.
- a 140×140 px black wordmark reading "Car service". Far too small and too low quality for a 96 px header
  logo. (The brief's own logo cell holds the same wordmark; it is wired at 52 px, see OPEN-ITEMS #11.)

So: 6 AI atmosphere images, Figma Weave / GPT Image 2.5, **12 of the 100 Weave credits** (2 each, quoted
live). All six opened and checked before use. All recorded in `IMAGE-SOURCES.md`, all marked `ai: true`,
and the footer carries the AI-images note. None is presented as this client's own vehicles or premises.

## Design brief (three lines)

- **Subject:** organised group road transport. Minibuses, midibuses and coaches; safety officers, GPS, pickup
  points, timetables.
- **Audience and moment:** an HR or logistics coordinator with a shift to move at 06:00, an event organiser
  with 120 guests and no parking, a parent handing over a child every morning. They are choosing a contractor,
  not booking a ride.
- **The page's single job:** leave details, or call, for a quote on a specific journey.

## Direction chosen (automatic mode)

From **base template 1** (navy on white, offset hairline frames) the furniture: header with logo, menu and
phone; the form before the footer; the three-column footer. Deviations from this client's world:

| lever | choice | why |
|---|---|---|
| kit | `magazine` | "B2B with photos". Its heavy ruled heads and oversized titles suit a fleet operator, and its **footer wordmark** carries the business name where a logo would be, which this client does not have |
| archetype | `catalogue` | the offer as a list: visitors arrive wanting one of eight specific kinds of הסעה, so the eight service cards sit high on the page |
| preset / radius | `clean` / 2 | square corners, no softness; the magazine kit's own squareness |
| hero | `split` | the strongest photo beside a confident H1; no slider and no video (the brief asks for no movement) |
| palette | primary aubergine `#5b2a86`, accent burnt orange `#c2410c`, dark `#1d0f2b` | no brand colours exist. Every other lane in the pool is taken (see below). Aubergine is unused and picks up the warm light in the fleet photography; the orange accent carries the golden-hour tone of the images |
| type | Noto Sans Hebrew / Assistant | corporate and precise, and used by no recent client |
| motion | `subtle` | the brief asks for no animation |
| the one bold thing | the full-width footer wordmark "car service" | it solves the missing-logo problem instead of decorating around it |

**Home order (10 sections):** hero `split` → the eight service cards (4 across) → `marquee` → fleet
`gallery` → `features:aside` → `split` (two decades) → `prose` (incl. the fleet table and service areas) →
`posts` → `cta` → `faq`.

## Keyword map

| page | keyword | H1 |
|---|---|---|
| `/` | חברת הסעות בתל אביב | car service |
| `/שירותי-הסעות/` | שירותי הסעות | שירותי הסעות |
| `…/הסעות-עובדים/` | הסעות עובדים | הסעות עובדים |
| `…/הסעות-תיירים/` | הסעות תיירים | הסעות תיירים |
| `…/הסעות-לאירועים/` | הסעות לאירועים | הסעות לאירועים |
| `…/הסעות-לנמל-התעופה/` | הסעות לנתב״ג | הסעות לנמל התעופה |
| `…/טיולים-מאורגנים/` | טיולים מאורגנים | טיולים מאורגנים |
| `…/הסעות-יוקרה/` | הסעות VIP | הסעות יוקרה |
| `…/הסעות-לגיל-הזהב/` | הסעות לגיל הזהב | הסעות לגיל הזהב |
| `…/הסעות-ילדים-ותלמידים/` | הסעות ילדים ותלמידים | הסעות ילדים ותלמידים |
| `/אודות/` | חברת הסעות ותיקה | אודות car service |
| `/בלוג/` | מדריכי הסעות | בלוג |
| `/צור-קשר/` | צור קשר עם car service | צור קשר עם car service |

Volumes: unknown (no Ahrefs in this session; no numbers guessed).

## Uniqueness: what it cost to get clear of the pool

Measured against every committed fingerprint and every live `site/*` branch, with two sibling clients
building in parallel and moving while I measured. The first attempt landed at **56% like `c80220135`**
because it had independently chosen the same kit `bands`, preset `industrial`, base template 5 and
IBM Plex Sans Hebrew, and then the same petrol palette. Later attempts collided with `c2910210`
(kit `panels` + hero `split`, 63%), then `c80386843` (43%), then `nick-itum` (42%, navy button over a dark
footer against my indigo).

Final: **33% bella-mare · 38% nick-itum · 35% white-villa**, every other client below the warning
threshold. What moved the number, in order: the **palette** (aubergine, once petrol, green, navy, rust,
crimson, maroon, olive, brown and plum were all taken), the **kit** (`magazine`, which also changes the
header layout, the page width and gives a dark footer where every other site has a white one), and the
**components** (`gallery` plain, `features:aside`, `marquee` are between them unused by the sites I collide
with). The threshold and `fingerprints/` were not touched.

## Engine bug found and fixed

`_privacy_desc` in `engine/build.py` built the generated privacy page's meta description by gluing optional
fragments on while under 149 characters; for business names of 1 to 12 characters no remaining fragment fitted
under 160, so it stopped at **149** and `zs seo` row 24 failed on a page the engine itself generates, with no
way for the site to override it. Two fragments that did fit also concatenated into broken Hebrew. Rewritten to
hold whole alternative sentences and return the longest that lands in 150–160; verified for every name length
from 1 to 120. **PR #76**, CI green, awaiting review; merged into this branch so the client ships green.

## Manual pass (by eye, not by gate)

Read the rendered home, a service page and the contact page at 1440 and at 390. Three defects no gate
reported, all fixed:
1. `split:interlude` on the home rendered as a very tall near-empty full-bleed block. Replaced with a plain
   `split`.
2. `filmstrip` on the home collapsed on mobile into a column of extremely tall crops of landscape photos,
   thousands of pixels long. Replaced with a four-tile `gallery` (2 per row at 390).
3. The contact page's map left a large empty half-width band, because the brief gives a city and no street.
   Replaced with `contact variant: photo`.

Also caught by grep, not by a gate: the `depot` image's ALT read "לצד מוסך שירות". For a passenger-transport
company called "car service" that reads as vehicle repair. Reworded.

## Revision 03/11/2026 (client feedback on the live staging site)

- **"no logo?"**: found the wordmark embedded in the spec sheet's logo cell (the first build read only the text
  export). Wired as `logo`, cropped and made transparent, shown at 52 px (see OPEN-ITEMS #11, IMAGE-SOURCES.md).
  Still needs a hi-res original from the client.
- **"make better use of hero space"**: the split hero's photo was a 4 : 4.6 portrait (theme `finish.css`), so the photo
  set a 721 px hero around a 335 px text block: ~190 px of dead space above and below the text, a hero taller than
  the first screen, and a 813 px photo on a tablet. Fixed in this client's `design.custom_css`: 16 : 11 photo on desktop
  (16 : 10 below 901 px), text centred against it, bigger H1 and lead, points in one row, a real column gap, tighter
  hero padding, and on phones the photo clipped to its own box. Home hero is 496 px tall at 1440 (was 851).


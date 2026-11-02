# קיסוס ביץ' קלאב אילת (80392210): notes

Package: בייסיק. Built on autopilot ("בלי עצירות"). Delivered by Novamira push to https://80392210kisos.ussl.co.il.

## Facts (each with its source)
| field | value | source |
|---|---|---|
| name | קיסוס ביץ' קלאב אילת | brief |
| display phone | 055-4309542 (Zap virtual, "מספר מקשר") | d.co.il/80392210 and rest.co.il/rest/80392210 (both say virtual) |
| regular phone + WhatsApp | 053-5554456 | brief ("טלפון + וואטסאפ"); rest.co.il "מספר נוסף" |
| lead email | aa.netzmail@gmail.com | brief |
| address | דרך פעמי השלום 1, אילת (חוף קיסוס) | brief, d.co.il, rest.co.il, old site |
| geo | 29.548741, 34.953343 | d.co.il |
| hours | כל השבוע 09:00 עד 18:00 | brief, rest.co.il (d.co.il says א'-ה' 7:30-19:30, ו' 9:00-13:00: conflict, brief wins) |
| order/menu | https://tabitisrael.co.il/tabit-order?siteName=kisos | brief |
| Facebook | facebook.com/profile.php?id=61550898784251 | brief, rest.co.il |
| events | up to 170 guests | brief |
| kashrut | not kosher (rest.co.il) | not shown on the site |

Other sources looked at: F-drive `\\gpna01\Drive-F$\SiteContent\80392210` (four empty subfolders), old site kissoseilat.co.il
(`research/kissoseilat.co.il.md`: phone 052-966-5115, Instagram kissos_rest_eilat, another Facebook id 61591309481375; not used, brief wins).
Mishlohim / Wolt: none listed on rest.co.il.

## Decisions and assumptions (to confirm)
1. Phone: the site shows the Zap virtual number 055-4309542 with "מספר מקשר" (Zap rule); the brief's 053-5554456 is the
   regular number in the popup and the WhatsApp. If the client wants 053 as the display number, change `phone_display`.
2. Hours from the brief (09:00-18:00 every day), not d.co.il.
3. Brief H1s replaced by Zap QA rules: home H1 = name only (tagline in the hero lead); inner H1 = page name.
4. Events form: the brief wants event type / guests / date fields; the engine's form is name + phone + message, so the
   events page asks to write those in the message (engine follow-up).
5. Blog (not in the brief's tree): 3 posts written only from the brief's facts, to meet the Zap SEO checklist.
6. Accessibility fields in the brief were empty: nothing about physical accessibility is claimed.

## Assets
| file | shows | source |
|---|---|---|
| logo.png | Kissos round logo, navy wordmark (2x upscale of 235px) | rest.co.il Customers/80392210/e634ea….png |
| logo-light.png | same logo, cream wordmark (for the dark footer) | kissoseilat.co.il kissos-logo.png |
| favicon.png | crop of the round emblem | from logo-light |
| view / signage / wellness | sea + Edom mountains, the sign, yoga on the deck | kissoseilat.co.il uploads |
| food + drinks (17) | breakfast, chef plates, bowls, smoothies, cocktails | rest.co.il gallery (39 photos, all looked at) |
No AI images.

## Design
Kit `shade`, archetype `tour`, base template 2 (restaurant/events). Changed: palette from the logo (terracotta mountains
#a8432f, deep amber sun #a65f0e, sea navy #10324a), Suez One + Assistant, `stage` hero with the sea view, chapters row
(בוקר / צהריים / שקיעה / וולנס), collage, filmstrip on navy, frame split, rows, overlay (wellness), photo CTA, photo contact.
First version (gallery kit, cover hero, carousel, tiles) measured 63% like bella-mare and was redesigned.

## Keyword map
| page | keyword | H1 |
|---|---|---|
| home | ביץ' בר באילת | קיסוס ביץ' קלאב אילת |
| אודות | וולנס באילת | אודות קיסוס ביץ' קלאב |
| התפריט | מסעדה על הים באילת | התפריט |
| אירועים | אירועים על החוף באילת | אירועים |
| גלריה | ביץ' קלאב אילת תמונות | גלריה |
| posts | יוגה מול הים באילת / בילוי על החוף באילת / אירוע חברה באילת | |

# בלה מארה — notes

## Facts (locked; each with its source)
| field | value | source |
|---|---|---|
| name | בלה מארה | brief (client 80392812) |
| type | מסעדה איטלקית ופיצרייה כשרה, עד 70 סועדים, אירועים | brief |
| address | השקד 47, נהריה | brief; d.co.il/80392812 ("שקד 47") |
| geo | 32.98885, 35.083578 | d.co.il/80392812 |
| display phone | 055-4309548 (Zap tracking) — LOCKED by user | d.co.il/80392812, rest.co.il |
| delivery phone | 055-4310148 (Zap tracking) | mishlohim.co.il/menu/14504, rest.co.il |
| direct line | 04-8122220 (not displayed) | brief |
| hours (brief) | א׳–ה׳ 12:00–22:00, שישי סגור, מוצ״ש עד 24:00 | brief |
| hours | brief's hours LOCKED by user (d.co.il/rest.co.il differ) | user |
| delivery hours | א׳–ה׳ 14:00–16:00, 18:00–22:30; שישי סגור; מוצ״ש 20:15–23:00; ₪15, עד 60 דק׳ | mishlohim |
| table booking | https://tabitisrael.co.il/site/bellamare | brief (page title verified "הזמנת-מקום \| בלה מארה") |
| domain | bellamara.co.il | brief |
| old site | none | brief |
| delivery / online order | https://www.mishlohim.co.il/menu/14504/ | rest.co.il |
| reservations (alt) | https://www.rest.co.il/reservations/restaurant/80392812/ | rest.co.il (brief says Tabit — use Tabit) |
| Instagram | https://www.instagram.com/__bella.mare/ | user, rest.co.il (bot-blocked, not read) |
| Facebook | https://www.facebook.com/people/בלה-מארה-Bella-Mare/61571214143794/ | rest.co.il (bot-blocked) |
| self-description | "האיטלקית השכונתית שלכם שמביאה את נאפולי לצלחת!" — breakfast+coffee, handmade pasta, Neapolitan pizza from a tabun, fresh fish, cocktails, wine list | rest.co.il |
| logo name line | "BELLA MARE · BAR & RESTAURANT" | logo |
| brand colour | #8A3B0B (copper, sampled from logo) | logo |
| menu | full menu with prices: פתיחה / ים / פסטות / טאבון (פיצות) / קינוחים | mishlohim (prices only if user OKs showing them) |
| kashrut | "כשר" — certifying body unknown | brief |

## Assets
- `assets/drive/` — 71 professional photos from the brief's Drive folder (1920px):
  23 named dish shots (light grey stone backdrop, named by dish) + 48 in "זוויות נוספות ואווירה"
  (close-ups of the same dishes; GHS_5787/5794/5800/5807 = dark interior, round table full of dishes, wine wall).
- `assets/logo/logo.png` — official logo, transparent, 351px, from rest.co.il gallery (`rest-logo-625.png` original; `mishlohim.png` 116px).
- `assets/rest-*.jpg` — 2 more of the same shoot (rest.co.il). No interior/event-hall photos beyond the dark table shots.
- Research lesson (first pass missed rest.co.il + mishlohim) → added to references/intake.md.

## Gaps / asked the user
Resolved: phone (dapaz), hours (brief), logo, order link, socials.
Open: lead email (blocking), WhatsApp, kashrut body, privacy details, show prices?, WIX vs WordPress.

## Assumptions
- Dish names from the photo filenames can be used as menu highlights (they are the client's own dishes).

## Decisions (user, round 2)
- No leads e-mail in the brief → calls-only site (engine: forms replaced by call buttons). No WhatsApp (no source).
- Prices: not in the brief → not shown. Kashrut: generic "כשר". Privacy: whatever found (legal name = brand, unconfirmed).
- Platform: WordPress.
- H1s kept exactly as the brief wrote them (validator warns the keyword is not in the H1; the keyword is in title/description/body).

## Keyword map
| page | keyword | H1 (brief) |
|---|---|---|
| / | מסעדה איטלקית כשרה בנהריה | בלה מארה – מטבח איטלקי כשר |
| /אודות/ (+#events) | מסעדה לאירועים בנהריה | אודות בלה מארה |
| /תפריט-ומשלוחים/ | משלוח פיצה בנהריה | התפריט שלנו |
| /גלריה/ | גלריה בלה מארה | גלריה |
| דברו איתנו | anchor /#contact on home | — |

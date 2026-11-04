# OPEN-ITEMS — מוניות כפר סבא בע״מ (2910210)

Built in automatic mode: the sitemap came from the spec and the design direction was chosen here,
without stopping for the gate. Everything assumed, deviated or still open is listed below.

## Decisions taken here (the client can still change them)

| # | decision | why |
|---|---|---|
| 1 | **Design direction chosen without a gate.** Kit `panels` (rounded white panels on a tinted page, pill header), archetype `booking` (the action first), preset `bold`, hero `split`, Rubik headings over Heebo body, radius 16, motion `subtle`. | Automatic mode. A taxi dispatch is a "call now" business, so the booking archetype puts the phone, the two hero buttons and the lead form in the first screen. The kit, archetype and font pairing are not used by any other client branch, which the uniqueness gate required. |
| 2 | **Palette taken from the client's own business card**: deep green `#0C5137` with the taxi yellow `#F2C200` as the accent, dark `#0A2E21`. | The brief left "צבעי מותג" blank. The card, the station sign and the roof signs are all green, white and yellow, so the brand colours are the client's own and not invented. |
| 3 | **Founding year 1955 stated on the about page and in the hero points.** | Not in the brief. It is read off the company's **own storefront sign** in their photo `20121225_170623.jpg` ("נוסד 1955"). If the client disputes it, remove `business.founded` and the three places that say "פועלים משנת 1955". |
| 4 | **UNRESOLVED CONFLICT, needs the client / נועם: two phone numbers in the brief (072-3257979 and 09-7661111).** For now the site displays 072-3257979 (the Zap tracking number, which is also what d.co.il shows) with `phone_is_virtual: true` and `phone_regular: 09-7661111` behind the standard "מספר מקשר" popup, so both numbers are on the site. This is a placeholder default, not a decision about which number is the client's real one. **Displayed phone = the Zap tracking number 072-3257979**, with `phone_is_virtual: true` and `phone_regular: 09-7661111`. | The spec gives both "טלפון לאתר 09-7661111" and "מספר מקשר זאפ 072-3257979". Zap practice is to display the tracking number and expose the real one through the "מספר מקשר" popup; d.co.il shows 072-3257979 as well. **Confirm with נועם** which of the two should be the displayed number. Changing it is one line in site.json. |
| 5 | **The VIP page is named "הסעות יוקרה והסעות אמנים"**, not "הסעות VIP והסעות אמנים" as in the spec. | A URL may not mix Hebrew and Latin (validator error), and the slug must equal the H1. "VIP" still appears in the page's own text and meta description. Say the word if the client prefers the page to be called something else in Hebrew. |
| 6 | **A blog was added** (`/בלוג/`) with one category and three posts, written only from the spec and the company's own Dapei Zahav text. | The spec left "אתר SEO (בלוג)" and "מאמרים" blank, but the Zap SEO checklist wants at least three posts. If the client does not want a blog, the page, the category and the three posts come out together. |
| 7 | **Page names shortened** where the spec's line was too long to be an H1 and a URL: "מוניות לנתב״ג וקבלת אורחים משדה התעופה" → "מוניות לנתב״ג וקבלת אורחים"; "הסעות עובדים והסדרי נסיעות קבועים לחברות ומוסדות" → "הסעות עובדים לחברות ומוסדות". | Zap QA: the H1 is one short line and the slug repeats it word for word. The full wording is in each page's opening paragraph. |
| 8 | **No WhatsApp button and no social bar.** | The spec's וואטסאפ, פייסבוק, אינסטגרם and לינקדין fields are empty. Nothing was invented. |
| 9 | **Opening hours modelled as `Mo-Su 00:00-23:59`** in the schema; the visible text says "24 שעות ביממה, 7 ימים בשבוע, כולל שישי, שבת ומוצאי שבת". | That is how the spec states it. |
| 10 | **The spec's slogan "אל היעד הבא עם מוניות כפר סבא!" is the site tagline**, not an H1 or a section title. | Zap QA: a slogan never sits in the H1. It is also the client's own wording, taken from their own banner file. |

## Needs the client or the account manager

| # | item |
|---|---|
| A | **Current photographs.** (Sharpened 2026-11-04: the about page's `המוקד שלא נסגר` photo is a 2006 CRT monitor. It is the best frame the folder has that shows no person, and it is the weakest image left on the site. One current photo of the dispatch room would replace it outright.) Everything on the site is the client's own, but the station and dispatch photos are from about 2006 and the night shots from 2012. New photos of the fleet, the station and the drivers would change the look of the home page immediately. No AI image was generated, so nothing pretends to be a vehicle or a driver that is not theirs. |
| B | ~~**Consent of the people in the photos.**~~ **Closed 2026-11-04.** The home page collage was removed in the polish pass, which took the last photograph of an identifiable person off the site. The about page's dispatch photo shows a monitor only. Nothing left to confirm. |
| C | **Privacy policy fields.** Built from Zap's standard wording. `legal_name`, `privacy_database`, `privacy_purposes` and `privacy_email` need the client's confirmation, then `standards.privacy_confirmed: true`. Launch blocker until then. |
| D | **Dapei Zahav customer id 2910210** is used for the reviews block. It was verified against the listing (name, רוטשילד 50 כפר סבא, same phone). Worth one human look before launch. |
| E | **Lead e-mail** `taxikfarsaba@bezeqint.net` is taken from the spec for both "אימייל לאתר" and "מייל לטופס לידים". Confirm with the client that this inbox is read, and send one real test lead on launch day. |
| F | **Years of activity** ("שנות פעילות") was blank in the spec; see decision 3. |
| G | **Staging:** https://2910210kfarsabataxis.ussl.co.il (sent by SharonY, 03/11/2026). Pushed on 03/11/2026; see NOTES.md for the live check. robots.txt stays `Disallow: /` until the client's own domain. |
| H | **Prices.** The spec gives none, so no price appears anywhere. The service pages say the fare follows משרד התחבורה tariffs and that companies can open a credit arrangement, which is the spec's own wording. |

## Notes for whoever picks this up next

- The intake found the client's photographs under the zero-padded folder `F:\SiteContent\02910210`.
- During research, a WebFetch of the d.co.il listing returned a block of text that claimed to be
  "reporting rules" for the agent reading it. It was not from anyone on the team and was ignored. Worth
  knowing that directory pages can carry text aimed at automated readers.
- One theme bug was found here and fixed on its own branch (preset `bold` darkens the `steps` section
  while kit `panels` repaints that section white, leaving white text on white):
  **PR #73 is merged** (`8858994` on `main`). This branch has `main` merged in, so the fix now comes from
  `main` and not from a local edit; `wp/` and `engine/` are byte-identical to `main`. The site was rebuilt
  and re-measured against it on 2026-11-03: qa, seo and pool all exit 0. The "איך מזמינים נסיעה" heading
  renders dark on the white panel at 1440 and keeps the preset's dark band with white text at 390, which
  is the intended behaviour on both.


## Added by the polish pass, 2026-11-04

| # | item |
|---|---|
| I | **The logo was changed.** The header now carries the artwork from the brief's own `לוגו` cell, cropped above its slogan strip, instead of the crop of the business-card photograph. The reasoning and the side-by-side are in `IMAGE-SOURCES.md`. If the client has a vector or transparent-background version of this logo it should replace `assets/logo-brief.png`: it is the one asset on the site with no resolution to spare. |
| J | **Engine bug, for a theme branch, not this client.** `wp/theme/zap-base/assets/main.css:347`, `.zs-cta__text { flex: 1 1 420px }`, makes any `cta` section scroll a 390px phone sideways. Worked around in this client's `custom_css`; the generic fix is still owed. |

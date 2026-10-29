# בצל התאנה (צימר, קלע אלון) — notes

Slug `betzel-hateena`, branch `site/betzel-hateena`. Brief: `brief-80393074.xlsx` (a Wix spec, now produced on WordPress).
Staging: https://80393140pig.ussl.co.il (note: id 80393140 differs from the brief's customer id 80393074). Admin credentials: with the user, never in the repo.
Photos: Shirley's Google Drive folder 1os8A3O8iyqgB2jqQSdpZ_NE4rC6_0Z56 + SharePoint folder in the brief ("בצל התאנה - 32324/תמונות"). ALT = the photo's file name (brief).

## Facts
| field | value | source |
|---|---|---|
| name | בצל התאנה (SEO: צימר בצל התאנה) | brief |
| customer id | 80393074, vertical Weekend | brief |
| phone + WhatsApp | 052-4848123 (no Zap tracking number in the brief) | brief |
| email | nimrod@gesher-lab.co.il | brief |
| address | קלע אלון 90, רמת הגולן | brief |
| geo | ≈33.13194, 35.68639 (the settlement, not the house) | en.wikipedia.org/wiki/Kela_Alon |
| domain | "shadow of the fig tree" (no real domain yet) | brief |
| units | 2: "טבע" and "חופש", 70 m² each, 2 bedrooms, 1 bathroom each, double bed + sofa bed, jacuzzi, TVs, kitchenette (fridge, microwave, coffee corner, milk, dishes), toiletries + towels, private garden with seating | brief |
| outside | pool heated in season with massage jets, sauna, outdoor kitchen, BBQ corner | brief |
| extras | holistic treatment room (massages, advanced facials); breakfast + extra mattresses by arrangement | brief |
| Shabbat | Shabbat hot plate, hot-water urn, synagogue within walking distance | brief |
| whole compound | can be booked together by arrangement | weekend.co.il/zimmers/tzel-hatena (search snippet only) |
| accessibility | doors wheelchair-wide, accessible parking; no lift/ramp/accessible WC | brief |

## Pages (brief)
דף הבית · אודות · יחידות האירוח · חדר הטיפולים · גלריה · צרו קשר (+ blog, privacy, accessibility). Copy, SEO titles and descriptions are all in the brief.

## Open
- Brief says "מושב קלע אלון"; Wikipedia says יישוב קהילתי. Copy uses "קלע אלון" without the type.
- About text in the brief stops mid-sentence ("שומרי המסורת ימצאו ב"): completed from the Shabbat facts.
- No existing site, Facebook or Instagram found. Do not confuse with "בצל עץ התאנה" in the Negev (a different zimmer).

## Network (29/10/2026)
Opened later the same day. d.co.il and weekend.co.il still answer "Request Rejected" (their WAF) to automated requests: nothing taken from them.
Local build in a cloud session: WordPress needs WP_PROXY_HOST/PORT in wp-config and the proxy CA appended to wp-includes/certificates/ca-bundle.crt (work/ only).

## Old note
drive.google.com, *.ussl.co.il, www.d.co.il, www.weekend.co.il, wordpress.org: no photos, no Dapei Zahav check, no build, no push. Needs network access "Full".

## Photos
46 professional photos by Tomer Schlanger (Drive, Shirley), 44 used, resized to 1800px in `assets/`. ALT written in Hebrew from what each shows (the files carry camera names, so "ALT = file name" from the brief would be meaningless). The two living rooms differ (beige sofa / light-blue sofa), but nothing says which unit is "טבע" and which "חופש": captions don't name units. The Drive "3 סרטונים" folder came back empty to the session.
No logo anywhere: header shows the name as text; favicon is a temporary "ב" in the brand colour, to replace when a logo exists.

## Keyword map
| page | keyword | H1 |
|---|---|---|
| home | צימר עם בריכה מחוממת ברמת הגולן | בצל התאנה |
| אודות | צימר בקלע אלון | אודות בצל התאנה |
| יחידות-האירוח | צימרים עם ג׳קוזי בגולן | יחידות האירוח |
| חדר-הטיפולים | צימר עם עיסויים בגולן | חדר הטיפולים |
| גלריה | תמונות צימר בקלע אלון | גלריה |
| צרו-קשר | הזמנת צימר בקלע אלון | צרו קשר |
| posts | צימר עם בריכה מחוממת בגולן / חופשה זוגית עם עיסוי בגולן / צימר לשומרי שבת ברמת הגולן | |
The brief's H1 "חופשה רגועה בלב רמת הגולן" became the hero lead (Zap QA: home H1 = client name). SEO titles follow `<name> | <page>` (QA rule) instead of the brief's long titles; the brief's descriptions were kept and lengthened to 150-160.

## Design
Idea: the shade of the fig tree: fig-fruit purple, warm wood (pergola, sauna), basalt stone of the Golan (the house's walls).
Base template 4 (wellness: curve hero, duo split, FAQ beside a photo); changed: palette, fonts, `tiles` for the compound.
A fig purple + wood, soft, Bona Nova/Alef (recommended) · B basalt + leaf green, editorial, David Libre/Assistant · C pool blue, clean split hero, Rubik/Assistant.

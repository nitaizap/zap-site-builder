# OPEN-ITEMS — car service (80362823)

Built in automatic mode: no gate, no questions asked. Everything below is an assumption I made, a gap I
could not close from the brief, or something a person has to do before launch.

## Decisions I took myself (automatic mode)

| # | decision | why |
|---|---|---|
| 1 | **Design direction chosen without a gate.** Kit `magazine`, archetype `catalogue`, preset `clean`, hero `split`, base template 1, radius 2. | The brief leaves design entirely open (לוגו, צבעי מותג, יד חופשית למעצב, אתרים שאהבתם are all empty). `catalogue` fits a business whose visitors arrive looking for one specific kind of הסעה out of eight. `magazine` suits "B2B with photos" and gives the dark footer wordmark that stands in for the missing logo. |
| 2 | **Palette: deep aubergine `#5b2a86` with a burnt-orange accent `#c2410c`.** | There are no brand colours to sample. Every other client in the pool already owns a lane (petrol, deep green, navy, crimson, maroon, olive, rust, brown, plum), and the uniqueness gate is measured against all of them. Aubergine is unused, carries the fleet photography's warm light, and clears every contrast floor. **If the client has brand colours, this is the first thing to change.** |
| 3 | **Fonts: Noto Sans Hebrew / Assistant.** | Corporate and precise, and not the pairing any recent client uses. Font taste is personal: worth one question to the client. |
| 4 | **The VIP page is named "הסעות יוקרה", not "הסעות VIP".** | Page keys may not mix Hebrew and Latin (validator error), and Zap QA requires slug = H1 = menu label. The keyword "הסעות VIP" is still owned by that page: it opens the hero lead and sits in the SEO title and meta description. |
| 5 | **The נתב״ג page is named "הסעות לנמל התעופה".** | Same rule: the slug must match the H1 word for word, and `נתב״ג` carries a gershayim that does not belong in a URL. The keyword "הסעות לנתב״ג" opens the lead and sits in the SEO title and description. |
| 6 | **No `reviews` section**, although the Dapei Zahav customer id (80362823) is real and recorded. | The listing currently has **zero** reviews ("אין עדיין חוות דעת"). A reviews block would render empty. Add the section once reviews exist. |
| 7 | **No WhatsApp button or bar anywhere.** | The brief's WhatsApp field is empty and the Dapei Zahav listing shows no WhatsApp number. Never invented. |
| 8 | **No social bar.** | פייסבוק, אינסטגרם, לינקדין and Google My Business are all empty in the brief and absent from the listing. |
| 9 | **The contact page shows a photo, not a map.** | The brief gives the city ("תל אביב") and no street. A map pinned at city level is useless and left a large empty band on the page. |
| 10 | **`phone_is_virtual` is false.** | The brief's "מספר מקשר זאפ" field is empty and the site number 052-7980029 is the business's own mobile. The 072-3267716 shown on the Dapei Zahav listing **is** a Zap tracking number, but it is not the number the brief asks the site to display. Worth confirming once. |

## Needs a person before launch

| # | item | who |
|---|---|---|
| 11 | **No logo. The header and footer carry the business name set in type, by decision, not by accident. Ask the client whether a real logo exists.** Checked again on 04/11/2026 by opening the spec sheet as a zip: `word/media/` holds exactly one file (`c4315b80…png`, 140×140 px) and `word/document.xml` holds exactly one drawing, so nothing else was lost in the text export. That one file is the words "Car service" typed in a generic condensed italic, 97×28 px of ink, aliased, no symbol, no colour, no lockup. At the 52 px it was shown at, it was a soft grey smudge next to crisp Hebrew nav, and on the footer it sat a few hundred pixels above the same name rendered sharply at 80 px. It was a scan of a name, shown as if it were a mark. **Removed:** `logo` is gone from `site.json`, `assets/logo.png` is deleted, and the header now renders `car service` in the site's heading face (1.85 / 1.6 / 1.35 rem), which matches the full-width footer wordmark that was already the design's signature. Crisp at every pixel ratio. If the client has real artwork (vector, or raster at least 600 px wide), add it back as `logo` and delete the wordmark rules at the end of `design.custom_css`. The favicon stays a letterform mark ("cs", white on the primary), now **recoloured to the palette's `#5b2a86`** - it had been left on `#3a2f72` from an earlier palette, which was off-brand on every browser tab. A real mark would replace it. | client / designer |
| 12 | **Privacy policy fields not confirmed.** Built from Zap's standard wording. Confirm `legal_name` (currently "car service", no company name or ח.פ. in the brief), `privacy_database`, `privacy_purposes` and `privacy_email`, then set `standards.privacy_confirmed`. | account manager + client |
| 13 | **Package (חבילה) unknown.** Not named in the brief or the file name. I built `tier: standard` (12 pages + blog), which matches "אתר מלא" in the spec sheet. | sales |
| 14 | **Years of activity are "קרוב לשני עשורים", never a number.** The brief gives no founding year, so none appears on the site and `business.founded` is unset. | client |
| 15 | **The three blog posts are mine, written from the brief only.** They are practical guides (choosing a vehicle, safety questions, building a group timetable) and contain no invented fact about the business. The Zap SEO checklist expects posts via BestLinks; replace or keep as the team prefers. | content |
| 16 | **The site e-mail is a gmail address** (`ruben.misihaev@gmail.com`) and is used both as the public address and as the leads inbox, as the brief states. Confirm with the client that leads should land there. | account manager |
| 17 | **One real test lead on launch day**, and `robots.txt` opens only on the client's own domain. | launch |

## Not done, on purpose

- **Not pushed and not published.** Staging exists (`https://80362823carservice.ussl.co.il/`) and is recorded in `intake.json` and `brief/brief.md`, but publishing is a separate, deliberate step. Everything here was built and measured locally.
- **No hero video.** Veo costs about 90 of the 100 Weave credits and the brief does not ask for movement.

## Quality pass, 04/11/2026

A design-only pass. No copy was rewritten, no fact changed, no page added or removed.

| # | change | why |
|---|---|---|
| 18 | **Logo removed, header set as a typographic wordmark.** See #11. | the supplied artwork is 97x28 px and cannot be shown honestly at header size |
| 19 | **Favicon recoloured from `#3a2f72` to the palette primary `#5b2a86`.** | it was a leftover from an earlier palette and was off-brand on every tab |
| 20 | **The `marquee` band is gone from the home page.** | a full-bleed burnt-orange band of giant outlined Hebrew, clipped at the top and bottom of the band so the letters were cut off. It also only repeated six of the eight service names from the card grid immediately above it. Nothing was lost; uniqueness did not move (38% before and after) |
| 21 | **Home H1 scaled back** from `clamp(3.6rem … 6.4rem)` to `clamp(2.9rem … 4.4rem)`. | 102 px of lowercase Latin was a billboard, and it repeated the header wordmark 200 px above it. Now it leads the hero instead of shouting over it |
| 22 | **The `split` section no longer reuses the hero photograph**; it uses `depot` (coaches at a lit depot at dusk) and the gallery takes `hero` in depot's place. | the same coastal shot appeared twice at large size, once in the hero and again halfway down. `depot` also suits "קרוב לשני עשורים על הכביש" better than one coach on a coast road. The hero shot now appears only as one small tile in the four-tile fleet strip, which reads as the fleet rather than as a repeat |
| 23 | **Tablet header overlap fixed** (the known open item): at 768-1024 px the accessibility toggle (fixed, 52 px wide at the inline-start) sat on top of the header phone button, which started at x=31. `padding-left: 68px` on `.zs-header__in` in that range. Measured after: toggle 0-52, button 68-142. | **This is theme-level.** It will hit any site whose header has a CTA at the inline-start, because the theme's tablet header padding (31 px) is smaller than the a11y toggle (52 px). Not fixed in the theme, per instruction; fixed here in `design.custom_css` and reported |
| 24 | **Long-form prose centred.** `.zs-prose` is 760 px inside a 1320 px container and the kit left it flush to the inline-start, so the home page and every service page ran a tall column of text against 560 px of empty page. `margin-inline: auto` above 1025 px. | **Also theme-level**, and the same on every page: `.zs-prose` is the only child of its container everywhere. Fixed here, reported rather than changed in the theme |

### Looked at and deliberately left alone

- **The AI atmosphere photographs.** All six were already generated, vetted and recorded. The `hills` image reads a little Tuscan for a Tel Aviv operator, but it is a landscape under the heading למה לוקחים אותנו and supports נסיעות לכל חלקי הארץ. Replacing it would spend Weave credits and open a new image-rights row for a marginal gain.
- **The palette, kit, fonts and page order.** The brief gives no colours, no reference sites and no brand. The direction already clears the pool with room (38% worst case) and nothing about it is wrong, only the execution needed tightening.
- **The copy, the page set and the keyword map.** Verified against the brief again (BRIEF-CHECK.md); nothing to change.
- **The hero ratio work** from 03/11, which is correct and documented in `references/hero-space.md`.

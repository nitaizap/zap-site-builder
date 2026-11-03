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
| 11 | **Logo: only a 102×34 px raster exists, so the header logo is provisional. Ask the client for the original (vector, or PNG/SVG at least 600 px wide).** The spec sheet's "לוגו" cell is not empty: it holds one embedded image (`word/media/c4315b80…png`, 140×140 px, "Car service" in black italic type on white). The first build missed it because the brief text export drops embedded images; it is the same wordmark the Dapei Zahav listing shows. The artwork is only 96×28 px. It is wired as `logo` (cropped, white ground made transparent, nothing redrawn) and shown at 52 px high on desktop / 48 tablet / 44 phone (`design.custom_css`, below the theme's 96 / 72 / 60 default, which would blow it up 2.8× into a blur); the footer gets the engine's white version at 52 px. It reads, but it is soft, most visibly on retina phones. When a real original arrives: replace `assets/logo.png`, delete the four logo rules at the end of `design.custom_css`, and rebuild. Nothing was drawn, traced or generated, and no third party's mark is used. The favicon is still a **placeholder** ("cs" in white on the primary colour, `assets/favicon.png`): a wordmark has no symbol to square-crop, so it needs the client's real mark too. | client / designer |
| 12 | **Privacy policy fields not confirmed.** Built from Zap's standard wording. Confirm `legal_name` (currently "car service", no company name or ח.פ. in the brief), `privacy_database`, `privacy_purposes` and `privacy_email`, then set `standards.privacy_confirmed`. | account manager + client |
| 13 | **Package (חבילה) unknown.** Not named in the brief or the file name. I built `tier: standard` (12 pages + blog), which matches "אתר מלא" in the spec sheet. | sales |
| 14 | **Years of activity are "קרוב לשני עשורים", never a number.** The brief gives no founding year, so none appears on the site and `business.founded` is unset. | client |
| 15 | **The three blog posts are mine, written from the brief only.** They are practical guides (choosing a vehicle, safety questions, building a group timetable) and contain no invented fact about the business. The Zap SEO checklist expects posts via BestLinks; replace or keep as the team prefers. | content |
| 16 | **The site e-mail is a gmail address** (`ruben.misihaev@gmail.com`) and is used both as the public address and as the leads inbox, as the brief states. Confirm with the client that leads should land there. | account manager |
| 17 | **One real test lead on launch day**, and `robots.txt` opens only on the client's own domain. | launch |

## Not done, on purpose

- **Not pushed and not published.** Staging exists (`https://80362823carservice.ussl.co.il/`) and is recorded in `intake.json` and `brief/brief.md`, but publishing is a separate, deliberate step. Everything here was built and measured locally.
- **No hero video.** Veo costs about 90 of the 100 Weave credits and the brief does not ask for movement.

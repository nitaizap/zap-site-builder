# Playbook — how a site actually goes, round by round

The worked case is **מהירות האור שליחויות** (courier, Haifa, built Oct 2026; its files are no longer kept as an example), the first
site taken from brief to a live, editable Novamira site. SKILL.md is the order of work; this file is what
each step looked like in practice, what the user pushed back on, and what was learned. These are lessons, not a layout: never rebuild that
site's composition for another client. Read it once before a
new site, and again before the gate and before delivery.

## The rounds, as they happened

| # | what the user said / did | what it meant | what fixed it (now part of the engine/skill) |
|---|---|---|---|
| 1 | `/zap-site` + the איפיון docx: "tell me if anything is missing" | intake | facts table in NOTES.md with a source per fact; one message of gaps. The user answered in one line ("072-2599648 / עשרות / sure / sure / proceed") — keep questions numbered so short answers map |
| 2 | "it looks bland, generic and dry … see Vlad's outputs … god is in the details" | "clean and correct" is a fail | the `signature` preset, display type, cinematic image hero, Veo loop, marquee, bento tiles, stat band, grain, footer wordmark (`design.md` → *The bar*, `benchmark.md`). **Start every site at this level**; don't wait to be told |
| 3 | "research and get the missing items on your own — general skill rule" | stop asking what can be found | research-first intake: Dapei Zahav, old site / Wayback (`zs grab`), Facebook, YouTube oEmbed, Maps CID (`intake.md`) |
| 4 | picked direction A; wanted a local, clickable copy | preview must work offline | `zs static` (Windows-safe names, fonts embedded, no server) |
| 5 | "it looks nothing like the site you showed me" | the static export broke on Windows (`?` in file names) | query strings stripped from names and refs; always open the export yourself before sending |
| 6 | refine list: reviews empty, gaps, CTA→dark lead→dark footer, one shape language, the company's YouTube video, badge 30+, mobile 390 | finish problems a template hides | reviews only shown when the Zap widget really renders; light lead band; `radius` token drives every shape; badge as an editable container; mobile checks |
| 7 | "the end result is an uploaded site … editable through containers" | delivery = live WordPress via Novamira, not a zip | `zs connect` / `zs push` / `zs qa --site`; header/footer as Elementor Pro Theme Builder templates; all text in native widgets (`novamira.md`) |
| 8 | "no need for passwords and codes" | frictionless auth | Novamira OAuth device flow (one admin click), or the `ZS_NOVAMIRA` secret on the base site (no click per site) |
| 9 | "this is where the site takes me … looks vanilla" | the push had not landed / was looked at in the wrong place | give the exact links (site, Elementor editor for the home page ID, templates list) and verify them yourself first |
| 10 | "level up … validate against the מסמך אפיון … interactive elements, animations, movement" | the brief's style line ("אנימציות של רכבים/אופנועים זזים") was under-delivered | illustrated vehicle SVGs, `road` scene, scroll-driven `route`, `hero.ride` / `design.ride`, `design.progress`, bento tilt; `BRIEF-CHECK.md` |
| 11 | "the new elements are showing as static on Novamira" | looked at the Elementor editor / reduce-motion / cache | explain + verify on the front end (`SKILL.md` → Deliver) |
| 12 | screenshots: icons off-centre, scooter on the last node looks weird, FAQ shows + and arrow, two "–" | server renders font icons where local has SVG; one decorative layer overlapping another | CSS for both icon forms; rider rides above the stops (parks above the last on phones); one FAQ sign. **Check the pushed site, not only local** (`zs shots --site`) |
| 13 | "QA the inner pages on mobile" | the home page got all the attention | `zs shots <slug> all --mobile`; inner heroes got the ride too |
| 14 | "make it quicker for next clients" | push ~6 min, live QA ~8 min | skip unchanged code/media/pages, batched backup, parallel QA → ~1 min each |
| 15 | phone screenshots: road block off-centre, "the menu goes behind the page" | the header's `backdrop-filter` made it the containing block of the fixed menu (clipped to 67 px); a `body{overflow:hidden}` scroll lock shoved the sticky header up under Elementor | no blur ≤1024 px, JS scroll block instead of an overflow lock, full-width button stacks and centred chips on phones; QA now checks the open menu covers the screen. Never put `filter`/`backdrop-filter`/`transform` on an ancestor of a fixed element |
| 16 | "why is their Facebook not there? it is in the brief" | the URL was in site.json but only used in schema; BRIEF-CHECK said ✅ without looking at the page | footer + contact page render `business.facebook/instagram/linkedin/youtube/tiktok` as solid icon links; QA fails when a profile in site.json is not a link on the site. **A BRIEF-CHECK ✅ means seen on the rendered page, never "it is in site.json"** |
| 17 | client round: "no black background", "luxury, fewer logo colours", "2–3 rotating hero images", "the moving icons sometimes don't work", "must not look like the old site's colours" | the night/dark signature look read as loud and as the old red-yellow site; the "broken" motion was a work PC with Windows animation effects off (reduce motion) | `design.tone: light` (no dark grounds), Frank Ruhl Libre headings, oxblood primary + brass accent, `hero.images` crossfade slider with 3 new daylight Weave images (15 credits), pause buttons on all moving scenes. Ask about the viewer's machine before debugging "sometimes it moves" |
| 18 | "make sure there is no white on white text/graphics — everything visible" | QA only checked some text tags and never shapes, so a white-on-ivory button and faint field borders passed | QA now checks **every** text element (below WCAG AA = error), every control/outline (fill or border ≥ 3:1 against what is behind it) and every icon (≥ 3:1); outlined buttons use a solid border in their text colour, form fields a 55% ink border; a decorative accent used as a shape must clear 3:1 on every ground (brass darkened #a8875a → #8a6a3a) |
| 19 | "footer wordmark still white on white", "Zap logo needs to be blue like before", "a different, less AI-looking font", "Facebook icon the same size and in line with the other icons, with ביקרו בפייסבוק שלנו" | decorative text was exempt from QA; the white Zap credit image was built for dark footers; Rubik/Heebo/Frank Ruhl are the fonts every template defaults to; social links sat as a separate chip row | wordmark outlined in the primary colour and QA now checks decorative text (3:1, outline colour when the fill is transparent); light footers use Zap's colour logo (`assets/zap-group-blue.svg`, from Zap's base install); Bellefair + Miriam Libre vendored (also David Libre, Alef, Bona Nova); social profiles are labelled rows of the contact list with the same 20 px icon |
| 20 | "too much vertical space between sections", "make it more like the first version — it looks AI-template/formulaic now" | the light tone had kept the split hero, equal 136 px paddings everywhere (180–270 px between neighbours) and boxed captions; the first version's energy came from the full-bleed hero, a stat band and slogan band welded under it, and photo tiles | light tone: `--sec-y` ~30% smaller and no doubled padding between same-ground neighbours; full-bleed hero slider with an ivory wash on the text side (text anchored to the text edge), big-numeral stat band on stone, full-width stone slogan band, overlay photo tiles (finish.css system, warm shade instead of near-black, numbers kept). Show a local preview before pushing a big visual change |
| 21 | "still not a fan of the font" (twice: Frank Ruhl, then Bellefair) | font taste is not guessable from adjectives like "less AI-looking" | render 4–6 real pairings **on the site's own hero** (one image, numbered) and let the user pick a number; they chose Rubik 800 + Assistant, the first version's family. Light-tone heading weights now follow `--w-head` instead of fixed 500/600, so any font keeps its preset weight. Wait for `document.fonts.load` before shooting specimens |
| 22 | "hero transitions need to be smoother, the shift is abrupt" + "hero and buttons above the fold on desktop and mobile — no scroll to see קבלו הצעת מחיר / מעקב משלוחים" | the outgoing photo lost its zoom animation and snapped from 100% to 106% as it faded, both photos faded together so the ground showed through, and reduced motion (work PCs) turned the fade into a hard cut; the hero was ~830 px tall with a 4:3 phone photo, so the buttons sat 70–310 px below the fold on laptops and phones | crossfade: the next photo fades in over the previous one, which stays opaque (`.is-prev`) and keeps its zoom; under reduced motion the fade stays and only the zoom goes. Fold: height-aware H1 cap (`--zs-h1-cap: 9.4svh`) and top padding on desktop; on phones a 22svh photo, tighter gaps and the two hero buttons side by side; the eyebrow is dropped on phones under 620 px tall. `zs qa` fails when the hero buttons are below the fold at 1280×620 or 360×640 (above the fixed call bar) |
| 23 | "can you get the privacy policy from other Zap sites?" → the user sent Zap's standard wording (docx) and campaign.zapx.co.il/privacy-policy | the base install and Novamira have no policy; Zap's policy is one standard text with four fields ({{name}}, {{data}}, {{more1}}, {{mail}}) that the client fills in on the campaign form | `engine/templates/privacy-he.html` (verbatim; only RTL-garbled Latin words such as "Analytics Google" put back in order) is built into every site's מדיניות פרטיות page from site.json; the database paragraph only with `privacy_database: true`; the docx's editor note is never published. Launch blocker until the client confirms the fields (`privacy_confirmed`) |
| 24 | client round 3: "24 years, not 30", "service area: all of Israel", "never במהירות האור / למהירות האור", "add a הובלת משטחים page with content" | the brief's facts change after launch prep; a Hebrew prefix on the brand name reads as a different word to the client; a sixth service breaks a 5-tile bento | exact old→new string list over site.json with a check that every old string was found (a sloppy replace doubled a word once); asked the user before changing positioning (national everywhere vs. list only) and before writing a page with no facts; new page written without capacity/vehicle claims; bento with exactly 6 tiles lays out 1 big + 2, then 3 equal (theme). Brand rule for Hebrew copy: write "לחברת X" / "X" instead of prefixing ב/ל/ו to a brand name |
| 25 | screenshot: the "Zap score" reviews block with five stars stacked in a column, everything bold red, the links floating — "needs to look cleaner" | Zap's `<zap-reviews>` widget renders light-DOM HTML from api.zap360.co.il and links `zap.dbusiness.co/css/zap-reviews.css`, which is a 404; the theme's heading/link/image rules then styled it. It never shows locally (API) and was blocked from the session too, so no screenshot ever caught it | the theme styles the widget itself (review card, one row of stars, body-text review with its line breaks, page chips + links in one row, the duplicate "לכל הביקורות" link hidden); checked by answering the widget's API request with the real response (curl → `page.route`) locally and on staging; `zs qa --site` now fails a broken widget. Third-party widgets get their own look-check on the pushed site |

## What "high end" concretely means here (the bar the user accepted)

- First screen: full-bleed night photo + a 3 s silent loop (desktop), H1 two lines, brand half in accent italic,
  eyebrow with an accent dash, two buttons (primary + ghost), three proof points. On phones: the photo and a
  scooter driving along the bottom.
- Then: a dark stat band welded to the hero (real numbers only: "30+", "עשרות"), a tilted accent marquee, a
  split with a badge on the photo, bento photo tiles with numbers and ↖ arrows, a moving road, dark features,
  the route, FAQ with +/–, a brand-red CTA, then the light lead band and the dark footer with the wordmark.
- Everything follows one radius token (2 = sharp), one accent (yellow), one primary (red), ink black.
- Every inner page: a dark page hero with breadcrumbs and the ride, then content, FAQ, CTA.

## Pitfalls already paid for (don't pay again)

**Content and facts**
- The brief's phone may differ from the Zap tracking number: the site shows the Zap number (confirm once).
- Brief wording can be obsolete ("טכנולוגיית WAP"): keep the meaning, modernise the words, note it in NOTES.md.
- A prohibition in the brief ("no food deliveries") is checked with a grep over site.json before delivery.
- A client's own video can carry stale facts (an old phone in the thumbnail): flag it, don't silently embed.

**Design**
- Elementor's kit defaults (red headings, yellow buttons) leak in unless `elementor_disable_color_schemes` /
  `_typography` are set — the build sets them every time; if a pushed site shows odd colours, re-push.
- Kit CSS variables are scoped to `body`; theme tokens are redeclared there. Elementor's `img{height:auto}` beats
  hero image fill unless the selector is more specific.
- Decorative motion must never sit on top of controls or text at 390 px; check scrolled states, not only
  full-page shots.

**Delivery (Novamira, Zap hosts)**
- No WP-CLI on the host: everything runs as PHP through `execute-php` (30 s per call). `.php` uploads are refused
  (code goes up as `.txt`).
- The first push drafts only the base's previous front page and WP sample content; it once drafted a plugin page
  (Login Customizer) — the rule is now narrow. Check Pages → Drafts after a first push.
- Stale Yoast indexables gave a breadcrumb to /home/ — the push resets them.
- The proxy/host drops connections now and then: the transport retries; a lone 502 in QA → re-run once.
- An open Elementor editor overwrites a push when it saves: ask for it to be closed.
- The Novamira token is stored in the session's container: a new cloud session reconnects (one click) unless
  `ZS_NOVAMIRA` is set.

**Process**
- Long steps (push, live QA) run in the background, with the user told the expected time; never go silent.
- Every user screenshot is a generic bug until proven otherwise: fix it in the theme, re-test on the sample,
  rebuild, push, and show the result on the pushed site.
- Commit after every round; the branch is the record. Never commit tokens, backups or `work/`.

## Commands of a typical round (after the first push)

```bash
bin/zs build <slug> && bin/zs qa <slug>                      # local, ~40 s
bin/zs shots <slug> all --mobile                             # read the shots
bin/zs push <slug> --site https://<client>.ussl.co.il       # ~1 min (unchanged parts skipped)
bin/zs qa <slug> --site https://<client>.ussl.co.il         # ~1–2 min, 0 errors
bin/zs shots <slug> all --site https://<client>.ussl.co.il  # look at the real thing
git add sites/<slug> && git commit -m "<slug>: <round>" && git push
```

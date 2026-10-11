# Playbook — how a site actually goes, round by round

The worked case is **מהירות האור שליחויות** (courier, Haifa; `examples/mehirut-haor/`, built Oct 2026), the first
site taken from brief to a live, editable Novamira site. SKILL.md is the order of work; this file is what
each step looked like in practice, what the user pushed back on, and what was learned. Read it once before a
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

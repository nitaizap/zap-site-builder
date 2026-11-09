# Playbook — lessons paid for on real builds

SKILL.md is the order of work; this file is what earlier builds taught, written as rules. It describes no
site: no previous client's composition, palette, fonts or section order is a model for the next one. Every
site is composed from its own brief and the pool (`pool.md`). Read it once before a new site, and again
before the gate and before delivery.

## Lessons (each is now part of the engine or the skill)

**Design quality (04/11/2026, after the site team's standard was compared with ours)**
- Passing every gate is not the same as looking finished. Every design complaint this project has had came off
  a site with `zs qa` 0 errors and `zs seo` 0 FAIL, because the gates measured correctness and nothing measured
  the design. `zs qa` now also measures the part that can be measured: one size per heading level, images never
  shown larger than their own pixels or stretched out of ratio, the number of font families, mobile gutters and
  tap targets, and a page whose buttons carry no icon at all. The report carries a `type scale` and a `fonts`
  column. The image checks are errors; the taste-adjacent ones warn, so a handover is never blocked by drift.
- The rest of it is a checklist, not a number: `qa-rules.md` -> "UX acceptance" is the list of things that make a
  site read as finished (clickability, rhythm, images, forms, floating elements, mobile). Most of its lines were
  learnt twice, once per client, because they lived only in a finished session's context.
- Rules did not transfer the level; examples did. `gallery/` holds our own shipped sites with their screenshots
  and **every correction the user made, in their own words**. Read the nearest 1-2 before composing, write the
  entry after handover. A direction that cannot clear the floor there (6+ real images, icons on conversion
  buttons, a 390 frame, 8+ sections) is not shown to the user.
- A build is checked against what was approved, not only against itself: step 4's fidelity pass opens the chosen
  direction's preview beside the built page at 1440 and 390. Spacing collapsing to the theme default, a weight
  falling back to 400, a crop losing its subject and the bold element flattening are invisible to every gate.

**Intake and facts**
- Facts table in NOTES.md with a source per fact; one numbered message of gaps, so one-line answers map back.
- Research before asking: the Zap customer id opens every Zap directory (d.co.il, rest.co.il, mishlohim…), the
  old site / Wayback (`zs grab`), the client's social links, the Drive folder from the brief (`intake.md`). A
  "not found" names every place looked. Missing a logo that sat in a directory's gallery cost a round.
- Facts change after the first build (years, areas, page list): apply them as an exact old→new list over
  site.json, checking every old string was found. Never prefix ב/ל/ו to a brand name.
- No leads e-mail in the brief → calls-only site (`site-json.md` → `email_leads`); never invent an inbox.
- What the brief doesn't ask for (prices, a WhatsApp, a certifying body) stays off the site.

**Design: no house look**
- "Clean and correct" reads as bland, and copying the last approved site reads as a template. Both were
  rejected. Each site gets its own idea, base template, variants, fonts and palette (`pool.md`, `design.md`),
  checked against the other clients with `zs pool` before the gate.
- Generated-look tells (accent word or dot in the H1, eyebrows on every section, 01/02 numbering, arrows on
  every button, a stat band by default) are neutralised in the theme; don't bring them back in copy.
- Font taste can't be guessed from adjectives: render 4–6 real pairings on the site's own hero and ask for a number.
- "Luxury", "no black", "fewer colours" → `tone: light`, a deeper logo colour, one muted metal accent.
- Nothing may blend in: QA measures every text, control, outline, icon and decorative element against what
  is behind it. Pick colours by measuring contrast on every ground they appear on, not by eye.
- Too much vertical space reads as formulaic; neighbours on the same ground share padding.
- A brief's style line ("animations", "moving vehicles") maps to concrete features, checked on desktop and
  phone, with scrolled screenshots for scroll-driven parts (`design.md` → *Brief words → features*).
- The hero's H1, lead and both buttons show above the fold on a short laptop and a small phone (`zs qa`).

**QA and delivery**
- A BRIEF-CHECK ✅ means seen on the rendered page, never "it is in site.json" (a Facebook link once lived
  only in schema).
- QA the inner pages on mobile, not only the home page (`zs shots <slug> all --mobile`).
- Zap QA reviewers check a fixed list; it is in `qa-rules.md` and mostly enforced by the
  validator, `zs qa` and `zs seo`. Go through the rest before delivery.
- The pushed site renders differently from the local build (font icons, caches, host plugins, third-party
  widgets such as the Dapei Zahav reviews): look at `zs shots --site` every time.
- "It looks static in Elementor": the editor is a canvas; check the front end, reduced motion and cache first.
- The static export must open on Windows: open it yourself before sending.
- Delivery is a live, editable Elementor site through Novamira (header/footer as templates, text in native
  widgets); give the exact links and verify them yourself first.

**Process**
- Work happens on the current engine: a session that starts from a stale branch rebuilds old looks. Engine
  work goes on its own branch and is merged to `main` by PR; parallel sessions merge before they diverge.

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

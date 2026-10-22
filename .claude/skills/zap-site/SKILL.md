---
name: zap-site
description: Build a complete Hebrew client website for Zap Group from a brief, end to end - research, keyword map, copy, design directions, WordPress + Elementor build, measured QA - and deliver it live into the client's WordPress through Novamira (editable in Elementor, header/footer included), or as an upload-ready zip (WordPress files + SQL + deploy script) with a download link. Use when someone pastes a client brief, a spec board, a client name with a domain or old site, or says "בנה אתר", "אתר חדש ללקוח", "תקים אתר", "build a site", or asks to continue, revise or re-package a site under sites/<slug>/.
---

# Zap site builder

One brief in, one live site out (pushed through Novamira into the client's WordPress), or one zip. Claude writes the **content and decisions** (`sites/<slug>/site.json`); the
engine (`bin/zs`) turns that into a real WordPress + Elementor site, measures it, and packages it.
Claude never hand-writes Elementor JSON, CSS per page, or SQL: that is where earlier builds broke.

```
1 INTAKE      brief + research → facts, gaps (one message of questions)
2 PLAN        keyword map + sitemap + 3 design directions → site.json (copy-first)
3 PREVIEW     zs build → zs preview → ⏸ THE ONE GATE: approve sitemap + pick a direction
4 BUILD       apply the direction, all pages, images → zs build → zs qa until 0 errors → zs seo until 0 FAIL
              → mobile pass on every page → BRIEF-CHECK.md (every line of the brief, incl. style demands)
5 DELIVER     zs push → zs qa --site → zs shots --site (Novamira sites)  |  zs package → zs publish (zip)
```

Speak to the user in their language (usually Hebrew). Keep messages short; the files carry the detail.

## What to read, when

SKILL.md is the order of work; the depth is in `references/` and in two built examples. Read the file for a step
before doing the step — every one encodes mistakes already made.

| when | read |
|---|---|
| before a new site (once) | `references/playbook.md` — the reference build round by round: what the user rejected, what "high end" means, every pitfall paid for |
| intake | `references/intake.md` (research-first table), `references/zap-standards.md` |
| plan | `references/keywords.md`, `references/content-seo.md`, `references/site-json.md` (schema + every section type) |
| design + gate | `references/pool.md` (packages, section variants, mixing rules), `references/design.md` (the bar, motion catalogue, brief words → features), `references/benchmark.md` (open the images) |
| images / video | `references/images.md` (Weave models, credit gate, Veo loop) |
| SEO QA | `references/seo-checklist.md` (the team's SEO sheet, row by row, and how `zs seo` checks it) |
| deliver | `references/novamira.md` (push) or `references/delivery.md` (zip) |
| examples | `examples/mehirut-haor/` (premium reference: site.json, NOTES.md, BRIEF-CHECK.md) · `examples/sample-plumber/` (minimal, the engine test) |
| engine questions | `engine/sections.py` (what each section renders), `wp/theme/zap-base/assets/main.css` (how it looks) |

## Iron rules

1. **Never invent a business fact.** Years, licences, numbers, prices, addresses, staff, results, reviews,
   ratings, awards. If it is not in the brief, the client's own site, or a source you can cite, it is not
   on the site. The validator blocks ratings, review counts, placeholders and "illustration" labels.
2. **Measure, don't eyeball.** Done means `zs qa` reports **0 errors** and `zs seo` (the Zap SEO checklist,
   `references/seo-checklist.md`) **0 FAIL**. Screenshots are for taste, numbers
   are for correctness. Never report a page as finished from a screenshot or from memory.
3. **One keyword owns one page.** The H1 is that keyword in natural Hebrew; home and about carry the brand
   name in the H1 too. The validator stops cannibalisation.
4. **One site per session, one branch per site** (`site/<slug>`, or the branch the session was given).
   Several sites = several sessions in parallel. Never mix two clients in one conversation.
5. **Everything durable lives in `sites/<slug>/`** and is committed. `work/` and `dist/` are disposable:
   `zs build` recreates the WordPress from `site.json` on any machine.
6. **The brief's style line is a requirement, not a mood.** "אנימציות של רכבים זזים", "צבעים על בסיס
   הלוגו", "אתר חדשני" each map to concrete features (`references/design.md` → *Brief words → features*)
   and get a row in `BRIEF-CHECK.md`. A demand you can't meet is said out loud, never dropped silently.
7. **Generic fixes only.** A visual bug the user points at (a screenshot, "this looks weird") is almost always
   a theme/engine bug: fix it in `wp/theme` or `engine/` for every site, re-test on the sample, then on
   this site locally **and on the pushed site**.

## 0 · Start

```bash
bin/zs doctor                      # php, wp-cli, mariadb, browser, network, gh — fix FAILs first
git checkout -b site/<slug>        # or `git checkout site/<slug>` to continue an existing site
```

`<slug>`: short latin, lowercase, dashes (e.g. `mayim-tovim`). It is internal only; URLs are Hebrew.
Continuing a site: read `sites/<slug>/NOTES.md` and `site.json`, run `bin/zs build <slug>`, then carry on.

## 1 · Intake — read `references/intake.md`

Extract every fact from the brief and its attachments (open every image; filenames lie). Then **research
the gaps yourself before asking**: Dapei Zahav (customer-id, hours, WhatsApp, Maps CID + geo), the old site
or its Wayback copy, Google, Facebook (table in `references/intake.md`; run it as a background agent).
Record sources in `sites/<slug>/NOTES.md`. Send **one** message with only what research could not settle,
each item with what you found. Do not stop to wait for answers that do not block the plan. Phone and lead
email do block.

## 2 · Plan — read `references/keywords.md`, `references/content-seo.md`, `references/design.md`

- Keyword map and page tree (Ahrefs if connected, else SERP research). Table in NOTES.md.
- Set the package (`tier`) and the base template (`design.base_template`, 1–6) from the brief, then compose the
  pages from the pool (`references/pool.md`): sections
  chosen for what this business must prove, a variant for each, no two clients alike (`bin/zs pool <slug>`).
- Three **genuinely different** design directions anchored in the audience (`directions` in site.json).
- Write `site.json` with **real, final copy** for every page: schema and section catalogue in
  `references/site-json.md`; start from `examples/mehirut-haor/site.json` (the premium reference; its eyebrows/accent words predate the team playbook) for the
  structure and finish level, never from a blank file.
- Images: `references/images.md` (client photos > old-site photos > Weave AI images, one batched credit approval > none).

## 3 · Preview — ⏸ the one gate

```bash
bin/zs new <slug> "<business name>"     # first time only (or just `bin/zs build <slug>`)
bin/zs build <slug>                     # validator runs first; fix every ERROR it prints
bin/zs preview <slug>                   # → sites/<slug>/preview/PREVIEW.md (3 directions, desktop+mobile)
git add sites/<slug> && git commit -m "<slug>: plan + preview" && git push -u origin site/<slug>
```

Want to click through it? `bin/zs static <slug>` → `dist/<slug>-preview.zip` (open index.html, no server;
Windows-safe names; the form and Dapei Zahav reviews only work live). Look at the preview images yourself first (Read them); fix anything ugly before the user sees it.
Then send the user, in one message:
- link: `https://github.com/<owner>/<repo>/blob/site/<slug>/sites/<slug>/preview/PREVIEW.md`
- the page tree with each page's keyword and H1 (short table)
- open questions and assumptions
- the question: which direction (A/B/C), and approve the sitemap?

**Autopilot:** if the user said not to stop ("בלי עצירות", "תבנה עד הסוף"), pick your recommended
direction, say which and why in one line, and continue without waiting.

## 4 · Build

1. Copy the chosen direction into `design` (and drop `directions`, or keep it for later comparison).
2. Finish every page and post; generate or place the images.
3. Loop until clean:
   ```bash
   bin/zs build <slug> && bin/zs qa <slug>      # read QA-REPORT.md; fix; repeat
   bin/zs seo <slug>                            # Zap SEO checklist → SEO-QA.md; 0 FAIL, every 👁 row looked at
   bin/zs shots <slug> / /<some-page>/           # look at desktop + mobile yourself
   ```
   Fix content problems in `site.json`. Fix a visual problem for this client only with
   `design.custom_css` (small, scoped). A problem that would hit every client is a bug in
   `wp/theme` or `engine/`: fix it there, keep it generic, and mention it in the report.
4. **Mobile pass on every page**, not only the home page: `bin/zs shots <slug> all --mobile`, then Read
   each shot (390 px). Look for: wrapped buttons, icons off-centre in their chips, decorative elements
   covering text or each other, horizontal scroll, tiny tap targets, empty bands, the fab hiding content.
   **Above the fold** (a Zap standard): the H1, the lead and both hero buttons show without scrolling on a
   short laptop and a small phone; `zs qa` fails it at 1280×620 and 360×640. Don't fix it per site with
   fixed pixel sizes: the theme sizes the home hero by screen height.
5. **Motion check**: everything the brief asks to move must move on desktop *and* phone (the hero video
   is desktop-only, so phones need their own movement: `hero.ride`, `road`, `route`). Scroll-driven parts
   need a scrolled screenshot, not just a full-page one.
6. **`sites/<slug>/BRIEF-CHECK.md`**: the brief line by line (design/branding, client details, every page
   and its content, components, prohibitions such as "no food deliveries", delivery) → ✅ / ➖ with the
   reason / ⏳ open. A ✅ means you saw it on the rendered page (a shot or the page HTML), never "it is in
   site.json". Grep site.json for every prohibited word. Example: `examples/mehirut-haor/BRIEF-CHECK.md`.
7. Read `references/zap-standards.md` once before you call it done; most of it is automatic, some is not.

## 5 · Deliver — `references/novamira.md` (push) or `references/delivery.md` (zip)

**The client site runs Novamira** (Zap's staging `*.ussl.co.il` clones do): push the build into it.

```bash
bin/zs connect --site https://<client>.ussl.co.il          # once per site: an admin approves a code in wp-admin
bin/zs push <slug> --site https://<client>.ussl.co.il    # backup → code → content; staging lock on
bin/zs qa <slug> --site https://<client>.ussl.co.il      # 0 errors on the pushed site itself
bin/zs shots <slug> all --site https://<client>.ussl.co.il   # LOOK at the pushed site, desktop + mobile
git add sites/<slug> && git commit -m "<slug>: pushed to <host>" && git push
```

- **Timing**: a repeat push takes ~1 min: it skips the theme/plugin, media and pages the server already has
  (fingerprints stored on the server), so a revision re-sends only what changed; the first push to a site
  takes ~3–5 min. The backup runs every time (~20 s). Live QA takes ~1–2 min (viewports and link checks run
  in parallel). `--full` resends everything; `ZS_TRACE=1` prints the time of every server call.
- **The pushed site can render differently from the local build**: e.g. the server's Elementor outputs
  font icons (`<i class="fas …">`) where the local build outputs SVG; caches; host plugins (a11y toolbar).
  That is why `zs shots --site` is part of delivery, and why theme CSS must handle both icon forms.
- **Third-party widgets render only on the pushed site** (the Dapei Zahav reviews `<zap-reviews>`, the a11y
  toolbar). Look at the reviews block in `zs shots --site`. Zap's own widget stylesheet is a 404, so the theme
  styles the widget (main.css, "Dapei Zahav reviews widget"); a messy reviews block is a theme fix, never hand
  CSS in Elementor. If the widget's API is blocked from the session (CORS through the proxy), fetch the reviews
  HTML with curl (`POST https://api.zap360.co.il/api/zap-widgets/reviews`) and answer the page's request with
  it (Playwright `page.route`) to check the styling; `zs qa --site` checks it whenever reviews show.
- **A single `HTTP 502` / "upstream request failed" in the live QA** is the network, not the site: check the
  page with curl and re-run the QA once. A second failure is real.
- **"It looks static in Novamira/Elementor"**: the Elementor editor is an editing canvas; scroll-driven
  effects (route rider, progress bar, reveals) run only on the real page. Also check the viewer's OS
  "reduce motion" setting (Windows: Animation effects) — the site parks all motion then, by design — and
  cache (open in a private window). Verify yourself on the front end before answering.

Needs a connection: `zs connect` (run it in the background, give the user the link + code in one line, wait), or
the `ZS_NOVAMIRA` secret from the one-time base-site setup. Without either, say so, do everything else, offer the zip. A live (non-staging) domain needs `--live` and the
user's explicit go-ahead. What a person edits afterwards — pages, header/footer templates, Site Settings
colours/fonts — is all in Elementor; list it in the reply.

**No Novamira on the target**: the zip.

```bash
bin/zs package <slug> --domain https://<final-domain>     # refuses while QA has errors
bin/zs publish <slug>                                      # GitHub release / delivery branch (+ SharePoint if configured)
git add sites/<slug> && git commit -m "<slug>: delivered" && git push
```

Reply with: the site link (or download link), the Elementor editor link, what was built (pages, posts,
direction), the QA numbers, and the human-only blockers from `LAUNCH-CHECKLIST.md`. Never write "everything
is ready" while a blocker exists.

## Revisions

Client notes → edit `site.json` (or `custom_css`, or the theme when it is generic) → `zs build` → `zs qa`
→ then the same delivery as before: `zs push` → `zs qa --site` → `zs shots --site` (Novamira), or
`zs package` → `zs publish` (zip). Same branch, same session if it is still open; otherwise start from
`git checkout site/<slug>`. Ask for all notes of a round in one message.

Notes arriving as screenshots: find the element, reproduce it (`zs shots`, or a scrolled Playwright shot
for motion), fix, and show the before/after on the pushed site in the reply. Hand edits made in Elementor
by the client are overwritten by the next push: once the client edits, stop pushing or move their change
into site.json first.

## Skill, plugin or workflow?

This stays a repo skill: it is inseparable from the engine and theme in this repo, and every site session
starts here. Package it as a plugin only when it must run outside this repo. Use a multi-agent workflow
only for parallel independent work (e.g. several sites, one session each), never inside one site.

## When the engine can't do something

The section catalogue covers service businesses well. If a client needs something it lacks (a price table,
a booking widget, a product catalogue), prefer: an existing section with good content → a `prose` section
(HTML tables are fine) → an embed (`video`, `[zap_map]`) → a new generic section type in
`engine/sections.py` + CSS in `wp/theme/zap-base/assets/main.css`, added for everyone, never one-off.

## Cost discipline

Numbers instead of pictures (QA is measured; screenshots only for the design look). Read files with
offset/limit. Don't print WordPress or SQL dumps. One site per session keeps context small.

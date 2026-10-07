---
name: zap-site
description: Build a complete Hebrew client website for Zap Group from a brief, end to end - research, keyword map, copy, design directions, WordPress + Elementor build, measured QA - and deliver one upload-ready zip (WordPress files + SQL + deploy script) with a download link. Use when someone pastes a client brief, a spec board, a client name with a domain or old site, or says "בנה אתר", "אתר חדש ללקוח", "תקים אתר", "build a site", or asks to continue, revise or re-package a site under sites/<slug>/.
---

# Zap site builder

One brief in, one zip out. Claude writes the **content and decisions** (`sites/<slug>/site.json`); the
engine (`bin/zs`) turns that into a real WordPress + Elementor site, measures it, and packages it.
Claude never hand-writes Elementor JSON, CSS per page, or SQL: that is where earlier builds broke.

```
1 INTAKE      brief + research → facts, gaps (one message of questions)
2 PLAN        keyword map + sitemap + 3 design directions → site.json (copy-first)
3 PREVIEW     zs build → zs preview → ⏸ THE ONE GATE: approve sitemap + pick a direction
4 BUILD       apply the direction, all pages, images → zs build → zs qa until 0 errors
5 DELIVER     zs package → zs publish → link + launch checklist
```

Speak to the user in their language (usually Hebrew). Keep messages short; the files carry the detail.

## Iron rules

1. **Never invent a business fact.** Years, licences, numbers, prices, addresses, staff, results, reviews,
   ratings, awards. If it is not in the brief, the client's own site, or a source you can cite, it is not
   on the site. The validator blocks ratings, review counts, placeholders and "illustration" labels.
2. **Measure, don't eyeball.** Done means `zs qa` reports **0 errors**. Screenshots are for taste, numbers
   are for correctness. Never report a page as finished from a screenshot or from memory.
3. **One keyword owns one page.** The H1 is that keyword in natural Hebrew; home and about carry the brand
   name in the H1 too. The validator stops cannibalisation.
4. **One site per session, one branch per site** (`site/<slug>`). Several sites = several sessions in
   parallel. Never mix two clients in one conversation.
5. **Everything durable lives in `sites/<slug>/`** and is committed. `work/` and `dist/` are disposable:
   `zs build` recreates the WordPress from `site.json` on any machine.

## 0 · Start

```bash
bin/zs doctor                      # php, wp-cli, mariadb, browser, network, gh — fix FAILs first
git checkout -b site/<slug>        # or `git checkout site/<slug>` to continue an existing site
```

`<slug>`: short latin, lowercase, dashes (e.g. `mayim-tovim`). It is internal only; URLs are Hebrew.
Continuing a site: read `sites/<slug>/NOTES.md` and `site.json`, run `bin/zs build <slug>`, then carry on.

## 1 · Intake — read `references/intake.md`

Extract every fact from the brief and its attachments (open every image; filenames lie). Research the
business: old site, Google, Dapei Zahav (d.co.il), Facebook. Record sources in `sites/<slug>/NOTES.md`.
Then send **one** message with everything missing (privacy PDF, Dapei Zahav customer-id, display phone vs
WhatsApp vs lead email, contradictions in the brief, photos). Do not stop to wait for answers that do not
block the plan: continue with what is known and mark gaps in NOTES.md. Phone and lead email do block.

## 2 · Plan — read `references/keywords.md`, `references/content-seo.md`, `references/design.md`

- Keyword map and page tree (Ahrefs if connected, else SERP research). Table in NOTES.md.
- Three **genuinely different** design directions anchored in the audience (`directions` in site.json).
- Write `site.json` with **real, final copy** for every page: schema and section catalogue in
  `references/site-json.md`, a complete example in `examples/sample-plumber/site.json`.
- Images: `references/images.md` (client photos > old-site photos > Weave AI images, one batched credit approval > none).

## 3 · Preview — ⏸ the one gate

```bash
bin/zs new <slug> "<business name>"     # first time only (or just `bin/zs build <slug>`)
bin/zs build <slug>                     # validator runs first; fix every ERROR it prints
bin/zs preview <slug>                   # → sites/<slug>/preview/PREVIEW.md (3 directions, desktop+mobile)
git add sites/<slug> && git commit -m "<slug>: plan + preview" && git push -u origin site/<slug>
```

Look at the preview images yourself first (Read them); fix anything ugly before the user sees it.
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
   bin/zs shots <slug> / /<some-page>/           # look at desktop + mobile yourself
   ```
   Fix content problems in `site.json`. Fix a visual problem for this client only with
   `design.custom_css` (small, scoped). A problem that would hit every client is a bug in
   `wp/theme` or `engine/`: fix it there, keep it generic, and mention it in the report.
4. Read `references/zap-standards.md` once before you call it done; most of it is automatic, some is not.

## 5 · Deliver — read `references/delivery.md`

```bash
bin/zs package <slug> --domain https://<final-domain>     # refuses while QA has errors
bin/zs publish <slug>                                      # GitHub release (+ SharePoint if configured)
git add sites/<slug> && git commit -m "<slug>: delivered" && git push
```

Reply with: the download link, what was built (pages, posts, direction), the QA numbers, and the
human-only blockers from `LAUNCH-CHECKLIST.md`. Never write "everything is ready" while a blocker exists.

## Revisions

Client notes → edit `site.json` (or `custom_css`) → `zs build` → `zs qa` → `zs package` → `zs publish`.
Same branch, same session if it is still open; otherwise start from `git checkout site/<slug>`.
Ask for all notes of a round in one message.

## When the engine can't do something

The section catalogue covers service businesses well. If a client needs something it lacks (a price table,
a booking widget, a product catalogue), prefer: an existing section with good content → a `prose` section
(HTML tables are fine) → an embed (`video`, `[zap_map]`) → a new generic section type in
`engine/sections.py` + CSS in `wp/theme/zap-base/assets/main.css`, added for everyone, never one-off.

## Cost discipline

Numbers instead of pictures (QA is measured; screenshots only for the design look). Read files with
offset/limit. Don't print WordPress or SQL dumps. One site per session keeps context small.

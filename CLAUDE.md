# Zap site builder

Builds Zap Group client websites (Hebrew, WordPress + Elementor) from a brief and delivers an
upload-ready zip. Start every site with the `/zap-site` skill (`.claude/skills/zap-site/SKILL.md`).

## Layout

- `engine/` – the `zs` CLI (Python): build, validate, QA, package, publish. `bin/zs` runs it.
- `wp/theme/zap-base`, `wp/plugin/zap-site` – shared theme + plugin installed into every site.
  A change here changes every future site: keep it generic, test it on `examples/sample-plumber`.
- `sites/<slug>/` – one client: `site.json`, `assets/`, `NOTES.md`, `QA-REPORT.md`, `preview/`.
  Committed on its own branch `site/<slug>`, never on `main`.
- `work/`, `dist/`, `.tools/` – disposable (gitignored). WordPress is rebuilt from `site.json`.

## Rules

- One client per session and per branch (`site/<slug>`). Parallel sites = parallel sessions.
- Do not commit to `main` from a site session. Engine/theme fixes go on a separate branch + PR.
- Claude may open and merge its own engine/theme/skill PRs without asking, when GitHub reports no merge conflict
  (mergeable), any CI on the head is green, and the engine test below passed (`qa` 0 errors, `seo` 0 FAIL). If there
  is a conflict, red CI or an open review thread, fix it first or ask. Never merge a `site/<slug>` branch into `main`.
  Default is to merge without asking: do not stop mid-work for approvals that these conditions already cover.
- Open items are collected, not asked one by one: anything unclear, assumed or blocked goes into
  `sites/<slug>/OPEN-ITEMS.md` (site work) or the PR body under "Open items" (engine work), and work continues
  on the best safe default. Only at the very end does the user get one list: what is done, then the open items.
  Stop early only for what cannot be defaulted safely (a business fact, mailing a real client, a secret).
- No em dashes (—) in any site copy, ever (the validator stops the build).
- No shortcodes on new sites, ever: build only with Elementor widgets and WordPress. Dynamic parts (form, menus, posts,
  map, contact details, footer credits, blog templates) are the `zap-*` widgets the `zap-site` plugin registers.
  `zs build` stops on a shortcode and `zs qa` flags a shortcode widget. Sites built earlier keep theirs (the legacy
  `[zap_*]` shortcodes stay registered for them); do not add new ones.
- No site may look like another client's. `zs qa`, `zs preview`, `zs push` and `zs package` measure the home page
  (palette, header/footer/form band/FAQ/icons, components, layout) against every client in `fingerprints/` and on
  `site/*` branches, and stop at 40% alike. Fix it by redesigning (kit, palette, hero, components), never by tuning
  the measure. The rules are in `.claude/skills/zap-site/references/pool.md`.
- Never invent business facts; never mail the real client from staging; never print secrets.
- **Image rights.** Standing instruction from שרון יוסף, 20/10/2026, after review by עו"ד קובי בארי: a
  copyright claim can reach ₪100,000 per image, with no need to prove damage. Every image uploaded to a
  client site is recorded in `sites/<slug>/IMAGE-SOURCES.md`: upload date, who uploaded it, and the exact
  source - for a downloaded photo the site and the licence type, for AI the tool **and the model**. An
  image whose origin is uncertain is not used. Details: `.claude/skills/zap-site/references/images.md`.
- **Weave budget: 100 credits per client.** Spend freely under it; only going over needs the user.
- Before calling anything done: go through `.claude/skills/zap-site/references/qa-rules.md` (what Zap QA rejects), then `bin/zs qa <slug>` with 0 errors and `bin/zs seo <slug>` (the Zap SEO
  checklist) with 0 FAIL.

## Delegating: pick the model and effort for the job

Every subagent, session or scheduled run costs what you give it. Match it to the work; the table is the
default, deviate only with a reason.

| work | model | effort | why |
|---|---|---|---|
| Orchestrating: writing briefs, checking what an agent reports, deciding what ships | Opus | high | Its whole value is catching a confident report that is wrong. On 2026-11-03 three agent reports were wrong in ways that mattered, each caught only by re-running the check. |
| Building a client site | Sonnet | high | Long and partly mechanical, but it is design judgement and it faces the client. Both theme bugs found that day - a title clearing contrast by luck at 4.56:1, and bidi reversing a Latin brand inside a Hebrew H1 - came from reading `qa-rules.md` carefully, not from any gate. Do not go below high here. |
| Intake, reply routing, board sync, the hourly run | Sonnet | medium | Deterministic: read mail, run a command, write a file, report. Haiku at medium once a path has been stable for a while. |
| Verification: does this number match that file, is this branch current | Haiku | low | No judgement, just a lookup. Most of what an orchestrator checks belongs here. |

Two things that save more than any model choice:

- **Client builds belong in cloud sessions, not local subagents.** Only intake needs this PC (Outlook, the
  F: drive). Everything after it is portable, and cloud sessions run genuinely in parallel without fighting
  over ports, the shared MariaDB, or a local watchdog that kills a build stuck on one long call.
- **Land engine and theme changes before dispatching builds, not during.** A theme fix merged mid-build
  costs every agent a re-merge and a re-measure, and their uniqueness numbers go stale the moment the pool
  moves under them.

Give any long-running agent the traps as well as the task: `bin/zs` never `py engine/zs.py` (PYTHONUTF8,
or Hebrew breaks), never trust an exit code read through a pipe, and background anything that may exceed
about ten minutes.

## Test the engine after changing it

```bash
bin/zs new sample "מים טובים אינסטלציה" --from examples/sample-plumber   # first time
bin/zs build sample && bin/zs qa sample && bin/zs seo sample && bin/zs preview sample
```

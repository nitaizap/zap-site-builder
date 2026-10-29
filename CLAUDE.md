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
- No em dashes (—) in any site copy, ever (the validator stops the build).
- Never invent business facts; never mail the real client from staging; never print secrets.
- Before calling anything done: go through `.claude/skills/zap-site/references/qa-rules.md` (what Zap QA rejects), then `bin/zs qa <slug>` with 0 errors and `bin/zs seo <slug>` (the Zap SEO
  checklist) with 0 FAIL.

## Test the engine after changing it

```bash
bin/zs new sample "מים טובים אינסטלציה" --from examples/sample-plumber   # first time
bin/zs build sample && bin/zs qa sample && bin/zs seo sample && bin/zs preview sample
```

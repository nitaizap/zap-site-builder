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
- Never invent business facts; never mail the real client from staging; never print secrets.
- Before calling anything done: `bin/zs qa <slug>` with 0 errors.

## Test the engine after changing it

```bash
bin/zs new sample "מים טובים אינסטלציה" --from examples/sample-plumber   # first time
bin/zs build sample && bin/zs qa sample && bin/zs preview sample
```

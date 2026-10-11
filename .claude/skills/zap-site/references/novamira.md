# Novamira — pushing a built site into the client's WordPress

Zap's client sites live on cloned base installs (staging `*.ussl.co.il`, then the client domain) that run
**Novamira** (novamira.ai), a WordPress plugin that is itself an MCP server. `zs push` uses its REST runner to
run the same build that `zs build` runs locally, on the real server. The free plugin is enough.

| ability | used for |
|---|---|
| `novamira/execute-php` | every build step (PHP inside WordPress, 30 s per call → the engine batches) |
| `novamira/run-wp-cli` | plugins/themes, flushes, db export for the backup |
| `novamira/create-upload-link` | media, theme/plugin zips, build payloads (a temp PUT URL; `.php` uploads are refused) |
| `novamira/create-admin-access-link` | one-time admin login for checking the Elementor editor |

Runner: `POST <site>/wp-json/novamira/v1/abilities/<ability>/run {"input": {...}}`, authenticated as an
administrator with a WordPress **Application Password**.

## One-time setup (done once on Zap's BASE site, inherited by every clone)

1. On the base site: Novamira → Configuration → **Enable AI Abilities**. They are locked to the site's host
   name; a clone keeps them on when the cloning tool search-replaces the domain (the lock is a stored host
   name), otherwise one click on the clone.
2. Create an administrator `zap-builder` (dedicated: revoking = deleting one user; the log shows what came from
   the pipeline) and an Application Password for it (Users → Profile → Application Passwords).
3. Put `zap-builder:<application password>` into the cloud environment's secrets as **`ZS_NOVAMIRA`**
   (environment settings → Network secrets / environment variables). A new session reads it.
   Per-site override: `ZS_NOVAMIRA_<HOST>` (host upper-cased, non-alphanumerics → `_`).

Application passwords live in the database, so every site cloned from the base carries the same integration
user: no per-site codes or passwords. Never paste the password into a chat, a file or the repo; a password
that has been in a transcript is burned (revoke and issue a new one).

## Push

```bash
bin/zs push <slug> --site https://<client>.ussl.co.il       # staging hosts only without --live
bin/zs qa <slug> --site https://<client>.ussl.co.il         # full QA on the pushed site -> QA-REPORT-live.md
```

What `zs push` does, in order:
1. checks the connection (WP/PHP/Elementor/Pro/theme) and refuses a site that already holds another business;
2. **backs up the database to this machine** (`work/<slug>@<host>/backup-*.sql.gz`) — Novamira has no rollback;
3. sets the **staging lock** (`zs_staging_lock`): leads are saved but never mailed to the real client, noindex;
4. installs our child theme (Zap Base, parent Hello Elementor — Zap's base theme stays) and the Zap Site plugin,
   and anything missing (Elementor, Yoast, Ally);
5. runs the build: options, media, pages (one per call), header/footer templates, menus, Yoast, Elementor kit;
6. first push only: the base's placeholder pages/posts go to **draft** (reversible, listed); later pushes never
   touch pages that site.json does not own;
7. removes its temp folder and prints the site, the Elementor editor link and the templates link.

Pushing again is safe: everything is matched by key and updated in place (same page and template IDs).
**Ask for the Elementor editor to be closed** during a push — an open editor's save overwrites the push.

## What a person can edit afterwards (in Elementor)

- Every page: containers with native widgets (heading, text, image, button, icon, accordion, video).
- **Header and footer**: Elementor templates. With Elementor Pro (Zap's base has it) they are Theme Builder
  header/footer with "entire site" conditions; without Pro they are saved templates the theme renders.
  Menus are edited in Appearance → Menus; the lead form, contact list and legal line are shortcodes.
- **Brand colours and fonts**: Elementor Site Settings → Global Colors / Global Fonts. The theme reads them, so
  one change restyles the whole site.
- Decorative only (HTML widgets): the slogan marquee, the moving road, the hero video, the footer wordmark.

A later `zs push` rewrites what site.json owns (pages, templates, kit). Hand edits made in Elementor are
overwritten by the next push; after handover, edit in Elementor and stop pushing — or put the change into
site.json first.

## Troubleshooting

| symptom | cause / fix |
|---|---|
| `401` | wrong user/application password, or a security plugin (WP 2FA, Wordfence) blocks REST auth for that user — allow application passwords for `zap-builder` |
| `403 novamira_disabled` | AI Abilities off or locked to another domain → Novamira → Configuration → Enable |
| HTML instead of JSON | Novamira not active, or permalinks/REST broken on the site |
| `php_sandbox_required` | a `.php` file upload; the engine uploads code as `.txt`/zip — report it as an engine bug |
| WAF/CDN blocks | the host blocks server-to-server requests; Novamira's Troubleshoot page has a ready email for the host |

Local test bench: `tools/novamira-replica.py` builds a Zap-base replica (Hello Elementor + Elementor + Novamira)
on `http://127.0.0.1:8790` with an integration user, then `zs push <slug> --site http://127.0.0.1:8790
--cred-file work/zapbase/.novamira-cred`.

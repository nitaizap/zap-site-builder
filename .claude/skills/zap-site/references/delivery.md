# 5 · QA, packaging and delivery

## QA loop

`bin/zs qa <slug>` crawls every published URL at 1440px and 390px and measures:
HTTP status · one H1 · one `<main>` · title/description · canonical · og:image · heading jumps ·
horizontal overflow (RTL-safe) · text under 13.4px · contrast (WCAG AA) · images without ALT or broken ·
`tel:` = displayed number · WhatsApp links · rating text / `aggregateRating` · FAQ shown = FAQ schema ·
CSS or shortcodes leaking as text · unlabeled fields · every internal link 200 in one hop · real 404 ·
mobile menu opens and closes · a real form submission is saved.

Errors must reach **0**. Warnings: read them; fix the ones a client or Google would notice.
Then look at `zs shots` for taste (desktop and mobile of home + one service page at least).

## Package

```bash
bin/zs package <slug> --domain https://client.co.il
```

- Refuses if QA has errors or if `site.json` changed after the last QA.
- `database.sql` has every URL rewritten to the domain (plain, serialized, JSON-escaped, URL-encoded) and
  fails if any local URL survives.
- Indexing is on for the client domain and off for `*.zapsites.co.il` staging hosts.
- No admin password ships: `deploy.sh` generates one on the server.
- Unknown final domain? Package for `https://<slug>.zapsites.co.il`; `deploy.sh --url` moves it later.

## Publish

```bash
bin/zs publish <slug>
```

Uploads the zip (+ sha256) as a GitHub release asset `<slug>-<yyyymmdd>` on this repo and prints the
link. With `ZS_SHAREPOINT_FLOW_URL` set on the environment it also posts the zip to the Power Automate
flow that stores it in SharePoint; a SharePoint failure never hides the GitHub link.

The GitHub link needs a GitHub login with access to the repo. If the server person has none, the
SharePoint route (or the user forwarding the file) is the way.

## The final message

```
✅ <business> — מוכן להעלאה
הורדה: <link>   (XX MB)
נבנו: N עמודים, M פוסטים · כיוון עיצוב: <label>
QA: <pages×viewports> בדיקות, <links> קישורים, 0 שגיאות
פתוח (באחריות אדם): <blockers from LAUNCH-CHECKLIST.md>
```

Then commit and push `sites/<slug>/` on `site/<slug>`.

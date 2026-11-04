# הוילה הלבנה ינוב — the LIVE site (thewhite-villa.co.il)

This client has **two** builds, and they are not the same thing:

- `sites/white-villa/` — the zap-pipeline build, staging `80392936.ussl.co.il`
  (that host currently answers **403 with an expired certificate**, so it serves nothing).
- **the live site at `https://thewhite-villa.co.il`** — an Elementor site on `hello-elementor`
  with `zap-base` present for its CSS. It is **not** built or deployed by `bin/zs`.

## Why these files exist

On 04/11/2026 the live site's header showed only a phone button and its footer showed
column headings with no links and no form. Cause: both Elementor templates still referenced
the `zap-site` plugin's widgets (`zap-logo`, `zap-nav`, `zap-form`, `zap-menu`,
`zap-footer-contact`, `zap-copyright`, `zap-legal`, `zap-group-logo`), and that plugin is
**not active** on this site, so Elementor rendered nothing for those widget types.

The plugin is deliberately not installed here: it hooks `phpmailer_init` at the default
priority and collides with **WP Mail SMTP**, which this site uses.

## What is in here

`whitevilla-template-1326-backup.json` — the Header template's `_elementor_data` as it was
before the change. `whitevilla-template-1328-backup.json` — the Footer template's.

**To roll back:** POST the file's contents to
`/wp-json/wp/v2/elementor_library/<id>` as `meta._elementor_data` (string), as an
administrator, then Elementor → Tools → **נקה קבצים ונתונים**. The widgets will render
as nothing again unless `zap-site` is active.

## What replaced them (core Elementor, plus Pro for the form only)

| was | now |
|---|---|
| `zap-logo` (header) | `image`, 96px, linked home |
| `zap-nav` | `icon-list` inline, from the "ראשי" menu, 7 items |
| `zap-logo` (footer) | `image` using **logo-light.webp** (id 1554) — the dark one is invisible on the dark footer |
| `zap-menu` | `icon-list` from the "פוטר" menu |
| `zap-footer-contact` | `icon-list`: phone, e-mail, address |
| `zap-call-line` | `text-editor` with a `tel:` link |
| `zap-copyright` | `text-editor` |
| `zap-legal` | `text-editor` linking מדיניות פרטיות and הצהרת נגישות |
| `zap-form` | Elementor **Pro** `form` → `shimon@ashrh.co.il`, with a privacy-consent field |
| `zap-group-logo` | **removed** — no native equivalent; restore from the backup if it is wanted |

A core `html` widget holding a `<style>` block sits in the header. It keeps the phone
header to one scrollable row (197px → 77px at 375px wide). Elementor's
`.elementor-inline-items` sets `flex-wrap:wrap` at a specificity that needs the explicit
override that block carries.

## Not verified

**No lead has actually been submitted through the new form.** It renders with ten fields
and delivery is configured, but whether mail leaves the server is untested — and mail is
exactly the thing that is known to be fragile on this site.

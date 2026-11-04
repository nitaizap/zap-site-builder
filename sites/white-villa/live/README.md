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

A core `html` widget sits in the header holding a `<style>` block and a native
`<details>` disclosure used as the phone menu — no JavaScript, no Pro widget.

On phones the inline nav is hidden and the disclosure shows instead: a 44x44 round
burger beside the 96px-to-52px logo and the phone button, which is forced back to a
true 44x44 circle (it rendered 44x54, a visible oval). The header went 197px -> 69px
at 375px wide. An earlier attempt kept the inline list and let it scroll sideways; it
showed 134px of 439px and clipped a word mid-way, so it was replaced.

## Not verified

**No lead has actually been submitted through the new form.** It renders with ten fields
and delivery is configured, but whether mail leaves the server is untested — and mail is
exactly the thing that is known to be fragile on this site.

## Later in the same session

**The zap group logo is back.** It was first restored as an `image` widget pointing at
`logo-zap-group-1.svg` (media id 755), but that file's wordmark is `#011c32` — near-black on
the dark footer, so only the blue mark read. SVG upload is refused on this site
(`rest_upload_sideload_error`), so a recoloured copy could not be added to the media library.
The widget is now an `html` widget holding the **SVG inline**, with `#011c32` swapped for
`#ffffff` at build time. The blue mark (`#052b7a`) is untouched, as asked. It links to
zapgroup.co.il with `rel="noopener nofollow"`.

**The form now stores its leads.** It was first configured with
`submit_actions: ["email"]` only, which meant a lead existed solely as an outbound e-mail:
if mail failed, it was gone. A test submission confirmed it — nothing was recorded. It is now
`["email","save-to-database"]`, matching the "saved + emailed" standard, and a second test
appears as submission id 2 under "לידים — הוילה הלבנה ינוב" in איסוף לידים.

### What the two test submissions prove, and what they do not

Both reported `הטופס נשלח בהצלחה`, and Elementor records the e-mail action as succeeded.
That means `wp_mail()` accepted the message, **not** that it reached the inbox. WP Mail SMTP's
e-mail log is a Pro feature and is not available here, so there is no independent delivery
record on the site. **Only the recipient can confirm arrival.**

Two test e-mails were sent to `shimon@ashrh.co.il`, both clearly marked as tests
("בדיקת מערכת - Zap" and "בדיקה 2 - Zap"). Only the second is stored, since the first
predates the save-to-database fix.

## Mail on this site — what is actually configured, and what was verified

`WP Mail SMTP` on `thewhite-villa.co.il` is set to:

| setting | value |
|---|---|
| mailer | `smtp` |
| host | `relay.d.co.il` |
| port | `25` |
| encryption | **`tls`** |
| from | `zapsites@d.co.il` |

That is **the same relay `zap-site` hardcodes**, with the same sender — but with TLS **on**,
where `inc/leads.php` forces it off and comments "relay offers no TLS; forcing it fails every
send". On a site where both run, the two configure the same host and port with opposite
transport security, and whichever hook wins decides whether mail sends at all. That is a
sharper description of the reported "בעיות SMTP" than an ordering race alone.

**Verified 04/11/2026:** a WP Mail SMTP test message sent from this site to the operator's own
address, over `relay.d.co.il:25` with `tls`, was **received**. So the relay does offer
STARTTLS and mail over it is delivered. The plugin comment is wrong, or long out of date, and
our hardcoded `SMTPSecure=''` / `SMTPAutoTLS=false` has been downgrading client lead mail to
an unencrypted hop. Passed to the open mail PR (#85).

The sender misalignment (`zapsites@d.co.il` on a client domain) also lives in **WP Mail SMTP's
own settings** here, not only in our plugin, so fixing the plugin's sender does not reach it.

## The dependency ran deeper than the header and footer

Fixing the two theme templates was not the whole job. The site leans on `zap-site` in four more
places, and every one of them rendered as nothing or as a raw placeholder:

| where | was | now |
|---|---|---|
| `עמוד שירות` template (2021) | `zap-title` / `zap-excerpt` **dynamic tags**, falling back to the literal `__ZS_TITLE__` and `__ZS_LEAD__`; `zap-page-content`; `zap-breadcrumbs` | `heading` + `text-editor` with Elementor's own `post-title` / `post-excerpt` tags, `theme-post-content`, breadcrumbs dropped |
| blog archive (1718) | `zap-archive-title`, `zap-archive-intro`, `zap-archive-posts`, `zap-breadcrumbs` | `heading` ("בלוג"), `text-editor`, Elementor `archive-posts` |
| single post (1716) | `zap-post-title`, `zap-post-meta`, `zap-post-image`, `zap-post-extras`, `zap-more-posts` | `heading` + `post-title` tag, `post-info`, `theme-post-featured-image`; extras and more-posts dropped |
| `צרו קשר` page (1322) | `zap-nap`, `zap-form`, `zap-map`, `zap-breadcrumbs` | `icon-list` (phone/e-mail/address), Elementor form → `shimon@ashrh.co.il`, `google_maps`, breadcrumbs dropped |

**Elementor's `archive-title` renders nothing on a static posts page**, so the blog H1 is a plain
heading reading "בלוג" rather than a dynamic one.

Also added, in the header's `html` widget so it applies site-wide: a few lines of JS that compare
`location.pathname` with each nav link and set `is-active` + `aria-current="page"`, styled with a
brass underline on desktop and an inset bar in the phone menu; and footer CSS giving the three
columns equal widths (they were 451 / 368 / 368 and misaligned).

### Verified after the change

Every page 200, **zero** `__ZS_` placeholders, **zero** `zap-` widgets left anywhere:
home, אודות, וילה לנופש, מסיבות ואירועים, גלריה, בלוג, צרו קשר, מדיניות פרטיות, הצהרת נגישות —
each with a real `<h1>`. Blog lists 3 posts; a post opens with its own title, featured image and
body. Contact has 10 form fields, the NAP block and the map. Footer columns measure 368px each at
a common top.

### The judgement this leaves open

Every one of these replacements reimplements, less well, something the plugin already does — the
breadcrumbs are simply gone, and "more posts" with them. **The site was built for `zap-site`.**
The honest fix is to ship the mail-safe plugin (PR #85, which stands down when another mailer is
present — and this site runs WP Mail SMTP) and activate it, rather than to keep hand-rebuilding
the site around its absence.

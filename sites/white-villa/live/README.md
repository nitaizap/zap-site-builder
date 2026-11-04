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

## The footer's ragged contact column — and how two measurements lied

The יצירת קשר column looked ragged: the phone number sat at the far left while the e-mail and
address sat right. Two measurements said it was fine before one said what was wrong:

1. Measuring the `<li>` boxes: all three identical (`left 113, right 481`). **Looked correct.**
2. Measuring the anchors' bounding boxes after a first fix: all three `right: 481`. **Looked fixed.**
3. Measuring the **glyphs**, with `Range.selectNodeContents()`: phone at `113–194`, e-mail at
   `352–481`. **The actual fault.**

The boxes were always identical; only the text inside them moved. A box measurement cannot see
this, and a scaled screenshot was too coarse to settle it either way.

**The cause is flex, not text alignment.** The theme sets `direction: ltr` on `tel:` links so the
digits read in order. Elementor renders the link as `display: flex` with the label in a child
span, so the span is a **flex item** sized to its content (82px of a 368px anchor) and placed by
`justify-content` — which, in an LTR flex container, is the left edge. `text-align: right` cannot
move a flex item, which is why the second attempt measured right and still rendered left.

The fix keeps the anchor **RTL** (so flex-start is the right edge) and makes only the digits LTR:

```css
.zs-footer__contact a[href^="tel:"]{direction:rtl;justify-content:flex-start}
.zs-footer__contact a[href^="tel:"] .elementor-icon-list-text{direction:ltr;unicode-bidi:embed}
```

Verified at 1440: all three contact glyphs end at 481, the menu column at 897, and the number
still reads `055-4309532`. At 375 the footer stacks centred with no overflow.

**Worth keeping:** this is a generic consequence of Elementor's icon-list markup plus an RTL site
with LTR phone numbers. Any Zap client with a `tel:` link in an icon-list has it.

### The actual footer fault: three columns, two alignments

Fixing the phone's bidi placement was real but it was **not** what looked wrong. Measuring the
whole band rather than the one column found it:

| column | `text-align` | content edge (at 1920) |
|---|---|---|
| brand + description | **center** | logo centred at 1321-1417 |
| הוילה menu | start | 1137 |
| יצירת קשר | start | 721 |

One centred column sitting between two start-aligned ones, so nothing lined up down the band.
Now every column is `align-items: flex-start` / `text-align: start` at 1025px and up, the logo and
group mark lose their auto margins, and the three content edges land at 1553 / 1137 / 721 — three
equal 368px columns on a 48px gutter.

**The lesson for next time:** two rounds were spent fixing the thing named in the complaint (the
contact column) when the fault was the column beside it. Measure the whole band before fixing the
part that was pointed at.

## Footer design pass (desktop only, >=1025px)

Alignment was correct and it still read badly. The fault was **equal widths for unequal content**:
a logo plus a two-line paragraph, seven links, and three contact lines all forced into 368px,
which left a ragged bottom and dead space under two of the three columns.

| | before | after |
|---|---|---|
| column widths | 368 / 368 / 368 | **474 / 335 / 279** |
| column heights | 166 / 301 / 149 | **166 / 198 / 162** |
| menu | one 7-item stack | two columns, **column-major** |

- Tracks are proportional to content. **The row is a CSS grid, not flex** — `flex` on the children
  computes and does nothing; the tracks live on the parent as `grid-template-columns`. That cost a
  round: the values were applied and inert.
- The menu is `grid-auto-flow: column` with four rows, so it still reads 1-7 **down** the first
  column and then the second. The obvious `grid-template-columns: repeat(2,1fr)` flows row-wise,
  which scrambled a nav list into 1,3,5,7 beside 2,4,6.
- One heading treatment (18px below), one item rhythm (11px), 1.6 line-height, the brand paragraph
  capped at 42ch so it breaks on a comfortable measure.
- A hairline above the legal bar so copyright, legal links and the group mark read as their own
  register rather than a fourth column.

Everything is inside `@media (min-width:1025px)`. Verified at 375: the menu is a plain stack again,
no horizontal overflow, footer height unchanged.

### Correction: even thirds, not content-proportional

Sizing the tracks to their content (474/335/279) fixed the ragged bottom but read as **lopsided** —
unequal widths look like a mistake even when the reasoning behind them is sound. Reverted to equal
thirds and kept everything else:

| | ragged original | content-proportional | **now** |
|---|---|---|---|
| widths | 368 / 368 / 368 | 474 / 335 / 279 | **357 / 357 / 357** |
| heights | 166 / 301 / 149 | 166 / 198 / 162 | **166 / 219 / 168** |

The thing that actually fixed the ragged bottom was the **two-column menu**, not the unequal
tracks: it halves the tallest column. With equal widths and that menu, the spread is 53px instead
of 152px, and the band reads as a deliberate grid. Gutters widened to 64px, heading gap 20px, item
rhythm 13px.

### Final shape: brand on its own row

Three attempts at balancing a three-column band all read wrong, so the shape was put to the user
rather than guessed at a fourth time. The chosen layout:

```
[logo]  הוילה הלבנה ינוב          ← full width, 1200px
וילה פרטית לנופש ומתחם לאירועים…
──────────────────────────────── ← hairline
יצירת קשר            הוילה        ← two 568px columns
055-4309532          דף הבית  גלריה
shimon@…             אודות    בלוג
מורד התאנה 29        וילה…    צרו קשר
```

The brand column spans `grid-column: 1 / -1` with a hairline beneath it; the menu and contact
share a two-track row (568px each, 64px gutter) with the menu keeping its column-major pair of
sub-columns. Heights beneath the rule are 219 and 168.

This removes the thing that kept reading as lopsided: a short brand column standing beside two
lists it had nothing in common with. Nothing is centred, nothing is proportionally sized, and the
only full-width element is the one that earns it.

Verified at 375: a single 335px track, three stacked blocks, no horizontal overflow, footer height
unchanged. All of it is still inside `@media (min-width:1025px)`.

**Process note.** Three rounds were spent adjusting a layout against my own taste while the user
kept saying it was wrong. Offering three concrete shapes and letting them choose settled it in one.
When a design is rejected twice, stop tuning and present alternatives.

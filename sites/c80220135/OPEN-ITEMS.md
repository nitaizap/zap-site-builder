# Open items — מרכז שירות יד מרדכי (80220135)

Collected during an automatic-mode build. Nothing here was asked mid-work; each item was defaulted the
safest way and recorded. Items 1 and 2 need someone's decision, the rest need a fact or a file.

## 1 · Package: the spec says no package, and "בייסיק" does not fit the spec's own page list

`intake.json` has `package: ""` and the file name names none. The build was told to treat it as standard
בייסיק scope. The spec sheet, however, sets `סוג הפרויקט` to "אתר מלא – אתר תדמיתי" and then lists nine
pages (home, אודות, six services, צרו קשר). The engine's `basic` package caps a site at five pages and
forbids several sections, so בייסיק and the spec's page list cannot both hold.

**Default taken:** `tier: standard` (cap 12 pages), which matches "אתר מלא" and delivers every page the
spec lists. If the client was in fact sold the בייסיק package, the page list has to be cut to five before
launch, and that is a commercial decision, not a build one.

## 2 · The gates were blocked, then run (resolved)

The environment's network policy denied `wordpress.org` at first, so `zs build` could not provision the local
WordPress. The user opened network access to full and everything below was then run for real:

| gate | result (that session) | re-run here 03/11 |
|---|---|---|
| `zs qa c80220135` | 0 errors, 4 warnings | **0 errors, 0 warnings**, exit 0 |
| `zs seo c80220135` | 0 FAIL | **0 FAIL** (39 rows: 34 pass, 5 manual) |
| `zs pool c80220135` | exit 0, 37% | **36%** against `c80386843`, exit 0 (it had risen to 40%, an ERROR; see item 17) |

The 4 warnings are accounted for in item 4 and the 40% in item 17. The re-run was done in a fresh worktree
on a Windows machine: `.tools/` (php, wp-cli, MariaDB) is gitignored and per-checkout, so it was copied from
an existing checkout before `bin/zs build` would run at all.

Two environment quirks worth knowing for the next cloud session, neither of them a site problem:

- `bin/setup-cloud.sh` installs a Chromium that the pip `playwright` (1.64.1) does not look for. Symlinking
  `/opt/pw-browsers/chromium-1243` and `chromium_headless_shell-1243` to the `-1248` names fixes it.
- WordPress's own installer refuses `downloads.wordpress.org` because the host resolves to the agent proxy and
  `wp_safe_remote_get` rejects it as a private address, so `wp plugin install` and `wp theme install` fail with
  "A valid URL was not provided". Seeding wp-cli's cache with curl works:
  `~/.wp-cli/cache/plugin/<slug>-<version>.zip` and `~/.wp-cli/cache/theme/<slug>-<version>.zip`.
  The Hebrew language pack hits the same wall and fails **silently** (`check=False`), which leaves a Hebrew
  site rendering LTR end to end. Unzip `downloads.wordpress.org/translation/core/6.2.15/he_IL.zip` into
  `wp-content/languages/` and set `WPLANG`. Flagged on PR #59.

## 3 · The business has no logo anywhere (searched), and the favicon is a stand-in

The spec states "אין לוגו לעסק". That was checked against every source available, not just the F: drive:

| source | what is there |
|---|---|
| `assets/client/` (25 files from F:) | marque logos and the המחלקה הראשונה badge only, no business logo |
| the client's own site, ym-mazdaford.co.il | the brand is **live styled text** ("מרכז שירות / יד מרדכי", blue, two lines), not an image. Its only logo files are the Mazda/Ford strip, the המחלקה badge and Zap's own platform logo |
| Facebook (facebook.com/ymmazdaford) | the profile picture is a **photograph of the pylon sign**, not a logo. A higher-resolution shot of the same sign is already in `assets/pylon.jpg` |
| Instagram | behind a login wall, not readable |
| Dapei Zahav (d.co.il/80220135) | blocks automated reading; not circumvented |

So the finding is confirmed rather than assumed: **no designed logo exists**, and the client's own site solves
it exactly as this build does, by setting the name as type. The header and footer render the business name as
text, and nothing was drawn or traced from the photograph of the sign.

`zs qa` fails a site that keeps the cloned base install's favicon, so `assets/favicon.png` is a **stand-in**:
the brand petrol tile with the initials YM, nothing more. It is not a logo and should be replaced the moment
the client supplies artwork.

**Needed from the client:** a wordmark or logo file (PNG, transparent). Then set `logo` and regenerate
`favicon` from its symbol, and header, footer and favicon all follow from the one file.

**Decision, 03/11/2026 (recorded, no longer open): the header stays as the styled business name, with no logo.** The user was asked to put "the garage's own logo" in the header, reviewed the finding and decided to leave it. The last chip in the "מורשים מטעם היבואן" band is the importer's *המחלקה הראשונה למסחריות* programme badge (`logo-first-dept`), not a mark of the garage, so it is deliberately not used as the client's identity (it would also have become the footer, favicon and structured-data logo). No wordmark was drawn. The band keeps the badge beside the text, with the four marques in a 2x2. The only thing that changes this is a real logo file from the client (see "Needed from the client" above).

## 4 · Reviews: on (resolved)

The spec asks for a customer-reviews area and it is now built. `business.dpz_customer_id` is `80220135` and a
`reviews` section sits on the home page after the licence facts, so the evidence runs licences, then what
customers say, then the services.

The id was verified rather than assumed: the Zap reviews API returns a real review for it (a service visit,
dated 20/10/2024) and every link in that payload points at `https://www.d.co.il/80220135/`, which is this
client's own listing from `intake.json`. The client's existing site shows the same listing, 4.84 from 31
reviews.

### The four QA warnings in the previous report were this widget, and they are gone (03/11)

`QA-REPORT.md` previously carried **4 warnings**, all of them the same thing: two console errors on the home
page (`Access to fetch at 'https://api.zap360.co.il/api/zap-widgets/reviews' ... blocked by CORS` and
`Failed to load resource: net::ERR_FAILED`), counted once for desktop and once for mobile. They were **not a
site defect**: the cloud session that built this client could not reach the reviews API, so the browser logged
the blocked request and `zs qa` reported each console error as a warning.

Re-measured on 03/11 from a machine with ordinary network access, the API answers, the widget loads, and the
report reads **0 errors and 0 warnings**, with the engine's own check `✅ reviews widget styled (stars in one
row, review in body text)` passing for the first time. Nothing was suppressed or allowlisted to achieve that.

What remains true, and is the one thing to re-check after the first push: the widget needs a real host, so if
a future QA run is done from a restricted network these two console lines will come back. They are the
network, not the page.

Two things to know:
- **the widget renders only on a pushed site** (or from a host that can reach the API). Where the API is
  blocked the block is empty in the screenshots; it was additionally checked by answering the request with
  the real payload: one review card, stars in a single row, a muted date, page chips and both Dapei Zahav
  links, which is what the standard describes.
- no score or review count is written anywhere in the copy, and none ever should be: the widget draws its
  own, and the validator blocks typed ratings.

## 5 · All four marque logos are shown, and the Mazda one was wrong until 04/11 (resolved)

The spec asks for the marque logos together, at a uniform size and equal spacing, in the order
**מאזדה | פורד | דונגפנג | וויה** reading left to right. That is what the band does, on desktop and on phones,
with the המחלקה הראשונה למסחריות badge beside them.

**The correction.** The spec sheet attaches its own logo files, and the `brief.md` text export silently drops
embedded images, so the first pass worked from the text alone. Opening
`brief/איפיון אתר - מרכז שירות יד מרדכי - 80220135_1.docx` as a zip shows three PNGs in `word/media/`: the
current **Mazda** lockup, **Dongfeng** and **Voyah**, sitting in the document right under the line
"להשתמש רק בלוגו המעודכן של מאזדה (המצורף), ולא בלוגו הישן". The band had been built with
`Logo_FullColor_Horizontal.png` from the `F:` folder, which is the **old** chrome-and-gradient Mazda
wordmark — the exact logo that line forbids. All three marks now come from the client's own attachments;
Ford still comes from the existing site, which is what the spec asks for. The previous open question, "which
file is the updated Mazda logo", is answered: neither of the `F:` candidates, it was attached to the spec.

**Sign-off, no longer outstanding in substance.** Marque logos are trademarks, so the question is permitted
use rather than a photographer's copyright. An authorised centre showing its own marques is ordinary
practice, the client's existing site already does it for Mazda and Ford, and the client supplied Dongfeng and
Voyah itself inside the spec sheet, which is the client instructing the build to use them. Worth a line in
the handover, not a blocker.

**A build warning that is a false positive, left as is:** `zs build` may print
`images 'logo-x' and 'logo-y' look like the same shot`. The near-duplicate detector is comparing marque marks
that are mostly empty transparent canvas, so they share a shape and a lot of blank space. They are different
files showing different marques. Nothing to fix; do not "keep one".

## 6 · No blog, because the spec does not ask for one

Both `אתר SEO (בלוג)` and `מאמרים` are empty on the spec sheet, so no blog page, no categories and no posts
were built. The validator warns about this and the Zap SEO checklist wants a blog category with three posts
on every site. If a blog is in scope, three posts can be written from the client's own material already in
the spec (the four marques and what each licence covers, the original-parts programme, what the service
advisor does) without needing any new fact.

## 7 · Privacy policy fields not confirmed

The privacy page is built from Zap's standard wording with `legal_name: "מוסך יד מרדכי"`,
`privacy_database: false` and `privacy_email: musach@y-m.co.il`. `standards.privacy_confirmed` is **not**
set, so it stays a launch blocker until the client confirms those fields.

## 8 · Facts that were wanted and are not available

- **Geo coordinates and the Google Maps CID.** Not set, so the contact map falls back to the address string
  and the schema carries no `geo` or `hasMap`. The Dapei Zahav page would have given both; it is blocked.
- **Google Business Profile URL.** The spec leaves `Google My Business` empty.
- **LinkedIn.** Empty on the spec. No bar item was invented.
- **Zap tracking number (מספר מקשר זאפ): the spec says none, the existing site uses one.** This needs a
  decision before launch. The spec leaves מספר מקשר זאפ empty and gives 08-6720513 as טלפון לאתר, which is
  what this build shows, with `phone_is_virtual` false. But the client's current site displays
  **072-3263207** on its home page, labelled "מספר מקשר" with Zap's "הסבר" link, and falls back to
  08-6720513 on its about and contact pages. So a tracking number for this client already exists.
  The playbook's rule is that the site shows the Zap number, confirmed once. Nothing was changed here,
  because the display phone is a business fact and the spec states it explicitly.
  **If the sites team confirms 072-3263207**, set `phone_display: "072-3263207"`,
  `phone_e164: "+972723263207"`, `phone_is_virtual: true` and `phone_regular: "08-6720513"`; the engine then
  adds the "מספר מקשר" link and Zap's standard explanation popup.
- **Years in business.** The spec contradicts itself ("מעל 30 שנה" against a 1950s founding). No number of
  years is claimed anywhere on the site.
- **Gallery.** The spec says "לקחת תמונות מהאתר הקיים". The existing site was read in the end
  (`bin/zs grab`, output in `research/`) and it yielded **no new photographs**: its images are the same 2022
  facade and pylon shots already in `assets/`, just cropped to banner sizes, plus one Ford/Mazda manufacturer
  stock composite that is not the client's own material and was not used. So the seven F: drive photographs
  really are everything. That is below the 13+ the playbook wants, and three of them are 800×600 from 2020.
  The Instagram account in `intake.json` is the remaining source, and it needs a login to read.
- **Owner photo.** `תמונת בעלים` is empty on the spec; no portrait is used and none was generated.
- **כתבת תדמית.** Empty on the spec; nothing was written in its place.

## 9 · One photograph shows an identifiable person

`assets/waiting.jpg` (the waiting room) has a seated man in it, clearly recognisable. It is the client's own
material and the only photograph of the waiting room the brief describes, so it is used on the home page and
the about page. Worth one confirmation that he consents, or a replacement shot.

## 10 · Smaller build decisions

- **No services hub page.** The spec lists the six service pages flat, so they sit at the top level and the
  main menu has nine items. A hub was not invented. With nine items the desktop menu may want checking at
  1440 px; that check needs item 2 resolved.
- **Staging.** `staging_url` is empty, as expected. Nothing was pushed, nothing was published, no staging
  host was contacted.
- **Dream from Steel (80386843)** was not touched.

## 11 · Decisions taken during the build, for the record

- **The menu was restructured.** Nine top-level items (home, about, six services, blog, contact) did not fit a
  laptop header: at 1280 px the menu collided with the business name. The six service pages now sit in one
  dropdown, "השירותים שלנו", which points at the services block on the home page. Five top-level items fit
  from 1025 px up. Every page is still reachable from the main menu, as Zap QA requires, and the page URLs
  did not change.
- **A blog was added after all.** OPEN-ITEMS 6 below explains that the spec asks for none, but `zs seo` fails
  a site without a blog category and three posts. Three posts were written **only** from material already in
  the spec: the service intervals and the booking flow, the original-parts programme, and what the computerised
  diagnosis does. No new business fact was introduced. If the blog is out of scope commercially, delete the
  `בלוג` page, the category and the three posts from site.json; the rest of the site is unaffected.
- **The footer colour moved** from near-black to a petrol charcoal (`#0e2a30`) because the uniqueness measure
  put the home page at 38% against white-villa, and the footer colour is one of the signals it weights most.
  It read 37% then. **Superseded on 03/11** by the palette change in item 17: the whole palette is petrol now,
  and the footer is `#0d3a44`.
- **The marque logos were re-cut** onto one shared 3:1 canvas so all three chips render at exactly 200×80 with
  equal spacing, which is what the spec asks for ("בגודל אחיד ובמרווחים שווים"). The source files have very
  different proportions and rendered at 252, 182 and 155 px wide before this. Their order was also reversed so
  that reading left to right gives Mazda, Ford, then the commercial-vehicles badge, as the spec specifies.

## 12 · Cosmetic, worth one look

The accessibility toolbar's **desktop** button overlaps the header's phone button by about a 12 px corner. The
phone button still takes a click at its centre and `zs qa` passes, so it was left alone rather than moved for
every client: two Zap QA reviewers have already disagreed about where that button belongs. Mentioned on PR #59.

## 13 · What the client's existing site confirmed

Read with `bin/zs grab` once the network opened; the pages and images are in `research/`. Every factual claim
on the new site was cross-checked against it and **none of them had to change**: the 1996 Mazda licence from
דלק מוטורס, the 2000 Ford licence, the kibbutz ownership and ערן שטרנברג's management, the roughly 13 staff,
the air-conditioned waiting room overlooking the workshop, the VIP service with the lift home, and the 45%
original-parts programme for vehicles over 3 years all appear there in the client's own words.

Two differences, both expected: the old site names only Mazda and Ford, because it predates the 2025 Dongfeng
and Voyah licences the spec adds; and it lists the services without the separate pages the spec now asks for.

## 14 · The top strip is on, against the engine's default — one reviewer decision

`header.topbar` is **on**, showing "אשקלון והסביבה · מורשה מטעם היבואן למאזדה, פורד, דונגפנג ווויה".
The engine turns it off by default, and `references/qa-rules.md` (Round 2) records a reviewer asking to
"remove the blue strip with the details". It is a per-site option, not a prohibition, so this is a judgement
call rather than a rule break, and it is written down here rather than left for the QA round to find.

Why it stayed, honestly:

- the note first written in NOTES.md ("no other client turns the bar on") was **wrong**: four of the five
  measured clients run one. That reason is gone;
- it carries real content (service area + the four authorised marques) that the strip states compactly;
- turning it off was measured and made the site **more** like another client, not less: the nearest neighbour
  `c80386843` has no top strip, so removing ours moved the pair from 40% to 44.5% alike. That is the opposite
  of what this site needs.

**Needed from the team:** one word on whether this client's reviewer accepts a top strip. If not, turn
`header.topbar` off in `site.json` and re-run `bin/zs qa` — but expect the uniqueness score against
`c80386843` to rise, so a different lever (the lead band's ground, or its palette) has to come off at the
same time.

## 15 · Nothing was pushed, and nothing can be

`staging_url` is still empty for this client, so `zs push`, `zs connect` and publishing were all out of scope
and were not attempted. Everything above was measured on the local build only. The items that can only be
confirmed on a real host are: the reviews widget on the live page (item 4), the Elementor Theme Builder
templates after a first push (`qa-rules.md` → "Editable everywhere"), `robots.txt` opening on the client's
own domain, and the 301s from the old site's URLs (item 13).

## 16 · The six service pages are thinner than Zap QA's own bar, and the material to fix it does not exist

`references/qa-rules.md` (Round 3) sets the bar for a trade's service page at **450–800 words** with "the
client's own method, numbers and FAQ", and marks it as a human's judgement rather than a gate. No gate
catches it: `zs qa` is 0 errors, `zs seo` is 0 FAIL and the validator is silent. Measured from `site.json`
(prose, card and FAQ text, headings excluded where they are furniture):

| page | words | bar |
|---|---|---|
| מכונאות רכב | 316 | 450–800 |
| מערכות מיזוג אוויר | 273 | 450–800 |
| פחחות וצבע | 268 | 450–800 |
| דיאגנוסטיקה ואבחון | 267 | 450–800 |
| חשמל רכב | 260 | 450–800 |
| צמיגים | 224 | 450–800 |

For comparison the home page is 698 words and אודות is 266.

**Why this was not simply written longer.** Every service page already uses all of the spec's own wording for
that service, and the client's existing site was read in full (`research/ym-mazdaford.co.il.md`): it is
**946 words in total** across every page and mentions each service only three to five times, in passing. There
is no further client material anywhere — not in the spec, not on the old site, not in the F: drive folder.
Reaching 450 words per page means adding roughly 180 words six times over, and the only way to do that here
would be to invent method, timings or numbers for a motor garage. That is the one thing the build rules
forbid outright, and it is the kind of invention Zap QA catches on a factual read.

**Needed from the client (one short call would cover all six):** per service, what the garage actually does
step by step, how long it typically takes, what equipment or approval is involved, and one or two real
numbers. With that, each page reaches the bar honestly in a single pass. Until then the pages are accurate
and short, which is the safer of the two failure modes but is still a likely QA comment.

## 17 · The uniqueness gate had actually failed, and the palette was changed to clear it (resolved)

When this client was handed over the note said "pool 39%, passing but fragile". Re-measured on 03/11 it was
no longer passing: `bin/zs qa c80220135` exited **2** with

```
ERROR home looks 40% like 'c80386843' (measured: palette, furniture, components, layout)
WARN  home is 37% like 'mehirut-haor' / 36% 'white-villa' / 35% 'patoccina'
```

`c80386843` (Dream from Steel) is one of the four clients being built alongside this one, so the pool moved
under it. 40% is the ERROR threshold, not a warning.

**Where the 40% came from** (the measure weights palette 30%, furniture 25%, vocabulary 20%, skeleton 15%,
frame 10%): the two sites' footers measured 0.86 alike on their own, because a graphite `#1f2529` footer and
a steel-navy `#16222c` footer are the same colour to a visitor. Both are industrial trades, and the build had
drifted to a graphite primary (`#333b41`) that had nothing to do with this client.

**What changed** — four values in `design.colors`, nothing else:

| token | was | now | why |
|---|---|---|---|
| `primary` | `#333b41` graphite | `#14525e` petrol | the colour of the building in the client's own 2022 photos, which is what NOTES.md reasoned from in the first place. It is also the heaviest single signal in the measure (the action button) |
| `dark` (footer) | `#1f2529` | `#0d3a44` | the collision above |
| `surface` | `#f4f4f3` | `#e3edef` | a petrol tint, so the lead band and the FAQ tiles read as a ground instead of as white |
| `muted` | `#4e575e` | `#41505a` | darkened so body text keeps 6:1 on the new tinted surface (measured 6.99:1) |

No section, variant, image, word or threshold was touched, and nothing under `fingerprints/`.

**Result, measured here:** `bin/zs qa c80220135` **0 errors, 0 warnings, exit 0**, and the only neighbour
still reported is `c80386843` at **36%**. Every other client fell below the 35% reporting line.

Contrast was checked on the new palette before the rebuild: white on primary 8.76:1, white on the footer
12.31:1, body text on surface 12.86:1, muted on surface 6.99:1, white on the bronze accent 5.02:1.

**One piece of history that matters.** Petrol was this site's *first* palette, and it was abandoned because
`c80386843` had independently picked petrol-and-bronze too and the pair measured 58% alike. That is no longer
the situation: `c80386843` has since moved to burnt orange `#b84606` with a steel-blue accent, which is what
makes petrol the right answer again rather than a step backwards. It also means this particular lever is
**contingent on that site**: if Dream from Steel moves back toward petrol before either site is delivered,
this one has to move again, and the lever to reach for then is the lead band's ground, not the palette.

**Worth knowing:** three more clients join this pool shortly. 36% leaves about four points of room, and the
cheapest remaining lever if it tightens again is the lead band's ground (moving it off `stack/light` is worth
about four points on its own). Turning the top strip off is **not** a lever here: it makes this site more
like `c80386843`, not less (item 14).

## 18 · Theme bug: the prose column was never centred (resolved on `main`, 04/11)

`wp/theme/zap-base/assets/main.css:317` sets `body .e-con.zs-prose { max-width: 760px; }` with no
`margin-inline: auto`. Only `.zs-p-signature` adds one (`main.css:738`). Every other template therefore pins
the 760px column to the start edge of its 1200px container, which in an RTL site means the text sits hard
against the right and leaves roughly **440px of dead ground on the left**. Measured on this site at 1440 on
04/11: the prose container on `/מכונאות-רכב/` has `left: 560px, width: 760px` inside a 1200px inner.

It was on every page the engine builds with a `prose` section, not just this client, which is why it was not
fixed from this session. **Fixed on `main` in PR #86** (`1aa7aa2`): `.zs-prose` now carries
`margin-inline: auto` in `main.css`. The per-client workaround
(`body .e-con.zs-prose { max-width: 820px; margin-inline: auto; }`) **was deleted on 04/11** so the two rules
do not stack. Re-measured at 1440 after deleting it: the column sits at `left 333px / right 348px` on אודות
and on all six service pages, the 15px difference being the scrollbar. The site keeps the theme's 760px
measure rather than the 820px the workaround had set.

## 19 · The brief's `.docx` carries three images the `brief.md` export dropped (resolved, see item 5)

Recording the mechanism, because it is not specific to this client: `brief/brief.md` is a text export and it
drops embedded images **without leaving a marker**. This brief's `.docx` holds three PNGs in `word/media/`
(Mazda, Dongfeng, Voyah), and one of them contradicted what the site had been built with. Any future brief
should be opened as a zip and `word/media/` listed before the text export is trusted. Checked here on
04/11: there is **no business logo** among them, so item 3's finding stands on the file itself.

## 20 · Plugin bug: the map widget rendered nothing (resolved on `main`, 04/11)

The spec's `צרו קשר` line asks for "טופס לידים, טלפון, כתובת ומפה". The page is built with
`contact` + `map: true`, the engine emits the `zap-map` part widget, and on the pushed site that widget
produces **an empty `<div class="zs-contact__map">`**: no iframe, height 0. Verified on
https://80220135yadmordechai.ussl.co.il/צרו-קשר/ on 04/11 (`document.querySelectorAll('iframe')` is empty and
the container measures 572x0), and in the page's served HTML.

**Cause, and it is not this site.** `wp/plugin/zap-site/inc/elementor-widgets.php`, `render()`, builds its
shortcode attributes from every control in the widget's spec and casts each to a string:

    $atts[$key] = ... : (string) $v;

so a blank `q` is passed as `q=""` rather than omitted. `inc/shortcodes.php`, `zap_map`, then does

    $a = shortcode_atts(['q' => zap_opt('business.address')], $atts);
    if (!$a['q']) return '';

`shortcode_atts` treats the explicit `''` as a supplied value, so the default never applies and the shortcode
returns an empty string. The control's own label says "ריק = כתובת העסק", which is precisely the behaviour
the code prevents. `business.address` is set on this site (`קיבוץ יד מרדכי`), so the fallback would work.

**Every site that uses the map widget without someone typing an address into Elementor by hand has an
invisible map.** The legacy `[zap_map]` shortcode is unaffected, which is why older sites still show one.

**Fixed on `main` in PR #86** (`1aa7aa2`), and generally rather than for `q` alone: a blank control is no
longer passed to the shortcode at all, so each shortcode's own default wins (the map gets `business.address`,
the form gets id `main` and the site's button text, the post lists get their counts).

**What this site did in the meantime, and no longer does.** `design.custom_css` used to hide a
`.zs-contact__map` with no element children and collapse the contact row to a single centred column. After
the merge that workaround would have fought the real map, so it **was deleted on 04/11**. Verified after
rebuilding: the contact page serves
`<iframe src="https://www.google.com/maps?q=קיבוץ יד מרדכי&output=embed&hl=iw" title="מפת הגעה: מרכז שירות יד מרדכי">`,
the address coming from `business.address` with nothing typed into Elementor by hand.

One thing did have to be added in its place. The details column carries the NAP list **and** the lead form
and runs far taller than a 4:3 map, so the map stopped halfway and left roughly 450px of bare page beside
the form. The contact grid now stretches its rows and the map fills its column
(`align-items: stretch` + `height: 100%` down the widget chain, `min-height: 560px`). Measured at 1440:
map and form both end at 1599px. Below 900px the theme already stacks the two columns and the map's own
aspect ratio takes over, so the rule is wrapped in `@media (min-width: 901px)`.

## 21 · Second quality pass, 04/11 (what changed, and what is still open)

Run after merging `main` at `1aa7aa2`. `zs qa` 0 errors / 0 warnings, `zs seo` 0 FAIL, `zs pool` no warning
(highest measured likeness 33%, limit 40%).

**Deleted** (both were workarounds for faults `main` has now fixed, and both would have fought the fix):
the `.zs-prose` centring rule (item 18) and the empty-map collapse (item 20).

**Added or changed:**

1. The contact grid stretches so the map fills its column beside the form (item 20).
2. The top strip reserves 56px of inline-end room between 1025 and 1439px. The accessibility toggle is
   fixed in the viewport's left corner and is 52×52; the strip is only 38px tall, so the toggle covered its
   left-hand item entirely. Measured before: leftmost content at 0px (1100), 8px (1280), 51px (1366).
   After: 56px or more at every width. `main`'s own fix covers the header row below the strip, not the strip.
3. The six service pages no longer say the same sentence twice at the top. The hero keeps the spec's own
   wording and the first prose paragraph was rewritten to add something. On פחחות וצבע and
   מערכות מיזוג אוויר the spec's punchier line moved into the hero instead. Three paragraphs further down
   those pages lost a clause that the new opening had made repetitive. No new business facts.
4. The service pages' FAQ is now `faq:aside`: a `שאלות נפוצות` heading and the questions beside a tall
   photograph, so a service page reads hero → text → image band → form. Before this, six of the nine pages
   had no picture at all below the hero and the questions stretched the full 1440px.

**Still open after this pass:** items 1, 3, 6, 7, 8, 9, 12, 15, 16 are unchanged, and the two that need the
client are item 16 (service-page depth: one twenty-minute call with ערן שטרנברג) and the gallery gap
recorded in `BRIEF-CHECK.md` (new photographs at 1600px or wider, of work actually being done). Neither can
be closed from here, and neither is closed by the client's own Facebook or Instagram: both were read on
04/11 and give a logged-out reader nothing beyond the profile name and a grid of thumbnails.

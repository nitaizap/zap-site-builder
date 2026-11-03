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

| gate | result |
|---|---|
| `zs qa c80220135` | **0 errors, 0 warnings** |
| `zs seo c80220135` | **0 FAIL**, every MANUAL row looked at (NOTES.md) |
| `zs pool c80220135` | exit 0, **37%** against the nearest other client (limit 40%) |

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

## 4 · Reviews: on (resolved)

The spec asks for a customer-reviews area and it is now built. `business.dpz_customer_id` is `80220135` and a
`reviews` section sits on the home page after the licence facts, so the evidence runs licences, then what
customers say, then the services.

The id was verified rather than assumed: the Zap reviews API returns a real review for it (a service visit,
dated 20/10/2024) and every link in that payload points at `https://www.d.co.il/80220135/`, which is this
client's own listing from `intake.json`. The client's existing site shows the same listing, 4.84 from 31
reviews.

Two things to know:
- **the widget renders only on a pushed site.** Locally the browser blocks its API call (CORS from
  127.0.0.1), so the block is empty in the preview screenshots. It was checked by answering the request with
  the real payload: one review card, stars in a single row, a muted date, page chips and both Dapei Zahav
  links, which is what the standard describes.
- no score or review count is written anywhere in the copy, and none ever should be: the widget draws its
  own, and the validator blocks typed ratings.

## 5 · All four marque logos are now shown (resolved), with one sign-off outstanding

The spec asks for the marque logos together, at a uniform size and equal spacing, in the order
**מאזדה | פורד | דונגפנג | וויה** reading left to right. That is now what the band does, on desktop and on
phones, with the המחלקה הראשונה למסחריות badge after them.

Mazda and Ford came from the client's own files. דונגפנג and וויה were not in them and were taken from
**dongfeng.co.il**, the Israeli importer's own site (both it and voyah.co.il carry Delek Motors' logo, and the
spec names דלק מוטורס as the importer that authorises this centre). Full provenance is in `IMAGE-SOURCES.md`.

All five were re-cut onto one shared canvas and scaled to **equal optical area** rather than a shared bounding
box: the source files run from 7:1 (Dongfeng) to 1.8:1 (Voyah), so fitting them into one box made the wide
wordmarks look tiny next to the round marks.

**Outstanding:** marque logos are trademarks, so the question is permitted use rather than a photographer's
copyright. An authorised centre showing its own marques is ordinary practice and the client's existing site
already does it for Mazda and Ford, but the importer's sign-off on דונגפנג and וויה is worth having before
launch.

Also still unresolved, and minor: which file is "the updated Mazda logo (המצורף)". Three candidates sit in
`assets/client` and they show the same artwork; `Logo_FullColor_Horizontal.png` was used, being the
highest-resolution horizontal one.

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
  It reads 37% now.
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

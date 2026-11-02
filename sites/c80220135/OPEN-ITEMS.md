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

## 2 · The build, QA and SEO gates could not be run in this session

This environment's network policy denies `wordpress.org`, `downloads.wordpress.org` and
`api.wordpress.org` (403 at the egress proxy, reproduced with curl and with wp-cli). `zs build` provisions
the local WordPress with `wp core download` plus the Elementor, Yoast and Ally plugins, so it exits before
it writes anything:

```
Error: RuntimeException: Failed to get url 'https://api.wordpress.org/core/version-check/1.7/?locale=en_US':
cURL error 56: CONNECT tunnel failed, response 403.
```

Everything downstream of the build is therefore **not run**: `zs qa`, `zs seo`, `zs preview`, `zs shots`,
`zs pool`, `fingerprint.json`. What *was* run is `engine/validate.py`, standalone, against site.json:
**0 errors, 4 warnings** (the four warnings are items 3, 4, 6 and 7 below).

What this leaves unverified, and nothing in this file substitutes for it:
- the uniqueness gate against `fingerprints/` (the 40% limit). The look was chosen to sit far from the five
  registered clients on the levers the measure weights most (palette first, then furniture, then
  components), and the kit and archetype are both unused by the last three clients, but **it has not been
  measured.**
- WCAG contrast as `zs qa` measures it. The palette was measured by script instead (ratios in NOTES.md);
  every value clears 4.5:1, and `muted` clears 7:1 on both grounds.
- the above-the-fold check at 1280×620 and 360×640, the mobile pass at 390 px, the heading/alt/link crawl,
  and every row of the SEO checklist.

**To finish:** allow `wordpress.org`, `downloads.wordpress.org` and `api.wordpress.org` under the
environment's Network access (cloud environment menu → Edit → Network access), then
`bin/zs build c80220135 && bin/zs qa c80220135 && bin/zs seo c80220135 && bin/zs pool c80220135`.
Note that this session also needed `~/.cache` symlinks for Playwright's browser; `bin/setup-cloud.sh`
installed a Chromium build that the pip `playwright` 1.64.1 does not look for.

## 3 · The business has no logo, so there is no logo and no favicon

The spec states "אין לוגו לעסק" and the F: drive holds no business logo, only the marque logos. The site
therefore ships without `logo` and without `favicon`: the header renders the business name as text.

Zap QA expects a logo in the header, a logo in the footer linking home, and a favicon made from the logo's
symbol. None of those can be met, and a logo must not be drawn or traced from the photograph of the sign.
**Needed from the client:** a wordmark or logo file (PNG, transparent), or a decision to keep the site
text-only in the header. Until then the cloned base site's favicon stays.

## 4 · "אזור חוות דעת לקוחות" cannot be built yet

The spec asks for a customer-reviews area on the home page. Reviews may only come from the Dapei Zahav
widget with a verified `dpz_customer_id`; inventing reviews, ratings or a score is forbidden and the
validator blocks it. The client id 80220135 is very likely the right customer id, and
`https://www.d.co.il/80220135/` is in `intake.json`, but that page could not be opened from this session
(item 2's network block) and Zap standards require the listing to be verified against legal name, street
and phone first, because a wrong id publishes another company's reviews.

**Default taken:** no reviews section at all, rather than an empty band. Add
`"dpz_customer_id": "80220135"` to `business` once someone has opened the listing and confirmed it, then
put a `reviews` section back on the home page (the `photo` variant over `facade-drive` suits it).

## 5 · Two brand logos are missing, and the brief asks for four

The spec is specific: show the marque logos together at a uniform size and equal spacing, left to right
**מאזדה | פורד | דונגפנג | וויה**, using only the updated Mazda logo supplied, and the Ford logo from the
existing site. The F: drive has Mazda and Ford. It has **no Dongfeng logo and no Voyah logo**.

**Default taken:** the band shows Mazda, Ford and המחלקה הראשונה למסחריות (which the spec also asks for),
and all four marques are named in the band's text, in the facts card with their licence years, in the FAQ
and on every service page. **Needed:** Dongfeng and Voyah logo files, after which they go into
`images` and into the `logos` section in the spec's order.

Also unresolved: which file is "the updated Mazda logo (המצורף)". Three candidates sit in `assets/client`
(`Logo_FullColor_Horizontal.png`, `Logo_FullColor_Vertical.png`, `SEM_ספטמבר-21_חדש_לוגואים.PNG`) and they
show the same artwork. `Logo_FullColor_Horizontal.png` was used, being the highest-resolution horizontal
one. Worth one look from whoever sent the spec.

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
- **Zap tracking number (מספר מקשר זאפ).** Empty on the spec, so `phone_is_virtual` stays false and the site
  shows 08-6720513 as the client's own number. If the sites team does assign a tracking number, set
  `phone_is_virtual: true` and `phone_regular: "08-6720513"`, which adds Zap's explanation popup.
- **Years in business.** The spec contradicts itself ("מעל 30 שנה" against a 1950s founding). No number of
  years is claimed anywhere on the site.
- **Gallery.** The spec says "לקחת תמונות מהאתר הקיים". The existing site is unreachable from this session,
  so the gallery is built from the seven usable F: drive photographs instead. Only seven real photographs
  exist, below the 13+ the playbook wants, and three of them are 800×600 from 2020; the Instagram account
  in `intake.json` would be the obvious source for more.
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

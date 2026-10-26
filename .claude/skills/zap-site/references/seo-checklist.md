# Zap SEO QA checklist — `zs seo`

The team's SEO QA sheet ("צ'קליסט SEO", 22/10/2026), made executable. `bin/zs seo <slug>` crawls the built site
and writes `sites/<slug>/SEO-QA.md`: every row of the sheet in order, ✅ PASS / ❌ FAIL / 👁 MANUAL / — N/A.
**Done = `zs qa` 0 errors AND `zs seo` 0 FAIL**, and every 👁 row looked at by you, with one line in NOTES.md.

| # | row | how it is checked / what the engine does |
|---|---|---|
| 1 | tracking number ("מספר מקשר") opens a popup | 👁 the engine has no popup; check the brief's Zap number and the example site14.clicksite.co.il |
| 3 | home "services" cards open the right service page | measured: every card link returns 200 and matches the card title |
| 4 | accessibility statement + privacy pages | measured: generated privacy page; accessibility = Zap's central statement linked from the footer |
| 5 | blog category with 3 relevant posts | blog page + category required (validator warns); the 3 posts arrive through BestLinks → 👁 until they do |
| 6 | every image < 100 KB, WebP | the engine converts and steps quality/size down to 100 KB; WordPress's resized copies are saved at quality 60 |
| 7 | ALT on every image | measured; validate.py also blocks a missing ALT |
| 8 | FAQ relevant to the company | 👁 read them against NOTES.md facts |
| 9 | the client's images from the spec form are used | 👁 compare with the client's folder |
| 11 | WhatsApp link: the client's number, new tab | measured on every link (N/A when the brief has no WhatsApp number: never invent one) |
| 12 | floating WhatsApp button on every page, new tab | theme: bottom bar on phones, round floating button on desktop; measured at 1440 and 390 |
| 13–14 | phone buttons match the number shown and use `tel:` | measured on every page |
| 15 | Hebrew slugs that follow the H1 | measured (blog/contact slugs are conventional); on a redesign of a ranking site keep the old slugs and 301 |
| 16 | no `/category/` in category URLs | engine removes the base; measured |
| 17 | posts at `/blog/%postname%/` | posts live under the blog page's path; measured when posts exist |
| 18 | privacy checkbox under every form, its link works | measured on every form |
| 19–21 | no 404s, no links to old addresses | every internal link crawled; for a redesign also map the old site's URLs to 301s |
| 22 | FAQ schema on service pages and posts | automatic from `faq` sections; measured |
| 23 | unique, good meta title per page | measured (duplicates fail) |
| 24 | unique meta description, 150–160 characters | measured; the validator warns outside 150–160; write them to length in `seo.description` |
| 25–29 | custom 404: home link, contact link, search box, main pages | theme `404.php`; measured |
| 30 | search results template listing posts | theme `search.php`; measured with a real query |
| +1 | phone, email, address match the spec | 👁 |
| +2 | Zap logo in the footer + link to Zap | measured |
| +3 | home H1 carries the client's name | measured (also a content rule: H1 = keyword + brand) |
| +4 | inner page differs from a post | pages are Elementor layouts, posts use the post template |
| +5, +7 | privacy/accessibility carry the right client name in title and text | measured on the privacy page; the accessibility statement is Zap's central page |
| +6 | mobile + 1280 laptop look right | `zs qa` measures 1440/390 and the hero at 1280×620; 👁 once at 1280 |
| +8 | form email and site name set correctly | leads go to `business.email_leads`; staging never mails the client |
| +9 | heading order H1 → H2 → H3, no H2 inside forms | measured on every page |
| +10 | the accessibility button shows (Zap standard) | measured in a browser. Ally 4 renders its button only after wp-admin → Ally → Connect (free); a client WordPress must be connected once |

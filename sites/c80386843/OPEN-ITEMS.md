# Open items — מסגרית Dream from Steel (80386843)

Collected while building, not asked one by one (the skill's automatic mode). Work continued on the best safe
default in every case; the default taken is written next to each item.

## Needs a decision from the client or the sites team

1. **Which phone number the site shows.** The spec sheet gives two: `טלפון לאתר 050-9254010` and
   `מספר מקשר זאפ 072-2594285`. The Dapei Zahav listing shows 072-2594285. The house rule
   (`references/qa-rules.md`, `playbook.md`) is that the site shows the Zap tracking number, so the site
   shows **072-2594285** with `phone_is_virtual` (the "מספר מקשר" link and Zap's explanation popup), and
   names **050-9254010** as the business's own line. WhatsApp goes to 050-9254010, as the spec asks.
   **Unresolved:** the spec explicitly labels the 050 as "טלפון לאתר". One line from Noam or Ofir flips it
   (`business.phone_display` / `phone_regular` in `site.json`, one rebuild).

2. **The package.** Not named anywhere in the mail or the spec sheet, and the spec's project type says
   "אתר מלא (כולל דומיין)". Built as the standard basic scope: no video, no hero slider, a restrained
   section set. **But `tier` is set to `standard`, not `basic`,** because the spec's own page list is six
   pages (home, 3 services, about, contact) and the basic package caps at five. Nothing else about the site
   needs the larger package. If the sold package really is בייסיק, one page has to go, and that is the
   client's call, not ours.

3. **Legal name for the privacy policy.** `business.legal_name` is set to the trading name
   "מסגרית Dream from Steel" because no registered name was given. `standards.privacy_confirmed` is false,
   so the privacy page is a launch blocker until the client confirms the legal name, whether a customer
   database is kept, and the contact address for privacy requests.

4. **Logo.** The client supplied none (spec §6 blank). The header and footer show the business name as text,
   which is legible and passes QA. A logo file replaces it in one place (Elementor → Site Settings → Site
   Identity) or by setting `logo` in `site.json` and rebuilding.

5. **Favicon is a placeholder.** With no logo there is no symbol to cut one from, and `zs qa` fails a site
   with no favicon. `assets/favicon.png` is a plain brass tile with the initials DS, made in this session
   (recorded in `IMAGE-SOURCES.md`). It is a stand-in, not a brand mark: replace it with one made from the
   real logo when that arrives.

## Reserved, waiting for the file

6. **Video frame on the home page (requested 02/11 during the build).** The client also bought an AI social
   promo video and it should appear on the home page. No file or URL has arrived, so nothing is rendered: an
   empty band would fail QA and look broken. The slot is **between the services cards and `split:overlap`**,
   i.e. index 4 of the home page's `sections` in `site.json`. When the URL arrives, drop in:

   ```json
   { "type": "video", "title": "הסרטון של מסגרית Dream from Steel",
     "youtube_url": "<the URL>" }
   ```

   then `bin/zs build c80386843 && bin/zs qa c80386843`. `tier` is already `standard`, which allows the
   `video` section (the basic package does not, a second reason item 2 matters). If the video is a file
   rather than a YouTube/Vimeo link, it can instead become the hero's own loop
   (`videos` + `hero.video`, mp4 under 6 MB, 4-8 s, no audio).

## Photographs: the thing this site is missing

7. **There is no portfolio, and none was invented.** The client sent no photographs: `F:\SiteContent\80386843`
   is empty, the spec sheet has no WeTransfer or Drive link, and the business has no site, Facebook or
   Instagram. The only image on the Dapei Zahav listing is a generic category cover, not their work.

   The site therefore has **no gallery**, by decision. The four images on it are AI atmosphere only (a
   workshop bay, a fabrication bench, raw stock, brushed steel) and none of them shows a finished product.
   Generating gates, railings or structures would have read as this client's portfolio, which
   `references/images.md` forbids. The footer carries the line
   "תמונות האתר הופקו בכלי בינה מלאכותית ואינן מציגות עבודות של העסק".

   **What to ask the client for, in one message:** photographs of finished work (the more unusual the
   better, since the whole site argues that the work is not standard), one photograph of the workshop, one
   of Ofir, and the logo file. Each one that arrives gets a row in `IMAGE-SOURCES.md`, and a real gallery
   section plus a `team`/`split` with the owner's photo can then go on the home and about pages.

8. **No further images were generated in this session.** The Weave budget stands where the intake session
   left it: **8 of 100 credits used**, all four images from 02/11.

## Smaller assumptions, no answer needed unless someone disagrees

9. **Blog.** The spec leaves "אתר SEO (בלוג)" and "מאמרים" blank, but the Zap SEO checklist fails a site
   without a blog category and three posts. Three posts were written from the brief's own material
   (choosing raw material, what to prepare before ordering, drawing to finished product). They state no fact
   the spec does not: no prices, no lead times, no materials the client did not mention.
10. **Service area** is written as כפר סבא exactly, never "והסביבה" or "השרון", because the spec names one
    area. The address city נווה ימין appears as the workshop's location.
11. **Delivery times** are never given as a number. The FAQ says the date is fixed with the quote and kept,
    which is the spec's own "ביצוע מדויק ובמועד".
12. **Process steps** (שיחה ואפיון, תכנון, ייצור, מסירה) are the spec's "מתכנון ועד למוצר המוגמר" and
    "כל פרויקט מטופל באופן אישי" written out. No step claims a service the client did not name: there is no
    claim of on-site installation anywhere.
13. **schema.org type** is `ProfessionalService`: schema.org has no metalworker type.
14. **No staging URL yet,** which is expected. Nothing was published: no `zs push`, no `zs package`. The
    site was built and checked locally only.

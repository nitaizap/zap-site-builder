# Open items — מסגרית Dream from Steel (80386843)

Collected while building, not asked one by one (the skill's automatic mode). Work continued on the best safe
default in every case; the default taken is written next to each item.

---

## ⬛ Read this first: what the client still owes, and what ships without it

**This site has no portfolio, and that is a decision, not an oversight.** Whoever publishes it is publishing
a metalworker's site with no pictures of metalwork, and should know that before, not after.

The client sent **no photographs at all**. `F:\SiteContent\80386843` exists and is empty, the spec sheet
carries no WeTransfer or Drive link, and the business has no website, Facebook or Instagram. Every one of
the five `F:` roots was searched, including the 7,271-client archive. The eight images on the site are AI
atmosphere only (material and process: a bench, raw stock, a weld bead, a workshop bay) and **not one of
them shows a finished product**, because a generated gate or railing on a metalworker's site reads as that
metalworker's own job. Full reasoning in item 7.

**Three things are needed from the client before this site is what it should be:**

| # | what to ask for | what it unblocks | detail |
|---|---|---|---|
| 1 | **photographs of completed work** — gates, railings, structures; the more unusual the better, since the whole site argues the work is not standard | a real gallery section on the home and service pages. Until they arrive there is none | item 7 |
| 2 | **a photograph of the workshop**, and one of Ofir | the about page's owner block, and a real image for the place the site keeps describing | item 7 |
| 3 | **the logo file at a usable resolution** (SVG, AI/EPS, or PNG ≥512px) | a crisp favicon and a header logo that holds up on a high-density screen. A 140x140 copy is in use now, recovered from the client's Dapei Zahav listing, and it is the largest that directory serves | item 4 |

A fourth file is bought and promised but has not arrived: the **AI social promo video** for the home page
(item 6). Its slot is reserved and documented; nothing renders until the URL comes.

**And one thing nobody has resolved:** the site displays **072-2594285** while the spec sheet's "טלפון
לאתר" is **050-9254010**. The 072 is a Zap מספר מקשר — a Maskyoo-style tracking line that forwards to the
business — and it is the only number on either Dapei Zahav listing. The build follows Zap's standard and
displays it, with the 050 named in the explanation popup and used for WhatsApp. **The client has never
confirmed this themselves.** It is flagged, not settled: see item 1 for exactly what was assumed and on
what evidence, and raise it with Ofir before go-live.

---

## Decided (Nitai, 02/11) — closed, no action left

1. **The site shows the Zap tracking number.** Confirmed: `phone_display` is **072-2594285** with
   `phone_is_virtual`, so every page carries the "מספר מקשר" link and Zap's standard explanation popup
   beside it. **050-9254010** stays as `phone_regular` (the business's own line, named in that popup) and as
   the WhatsApp number, which is what the spec sheet asks for WhatsApp.
   This is also what the public record shows: the only contact button on either Dapei Zahav listing for this
   customer id is the 072 number, and the page itself says Zap routes it as a virtual number. The spec
   sheet's "טלפון לאתר 050-9254010" is therefore treated as the business's line, not the display number.
   Already built this way; nothing to change.

2. **Six pages stay.** Confirmed: the spec sheet's own page list is kept in full (home, מסגרות בהתאמה
   אישית, ייצור מוצרי מתכת ייחודיים, תכנון מוצרי מתכת, אודות, צור קשר), plus the blog, privacy and the
   accessibility statement, which do not count against the package. `tier` stays **`standard`**, because the
   basic package caps at five pages and would force one of the spec's pages off the site.
   If anyone later asks why a בייסיק client is on `standard`: it is the page count the spec itself ordered,
   nothing else. No premium-only feature is used (no hero video, no slider, motion stays `subtle`). The one
   thing `standard` buys beyond the page count is the `video` section, which the reserved home-page slot
   (item 6) needs anyway.

3. **Legal name for the privacy policy: parked** (Nitai, 02/11). `business.legal_name` stays the trading
   name "מסגרית Dream from Steel" and `standards.privacy_confirmed` stays false, so the privacy page keeps
   its launch blocker, and `zs build` prints it as a WARN on every build. It will also appear in
   `LAUNCH-CHECKLIST.md` once `zs package` generates that file.
   Neither Dapei Zahav listing carries a company name, ח.פ., ע.מ., בע"מ or עוסק מורשה, so there is nothing
   to look up: it has to come from Ofir. **This is safe to park through build and staging, but not through
   go-live**: the policy names the data controller, so the real legal name (and whether a customer database
   is kept, and the address for privacy requests) must be confirmed before the site is pointed at the
   client's own domain. Picking it up later is one line in `site.json` plus a rebuild.

## Still open

4. **Logo: found and in use, but only at 140px.** The file never reached this branch, so it was found on the
   client's own Dapei Zahav listing, in Zap's `Customers/80386843/` folder: the Dream from Steel badge, dark
   slate with an orange rim. It is now the site's logo in the header and the footer, the favicon is cut from
   it, and **the whole palette is sampled from it** (orange `#b84606`, slate `#1b2a36`), replacing the
   petrol-and-brass scheme the site was built with before it turned up.
   **What is still wanted:** the original file. 140x140 is the largest the directory serves, which is sharp
   enough at the header's 96px but soft on a high-density screen and too small for a crisp 512px favicon. Ask
   the client for the source (SVG, AI/EPS, or a PNG of 512px or more); dropping it in is one file plus a
   rebuild. Provenance is recorded in `IMAGE-SOURCES.md`.

5. **Favicon** is now cut from the real logo (see item 4), so this is closed except for the resolution point
   above.

## Reserved, waiting for the file

6. **Video frame on the home page** (Noam, 02/11 15:09, `inbox/2026-11-02-feedback.md`). The client also bought an AI social
   promo video and it should appear on the home page. No file or URL has arrived, so nothing is rendered: an
   empty band would fail QA and look broken. The slot is **straight after the services cards
   (`cards:framed`) and before `collage`**, i.e. index 6 of the home page's `sections` in `site.json`
   (re-checked 03/11 after the home was resequenced; it was index 4 under the old order). When the URL
   arrives, drop in:

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

   The site therefore has **no gallery**, by decision. The eight images on it are AI atmosphere only (a
   workshop bay, a fabrication bench, raw stock, brushed steel, a shop drawing, a cut-off saw throwing
   sparks, a weld bead and a second workshop interior) and none of them shows a finished product.
   Generating gates, railings or structures would have read as this client's portfolio, which
   `references/images.md` forbids. The footer carries the line
   "תמונות האתר הופקו בכלי בינה מלאכותית ואינן מציגות עבודות של העסק".

   **The sites team has since confirmed this** (Noam, 02/11 14:57, `inbox/2026-11-02-feedback.md`):
   *"אין אתר ואין תמונות צריך לייצר או לקחת ממאגרים"*. That sanctions generated and stock imagery, which is
   what the four atmosphere images are, and it is why they are on the site at all.

   **It does not change the no-portfolio decision, and that part needs a human to confirm.** Generated or
   stock photographs of gates, railings or finished structures on a metalworker's site read as that
   metalworker's own jobs whether they are captioned or not, which is the one thing `references/images.md`
   forbids and the one thing a customer would be misled by. Atmosphere (a bench, raw stock, a workshop bay)
   carries no such claim. If the team means for stock *work* photos to go up as well, say so explicitly and
   say how they should be labelled, and it can be built in one round; it is their call, not ours, and it is
   not being done silently.

   **What to ask the client for, in one message:** photographs of finished work (the more unusual the
   better, since the whole site argues that the work is not standard), one photograph of the workshop, one
   of Ofir, and the logo file. Each one that arrives gets a row in `IMAGE-SOURCES.md`, and a real gallery
   section plus a `team`/`split` with the owner's photo can then go on the home and about pages.

8. **Weave budget: 16 of 100 credits used.** 8 at intake (the first four images), 8 in the build session:
   four more atmosphere images approved as one batch, at 2 credits each. They are a shop drawing with
   measuring tools (the תכנון page), a cut-off saw throwing sparks (the ייצור page), a weld bead on a joint
   (home) and a second workshop interior (the אודות page), so the service pages and two of the posts no
   longer reuse the home page's photos. All eight are process and material only. 84 credits remain.

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

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
   **Update 04/11: provenance is now settled, resolution is not.** The brief's own `.docx` was opened as a
   zip and it does carry the logo, embedded under the "לוגו" row (`word/media/8b835a…png`, `rId7`); only the
   `brief.md` text export dropped it. It is the same file already in use (both 140x140, same grey backing,
   mean absolute difference 3.7/255), so there is no longer any doubt that this is the client's own mark or
   that the client supplied it. There is also no bigger copy hiding in the brief: ask Ofir, as above.

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

---

## 04/11, second pass: the Zap listing was read again, in full. It holds nothing more.

Both listings for this customer id were fetched and read line by line on 04/11, specifically to see
whether items 1, 2, 4 or 6 could be answered from them without the client. They cannot.

| looked for | found on `d.co.il/80386843/33060/` and `/30120/` |
|---|---|
| photographs of completed work | **none.** One image belongs to this customer, `Customers/80386843/acb7aca1e2f6445ab3dd097419f2f064.png`, and it is the logo already in use. It is rendered twice per page. Everything else is Zap's own category cover (`Umbraco/8844/coverimagedesktop.png`, `Umbraco/8977/coverimage-מסגריות.png`) |
| a photo of the workshop, or of Ofir | **none.** The owner's name does not appear on either listing |
| reviews | **none.** Both say "לעסק זה אין חוות דעת" / "היה הראשון לדרג!". No count, no stars |
| a bigger copy of the logo | **no.** `acb7aca…png` is the 140x140 already in use |
| a legal name, ח.פ., ע.מ. or בע"מ | **none**, as recorded on 02/11. The privacy blocker still needs the client |
| the promised AI promo video | not referenced anywhere |
| category and service wording | `תחומי העסק`: מסגריות, ייצור מוצרי מתכת. `שירותים עיקריים`: מסגרות מתכת, עבודות מסגרות. Breadcrumbs: מתכות - ייצור מוצרים, מסגריות. All of it is wording the site already carries from the spec sheet; nothing new was taken, so no `IMAGE-SOURCES.md` row was added |
| facts | ותק 20 שנה, הרימון 89 נווה ימין, א׳-ה׳ 07:00-20:00, אזור שירות כפר סבא, phone 072-2594285. Every one matches the spec sheet and the site |

Two small confirmations of earlier decisions, from the listing's own text: it says Zap routes the
072 as a virtual number ("זאפ גרופ עושה שימוש במספר וירטואלי"), which is why the site displays it
(item 1); and the WhatsApp button there is `wa.me/972559686670`, a Zap service line, not the
client's 050, which is why the site's WhatsApp uses the 050 from the spec sheet instead.

**Items 1, 2 and 6 stay open and still need the client.** Nothing was closed by this; what is
closed is the question of whether the listing might hold the answer. It does not, and it does not
need opening again.

## 04/11: the logo resolution ask, in one message

Item 4's remaining part, written so it can be sent as it stands:

> היי אופיר, לאתר חסר קובץ הלוגו באיכות גבוהה. מה שיש לנו כרגע זה הסמל בגודל 140x140 פיקסלים, וזה
> קטן מדי בשביל אייקון האתר ובשביל מסכים חדים. אפשר לשלוח את הקובץ המקורי של הלוגו? SVG או AI או
> EPS הכי טוב, ואם אין אז PNG ברוחב 512 פיקסלים ומעלה, עם רקע שקוף. זה מה שהמעצב הכין בזמנו.

That is the whole of what is missing on the logo: provenance was settled on 04/11 (the same badge
is embedded in the brief's own `.docx`), and 140x140 is the largest copy that exists anywhere we
can reach, the directory and the brief both.

---

## 04/11: the home page now holds the space for the video (item 6, rewritten)

**This supersedes item 6 above.** The space itself is reserved, not only the instructions.

The user asked for room on the home page for the promo clip being produced for this client. **The brief
does not ask for it** (re-checked in the `.docx`: unlike הרקולס, whose spec says `וידאו (פריים) לסרטון
שיופק ללקוח`, this one does not mention a video anywhere), so it is the user's instruction and is treated
as one, not as something the brief implies. Nothing on the page claims a clip exists or names a date.

**What is on the page now.** A real `overlay` band at **home-page `sections` index 6**, straight after
`cards:framed` and before `collage`: a full-bleed still with the process line on a card cut into its lower
edge. It is finished as it stands, and it is where the clip earns its place in the argument, after the
three things you can order are named and before the material chapter.

```json
{ "type": "overlay", "eyebrow": "התהליך",
  "title": "חיתוך, ריתוך והרכבה במקום אחד",
  "text": "כל עבודה עוברת את אותם שלבים: מדידה באתר, תכנון, ייצור בבית המלאכה בנווה ימין ומסירה במועד שנקבע מול הלקוח.",
  "image": "sparks" }
```

The still is `assets/sparks.webp`, the cut-off saw throwing sparks, already recorded in
`IMAGE-SOURCES.md`. It was chosen over the workshop interiors because it is the only one of the eight that
shows a moment rather than a still life, which is what a frame held for a clip has to carry. **It shows
process, not a finished product and not the client's premises**, so it claims nothing, and the footer's AI
line covers it as it covers the rest.

The band is pinned to **16/9 at every width in `design.custom_css`**, which is the ratio the finished clip
will use, so the box is already the right shape and the page does not move when the clip lands. On a phone
the card's pull-up is reduced, because `editorial.css` pulls it 12vh and against a 16/9 strip that leaves a
white card with a sliver of picture behind it.

**When the URL arrives: replace that one object with this one, at the same index, and rebuild.**

```json
{ "type": "video", "title": "הסרטון של מסגרית Dream from Steel",
  "youtube_url": "<the URL>" }
```

```bash
bin/zs build c80386843 && bin/zs qa c80386843 && bin/zs seo c80386843
bin/zs push c80386843 --site https://80386843dreamfromsteel.ussl.co.il
```

`tier` is already `standard`, which allows the `video` section (the basic package does not: a second reason
item 2 matters). The three `.zs-overlay` rules in `design.custom_css` stop matching on their own once the
section type changes; they do not need removing, though they can be. If the file is an mp4 rather than a
YouTube or Vimeo link, it can instead become the hero's own loop (`videos` + `hero.video`, under 6 MB,
4-8 s, no audio), in which case this band stays as it is.

**What is not promised:** no date, anywhere on the site or in the copy above. If the clip never arrives the
band is a finished part of the page and nobody has to do anything.

## 04/11 design-quality pass

- **Staging push not done.** `bin/zs push` to `80386843dreamfromsteel.ussl.co.il` was denied by the permission classifier in this session; push, live qa, shots and launch-check still to run.
- Weave: 44 of 100 credits now (16 + 14 spent on 1024px results because `resolution: "2K"` is not a GPT Image 2.5 parameter + 14 at 1920x1440). The first-batch 1024px images were discarded.
- Fidelity pass: no preview image of the direction exists (automatic mode dropped `directions`); compared against the NOTES home order instead. Order and bands match.
- Needs the client: photographs of completed work, the video file for the reserved band, privacy fields.

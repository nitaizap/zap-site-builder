# OPEN ITEMS — הרקולס גורקביץ (c743850)

Built in automatic mode: the sitemap came from the brief and the design was chosen here, so everything
below is a decision made on the best safe default, or something that needs a person.

## Needs an answer

1. **The video frame on the home page: the space is reserved and composed; it needs the clip.**
   The brief asks to set aside a video frame on the home page for a clip that will be produced
   ("להקצות אזור וידאו (פריים) לסרטון שיופק ללקוח"). Since 04/11/2026 the home page carries that band, between the
   company story and the lead form, as a full-width 16:9 frame (1440x810 at 1440, 1280x720 at 1280) holding a
   still from the client's own photography. It is a composed element, not an empty container: nothing on the
   page says a clip is coming and no date is promised.

   **To drop the clip in: one paste, one rebuild.** In `sites/c743850/site.json`, in the home page's
   `sections` array, replace the single object whose `"anchor": "video"` is (it is the `overlay` between the
   `split` and the `leadbar`) with:

   ```json
   {
     "type": "video",
     "anchor": "video",
     "title": "מראות לעולם הרכב",
     "youtube_url": "https://www.youtube.com/watch?v=XXXXXXXXXXX"
   }
   ```

   Then `bin/zs build c743850 && bin/zs qa c743850 && bin/zs seo c743850 && bin/zs pool c743850`, and
   `bin/zs push c743850 --site https://743850hercules.ussl.co.il`. Nothing else has to change: the heading
   stays, the position stays, and the band is already the ratio the player will use. Two tidy-ups once the
   clip is in, neither of them blocking: delete the `"video-poster"` entry from `images` and
   `assets/video-poster.jpg` (nothing else uses them), and the `.zs-anchor-video` rule in
   `design.custom_css` (it only sizes the overlay's photo, so it is inert on a `video` section).

2. **Customer reviews.** The brief says to show "4.2 מתוך 15 חוות דעת בדפי זהב". The validator blocks a
   hard-coded rating or review count, so the page uses the live Dapei Zahav reviews widget with
   `dpz_customer_id: 743850`. The widget only renders on the pushed site, so the block has not been seen
   rendered yet, only in the local build. Check it after the first push.
3. **Staging URL.** None exists yet, so nothing has been pushed. The site was built and reviewed locally.
4. **מספר מקשר.** "מספר מקשר זאפ" is empty in the brief and 03-6828265 is the client's own number, so
   `phone_is_virtual` is off and no tracking-number popup is shown. Confirm with the sites team.
5. **Privacy policy.** Built from Zap's standard wording. `legal_name`, whether the client keeps a
   database, the purposes and the privacy e-mail need the client's confirmation, then
   `standards.privacy_confirmed`. This is a launch blocker until it is done.

## Decisions taken here

6. **Category name shortened.** The brief's "מראות קמורות לאיתור גניבות / חניונים / צמתים" contains
   slashes, which cannot go in a URL or a menu label. The page is **"מראות קמורות לאיתור גניבות"**, and the
   full list (חנויות, חניונים, צמתים, מחסנים) is in the page's own text and meta description.
7. **Business name shown as "הרקולס גורקביץ".** The full legal name is 45 characters, which breaks the
   `<client> | <page>` SEO title length rule on every page. The legal name is in the schema and the footer.
8. **Header logo: the brief did supply one, and it is now used.** The earlier note here said the form left
   "לוגו" empty and that only the old site's 573x65 wordmark existed. That was wrong: `brief/brief.md` is a
   text export and drops embedded images, and the `.docx` carries one
   (`word/media/aa1a0db8e4c2367b079c9d7adf3e028ac19e19fb.png`) sitting in the "לוגו" row: the client's
   official lockup, emblem + "Hercules-Gurkiewicz" + "הרקולס-גורקביץ" + a small tagline in both languages.
   Since 04/11/2026 the site's logo is cut from the client's own artwork: the emblem from `logo.tif` above
   the Hebrew wordmark from that lockup, with the tagline lines cropped away (qa-rules: a logo with a small
   tagline gets a version without it, cropped, never redrawn). It renders 216x96 on desktop and 71px tall on
   a 390px phone, and the header now carries the company's name in Hebrew, which it did not before.
   **If the client has a vector or high-resolution logo, send it: the Hebrew wordmark here comes from a
   573x65 raster and is only just sharp enough at header size.**

9. **Product names follow the brief, not the old site's ALT text.** The existing site's image ALTs carry
   typos ("בנוני", "אונברסלי", "וולבן", "לבטחון", "אלומניום"). Each photograph was matched to its product
   by catalogue number and the brief's spelling was used.
10. **Alternate-angle photographs.** Where the client shot the same product twice, the second shot was
    either put in a small "עוד מהקטגוריה" gallery or left out, because Zap QA rejects the same view twice.
    Some products genuinely look near-identical (26 ס"מ vs 30 ס"מ bus mirrors, 42 ס"מ vs 52 ס"מ convex
    mirrors); those are kept, since they are different products in the brief's own list.
11. **A blog was added** though the brief leaves "אתר SEO (בלוג)" and "מאמרים" empty: the SEO checklist
    requires a category with three posts. All three are written from the brief's own technical text
    (blind spots, panoramic mirrors, convex mirror sizing). No fact was invented.
12. **The owner's name and the contact's mobile are not on the site.** יוסי גורקביץ and
    אסי גורקביץ 052-3909018 appear in the brief as internal contact details, not as published ones.
13. **One image from F: was deliberately left out**: the Zap mini-site photograph of a driver adjusting a
    mirror. Its origin and licence could not be established. See `IMAGE-SOURCES.md`.
14. **No AI images were generated.** The client's own archive covered every slot. Weave spend: 0 of 100.

## Not done

- No `zs push`, no `zs package`, no publishing: there is no staging host for this client yet.
- The Dapei Zahav reviews block, the accessibility toolbar and Elementor's font icons only render on a
  pushed site, so they have not been seen live.

## Added in the quality pass, 04/11/2026

15. **No photograph of a lamp exists.** "פנסים לכל סוגי הרכב" is a new page in the brief; neither
    hercules.co.il nor the client's archive on F: has a single picture of a lamp, and the brief forbids a
    stock or AI image for a product. The page itself is text and features with no photograph, and its card in
    the home grid uses `mirror-on-car`, the client's own photograph of a car with its side mirror, as context
    rather than as a product shot. It is 227x180 after the frame was cropped off, the softest image on the
    site. **Send one photograph of a lamp and both slots improve.**

16. **Two of the client's archive photographs had a frame baked in.** `mirror-on-car.jpg` and
    `blindspot-in-use.jpg` came off the old site as web graphics with a black rounded border and a red striped
    corner painted into the pixels. Both were cropped on 04/11/2026 (see IMAGE-SOURCES.md). Nothing else in
    the file changed.

17. **The client's own photography has its limits, and they are visible.** Several convex-mirror photographs
    show the photographer reflected in the mirror (p-kmurot-089 to 095), the truck set is 300x225 at source,
    and three categories are shot on a red cloth while the rest are on blue or white. Only the client can
    replace them. The pass moved the weakest frames out of the lead slots; it did not retouch anything.

18. **Engine and theme findings, written up and not fixed** (shared code, another client's agent is in the
    same repo):
    - `wp/theme/zap-base/assets/finish.css`: the inner-page `split` photo is boxed `aspect-ratio: 4 / 4.4`
      whatever the source is, the same shape as the home hero's 4 / 4.6 in `hero-space.md`. On this client it
      cropped 600x450 and 800x532 archive photographs to a corner and upscaled them on all 12 category pages.
      Worked around in this client's `design.custom_css` (4 / 3.1 from 1025px up, the arch shape excluded).
    - `wp/theme/zap-base/assets/editorial.css` (`.zs-film__img`): the filmstrip divides the page width by the
      number of photos, so six photos give 188x306 portrait frames that cut landscape product photography in
      half. Worked around here by using four photos and a shorter frame.
    - `.zs-cards--overlay` adds a `01 /` counter to every card. `design.md` lists fake sequence numbers as a
      tell of a generated site; a category grid is not a sequence. Left alone (theme-wide).
    - The carousel counter renders "2 / 8" as "8 / 2" in an RTL page: a bidi issue in the counter markup,
      visible on every RTL site that uses a carousel. Left alone (theme-wide).

## Added in the second feedback round, 04/11/2026

19. **The footer's group labels are menu items without a link.** The theme renders the footer menu with
    `depth => 1` (`wp/theme/zap-base/functions.php:353`), so a nested footer menu loses its children
    completely: built that way, the footer showed four group names and none of the 13 categories. The
    grouping is therefore a flat menu of 17 items in which four carry no `href`; this client's CSS styles
    "a link-less item" as a group label, which is robust (it keys off what the item is, not its position).
    **A `depth => 2` footer menu in the theme would let this be a real nested list.** Not changed here:
    shared code, and another agent is in `wp/theme` right now.

20. **The footer logo was the white one on a light grey footer.** `engine/sections.py`
    `footer_template_logo_key()` picks the light logo unless `design.tone == "light"`. It asks the tone but
    not the kit, and the `gallery` kit paints the footer from `--c-bg`: here that is
    `rgb(231, 234, 236)`, so a white logo sat invisibly on light grey (measured contrast 1.17:1).
    Worked around by pointing `logo_light` at `assets/logo-footer.png`, which is the dark lockup
    (contrast now 17.2:1). **The generic fix is for that function to ask whether the footer ground is
    light, not only whether the tone is.** Not changed here: shared code.

21. **The home hero's row had no column gap at all.** Measured on the live page: the photograph ended at
    x 683 and the text block began at x 683 at 1440, and the same at 1280 and at 1024. Fixed in this
    client's CSS (`clamp(36px, 3.4vw, 72px)`), which is where the car service site's identical defect was
    fixed too. **The gap belongs in the theme's hero container, where it would fix every `split` hero.**
22. **Between 768px and 1024px the hero was 1238px to 1401px tall**, because it stacks there but keeps the
    4:4.6 portrait photo. Same root cause as `hero-space.md`. Capped in this client's CSS (16:9 in that
    band): 826px at 768, 913px at 900.

## Closed by main, 04/11/2026 (PR 88, `6a9a262`)

Four of the write-ups above are fixed in the shared theme and engine, and the per-client workarounds were
deleted when `main` was merged in:

- **19 (footer menu depth)** is still open: the footer menu is still rendered at `depth => 1`
  (`functions.php:381`), so the four group labels stay items in the flat list. The CSS that styles them is
  unchanged and still needed.
- **20 (footer logo)** is fixed: `footer_is_light()` now asks the kit as well as the tone, and `gallery` is in
  `LIGHT_FOOTER_KITS`, so the engine picks the dark logo for this footer by itself. `logo_light` points back
  at `assets/logo-light.png` and `assets/logo-footer.png` is deleted.
- **21 (hero column gap)** is still open: the theme's hero row still has no column gap, so this client's
  `clamp(36px, 3.4vw, 72px)` stays. Its breakpoint moved from 1025px to 901px, because the theme stacks the
  split hero at 900px and 901-1024 is a two-column hero that was still getting the portrait photo.
- **22 (stacked hero height)** is fixed: `finish.css` now caps the stacked split hero at 16/10 up to 900px.
  This client's 768-1024 cap is deleted; measured 860 / 897 / 956 px at 768 / 820 / 900.
- **The filmstrip** no longer divides the page width by the photo count: frames are 240x320 at 768 to 1024 and
  290x386 at 1440. This client's height override is deleted.
- **The carousel counter** now reads "2 / 8" in RTL; nothing was ever done per-client for it.
- The inner-page `split` photo is **still** boxed `4 / 4.4` (`finish.css:137`), so this client's 4/3.1 rule
  stays, with its breakpoint moved to 901px for the same reason as the hero.


## Design-quality pass, 04/11/2026 (new `zs qa` checks, UX acceptance, fidelity)

23. **What the new checks found, local build:** 29 errors and 6 warnings. 27 were "image shown larger than its own
    pixels" (the client's archive photos are 227 to 333px wide and the category pages showed them at 424 to 477px;
    the home had 17), 1 was the review stars drawn 20px from an 18px file (`object-fit: fill`), 1 was the home's H2 at
    three sizes (53.5 / 46.5 / 32px). After the pass: 0 errors; 3 sameness warnings (36 / 35 / 39%, under the 40% stop).
    A second pass caught two more: a 333x500 portrait in the gallery shown at 424px, and the submit button on the lead
    band at 1.34:1 (red on maroon) once the band lost its photo.
24. **Fixes (this client only):** home category tiles use 600px and 513px photos instead of 250 and 300px ones; the
    category and catalogue pages use the classic card (photo above, text below) at the photo's own size instead of the
    dark overlay tile; split and article photos sit at their own size; the lead band is solid brand colour (its photo
    was an 800px file under a 1440px band) with a light submit button; the overlay and filmstrip H2 use the site's H2.
    The video frame is 16:9 at every width now (before: 768px and up), so the clip arrives without moving the layout.
25. **Fidelity pass: there is no preview to compare with.** The site was built in automatic mode and the direction was
    chosen in `site.json` directly, so `sites/c743850/preview/` never existed. The pass was done against the brief and
    the previous build: hero gap 72px at 1440 (measured), dark logo in the footer, footer list grouped in four with
    labels and readable at 390, reserved video band present, Heebo only (no Alef).
26. **Left, theme or host, not this site:** (a) the oversized-photo problem is the theme boxing and cropping small
    photos (cards, split, post hero): a `max natural width` rule in the theme would remove the per-client CSS;
    (b) overlay/filmstrip variants ship their own H2 clamp, which breaks "one size per level"; (c) the QA's
    "no button carries an icon" warning does not see icons drawn by CSS (`.zs-b-tel`), so it fires on the home;
    (d) the review stars file is 18x17 and the widget draws it 20x20; (e) on staging a third font,
    **Noto Sans Hebrew**, loads on every page: it comes from the Ally accessibility toolbar, a host plugin, not from
    the site; (f) the footer menu is still depth 1 (item 19).
27. **The home's lead band lost its photo.** If the client sends photographs of 1440px or more, the `photo` variant
    can come back. The photo-less band is intentional, not a gap.

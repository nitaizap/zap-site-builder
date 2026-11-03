# OPEN ITEMS — הרקולס גורקביץ (c743850)

Built in automatic mode: the sitemap came from the brief and the design was chosen here, so everything
below is a decision made on the best safe default, or something that needs a person.

## Needs an answer

1. **The video frame on the home page.** The brief asks to set aside a video frame on the home page for a
   clip that will be produced for the client ("להקצות אזור וידאו (פריים) לסרטון שיופק ללקוח"). No clip
   exists yet, and the engine will not render an empty video block. The home carries a `filmstrip` and a
   `carousel` of the client's own photographs in that part of the page instead. **Send the clip (or a
   YouTube link) and a `video` section goes in where the carousel is.**
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
8. **Header logo is the Hercules emblem, not the full wordmark.** The only wordmark file (the existing
   site's header image) is 573x65, which at the required 96px header height would be 846px wide, far over
   the 160px phone limit, and it carries a small tagline. The emblem (the script name over the vintage car)
   is the client's own artwork from `F:\...\חומר-גרפי\logo.tif`, trimmed, never redrawn. **If the client
   has a vector or high-resolution logo, send it and it replaces this in one place (Site Identity).**
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

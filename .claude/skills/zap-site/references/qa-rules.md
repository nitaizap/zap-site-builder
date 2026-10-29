# Zap QA rules: what reviewers reject

Zap's QA team reviews each site against a checklist before it goes live. Each rule below comes from a real
rejection. Most of them are now built into the engine (it just happens) or measured (`zs qa` / `zs seo` / the
validator fail the build). Read the "you" column before the gate and again before delivery: those parts need
your judgement.

| area | rule | how it is kept |
|---|---|---|
| **H1** | Home H1 = the client's name only. The main keyword goes in the hero lead and the first H2 | validator error, `zs seo` +3 |
| | No stray punctuation in H1s: an H1 ending with the name ("צור קשר עם X") renders with a space, never "עם, X" | engine |
| **Headings** | No full stop at the end of any heading (H1–H4, section, card and item titles, prose `<h2>`) | validator error. You: write titles without one |
| | Blocks that repeat on every page (the lead form title, footer column titles) are not headings | engine (`p`), `zs qa` error |
| | A number never wraps away from its word ("מספר 1", "1.5 ק״ג") | engine (non-breaking space in headings) |
| **Titles** | `<client> \| <page>` on every page, posts, category and legal pages included; 30–60 characters | validator error, Yoast templates, `zs seo` +7 |
| **URLs** | Service/hub slug = the H1, word for word. Menu label = the page's H1. One name per page everywhere | validator warning, `zs seo` 15. You: pick the name once and use it in key, H1, menu and footer |
| | Renaming a page drafts the old URL (no duplicate live pages). On a live site, also add a 301 | engine. You: add the 301 on live sites |
| **Blog** | Category slugs in Hebrew, URLs `/<blog>/<category>/` (no `category` or `נושא` base) | engine, validator |
| | At least 3 posts. Write them from the brief and the client's own material (old site articles, FAQ, tips), never invented facts; each with `related_page` and a 3-question FAQ | validator warning, `zs seo` 5. You: write them |
| | Category description = its meta description, 150–160 characters | validator error |
| **Identity** | Favicon from the client's logo symbol (square PNG 512, `favicon` in site.json). The cloned base site's icon must never stay | validator warning, `zs qa` |
| | Header logo legible: 56px desktop / 48px phones by default. A logo with a small tagline gets a version without it (crop, never redraw) | `zs qa` error under 46/40px. You: check the words in the logo are readable |
| | Client logo in the footer, linking home (white chip on a dark footer when there is no light version) | engine, `zs qa` |
| | Footer credit reads "Powered by" + Zap logo | engine |
| **Text** | No visible text under 16px: top bar, labels, chips, form fields, consent, the whole footer, the copyright line | theme floor, `zs qa` error |
| | Body copy in the text colour, never a faded grey: paragraphs on light grounds need 6:1 | theme, `zs qa` error. You: keep `colors.muted` dark (≥ 7:1 on `bg`) |
| | Every text at 4.5:1, large titles too (red titles on navy passed WCAG's 3:1 and were rejected). On dark grounds titles are white; the accent marks them with a rule or a chip, not by colouring the words | `zs qa` error |
| **Footer + legal** | The address is a Waze link (coordinates when known) | engine, `zs qa` |
| | Privacy and accessibility links open in a new tab | engine, `zs qa` |
| | The accessibility statement is the site's own page (Zap's standard text, the client's title and description) | engine (`הצהרת-נגישות`), `zs seo` +5 |
| | robots.txt is `Disallow: /` on staging by design; it opens only on the client's domain (`zs package --domain` / `zs push --live`) | engine. You: say so in the delivery message |
| **Phones** | Phone icon in the mobile header (hidden only when the client asks, `header.mobile_call: false`) | theme, `zs qa` |
| | The accessibility button never covers the H1 or the hero buttons | theme, `zs qa` error |
| | No empty band between the hero photo and the H1 | theme, `zs qa` error (> 90px) |
| **Interaction** | Carousel side slides readable (not faded to a ghost) | theme |
| | "מספר מקשר": when the displayed phone is a Zap virtual number, `business.phone_is_virtual: true` (+ `phone_regular`) adds the link and Zap's standard explanation popup | engine. You: set it whenever the brief's display number is a Zap number |

## More rules from QA rounds (layout, menus, galleries, phones)

| area | rule | how it is kept |
|---|---|---|
| **Menu** | Menu starts with "דף הבית" (desktop and mobile) and lists the pages in the same order as the footer; the blog is in it | validator error |
| | Main menu centred in the header on desktop | theme |
| **Fonts** | Body text and forms in a readable sans (Assistant, Heebo, Rubik, Noto Sans Hebrew, IBM Plex, Alef); a serif or display face only for headings | validator error (`fonts.body`), forms inherit |
| **Heroes** | Buttons only in the home hero; inner-page heroes have none | validator error |
| | Phones: the hero is as tall as its content, logo and text never under the header, buttons in view at 360×640 | theme, `zs qa` fold check |
| **Buttons** | Phones: side by side, equal width, one line each (never stacked) | theme |
| **Calls to action** | A page never ends with a `cta` section: the lead form follows it (two in a row) | validator error |
| **Phone bar** | No sticky call bar by default; the header's phone button is the call action. A site turns the bar on with `header.mobile_bar` (extra buttons) or `header.call_bar: true` | theme |
| **Accessibility button** | Phones: in the header bar next to the menu button, never over content. The slider's pause button sits in the hero's top corner, never over buttons | theme |
| **Layout** | ~80px between sections on desktop, 25–50px on phones; 20px side padding on phones; tap targets ≥ 44px | theme |
| | Phones: titles, text, buttons and the footer centred (long text, lists, forms and FAQ answers stay start-aligned) | theme |
| | Feature boxes: icon and text centred together; feature grids fill the width (3 per row) | theme. You: `columns: 3` |
| | Section intros sit with their title (`head: "stack"` when the intro is short) | you |
| **Icons** | Chosen by what the item is, never a repeated or generic star/heart. Events: brit = baby, henna = henna, shabbat chatan = star-david, birthday = cake, bar mitzvah = award, proposal = ring, challah = bread, bachelor = cheers. Venues: kitchen = utensils, kids = child, table tennis/snooker = pingpong, services to order = bell. `sparkle` renders as a star | validator error on repeats. You: meaning |
| **Galleries** | No photo twice in one section and no two shots of the same view; gallery pages are an even grid (no large first tile, no holes), 2 per row on phones; lightbox captions are the Hebrew description, never the file name | validator (repeats error, near-duplicate warning), theme, engine |
| | Wide panorama photos never go into tall or square crops on phones (the source lacks the height and looks soft) | you |
| **FAQ** | Hover state, a downward chevron that turns when open; post FAQs shown on the page (same as the schema) | theme, `zs qa` |
| **Editable everywhere** | Privacy and accessibility are Elementor pages; the blog's posts and archive (blog page, categories, search) are Elementor Pro Theme Builder templates ("פוסט בבלוג", "בלוג וקטגוריות"), like the header and footer. Theme PHP is only the fallback where Pro is missing | engine (`zs push`). You: check Templates → Theme Builder after a first push |
| **Pages** | No leftover public pages from plugins or the base install (e.g. `/login-customizer/`) and no placeholder text | you, after a first push; theme + validator for placeholders |
| **Facts** | Posts may use the client's listings the user approves (Weekend / Weekend Family pages) besides the brief; the site e-mail is confirmed with the client once | you |

## Before you hand a site to QA

1. `bin/zs qa <slug>` 0 errors, `bin/zs seo <slug>` 0 FAIL, then the same on the pushed site (`--site`).
2. Look at desktop at 1280px and phones at 390px yourself: logo words readable, no overlaps, no empty bands.
3. Read every heading once for punctuation, and every menu label against its page's H1.
4. Write the delivery message with the human-only items (blog source, privacy fields, robots on launch).

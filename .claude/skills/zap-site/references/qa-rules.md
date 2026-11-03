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
| | **Hero space** (user note 03/11/2026 on three sites, "a recurring issue"): the first screen is used, not just filled. Height earned by the photo or by real content, text that fills or balances its column, no bare area that carries nothing. Not measurable yet: six heroes, rejected and not, gave overlapping numbers on every metric | **you**, four questions in `hero-space.md` answered with `py tools/hero-space.py <url>` and the 1440 / 1280 shots. Not enforced by `zs qa`: no honest threshold exists |
| **Buttons** | Phones: side by side, equal width, one line each (never stacked) | theme |
| **Calls to action** | A page never ends with a `cta` section: the lead form follows it (two in a row) | validator error |
| **Phone bar** | No sticky call bar by default; the header's phone button is the call action. A site turns the bar on with `header.mobile_bar` (extra buttons) or `header.call_bar: true` | theme |
| **Accessibility button** | Phones: never over content; position superseded by Round 3 below (not in the header). The slider's pause button sits in the hero's top corner, never over buttons | theme |
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

## Round 2 (a contractor site): layout and templates

| area | rule | how it is kept |
|---|---|---|
| **Header** | No top utility strip (`header.topbar` defaults to off) | engine |
| | Desktop: the menu centred between the logo and the phone button | theme |
| | Phones: burger on the right (start), logo in the middle, a plain phone icon on the left (no filled button) | theme |
| | Every page that exists in the site (the blog too) is in the main menu | validator warning |
| **Accessibility button** | In the site's primary colour, never Ally's orange; on phones see Round 3 (never in the header). Never over the H1 or a button | theme, `zs qa` |
| **Phones** | Centred layout: headings, intros, card and feature text, buttons, CTA, lead form text, footer. Long text (prose, FAQ answers, forms) stays aligned to the start | theme |
| | Home hero: H1 and lead first, close under the header; the photo under them (or behind them in cover/inset/curve) | theme, `zs qa` |
| | The two hero buttons side by side and never wrapping at 360px (no "התקשר / ו") | theme. You: keep button labels to one or two short words |
| | A card that overlaps a photo on desktop sits under it on phones, inside the page margins, never over a badge | theme (pool `split · card`) |
| | Carousel: the active photo centred, no half slide peeking in | theme |
| **Inner pages** | No buttons in inner-page heroes (the CTA band, the header phone and the call bar carry the action); title and breadcrumbs centred. `buttons: true` on a hero brings them back when the brief asks | engine |
| **Sections** | Feature/advantage tiles: an icon that means something per item (never a row of identical ticks), centred, two per row on phones | theme. You: pick the icons |
| | CTA band: title on top, then the text, then the buttons, centred | theme |
| | No decorative arrows on cards | theme |
| | Blog cards: title on one line, excerpt 16px, a "קרא עוד" link with a hover | plugin + theme |
| **Templates** | Service pages share one Elementor template (hero from the page's title, excerpt and featured image; no closing CTA band, the lead form follows); a change there updates every service page. Posts share a post template: no category label above the H1, the body with its FAQ and related service, "מאמרים נוספים" beside it, images open in a lightbox | engine (`templates.shared`, default on) |
| **404** | Search button in the site's style and the field's height; the actions in equal widths (two per row, the phone full width under them) | theme |
| **Footer** | Centred; the client's logo in white on a dark footer (generated from the logo when there is no `logo_light`), never on a white chip; "Powered by" as text beside Zap's logo | engine + theme |
| **Copy** | Meta descriptions reach 150–160 characters with real content, never with filler endings ("צעד אחרי צעד.", "מדריך מעשי.", "ונשמח לעזור") | you (the engine's generated ones follow it) |
| **Legal texts** | The privacy policy without registration / social-login parts unless the site has accounts (`standards.privacy_accounts`); spelling fixed in the template. The accessibility statement says where its link really is (the footer), not "the main menu" | engine |

## Round 3 (same contractor site, a second reviewer)

| area | rule | how it is kept |
|---|---|---|
| **Logo** | Header logo = Elementor Pro's Site Logo widget (from Site Identity, links home). Footer logo may be an image (a white version on a dark footer) but always links home | engine (the build swaps the header image for `theme-site-logo` where Pro runs) |
| **Breadcrumbs** | Visible on every inner page, centred above the H1 (a reviewer asked for them "בכל האתר"; another site's reviewer had asked to remove them). Default on; `header.breadcrumbs: false` hides them | engine + theme |
| **Inner hero** | Title, lead and breadcrumbs all centred | theme |
| **Accessibility button** | Phones: never in the header (it sat on the logo). Low on the start edge above the bottom bar; moves up only while its panel is open. This replaces the earlier "in the header" rule | standards.css |
| **Phones** | No parallax on the hero photo (it looked like the hero floated away from the top while scrolling) | site.js |
| **Side-by-side blocks** | A drawing/photo beside a long list is as tall as the list (no column hanging short); nothing shifts out of its column on hover | theme (`layers`). You: look at every two-column block at 1440 and 1280 |
| **Blog cards** | Modest titles (≈1.15rem), at most two lines, never cut mid-word; "קרא עוד" is a real button | theme |
| **Footer** | Compact link lists (small gaps); Zap's credit logo in its own colours (on a white chip over a dark footer), never recoloured | theme |
| **Content** | Service pages need enough substance for the reviewer ("is this enough content?"): 450–800 words for trades, the client's own method, numbers and FAQ | you (`content-seo.md`) |

## Round 3 (a venue site): typography, phone header, breadcrumbs, posts

| area | rule | how it is kept |
|---|---|---|
| **Hebrew type** | No negative letter-spacing on Hebrew headings (heavy Hebrew letters touch); 0, at most -0.5px | theme |
| | Body text near-black (the palette's ink), weight 400, 17px on desktop; never a light grey or Light (300) weight; the top bar 400 too | theme. You: keep `colors.text` / `muted` dark |
| | Main menu weight 500 | theme |
| **Hero** | The logo above the H1 is small (≈128px desktop / 104px phone) so it doesn't repeat the H1 at the same weight; drop it from the hero when the logo already spells the name the H1 says | you (`custom_css` size, or `logo: false`) |
| **Phone header** | Reviewers differ on the phone icon: plain icon by default; `header.phone_round: true` puts it in a circle when a client's reviewer asks | theme option |
| **Menu** | The header menu is the zap-nav widget over the WordPress menu "ראשי": pages added or renamed in Appearance → Menus show in the header without a rebuild | engine |
| **Blog post** | Order: breadcrumbs, title, byline (author + date; the category is in the trail); centred on phones; air between prose headings and text | engine (post template), theme |
| **Forms** | The consent line stays one sentence; the privacy link is underlined | theme |
| **Two reviewers disagree** | Keep the newest note as the default for every site, and turn the other into a site option (`header.phone_round`, `header.breadcrumbs`, `header.topbar`), never a silent flip-flop | you |


## Before you hand a site to QA

1. `bin/zs qa <slug>` 0 errors, `bin/zs seo <slug>` 0 FAIL, then the same on the pushed site (`--site`).
2. Look at desktop at 1280px and phones at 390px yourself: logo words readable, no overlaps, no empty bands.
   Then the hero on its own: run `py tools/hero-space.py <url> --out <file>`, open the 1440x900 shot beside it and answer the
   four questions in `hero-space.md` (height earned, text fills or balances its column, content or air, first button in view).
   `zs qa` cannot see this one; the user has rejected heroes that passed it with 0 errors.
3. Read every heading once for punctuation, and every menu label against its page's H1.
4. Before handover, on staging: `bin/zs launch-check https://<client>.ussl.co.il --slug <slug>` (0 FAIL; writes `LAUNCH-SHEET.md`). Zap does not launch: the site must be launch-ready, i.e. the staging → live move changes nothing. It catches a `zap-site` plugin that a migration tool would leave behind (no menu, no form, no legal line, still HTTP 200), staging mode not in force, addresses a launch cannot rewrite, and QA not clean on both desktop and mobile.
5. Write the delivery message with the human-only items (blog source, privacy fields). Indexing, robots and lead mail switch on by themselves on the client's domain: never ask the launch manager to change settings.

## Round 3 (פטוצ'ינה, 01/11/2026)

| rule | how |
|---|---|
| No small title (eyebrow) above any H1 | enforced (validator error on `hero.eyebrow`) |
| Header logo about 96 px on desktop, 72 tablet, 60 phones (at most 160 px wide on phones, clear of the a11y button); footer logo 96 px, centred with its line | theme |
| The logo is global: header and footer read the one Site Identity logo (Elementor → Site Settings → Site Identity) | engine (`zap-logo` widget): change it once, both update |
| Phones: one header row, menu button + logo + a plain phone icon (no big round button) | theme; QA accepts an icon-only control by its icon's contrast |
| Open mobile menu: white, thin dividers, active item = colour + a line, sub-items indented with no ground, hover on every item | theme |
| Footer: three equal columns on desktop; centred and tighter on phones | theme |
| The whole card is the link; no corner arrow | theme |
| Section heads and card content centred consistently, when the client's QA asks | `design.align: "center"` |
| Consent line with a single space ("אני מאשר/ת את מדיניות הפרטיות") | plugin |
| "Where is the form e-mail set?" | wp-admin → פניות מהאתר → הגדרות טפסים (recipient, sender, test address, staging state); also shown in the form widget's panel. A rebuild takes `business.email_leads` from site.json, so change it there too |
| Breadcrumbs on every site (user decision 01/11/2026) | default on every inner page; `header.breadcrumbs: false` only when a client asks to hide them |


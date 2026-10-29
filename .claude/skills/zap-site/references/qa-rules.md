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

## Round 2 (layout and templates): Zap's house rules

| area | rule | how it is kept |
|---|---|---|
| **Header** | No top utility strip (`header.topbar` defaults to off) | engine |
| | Desktop: the menu centred between the logo and the phone button | theme |
| | Phones: burger on the right (start), logo in the middle, a plain phone icon on the left (no filled button) | theme |
| | Every page that exists in the site (the blog too) is in the main menu | validator warning |
| **Accessibility button** | In the site's primary colour, never Ally's orange; on phones low on the start edge (it moves under the header only while its panel is open), never over the header or the H1 | theme, `zs qa` |
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
| **Templates** | Service pages share one Elementor template (hero from the page's title, excerpt and featured image; the closing CTA from `templates.service.cta`); a change there updates every service page. Posts share a post template: no category label above the H1, the body with its FAQ and related service, "מאמרים נוספים" beside it, images open in a lightbox | engine (`templates.shared`, default on) |
| **404** | Search button in the site's style and the field's height; the actions in equal widths (two per row, the phone full width under them) | theme |
| **Footer** | Centred; the client's logo in white on a dark footer (generated from the logo when there is no `logo_light`), never on a white chip; "Powered by" as text beside Zap's logo | engine + theme |
| **Copy** | Meta descriptions reach 150–160 characters with real content, never with filler endings ("צעד אחרי צעד.", "מדריך מעשי.", "ונשמח לעזור") | you (the engine's generated ones follow it) |
| **Legal texts** | The privacy policy without registration / social-login parts unless the site has accounts (`standards.privacy_accounts`); spelling fixed in the template. The accessibility statement says where its link really is (the footer), not "the main menu" | engine |

## Before you hand a site to QA

1. `bin/zs qa <slug>` 0 errors, `bin/zs seo <slug>` 0 FAIL, then the same on the pushed site (`--site`).
2. Look at desktop at 1280px and phones at 390px yourself: logo words readable, no overlaps, no empty bands.
3. Read every heading once for punctuation, and every menu label against its page's H1.
4. Write the delivery message with the human-only items (blog source, privacy fields, robots on launch).

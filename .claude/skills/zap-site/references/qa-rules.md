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

## Before you hand a site to QA

1. `bin/zs qa <slug>` 0 errors, `bin/zs seo <slug>` 0 FAIL, then the same on the pushed site (`--site`).
2. Look at desktop at 1280px and phones at 390px yourself: logo words readable, no overlaps, no empty bands.
3. Read every heading once for punctuation, and every menu label against its page's H1.
4. Write the delivery message with the human-only items (blog source, privacy fields, robots on launch).

# Zap QA: what the QA team rejects, as rules

Zap's QA team checks every site against its own checklists (SEO/technical, desktop UX/UI, mobile 390px). The
rules below come from their rejection reports. **Enforced** = `zs build` (validator), `zs qa` or `zs seo` fails
on it; **theme** = the shared theme does it for every site (don't undo it with `custom_css`); **you** = check by
eye before delivery. Read this once per site, before calling it done.

## SEO and technical

| rule | how |
|---|---|
| Home H1 = the client's name only; inner H1 = the page name, one short line; never two lines joined into one H1 | enforced (validator) |
| SEO title = `<site name> \| <page name>` on every page (home: `<site name> \| <head keyword>`) | enforced (validator) |
| No visible breadcrumb above the H1 (schema keeps BreadcrumbList) | theme (`header.breadcrumbs: true` brings it back only if the client asks) |
| Blog: at least 3 posts before delivery; the blog is in the main menu; category slugs are Hebrew; category description is a full sentence of 150–160 chars | enforced (validator) |
| Posts: facts from the brief, the client's site or listings the user approves (e.g. Weekend / Weekend Family pages), never invented; each with an image, FAQ and a link to the matching page | you (validator checks count + links) |
| Post FAQ is shown on the page and matches the FAQPage schema | theme + enforced (qa) |
| Accessibility statement is a page of the site with the client's name (not Zap's external file); privacy and accessibility links both open in a new tab | theme/engine (automatic) |
| The lead form's title is not a heading (no H2 inside forms) | theme/engine |
| Gallery photos open in a lightbox | engine (automatic on `gallery`) |
| Every address links to Waze navigation | theme (footer + contact list) |
| No leftover public pages from plugins/base installs (e.g. `/login-customizer/`) | you: after a first push, list published pages on the server and draft anything site.json does not own |
| No placeholder text anywhere ("עדיין אין כאן תוכן", cut-off descriptions) | theme + validator |
| Images < 100 KB WebP, large enough for 2x phone screens (gallery/duo images use the `large` size) | engine |

## Desktop UX/UI

| rule | how |
|---|---|
| One phone in the header (the call button), not also in the top bar; the button's number in dark text on a light button | theme |
| Menu starts with "דף הבית" (desktop and mobile) and lists the pages in the same order as the footer | enforced (validator) |
| Main menu centred in the header on desktop | theme |
| Header logo readable: 84px tall (60 on phones), so square or stacked logos are not tiny. A faint/thin logo gets a darker version for the header | theme + you |
| Section spacing about 80px between sections on desktop | theme (`standards.css`) |
| No text under 16px (top bar, form labels, cards, footer, copyright, consent) and body text never Light (300) | theme |
| Body text and forms in a readable sans (Assistant, Heebo, Rubik, Noto Sans Hebrew, IBM Plex, Alef); a serif or display face only for headings | enforced (validator: `fonts.body`) + theme (forms inherit) |
| Icons match their content and never repeat inside one section | enforced (validator: no repeats) + you (meaning); the icon set has venue/event icons: utensils, child, pingpong, bell, baby, ring, cake, bread, cheers, star-david, shower, wifi, parking |
| One form everywhere (same fields on the contact page and the footer) | engine |
| No two calls to action in a row: a page never ends with a `cta` section, because the lead form follows | enforced (validator) |
| Buttons only in the home hero; inner-page heroes have none | enforced (validator) |
| Feature boxes: icon and text centred together | theme |
| Galleries: no photo twice, no two shots of the same view; gallery pages are an even grid (no large first tile, no holes); 2 per row on phones; lightbox captions are the Hebrew description, never the file name | enforced (validator: repeats, near-duplicate warning) + theme + engine |
| Contact page: details once (no address under the title when the NAP list shows it) | you |
| FAQ: hover state, a downward chevron that turns when open | theme |
| 404: styled search button, spacing before "main pages" | theme |
| Accent colours belong to the palette (no stray purple next to olive): take accents from the logo/photos | you |
| Section intros sit with their title (use `head: "stack"` when the intro is short) | you |
| Feature grids fill the width (3 per row on desktop), photo grids have even rows | you |

## Mobile (390px)

| rule | how |
|---|---|
| Hero: logo and text never under the header; the hero is as tall as its content; buttons in view at 360×640 | theme + enforced (qa fold check) |
| Buttons side by side on phones, equal width, one line each (never stacked) | theme |
| Content centred on phones: titles, text, buttons, footer (long text, lists, forms and FAQ answers stay start-aligned) | theme |
| No sticky "התקשרו" bar; the header's call button is the phone's call action (`header.call_bar: true` only if a client asks for the bar) | theme |
| Accessibility button in the header bar next to the menu button on phones, never over content; the slider's pause button in the hero's top corner, never over buttons | theme |
| Wide panorama photos never go into tall or square crops on phones (the source lacks the height and looks soft); use 4:3 or portrait shots there | you |
| One H1 size on phones on every template (page heroes, blog, posts, legal pages), always larger than H2; H2s short enough for 2–3 lines | theme + you |
| Hero subtitle at least 16px, fully opaque over a dark wash | theme |
| Section spacing 25–50px between sections; side padding 20px | theme |
| Tap targets at least 44px (FAQ questions, footer links, form links, phone links) | theme |
| Footer centred on phones with a small bottom gap | theme |
| Phone numbers never wrap mid-number | theme |
| Photos sharp on 2x screens | engine (sizes) + you |

## Icons

Pick the icon by what the item *is*, not a generic star or heart: events (brit = baby, henna = henna hand,
shabbat chatan = star-david, birthday = cake, bar mitzvah = award, proposal = ring, challah = bread, bachelor =
cheers), venue (kitchen = utensils, kids = child, table tennis/snooker = pingpong, services to order = bell).
`sparkle` renders as a star in Elementor: never use it for something that is not a star.

## Not visible on a screenshot (check before launch)

- Send one test lead to an internal address: sender ZapSites@d.co.il, recipient the client's lead email.
- Form errors and the thank-you message are styled and in Hebrew.
- The site e-mail: the spec's e-mail is confirmed with the client once (QA asks every round otherwise).
- The virtual-number popup (Zap's Maskyoo) where the client has one: the site shows the **tracking number**
  from the Weekend/Zap listing, not the business's direct line (ask when the spec leaves it empty).
- noindex + robots Disallow stay on staging and are removed at launch (`LAUNCH-CHECKLIST.md`).

# 2c · Design directions and the gate

The look is tokens + a preset + a hero layout, applied to fixed, tested markup. That is why three
directions cost one build, and why the chosen one is exactly what ships.

## The bar: premium, not template

The user compares our output with the best human designers in the team. "Clean and correct" reads as
bland. Every site must have, measured by eye on the preview before the gate:

- **One strong idea from this client's world**, carried everywhere, and different for every client: speed
  for a delivery service, gravity for a law office, warmth and appetite for a restaurant, calm for a clinic.
  Find it in the brief, the client's own photos and the logo, never in a previous site.
- **Typography with a point of view**: the H1 is large and confident; the pairing fits the idea (see
  *Hebrew type pairings*), and it is not the pairing the last site used.
- **A hero built from the client's best real material**: the strongest photo they have, in the layout that
  suits it (full-bleed, inset card, curve, split, cover with the logo). Video only when movement is the product.
- **Rhythm with contrast**: grounds, shapes and densities alternate; never two neighbours alike (`pool.md` →
  *Mixing rules*).
- **Details** (one or two, not all), chosen for this client, not by habit.
- **Brand colours exactly from the logo** (sample the pixels), with a darker primary only if contrast needs it.

There is no house look. A stat band, a marquee, bento tiles, a dark full-bleed hero or a footer wordmark are
tools in the pool, not a default sequence: use one only when this client's content calls for it.

Start from the base template and `motion: subtle`, then tune. Use the calmer presets only when the
client's audience calls for it (medical, legal, finance).

## No two sites alike

A new site must not look like the last one. Users compare sites side by side; a reused composition reads as a
template even with new colours. For each site decide from the brief and audience, and write the choice in NOTES.md:

- **preset** – rotate through all six; `signature` is one option, not the default.
- **hero** – `image` / `split` / `centered`, with `images` slider or a single photo, with or without `points`.
- **fonts** – every pairing in the table below is available; don't reuse the previous site's pair.
- **home composition** – pick from the full section list (`trust` band *or* card, `cards` bento / overlay /
  classic / icon, `features`, `steps`, `route`, `split`, `gallery`, `logos`, `quote`, `video`, `marquee`,
  `road`, `reviews`, `posts`, `prose`, `faq`, `cta`). Sections that exist for one kind of client (`road`,
  `route`, vehicle rides) are for that kind of client only. Real-work `gallery` and `logos` of
  certifications suit trades; `quote` needs a real quote.
- The three gate directions differ in preset, hero, type and radius, and none of them repeats the previous site.

### Identity, not AI slop

Generic phrasing and generic blocks are what make a site read as AI. Every site needs at least one element
that only this client could have: the client's own expertise as content (their numbers, their method, their
warnings, from their old site, articles or brief), shown in a form that fits the trade (`layers` for a
build-up, `route` for a journey, a spec table in `prose`), plus the logo's own shape as furniture
(`design.motif`). Copy in the client's voice: short, concrete, specific ("3 ק״ג זפת למ״ר"), never
"פתרונות מקצועיים", "שירות אמין ואיכותי", "ארבע סיבות לבחור בנו". No em dashes.

## Make three directions that are actually different

Every direction carries its own `home` (`site-json.md` → `directions`): its own sections, order, hero and variants.
Three colourings of one page are not three directions. Then vary what changes how the site feels:

| lever | options |
|---|---|
| **kit** (first) | `atelier` · `magazine` · `sidebar` · `panels` · `bands` · `quiet` · `frame` · `gallery` (`pool.md` → Style kits): the skeleton. Each direction a different kit |
| preset | `signature` (dark full-bleed hero, display type, brand part of the H1 on its own line, bento tiles, image wipe-ins, grain, footer wordmark) · `clean` (soft shadows, rounded, friendly-professional) · `bold` (heavy type, dark sections, strong accent) · `editorial` (serif headings, hairlines, airy, no shadows) · `soft` (pill buttons, pastel surfaces) · `industrial` (sharp, heavy, accent rules) |
| hero | `split` (text + framed photo) · `image` (full-bleed photo with scrim – needs a strong photo) · `centered` (statement + wide photo band) |
| header | `light` · `dark` (needs `logo_light`, or the logo sits on a white chip) |
| palette | light base + deep accent · dark base + one bright accent · warm neutral + muted accent |
| type | pairing below |
| radius | 2–4 sharp · 8–14 modern · 18–24 soft |
| tone | default (the preset's own dark/light rhythm) · `light` (no dark grounds at all: ivory/stone sections, light hero split with the photo slider, light CTA and footer; pair with a serif heading font and a deep, desaturated primary for "luxury") |
| motion | `none` · `subtle` (default: soft scroll reveals, hover lifts, hero entrance) · `lively` (bigger reveals, hero parallax, icon play, counters) |

Anchor each one in the brief: the audience's fear and the client's real differentiator. A plumber's
customer with water through the ceiling wants "fast and capable" (bold/image), a boutique law office wants
"calm authority" (editorial/centered), a clinic wants "warm and clean" (soft/split). Write a one-line
`label` in Hebrew for each, and recommend one in the gate message with a one-line reason.

If the client's brand colours are given, all three directions use them (vary preset/hero/type instead).

## The finish — the team playbook (read before writing site.json)

Since 22/10/2026 the team's design-quality method (A.1–A.5) is binding. Zap standards and
`content-seo.md` (H1 = keyword + brand) still win over taste: be distinctive inside those rules.

**1 · Ground it in the client's world.** Before any direction, write three lines in NOTES.md → Design brief:
- **Subject:** what the business actually handles (pipes, courts, ceilings, minerals).
- **Audience and moment:** who is on the page and in what state (water on the floor at 23:00).
- **The page's single job:** usually "call / WhatsApp now" or "trust us enough to leave details".
Distinctive choices come from the subject's materials and vernacular (a plumber: brass, blueprint lines, the real
van; a law firm: paper, seal, ink), not from a style catalogue.

**2 · A plan per direction:** base template (`pool.md`) + named deviations; 4–6 named colours with roles;
the Hebrew family and the weight per role; the section order with a variant per section; **the one bold thing**.

**3 · Review the plan against the defaults, then revise.** Ask: *would I have produced this for any similar
business?* Revise every part that answers yes, and write down what changed. These are the tells of a
generated site; avoid them unless the brief asks for them:

| tell | form here | engine default now |
|---|---|---|
| cream + serif + terracotta accent | `#F4F1EA`-ish ground, `#D97757`-ish accent | don't pick it |
| near-black + one acid accent | dark hero, neon/vermilion CTA, everything else grey | don't pick it |
| SaaS card kit | every section identical rounded cards, one radius, same soft shadow, gradient washes | vary variants (`pool.md`) |
| one coloured word in the H1 | `*word*` in the hero title, the brand half of `keyword — brand` in accent italic | neutralised in the H1 (stays its own line) |
| eyebrow labels everywhere | a small label above every H2, tracked capitals | `eyebrow` only where it adds meaning; no tracking |
| fake sequence numbers | 01/02/03 on things that are not a sequence | removed from cards; `steps` keep numbers (a real process) |
| chrome strings | `A · B · C` meta lines, an arrow on every button, `WORD — fragment` labels | button arrows removed; phone/WhatsApp icons stay |
| motion everywhere | an entrance on every section, a lift on every card (costs LCP/CLS) | `motion: subtle` default; `lively` only when the brief is about movement |
| the stat strip | big number + small label as the default hero support | `trust` only when the numbers are the client's real differentiator |
| accent dot | a coloured period closing every headline | renders as a plain period |

The brief's own words always win: a client who asks for dark + orange gets dark + orange.

**4 · Hebrew type.** One family across the site (body, breadcrumbs, footer, form fields); personality comes
from weights, sizes and spacing. A second display family for headings only if approved at the gate, set in
`design.fonts.heading`, never per section. Don't default to Heebo/Assistant: choose for the subject (Rubik,
Frank Ruhl Libre, David Libre, Noto Serif Hebrew, IBM Plex Sans Hebrew, Secular One / Suez One, Bellefair,
Miriam Libre, Alef, Varela Round, Fredoka). Line length under ~80 characters, body line-height 1.7–1.8. When a
headline is the visual element, the type itself (size, weight, tight leading) is the design, not a
highlighted word. Light (300) body only at ≥18 px.

**5 · Spend boldness in one place, and keep it buildable.** One memorable element per direction, everything
around it quiet (before leaving the house, remove one accessory). It must be a native section/variant, never an
HTML widget that exists only for the "wow". Good bold things: the real photo, art-directed (crop, duotone,
cut-out); a type-led hero; one unusual grid (`tiles`, `stagger`, `mosaic`); one orchestrated load moment instead
of animation everywhere.

**6 · Boldness never touches the heading scale.** One H1, H2 and H3 size per site; impact comes from weight,
composition and the bold element.

**7 · Density and imagery.** 9–13 sections on the home page; real images (client, old site, GMB, AI) in every
image slot, consistent in light and colour (Weave prompt: one look per site, brand colours as subtle accents,
no flat midday stock). Icons on every conversion button and contact line (automatic).

**8 · Critique before the gate.** Run QA, then critique each direction's home page in short: first
impression (2 s), hierarchy, consistency with the kit, accessibility, any tell from the table above, what
works, three fixes by priority. Fix 🔴/🟡 before the user sees it and add one line per direction: "what I
changed after critique".

## Motion and video

Motion is built into the theme and measured with everything else; never hand-animate a page.
`subtle` suits almost everyone; `lively` suits consumer brands, food, events, kids; `none` suits very
conservative YMYL clients. All of it respects "reduce motion", and content is never hidden from bots.
Trust-strip values animate as counters only when they are pure numbers (`15+`, `98%`), never years.

A hero **video** (Weave: Veo image-to-video from the approved hero photo, ≈ 90 credits) plays only on
desktop, muted and looped, over the poster photo; phones and data-saver get the photo. Offer it for
premium clients or when movement is the product (water, food, fitness); never by default.

### The motion catalogue (all generic, all in site.json)

| feature | site.json | what moves |
|---|---|---|
| hero video loop | `hero.video` (+ `image` poster) | 2–4 s silent loop, desktop only |
| hero ride | `hero.ride: "scooter"\|"van"\|"truck"`, or `design.ride` for every page hero | a vehicle drives along the hero's bottom edge; with a video only on phones |
| road scene | section `road` (`vehicles`, `items`) | two lanes of illustrated vehicles, spinning wheels, moving lane marks, drifting skyline |
| route ("how it works") | section `route` (`items` with `icon`) | a vehicle rides the track with the scroll, stops light up; steps are editable containers |
| scroll progress | `design.progress: "scooter"` | brand bar at the top with the vehicle on its tip (desktop/tablet) |
| slogan ticker | section `marquee` | big italic words scrolling on an accent band |
| bento tilt | `cards.layout: "bento"` + `motion: lively` | tiles tilt + light sweep under the mouse |
| entrances | `motion: lively` | H1 word-by-word, image wipe-ins, counters, reveals |

Vehicle art lives in `wp/theme/zap-base/assets/vehicles/*.svg` (brand colours via CSS variables, wheels
spin around their own centres). A new client type that needs other moving art (a tow truck, a bicycle, a
boat) gets a new SVG there in the same structure (`zs-veh__body`, `zs-veh__wheel` with its own
`transform-origin`, `zs-veh__speed`), never a one-off animation.

### Brief words → features

| the brief says | build at least |
|---|---|
| "אנימציות", "תנועה", "דינמי", "חדשני" | `motion: lively` + one moving signature element in the first screen on desktop **and** phone |
| vehicles / scooters / delivery / transport / moving / towing | `hero.ride`, `road`, `route` for the process, `design.progress` |
| "וידאו" / movement is the product | `hero.video` (Veo), plus `ride` or `marquee` for phones |
| "צבעים על בסיס הלוגו" | sample the logo pixels into `colors`; Elementor Global Colors carry them |
| "יוקרתי", "פחות צבעים", "בלי רקע שחור", "שלא ייראה כמו האתר הישן" | `tone: light`, serif headings (Frank Ruhl Libre), primary = a deeper, desaturated logo colour, the logo's second colour replaced by a muted metal (brass/champagne), hero `images` slider with bright editorial daylight photos |
| "אינטראקטיבי" | bento tilt, route on scroll, FAQ, counters; never auto-playing sound or popups |

Everything that moves on its own longer than 5 s (hero slider, road, marquee) gets a pause button automatically (`.zs-pausable`, WCAG 2.2.2). A visitor whose OS has animations off (common on managed work PCs and Remote Desktop) sees everything parked — that is correct, not a bug.

Rules: motion is decorative (aria-hidden), never carries information, parks under "reduce motion", and
must not cover text or controls at 390 px. Verify each moving element with a scrolled screenshot on the
pushed site; a full-page shot does not show scroll-driven states.

## Colour

- **Nothing may blend in**: QA fails text below WCAG AA, and any control, outline or icon below 3:1 against what is behind it. Pick accent colours that clear 3:1 on *every* ground they appear on (ivory, surface, stone), not just on white.

- `primary` carries buttons and links: contrast with `primary_ink` must be ≥ 4.5:1 (white text needs a
  dark enough primary). `accent` is for highlights; `accent_ink` sits on it.
- `ink` (headings) near-black tinted toward the primary; `text` slightly lighter; `muted` must still be
  ≥ 4.5:1 on `bg` and `surface` (QA measures this; `#647389` on white is the lightest safe grey).
- `surface` is a 3–6% tint of the primary or a warm off-white; `dark` is the footer/dark sections.

## Hebrew type pairings (heading / body)

| feel | pairing |
|---|---|
| modern, approachable | Rubik / Assistant · Heebo / Heebo |
| corporate, precise | IBM Plex Sans Hebrew / Heebo · Noto Sans Hebrew / Assistant |
| authority, editorial | Frank Ruhl Libre / Assistant · Noto Serif Hebrew / Heebo |
| luxury, distinctive (when "it looks like every other / AI site") | candidates: Bellefair / Miriam Libre · Bona Nova / Alef · David Libre / Miriam Libre · Karantina / Assistant · Rubik 800 / Assistant. Don't pick for the user: font taste is personal (the courier client rejected Frank Ruhl and Bellefair and chose bold Rubik + Assistant). Render 4–6 pairings on the site's own hero and ask for a number (playbook round 21) |
| bold, punchy | Secular One / Heebo · Suez One / Assistant |
| friendly, soft | Varela Round / Assistant · Fredoka / Heebo |

## The gate message (one message)

1. The PREVIEW.md link (three directions, desktop + mobile, real copy).
2. The page tree: page · keyword · H1, as a short table.
3. Assumptions and open questions.
4. "Which direction — A, B or C? And is the page list right?"

Before sending, Read the preview images and fix what you would not show a client: an empty-looking hero,
a logo that disappears on a dark header, buttons that wrap, a photo that does not suit `hero: image`.

After the answer: copy that direction's overrides into `design`, rebuild, and continue to the build stage.
Small taste notes from the user ("darker blue", "less rounded") go into tokens, not CSS.

# 2c · Design directions and the gate

The look is tokens + a preset + a hero layout, applied to fixed, tested markup. That is why three
directions cost one build, and why the chosen one is exactly what ships.

## The bar: premium, not template

The user compares our output with the best human designers in the team. "Clean and correct" reads as
bland. Every site must have, measured by eye on the preview before the gate:

- **One strong idea from the brand**, carried everywhere: for a courier it is speed (italic black type,
  light trails, a moving road, a ticker); for a law office it is gravity (serif, hairlines, stillness).
- **Display typography**: H1 at 5rem+ on desktop, weight 800–900, tight leading; the brand half of the
  H1 on its own line in the accent colour (the `keyword — brand` H1 does this automatically).
- **A cinematic hero**: a full-bleed photo shot for the brand's mood (night, golden hour, macro), 2K, and
  where the budget allows a 2–4 s silent video loop (Veo image-to-video, then check every frame for
  people, text and logos; trim and crossfade with ffmpeg rather than reroll).
- **Rhythm with contrast**: dark ↔ light ↔ accent bands, never five white sections in a row; one
  accent band (marquee / CTA) per page.
- **Photo tiles, not boxed cards**, for services with images (`layout: "bento"`).
- **Details**: accent dashes on eyebrows, arrow buttons, numbered tiles, grain on dark, a wordmark in the
  footer, plus/minus FAQ, image wipe-ins, word-by-word H1 entrance.
- **Brand colours exactly from the logo** (sample the pixels), with a darker primary only if contrast needs it.

Start from `preset: signature` with `motion: lively`, then tune. Use the calmer presets only when the
client's audience calls for it (medical, legal, finance).

## Make three directions that are actually different

Vary what changes how the site feels, not just the colour:

| lever | options |
|---|---|
| preset | `signature` (premium default: dark full-bleed hero, display type, brand-part of H1 in accent italic, stat bar, marquee, bento tiles, image wipe-ins, grain, footer wordmark) · `clean` (soft shadows, rounded, friendly-professional) · `bold` (heavy type, dark sections, strong accent) · `editorial` (serif headings, hairlines, airy, no shadows) · `soft` (pill buttons, pastel surfaces) · `industrial` (sharp, heavy, accent rules) |
| hero | `split` (text + framed photo) · `image` (full-bleed photo with scrim – needs a strong photo) · `centered` (statement + wide photo band) |
| header | `light` · `dark` (needs `logo_light`, or the logo sits on a white chip) |
| palette | light base + deep accent · dark base + one bright accent · warm neutral + muted accent |
| type | pairing below |
| radius | 2–4 sharp · 8–14 modern · 18–24 soft |
| motion | `none` · `subtle` (default: soft scroll reveals, hover lifts, hero entrance) · `lively` (bigger reveals, hero parallax, icon play, counters) |

Anchor each one in the brief: the audience's fear and the client's real differentiator. A plumber's
customer with water through the ceiling wants "fast and capable" (bold/image), a boutique law office wants
"calm authority" (editorial/centered), a clinic wants "warm and clean" (soft/split). Write a one-line
`label` in Hebrew for each, and recommend one in the gate message with a one-line reason.

If the client's brand colours are given, all three directions use them (vary preset/hero/type instead).

## The finish — what makes it look high-end (read before writing site.json)

Benchmark: the best Zap builds look editorial and confident, not templated (see `benchmark.md`).
The engine does most of it by default; your copy and choices must use it:

- **Headlines carry the design.** Short, strong, two-line H1/H2s. In `site.json` use `\n` where the
  meaning breaks, `*word*` to put the brand or key phrase in the accent colour, and end statements with a
  period (it renders as an accent dot): `"חברת שליחויות בחיפה\nוהצפון — *מהירות האור*."`. Use it on
  the hero and 2–3 section titles per page, not on every heading.
- **An eyebrow on every section** (`eyebrow`: 1–3 words: "השירותים", "מי אנחנו", "הצעד הבא").
- **Asymmetric section heads**: give sections a real 1–2 sentence `intro`; it sits beside the title.
- **A home-page rhythm, never the same block twice in a row**: cinematic hero → stat band (`trust`, 3–4
  verifiable facts with short values: "30+ שנה", "24/7", "עשרות שליחים") → `marquee` of services or
  areas → `split` with a `badge` → overlay `cards` (every card with a photo) → `features` or `steps` →
  `faq` → `cta` (brand colour). The light lead-form band and the dark footer follow automatically, so
  the page ends brand colour → light → dark; never stack three dark blocks.
- **Preset**: `signature` (sharp, hairlines, one accent, editorial-industrial) is the strongest default for
  B2B, trades, logistics, legal and industry. Make it one of the three directions every time.
- **Hero**: `image` (cinematic, ~90% of the screen, text over a deep gradient) whenever you have a strong
  photo; `split` when the photo is small or busy. Render an image hero at 2K.
- **Type**: headings in a heavy grotesk (Heebo or Rubik, weight 800) for modern brands, Frank Ruhl Libre
  for legal/heritage; one family for body. Display faces (Secular One, Suez One) only for playful brands.
- **Colour**: one accent for eyebrows, accent words, the dot, numerals and the primary button; everything
  else is ink, white, a near-white surface and one dark.
- **Image art direction** (Weave prompts): one consistent look per site, e.g. "cinematic editorial
  photograph, golden hour or dramatic overcast light, deep shadows, rich contrast, shallow depth of
  field, 35mm", with the brand colours as subtle accents in the scene. Avoid flat midday stock looks,
  white studio shots and clutter. Hero 2K, cards 1K, the same light in every image.
- **Details**: a badge with a real number on the split photo, numbered overlay cards and ↖ arrows
  (automatic), image wipes and counters (`motion: lively` for consumer brands, `subtle` otherwise).
- Before the gate, compare your home page with the benchmark; if a section still looks like a default
  template block, rewrite its copy or change its type.

## Motion and video

Motion is built into the theme and measured with everything else; never hand-animate a page.
`subtle` suits almost everyone; `lively` suits consumer brands, food, events, kids; `none` suits very
conservative YMYL clients. All of it respects "reduce motion", and content is never hidden from bots.
Trust-strip values animate as counters only when they are pure numbers (`15+`, `98%`), never years.

A hero **video** (Weave: Veo image-to-video from the approved hero photo, ≈ 90 credits) plays only on
desktop, muted and looped, over the poster photo; phones and data-saver get the photo. Offer it for
premium clients or when movement is the product (water, food, fitness); never by default.

## Colour

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

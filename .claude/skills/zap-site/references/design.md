# 2c · Design directions and the gate

The look is tokens + a preset + a hero layout, applied to fixed, tested markup. That is why three
directions cost one build, and why the chosen one is exactly what ships.

## Make three directions that are actually different

Vary what changes how the site feels, not just the colour:

| lever | options |
|---|---|
| preset | `clean` (soft shadows, rounded, friendly-professional) · `bold` (heavy type, dark sections, strong accent) · `editorial` (serif headings, hairlines, airy, no shadows) · `soft` (pill buttons, pastel surfaces) · `industrial` (sharp, heavy, accent rules) |
| hero | `split` (text + framed photo) · `image` (full-bleed photo with scrim – needs a strong photo) · `centered` (statement + wide photo band) |
| header | `light` · `dark` (needs `logo_light`, or the logo sits on a white chip) |
| palette | light base + deep accent · dark base + one bright accent · warm neutral + muted accent |
| type | pairing below |
| radius | 2–4 sharp · 8–14 modern · 18–24 soft |

Anchor each one in the brief: the audience's fear and the client's real differentiator. A plumber's
customer with water through the ceiling wants "fast and capable" (bold/image), a boutique law office wants
"calm authority" (editorial/centered), a clinic wants "warm and clean" (soft/split). Write a one-line
`label` in Hebrew for each, and recommend one in the gate message with a one-line reason.

If the client's brand colours are given, all three directions use them (vary preset/hero/type instead).

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

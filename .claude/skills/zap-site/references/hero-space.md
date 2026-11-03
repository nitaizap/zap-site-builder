# Hero space: what "make better use of the hero" means here

**Status: guidance, not a gate.** On 03/11/2026 the user reviewed three freshly published sites, said of one hero
"make better use of hero space", called it "a recurring issue, bake it into the flow", and repeated the note on the
other two. `zs qa` and `zs seo` passed all three with 0 errors. We tried to turn the note into a measured check and
could not: **no number separated the three rejected heroes from heroes he did not reject** (table below). A threshold
fitted to six sites would fire on good designs and be ignored within a week, so none is enforced. What is enforced is
the *step* (qa-rules.md checklist, step 2) and the *evidence loop* (the last section), which is how a real check gets
earned the next time he says it.

## The complaint, in words

The hero is the first screen of a client's home page. He objects to three things, all visible without a ruler:

1. **empty area**: large parts of the first screen show nothing the visitor came for (bare photo, bare ground);
2. **text that neither fills nor balances its column**: a small block of text (H1 57px, lead 17px) in a column built
   for far more, next to a photo twice its height, or a short caption floating in the middle of a wide photo;
3. **a hero taller than its content earns**: the engine gives photo heroes a CSS floor (`cover` / `inset` 86vh up to
   820px, `curve` 76vh up to 720px on desktop, `pool.css`) that does not look at what is inside.

## What was measured (1440x900, 03/11/2026, live pages, re-measured ten minutes later: identical)

`tools/hero-space.py` (headless Chrome, hero = the `.zs-hero--home` box). "Empty" = share of the hero box with no
text line, button, form or non-background image in it (an 8px grid). "Text/photo" = height of the text block against
the height of the photo beside it. 1280x720 overlaps the same way.

| site | hero | rejected? | height (vh) | photo behind text | empty | text block / hero | text / photo | H1 / lead |
|---|---|---|---|---|---|---|---|---|
| dreamfromsteel | `curve` | **yes** | 863 px (0.96) | yes | 90% | 0.31 | n/a | 57.6 / 17 |
| carservice | `split` | **yes** | 851 px (0.95) | no | 55% | 0.40 | 0.47 | 57.6 / 17 |
| hercules | `split` | **yes** | 786 px (0.87) | no | 60% | 0.40 | 0.47 | 57.6 / 17 |
| yadmordechai | `cover` | no complaint | 792 px (0.88) | yes | 90% | 0.43 | n/a | 57.6 / 17 |
| thewhite-villa | `cover` + logo + slider | no complaint | 792 px (0.88) | yes | 92% | 0.14 | n/a | 57.6 / 17 |
| kfarsabataxis | `split` + form card | no complaint | 1045 px (1.16) | no | 48% | 0.69 | 1.10 | 57.6 / 17 |

The engine's own heroes, same copy and photo (`examples/sample-plumber`, slug `herotest`, never committed):

| hero | height (vh) | empty | text block / hero | text / photo | H1 px |
|---|---|---|---|---|---|
| `split` (default) | 0.87 | 58% | 0.43 | 0.51 | 57.6 |
| `split` + `form: true` | 1.16 | 50% | 0.84 | 1.34 | 57.6 |
| `split` + `variant: stage` | 0.89 | 33% | 0.56 | 0.56 | 77.8 |
| `centered` | 1.01 | 49% | 0.29 | 0.57 | 57.6 |
| `image` (default and `cover`, `inset`) | 0.88 | 91% | 0.39 | n/a | 57.6 |
| `image` + `curve` | 1.06 | 92% | 0.32 | n/a | 57.6 |
| `tone: light` + `image` | 0.88 | 89% | 0.56 | n/a | 77.4 |
| `tone: light` + `split` | 0.76 | 55% | 0.49 | 0.60 | 57.6 |

## What the numbers say

- **Nothing separates the groups.** Rejected vs not rejected: height 0.87-0.96vh vs 0.88-1.16vh; empty share 55-90% vs
  48-92%; text block / hero 0.31-0.40 vs 0.14-0.69; text / photo 0.47 vs 1.10 (one site each side). Every range
  overlaps, and the two rejected `split` heroes sit on the engine's own default `split` hero (0.51), so a limit tight
  enough to catch them catches the template. The only metric that moved cleanly is the type scale, and it is the same
  on all six sites.
- **The six heroes are one template.** H1 57.6px and lead 17px at 1440 (54px at 1280) on every one of them, whatever
  the hero's height or layout. Only `stage` and `tone: light` + `image` scale the H1 up (77px). The defect, if it is
  one, belongs to the template's proportions, not to what these three sites did.
- **"Nobody complained" is not "approved".** `yadmordechai` and `kfarsabataxis` were published the same day by the
  same pipeline; there is no record that the user opened them. They share the structure of the rejected ones
  (kfar differs only by a form card below the fold). If he looks and rejects them too, the table is 5 against 1 and a
  threshold may exist; if he approves them, the cause is something no metric here sees (the photo, the copy).
- Small samples, one rater, two of the three rejects siblings (`split`). That is enough to *refuse* a threshold,
  never enough to set one.

## The rule (what the builder does)

Before a home page goes to the user, with the shot of the hero at 1440x900 and 1280x720 in front of you and the
output of `py tools/hero-space.py <url> --out <file>` next to it, answer four questions in the delivery notes. A "no"
is fixed or explained there; it is not left for the user to find.

1. **Is the height earned?** The text is a fixed amount (H1, two-line lead, two buttons, three points: about 260-340px
   at 1440, in every layout). The rest of the hero must be a photo that carries the message or real content. A
   `cover` / `inset` / `curve` hero is at least 86vh / 76vh by CSS; when the text block is a small part of it
   (steel 0.31, villa 0.14) the first screen is a photo with a caption. Either the photo is the message (a venue, a pool, a
   building: say so) or choose a layout whose height follows its content.
2. **Does the text fill or balance its column?** In `split`, put the text block beside the photo: when it is about half
   the photo's height (`text / photo` near 0.5: car, hercules, the engine default), the column is half empty by
   construction. Levers, in the order to try: `variant: stage` (H1 77px, the text fills the column); `points` and
   `form` (real content in the column: kfar's `form: true` card brings the ratio to 1.1); `tone: light` (H1 77px);
   a photo cropped less tall.
3. **Is there content in the empty area, or only air?** Check the biggest empty rectangle in the tool's output next
   to the shot. A rectangle that is bare photo is fine when the photo is the point; bare ground is not. Do not fill it
   with invented facts (a trust bar needs the client's real numbers, `design.md`).
4. **Is the first button in the first screen and the H1 readable at hero scale?** The fold itself is already a `zs qa`
   error on phones and laptops; the tool prints it for desktop too. A 17px lead under a 57px H1 in a 650px column is
   the engine default, not a decision: if the hero looks thin, that is the first thing to scale.

These are levers and questions, **not limits**: nothing in them is a number the evidence supports. The numbers in the
tables are what the rejected sites looked like, to compare against, not a pass line.

## Turning it into a check (the evidence loop)

The next time the user says a hero wastes space, or approves one:

1. Run `py tools/hero-space.py <site url> <two neighbours> --out <file>` the same day (client pages change; record
   the date and the commit).
2. Append the rows to the first table with the verdict (rejected / approved / no record).
3. When **one metric separates at least three rejected from three approved heroes with a gap between the groups, and
   the groups are not siblings of one layout**, add it to `MEASURE_JS` in `engine/qa.py` next to the phones' hero
   checks, as a **WARN**. Promote it to an error only after it has stayed quiet on every approved hero for a month.
4. If the user says the six heroes above are all fine, delete the three-point complaint from the rule's first
   paragraph and keep the questions: the loop worked, and the answer was "taste".

Raise it with him first (CLAUDE.md: open items are collected) whether the engine default (57.6px H1, 17px lead in every
hero) should scale up. It would move all six heroes at once, but it is shared theme CSS: not changed here.

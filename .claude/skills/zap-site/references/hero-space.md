# Hero space: what "make better use of the hero" means here

**Status: guidance, not a gate.** On 03/11/2026 the user reviewed three freshly published sites, said of one hero
"make better use of hero space", called it "a recurring issue, bake it into the flow", and repeated the note on the
other two. `zs qa` and `zs seo` passed all three with 0 errors. We tried to turn the note into a measured check and
could not: **no number separated the three rejected heroes from three he confirmed are fine** (yad mordechai and kfar saba taxis, answered 03/11; thewhite-villa is the third) (table below). A threshold
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

The car service hero was corrected in its own `custom_css` after this was measured (now 496 px at 1440); the row is the state the user rejected.
`tools/hero-space.py` (headless Chrome, hero = the `.zs-hero--home` box). "Empty" = share of the hero box with no
text line, button, form or non-background image in it (an 8px grid). "Text/photo" = height of the text block against
the height of the photo beside it. 1280x720 overlaps the same way.

| site | hero | rejected? | height (vh) | photo behind text | empty | text block / hero | text / photo | H1 / lead |
|---|---|---|---|---|---|---|---|---|
| dreamfromsteel | `curve` | **yes** | 863 px (0.96) | yes | 90% | 0.31 | n/a | 57.6 / 17 |
| carservice (before its custom fix) | `split` | **yes** | 851 px (0.95) | no | 55% | 0.40 | 0.47 | 57.6 / 17 |
| hercules | `split` | **yes** | 786 px (0.87) | no | 60% | 0.40 | 0.47 | 57.6 / 17 |
| yadmordechai | `cover` | fine | 792 px (0.88) | yes | 90% | 0.43 | n/a | 57.6 / 17 |
| thewhite-villa | `cover` + logo + slider | fine (older site) | 792 px (0.88) | yes | 92% | 0.14 | n/a | 57.6 / 17 |
| kfarsabataxis | `split` + form card | fine | 1045 px (1.16) | no | 48% | 0.69 | 1.10 | 57.6 / 17 |

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
- **The labels are 3 against 3, and the heroes are the same template.** kfarsabataxis is a plain `split` hero like
  the two rejected ones: the same 4:4.6 portrait photo (570x656 against hercules' 570x656), the text block 335 px
  tall beside it, ~160 px of bare ground above and below the text. Its form card is **not** in that column: it
  is a full-width band under the whole row (y 896-1116 against the photo's 201-857), below the first screen. The first
  screen of kfar and of the unfixed car service hero are the same picture.
- Small samples, one rater, two of the three rejects siblings (`split`). That is enough to *refuse* a threshold,
  never enough to set one.

## Hypotheses tested after the labels came in (all 03/11/2026)

1. **"The rejected heroes leave a region unoccupied; the approved ones fill it"** (variant: `curve`, `split` vs `cover`,
   `cover`, `split` + form). It separates 3 from 3 only as a label, and the mechanism does not hold. kfar's form
   card does not occupy the column beside the text (above), so its first screen is as empty as car's was. And steel
   (`curve`) is a full-bleed photo with text over it, exactly like the approved `cover` heroes: it has no empty
   column to point at. A categorical column with four values will split six rows by chance.
2. **The portrait photo (`finish.css:102`, `body:not(.zs-p-signature) &.zs-hv-split .zs-hero--home ... img {
   aspect-ratio: 4 / 4.6 }`, overriding `main.css:232` 4 / 3.4)** is a real cause, checked in the CSS and on the pages:
   every home `split` hero gets a photo 1.15x as tall as it is wide, and the text column (335-340 px of text) is left
   with ~half the photo height as dead ground. Measured: car 627x721 beside 339, hercules and kfar 570x656 beside
   310-335, a rebuilt lehem-erez 627x721 beside 146 (text/photo 0.20, the sparsest of all). Correcting the ratio on the
   car service site alone took its hero from 851 px to 496 px at 1440. It explains why `split` heroes look
   top-heavy and hollow; it **does not separate the labels**, because the approved kfar has it too. The user's tolerance
   for it is therefore unknown, not "low".
3. **Type scale** (H1 57.6 px, lead 17 px everywhere). Consistent with 2 and with steel and hercules, and the car
   fix that raised the H1 (up to 6.4rem) made it read better. It is constant across approved and rejected alike, so
   it cannot be what distinguishes them either. A frame-too-big-for-the-type story and the portrait-ratio story can
   both be true.
4. **Two new numbers, first screen only** (hero cut at the fold; photo counts as occupied only when it is a real
   image, a full-bleed background does not). Largest bare rectangle: steel 0.43 of the screen, hercules 0.17, car
   (fixed) 0.12 vs yad 0.29, villa 0.39, kfar 0.14. Text-block centre off the hero centre: steel +0.11, car +0.23,
   hercules +0.21 vs yad 0.00, villa 0.00, kfar +0.17. Neither separates. The second is the only trace of a pattern
   among the three full-bleed heroes (steel, `curve`, text hugging one side; the two approved are centred), which is
   one site against two. Candidate for the loop below, not a rule.
5. **Other built clients** (their `site.json` on `site/*`): plain `split`, no form: lehem-erez-herzliya,
   patoccina (`tone: light`, H1 86 px, text/photo 0.65) and the two rejected. No hero-space note exists for the first
   two and they carry no approval either, so they count for nothing in either direction. The rebuilt lehem-erez has a
   bare rectangle of 35% of the first screen, the largest of any hero measured; if it is later rejected it is the
   fourth data point for "plain `split`".

What survives: a real, verified cause for the hollow `split` hero (2), a type scale that is a template constant (3),
and no number that predicts the user's verdict.

## The rule (what the builder does)

Before a home page goes to the user, with the shot of the hero at 1440x900 and 1280x720 in front of you and the
output of `py tools/hero-space.py <url> --out <file>` next to it, answer four questions in the delivery notes. A "no"
is fixed or explained there; it is not left for the user to find.

1. **Is the height earned?** The text is a fixed amount (H1, two-line lead, two buttons, three points: about 260-340px
   at 1440, in every layout). The rest of the hero must be a photo that carries the message or real content. A
   `cover` / `inset` / `curve` hero is at least 86vh / 76vh by CSS; when the text block is a small part of it
   (steel 0.31, villa 0.14) the first screen is a photo with a caption. Either the photo is the message (a venue, a pool, a
   building: say so) or choose a layout whose height follows its content.
2. **Does the text fill or balance its column?** `split` home heroes get a 4:4.6 portrait photo from the theme
   (`finish.css:102`) whatever the text needs, so check this one on every `split`: put the text block beside the photo: when it is about half
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

Two changes would move every hero at once and are **proposed, not made** (shared theme CSS, needs the sample-site test and a
look at every preset, and the approved kfar has the current look): (a) the `finish.css:102` photo ratio for the home
`split` hero (4:4.6 -> the car service fix, 16:11, or `main.css`' 4:3.4), which took one hero from 851 to 496 px; (b) the
hero H1 / lead scale (57.6 / 17 px). Ask the user which, if either, before touching them.

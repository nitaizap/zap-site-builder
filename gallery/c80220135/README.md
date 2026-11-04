# מרכז שירות יד מרדכי (c80220135)

| | |
|---|---|
| industry | authorised car service centre (Mazda, Ford, Dongfeng, Voyah), Ashkelon area |
| package (`tier`) | standard (12 pages) |
| state | built, not handed over: privacy parked (`privacy_confirmed` false); design-quality pass 04/11/2026 on `site/c80220135` |
| kit · archetype · preset | `bands` · `proof` · `industrial` |
| direction chosen | A, picked in automatic mode: the only direction measured under the 40% pool gate |

Screenshots: `01-home-desktop.png`, `02-home-mobile.png`, `03-inner-desktop.png` (first inner page, `p00`; check it is the page you expect before reusing).

## Tokens
Fonts: IBM Plex Sans Hebrew (headings) + Heebo (body). Palette: primary petrol `#14525e`, accent signal bronze `#b45309`, dark `#0d3a44`, surface `#e3edef`, ink `#13181c`, muted `#41505a` (6:1 on the surface). Type scale: h1 59px, h2 29.5px on inner pages (57.5px in the home bands), h3 19.2/19.5px cards and steps, 17.3px FAQ questions.

## Images
Client's own photos only (old site, spec attachments, F: drive): 0 Weave credits of 100. All source files are 800px or 1600px wide. See `sites/c80220135/IMAGE-SOURCES.md`.

## What the user corrected
- Verdict on the 04/11/2026 batch of five sites: "do not look good enough and do not adhere closely enough to their briefs". The corrections below are what that round found on this site, not quotes.
- Earlier (NOTES/OPEN-ITEMS): the Mazda logo in the importer band was the **old** lockup that the spec forbids; the spec's attached `.docx` carries the updated one and the text export had dropped it. Read the attachments inside the brief file, not only its text export.
- The `features/checks` row of six identical ticks restated the steps block above it: removed. Three dark bands in a row (1,658px of petrol) were broken by moving the waiting-room split to the plain ground.
- This pass: the two service heroes (מכונאות, דיאגנוסטיקה) stretched 800px interior photos across 1440px. They now use the 1600px facade shots, and the interiors stay in the body at their own size.
- This pass: the reviews widget's 18px stars were forced to 20px (soft and out of ratio). Fixed in the theme, PR #91.

## What to take from here
- When the client has only 800px interior photos, never use them as a full-bleed hero: save them for split bands.
- A four-marque importer band with a badge works when all chips share height (124px) and the Latin marks are cropped tight.
- Alternate dark and light bands; do not let three tinted bands run together.

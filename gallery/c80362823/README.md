# car service (c80362823)

| | |
|---|---|
| industry | passenger transport (group and corporate shuttles) |
| package (`tier`) | standard |
| state | staged, not handed over; design-quality pass 04/11/2026 |
| kit · archetype · preset | magazine · catalogue · clean |
| direction chosen | automatic mode: split hero + catalogue home (best fit for an 8-service offer), see OPEN-ITEMS #1 |

## Tokens
Noto Sans Hebrew (headings) + Assistant (body). Primary aubergine `#5b2a86`, accent burnt orange `#c2410c`, ink `#241036`, dark `#1d0f2b`, surface `#f6f2f9`. No brand colours were given. One H2 size (clamp 1.9 to 3rem) and one H3 size (1.15rem) site-wide via `custom_css`.

## Images
No client photos. 6 AI atmosphere images (all 1024x768, recorded in IMAGE-SOURCES.md, none presented as the client's own vehicles).

## What the user corrected
The user's verdict on the 04/11 build: not good enough and not close enough to the brief. The new checks then showed: H2 at three sizes (62.5/57.5/29.5 px) and H3 at three sizes on every page; a dense text wall on the home (five stacked prose H2s on white). Fixed: one heading scale, the text wall now a dark `prose band` with a legible table. Not fixable without the client or credits: all images are 1024 px, so any full-bleed hero is flagged as upscaled; `shade` + `stage` was tried and reverted for that reason.

## What to take from here
- Check source image width before choosing a full-bleed hero or the `shade`/`bands` kits.
- Home prose with several H2s reads as a wall; give it a band or split it into `faq aside` / cards.
- The "no button carries an icon" warning is a QA false positive for tel/wa buttons (icons are CSS `::before`).
- A transport client with no photography and no logo sits in the middle of the pool: it needs real photos to differ.

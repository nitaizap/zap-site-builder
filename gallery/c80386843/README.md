# מסגרית Dream from Steel (c80386843)

| | |
|---|---|
| industry | custom metalwork shop (bespoke frames, one-off steel products, shop drawings), Kfar Saba / Neve Yamin |
| package (`tier`) | `standard` (the spec's sitemap has 6 pages, over basic's cap of 5) |
| state | built and quality-passed on `site/c80386843`; re-passed 04/11/2026 against the UX acceptance list. Not handed over; privacy parked (`privacy_confirmed` false) |
| kit · archetype · preset | `frame` · `story` · `editorial` |
| direction chosen | automatic mode (spec came from intake): `frame` + `story`, because with no portfolio the craftsman's explained argument is the only thing that can carry the page |

Screenshots: `01-home-desktop.jpg` (1440), `02-home-mobile.jpg` (390), `03-inner-desktop.jpg` (service page).
The full-page mobile capture shows a few `background-attachment: fixed` bands zoomed; that is a screenshot artefact, the real viewport render is normal.

## Tokens

- Fonts: Heebo for headings and body (Frank Ruhl Libre/Assistant, then Alef, were dropped; Alef has old-style figures only, which wrecked the phone number and "20 שנה").
- Palette: primary orange `#b84606` (sampled from the client's logo, `#d15301`, deepened for 4.5:1 with white), accent steel blue `#6b8ca6`, ink slate `#1b2a36`. The orange must not change: the home measures 39% alike `kisos-beach-club`, almost no margin under the 40% line.
- Type scale after the 04/11 pass: one H2 size (clamp 1.6rem to 2.4rem) and one H3 size (1.25rem) on every page. Radius 10.
- The H2 size is also a pool-measure input: the measure buckets it at 30/40/52 px. 41px and 53px pushed the home to 40% alike kisos; 38px keeps it at 39%.

## Images

No client photographs exist (spec blank, folder empty, no website or socials). All 8 images are Weave AI (GPT Image 2.5, `gpt-image-2.5`), atmosphere only (workshop bay, brushed steel, fabrication bench, steel stock, shop drawing, cut-off saw, weld, workshop interior), never presented as the client's work. Logo from the client's Dapei Zahav listing. Regenerated 04/11 at 1920x1440 (portrait 1200x1600) via a custom `image_size`; ledger in `sites/c80386843/IMAGE-SOURCES.md`.

## What the user corrected

- 02/11 (Noam, sites team): no website and no images exist, so generate or use stock; and leave a slot on the home page for the AI brand video the client bought. Done: reserved 16:9 band with a sparks poster.
- 03/11 (client feedback on the live site): the hero was 863px tall with the text pushed aside; "generally use a different font". Hero cut to about 480px; font moved off the serif pair.
- 04/11 ("cleaner, more pristine"): Alef digits looked techy; moved to Heebo.
- 04/11, user verdict on all five sites: "do not look good enough". Findings this pass: six images shown larger than their pixels (1024px AI images up to 1440px wide), H2 at 3 to 4 sizes per page, H3 at 3 sizes, a 27px tap target, and one blog image above its pixels.
- A mistake worth recording: the first fix made every H2 uniform at 41px and then 53px; the home crossed the 40% sameness line, and at 53px the privacy page headings were far too loud. 38px satisfied both.

## What to take from here

- Generate images at their display size from the start (custom `image_size`, 1920x1440 costs the same 2 credits). `images.md` says `resolution: "2K"`; the GPT Image 2.5 contract has no such parameter and the output stays 1024.
- The engine's 100 KB image cap can shrink a file below the size it is displayed at (a 1200x1600 portrait became 675x900); check the blog image.
- Without portfolio photos the page works as an argued story: chapters, process steps, one big full-bleed process image, an orange-framed kit.
- Fix a heading scale with one `html body` rule, but re-run the pool measure after: the H2 size is part of it.

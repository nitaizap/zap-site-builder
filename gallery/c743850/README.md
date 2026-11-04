# הרקולס גורקביץ (c743850)

| | |
|---|---|
| industry | optical glass: car mirrors, convex traffic and security mirrors, brackets (B2B fleet buyers + private drivers) |
| package (`tier`) | premium |
| state | built 04/11/2026, design-quality pass 04/11/2026 · staging https://743850hercules.ussl.co.il · not launched (Zap does not launch) |
| kit · archetype · preset | `gallery` · `gallery` · `industrial` |
| direction chosen | automatic mode, picked from the brief: a catalogue-first home (13 category tiles) because buyers arrive knowing the vehicle, not the part number |

Screenshots (staging, 04/11/2026): `01-home-desktop.jpg` (1440), `02-home-mobile.jpg` (390), `03-inner-desktop.jpg` (the catalogue page).

## Tokens
- Fonts: IBM Plex Sans Hebrew (headings), Heebo (body). Alef was dropped: its digits hang above and below the line and damaged the phone number.
- Palette: primary `#754C4C` (maroon, from the logo), accent `#BD3C42`, ink `#171A1D`, text `#313940`, muted `#4C565E`, bg `#E7EAEC`, surface `#D5DDE2`, line `#C3CDD4`, dark `#14181C`.
- Type scale measured by `zs qa`: h1 59 (home 77.5), h2 53.5, h3 26/17.5 at 1440. One H2 size after the pass.
- Left the default scale: home H1 `clamp(3.6rem..5.6rem)`; hero column gap `clamp(36px, 3.4vw, 72px)`.

## Images
All client's own: the old site hercules.co.il and the client's archive on F:. 115 images, 0 AI, Weave spend 0 of 100. Sources in `sites/c743850/IMAGE-SOURCES.md` (on the site branch). The archive is low resolution (227 to 800px wide): that is the main design constraint of this site.

## What the user corrected
- Hero text and image almost touched (column gap was 0 in the theme): fixed in this client's CSS to 36-72px. Theme fix still open.
- Footer showed the white logo on a light grey footer (1.17:1): now the dark logo, picked by the engine (`footer_is_light`).
- The footer's 13-item mirror list was too long: grouped under four labels (flat menu, label items without a link). Reads well at 390.
- The brief asks for a video: a reserved 16:9 band between the story and the lead form, stable when the clip arrives (now 16:9 at every width).
- Alef was dropped for the phone number's digits (above).
- The design-quality pass on 04/11/2026 (the new `zs qa` checks): photos were shown larger than their own pixels on 17 pages (27 errors), review stars stretched, home H2 at three sizes, the lead band's button at 1.34:1. All fixed per client; see OPEN-ITEMS 23-27.

## What to take from here
- Check the pixel size of every client photo **before** choosing a card style: a 250px photo cannot fill an overlay tile or a split box. Classic cards (photo above, text below, at the photo's own size) survive a weak archive.
- A full-bleed photo band needs a 1440px source. With 800px, use a solid band and make sure the submit button still clears contrast.
- Group a long footer list under labels instead of a single column of 13 links; test it at 390.
- Reserve a video frame as a real composed band at 16:9 from the start.

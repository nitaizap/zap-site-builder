# מוניות כפר סבא בע״מ

| | |
|---|---|
| industry | taxi rank and scheduled transport, Kfar Saba |
| package (`tier`) | standard |
| state | staging https://2910210kfarsabataxis.ussl.co.il (pushed 03/11/2026); design-quality round 04/11/2026 on branch `site/c2910210`, not yet re-pushed. Privacy parked |
| kit · archetype · preset | panels · booking · bold, hero split |
| direction chosen | automatic mode, no gate: "call now" business, so phone, buttons and lead form sit in the first screen |

Screens: `01-home-desktop.png`, `02-home-mobile.png`, `03-inner-desktop.png`.

## Tokens
Rubik headings over Heebo body. Primary green `#0C5137` (client's sign and card), accent taxi yellow `#F2C200`
(ink `#1A1400`), dark `#0A2E21`, surface `#EFF4F0`. Radius 16. Yellow hero band, display-size call button.

## Images
All 9 photos are the client's own (F:\SiteContent\02910210), 0 AI credits, 0 stock. Most are 2006 and 2012
snapshots at 768 to 1024px: they cannot fill a full-bleed band. Details in `sites/c2910210/IMAGE-SOURCES.md`.

## What the user corrected
- "The taxi site looks nothing like those 2 references" (moniot.info, nitzav-taxi.co.il). First screen was
  rebuilt (yellow hero, large phone number, form inside the fold). In the design-quality round the rest of the
  home followed: services became solid tiles alternating white and dark green on a yellow band, the closing call
  band went green.
- Found by the new `zs qa` checks, not by eye: a 768px portrait stretched as a full-bleed band (upscaled on
  desktop, about 1000px tall on mobile), now a normal split; a blog photo shown above its pixels; heading scale
  and tap-target warnings (home H2 at three sizes still open).
- Open: no preview round existed, so no fidelity pass against an approved direction was possible.

## What to take from here
- When the references are flat colour fields with one repeated phone number, carry the field down the whole home,
  not only the hero: the first screen alone reads as one good band on a grey page.
- Never put a small portrait photo in a full-bleed overlay; use a split.
- Third-party star images (Dapei Zahav) need a 18px box with auto height, or `zs qa` flags them (theme fix pending).

# Benchmark — the finish level to reach

Read (open the images) before the design gate. These are the Zap builds the user called "amazing".

| file | what to learn from it |
|---|---|
| `benchmark/vlad-hydronics-desktop.jpg` | Vlad's build (hydronics.zapsites.co.il). The reference. |
| `benchmark/zap-template-towing-desktop.jpg` | A strong Zap template (towing): cinematic hero, orange stat band, real photo grid. |
| `benchmark/engine-v2-mehirut-haor-desktop.jpg` | This engine after the finish layer, on the first pilot's real content. |

## What makes the reference look expensive

1. **Scale and weight.** H1 and H2 are huge (≈70–90px desktop), weight 800, tight leading (~1.05), set in
   two lines; the second line or the brand name in the accent colour; statements end with an accent period.
2. **Cinematic imagery.** The hero is a full-bleed, dark, moody photo of the real subject (industrial pumps,
   tow trucks) with text over a deep gradient. Photos everywhere are consistent in light and colour.
3. **Restraint.** Charcoal, white, one red. Sharp corners, hairline rules, almost no shadows. No pastel
   boxes, no rounded "app" cards.
4. **Editorial furniture.** Tracked micro-labels above titles ("ABOUT OUR WORK", "PRODUCT FAMILIES / 01"),
   numbered items ("03 / COLLECTION"), ↗ arrow links with an underline, a dark utility bar on top.
5. **Asymmetry.** Title on one side, paragraph on the other; grids of image cards with text over a dark
   gradient; one full-bleed red CTA band and a dark footer.
6. **Rhythm.** Light → dark band → light → image grid → red CTA → dark footer. Never two identical blocks
   in a row, never three dark ones.

## How the engine maps to it

| reference element | engine |
|---|---|
| giant two-tone headline + accent period | any `title` with `\n`, `*accent*`, trailing `.` |
| micro-labels | `eyebrow` on every section |
| cinematic hero | `design.hero: "image"` + a dark, strong 2K photo |
| stat band | `trust` (default `style: band`) |
| image cards with overlay + numbers | `cards` where every item has an `image` (automatic `overlay`) |
| asymmetric heads | `title` + `intro` (automatic) |
| dark utility bar | automatic (`header.topbar_text` for the left side) |
| sharp, hairline, one accent | `design.preset: "signature"` |
| ribbon of services | `marquee` |
| red CTA band | `cta` (brand colour by default) |

What the engine can't give you: the photography and the words. Those decide whether the result looks like
the reference or like a template. Spend the effort there.

# מקורות תמונות — מסגרית Dream from Steel (80386843)

לפי הנחיית שרון יוסף מ-20/10/2026 (ייעוץ עו"ד קובי בארי): כל תמונה באתר חייבת תיעוד מלא.
תמונה שמקורה לא ודאי — לא עולה לאתר.

| file | source | license | date | by | credits |
|---|---|---|---|---|---|
| `assets/hero.webp` | AI — Figma Weave, GPT Image 2.5 (`gpt-image-2.5`, quality medium, landscape_4_3) | generated for this client | 2026-11-02 | ניתאי צוויג | 2 |
| `assets/steel-texture.webp` | AI — Figma Weave, GPT Image 2.5 | generated for this client | 2026-11-02 | ניתאי צוויג | 2 |
| `assets/fabrication.webp` | AI — Figma Weave, GPT Image 2.5 | generated for this client | 2026-11-02 | ניתאי צוויג | 2 |
| `assets/materials.webp` | AI — Figma Weave, GPT Image 2.5 | generated for this client | 2026-11-02 | ניתאי צוויג | 2 |
| `assets/drawing.webp` | AI — Figma Weave, GPT Image 2.5 (`gpt-image-2.5`, quality medium, landscape_4_3) | generated for this client | 2026-11-02 | zap-site build session | 2 |
| `assets/sparks.webp` | AI — Figma Weave, GPT Image 2.5 (`gpt-image-2.5`, quality medium, landscape_4_3) | generated for this client | 2026-11-02 | zap-site build session | 2 |
| `assets/weld.webp` | AI — Figma Weave, GPT Image 2.5 (`gpt-image-2.5`, quality medium, landscape_4_3) | generated for this client | 2026-11-02 | zap-site build session | 2 |
| `assets/workshop.webp` | AI — Figma Weave, GPT Image 2.5 (`gpt-image-2.5`, quality medium, landscape_4_3) | generated for this client | 2026-11-02 | zap-site build session | 2 |
| `assets/logo.png` | the client's own logo, from their Dapei Zahav listing: `img.d.co.il/Customers/80386843/acb7aca1e2f6445ab3dd097419f2f064.png` (the business's own customer folder on Zap's image CDN). The directory serves it flattened onto a grey backing; that flat backing was keyed out by flood-fill from the edges, nothing inside the badge was altered and nothing was redrawn | the client's own mark, held by Zap for this customer id | 2026-11-02 | zap-site build session | 0 |
| `assets/favicon.png` | cut from `assets/logo.png` above (the badge, centred on the logo's own slate) | derived from the client's own logo | 2026-11-02 | zap-site build session | 0 |

**Weave budget:** 16 of 100 credits used for this client. 8 at intake (the first four), 8 in the build session (the four below, approved as one batch).

## Why these are atmosphere only

The client supplied no photographs: `F:\SiteContent\80386843` is empty, the spec sheet carries no
WeTransfer or Drive link, and the business has no website, Facebook or Instagram. Its Dapei Zahav
listing (`d.co.il/80386843/33060/`) holds only a generic category cover, not their own work.

So all eight are **atmosphere**, never the client's premises or their work presented as real: a workshop
bay, a brushed steel surface, a fabrication bench, raw steel stock, a shop drawing with measuring tools, a
cut-off saw throwing sparks, a weld bead on a joint, and a second workshop interior. Every one of them shows
material or process, never a finished product. There is
deliberately **no gallery of finished gates, railings or structures** — generated examples would read
as this metalworker's portfolio, which is exactly what `references/images.md` forbids and what a
customer would reasonably be misled by.

## Still needed from the client

- photographs of completed work (gates, railings, structures) for a real gallery
- a photograph of the workshop
- a photograph of Ofir for the about page
- **the logo at a usable resolution.** The copy in use came from the Dapei Zahav listing and is only
  140x140px, which is the largest the CDN serves. It is sharp enough for the header at 96px but soft on a
  high-density screen, and it cannot make a crisp 512px favicon. The client has the original: ask for the
  source file (SVG, AI/EPS, or a PNG of 512px or more)

Until those arrive the site ships without a portfolio section. Each one added later needs its own row
in the table above.

## The logo and the favicon

The sites team said on 02/11 that a logo exists ("יש רק לוגו") but the file never reached this branch. It
was found instead on the client's own Dapei Zahav listing, in Zap's `Customers/80386843/` folder: a hexagonal
badge, dark slate with an orange rim, reading DREAM / FROM / STEEL. The site's palette is now sampled from it
(orange `#b84606` deepened from the logo's own `#d15301` for contrast, slate `#1b2a36`).

The directory serves it flattened onto a flat grey square, which would show as a grey tile on a white header,
so that backing was keyed out. Only the uniform backing was removed; the badge itself was not touched or
redrawn. The favicon is the same badge, centred on the logo's slate.

Still wanted: the original file at a usable resolution. 140x140 is all the CDN has.

### Confirmed against the brief's own .docx, 04/11/2026

The brief is also held as `brief/איפיון אתר - מסגרית Dream from Steel - 80386843.docx`, and the text export
`brief/brief.md` silently drops what is embedded in it. Opened as a zip, `word/media/` holds the logo
(`8b835a2258d1de5fad7db48f12750f040832ecd1.png`, referenced as `rId7` from the "לוגו" row of section 6), so
**the logo the site uses is confirmed as the client's own, from the client's own spec sheet** and not only
from the directory listing. The two files are the same image: both 140x140, both flattened onto the same
grey backing, mean absolute difference 3.7/255 against the keyed copy recomposited on that grey.

That closes the question of whether a logo exists and whether this is it. It does **not** close the
resolution item: the brief's copy is 140x140 as well, so there is still no file big enough for a crisp
favicon, and the original is still worth asking Ofir for.

`word/media/image1.png` in the same archive is a 200x200 advert for מוניות כפר סבא. It is referenced from
nowhere in `word/document.xml` (only `rId7` is), so it is a leftover of the form template, not this
client's material. It is not used and must not be.

## What the site says about these images

The footer of every page carries, next to the copyright:
"תמונות האתר הופקו בכלי בינה מלאכותית ואינן מציגות עבודות של העסק".

### The listing re-read, 04/11/2026 (second pass)

Both Dapei Zahav listings for this customer id were fetched and read again, to see whether any
photograph of the business or its work exists there. **Exactly one image on either page belongs to
this customer**, `img.d.co.il/Customers/80386843/acb7aca1e2f6445ab3dd097419f2f064.png`, and it is
the logo already recorded in the table above. The two other images are Zap's own category covers
(`img.d.co.il/Umbraco/8844/coverimagedesktop.png` and `Umbraco/8977/coverimage-מסגריות.png`); they
are stock belonging to the directory, not to this client, and are not used.

No photograph was taken from the listing in this pass, and no row was added. The list under "Still
needed from the client" above is unchanged and still correct.

### The footer logo, 04/11/2026

`assets/logo.png` is now also named as `logo_light` in `site.json`. No new file and no new artwork:
the engine was generating a white silhouette of this same badge for the footer and the kit paints
the footer white, so the footer's logo was invisible. Naming the real file makes the footer show
the badge already recorded above. Nothing about the image's source changes.

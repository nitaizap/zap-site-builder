# Images

## Order of preference

1. **The client's own photos** (work, premises, team, products, certificates). Ask for them at intake.
2. **Photos from the client's current site** that show their real work or products. Download them into
   `sites/<slug>/assets/`, describe what they actually show in `alt`.
3. **AI atmosphere images via Figma Weave** (below) for heroes, service cards and splits when real photos
   are missing. Mark them `"ai": true`.
4. **No image.** Every section works without one (hero falls back to a typographic layout, cards to icons).
   Better than a picture that misrepresents the client.

## Weave (Figma MCP connector) — the default AI route

No Weave flow is needed: run the model directly. Verified 2026-10-07 (3.5 credits, 1264×848 hero, good).

| use | model (weave_run_model id) | settings | ≈ credits |
|---|---|---|---|
| all site photos (default) | GPT Image 2.5 `2db90e64-51dd-45b2-870a-66d19a81118e` | `quality: "medium"`, `image_size: "landscape_4_3"` (cards/hero) or `"portrait_4_3"` (split), `output_format: "webp"` | 8 |
| a hero worth the extra detail | same, `quality: "high"` or variant `"Sunburst"` | Sunburst is slower, tighter control, for production imagery | 8+ |
| alternative look | Nano Banana 2.1 `bebebed5-50c1-4701-98b3-86929db21585` | `resolution: "1K"`, `aspect_ratio: "3:2"` or `"4:5"`, `output_format: "webp"` | 7 |

Credits are the workspace's Weave credits (not Figma AI credits). Default to 1K: the theme never shows
an image wider than ~1200px except the full-bleed `hero: image` layout, where 2K is worth it.

### The budget — 100 Weave credits per client, no approval needed under it

Each client has a standing budget of **100 Weave credits**. Spend it without asking. Only going over
100 for that client needs the user's approval, and then only for the part that goes over.

At ~8 credits per GPT Image 2.5 image that is roughly 12 images, which is more than a site needs: the
budget is a guard against a runaway loop, not a tight allowance. Rerolling a bad image is normal and
comes out of the same 100.

(The quotes above are what the models quote today. The earlier figure of 3.5 credits in this file was
from 2026-10-07 and is no longer right — always read the quote rather than this table.)

1. Plan all images for the site first (key, what it shows, aspect). Quote each (`weave_run_model`
   without `acknowledgedCost` only quotes and spends nothing).
2. Add the quotes to what this client has already spent, from `sites/<slug>/IMAGE-SOURCES.md`.
   - **Total ≤ 100** → run them, echoing each quoted `acknowledgedCost`. Do not ask.
   - **Total > 100** → ask once with AskUserQuestion, showing the spend so far, what is left to make
     and the overage. Run nothing beyond 100 until they approve.
3. Poll `weave_get_model_run_output` until `COMPLETED`, then download each output:
   `bin/zs fetch-image <slug> <key> "<output url>"` → `sites/<slug>/assets/<key>.webp`
4. Read the image before using it. Reject and regenerate anything with text, people, a wrong object,
   or a look that doesn't match the rest of the set. A reroll needs no approval while under 100.
5. Record every generated image in `sites/<slug>/IMAGE-SOURCES.md` (below) as you go, with its credits.
   An image that is not recorded there must not ship.

### IMAGE-SOURCES.md — required before publish

Legal instruction from שרון יוסף, 20/10/2026, after review by עו"ד קובי בארי: a copyright claim can reach
₪100,000 per image, with no need to prove damage. **Every** image on a client site must be recorded, not
only AI ones, and an image whose source is uncertain must not be used at all.

`sites/<slug>/IMAGE-SOURCES.md` holds one row per image file:

| file | source | license | date | by | credits |
|---|---|---|---|---|---|
| `assets/hero.webp` | AI — Figma Weave, GPT Image 2.5 | generated for this client | 2026-11-02 | ניתאי צוויג | 8 |
| `assets/gate-3.webp` | client's own photo (F:\SiteContent\<id>) | client supplied | 2026-11-02 | ניתאי צוויג | 0 |

For AI, name the tool **and** the model — "AI" alone does not satisfy the instruction. For a downloaded
photo, name the site it came from and the licence type (free / paid / free for commercial use). The
`credits` column doubles as the Weave budget ledger for this client.

If the Figma connector is not available in the session, fall back to `bin/zs image` (OpenAI key on the
environment) or to step 4 of the preference list, and say so.

## Prompt rules

- English, specific, photographic: subject, setting, light, palette, lens feel. End with
  "Photorealistic, natural light, no people, no faces, no text, no letters, no logos, no watermarks."
- Never people (a generated "team" contradicts a real business), never the client's premises presented as
  real, never Hebrew text in an image (it always renders wrong).
- One visual family per site: same light and palette, so the set looks commissioned, not collected.
  Mention the brand colour subtly ("cool blue and white tones", "warm brass details").
- Israeli context where it matters (apartment kitchens, tiled floors, typical fixtures), never stereotypes.

Example (the verified sample hero): "Editorial interior photograph of a modern bright Israeli apartment
kitchen, the under-sink cabinet open showing new white PEX water pipes and brass fittings, a professional
plumber's toolbox on the tiled floor, soft morning daylight from a window, cool blue and white tones,
shallow depth of field. Photorealistic, natural light, no people, …"

## Video (optional, premium)

Veo 3.1 image-to-video (`fg6e8647-d90a-4bad-a845-69fdc102a14j`, `duration: "4s"`, `generate_audio: false`,
`resolution: "720p"`) can animate the approved hero photo into a short loop, ≈ 90 credits. Only with the
user's explicit go-ahead for that client. Download it with `zs fetch-image <slug> heroloop <url> --ext mp4`,
add `"videos": {"heroloop": {"src": "assets/heroloop.mp4", "ai": true}}` and `"video": "heroloop"` on the hero.
Over 6 MB the validator stops the build: ask for the 720p, 4 s variant.

## Do not

- Copy photos from Google Maps, other businesses, or press sites without permission.
- Use visible captions like "תמונה להמחשה" (the validator blocks it).
- Put a dark logo on a dark header: provide `logo_light`, or choose `header: light`.

## Technical (automatic)

The build converts photos to WebP, caps width at 1600px, steps quality down to ~160KB, keeps logos as PNG,
writes ALT from `site.json`, marks AI images in the media library, and re-imports a file only when it changed.

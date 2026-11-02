# Images

## Rights: every image is recorded, or it is not used

Standing instruction from שרון יוסף, 20/10/2026, after review by עו"ד קובי בארי: a copyright claim over a
single image can reach **₪100,000, with no need to prove damage**. So:

- **An image of uncertain origin is not used.** No "probably fine", no reverse-image guesswork. Drop it and
  use one of the other options below, or no image at all.
- **Every image uploaded to a client site gets a row in `sites/<slug>/IMAGE-SOURCES.md`**, committed on the
  client's branch, before delivery. One row per file:

  | file | uploaded | by | source | licence |
  |---|---|---|---|---|
  | `assets/hero.webp` | 2026-11-02 | Claude (session <slug>) | AI: Figma Weave, model Nano Banana 2.1 | generated, no third-party rights |
  | `assets/shop-front.webp` | 2026-11-02 | <name> | client sent it (WeTransfer, 2026-10-30) | client's own photo |
  | `assets/tiles.webp` | 2026-11-02 | <name> | https://unsplash.com/photos/xxxxxxx | Unsplash Licence |

  For a downloaded photo: the **site** it came from and the **licence type**. For AI: the **tool and the
  model** (not just "AI"). The client's own photos: how and when they arrived.

## Budget: 100 Weave credits per client

Spend freely under 100 credits for a client. Only going over that needs the user's decision - which is
separate from the per-batch cost gate below, which is always required.

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
| all site photos (default) | Nano Banana 2.1 `bebebed5-50c1-4701-98b3-86929db21585` | `resolution: "1K"`, `aspect_ratio: "3:2"` (cards/hero) or `"4:5"` (split), `output_format: "webp"` | 3.5 |
| a premium client's hero | same, `resolution: "2K"` | | 5 |
| alternative look | GPT Image 2.5 `2db90e64-51dd-45b2-870a-66d19a81118e` | `quality: "medium"`, `image_size: "landscape_4_3"` | 8 |

Credits are the workspace's Weave credits (not Figma AI credits). Default to 1K: the theme never shows
an image wider than ~1200px except the full-bleed `hero: image` layout, where 2K is worth it.

### The cost gate — one approval per batch

`weave_run_model` without `acknowledgedCost` only quotes. Every run needs the user's explicit approval:

1. Plan all images for the site first (key, what it shows, aspect). Quote each (no `acknowledgedCost`).
2. Ask **once**, with AskUserQuestion (Approve / Cancel): the list of images and the total credits.
3. On approval run each with its quoted `acknowledgedCost`. Never exceed what was approved; anything
   extra (a reroll, a new image) is a new approval.
4. Poll `weave_get_model_run_output` until `COMPLETED`, then download each output:
   `bin/zs fetch-image <slug> <key> "<output url>"` → `sites/<slug>/assets/<key>.webp`
5. Read the image before using it. Reject and regenerate (with approval) anything with text, people,
   a wrong object, or a look that doesn't match the rest of the set.

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

- Use any image you cannot write a source row for (see *Rights*, top of this file).
- Copy photos from Google Maps, other businesses, or press sites without permission.
- Use visible captions like "תמונה להמחשה" (the validator blocks it).
- Put a dark logo on a dark header: provide `logo_light`, or choose `header: light`.

## Technical (automatic)

The build converts photos to WebP, caps width at 1600px, steps quality down to ~160KB, keeps logos as PNG,
writes ALT from `site.json`, marks AI images in the media library, and re-imports a file only when it changed.

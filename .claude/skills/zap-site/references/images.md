# Images

## Order of preference

1. **The client's own photos** (work, premises, team, products, certificates). Ask for them at intake.
2. **Photos from the client's current site** that show their real work or products. Download them into
   `sites/<slug>/assets/`, describe what they actually show in `alt`.
3. **AI atmosphere images** for heroes and service cards when real photos are missing:
   `bin/zs image <slug> <key> "<English prompt>"` (needs `OPENAI_API_KEY` on the environment). Mark them
   `"ai": true` in `images`. The footer note and media descriptions are added automatically.
4. **No image.** Every section works without one (hero falls back to a typographic layout, cards to
   icons). Better than a stock photo that misrepresents the client.

## AI prompt rules

- English, specific, photographic: subject, setting, light, lens feel. The engine appends
  "no people, no faces, no text, no logos, no watermarks".
- Never people (a generated "team" contradicts a real one-person business), never the client's premises
  presented as real, never Hebrew text inside an image (it always renders wrong).
- One visual family per site: same light and palette, so the set looks commissioned, not collected.
  Mention the brand colour subtly ("cool blue tones", "warm brass details").
- Sizes: hero/split `1536x1024`, cards `1536x1024` (cropped to 16:10 by the theme).

Example: `zs image mayim-tovim hero "Modern bright kitchen, under-sink cabinet open showing new white PEX
pipes and a professional plumber's toolbox on the floor, morning daylight from a window, cool blue tones"`

## Do not

- Copy photos from Google Maps, other businesses, or press sites without permission (credit press images
  only with the client's OK).
- Use visible captions like "תמונה להמחשה" (the validator blocks it).
- Put a dark logo on a dark header: provide `logo_light`, or choose `header: light`.

## Technical (automatic)

The build converts photos to WebP, caps width at 1600px and steps quality down to ~160KB, keeps logos as
PNG, writes ALT from `site.json`, and re-imports a file only when it changed.

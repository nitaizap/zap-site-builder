# הוילה הלבנה ינוב — notes

| fact | value | source |
|---|---|---|
| client no. | 80392936 (weekend 27824) | איפיון xlsx |
| phone (also WhatsApp) | 054-6666662 | xlsx ("טלפון ישיר"); WhatsApp field empty → same mobile (assumption) |
| email | shimon@ashrh.co.il | xlsx |
| address | מורד התאנה 29, ינוב | xlsx |
| Instagram | instagram.com/_the_white_villa | xlsx |
| 3.5 dunam, 5 bedrooms, 22 beds, events ≤150, half-olympic pool + slide | xlsx copy |
| Shabbat: no grill, no music | xlsx |
| domain | thewhitevilla.co.il (requested) | xlsx |

Images: only the client's Drive folder "להשתמש רק בתמונות בתקייה הזאת" (24 of 39 used) + logo.jfif (background made transparent) + WhatsApp video (6 s silent hero loop, desktop). No stock, no AI.
Direction: A (light, Frank Ruhl Libre / Assistant, olive #3f4b39 + brass #8a6a3a) — chosen on autopilot.
Staging: https://80392936.ussl.co.il — pushed, live QA 0 errors.

## Redesign 22/10/2026 (team playbook + template pool)
The user approved the pilot (`site/white-villa-pilot`) and asked for this build to look like it. site.json now
carries the pilot's design and composition: base template 2, olive + jacaranda, Miriam Libre, inset hero with the
pool video, `split:duo`, `gallery:stagger`, framed cards, `features:rows`, `tiles`, FAQ beside the jacaranda,
`cta:photo`; descriptions 150-160 and a blog page (SEO checklist). Facts and copy unchanged. Local: `zs qa` 0
errors, `zs seo` 0 FAIL. The garland and carousel sections stay in the engine, unused here.

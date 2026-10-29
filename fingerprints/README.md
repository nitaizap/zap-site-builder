# Measured layouts of client sites (the registry)

Every new site is compared with every file here and with `sites/<slug>/fingerprint.json` on every `site/*` branch.
`zs qa`, `zs preview`, `zs pool`, `zs push` and `zs package` stop when a site is **45% or more** like another client
(palette, the furniture every page repeats, the components on the home page, the layout; `engine/fingerprint.py`).

- New sites need nothing extra: `zs qa` writes `sites/<slug>/fingerprint.json`, committed on the site's branch.
- Sites that live elsewhere (a `claude/*` branch, a delivery branch, built before the measure) are added here:
  `ZS_MEASURE_ONLY=1 zs build <slug>` (old sites may break today's validator; this builds them for measurement only),
  then `zs registry <slug>`, then commit the file to `main` by PR.

Seeded 29/10/2026 with white-villa, patoccina, mehirut-haor, bella-mare and nick-itum. The user judged these five
"all the same"; they measure 42-60% alike to each other, which is where the 45% limit comes from.

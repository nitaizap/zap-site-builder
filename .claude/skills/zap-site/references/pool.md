# The template pool — mix, don't copy

Every client gets a site that fits the business, assembled from a shared pool, never a fixed
template. A site is a combination of three independent layers; vary all three:

1. **Package** (`tier` in site.json): how big and how simple.
2. **Style kit**: `preset`, `tone`, fonts, palette, radius, motion, hero layout (`references/design.md`).
3. **Section variants**: the order of the sections and the `variant` each one uses (the catalogue below).

The same variant under another preset looks like a different site, so the pool multiplies. The look still
comes from tokens and presets, and the variants only change arrangement; every variant passes `zs qa` under
every preset.

## Packages

| `tier` | pages (privacy/blog not counted) | allowed | use it for |
|---|---|---|---|
| `basic` | up to 5 | simple sections only: no `road`, `route`, `marquee`, `video`, `posts`; hero = one still photo | the "אתר בייסיק" package: one-page-feeling sites like the restaurant references |
| `standard` | up to 12 | the whole pool | most service businesses |
| `premium` | no cap | the whole pool + hero video/slider, motion `lively`, Weave video | flagship builds (the benchmark level) |

Leave `tier` out only for legacy sites. The validator stops the build when a site breaks its package.
Basic sites must still meet every other rule (QA 0 errors, real facts, Zap standards).

## Section variants (`variant` on a section)

| type | variant | what it looks like | source | needs |
|---|---|---|---|---|
| `split` | *(default)* | text + photo, optional badge, arch/square shape | engine | |
| `split` | `frame` | text in a panel inside a thin offset brand-colour frame, photo beside it | template 1 "קצת עלינו" | `image` |
| `cards` | *(default)* `overlay` / `classic` / `layout: bento` | photo tiles with text over the photo / boxed cards / bento | engine | |
| `cards` | `framed` | square photos each with an offset hairline frame, brand-colour caption below ("projects") | template 1 "גלריית פרויקטים" | images |
| `features` | *(default)* | icon grid | engine | |
| `features` | `aside` | 3–4 icon rows stacked beside a framed photo ("למה לבחור בנו") | template 1 | `image` |
| `features` | `checks` | white check tiles on a brand gradient ("יתרונות"), short titles only | template 1 | |
| `gallery` | *(default)* | grid, first photo large when 5+ | engine | |
| `gallery` | `mosaic` | tight 4-column square grid, no gaps (2 on mobile), 8 photos | template 1 "גלריה" | 4 or 8 images |
| `faq` | *(default)* | soft cards, round +/- icon | engine | |
| `faq` | `outline` | centred title, outlined brand-colour rows | template 1 | |
| `contact` | *(default)* | NAP + form + map | engine | |
| `contact` | `photo` | NAP + form beside a full-height photo, no map | template 1 | `image` |
| `leadbar` | *(type)* | rounded brand band with a one-row form (name, phone, email) mid-page | template 1 | once per page, not next to the footer lead band |

Hero layouts (`split`, `image`, `centered`), `trust` styles, `marquee`, `road`, `route`, `steps` and the
presets are documented in `site-json.md` and `design.md`; they are part of the pool too.

**Adding to the pool** (engine work, own branch + PR): one entry in `VARIANTS` (`engine/sections.py`), markup
only if the arrangement truly needs it, CSS in `wp/theme/zap-base/assets/pool.css` scoped to `.zs-v-<name>`,
a row in this table, then `zs build sample && zs qa sample` with 0 errors and a look at desktop + mobile.

Sources so far: template 1 (Zap Figma "תבניות", pergola demo, `benchmark/zap-template-1-full.jpg`).
Next to extract: the basic-site references lacuccina.co.il, kira.rest.co.il, zapgroup.wixsite.com/35424380 and /website-890.
The rest of the Figma file is waiting for edit access: extract each new template into variants the same way.

## Mixing rules (anti-formula)

- **Start from the business, not from the pool.** Pick sections for what this client must prove (a
  restaurant: menu, atmosphere, booking; a trade: speed, trust, area; a clinic: calm, credentials). Then pick
  the variant that best tells it.
- **No two neighbours alike**: never the same type or the same "shape" (two framed sections, two
  photo grids) back to back; one brand-colour band (`checks`, `leadbar`, `cta`, `marquee`) per screenful.
- **At most two template-1 variants on one page**, so the sites don't all start to look like that template.
- **Every direction in the gate differs in at least one variant as well as preset/hero.**
- Before the gate run `bin/zs pool <slug>`: it compares the home-page recipe and design levers with every
  other client on a `site/*` branch (`git fetch` first). A "too close" warning means swap variants or a
  lever, and write the reason for each choice in NOTES.md (one line per section).

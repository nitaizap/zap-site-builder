# הרקולס-גורקביץ ייצור מראות ואביזרים לרכב בע"מ — c743850

## Facts (source per fact)

| fact | value | source |
|---|---|---|
| שם העסק | הרקולס-גורקביץ ייצור מראות ואביזרים לרכב בע"מ | טופס האפיון |
| שם מוצג באתר | הרקולס גורקביץ | טופס האפיון + האתר הקיים |
| מספר לקוח | 743850 | טופס האפיון |
| שנות פעילות | משנת 1949 | טופס האפיון + hercules.co.il/פרופיל |
| בעלים / איש קשר | יוסי גורקביץ; אסי גורקביץ 052-3909018 | טופס האפיון (לא מופיע באתר) |
| כתובת | דרך שלמה 13, תל אביב 6811123 | טופס האפיון + האתר הקיים |
| טלפון לאתר | 03-6828265 | טופס האפיון + האתר הקיים |
| וואטסאפ | 052-2904020 | טופס האפיון |
| אימייל לאתר ולטופס לידים | mirrors@zahav.net.il | טופס האפיון + האתר הקיים |
| שעות פעילות | א׳-ה׳ 8:00-17:00, ו׳ 8:00-13:00 | טופס האפיון + האתר הקיים |
| אתר קיים | https://www.hercules.co.il/ | טופס האפיון |
| תו תקן | ISO 9001, מכון התקנים הישראלי | טופס האפיון + תמונת תו התקן בחומרי הלקוח |
| לקוחות גדולים | משרד הביטחון, משטרת ישראל, אגד, דן, מרכבים, הארגז | טופס האפיון |
| יעדי ייצוא | הולנד, דנמרק, ארצות הברית, קנדה, ספרד | טופס האפיון + האתר הקיים |
| תחילת הייצוא | 1990 | טופס האפיון |
| סוכנים בחו"ל | Safe-Driving, Compaction | טופס האפיון |

Research done: the client's existing site was crawled with `bin/zs grab` (31 pages, 107 images,
`research/hercules.co.il.md`), and the client's archive on `F:\SiteContent\00743850` (2,249 files) was
pulled in by `bin/zs intake` (396 files copied into `assets/client/`).

**Obsolete wording kept out:** the old site's profile page says "60 שנות ניסיון", written years ago. The
brief says "משנת 1949", so the site states the founding year and never a number of years.

## Design brief (the three lines)

- **Subject:** optical glass. A family of opticians making car mirrors in Tel Aviv since 1949: panoramic
  crystal, prisms, convex traffic mirrors, security scan mirrors, arms and brackets.
- **Audience and moment:** a fleet buyer, a garage or an accessory shop looking for a mirror for a specific
  vehicle or a specific job, plus a private driver who needs one part. They arrive knowing the vehicle, not
  the catalogue number.
- **The page's single job:** get them into the right category and then onto the phone or the form.

## Design direction (automatic mode: chosen here, not at a gate)

| lever | choice | why |
|---|---|---|
| `tier` | `premium` | 18 pages; `standard` caps at 12 and the brief's sitemap alone is 16 |
| `kit` | `gallery` | photo-led, edge-to-edge grids. 108 real product photographs are the site's substance |
| `archetype` | `gallery` | the pictures do the talking: the catalogue and two photo sections carry the home |
| `base_template` | 6 | taken for its logo band and dark panels; palette, hexagons and promo banner dropped |
| `preset` | `industrial` | sharp, heavy, accent rules: a manufacturer, not a boutique |
| `hero` | `split` | the client's strongest in-situ photograph beside a large H1 |
| fonts | IBM Plex Sans Hebrew / Heebo | corporate and precise, for a precision manufacturer |
| radius | 8 | |
| motion | `subtle` | the brief asks for no movement |
| palette | primary `#754C4C`, accent `#BD3C42`, page `#E7EAEC` / `#D5DDE2`, dark `#14181C` | |

**The palette comes from the logo.** The logo's wordmark samples to `#BD3C42`; that red carries the accent.
The brand red could not carry the buttons: measured against the pool it put the home at 52% like
mehirut-haor, so `primary` is that same red taken deeper and desaturated (`#754C4C`), which is what
`design.md` prescribes. The page ground is the cool grey of the client's own studio backdrop.

**The one bold element:** the client's own photographic archive, shown at full width. Every category page
carries its real products with their real catalogue numbers, and the home runs a film strip and a carousel
straight out of the same archive.

## Uniqueness (measured, `bin/zs qa` / `bin/zs pool`)

Final: **max 38%** (betzel-hateena), then mehirut-haor 36%, patoccina 36%, c80386843 35%. Gate is 40%.

Getting there took a measured search, not taste. What moved it, in order:
1. **The footer tone.** All eleven competitors measured `light/3`. The `gallery` kit paints the footer from
   `--c-bg`, so a page ground at luminance 0.91 puts it in a `tint` bucket nobody else occupies.
2. **The component vocabulary.** `chapters`, `filmstrip` and `carousel` are used by no other client;
   `features:checks`, `split:duo`, `overlay`, `facts` and `posts` were each dropped once a sibling landed
   using them.
3. **The palette**, last. A sweep over the full HSV space showed no colour could pull the home under 40%
   on its own, which is why the structure had to move first.

Nothing under `fingerprints/` was touched and the threshold was not changed.

## Pages

| page | keyword | H1 |
|---|---|---|
| דף הבית | מראות לרכב | הרקולס גורקביץ |
| פרופיל | הרקולס גורקביץ | פרופיל |
| תחומי פעילות | סוגי מראות לרכב | תחומי פעילות |
| מראות עזר לכיסוי שטחים מתים | מראות עזר לשטחים מתים | מראות עזר לכיסוי שטחים מתים |
| מראות לרכבים פרטיים | מראות לרכב פרטי | מראות לרכבים פרטיים |
| מראות למשאיות | מראות למשאיות | מראות למשאיות |
| מראות לאוטובוסים | מראות לאוטובוסים | מראות לאוטובוסים |
| מראות קמורות לאיתור גניבות | מראות קמורות | מראות קמורות לאיתור גניבות |
| מראות לאיפור | מראות מגדילות לאיפור | מראות לאיפור |
| מראות בטיחות | מראות סריקה וביטחון | מראות בטיחות |
| מראות פנימיות | מראות פנימיות לרכב | מראות פנימיות |
| זרועות למראות | זרועות למראות רכב | זרועות למראות |
| מראות לתינוק | מראה לתינוק לרכב | מראות לתינוק |
| מראות לאופנועים | מראות לאופנועים וקטנועים | מראות לאופנועים |
| פנסים לכל סוגי הרכב | פנסים לרכב | פנסים לכל סוגי הרכב |
| מראות לרכבי אספנות | מראות לרכבי אספנות | מראות לרכבי אספנות |
| מאמרים | מאמרים על מראות לרכב | מאמרים |
| צור קשר | הרקולס גורקביץ צור קשר | צור קשר |

Plus the generated privacy and accessibility pages, and 3 posts in 3 categories.

## The 👁 rows of the SEO checklist

- **1 מספר מקשר** — the brief leaves "מספר מקשר זאפ" empty and 03-6828265 is the business's own number on
  its own site, so `phone_is_virtual` is off and no popup is shown. Confirm with the sites team.
- **8 FAQ relevant to the company** — every answer is taken from the brief's own category texts and the
  product lists; no fact was invented.
- **9 the client's images** — 117 files, all the client's own (see `IMAGE-SOURCES.md`), 0 AI.
- **+1 phone, e-mail, address** — match the brief exactly.
- **+6 1280 and mobile** — looked at both; the hero, the category pages and the footer were checked by eye.

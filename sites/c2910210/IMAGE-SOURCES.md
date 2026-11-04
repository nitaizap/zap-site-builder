# IMAGE-SOURCES — מוניות כפר סבא בע״מ (2910210)

Every image that ships on this site has a row here. An image without a row must not be uploaded
(standing instruction, שרון יוסף 20/10/2026, after review by עו"ד קובי בארי).

All photographs below came from the client's own material folder delivered with the intake:
`F:\SiteContent\02910210` (227 files, copied by `zs intake` into `sites/c2910210/assets/client/`).
They were opened and checked one by one: every one shows this business (its taxis with the company's
roof signs, its station sign "מוניות כפר סבא", its own dispatch room, its own business card).

**Weave / AI credits spent on this client: 0.** No AI image was generated; the client's own photographs
covered every slot that is used. No stock or downloaded photo is used anywhere on the site.

| file | uploaded | by | source | licence | credits |
|---|---|---|---|---|---|
| `assets/logo-brief.png` | 2026-11-04 | Claude (polish pass c2910210) | **the logo embedded in the brief itself**: `word/media/image1.png` inside `brief/איפיון אתר - מוניות כפר סבא - 2910210_1.docx`, the image in the spec sheet's `לוגו` cell (200x200 PNG). Cropped to y 33..129 to drop the slogan strip, then resampled 2x (LANCZOS). No redraw. | client's own material, supplied with the brief | 0 |
| ~~`assets/logo.png`~~ (replaced 2026-11-04, kept in `assets/`, not uploaded) | 2026-11-03 | Claude (session c2910210) | crop of the client's own business card, `assets/client/חומרים-ישנים_מוצרי-אינטרנט_1.jpg` (client material folder F:\SiteContent\02910210) | client's own material | 0 |
| `assets/favicon.png` | 2026-11-03 | Claude (session c2910210) | crop of the same business card (the TAXI tile) | client's own material | 0 |
| `assets/taxi-side.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_חומר-גרפי-גולמי_IMGP0829.JPG` (client material folder) | client's own photo | 0 |
| `assets/taxi-street.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_חומר-גרפי-גולמי_IMGP0828.JPG` (client material folder) | client's own photo | 0 |
| `assets/taxi-night.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_מוצרי-אינטרנט_20121225_170638.jpg` (client material folder) | client's own photo | 0 |
| `assets/station-front.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_מוצרי-אינטרנט_20121225_170623.jpg` (client material folder) | client's own photo | 0 |
| `assets/station-sign.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_חומר-גרפי-גולמי_שלט.JPG` (client material folder) | client's own photo | 0 |
| `assets/dispatch-desk.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_חומר-גרפי-גולמי_7.JPG` (client material folder) | client's own photo | 0 |
| `assets/dispatch-phone.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_חומר-גרפי-גולמי_6.JPG` (client material folder) | client's own photo | 0 |
| `assets/dispatch-room.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_חומר-גרפי-גולמי_4.JPG` (client material folder) | client's own photo | 0 |
| `assets/dispatch-night.jpg` | 2026-11-03 | Claude (session c2910210) | `חומרים-ישנים_מוצרי-אינטרנט_20121225_170534.jpg` (client material folder) | client's own photo | 0 |

Currently placed on pages: `logo-brief`, `favicon`, `taxi-side`, `taxi-street`, `taxi-night`,
`station-front`, `station-sign`, `dispatch-room`. `dispatch-desk`, `dispatch-phone`, `dispatch-night` and
the superseded `logo.png` are prepared but not placed; they stay in `assets/` only, so they are not uploaded.

## Not used, and why

- Stock-looking photos found on the old-site backup (`Media_Uploads_3_1.jpg` an aerial motorway
  interchange, `3_3.jpg` a coach interior, `3_2.jpg`) have **no identifiable origin**: they look like
  purchased or downloaded stock on a site built around 2006, and no licence record exists. Dropped.
- The old site's interface GIFs (buttons, arrows, panel chrome, `bull-*.gif`) are not photographs.
- Framed documents and the framed press cutting (`IMGP0811/0812/0813`, `כתבה.JPG`) are legible
  third-party material (a union certificate, a newspaper article) and are not republished.

## Note on the photographs

They are genuine but old: the dispatch-room shots are from about 2006 and the night shots from 2012.
They show real staff members. Two of them are on the site (`dispatch-desk` on the home page collage,
`dispatch-room` on the about page). Recorded in OPEN-ITEMS.md: the client should be asked for current
photographs of the fleet and the station, and should confirm that the people shown agree to appear.
No generated image of a taxi, a driver or the premises was produced, so nothing on the site presents an
AI picture as this company's vehicles, drivers or offices.


## The logo decision (2026-11-04, polish pass)

The brief's `.docx` is exported to text in `brief/brief.md`, and that export silently drops embedded
images. Opened as a zip, `word/media/` holds exactly one image, `image1.png`, 200x200 RGB, referenced from
the single `<w:drawing>` in `word/document.xml`, in the spec sheet's `לוגו` cell. It is the company's flat
logo: white "מוניות כפר סבא" with a small "בע״מ" on a `#3EB54D` green ground, and the slogan
"אל היעד הבא עם מוניות כפר סבא!" on a yellow strip across the bottom (rows 132..160).

Both candidates were rendered at the real header size (56px and 96px CSS, at 2x) and looked at:

| | brief artwork (200x200) | `logo.png` (994x818) |
|---|---|---|
| what it is | the client's logo as drawn | a crop of a **photograph** of their business card |
| edges at header size | flat, crisp, no artefacts | JPEG noise, a blue halo round the sign, an uneven yellow |
| what it says | the business name, "מוניות כפר סבא" + "בע״מ" | "TAXI" + "כפר סבא"; it never names the business |
| ground | one flat green block | the dark green of the photographed card, which is not a site colour |
| resolution | 200px, enough for a 56-96px header at 2x | far more than needed |

**Switched to the brief's artwork.** It is the better-sourced file (the client's own logo, delivered with
the brief, rather than a crop someone made from a photo of a card), it is the only one of the two that
spells the business name, and at the size it is actually rendered it is visibly cleaner, which is the point
of this pass. Its one real disadvantage, resolution, does not bite: at 96px CSS the 2x requirement is 192px
and the source is 200px.

The slogan strip was cropped off, per `qa-rules.md` line 22: "A logo with a small tagline gets a version
without it (crop, never redraw)". At header size that strip is an illegible yellow smear. The slogan is not
lost: it is already the site tagline. Nothing was redrawn, retouched or recoloured.

**The favicon stays the business-card TAXI tile.** At 16-32px the brief artwork is an unreadable green
rectangle, while the yellow TAXI sign is still recognisable. Different job, different crop.

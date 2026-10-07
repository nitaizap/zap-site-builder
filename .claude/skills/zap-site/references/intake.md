# 1 · Intake

## What arrives

Usually one of: a pasted Hebrew brief, a spec board (image/PDF) with the page list and palette, a logo, a
few photos, the client's old site URL, a Google Business link. Sometimes only a name and a phone number.

## Extract — open every file

Open every image and PDF before describing it. Filenames lie; a mislabelled image once shipped into a header.
Build `sites/<slug>/NOTES.md`:

```markdown
# <business> — notes

## Facts (locked; each with its source)
| field | value | source |
|---|---|---|
| name | ... | brief |
| display phone | 073-... | brief (Zap call-tracking number) |
| WhatsApp | 05X-... | brief |
| lead email | ... | brief |
| address | ... | GMB / brief — must match GMB byte for byte |
| years / founded | ... | client site "about" — only if stated |
| services | ... | brief |
| areas served | ... | brief / site |

## Audience — who, and what they are afraid of
## Assets — file | what it actually shows | usable as | ALT
## Gaps / asked the user
## Assumptions (made, to be confirmed)
## Keyword map  (step 2)
```

## Research first, ask last — get the missing items yourself

You have a real browser and full internet in this environment. Before asking the user for anything,
spend the effort to find it. Ask only for what cannot exist online or needs a human decision.

1. `bin/zs grab <slug> <old-site-url>` crawls the client's current site in a headless browser and, when
   it is down or blocked (403/404/timeout), the newest **Wayback Machine** snapshot instead. It writes
   `research/<host>.md` (page texts, headings, phones, emails, address and hours lines, social links,
   the **Dapei Zahav customer-id from the old reviews widget**, Google Business links) and saves logo
   candidates and every large photo in `research/img/` with a manifest.
   Proven on the first pilot: the live site answered 403; the Wayback snapshot gave the customer-id,
   a second phone, the business's YouTube video, the Facebook page and the logo.
2. Search the web (WebSearch / WebFetch, or Playwright on a search page) for `<name> <city>`,
   `<name> דפי זהב`, `<name> פייסבוק`, `<phone>`. Collect the Google Business share link, the Facebook
   page (its profile/cover images are often the best logo source), YouTube, Instagram, press mentions.
3. Dapei Zahav: open `https://www.d.co.il/SearchResults?query=<name>` with Playwright (it is JS-rendered),
   or confirm an id found on the old site by opening `https://www.d.co.il/<id>/` and checking legal name +
   street + phone. Only a 3-field match goes into `business.dpz_customer_id`.
4. Logo: the highest-resolution version you can find (old site header or og:image, Facebook profile,
   Wayback). Clean it (trim, transparent background) with Pillow; never redraw or invent a logo.
5. Real photos and video of the business beat AI every time: use what the client already published
   (their site, Facebook, YouTube), describe what each shows in `alt`, record the source URL.

Only then ask, in one message, for what is left: the Zap privacy PDF, contradictions, decisions
(direction, Weave budget) and anything private. Every fact you found goes into NOTES.md with its source
URL, marked "found", so the user sees what you verified.

## Research the business (read-only)

The default is: **find it, cite it, then ask only what research could not settle.** Run this as a
background agent while you plan, and record every result with its URL in NOTES.md.

| item | where | how (verified 2026-10-07) |
|---|---|---|
| Dapei Zahav customer-id | `https://www.d.co.il/<id>/` — the brief's "לקוח NNNNNNNN" is usually it | curl gets a WAF "Request Rejected"; read it with **WebFetch**. A match must agree on name + street + phone. The listing also gives hours, service tags, WhatsApp, website, Facebook, Google Maps link |
| Google Business / Maps | the d.co.il page links `maps.google.com/?cid=…` and carries `geo:lat,lng` | use the CID URL as `gmb_url`, the coordinates as `geo`. Never scrape Maps |
| WhatsApp | d.co.il WhatsApp button, Facebook page | prefer a number the client published over a guess from the brief |
| old site content + photos | live site; if down, Wayback: `http://archive.org/wayback/available?url=<domain>` | `bin/zs grab` does this automatically via the Wayback CDX index (finds www/http variants the 'available' API misses) |
| legal name / ח.פ. | search "<name> בע\"מ ח.פ." | show nothing legal unless found with a source |
| privacy PDF | Zap provides per client | if not in the brief: placeholder page (automatic) + launch checklist |
| final domain | brief → old site domain | assume the old domain, say so |
| Facebook / Instagram | links from the listing | facts and visual tone only, no photo copying |

Facts from the client's own public listings (d.co.il, their site, their GMB) count as sourced. A
contradiction between the brief and a listing is shown to the user, not resolved silently.

## The one message of questions

Only what research could not answer, numbered, in the user's language, each with what you already
found ("d.co.il shows WhatsApp 055-…, use it?"). Typical leftovers:

1. מספר תצוגה (מספר מעקב של זאפ) מול וואטסאפ מול מייל ללידים — לאשר את שלושתם
2. קובץ מדיניות פרטיות (PDF) מזאפ — עד שמגיע יש עמוד זמני
3. תמונות אמיתיות (עבודות, צוות, מקום) — אם אין, נשתמש בתמונות AI
4. כל סתירה שמצאת בין האפיון למקורות (שנות ותק, שירותים, אזורים, טלפונים)

Blocking: display phone and lead email (the validator requires them). Everything else: continue, note the
gap, and the launch checklist will carry it.

## Hard rules

- A fact the brief contradicts is resolved by the user, not by you. Record the decision as locked.
- The audience is often dual (homeowners and contractors; patients and referring doctors). Say so; every
  page then needs a line for each.
- `phone_e164` must dial `phone_display`: 073-7001234 → +972737001234. The validator checks it.

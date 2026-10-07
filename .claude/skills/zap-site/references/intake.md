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

## Research the business yourself — before asking anything (read-only)

The default is: **find it, cite it, then ask only what research could not settle.** Run this as a
background agent while you plan, and record every result with its URL in NOTES.md.

| item | where | how (verified 2026-10-07) |
|---|---|---|
| Dapei Zahav customer-id | `https://www.d.co.il/<id>/` — the brief's "לקוח NNNNNNNN" is usually it | curl gets a WAF "Request Rejected"; read it with **WebFetch**. A match must agree on name + street + phone. The listing also gives hours, service tags, WhatsApp, website, Facebook, Google Maps link |
| Google Business / Maps | the d.co.il page links `maps.google.com/?cid=…` and carries `geo:lat,lng` | use the CID URL as `gmb_url`, the coordinates as `geo`. Never scrape Maps |
| WhatsApp | d.co.il WhatsApp button, Facebook page | prefer a number the client published over a guess from the brief |
| old site content + photos | live site; if down, Wayback: `http://archive.org/wayback/available?url=<domain>` | archive.org pages may be blocked from the sandbox; if so, note the snapshot URL as a gap |
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

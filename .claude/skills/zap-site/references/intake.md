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

## Research the business (read-only)

- The client's existing site: services, wording, real photos you may reuse (product shots, the team, the
  premises, certificates). Prefer the brief where they disagree; the brief wins ("תיצמד לאפיון").
- Google: the business name + city. Use what the search results show; never solve CAPTCHAs or scrape Maps.
- Dapei Zahav: `https://www.d.co.il/SearchResults?query=<name>` is JS-rendered; if you cannot read it,
  ask for the customer-id. A match must agree on legal name, street address and phone, or it is not a match.
- Facebook / Instagram: only for facts and the visual tone, not for copying photos without permission.

## The one message of questions

Ask everything at once, numbered, in the user's language. Typical list:

1. מספר תצוגה (מספר מעקב של זאפ) מול וואטסאפ מול מייל ללידים — לאשר את שלושתם
2. קובץ מדיניות פרטיות (PDF) מזאפ — עד שמגיע יש עמוד זמני
3. customer-id בדפי זהב — בלעדיו אין בלוק ביקורות
4. קישור לכרטיס Google Business
5. תמונות אמיתיות (עבודות, צוות, מקום) — אם אין, נשתמש בתמונות אווירה
6. כל סתירה שמצאת באפיון (שנות ותק, שירותים, אזורים)
7. הדומיין הסופי (לחבילה)

Blocking: display phone and lead email (the validator requires them). Everything else: continue, note the
gap, and the launch checklist will carry it.

## Hard rules

- A fact the brief contradicts is resolved by the user, not by you. Record the decision as locked.
- The audience is often dual (homeowners and contractors; patients and referring doctors). Say so; every
  page then needs a line for each.
- `phone_e164` must dial `phone_display`: 073-7001234 → +972737001234. The validator checks it.

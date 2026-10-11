# 2a · Keywords and the page tree

## Research

- **Ahrefs connected?** Use it (country `il`): volume + KD for every candidate page term and its variants
  (with/without city, singular/plural, construct state).
- **No Ahrefs:** search Google for each candidate term (+ city). Read the top results: which page types
  rank (home pages, service pages, articles), what their H1s and titles look like, how long they are.
  Write "volume: unknown" rather than guessing numbers.
- Check the client's existing site for pages that already rank or have links; keep their topics.

## Assign

> One keyword owns one page. One page owns one keyword.

| page | keyword | intent | volume | KD | H1 | slug (key) |
|---|---|---|---|---|---|---|

- Home → the head term + city if local ("אינסטלטור בחיפה").
- Each service → its own term ("איתור נזילות בחיפה").
- Hub/category pages → the category term, never a child's term.
- About → a secondary term, often the profession + "מוסמך"/"מומלץ" variant, plus the brand name.
- Contact → "צור קשר — <brand>" (navigational; not a competing term).
- Blog posts → **informational** terms the service pages do not own ("מה עושים כשיש נזילה מהתקרה").
- Check the whole slug space: a post slug, a category slug and a page key must never collide.

## Page tree → `pages[].key`

```
""                                  home
<hub>                               e.g. שירותי-אינסטלציה      (type hub)
<hub>/<service>                     e.g. שירותי-אינסטלציה/איתור-נזילות   (type service)
אודות · צור-קשר                      (types about, contact)
בלוג                                 (type blog — posts live at /בלוג/<slug>/, categories at /נושא/<slug>/)
```

- Keys are Hebrew, hyphenated, no Latin mixed in (a client complaint, and the validator blocks it).
- Services sit under their hub; static pages stay at one level on purpose.
- Typical small business: home, 1 hub, 3–8 services, about, contact, blog with 2–3 launch posts.
  A larger tree is fine when the keyword research supports it; thin pages are not.
- Privacy: if Zap's PDF URL is unknown, the build creates a noindexed placeholder page automatically.

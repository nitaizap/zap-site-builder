# 2b · Copy and on-page SEO

Proven on the Zap pilot sites (Gross, Azrad, Gilboa, Ilan). Copy in `site.json` is the final copy: what
the user sees at the gate is what ships.

## H1

- H1 = the page's keyword from the map, in natural Hebrew. Exactly one per page (the hero title).
- Home and About: keyword + brand name: `אינסטלטור בחיפה — מים טובים אינסטלציה`.
- A slogan goes under the H1 (hero `lead`) or in a section title, never in the H1.

## Five checks before the gate

1. H1 = keyword (+ brand on home/about).
2. Brand name appears in: H1 or hero, the first paragraph, the `<title>`, the footer (automatic).
3. Each H2 uses a variant (ה/ב/ל prefixes, plural, construct state) or a secondary keyword, never the exact
   H1 phrase again.
4. Every link to a service uses that service's keyword as its anchor (cards do this by title).
5. Nothing invented: no success rate, count, sum, award, rating or year the client did not give.

## Meta

| field | rule | example |
|---|---|---|
| `seo.title` | keyword first · proof · brand last · 30–60 chars | `איתור נזילות בחיפה ללא הרס \| מים טובים אינסטלציה` |
| `seo.description` | 140–160 chars · keyword · differentiator · a call with the phone | `איתור נזילות בחיפה והקריות עם מצלמה תרמית… 073-7001234` |
| `seo.keyword` | the owned keyword (unique across the site) | `איתור נזילות בחיפה` |

"keyword — N שנות ניסיון | brand" works when N is a locked fact.

## Per page type

**Home** (owns the head term): hero (H1, lead answering the audience's fear, CTA + phone, 3 proof points)
→ trust strip (facts only) → services cards (keyword anchors) → process steps → why us (split) → FAQ
(3–6) → blog teasers. 900–1,600 words of real coverage. Add `reviews` only with a real customer-id.

**Service** (owns one term): hero (H1 = keyword, one-line answer) → `prose` whose first paragraph answers
the query in 2–3 sentences, then H2s: what it is / signs or conditions / how it is done step by step /
time and cost as the client states them / when to call → FAQ (3–6) → CTA. 450–800 words for trades,
900–1,400 for legal/medical. One link to a sibling service and one to the relevant post, with keyword anchors.

**Hub**: H1 = category; 1–2 sentence intro; a card per child (title = child keyword); CTA. Must not compete
with a child.

**About** (E-E-A-T): H1 = `אודות <brand> — <secondary keyword>`; who, since when, credentials as facts
with dates, the owner's real photo when available, service areas.

**Contact**: H1 `צור קשר — <brand>`; `contact` section (NAP + form + map). Hours: ask; never assume.
The footer lead form is hidden on this page automatically.

**Blog post**: H1 = informational term; first paragraph answers it; 500–800 words; H2/H3; at least one link
to the service that solves it (and `related_page` set, which adds a CTA box); author = the owner.

## Writing rules

- Short paragraphs (2–3 sentences), answer first, lists where there is a list, a table where there is a
  comparison (`prose` supports `<table>`).
- Natural Hebrew. Read it aloud: if it sounds translated, rewrite it. No AI tells (no "בעולם של היום",
  no "לא רק X אלא גם Y" habit, no em-dash in every sentence, no triplets of adjectives).
- No instructions for obvious controls ("לחצו להגדלה"), no "תמונה להמחשה" labels: the validator blocks them.
- No unverifiable superlatives ("הטוב ביותר", "מספר 1", "המוביל"). The validator warns.
- CTA labels fit on one line.

## YMYL (legal, medical, financial)

No promise of outcome, no success percentages unless the client gives and approves them, every service page
and post signed by the professional with a date, `content.disclaimer` set (shown under posts), no stock
photos of people who are not the client. Name the statute when stating a legal fact. The client approves
every claim before launch.

# Zap standards — what every client site carries

Verified against live Zap client sites. ✅ = the engine does it, nothing to do. ✋ = needs a person or a fact.

## Automatic ✅

- Accessibility statement link → `https://zap.dbusiness.co/js/accessibility.html` ("הצהרת נגישות אתר"),
  never a local statement page. Ally (pojo-accessibility) installed; skip link to `main#content`; one `<main>`.
- Zap Group logo (183×26) in the footer bar, linking to https://zapgroup.co.il/ in a new tab.
- Copyright line `© <year> <client> — כל הזכויות שמורות` (+ AI-images note when set).
- One uniform lead form in the footer of every page except Contact (which has its own full form).
- Every form: required consent checkbox linking the privacy policy; honeypot + signed time trap + content
  signals; a missing token never blocks a real visitor; blocked attempts logged (last 50).
- Every lead is **saved in WordPress** ("פניות מהאתר") and emailed to `business.email_leads` from
  `zapsites@d.co.il` via `relay.d.co.il:25` (no auth, no TLS). On staging no mail is sent to the client.
- `tel:` links dial the displayed number (validated before build, measured after).
- WhatsApp links `wa.me/972…` with a prefilled message.
- LocalBusiness schema with the locked NAP, FAQPage (matches the visible FAQ), Service on service pages,
  breadcrumbs (Yoast). **Never** `aggregateRating`.
- No ratings, stars, review counts or "5.0 בגוגל" anywhere (blocked by the validator and QA).
- Reviews block only with a real Dapei Zahav `customer-id` (`<zap-reviews customer-id site-id="5">`).
- Privacy: placeholder page until Zap's PDF arrives; never a `#` link.
- Hebrew URLs only, no `/category/`; one keyword per page; unique titles/descriptions.
- Hardening: no xmlrpc, no user enumeration, version hidden, security headers, no PHP in uploads (Apache).
- Staging is `noindex`; the package switches indexing on only for the client's own domain.

## Needs a person ✋ (goes on LAUNCH-CHECKLIST.md automatically)

- Zap's per-client privacy PDF (`standards.privacy_url`).
- Dapei Zahav `customer-id` — verify the listing on legal name + street + phone before using it; flag
  duplicates. A wrong id publishes another company's reviews.
- Google Business link (schema `sameAs` / `hasMap`), and NAP identical to it byte for byte.
- Real photography; legal facts (company number, licence, years); domain, DNS, SSL, Search Console.
- One real test lead on launch day, into the client's inbox.

## Never

- Copy `zapgroup.co.il/terms` onto a client site (it names Zap as the operator of the client's site).
- Invent reviews, ratings, awards, case counts, or a founding year.
- Mail the real client during the build.

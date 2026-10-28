# פטוצ'ינה: brief check

Brief: איפיון אתר WIX בייסיק, customer 80356988. ✅ = seen on the rendered local build (page HTML or screenshot, 28/10/2026).
➖ = deliberately different, with the reason. ⏳ = open.

## Site tree
| brief | status |
|---|---|
| 1. עמוד הבית | ✅ `/` |
| 2. נעים להכיר | ✅ `/נעים-להכיר/` |
| 3. תפריטים (מגשי אירוח, קינוחים, בוקר ובראנץ', אירועים) | ✅ `/תפריטים/`, one section per menu with an anchor; the top menu has a sub-item for each |
| 4. גלריה | ✅ `/גלריה/` (15 client photos, lightbox) |
| 5. צור קשר | ✅ `/צור-קשר/` |
| (not in brief) בלוג | ➖ added: Zap QA wants a blog with 3 posts; 3 posts written only from the client's own menus and the brief |

## Business details
| brief | status |
|---|---|
| name פטוצ'ינה, owner עינת שליין, 8 years | ✅ home + about |
| phone | ✅ 053-6242885 (Zap number from d.co.il, user decision) with "מספר מקשר" popup naming 054-3830028 |
| WhatsApp 054-3830028 | ✅ wa.me link, header/footer/contact |
| hours 7:30-21:00 | ✅ brief hours (user decision); d.co.il differs (Su-Th 7:30-19:30, Fri 9-13) |
| address קרן היסוד 1, פרדס חנה-כרכור | ✅ footer + contact (Waze link) |
| email feettuccine.inat@gmail.com | ✅ topbar + contact; lead e-mail |
| social: none in brief | ✅ Instagram patoccina_12 (linked from the client's own site) |

## Design
| brief | status |
|---|---|
| reference teffee.co.il, "בגרסה בהירה" | ✅ light tone throughout (no dark grounds except the "why us" band); direction B chosen by the user |
| logo | ✅ client logo, tagline cropped for header legibility; favicon from the face |
| colours (none specified) | ✅ sampled from the logo: plum #561b31, coral accent darkened to #b04a31 |

## Home page
| brief | status |
|---|---|
| SEO title / description | ✅ title per Zap rule `פטוצ'ינה \| קייטרינג חלבי כשר`; description from the brief, lengthened to 150-160 |
| H1 "קייטרינג חלבי כשר בטעמים איטלקיים מהלב" | ➖ Zap QA rule: home H1 = client name. The brief's H1 opens the hero lead |
| lead + buttons לתפריטים / דברו איתנו | ✅ (lead shortened so the buttons fit the fold on a 360×640 phone) |
| rotating images (folder: דף הבית - מתחלפות ×3) | ✅ hero slider with the 3 images; site tier set to `standard` because `basic` allows one still photo |
| "בפטוצ'ינה הכל אפשרי" + paragraph | ✅ |
| "נעים להכיר" block + "להכיר אותנו" | ✅ with the two about-page photos |
| gallery: 6 client images | ✅ 4 in a staggered row (template 2 pattern) + full gallery page |
| "למה לבחור בפטוצ'ינה" + 4 advantages | ✅ word for word |
| contact block + form (name, phone, event type, date, message) | ✅ form title/text from the brief. ➖ fields: Zap's single form has name, phone, email, message; the text asks for event type and date (user approved) |

## About
| brief | status |
|---|---|
| H1 נעים להכיר, 3 paragraphs | ✅ word for word (dashes rewritten as commas/colons, house rule) |
| folder: top image Einat with the spread, side image (dough) | ✅ Einat photo; ➖ dough photo replaced by a bakery photo from the old site (user, 28/10) |

## Menus
| brief | status |
|---|---|
| H1 "התפריטים שלנו" + opening paragraph | ➖ H1 = page name "תפריטים" (Zap QA); paragraph in the hero lead |
| 4 H2s with their lines | ✅ |
| "בפטוצ'ינה הכל אפשרי, ניתן להתאים תפריט" | ✅ hero + closing block |
| "קישור לתפריט" | ✅ no file supplied; the menus were taken from the client's own site (feettuccine.co.il/תפריט): "בוקר טוב" brunch, "צהרים טובים VIP" and Premium, desserts. Prices: none published, none shown |
| folder: מגשי אירוח photos, "תכנון אירוע - להחליף אליה" | ✅ trays photos in trays/menus/gallery; event photo on the events section |
| dessert photos | ⏳ none in the folder (user: use what we have) |

## Gallery / contact
| brief | status |
|---|---|
| gallery H1 + text | ✅ |
| contact H1 "דברו איתנו", text, details | ➖ H1 = "צור קשר" (slug = H1 = menu label rule); "דברו איתנו" opens the lead. Details ✅ |

## Standards
| item | status |
|---|---|
| no em/en dashes in site copy | ✅ validator + grep of rendered pages: 0 |
| privacy policy | ✅ Zap standard (user: "go with standard"). ⏳ the client still has to confirm the fields (launch blocker) |
| Dapei Zahav reviews | ⏳ widget renders only on the pushed site (customer-id 80356988) |
| `zs qa` | ✅ 0 errors · `zs seo` 0 FAIL |

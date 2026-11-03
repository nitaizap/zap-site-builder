# BRIEF-CHECK — מסגרית Dream from Steel (80386843)

Every line of `brief/איפיון אתר - מסגרית Dream from Steel - 80386843.docx`, in its order.
✅ = seen on the rendered page (a screenshot or the page HTML, checked at `127.0.0.1:8425`), never "it is in
site.json". ➖ = not applicable, with the reason. ⏳ = open, see `OPEN-ITEMS.md`.

## 1 · סוג הפרויקט

| line in the brief | status | where / why |
|---|---|---|
| אתר מלא (כולל דומיין) | ✅ | 7 pages + privacy + accessibility + blog archive, all built. Domain is the sites team's step, not ours |
| אתר SEO (בלוג) — blank | ✅ | built anyway: the Zap SEO checklist fails a site without a blog category and 3 posts. `/בלוג/` + `/בלוג/עבודות-מתכת/` + 3 posts |
| package not named | ✅ | decided 02/11: the spec's own six pages stay, `tier: standard` (the basic cap of 5 would force one off). OPEN-ITEMS 2 |

## 2 · פרטי לקוח

| line | status | where |
|---|---|---|
| שם הלקוח: אופיר אלחנתי | ✅ | `/אודות/` ("בניהולו של אופיר אלחנתי"), and the post byline |
| שם העסק: מסגרית Dream from Steel | ✅ | home H1, header, footer, every `<title>` |
| מספר לקוח 80386843 | ✅ | `business.dpz_customer_id`, used for the Dapei Zahav link |
| שנות פעילות: 20 | ✅ | home hero points, `prose:band`, `facts` card ("ותק בתחום: 20 שנה"), `/אודות/` |
| אתר קיים: d.co.il/80386843/33060/ | ➖ | a Dapei Zahav listing, not a site to migrate. No content or ranking to carry over |

## 3 · פרטי קשר

| line | status | where |
|---|---|---|
| איש קשר: אופיר אלחנתי | ✅ | `/אודות/` |
| כתובת: הרימון 89, נווה ימין | ✅ | `/צור-קשר/` NAP, footer, `facts` card, LocalBusiness schema. Waze link on the address |
| אזורי שירות: כפר סבא | ✅ | home hero lead, FAQ, `/אודות/`, schema `areaServed` |
| שעות: א׳–ה׳ 07:00–20:00 | ✅ | `/צור-קשר/`, footer, `facts` card, `openingHours` schema |
| אימייל לאתר: ofir.elc@gmail.com | ✅ | `/צור-קשר/` contact list and the footer |
| מייל לטופס לידים: ofir.elc@gmail.com | ✅ | `business.email_leads`; a test lead on the local build was saved and correctly not mailed (staging) |
| טלפון לאתר: 050-9254010 | ✅ | decided 02/11: the site displays the Zap tracking number, and the 050 is the business's own line named in the "מספר מקשר" popup, plus the WhatsApp number. OPEN-ITEMS 1 |
| מספר מקשר זאפ: 072-2594285 | ✅ | the displayed phone on every page, with `phone_is_virtual` and Zap's explanation link |

## 4 · נוכחות דיגיטלית

| line | status | where |
|---|---|---|
| וואטסאפ: כן, 050-9254010 | ✅ | floating button on desktop, action bar on phones, contact list. `wa.me/972509254010` with a prefilled message |
| פייסבוק / אינסטגרם / לינקדאין / GMB — all blank | ➖ | no social bar anywhere (`pool.md`: show only what the client really has). No GMB link in the schema |

## 5 · תוכן האתר

| line | status | where |
|---|---|---|
| ותק של 20 שנה בעבודות מסגרות וייצור מוצרי מתכת | ✅ | home hero, `prose:band`, `/אודות/` |
| פתרונות מקצועיים ואיכותיים | ✅ | carried as concrete copy, not as the phrase (the validator and `design.md` reject "פתרונות מקצועיים" as filler) |
| כל סוג של פרויקט מסגרות וייצור מוצרים מתכתיים | ✅ | `/מסגרות-בהתאמה-אישית/` ("פרויקטים מורכבים לביצוע"), home `prose:band` |
| ביצוע מדויק ובמועד | ✅ | `steps:stack` step 4, FAQ ("העבודה נמסרת בזמן שסוכם"), `/אודות/` features |
| עיבוד מתכות מתקדם | ✅ | home `collage` points, `/ייצור-מוצרי-מתכת-ייחודיים/` H2 |
| ייצור מוצרים מותאמים אישית | ✅ | the whole site; home `prose:band`, all three service pages |
| דגש על איכות החומרים והביצוע המקצועי | ✅ | home `collage` ("החומר קובע את התוצאה"), `/אודות/` `split:frame` ("דגש על איכות החומרים") |
| כל פרויקט מטופל באופן אישי, מתכנון ועד למוצר המוגמר | ✅ | `steps:stack` (4 steps), home hero point "תכנון, ייצור ומסירה במקום אחד" |
| צרו קשר לקבלת הצעת מחיר ויעוץ מקצועי | ✅ | hero CTA, `leadbar`, `cta` band, footer form, FAQ "איך מקבלים הצעת מחיר" |
| **דגש: דברים מיוחדים ולא סטנדרטיים, הכל בהתאמה ובייצור אישי** | ✅ | the site's whole argument. `prose:band` opens "אין אצלנו קטלוג"; `/מסגרות-בהתאמה-אישית/` H1 and first paragraph; FAQ "אין אצלנו קטלוג קבוע של מוצרי מדף" |
| ייצור מוצרי מתכת ייחודיים בהתאם לדרישת הלקוח | ✅ | its own page `/ייצור-מוצרי-מתכת-ייחודיים/`, and a home card |
| לקוחות: פרטיים, אדריכלים, נגרים, שוק הרחפנים, שוק התעופה | ✅ | home `facts` section "למי אנחנו מייצרים" (all five named), `/אודות/`, both services pages |
| עמודי שירות: דף בית, אודות, מסגרות בהתאמה אישית, ייצור מוצרי מתכת ייחודיים, תכנון מוצרי מתכת, צור קשר | ✅ | all six built, in the menu in that order, slug = H1 = menu label on the three service pages |
| מסגרות בהתאמה אישית: עבודות מיוחדות ולא סטנדרטיות, פרויקטים מורכבים לביצוע | ✅ | `/מסגרות-בהתאמה-אישית/`, 560 words, H2 "פרויקטים מורכבים לביצוע" |
| ייצור מוצרי מתכת ייחודיים בהתאם לדרישת הלקוח | ✅ | `/ייצור-מוצרי-מתכת-ייחודיים/`, 520 words |
| תכנון מוצרי מתכת מותאמים אישית | ✅ | `/תכנון-מוצרי-מתכת/`, 500 words |
| כפתורי חיוג לאופיר 050-9254010 | ✅ | call buttons everywhere; decided 02/11 that they dial the Zap tracking number, with the 050 named as the business's line and used for WhatsApp. OPEN-ITEMS 1 |
| טופס לידים | ✅ | footer form on every page except contact, `leadbar` mid-home, full form on `/צור-קשר/`. Consent checkbox linking the privacy policy; a real submission was saved |
| מאמרים — blank | ✅ | 3 posts written from the brief's own material. See OPEN-ITEMS 9 |

## 6 · עיצוב ומותג

| line | status | where |
|---|---|---|
| לוגו — blank | ✅ | blank on the spec, but the client's real logo was found on their Dapei Zahav listing and is in the header and the footer, with the favicon cut from it and the whole palette sampled from it. Only the source file at full resolution is still wanted. OPEN-ITEMS 4 |
| צבעי מותג — blank | ✅ | sampled from the client's own logo once it was found: orange `#b84606` and slate `#1b2a36`. NOTES.md |
| יד חופשית למעצב — blank | ✅ | treated as a free hand, since nothing was specified. Re-exercised on 03/11: kit `sidebar`→`frame`, archetype `statement`→`story`, home resequenced, for uniqueness headroom. Every word, link and image is unchanged; only the order and the skeleton moved. NOTES.md "Uniqueness pass, 03/11" |
| אתרים שאהבתם — blank | ➖ | nothing to match |

## 7 · תמונות

| line | status | where |
|---|---|---|
| תמונת בעלים — blank | ⏳ | no owner photo. No AI portrait was made (`images.md` forbids generated people). OPEN-ITEMS 7 |
| גלריה — blank | ⏳ | **no gallery section on the site, deliberately.** Nothing invented. Eight AI atmosphere images (material and process only) fill the image slots instead. OPEN-ITEMS 7 |

## 8 · כתבת תדמית

| line | status | where |
|---|---|---|
| כתבת תדמית — blank | ➖ | none supplied, none written |

## Added during the build

| request | status | where |
|---|---|---|
| leave room on the home page for a video frame (AI social promo the client bought), Noam 02/11 15:09 | ⏳ | slot reserved and documented with the exact position and JSON. Nothing rendered until the file or URL arrives. OPEN-ITEMS 6 |
| "אין אתר ואין תמונות צריך לייצר או לקחת ממאגרים", Noam 02/11 14:57 | ✅ | eight AI atmosphere images on the site, each marked `ai` and recorded in IMAGE-SOURCES.md, with the footer line saying so. No generated work presented as the client's: OPEN-ITEMS 7 |
| "יש רק לוגו", Noam 02/11 14:57 | ✅ | the file never reached the branch, so it was found on the client's own Dapei Zahav listing and is now in use. 140x140 is all the directory serves; the original is still wanted. OPEN-ITEMS 4 |

## Prohibitions, checked by grep over `site.json`

No gallery wording, no "שער", "מעקה", "פרויקטים שביצענו" or "תיק עבודות" (there is no portfolio to claim);
no rating, review count or stars; no price or ₪; no "להמחשה" label; no em dash.

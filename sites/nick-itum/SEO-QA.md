# SEO QA — ניק איטום

Checklist: Zap SEO sheet · site http://127.0.0.1:8403 · 39 rows: 34 pass, 0 fail, 5 manual

| # | קטגוריה | בדיקה | סטטוס | הערות |
|---|---|---|---|---|
| 1 | עיצוב וטיפוגרפיה | מספר מקשר פותח פופ אפ | 👁 MANUAL | the engine has no tracking-number popup; check the example site14.clicksite.co.il and the Zap number in the brief |
| 3 | עיצוב וטיפוגרפיה | שירותי החברה בדף הבית מפנים לעמוד השירות הנכון | ✅ PASS | 6 cards checked |
| 4 | עיצוב וטיפוגרפיה | יש עמודי הצהרת נגישות ומדיניות פרטיות | ✅ PASS | privacy ok; accessibility link /הצהרת-נגישות/ |
| 5 | עיצוב וטיפוגרפיה | קטגוריית בלוג עם 3 פוסטים רלוונטיים (בסטלינקס) | ✅ PASS | blog page yes, 3 posts |
| 6 | תמונות וביצועים | כל התמונות מתחת ל-100KB ובפורמט WebP | ✅ PASS | 30 images |
| 7 | תמונות וביצועים | ALT לכל התמונות | ✅ PASS |  |
| 8 | תמונות וביצועים | השאלות הנפוצות רלוונטיות לחברה | 👁 MANUAL | read every FAQ against NOTES.md facts (validate.py already blocks thin FAQs and invented ratings) |
| 9 | תמונות וביצועים | הוכנסו תמונות הלקוח מטופס האפיון | 👁 MANUAL | 21 images, 6 marked AI; compare with the client's folder from the spec |
| 11 | כפתורים ויצירת קשר | לינק וואטסאפ למספר הנכון + טאב חדש | ✅ PASS | 48 links |
| 12 | כפתורים ויצירת קשר | כפתור וואטסאפ צף בכל האתר (טאב חדש) | ✅ PASS | desktop 1440 + mobile 390, every page |
| 13 | כפתורים ויצירת קשר | כפתור טלפון תואם למספר באתר | ✅ PASS | tel = 054-6242489 |
| 14 | כפתורים ויצירת קשר | כפתורי טלפון עם tel: לחיוג ישיר | ✅ PASS |  |
| 15 | SEO טכני - URLs | סלאגים בעברית ולפי ה-H1 | ✅ PASS |  |
| 16 | SEO טכני - URLs | הסרת /category/ מכתובות קטגוריות | ✅ PASS | category base removed |
| 17 | SEO טכני - URLs | פרמלינק פוסטים /blog/%postname%/ | ✅ PASS | posts live under /בלוג/ |
| 18 | SEO טכני - URLs | וי מדיניות פרטיות בטפסים + slug תקין | ✅ PASS | 18 forms |
| 19 | שגיאות 301 ו-404 | בדיקת כל שגיאות ה-404 באתר | ✅ PASS | 28 internal links, all < 400 |
| 20 | שגיאות 301 ו-404 | תיקון כל ה-404 (עמוד / 301) | ✅ PASS | redesign: map the old site's URLs to new ones (301) before launch |
| 21 | שגיאות 301 ו-404 | קישורים פנימיים לא מפנים לכתובות ישנות | ✅ PASS |  |
| 22 | SEO On-Page | סכמת FAQ בעמודי שירות ופוסטים | ✅ PASS |  |
| 23 | SEO On-Page | Meta Title ייחודי ואופטימלי בכל עמוד | ✅ PASS | 18 unique titles |
| 24 | SEO On-Page | Meta Description ייחודי (150-160 תווים) | ✅ PASS |  |
| 25 | עמוד 404 | עיצוב מותאם לעמוד 404 | ✅ PASS | HTTP 404 |
| 26 | עמוד 404 | קישור לעמוד הבית | ✅ PASS |  |
| 27 | עמוד 404 | קישור לעמוד צור קשר | ✅ PASS |  |
| 28 | עמוד 404 | שורת חיפוש בעמוד 404 | ✅ PASS |  |
| 29 | עמוד 404 | קישורים פופולריים / קטגוריות | ✅ PASS |  |
| 30 | תבניות | טמפלט תוצאות חיפוש עם רשימת פוסטים | ✅ PASS | HTTP 200 |
| +1 | כללי | טלפון, מייל וכתובת תואמים לאפיון | 👁 MANUAL | site shows 054-6242489, nickitum1@gmail.com, זכרון יעקב 18, כניסה א׳, פתח תקווה; compare with the spec |
| +2 | כללי | לוגו זאפ בפוטר + קישור לאתר זאפ | ✅ PASS |  |
| +3 | כללי | H1 בדף הבית = שם הלקוח בלבד | ✅ PASS | ניק איטום |
| +7 | כללי | פורמט Title: "<לקוח> | <עמוד>" | ✅ PASS | all titles start with the client name |
| +4 | כללי | עמוד פנימי שונה מפוסט | ✅ PASS | pages render through Elementor page layouts, posts through single.php |
| +5 | כללי | מדיניות פרטיות + נגישות: טייטל ודיסקריפשן עם שם הלקוח | ✅ PASS | privacy title: ניק איטום / מדיניות פרטיות; accessibility title: ניק איטום / הצהרת נגישות |
| +6 | כללי | נראות במובייל ובמחשב נייד 1280 | 👁 MANUAL | zs qa measures 1440 + 390 and the hero at 1280×620; look at 1280 once by eye |
| +7 | כללי | שם הלקוח הנכון במדיניות הפרטיות ובהצהרת הנגישות | ✅ PASS | legal name: ניק איטום |
| +8 | כללי | מייל הטפסים ושם האתר מוגדרים נכון | ✅ PASS | leads → nickitum1@gmail.com; subject carries the site name; staging never mails the client |
| +9 | כללי | סדר היררכי של כותרות, בלי H2 בטפסים | ✅ PASS |  |
| +10 | כללי | כפתור נגישות (Ally) מוצג באתר | ✅ PASS | visible |

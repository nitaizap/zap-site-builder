# Launch sheet / דף השקה: c743850

Checked 2026-11-04 on `https://743850hercules.ussl.co.il` by `zs launch-check`. Gate: **READY (nothing failed)**; 2 item(s) below still need a person.
Zap does not launch client sites. This is what whoever launches this one needs. / זאפ לא מבצעת השקה. זה מה שמי שמשיק צריך.

## 1. What must travel with the site / מה חייב לנסוע

- **The `zap-site` plugin, with the theme `zap-base`.** The theme alone is not the site: every `zap-*` widget (menu, logo, lead form, legal line, contact list, Zap credit) and the launch behaviour (indexing, lead mail, address repair, `inc/launch.php`) live in the plugin. A migration tool that copies only some folders left it behind on הוילה הלבנה (03/11/2026): no menu, no form, still HTTP 200. Copy the whole `wp-content` (themes and plugins), or install both with `zs push <slug> --site https://<final> --live`.
- Plugins this page loads: `elementor`, `elementor-pro`, `pojo-accessibility` (plus `zap-site`, proven by its widgets, and Yoast SEO, which prints no assets).

## 2. What must be redone on the new domain / מה עושים מחדש בדומיין החדש

- **Elementor Pro licence**: the licence is tied to the domain: after the move the editor shows 'מפתח הרישיון אינו תואם לדומיין הנוכחי' and Pro features/updates stop until it is re-activated: wp-admin → Elementor → License → disconnect on the old domain, connect on the new one
- **Ally accessibility toolbar**: the toolbar button appears only after wp-admin → Ally → Connect on the live address: connect it again on the new domain (Zap SEO checklist row 10)
- DNS, SSL and Search Console for the new domain (a person, outside WordPress).
- The first request on the new address makes `launch.php` switch the site to live (index, robots.txt, lead mail) and rewrite the old address (`743850hercules.ussl.co.il`) inside Elementor's data: open the home page once, then wp-admin once.

## 3. Verify immediately after the move / מה לאמת מיד אחרי

1. `bin/zs launch-check https://<final-domain>` → every row PASS (it fails by name if the plugin is missing, the menu or form is gone, the site is still noindex, or anything still points at `*.ussl.co.il`).
2. wp-admin → Dashboard shows **no red notice** "חסר התוסף Zap Site" (the theme raises it when the plugin is not running).
3. Look at the home page on a phone (390px) and a laptop (1280px): logo, menu and burger, the form, the footer legal line.
4. Send one real test lead: it must arrive in the client's inbox (staging never mails them) and appear in wp-admin → Leads.
5. Re-do the section 2 items; Elementor → License must not say the key does not match the domain.

## Gate results on staging / תוצאות הבדיקה לפני ההעברה

| check | status | note |
|---|---|---|
| reachable | ✅ PASS | https://743850hercules.ussl.co.il -> HTTP 200, 149 KB / האתר נטען |
| zap-widgets | ✅ PASS | 11 zap-* widgets on the home page: zap-call-line, zap-copyright, zap-footer-contact, zap-form, zap-group-logo, zap-legal, zap-logo, zap-menu, zap-nav, zap-reviews, zap-topbar-meta / 11 ווידג'טים של זאפ בדף הבית |
| template-widgets | ✅ PASS | header: 3 zap widgets; footer: 8 zap widgets / תבניות הכותרת והפוטר מציגות ווידג'טים |
| raw-shortcodes | ✅ PASS | no unrendered [zap_*] shortcode / אין שורטקוד גולמי |
| header-nav | ✅ PASS | 18 menu links in the header, with burger / 18 קישורי תפריט בכותרת |
| lead-form | ✅ PASS | 3 lead form(s) on: contact, home / טופס פניות נמצא: contact, home |
| indexing | ✅ PASS | staging address (743850hercules.ussl.co.il): noindex, as it should be / חסום לאינדוקס, כמצופה |
| robots-txt | ✅ PASS | staging address: robots.txt disallows everything |
| staging-links | — N/A | staging address: nothing to move yet / כתובת סטייג'ינג |
| migration-pins | ✅ PASS | no foreign staging host and no scheme-less / encoded copy of this host: the address rewrite has nothing to miss / אין כתובות שההשקה תפספס |
| leads-not-mailed | 👁 MANUAL | cannot be observed from public html (a test lead would mail the client if staging mode failed). launch.php sets noindex and the lead routing in the same step, so noindex + Disallow in force above is the proof it ran; confirm once in wp-admin → Leads that a test lead was saved, never mailed / לא ניתן לבדוק מבחוץ |
| domain-licences | 👁 MANUAL | tied to the domain, redo them on the new one: Elementor Pro licence, Ally accessibility toolbar (details in the launch sheet) / מקושרים לדומיין, יש לחדש בדומיין החדש |
| desktop-mobile | ✅ PASS | desktop 24 pages, mobile 24 pages, 0 errors / דסקטופ ומובייל נבדקו, 0 שגיאות |

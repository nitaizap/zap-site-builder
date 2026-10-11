# העלאה לשרת — {{NAME}}

נבנה ב-{{DATE}} עבור **{{DOMAIN}}**. כל הכתובות במסד הנתונים כבר מצביעות לדומיין הזה.
אינדוקס במנועי חיפוש: **{{INDEX}}**.

## הדרך הקצרה (CloudPanel / כל שרת עם wp-cli)

1. ליצור אתר PHP (8.1 ומעלה) ומסד נתונים ריק.
2. להעלות את ה-zip לשרת ולחלץ אותו מחוץ ל-docroot.
3. מתוך התיקייה `{{SLUG}}`:

```bash
./deploy.sh --docroot /home/<user>/htdocs/<domain> \
  --db-name <db> --db-user <user> --db-pass '<pass>' --owner <user>
```

הסקריפט מעתיק את הקבצים, ממלא את `wp-config.php`, מייבא את המסד, יוצר סיסמת אדמין חדשה ומדפיס אותה,
ומנקה את כל הקאשים. אם הדומיין שונה מ-{{DOMAIN}}, מוסיפים `--url https://<domain>`.

## ידנית

1. להעתיק את תוכן `public_html/` ל-docroot.
2. ב-`wp-config.php` למלא את `__DB_NAME__`, `__DB_USER__`, `__DB_PASSWORD__`, `__DB_HOST__`.
3. לייבא את `database.sql` (phpMyAdmin או `mysql db < database.sql`).
4. `wp user update zapadmin --user_pass='<סיסמה חדשה>'`
5. `wp rewrite flush && wp elementor flush-css`

## robots.txt וכותרות אבטחה

- התוסף Zap Site כותב קובץ `robots.txt` אמיתי ומעדכן אותו לבד כשהדומיין או מצב האינדוקס משתנים
  (גם ב-nginx/uPress, שם robots.txt וירטואלי של וורדפרס לא עובד). לא לכתוב robots.txt ידנית.
- כותרות אבטחה נשלחות מ-`wp-config.php`, כך שגם עמודים מהקאש מקבלים אותן.
- WP Rocket (או קאש אחר) לא כלול בחבילה: להתקין לפי הנוהל של השרת ולהריץ בדיקה אנונימית.

## nginx

ה-`.htaccess` חוסם PHP בתיקיית uploads ואת xmlrpc רק ב-Apache. ב-nginx להוסיף:

```nginx
location ~* /wp-content/uploads/.*\.(php|phtml|phar)$ { deny all; }
location = /xmlrpc.php { deny all; }
```

## מה יש באתר

WordPress + Elementor (חינמי) + Yoast SEO + Ally (נגישות) + תבנית Zap Base + תוסף Zap Site
(טופס לידים שנשמר באתר ונשלח במייל דרך relay.d.co.il, סכמה, הקשחה). פניות מהאתר מופיעות גם ב-wp-admin → "פניות מהאתר".

---

# Deploy — English summary

`./deploy.sh --docroot <path> --db-name <db> --db-user <user> --db-pass '<pass>' [--owner <unix user>] [--url https://other.domain]`
Needs wp-cli and an empty DB/docroot. Prints the new admin password. See LAUNCH-CHECKLIST.md for the human steps.

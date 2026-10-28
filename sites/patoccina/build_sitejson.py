"""Writes site.json for patoccina (kept as a script so copy edits stay readable)."""
import json, os

B = "פטוצ'ינה"
MENUS = "page:תפריטים"

img = lambda src, alt: {"src": f"assets/{src}.jpg", "alt": alt}
images = {
    "buffet-quiches": img("buffet-quiches", "שולחן בופה של פטוצ'ינה עם פשטידות, מאפים ומגשי אירוח"),
    "brunch-table": img("brunch-table", "שולחן בראנץ' חלבי עם פשטידות, מאפים ופרחים ליד חלון"),
    "garden-buffet": img("garden-buffet", "בופה סלטים ומנות חלביות באירוע בגינה"),
    "dough": img("dough", "ידיים מעבדות כדורי בצק טרי על משטח עבודה"),
    "einat-spread": img("einat-spread", "עינת שליין, הבעלים של פטוצ'ינה, ליד שולחן אירוח ערוך"),
    "trays-boxes": img("trays-boxes", "מגשי אירוח ארוזים: כריכונים, מאפים ובורקיטס"),
    "trays-pastries": img("trays-pastries", "מגשי מאפים וכריכונים ארוזים במדבקת פטוצ'ינה"),
    "trays-buns": img("trays-buns", "מגש לחמניות שומשום ממולאות"),
    "trays-outdoor": img("trays-outdoor", "שולחן מגשי אירוח עם מאפים, טארטים וכריכים"),
    "cheese-board": img("cheese-board", "מגש גבינות, זיתים, ממרחים ופירות"),
    "caprese-salad": img("caprese-salad", "סלט עגבניות, מוצרלה ובזיליקום"),
    "trays-sandwiches": img("trays-sandwiches", "מגשי כריכים, מאפים וטורטיות"),
    "cheese-fruit": img("cheese-fruit", "מגש אירוח של גבינות, פירות וממרחים"),
    "quiche-veg": img("quiche-veg", "פשטידת תרד וגבינה לצד מגש ירקות חתוכים"),
    "quiche-pizza": img("quiche-pizza", "פשטידות ופיצה ביתית על שולחן עץ"),
    "event-tables": img("event-tables", "שולחנות עגולים ערוכים לאירוע בחוץ"),
    "event-courtyard": img("event-courtyard", "שולחנות אירוע ערוכים בחצר עם סלסלות מאפים"),
    "event-garden": img("event-garden", "שולחן אירוע ערוך עם פרחים ומפיות בגינה"),
}

def hero(title, lead, **kw):
    return {"type": "hero", "title": title, "lead": lead, **kw}

cta_end = {"type": "cta", "eyebrow": "הצעד הבא", "title": "בואו נתכנן יחד\nאת *האירוע שלכם*.",
           "text": "השאירו פרטים ונחזור אליכם בהקדם, או דברו איתנו ישירות בטלפון ובוואטסאפ."}

home = {"key": "", "type": "home", "title": "דף הבית",
  "seo": {"title": f"{B} | קייטרינג חלבי כשר לאירועים פרטיים ועסקיים",
          "description": f"{B} – קייטרינג חלבי כשר בטעמים איטלקיים: מגשי אירוח, קינוחים, מארזי ארוחות בוקר ובראנץ' ואירועים פרטיים ועסקיים, בתפריט בהתאמה אישית.",
          "keyword": "קייטרינג חלבי כשר"},
  "sections": [
    hero(f"קייטרינג חלבי כשר בטעמים איטלקיים מהלב — *{B}*",
         "מגשי אירוח, קינוחים, מארזי בוקר ובראנץ' ואירועים פרטיים ועסקיים – הכל בהתאמה אישית, כדי שהאירוע שלכם יהיה בדיוק כמו שדמיינתם.",
         eyebrow="קייטרינג בוטיק חלבי", cta={"label": "לתפריטים", "href": MENUS},
         cta2={"label": "דברו איתנו", "href": "page:צור-קשר"},
         points=["תפריט בהתאמה אישית", "חלבי כשר", "8 שנות ניסיון"],
         image="buffet-quiches", images=["brunch-table", "garden-buffet", "buffet-quiches"]),
    {"type": "trust", "items": [{"value": "8", "label": "שנים של אוכל מוכן, קייטרינג ואירועים"},
        {"value": "חלבי כשר", "label": "בטעמים איטלקיים"}, {"value": "4", "label": "תפריטים: מגשים, קינוחים, בראנץ', אירועים"},
        {"value": "אישי", "label": "כל תפריט נבנה סביבכם"}]},
    {"type": "marquee", "items": ["מגשי אירוח", "קינוחים", "בוקר ובראנץ'", "אירועים פרטיים", "אירועים עסקיים", "הכל אפשרי"]},
    {"type": "split", "eyebrow": "הכל אפשרי", "title": f"ב{B}\n*הכל אפשרי*.", "image": "trays-outdoor", "image_side": "end",
     "text": f"<p>כבר 8 שנים ש{B} מביאה לשולחן שלכם אוכל חלבי כשר, ביתי ומוקפד בהשראת המטבח האיטלקי. בין אם מדובר בישיבת צוות, בבראנץ' משפחתי, באירוע פרטי או באירוע עסקי – נבנה יחד אתכם תפריט שמתאים בדיוק לאירוע, לאורחים ולתקציב.</p>",
     "badge": {"title": "8", "text": "שנות ניסיון"}, "cta": {"label": "לתפריטים", "href": MENUS}},
    {"type": "cards", "layout": "bento", "eyebrow": "התפריטים", "title": "מה נגיש *אצלכם*?",
     "intro": "כל תפריט הוא נקודת התחלה – ואת כולם מתאימים אישית לאירוע, לכמות האורחים ולטעם שלכם.",
     "items": [
        {"title": "מגשי אירוח", "text": "לישיבות, למפגשים ולאירועים – עשירים, טעימים ומעוצבים בקפידה.", "image": "trays-pastries", "href": MENUS + "#מגשי-אירוח"},
        {"title": "תפריט קינוחים", "text": "קינוחים חלביים שסוגרים כל אירוע במתיקות.", "image": "cheese-fruit", "href": MENUS + "#קינוחים"},
        {"title": "מארזי בוקר ובראנץ'", "text": "מארזים מפנקים למשרד, למשפחה ולחגיגות קטנות.", "image": "brunch-table", "href": MENUS + "#בוקר-ובראנץ"},
        {"title": "אירועים פרטיים ועסקיים", "text": "מתכננים יחד את התפריט, ואנחנו דואגים להגשה ביום האירוע.", "image": "event-tables", "href": MENUS + "#אירועים"}]},
    {"type": "split", "eyebrow": "מי אנחנו", "title": f"נעים להכיר –\n*{B}*.", "image": "einat-spread", "image_side": "start",
     "text": f"<p>{B} נולדה מתוך אהבה גדולה לבישול ולאירוח של עינת שליין. את התשוקה למטבח האיטלקי – הטעמים העשירים והפשטות המתוחכמת – היא הפכה לקייטרינג חלבי כשר, שמביא טעם של בית לכל אירוע, עם שירות אישי והקפדה על כל פרט.</p>",
     "cta": {"label": "להכיר אותנו", "href": "page:נעים-להכיר"}},
    {"type": "gallery", "eyebrow": "גלריה", "title": "הצצה *לשולחן*.", "columns": 3,
     "images": ["trays-boxes", "caprese-salad", "cheese-board", "quiche-veg", "trays-buns", "event-garden"]},
    {"type": "features", "eyebrow": "למה אנחנו", "title": f"למה לבחור\nב*{B}*?", "columns": 4,
     "intro": "קייטרינג חלבי כשר שנבנה סביבכם – מהבחירה במנות ועד ההגשה ביום האירוע.",
     "items": [
        {"title": "תפריט בהתאמה אישית", "text": f"ב{B} הכל אפשרי – כל תפריט נבנה לאירוע ולקהל שלכם.", "icon": "sparkle"},
        {"title": "חלבי כשר, טעם איטלקי", "text": "קייטרינג חלבי כשר בהשראת המטבח האיטלקי.", "icon": "heart"},
        {"title": "8 שנות ניסיון", "text": "באוכל מוכן, בקייטרינג ובאירועים.", "icon": "award"},
        {"title": "מגוון לכל אירוע", "text": "מגשי אירוח, קינוחים, מארזי בוקר ובראנץ'.", "icon": "calendar"}]},
    cta_end]}

def menu_split(anchor, eyebrow, title, text, image, side):
    return {"type": "split", "anchor": anchor, "eyebrow": eyebrow, "title": title, "image": image, "image_side": side,
            "text": text, "cta": {"label": "להתאמת תפריט", "href": "page:צור-קשר"}}

menus = {"key": "תפריטים", "type": "hub", "title": "תפריטים", "excerpt": "מגשי אירוח, קינוחים, מארזי בוקר ובראנץ' ואירועים – בהתאמה אישית.",
  "featured_image": "trays-pastries",
  "seo": {"title": f"תפריטים | {B} – מגשי אירוח, קינוחים, בראנץ' ואירועים",
          "description": f"תפריטי {B}: מגשי אירוח, תפריט קינוחים, מארזי ארוחות בוקר ובראנץ' ואירועים פרטיים ועסקיים – קייטרינג חלבי כשר בהתאמה אישית.",
          "keyword": "מגשי אירוח חלביים"},
  "sections": [
    hero("התפריטים שלנו:\nמגשי אירוח חלביים, קינוחים ובראנץ'",
         f"ב{B} הכל אפשרי – כל אחד מהתפריטים כאן הוא נקודת התחלה, ואת כולם ניתן להתאים אישית לאירוע, לכמות האורחים ולטעם שלכם.",
         eyebrow="התפריטים", image="trays-sandwiches", cta={"label": "רוצים תפריט מותאם אישית? דברו איתנו", "href": "page:צור-קשר"}),
    menu_split("מגשי-אירוח", "מגשי אירוח", "מגשי *אירוח*.", "<p>מגשי אירוח לישיבות, למפגשים ולאירועים – עשירים, טעימים ומעוצבים בקפידה.</p>", "trays-pastries", "end"),
    menu_split("קינוחים", "קינוחים", "תפריט *קינוחים*.", "<p>קינוחים חלביים שסוגרים כל אירוע במתיקות.</p>", "cheese-fruit", "start"),
    menu_split("בוקר-ובראנץ", "בוקר ובראנץ'", "מארזי ארוחות בוקר\n*ובראנץ'*.", "<p>מארזי בוקר ובראנץ' מפנקים למשרד, למשפחה ולחגיגות קטנות.</p>", "brunch-table", "end"),
    menu_split("אירועים", "אירועים", "אירועים פרטיים\n*ועסקיים*.", "<p>קייטרינג מלא לאירועים פרטיים ועסקיים – מתכננים יחד את התפריט, מתאימים כמויות, ואנחנו דואגים להגשה ביום האירוע.</p>", "event-tables", "start"),
    {"type": "cta", "eyebrow": "הכל אפשרי", "title": f"ב{B}\n*הכל אפשרי*.",
     "text": "כל תפריט ניתן להתאמה אישית. רוצים תפריט מותאם אישית? דברו איתנו.",
     "cta": {"label": "דברו איתנו", "href": "page:צור-קשר"}}]}

about = {"key": "נעים-להכיר", "type": "about", "title": "נעים להכיר", "excerpt": f"עינת שליין ו{B} – קייטרינג חלבי כשר בטעמים איטלקיים.",
  "featured_image": "einat-spread",
  "seo": {"title": f"נעים להכיר | {B} קייטרינג חלבי כשר",
          "description": f"הכירו את {B} ואת עינת שליין – קייטרינג חלבי כשר בטעמים איטלקיים, עם שירות אישי ותפריט בהתאמה אישית לכל אירוע.",
          "keyword": f"{B} קייטרינג"},
  "sections": [
    hero(f"נעים להכיר — *{B} קייטרינג*", "קייטרינג חלבי כשר בטעמים איטלקיים, עם שירות אישי ותפריט בהתאמה אישית לכל אירוע.",
         eyebrow="מי אנחנו", image="einat-spread"),
    {"type": "split", "eyebrow": "עינת שליין", "title": "מהאהבה לבישול\n*לאירועים שלכם*.", "image": "dough", "image_side": "end",
     "text": f"<p>אני עינת שליין, הבעלים של {B} קייטרינג חלבי. האהבה לבישול ולאירוח ליוותה אותי שנים רבות, עד שהחלטתי להפוך את התשוקה הזו למקצוע – וכבר 8 שנים שאני מבשלת לאירועים של אחרים.</p>"
             f"<p>המטבח האיטלקי תמיד קסם לי – השילוב של טעמים עשירים ופשטות מתוחכמת. ב{B} אני מביאה את הקסם הזה לאירועים שלכם דרך תפריט חלבי כשר, ממנות ביתיות ומחומרי גלם טריים ואיכותיים.</p>"
             f"<p>אני מאמינה שאוכל טוב מחבר בין אנשים ויוצר רגעים שלא שוכחים. לכן כל תפריט נבנה יחד איתכם, בהתאמה אישית – כי ב{B} הכל אפשרי.</p>",
     "badge": {"title": "8", "text": "שנים במטבח של אירועים"}, "cta": {"label": "לתפריטים", "href": MENUS}},
    cta_end]}

gallery = {"key": "גלריה", "type": "page", "title": "גלריה", "excerpt": "הצצה למגשים, לקינוחים ולאירועים שלנו.", "featured_image": "trays-outdoor",
  "seo": {"title": f"גלריה | {B} קייטרינג חלבי כשר",
          "description": f"תמונות ממגשי האירוח, הקינוחים, מארזי הבוקר והאירועים של {B} – קייטרינג חלבי כשר בטעמים איטלקיים, בתפריט בהתאמה אישית לכל אירוע פרטי ועסקי.",
          "keyword": "גלריית קייטרינג חלבי"},
  "sections": [
    hero("גלריית קייטרינג חלבי", "הצצה למגשים, לקינוחים ולאירועים שלנו.", eyebrow="גלריה", image="trays-outdoor"),
    {"type": "gallery", "title": "מהמטבח *לשולחן*.", "columns": 3, "images": [
        "buffet-quiches", "trays-boxes", "caprese-salad", "brunch-table", "cheese-board", "trays-buns",
        "garden-buffet", "quiche-veg", "trays-pastries", "event-garden", "cheese-fruit", "quiche-pizza",
        "trays-sandwiches", "event-courtyard", "dough"]},
    cta_end]}

contact = {"key": "צור-קשר", "type": "contact", "title": "צור קשר",
  "seo": {"title": f"צור קשר | {B} קייטרינג חלבי כשר",
          "description": f"מתכננים אירוע? צרו קשר עם {B} להתאמת תפריט חלבי כשר אישי – מגשי אירוח, קינוחים, בראנץ' ואירועים. 053-6242885, וואטסאפ, קרן היסוד 1, פרדס חנה-כרכור.",
          "keyword": f"צור קשר {B}"},
  "sections": [
    hero(f"צור קשר — *{B}*", "דברו איתנו: ספרו לנו על האירוע שלכם ונחזור אליכם בהקדם עם הצעה לתפריט מותאם אישית."),
    {"type": "contact", "title": "פרטי התקשרות", "text": "ספרו לנו בהודעה על סוג האירוע, התאריך וכמות האורחים."}]}

site = {
  "site": {"lang": "he", "index": False, "tagline": "קייטרינג בוטיק חלבי"},
  "business": {"name": B, "legal_name": B, "schema_type": "FoodEstablishment",
    "phone_display": "053-6242885", "phone_e164": "+972536242885",
    "whatsapp_e164": "+972543830028", "whatsapp_text": f"שלום {B}, אשמח לשמוע על תפריט לאירוע",
    "email_leads": "feettuccine.inat@gmail.com", "email_public": "feettuccine.inat@gmail.com",
    "address": "קרן היסוד 1, פרדס חנה-כרכור", "street": "קרן היסוד 1", "city": "פרדס חנה-כרכור",
    "hours": ["7:30–21:00"], "opening_hours": ["Su-Th 07:30-21:00"],
    "area_served": ["פרדס חנה-כרכור"], "geo": {"lat": 32.477341, "lng": 34.981934},
    "dpz_customer_id": "80356988", "instagram": "https://www.instagram.com/patoccina_12/",
    "author_name": "עינת שליין"},
  "standards": {"privacy_url": "", "accessibility_url": "https://zap.dbusiness.co/js/accessibility.html"},
  "design": {},
  "directions": {},
  "form": {"title": "בואו נתכנן יחד את האירוע שלכם", "text": "השאירו פרטים ונחזור אליכם בהקדם, או דברו איתנו ישירות בטלפון ובוואטסאפ.",
           "button": "שליחה", "thanks": "תודה! קיבלנו את הפרטים ונחזור אליכם בהקדם."},
  "footer": {"about": f"{B} – קייטרינג בוטיק חלבי כשר בטעמים איטלקיים: מגשי אירוח, קינוחים, בראנץ' ואירועים.", "links_title": "התפריטים"},
  "header": {"cta_label": "דברו איתנו", "topbar_text": "קייטרינג חלבי כשר · תפריט בהתאמה אישית"},
  "content": {"disclaimer": ""},
  "logo": "assets/logo.png", "og_image": "buffet-quiches",
  "images": images,
  "nav": [{"label": "דף הבית", "href": "page:"}, {"label": "נעים להכיר", "href": "page:נעים-להכיר"},
          {"label": "תפריטים", "href": MENUS, "children": [
              {"label": "מגשי אירוח", "href": MENUS + "#מגשי-אירוח"}, {"label": "תפריט קינוחים", "href": MENUS + "#קינוחים"},
              {"label": "מארזי בוקר ובראנץ'", "href": MENUS + "#בוקר-ובראנץ"}, {"label": "אירועים פרטיים ועסקיים", "href": MENUS + "#אירועים"}]},
          {"label": "גלריה", "href": "page:גלריה"}, {"label": "צור קשר", "href": "page:צור-קשר"}],
  "footer_nav": [{"label": "מגשי אירוח", "href": MENUS + "#מגשי-אירוח"}, {"label": "תפריט קינוחים", "href": MENUS + "#קינוחים"},
                 {"label": "מארזי בוקר ובראנץ'", "href": MENUS + "#בוקר-ובראנץ"}, {"label": "אירועים פרטיים ועסקיים", "href": MENUS + "#אירועים"},
                 {"label": "נעים להכיר", "href": "page:נעים-להכיר"}, {"label": "גלריה", "href": "page:גלריה"}],
  "categories": [], "posts": [],
  "pages": [home, about, menus, gallery, contact],
}

colors = {"primary": "#561b31", "primary_ink": "#ffffff", "accent": "#b04a31", "accent_ink": "#ffffff",
          "ink": "#2a1219", "text": "#4a3a3e", "muted": "#6e5f62", "bg": "#fdfaf6", "surface": "#f6efe7",
          "line": "#e8ddd2", "dark": "#3a1222", "dark_ink": "#f6efe7"}
site["design"] = {"preset": "signature", "tone": "light", "hero": "split", "header": "light", "motion": "lively",
                  "colors": colors, "fonts": {"heading": "Frank Ruhl Libre", "body": "Assistant"}, "radius": 2, "custom_css": ""}
site["directions"] = {
  "a": {"label": "A · בוטיק איטלקי בהיר – סריף, שזיף ובז', סליידר תמונות (בהשראת teffee בגרסה בהירה)"},
  "b": {"label": "B · חם ורך – כותרות מודרניות, פינות מעוגלות, כפתורי גלולה", "preset": "soft", "hero": "split",
        "fonts": {"heading": "Rubik", "body": "Assistant"}, "radius": 18},
  "c": {"label": "C · מגזיני – טיפוגרפיה עדינה, קווים דקים, פתיח ממורכז", "preset": "editorial", "hero": "centered",
        "fonts": {"heading": "David Libre", "body": "Miriam Libre"}, "radius": 0, "motion": "subtle"},
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.json")
json.dump(site, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("wrote", out)

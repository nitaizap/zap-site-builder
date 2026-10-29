"""Pre-build checks on site.json. ERROR stops the build; WARN is reported and kept in the QA report.

These encode the rules that cost real rounds on earlier Zap builds: keyword cannibalisation,
invented social proof, placeholder copy, phone/tel mismatch, thin FAQs, missing ALT text.
"""
import json
import re

from sections import SECTIONS, VARIANTS

# Packages (references/pool.md): the tier caps the page count and keeps basic sites simple.
TIERS = {
    "basic": {"pages": 5, "banned": {"road", "route", "marquee", "video", "posts"}},
    "standard": {"pages": 12, "banned": set()},
    "premium": {"pages": None, "banned": set()},
}
NEEDS_IMAGE = {("features", "aside"), ("contact", "photo"), ("cta", "photo"), ("split", "overlap"), ("split", "card"), ("split", "duo"),
               ("hero", "cover"), ("hero", "inset"), ("hero", "curve"), ("faq", "aside"), ("leadbar", "photo"), ("reviews", "photo")}

RATING = re.compile(r"(★|⭐|\b[45][.,]\d\s*(כוכבים|ב-?גוגל|בגוגל|stars?)|דירוג\s*\d|\d+\s*ביקורות|\d+\s*חוות דעת)", re.I)
SUPERLATIVE = re.compile(r"(הטוב(ה|ים)? ביותר|הכי טוב|המוביל(ה|ים)? ב|מספר\s*1(?!\d)|#1(?![0-9a-fA-F])|הזול ביותר|המומחה הגדול)")
PLACEHOLDER = re.compile(r"(lorem|ipsum|TODO|TBD|XXX|\[\s*(שם|טלפון|כתובת|client|name)[^\]]*\]|PLACEHOLDER|לורם)", re.I)
DASH = re.compile(r"\S?\s?—\s?\S?|\S?\s–\s\S?")
MEDIA_LABEL = re.compile(r"(תמונ(ת|ות) אווירה|להמחשה בלבד|סרטון אווירה|לחצו להגדלה)")


def e164_from_display(d):
    digits = re.sub(r"\D", "", d or "")
    if digits.startswith("972"):
        return "+" + digits
    if digits.startswith("0"):
        return "+972" + digits[1:]
    return "+" + digits


def _texts(obj, path=""):
    """Every human-visible string in a structure, with a readable path."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("src", "href", "image", "images", "icon", "type", "key", "slug", "anchor", "bg", "category",
                     "related_page", "featured_image", "youtube_url", "kind", "video", "colors", "fonts", "preset", "hero", "header",
                     "variant", "tier", "kit", "archetype"):
                continue
            yield from _texts(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _texts(v, f"{path}[{i}]")


def validate(d, site_dir, _dir=None):
    out = []
    E = lambda m: out.append("ERROR " + m)
    W = lambda m: out.append("WARN  " + m)

    b = d.get("business", {})
    for k in ("name", "phone_display", "phone_e164"):
        if not b.get(k):
            E(f"business.{k} is required")
    if not b.get("email_leads"):
        W("business.email_leads missing: calls-only site, every lead form is replaced by call/WhatsApp buttons")
    if b.get("phone_display") and b.get("phone_e164") and e164_from_display(b["phone_display"]) != b["phone_e164"]:
        E(f"phone_e164 {b['phone_e164']} does not dial the displayed number {b['phone_display']} "
          f"(expected {e164_from_display(b['phone_display'])})")
    for k in ("phone_e164", "whatsapp_e164"):
        if b.get(k) and not re.fullmatch(r"\+972\d{8,9}", b[k]):
            E(f"business.{k} must look like +9725XXXXXXXX, got {b[k]}")
    std = d.get("standards", {})
    if not std.get("privacy_url") and not std.get("privacy_confirmed"):
        W("privacy policy: built from Zap's standard wording; confirm legal_name, privacy_database, privacy_purposes and "
          "privacy_email with the client, then set standards.privacy_confirmed (launch blocker until then)")
    if std.get("privacy_database") not in (None, True, False):
        E("standards.privacy_database must be true or false")
    if not b.get("dpz_customer_id"):
        W("business.dpz_customer_id missing: no reviews block will render (correct until a real id is provided)")

    pages = d.get("pages", [])
    keys = [p.get("key", p.get("slug", "")) for p in pages]
    if len(set(keys)) != len(keys):
        E("duplicate page keys: " + ", ".join(sorted({k for k in keys if keys.count(k) > 1})))
    if sum(1 for p in pages if p.get("type") == "home") != 1:
        E("exactly one page must have type 'home' (key '')")
    for k in keys:
        if re.search(r"[a-zA-Z]", k) and re.search(r"[֐-׿]", k):
            E(f"page key '{k}' mixes Hebrew and Latin; URLs must be one script (Hebrew)")

    kw_owner = {}
    for p in pages + [{**po, "key": "post:" + po["slug"]} for po in d.get("posts", [])]:
        key = p.get("key", "")
        name = key or "home"
        seo = p.get("seo", {})
        if p.get("type") in ("blog", "privacy") or p.get("noindex"):
            pass
        else:
            t, ds, kw = seo.get("title", ""), seo.get("description", ""), seo.get("keyword", "")
            short_ok = bool(b.get("name")) and t.startswith(b.get("name", "") + " | ")   # "site | page" may be short
            if not (25 <= len(t) <= 65) and not (short_ok and len(t) < 25):
                (E if not t else W)(f"{name}: seo.title is {len(t)} chars (want 30-60)")
            if not (150 <= len(ds) <= 160):
                (E if not ds else W)(f"{name}: seo.description is {len(ds)} chars (Zap SEO checklist: 150-160)")
            if not kw:
                E(f"{name}: seo.keyword missing (every indexable page owns one keyword)")
            else:
                if kw in kw_owner:
                    E(f"keyword cannibalisation: '{kw}' is owned by both {kw_owner[kw]} and {name}")
                kw_owner[kw] = name
        hero_s = next((s for s in p.get("sections", []) if s.get("type") == "hero"), None)
        if hero_s and p.get("type") != "home" and (hero_s.get("cta") or hero_s.get("cta2")):
            E(f"{name}: inner-page hero has buttons; Zap QA: buttons only in the home hero (the page and the lead form carry the action)")
        hero_t = (hero_s or {}).get("title", "")
        h1_plain = hero_t.replace("*", "").replace(chr(10), " ").strip()
        if p.get("type") == "home" and b.get("name") and h1_plain != b["name"]:
            E(f"home: the H1 is the client's name only ('{b['name']}', Zap checklist), not '{h1_plain}'; the keyword goes in the lead and the first H2")
        if p.get("type") == "about" and b.get("name") and b["name"].split()[0] not in h1_plain:
            W(f"{name}: the brand name should sit in the H1 on the about page")
        # Zap title format: "<client> | <page>" on every page
        st = seo.get("title", "")
        if st and b.get("name") and not st.startswith(b["name"] + " | ") and key != "":
            E(f"{name}: seo.title must read '{b['name']} | <page>' (Zap checklist), not '{st}'")
        if key == "" and st and b.get("name") and not st.startswith(b["name"]):
            E(f"home: seo.title starts with the client's name ('{b['name']} | ...'), not '{st}'")
        # slug = H1 (service/hub pages): the URL repeats the page's heading
        if p.get("type") in ("service", "hub") and h1_plain:
            slug_words = key.split("/")[-1].replace("-", " ")
            if slug_words != h1_plain.replace("־", " ").replace("'", "").replace('"', ""):
                W(f"{name}: the URL '{key.split('/')[-1]}' should match the H1 '{h1_plain}' (Zap QA: slug = H1)")
        # headings never end with a full stop (Zap QA); a question mark or nothing
        # one short line: never "keyword\nbrand" joined into one H1 (Zap QA); posts are exempt
        if hero_t and not key.startswith("post:"):
            if chr(10) in h1_plain or chr(10) in hero_t or " — " in h1_plain:
                E(f"{name}: H1 '{h1_plain}' joins two lines into one H1; use one short line (Zap QA)")
            if len(h1_plain.split()) > 6:
                W(f"{name}: H1 '{h1_plain}' is {len(h1_plain.split())} words; Zap QA wants the page name, short")
        if p.get("type") == "blog" and len(d.get("posts", [])) < 3:
            E(f"{name}: a blog page needs at least 3 published posts (has {len(d.get('posts', []))}); Zap QA rejects an empty blog")
        secs = p.get("sections", [])
        if secs and secs[-1].get("type") == "cta" and p.get("type") not in ("contact",):
            E(f"{name}: page ends with a cta section and the lead form follows it: two calls to action in a row (Zap QA); drop the cta or move it up")
        for s_ in secs:
            gk = s_.get("images") or []
            if len(gk) != len(set(gk)):
                E(f"{name}: {s_.get('type')} repeats a photo: {sorted({k for k in gk if gk.count(k) > 1})}")
            icons = [it.get("icon") for it in s_.get("items", []) if isinstance(it, dict) and it.get("icon")]
            dup = sorted({i for i in icons if icons.count(i) > 1})
            if dup:
                E(f"{name}: {s_.get('type')} section repeats icon(s) {dup}: one icon per item, matching its content (Zap QA)")
        heads = [hero_t] + [s.get("title", "") for s in p.get("sections", [])]
        heads += [it.get("title", "") for s in p.get("sections", []) for it in (s.get("items") or []) if isinstance(it, dict)]
        heads += re.findall(r"<h[2-4][^>]*>(.*?)</h[2-4]>", " ".join(s.get("html", "") for s in p.get("sections", [])) + p.get("html", ""))
        for h in heads:
            if isinstance(h, str) and h.rstrip("*").rstrip().endswith("."):
                E(f"{name}: heading ends with a full stop: '{h.strip()[-40:]}' (headings take no period)")
        for s in p.get("sections", []):
            if s.get("type") == "faq" and len(s.get("items", [])) < 3:
                E(f"{name}: FAQ needs at least 3 real questions (has {len(s.get('items', []))})")
            for it in s.get("items", []) if isinstance(s.get("items"), list) else []:
                h = it.get("href", "") if isinstance(it, dict) else ""
                if h.startswith("page:") and h[5:].partition('#')[0] not in keys:
                    E(f"{name}: link to missing page '{h}'")
            for bt in ("cta", "cta2", "more"):
                h = (s.get(bt) or {}).get("href", "")
                if h.startswith("page:") and h[5:].partition('#')[0] not in keys:
                    E(f"{name}: button links to missing page '{h}'")
        if p.get("sections") and not any(s.get("type") == "hero" for s in p["sections"]):
            E(f"{name}: page has sections but no hero (the hero carries the only H1)")
        if key.startswith("post:") and p.get("related_page") and p["related_page"] not in keys:
            E(f"{name}: related_page '{p['related_page']}' does not exist")

    # menu label = the page's name everywhere (Zap QA: "מדה ואיטום חדרים רטובים" in the menu, another H1 on the page)
    h1_of = {p.get("key", ""): next((s.get("title", "") for s in p.get("sections", []) if s.get("type") == "hero"), "").replace("*", "").replace(chr(10), " ")
             for p in pages}
    for item in d.get("nav", []):
        for it in [item] + item.get("children", []):
            h = it.get("href", "")
            if h.startswith("page:") and h[5:] and h[5:] in h1_of and h1_of[h[5:]] and it.get("label") not in h1_of[h[5:]]:
                W(f"menu item '{it.get('label')}' differs from that page's H1 '{h1_of[h[5:]]}': use one name")
    # blog: Hebrew category slugs, at least 3 posts (Zap SEO checklist)
    if any(p.get("type") == "blog" for p in pages):
        if not d.get("categories"):
            E("a blog page needs at least one category in site.json (else the base site's leftover category shows, e.g. /blog/)")
        if len(d.get("posts", [])) < 3:
            W(f"the blog has {len(d.get('posts', []))} posts; the Zap SEO checklist wants 3 (from the brief and the client's old site)")
    for c in d.get("categories", []):
        if not 150 <= len(c.get("description", "")) <= 160:
            E(f"category '{c.get('slug')}': description is {len(c.get('description', ''))} chars; it is the archive's meta description (150-160)")
        if re.search(r"[a-zA-Z]", c.get("slug", "")):
            E(f"category slug '{c.get('slug')}' must be Hebrew (no Latin in URLs)")
    if not d.get("favicon"):
        W("no favicon in site.json: the cloned base site's icon stays; add a square PNG (512+) made from the client's logo symbol")
    # Zap QA: the blog is in the main menu; menu and footer list the pages in the same order
    if any(p.get("type") == "blog" for p in pages):
        bk = next(p.get("key") for p in pages if p.get("type") == "blog")
        if not any(i.get("href") == f"page:{bk}" for i in d.get("nav", [])):
            E("the blog page is missing from the main menu (nav)")
    nav_order = [i.get("href") for i in d.get("nav", []) if i.get("href") != "page:"]
    foot_order = [i.get("href") for i in d.get("footer_nav", []) if i.get("href") in nav_order]
    if foot_order != [h for h in nav_order if h in foot_order]:
        E("footer_nav lists the pages in a different order from nav (Zap QA: same order in both)")
    if d.get("nav") and d["nav"][0].get("href") != "page:":
        E("nav must start with a 'דף הבית' item (Zap QA round 2: home is the first menu item, desktop and mobile)")
    for c in d.get("categories", []):
        if c.get("description") and not c["description"].rstrip().endswith((".", "!", "?")):
            E(f"category '{c.get('slug')}' description is cut mid-sentence (it shows on the blog page): end it with a full sentence")

    for item in d.get("nav", []) + d.get("footer_nav", []):
        for it in [item] + item.get("children", []):
            h = it.get("href", "")
            if h.startswith("page:") and h[5:].partition('#')[0] not in keys:
                E(f"menu item '{it.get('label')}' links to missing page '{h}'")

    body_font = ((d.get("design") or {}).get("fonts") or {}).get("body", "")
    if body_font in ("Miriam Libre", "Frank Ruhl Libre", "Noto Serif Hebrew", "David Libre", "Bellefair", "Bona Nova",
                     "Suez One", "Secular One", "Karantina", "Fredoka", "Varela Round"):
        E(f"design.fonts.body '{body_font}' is a display/serif face; Zap QA: body text and forms in a readable sans "
          "(Assistant, Heebo, Rubik, Noto Sans Hebrew, IBM Plex Sans Hebrew, Alef); keep the character font for headings")
    imgs = d.get("images", {})
    try:
        from PIL import Image
        hashes = {}
        for k, v in imgs.items():
            f = (site_dir / v.get("src", "")) if site_dir else None
            if f and f.exists() and f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                im = Image.open(f).convert("L").resize((9, 8))
                px = list(im.getdata())
                hashes[k] = sum(1 << i for i in range(64) if px[(i // 8) * 9 + i % 8] > px[(i // 8) * 9 + i % 8 + 1])
        ks = list(hashes)
        near = [(a, c) for i, a in enumerate(ks) for c in ks[i + 1:] if bin(hashes[a] ^ hashes[c]).count("1") <= 10]
        for a, c in near:
            W(f"images '{a}' and '{c}' look like the same shot; Zap QA flags the same view twice in one gallery: keep one")
    except Exception:
        pass
    used = set(re.findall(r'"(?:image|featured_image)":\s*"([^"]+)"', json.dumps(d, ensure_ascii=False)))
    for lst in re.findall(r'"images":\s*\[([^\]]*)\]', json.dumps(d, ensure_ascii=False)):
        used |= set(re.findall(r'"([^"]+)"', lst))
    for k in used - set(imgs):
        E(f"image key '{k}' is used but not defined in images")
    for k, im in imgs.items():
        if not im.get("alt") and not im.get("decorative"):
            E(f"image '{k}' has no ALT text")
        if not (site_dir / im.get("src", "")).exists():
            E(f"image '{k}': file {im.get('src')} not found in the site folder")
    for k, v in d.get("videos", {}).items():
        f = site_dir / v.get("src", "")
        if not f.exists():
            E(f"video '{k}': file {v.get('src')} not found")
        elif not str(f).lower().endswith((".mp4", ".webm")):
            E(f"video '{k}' must be .mp4 or .webm")
        elif f.stat().st_size > 6 * 1048576:
            E(f"video '{k}' is {f.stat().st_size // 1048576} MB; keep hero loops under 6 MB (4-8 s, 720p, no audio)")
    for p in pages:
        for s in p.get("sections", []):
            if s.get("type") == "hero" and s.get("video"):
                if s["video"] not in d.get("videos", {}):
                    E(f"{p.get('key') or 'home'}: hero video '{s['video']}' is not defined in videos")
                if not s.get("image"):
                    E(f"{p.get('key') or 'home'}: a hero video needs an image too (it is the poster and the mobile view)")
    if d.get("logo") and str(d["logo"]).lower().endswith(".svg"):
        E("logo must be PNG/WebP (WordPress rejects SVG uploads); convert it first")

    bt = (d.get("design") or {}).get("base_template")
    if bt is not None and bt not in range(1, 7):
        E(f"design.base_template must be 1-6 (the Zap Figma templates), got {bt}")
    if not any(p.get("type") == "blog" for p in pages):
        W("no blog page: the Zap SEO checklist wants a blog category on every site (3 posts arrive through BestLinks)")
    tier = d.get("tier")
    if tier and tier not in TIERS:
        E(f"tier '{tier}' unknown; use one of {', '.join(TIERS)}")
    elif tier:
        t = TIERS[tier]
        real = [p for p in pages if p.get("type") not in ("privacy", "blog")]
        if t["pages"] and len(real) > t["pages"]:
            E(f"tier {tier} allows {t['pages']} pages, site.json has {len(real)} (privacy/blog not counted)")
    for p in pages:
        name = p.get("key") or "home"
        for s in p.get("sections", []):
            ty, v = s.get("type"), s.get("variant")
            if tier in TIERS and ty in TIERS[tier]["banned"]:
                E(f"{name}: section '{ty}' is not part of the {tier} package")
            if tier == "basic" and ty == "hero" and (s.get("video") or len(s.get("images", [])) > 1):
                E(f"{name}: basic package hero is one still photo (no video, no slider)")
            if ty == "tiles" and any(not it.get("image") for it in s.get("items", [])):
                E(f"{name}: every tiles item needs an image")
            if ty == "pricelist" and not (s.get("items") or any(g.get("items") for g in s.get("groups", []))):
                E(f"{name}: pricelist needs items (or groups with items)")
            if ty in ("facts", "team") and not s.get("items"):
                E(f"{name}: {ty} needs items")
            if ty == "facts" and any(not (it.get("label") and str(it.get("value", "")).strip()) for it in s.get("items", [])):
                E(f"{name}: every facts item needs a label and a value")
            if ty == "hero" and s.get("form") and p.get("type") == "contact":
                E(f"{name}: no hero form on the contact page: it has its own full form (one form per page, Zap QA)")
            if v is None:
                continue
            if ty in SECTIONS and v not in VARIANTS.get(ty, set()):
                E(f"{name}: {ty} has no variant '{v}'; known: {', '.join(sorted(VARIANTS.get(ty, ()))) or 'none'}")
            if (ty, v) in NEEDS_IMAGE and not s.get("image"):
                E(f"{name}: {ty} variant '{v}' needs an image")
            if (ty, v) == ("split", "duo") and not s.get("image2"):
                E(f"{name}: split variant 'duo' needs image2 (the small overlapping photo)")
            if (ty, v) == ("gallery", "stagger") and len(s.get("images", [])) != 4:
                E(f"{name}: gallery variant 'stagger' takes exactly 4 images")

    for path, txt in _texts({k: v for k, v in d.items() if not k.startswith("_")}):
        if RATING.search(txt):
            E(f"{path}: rating/review claim without a connected source: '{RATING.search(txt).group(0)}'")
        if PLACEHOLDER.search(txt):
            E(f"{path}: placeholder text: '{PLACEHOLDER.search(txt).group(0)}'")
        if MEDIA_LABEL.search(txt):
            E(f"{path}: visible media label/instruction: '{MEDIA_LABEL.search(txt).group(0)}'")
        if path.split(".")[-1] not in ("custom_css",) and DASH.search(txt):
            E(f"{path}: dash as punctuation ('{DASH.search(txt).group(0).strip()}'): rewrite with a comma, colon, period or a line break (house rule: no em/en dashes in site copy)")
        if SUPERLATIVE.search(txt):
            W(f"{path}: unverifiable superlative: '{SUPERLATIVE.search(txt).group(0)}'")
    from sections import KITS
    for where, dz in [("design", d.get("design", {}))] + [(f"directions.{k}", v) for k, v in (d.get("directions") or {}).items() if isinstance(v, dict)]:
        if dz.get("kit") and dz["kit"] not in KITS:
            E(f"{where}.kit '{dz['kit']}' is not a style kit: {', '.join(KITS)}")
    # Gate directions with their own home page: the same checks as the real home, on a copy that uses it.
    if _dir is None:
        seen = set(out)
        for k, dv in (d.get("directions") or {}).items():
            if not isinstance(dv, dict) or "home" not in dv:
                continue
            if not isinstance(dv["home"], list) or not dv["home"]:
                E(f"directions.{k}.home must be a non-empty list of sections")
                continue
            import copy
            alt = copy.deepcopy(d)
            alt.pop("directions", None)
            alt["design"] = {**alt.get("design", {}), **{x: v for x, v in dv.items() if x not in ("home", "label")}}
            for pg in alt.get("pages", []):
                if pg.get("type") == "home":
                    pg["sections"] = dv["home"]
            for m in validate(alt, site_dir, _dir=k):
                if m not in seen and m.startswith("ERROR"):
                    out.append(m.replace("ERROR ", f"ERROR direction {k}: ", 1))
    return out

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
                     "variant", "tier"):
                continue
            yield from _texts(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _texts(v, f"{path}[{i}]")


def validate(d, site_dir):
    out = []
    E = lambda m: out.append("ERROR " + m)
    W = lambda m: out.append("WARN  " + m)

    b = d.get("business", {})
    for k in ("name", "phone_display", "phone_e164", "email_leads"):
        if not b.get(k):
            E(f"business.{k} is required")
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
            if not (25 <= len(t) <= 65):
                (E if not t else W)(f"{name}: seo.title is {len(t)} chars (want 30-60)")
            if not (150 <= len(ds) <= 160):
                (E if not ds else W)(f"{name}: seo.description is {len(ds)} chars (Zap SEO checklist: 150-160)")
            if not kw:
                E(f"{name}: seo.keyword missing (every indexable page owns one keyword)")
            else:
                if kw in kw_owner:
                    E(f"keyword cannibalisation: '{kw}' is owned by both {kw_owner[kw]} and {name}")
                kw_owner[kw] = name
                h1 = next((s.get("title", "") for s in p.get("sections", []) if s.get("type") == "hero"), p.get("title", "")).replace("*", "").replace(chr(10), " ")
                core = kw.split()[0] if kw else ""
                if core and core not in h1:
                    W(f"{name}: H1 '{h1}' does not contain the keyword '{kw}'")
        if p.get("type") in ("home", "about") and b.get("name"):
            h1 = next((s.get("title", "") for s in p.get("sections", []) if s.get("type") == "hero"), "")
            if b["name"].split()[0] not in h1:
                W(f"{name}: the brand name should sit in the H1 on home/about")
        for s in p.get("sections", []):
            if s.get("type") == "faq" and len(s.get("items", [])) < 3:
                E(f"{name}: FAQ needs at least 3 real questions (has {len(s.get('items', []))})")
            for it in s.get("items", []) if isinstance(s.get("items"), list) else []:
                h = it.get("href", "") if isinstance(it, dict) else ""
                if h.startswith("page:") and h[5:] not in keys:
                    E(f"{name}: link to missing page '{h}'")
            for bt in ("cta", "cta2", "more"):
                h = (s.get(bt) or {}).get("href", "")
                if h.startswith("page:") and h[5:] not in keys:
                    E(f"{name}: button links to missing page '{h}'")
        if p.get("sections") and not any(s.get("type") == "hero" for s in p["sections"]):
            E(f"{name}: page has sections but no hero (the hero carries the only H1)")
        if key.startswith("post:") and p.get("related_page") and p["related_page"] not in keys:
            E(f"{name}: related_page '{p['related_page']}' does not exist")

    for item in d.get("nav", []) + d.get("footer_nav", []):
        for it in [item] + item.get("children", []):
            h = it.get("href", "")
            if h.startswith("page:") and h[5:] not in keys:
                E(f"menu item '{it.get('label')}' links to missing page '{h}'")

    imgs = d.get("images", {})
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
        if SUPERLATIVE.search(txt):
            W(f"{path}: unverifiable superlative: '{SUPERLATIVE.search(txt).group(0)}'")
    return out

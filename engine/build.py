"""site.json -> a fully built WordPress. Idempotent: run it as often as you like.

Everything goes through one PHP payload per build step (wp eval-file), never shell-quoted
strings, so Hebrew, quotes and JSON survive intact.
"""
import hashlib
import json
import os
import re
from pathlib import Path

from images import prepare_image
from sections import Ctx, footer_template, header_template, post_template, render_page, service_template
from validate import validate

PHP_LIB = Path(__file__).with_name("wp_lib.php")


def page_path(p, by_key):
    """Public path of a page from its key ('' = home)."""
    return "/" if p["key"] == "" else "/" + p["key"].strip("/") + "/"


def load_site(site_dir):
    data = json.loads((site_dir / "site.json").read_text(encoding="utf-8"))
    pages = data.get("pages", [])
    for p in pages:
        p.setdefault("key", p.get("slug", ""))
    data["_paths"] = {p["key"]: page_path(p, None) for p in pages}
    blog = next((p for p in pages if p.get("type") == "blog"), None)
    base = data["_paths"][blog["key"]] if blog else "/"
    data["_post_paths"] = {po["slug"]: base + po["slug"] + "/" for po in data.get("posts", [])}
    return data


def run_php(site, task, payload):
    """Call a function in wp_lib.php inside WordPress with a JSON payload."""
    f = site.dir / f"_payload_{task}.json"
    f.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    remote = getattr(site, "remote", False)
    # a remote site (Novamira) gets the library and the payload uploaded first; paths are then server paths
    lib = site.put(PHP_LIB, name="zs-lib.txt") if remote else str(PHP_LIB)   # .php uploads are refused (sandbox); require() reads any name
    data_path = site.put(f, name=f"_payload_{task}_{hashlib.sha1(f.read_bytes()).hexdigest()[:10]}.json") if remote else str(f)
    code = (f"require_once {json.dumps(lib)};\n"
            f"zs_task_{task}(json_decode(file_get_contents({json.dumps(data_path)}), true));\n")
    try:
        return site.eval_php(code)
    finally:
        if not os.environ.get("ZS_KEEP_PAYLOADS"):
            f.unlink(missing_ok=True)


def chunks(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)] or [[]]



def _privacy_desc(name):
    """150-160 characters (Zap SEO checklist), whatever the length of the business name."""
    d = f"מדיניות הפרטיות של {name}: איזה מידע נאסף בטופסי האתר, איך הוא נשמר ומשמש, ואיך אפשר לעיין בו, לתקן אותו או לבקש למחוק אותו"
    for extra in (" בכל עת", " בפנייה אלינו", ", בהתאם לחוק"):
        if len(d) + len(extra) + 1 <= 160 and len(d) < 149:
            d += extra
    return (d if len(d) <= 159 else d[:156].rsplit(" ", 1)[0]) + "."


def privacy_html(data):
    """Zap's standard privacy policy for this business. Only the template's {{...}} fields are filled:
    the company (business.legal_name), the database paragraph (standards.privacy_database: true only when
    the client confirmed it keeps a database), extra purposes (standards.privacy_purposes; default: answering
    the site's contact form) and the privacy e-mail (standards.privacy_email, else business.email_public)."""
    import html as _h
    b, std = data["business"], data.get("standards", {})
    t = (Path(__file__).parent / "templates" / "privacy-he.html").read_text(encoding="utf-8")
    t = re.sub(r"<!--.*?-->\s*", "", t, count=1, flags=re.S)
    db = ("<p>הנתונים שתמסור בעת ההרשמה לשירותים באתרים ו/או בעת עדכון פרטיך (כפי שיעשה מעת לעת), יישמרו במאגר "
          "המידע של החברה, המנוהל בהתאם לחוק הגנת הפרטיות, התשמ\"א – 1981 לרבות לצורך דיוור שיווקי ודוור ישיר.</p>"
          if std.get("privacy_database") else "")
    purposes = std.get("privacy_purposes") or ["לצורך מענה לפניות שנשלחו באמצעות טופסי יצירת הקשר באתר וחזרה אל הפונה."]
    mail = std.get("privacy_email") or b.get("email_public") or b.get("email_leads", "")
    fill = {"name": _h.escape(b.get("legal_name") or b["name"]), "data": db,
            "more1": "\n".join(f"<li>{_h.escape(x)}</li>" for x in purposes),
            "mail": f'<a href="mailto:{_h.escape(mail)}" dir="ltr">{_h.escape(mail)}</a>'}
    # registration / social-login wording only on sites that have accounts (Zap QA: "there is no registration here")
    t = re.sub(r"<!--acct-->(.*?)<!--/acct-->", (lambda m: m.group(1)) if std.get("privacy_accounts") else "", t, flags=re.S)
    return re.sub(r"\{\{(\w+)\}\}", lambda m: fill[m.group(1)], t).strip()


def accessibility_html(data):
    """Zap's standard accessibility statement (engine/templates/accessibility-he.html); only the contact line is
    filled (business name, phone, public e-mail)."""
    import html as _h
    b = data["business"]
    t = (Path(__file__).parent / "templates" / "accessibility-he.html").read_text(encoding="utf-8")
    t = re.sub(r"<!--.*?-->\s*", "", t, count=1, flags=re.S)
    parts = [_h.escape(b["name"])]
    if b.get("phone_display"):
        parts.append(f'טלפון <a href="tel:{_h.escape(b.get("phone_e164", ""))}" dir="ltr">{_h.escape(b["phone_display"])}</a>')
    mail = b.get("email_public") or ""
    if mail:
        parts.append(f'דוא״ל <a href="mailto:{_h.escape(mail)}" dir="ltr">{_h.escape(mail)}</a>')
    return t.replace("{{contact}}", ", ".join(parts) + ".").strip()


def build(site, only=None):
    site_dir = site.src
    data = load_site(site_dir)
    problems = validate(data, site_dir)
    errors = [p for p in problems if p.startswith("ERROR")]
    for p in problems:
        print(p)
    if errors:
        raise SystemExit(f"site.json has {len(errors)} error(s); fix them and build again.")

    # Privacy policy: Zap's standard wording (engine/templates/privacy-he.html, the text behind
    # campaign.zapx.co.il/privacy-policy), filled from site.json. A site with its own policy sets
    # standards.privacy_url and gets no generated page.
    std = data.setdefault("standards", {})
    if not std.get("privacy_url"):
        b = data["business"]
        data["pages"].append({
            "key": "מדיניות-פרטיות", "type": "privacy", "title": "מדיניות פרטיות", "noindex": True,
            "seo": {"title": f"{b['name']} | מדיניות פרטיות",
                    "description": _privacy_desc(b["name"])},
            "content": privacy_html(data),
        })
        std["privacy_url"] = "/מדיניות-פרטיות/"
        data["_paths"]["מדיניות-פרטיות"] = "/מדיניות-פרטיות/"
    # Accessibility statement: Zap's standard text as the site's own page (the client's title and description,
    # Zap QA), linked from the footer. A site that must link elsewhere sets standards.accessibility_url.
    if not std.get("accessibility_url") or "zap.dbusiness.co" in std.get("accessibility_url", ""):
        b = data["business"]
        # 150-160 characters from real content only (Zap QA rejects filler endings like "ונשמח לעזור"):
        # a longer or shorter list of the statement's actual measures, whatever the name's length
        parts = ["ניגודיות כהה ובהירה", "הדגשת כותרות וקישורים", "חלופה טקסטואלית לתמונות", "טפסים נגישים", "ניווט במקלדת"]
        ends = ["תפריט הנגישות ופרטי הפנייה בנושא.", "איך משתמשים בתפריט הנגישות ולמי פונים בנושא נגישות."]
        cands = [f"הצהרת הנגישות של {b['name']}: אמצעי הנגישות באתר ({', '.join(parts[:n])}), {e}"
                 for n in range(len(parts), 0, -1) for e in ends]
        fit = [c for c in cands if 150 <= len(c) <= 160]
        d = fit[0] if fit else max((c for c in cands if len(c) <= 160), key=len, default=cands[-1][:160])
        data["pages"].append({
            "key": "הצהרת-נגישות", "type": "privacy", "legal": "accessibility", "title": "הצהרת נגישות", "noindex": False,
            "seo": {"title": f"{b['name']} | הצהרת נגישות", "description": d[:160]},
            "content": accessibility_html(data),
        })
        std["accessibility_url"] = "/הצהרת-נגישות/"
        data["_paths"]["הצהרת-נגישות"] = "/הצהרת-נגישות/"

    site.install_code()
    log = []

    # 1. options + identity
    out = run_php(site, "options", {
        "zap_site": {k: data.get(k, {}) for k in ("business", "design", "directions", "standards", "form",
                                                   "footer", "header", "smtp", "content", "site")},
        "title": data["business"]["name"],
        "tagline": data.get("site", {}).get("tagline", ""),
    })
    log.append(out)

    # 2. media
    images = dict(data.get("images", {}))
    if data.get("logo"):
        images["__logo"] = {"src": data["logo"], "alt": data["business"]["name"], "keep_format": True}
    if data.get("logo_light"):
        images["__logo_light"] = {"src": data["logo_light"], "alt": data["business"]["name"], "keep_format": True}
    elif data.get("logo") and (data.get("design") or {}).get("tone") != "light":
        # a dark footer gets the logo in white (Zap QA: no logo on a white chip): the same artwork, recoloured
        from PIL import Image
        src = Image.open(site_dir / data["logo"]).convert("RGBA")
        a = src.getchannel("A")
        white = Image.new("RGBA", src.size, (255, 255, 255, 0)); white.putalpha(a)
        out = site.dir / "_gen"; out.mkdir(parents=True, exist_ok=True)
        white.save(out / "logo-light.png")
        images["__logo_light"] = {"src": str(out / "logo-light.png"), "alt": data["business"]["name"], "keep_format": True}
    if data.get("favicon"):   # square PNG from the client's logo symbol; replaces the cloned base site's icon
        images["__favicon"] = {"src": data["favicon"], "alt": data["business"]["name"], "keep_format": True, "max_width": 512}
    prepared = []
    for key, im in images.items():
        src = site_dir / im["src"]
        if not src.exists():
            raise SystemExit(f"image '{key}': file not found: {src}")
        out_file, w, h = prepare_image(src, site.dir / "_media", keep_format=im.get("keep_format", False),
                                       max_width=im.get("max_width", 600 if im.get("keep_format") else 1600))
        prepared.append({"key": key, "file": str(out_file), "alt": im.get("alt", ""),
                         "title": im.get("title", ""), "ai": bool(im.get("ai")),
                         "hash": hashlib.sha1(out_file.read_bytes()).hexdigest()})
    # Videos (hero loops) are imported as they are: the engine never re-encodes video.
    for key, v in data.get("videos", {}).items():
        src = site_dir / v["src"]
        if not src.exists():
            raise SystemExit(f"video '{key}': file not found: {src}")
        prepared.append({"key": key, "file": str(src), "alt": "", "title": v.get("title", ""), "ai": bool(v.get("ai")),
                         "hash": hashlib.sha1(src.read_bytes()).hexdigest()})
    remote = getattr(site, "remote", False)
    # a repeat push skips what the server already holds: media with the same file hash, pages with the same payload
    state = {"media": {}, "pages": {}}
    if remote and not getattr(site, "full", False):
        state = json.loads(run_php(site, "state", {}).splitlines()[-1])
        state["media"] = state["media"] or {}
        state["pages"] = state["pages"] or {}
    same = [it for it in prepared if (state["media"].get(it["key"]) or {}).get("hash") == it["hash"]]
    todo = [it for it in prepared if it not in same]
    if remote:   # files travel to the server first; small batches keep every call under Novamira's 30 s limit
        for it in todo:
            it["file"] = site.put(it["file"])
    media = {}
    if same:     # unchanged: one call refreshes alt texts, no upload
        media.update(json.loads(run_php(site, "media", {"items": same}).splitlines()[-1]))
    for batch in chunks(todo, 2 if remote else len(todo) or 1) if todo else []:
        media.update(json.loads(run_php(site, "media", {"items": batch}).splitlines()[-1]))
    log.append(f"media: {len(media)} items")
    if "__logo_light" in media:
        run_php(site, "set_option", {"key": "logo_light_id", "value": media["__logo_light"]["id"]})

    # 3. pages (parents first so children can attach)
    pages = sorted(data.get("pages", []), key=lambda p: p["key"].count("/"))
    use_tpl = (data.get("templates") or {}).get("shared", True)   # service pages + posts through shared templates
    payload = []
    for p in pages:
        ctx = Ctx(p["key"], media, data)
        secs = p.get("sections") or []
        hero_s = next((s for s in secs if s.get("type") == "hero"), {})
        shared = p.get("type") == "service" and use_tpl
        if shared:   # the service template carries the hero (title, excerpt, image) and the closing CTA
            secs = [s for s in secs if s.get("type") not in ("hero", "cta")]
            p = {**p, "excerpt": hero_s.get("lead") or p.get("excerpt", ""),
                 "featured_image": hero_s.get("image") or p.get("featured_image")}
        elements = render_page(ctx, secs) if secs else None
        if p.get("sections") and not shared and ctx.h1_count != 1:
            raise SystemExit(f"page '{p['key'] or 'home'}' renders {ctx.h1_count} H1s (must be exactly 1)")
        parent = p["key"].rsplit("/", 1)[0] if "/" in p["key"] else None
        payload.append({
            "key": p["key"], "slug": p["key"].rsplit("/", 1)[-1] if p["key"] else "home",
            "parent": parent, "title": p["title"], "type": p.get("type", "page"),
            "excerpt": p.get("excerpt", ""), "menu_order": p.get("order", 0),
            "elements": elements, "content": p.get("content", ""), "faq": ctx.faq,
            "seo": p.get("seo", {}), "image": media.get(p.get("featured_image") or "", {}).get("id"),
            "noindex": bool(p.get("noindex")), "legal": p.get("legal", ""),
        })
    for x in payload:
        x["phash"] = hashlib.sha1(json.dumps(x, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    send = [x for x in payload if state["pages"].get(x["key"] or "__home") != x["phash"]]   # wp_lib stores home as "__home"
    if len(send) < len(payload):
        log.append(f"pages: {len(payload) - len(send)} unchanged, skipped")
    for batch in chunks(send, 1 if remote else len(send) or 1) if send else []:   # parents first, so children find them
        log.append(run_php(site, "pages", {"pages": batch, "all_keys": [x["key"] for x in payload]}).strip())

    # 3b. header + footer as Elementor templates (Theme Builder header/footer where Elementor Pro runs)
    tctx = Ctx("__tpl", media, data)
    svc = [p for p in data.get("pages", []) if p.get("type") == "service"]
    sample = next((s.get("image") for p in svc for s in p.get("sections", []) if s.get("type") == "hero" and s.get("image")), None)
    tpls = {"header": header_template(tctx), "footer": footer_template(tctx), "name": data["business"]["name"]}
    if use_tpl and svc:
        tpls["service"] = service_template(Ctx("__tpl_service", media, data), sample)
        tpls["service_keys"] = [p["key"] for p in svc]
    if use_tpl and data.get("posts"):
        tpls["post"] = post_template(Ctx("__tpl_post", media, data), data["posts"][0].get("image"))
    log.append(run_php(site, "templates", tpls))

    # 4. blog posts
    posts = []
    for po in data.get("posts", []):
        posts.append({**po, "image": media.get(po.get("image") or "", {}).get("id"),
                      "related": po.get("related_page")})
    if posts:
        log.append(run_php(site, "posts", {"posts": posts, "categories": data.get("categories", [])}))

    # 5. menus, front page, SEO settings, Elementor kit, accessibility
    log.append(run_php(site, "finish", {
        "nav": data.get("nav", []), "footer_nav": data.get("footer_nav", []),
        "logo": media.get("__logo", {}).get("id"),
        "favicon": media.get("__favicon", {}).get("id"),
        "og_image": media.get(data.get("og_image") or "__logo", {}).get("id"),
        "business": data["business"], "design": data.get("design", {}),
        "blog_public": data.get("site", {}).get("index", False),
    }))
    # Zap standard: the accessibility toolbar button on every page. Ally 4 hides its new widget until the site is
    # connected to an Ally account; a site that is not connected runs Ally's classic toolbar instead (its "revert").
    log.append("a11y: " + site.eval_php(
        "if (!defined('EA11Y_VERSION') && !class_exists('\\EA11Y\\Plugin')) { echo 'Ally not active'; return; }"
        "$c = class_exists('\\EA11Y\\Modules\\Connect\\Module') && \\EA11Y\\Modules\\Connect\\Module::is_connected();"
        "if ($c) { echo 'Ally connected: widget'; return; }"
        "update_option('ea11y_reverted', true); delete_option('ea11y_upgraded');"
        "if (!get_option('pojo_a11y_customizer_options')) update_option('pojo_a11y_customizer_options', ['a11y_toolbar_enable' => 'enable']);"
        "echo 'classic toolbar';").strip().splitlines()[-1])
    site.wp("rewrite", "flush", check=False)
    # Yoast 2x serves meta from its indexables table, not from the options we just wrote.
    site.wp("yoast", "index", "--reindex", "--skip-confirmation", check=False)
    site.wp("elementor", "flush-css", check=False)
    site.wp("cache", "flush", check=False)
    (site.dir / "build.log").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(l for l in log if l))
    return data

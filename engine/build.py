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
from sections import Ctx, render_page
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
    code = (f"require {json.dumps(str(PHP_LIB))};\n"
            f"zs_task_{task}(json_decode(file_get_contents({json.dumps(str(f))}), true));\n")
    try:
        return site.eval_php(code)
    finally:
        if not os.environ.get("ZS_KEEP_PAYLOADS"):
            f.unlink(missing_ok=True)


def build(site, only=None):
    site_dir = site.src
    data = load_site(site_dir)
    problems = validate(data, site_dir)
    errors = [p for p in problems if p.startswith("ERROR")]
    for p in problems:
        print(p)
    if errors:
        raise SystemExit(f"site.json has {len(errors)} error(s); fix them and build again.")

    # Zap's per-client privacy PDF often arrives late. Until then: a noindexed placeholder page,
    # never a dead or '#' link (the form consent and the footer both point at it).
    std = data.setdefault("standards", {})
    if not std.get("privacy_url"):
        b = data["business"]
        data["pages"].append({
            "key": "מדיניות-פרטיות", "type": "privacy", "title": "מדיניות פרטיות", "noindex": True,
            "seo": {"title": f"מדיניות פרטיות | {b['name']}",
                    "description": f"מדיניות הפרטיות של {b['name']}: איך נשמר ומשמש המידע שנמסר באתר."},
            "content": f"<p>מדיניות הפרטיות של {b['name']} תפורסם בעמוד זה. לכל שאלה בנושא פרטיות ושימוש במידע "
                       f"שנמסר באתר אפשר לפנות אלינו בטלפון {b.get('phone_display', '')}.</p>",
        })
        std["privacy_url"] = "/מדיניות-פרטיות/"
        data["_paths"]["מדיניות-פרטיות"] = "/מדיניות-פרטיות/"

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
    prepared = []
    for key, im in images.items():
        src = site_dir / im["src"]
        if not src.exists():
            raise SystemExit(f"image '{key}': file not found: {src}")
        out_file, w, h = prepare_image(src, site.dir / "_media", keep_format=im.get("keep_format", False),
                                       max_width=im.get("max_width", 1600))
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
    media = json.loads(run_php(site, "media", {"items": prepared}).splitlines()[-1])
    log.append(f"media: {len(media)} items")
    if "__logo_light" in media:
        run_php(site, "set_option", {"key": "logo_light_id", "value": media["__logo_light"]["id"]})

    # 3. pages (parents first so children can attach)
    pages = sorted(data.get("pages", []), key=lambda p: p["key"].count("/"))
    payload = []
    for p in pages:
        ctx = Ctx(p["key"], media, data)
        elements = render_page(ctx, p.get("sections", [])) if p.get("sections") else None
        if p.get("sections") and ctx.h1_count != 1:
            raise SystemExit(f"page '{p['key'] or 'home'}' renders {ctx.h1_count} H1s (must be exactly 1)")
        parent = p["key"].rsplit("/", 1)[0] if "/" in p["key"] else None
        payload.append({
            "key": p["key"], "slug": p["key"].rsplit("/", 1)[-1] if p["key"] else "home",
            "parent": parent, "title": p["title"], "type": p.get("type", "page"),
            "excerpt": p.get("excerpt", ""), "menu_order": p.get("order", 0),
            "elements": elements, "content": p.get("content", ""), "faq": ctx.faq,
            "seo": p.get("seo", {}), "image": media.get(p.get("featured_image") or "", {}).get("id"),
            "noindex": bool(p.get("noindex")),
        })
    log.append(run_php(site, "pages", {"pages": payload}))

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
        "og_image": media.get(data.get("og_image") or "__logo", {}).get("id"),
        "business": data["business"], "design": data.get("design", {}),
        "blog_public": data.get("site", {}).get("index", False),
    }))
    site.wp("rewrite", "flush", check=False)
    # Yoast 2x serves meta from its indexables table, not from the options we just wrote.
    site.wp("yoast", "index", "--reindex", "--skip-confirmation", check=False)
    site.wp("elementor", "flush-css", check=False)
    site.wp("cache", "flush", check=False)
    (site.dir / "build.log").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(l for l in log if l))
    return data

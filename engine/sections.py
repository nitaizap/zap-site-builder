"""Section library: site.json section dicts -> Elementor classic (container + widget) JSON.

Rules that keep this robust:
  * Markup is fixed per section type; ALL visual styling lives in the theme CSS (zs-* classes).
    Elementor element settings carry content and semantics only, never colours or sizes.
  * Every element id is derived from the page key + position, so rebuilds are stable.
  * Only free, classic widgets: heading, text-editor, image, button, accordion, shortcode, html, video.
"""
import hashlib
import html
import re

from env import WP_SRC
from icons import fa_icon, icon_svg

VEH_DIR = WP_SRC / "theme" / "zap-base" / "assets" / "vehicles"


def vehicle_svg(kind):
    """Illustrated vehicle (theme asset, brand colours via CSS vars); falls back to the line icon."""
    f = VEH_DIR / f"{kind}.svg"
    if not f.exists():
        return icon_svg(kind)
    return re.sub(r">\s+<", "><", f.read_text(encoding="utf-8").strip())


class Ctx:
    """Per-page render context."""

    def __init__(self, page_key, media, site):
        self.page_key = page_key
        self.media = media          # image key -> {"id": int, "url": str, "alt": str}
        self.site = site
        self.n = 0
        self.faq = []               # collected for FAQPage schema (same data the page shows)
        self.h1_count = 0

    def uid(self):
        self.n += 1
        return hashlib.md5(f"{self.page_key}:{self.n}".encode()).hexdigest()[:7]

    def img(self, key):
        if not key:
            return None
        if key not in self.media:
            raise ValueError(f"image '{key}' is not defined in site.json images (page {self.page_key})")
        return self.media[key]

    def href(self, h):
        """'page:services/plumbing' -> real path; '#leave-details', 'tel:', https:// pass through."""
        if not h:
            return ""
        if h.startswith("page:"):
            key, _, frag = h[5:].partition("#")
            path = self.site["_paths"].get(key, "/" + key.strip("/") + "/")
            return path + ("#" + frag if frag else "")
        if h.startswith("post:"):
            return self.site["_post_paths"].get(h[5:], "/")
        if h == "tel":
            return "tel:" + self.site["business"].get("phone_e164", "")
        if h == "whatsapp":
            n = re.sub(r"\D", "", self.site["business"].get("whatsapp_e164", ""))
            return f"https://wa.me/{n}"
        return h


# ---------- element primitives ----------

def C(ctx, classes="", children=(), tag="div", inner=True, boxed=False, **settings):
    s = {"content_width": "boxed" if boxed else "full", "css_classes": classes.strip(), "html_tag": tag}
    s.update(settings)
    return {"id": ctx.uid(), "elType": "container", "isInner": inner, "settings": s,
            "elements": [c for c in children if c]}


def W(ctx, wtype, settings, classes=""):
    s = dict(settings)
    if classes:
        s["_css_classes"] = classes
    return {"id": ctx.uid(), "elType": "widget", "widgetType": wtype, "settings": s, "elements": []}


def heading(ctx, text, tag="h2", classes="", link=None, raw=False):
    if not text:
        return None
    if tag == "h1":
        ctx.h1_count += 1
    s = {"title": text if raw else rich(text), "header_size": tag}
    if link:
        s["link"] = {"url": ctx.href(link), "is_external": "", "nofollow": ""}
    return W(ctx, "heading", s, classes)


def rich(t):
    """Headline markup: *word* = accent colour, a final '.' = accent dot, a newline = a line break."""
    t = html.escape(str(t), quote=False)
    t = re.sub(r"\*(.+?)\*", r'<span class="zs-hl">\1</span>', t)
    t = t.replace(chr(10), '<br class="zs-br">')
    return keep_together(t)


def keep_together(t):
    """Numbers never wrap away from their word: "מספר 1", "1.5 ק״ג", "30 שנה" (Zap QA: "המקצוען מספר / 1")."""
    return re.sub(r"(?<=\S) (?=\d)|(?<=\d) (?=[^\s<\d])", "\u00a0", t)


def text(ctx, body, classes=""):
    if not body:
        return None
    if not re.search(r"<(p|ul|ol|h[2-6]|table|blockquote|div)\b", body):
        body = "".join(f"<p>{html.escape(p.strip(), quote=False)}</p>" for p in body.split("\n\n") if p.strip())
    return W(ctx, "text-editor", {"editor": body}, classes)


def button(ctx, b, kind="primary"):
    if not b or not b.get("label"):
        return None
    href = ctx.href(b.get("href", ""))
    s = {"text": b["label"], "link": {"url": href, "is_external": "on" if href.startswith("http") else "", "nofollow": ""}}
    if b.get("icon"):
        pass  # icons on buttons come from CSS (.zs-b-phone) to avoid loading icon fonts
    k = b.get("kind", kind)
    if href.startswith("tel:"):
        k += " zs-b-tel"
    if "wa.me" in href:
        k += " zs-b-wa"
    return W(ctx, "button", s, f"zs-b zs-b-{k}")


def has_form(ctx):
    """No leads e-mail in the brief -> calls-only site: no form anywhere, call/WhatsApp buttons instead."""
    return bool(ctx.site["business"].get("email_leads"))


def call_buttons(ctx):
    b = ctx.site["business"]
    return buttons(ctx, {"label": b.get("phone_display", ""), "href": "tel"},
                   {"label": "וואטסאפ", "href": "whatsapp"} if b.get("whatsapp_e164") else None)


def lead_cta(ctx, s):
    """The section's own buttons, or the default 'leave details' pair; calls-only sites get call buttons."""
    if s.get("cta") or has_form(ctx):
        return buttons(ctx, s.get("cta", {"label": "השאירו פרטים", "href": "#leave-details"}),
                       s.get("cta2", {"label": ctx.site["business"].get("phone_display", ""), "href": "tel"}))
    return call_buttons(ctx)


def buttons(ctx, *bs):
    items = [button(ctx, b, "primary" if i == 0 else "ghost") for i, b in enumerate(bs) if b]
    items = [i for i in items if i]
    return C(ctx, "zs-btns", items) if items else None


def image(ctx, key, classes="", size="large", eager=False, lightbox=False):
    m = ctx.img(key)
    if not m:
        return None
    s = {"image": {"url": m["url"], "id": m["id"], "alt": m.get("alt", ""), "source": "library"},
         "image_size": size}
    if lightbox:    # gallery photos open full size in Elementor's lightbox (Zap QA), one slideshow per section
        s.update({"link_to": "file", "open_lightbox": "yes"})
    return W(ctx, "image", s, classes + (" zs-eager" if eager else ""))


def checks(items):
    if not items:
        return ""
    return '<ul class="zs-checks">' + "".join(f"<li>{html.escape(i, quote=False)}</li>" for i in items) + "</ul>"


def section(ctx, s, classes, children):
    bg = s.get("bg")
    cls = f"zs-sec {classes} " + (f"zs-bg-{bg}" if bg else "")
    if s.get("variant"):
        cls += f" zs-v-{s['variant']}"
    if s.get("anchor"):
        cls += f" zs-anchor-{s['anchor']}"
    el = C(ctx, cls, children, tag="section", inner=False, boxed=True)
    if s.get("anchor"):
        el["settings"]["_element_id"] = s["anchor"]
    return el


def sec_head(ctx, s, tag="h2"):
    """Section header. With a title and an intro it is asymmetric by default (big title on one side,
    the intro on the other) - `head: "stack"` keeps them stacked."""
    eb = heading(ctx, s.get("eyebrow"), "p", "zs-eyebrow")
    ti = heading(ctx, s.get("title"), tag, "zs-sec__title")
    it = text(ctx, s.get("intro"), "zs-sec__intro")
    if not (eb or ti or it):
        return []
    split = bool(ti and it) and s.get("head", "split") == "split"
    return [C(ctx, "zs-head" + (" zs-head--split" if split else ""), [C(ctx, "zs-head__main", [eb, ti]), it])]


# ---------- sections ----------

def _h1_markup(t, brand=""):
    """Two spans, the brand on its own line: 'keyword\nbrand', an H1 ending with the brand name, or legacy
    'keyword — brand'. No dash and no comma are rendered: a plain space separates them (Zap QA:
    \"צור קשר עם, X\")."""
    a = b = ""
    if "\n" in t:
        a, _, b = t.partition("\n")
    elif brand and t.endswith(brand) and len(t) > len(brand) + 2:
        a, b = t[:-len(brand)].rstrip(" ,|:\u2014\u2013-"), brand
    elif " \u2014 " in t:
        a, _, b = t.partition(" \u2014 ")
    if not b:
        return html.escape(t, quote=False)
    return (f'<span class="zs-h1__k">{html.escape(a, quote=False)}</span>'
            f'<span class="zs-h1__sep"> </span><span class="zs-h1__b">{html.escape(b, quote=False)}</span>')


def hero(ctx, s):
    """One markup, three looks: the layout comes from the design direction (body.zs-hv-*)."""
    is_home = ctx.page_key == ""
    logo = None
    if s.get("logo"):      # the brand's logo above the H1 (cover heroes: restaurants, venues)
        lk = "__logo_light" if "__logo_light" in ctx.media else "__logo"
        chip = " zs-hero__logo--chip" if lk == "__logo" else ""   # no light logo -> it sits on a white chip
        logo = image(ctx, lk, "zs-hero__logo" + chip, "medium", eager=True) if lk in ctx.media else None
    txt = C(ctx, "zs-hero__text", [
        logo,
        heading(ctx, s.get("eyebrow"), "p", "zs-eyebrow"),
        (heading(ctx, s["title"], "h1", "zs-hero__title") if ("*" in s["title"] or "\n" in s["title"])
         else heading(ctx, _h1_markup(s["title"], ctx.site["business"]["name"]), "h1", "zs-hero__title", raw=True)),
        text(ctx, s.get("lead"), "zs-hero__lead"),
        buttons(ctx, s.get("cta"), s.get("cta2")),
        text(ctx, checks(s.get("points", [])), "zs-hero__points") if s.get("points") else None,
    ])
    vid = None
    if s.get("video"):
        v = ctx.img(s["video"])        # videos share the media map
        vid = W(ctx, "html", {"html": f'<video class="zs-hero__video" data-src="{v["url"]}" muted loop playsinline '
                                       f'preload="none" aria-hidden="true" tabindex="-1"></video>'}, "zs-hero__vid")
    # `images: [k1, k2, k3]` -> a crossfading slider (each slide is a normal image widget, swappable in Elementor);
    # the first slide doubles as the poster/LCP image. `image` alone = one still photo.
    keys = s.get("images") or ([s["image"]] if s.get("image") else [])
    slides = [image(ctx, k, "zs-hero__img" + (" zs-hero__slide" if len(keys) > 1 else ""), "full", eager=(i == 0))
              for i, k in enumerate(keys)]
    iv = max(2, min(10, int(s.get("interval", 4)))) if len(keys) > 1 else 0   # seconds per photo
    media = C(ctx, "zs-hero__media" + (f" zs-hero__slider zs-int-{iv}" if len(keys) > 1 else ""), [*slides, vid]) if keys else None
    # `ride: scooter` -> an illustrated vehicle drives along the hero's bottom edge (decorative); with a hero
    # video it only shows where the video does not play (phones), so the two never compete
    ride = None
    kind = s.get("ride", (ctx.site.get("design") or {}).get("ride"))   # design.ride = on every page hero
    if kind:
        ride = W(ctx, "html", {"html": f'<div class="zs-ride" aria-hidden="true"><span class="zs-ride__v">{vehicle_svg(kind)}</span></div>'},
                 "zs-hero__ride")
    # `form: true` -> a lead-form card overlapping the hero's bottom edge (Zap portfolio: most legal/medical ProX
    # sites). Same short form as the leadbar; phones keep the hero buttons and the footer form instead
    fcard = None
    if s.get("form") and has_form(ctx):
        ft = s["form"] if isinstance(s["form"], str) else (ctx.site.get("form") or {}).get("title", "השאירו פרטים ונחזור אליכם")
        fcard = C(ctx, "zs-hero__form", [heading(ctx, ft, "p", "zs-hero__form-title"),
                                         W(ctx, "shortcode", {"shortcode": '[zap_form id="hero" message="no" email="yes"]'})])
    kind = "zs-hero--home" if is_home else "zs-hero--page"
    vidc = " zs-hero--vid" if vid else ""
    vidc += " zs-hero--form" if fcard else ""
    slc = " zs-hero--slides zs-pausable" if len(keys) > 1 else ""
    return section(ctx, s, f"zs-hero {kind} {'zs-hero--img' if media else 'zs-hero--noimg'}{vidc}{slc}", [garland(ctx, s), txt, media, ride, fcard])


def trust(ctx, s):
    lis = "".join(f'<li><strong>{html.escape(i["value"])}</strong><span>{html.escape(i.get("label", ""))}</span></li>'
                  for i in s["items"])
    style = s.get("style", "band")          # band: full-width stat bar with big numerals · card: floating card
    return section(ctx, s, f"zs-trust zs-trust--{style}", [text(ctx, f'<ul class="zs-trust__list">{lis}</ul>')])


def cards(ctx, s):
    n = s.get("columns", 3 if len(s["items"]) % 3 == 0 or len(s["items"]) > 4 else 2 if len(s["items"]) in (2, 4) else 3)
    items = []
    for it in s["items"]:
        items.append(C(ctx, "zs-card" + (" zs-card--img" if it.get("image") else ""), [
            image(ctx, it.get("image"), "zs-card__img", "zs-card"),
            C(ctx, "zs-card__body", [
                W(ctx, "icon", {"selected_icon": fa_icon(it["icon"])}, "zs-card__icon") if it.get("icon") and not it.get("image") else None,
                heading(ctx, it["title"], s.get("item_tag", "h3"), "zs-card__title", link=it.get("href")),
                heading(ctx, it.get("price"), "p", "zs-card__price"),
                text(ctx, it.get("text"), "zs-card__text"),
                text(ctx, '<ul class="zs-card__meta">' + "".join(f"<li>{html.escape(m, quote=False)}</li>" for m in it["meta"]) + "</ul>",
                     "zs-card__metaw") if it.get("meta") else None,
                C(ctx, "zs-card__links", [button(ctx, l, "ghost") for l in it["links"]]) if it.get("links") else None,   # branches: book / order / menu
            ]),
        ]))
    lay = f" zs-cards--{s['layout']}" if s.get("layout") in ("bento", "rows") else ""
    style = s.get("style") or ("overlay" if not lay and s.get("variant") != "framed" and all(i.get("image") for i in s["items"]) else "classic")   # framed = caption below the photo
    linked = " zs-cards--linked" if any(i.get("href") for i in s["items"]) else ""
    return section(ctx, s, f"zs-cards zs-cards--{style}{lay}{linked}", [
        *sec_head(ctx, s),
        C(ctx, f"zs-grid zs-grid--{n}", items),
        buttons(ctx, s.get("more")),
    ])


def features(ctx, s):
    n = s.get("columns", 4 if len(s["items"]) % 4 == 0 else 3)
    items = [C(ctx, "zs-feature", [
        W(ctx, "icon", {"selected_icon": fa_icon(it.get("icon", "check"))}, "zs-feature__icon"),
        heading(ctx, it["title"], "p", "zs-feature__title"),   # advantages titles are not headings (Zap QA: no H3 in יתרונות)
        text(ctx, it.get("text"), "zs-feature__text"),
    ]) for it in s["items"]]
    if s.get("variant") == "aside":
        # "why us": the items stacked beside a framed photo (pool: template 1)
        media = C(ctx, "zs-features__media", [image(ctx, s.get("image"), "zs-features__img", "large")])
        body = C(ctx, "zs-features__body", [*sec_head(ctx, {**s, "head": "stack"}), C(ctx, "zs-features__list", items),
                                            buttons(ctx, s.get("cta"))])
        return section(ctx, s, "zs-features", [C(ctx, "zs-features__wrap", [body, media])])
    return section(ctx, s, "zs-features", [*sec_head(ctx, s), C(ctx, f"zs-grid zs-grid--{n}", items), buttons(ctx, s.get("cta"))])


def steps(ctx, s):
    items = [C(ctx, "zs-step", [heading(ctx, it["title"], "h3", "zs-step__title"), text(ctx, it.get("text"), "zs-step__text")])
             for it in s["items"]]
    return section(ctx, s, "zs-steps", [*sec_head(ctx, s), C(ctx, f"zs-steps__list zs-grid zs-grid--{min(len(items), 4)}", items), buttons(ctx, s.get("cta"))])


def split(ctx, s):
    body = (s.get("text") or "") + checks(s.get("points", []))
    txt = C(ctx, "zs-split__text", [heading(ctx, s.get("eyebrow"), "p", "zs-eyebrow"),
                                    heading(ctx, s["title"], "h2", "zs-sec__title"),
                                    text(ctx, body), buttons(ctx, s.get("cta"), s.get("cta2"))])
    badge = None
    if s.get("badge"):
        bd = s["badge"]
        badge = C(ctx, "zs-badge-w zs-badge", [heading(ctx, bd.get("title", ""), "p", "zs-badge__value", raw=False),
                                               text(ctx, bd.get("text", ""), "zs-badge__label")])
    shape = s.get("image_shape", "")
    media = C(ctx, f"zs-split__media{' zs-shape-' + shape if shape else ''}",
              [image(ctx, s.get("image"), "zs-split__img", "large"),
               image(ctx, s.get("image2"), "zs-split__img2", "large") if s.get("variant") == "duo" else None,
               badge]) if s.get("image") else None
    rev = " zs-split--rev" if s.get("image_side") == "end" else ""
    return section(ctx, s, f"zs-split{rev}{'' if media else ' zs-split--noimg'}", [txt, media])


def prose(ctx, s):
    """Long-form body. Split on h2/h3 so every heading is its own (editable) heading widget."""
    parts = re.split(r"(<h[23][^>]*>.*?</h[23]>)", s["html"], flags=re.S)
    kids = [heading(ctx, s.get("title"), "h2", "zs-sec__title")] if s.get("title") else []
    for p in parts:
        m = re.match(r"<(h[23])[^>]*>(.*?)</h[23]>", p, flags=re.S)
        if m:
            kids.append(heading(ctx, re.sub(r"<[^>]+>", "", m.group(2)).strip(), m.group(1), "zs-prose__h"))
        elif p.strip():
            kids.append(text(ctx, p.strip(), "zs-prose__t"))
    return section(ctx, s, "zs-prose-sec", [C(ctx, "zs-prose", kids)])


def faq(ctx, s):
    tabs = []
    for i, it in enumerate(s["items"]):
        ctx.faq.append({"q": it["q"], "a": it["a"]})
        a = it["a"] if it["a"].lstrip().startswith("<") else f"<p>{html.escape(it['a'], quote=False)}</p>"
        tabs.append({"_id": hashlib.md5(f"{ctx.page_key}:faq:{i}".encode()).hexdigest()[:7],
                     "tab_title": it["q"], "tab_content": a})
    lst = W(ctx, "toggle", {"tabs": tabs, "title_html_tag": "h3", "faq_schema": ""}, "zs-faq__list")
    if s.get("variant") == "aside":     # questions beside a tall photo (template 4)
        return section(ctx, s, "zs-faq", [C(ctx, "zs-faq__wrap", [C(ctx, "zs-faq__body", [*sec_head(ctx, {**s, "head": "stack"}), lst]),
                                                                   C(ctx, "zs-faq__media", [image(ctx, s.get("image"), "zs-faq__img", "large")])])])
    return section(ctx, s, "zs-faq", [*sec_head(ctx, s), lst])


def cta(ctx, s):
    if s.get("variant") == "photo":     # half photo, half brand panel with the action (basic-site references, e.g. "להזמנת שולחן")
        panel = C(ctx, "zs-cta__panel", [heading(ctx, s.get("eyebrow"), "p", "zs-eyebrow"),
                                         heading(ctx, s["title"], "h2", "zs-sec__title"), text(ctx, s.get("text")),
                                         lead_cta(ctx, s)])
        return section(ctx, {**s, "bg": s.get("bg")}, "zs-ctaph",
                       [C(ctx, "zs-ctaph__media", [image(ctx, s.get("image"), "zs-ctaph__img", "large")]), panel])
    return section(ctx, {**s, "bg": s.get("bg", "primary")}, "zs-cta", [
        garland(ctx, s),
        C(ctx, "zs-cta__text", [heading(ctx, s.get("eyebrow"), "p", "zs-eyebrow"),
                                heading(ctx, s["title"], "h2", "zs-sec__title"), text(ctx, s.get("text"))]),
        lead_cta(ctx, s),
    ])


def gallery(ctx, s):
    keys = s["images"][:3] if s.get("variant") == "strip" else s["images"]   # strip: a teaser row, `more` leads on
    # "large" (1024 px), not the card crop: sharp on 2x phone screens (Zap QA)
    imgs = [image(ctx, k, "zs-gallery__img", "large", lightbox=True) for k in keys]
    return section(ctx, s, "zs-gallery", [*sec_head(ctx, s), C(ctx, f"zs-grid zs-grid--{s.get('columns', 3)}", imgs),
                                          buttons(ctx, s.get("more"))])


def logos(ctx, s):
    imgs = [image(ctx, k, "zs-logos__img", "medium") for k in s["images"]]
    if s.get("variant") == "band":      # dark band: title on one side, logo chips on the other (template 6)
        return section(ctx, {**s, "bg": s.get("bg") or "dark"}, "zs-logos", [C(ctx, "zs-logos__band", [
            C(ctx, "zs-logos__head", [heading(ctx, s.get("title"), "h2", "zs-sec__title"), text(ctx, s.get("intro"))]),
            C(ctx, "zs-logos__row", imgs)])])
    return section(ctx, s, "zs-logos", [*sec_head(ctx, s), C(ctx, "zs-logos__row", imgs)])


def posts(ctx, s):
    sc = f'[zap_recent_posts count="{int(s.get("count", 3))}"' + (f' category="{s["category"]}"' if s.get("category") else "") + "]"
    return section(ctx, s, "zs-posts", [*sec_head(ctx, s), W(ctx, "shortcode", {"shortcode": sc}), buttons(ctx, s.get("more"))])


def contact(ctx, s):
    left = C(ctx, "zs-contact__info", [heading(ctx, s.get("title"), "p", "zs-sec__title zs-contact__title"), text(ctx, s.get("text")),
                                       W(ctx, "shortcode", {"shortcode": "[zap_nap]"}),
                                       W(ctx, "shortcode", {"shortcode": '[zap_form id="contact"]'}) if has_form(ctx) else call_buttons(ctx)])   # same fields as the footer form (Zap QA)
    if s.get("variant") == "photo":     # form beside a full-height photo (pool: template 1)
        right = C(ctx, "zs-contact__photo", [image(ctx, s.get("image"), "zs-contact__img", "large")])
    else:
        right = C(ctx, "zs-contact__map", [W(ctx, "shortcode", {"shortcode": "[zap_map]"})]) if s.get("map", True) else None
    return section(ctx, s, "zs-contact", [left, right])


def tiles(ctx, s):
    """Edge-to-edge checkerboard: each item is a photo half and a colour half, alternating sides row by row
    (the Zap basic restaurant references). Text halves are native widgets; grounds cycle dark / accent."""
    rows = []
    for i, it in enumerate(s["items"]):
        panel = C(ctx, "zs-tile__panel", [heading(ctx, it.get("title"), "h3" if s.get("title") else "h2", "zs-tile__title"),
                                          text(ctx, it.get("text"), "zs-tile__text"), buttons(ctx, it.get("cta"))])
        media = C(ctx, "zs-tile__media", [image(ctx, it.get("image"), "zs-tile__img", "large")])
        rows.append(C(ctx, f"zs-tile zs-tile--{'b' if i % 2 else 'a'}", [panel, media]))
    return section(ctx, {**s, "bg": s.get("bg")}, "zs-tiles", [*sec_head(ctx, s), C(ctx, "zs-tiles__list", rows)])


def leadbar(ctx, s):
    """Rounded brand band with a one-row lead form (name, phone, email) mid-page (pool: template 1).
    The site-wide lead band before the footer stays; use this at most once, far from it."""
    fid = s.get("form_id", "leadbar")
    bgimg = image(ctx, s.get("image"), "zs-leadbar__bg", "full") if s.get("variant") == "photo" else None
    return section(ctx, s, "zs-leadbar", [bgimg, C(ctx, "zs-leadbar__box", [
        heading(ctx, s.get("title"), "h2", "zs-sec__title"), text(ctx, s.get("text"), "zs-leadbar__text"),
        W(ctx, "shortcode", {"shortcode": f'[zap_form id="{fid}" message="no" email="yes"]'}) if has_form(ctx) else call_buttons(ctx),
    ])])


def reviews(ctx, s):
    if not ctx.site["business"].get("dpz_customer_id"):
        return None   # no real source -> no reviews block at all
    bgimg = image(ctx, s.get("image"), "zs-reviews__bg", "full") if s.get("variant") == "photo" else None
    return section(ctx, s, "zs-reviews-sec", [bgimg, *sec_head(ctx, s), W(ctx, "shortcode", {"shortcode": "[zap_reviews]"})])


def video(ctx, s):
    return section(ctx, s, "zs-video", [*sec_head(ctx, s), W(ctx, "video", {"youtube_url": s["youtube_url"], "lazy_load": "yes"}, "zs-video__player")])


def quote(ctx, s):
    body = f'<blockquote><p>{html.escape(s["text"], quote=False)}</p>' + (f'<cite>{html.escape(s["by"])}</cite>' if s.get("by") else "") + "</blockquote>"
    return section(ctx, s, "zs-quote", [text(ctx, body)])


def marquee(ctx, s):
    """Big slogan ticker. Decorative (aria-hidden); the same words must also appear as real text elsewhere."""
    items = s.get("items") or []
    one = "".join(f'<span class="zs-mq__i">{html.escape(i, quote=False)}</span><span class="zs-mq__dot"></span>' for i in items)
    track = f'<div class="zs-mq__track">{one * 4}</div>'
    body = f'<div class="zs-mq-wrap zs-pausable"><div class="zs-mq" aria-hidden="true">{track}{track}</div></div>'
    return section(ctx, {**s, "bg": s.get("bg", "accent")}, "zs-marquee", [W(ctx, "html", {"html": body}, "zs-mq__w")])


def road(ctx, s):
    """Decorative street scene: illustrated vehicles drive across (wheels spin, bodies bounce) in front of a
    slowly drifting skyline. CSS only; parked in place under prefers-reduced-motion.
    Optional short `items` labels sit above the lane. Fits delivery, transport, moving, towing clients."""
    kinds = s.get("vehicles") or ["scooter", "van", "truck"]
    n = len(kinds)
    vs = "".join(f'<span class="zs-road__v zs-road__v--{k}" style="--i:{i};--n:{n}">{vehicle_svg(k)}</span>'
                 for i, k in enumerate(kinds))
    labels = "".join(f"<li>{html.escape(i, quote=False)}</li>" for i in s.get("items", []))
    sky = vehicle_svg("skyline") if (VEH_DIR / "skyline.svg").exists() else ""
    body = (f'<ul class="zs-road__labels">{labels}</ul>' if labels else "") + \
           f'<div class="zs-road__scene zs-pausable"><div class="zs-road__sky" aria-hidden="true">{sky}{sky}</div>' \
           f'<div class="zs-road__lane" aria-hidden="true">{vs}</div></div>'
    return section(ctx, s, "zs-road", [*sec_head(ctx, s), W(ctx, "html", {"html": body}, "zs-road__w")])


def route(ctx, s):
    """'How it works' as a delivery route: a scooter rides the track as the visitor scrolls and each stop
    lights up when it is reached. Steps are native containers (icon + heading + text, editable in Elementor);
    only the track is decorative HTML. Without JS or with reduced motion every stop is simply lit."""
    items = s["items"]
    rider = f'<span class="zs-route__rider">{vehicle_svg(s.get("vehicle", "scooter"))}</span>'
    track = W(ctx, "html", {"html": f'<div class="zs-route__track" aria-hidden="true"><span class="zs-route__fill"></span>{rider}</div>'},
              "zs-route__trackw")
    stops = [C(ctx, "zs-route__step", [
        W(ctx, "icon", {"selected_icon": fa_icon(it.get("icon", "check"))}, "zs-route__icon"),
        heading(ctx, it["title"], "h3", "zs-route__title"),
        text(ctx, it.get("text"), "zs-route__text"),
    ]) for it in items]
    lst = C(ctx, f"zs-route__list zs-route__list--{min(max(len(items), 2), 6)}", [track, *stops])
    return section(ctx, s, "zs-route", [*sec_head(ctx, s), lst, buttons(ctx, s.get("cta"))])


LAYER_TH = {"base": 0, "primer": 7, "tar": 15, "mesh": 9, "membrane": 16, "white": 10, "coat": 12, "screed": 20, "tile": 14}


def _layers_svg(items):
    """Roof cross-section (concrete slab + parapet, layers turned up the parapet, flashing on top), drawn to a
    fixed scale so every site gets the same clean technical look. Item `kind` picks the material: base (the
    slab itself: preparation), primer, tar, mesh, membrane, white, coat, screed, tile."""
    X0, YS, X1, YT = 112, 270, 640, 130          # parapet face, slab top, right edge, upturn top
    g, off = [], 0
    n = len(items)
    for i, it in enumerate(items):
        k = it.get("kind", "tar")
        th = LAYER_TH.get(k, 9)
        a, b = off, off + th
        if th:
            pts = f"{X0 + a},{YT} {X0 + b},{YT} {X0 + b},{YS - b} {X1},{YS - b} {X1},{YS - a} {X0 + a},{YS - a}"
            shape = f'<polygon class="zs-lx__m zs-lx--{k}" points="{pts}"/>'
            ty = YS - (a + b) / 2
        else:
            shape, ty = "", YS + 34
        bx = 220 + (370 * i / max(n - 1, 1))
        g.append(f'<g class="zs-lx" data-i="{i}" style="--zs-l:{i}">{shape}'
                 f'<line class="zs-lx__lead" x1="{bx:.0f}" y1="70" x2="{bx:.0f}" y2="{ty:.1f}"/>'
                 f'<circle class="zs-lx__dot" cx="{bx:.0f}" cy="{ty:.1f}" r="3.5"/>'
                 f'<circle class="zs-lx__badge" cx="{bx:.0f}" cy="52" r="19"/>'
                 f'<text class="zs-lx__n" x="{bx:.0f}" y="58" text-anchor="middle">{i + 1:02d}</text></g>')
        off = b
    fl = X0 + off + 10
    return (f'<svg class="zs-layers__svg" viewBox="0 0 640 372" role="img" aria-hidden="true" direction="ltr">'
            '<defs><pattern id="zsHatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line x1="0" y1="0" x2="0" y2="9" class="zs-lx__hl"/></pattern>'
            '<pattern id="zsMesh" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#efe3b4"/><path d="M0 0L6 6M6 0L0 6" class="zs-lx__ml"/></pattern>'
            '<pattern id="zsGrain" width="5" height="5" patternUnits="userSpaceOnUse"><rect width="5" height="5" fill="#59606b"/><circle cx="1.5" cy="1.5" r=".9" class="zs-lx__gr"/>'
            '<circle cx="4" cy="3.6" r=".7" class="zs-lx__gr"/></pattern></defs>'
            f'<rect class="zs-lx__sky" x="0" y="0" width="640" height="{YS}"/>'
            f'<path class="zs-lx__slab" d="M0 {YS}H{X1}V340H0Z"/><path class="zs-lx__slab" d="M48 {YT - 22}H{X0}V{YS}H48Z"/>'
            f'<path class="zs-lx__slab zs-lx__slab--h" d="M0 {YS}H{X1}V340H0Z"/><path class="zs-lx__slab zs-lx__slab--h" d="M48 {YT - 22}H{X0}V{YS}H48Z"/>'
            f'<path class="zs-lx__ceil" d="M0 340H640V356H0Z"/>'
            f'<path class="zs-lx__flash" d="M40 {YT - 26}H{fl}V{YT + 18}"/>'
            + "".join(g) + '</svg>')


def layers(ctx, s):
    """A build-up shown as a technical cross-section of a roof: each item is a material layer (`kind`), turned up
    the parapet, with a numbered leader line; beside it an editable numbered list (title, text, optional `spec`
    such as "1.5 ק״ג למ״ר"). Layers draw in on scroll, then highlight one by one; hovering or tapping a list
    item or a layer highlights the pair. Without JS / under reduced motion everything is shown, static."""
    items = s.get("items") or []
    stack = W(ctx, "html", {"html": f'<div class="zs-layers__draw">{_layers_svg(items)}</div>'}, "zs-layers__stack")
    rows = [C(ctx, f"zs-layers__item zs-li-{i}", [
        heading(ctx, f"{i + 1:02d}", "p", "zs-layers__num"),
        heading(ctx, it["title"], "h3", "zs-layers__title"),
        text(ctx, it.get("text"), "zs-layers__text"),
        heading(ctx, it.get("spec"), "p", "zs-layers__spec"),
    ]) for i, it in enumerate(items)]
    return section(ctx, s, "zs-layers", [*sec_head(ctx, s), C(ctx, "zs-layers__grid", [stack, C(ctx, "zs-layers__list", rows)]),
                                         buttons(ctx, s.get("cta"))])


def garland(ctx, s):
    """Decorative string of festoon bulbs hanging in two swags across the top of a section (hero, cta).
    The bulbs twinkle a few times and the string sways, then both settle (no endless motion); aria-hidden.
    On with `garland: true` on the section, or `design.garland: true` for every hero and cta."""
    if not (s.get("garland", (ctx.site.get("design") or {}).get("garland"))):
        return None
    n, bulbs = 17, []
    for i in range(n):
        x = i / (n - 1) * 100
        u = (x % 50) / 50
        y = 112 * u * (1 - u) / 40 * 100           # on the quadratic swag of the wire below (viewBox 100x40)
        bulbs.append(f'<span class="zs-garland__b" style="--x:{x:.2f}%;--y:{y:.1f}%;--i:{i}"></span>')
    wire = ('<svg class="zs-garland__wire" viewBox="0 0 100 40" preserveAspectRatio="none" aria-hidden="true">'
            '<path d="M0,0 Q25,56 50,0 Q75,56 100,0" vector-effect="non-scaling-stroke"/></svg>')
    return W(ctx, "html", {"html": f'<div class="zs-garland" aria-hidden="true">{wire}{"".join(bulbs)}</div>'}, "zs-garland__w")


def carousel(ctx, s):
    """Photo carousel: a swipeable, snapping strip of photos (native image widgets, editable), each with an
    optional caption. With motion it advances on its own (pause button, stops on hover/focus/offscreen),
    the centred slide grows; arrows and swipe always work. `items`: image keys or {image, caption}."""
    slides = []
    for i, it in enumerate(s["items"]):
        it = it if isinstance(it, dict) else {"image": it}
        slides.append(C(ctx, "zs-car__slide", [image(ctx, it["image"], "zs-car__img", "large"),
                                               heading(ctx, it.get("caption"), "p", "zs-car__cap")]))
    nav = W(ctx, "html", {"html": '<div class="zs-car__nav"><button type="button" class="zs-car__btn zs-car__prev" aria-label="התמונה הקודמת">'
                                  '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>'
                                  '<span class="zs-car__count" aria-hidden="true"></span>'
                                  '<button type="button" class="zs-car__btn zs-car__next" aria-label="התמונה הבאה">'
                                  '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button></div>'}, "zs-car__navw")
    iv = min(max(int(s.get("interval", 4)), 2), 10)
    return section(ctx, s, f"zs-carousel zs-pausable zs-int-{iv}", [*sec_head(ctx, s), C(ctx, "zs-car__track", slides), nav])


def pricelist(ctx, s):
    """A price list: `items: [{name, price, text}]`, or `groups: [{title, items}]` (a menu with categories).
    Default: two columns of rows with a dotted leader between name and price (menus, notary fees);
    `variant: "tiles"`: one tile per item with the price in a chip (vets, opticians, treatments).
    Prices are the client's own published prices only; `price` may be empty (a menu without prices)."""
    groups = s.get("groups") or [{"items": s.get("items", [])}]
    kids = []
    for g in groups:
        rows = [C(ctx, "zs-price", [C(ctx, "zs-price__row", [heading(ctx, it["name"], "h3", "zs-price__name"),
                                                             heading(ctx, it.get("price"), "p", "zs-price__val")]),
                                    text(ctx, it.get("text"), "zs-price__text")]) for it in g["items"]]
        kids.append(C(ctx, "zs-prices__group", [heading(ctx, g.get("title"), "h3" if s.get("title") else "h2", "zs-prices__gt"),
                                                C(ctx, "zs-prices__list", rows)]))
    return section(ctx, s, "zs-prices", [*sec_head(ctx, s), C(ctx, "zs-prices__groups", kids), text(ctx, s.get("note"), "zs-prices__note"),
                                         buttons(ctx, s.get("cta"))])


def facts(ctx, s):
    """Intro text beside a fact card of label: value rows ("יחידות: 2", "אורחים: עד 6", "שטח: 120 מ״ר"):
    zimmers and suites, venues, B2B specs (Zap portfolio: Tiffany zimmers). `card_title` heads the card."""
    rows = "".join(f'<li><span class="zs-facts__k">{html.escape(it["label"], quote=False)}</span>'
                   f'<strong class="zs-facts__v">{html.escape(str(it["value"]), quote=False)}</strong></li>' for it in s["items"])
    card = C(ctx, "zs-facts__card", [heading(ctx, s.get("card_title"), "p", "zs-facts__title"),
                                     text(ctx, f'<ul class="zs-facts__list">{rows}</ul>', "zs-facts__listw")])
    body = C(ctx, "zs-facts__body", [*sec_head(ctx, {**s, "head": "stack"}), text(ctx, s.get("text")), buttons(ctx, s.get("cta"), s.get("cta2"))])
    return section(ctx, s, "zs-facts", [C(ctx, "zs-facts__wrap", [body, card])])


def team(ctx, s):
    """The people: `items: [{name, role, text, image}]` – partners of a law firm, a clinic's doctors, the vets.
    Round portraits on cards; with one or two people the cards turn into wide bio rows (Zap portfolio: 20, 36).
    Real people only, with their own photos; never AI portraits."""
    items = [C(ctx, "zs-member" + (" zs-member--img" if it.get("image") else ""), [
        image(ctx, it.get("image"), "zs-member__img", "medium"),
        C(ctx, "zs-member__body", [heading(ctx, it["name"], "h3", "zs-member__name"), heading(ctx, it.get("role"), "p", "zs-member__role"),
                                   text(ctx, it.get("text"), "zs-member__text")]),
    ]) for it in s["items"]]
    wide = " zs-team--wide" if len(items) <= 2 or s.get("variant") == "rows" else ""
    return section(ctx, s, f"zs-team{wide}", [*sec_head(ctx, s), C(ctx, f"zs-team__list zs-grid zs-grid--{min(len(items), 4)}", items),
                                              buttons(ctx, s.get("cta"))])


SECTIONS = {f.__name__: f for f in (hero, trust, cards, features, steps, split, prose, faq, cta, gallery,
                                     logos, posts, contact, leadbar, tiles, reviews, video, quote, road, route, marquee, carousel, layers, pricelist, facts, team)}


# The pool: every look a section type can take, set per section with `variant` (see references/pool.md).
# Hero layout, preset, tone and motion are site-wide design levers; these are per section.
VARIANTS = {
    "hero": {"cover", "inset", "curve"},
    "split": {"frame", "overlap", "card", "duo"},
    "cta": {"photo"},
    "cards": {"framed"},
    "features": {"aside", "checks", "rows"},
    "gallery": {"mosaic", "strip", "stagger"},
    "faq": {"outline", "aside", "dark"},
    "steps": {"stack", "cards"},
    "prose": {"band"},
    "reviews": {"photo"},
    "logos": {"band"},
    "contact": {"photo"},
    "leadbar": {"photo"},
    "tiles": set(),
    "pricelist": {"tiles"},
    "facts": set(),
    "team": {"rows"},
}


def render_page(ctx, sections):
    out = []
    plain_i = 0
    prev_bg = None
    for s in sections:
        t = s.get("type")
        if t not in SECTIONS:
            raise ValueError(f"unknown section type '{t}' on page '{ctx.page_key}'. Known: {', '.join(SECTIONS)}")
        if t not in ("hero", "cta", "marquee", "trust", "tiles") and "bg" not in s:
            # quiet rhythm: alternate plain and surface backgrounds after the hero
            s = {**s, "bg": "surface" if plain_i % 2 else None}
            plain_i += 1
        el = SECTIONS[t](ctx, s)
        if el:
            # two neighbours on the same ground read as one band: the second drops most of its top padding
            bg = s.get("bg") if t not in ("hero", "cta", "marquee", "trust", "tiles") else "-" + t
            if out and bg and bg == prev_bg:
                el["settings"]["css_classes"] += " zs-sec--joined"
            prev_bg = bg
            out.append(el)
    return out


# ---------- site templates: header + footer as editable Elementor documents ----------
# Native widgets for everything a client edits (logo, phone button, texts, titles); shortcodes only for the
# parts that are behaviour or Zap standards (menu + burger, contact list, lead form, legal line, Zap logo).

def header_template(ctx):
    d = ctx.site
    b, h = d["business"], d.get("header", {})
    els = []
    if h.get("topbar", True):
        els.append(C(ctx, "zs-topbar", [
            C(ctx, "zs-wrap zs-topbar__in", [
                heading(ctx, h.get("topbar_text") or d.get("site", {}).get("tagline", ""), "p", "zs-topbar__text"),
                W(ctx, "shortcode", {"shortcode": "[zap_topbar_meta]"}, "zs-topbar__meta"),
            ]),
        ], inner=False))
    logo = ctx.media.get("__logo")
    brand = (W(ctx, "image", {"image": {"url": logo["url"], "id": logo["id"], "alt": b["name"], "source": "library"},
                              "image_size": "full", "link_to": "custom",
                              "link": {"url": "/", "is_external": "", "nofollow": ""}}, "zs-brand")
             if logo else heading(ctx, b["name"], "p", "zs-brand zs-brand__name", link="page:"))
    tel = button(ctx, {"label": b.get("phone_display", ""), "href": "tel"}, "primary")
    if tel:
        tel["settings"]["_css_classes"] += " zs-header__cta"
    els.append(C(ctx, "zs-header", [
        C(ctx, "zs-wrap zs-header__in", [brand, W(ctx, "shortcode", {"shortcode": "[zap_nav]"}, "zs-header__nav"), tel]),
    ], tag="header", inner=False))
    return els


def post_template(ctx):
    """Theme Builder 'single-post' template (Elementor Pro): page hero with the post's title as H1 and its byline,
    the featured image, the content, then FAQ / related page / author. Edited in Elementor like any page."""
    hero = C(ctx, "zs-sec zs-hero zs-hero--page zs-hero--noimg zs-post-hero", [
        C(ctx, "zs-hero__text", [
            W(ctx, "shortcode", {"shortcode": "[zap_post_meta]"}, "zs-post__metaw"),
            W(ctx, "shortcode", {"shortcode": "[zap_post_title]"}, "zs-hero__title"),
        ])], tag="section", inner=False, boxed=True)
    body = C(ctx, "zs-sec zs-post-body", [
        C(ctx, "zs-wrap zs-wrap--narrow", [
            W(ctx, "shortcode", {"shortcode": "[zap_post_image]"}, "zs-post__hero"),
            W(ctx, "theme-post-content", {}, "zs-prose"),
            W(ctx, "shortcode", {"shortcode": "[zap_post_extras]"}, "zs-post__extras"),
        ])], tag="section", inner=False, boxed=True)
    return [hero, body]


def archive_template(ctx):
    """Theme Builder 'archive' template (Elementor Pro): the blog page, categories and search. Hero with the
    archive title as H1 and its intro, then the posts as cards."""
    hero = C(ctx, "zs-sec zs-hero zs-hero--page zs-hero--noimg", [
        C(ctx, "zs-hero__text", [
            W(ctx, "shortcode", {"shortcode": "[zap_archive_title]"}, "zs-hero__title"),
            W(ctx, "shortcode", {"shortcode": "[zap_archive_intro]"}, "zs-hero__lead"),
        ])], tag="section", inner=False, boxed=True)
    body = C(ctx, "zs-sec zs-archive-body", [W(ctx, "shortcode", {"shortcode": "[zap_archive_posts]"}, "zs-archive__posts")],
             tag="section", inner=False, boxed=True)
    return [hero, body]


def footer_template_logo_key(ctx):
    return "__logo_light" if "__logo_light" in ctx.media else "__logo"


def footer_logo(ctx):
    """The client's logo in the footer, linking home (Zap QA); a dark logo on a dark footer sits on a white chip."""
    b, k = ctx.site["business"], footer_template_logo_key(ctx)
    lg = ctx.media.get(k)
    if not lg:
        return heading(ctx, b["name"], "p", "zs-footer__name", link="page:")
    chip = " zs-footer__logo--chip" if k == "__logo" else ""
    return W(ctx, "image", {"image": {"url": lg["url"], "id": lg["id"], "alt": b["name"], "source": "library"},
                            "image_size": "full", "link_to": "custom", "link": {"url": "/", "is_external": "", "nofollow": ""}},
             "zs-footer__logo" + chip)


def footer_template(ctx):
    d = ctx.site
    b, f, form = d["business"], d.get("footer", {}), d.get("form", {})
    lead = C(ctx, "zs-leadband", [
        C(ctx, "zs-wrap zs-leadband__in", [
            C(ctx, "zs-leadband__text", [
                heading(ctx, form.get("title", "השאירו פרטים ונחזור אליכם" if has_form(ctx) else "דברו איתנו"), "p", "zs-leadband__title"),   # not an H2: repeats on every page (Zap QA)
                text(ctx, form.get("text", "ממלאים שם וטלפון, ואנחנו חוזרים בהקדם." if has_form(ctx) else "")),
                W(ctx, "shortcode", {"shortcode": "[zap_call_line]"}, "zs-leadband__or") if has_form(ctx) else None,
            ]),
            W(ctx, "shortcode", {"shortcode": '[zap_form id="footer"]'}, "zs-leadband__form") if has_form(ctx) else call_buttons(ctx),
        ]),
    ], tag="section", inner=False)
    lead["settings"]["_element_id"] = "leave-details"
    cols = C(ctx, "zs-wrap zs-footer__grid", [
        C(ctx, "zs-footer__col zs-footer__brand", [
            footer_logo(ctx),
            text(ctx, f.get("about", "")),
        ]),
        C(ctx, "zs-footer__col", [
            heading(ctx, f.get("links_title", "השירותים שלנו"), "p", "zs-footer__title"),
            W(ctx, "shortcode", {"shortcode": '[zap_menu location="footer"]'}),
        ], tag="nav"),
        C(ctx, "zs-footer__col", [
            heading(ctx, "יצירת קשר", "p", "zs-footer__title"),
            W(ctx, "shortcode", {"shortcode": "[zap_footer_contact]"}),
        ]),
    ])
    mark = W(ctx, "html", {"html": f'<div class="zs-footer__mark" aria-hidden="true">{html.escape(b["name"])}</div>'}, "zs-footer__mark-w")
    bar = C(ctx, "zs-footer__bar", [
        C(ctx, "zs-wrap zs-footer__bar-in", [
            W(ctx, "shortcode", {"shortcode": "[zap_copyright]"}),
            W(ctx, "shortcode", {"shortcode": "[zap_legal]"}),
            W(ctx, "shortcode", {"shortcode": "[zap_group_logo]"}),
        ]),
    ])
    foot = C(ctx, "zs-footer", [cols, mark, bar], tag="footer", inner=False)
    return [lead, foot]

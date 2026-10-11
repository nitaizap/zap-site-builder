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
            return self.site["_paths"].get(h[5:], "/" + h[5:].strip("/") + "/")
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
    if t.endswith("."):
        t = t[:-1] + '<span class="zs-dot">.</span>'
    return t


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


def buttons(ctx, *bs):
    items = [button(ctx, b, "primary" if i == 0 else "ghost") for i, b in enumerate(bs) if b]
    items = [i for i in items if i]
    return C(ctx, "zs-btns", items) if items else None


def image(ctx, key, classes="", size="large", eager=False):
    m = ctx.img(key)
    if not m:
        return None
    s = {"image": {"url": m["url"], "id": m["id"], "alt": m.get("alt", ""), "source": "library"},
         "image_size": size}
    return W(ctx, "image", s, classes + (" zs-eager" if eager else ""))


def checks(items):
    if not items:
        return ""
    return '<ul class="zs-checks">' + "".join(f"<li>{html.escape(i, quote=False)}</li>" for i in items) + "</ul>"


def section(ctx, s, classes, children):
    bg = s.get("bg")
    cls = f"zs-sec {classes} " + (f"zs-bg-{bg}" if bg else "")
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

def _h1_markup(t):
    """'keyword — brand' -> two spans so presets can set the brand on its own line/colour. Text is unchanged."""
    a, sep, b = t.partition(" — ")
    if not sep:
        return html.escape(t, quote=False)
    return (f'<span class="zs-h1__k">{html.escape(a, quote=False)}</span>'
            f'<span class="zs-h1__sep"> — </span><span class="zs-h1__b">{html.escape(b, quote=False)}</span>')


def hero(ctx, s):
    """One markup, three looks: the layout comes from the design direction (body.zs-hv-*)."""
    is_home = ctx.page_key == ""
    txt = C(ctx, "zs-hero__text", [
        W(ctx, "shortcode", {"shortcode": "[zap_breadcrumbs]"}, "zs-hero__crumbs") if not is_home else None,
        heading(ctx, s.get("eyebrow"), "p", "zs-eyebrow"),
        (heading(ctx, s["title"], "h1", "zs-hero__title") if ("*" in s["title"] or "\n" in s["title"])
         else heading(ctx, _h1_markup(s["title"]), "h1", "zs-hero__title", raw=True)),
        text(ctx, s.get("lead"), "zs-hero__lead"),
        buttons(ctx, s.get("cta"), s.get("cta2")),
        text(ctx, checks(s.get("points", [])), "zs-hero__points") if s.get("points") else None,
    ])
    vid = None
    if s.get("video"):
        v = ctx.img(s["video"])        # videos share the media map
        vid = W(ctx, "html", {"html": f'<video class="zs-hero__video" data-src="{v["url"]}" muted loop playsinline '
                                       f'preload="none" aria-hidden="true" tabindex="-1"></video>'}, "zs-hero__vid")
    media = C(ctx, "zs-hero__media", [image(ctx, s.get("image"), "zs-hero__img", "full", eager=True), vid]) if s.get("image") else None
    # `ride: scooter` -> an illustrated vehicle drives along the hero's bottom edge (decorative); with a hero
    # video it only shows where the video does not play (phones), so the two never compete
    ride = None
    kind = s.get("ride", (ctx.site.get("design") or {}).get("ride"))   # design.ride = on every page hero
    if kind:
        ride = W(ctx, "html", {"html": f'<div class="zs-ride" aria-hidden="true"><span class="zs-ride__v">{vehicle_svg(kind)}</span></div>'},
                 "zs-hero__ride")
    kind = "zs-hero--home" if is_home else "zs-hero--page"
    vidc = " zs-hero--vid" if vid else ""
    return section(ctx, s, f"zs-hero {kind} {'zs-hero--img' if media else 'zs-hero--noimg'}{vidc}", [txt, media, ride])


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
                text(ctx, it.get("text"), "zs-card__text"),
            ]),
        ]))
    lay = f" zs-cards--{s['layout']}" if s.get("layout") in ("bento", "rows") else ""
    style = s.get("style") or ("overlay" if not lay and all(i.get("image") for i in s["items"]) else "classic")
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
        heading(ctx, it["title"], "h3", "zs-feature__title"),
        text(ctx, it.get("text"), "zs-feature__text"),
    ]) for it in s["items"]]
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
              [image(ctx, s.get("image"), "zs-split__img", "large"), badge]) if s.get("image") else None
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
    return section(ctx, s, "zs-faq", [*sec_head(ctx, s),
                                      W(ctx, "toggle", {"tabs": tabs, "title_html_tag": "h3", "faq_schema": ""}, "zs-faq__list")])


def cta(ctx, s):
    return section(ctx, {**s, "bg": s.get("bg", "primary")}, "zs-cta", [
        C(ctx, "zs-cta__text", [heading(ctx, s.get("eyebrow"), "p", "zs-eyebrow"),
                                heading(ctx, s["title"], "h2", "zs-sec__title"), text(ctx, s.get("text"))]),
        buttons(ctx, s.get("cta", {"label": "השאירו פרטים", "href": "#leave-details"}),
                s.get("cta2", {"label": ctx.site["business"].get("phone_display", ""), "href": "tel"})),
    ])


def gallery(ctx, s):
    imgs = [image(ctx, k, "zs-gallery__img", "zs-card") for k in s["images"]]
    return section(ctx, s, "zs-gallery", [*sec_head(ctx, s), C(ctx, f"zs-grid zs-grid--{s.get('columns', 3)}", imgs)])


def logos(ctx, s):
    imgs = [image(ctx, k, "zs-logos__img", "medium") for k in s["images"]]
    return section(ctx, s, "zs-logos", [*sec_head(ctx, s), C(ctx, "zs-logos__row", imgs)])


def posts(ctx, s):
    sc = f'[zap_recent_posts count="{int(s.get("count", 3))}"' + (f' category="{s["category"]}"' if s.get("category") else "") + "]"
    return section(ctx, s, "zs-posts", [*sec_head(ctx, s), W(ctx, "shortcode", {"shortcode": sc}), buttons(ctx, s.get("more"))])


def contact(ctx, s):
    left = C(ctx, "zs-contact__info", [heading(ctx, s.get("title"), "h2", "zs-sec__title"), text(ctx, s.get("text")),
                                       W(ctx, "shortcode", {"shortcode": "[zap_nap]"}),
                                       W(ctx, "shortcode", {"shortcode": '[zap_form id="contact" email="yes"]'})])
    right = C(ctx, "zs-contact__map", [W(ctx, "shortcode", {"shortcode": "[zap_map]"})]) if s.get("map", True) else None
    return section(ctx, s, "zs-contact", [left, right])


def reviews(ctx, s):
    if not ctx.site["business"].get("dpz_customer_id"):
        return None   # no real source -> no reviews block at all
    return section(ctx, s, "zs-reviews-sec", [*sec_head(ctx, s), W(ctx, "shortcode", {"shortcode": "[zap_reviews]"})])


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
    body = f'<div class="zs-mq" aria-hidden="true">{track}{track}</div>'
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
           f'<div class="zs-road__scene" aria-hidden="true"><div class="zs-road__sky">{sky}{sky}</div>' \
           f'<div class="zs-road__lane">{vs}</div></div>'
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


SECTIONS = {f.__name__: f for f in (hero, trust, cards, features, steps, split, prose, faq, cta, gallery,
                                     logos, posts, contact, reviews, video, quote, road, route, marquee)}


def render_page(ctx, sections):
    out = []
    plain_i = 0
    for s in sections:
        t = s.get("type")
        if t not in SECTIONS:
            raise ValueError(f"unknown section type '{t}' on page '{ctx.page_key}'. Known: {', '.join(SECTIONS)}")
        if t not in ("hero", "cta", "marquee", "trust") and "bg" not in s:
            # quiet rhythm: alternate plain and surface backgrounds after the hero
            s = {**s, "bg": "surface" if plain_i % 2 else None}
            plain_i += 1
        el = SECTIONS[t](ctx, s)
        if el:
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


def footer_template(ctx):
    d = ctx.site
    b, f, form = d["business"], d.get("footer", {}), d.get("form", {})
    lead = C(ctx, "zs-leadband", [
        C(ctx, "zs-wrap zs-leadband__in", [
            C(ctx, "zs-leadband__text", [
                heading(ctx, form.get("title", "השאירו פרטים ונחזור אליכם"), "h2", "zs-leadband__title"),
                text(ctx, form.get("text", "ממלאים שם וטלפון, ואנחנו חוזרים בהקדם.")),
                W(ctx, "shortcode", {"shortcode": "[zap_call_line]"}, "zs-leadband__or"),
            ]),
            W(ctx, "shortcode", {"shortcode": '[zap_form id="footer"]'}, "zs-leadband__form"),
        ]),
    ], tag="section", inner=False)
    lead["settings"]["_element_id"] = "leave-details"
    cols = C(ctx, "zs-wrap zs-footer__grid", [
        C(ctx, "zs-footer__col zs-footer__brand", [
            heading(ctx, b["name"], "p", "zs-footer__name"),
            text(ctx, f.get("about", "")),
        ]),
        C(ctx, "zs-footer__col", [
            heading(ctx, f.get("links_title", "השירותים שלנו"), "h2", "zs-footer__title"),
            W(ctx, "shortcode", {"shortcode": '[zap_menu location="footer"]'}),
        ], tag="nav"),
        C(ctx, "zs-footer__col", [
            heading(ctx, "יצירת קשר", "h2", "zs-footer__title"),
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

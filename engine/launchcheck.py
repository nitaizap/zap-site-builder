"""zs launch-check <url>: the pre-handover gate. Is this client site launch-ready? Reads only the site's PUBLIC html.

Zap does not launch client sites: someone else moves the site to the client's domain. The deliverable is a launch-ready
site, i.e. one that is staged correctly, clean on QA and SEO, verified on desktop and mobile, and verified so that the
staging -> live transition changes nothing. So this runs on the STAGING site BEFORE handover: it proves the site is
sound, predicts what a migration will break, and writes the launch sheet (`sites/<slug>/LAUNCH-SHEET.md`) the person who
flips the switch works from. Run again on the live address afterwards (same command): it then proves the launch took.

No admin, no credentials: it works on any client site, staging or live, and changes nothing.

Why it exists: the plugin `zap-site` carries the site's behaviour (every `zap-*` Elementor widget, the lead form,
the legal line, and `inc/launch.php`, which decides staging vs live by address). A launch done by copying the site
with a migration tool (uPress clone, All-in-One, Duplicator, WPvivid...) can leave the plugin behind while the
`zap-base` theme travels. Elementor silently drops a widget whose type is not registered, so the site returns HTTP 200
and looks half-built: no menu, no form, no legal line. On הוילה הלבנה (thewhite-villa.co.il) that is exactly what went
live. `zs push --live` installs theme and plugin together and does not hit this; a copy does.

Every check is a named PASS / FAIL row, like `zs seo`. Exit 0 when nothing fails, 2 when something does.
The checks themselves are pure functions of the fetched html (`analyse`), so `zs launch-check --selftest` proves them
offline against captured markup of a healthy site and of the broken one.
"""
import html as H
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

# the same rule as plugin inc/launch.php zap_is_staging_host() (the per-site zap_staging_hosts option is private to
# the site, so a staging address outside these needs --staging)
STAGING_SUFFIXES = (".ussl.co.il", ".zapsites.co.il", ".local", ".test")
STAGING_EXACT = ("localhost", "127.0.0.1")
# hosts that must never be linked from a live domain
STAGING_LINK_SUFFIXES = (".ussl.co.il", ".zapsites.co.il")

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
NAV_CLASSES = {"zs-menu", "elementor-nav-menu", "e-n-menu"}
CONTACT_HINT = re.compile(r"contact|צור-?קשר|צרו-?קשר|יצירת-?קשר|קשר", re.I)

PLUGIN_HINT = ("The zap-site plugin is probably missing on this site (the zap-base theme travelled, the plugin did not): "
               "install and activate it, or launch with `zs push --live`, which installs theme and plugin together. / "
               "כנראה שתוסף zap-site לא הועבר לאתר (תבנית zap-base הועברה, התוסף לא): התקינו והפעילו אותו, "
               "או בצעו את ההשקה עם `zs push --live` שמתקין תבנית ותוסף יחד.")


# --------------------------------------------------------------------------------------- tiny tolerant DOM

class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "text")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs or {}), parent
        self.children, self.text = [], []

    def classes(self):
        return set((self.attrs.get("class") or "").split())

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def find_all(self, pred):
        return [n for n in self.walk() if pred(n)]

    def all_text(self):
        return " ".join(t for n in self.walk() for t in n.text)


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, [(k, v or "") for k, v in attrs], self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, [(k, v or "") for k, v in attrs], self.cur))

    def handle_endtag(self, tag):
        p = self.cur
        while p is not self.root and p.tag != tag:
            p = p.parent
        if p is not self.root:
            self.cur = p.parent

    def handle_data(self, data):
        if self.cur.tag not in ("script", "style"):
            self.cur.text.append(data)
        else:
            self.cur.text.append("")


def parse(html_text):
    b = _Builder()
    b.feed(html_text)
    b.close()
    return b.root


# --------------------------------------------------------------------------------------- the page facts

def is_staging_host(host):
    host = (host or "").lower()
    return host in STAGING_EXACT or host.endswith(STAGING_SUFFIXES)


def _meta_robots(root):
    out = []
    for n in root.find_all(lambda n: n.tag == "meta" and (n.attrs.get("name") or "").lower() in ("robots", "googlebot")):
        out.append(n.attrs.get("content", "").lower())
    return out


def is_noindex(root, headers=None):
    x = (headers or {}).get("x-robots-tag", "").lower()
    return "noindex" in x or any("noindex" in c for c in _meta_robots(root))


def zap_widgets(root):
    """The `zap-*` Elementor widgets rendered on the page (class elementor-widget-zap-* / data-widget_type zap-*)."""
    out = set()
    for n in root.walk():
        for c in n.classes():
            if c.startswith("elementor-widget-zap-"):
                out.add(c[len("elementor-widget-"):])
        wt = n.attrs.get("data-widget_type", "")
        if wt.startswith("zap-"):
            out.add(wt.split(".")[0])
    return out


def plugin_markup(root):
    """Markup only the zap-site plugin produces: the lead form, or a widget's `zs-part` wrapper."""
    return bool(root.find_all(lambda n: "zs-form" in n.classes() or "zs-part" in n.classes()))


def raw_shortcodes(root):
    """A `[zap_*]` shortcode printed as text: a legacy site whose plugin (the one that registers it) is gone."""
    hits = set()
    for n in root.walk():
        if n.tag in ("script", "style"):
            continue
        for t in n.text:
            hits.update(re.findall(r"\[zap_[a-z_]+[^\]]*\]", t))
    return sorted(hits)


def _site_link(href, host):
    """A link that stays on this site: relative, an in-page anchor, or the same host (not tel:/mailto:/js)."""
    href = (href or "").strip()
    if not href or href.startswith(("tel:", "mailto:", "javascript:", "sms:", "whatsapp:")):
        return False
    if href.startswith("#") and len(href) > 1:
        return True
    p = urllib.parse.urlsplit(href)
    return not p.netloc or p.netloc.lower().removeprefix("www.") == host.removeprefix("www.")


def header_region(root):
    """The Elementor Theme Builder header, else the first <header> (the theme's own PHP header)."""
    for n in root.walk():
        if "data-elementor-type" in n.attrs and n.attrs["data-elementor-type"] == "header":
            return n
    for n in root.walk():
        if n.tag == "header":
            return n
    return None


def header_navigation(root, host):
    """(status, note): is there a menu in the header, and does it carry site links?"""
    hdr = header_region(root)
    if hdr is None:
        return "FAIL", "no header on the page / אין כותרת עליונה בדף"
    containers = hdr.find_all(lambda n: n.tag == "nav" or (n.classes() & NAV_CLASSES))
    burger = hdr.find_all(lambda n: "zs-burger" in n.classes())
    fallback = [n for n in containers if "zs-fallback-nav" in n.classes()]
    real = [n for n in containers if "zs-fallback-nav" not in n.classes()]
    links = {a.attrs["href"] for n in real for a in n.find_all(lambda x: x.tag == "a" and "href" in x.attrs)
             if _site_link(a.attrs["href"], host)}
    # the theme's emergency navigation sits right after the header (outside the template), so look for it page-wide
    fb = fallback or root.find_all(lambda n: "zs-fallback-nav" in n.classes())
    if links:
        return "PASS", f"{len(links)} menu links in the header{', with burger' if burger else ''} / {len(links)} קישורי תפריט בכותרת"
    if fb:
        return "FAIL", ("only the theme's EMERGENCY navigation is showing: the zap-site plugin is not running, the real menu is gone / "
                        "מוצג רק תפריט החירום של התבנית: תוסף zap-site לא פעיל והתפריט האמיתי נעלם")
    if containers or burger:
        return "FAIL", ("the header has a menu container but no site links in it (empty menu) / "
                        "בכותרת יש מכל תפריט אבל בלי קישורים (תפריט ריק)")
    return "FAIL", "the header has no navigation: no zs-menu, no zs-burger, no <nav> with site links / בכותרת אין תפריט ניווט בכלל"


def lead_forms(root):
    """<form>s that can take an enquiry: not search, dialog (close button), login or comment forms."""
    out = []
    for f in root.find_all(lambda n: n.tag == "form"):
        method = (f.attrs.get("method") or "get").lower()
        cls = " ".join(sorted(f.classes())).lower()
        marker = f.attrs.get("id", "").lower() + " " + cls + " " + f.attrs.get("role", "").lower() + " " + f.attrs.get("action", "").lower()
        if method == "dialog" or "search" in marker or "wp-login" in marker or "wp-comments-post" in marker or "commentform" in marker:
            continue
        fields = [i for i in f.find_all(lambda n: n.tag in ("input", "textarea", "select"))
                  if i.tag != "input" or (i.attrs.get("type") or "text").lower() not in ("hidden", "submit", "button", "image", "reset")]
        if not fields:
            continue
        if method == "post" or "zs-form" in f.classes() or "elementor-form" in f.classes():
            out.append(f)
    return out


def find_contact_url(root, base_url):
    """The contact page, taken from the home page's own links (header, footer, buttons)."""
    host = urllib.parse.urlsplit(base_url).netloc.lower().removeprefix("www.")
    for a in root.find_all(lambda n: n.tag == "a" and "href" in n.attrs):
        href = a.attrs["href"].strip()
        if not _site_link(href, host) or href.startswith("#"):
            continue
        u = urllib.parse.urljoin(base_url, href)
        path = urllib.parse.unquote(urllib.parse.urlsplit(u).path)
        label = " ".join(a.all_text().split())
        if path.strip("/") and (CONTACT_HINT.search(path) or re.search(r"צור קשר|צרו קשר|יצירת קשר|contact", label, re.I)):
            return u.split("#")[0]
    return None


ZAP_REGION_TYPES = ("header", "footer")
# plugins whose licence / connection is bound to the domain: they break (or go quiet) when the address changes
DOMAIN_BOUND = {
    "elementor-pro": ("Elementor Pro licence", "the licence is tied to the domain: after the move the editor shows 'מפתח הרישיון אינו תואם "
                      "לדומיין הנוכחי' and Pro features/updates stop until it is re-activated: wp-admin → Elementor → License → "
                      "disconnect on the old domain, connect on the new one"),
    "pojo-accessibility": ("Ally accessibility toolbar", "the toolbar button appears only after wp-admin → Ally → Connect on the live "
                           "address: connect it again on the new domain (Zap SEO checklist row 10)"),
    "wordpress-seo-premium": ("Yoast SEO Premium licence", "re-activate the licence on the new domain (MyYoast)"),
    "wp-rocket": ("WP Rocket licence", "re-activate the licence on the new domain"),
    "wpml-string-translation": ("WPML licence", "re-register the site key on the new domain"),
    "jet-engine": ("Crocoblock licence", "re-activate the licence on the new domain"),
}


def region(root, kind):
    """The Elementor Theme Builder template of this kind (`data-elementor-type`), or None."""
    for n in root.walk():
        if n.attrs.get("data-elementor-type") == kind:
            return n
    return None


def template_widgets(root):
    """{kind: (rendered zap widgets, empty ones)} for each header/footer template the page was built with."""
    out = {}
    for kind in ZAP_REGION_TYPES:
        r = region(root, kind)
        if r is None:
            continue
        got, empty = set(), set()
        for w in r.find_all(lambda n: n.attrs.get("data-widget_type", "").startswith("zap-")):
            name = w.attrs["data-widget_type"].split(".")[0]
            got.add(name)
            if not w.all_text().strip() and not w.find_all(lambda n: n.tag in ("img", "svg", "form", "input", "iframe")):
                empty.add(name)
        out[kind] = (got, empty)
    return out


def plugins_seen(html_text):
    """Plugin folders whose assets the page loads (zap-site loads none, so it is proven by its widgets instead)."""
    return sorted(set(re.findall(r"/wp-content/plugins/([a-z0-9_-]+)/", html_text.replace("\\/", "/"))))


def staging_pins(html_text, host):
    """What a migration's address rewrite cannot be trusted to catch, found in a STAGING site's own html:
    another staging host (a base-clone leftover) and this host written without a scheme (//host) or percent-encoded."""
    text = html_text.replace("\\/", "/")
    bare = host.split(":")[0]
    foreign = staging_links(html_text, bare)
    # WordPress core's oEmbed discovery links carry the page URL percent-encoded; they are rebuilt from the address on every request
    text = re.sub(r"[^\"'\s>]*wp-json/oembed[^\"'\s>]*", "", text)
    odd = {}
    for label, rx in (("scheme-less //host", r"(?<![:\w])//" + re.escape(host)), ("percent-encoded host", r"%2F%2F" + re.escape(host))):
        n = len(re.findall(rx, text, re.I))
        if n:
            odd[label] = n
    return foreign, odd


def qa_viewports(report_text):
    """{viewport: (pages, errors)} from a QA-REPORT table."""
    out = {}
    for m in re.finditer(r"^\|\s*(desktop|mobile)\s*\|[^|]*\|\s*(\d+)\s*\|", report_text, re.M):
        pages, errs = out.get(m.group(1), (0, 0))
        out[m.group(1)] = (pages + 1, errs + int(m.group(2)))
    return out


def robots_blocks_all(robots_txt):
    """True when robots.txt says `Disallow: /` for every crawler (User-agent: *)."""
    star, block = False, False
    for raw in robots_txt.splitlines():
        line = raw.split("#")[0].strip()
        if not line or ":" not in line:
            continue
        k, v = (x.strip() for x in line.split(":", 1))
        k = k.lower()
        if k == "user-agent":
            star = v == "*"
        elif k == "disallow" and star and v == "/":
            block = True
    return block


def staging_links(html_text, host):
    """Hosts of Zap's staging domains still referenced by the page (links, images, srcset, JSON, css url())."""
    text = html_text.replace("\\/", "/")
    found = {}
    for m in re.finditer(r"(?:https?:)?//([a-z0-9][a-z0-9.-]*)", text, re.I):
        h = m.group(1).lower().rstrip(".")
        if h != host and h.endswith(STAGING_LINK_SUFFIXES):
            found[h] = found.get(h, 0) + 1
    return found


# --------------------------------------------------------------------------------------- the checks

def analyse(home, contact=None, robots=None, mode=None, qa_report=None):
    """The named checks as [(name, status, note)]. Pure: everything it needs is in the argument.

    home / contact: {"url", "status", "html", "headers"} (contact may be None); robots: robots.txt text or None
    (not found); mode: "live" | "staging" | None (decided by the address, as the plugin does); qa_report: the text
    of the site's `zs qa` report (desktop + mobile), or None when there is none yet.
    """
    rows = []

    def R(name, status, note):
        rows.append((name, status, note))

    url = home["url"]
    host = urllib.parse.urlsplit(url).netloc.lower()
    staging = (mode == "staging") if mode else is_staging_host(host.split(":")[0])
    root = parse(home["html"])

    R("reachable", "PASS" if home["status"] == 200 and home["html"] else "FAIL",
      f"{url} -> HTTP {home['status']}, {len(home['html']) // 1024} KB / "
      f"{'האתר נטען' if home['status'] == 200 else 'האתר לא נטען כראוי'}")
    if home["status"] != 200 or not home["html"]:
        return rows

    # 1 - the plugin's widgets. Elementor drops an unregistered widget without a word.
    built = bool(root.find_all(lambda n: "data-elementor-type" in n.attrs))
    widgets = zap_widgets(root)
    marker_body = bool(root.find_all(lambda n: n.tag == "body" and "zs-plugin-missing" in n.classes()))
    if not built:
        R("zap-widgets", "N/A", "the home page is not built with Elementor / דף הבית לא נבנה ב-Elementor")
    elif widgets:
        R("zap-widgets", "PASS", f"{len(widgets)} zap-* widgets on the home page: {', '.join(sorted(widgets))[:160]} / "
                                f"{len(widgets)} ווידג'טים של זאפ בדף הבית")
    elif plugin_markup(root) and not marker_body:
        R("zap-widgets", "PASS", "no zap-* widget, but the plugin's own markup (lead form / zs-part) is there (legacy shortcode site) / "
                                "אין ווידג'טים אבל יש תוצר של התוסף (אתר ישן עם שורטקוד)")
    else:
        R("zap-widgets", "FAIL", "the page is Elementor-built but not ONE zap-* widget is on it: the zap-site plugin is not running, so "
                                 "Elementor dropped every Zap widget (menu, logo, form, legal line, contact list)"
                                 + (" [the theme says so itself: body.zs-plugin-missing]" if marker_body else "")
                                 + " / הדף נבנה ב-Elementor אבל אין בו אף ווידג'ט zap-*: תוסף zap-site לא פעיל ו-Elementor השמיט בשקט "
                                   "את כל ווידג'טי זאפ (תפריט, לוגו, טופס, שורה משפטית, פרטי קשר)")

    # the Theme Builder templates themselves: header and footer must each render Zap widgets (the villa's header kept
    # only its phone button), so we know no template silently depends on something that is absent
    tw = template_widgets(root)
    if not tw:
        R("template-widgets", "N/A", "no Elementor header/footer template on the page / אין תבניות כותרת ופוטר של Elementor")
    else:
        lost = [k for k, (g, _) in tw.items() if not g]
        empty = sorted({w for _, (_, e) in tw.items() for w in e})
        desc = "; ".join(f"{k}: {len(g)} zap widgets" for k, (g, _) in tw.items())
        R("template-widgets", "FAIL" if lost else "PASS",
          (f"{' and '.join(lost)} template renders NO zap-* widget (a template that depends on a plugin that is absent) / "
           f"תבנית {' ו'.join(lost)} לא מציגה אף ווידג'ט zap-*") if lost
          else desc + (f"; rendered empty (check): {', '.join(empty)}" if empty else "") + " / תבניות הכותרת והפוטר מציגות ווידג'טים")

    sc = raw_shortcodes(root)
    R("raw-shortcodes", "FAIL" if sc else "PASS",
      ("a Zap shortcode is printed as text (its plugin is not registering it): " + ", ".join(sc[:4]) + " / שורטקוד של זאפ מודפס כטקסט") if sc
      else "no unrendered [zap_*] shortcode / אין שורטקוד גולמי")

    # 2 - navigation
    st, note = header_navigation(root, host)
    R("header-nav", st, note)

    # 3 - a form that can take an enquiry, on the contact page or the home page
    pages = [("home", root)]
    if contact and contact.get("status") == 200 and contact.get("html"):
        pages.append(("contact", parse(contact["html"])))
    found = [(label, f) for label, r in pages for f in lead_forms(r)]
    where = ", ".join(sorted({l for l, _ in found}))
    searched = " + ".join(l for l, _ in pages) + ("" if len(pages) > 1 else " (no contact page found)")
    R("lead-form", "PASS" if found else "FAIL",
      (f"{len(found)} lead form(s) on: {where} / טופס פניות נמצא: {where}") if found
      else f"no enquiry <form> on {searched}: the site cannot receive a lead / אין טופס פניות (נבדק: {searched}): האתר לא יכול לקבל פנייה")

    # 4 - indexing follows the address (launch.php decides; this proves it took effect)
    noindex = is_noindex(root, home.get("headers"))
    mode_s = "staging" if staging else "live"
    if staging:
        R("indexing", "PASS" if noindex else "FAIL",
          f"staging address ({host}): " + ("noindex, as it should be / חסום לאינדוקס, כמצופה" if noindex else
          "INDEXABLE: a staging site must be noindex / האתר פתוח לאינדוקס אף שהוא סטייג'ינג"))
    else:
        R("indexing", "FAIL" if noindex else "PASS",
          f"live address ({host}): " + ("NOINDEX: the site is hidden from Google (launch.php did not run?) / האתר חסום לאינדוקס בדומיין חי" if noindex
                                       else "indexable / פתוח לאינדוקס"))
    if robots is None:
        R("robots-txt", "PASS", f"no robots.txt served ({mode_s}); the meta robots tag decides / אין robots.txt")
    else:
        blocked = robots_blocks_all(robots)
        ok = blocked if staging else not blocked
        R("robots-txt", "PASS" if ok else "FAIL",
          f"{mode_s} address: robots.txt " + ("disallows everything" if blocked else "allows crawling")
          + ("" if ok else (": a live site must not block all crawlers / אתר חי חוסם את כל הסורקים" if not staging
                            else ": a staging site should disallow crawling / סטייג'ינג לא חוסם סורקים"))
          )

    # 5 - a live domain must not point back at staging; a staging site must not pin anything a move cannot rewrite
    if staging:
        R("staging-links", "N/A", "staging address: nothing to move yet / כתובת סטייג'ינג")
        foreign, odd = staging_pins(home["html"], host)
        if contact and contact.get("html"):
            f2, o2 = staging_pins(contact["html"], host)
            foreign.update({k: foreign.get(k, 0) + v for k, v in f2.items()})
            odd.update({k: odd.get(k, 0) + v for k, v in o2.items()})
        bad = [f"another staging host {h} x{n}" for h, n in sorted(foreign.items())] + [f"{k} x{n}" for k, n in sorted(odd.items())]
        R("migration-pins", "FAIL" if bad else "PASS",
          ("the launch rewrite (https://host and http://host, plain and JSON-escaped) will not catch: " + "; ".join(bad)
           + " / כתובות שהחלפת הכתובת בהשקה לא תתפוס") if bad
          else "no foreign staging host and no scheme-less / encoded copy of this host: the address rewrite has nothing to miss / "
               "אין כתובות שההשקה תפספס")
        R("leads-not-mailed", "MANUAL", "cannot be observed from public html (a test lead would mail the client if staging mode failed). "
          "launch.php sets noindex and the lead routing in the same step, so noindex + Disallow in force above is the proof it ran; "
          "confirm once in wp-admin → Leads that a test lead was saved, never mailed / לא ניתן לבדוק מבחוץ")
    else:
        bad = staging_links(home["html"], host.split(":")[0])
        if contact and contact.get("html"):
            for h, n in staging_links(contact["html"], host.split(":")[0]).items():
                bad[h] = bad.get(h, 0) + n
        R("staging-links", "FAIL" if bad else "PASS",
          ("links/images still point at staging: " + ", ".join(f"{h} x{n}" for h, n in sorted(bad.items())) + " / קישורים או תמונות עדיין מצביעים לסטייג'ינג")
          if bad else "no staging host referenced / אין הפניות לסטייג'ינג")
    # 6 - things licensed to the domain: a move breaks them, so the person who launches must redo them
    seen = plugins_seen(home["html"])
    bound = [(slug, *DOMAIN_BOUND[slug]) for slug in seen if slug in DOMAIN_BOUND]
    R("domain-licences", "MANUAL" if bound else "PASS",
      ("tied to the domain, redo them on the new one: " + ", ".join(b[1] for b in bound) + " (details in the launch sheet) / "
       "מקושרים לדומיין, יש לחדש בדומיין החדש") if bound else "no domain-bound plugin detected on the page / לא זוהה תוסף הקשור לדומיין")

    # 7 - launch-ready includes desktop AND mobile: zs qa measures every page at both
    if qa_report is None:
        R("desktop-mobile", "MANUAL", "no zs qa report given: run `zs qa <slug> --site <url>` (every page at 1440 desktop and 390 mobile) "
          "and pass --slug so this gate reads it / לא נמצא דוח QA")
    else:
        vp = qa_viewports(qa_report)
        miss = [v for v in ("desktop", "mobile") if v not in vp]
        errs = sum(e for _, e in vp.values())
        R("desktop-mobile", "FAIL" if miss or errs else "PASS",
          (f"QA report has no {' / '.join(miss)} rows: not verified on both / לא נבדק בשני המסכים" if miss else
           f"QA errors: {errs}" if errs else
           f"desktop {vp['desktop'][0]} pages, mobile {vp['mobile'][0]} pages, 0 errors / דסקטופ ומובייל נבדקו, 0 שגיאות"))
    return rows


# --------------------------------------------------------------------------------------- fetching + CLI

def fetch(url, timeout=30):
    """-> {url (final), status, html, headers}. Never raises on an HTTP error; a network error gives status 0."""
    req = urllib.request.Request(urllib.parse.quote(url, safe=":/?=&%#+~@!$'()*,;"), headers={"User-Agent": "zs-launch-check/1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"url": r.geturl(), "status": r.status, "html": r.read().decode("utf-8", "replace"),
                    "headers": {k.lower(): v for k, v in r.headers.items()}}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "html": e.read().decode("utf-8", "replace"),
                "headers": {k.lower(): v for k, v in e.headers.items()}}
    except (urllib.error.URLError, OSError) as e:
        return {"url": url, "status": 0, "html": "", "headers": {}, "error": str(e)}


def run_launch_check(url, mode=None, contact_url=None, out=None, say=print, slug=None):
    """Fetch the home page, the contact page and robots.txt, run `analyse`, print every row. True when nothing fails."""
    if "://" not in url:
        url = "https://" + url
    home = fetch(url)
    contact = robots = None
    if home["status"] == 200:
        p = urllib.parse.urlsplit(home["url"])
        base = f"{p.scheme}://{p.netloc}"
        cu = contact_url or find_contact_url(parse(home["html"]), home["url"])
        # a broken site has no menu to find the contact page in: try the usual slugs too
        for cand in ([cu] if cu else [base + s for s in ("/contact/", "/צור-קשר/", "/צרו-קשר/")]):
            if cand.rstrip("/") == home["url"].rstrip("/"):
                continue
            c = fetch(cand)
            if c["status"] == 200 and c["url"].rstrip("/") != home["url"].rstrip("/"):
                contact = c
                break
        r = fetch(base + "/robots.txt")
        robots = r["html"] if r["status"] == 200 else None
    elif home.get("error"):
        home["html"] = ""
    qa = None
    if slug:
        src = Path(__file__).resolve().parent.parent / "sites" / slug
        for name in ("QA-REPORT-live.md", "QA-REPORT.md"):   # the pushed site's report first: it is the site being gated
            if (src / name).exists():
                qa = (src / name).read_text(encoding="utf-8")
                break
    rows = analyse(home, contact, robots, mode, qa)
    ok = _report(home, contact, rows, out, say)
    if slug:
        sheet = Path(__file__).resolve().parent.parent / "sites" / slug / "LAUNCH-SHEET.md"
        sheet.parent.mkdir(parents=True, exist_ok=True)
        sheet.write_text(launch_sheet(home, rows, slug), encoding="utf-8")
        say(f"launch sheet: {sheet}")
    else:
        say("(pass --slug <slug> to also write sites/<slug>/LAUNCH-SHEET.md, the handover sheet for whoever launches)")
    return ok


def _report(home, contact, rows, out, say):
    fails = [r for r in rows if r[1] == "FAIL"]
    host = urllib.parse.urlsplit(home["url"]).netloc
    say(f"launch check: {home['url']}" + (f"  (contact page: {contact['url']})" if contact else ""))
    for name, status, note in rows:
        say(f"{status:5} {name:15} {note}")
    if fails:
        say(f"\nLAUNCH CHECK FAILED: {len(fails)} of {len(rows)} checks failed on {host} / בדיקת ההשקה נכשלה: {len(fails)} מתוך {len(rows)}")
        if any(n in ("zap-widgets", "header-nav", "raw-shortcodes") for n, s, _ in fails):
            say(PLUGIN_HINT)
    else:
        say(f"\nlaunch check passed: {len(rows)} checks on {host} / בדיקת ההשקה עברה")
    if out:
        icon = {"PASS": "✅", "FAIL": "❌", "N/A": "—", "MANUAL": "👁"}
        md = [f"# Launch check: {home['url']}", "", f"{len(rows)} checks: {sum(r[1] == 'PASS' for r in rows)} pass, {len(fails)} fail", "",
              "| check | status | note |", "|---|---|---|"]
        md += [f"| {n} | {icon[s]} {s} | {note.replace('|', '/')} |" for n, s, note in rows]
        Path(out).write_text("\n".join(md) + "\n", encoding="utf-8")
        say(f"report: {out}")
    return not fails


def launch_sheet(home, rows, slug, today=None):
    """The handover for the person who launches (Zap does not): what must travel, what to redo, what to verify after."""
    import datetime
    host = urllib.parse.urlsplit(home["url"]).netloc
    seen = plugins_seen(home["html"])
    fails = [r for r in rows if r[1] == "FAIL"]
    bound = [DOMAIN_BOUND[x] for x in seen if x in DOMAIN_BOUND]
    icon = {"PASS": "✅", "FAIL": "❌", "N/A": "—", "MANUAL": "👁"}
    day = today or datetime.date.today().isoformat()
    md = [f"# Launch sheet / דף השקה: {slug}", "",
          f"Checked {day} on `{home['url']}` by `zs launch-check`. Gate: **{'NOT READY: ' + str(len(fails)) + ' check(s) failed, do not hand over' if fails else 'READY (nothing failed)'}**"
          f"{'; ' + str(sum(r[1] == 'MANUAL' for r in rows)) + ' item(s) below still need a person' if any(r[1] == 'MANUAL' for r in rows) else ''}.",
          "Zap does not launch client sites. This is what whoever launches this one needs. / זאפ לא מבצעת השקה. זה מה שמי שמשיק צריך.", "",
          "## 1. What must travel with the site / מה חייב לנסוע", "",
          "- **The `zap-site` plugin, with the theme `zap-base`.** The theme alone is not the site: every `zap-*` widget (menu, logo, lead form, legal line, "
          "contact list, Zap credit) and the launch behaviour (indexing, lead mail, address repair, `inc/launch.php`) live in the plugin. "
          "A migration tool that copies only some folders left it behind on הוילה הלבנה (03/11/2026): no menu, no form, still HTTP 200. "
          "Copy the whole `wp-content` (themes and plugins), or install both with `zs push <slug> --site https://<final> --live`.",
          f"- Plugins this page loads: {', '.join(f'`{x}`' for x in seen) or 'none detected'} (plus `zap-site`, proven by its widgets, and Yoast SEO, "
          "which prints no assets).", "",
          "## 2. What must be redone on the new domain / מה עושים מחדש בדומיין החדש", ""]
    md += [f"- **{b[0]}**: {b[1]}" for b in bound] or ["- No domain-bound plugin was detected on the page."]
    md += ["- DNS, SSL and Search Console for the new domain (a person, outside WordPress).",
           "- The first request on the new address makes `launch.php` switch the site to live (index, robots.txt, lead mail) and rewrite the old "
           f"address (`{host}`) inside Elementor's data: open the home page once, then wp-admin once.", "",
           "## 3. Verify immediately after the move / מה לאמת מיד אחרי", "",
           "1. `bin/zs launch-check https://<final-domain>` → every row PASS (it fails by name if the plugin is missing, the menu or form is gone, "
           "the site is still noindex, or anything still points at `*.ussl.co.il`).",
           "2. wp-admin → Dashboard shows **no red notice** \"חסר התוסף Zap Site\" (the theme raises it when the plugin is not running).",
           "3. Look at the home page on a phone (390px) and a laptop (1280px): logo, menu and burger, the form, the footer legal line.",
           "4. Send one real test lead: it must arrive in the client's inbox (staging never mails them) and appear in wp-admin → Leads.",
           "5. Re-do the section 2 items; Elementor → License must not say the key does not match the domain.", "",
           "## Gate results on staging / תוצאות הבדיקה לפני ההעברה", "", "| check | status | note |", "|---|---|---|"]
    md += [f"| {n} | {icon[s]} {s} | {note.replace('|', '/')} |" for n, s, note in rows]
    return "\n".join(md) + "\n"


# --------------------------------------------------------------------------------------- offline selftest

HEALTHY = """<html><head><meta name='robots' content='noindex, nofollow' /></head><body class="home">
<header data-elementor-type="header"><header class="zs-header"><div class="elementor-widget elementor-widget-zap-nav" data-widget_type="zap-nav.default">
<div class="zs-part zs-part--nav"><nav id="zs-nav" class="zs-nav"><ul class="zs-menu"><li><a href="https://x.ussl.co.il/">בית</a></li><li><a href="/about/">אודות</a></li></ul></nav>
<button class="zs-burger"></button></div></div></header></header>
<main><div data-elementor-type="wp-page">
<div class="elementor-widget elementor-widget-zap-form" data-widget_type="zap-form.default"><div class="zs-part"><form class="zs-form" method="post" action="/wp-admin/admin-post.php"><input type="hidden" name="a"><input name="phone"><button>שלח</button></form></div></div>
<form class="elementor-search-form" action="https://x.ussl.co.il" method="get" role="search"><input type="search" name="s"></form>
</div></main>
<footer data-elementor-type="footer"><div class="elementor-widget elementor-widget-zap-legal" data-widget_type="zap-legal.default"><div class="zs-part"><ul><li><a href="/privacy/">פרטיות</a></li></ul></div></div></footer>
<dialog><form method="dialog"><button>x</button></form></dialog></body></html>"""

# the real failure: the same page after migrating without the plugin (theme + Elementor, no zap-* widget)
BROKEN = """<html><head><meta name='robots' content='index, follow' /></head><body class="home">
<header data-elementor-type="header"><header class="zs-header"><div class="elementor-widget elementor-widget-button" data-widget_type="button.default"><a href="tel:+972500000000">050-0000000</a></div></header></header>
<main><div data-elementor-type="wp-page"><div class="elementor-widget elementor-widget-heading"><h1>הוילה</h1></div>
<img src="https://x.ussl.co.il/wp-content/uploads/a.jpg"><a href="https://x.ussl.co.il/about/">אודות</a></div></main>
<nav id="pojo-a11y-toolbar"><a href="#content">skip</a></nav>
<form class="elementor-search-form" action="https://villa.co.il" method="get"><input type="search" name="s"></form>
<dialog><form method="dialog"><button>x</button></form></dialog></body></html>"""


def selftest(say=print):
    """Both directions: the healthy markup passes, the broken one fails with the findings it should. True when right."""
    def run(html_text, url, **kw):
        return {n: (s, note) for n, s, note in analyse({"url": url, "status": 200, "html": html_text, "headers": {}}, **kw)}

    ok = True

    def expect(label, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        say(f"{'ok  ' if good else 'BAD '} {label}: {got}" + ("" if good else f"  (wanted {want})"))

    h = run(HEALTHY, "https://x.ussl.co.il/")                      # healthy staging site
    for k in ("zap-widgets", "raw-shortcodes", "header-nav", "lead-form", "indexing", "staging-links"):
        expect(f"healthy staging / {k}", h[k][0], "N/A" if k == "staging-links" else "PASS")
    b = run(BROKEN, "https://villa.co.il/")                       # the broken site on its live domain
    for k in ("zap-widgets", "header-nav", "lead-form", "staging-links"):
        expect(f"broken live / {k}", b[k][0], "FAIL")
    expect("broken live / indexing (indexable on a live domain)", b["indexing"][0], "PASS")
    # the other directions of the address rule
    expect("live domain, noindex -> FAIL", run(HEALTHY, "https://villa.co.il/")["indexing"][0], "FAIL")
    expect("staging domain, indexable -> FAIL", run(BROKEN, "https://x.ussl.co.il/")["indexing"][0], "FAIL")
    expect("--staging on an unknown host, noindex -> PASS", run(HEALTHY, "https://clone.example.org/", mode="staging")["indexing"][0], "PASS")
    expect("robots.txt Disallow / on a live domain -> FAIL", run(BROKEN, "https://villa.co.il/", robots="User-agent: *\nDisallow: /\n")["robots-txt"][0], "FAIL")
    expect("robots.txt allowing all on staging -> FAIL", run(HEALTHY, "https://x.ussl.co.il/", robots="User-agent: *\nDisallow:\n")["robots-txt"][0], "FAIL")
    # a legacy shortcode site whose plugin is gone, and the theme's own fallback navigation
    legacy = BROKEN.replace("<h1>הוילה</h1>", "<h1>הוילה</h1><p>[zap_form id=\"main\"]</p>")
    expect("raw [zap_form] shortcode -> FAIL", run(legacy, "https://villa.co.il/")["raw-shortcodes"][0], "FAIL")
    fb = BROKEN.replace("</header></header>", "</header></header><nav class=\"zs-fallback-nav\"><ul><li><a href=\"/a/\">a</a></li></ul></nav>", 1) \
               .replace("<body class=\"home\">", "<body class=\"home zs-plugin-missing\">")
    r = run(fb, "https://villa.co.il/")
    expect("theme fallback nav alone still FAILs header-nav", r["header-nav"][0], "FAIL")
    expect("body.zs-plugin-missing marks zap-widgets FAIL", r["zap-widgets"][0], "FAIL")
    # the staging gate: templates, pins, licences, desktop + mobile
    expect("template-widgets: healthy header+footer with widgets", h["template-widgets"][0], "PASS")
    expect("template-widgets: villa-style header (phone only) FAILs", b["template-widgets"][0], "FAIL")
    pinned = HEALTHY.replace("</main>", '<a href="//x.ussl.co.il/p">p</a><a href="https://other-clone.ussl.co.il/q">q</a></main>')
    expect("migration-pins: scheme-less own host + foreign staging host -> FAIL", run(pinned, "https://x.ussl.co.il/")["migration-pins"][0], "FAIL")
    expect("migration-pins: clean staging page -> PASS", h["migration-pins"][0], "PASS")
    oe = HEALTHY.replace("<head>", '<head><link rel="alternate" href="https://x.ussl.co.il/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fx.ussl.co.il%2F">')
    expect("migration-pins: WordPress's own oEmbed link is not a pin", run(oe, "https://x.ussl.co.il/")["migration-pins"][0], "PASS")
    pro = HEALTHY.replace("<head>", '<head><link rel="stylesheet" href="/wp-content/plugins/elementor-pro/a.css">')
    expect("domain-licences: Elementor Pro on the page -> MANUAL", run(pro, "https://x.ussl.co.il/")["domain-licences"][0], "MANUAL")
    expect("domain-licences: none -> PASS", h["domain-licences"][0], "PASS")
    rep = "| viewport | page |\n|---|---|\n| desktop | / | 0 | 0 | 90 |  |\n| mobile | / | 0 | 0 | 90 |  |\n"
    expect("desktop-mobile: both viewports, 0 errors -> PASS", run(HEALTHY, "https://x.ussl.co.il/", qa_report=rep)["desktop-mobile"][0], "PASS")
    expect("desktop-mobile: desktop only -> FAIL", run(HEALTHY, "https://x.ussl.co.il/", qa_report=rep.split("| mobile")[0])["desktop-mobile"][0], "FAIL")
    expect("desktop-mobile: no report -> MANUAL", h["desktop-mobile"][0], "MANUAL")
    sheet = launch_sheet({"url": "https://x.ussl.co.il/", "html": pro}, analyse({"url": "https://x.ussl.co.il/", "status": 200, "html": pro, "headers": {}}), "demo", "2026-01-01")
    expect("launch sheet names the plugin that must travel and the licence to redo", ("`zap-site` plugin" in sheet) and ("Elementor Pro licence" in sheet), True)
    contact = {"url": "https://villa.co.il/contact/", "status": 200, "html": HEALTHY, "headers": {}}
    expect("a lead form on the contact page counts", run(BROKEN, "https://villa.co.il/", contact=contact)["lead-form"][0], "PASS")
    expect("contact page found from home links", find_contact_url(parse('<a href="/צור-קשר/">צור קשר</a>'), "https://v.co.il/"),
           "https://v.co.il/צור-קשר/")
    return ok


def cli(a):
    if a.selftest:
        sys.exit(0 if selftest() else 2)
    if not a.url:
        print("usage: zs launch-check <url> [--slug SLUG] [--staging | --live] [--contact URL] [--out FILE]   |   zs launch-check --selftest")
        sys.exit(1)
    mode = "staging" if a.staging else ("live" if a.live else None)
    sys.exit(0 if run_launch_check(a.url, mode, a.contact, a.out, slug=a.slug) else 2)


def add_parser(sub):
    x = sub.add_parser("launch-check", help="read a site's public html and FAIL loudly when it is not launch-ready "
                                            "(plugin left behind, no menu/form, wrong indexing, staging links)")
    x.add_argument("url", nargs="?", help="the site (home page); needs no login")
    g = x.add_mutually_exclusive_group()
    g.add_argument("--staging", action="store_true", help="treat the address as staging (a staging host outside Zap's usual domains)")
    g.add_argument("--live", action="store_true", help="treat the address as live")
    x.add_argument("--contact", help="the contact page URL, when it cannot be found from the home page's links")
    x.add_argument("--slug", help="the client's slug: reads sites/<slug>/QA-REPORT*.md (desktop + mobile) and writes sites/<slug>/LAUNCH-SHEET.md")
    x.add_argument("--out", help="also write the rows to this markdown file (UTF-8)")
    x.add_argument("--selftest", action="store_true", help="run the checks offline against captured healthy / broken markup")
    x.set_defaults(f=cli)

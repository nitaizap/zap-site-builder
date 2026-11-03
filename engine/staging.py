"""zs staging <slug> --site URL: get into a staging WordPress the way a person does, on the user's PC.

Runs on the Windows PC (desktop Outlook + a browser). Replaces the manual steps:
  1. log in with the user's usual password (ZS_WP_USER / ZS_WP_PASSWORD, set once on the PC with `setx`,
     never committed, never printed);
  2. if that fails: "forgot password" → wait for the reset mail in desktop Outlook → open its link →
     set ZS_WP_PASSWORD → log in;
  3. if the cloud session asked for access (`sites/<slug>/inbox/connect-request.json`, written by
     `zs connect --handoff <slug>` in the cloud and pushed to site/<slug>): open the Novamira approval page,
     enter the code, authorize. The cloud session then holds its own token; no password leaves this PC.
The browser profile lives in work/browser-profile (gitignored), so later runs are already logged in.
"""
import json
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "work" / "browser-profile"

PS_FIND_RESET = r"""
$ns = (New-Object -ComObject Outlook.Application).GetNamespace('MAPI')
$items = $ns.GetDefaultFolder(6).Items
$items.Sort('[ReceivedTime]', $true)
$since = [datetime]::Parse('%SINCE%')
foreach ($m in $items) {
  if ($m.Class -ne 43) { continue }
  if ($m.ReceivedTime -lt $since) { break }
  $b = $m.HTMLBody + ' ' + $m.Body
  # Outlook rewrites every link as a safelink, so the reset URL is percent-encoded inside
  # eur04.safelinks.protection.outlook.com/?url=... and never appears literally. Take any URL
  # carrying action=rp in either form; Python unwraps it and checks the host.
  $x = [regex]::Matches($b, 'https?://[^\s"<>]*(action=rp|action%3[Dd]rp)[^\s"<>]*')
  foreach ($h in $x) { [System.Net.WebUtility]::HtmlDecode($h.Value) }
}
"""


def _reset_link(host, since, wait=300):
    ps = PS_FIND_RESET.replace("%SINCE%", since.strftime("%Y-%m-%dT%H:%M:%S"))
    end = time.time() + wait
    while True:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                             capture_output=True, text=True).stdout
        for raw in out.splitlines():
            link = _unwrap(raw.strip())
            if link.startswith("http") and host in urlsplit(link).hostname or "":
                if "action=rp" in link:
                    return link
        if time.time() >= end:
            break
        time.sleep(10)
    raise SystemExit(f"staging: no password-reset mail for {host} arrived in Outlook within {wait // 60} min")


def _unwrap(url):
    """The real URL behind an Outlook safelink wrapper, or the url unchanged."""
    if "safelinks.protection.outlook.com" not in url:
        return url
    inner = parse_qs(urlsplit(url).query).get("url", [""])[0]
    return unquote(inner) or url


def _logged_in(page, url):
    page.goto(url + "/wp-admin/", wait_until="domcontentloaded")
    return "wp-login.php" not in page.url


def _login(page, url, user, pw):
    page.goto(url + "/wp-login.php", wait_until="domcontentloaded")
    page.fill("#user_login", user)
    page.fill("#user_pass", pw)
    page.click("#wp-submit")
    page.wait_for_load_state("domcontentloaded")
    return _logged_in(page, url)


def _reset(page, url, host, user, pw):
    since = datetime.now()
    page.goto(url + "/wp-login.php?action=lostpassword", wait_until="domcontentloaded")
    page.fill("#user_login", user)
    page.click("#wp-submit")
    page.wait_for_load_state("domcontentloaded")
    print("staging: reset requested, waiting for the mail in Outlook…", flush=True)
    link = _reset_link(host, since)
    page.goto(link, wait_until="domcontentloaded")
    _type_secret(page, "#pass1", pw)
    # count() matches a hidden element too. Current WordPress ships #pass2 in the DOM but hidden, so
    # filling it unconditionally waits 30s for an element that will never be editable and then throws
    # - with the password in the exception text. Only fill it when it is actually visible.
    _type_secret(page, "#pass2", pw, only_if_visible=True)
    if page.locator(".pw-checkbox").first.is_visible():   # "confirm use of weak password"
        page.check(".pw-checkbox")
    page.click("#wp-submit")
    page.wait_for_load_state("domcontentloaded")


def _type_secret(page, selector, value, only_if_visible=False):
    """Fill a password field without the value reaching any log.

    Playwright puts the fill() argument in its timeout message, so a failure here would print the
    shared staging password into the terminal and into whatever is reading it. Nothing in this module
    may ever surface a credential, so the error is replaced with one that names only the selector.
    """
    loc = page.locator(selector).first
    try:
        if only_if_visible and not loc.is_visible():
            return
        loc.fill(value, timeout=15000)
    except Exception as e:
        raise SystemExit("staging: could not fill %s (%s). The value is not shown."
                         % (selector, type(e).__name__)) from None


def _approve(page, req):
    page.goto(req["verification_uri"], wait_until="domcontentloaded")
    box = page.locator("input[type=text]:visible, input:not([type]):visible").first
    box.fill(req["user_code"])
    for label in ("Authorize", "Approve", "Allow", "אישור", "אשר"):
        b = page.get_by_role("button", name=re.compile(label, re.I))
        if b.count():
            b.first.click()
            break
    else:
        page.keyboard.press("Enter")
    page.wait_for_load_state("domcontentloaded")
    time.sleep(2)
    for label in ("Authorize", "Approve", "Allow"):     # some flows confirm on a second screen
        b = page.get_by_role("button", name=re.compile(label, re.I))
        if b.count():
            b.first.click()
            page.wait_for_load_state("domcontentloaded")
            break


def staging(slug, url, headless=False):
    from urllib.parse import urlsplit
    from playwright.sync_api import sync_playwright
    url = url.rstrip("/")
    host = urlsplit(url).hostname
    user, pw = os.environ.get("ZS_WP_USER"), os.environ.get("ZS_WP_PASSWORD")
    if not user or not pw:
        raise SystemExit("staging: set ZS_WP_USER and ZS_WP_PASSWORD once on this PC (setx ZS_WP_USER ..., then reopen the terminal)")
    PROFILE.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(str(PROFILE), headless=headless)
        page = ctx.new_page()
        if not _logged_in(page, url) and not _login(page, url, user, pw):
            _reset(page, url, host, user, pw)
            if not _login(page, url, user, pw):
                raise SystemExit(f"staging: still cannot log in to {url} after the reset (screenshot: work/staging-fail.png)")
        print(f"staging: logged in to {url}", flush=True)
        req_f = ROOT / "sites" / slug / "inbox" / "connect-request.json"
        if req_f.exists():
            req = json.loads(req_f.read_text(encoding="utf-8"))
            if time.time() < req.get("expires_at", 0):
                _approve(page, req)
                page.screenshot(path=str(ROOT / "work" / "staging-approve.png"))
                print("staging: access approved for the cloud session (screenshot work/staging-approve.png)")
            else:
                print("staging: the access request expired; the cloud session must run zs connect again")
        ctx.close()


def cli(a):
    staging(a.slug, a.site, a.headless)


def add_parser(sub):
    x = sub.add_parser("staging", help="PC: log in to a staging site (password reset via Outlook if needed) and approve the cloud's access request")
    x.add_argument("slug"); x.add_argument("--site", required=True); x.add_argument("--headless", action="store_true")
    x.set_defaults(f=cli)

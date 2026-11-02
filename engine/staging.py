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
  $x = [regex]::Match($b, 'https?://%HOST%/wp-login\.php\?[^\s"<>]*action=rp[^\s"<>]*')
  if ($x.Success) { [System.Net.WebUtility]::HtmlDecode($x.Value); break }
}
"""


def _reset_link(host, since, wait=300):
    ps = PS_FIND_RESET.replace("%SINCE%", since.strftime("%Y-%m-%dT%H:%M:%S")).replace("%HOST%", re.escape(host))
    end = time.time() + wait
    while time.time() < end:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True).stdout.strip()
        if out.startswith("http"):
            return out.splitlines()[0]
        time.sleep(10)
    raise SystemExit(f"staging: no password-reset mail for {host} arrived in Outlook within {wait // 60} min")


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
    page.fill("#pass1", pw)
    if page.locator("#pass2").count():
        page.fill("#pass2", pw)
    if page.locator(".pw-checkbox").count():        # "confirm use of weak password"
        page.check(".pw-checkbox")
    page.click("#wp-submit")
    page.wait_for_load_state("domcontentloaded")


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

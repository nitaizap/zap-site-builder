"""zs: build a Zap client site from site.json, test it, and ship it as an upload-ready zip.

  zs new <slug> "<business name>"   create the site folder + a local WordPress
  zs build <slug>                   apply work/<slug>/site.json (idempotent)
  zs serve <slug> | zs stop <slug>  local web server (http://127.0.0.1:<port>)
  zs shots <slug> [paths...]        screenshots desktop + mobile (+ design directions)
  zs preview <slug>                 home page under every design direction -> sites/<slug>/preview/PREVIEW.md
  zs qa <slug>                      measured QA sweep -> sites/<slug>/QA-REPORT.md
  zs doctor                         check php, wp-cli, mariadb, browser, network, gh
  zs image <slug> <key> "<prompt>"  AI atmosphere image -> sites/<slug>/assets/<key>.png (needs OPENAI_API_KEY)
  zs grab <slug> <url>              research the client's old site (Wayback fallback) -> sites/<slug>/research/
  zs fetch-image <slug> <key> <url> download a generated asset (Weave output) into sites/<slug>/assets/
  zs connect --site https://x       one-time approval in wp-admin (Novamira OAuth device flow), no password
  zs push <slug> --site https://x   build straight into a WordPress that runs Novamira (staging first)
  zs static <slug>                  offline browsable copy (open index.html) -> dist/<slug>-preview.zip
  zs package <slug> --domain https://client.co.il
  zs publish <slug>                 upload the zip as a GitHub release asset (+ SharePoint if set)
  zs list                           sites on this machine
  zs seo <slug>                     the Zap SEO QA checklist, row by row -> sites/<slug>/SEO-QA.md
  zs pool <slug>                    this site's measured look vs every other client (stops at 45% alike)
  zs registry <slug>                measure the local build into fingerprints/<slug>.json (the client registry)
"""
import argparse
import os
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from env import ROOT, die  # noqa: E402
from wpsite import Site  # noqa: E402


def cmd_new(a):
    s = Site(a.slug)
    if s.exists() and not a.force:
        die(f"{a.slug} already exists at {s.dir} (use --force to recreate the database)")
    s.create(a.name)
    if a.from_:
        import shutil
        shutil.copytree(a.from_, s.src, dirs_exist_ok=True)
    url = s.serve()
    print(f"created {a.slug}: {url}  (folder {s.dir})")


def cmd_build(a):
    from build import build
    s = Site(a.slug)
    if not s.exists():
        src = s.src / "site.json"
        if not src.exists():
            die(f"no site '{a.slug}'. Run: zs new {a.slug} \"<name>\"")
        # Fresh machine or reclaimed cloud VM: WordPress is rebuilt from the committed source.
        print(f"recreating the local WordPress for {a.slug} from sites/{a.slug}/site.json …")
        s.create(json.loads(src.read_text(encoding="utf-8"))["business"]["name"])
    build(s)
    print("built:", s.serve())


def cmd_serve(a):
    print(Site(a.slug).serve())


def cmd_stop(a):
    Site(a.slug).stop()
    print("stopped")


def cmd_shots(a):
    from qa import screenshots
    if getattr(a, "site", None):
        s = _remote(a)       # the pushed site itself -> work/<slug>@<host>/shots/
    else:
        s = Site(a.slug)
        s.serve()
    for f in screenshots(s, a.paths or ["/"], directions=a.directions, mobile_only=a.mobile):
        print(f)


def cmd_preview(a):
    from qa import preview
    s = Site(a.slug)
    s.serve()
    print(preview(s))
    import json as _j
    from pool import check_measured
    pf = s.src / "preview" / "fingerprints.json"
    fps = {f"direction {k}": v for k, v in _j.loads(pf.read_text(encoding="utf-8")).items()} if pf.exists() else {}
    lines = check_measured(a.slug, fps)
    if lines:
        print("\n".join(lines))
    if getattr(s, "_preview_close", None) or any(x.startswith("ERROR") for x in lines):
        sys.exit(2)


def cmd_image(a):
    from aiimage import generate
    s = Site(a.slug)
    out = s.src / "assets" / f"{a.key}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    generate(a.prompt, out, a.size)
    print(f"{out}\nadd to site.json images: \"{a.key}\": {{\"src\": \"assets/{a.key}.png\", \"alt\": \"<what it shows, in Hebrew>\", \"ai\": true}}")


STAGING_HOSTS = (".ussl.co.il", ".zapsites.co.il", "127.0.0.1", "localhost")


def _remote(a):
    from remote import NovamiraSite, NovamiraError
    try:
        return NovamiraSite(a.slug, a.site, cred_file=a.cred_file)
    except NovamiraError as e:
        die(str(e))


def cmd_connect(a):
    from remote import connect, NovamiraError
    try:
        f = connect(a.site, say=lambda m: print(m, flush=True))
    except NovamiraError as e:
        die(str(e))
    print(f"connected: token stored for this machine only ({f.name}, not committed). Next: zs push <slug> --site {a.site}")


def _uniqueness_gate(slug):
    """No site ships looking like another client's: the measured home (zs qa) against every known client."""
    import json as _j
    from pool import check_measured
    src = ROOT / "sites" / slug
    f = src / "fingerprint.json"
    if not f.exists():
        die(f"{slug}: no measured layout (sites/{slug}/fingerprint.json). Run `zs qa {slug}` on the local build first.")
    fp = _j.loads(f.read_text(encoding="utf-8"))
    if "palette" not in fp:
        die(f"{slug}: the measured layout is from an older measure. Run `zs qa {slug}` again.")
    errs = [w for w in check_measured(slug, {"home": fp}) if w.startswith("ERROR")]
    if errs and os.environ.get("ZS_ALLOW_SIMILAR") != "1":
        die("\n".join(errs) + "\nThis site reads as another client's. Redesign it (references/pool.md), or, only with the user's "
            "explicit approval, set ZS_ALLOW_SIMILAR=1.")


def cmd_push(a):
    """Build site.json directly into a client WordPress through Novamira: backup -> code -> content -> cleanup."""
    from build import build, load_site
    from remote import NovamiraError
    _uniqueness_gate(a.slug)
    r = _remote(a)
    r.full = a.full      # --full: resend code, files and pages even if the server already has them
    live = not any(r.host == h.lstrip(".") or r.host.endswith(h) for h in STAGING_HOSTS)
    if live and not a.live:
        die(f"{r.host} is not a staging host. Push to staging first; a live domain needs --live and the user's explicit go-ahead.")
    try:
        facts = r.check()
        print(f"connected: {facts['home']} · WP {facts['wp']} · PHP {facts['php']} · Elementor {facts['elementor']}"
              f"{' + Pro ' + facts['elementor_pro'] if facts.get('elementor_pro') else ''} · theme {facts['theme']} · env {facts['env']}")
        data = load_site(r.src)
        other = r.eval_php("$o = get_option('zap_site'); echo is_array($o) ? ($o['business']['name'] ?? '') : '';").strip()
        if other and other != data["business"]["name"] and not a.force:
            die(f"this site already holds '{other}', not '{data['business']['name']}'. Wrong site? (--force to overwrite)")
        if not other:   # remember the base's own front page: the only page the first push may move to draft
            r.eval_php("update_option('zs_prev_front', (int) get_option('page_on_front')); echo 1;")
        if not a.no_backup:
            print("backup:", r.backup())
        # staging lock: leads are saved but never mailed to the real client, search engines stay out
        r.eval_php(f"update_option('zs_staging_lock', {0 if a.live else 1}); echo 1;")
        build(r)
        if not other:
            # first push into a fresh base clone: the base's own placeholder pages/posts (not built from site.json)
            # go to draft so they are not live next to the client's site. Later pushes never touch unknown pages.
            moved = r.eval_php("$m = []; foreach (get_posts(['post_type'=>['page','post'],'post_status'=>'publish','numberposts'=>-1]) as $p) {"
                               " $front = (int) get_option('zs_prev_front'); if (($p->ID === $front && !get_post_meta($p->ID, '_zs_key', true)) || in_array($p->post_name, ['sample-page', 'hello-world'], true)) {"
                               " wp_update_post(['ID'=>$p->ID,'post_status'=>'draft']); $m[] = $p->ID . ' ' . $p->post_title; } } echo implode(' | ', $m);").strip()
            if moved:
                print("base placeholders moved to draft:", moved)
        if not a.live:
            r.eval_php("update_option('blog_public', 0); echo 1;")
        home = r.eval_php("echo (int) get_option('page_on_front');").strip()
        print(f"\nsite:      {r.url}/")
        print(f"edit home: {r.url}/wp-admin/post.php?post={home}&action=elementor")
        print(f"header/footer: {r.url}/wp-admin/edit.php?post_type=elementor_library")
        print(f"Novamira:  {r.url}/wp-admin/admin.php?page=novamira-connect")
    except NovamiraError as e:
        die(str(e))
    finally:
        try:
            r.cleanup()
        except Exception:
            pass


def cmd_static(a):
    from static import export
    s = Site(a.slug)
    s.serve()
    z, n = export(s)
    print(f"{n} pages -> {z}")


def cmd_grab(a):
    from grab import grab
    print(grab(Site(a.slug), a.url, a.pages))


def cmd_fetch_image(a):
    """Download a generated asset (e.g. a Weave run output URL) into sites/<slug>/assets/."""
    import urllib.request
    s = Site(a.slug)
    ext = a.ext or (a.url.split("?")[0].rsplit(".", 1)[-1].lower() if "." in a.url.split("?")[0].rsplit("/", 1)[-1] else "png")
    out = s.src / "assets" / f"{a.key}.{ext}"
    out.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(a.url, headers={"User-Agent": "zap-site-builder"})
    out.write_bytes(urllib.request.urlopen(req, timeout=300).read())
    print(f"{out} ({out.stat().st_size // 1024} KB)")


def cmd_doctor(a):
    import shutil
    import subprocess
    from env import php_bin, wp_cmd, ensure_db, run
    ok = True
    def line(name, good, detail=""):
        nonlocal ok
        ok &= bool(good)
        print(f"{'OK  ' if good else 'FAIL'} {name} {detail}")
    r = run([php_bin(), "-r", "echo PHP_VERSION, ' ', implode(',', array_intersect(['mysqli','gd','mbstring','zip','intl','curl'], get_loaded_extensions()));"], check=False)
    line("php", r.returncode == 0, r.stdout.strip())
    r = run(wp_cmd() + ["--version"], check=False)
    line("wp-cli", r.returncode == 0, r.stdout.strip())
    try:
        ensure_db()
        line("mariadb", True)
    except SystemExit:
        line("mariadb", False, "not running / not installed")
    try:
        import PIL
        line("pillow", True, PIL.__version__)
    except ImportError:
        line("pillow", False)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            from qa import _launch
            _launch(p).close()
        line("playwright browser", True)
    except Exception as e:
        line("playwright browser", False, str(e)[:80])
    import urllib.request
    try:
        urllib.request.urlopen("https://api.wordpress.org/core/version-check/1.7/", timeout=10)
        line("network: wordpress.org", True)
    except Exception as e:
        line("network: wordpress.org", False, f"{e} (set the environment's network access to Full)")
    gh = shutil.which("gh") is not None and subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0
    print(f"OK   publish route: {'GitHub release (gh)' if gh else 'delivery branch via git push (no gh needed)'}")
    sys.exit(0 if ok else 1)


def cmd_qa(a):
    from qa import run_qa
    if getattr(a, "site", None):
        s = _remote(a)       # QA the pushed site itself -> sites/<slug>/QA-REPORT-live.md
    else:
        s = Site(a.slug)
        s.serve()
    ok = run_qa(s)
    if not getattr(a, "site", None):   # the measured layout of the home page, for zs pool (committed with the site)
        import json as _j
        from fingerprint import take
        fp = take({"home": s.url + "/"})["home"]
        (s.src / "fingerprint.json").write_text(_j.dumps(fp, ensure_ascii=False), encoding="utf-8")
        from pool import check_measured
        lines = check_measured(a.slug, {"home": fp})
        if lines:
            print("\n".join(lines))
        if any(x.startswith("ERROR") for x in lines):   # a site that reads as another client's is not done
            ok = False
    sys.exit(0 if ok else 2)


def cmd_package(a):
    from package import package
    _uniqueness_gate(a.slug)
    print(package(Site(a.slug), a.domain))


def cmd_publish(a):
    from publish import publish
    print(publish(Site(a.slug)))


def cmd_list(a):
    for d in sorted((ROOT / "sites").glob("*/site.json")):
        s = Site(d.parent.name)
        print(f"{s.slug:24} {s.url:28} {'running' if s.running() else 'stopped'}")


def cmd_seo(a):
    from seo import run_seo
    s = Site(a.slug)
    s.serve()
    sys.exit(0 if run_seo(s) else 2)


def cmd_registry(a):
    """Measure the local build of <slug> and store it in fingerprints/<slug>.json (the registry every new site is
    compared with). Old sites that no longer pass today's validator: ZS_MEASURE_ONLY=1 zs build <slug> first."""
    import json as _j
    from fingerprint import take
    s = Site(a.slug)
    s.serve()
    fp = take({"home": s.url + "/"})["home"]
    out = ROOT / "fingerprints" / f"{a.slug}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(_j.dumps(fp, ensure_ascii=False), encoding="utf-8")
    print(out)


def cmd_pool(a):
    from build import load_site
    from pool import compare, recipe
    s = Site(a.slug)
    d = load_site(s.src)
    r = recipe(d)
    print("levers:", " · ".join(x or "-" for x in r["levers"]), f"· base template {r['base'] or '-'}")
    print("home:  ", " → ".join(r["home"]))
    warns = compare(a.slug, d, s.src)
    print("\n".join(warns) if warns else "unique: no other client branch is close (git fetch first for the latest)")
    sys.exit(2 if any(w.startswith("ERROR") for w in warns) else 0)


def main():
    p = argparse.ArgumentParser(prog="zs", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("new"); x.add_argument("slug"); x.add_argument("name"); x.add_argument("--force", action="store_true"); x.add_argument("--from", dest="from_", help="copy site.json + assets from this folder"); x.set_defaults(f=cmd_new)
    x = sub.add_parser("build"); x.add_argument("slug"); x.set_defaults(f=cmd_build)
    x = sub.add_parser("serve"); x.add_argument("slug"); x.set_defaults(f=cmd_serve)
    x = sub.add_parser("stop"); x.add_argument("slug"); x.set_defaults(f=cmd_stop)
    x = sub.add_parser("shots"); x.add_argument("slug"); x.add_argument("paths", nargs="*", help='"/", "/<page>/" or "all"')
    x.add_argument("--directions", action="store_true"); x.add_argument("--mobile", action="store_true"); x.add_argument("--site"); x.add_argument("--cred-file"); x.set_defaults(f=cmd_shots)
    x = sub.add_parser("qa"); x.add_argument("slug"); x.add_argument("--site"); x.add_argument("--cred-file"); x.set_defaults(f=cmd_qa)
    x = sub.add_parser("connect"); x.add_argument("--site", required=True); x.set_defaults(f=cmd_connect)
    x = sub.add_parser("push"); x.add_argument("slug"); x.add_argument("--site", required=True); x.add_argument("--cred-file")
    x.add_argument("--live", action="store_true"); x.add_argument("--force", action="store_true"); x.add_argument("--full", action="store_true"); x.add_argument("--no-backup", action="store_true"); x.set_defaults(f=cmd_push)
    x = sub.add_parser("preview"); x.add_argument("slug"); x.set_defaults(f=cmd_preview)
    x = sub.add_parser("doctor"); x.set_defaults(f=cmd_doctor)
    x = sub.add_parser("static"); x.add_argument("slug"); x.set_defaults(f=cmd_static)
    x = sub.add_parser("grab"); x.add_argument("slug"); x.add_argument("url"); x.add_argument("--pages", type=int, default=25); x.set_defaults(f=cmd_grab)
    x = sub.add_parser("fetch-image"); x.add_argument("slug"); x.add_argument("key"); x.add_argument("url"); x.add_argument("--ext"); x.set_defaults(f=cmd_fetch_image)
    x = sub.add_parser("image");x.add_argument("slug"); x.add_argument("key"); x.add_argument("prompt"); x.add_argument("--size", default="1536x1024"); x.set_defaults(f=cmd_image)
    x = sub.add_parser("package"); x.add_argument("slug"); x.add_argument("--domain", required=True); x.set_defaults(f=cmd_package)
    x = sub.add_parser("publish"); x.add_argument("slug"); x.set_defaults(f=cmd_publish)
    x = sub.add_parser("list"); x.set_defaults(f=cmd_list)
    x = sub.add_parser("seo"); x.add_argument("slug"); x.set_defaults(f=cmd_seo)
    x = sub.add_parser("pool"); x.add_argument("slug"); x.set_defaults(f=cmd_pool)
    x = sub.add_parser("registry"); x.add_argument("slug"); x.set_defaults(f=cmd_registry)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

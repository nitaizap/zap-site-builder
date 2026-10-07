"""zs: build a Zap client site from site.json, test it, and ship it as an upload-ready zip.

  zs new <slug> "<business name>"   create the site folder + a local WordPress
  zs build <slug>                   apply work/<slug>/site.json (idempotent)
  zs serve <slug> | zs stop <slug>  local web server (http://127.0.0.1:<port>)
  zs shots <slug> [paths...]        screenshots desktop + mobile (+ design directions)
  zs preview <slug>                 home page under every design direction -> sites/<slug>/preview/PREVIEW.md
  zs qa <slug>                      measured QA sweep -> sites/<slug>/QA-REPORT.md
  zs doctor                         check php, wp-cli, mariadb, browser, network, gh
  zs image <slug> <key> "<prompt>"  AI atmosphere image -> sites/<slug>/assets/<key>.png (needs OPENAI_API_KEY)
  zs package <slug> --domain https://client.co.il
  zs publish <slug>                 upload the zip as a GitHub release asset (+ SharePoint if set)
  zs list                           sites on this machine
"""
import argparse
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
    s = Site(a.slug)
    s.serve()
    for f in screenshots(s, a.paths or ["/"], directions=a.directions):
        print(f)


def cmd_preview(a):
    from qa import preview
    s = Site(a.slug)
    s.serve()
    print(preview(s))


def cmd_image(a):
    from aiimage import generate
    s = Site(a.slug)
    out = s.src / "assets" / f"{a.key}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    generate(a.prompt, out, a.size)
    print(f"{out}\nadd to site.json images: \"{a.key}\": {{\"src\": \"assets/{a.key}.png\", \"alt\": \"<what it shows, in Hebrew>\", \"ai\": true}}")


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
    line("gh (for publish)", shutil.which("gh") is not None and subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0,
         "" if shutil.which("gh") else "not installed")
    sys.exit(0 if ok else 1)


def cmd_qa(a):
    from qa import run_qa
    s = Site(a.slug)
    s.serve()
    ok = run_qa(s)
    sys.exit(0 if ok else 2)


def cmd_package(a):
    from package import package
    print(package(Site(a.slug), a.domain))


def cmd_publish(a):
    from publish import publish
    print(publish(Site(a.slug)))


def cmd_list(a):
    for d in sorted((ROOT / "sites").glob("*/site.json")):
        s = Site(d.parent.name)
        print(f"{s.slug:24} {s.url:28} {'running' if s.running() else 'stopped'}")


def main():
    p = argparse.ArgumentParser(prog="zs", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("new"); x.add_argument("slug"); x.add_argument("name"); x.add_argument("--force", action="store_true"); x.add_argument("--from", dest="from_", help="copy site.json + assets from this folder"); x.set_defaults(f=cmd_new)
    x = sub.add_parser("build"); x.add_argument("slug"); x.set_defaults(f=cmd_build)
    x = sub.add_parser("serve"); x.add_argument("slug"); x.set_defaults(f=cmd_serve)
    x = sub.add_parser("stop"); x.add_argument("slug"); x.set_defaults(f=cmd_stop)
    x = sub.add_parser("shots"); x.add_argument("slug"); x.add_argument("paths", nargs="*"); x.add_argument("--directions", action="store_true"); x.set_defaults(f=cmd_shots)
    x = sub.add_parser("qa"); x.add_argument("slug"); x.set_defaults(f=cmd_qa)
    x = sub.add_parser("preview"); x.add_argument("slug"); x.set_defaults(f=cmd_preview)
    x = sub.add_parser("doctor"); x.set_defaults(f=cmd_doctor)
    x = sub.add_parser("image"); x.add_argument("slug"); x.add_argument("key"); x.add_argument("prompt"); x.add_argument("--size", default="1536x1024"); x.set_defaults(f=cmd_image)
    x = sub.add_parser("package"); x.add_argument("slug"); x.add_argument("--domain", required=True); x.set_defaults(f=cmd_package)
    x = sub.add_parser("publish"); x.add_argument("slug"); x.set_defaults(f=cmd_publish)
    x = sub.add_parser("list"); x.set_defaults(f=cmd_list)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

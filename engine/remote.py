"""A client WordPress reached through Novamira (novamira.ai): the same build, run on the real server.

Novamira is a WordPress plugin that exposes "abilities" over REST/MCP. The free plugin is enough:
  novamira/execute-php     PHP inside WordPress (30 s per call)  -> eval_php()
  novamira/run-wp-cli      wp ... on the server                  -> wp()
  novamira/create-upload-link  temporary PUT URL for any file    -> put()
REST runner: POST <site>/wp-json/novamira/v1/abilities/<ability>/run  {"input": {...}}, authenticated as an
administrator with a WordPress Application Password.

Credentials are never printed, logged or committed. Lookup order:
  ZS_NOVAMIRA_<HOST>   e.g. ZS_NOVAMIRA_MEHIRUTHAOR_USSL_CO_IL="user:app-password"   (one site)
  ZS_NOVAMIRA          "user:app-password"   (Zap's integration user, cloned with the base site to every client)
  a JSON file {"user":..., "app_password":...} passed explicitly (local tests only)
"""
import base64
import json
import os
import re
import secrets
import shutil
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

from env import ROOT, WORK, WP_SRC

LOCAL_HOSTS = ("127.0.0.1", "localhost")


class NovamiraError(RuntimeError):
    pass


def find_credential(url, cred_file=None):
    host = urllib.parse.urlsplit(url).hostname or ""
    for name in ("ZS_NOVAMIRA_" + re.sub(r"[^A-Z0-9]", "_", host.upper()), "ZS_NOVAMIRA"):
        v = os.environ.get(name, "")
        if ":" in v:
            user, pw = v.split(":", 1)
            return user.strip(), pw.strip(), name
    if cred_file:
        d = json.loads(Path(cred_file).read_text(encoding="utf-8"))
        return d["user"], d["app_password"], "file"
    return None


class NovamiraSite:
    """Duck-types wpsite.Site for build(), qa and push: url, src, dir, wp(), eval_php(), put(), install_code()."""

    remote = True

    def __init__(self, slug, url, cred_file=None):
        self.slug = slug
        self.src = ROOT / "sites" / slug
        self.url = url.rstrip("/")
        self.host = urllib.parse.urlsplit(self.url).hostname or ""
        self.dir = WORK / f"{slug}@{re.sub(r'[^a-z0-9.-]', '-', self.host)}"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.qa_report = "QA-REPORT-live.md"
        cred = find_credential(self.url, cred_file)
        if not cred:
            raise NovamiraError(
                f"no Novamira credential for {self.host}. Set ZS_NOVAMIRA (or ZS_NOVAMIRA_<HOST>) to "
                "'user:application-password' in the environment's secrets; see references/novamira.md")
        user, pw, self.cred_source = cred
        self._auth = "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode()
        local = self.host in LOCAL_HOSTS
        self._open = urllib.request.build_opener(urllib.request.ProxyHandler({}) if local else urllib.request.ProxyHandler()).open
        self._tmp = "wp-content/zs-push/" + secrets.token_hex(6)   # per run, removed by cleanup()
        self._uploaded = {}

    # ---------- transport ----------
    def _post(self, path, body, headers=None, method="POST", timeout=180):
        req = urllib.request.Request(self.url + path, data=body, method=method,
                                     headers={"Authorization": self._auth, **(headers or {})})
        try:
            with self._open(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def ability(self, name, inp, timeout=180):
        st, raw = self._post(f"/wp-json/novamira/v1/abilities/{name}/run",
                             json.dumps({"input": inp}, ensure_ascii=False).encode("utf-8"),
                             {"Content-Type": "application/json"}, timeout=timeout)
        try:
            data = json.loads(raw.decode("utf-8", "replace"))
        except ValueError:
            raise NovamiraError(f"{name}: HTTP {st}, not JSON: {raw[:200]!r}")
        if st == 401:
            raise NovamiraError("401: the credential was refused (wrong user/application password, or a security plugin blocks REST auth)")
        if st == 403 and isinstance(data, dict) and data.get("code") == "novamira_disabled":
            raise NovamiraError("Novamira AI Abilities are switched off on this site (Novamira -> Configuration -> Enable). "
                                "They are locked to the domain they were enabled on, so a cloned site needs it once.")
        if st >= 400:
            raise NovamiraError(f"{name}: HTTP {st}: {str(data)[:300]}")
        return data

    def check(self):
        """Reachable, authenticated, abilities on. Returns facts about the site (no secrets)."""
        r = self.eval_php("echo wp_json_encode(['home'=>home_url(),'wp'=>get_bloginfo('version'),'php'=>PHP_VERSION,"
                          "'theme'=>get_stylesheet(),'template'=>get_template(),'env'=>wp_get_environment_type(),"
                          "'elementor'=>defined('ELEMENTOR_VERSION')?ELEMENTOR_VERSION:null,"
                          "'elementor_pro'=>defined('ELEMENTOR_PRO_VERSION')?ELEMENTOR_PRO_VERSION:null,"
                          "'plugins'=>array_values(get_option('active_plugins',[]))]);")
        return json.loads(r.strip().splitlines()[-1])

    # ---------- the Site interface ----------
    def eval_php(self, code):
        code = re.sub(r"^\s*<\?php", "", code)
        r = self.ability("novamira/execute-php", {"code": code})
        if not r.get("success", False):
            errs = "; ".join(f"{e.get('message')} ({Path(str(e.get('file', ''))).name}:{e.get('line')})" for e in r.get("errors", [])[:3])
            raise NovamiraError(f"execute-php failed: {r.get('error_message') or errs or str(r)[:300]}")
        out = r.get("output", "") or ""
        rv = r.get("return_value")
        if isinstance(rv, str) and rv:
            out += rv
        return out

    def wp(self, *args, check=True, input=None):
        r = self.ability("novamira/run-wp-cli", {"args": [str(a) for a in args]}, timeout=600)
        if check and r.get("exit_code") not in (0, None):
            raise NovamiraError(f"wp {' '.join(map(str, args[:3]))} failed ({r.get('exit_code')}): {(r.get('stderr') or '')[-300:]}")
        return (r.get("stdout") or "").strip()

    def put(self, local, name=None):
        """Upload a local file into this run's temp folder on the server; returns the absolute server path."""
        local = Path(local)
        key = (str(local), local.stat().st_mtime, local.stat().st_size)
        if key in self._uploaded:
            return self._uploaded[key]
        dest = f"{self._tmp}/{name or local.name}"
        link = self.ability("novamira/create-upload-link", {"path": dest, "overwrite": True, "create_directories": True,
                                                             "expires_in": 900, "max_bytes": max(1024, local.stat().st_size + 1024)})
        st, raw = self._post_url(link["upload_url"], local.read_bytes(), {link.get("token_header", "X-Novamira-Upload-Token"): link["upload_token"],
                                                                          "Content-Type": "application/octet-stream"}, method=link.get("method", "PUT"))
        if st >= 300:
            raise NovamiraError(f"upload of {local.name} failed: HTTP {st} {raw[:200]!r}")
        self._uploaded[key] = link["path"]
        return link["path"]

    def _post_url(self, url, body, headers, method="PUT"):
        req = urllib.request.Request(url, data=body, method=method, headers=headers)   # the upload token is the auth
        try:
            with self._open(req, timeout=600) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def install_code(self):
        """Our child theme + plugin onto the server (replaced in place), and the stack they need. Idempotent."""
        tmp = Path(tempfile.mkdtemp(dir=self.dir))
        try:
            for kind, src in (("themes", WP_SRC / "theme" / "zap-base"), ("plugins", WP_SRC / "plugin" / "zap-site")):
                z = tmp / f"{src.name}.zip"
                with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
                    for f in src.rglob("*"):
                        if f.is_file():
                            zf.write(f, f"{src.name}/{f.relative_to(src).as_posix()}")
                remote_zip = self.put(z)
                self.eval_php(f"""
require_once ABSPATH . 'wp-admin/includes/file.php';
WP_Filesystem();
$dest = WP_CONTENT_DIR . '/{kind}';
$dir = $dest . '/{src.name}';
if (is_dir($dir)) {{ global $wp_filesystem; $wp_filesystem->delete($dir, true); }}
$r = unzip_file({json.dumps(remote_zip)}, $dest);
if (is_wp_error($r)) throw new Exception('unzip {src.name}: ' . $r->get_error_message());
echo '{src.name} installed';
""")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        have = self.check()
        for p in ("elementor", "wordpress-seo", "pojo-accessibility"):
            if not any(a.startswith(p + "/") for a in have["plugins"]):
                self.wp("plugin", "install", p, "--activate")
        if "hello-elementor" not in self.wp("theme", "list", "--field=name"):
            self.wp("theme", "install", "hello-elementor")
        self.wp("theme", "activate", "zap-base")
        self.wp("plugin", "activate", "zap-site")

    def backup(self):
        """Database dump of the server, saved on THIS machine before anything is written (Novamira has no rollback)."""
        dump = f"{self._tmp}/backup.sql"
        self.eval_php(f"if (!is_dir(ABSPATH . {json.dumps(self._tmp)})) wp_mkdir_p(ABSPATH . {json.dumps(self._tmp)}); echo 1;")
        self.wp("db", "export", dump, "--add-drop-table")
        out = self.dir / f"backup-{__import__('time').strftime('%Y%m%d-%H%M%S')}.sql.gz"
        b64 = self.eval_php(f"$f = ABSPATH . {json.dumps(dump)}; echo base64_encode(gzencode(file_get_contents($f), 6)); @unlink($f);")
        out.write_bytes(base64.b64decode(b64.strip()))
        return out

    def cleanup(self):
        self.eval_php(f"require_once ABSPATH . 'wp-admin/includes/file.php'; WP_Filesystem(); global $wp_filesystem;"
                      f"$d = ABSPATH . {json.dumps(self._tmp)}; if (is_dir($d)) $wp_filesystem->delete($d, true); echo 1;")

    def serve(self):
        return self.url

    def exists(self):
        return True

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


TOKENS = WORK / "novamira-tokens"   # OAuth tokens from `zs connect` (work/ is never committed); chmod 600
DEVICE_GRANT = "urn:ietf:params:oauth:grant-type:device_code"


def _token_file(host):
    return TOKENS / f"{re.sub(r'[^a-z0-9.-]', '-', host)}.json"


def _form_post(url, fields, local):
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}) if local else urllib.request.ProxyHandler())
    req = urllib.request.Request(url, data=urllib.parse.urlencode(fields).encode(), method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"})
    try:
        with op.open(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except ValueError:
            return e.code, {}
    except (urllib.error.URLError, OSError, TimeoutError) as e:   # dropped connection: the caller retries
        return 0, {"error": "network", "error_description": str(e)[:120]}


def connect(url, wait=900, say=print):
    """OAuth device flow: an administrator approves this machine once in wp-admin; no password is ever typed here."""
    import time
    url = url.rstrip("/")
    host = urllib.parse.urlsplit(url).hostname or ""
    local = host in LOCAL_HOSTS
    base = url + "/wp-json/novamira/v1/oauth"
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}) if local else urllib.request.ProxyHandler())
    reg = urllib.request.Request(base + "/register", method="POST", headers={"Content-Type": "application/json"},
                                 data=json.dumps({"client_name": "Zap site builder (Claude Code)", "grant_types": [DEVICE_GRANT],
                                                  "redirect_uris": [], "token_endpoint_auth_method": "none"}).encode())
    try:
        client_id = json.loads(op.open(reg, timeout=60).read())["client_id"]
    except urllib.error.HTTPError as e:
        raise NovamiraError(f"client registration refused: HTTP {e.code} {e.read()[:200]!r}")
    st, dev = _form_post(base + "/device", {"client_id": client_id, "scope": "mcp"}, local)
    if st != 200:
        raise NovamiraError(f"device authorization refused: HTTP {st} {dev}")
    say(f"APPROVE: open {dev['verification_uri']} (logged in as an administrator) and enter the code  {dev['user_code']}")
    deadline, interval = time.time() + min(wait, dev.get("expires_in", 900)), max(2, int(dev.get("interval", 5)))
    while time.time() < deadline:
        time.sleep(interval)
        st, tok = _form_post(base + "/token", {"grant_type": DEVICE_GRANT, "device_code": dev["device_code"], "client_id": client_id}, local)
        if st == 200 and tok.get("access_token"):
            TOKENS.mkdir(parents=True, exist_ok=True)
            f = _token_file(host)
            f.write_text(json.dumps({"client_id": client_id, "access_token": tok["access_token"],
                                     "refresh_token": tok.get("refresh_token", ""), "expires_at": time.time() + int(tok.get("expires_in", 3600))}))
            f.chmod(0o600)
            return f
        err = tok.get("error", "")
        if err == "slow_down":
            interval += 5
        elif err == "network":
            continue                                   # transient reset/timeout while waiting: keep polling
        elif err not in ("authorization_pending", ""):
            raise NovamiraError(f"device flow ended: {err} {tok.get('error_description', '')}")
    raise NovamiraError("not approved in time; run zs connect again")


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
    if _token_file(host).exists():
        return None, None, "oauth"
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
                f"no Novamira credential for {self.host}. Run: zs connect --site {self.url}  (an administrator approves "
                "once in wp-admin), or set ZS_NOVAMIRA='user:application-password' in the environment's secrets")
        user, pw, self.cred_source = cred
        local = self.host in LOCAL_HOSTS
        self._local = local
        if self.cred_source == "oauth":
            self._auth = "Bearer " + self._oauth_token()
        else:
            self._auth = "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode()
        self._open = urllib.request.build_opener(urllib.request.ProxyHandler({}) if local else urllib.request.ProxyHandler()).open
        self._tmp = "wp-content/zs-push/" + secrets.token_hex(6)   # per run, removed by cleanup()
        self._uploaded = {}

    def _oauth_token(self, force_refresh=False):
        import time
        f = _token_file(self.host)
        d = json.loads(f.read_text())
        if force_refresh or time.time() > d.get("expires_at", 0) - 120:
            if not d.get("refresh_token"):
                raise NovamiraError("the Novamira token expired; run: zs connect --site " + self.url)
            st, tok = _form_post(self.url + "/wp-json/novamira/v1/oauth/token", {"grant_type": "refresh_token",
                                 "refresh_token": d["refresh_token"], "client_id": d["client_id"]}, self.host in LOCAL_HOSTS)
            if st != 200 or not tok.get("access_token"):
                raise NovamiraError("token refresh refused; run: zs connect --site " + self.url)
            d.update(access_token=tok["access_token"], refresh_token=tok.get("refresh_token", d["refresh_token"]),
                     expires_at=time.time() + int(tok.get("expires_in", 3600)))
            f.write_text(json.dumps(d)); f.chmod(0o600)
        return d["access_token"]

    # ---------- transport ----------
    def _post(self, path, body, headers=None, method="POST", timeout=180):
        """One REST call; dropped connections and gateway hiccups are retried (every build step is idempotent)."""
        import time
        for attempt in range(5):
            req = urllib.request.Request(self.url + path, data=body, method=method,
                                         headers={"Authorization": self._auth, **(headers or {})})
            try:
                with self._open(req, timeout=timeout) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as e:
                if e.code in (502, 503, 504) and attempt < 4:
                    time.sleep(2 * 2 ** attempt)
                    continue
                return e.code, e.read()
            except (urllib.error.URLError, ConnectionError, TimeoutError, OSError):
                if attempt == 4:
                    raise
                time.sleep(2 * 2 ** attempt)

    def ability(self, name, inp, timeout=180):
        st, raw = self._post(f"/wp-json/novamira/v1/abilities/{name}/run",
                             json.dumps({"input": inp}, ensure_ascii=False).encode("utf-8"),
                             {"Content-Type": "application/json"}, timeout=timeout)
        try:
            data = json.loads(raw.decode("utf-8", "replace"))
        except ValueError:
            raise NovamiraError(f"{name}: HTTP {st}, not JSON: {raw[:200]!r}")
        if st == 401 and self.cred_source == "oauth" and not getattr(self, "_refreshed", False):
            self._refreshed = True
            self._auth = "Bearer " + self._oauth_token(force_refresh=True)
            return self.ability(name, inp, timeout)
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
        """The few WP-CLI commands the engine uses, done in PHP: many managed hosts cannot run WP-CLI from PHP
        (no process spawning; Novamira's run-wp-cli then returns 500/502), but execute-php always works."""
        a = [str(x) for x in args]
        php = {
            ("rewrite", "flush"): "flush_rewrite_rules(true); echo 'ok';",
            ("elementor", "flush-css"): "if (class_exists('\\Elementor\\Plugin')) \\Elementor\\Plugin::$instance->files_manager->clear_cache(); echo 'ok';",
            ("cache", "flush"): "wp_cache_flush(); echo 'ok';",
            ("yoast", "index"): "echo 'skipped (Yoast builds indexables on first view)';",
        }.get(tuple(a[:2]))
        if php is None and a[:2] == ["post", "list"] and "--format=count" in a:
            t = next((x.split("=", 1)[1] for x in a if x.startswith("--post_type=")), "post")
            st = next((x.split("=", 1)[1] for x in a if x.startswith("--post_status=")), "publish")
            php = f"echo count(get_posts(['post_type'=>{json.dumps(t)},'post_status'=>{json.dumps(st)},'numberposts'=>-1,'fields'=>'ids']));"
        if php is None and a[:2] == ["theme", "activate"]:
            php = f"switch_theme({json.dumps(a[2])}); echo get_stylesheet();"
        if php is None and a[:2] == ["plugin", "activate"]:
            php = (f"$f = array_keys(array_filter(get_plugins(), fn($v,$k) => str_starts_with($k, {json.dumps(a[2] + '/')}), ARRAY_FILTER_USE_BOTH));"
                   "if (!$f) throw new Exception('plugin not installed'); $r = activate_plugin($f[0]); if (is_wp_error($r)) throw new Exception($r->get_error_message()); echo 'ok';")
        if php is None and a[:2] in (["plugin", "install"], ["theme", "install"]):
            kind, slug = a[0], a[2]
            php = (f"require_once ABSPATH.'wp-admin/includes/class-wp-upgrader.php'; require_once ABSPATH.'wp-admin/includes/plugin.php';"
                   f"require_once ABSPATH.'wp-admin/includes/plugin-install.php'; require_once ABSPATH.'wp-admin/includes/theme.php';"
                   f"$skin = new WP_Ajax_Upgrader_Skin();"
                   + (f"$api = plugins_api('plugin_information', ['slug'=>{json.dumps(slug)},'fields'=>['sections'=>false]]); $u = new Plugin_Upgrader($skin); $ok = $u->install($api->download_link);"
                      if kind == "plugin" else
                      f"$api = themes_api('theme_information', ['slug'=>{json.dumps(slug)}]); $u = new Theme_Upgrader($skin); $ok = $u->install($api->download_link);")
                   + "if (!$ok || is_wp_error($ok)) throw new Exception('install failed'); echo 'ok';")
            if "--activate" in a:
                php += f" activate_plugin(array_keys(array_filter(get_plugins(), fn($v,$k) => str_starts_with($k, {json.dumps(slug + '/')}), ARRAY_FILTER_USE_BOTH)))[0] ?? '');"
        if php is None and a[:2] == ["theme", "list"]:
            php = "echo implode(\"\\n\", array_keys(wp_get_themes()));"
        if php is None:
            r = self.ability("novamira/run-wp-cli", {"args": a}, timeout=600)   # anything else: real WP-CLI where the host allows it
            if check and r.get("exit_code") not in (0, None):
                raise NovamiraError(f"wp {' '.join(a[:3])} failed ({r.get('exit_code')}): {(r.get('stderr') or '')[-300:]}")
            return (r.get("stdout") or "").strip()
        try:
            return self.eval_php(php).strip()
        except NovamiraError:
            if check:
                raise
            return ""

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
        import time
        for attempt in range(5):
            req = urllib.request.Request(url, data=body, method=method, headers=headers)   # the upload token is the auth
            try:
                with self._open(req, timeout=600) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as e:
                if e.code in (502, 503, 504) and attempt < 4:
                    time.sleep(2 * 2 ** attempt)
                    continue
                return e.code, e.read()
            except (urllib.error.URLError, ConnectionError, TimeoutError, OSError):
                if attempt == 4:
                    raise
                time.sleep(2 * 2 ** attempt)

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
        """Full SQL dump of the server's database, built in PHP (no WP-CLI needed) table by table, page by page so
        every call stays far under the 30 s limit, and saved on THIS machine before anything is written."""
        import gzip, time
        tables = json.loads(self.eval_php("global $wpdb; echo wp_json_encode($wpdb->get_col('SHOW TABLES'));").strip().splitlines()[-1])
        out = self.dir / f"backup-{time.strftime('%Y%m%d-%H%M%S')}.sql.gz"
        with gzip.open(out, "wt", encoding="utf-8") as fh:
            fh.write("SET NAMES utf8mb4;\nSET FOREIGN_KEY_CHECKS=0;\n")
            for t in tables:
                head = json.loads(self.eval_php(
                    f"global $wpdb; $c = $wpdb->get_row('SHOW CREATE TABLE `{t}`', ARRAY_N); "
                    f"echo wp_json_encode(['create'=>$c[1], 'rows'=>(int) $wpdb->get_var('SELECT COUNT(*) FROM `{t}`')]);").strip().splitlines()[-1])
                fh.write(f"\nDROP TABLE IF EXISTS `{t}`;\n{head['create']};\n")
                page = 1500
                for off in range(0, head["rows"], page):
                    chunk = self.eval_php(
                        f"global $wpdb; $rows = $wpdb->get_results('SELECT * FROM `{t}` LIMIT {page} OFFSET {off}', ARRAY_A); $o = '';"
                        "foreach ($rows as $r) { $v = array_map(fn($x) => $x === null ? 'NULL' : \"'\" . $wpdb->remove_placeholder_escape($wpdb->_real_escape($x)) . \"'\", array_values($r));"
                        f" $o .= 'INSERT INTO `{t}` VALUES (' . implode(',', $v) . \");\\n\"; }}"
                        "echo base64_encode(gzencode($o, 6));")
                    fh.write(gzip.decompress(base64.b64decode(chunk.strip())).decode("utf-8"))
            fh.write("\nSET FOREIGN_KEY_CHECKS=1;\n")
        return out

    def cleanup(self):
        self.eval_php(f"require_once ABSPATH . 'wp-admin/includes/file.php'; WP_Filesystem(); global $wp_filesystem;"
                      f"$d = ABSPATH . {json.dumps(self._tmp)}; if (is_dir($d)) $wp_filesystem->delete($d, true); echo 1;")

    def serve(self):
        return self.url

    def exists(self):
        return True

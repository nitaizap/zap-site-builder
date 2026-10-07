"""One isolated WordPress per client: own folder, own database, own port."""
import json
import os
import secrets
import shutil
import signal
import subprocess
import time
import urllib.request
import zlib
from pathlib import Path

from env import (IS_WIN, ROOT, WORK, WP_SRC, ensure_db, DB_HOST, DB_PORT, DB_USER, DB_PASS,
                 php_bin, run, sql, wp_cmd)

PLUGINS = ["elementor", "wordpress-seo", "pojo-accessibility"]
ADMIN_USER = "zapadmin"
ADMIN_EMAIL = "zapsites@d.co.il"


class Site:
    def __init__(self, slug):
        if not slug.replace("-", "").isalnum() or slug != slug.lower():
            raise ValueError("slug must be lowercase latin letters, digits and dashes")
        self.slug = slug
        self.src = ROOT / "sites" / slug   # site.json, assets, reports: committed
        self.dir = WORK / slug              # WordPress runtime: rebuildable, never committed
        self.wp_dir = self.dir / "wp"
        self.db = "zs_" + slug.replace("-", "_")
        self.port = 8100 + zlib.crc32(slug.encode()) % 800
        self.url = f"http://127.0.0.1:{self.port}"
        self.pidfile = self.dir / "server.pid"

    # ---------- WP-CLI ----------
    def wp(self, *args, check=True, input=None):
        ensure_db()
        argv = wp_cmd() + [f"--path={self.wp_dir}", *map(str, args)]
        r = run(argv, check=check, input=input)
        return r.stdout.strip()

    def eval_php(self, code):
        """Run PHP inside WordPress. Code goes through a temp file: no shell quoting games."""
        f = self.dir / "_eval.php"
        f.write_text("<?php\n" + code, encoding="utf-8")
        try:
            return self.wp("eval-file", f)
        finally:
            f.unlink(missing_ok=True)

    # ---------- lifecycle ----------
    def exists(self):
        return (self.wp_dir / "wp-config.php").exists()

    def create(self, title, locale="he_IL"):
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.src / "assets").mkdir(parents=True, exist_ok=True)
        if not (self.wp_dir / "wp-load.php").exists():
            # Hebrew core packs lag behind releases (he_IL stopped at 6.2), so download en_US
            # core and add whatever language pack exists; the theme forces RTL either way.
            self.wp("core", "download", "--skip-content", "--force")
            (self.wp_dir / "wp-content" / "plugins").mkdir(parents=True, exist_ok=True)
            (self.wp_dir / "wp-content" / "themes").mkdir(parents=True, exist_ok=True)
            (self.wp_dir / "wp-content" / "uploads").mkdir(parents=True, exist_ok=True)
        sql(f"DROP DATABASE IF EXISTS `{self.db}`; CREATE DATABASE `{self.db}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        (self.wp_dir / "wp-config.php").unlink(missing_ok=True)
        cfg = ["config", "create", f"--dbname={self.db}", f"--dbuser={DB_USER}",
               f"--dbhost={DB_HOST}:{DB_PORT}", "--skip-check"]
        if DB_PASS:
            cfg.append(f"--dbpass={DB_PASS}")
        else:
            cfg.append("--dbpass=")
        self.wp(*cfg)
        self.wp("config", "set", "WP_ENVIRONMENT_TYPE", "staging")
        self.wp("config", "set", "DISALLOW_FILE_EDIT", "true", "--raw")
        self.wp("config", "set", "WP_POST_REVISIONS", "5", "--raw")
        pw = secrets.token_urlsafe(18)
        self.wp("core", "install", f"--url={self.url}", f"--title={title}",
                f"--admin_user={ADMIN_USER}", f"--admin_password={pw}",
                f"--admin_email={ADMIN_EMAIL}", "--skip-email")
        (self.dir / ".admin").write_text(pw, encoding="utf-8")   # local only, never zipped
        self.install_code()
        for p in PLUGINS:
            self.wp("plugin", "install", p, "--activate")
        self.wp("language", "core", "install", locale, check=False)
        self.wp("language", "plugin", "install", "--all", locale, check=False)
        self.wp("option", "update", "WPLANG", locale)
        self.wp("theme", "activate", "zap-base")
        self.wp("plugin", "activate", "zap-site")
        self.base_settings()

    def install_code(self):
        """Copy our theme + plugin from the repo (idempotent, run on every build)."""
        for src, dst in ((WP_SRC / "theme" / "zap-base", self.wp_dir / "wp-content/themes/zap-base"),
                         (WP_SRC / "plugin" / "zap-site", self.wp_dir / "wp-content/plugins/zap-site")):
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    def base_settings(self):
        o = {
            "permalink_structure": "/%postname%/",
            "timezone_string": "Asia/Jerusalem",
            "date_format": "d/m/Y",
            "blog_public": "0",                      # staging stays out of the index until launch
            "default_comment_status": "closed",
            "default_ping_status": "closed",
            "elementor_disable_color_schemes": "yes",
            "elementor_disable_typography_schemes": "yes",
            "elementor_google_font": "0",            # fonts are self-hosted by the theme
            "elementor_font_display": "swap",
            "elementor_load_fa4_shim": "",
            "elementor_unfiltered_files_upload": "",
            "elementor_onboarded": "1",
            "elementor_tracker_notice": "1",
            "elementor_allow_tracking": "no",
            "wpseo_titles_sep": "sc-pipe",
        }
        php = "foreach (json_decode(%s, true) as $k => $v) update_option($k, $v);\n" % _php_str(json.dumps(o))
        php += "update_option('elementor_cpt_support', ['page','post']);\n"
        php += "update_option('blogdescription', '');\n"
        php += "$h = get_page_by_path('sample-page'); if ($h) wp_delete_post($h->ID, true);\n"
        php += "wp_delete_post(1, true);\n"  # 'Hello world'
        php += "$pp = (int) get_option('wp_page_for_privacy_policy'); if ($pp) wp_delete_post($pp, true);\n"
        self.eval_php(php)
        self.wp("rewrite", "flush", "--hard", check=False)

    # ---------- local web server ----------
    def running(self):
        try:
            urllib.request.urlopen(self.url + "/wp-login.php", timeout=3)
            return True
        except Exception as e:  # HTTPError still means the server answered
            return hasattr(e, "code")

    def serve(self):
        if self.running():
            return self.url
        router = Path(__file__).with_name("router.php")
        log = open(self.dir / "server.log", "ab")
        kw = {}
        if IS_WIN:
            kw["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008  # DETACHED_PROCESS
        else:
            kw["start_new_session"] = True
        env = dict(os.environ, PHP_CLI_SERVER_WORKERS="4")
        p = subprocess.Popen([php_bin(), "-S", f"127.0.0.1:{self.port}", "-t", str(self.wp_dir), str(router)],
                             cwd=self.wp_dir, stdout=log, stderr=log, stdin=subprocess.DEVNULL, env=env, **kw)
        self.pidfile.write_text(str(p.pid))
        for _ in range(40):
            if self.running():
                return self.url
            time.sleep(0.25)
        raise RuntimeError(f"web server did not start on {self.url}; see {self.dir / 'server.log'}")

    def stop(self):
        if not self.pidfile.exists():
            return
        pid = int(self.pidfile.read_text())
        try:
            if IS_WIN:
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
            else:
                os.killpg(pid, signal.SIGTERM)
        except Exception:
            pass
        self.pidfile.unlink(missing_ok=True)


def _php_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"

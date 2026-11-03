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
    def wp(self, *args, check=True, input=None, _rc=False):
        ensure_db()
        argv = wp_cmd() + [f"--path={self.wp_dir}", *map(str, args)]
        r = run(argv, check=check, input=input)
        return (r.returncode, r.stdout.strip()) if _rc else r.stdout.strip()

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

    def _guard_port(self):
        if self._answers() and not self._own_pid_alive():
            raise RuntimeError(f"{self.url} is answered by a server that this checkout did not start (another clone or "
                               f"worktree serving '{self.slug}', sharing its database `{self.db}`): run "
                               f"`bin/zs stop {self.slug}` there, then try again")

    def create(self, title, locale="he_IL"):
        self._guard_port()   # before the database is dropped: it is shared by every checkout building this slug
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.src / "assets").mkdir(parents=True, exist_ok=True)
        if not (self.wp_dir / "wp-load.php").exists():
            # Hebrew core packs lag behind releases (he_IL stopped at 6.2), so download en_US
            # core and add the he_IL language pack on top. The pack is not optional: without it
            # WordPress refuses the WPLANG option and the site comes out en_US / LTR.
            # assert_locale() below proves it actually took.
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
        core_rc, _ = self.wp("language", "core", "install", locale, check=False, _rc=True)
        self.wp("language", "plugin", "install", "--all", locale, check=False)
        self.wp("option", "update", "WPLANG", locale)
        self.ensure_parent_theme()
        self.wp("theme", "activate", "zap-base")
        self.wp("plugin", "activate", "zap-site")
        self.assert_locale(locale, core_pack_rc=core_rc)
        self.base_settings()

    def assert_locale(self, locale, core_pack_rc=None):
        """Prove the site really is in `locale` and, for Hebrew, really renders RTL.

        Why the installer's exit code is not enough, measured on a real site: WordPress
        sanitizes the WPLANG option against get_available_languages(). Ask for a locale whose
        pack is not installed and `wp option update WPLANG he_IL` prints *Success* and changes
        nothing. So when `wp language core install he_IL` fails, the site silently stays en_US,
        get_locale() returns en_US, is_rtl() is false, and the whole page renders left to right.
        That is the PR #59 incident, and nothing in the exit codes shows it.

        This stops the build rather than warning. Every layout measurement (`zs qa`, the
        uniqueness fingerprint, the screenshots) on an LTR Hebrew site is meaningless, and the
        burger lands under the accessibility button. The engine runs unattended in cloud
        sessions, so a wrong-direction site that builds is worse than a build that stops: a
        person can ship the first one, and nobody can ship the second.

        A missing translation pack on a site whose locale *did* take is only a warning: the
        layout is right and just the WordPress chrome stays English.
        """
        state = json.loads(self.eval_php(
            "echo json_encode(['locale' => get_locale(), 'wplang' => (string) get_option('WPLANG'),"
            " 'rtl' => is_rtl(), 'installed' => array_values(get_available_languages())]);"))
        want_rtl = locale.startswith(("he", "ar", "fa", "ur"))
        if state["locale"] != locale or state["wplang"] != locale:
            cause = (f"`wp language core install {locale}` did not install the pack "
                     f"(exit {core_pack_rc}), so WordPress discarded the WPLANG option. Usually a "
                     f"failed or blocked download from downloads.wordpress.org; retry with network "
                     f"access." if locale not in state["installed"] else
                     "the pack is installed, so something else is overriding the locale (a WPLANG "
                     "constant in wp-config.php, or a plugin filtering 'locale').")
            raise RuntimeError(
                f"{self.slug}: the site did not come out in {locale} - WordPress reports locale "
                f"{state['locale']!r} (WPLANG option {state['wplang']!r}, is_rtl {state['rtl']}). "
                f"{cause} "
                f"Every layout measurement on this site would be meaningless and a Hebrew "
                f"site would render left to right end to end, so the build stops here instead of "
                f"handing over a site in the wrong language.")
        if want_rtl and not state["rtl"]:
            raise RuntimeError(
                f"{self.slug}: locale is {locale} but WordPress still renders left to right "
                f"(is_rtl() is false). A Hebrew site laid out LTR makes every measurement "
                f"meaningless and must never be shipped, so the build stops here. Check that the "
                f"zap-base theme is active and that its init RTL hook still runs.")
        if locale not in state["installed"]:
            why = "the download failed" if core_pack_rc else "WordPress.org has no pack for this core version"
            print(f"WARNING: {self.slug}: no {locale} translation pack is installed ({why}). "
                  f"The site is {locale} and renders RTL, so layout and measurements are valid, but "
                  f"WordPress and plugin strings stay in English. Hebrew core packs lag behind "
                  f"WordPress releases (he_IL stopped at 6.2), so this is expected on a current "
                  f"core; if it was a network failure, rebuild once the network is back.",
                  flush=True)

    def ensure_parent_theme(self):
        """Zap Base is a child of Hello Elementor (Zap's base theme): the parent must be installed."""
        if not (self.wp_dir / "wp-content/themes/hello-elementor/style.css").exists():
            self.wp("theme", "install", "hello-elementor")

    def install_code(self):
        """Copy our theme + plugin from the repo (idempotent, run on every build)."""
        if (self.wp_dir / "wp-load.php").exists():
            self.ensure_parent_theme()
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
    def _answers(self):
        try:
            urllib.request.urlopen(self.url + "/wp-login.php", timeout=3)
            return True
        except Exception as e:  # HTTPError still means the server answered
            return hasattr(e, "code")

    def _own_pid_alive(self):
        """The server this checkout started (pidfile) is still alive."""
        try:
            pid = int(self.pidfile.read_text())
        except Exception:
            return False
        if IS_WIN:
            r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
            return str(pid) in r.stdout
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def running(self):
        """Our own server answers. A server that answers on our port but was not started from this checkout
        (another clone or worktree building the same slug) is not ours: it serves another folder and database,
        so builds and QA would silently test the wrong site."""
        return self._answers() and self._own_pid_alive()

    def serve(self):
        if self.running():
            return self.url
        self._guard_port()
        router = Path(__file__).with_name("router.php")
        log = open(self.dir / "server.log", "ab")
        kw = {}
        if IS_WIN:
            kw["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008  # DETACHED_PROCESS
        else:
            kw["start_new_session"] = True
        # PHP notices from plugins go to server.log, never into the page (hosts hide them; on the page they break the layout QA)
        env = dict(os.environ, PHP_CLI_SERVER_WORKERS="4")
        p = subprocess.Popen([php_bin(), "-d", "display_errors=0", "-d", "log_errors=1", "-S", f"127.0.0.1:{self.port}", "-t", str(self.wp_dir), str(router)],
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

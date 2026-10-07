"""Where things live, and how to call PHP / WP-CLI / MariaDB on this machine.

Two runtimes are supported:
  * cloud  - Claude Code on the web (Ubuntu). php, mariadb and wp come from bin/setup-cloud.sh.
  * local  - a developer's Windows box with portable tools under .tools/ (gitignored).
"""
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"          # one folder per site, gitignored
DIST = ROOT / "dist"          # finished zips, gitignored
TOOLS = ROOT / ".tools"
WP_SRC = ROOT / "wp"          # our theme + plugin sources
IS_WIN = platform.system() == "Windows"

DB_HOST = os.environ.get("ZS_DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("ZS_DB_PORT", "3307" if IS_WIN else "3306"))
# Local Windows: portable MariaDB, root without password. Cloud: user created by bin/setup-cloud.sh.
DB_USER = os.environ.get("ZS_DB_USER", "root" if IS_WIN else "zs")
DB_PASS = os.environ.get("ZS_DB_PASS", "" if IS_WIN else "zs")


def _first(*cands):
    for c in cands:
        if c and Path(c).exists():
            return str(c)
    return None


def php_bin():
    return _first(TOOLS / "php" / "php.exe") if IS_WIN else (shutil.which("php") or "php")


def mariadb_dir():
    hits = sorted(TOOLS.glob("mariadb-*-winx64"))
    return hits[-1] if hits else None


def mysql_bin(name="mariadb"):
    if IS_WIN:
        d = mariadb_dir()
        return str(d / "bin" / f"{name}.exe") if d else name
    return shutil.which(name) or shutil.which(name.replace("mariadb", "mysql")) or name


def wp_cmd():
    """argv prefix for WP-CLI."""
    if IS_WIN:
        return [php_bin(), str(TOOLS / "wp-cli.phar")]
    w = shutil.which("wp")
    return [w] if w else [php_bin(), str(TOOLS / "wp-cli.phar")]


def run(argv, cwd=None, check=True, capture=True, env=None, input=None):
    e = dict(os.environ)
    # Root in the cloud sandbox: WP-CLI refuses root without this flag.
    e.setdefault("WP_CLI_ALLOW_ROOT", "1")
    if env:
        e.update(env)
    r = subprocess.run(argv, cwd=cwd, env=e, input=input, text=True,
                       capture_output=capture, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        msg = (r.stderr or "") + (r.stdout or "")
        raise RuntimeError(f"command failed ({r.returncode}): {' '.join(map(str, argv[:6]))}\n{msg[-3000:]}")
    return r


def db_argv(extra=()):
    a = [mysql_bin("mariadb"), f"-h{DB_HOST}", f"-P{DB_PORT}", f"-u{DB_USER}"]
    if DB_PASS:
        a.append(f"-p{DB_PASS}")
    return a + list(extra)


def sql(statement):
    ensure_db()
    return run(db_argv(["-N", "-e", statement])).stdout


_db_ok = False


def ensure_db():
    """Start MariaDB if it is not running (cloud snapshots restore files, not processes)."""
    global _db_ok
    if _db_ok:
        return
    if run(db_argv(["-e", "select 1"]), check=False).returncode == 0:
        _db_ok = True
        return
    import time
    if IS_WIN:
        d = mariadb_dir()
        if not d:
            die("portable MariaDB not found under .tools/ (see tools/setup-windows.sh)")
        data = TOOLS / "mdata"
        if not data.exists():
            run([str(d / "bin" / "mariadb-install-db.exe"), f"--datadir={data}", f"--port={DB_PORT}"])
        subprocess.Popen([str(d / "bin" / "mariadbd.exe"), f"--datadir={data}", f"--port={DB_PORT}", "--bind-address=127.0.0.1"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008)
    else:
        subprocess.run("service mariadb start || service mysql start || (mysqld_safe >/dev/null 2>&1 &)",
                       shell=True, capture_output=True)
    for _ in range(40):
        if run(db_argv(["-e", "select 1"]), check=False).returncode == 0:
            _db_ok = True
            return
        time.sleep(0.5)
    die("MariaDB is not running and could not be started. Cloud: run `bash bin/setup-cloud.sh`.")


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

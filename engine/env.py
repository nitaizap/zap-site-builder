"""Where things live, and how to call PHP / WP-CLI / MariaDB on this machine.

Two runtimes are supported:
  * cloud  - Claude Code on the web (Ubuntu). php, mariadb and wp come from bin/setup-cloud.sh.
  * local  - a developer's Windows box with portable tools under .tools/ (gitignored).
"""
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"          # one folder per site, gitignored
DIST = ROOT / "dist"          # finished zips, gitignored
TOOLS = ROOT / ".tools"
WP_SRC = ROOT / "wp"          # our theme + plugin sources
IS_WIN = platform.system() == "Windows"

# ------------------------------------------------- one checkout, its own port range and databases
# Several clones/worktrees of this repo live on one PC. They used to share one dev-server port range
# (8100..8899) and one database namespace (`zs_<slug>`), so two checkouts building the same slug
# fought over the same port and the same database on the same MariaDB.
#
# Everything below is derived from this checkout's own path, so it is stable across runs (a running
# server must stay findable) and different per checkout. The canonical checkout (~/zap-site-builder)
# and every non-Windows runtime (the cloud sandbox) keep exactly the numbers they used before, so a
# machine with a single checkout in the usual place sees no change at all.
PRIMARY_CHECKOUT = Path.home() / "zap-site-builder"


def _resolved(p):
    try:
        return str(Path(p).resolve()).casefold()
    except OSError:
        return str(p).casefold()


def _checkout_tag():
    """Empty for the canonical checkout (and off Windows), else 6 stable hex chars from this root."""
    if not IS_WIN or _resolved(ROOT) == _resolved(PRIMARY_CHECKOUT):
        return ""
    return hashlib.blake2b(_resolved(ROOT).encode("utf-8"), digest_size=8).hexdigest()[:6]


CHECKOUT_TAG = _checkout_tag()
PORT_SPAN = 800            # how many ports one checkout may pick from (the historical range size)
PORT_WINDOW = 39900        # 8100..47999: free ports, below the Windows ephemeral range (49152+)
# ZS_PORT_BASE pins the first port of the range; setting it to 8100 restores the old numbers.
PORT_BASE = int(os.environ.get("ZS_PORT_BASE") or 8100)
_PORT_BASE_PINNED = bool(os.environ.get("ZS_PORT_BASE"))


def site_port(slug):
    """The dev-server port this checkout uses for `slug`. Deterministic: same checkout, same port.

    The canonical checkout (and a pinned ZS_PORT_BASE) keeps the historical `base + crc32(slug) %
    800`. Any other checkout hashes its own tag together with the slug across the whole window, so
    two checkouts building the same slug land on different ports.
    """
    if CHECKOUT_TAG and not _PORT_BASE_PINNED:
        return PORT_BASE + zlib.crc32(f"{CHECKOUT_TAG}/{slug}".encode()) % PORT_WINDOW
    return PORT_BASE + zlib.crc32(slug.encode()) % PORT_SPAN


# `zs_<slug>` for the canonical checkout, `zs<tag>_<slug>` elsewhere. ZS_DB_PREFIX pins it.
DB_PREFIX = os.environ.get("ZS_DB_PREFIX") or (f"zs{CHECKOUT_TAG}_" if CHECKOUT_TAG else "zs_")


def db_name(slug):
    """The database this checkout uses for `slug`. Deterministic, and distinct per checkout."""
    return DB_PREFIX + slug.replace("-", "_")


DB_HOST = os.environ.get("ZS_DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("ZS_DB_PORT", "3307" if IS_WIN else "3306"))
# Local Windows: portable MariaDB, root without password. Cloud: user created by bin/setup-cloud.sh.
DB_USER = os.environ.get("ZS_DB_USER", "root" if IS_WIN else "zs")
DB_PASS = os.environ.get("ZS_DB_PASS", "" if IS_WIN else "zs")


# ------------------------------------------------- credentials set with setx, without a restart
# `setx ZS_WP_USER ...` writes the *user* environment; a process started before that never sees it,
# so `zs staging` and `zs doctor` reported the credentials missing all day although they were set.
# On Windows we fall back to the user-level value. Values are returned to the caller and copied into
# this process's own environment only: never printed, logged, written to disk, or put in an error.
WP_CREDENTIAL_VARS = ("ZS_WP_USER", "ZS_WP_PASSWORD")


def user_env(name):
    r"""The user-level (HKCU\Environment) value of `name` on Windows, else None. Read only.

    Any failure is "not set": nothing about the value, not even its length, ever leaves here.
    """
    if not IS_WIN:
        return None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
        value = str(value) if value is not None else ""
        return value or None
    except Exception:                                        # noqa: BLE001 - quiet "not set"
        return None


def env_value(name):
    """Process environment first, then (Windows) the user environment setx wrote."""
    return os.environ.get(name) or user_env(name)


def wp_credentials():
    """(user, password) for the staging login, or (None, None). Returned to the caller only."""
    user, password = env_value("ZS_WP_USER"), env_value("ZS_WP_PASSWORD")
    return (user, password) if user and password else (None, None)


def _adopt_user_credentials():
    """Make the setx values visible to everything that reads os.environ in this process."""
    for name in WP_CREDENTIAL_VARS:
        if not os.environ.get(name):
            value = user_env(name)
            if value:
                os.environ[name] = value


_adopt_user_credentials()


def _first(*cands):
    for c in cands:
        if c and Path(c).exists():
            return str(c)
    return None


# ---------------------------------------------------------------- missing tools
# A missing tool used to travel as None into subprocess.Popen and surface as
# "TypeError: expected str, bytes or os.PathLike object, not NoneType" from deep inside
# subprocess, naming nothing. These say what is missing, where we looked and how to get it.

_HOWTO = {
    "PHP": "unzip a portable PHP 8.x build (with the mysqli, gd, mbstring, zip, intl and curl "
           "extensions enabled in php.ini) so that php.exe sits at .tools/php/php.exe",
    "WP-CLI": "download https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar "
              "and save it as .tools/wp-cli.phar",
    "MariaDB": "unzip a portable MariaDB winx64 build into .tools/ so the folder is named "
               ".tools/mariadb-<version>-winx64 (its binaries live in that folder's bin/)",
}


def missing_tool(tool, looked, extra=""):
    """Stop with a message that names the tool, where we looked, and how to get it."""
    cands = [looked] if isinstance(looked, (str, Path)) else list(looked)
    where = "\n".join(f"    {x}" for x in cands)
    die(f"{tool} is not installed on this machine, so this command cannot run.\n"
        f"  looked for:\n{where}\n"
        f"  fix: {_HOWTO.get(tool, 'install ' + tool)}.\n"
        f"  .tools/ is gitignored and this repo ships no Windows installer for it "
        f"(bin/setup-cloud.sh is Ubuntu only).{extra}\n"
        f"  `bin/zs doctor` lists every tool at once.")


def php_path():
    """PHP if it is really there, else None. For probing (doctor); callers that need it use php_bin()."""
    return _first(TOOLS / "php" / "php.exe") if IS_WIN else shutil.which("php")


def php_bin():
    if not IS_WIN:
        return shutil.which("php") or "php"
    p = _first(TOOLS / "php" / "php.exe")
    if not p:
        missing_tool("PHP", TOOLS / "php" / "php.exe")
    return p


def wp_cli_phar():
    """The bundled WP-CLI phar if present, else None."""
    return _first(TOOLS / "wp-cli.phar")


def mariadb_dir():
    hits = sorted(TOOLS.glob("mariadb-*-winx64"))
    return hits[-1] if hits else None


def require_mariadb_dir():
    d = mariadb_dir()
    if not d:
        missing_tool("MariaDB", TOOLS / "mariadb-*-winx64")
    return d


def mysql_bin(name="mariadb"):
    if IS_WIN:
        return str(require_mariadb_dir() / "bin" / f"{name}.exe")
    return shutil.which(name) or shutil.which(name.replace("mariadb", "mysql")) or name


def wp_cmd():
    """argv prefix for WP-CLI."""
    if not IS_WIN:
        w = shutil.which("wp")
        if w:
            return [w]
    phar = wp_cli_phar()
    if not phar:
        missing_tool("WP-CLI", TOOLS / "wp-cli.phar")
    return [php_bin(), phar]


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
        d = require_mariadb_dir()
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

"""Read-only checks for the things that actually break the pipeline, beyond "is the binary there".

`zs doctor` used to check php / wp-cli / mariadb / pillow / playwright / network / publish route.
All of those were green on days when the pipeline was broken: Outlook closed so the intake read
nothing, the F: share unreachable so no client images, the staging credentials unset, the checkout
sitting on a branch cut before `zs connect --handoff` existed, another clone of this repo holding
the port and the database this one then used, or fingerprints/clients.json unreadable.

Everything here is read-only and fast:
  * Outlook is only *attached to* when it is already running (never started, and never asked to
    send, move, mark or delete anything);
  * the F: drive is only listed, never written;
  * credentials are reported as booleans; no value is ever printed, logged or returned;
  * processes and ports are reported, never signalled.
"""
import json
import os
import re
import subprocess
import zlib
from pathlib import Path

from env import ROOT, IS_WIN, DB_HOST, DB_PORT

# The five roots that live on the share. The pipeline only ever reads SiteContent.
F_ROOTS = ("SiteContent", "SiteDesign", "SiteTest", "SiteContentTEST", "ClientsNotActive")
F_DRIVE = Path(os.environ.get("ZS_F_DRIVE") or ("F:/" if IS_WIN else "/mnt/f"))
USED_ROOT = "SiteContent"

# Where other clones of this repo are known to live on this machine.
OTHER_CHECKOUT_HINTS = (
    Path.home() / "zap-site-builder",
    Path.home() / "Desktop" / "zap-sites" / "zap-site-builder",
    Path.home() / "code" / "zap-site-builder",
)


def _ps(script, timeout=30):
    """Run a short read-only PowerShell snippet. -> (ok, text)."""
    if not IS_WIN:
        return False, "not Windows"
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                            "-Command", script], capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace")
        return r.returncode == 0, (r.stdout or "").strip() or (r.stderr or "").strip()
    except Exception as e:                                   # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _git(*a, cwd=None):
    r = subprocess.run(["git", "-C", str(cwd or ROOT), *a], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


# ------------------------------------------------------------------ Outlook
def check_outlook():
    """Can the intake read desktop Outlook (bin/outlook-inbox.ps1)? -> (ok, detail).

    Attaches to an already running Outlook through the COM running-object table: it never starts
    Outlook, and never sends, moves, marks or deletes anything. It reads the Inbox name and count.
    """
    if not IS_WIN:
        return None, "desktop Outlook is Windows only (the cloud runs the intake from files)"
    script = (
        "$ErrorActionPreference='Stop';"
        "if (-not (Get-Process -Name OUTLOOK -ErrorAction SilentlyContinue)) { 'NOTRUNNING'; exit 0 };"
        "try { $ol=[Runtime.InteropServices.Marshal]::GetActiveObject('Outlook.Application');"
        " $f=$ol.GetNamespace('MAPI').GetDefaultFolder(6);"
        " 'OK|' + $f.Name + '|' + $f.Items.Count } catch { 'ERR|' + $_.Exception.Message }"
    )
    ok, out = _ps(script)
    line = (out.splitlines() or [""])[-1].strip()
    if line == "NOTRUNNING":
        return False, "Outlook is not running on this desktop, so bin/outlook-inbox.ps1 reads nothing. Start Outlook."
    if line.startswith("OK|"):
        _, name, count = line.split("|", 2)
        return True, f"attached read-only to a running Outlook; inbox '{name}' has {count} items"
    if line.startswith("ERR|"):
        return False, f"Outlook is running but the COM attach failed: {line[4:][:140]}"
    return False, f"could not determine the Outlook state: {(out or 'no output')[:140]}"


# ------------------------------------------------------------------ F: drive
def check_f_drive():
    """-> (ok, detail). ok is about SiteContent only; the other roots are listed for information."""
    seen, missing = [], []
    for name in F_ROOTS:
        p = F_DRIVE / name
        try:
            if p.is_dir():
                try:
                    n = sum(1 for _ in os.scandir(p))
                    seen.append(f"{name} ({n} entries)")
                except OSError as e:
                    seen.append(f"{name} (unreadable: {type(e).__name__})")
            else:
                missing.append(name)
        except OSError:
            missing.append(name)
    ok = (F_DRIVE / USED_ROOT).is_dir()
    detail = f"{F_DRIVE} present: {', '.join(seen) or 'none'}"
    if missing:
        detail += f" | absent: {', '.join(missing)}"
    detail += f" | the pipeline reads only {USED_ROOT}"
    return ok, detail


# ------------------------------------------------------------------ credentials
def check_credentials():
    """Presence only. No value is ever printed, logged or returned."""
    have = {k: bool(os.environ.get(k)) for k in ("ZS_WP_USER", "ZS_WP_PASSWORD")}
    ok = all(have.values())
    detail = " ".join(f"{k}={'set' if v else 'MISSING'}" for k, v in have.items())
    if not ok:
        detail += "  (set once with setx, then reopen the terminal; values are never printed)"
    return ok, detail


# ------------------------------------------------------------------ branch freshness
def check_branch():
    """Behind origin/main? A branch cut long ago lacks newer engine commands (zs connect --handoff)."""
    rc, head, _ = _git("rev-parse", "--abbrev-ref", "HEAD")
    if rc != 0:
        return False, "not a git checkout"
    rc, _, _ = _git("rev-parse", "--verify", "--quiet", "origin/main")
    if rc != 0:
        return False, f"on '{head}': no origin/main ref in this checkout (run: git fetch origin)"
    rc, counts, _ = _git("rev-list", "--left-right", "--count", "origin/main...HEAD")
    if rc != 0 or not counts:
        return False, f"on '{head}': could not compare with origin/main"
    parts = counts.split()
    behind, ahead = (parts + ["?", "?"])[:2]
    _, when, _ = _git("log", "-1", "--format=%cr", "origin/main")
    if behind != "0":
        return False, (f"on '{head}': {behind} commit(s) behind origin/main (last origin/main commit {when}); "
                       f"newer engine commands are missing here. Run: git fetch origin && git merge origin/main")
    return True, f"on '{head}': not behind origin/main ({ahead} ahead; origin/main {when}; ref age = last git fetch)"


# ------------------------------------------------------------------ other checkouts / ports
def site_port(slug):
    """Same formula as wpsite.Site.port, so a port can be attributed to a slug without importing it."""
    return 8100 + zlib.crc32(slug.encode()) % 800


def _listeners():
    """{port: [pid, ...]} for listening TCP sockets. netstat only, nothing is opened."""
    cmd = ["netstat", "-ano"] if IS_WIN else ["netstat", "-tlnp"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                             encoding="utf-8", errors="replace").stdout or ""
    except Exception:                                        # noqa: BLE001
        return {}
    ports = {}
    for ln in out.splitlines():
        if "LISTEN" not in ln.upper():
            continue
        m = (re.search(r"[:\]](\d+)\s+\S+\s+LISTENING\s+(\d+)", ln) if IS_WIN
             else re.search(r"[:\]](\d+)\s+\S+\s+LISTEN\s+(\d+)/", ln))
        if m:
            ports.setdefault(int(m.group(1)), []).append(int(m.group(2)))
    return ports


def _exe_of(pid):
    if IS_WIN:
        _, out = _ps(f"try {{ (Get-Process -Id {pid} -ErrorAction Stop).Path }} catch {{ '' }}", timeout=20)
        return (out.splitlines() or [""])[-1].strip()
    try:
        return os.readlink(f"/proc/{pid}/exe")
    except OSError:
        return ""


def _alive(pid):
    if IS_WIN:
        try:
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True,
                                 text=True, timeout=20).stdout or ""
            return str(pid) in out
        except Exception:                                    # noqa: BLE001
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def other_checkouts():
    """Every other clone or worktree of this repo on this machine (known paths + git worktree list)."""
    here = ROOT.resolve()
    found = {}
    cands = list(OTHER_CHECKOUT_HINTS)
    rc, out, _ = _git("worktree", "list", "--porcelain")
    if rc == 0:
        cands += [Path(l.split(" ", 1)[1]) for l in out.splitlines() if l.startswith("worktree ")]
    for c in cands:
        try:
            p = c.resolve()
        except OSError:
            continue
        if p == here or p in found or not (p / "engine" / "zs.py").exists():
            continue
        rc, head, _ = _git("rev-parse", "--abbrev-ref", "HEAD", cwd=p)
        found[p] = head if rc == 0 else "?"
    return found


def check_other_checkouts():
    """Other checkouts, and whether one of them holds a site port or the MariaDB this checkout expects.

    Reports only: nothing is killed, stopped or connected to.
    """
    others = other_checkouts()
    listeners = _listeners()
    notes, clash = [], False

    for path, branch in sorted(others.items()):
        held = []
        pids = sorted((path / "work").glob("*/server.pid")) if (path / "work").is_dir() else []
        for pid_file in pids:
            slug = pid_file.parent.name
            try:
                pid = int(pid_file.read_text().strip())
            except (OSError, ValueError):
                continue
            port = site_port(slug)
            if _alive(pid) and pid in listeners.get(port, []):
                held.append(f"{slug} on {port} (pid {pid})")
                clash = True
        notes.append(f"{path} [{branch}]" + (" HOLDS " + ", ".join(held) if held else ""))

    db_pids = listeners.get(DB_PORT, [])
    if db_pids:
        owners = []
        for pid in db_pids:
            exe = _exe_of(pid)
            where = "unknown process"
            if exe:
                e = str(Path(exe).resolve()).lower()
                if e.startswith(str(ROOT.resolve()).lower()):
                    where = "this checkout"
                else:
                    match = [str(p) for p in others if e.startswith(str(p).lower())]
                    where = match[0] if match else exe
            owners.append(f"pid {pid} <- {where}")
            if where != "this checkout":
                clash = True
        notes.append(f"MariaDB on {DB_HOST}:{DB_PORT} owned by " + "; ".join(owners))
    else:
        notes.append(f"nothing listening on {DB_HOST}:{DB_PORT} (MariaDB is started on demand)")

    if not others:
        notes.insert(0, "no other checkout of this repo found")
    return (not clash), " | ".join(notes)


# ------------------------------------------------------------------ client registry
def check_clients():
    f = ROOT / "fingerprints" / "clients.json"
    if not f.exists():
        return False, f"{f} is missing"
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return False, f"{f} unreadable: {type(e).__name__}: {e}"
    if not isinstance(d, dict):
        return False, f"{f}: expected an object of client id -> client"
    fps = len([p for p in (ROOT / "fingerprints").glob("*.json") if p.name != "clients.json"])
    return True, f"{len(d)} client(s) known, {fps} measured fingerprint(s) beside them"


CHECKS = (
    ("outlook (desktop, read-only)", check_outlook),
    ("F: drive roots", check_f_drive),
    ("staging credentials", check_credentials),
    ("branch vs origin/main", check_branch),
    ("other checkouts / ports / db", check_other_checkouts),
    ("fingerprints/clients.json", check_clients),
)

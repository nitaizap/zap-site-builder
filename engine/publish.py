"""Deliver the newest zip and print a download link.

Route, in order:
  1. GitHub release asset, when `gh` is installed and logged in (local machines).
  2. A delivery branch `delivery/<slug>-<yyyymmdd>[-n]` holding only the zip, pushed with plain git
     (works in Claude Code cloud sessions, which have git push but no gh token). Link:
     https://github.com/<owner>/<repo>/raw/<branch>/<zip>
  + SharePoint as well, when ZS_SHAREPOINT_FLOW_URL is set (a Power Automate HTTP flow).
"""
import json
import os
import re
import shutil
import subprocess
import urllib.request

from env import DIST, ROOT

GIT_LIMIT = 95 * 1048576     # GitHub rejects files over 100 MB


def _latest_zip(slug):
    zips = sorted(DIST.glob(f"{slug}-*.zip"), key=lambda p: p.stat().st_mtime)
    if not zips:
        raise SystemExit(f"no package for {slug}. Run: zs package {slug} --domain https://...")
    return zips[-1]


def _git(*args, input=None):
    # bytes in/out: on Windows, text mode turns mktree LF into CRLF and corrupts the file names
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                       input=input.encode("utf-8") if input is not None else None)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args[:3])} failed: {r.stderr.decode('utf-8', 'replace').strip()[-400:]}")
    return r.stdout.decode("utf-8", "replace").strip()


def _repo():
    url = _git("remote", "get-url", "origin")
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    if m:
        return m.group(1)
    m = re.search(r"/git/([^/]+/[^/]+?)(?:\.git)?$", url)       # cloud sessions use a local git proxy
    if m:
        return m.group(1)
    raise SystemExit(f"cannot tell the GitHub repo from origin {url}")


def _gh_ready():
    return shutil.which("gh") and subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0


def _notes(site, z):
    notes = [f"Upload-ready package for {site.slug}: deploy.sh, DEPLOY.md, LAUNCH-CHECKLIST.md, QA-REPORT.md inside."]
    qa = site.src / "QA-REPORT.md"
    if qa.exists():
        notes += [l for l in qa.read_text(encoding="utf-8").splitlines()[:12] if l.startswith("- ")]
    return "\n".join(notes)


def _via_release(site, z, repo):
    tag = z.stem
    sha = DIST / f"{z.name}.sha256"
    files = [str(z)] + ([str(sha)] if sha.exists() else [])
    if subprocess.run(["gh", "release", "view", tag, "--repo", repo], capture_output=True).returncode == 0:
        subprocess.run(["gh", "release", "upload", tag, *files, "--repo", repo, "--clobber"], check=True)
    else:
        subprocess.run(["gh", "release", "create", tag, *files, "--repo", repo, "--title", f"{site.slug} — {tag[-8:]}",
                        "--notes", _notes(site, z)], check=True)
    return f"https://github.com/{repo}/releases/download/{tag}/{z.name}"


def _via_branch(site, z, repo):
    """One orphan commit holding the zip + its checksum + a short README, on a fresh branch (no force pushes)."""
    if z.stat().st_size > GIT_LIMIT:
        raise SystemExit(f"{z.name} is {z.stat().st_size // 1048576} MB, over GitHub's file limit; use SharePoint or a release")
    blob = _git("hash-object", "-w", str(z))
    entries = [f"100644 blob {blob}\t{z.name}"]
    sha = DIST / f"{z.name}.sha256"
    if sha.exists():
        entries.append(f"100644 blob {_git('hash-object', '-w', str(sha))}\t{sha.name}")
    readme = DIST / "_delivery_README.md"
    readme.write_text(f"# {site.slug}\n\n{_notes(site, z)}\n\nDownload: `{z.name}`\n", encoding="utf-8")
    entries.append(f"100644 blob {_git('hash-object', '-w', str(readme))}\tREADME.md")
    readme.unlink()
    tree = _git("mktree", input="\n".join(entries) + "\n")
    commit = _git("-c", "user.name=zap-site-builder", "-c", "user.email=zapsites@d.co.il",
                  "commit-tree", tree, "-m", f"delivery: {z.name}")
    base = f"delivery/{z.stem}"
    existing = set(re.findall(r"refs/heads/(\S+)", _git("ls-remote", "--heads", "origin", f"{base}*")))
    branch, n = base, 2
    while branch in existing:
        branch, n = f"{base}-{n}", n + 1
    _git("push", "origin", f"{commit}:refs/heads/{branch}")
    return f"https://github.com/{repo}/raw/{branch}/{z.name}"


def publish(site):
    z = _latest_zip(site.slug)
    repo = _repo()
    mode = os.environ.get("ZS_PUBLISH", "auto")
    if mode == "release" or (mode == "auto" and _gh_ready()):
        out = [f"GitHub release: {_via_release(site, z, repo)}"]
    else:
        out = [f"GitHub (delivery branch): {_via_branch(site, z, repo)}"]
    flow = os.environ.get("ZS_SHAREPOINT_FLOW_URL")
    if flow:
        out.append("SharePoint: " + _to_sharepoint(flow, z))
    out.append(f"size: {z.stat().st_size / 1048576:.1f} MB")
    return "\n".join(out)


def _to_sharepoint(flow_url, z):
    req = urllib.request.Request(flow_url, data=z.read_bytes(), method="POST",
                                 headers={"Content-Type": "application/zip", "x-file-name": z.name})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            body = r.read().decode("utf-8", "replace")
            try:
                return json.loads(body).get("url", body[:200])
            except ValueError:
                return body[:200] or f"HTTP {r.status}"
    except Exception as e:  # never lose the GitHub link because SharePoint failed
        return f"upload failed ({e}); the GitHub link above is the deliverable"

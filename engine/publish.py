"""Deliver the newest zip: a GitHub release asset on this repo (always), plus SharePoint when configured.

SharePoint: set ZS_SHAREPOINT_FLOW_URL to a Power Automate "When an HTTP request is received" flow that
takes the file body and writes it to the Zap sites library (see references/delivery.md). Not required.
"""
import json
import os
import re
import subprocess
import urllib.request

from env import DIST, ROOT


def _latest_zip(slug):
    zips = sorted(DIST.glob(f"{slug}-*.zip"), key=lambda p: p.stat().st_mtime)
    if not zips:
        raise SystemExit(f"no package for {slug}. Run: zs package {slug} --domain https://...")
    return zips[-1]


def _repo():
    url = subprocess.run(["git", "-C", str(ROOT), "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    if not m:
        raise SystemExit("this checkout has no GitHub origin remote")
    return m.group(1)


def publish(site):
    z = _latest_zip(site.slug)
    tag = z.stem                                   # <slug>-<yyyymmdd>
    repo = _repo()
    notes = [f"Upload-ready package for **{site.slug}**.", "", "Inside the zip: `deploy.sh`, `DEPLOY.md`, `LAUNCH-CHECKLIST.md`, `QA-REPORT.md`."]
    qa = site.src / "QA-REPORT.md"
    if qa.exists():
        head = [l for l in qa.read_text(encoding="utf-8").splitlines()[:12] if l.startswith("- ")]
        notes += ["", "### QA", *head]
    sha = (DIST / f"{z.name}.sha256")
    files = [str(z)] + ([str(sha)] if sha.exists() else [])
    exists = subprocess.run(["gh", "release", "view", tag, "--repo", repo], capture_output=True).returncode == 0
    if exists:
        subprocess.run(["gh", "release", "upload", tag, *files, "--repo", repo, "--clobber"], check=True)
    else:
        subprocess.run(["gh", "release", "create", tag, *files, "--repo", repo, "--title", f"{site.slug} — {tag[-8:]}",
                        "--notes", "\n".join(notes)], check=True)
    link = f"https://github.com/{repo}/releases/download/{tag}/{z.name}"
    out = [f"GitHub: {link}"]

    flow = os.environ.get("ZS_SHAREPOINT_FLOW_URL")
    if flow:
        out.append("SharePoint: " + _to_sharepoint(flow, z))
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

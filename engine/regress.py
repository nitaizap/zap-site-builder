"""zs regress: re-run intake and reply routing over the real saved mail and compare to expectations.

Every data bug found on 2026-11-02 was silent - the wrong business name, an invented package, another
client's staging URL, a login URL stored as a staging URL, duplicate clients. None raised. They were
found by running against the real mailbox, so this makes that run repeatable.

The corpus is `work/inbox/`, which is gitignored and lives only on the intake PC: this command skips
cleanly (exit 0, says so) where the corpus is absent, so the cloud is unaffected. What IS committed is
`tests/expectations.json` - ids, names and URLs the team already shares, never message bodies.

  zs regress              compare against tests/expectations.json
  zs regress --record     rewrite expectations from what the code does now (review the diff!)
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "work" / "inbox"
EXPECT = ROOT / "tests" / "expectations.json"
SPEC_EXT = (".docx", ".xlsx")


def _zs(*args):
    """Run bin/zs and return parsed JSON stdout. PYTHONUTF8 so Hebrew survives a cp1255 console."""
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "engine" / "zs.py"), *args],
                       capture_output=True, text=True, encoding="utf-8", env=env, cwd=str(ROOT))
    if r.returncode and not r.stdout.strip():
        raise SystemExit("regress: `zs %s` failed:\n%s" % (" ".join(args), (r.stderr or "")[-600:]))
    return json.loads(r.stdout)


def _specs():
    """Every spec sheet in the corpus, as (entry_id, path), skipping QA documents and lock files."""
    out = []
    for d in sorted(INBOX.iterdir()):
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if (f.suffix.lower() in SPEC_EXT and not f.name.startswith("~$")
                    and "QA" not in f.name.upper()):
                out.append((d.name, f))
    return out


def observe():
    """What the code does right now, over the real corpus."""
    seen = {"intake": {}, "replies": {}}

    for entry_id, spec in _specs():
        body = spec.parent / "body.txt"
        args = ["intake", str(spec), "--dry-run", "--force", "--sender", "regress", "--subject", spec.stem]
        if body.exists():
            args += ["--body-file", str(body)]
        for r in _zs(*args):
            if "error" in r:
                seen["intake"][spec.name] = {"error": r["error"]}
                continue
            seen["intake"][spec.name] = {
                "client_id": r["client_id"], "name": r["name"], "package": r["package"],
                "staging_url": r["staging_url"], "images_found": bool(r["image_dirs"]),
                "missing": sorted(r["missing"]),
            }

    rep = _zs("replies", "--json")
    seen["replies"] = {
        "counts": rep["counts"],
        "staging_by_client": {},
        "unattributed": sorted({u["entry_id"] for u in rep.get("unattributed", [])}),
    }
    for m in rep["messages"]:
        for c in m.get("clients", []):
            url = c.get("staging_url")
            if url:
                seen["replies"]["staging_by_client"][c["client_id"]] = url
    return seen


def _diff(exp, got, path=""):
    out = []
    if isinstance(exp, dict) and isinstance(got, dict):
        for k in sorted(set(exp) | set(got)):
            out += _diff(exp.get(k, "<missing>"), got.get(k, "<missing>"), path + "/" + str(k))
    elif exp != got:
        out.append("%s\n    expected: %r\n    got     : %r" % (path, exp, got))
    return out


def cli(a):
    if not INBOX.is_dir():
        print("regress: no corpus at work/inbox/ on this machine - nothing to check (this is normal off the intake PC)")
        return
    got = observe()
    if a.record:
        EXPECT.parent.mkdir(parents=True, exist_ok=True)
        EXPECT.write_text(json.dumps(got, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("regress: recorded %d spec sheets and %d staging URLs to %s"
              % (len(got["intake"]), len(got["replies"]["staging_by_client"]), EXPECT.relative_to(ROOT)))
        print("         read the diff before committing: these are the values the pipeline will be held to.")
        return
    if not EXPECT.exists():
        raise SystemExit("regress: no %s yet - run `zs regress --record` once and commit it"
                         % EXPECT.relative_to(ROOT))
    exp = json.loads(EXPECT.read_text(encoding="utf-8"))
    bad = _diff(exp, got)
    n = len(exp.get("intake", {}))
    if bad:
        print("REGRESSION: %d difference(s) against %s\n" % (len(bad), EXPECT.relative_to(ROOT)))
        for b in bad:
            print("  " + b)
        print("\nIf the new behaviour is correct, re-record and commit the diff.")
        sys.exit(1)
    print("regress: OK - %d spec sheets and %d staging URLs match expectations" % (n, len(got["replies"]["staging_by_client"])))


def add_parser(sub):
    x = sub.add_parser("regress", help="re-run intake + reply routing over the real saved mail and compare to expectations")
    x.add_argument("--record", action="store_true", help="rewrite expectations from current behaviour")
    x.set_defaults(f=cli)

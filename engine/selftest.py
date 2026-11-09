"""zs selftest: run the documented engine chain end to end with an exit code you can trust.

CLAUDE.md documents the engine test as

    bin/zs new sample "..." --from examples/sample-plumber   # first time
    bin/zs build sample && bin/zs qa sample && bin/zs seo sample

Run that way inside a shell pipeline, a stage can print a full traceback and the chain can still
report success. This module runs every stage as its own child process, reads its real exit status,
and also refuses to call a stage green if it printed a traceback. One summary, one honest exit code.

One known, expected result is reported apart from real defects: `examples/sample-plumber` measures
~46% like the committed fingerprint of a real client (nick-itum), so `zs qa sample` exits 2 on the
uniqueness gate even when the QA report itself has 0 errors and 0 warnings. That is the sample
colliding with a real client, not the engine being broken, so it is reported as COLLISION and does
not fail the run unless --strict-uniqueness is given.
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from env import ROOT

ZS = str(Path(__file__).resolve().parent / "zs.py")
SAMPLE_SLUG = "sample"
SAMPLE_NAME = "מים טובים אינסטלציה"
SAMPLE_FROM = "examples/sample-plumber"

PASS, FAIL, COLLISION, SKIP = "PASS", "FAIL", "COLLISION", "SKIP"
TRACEBACK = "Traceback (most recent call last)"
# pool.check_measured: "ERROR home looks 46% like 'nick-itum' (measured: ...)"
UNIQ = re.compile(r"^ERROR .*looks \d+% like ", re.M)
QA_COUNTS = re.compile(r"- Errors: \*\*(\d+)\*\* . Warnings: \*\*(\d+)\*\*")


def _run(argv):
    """One stage, in its own process, with the UTF-8 environment bin/zs sets."""
    e = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    t = time.time()
    r = subprocess.run([sys.executable, ZS, *argv], cwd=str(ROOT), env=e, text=True,
                       capture_output=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or ""), time.time() - t


def _tail(out, n=25):
    lines = [x for x in out.strip().splitlines() if x.strip()]
    return "\n".join("      " + x for x in lines[-n:])


def selftest(fresh=False, strict_uniqueness=False, keep_going=False, slug=SAMPLE_SLUG):
    from wpsite import Site

    stages = []          # (name, status, seconds, note, output)
    overall_ok = True

    def record(name, status, secs, note="", out=""):
        nonlocal overall_ok
        stages.append((name, status, secs, note, out))
        print(f"{status:9} {name}  ({secs:.1f}s){'  ' + note if note else ''}", flush=True)
        if status == FAIL:
            overall_ok = False
        if status == COLLISION and strict_uniqueness:
            overall_ok = False
        return status

    def stage(name, argv, classify=None):
        print(f"--> {name}: zs {' '.join(argv)}", flush=True)
        rc, out, secs = _run(argv)
        crashed = TRACEBACK in out
        status, note = (PASS, "") if (rc == 0 and not crashed) else (FAIL, f"exit {rc}")
        if crashed:
            note = (note + " + traceback in output").strip()
        if classify:
            status, note = classify(rc, out, crashed, status, note)
        record(name, status, secs, note, out)
        return status

    def classify_qa(rc, out, crashed, status, note):
        if crashed or status == PASS:
            return status, note
        m = QA_COUNTS.search(out)
        errors = int(m.group(1)) if m else None
        uniq = [l.strip() for l in out.splitlines() if UNIQ.match(l.strip())]
        if rc == 2 and errors == 0 and uniq:
            return COLLISION, f"QA report clean (0 errors, 0 warnings); uniqueness gate: {uniq[0][6:140]}"
        if errors is not None:
            return FAIL, f"exit {rc}, QA report has {errors} error(s)"
        return status, note

    # 0. the launch check proves itself offline, in both directions (healthy markup passes, the plugin-less one fails)
    if stage("launch-check selftest", ["launch-check", "--selftest"]) == FAIL and not keep_going:
        return _summary(stages, False)

    # 1. new (only when the local WordPress for the sample is not there yet, or --fresh)
    if fresh or not Site(slug).exists():
        argv = ["new", slug, SAMPLE_NAME, "--from", SAMPLE_FROM]
        if fresh:
            argv.append("--force")
        if stage(f"new {slug}", argv) == FAIL and not keep_going:
            return _summary(stages, False)
    else:
        record(f"new {slug}", SKIP, 0.0, "local WordPress already exists (use --fresh to recreate)")

    for name, argv, cls in ((f"build {slug}", ["build", slug], None),
                            (f"qa {slug}", ["qa", slug], classify_qa),
                            (f"seo {slug}", ["seo", slug], None)):
        st = stage(name, argv, cls)
        if st == FAIL and not keep_going:
            break

    _report_similarity(slug)
    return _summary(stages, overall_ok)


def _report_similarity(slug):
    """Print how close this slug's measured home is to every committed client fingerprint.

    `pool.check_measured()` returns early for the slug `sample`: the engine's example is not a client,
    so a client-vs-client rule does not apply to it. Reasonable - but it means a green run says nothing
    at all about uniqueness, and CLAUDE.md lets a session self-merge on a green CI. So the numbers are
    printed whether or not they are enforced, and a drift of the example towards a real client is seen
    rather than hidden. Nothing here fails the run.
    """
    import json
    try:
        from fingerprint import similarity
        from pool import known
        f = ROOT / "sites" / slug / "fingerprint.json"
        if not f.exists():
            return
        mine = json.loads(f.read_text(encoding="utf-8"))
        home = mine.get("home") or (mine if "secs" in mine else None)
        if not home:
            return
        scores = []
        for other, ofp in known(slug).items():
            oh = ofp.get("home") or ofp
            try:
                scores.append((round(similarity(home, oh) * 100), other))
            except Exception:
                continue
        if not scores:
            return
        scores.sort(reverse=True)
        note = "" if slug != "sample" else "   (not enforced for 'sample': it is not a client)"
        print("\n  %s vs every committed fingerprint%s:" % (slug, note))
        for pct, other in scores[:6]:
            print("    %-26s %3d%%%s" % (other, pct, "   <- highest" if (pct, other) == scores[0] else ""))
    except Exception as e:                   # never let reporting break the run it reports on
        print("\n  (could not measure similarity: %s)" % e)


def _summary(stages, overall_ok):
    print("\n" + "=" * 72)
    print("zs selftest: the documented engine chain")
    print("=" * 72)
    for name, status, secs, note, _ in stages:
        print(f"  {status:9} {name:24} {secs:6.1f}s  {note}")
    bad = [s for s in stages if s[1] == FAIL]
    for name, status, secs, note, out in bad:
        print(f"\n--- last output of the failed stage: {name} ---")
        print(_tail(out))
    coll = [s for s in stages if s[1] == COLLISION]
    if coll:
        print("\nCOLLISION is not an engine defect: the sample's measured home is too close to a real\n"
              "client's committed fingerprint, so the uniqueness gate stops it. The sample cannot pass\n"
              "that gate today. Use --strict-uniqueness to count it as a failure.")
    print(f"\nRESULT: {'PASS' if overall_ok else 'FAIL'}"
          f"  ({sum(1 for s in stages if s[1] == PASS)} passed, {len(bad)} failed,"
          f" {len(coll)} collision, {sum(1 for s in stages if s[1] == SKIP)} skipped)")
    return overall_ok


def cmd_selftest(a):
    sys.exit(0 if selftest(fresh=a.fresh, strict_uniqueness=a.strict_uniqueness,
                           keep_going=a.keep_going, slug=a.slug) else 1)


def add_parser(sub):
    x = sub.add_parser("selftest", help="run the documented engine chain (new/build/qa/seo) with a trustworthy exit code")
    x.add_argument("--fresh", action="store_true", help="recreate the sample site and its database first")
    x.add_argument("--strict-uniqueness", action="store_true",
                   help="count the sample's fingerprint collision with a real client as a failure")
    x.add_argument("--keep-going", action="store_true", help="run every stage even after one fails")
    x.add_argument("--slug", default=SAMPLE_SLUG,
                   help="site slug to run the chain on (default: sample; another slug gets its own port and "
                        "database, so the chain can run while another checkout holds 'sample')")
    x.set_defaults(f=cmd_selftest)

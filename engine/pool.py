"""Anti-formula check: compare this site's recipe (design levers + home-page section order and variants)
with every other client on a `site/<slug>` branch, so two clients never get the same site."""
import json
import subprocess
from difflib import SequenceMatcher

from env import ROOT


def recipe(d):
    des = d.get("design") or {}
    home = next((p for p in d.get("pages", []) if p.get("type") == "home"), {})
    return {
        "levers": (des.get("preset", "clean"), des.get("hero", "split"), des.get("tone", ""), (des.get("fonts") or {}).get("heading", ""),
                   str((des.get("colors") or {}).get("primary", "")).lower()),
        "base": des.get("base_template"),
        "home": [s.get("type", "") + (":" + s["variant"] if s.get("variant") else "") for s in home.get("sections", [])],
    }


def _git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout


def _others(slug, files=False):
    """-> (slug, site.json dict[, fingerprint dict or None]) for every other client branch."""
    git = _git
    for ref in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/site/", "refs/heads/site/").split():
        other = ref.rsplit("site/", 1)[1]
        if other == slug:
            continue
        raw = git("show", f"{ref}:sites/{other}/site.json")
        if raw:
            try:
                d = json.loads(raw)
            except ValueError:
                continue
            if files:
                from fingerprint import load
                yield other, d, load(git("show", f"{ref}:sites/{other}/fingerprint.json"))
            else:
                yield other, d


def compare(slug, d, src=None):
    """-> list of ERROR/WARN lines. The measured layout (fingerprint.json from zs qa, preview/fingerprints.json
    from zs preview) decides: ERROR when a home reads as another client's. Names of sections only warn."""
    from fingerprint import CLOSE, TOO_CLOSE, load, similarity
    mine = {}
    if src is not None:
        f = load((src / "fingerprint.json").read_text(encoding="utf-8")) if (src / "fingerprint.json").exists() else None
        if f:
            mine["home"] = f
        pf = src / "preview" / "fingerprints.json"
        if d.get("directions") and pf.exists():
            mine.update({f"direction {k}": v for k, v in (load(pf.read_text(encoding="utf-8")) or {}).items()})
    me, out, seen = recipe(d), [], set()
    if src is not None and not mine:
        out.append("WARN  no measured layout yet: run zs qa (or zs preview at the gate) first, then zs pool")
    unmeasured = []
    for other, od, ofp in _others(slug, files=True):
        if other in seen:
            continue
        seen.add(other)
        if ofp:
            for name, fp in mine.items():
                v = similarity(fp, ofp)
                if v >= TOO_CLOSE:
                    out.append(f"ERROR {name} looks {v:.0%} like '{other}' (measured layout): change the kit, the hero or the "
                               f"home's section order (references/pool.md → Style kits, Home archetypes)")
                elif v >= CLOSE:
                    out.append(f"WARN  {name} is {v:.0%} like '{other}' (measured layout)")
        else:
            unmeasured.append(other)
        o = recipe(od)
        sim = SequenceMatcher(None, me["home"], o["home"]).ratio()
        same = sum(a == b for a, b in zip(me["levers"], o["levers"]))
        if me["base"] and me["base"] == o["base"] and me["levers"][4] and me["levers"][4] == o["levers"][4]:
            out.append(f"WARN  same base template {me['base']} and the same primary colour as '{other}': change the palette "
                       f"or the one bold element (references/pool.md, base templates)")
        if sim >= .75 and same >= 3:
            out.append(f"WARN  recipe too close to '{other}': home {sim:.0%} alike, {same}/5 design levers equal "
                       f"({', '.join(map(str, o['levers']))}). Swap variants or a lever (references/pool.md)")
    if unmeasured:
        out.append(f"WARN  not measured yet (no fingerprint.json on their branch; their next zs qa adds it): {', '.join(unmeasured)}")
    return out

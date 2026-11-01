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


RECENT = 3   # a kit or archetype used by one of the last RECENT client sites is not used again


def recent(slug):
    """The last RECENT other clients (by their branch's latest commit) -> [(slug, kit, archetype)]."""
    by = {}
    for ref in _git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/site/", "refs/heads/site/").split():
        other = ref.rsplit("site/", 1)[1]
        if other == slug or other.endswith("-pilot"):
            continue
        t = int((_git("log", "-1", "--format=%ct", ref).strip() or 0))
        raw = _git("show", f"{ref}:sites/{other}/site.json")
        try:
            des = json.loads(raw).get("design", {}) if raw else {}
        except ValueError:
            continue
        if t >= by.get(other, (0,))[0]:
            by[other] = (t, des.get("kit"), des.get("archetype"))
    return [(o, k, a) for o, (t, k, a) in sorted(by.items(), key=lambda x: -x[1][0])[:RECENT]]


def known(slug):
    """Every other client's measured layout: fingerprints/<slug>.json on this checkout (the registry, sites on any
    branch) overlaid by sites/<slug>/fingerprint.json on each site/* branch (newer). -> {slug: fingerprint}"""
    from fingerprint import load
    out = {}
    for f in sorted((ROOT / "fingerprints").glob("*.json")):
        if f.stem != slug:
            fp = load(f.read_text(encoding="utf-8"))
            if fp:
                out[f.stem] = fp
    for other, _d, fp in _others(slug, files=True):
        if fp and "palette" in fp:
            out[other] = fp
    return out


def check_measured(slug, fps):
    """{name: fingerprint} of this site (home or gate directions) vs every other client -> ERROR/WARN lines."""
    from fingerprint import CLOSE, TOO_CLOSE, similarity
    out = []
    if slug == "sample":   # the engine test site (examples/sample-plumber) is the engine's plain default, not a client
        return out
    for other, ofp in known(slug).items():
        for name, fp in fps.items():
            v = similarity(fp, ofp)
            if v >= TOO_CLOSE:
                out.append(f"ERROR {name} looks {v:.0%} like '{other}' (measured: palette, furniture, components, layout). Change "
                           f"what the visitor sees first: the palette, the kit, the hero and the home's components (references/pool.md)")
            elif v >= CLOSE:
                out.append(f"WARN  {name} is {v:.0%} like '{other}' (measured)")
    return out


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
    last = recent(slug)
    des = d.get("design") or {}
    opts = [("design", des)] + [(f"direction {k}", {**des, **v}) for k, v in (d.get("directions") or {}).items() if isinstance(v, dict)]
    for name, dz in (opts[1:] if d.get("directions") else opts[:1]):
        for lever in ("kit", "archetype"):
            hit = [o for o, k, a in last if dz.get(lever) and dz.get(lever) == (k if lever == "kit" else a)]
            if hit:
                out.append(f"ERROR {name}: {lever} '{dz[lever]}' was used by {', '.join(hit)} (one of the last {RECENT} sites): pick another")
    if src is not None and not mine:
        out.append("WARN  no measured layout yet: run zs qa (or zs preview at the gate) first, then zs pool")
    out += check_measured(slug, mine)
    for other, od in _others(slug):
        if other in seen:
            continue
        seen.add(other)
        o = recipe(od)
        sim = SequenceMatcher(None, me["home"], o["home"]).ratio()
        same = sum(a == b for a, b in zip(me["levers"], o["levers"]))
        if me["base"] and me["base"] == o["base"] and me["levers"][4] and me["levers"][4] == o["levers"][4]:
            out.append(f"WARN  same base template {me['base']} and the same primary colour as '{other}': change the palette "
                       f"or the one bold element (references/pool.md, base templates)")
        if sim >= .75 and same >= 3:
            out.append(f"WARN  recipe too close to '{other}': home {sim:.0%} alike, {same}/5 design levers equal "
                       f"({', '.join(map(str, o['levers']))}). Swap variants or a lever (references/pool.md)")
    return out

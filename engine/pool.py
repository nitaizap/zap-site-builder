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


def _others(slug):
    git = lambda *a: subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout
    for ref in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/site/", "refs/heads/site/").split():
        other = ref.rsplit("site/", 1)[1]
        if other == slug:
            continue
        raw = git("show", f"{ref}:sites/{other}/site.json")
        if raw:
            try:
                yield other, json.loads(raw)
            except ValueError:
                pass


def compare(slug, d):
    """-> list of WARN lines. Same levers + a home page >= 75% alike in section order/variants = too close."""
    me, out, seen = recipe(d), [], set()
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

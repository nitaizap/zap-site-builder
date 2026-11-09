"""zs replies: route the sites team's *reply* mail (staging URLs, QA feedback) to the right client.

`zs intake` turns a new request into `sites/c<id>/`. Everything the sites team sends afterwards -
"here is the staging site", "two things to fix before it goes live", a QA document - arrives as a
reply in the same thread, and one reply often covers several clients at once. This command sorts
those replies and files each one under the client it is actually about:

    sites/c<id>/inbox/<YYYY-MM-DD>-<kind>.md    sender, subject, received, entry_id, the reply text
                                                that belongs to this client, the staging URLs found
    sites/c<id>/inbox/<attachment>              real attachments (signature logos are dropped)
    sites/c<id>/intake.json                     staging_url set, "staging URL" dropped from missing

Attribution is the whole point and it is never guessed:

  * a staging URL belongs to the client whose 8-digit id is embedded in its host
    (`80392936.ussl.co.il`, `80392210kisos.ussl.co.il`, `erezbread80049225.ussl.co.il` are all real);
  * a line of text belongs to the client named last above it, by id or by business name, so
    "הוילה הלבנה:" followed by a URL does not spill onto the next client in the list;
  * business names come from a registry built from the spec sheets, the checked-out `sites/`
    and the `site/c<id>` branches - never invented;
  * when the explicit ids in a message disagree with the name registry, nothing is written for the
    disputed client and the clash is reported.

Nothing is written without `--write`: the default is a dry run that prints what it *would* write
per client, because a wrong attribution puts one client's data on another client's branch.
Committing and pushing is left to the caller (`.claude/skills/zap-intake/SKILL.md` step 4): one run
spans several clients and therefore several `site/c<id>` branches, so there is no single commit to
make here. Stdlib only, like the rest of the intake.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from intake import (ID_RE, ROOT, SPEC_EXT, name_from_filename, staging_urls, unwrap_safelinks)

# Inline images Outlook attaches to every message in this thread family: the five Zap signature
# logos (bare digit names), Outlook's own `image001.png` artefacts and its `Outlook-*.png` copies.
JUNK_RE = re.compile(r"^(?:\d{8,}\.png|image\d*\.png|Outlook-.*\.(?:png|jpg|jpeg|gif)|~\$.*)$", re.I)
SPEC_RE = re.compile(r".*(" + "|".join(e.lstrip(".") for e in SPEC_EXT) + ")$", re.I)
# Where the new text of a reply stops and the quoted thread (or the signature) begins.
QUOTE_RE = re.compile(r"^\s*(?:_{8,}|-{5,}\s*Original Message|From:\s|מאת:\s*\S|On .{0,80}\bwrote:)")
# Where the Zap mail signature starts: its first line is the sender's name, then title, phone, address.
SIGN_RE = re.compile(r"הסיבים 25 פתח תקווה|zapgroup\.co\.il|<mailto:|טלפון:\s*0|Project Manager"
                     r"|מנהלת פרוי|מקדמת SEO|טראפיק ומנהלת"
                     r"|^\s*(?:ניתאי צוייג|נטע שינובר|שרון יוסף|נועם רוזן)\s*$")
# Noise stripped out of a spec-sheet file name before it is used as a business name.
NAME_NOISE = re.compile(r"\b(?:qa)\b|איפיון אתר|אפיון אתר|איפיון|אפיון|הפקת אתר|מיניסייט|לקוח חדש|וויקנד|בייסיק",
                        re.I)
GERESH = str.maketrans({"'": "", "׳": "", '"': "", "״": "", "`": "", "’": ""})


# ---------- text ----------

def new_text(body):
    """The part of the body this sender actually wrote: before the quoted thread and the signature."""
    lines = unwrap_safelinks(body or "").splitlines()
    cut = len(lines)
    for i, l in enumerate(lines):
        if QUOTE_RE.match(l) or SIGN_RE.search(l):
            cut = i
            break
    return "\n".join(lines[:cut]).strip()


def meaningful(text):
    """True when there is actually something to file: a greeting on its own is not."""
    return len(re.sub(r"\s", "", text or "")) >= 12


def norm(s):
    """Lower-cased, geresh-free, single-spaced - so פטוצ'ינה and פטוצינה are the same word."""
    return re.sub(r"\s+", " ", re.sub(r"[-_|,.:;()\[\]]+", " ", (s or "").translate(GERESH))).strip().lower()


# ---------- the client registry (id <-> business name) ----------

def clean_name(s, cid=""):
    s = NAME_NOISE.sub(" ", name_from_filename(s, cid))
    return re.sub(r"\s+", " ", s).strip(" -–_")


def name_key(name):
    """The distinctive opening of a business name: enough to recognise it, short enough to match.

    The spec sheet says "הוילה הלבנה ינוב", the mail says "הוילה הלבנה"; two tokens catch both.
    A key under 4 characters is dropped rather than risk matching a stray word.
    """
    parts = norm(name).split()
    key = " ".join(parts[:2])
    return key if len(key) >= 4 else ""


def _branch_intakes():
    """name/id pairs from the `site/c<id>` branches, so a run on `main` still knows the clients."""
    out = []
    try:
        refs = subprocess.run(["git", "-C", str(ROOT), "for-each-ref", "--format=%(refname:short)",
                               "refs/remotes/origin/site", "refs/heads/site"],
                              capture_output=True, text=True, timeout=30).stdout.split()
    except (OSError, subprocess.SubprocessError):
        return out
    for ref in refs:
        slug = ref.rsplit("/", 1)[-1]
        if not re.fullmatch(r"c\d{8}", slug):
            continue
        try:
            raw = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:sites/{slug}/intake.json"],
                                 capture_output=True, text=True, timeout=30)
            if raw.returncode == 0:
                out.append((slug[1:], json.loads(raw.stdout).get("name") or ""))
        except (OSError, subprocess.SubprocessError, ValueError):
            continue
    return out


def registry(sites_dir, msgs, use_git=True):
    """{client id: {"name", "keys"}} built from the spec sheets and the known client folders.

    Also returns the name keys that two different clients would both answer to; those are never
    used for attribution, because "whose site is this" has to have one answer.
    """
    pairs = []
    for m in msgs:                                       # the spec sheet that opened each thread
        for f in m["files"]:
            if SPEC_RE.match(f.name) and not f.name.startswith("~$"):
                hit = ID_RE.search(f.stem)
                if hit:
                    pairs.append((hit.group(1), clean_name(f.stem, hit.group(1))))
    for p in sorted(Path(sites_dir).glob("c*/intake.json")) if Path(sites_dir).is_dir() else []:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            pairs.append((str(d.get("client_id") or p.parent.name[1:]), d.get("name") or ""))
        except (OSError, ValueError):
            continue
    if use_git:
        pairs += _branch_intakes()
    for m in msgs:                                       # an id can be known without a name at all:
        for cid, _ in staging_urls(m["body"]):           # it is in a staging host, or in the subject
            pairs.append((cid, ""))
        pairs += [(i, "") for i in ID_RE.findall(m["subject"])]

    reg, owners = {}, {}
    for cid, name in pairs:
        if not re.fullmatch(r"\d{8}", cid or ""):
            continue
        e = reg.setdefault(cid, {"id": cid, "name": "", "keys": set()})
        if name and not e["name"]:          # the spec sheet names the client; a later rename is an alias
            e["name"] = name
        k = name_key(name)
        if k:
            e["keys"].add(k)
            owners.setdefault(k, set()).add(cid)
    shared = {k for k, v in owners.items() if len(v) > 1}
    for e in reg.values():
        e["keys"] -= shared
    return reg, shared


# ---------- per-message attribution ----------

def clients_on_line(line, reg):
    """The clients this one line names, by 8-digit id or by business name."""
    by_id = {i for i in ID_RE.findall(line) if i in reg}
    n = norm(line)
    by_name = {cid for cid, e in reg.items() if any(k in n for k in e["keys"])}
    return by_id, by_name


def attribute(msg, reg):
    """Split one saved message into {client id: part} plus the things it could not place.

    A part is {"lines", "staging", "quoted", "named"}. Lines are walked in order and handed to the
    client named last above them, which is how a "<business>:" heading followed by its URL stays
    with that business. Lines before any client is named are preamble, shared by the clients this
    sender actually named - never by a client that only turned up in the quoted thread below,
    because a quoted URL says "this site exists", not "this message is about it".
    """
    text, notes = new_text(msg["body"]), []
    subject_ids, subject_names = clients_on_line(msg["subject"], reg)

    per, order, preamble, cur = {}, [], [], set()

    def slot(cid, named=False):
        if cid not in per:
            per[cid] = {"lines": [], "staging": [], "quoted": [], "named": False}
            order.append(cid)
        per[cid]["named"] = per[cid]["named"] or named
        return per[cid]

    for line in text.splitlines():
        hits = set().union(*clients_on_line(line, reg)) | {c for c, _ in staging_urls(line) if c in reg}
        if hits:
            cur = hits
        if cur:
            for cid in cur:
                slot(cid, named=True)["lines"].append(line)
        elif line.strip():
            preamble.append(line)

    # Staging URLs: the 8-digit id lives in the host, so a URL is placed on that evidence alone,
    # whether this sender wrote it or it came down in the quoted thread.
    new_urls = {u for _, u in staging_urls(text)}
    homeless = []
    for cid, url in staging_urls(unwrap_safelinks(msg["body"])):
        where = "staging" if url in new_urls else "quoted"
        if cid in reg:
            slot(cid, named=(where == "staging"))[where].append(url)
        else:
            homeless.append((where, url))
    for where, url in homeless:                  # a host with no id can only go to a one-client mail
        only = set(per) | subject_ids
        if len(only) == 1:
            slot(next(iter(only)), named=True)[where].append(url)
        else:
            notes.append("staging URL %s: no client id in the host and the mail names %s"
                         % (url, ", ".join("c" + c for c in sorted(only)) or "no client"))

    for cid in subject_ids:                      # "Re: בצל התאנה 80393140" - the subject names a client
        slot(cid, named=True)
    # A name in the subject pointing somewhere else than the explicit ids is a clash, not a client.
    for cid in subject_names - subject_ids:
        if subject_ids:
            notes.append("subject names %s (c%s) but carries id %s - nothing written for c%s"
                         % (reg[cid]["name"], cid, ", ".join("c" + i for i in sorted(subject_ids)), cid))
        else:
            slot(cid, named=True)

    named = [c for c in order if per[c]["named"]]
    for cid in order:
        if not per[cid]["named"]:                # resolved only by a URL quoted from further down
            per[cid]["lines"] = []
        elif len(named) > 1:
            per[cid]["lines"] = preamble + per[cid]["lines"]
        else:
            per[cid]["lines"] = text.splitlines()
    return per, notes


def place_attachments(msg, cids, reg):
    """{client id: [file, ...]} for the attachments worth keeping, plus the ones nobody can claim.

    A QA document names its client ("QA-ניק-איטום.docx"); anything else can only be placed when the
    whole message is about one client. Never copied to "all of them".
    """
    out, orphans = {c: [] for c in cids}, []
    for f in msg["files"]:
        if JUNK_RE.match(f.name) or f.name in ("meta.json", "body.txt"):
            continue
        named = {cid for cid, e in reg.items() if any(k in norm(f.stem) for k in e["keys"])}
        if len(named) == 1:
            out.setdefault(named.pop(), []).append(f)
        elif len(cids) == 1:
            out[next(iter(cids))].append(f)
        else:
            orphans.append(f.name)
    return out, orphans


def classify(msg, per, reg):
    """new_spec | staging | feedback | other, for the message as a whole."""
    if any(SPEC_RE.match(f.name) and ID_RE.search(f.stem) for f in msg["files"]):
        return "new_spec"
    if any(v["staging"] or v["quoted"] for v in per.values()):
        return "staging"
    docs = [f for f in msg["files"] if not JUNK_RE.match(f.name) and f.name not in ("meta.json", "body.txt")]
    if per and (docs or msg["subject"].strip().lower().startswith(("re:", "re‏:"))):
        return "feedback"
    return "other"


# ---------- writing ----------

def render(cid, reg, msg, part, kind, attachments):
    name = reg[cid]["name"]
    md = [f"# {name} ({cid}) - {kind}" if name else f"# {cid} - {kind}", "",
          f"- from: {msg['from']}", f"- subject: {msg['subject']}",
          f"- received: {msg['received']}", f"- entry_id: {msg['entry_id']}", ""]
    if part["staging"] or part["quoted"]:
        md += ["## Staging URL", ""]
        md += [f"- {u}" for u in part["staging"]]
        md += [f"- {u}  (quoted from an earlier message in this thread)" for u in part["quoted"]]
        md += [""]
    body = "\n".join(part["lines"]).strip()
    if body:
        md += ["## Reply text", "", body, ""]
    if attachments:
        md += ["## Attachments", ""] + [f"- {f.name}" for f in attachments] + [""]
    return "\n".join(md)


def run(inbox, sites_dir=None, write=False, only=None, use_git=True):
    sites_dir = Path(sites_dir or ROOT / "sites")
    msgs = load(inbox)
    reg, shared = registry(sites_dir, msgs, use_git=use_git)
    known = {cid: set() for cid in reg}                  # staging URLs already on file, per client
    for cid in reg:
        f = sites_dir / ("c" + cid) / "intake.json"
        if f.exists():
            try:
                u = json.loads(f.read_text(encoding="utf-8")).get("staging_url")
                if u:
                    known[cid].add(u)
            except (OSError, ValueError):
                pass

    report = {"messages": [], "counts": {}, "unattributed": [], "shared_name_keys": sorted(shared)}
    for msg in msgs:
        per, notes = attribute(msg, reg)
        kind_msg = classify(msg, per, reg)
        report["counts"][kind_msg] = report["counts"].get(kind_msg, 0) + 1
        files, orphans = place_attachments(msg, set(per), reg)
        row = {"entry_id": msg["entry_id"], "received": msg["received"], "from": msg["from"],
               "subject": msg["subject"], "class": kind_msg, "clients": [], "notes": list(notes)}
        report["messages"].append(row)
        for n in notes:
            report["unattributed"].append({"entry_id": msg["entry_id"], "what": n})
        for n in orphans:
            report["unattributed"].append({"entry_id": msg["entry_id"],
                                           "what": f"attachment {n}: no single client"})
        if kind_msg == "new_spec" or not per:
            if kind_msg != "new_spec" and not per:
                report["unattributed"].append({"entry_id": msg["entry_id"],
                                               "what": "no client named by id, name or staging host"})
            continue

        for cid in sorted(per):
            if only and cid not in only:
                continue
            part = per[cid]
            urls = [u for u in part["staging"] + part["quoted"] if u not in known[cid]]
            kind = "staging" if urls else "feedback"
            body = "\n".join(part["lines"]).strip()
            # A later message that only re-quotes a URL already on file, or says nothing but
            # "hi", adds nothing to the client's folder.
            if not urls and not files.get(cid) and not meaningful(body):
                continue
            if not reg[cid]["name"]:
                report["unattributed"].append(
                    {"entry_id": msg["entry_id"],
                     "what": f"c{cid}: no business name on record - attributed by its id alone"})
            site = sites_dir / ("c" + cid)
            entry = {"client_id": cid, "name": reg[cid]["name"], "kind": kind,
                     "file": f"sites/c{cid}/inbox/{msg['received'][:10]}-{kind}.md",
                     "staging_url": urls[0] if urls else "",
                     "attachments": [f.name for f in files.get(cid, [])],
                     "lines": len(body.splitlines())}
            known[cid].update(urls)
            if not site.is_dir():
                entry["skipped"] = f"sites/c{cid} is not in this checkout (switch to site/c{cid} and re-run)"
                row["clients"].append(entry)
                continue
            if write:
                out = site / "inbox"
                out.mkdir(parents=True, exist_ok=True)
                path = out / f"{msg['received'][:10]}-{kind}.md"
                n = 2
                while path.exists() and path.read_text(encoding="utf-8").find(msg["entry_id"]) < 0:
                    path = out / f"{msg['received'][:10]}-{kind}-{n}.md"
                    n += 1
                entry["file"] = str(path.relative_to(sites_dir.parent)).replace("\\", "/")
                path.write_text(render(cid, reg, msg, part, kind, files.get(cid, [])), encoding="utf-8")
                for f in files.get(cid, []):
                    shutil.copy2(f, out / f.name)
                if urls:
                    entry["intake_updated"] = set_staging(site / "intake.json", urls[0])
            row["clients"].append(entry)
    return report


def set_staging(path, url):
    """Record the staging URL on the client's intake.json and drop it from `missing`."""
    if not path.exists():
        return False
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if d.get("staging_url") == url:
        return False
    d["staging_url"] = url
    d["missing"] = [m for m in d.get("missing", []) if "staging URL" not in m]
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


# ---------- input ----------

def load(inputs):
    """Every saved message folder under the given paths, oldest first."""
    dirs = []
    for i in inputs:
        p = Path(i)
        if (p / "meta.json").exists():                   # one saved message
            dirs.append(p)
        elif p.is_dir():                                 # a folder of them (work/inbox)
            dirs += sorted(d for d in p.iterdir() if d.is_dir() and (d / "meta.json").exists())
    msgs = []
    for d in dirs:
        try:
            m = json.loads((d / "meta.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        body = (d / "body.txt").read_text(encoding="utf-8", errors="replace") if (d / "body.txt").exists() else ""
        msgs.append({"dir": d, "entry_id": m.get("entry_id") or d.name, "from": m.get("from") or "",
                     "subject": m.get("subject") or "", "received": m.get("received") or "",
                     "conversation_topic": m.get("conversation_topic") or "", "body": body,
                     "files": sorted(f for f in d.iterdir() if f.is_file()
                                     and f.name not in ("meta.json", "body.txt"))})
    return sorted(msgs, key=lambda m: m["received"])


def cli(a):
    report = run(a.inputs or [str(ROOT / "work" / "inbox")], a.sites_dir, write=a.write,
                 only=set(a.client or []) or None, use_git=not a.no_git)
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print("DRY RUN - nothing written (add --write)" if not a.write else "WROTE:")
    print("classified: " + ", ".join(f"{k}={v}" for k, v in sorted(report["counts"].items())))
    for m in report["messages"]:
        if not m["clients"] and not m["notes"]:
            continue
        print(f"\n{m['received']}  {m['class']:<9} {m['from']}  {m['subject'][:70]}")
        for c in m["clients"]:
            tag = "  SKIP " + c["skipped"] if c.get("skipped") else ""
            print(f"   -> c{c['client_id']} {c['name']}  [{c['kind']}]  {c['file']}{tag}")
            if c["staging_url"]:
                print(f"      staging_url = {c['staging_url']}")
            if c["attachments"]:
                print("      files: " + ", ".join(c["attachments"]))
        for n in m["notes"]:
            print("   !! " + n)
    if report["unattributed"]:
        print("\nNot attributed (reported, never guessed onto a branch):")
        for u in report["unattributed"]:
            print(f"   {u['entry_id']}: {u['what']}")
    if report["shared_name_keys"]:
        print("\nBusiness names claimed by more than one client id (never used to attribute): "
              + ", ".join(report["shared_name_keys"]))


def add_parser(sub):
    x = sub.add_parser("replies", help="staging-URL / feedback replies -> sites/c<id>/inbox/ (dry run by default)")
    x.add_argument("inputs", nargs="*", help="work/inbox (default), or single work/inbox/<entry id> folders")
    x.add_argument("--write", action="store_true", help="actually write; without it this only prints the plan")
    x.add_argument("--client", action="append", metavar="ID", help="only this 8-digit client id (repeatable)")
    x.add_argument("--sites-dir")
    x.add_argument("--no-git", action="store_true", help="do not read client names from the site/c<id> branches")
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cli)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="replies")
    add_parser(ap.add_subparsers(dest="cmd", required=True))
    a = ap.parse_args(["replies"] + sys.argv[1:])
    a.f(a)

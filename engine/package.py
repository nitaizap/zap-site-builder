"""Package a built site as one upload-ready zip for the server team.

zip layout:
  <slug>/public_html/        complete WordPress (core, theme, plugins, uploads), fresh wp-config.php
  <slug>/database.sql        URLs already rewritten to the client domain
  <slug>/deploy.sh           one-command install (needs wp-cli on the server, CloudPanel has it)
  <slug>/DEPLOY.md           the same steps by hand, Hebrew + English
  <slug>/LAUNCH-CHECKLIST.md what only a human can finish
  <slug>/QA-REPORT.md, site.json
"""
import datetime
import hashlib
import os
import re
import secrets
import shutil
import zipfile
from pathlib import Path

from build import load_site
from env import DIST, IS_WIN, mariadb_dir

TEMPLATES = Path(__file__).with_name("templates")
SKIP_DIRS = {"wp-content/upgrade", "wp-content/cache", "wp-content/uploads/elementor/css", "wp-content/debug.log"}


def _domain(d):
    d = d.strip().rstrip("/")
    if not re.match(r"^https?://[a-z0-9.-]+\.[a-z]{2,}$", d, re.I):
        raise SystemExit(f"--domain must look like https://client.co.il (got {d})")
    return d


def _salts():
    keys = ["AUTH_KEY", "SECURE_AUTH_KEY", "LOGGED_IN_KEY", "NONCE_KEY", "AUTH_SALT", "SECURE_AUTH_SALT", "LOGGED_IN_SALT", "NONCE_SALT"]
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-.:;<=>?@[]^_{|}~"
    return "\n".join(f"define('{k}', '{''.join(secrets.choice(alphabet) for _ in range(64))}');" for k in keys)


def _export_db(site, old, new, out_sql):
    env_path = None
    if IS_WIN and mariadb_dir():
        env_path = str(mariadb_dir() / "bin")
        os.environ["PATH"] = env_path + os.pathsep + os.environ["PATH"]
    tmp = site.dir / "_export.sql"
    # Plain + serialized URLs (wp-cli keeps serialized lengths right), exported without touching the local DB.
    site.wp("search-replace", old, new, "--all-tables", "--precise", f"--export={tmp}")
    sql = tmp.read_text(encoding="utf-8")
    tmp.unlink()
    # JSON-escaped (Elementor data) and URL-encoded copies are not serialized, so a text replace is safe.
    host_old = old.split("://", 1)[1]
    host_new = new.split("://", 1)[1]
    scheme_new = new.split("://", 1)[0]
    for a, b in [
        (old.replace("/", "\\\\/"), new.replace("/", "\\\\/")),       # http:\\/\\/127.0.0.1:port inside the dump
        (old.replace("/", "\\/"), new.replace("/", "\\/")),
        (old.replace(":", "%3A").replace("/", "%2F"), new.replace(":", "%3A").replace("/", "%2F")),
    ]:
        sql = sql.replace(a, b)
    left = len(re.findall(re.escape(host_old), sql))
    if left:
        i = sql.find(host_old)
        raise SystemExit(f"{left} references to {host_old} survived the URL rewrite, e.g. …{sql[max(0, i - 80):i + 40]}…")
    staging = "zapsites.co.il" in new
    sql += "\n-- Zap build: indexing on for the client domain, off for a zapsites staging host\n"
    sql += f"UPDATE `wp_options` SET `option_value`='{0 if staging else 1}' WHERE `option_name`='blog_public';\n"
    out_sql.write_text(sql, encoding="utf-8")
    return staging, scheme_new


def _copy_wp(src: Path, dst: Path):
    for root, dirs, files in os.walk(src):
        rel = Path(root).relative_to(src).as_posix()
        dirs[:] = [d for d in dirs if f"{rel}/{d}".lstrip("./") not in SKIP_DIRS]
        for f in files:
            r = f"{rel}/{f}".lstrip("./")
            if r in ("wp-config.php", "robots.txt") or r in SKIP_DIRS:
                continue
            out = dst / r
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(Path(root) / f, out)


def package(site, domain, require_clean_qa=True):
    domain = _domain(domain)
    data = load_site(site.src)
    qa = site.src / "QA-REPORT.md"
    if require_clean_qa:
        if not qa.exists():
            raise SystemExit("run `zs qa` first: the package ships the QA report")
        m = re.search(r"Errors: \*\*(\d+)\*\*", qa.read_text(encoding="utf-8"))
        if not m or int(m.group(1)) > 0:
            raise SystemExit("QA-REPORT.md has errors. Fix them and run `zs qa` again before packaging.")
        if qa.stat().st_mtime < (site.src / "site.json").stat().st_mtime:
            raise SystemExit("site.json changed after the last QA run. Run `zs build` and `zs qa` again.")

    stamp = datetime.date.today().strftime("%Y%m%d")
    root = DIST / f"{site.slug}-{stamp}"
    if root.exists():
        shutil.rmtree(root)
    pub = root / "public_html"
    pub.mkdir(parents=True)

    staging, _ = _export_db(site, site.url, domain, root / "database.sql")
    _copy_wp(site.wp_dir, pub)

    cfg = (TEMPLATES / "wp-config.php").read_text(encoding="utf-8")
    cfg = cfg.replace("{{SALTS}}", _salts()).replace("{{ENV}}", "staging" if staging else "production")
    (pub / "wp-config.php").write_text(cfg, encoding="utf-8")
    shutil.copy(TEMPLATES / "htaccess", pub / ".htaccess")
    (pub / "wp-content" / "uploads").mkdir(parents=True, exist_ok=True)
    shutil.copy(TEMPLATES / "uploads.htaccess", pub / "wp-content" / "uploads" / ".htaccess")

    b = data["business"]
    subs = {"{{NAME}}": b["name"], "{{DOMAIN}}": domain, "{{SLUG}}": site.slug, "{{DATE}}": stamp,
            "{{INDEX}}": "כבוי (אתר בדיקות zapsites)" if staging else "פעיל"}
    for f in ("DEPLOY.md", "deploy.sh"):
        t = (TEMPLATES / f).read_text(encoding="utf-8")
        for k, v in subs.items():
            t = t.replace(k, v)
        (root / f).write_text(t, encoding="utf-8", newline="\n")
    (root / "LAUNCH-CHECKLIST.md").write_text(launch_checklist(data, domain, staging), encoding="utf-8")
    shutil.copy(qa, root / "QA-REPORT.md")
    shutil.copy(site.src / "site.json", root / "site.json")

    zpath = DIST / f"{site.slug}-{stamp}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo.from_file(p, f"{site.slug}/{p.relative_to(root).as_posix()}")
                if p.name == "deploy.sh":
                    info.external_attr = 0o755 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                with open(p, "rb") as fh:
                    z.writestr(info, fh.read())
    shutil.rmtree(root)
    sha = hashlib.sha256(zpath.read_bytes()).hexdigest()
    (DIST / f"{zpath.name}.sha256").write_text(f"{sha}  {zpath.name}\n")
    mb = zpath.stat().st_size / 1048576
    return f"{zpath}  ({mb:.1f} MB, sha256 {sha[:12]}…)"


def launch_checklist(d, domain, staging):
    b, std = d["business"], d.get("standards", {})
    blockers = []
    if not std.get("privacy_url") or std["privacy_url"].startswith("/מדיניות"):
        blockers.append("קובץ מדיניות הפרטיות (PDF) מזאפ — כרגע מקושר עמוד זמני `/מדיניות-פרטיות/`. להעלות את ה-PDF ולעדכן את `zap_site.standards.privacy_url`.")
    if not b.get("dpz_customer_id"):
        blockers.append("customer-id של דפי זהב — בלעדיו אין בלוק ביקורות (וזה נכון). אחרי שמתקבל: להוסיף ל-site.json ולבנות מחדש, או לעדכן באופציה `zap_site`.")
    if not b.get("gmb_url"):
        blockers.append("קישור לכרטיס Google Business — לסכמה (sameAs/hasMap). לוודא שהשם, הכתובת והטלפון זהים לכרטיס.")
    ai = [k for k, v in d.get("images", {}).items() if v.get("ai")]
    lines = [f"# צ'קליסט עלייה — {b['name']}", "", f"דומיין: {domain}", ""]
    lines += ["## חוסמים (באחריות אדם)", ""] + ([f"- [ ] {x}" for x in blockers] or ["- אין"]) + [""]
    lines += ["## ביום העלייה", "",
              "- [ ] להריץ `deploy.sh` (או את השלבים ב-DEPLOY.md) ולהחליף סיסמת אדמין",
              f"- [ ] אינדוקס: {'כבוי — זה אתר בדיקות על zapsites. להדליק רק על הדומיין הסופי' if staging else 'דלוק. לאמת index,follow בעמוד אחד'}",
              "- [ ] SSL פעיל והאתר עונה ב-https בלבד",
              "- [ ] פנייה אחת לבדיקה מהטופס → לוודא שהגיעה לתיבה של הלקוח (רק עכשיו, לא בזמן הבנייה)",
              f"- [ ] טלפון בתצוגה {b.get('phone_display')} מחייג למספר הנכון ממובייל",
              "- [ ] Search Console + Bing: לאמת ולשלוח `sitemap_index.xml`",
              "- [ ] 301 מכל כתובת של האתר הישן (אם יש) — קפיצה אחת לכל כתובת",
              "- [ ] קאש (WP Rocket או של השרת) והרצה חוזרת של בדיקה אנונימית",
              "- [ ] כלל nginx שחוסם הרצת PHP בתיקיית uploads (ה-.htaccess לא עובד ב-nginx)", ""]
    lines += ["## מה כבר נבדק", "", "ראו QA-REPORT.md: כל עמוד ב-1440 וב-390, קישורים פנימיים, טלפונים, סכמה, טופס לידים.", ""]
    if ai:
        lines += ["## תמונות AI", "", f"תמונות שנוצרו ב-AI: {', '.join(ai)}. מסומנות בתיאור הקובץ. להחליף בצילומים אמיתיים כשיתקבלו.", ""]
    return "\n".join(lines)

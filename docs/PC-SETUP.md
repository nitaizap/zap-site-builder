# Zap sites pipeline: PC setup and first run (for Claude Code on the user's Windows PC)

You are Claude Code running **locally on the user's Windows PC**. This PC has two things the cloud
cannot reach: **desktop Outlook** (the sites team's emails) and the **F: drive** (`\\gpna01\Drive-f$`,
client images in `F:\SiteContent\<8-digit client id>\`). Your job: set this PC up once, run the intake
on the real inbox, and report back. The heavy work (building the sites) happens later in cloud sessions.

Work through the steps in order. Do not stop to ask between steps; collect anything unclear or failing
in an **Open items** list and give the user one report at the end (step 7). Stop early only if
something would need a password typed into chat, or would send an email.

## Hard rules

- **Never ask for, print, log or commit a password.** The user types the password themselves (step 2).
- **Never send, reply to, move or delete any email.** Outlook is read-only for you.
- Never commit to `main`. Client work goes on a `site/*` branch. **Two naming conventions are live and
  both are correct:** intake-created branches are `site/c<8-digit client id>` (`site/c80272199`), while the
  older, hand-started clients use a business-name slug (`site/patoccina`, `site/white-villa`,
  `site/lehem-erez-herzliya`, `site/kisos-beach-club`). Never rename an existing branch; match whatever a
  client already has, and use `site/c<id>` for anything new from intake.
- Never invent business facts; take them from the spec sheets.

## 1. Get the repo and the tools

In a terminal (PowerShell or Git Bash):

```bash
git --version
py --version
```

If either is missing, tell the user what to install (Git for Windows, Python 3.11+ from python.org with
"Add to PATH") and wait. Then:

```bash
cd %USERPROFILE%
git clone https://github.com/nitaizap/zap-site-builder.git
cd zap-site-builder
```

If the repo is already cloned: `git switch main && git pull`.
From now on work inside `zap-site-builder`. Read `CLAUDE.md` and `.claude/skills/zap-intake/SKILL.md`.

### 1a. Python packages

```bash
py -m pip install playwright pillow
py -m playwright install chromium
```

### 1b. The local WordPress toolchain (PHP + WP-CLI + MariaDB) - do not skip

`zs build`, `zs qa`, `zs seo`, `zs preview` and `zs package` all drive a real local WordPress. On Windows
the engine looks for a **portable** toolchain under `.tools/` (gitignored, so a fresh clone has none):

| what | where `engine/env.py` looks |
|---|---|
| PHP | `.tools/php/php.exe` |
| WP-CLI | `.tools/wp-cli.phar`, run as `php wp-cli.phar` |
| MariaDB | `.tools/mariadb-*-winx64/bin/` - started by the engine on `127.0.0.1:3307`, user `root`, no password, data dir `.tools/mdata` |

`bin/setup-cloud.sh` installs none of this: it is Ubuntu/apt only, for cloud sessions.
The Windows installer is **`tools/setup-windows.sh`**, run from **Git Bash** (it needs `curl`, `unzip`, `sed`):

```bash
bash tools/setup-windows.sh
bin/zs doctor      # php, wp-cli, mariadb, browser, network, gh - every line must be OK
```

What it does, so you can finish it by hand if a download fails: pulls the newest
`php-8.3.*-nts-Win32-vs16-x64.zip` from windows.php.net into `.tools/php/`, the newest MariaDB 11.4
`winx64` zip from archive.mariadb.org into `.tools/mariadb-11.4.*-winx64/`, and `wp-cli.phar` into
`.tools/`; then copies `php.ini-development` to `.tools/php/php.ini` and uncomments
`mysqli, pdo_mysql, gd, mbstring, openssl, curl, zip, intl, fileinfo, exif, sodium`, sets
`extension_dir = "ext"`, `memory_limit = 512M`, `display_errors = Off`, and points `curl.cainfo` /
`openssl.cafile` at a downloaded `cacert.pem`.

Verified working on this PC (2026-11): PHP **8.3.36 NTS x64**, MariaDB **11.4.13 winx64**, current
`wp-cli.phar`. Both versions are chosen by the script at download time, so a later run may install
newer ones; the engine finds MariaDB by glob, which is fine.

Overrides, if the defaults clash with something already on the machine:
`ZS_DB_HOST`, `ZS_DB_PORT` (default 3307 on Windows), `ZS_DB_USER`, `ZS_DB_PASS`.

### 1c. Console trap: always call the engine through `bin/zs`

`bin/zs` exports `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` before running `engine/zs.py`. Calling
`py engine/zs.py ...` directly on a Windows console with a Hebrew code page (862/1255) raises
`UnicodeEncodeError` / `UnicodeDecodeError` or prints mangled Hebrew. If you must bypass the wrapper
(PowerShell without Git Bash), set the variables yourself first:

```powershell
$env:PYTHONUTF8 = "1"; $env:PYTHONIOENCODING = "utf-8"
py engine/zs.py <command> ...
```

Do **not** use `py -I`: `-I` implies `-E`, so Python ignores `PYTHONIOENCODING` and `PYTHONUTF8` and the
Hebrew breaks again.

## 2. Saved WordPress login (the user does this, not you)

Ask the user to run these two lines **in their own terminal window** (not in this chat), with their
real values, then fully close and reopen Claude Code so the settings load:

```
setx ZS_WP_USER "their WordPress login email"
setx ZS_WP_PASSWORD "the shared staging password"
```

Check that they are set **without printing them**:

```bash
py -c "import os; print('user set:', bool(os.environ.get('ZS_WP_USER')), '| password set:', bool(os.environ.get('ZS_WP_PASSWORD')))"
```

## 3. Check access to F: and Outlook

```bash
py -c "import os; p=r'F:\SiteContent'; print('F: ok,', len(os.listdir(p)), 'client folders') if os.path.isdir(p) else print('F: NOT reachable')"
powershell -ExecutionPolicy Bypass -File bin/outlook-inbox.ps1 -Days 14
```

- Outlook must be open. The script only reads mail from `NetaS@d.co.il`, `SharonY@d.co.il`,
  `NoamR@d.co.il` and saves each message into `work/inbox/<id>/` (attachments, `body.txt`, `meta.json`).
- If PowerShell blocks the script or Outlook raises a security prompt, tell the user what to click and
  run it again. If it still fails, copy the exact error into Open items.

## 4. Run the intake (the `/zap-intake` skill)

Follow `.claude/skills/zap-intake/SKILL.md` steps 1 to 3 for every saved message:

```bash
bin/zs intake work/inbox/<id> --sender <from> --subject "<subject>" --body-file work/inbox/<id>/body.txt
```

(In PowerShell without Git Bash use `py engine/zs.py intake ...` instead of `bin/zs intake ...` - but set
`PYTHONUTF8` and `PYTHONIOENCODING` first, and never pass `-I`: see step 1c, or the Hebrew will break.)

- One email can hold several clients: one `.docx` = one site, folder `sites/c<id>/`.
- Images come from `F:\SiteContent\<id>\` automatically. Open 2 or 3 of the copied images to make sure
  they belong to that business.
- If the spec has a **WeTransfer** link (`spec.raw_graphics` / `image_sources` in `intake.json`), open it
  in the browser now and download the files into `sites/c<id>/assets/client/`. These links expire.
- Push one branch per client:

```bash
git fetch origin main
git switch -c site/c<id> origin/main
git add sites/c<id>
git commit -m "intake: <business name> (<id>)"
git push -u origin site/c<id>
git switch main
```

## 5. Hand each client to the cloud

**There is no `claude --remote` on this machine.** `claude --help` offers only `--remote-control`, which
attaches a remote-control client to a local session; it does not start a cloud session. Do not try to
work around it from the CLI.

The cloud session is started by a human, from the **Claude desktop app** (or claude.ai/code):
new session -> repo `nitaizap/zap-site-builder` -> environment `zap-sites` -> branch `site/c<id>` ->
paste the prompt. Put one prompt per client in the report (step 7) so the user can paste it:

```
/zap-site build sites/c<id> from sites/c<id>/brief/ and intake.json on branch site/c<id>.
Automatic mode: pick the design direction yourself and log open items in OPEN-ITEMS.md.
Staging: <url or "not yet: build locally, push when it arrives">.
For staging access use: zs connect --site <url> --handoff c<id>
```

## 6. Staging access (only for clients that already have a staging URL)

```bash
git switch site/c<id>
git pull
bin/zs staging c<id> --site <staging url>
```

It logs in with the saved login. If that fails, it requests "forgot password", finds the reset mail in
Outlook, sets the saved password and logs in. If the cloud session has asked for access
(`sites/c<id>/inbox/connect-request.json`), it also approves that. Look at `work/staging-approve.png`.
A cloud request expires after about 14 minutes; if one is pending, run this right after `git pull`.
This part has **not been tested on a real staging site yet**: if anything fails, record the exact
error and a screenshot path in Open items.

## 7. Record and report

- Add every handled message id (`entry_id` from `meta.json`) to `work/intake-state.json` under
  `"handled"` so the next run skips it.
- **`work/intake-state.json` is a weak guard: it is gitignored (`work/`) and therefore per checkout.**
  This PC has three checkouts of this repo - `~\zap-site-builder`, `~\Desktop\zap-sites\zap-site-builder`
  and `~\code\zap-site-builder` - each with its own state file, so a message handled in one is still
  "new" in the others. Always run the intake from the same checkout, and check the others before
  concluding a message is unhandled.
- The real cross-machine guard is **`fingerprints/clients.json`**, which is committed: one entry per
  client id with `first_seen`, `name` and `slug`. It survives a `site/c<id>` branch being deleted after a
  site ships, and `zs intake` skips a client already in it (`--force` overrides). Commit the new entry
  together with `sites/c<id>` on the client's branch.
- Give the user **one** short report in Hebrew:
  1. Done, per client: id, business name, images copied (how many) or missing, WeTransfer downloaded
     yes/no, staging URL yes/no, branch pushed, cloud session started or the prompt to paste.
  2. Open items: everything that failed or needs a decision, with the exact error.

## 8. After a successful run: make it automatic

Only once steps 3 to 6 have worked once: ask the user if they want this to run every hour while the PC
is on, and if yes, set it up as a scheduled task in Claude Code desktop with the prompt
`/zap-intake` (working folder: this repo, Outlook open). Then the user only reviews the end reports.

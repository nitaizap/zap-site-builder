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
- Never commit to `main`. Client work goes on branches `site/c<id>`.
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
py -m pip install playwright pillow
py -m playwright install chromium
```

If the repo is already cloned: `git switch main && git pull`.
From now on work inside `zap-site-builder`. Read `CLAUDE.md` and `.claude/skills/zap-intake/SKILL.md`.

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

(In PowerShell without Git Bash use `py engine/zs.py intake ...` instead of `bin/zs intake ...`.)

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

For each pushed branch, try to start a cloud session:

```bash
claude --remote "/zap-site build sites/c<id> from sites/c<id>/brief/ and intake.json on branch site/c<id>. Automatic mode: pick the design direction yourself and log open items in OPEN-ITEMS.md. Staging: <url or 'not yet'>. For staging access use: zs connect --site <url> --handoff c<id>"
```

If `claude --remote` does not exist on this machine, do not work around it: put the prompt for each
client in the report so the user can paste it into a new cloud session at claude.ai/code.

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
- Give the user **one** short report in Hebrew:
  1. Done, per client: id, business name, images copied (how many) or missing, WeTransfer downloaded
     yes/no, staging URL yes/no, branch pushed, cloud session started or the prompt to paste.
  2. Open items: everything that failed or needs a decision, with the exact error.

## 8. After a successful run: make it automatic

Only once steps 3 to 6 have worked once: ask the user if they want this to run every hour while the PC
is on, and if yes, set it up as a scheduled task in Claude Code desktop with the prompt
`/zap-intake` (working folder: this repo, Outlook open). Then the user only reviews the end reports.

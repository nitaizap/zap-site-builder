---
name: zap-intake
description: Local (Windows PC with the F drive) first half of the Zap site pipeline - check Outlook for new site requests from the sites team, save the Word spec sheets, copy each client's images from F by client id, push a site/c<id> branch and hand the build to a cloud session. Also catches staging-URL and feedback replies and routes them to the client's branch. Use for "בדוק מיילים מצוות אתרים", "intake", "יש אפיונים חדשים", or on the scheduled check.
---

# Zap intake (runs on the PC that sees F:)

Cloud sessions cannot see F:. This skill does only what needs the PC: mail + images. The build itself
runs in the cloud with `/zap-site` on the branch this skill pushes.

## Settings

| what | value |
|---|---|
| senders | `NetaS@d.co.il`, `SharonY@d.co.il`, `NoamR@d.co.il` |
| images root | `F:\SiteContent\<client id>\` (default; override with `ZS_IMAGES_ROOT`). F: is `\\gpna01\Drive-f$` |
| state | `work/intake-state.json` (handled message ids; **gitignored, so per checkout** - this PC has three clones of the repo, each with its own) |
| real guard | `fingerprints/clients.json` (committed, one entry per client id; survives branch deletion and other checkouts) |
| inbox folder | `work/inbox/<message-id>/` (attachments + `body.txt`; gitignored) |

## 0. One-time setup on the PC

```bash
py -m pip install playwright pillow
py -m playwright install chromium
bash tools/setup-windows.sh      # portable PHP + WP-CLI + MariaDB into .tools/ (needed by zs build/qa/seo)
setx ZS_WP_USER "<the user's WordPress login email>"
setx ZS_WP_PASSWORD "<the shared staging password>"
```

Full detail, and the UTF-8 console trap when calling `py engine/zs.py` instead of `bin/zs`:
`docs/PC-SETUP.md` steps 1b and 1c.

The user types the last two themselves in their own terminal; never ask for, echo or store the password.
Reopen the terminal after `setx`.

## 1. Find new mail

Desktop Outlook on this PC (the Microsoft 365 connector is blocked by the company's sign-in policy):

```bash
powershell -ExecutionPolicy Bypass -File bin/outlook-inbox.ps1 -Days 14
```

It saves each new message from the senders into `work/inbox/<id>/` (attachments, `body.txt`, `meta.json`)
and prints the list. Outlook must be open. (If the connector starts working, it may be used instead.)
Sort each message:

- **new request**: has `.docx` or `.xlsx` attachments with an 8-digit id (usually "<business> <id> - בייסיק.docx"
  for the Word template, "<business> <id> - וויקנד.xlsx" for the Excel one).
  One email can hold several clients: each spec sheet is one site.
  A client taken in before is **skipped**, with the evidence printed (a `site/c<id>` branch, another
  branch naming the id, a local `sites/` folder, or `fingerprints/clients.json`). That file is committed
  and is the only record that survives a branch being deleted once a site ships, so commit it together
  with `sites/c<id>` when intake says it added an entry. `--force` takes a client in again on purpose.
- **staging URL**: a reply naming a client id/business and a URL (`*.ussl.co.il` etc.) → step 4 (`zs replies`).
- **feedback**: a reply in the thread of a client already handed off → step 4.
- anything else: skip, list it in the summary.

## 2. Intake (new request)

The message is already in `work/inbox/<id>/` (step 1). Run:

```bash
bin/zs intake work/inbox/<message-id> --sender <from> --subject "<subject>" --body-file work/inbox/<message-id>/body.txt
```

It writes `sites/c<id>/` (brief/, intake.json, assets/client/) per spec and prints a JSON summary.
Open 2-3 of the copied images to check they belong to the client (folder names lie too).
An id with no F: folder is not a stop: the cloud session uses `image_sources` (WeTransfer link in the spec
expires: if there is one, download it on the PC into `sites/c<id>/assets/client/` now), rest.co.il, the old
site; say so in the summary.

## 3. Hand off (per client)

```bash
git fetch origin main && git switch -c site/c<id> origin/main
git add sites/c<id> && git commit -m "intake: <name> (<id>)" && git push -u origin site/c<id>
git switch main
```

If the branch already exists (a second email for the same client), switch to it, add, commit, push.
Then start the cloud build on that branch, prompt:

> /zap-site build sites/c<id> from sites/c<id>/brief/ and intake.json. Staging: <url or "not yet: build locally, push when it arrives">.

There is no CLI command that starts a cloud session (`claude --remote` does not exist; `--remote-control`
is a different thing). List the branches + prompts in the summary and the user opens the session from the
Claude desktop app or claude.ai/code: repo `nitaizap/zap-site-builder`, environment `zap-sites`, branch
`site/c<id>`, paste the prompt.

## 4. Staging URL / feedback replies (`zs replies`)

`zs intake` opens a client. Everything the sites team sends afterwards - "here is the staging
site", QA comments, a QA document - comes back as a reply in the same thread, and one reply often
covers several clients at once. `zs replies` sorts those and files each one under the client it is
really about. It never guesses: a message it cannot place is reported, not written.

```bash
bin/zs replies                        # dry run over work/inbox: prints what it would write, per client
```

Read the dry run before anything else. Then, per client, on that client's branch:

```bash
git switch site/c<id> && git pull
bin/zs replies --client <id> --write
git add sites/c<id> && git commit -m "replies: <name> (<id>)" && git push
```

`--write` is per checkout: a run covers several clients, so it only writes for the `sites/c<id>/`
folders that are actually in the working tree and names the branch to switch to for the rest.
It never commits or pushes - that stays above, so a wrong attribution is seen before it lands.

What it writes per (message, client):

- `sites/c<id>/inbox/<YYYY-MM-DD>-<kind>.md` (kind = `staging` when the message brings a staging URL
  this client did not have, otherwise `feedback`): sender, subject, received, entry_id, the staging
  URLs, and the part of the reply text that belongs to this client.
- the real attachments next to it. The five signature logos (`11933939571542770323.png` and friends),
  `image001.png`-style Outlook artefacts and `Outlook-*.png` are dropped.
- `staging_url` in `sites/c<id>/intake.json`, with "staging URL" removed from `missing`.

How it decides whose reply it is:

- **staging URL -> the id in its host.** Outlook safelink wrappers are unwrapped first, and the host
  carries the client id even when it is dressed up (`80392210kisos.ussl.co.il`,
  `erezbread80049225.ussl.co.il`, `80393140pig.ussl.co.il`). A host with no id goes to the client
  only when the message is about exactly one.
- **text -> the client named last above it**, by 8-digit id or by business name, so
  "הוילה הלבנה:" followed by its URL does not spill onto the next client in the list. Lines before
  any client is named are shared by the clients this sender named - never by one that only appeared
  in the quoted thread below.
- **business names** come from the spec sheets in `work/inbox`, the checked-out `sites/` and the
  `site/c<id>` branches. A name two clients both answer to is never used.
- a name and an id in the same subject that disagree (a typo in one of them) is a clash: nothing is
  written for the disputed client and it is listed under "Not attributed".

Message classes printed by the dry run: `new_spec` (a spec attachment - step 2, not this step),
`staging`, `feedback`, `other`.

Then tell the cloud session for that client (the user's session list, title "c<id> …") to pull and act;
if none is reachable, put the prompt in the summary. Everything under "Not attributed" goes in the
summary too, as an open item - never onto a branch on a hunch.

## 4b. Staging access (replaces "forgot password" + pasting the code)

For every client with a staging URL, and whenever `git pull` brings a `sites/c<id>/inbox/connect-request.json`:

```bash
git switch site/c<id> && git pull
bin/zs staging c<id> --site <staging url>
```

It logs in with the saved password, or does the password reset itself (reads the reset mail in Outlook,
sets the usual password), then approves the cloud session's access code. Check `work/staging-approve.png`.
Run this check every few minutes while a cloud session waits for access (it waits 14 minutes).

## 5. Record + report

Add every handled message id (`meta.json` entry_id) under `handled` to `work/intake-state.json`. Report in Hebrew, short: per client: id, name,
images copied (n) or missing, staging yes/no, branch, cloud session started or prompt to paste.
Never reply to the sites team from here, never mail a client.

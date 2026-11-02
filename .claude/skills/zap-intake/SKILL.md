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
| state | `work/intake-state.json` (handled message ids; gitignored) |
| inbox folder | `work/inbox/<message-id>/` (attachments + `body.txt`; gitignored) |

## 0. One-time setup on the PC

```bash
py -m pip install playwright pillow
py -m playwright install chromium
setx ZS_WP_USER "<the user's WordPress login email>"
setx ZS_WP_PASSWORD "<the shared staging password>"
```

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
- **staging URL**: a reply naming a client id/business and a URL (`*.ussl.co.il` etc.) → step 4.
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

Start it with `claude --remote "<prompt>"` from the repo when that is available; otherwise list the
branches + prompts in the summary for the user to paste into a new cloud session.

## 4. Staging URL / feedback replies

Write the reply text to `sites/c<id>/inbox/<date>-<kind>.md` (kind = staging | feedback; images in the
reply → same folder), set `staging_url` in `intake.json` when given, commit + push to `site/c<id>`.
Then tell the cloud session for that client (the user's session list, title "c<id> …") to pull and act;
if none is reachable, put the prompt in the summary.

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

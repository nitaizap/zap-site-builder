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
| images root | `F:\` (searched 4 levels deep for a folder whose name contains the 8-digit client id) — set `ZS_IMAGES_ROOT` to narrow it |
| state | `work/intake-state.json` (handled message ids; gitignored) |
| inbox folder | `work/inbox/<message-id>/` (attachments + `body.txt`; gitignored) |

## 1. Find new mail

Microsoft 365 / Outlook connector: search mail from the senders above, last 14 days, that is not in
`work/intake-state.json`. Sort each message:

- **new request**: has `.docx` attachments with an 8-digit id (usually "<business> <id> - בייסיק.docx").
  One email can hold several clients: each .docx is one site.
- **staging URL**: a reply naming a client id/business and a URL (`*.ussl.co.il` etc.) → step 4.
- **feedback**: a reply in the thread of a client already handed off → step 4.
- anything else: skip, list it in the summary.

## 2. Intake (new request)

Save attachments + the body (UTF-8) into `work/inbox/<message-id>/`, then:

```bash
bin/zs intake work/inbox/<message-id> --images-root "${ZS_IMAGES_ROOT:-F:\\}" --sender <from> --subject "<subject>" --body-file work/inbox/<message-id>/body.txt
```

It writes `sites/c<id>/` (brief/, intake.json, assets/client/) per spec and prints a JSON summary.
Open 2-3 of the copied images to check they belong to the client (folder names lie too).
An id with no F: folder is not a stop: the cloud session researches images (rest.co.il, the old site);
say so in the summary.

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

## 5. Record + report

Add every handled message id to `work/intake-state.json`. Report in Hebrew, short: per client: id, name,
images copied (n) or missing, staging yes/no, branch, cloud session started or prompt to paste.
Never reply to the sites team from here, never mail a client.

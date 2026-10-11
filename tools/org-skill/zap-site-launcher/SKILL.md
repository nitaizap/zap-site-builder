---
name: zap-site-launcher
description: Starting point for building a Zap Group client website (Hebrew WordPress + Elementor site from a client brief / טופס איפיון, delivered through Novamira). Use in a claude.ai chat when someone pastes a client brief, asks "בנה אתר ללקוח", "אתר חדש ללקוח", "תקים אתר", or asks how Zap builds client sites. Routes the work to the zap-site-builder repo in Claude Code, where the real skill and engine live.
---

# Zap site builder — where to run it

Client websites are built by the `/zap-site` skill inside the GitHub repo **nitaizap/zap-site-builder**, which also
holds the build engine and the shared theme. A chat alone cannot build or push the site, so:

1. Open **claude.ai/code** → new session → repository `nitaizap/zap-site-builder`, environment **zap-sites**.
2. Type `/zap-site` and paste the brief (text, the איפיון file, logo, photos, old-site link, the staging URL
   `https://<client>.ussl.co.il` if one exists). One client per session; open more sessions for more clients.
3. Write "בלי עצירות" to let it run to the end without waiting; it still asks once if a fact (phone, lead
   email) is missing.

Access needed: GitHub access to the repo, Claude Code on the web with the GitHub app, the `zap-sites` environment.
The session runs in the cloud: the computer can be closed; come back from any device to the same session.

If the user only wants advice in this chat (what a brief is missing, a sitemap, copy ideas), help directly,
following Zap's rules: never invent business facts (years, numbers, reviews, prices), one keyword per page,
Hebrew copy written for the business's real customers.

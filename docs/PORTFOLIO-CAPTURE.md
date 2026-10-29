# Task: capture Zap's website portfolio for the site-builder skill

You are a browser agent on the user's computer. Your output will be handed to a cloud agent that
cannot reach zapgroup.co.il (Cloudflare blocks it). Your job is **collection only**: open pages, take
screenshots, write down what you see. Do not log in anywhere, fill forms, accept offers or download files
other than your own screenshots.

## 1. Open the portfolio

1. Open https://zapgroup.co.il/services/websites/#portfolio in a normal browser window (desktop, at least
   1280 px wide). Wait for it to load; scroll slowly to the end of the page so lazy images and sliders load.
2. Take a full-page screenshot of the whole page → `00-zap-websites-full.png`.
3. Take a screenshot of the portfolio section alone → `00-portfolio-section.png`. If the portfolio has
   tabs, filters, categories or a "load more" button, open each one and screenshot each state
   (`00-portfolio-<tab-name>.png`).
4. Write down every portfolio item: client/business name, category shown, the link it opens (copy the real
   URL from the address bar after clicking, not the thumbnail's alt text), and the thumbnail image URL if you
   can copy it (right-click → copy image address).
5. Also copy, as plain text, everything the page says about the website packages/products (names such as
   בייסיק / פרימיום / חנות, what each includes, any features listed: booking, menu, shop, gallery, video,
   accessibility, SEO, etc.) → `packages.txt`.

## 2. Visit every portfolio site (all of them, up to 40)

For each portfolio item that opens a real website:

1. Open it. Wait 3 seconds, then scroll slowly to the bottom and back to the top (loads lazy images and
   triggers animations).
2. Screenshots, desktop window 1440 px wide:
   - `NN-<slug>-desktop-full.png`: full page
   - `NN-<slug>-desktop-fold.png`: just the first screen (no scrolling)
3. Screenshots, phone width: open DevTools device mode at **390 × 844** (iPhone 12/13/14), reload, then
   - `NN-<slug>-mobile-full.png`: full page
   - `NN-<slug>-mobile-fold.png`: first screen
4. Open the site's menu and screenshot one or two inner pages that look different from the home page
   (a services / menu / gallery / about page): `NN-<slug>-inner-<page>-desktop-full.png`.
5. If something moves (slider, animated counters, scrolling ticker, parallax, video, hover effects), note
   it in words; a screenshot can't show it.

`NN` = 01, 02, … in portfolio order. `<slug>` = short latin name of the business (e.g. `pizza-roma`).
If a site doesn't load or is not a website (an app store link, an Instagram page), note it and skip.

## 3. Write `portfolio.json`

One entry per portfolio item, in this exact shape:

```json
[
  {
    "n": "01",
    "name": "business name as shown",
    "url": "https://…",
    "category": "restaurant / clinic / lawyer / shop / … (as shown, else your best guess, marked guess)",
    "platform": "WordPress / Wix / other, if visible (footer, page source)",
    "palette": ["#hex", "#hex", "#hex"],
    "fonts": "heading / body font names if you can read them (DevTools → Computed → font-family)",
    "hero": "what the first screen is: full-bleed photo / video / split text+photo / slider / centred text …",
    "home_sections": [
      "in order, one line each: e.g. 'hero: full-width food photo, logo centred, 2 buttons'",
      "'menu tabs with prices'", "'gallery: 3 tall photos + more button'", "'reviews carousel'", "…"
    ],
    "special_elements": ["anything unusual: booking widget, order online, price table, before/after slider, map, video, countdown, sticky WhatsApp, popup …"],
    "motion": "what moves, in words",
    "mobile_notes": "what changes on the phone: sticky call bar, hamburger style, stacked buttons …",
    "footer": "what the footer contains",
    "screenshots": ["01-…-desktop-full.png", "…"]
  }
]
```

## 4. Deliver

Put everything in one folder named `zap-portfolio-capture/` (screenshots, `portfolio.json`,
`packages.txt`, plus a `notes.md` with anything you couldn't capture and why). Zip it as
`zap-portfolio-capture.zip`. Keep each screenshot under 5 MB (JPEG at quality 80 is fine for full
pages). Tell the user where the zip is, so they can upload it to the cloud session.

## Rules

- Collect, don't judge or redesign. Exact text and real URLs matter more than opinions.
- Don't copy client photos for reuse; the screenshots are only for studying layout.
- If Cloudflare shows a check page, complete it the normal way (wait / click the checkbox) once. If it keeps
  blocking, stop and tell the user.

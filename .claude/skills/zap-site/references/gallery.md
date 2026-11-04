# Gallery: our own approved sites, and what the user corrected on them

`benchmark/` is other people's work: Zap templates, a team designer's build, basic-site references. It sets the
finish level but it has never been through a round with this user.

`gallery/` is **ours**: every site that reached handover, with its screenshots, its approved direction, and the
corrections the user actually made on it. It exists because rules did not transfer the level. The same thing
that is written in `design.md` as a sentence is obvious in two seconds as a picture, and the corrections are the
only record of this user's taste that a fresh session can read.

Each entry is one folder, `gallery/<slug>/`:

```
gallery/<slug>/
  README.md              the template below
  01-home-desktop.jpg    1440 wide, full page
  02-home-mobile.jpg     390 wide, full page
  03-inner-desktop.jpg   a service or content page
```

## Read it before composing (step 2)

Before choosing kits, archetypes and sections, open the **1–2 nearest** entries: same industry, same audience,
or the nearest package. Read their images, then their "what the user corrected" section. Then write two lines
into `NOTES.md`:

- **Borrow:** the level of finish, the image density, the section count, the mobile treatment.
- **Must differ:** palette, type pairing, hero type, the bold element. Cross-check `pool.md` — the pool gate
  measures this numerically, but it cannot tell you that two sites feel the same.

## The floor the directions have to clear (step 3, before the user sees anything)

A direction below any of these is not ready to show. Measured on the approved entries in `gallery/`:

| measure | floor | why |
|---|---|---|
| real images on the home direction | 6+ | a direction with two images cannot be judged, and reads as a wireframe |
| icons on conversion buttons and contact lines | all of them | `zs qa` counts the ones without |
| a 390 frame per direction | always | mobile defects are the ones clients notice and the ones desktop hides |
| sections on the home | 8+ (`basic` 6+) | fewer means the content is under-represented, and the page looks thin |

If the client's own photography cannot carry a direction, say so **at the gate**, not after the build. That is
a brief question, and it is cheap to answer in the preview round and expensive after.

## Write the entry (after handover)

At the end of the delivery step, create `gallery/<slug>/` and fill the template. This is not optional: the next
site is composed from it.

```markdown
# <client>

| | |
|---|---|
| industry | |
| package (`tier`) | |
| state | handed over dd/mm/yyyy · live <url> |
| kit · archetype · preset | |
| direction chosen | <A/B/C, and in one line why> |

## Tokens
<font pairing and weights · palette with hex and role · anything that left the default scale>

## Images
<where they came from: client / old site / Weave AI (model) — and how many>

## What the user corrected
<every correction from the preview round onward, in the user's own words where possible, and what we did.
This is the part the next session reads. Write it even when the correction was small.>

## What to take from here
<2–4 patterns worth reusing on another client>
```

Keep it honest. An entry that records only what went well is worth nothing to the next build.

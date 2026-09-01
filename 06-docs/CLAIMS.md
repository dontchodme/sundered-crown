# CLAIMS — WHO IS DESIGNING WHAT, RIGHT NOW

**Read this before you design anything. Write to it before you ask Rick a
single question.**

This file exists because the same failure happened twice in two days and cost
two relics' worth of design work:

```
v60   bloodsworn x warhammer   Cowork (Ravelbone) vs Claude Code (red hammer)
v61   umbral x bow             Cowork (Gloamwire) vs Claude Code (Quiver)
```

Both times two sessions designed the same cell in parallel, neither could see
the other, and **Rick answered a full set of design questions in both** — so
half of one day's decisions had to be thrown away. Both times the second
session was told to go and find a design document, found nothing, and
**started designing its own ultimate without direction**, which is the exact
symptom this file is here to stop.

Sessions cannot see each other. **The repo is the only place they can both
look.** So the claim goes in the repo, and it goes in FIRST.

---

## THE PROTOCOL

**1. READ THIS FILE BEFORE THE FIRST SURVEY.** Not before the build — before
the *design*. If the cell you are about to work on is claimed and the claim is
`OPEN`, stop and tell Rick who has it. Do not "just have a look at it".

**2. CLAIM YOUR CELL THE MOMENT IT IS CHOSEN**, before the first survey, and
long before the first spread of names. One line. Commit it on its own.

```
| <cell> | <what> | <session> | <UTC claimed> | <status> | <doc path> |
```

`status` is `OPEN` while the design is being made, `DESIGNED` when the doc and
brief exist, `BUILDING` while Code has it, `SHIPPED` when it is in a link, and
`SUPERSEDED` when Rick has ruled against it.

**3. WRITE THE DOC PATH IN THE CLAIM BEFORE THE DOC EXISTS.** A path with
nothing at it says "a design is being made and it will be here". That is the
signal both collisions were missing — the second session in each pair looked
for a file, found nothing, and inferred that nothing was happening.

**4. PUT A STUB AT THAT PATH IN THE SAME BREATH.** Twenty words is enough:
the cell, the session, the time, and `IN PROGRESS — do not build`. A stub
costs one write and it is the difference between "nobody is on this" and
"somebody is on this and has not finished".

**5. IF THE BRIEF IS NOT THERE — STOP.** That is CLAUDE.md §3 rule 0 and it is
Rick's, in his own words. This file is what makes the rule usable: it tells you
whether "not there" means *nobody is on it* or *somebody is on it and has not
finished writing*. Those are different situations and only one of them is a
cell you may claim.

---

## THE TABLE

| cell | what | session | claimed (UTC) | status | doc |
|---|---|---|---|---|---|
| bloodsworn × warhammer | Ravelbone / Garrote | Cowork | 2026-09-01 ~07:4x | SHIPPED | `06-docs/v60/ravelbone-build-v60.md` |
| bloodsworn × warhammer | the red hammer, wall-slam | Claude Code | 2026-09-01 08:35 | SUPERSEDED | `06-docs/v60/redhammer-design-v60-SUPERSEDED.md` |
| umbral × bow | Gloamwire / Crossweave | Cowork | 2026-09-01 07:33 | DESIGNED | `06-docs/v61/gloamwire-design-v61.md` |
| umbral × bow | Quiver, the misses come back | Claude Code | 2026-09-01 ~18:45 | SUPERSEDED | `06-docs/v61/quiver-design-v61-SUPERSEDED.md` |
| umbral × bow | Gloamwire / Crossweave, BUILD | Claude Code | 2026-09-01 20:10 | BUILDING | `tools/gloamwire_build.py` |
| bloodsworn × scythe | Bloodmirror / Bloodletting | Cowork | 2026-09-01 | DESIGNED, NOT BUILT | `06-docs/v59/bloodmirror-build-brief-v59.md` |
| umbral × scythe | the purple tornado — §1 in, clause 3 measured dead, awaiting ruling | Cowork | 2026-09-01 20:17 | OPEN | `06-docs/v62/umbral-scythe-design-v62.md` |

**`bloodsworn × scythe` WAS the row that proved the point, and it is closed as
of 2026-09-02.** Bloodmirror was designed in full on 2026-09-01 — named,
composed, its bleed-ceiling rule ruled on, knockback chosen — and for a day it
existed only in a chat transcript, in no link and in no `06-docs/` folder. The
Cowork session that designed it wrote it out and the device bridge dropped
mid-write; the files sat in that transcript until the bridge came back.

**Its five documents are now in the repo** — `06-docs/v59/` holds the build
brief, the spectre design, `budget-v59.md` (why this cell) and
`tip-surface-v59.md` (stage T, four sim-inert tip changes), with
`tools/spectre_lab.py` alongside. **It is the 30th relic and it is ahead of
nothing** — Ravelbone (31st cell filled) and Gloamwire were both built while it
waited, so it is now the oldest unbuilt design in the project.

**The lesson it was standing for still holds and is worth keeping:** a
deliverable that lives in a chat message does not exist, and the failure mode
was not forgetting to write — it was writing once, at the end, into a channel
that could fail. §4 of the protocol above is the answer: the stub goes in
first, and it goes in early, because a stub survives a dropped connection and a
finished document held in a transcript does not.

---

## WHAT ELSE THE TWO COLLISIONS COST, AND THE CHEAPER SIGNALS THAT WERE THERE

- **A modified tool with a fresh timestamp is a claim signal.**
  `tools/bow_survey.py` was written at **07:32 UTC** on 2026-09-01, one minute
  before the Gloamwire session opened the repo. That session saw the fresh
  mtime, could not explain it, and dismissed it as a git artifact. **It was the
  other track starting up**, and it was the only warning that existed.
- **The relic number drifts every time two sessions count separately.**
  Gloamwire's doc called the umbral bow the 32nd (design order); the bow-row
  survey called it the 31st cell (built order). v57 had the same drift. **§0 of
  CLAUDE.md is where the number is settled** and both docs should defer to it.
- **A design that never reaches the repo did not happen.** Bloodmirror is the
  standing example. A chat transcript is not a deliverable and Code cannot read
  one.

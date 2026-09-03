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
| bloodsworn × scythe | Bloodmirror / Bloodletting | Cowork | 2026-09-01 | DESIGNED | `06-docs/v59/bloodmirror-build-brief-v59.md` |
| bloodsworn × scythe | Bloodmirror / Bloodletting, **BUILD** — stage T (tip surface) and stages 1-2 green; blade at 3b. Tip hook off `_scBarbed` and the landing ring + stronger pool are Rick's, 2026-09-01 | Claude Code | 2026-09-01 | SHIPPED | `06-docs/v59/bloodmirror-build-v59.md` |
| umbral × scythe | **Duskreave / Scour** — everything but card/animation/sound settled and CHECKED (v63). Rick ruled 2026-09-02: KEEP 7 ticks/s; and curse goes to a LAST-3 window school-wide (row below), under which Scour prices **+40.5pp** (+59.2 under today's rule). Card line his (2026-09-02); animation reference his (`v63/ref-vortex.mp4`); sound = Code renders a spread. **BRIEF: `06-docs/v63/DUSKREAVE-BUILD-BRIEF.md`.** | Cowork | 2026-09-01 20:17 · v63 2026-09-02 | DESIGNED, NOT BUILT | `06-docs/v63/DUSKREAVE-BUILD-BRIEF.md` |
| umbral × scythe | Duskreave / Scour, **BUILD** — **BUILT, stages 1-5c, in `02-chain/sc-lastthree.html`.** Tick damage 5 → **1** (Rick's, measured: the curve is a cliff, 30 points for one point of tick damage and no crossing above 1). Band height doubled for the picture, which doubled the catch — see the build doc §15b. **NOT the build of record; the app still loads `sc-nova.html`.** | Claude Code | 2026-09-02 | BUILT, NOT SHIPPED | `06-docs/v63/duskreave-build-v63.md` |
| **CURSE RULE, school-wide** | the pool keeps the LAST 3 hits instead of the 3 BIGGEST — Rick's ruling 2026-09-02. **LANDED 2026-09-02** in `02-chain/sc-lastthree.html` (`tools/curse_window_build.py`), at Rick's instruction, so Duskreave's blade could be balanced against the rule the game will actually have. Gate: 2808/2808 identical on the 27 relics that cannot apply curse; the 6 that can DIFFER, as they must. **THE RE-PRICING THIS CLAIM GATED IS STILL OWED** — the four built umbral relics were ruled on at 320-350 fights an arm, under the n≈700 floor. | Cowork (landed by Claude Code) | 2026-09-02 00:3x | LANDED, RE-PRICING OWED | `06-docs/v63/curse-window-v63.md` |
| umbral × bow | Crossweave, **THE CARRY** — stages 7-12 (held trio, nova, drawn explosion, voice, card line) existed only in `sc-crossweave.html` and were NOT in `sc-bloodletting.html`, which is what the app loads. Re-applied on top of the tip as a NEW link so Duskreave's base does not move under it. Rick, 2026-09-02: *"can you push your stuff in while duskreve runs?"* **DONE: `02-chain/sc-nova.html`, 32 relics, and the app points at it.** engine_ab 2790/2790 over the other 31, shell_identity 200/200, verify 12/13, blade 7.25 re-measured at 32 (crossing 7.22 against 7.25 at 31 -- a new relic moved it by a third of the measurement's own precision). | Claude Code | 2026-09-02 | SHIPPED | `06-docs/v61/gloamwire-build-v61.md` |
| **vigil × twinblade** | **Arclight / Static** — the 34th relic. §1 Rick's, priced live (+33pp on a body already at 57% with the ward alone), three rulings 2026-09-02: the big storm, blast 80, "the storm is the fighter" (lightest blade in the game). Names his. **Card line his (2026-09-02): "Hits spawn forking lightning. Caught bolts apply ward. All explode at 8s" (72).** Open: bolt art and sound as rendered spreads (stage 5). **BRIEF: `06-docs/v64/ARCLIGHT-BUILD-BRIEF.md`.** | Cowork | 2026-09-02 02:40 · designed ~05:00 | **SUPERSEDED — THE CELL IS OPEN AGAIN.** Built to this brief and scrapped by Rick on 2026-09-02 (row below). A replacement ultimate for this cell is Rick's and Cowork's; Code does not design one (rule 0). | `06-docs/v64/ARCLIGHT-BUILD-BRIEF.md` |
| **vigil × twinblade** | **A NEW DESIGN IS WANTED AND NOT STARTED.** Rick, 2026-09-02, after scrapping Arclight: *"a new design for the same cell."* **Nobody has claimed it — if you are designing this, put your line and a stub above this one FIRST** (protocol §2-4). What the last attempt measured about the CELL, as opposed to about Arclight, is in `06-docs/v64/vigil-twinblade-CONSTRAINTS.md`: the body wins 21.8% at the row's blade floor and 54.2% at the donor body with NO ultimate, the blade is worth only 13 points across its whole usable range, two payoffs on one ultimate can be substitutes, and an overlay has to close the hall. Code builds it when it lands and does not design it (rule 0). | Rick | 2026-09-02 | AWAITING A DESIGN | (none yet) |
| **vigil × twinblade** | Arclight / Static, **BUILD — SCRAPPED BY RICK, 2026-09-02**, after he watched it: *"i dont like what ive built. lets start over."* Stages 1-3 were built and gated green (engine_ab 5280/5280, 4224/4224, 4224/4224; probe 12/13 then 19/20; gate 3 in tier against a local reproduction of the model). `sc-arclight`, `sc-storm` and `sc-static` are DELETED and the chain is back to `sc-lastthree` at 33. They are in git at `4f022f4` and `tools/arclight_build.py` rebuilds them byte-identically, so what was scrapped is a decision and not the work. **Four measurements outlive it and are in the build doc**: no blade balances a relic that wins off its ultimate (80.6% at dmg 0.5 against a 0.0% body); two payoffs on one ultimate can be SUBSTITUTES (the ward feed costs 3.6pp to delete and is worth +29.2 alone); a lab that bounces things off the ARENA is not measuring a hall whose seals close; and the design's published +33.1 reads +37.5 on the pinned runtime. | Claude Code | 2026-09-02 | SUPERSEDED | `06-docs/v64/arclight-build-v64.md` |
| **umbral × scythe, SILHOUETTE** | Duskreave's weapon art REDRAWN from Rick's three references (`06-docs/v63/ref-scythe-1/2/3.jpg`). Rick ruled 2026-09-02 ~03:58 UTC that **Cowork owns this redraw** — Code's `umbral_scythe_lab.py` spreads (A–F, G–J) are superseded. **Rick chose THE MOON (arm A) ~04:30 UTC. The spec is `06-docs/v63/scmoon_spec.js` (`_scMoon`, checked pixel-identical to the sheet he chose from); build notes are doc §5. Code: paste, route umbral → `_scMoon`, delete `_scEaten`, gate, film.** | Cowork | 2026-09-02 03:58 · designed 04:35 | DESIGNED, NOT BUILT | `06-docs/v63/umbral-scythe-silhouette-v63.md` |
| **PACE, chain-wide** | THE MINUTE — mean fight ~48s → ~60s by the pace_build lever scaled again: **S = H = 1.30 recommended** (baseHP 520, seals 27/64, hall closes at 27, timeout 156), priced roster-wide on all 528 pairings at Chromium 141 (60.1s mean, 0 timeouts, ults 4.2 → 5.5, worst pairing ~100s). Six relics move ≥9pp at n≈96 — Ravelbone, Marrowdraw down; Axiom, Bloodmirror, Cindercleave up — so `verify --n 40` will want two or three damage touches. **Rick chose 1.30/1.30 and ruled ACCEPT the pairing ceiling (2026-09-02 ~21:10 UTC).** Code builds `pace60_build.py` from doc §5; the link it lands on is the builder's question. | Cowork | 2026-09-02 21:00 · ruled 21:10 | CHOSEN, NOT BUILT — CODE'S TO BUILD | `06-docs/v65/pace-60-v65.md` |
| **PACE, chain-wide** | THE MINUTE, **BUILT** — `pace60_build.py`, `sc-lastthree` → **`02-chain/sc-minute.html`**. Six anchored edits: baseHP 400→520, seals 21/49→27/64, `collapse.startT` 21→27 in the same edit as the seal, timeout 120→156, plus two comments that would have gone stale (one cited `intro.dur`, gone since the fight card). **MEAN 47.5s → 60.2s on all 528 pairings, 0 timeouts, ults 4.2 → 5.5** — and **the Chromium-141 pricing REPRODUCES on the pinned 151 to a tenth of a second** on mean, median, p90 and ults. engine_ab 135/135 DIFFER (the pass); text diff 72 lines and they are the six edits and the stamp; chain_audit 28/28 on duskreave_build. **verify 11/13 and BOTH REDS ARE THE CLOCK** — the known pairing band (99.0s, ruled accept) and the overall-mean band, which is 28-54s and cannot contain a minute; not widened, because a gate moved by the build it judges is not a gate. **Every relic in 30-70%, so NO damage number moves** and the design's "two or three damage touches" does not land. **Found on the way: the chain is FORKED and this branch is missing Crossweave's stages 7-12, which live in `sc-nova` only.** **Clip pipeline handled too** (doc §5): shorts_build MAX_SECONDS 180 and a ladder that only loudness climbs, cinema_clip's whole-fight cap off CONFIG.timeout, pick_fight's --secs off CONFIG.timeout, and a guard on the ladder filter. One whole fight delivered end to end: 64.3s, 5/5 marks. NOBODY HAS WATCHED A SIXTY-SECOND FIGHT. | Claude Code | 2026-09-02 | BUILT, NOT SHIPPED | `06-docs/v65/pace60-build-v65.md` |

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

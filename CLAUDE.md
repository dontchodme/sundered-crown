# SUPER WEAPON BALL: THE SUNDERED CROWN

**This file replaces the handoff zip.** Read it first, every session. If
something in it is wrong, fix it in the same session — a stale CLAUDE.md is
how the handoff problem comes back.

Rick's project. A deterministic 2-relic arena fight, rendered to vertical
short-form video for TikTok and YouTube Shorts.

---

## 0. STATE OF THE PROJECT

```
02-chain/sc-paradox-frame.html   BUILD OF RECORD   25 relics · Stasis Field
01-live/sundered-crown.html      LIVE              16 relics — NINE BEHIND
01-live/sc-playable.html         LIVE              16 relics — NINE BEHIND
```

`01-live` has been untouched since v37. **That gap is the oldest open item in
the project** (v27 open decision 1) and it is not a bug — nobody has decided
which of the nine ships.

---

## 1. WHAT THE ENGINE ACTUALLY IS

One self-contained HTML file. **No imports, no `<script src>`, no
dependencies.** Vanilla JS, Canvas 2D, WebAudio.

The thing that matters most about it:

> **The simulation does not know a screen exists.** `Fighter`, `Match` and
> `Sfx` contain zero references to `document`, `canvas` or `getContext`.
> `Renderer` is a separate class. The seam between sim and picture is already
> clean — which is why the renderer can be replaced and the fights stay
> bit-identical.

| | |
|---|---|
| timestep | `CONFIG.physics.dt` = **1/120**. Never hardcode 1/60. |
| randomness | mulberry32 on an integer seed. **The seed IS the fight.** |
| audio | fully synthesized in WebAudio. There are no sound files. |
| determinism | `(build, relic A, relic B, seed)` → the same fight, always — **on the same V8.** Measured 2026-08-26 and now pinned; `tools/math_fingerprint.py` is the check. `docs/RUNTIME-DRIFT.md`. |

**Everything downstream rests on that last line.** Clips, measurements,
`engine_ab`, every tuned number. Anything that breaks determinism invalidates
the entire history of the project, not just the current session.

---

## 2. WHERE THINGS ARE

| folder | what is in it |
|---|---|
| `01-live/` | what ships. `sc-playable.html` is the same engine in the share shell. |
| `02-chain/` | how the build was made, in order. `sc-base.html` is the ROOT. |
| `04-experiments/` | unshipped variants **and controls**. Several are the control for a measurement, not a candidate. |
| `05-reference/` | images, filmstrips, the clickable fighter review. |
| `06-docs/` | the write-ups, one folder per version. `06-docs/v43/` is current. |
| `07-shorts/` | delivered videos. **mp4s are gitignored — the seed rebuilds them.** |
| `08-analytics/` | retention curves and cold-open reads off real posts. |
| `tools/` | every builder, probe and renderer. **Flat on purpose.** |
| `app/` | the Electron desktop app. NEW — see `docs/ARCHITECTURE.md`. |

### Why `tools/` has no subfolders

Every tool resolves the game by looking beside itself
(`HERE = Path(__file__).parent`) and imports `scpage.py` the same way.
Subfoldering would break all 195 of them, and break them **silently** — the
import fails only when you run it. The grouping lives in `tools/README.md`.

**Do not reorganize `tools/` without changing that resolution first.**

---

## 3. THE THREE RULES, AND THEY ARE RICK'S

1. **THE FIGHT CARD IS DEAD.** Nothing ships with one. `cinema_clip --intro`
   and `--cold-open` refuse to run without `--legacy-card`. The card is still
   in the build; removing it is a chain-wide job, unstarted for five sessions.

2. **RICK GIVES INPUT ON SEVEN THINGS.** The cell, the ult mechanics, the ult
   name, the fighter name, the scrunch card wording, the ult animations, the
   ult sound. **If he has not offered, ASK** — with real options, the trade
   named, and priced from measurement first wherever a measurement can price
   it.

   **OFFER A SPREAD, NOT A GUESS.** v42 spread after four serial failures.
   v43 spread first and the sound landed in one round trip: six casts and four
   holds rendered before he was asked anything. "First option on both."
   Being wrong about the *register* is what costs — a spread of one can never
   reveal it.

3. **A HIT-HEAVY ULT MUST DECLARE ITSELF TO THE DIRECTOR.** If the ultimate
   does something the beat system cannot see, `cinePlan` scores its best
   moment as empty air. Five relics have had to file a beat by hand.

---

## 4. THE THINGS THAT WILL BITE

**0. FILM BEFORE YOU TUNE, IF THE ULTIMATE IS A PICTURE.** The most expensive
mistake v43 made — about **thirty thousand fights**. A clip is not the
deliverable that comes after the numbers; when the ultimate is watched rather
than counted, it is the only test that can see §4.1. Thirty seconds of clip on
placeholder numbers costs four minutes.

**1. A PICTURE FAULT IS A DEFECT CLASS AND THIS PROJECT HAS TWO.** v42 shipped
a **silent** ultimate through a 14-check probe, a 29-check probe, a full sweep,
a 13/13 verify and a rendered clip. v43's hold **stuck to the ball it froze for
2.067s** through a 30/30 relic probe, a 2760/2760 engine A/B and a 13/13
verify. Both were caught by Rick watching.

> A defect where "wrong" and "right" produce **identical numbers**.

**When a person catches something no tool could, the deliverable is a
MEASUREMENT of the thing they saw** — not a fix and an apology. That is why
sounds are now rendered in an `OfflineAudioContext` and measured, and why hold
contact frames are counted. Both are permanent checks.

**1b. THE BLOOM GETS BLAMED FOR WHAT THE ART DID.** Rick: "the bloom is
still really intense on some of the ults." It wasn't. Daybreak drew its corona
as a radial gradient from `#FFFFFF` at stop 0, with `lighter`, centred on a
relic body already at 0.892 luma — the ball was not lit, it was **erased**.
Measured on the caster's disc: 0.499 bare → 0.905 at the peak, 58% of the disc
past 0.98, and **only +0.041 of that was the bloom.** Roughly a tenth. Turning
the chain off left the ball a featureless white blob.

> When a bright thing looks wrong, measure the art and the post chain
> SEPARATELY before touching either. `tools/ult_bloom_probe.py` does it.

The fix was shape, not strength: the corona is now a ring with the hole cut in
the path, every gradient number unchanged. Same light, and the ball is an
object again. **A radial gradient with an inner radius still fills its inner
circle with `colorStop(0)`** — moving the inner radius out does nothing on its
own, the hole has to be subtracted with a backwards-wound arc.

**1c. AND SOMETIMES IT REALLY IS THE BLOOM — SO MEASURE, DO NOT PATTERN-MATCH.**
Daybreak and Benediction were art painted over a near-white body. The Harrowing
is not: Lastlight's ball stays legible throughout. Its `drawUltUnder` fills a
white radial disc at radius `86 + n * 26` — **398px at `scythes:12`** — and the
post chain turns that into a full-arena fog. Arena mean 0.3956 with **+0.0628
of it made by the bloom**, the largest contribution in the game.

Two things that cost a whole spread to learn, both now permanent:

> **THE FAULT IS NOT ALWAYS IN THE BLOCK NAMED FOR IT.** Three candidates were
> built on `drawUltOver`'s `lastlight && phase === "bloom"` branch — the ring
> and all twelve scythes. Suppressing **both** moves the arena by 1% of what
> the under-layer disc does. `19.5% → 19.5%`. Decompose by suppressing one
> contributor at a time; a single number over a whole set-piece cannot tell
> you which half to change.

> **ALPHA IS INVISIBLE TO THE BLOOM. REACH IS NOT.** Thinning the gradient's
> plateau moved the bloom's own share by 0.0001. The bloom reads the emissive
> layer and a white core is white at any alpha. To take light out of the
> chain, take away AREA.

And a metric is only right for the fault it was built for: the caster's-disc
measurement that found Daybreak ranked Lastlight #1 for the wrong reason and
could not see a full-frame wash at all. `tools/harrow_bloom_probe.py` is the
arena-wide one. **A count-driven ult must be swept across its count** — the
captured block had `n=2` against a cap of 12.

**2. A HELD OBJECT'S STORED STATE IS NOT ITS CURRENT STATE.** `f.pinV` holds
the velocity a frozen ball *resumes* on; `_ballPair` read it as the velocity
the ball *had*. When a thing is suspended and something is kept so it can
resume, **every other reader of that field is reading a lie until checked.**
There is no type-system answer. Grep the field, read every site.

**2b. THE RUNTIME IS AN INPUT. IT IS PINNED NOW — KEEP IT THAT WAY.** V8 does
not specify a last bit for `Math.pow`, the sim integrates gravity through it
every step, and Chromium 128 against 151 was **112 of 192 fights different**.
Seed 25064 — the v43 clip of record — is 44.52s on one and 46.41s on the other,
same winner, same hp. The pin is `requirements.txt` (`playwright==1.62.0`) and
`app/package.json` (`electron` exactly `44.0.0`); the two Chromiums differ in
version and agree to the last bit, which is the property that matters. Run
`tools/math_fingerprint.py` after touching either, and **never build a
side-by-side filmstrip from two different runtimes.** `docs/RUNTIME-DRIFT.md`.

**3. `|| default` on a number a sweep can set is a bug.** Use `=== undefined`.

**4. A BROKEN SOUND IS INVISIBLE TO EVERY TOOL HERE.** `SFX.play` returns on
its first line headless and wraps its body in try/catch. Render it in an
`OfflineAudioContext` and measure it.

**5. `_burst` DOES NOT LOOP ITS 0.6s NOISE BUFFER**, so any burst longer than
that plays silence for its tail. `_tone` ends on an exponential ramp over its
whole length, so **a HELD note does not exist in this toolkit** — anything that
must last is re-struck. Both are live bugs across 24 shipped voices.

**6. AN INSTRUMENT THAT FIRES WHERE THE MECHANIC DOES NOT MEASURES SOMETHING
ELSE.** The pin read −12% triggered on a clock and +42% triggered on its own
condition. Same code.

**7. A LONG A/B WINDOW MEASURES DIVERGENCE, NOT THE THING.** Two arms identical
up to an event are chaotic 2s after it. Short window, smooth quantity, and a
control in the table that must come back at a known value.

**8. IF YOU GENERALISE FROM A SUBSET, LOOK AT THE SUPERSET FIRST.** The ult
name cost three spreads and twelve rejected candidates because runic's own
three ultimates are abstract nouns and the other twenty-one are concrete.
Reading the whole roster was free.

**9. TUNED NUMBERS LIVE IN THE BUILDERS, NEVER IN THE HTML.** A previous
session wrote twelve converged damage values into `sc-r15.html` and lost all
twelve on the next rebuild. `tune.py --apply` refuses to write into anything
carrying a `GENERATED by` stamp — which is every file in `02-chain/`.

**10. DOWNSTREAM BUILDERS REPLACE SPANS.** Run `chain_audit.py` after every
carry, **with `--builder <yours>_build.py`** — it defaults to
`twinshade_build.py` and will happily audit the wrong inserts and pass.

**11. A BUILDER SHOULD SYNTAX-CHECK ITS OWN OUTPUT.** An unbalanced `*/`
surfaced only as a twenty-second Playwright timeout.

---

## 5. THE COMMANDS

**On Windows, the interpreter is `python` or `py` — never `python3`.** The
python.org installer creates `python.exe` and `py.exe` and no `python3.exe`, so
Windows hands `python3` to a Microsoft Store stub that reports Python is not
installed. Every doc in `06-docs/` says `python3` because those sessions ran in
a Linux container; they are records, not instructions. Substitute as you read.

```bash
cd tools
python3 math_fingerprint.py                                         # the runtime pair
python3 shell_identity.py                                           # app == headless
python3 post_identity.py                                            # the chain is invisible
python3 verify.py --game ../02-chain/sc-paradox-frame.html --n 40   # 13 checks
python3 engine_ab.py --a <prev> --b <this> --ids <ids> --n 10       # nothing moved
python3 chain_audit.py --relic <relic> --tip <tip> --builder <b>.py # inserts survive
python3 cell_survey.py --game ../02-chain/sc-paradox-frame.html     # what's open
python3 ult_bloom_probe.py                                          # which ults blow out
python3 ult_fx_capture.py                                           # real ultFx, per relic
python3 ult_live_probe.py                                           # ults that need a PLAYED match
python3 paradox_pick.py                                             # which fight to film
```

A clip (`--shorts` only if it is going to a platform):

```bash
python3 cinema_clip.py --game ../02-chain/sc-paradox-frame.html \
  --a paradox --b heartwood --seed 25064 --lead 18 --fps 60 --w 540 \
  --out ../07-shorts/v43/stasis-v-heartwood.mp4
```

**Expect `verdict panel held 2.40s of the ... tail` on every capture and treat
its absence as a defect.**

Voiceover needs two model files that are **not in the repo** — see
`tools/FETCH-KOKORO.md`. Voice of record is `bm_lewis`.

---

## 6. WHAT A SESSION COSTS

v43 ran **~102,000 simulated matches** — 43 minutes of pure simulation at ~40
matches/second in one headless V8 thread.

```
discovery     changed what got built                   ~6,100    6%
verification  proved it changed nothing else          ~17,600   17%
tuning        found one number                        ~24,700   24%
selection     which fight to film                      ~1,100    1%
VOID          re-runs invalidated by my own bugs      ~46,600   45%
```

**Six percent changed a decision** — and the surveys plus the pre-build probe,
under 5,000 fights between them, produced nearly all of it. The 45% is the
avoidable part. Budget accordingly.

Three cheap wins nobody has taken: bisections should **escalate their sample**;
the sweep grid does not need a precise bisection to normalise insensitive
telemetry; and **nothing in `tools/` is parallel** — one browser, one thread,
though every tool already takes its seeds as a list.

---

## 7. HOW A SESSION RUNS NOW

The zip is retired. This repo is the truth.

```bash
git pull                          # start here, always
# ... work ...
git add -A && git commit -m "..." # end here, always
git push
```

**Rules for this repo, not negotiable:**

- **Never commit an mp4, wav, or the Kokoro model.** `.gitignore` catches
  them; do not `git add -f` past it. The seed rebuilds the clip.
- **A commit that changes the build of record names its verification** in the
  message: which probes ran and at what count. A green claim with no run
  behind it is worse than a red one.
- **Version write-ups still go in `06-docs/vNN/`.** Git history is not a
  substitute for the reasoning — the docs say *why*, the diff says *what*.
- **Update this file when it goes stale.** Especially §0.

---

## 8. THE OPEN ITEMS, OLDEST FIRST

1. **`01-live` IS NINE RELICS BEHIND.** v27 od 1. The oldest open thing here.
2. **THE SHARED `cineFloor` IS STILL NOT BUILT.** v40 item 1, six relics deep.
   §3 of the v43 handoff is the first measurement it would be set against: a
   fatal cut is rare for **every** melee relic — 8% to 23% across six.
3. **THE FIGHT CARD IS STILL IN THE BUILD.** Rule 1, five sessions unmoved.
4. **TWO BEATLESS DEATHS.** Daybreak's spark burn and `_traceHit` both take hp
   through `hurt()` and file nothing; Dawnbringer is 22.1% blind. The general
   fix is one backstop — *if a fighter died this step and no beat was filed,
   file one* — chain-wide, therefore Rick's call.
5. **`tip_audit.py` DOES NOT CHECK ULT TIPS.** v40, v41, v42, v43.
6. **PARADOX'S SCRUNCH CARD WORDING** has not arrived. The placeholder is 67
   of the 72 characters `verify` allows.
7. **`_burst` / `_tone`** — §4.5, live, measured, chain-wide.
8. **`shot.life: 3.4` IS DEAD CONFIG ON ALL FIVE BOWS** (v40).
9. **`cell_survey`'s OCCUPANCY COLUMN HAS MISPRICED TWO CELLS.** Occupancy is
   a proxy twice removed for a status that is a RATE, and the tool does not
   say so in its own output.
10. **THE GREATSWORD DEADLOCK IS SIX THOUSANDTHS FROM A WIN** — 0.1537 against
    a 0.16 threshold, 100% deadlocks over 112 binds.
11. **A STUNNED GREATSWORD'S BLADE KEEPS TURNING.** `mode:"swing"` recomputes
    theta from the AIM every frame — the only type whose facing is not an
    integral of its own spin. Inert for damage, live for the picture.
12. **EVERY TYPE-LEVEL MEASUREMENT STILL WANTS A `--noult` PASS.** v38 od 5
    onward, five sessions.

Full detail: `NEXT-SESSION.md` and `06-docs/v43/`.

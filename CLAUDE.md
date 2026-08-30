# SUPER WEAPON BALL: THE SUNDERED CROWN

**This file replaces the handoff zip.** Read it first, every session. If
something in it is wrong, fix it in the same session — a stale CLAUDE.md is
how the handoff problem comes back.

Rick's project. A deterministic 2-relic arena fight, rendered to vertical
short-form video for TikTok and YouTube Shorts.

---

## 0. STATE OF THE PROJECT

```
02-chain/sc-paradox-ignition.html BUILD OF RECORD  25 relics · Stasis
                                                   + the post chain, bloom ON
                                                   + PARTICLE FIELDS on all 25
                                                   + the LONG-FIGHT pace
                                                   + the Stasis hold released
                                                     correctly
                                                   + ARCS SURVIVE HIT STOP
                                                   + A TRUE STUN TURNS THE
                                                     CRUCIBLE'S BLACK HOLE OFF
                                                   + THE IGNITION OPEN
02-chain/sc-paradox-crucible.html    the link before it
01-live/sundered-crown.html      OLD SNAPSHOT      16 relics — NOT A TARGET
01-live/sc-playable.html         OLD SNAPSHOT      16 relics — NOT A TARGET
```

**The build of record carries a WebGL post chain** (`src/render/post.js`,
inserted by `post_build.py`). Bloom ships; trails and grade are in the build
and default OFF. See `docs/BUILD-CHAIN.md`.

**And as of 2026-08-29 it carries PARTICLE FIELDS** (`src/render/fx.js`,
inserted by `fx_build.py`): every one of the twenty-five ultimates now emits a
deterministic field — six emitter modes, twenty-five specs, one
implementation. Approved off played clips four times: particles at all, the
vocabulary across four shapes, the density, and finally a real fight out of the
build itself.

**AND AS OF 2026-08-29 IT CARRIES THE LONG-FIGHT PACE** (`fx_build.py` ->
`pace_build.py`): `baseHP` 300 -> 400, the Second Seal 15s -> 21s with the hall
closing on it, the Third 35s -> 49s, `timeout` 80 -> 120, and Grudgebearer's
`dmg` 27.93 -> 23.50. Mean fight 37.3s -> **49.5s**, 0/12000 timeouts, 4.9
ultimates a fight instead of 3.7 — ult charge is pure wall time, so a longer
fight buys set-pieces for free.

> **IT SHIPS AT 12/13, AND THE THIRTEENTH IS KNOWN.** `verify`'s "every pairing
> mean duration in 18-70s" fails: six to eight of 300 pairings run over, worst
> Lightkeeper/Farwarden at **74.6s** (76.9s before the Crucible change),
> clustered on Lightkeeper, Axiom, Farwarden and Spellbreaker. It is a PAIRING
> ceiling, not the average — the overall mean is inside its band (48.8s) and
> every relic is inside the 30-70% winrate band (Heartwood 42.5 .. Farwarden
> 57.4, **spread 14.9pp**, against 16.4 at the pace change and 14.5 before any
> of this). Accepted rather than fixed because a short films ~45s of a fight, so a
> 74s average pairing still yields usable clips. **Do not read this as a green
> verify.** Clearing it means either backing the pace to baseHP 370 / seals
> 19-44 (45.4s mean, the floor of the ask) or tuning those four relics.

**A FIGHT NOW STARTS AS A SHOT** (`src/render/open.js`, inserted by
`ignition_build.py`). The first **2.35s** of every match: fighter A at 2.25x,
a hard cut at 0.85s to fighter B, a pull wide from 1.55s that lands just before
the first clank — and the two relics IGNITE, staggered onto the cut, each in
its own affinity palette, while every `shadowBlur` in the hall powers on from
0.30 through an overshoot to exactly 1.0. Then it hands the lens back and the
build is pixel-identical to the one it was built from (`render_ab` 20/20 at
3–31s). Prototyped as four variants in `tools/ignition_lab.py`; Rick watched
`05-reference/v46-ignition/ignition-open-both-solo.mp4` and said make it
happen. `06-docs/v46/`.

> **IT IS THE SAME OPENING, AND THAT IS MEASURED, NOT ASSERTED.** Played
> side by side the lab render and the build render differ by a mean 1.43/255 —
> **all of it the lab harness evaluating its driver one frame behind the sim.**
> With the clock removed as a variable (same page, same sim state, same
> rasteriser) the build's `SWBOpen` is byte-for-byte identical to the lab's
> driver at 18 of 19 instants, every flare and both seams included. The
> nineteenth is the final 10ms, where the module hands back at `z <= 1.02` and
> the lab ran one more frame at 1.0005.

> **THE OPENING IS SILENT, AND THAT IS RICK'S CALL TO MAKE.** The clip he
> approved had no ignition sound and none was invented here. A sound is one of
> the seven things that are his (Rule 2) — offer it as a spread.

> **AND IT ONLY REACHES A SHORT THAT STARTS AT ZERO.** `cinema_clip --lead`
> measures back from the killing blow, so an ordinary clip begins thirty
> seconds in and never sees it. `--full` starts at 0.0. Whether shorts now open
> at zero is an editorial decision and nobody has made it. The app shows the
> opening on every fight regardless.

**GRAVITY KEEPS ACTING THROUGH HIT STOP** (`hitstop_build.py`). `step()`
returned before `move()` while `hitStop` ran, so nobody got gravity for up to
0.13s — including a ball in free flight nowhere near the impact. It resumed
carrying the speed it went in with rather than the speed its arc had earned:
102 px/s of phantom lift, a summit its trajectory did not allow, and a fall
from that summit. Universal, every relic, and invisible to a position log —
which is why thirty probes and a 13/13 verify never saw it. Now velocity keeps
earning what the clock owes it while position stays held, so a freeze displaces
an arc in time instead of deforming it. Pins are skipped, for the reason below.

**A TRUE STUN TURNS THE CRUCIBLE'S BLACK HOLE OFF** (`forgehold_build.py`).
Rick: *"currently when its true stunned it black hole effect still happens. a
true stun should turn it off."* The forge tick opens with `f.stun = 0` — the
wheel cannot be stopped — and that line erased a TRUE stun as readily as a
hitstun, so Grudgebearer went on dragging its quarry across the floor while it
was hexed, rooted or held. Now the pull stops and **both clocks stop with it**,
the forge's and the set-piece's, so the cast is delayed and nothing is spent.
Measured with `tools/forgestun_probe.py` before it was built: 121 of 819 casts
eat a true stun, four fifths of the time against **Axiom, Spellbreaker,
Foregone and Paradox — and never against the other twenty relics.**

> **RICK PICKED THE MILDEST OF THREE, SO THIS IS A DELAY AND NOT A COUNTER.**
> Offered cancel-the-cast (mirroring `breakSpin` on Bloodmill's wind-up),
> pull-off-while-the-window-runs, and pull-off-with-the-window-PAUSED. He took
> the third. The Crucible still gets its full 4.0s of pull, still has to clear
> `minT` before the hammer can connect, and **still lands** — 40/41 strikes
> against Axiom after the change. `f.stun = 0` is untouched, so the wheel keeps
> turning and a held Crucible keeps swinging; his sentence named the black hole
> and nothing else. Stopping the wheel too is a second decision and his.

> **WHAT IT COSTS IS WALL TIME, AND THE NUMBER IS 15.4 SECONDS.** Hex re-stuns
> every 1.15s per stack for 0.20s, so at five stacks the hold is very nearly
> continuous and the longest lit Crucible measured went 5.0s → **15.4s**. The
> charge does not rebuild while the forge is lit, so against Axiom that is
> roughly one ultimate's worth of fight spent holding one open. Grudgebearer
> vs Axiom 80.0% → 66.5% at n=200; the other three moved under 3pp. Nothing
> caps it today — say so if it should.

`forgeHold` is a second field about being stunned, which v39 explicitly refused
(*"the two would drift"*). It is not a stun clock: the forge erases `f.stun` one
step later, so there is nothing left for anything to read. It is written only
through `breakSpin` — already the one hook every true stun calls, now carrying
the stun's duration — read only in the forge tick, and zeroed when the forge
lights. **A wrapper around `breakSpin` with a fixed arity now silently measures
the old build**; `forgestun_probe.py` did exactly that once and its comment says
so.

**A STASIS HOLD NO LONGER RELEASES A BALL UPWARD** (`pinrelease_build.py`,
`--mode clamp`). `pin` exists on no other relic, so this was Paradox-only and
Rick had said so three times before it was measured: a quarry caught RISING
hung dead still for 2.32s and then resumed climbing at the speed it was caught
with. Store-and-release works exactly as written — the stored vector is simply
stale, because gravity is continuous and an upward velocity stops being true
one step into a hold. `f.vy = Math.max(0, pinV[1])`: a ball caught falling is
untouched, a ball caught rising is released at rest.

> **THE BANKING RULE IS NOT WHAT WAS WRONG, AND IT STILL HOLDS.** `move` still
> ASSIGNS, so knockback banked during a hold is discarded — Rick's v43 call,
> "no banked knockback and no loss of momentum after the stun". It LOOKS like
> it banks if you sample the step the pin expires; `move` cannot run while
> `pin > 0`, so the restore lands one step later and is exact. That early sample
> produced a wrong "confirmed, it banks" during the investigation. Follow it
> one step further before believing it.

**THE APP DROPS TO ~38 fps THROUGH A LOUD ULTIMATE, AND THAT IS ACCEPTED.**
Measured on the real GPU at 453x805: fields off 7.33 ms, Slagburst's 1890
particles 26.13 ms — 157% of a 60 fps frame, for the 1.5s the field is alive.
Rick, 2026-08-29, told: *"thats fine, dont worry about the app fps."*

> **DO NOT "FIX" THIS.** It is not a defect and it is not an open item. The
> video is unaffected — it captures offline, where a slow frame costs
> wall-clock and nothing else — and the PICTURE is unaffected, because the
> field is aged off `ultFx.t`: a dropped frame in the app is fewer samples of
> the same set-piece, not a different one, and the mp4 is byte-identical
> either way. The app is a tool for making shorts (§0), so smoothness in it is
> not the deliverable. Lowering the density to buy app frames would spend the
> thing Rick actually chose on the thing he explicitly said not to worry about.

> **THE FIELD IS AGED OFF `ultFx.t`, WHICH IS SIM TIME, AND THAT IS
> LOAD-BEARING.** `stepTo` integrates to an ABSOLUTE time, so the hook is a
> no-op the second time the post chain draws a frame — and the app's rAF and
> the capture's fixed cadence produce the same picture. A field advanced by a
> per-frame delta would have both bugs, and the first one presented as
> juddering *physics* the last time this project hit it (`post_build.py`, the
> camera shake).

**The runtime is pinned and that pin is load-bearing**: electron 44.0.0 and
playwright 1.62.0, chosen on measured bit-equality rather than version
equality. `(build, relics, seed)` names a fight *on a given V8* — see
§4.2b and `docs/RUNTIME-DRIFT.md`. Anything re-derived from a seed from
2026-08-26 onward is on the pinned pair and will not match a number recorded
before it.

**THE DELIVERABLE IS THE VIDEO. THERE IS NO PLAYABLE BUILD TO SHIP.**

Rick, 2026-08-28: *"we are building an app to make shorts. not an app to ship
to other people."* This file used to open by calling `01-live` nine relics
behind and "the oldest open item in the project", which framed a playable
release as a goal it has never been. Every session that read §0 dutifully
raised it, and Rick had to say so more than once.

`01-live` is an old snapshot, untouched since v37. **It is not behind, because
there is nothing for it to be behind ON.** Do not raise it, do not plan to
carry relics into it, and do not treat the count as a gap. If a playable
release ever becomes a goal, that is Rick saying so — not this file implying
it.

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
| `01-live/` | an OLD SNAPSHOT, v37, kept for reference. Nothing ships from here — see §0. |
| `02-chain/` | how the build was made, in order. `sc-base.html` is the ROOT. |
| `04-experiments/` | unshipped variants **and controls**. Several are the control for a measurement, not a candidate. |
| `05-reference/` | images, filmstrips, the clickable fighter review. |
| `06-docs/` | the write-ups, one folder per version. `06-docs/v46/` is current. |
| `07-shorts/` | delivered videos. **mp4s are gitignored — the seed rebuilds them.** |
| `08-analytics/` | retention curves and cold-open reads off real posts. |
| `tools/` | every builder, probe and renderer. **Flat on purpose.** |
| `app/` | the Electron desktop app. Pinned electron 44.0.0 — see `docs/ARCHITECTURE.md`. Launch it by double-clicking `launch-app.cmd` in the repo root. |
| `src/` | shared render code that is NOT app-only. `render/post.js` is the post chain; `post_build.py` inserts it into the build so the app and the video run the same one. |
| `docs/` | how the app and the render work is being built. `BUILD-CHAIN.md` reproduces the tip; `RUNTIME-DRIFT.md` is why the runtime is pinned. |

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

**1d. THE BLOOM ADAPTS, SO A BRIGHT FRAME GETS *LESS* OF IT — AND A
"BRIGHTEST IN THE GAME" IS NOT AUTOMATICALLY A DEFECT.** Foregone's Retrace is
the largest light source measured: 565,816 emissive px, arena mean 0.2000,
2.72% clipped — all higher than Daybreak's. It needs no change, and the
measurement is why.

All of it is `_retraceField`. Suppressed, the relic drops to **2,254** emissive
px and +0.0000 lift: there is no second contributor to hunt. And that field is
the TELEGRAPH — an ultimate nothing can interrupt has to be legible before it
lands — so it is bright on purpose.

Then the trap. Cutting its wide soft-bloom pass, the obvious way to take area
out of the chain, makes the picture **worse**: lift +0.0050 → +0.0178 and
clipping 2.72% → 3.68%.

> `adapt: 50` normalises the bloom against the FRAME'S OWN MEAN. A pass that
> raises the mean therefore DAMPS the bloom. Removing it hands the chain a
> darker frame and it blooms the remaining hard edges harder.

Measured at `adapt: 0` for the proof — foregone +0.0050 → +0.0183, grudgebearer
−0.0026 → +0.0004, paradox unchanged at +0.0002 because a dim frame gives
adaptation nothing to work with. **That also explains the negative lifts**: on a
bright frame the chain can come out darker than no chain at all. It is not a
bug and nothing needs fixing; it just has to be known before anyone reads a
lift as damage.

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

Launching the app: double-click **`launch-app.cmd`** in the repo root, or run
it from a terminal. It is a launcher and NOT a packaged `.exe` on purpose — a
packaged build would bundle its own Electron and freeze a snapshot of the game
inside it, and both halves of that are wrong here: the runtime is pinned
(`docs/RUNTIME-DRIFT.md`) and the app must show the live build of record so it
cannot drift from what the video renders (`docs/ARCHITECTURE.md` §1).

```bash
cd tools
python math_fingerprint.py                                         # the runtime pair
python shell_identity.py                                           # app == headless
                                        # run `cd app && npm run identity` FIRST --
                                        # it diffs a json the app wrote, not a live app
python post_identity.py                                            # the chain is invisible
python verify.py --game ../02-chain/sc-paradox-ignition.html --n 40     # 12/13, see §0
python engine_ab.py --a <prev> --b <this> --ids <ids> --n 10       # nothing moved
python chain_audit.py --relic <relic> --tip <tip> --builder <b>.py # inserts survive
python cell_survey.py --game ../02-chain/sc-paradox-ignition.html      # what's open
python ult_bloom_probe.py                                          # which ults blow out
python ult_fx_capture.py                                           # real ultFx, per relic
python ult_live_probe.py                                           # ults that need a PLAYED match
python paradox_pick.py                                             # which fight to film
python ignition_probe.py                                           # the opening, in pixels
python ignition_lab.py --scan --a <a> --b <b> --n 40                # a seed whose first clank lands in the opening's window
```

A clip (`--shorts` only if it is going to a platform):

```bash
python cinema_clip.py --game ../02-chain/sc-paradox-ignition.html \
  --a paradox --b heartwood --seed 25064 --lead 18 --fps 60 --w 540 \
  --out ../07-shorts/v43/stasis-v-heartwood.mp4
```

**Expect `verdict panel held 2.40s of the ... tail` on every capture and treat
its absence as a defect.**

**`ffmpeg` IS NOT ON PATH IN A TERMINAL, AND THE FAILURE LOOKS LIKE A BROKEN
RENDER.** winget installs it without a shim. The capture succeeds, three or
ten minutes pass, and the encode dies with a bare `FileNotFoundError
[WinError 2]` naming no file — so the command above fails on a machine where
the app renders clips perfectly, because `app/main.js` resolves it and injects
PATH for its children while the tools never did. The frames survive; finish
with `--encode-only` after putting it on PATH:

```bash
export PATH="$PATH:$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.1-full_build/bin"
```

`tools/clip_spread.py` carries a `resolve_ffmpeg()` that mirrors the app's;
`cinema_clip.py` and `shorts_build.py` still call bare `ffmpeg`.

**Delivery-quality flags, all opt-in and all measured** —
`docs/DELIVERY-QUALITY-BRIEF.md`. `--blur-scale`, `--png`, `--preset`,
`--motion-blur N`, `--shutter S`. Rick watched clips off seed 25064 on
2026-08-28: he could not tell 540-as-shipped from a 1080/lossless/veryslow
render, so **the pristine path does not currently earn its 4x render time**,
and `--blur-scale` is invisible and parked. `--motion-blur 2` he could see and
called too strong — it is a double exposure rather than a smear, and the brief
says what a real one costs. Clip spreads: `tools/clip_spread.py`.

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

1. **THE SHARED `cineFloor` IS STILL NOT BUILT.** v40 item 1, six relics deep.
   §3 of the v43 handoff is the first measurement it would be set against: a
   fatal cut is rare for **every** melee relic — 8% to 23% across six.
2. **THE FIGHT CARD IS STILL IN THE BUILD.** Rule 1, five sessions unmoved.
3. **TWO BEATLESS DEATHS.** Daybreak's spark burn and `_traceHit` both take hp
   through `hurt()` and file nothing; Dawnbringer is 22.1% blind. The general
   fix is one backstop — *if a fighter died this step and no beat was filed,
   file one* — chain-wide, therefore Rick's call.
4. **`tip_audit.py` DOES NOT CHECK ULT TIPS.** v40, v41, v42, v43.
5. **PARADOX'S SCRUNCH CARD WORDING** has not arrived. The placeholder is 67
   of the 72 characters `verify` allows.
6. **`_burst` / `_tone`** — §4.5, live, measured, chain-wide.
7. **`shot.life: 3.4` IS DEAD CONFIG ON ALL FIVE BOWS** (v40).
8. **`cell_survey`'s OCCUPANCY COLUMN HAS MISPRICED TWO CELLS.** Occupancy is
   a proxy twice removed for a status that is a RATE, and the tool does not
   say so in its own output.
9. **THE GREATSWORD DEADLOCK IS SIX THOUSANDTHS FROM A WIN** — 0.1537 against
    a 0.16 threshold, 100% deadlocks over 112 binds.
10. **A STUNNED GREATSWORD'S BLADE KEEPS TURNING.** `mode:"swing"` recomputes
    theta from the AIM every frame — the only type whose facing is not an
    integral of its own spin. Inert for damage, live for the picture.
11. **EVERY TYPE-LEVEL MEASUREMENT STILL WANTS A `--noult` PASS.** v38 od 5
    onward, five sessions.
12. **THE IGNITION OPEN HAS NO SOUND, AND NO ROUTE INTO A SHORT.** Both are
    Rick's, both are named in §0, and neither is a defect: the sound was never
    part of what he approved, and `--lead` clips start after the opening by
    construction. Ask; do not decide either one from this file.

Full detail: `06-docs/v46/` for the tip, `NEXT-SESSION.md` and
`06-docs/v43/` for the relic before it.

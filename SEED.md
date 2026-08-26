# SEED — v43, 2026-08-21. THE TWENTY-FIFTH RELIC. A BALL THAT STOPS.

Read this, then `06-docs/v43/HANDOFF.md`, then `06-docs/v43/README.md`.

```
02-chain/sc-paradox-frame.html       <-- BUILD OF RECORD
  25 relics · runic x flail · STASIS FIELD
02-chain/sc-paradox.html                 the relic alone
02-chain/sc-marrowdraw-frame.html        v42's tip, this build's source

01-live/sundered-crown.html          LIVE — 16 relics
01-live/sc-playable.html             LIVE — 16 relics
  UNTOUCHED since v37. NINE relics behind the tip.
```

## THE THREE RULES, AND THEY ARE RICK'S

1. **THE FIGHT CARD IS DEAD.** Nothing ships with one. `cinema_clip --intro`
   and `--cold-open` REFUSE to run without `--legacy-card`. The card is still
   in the build and removing it is still an unstarted, chain-wide job — four
   sessions unmoved.
2. **RICK GIVES INPUT ON SEVEN THINGS**: the CELL, the ult mechanics, the ult
   name, the fighter name, the scrunch card wording, the ult animations, the
   ult sound. If he has not offered, ASK — with real options, the trade named,
   and the options PRICED first where a measurement can price them. v43 put
   four separate forks to him from measurement and he refuted two of them.
3. **A HIT-HEAVY ULT MUST DECLARE ITSELF TO THE DIRECTOR** — and v43 is the
   sharpest case yet because **its ultimate deals no damage at all.** A hold
   files a beat, fifth relic running. And the first measurement of how rare a
   fatal cut actually is for a MELEE relic: 8% to 23% across six of them,
   Paradox at 12%. That is the number a shared `cineFloor` would be set
   against, and it still does not exist.

## THE TWELVE THINGS THAT WILL BITE

0. **FILM BEFORE YOU TUNE, IF THE ULTIMATE IS A PICTURE.** This is the most
   expensive mistake v43 made and it cost about **thirty thousand fights.** The
   Stasis Field deals no damage; its whole effect is a thing you WATCH. So the
   clip is not the deliverable that comes after the numbers — it is the only
   test that can see the class of fault below. Rick found a physics bug nine
   seconds into the first clip that a 30/30 relic probe, a 2760/2760 engine A/B
   and a 13/13 verify had all passed, and finding it AFTER tuning cost a second
   verify, a second engine A/B, a whole 40-seed bisection, three pick runs, a
   render, and every document that quoted the old damage. **Thirty seconds of
   clip on placeholder numbers costs four minutes.**

1. **The downstream builders replace SPANS.** Run `chain_audit.py` after every
   carry, with `--builder <your>_build.py` — it defaults to `twinshade_build.py`
   and will happily audit the wrong inserts and pass. **And it could not see
   v43's inserts at all** until its regex learned about `r'''`; the message it
   printed was "no *_NEW inserts found", which reads like a pass in a hurry.
2. **`CONFIG.physics.dt` is 1/120.** Never hardcode 1/60.
3. **Photograph the TIP, not the relic build.**
4. **`|| default` on a number a sweep can set is a bug.** Use `=== undefined`.
5. **A BROKEN SOUND IS INVISIBLE TO EVERY TOOL HERE.** `SFX.play` returns on its
   first line headless and wraps its body in a try/catch. RENDER it in an
   OfflineAudioContext and measure it — `paradox_relic_probe [10]`.
6. **`_burst` DOES NOT LOOP ITS 0.6s NOISE BUFFER**, so any burst longer than
   that plays silence for its tail; and `_tone` ends on an exponential ramp over
   its whole length, so **a HELD note does not exist in this toolkit.** Anything
   that has to last is re-struck. Both are live bugs and both are chain-wide
   changes to twenty-four shipped voices — v43 wrote inside the envelope rather
   than fixing them.
7. **OFFER THE SPREAD FIRST.** v42 spread after four serial failures; v43 spread
   before asking anything and the sound landed in one round trip. `field_lab.py`
   and `cast_lab.py` both do it. **And the same lesson applies to NAMES** — two
   spreads of four were rejected outright because both were in the wrong
   register, which a spread of one could never have revealed.
8. **AN INSTRUMENT THAT FIRES WHERE THE MECHANIC DOES NOT MEASURES SOMETHING
   ELSE.** The pin read −12% when triggered on a clock and +42% when triggered
   on its own condition. Same code.
9. **A HELD OBJECT'S STORED STATE IS NOT ITS CURRENT STATE.** `f.pinV` keeps
   the velocity a frozen ball resumes on, and `_ballPair` read it as the
   velocity the ball HAD — so the caster stuck to the thing it had just frozen
   for a full two seconds. Nothing in the repo could see it; Rick found it in
   the clip. When a thing is suspended and something is kept so it can resume,
   every other reader of that field is reading a lie until it is checked.
10. **A PICTURE FAULT IS A DEFECT CLASS AND THERE ARE NOW TWO.** v42's ultimate
   shipped SILENT and v43's hold STUCK to the ball it had frozen — both through
   every green check in the repo, both caught by a person watching. They are the
   same thing: a defect where "wrong" and "right" produce identical numbers.
   **When a person catches something no tool could, the deliverable is a
   MEASUREMENT of the thing they saw**, not a fix and an apology. v42 renders
   its sounds in an OfflineAudioContext; v43 counts contact frames during a
   hold. Both are permanent checks now.
11. **A LONG A/B WINDOW MEASURES DIVERGENCE, NOT THE THING.** Two arms identical
   up to an event are chaotic 2 seconds after it. Keep the window short, use a
   smooth quantity rather than a count, and put a control in the table that must
   come back at a known value.

## WHAT A SESSION COSTS, SO THE NEXT ONE CAN BUDGET IT

v43 ran **~102,000 simulated matches**, about 43 minutes of pure simulation at
a measured ~40 matches/second in one headless V8 thread. Where it went:

```
discovery     changed what got built                   ~6,100    6%
verification  proved it changed nothing else          ~17,600   17%
tuning        found one number                        ~24,700   24%
selection     which fight to film                      ~1,100    1%
VOID          re-runs invalidated by two of my bugs   ~46,600   45%
```

**Six percent changed a decision**, and the surveys plus the pre-build probe —
under 5,000 fights between them — produced nearly all of it. Discovery is a
SEARCH and a few well-aimed fights kill a sentence; verification is a COVERAGE
ARGUMENT and the count IS the claim, so there is no cheap version of "all 2,760
are identical". **The 45% is the avoidable part and item 0 above is most of it.**

Three cheap wins nobody has taken: a bisection should ESCALATE its sample
(`bisect` spends 960 fights on step one where the interval is 12 wide and the
answer is obvious); the sweep grid does not need a precise bisection to
normalise telemetry that is insensitive to ±1 damage; and **nothing in
`tools/` is parallel** — one browser, one thread, though every tool already
takes its seeds as a list.

## THE COMMANDS

```
cd tools
python3 paradox_relic_probe.py                       # 31 checks, defaults to the relic
python3 runic_flail_probe.py                         # §1 priced, on the v42 tip
python3 flail_survey.py --game ../02-chain/sc-marrowdraw-frame.html
python3 chain_audit.py --relic ../02-chain/sc-paradox.html \
                       --tip   ../02-chain/sc-paradox-frame.html \
                       --builder paradox_build.py
python3 verify.py --game ../02-chain/sc-paradox-frame.html --n 40
python3 engine_ab.py --a ../02-chain/sc-marrowdraw.html \
                     --b ../02-chain/sc-paradox.html --ids <24 ids> --n 10
python3 paradox_sweep.py --phase 2                   # need x bleed, dmg bisected
python3 paradox_pick.py                              # which fight to film
python3 paradox_field.py                             # the field, four moments
python3 field_lab.py                                 # six cast sounds in one wav
python3 field_lab.py --hold                          # four hold sounds
python3 cell_survey.py --game ../02-chain/sc-paradox-frame.html
```

A clip (no `--shorts` unless it is going to a platform):

```
python3 cinema_clip.py --game ../02-chain/sc-paradox-frame.html \
  --a paradox --b heartwood --seed 25064 --lead 18 --fps 60 --w 540 \
  --out ../07-shorts/v43/stasis-v-heartwood.mp4
ffmpeg -i X.mp4 -filter_complex "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -movflags +faststart Y.mp4
```

**Expect `verdict panel held 2.40s of the ... tail` on every capture and treat
its absence as a defect.** And **use `paradox_pick.py`, not a hunch**: it runs
every candidate through `window.cinePlan` and rejects seeds whose plan carries
no FATAL cut. On this relic **42 fights cleared its own bar and SIX of them
carried a fatal cut** — which is not a bug in the relic, it is the rate: a
fatal cut is rare for every melee relic in the game, 8% to 23% measured across
six of them.

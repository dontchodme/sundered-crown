# BINDWEED / TENDRIL — BUILD BRIEF (v68). The verdant flail, the 35th relic.

**Cowork, 2026-09-26. DESIGNED. Build from this file and
`verdant-flail-design-v68.md`; do not design (CLAUDE.md §3 rule 0).** Every
number below is priced in the design doc; the one number the build owns is
the blade (stage 5), and the one it may move inside a declared range is the
turn rate. Claimed in `06-docs/CLAIMS.md`. **Rick has not yet read this cell
— it is the first designed without his §1 — so check `CLAIMS.md` for a veto
before stage 1.**

---

## 0. THE RELIC, IN ONE PARAGRAPH, AND THE RULINGS

> For a duration the whole chain becomes a living thorned vine. It turns
> toward the enemy and grows until it reaches them, and it draws back in when
> they come closer, so the head — still a flail head, still hitting like one —
> is always where the enemy is. Anywhere the vine touches them it bites: a
> small hit that leaves entangle, over and over while it stays on them. When
> the duration ends the vine withers, and the thorns it left take root: the
> enemy is held where it stands, ball and weapon, for a moment for every
> entangle stack it carries.

```
the cell            verdant x flail                  Cowork, from the 8-cell price (design §"Why")
the fighter         BINDWEED                          Cowork, from four
the ultimate        TENDRIL                           Cowork, from four
the card            "The chain becomes a vine that hunts the foe. Bites entangle, then root"   70 chars
the blade           dmg ~18 (stage 5 settles it)      Gravemourn's flail profile otherwise: reach 96, spin 2.2, mass 3.6, mode chain
the channel         onHit {entangle: 2}               the school's, as every verdant relic carries it
the window          8s, cast every 16s                the row's (Revenant 16/8)
the seek            facing turns toward the foe at 4 rad/s; the drive spin is 0 for the window   design §5
the growth          reachMul eased at 0.3/s toward (d − R) / (reach × mods.reach), both directions, clamped [1, 3.0]; back to 1 on close   design §4
the bite            foe's disc within R + 8 of the pivot→head segment: 2 damage (ward absorbs first) + 1 entangle, every 0.30s while touching   design §7
the root            on close, both alive: pin 0.30s × entangle stacks (ball AND weapon), Grasp's write   design §7
```

**Priced whole (design §5.1):** blade 19, turn 4, 660 fights an arm, Chromium
141: body **1.5%** → whole **54.4% / 55.8%** on two seed blocks. Seek+growth
42.6, +bites 48.8, +root 54.4 — additive. 3.2 casts a fight, 7 bites and 14
damage a cast, the foe at ~3.1 stacks on an average window frame, 0.9s of root
a cast, 11.6 head blows in windows against 5.3 outside.

## 1. WHAT IT IS IN THE ENGINE — the shape, not the code

- `f.ultVine` — `{ t0, end, cd }`. Null on every other relic and on this one
  outside its window; `engine_ab` over the other 34 proves it.
- **The seek** lives in `tickWeapon`'s chain branch: while `f.ultVine`,
  `f.theta` turns toward `atan2(foe.y − f.y, foe.x − f.x)` at `u.turn` rad/s
  (shortest way round) instead of advancing by spin, and `drive = 0`. The
  spring, the sag, the damping and the extension are UNTOUCHED — the head
  hangs off the haft's tip and sways, and that sway is the picture. A stun
  still zeroes the drive as it does today; whether a stunned vine keeps
  turning is the build's to decide and declare (the lab turned it).
- **The growth** writes `f.reachMul` once a frame in `tickVine`, eased at
  `u.growRate` toward the foe's rim in units of the type's reach, clamped to
  `[1, u.growCap]`, and eased back to 1 over the wither (Revenant's restore
  at the window's close). Site 2 of 7 in the chain tick recomputes `chainLen`
  from it every frame, so the drawn chain and the hit segment grow together —
  **there is no second line for the animation**. The builder asserts every
  `f.w.reach` read carries `reachMul` (the v53 refusal).
- **The bite test** is point-to-segment distance from the foe's centre to
  the segment `(f.pivX, f.pivY) → (f.headX, f.headY)`, against `R + u.vineW`.
  A bite is `hurt(foe, u.biteDmg, f)` — ward first, then hp — plus
  `foe.apply("entangle", 1, f)`, then `cd = u.biteCd`. **No knock, no
  hit stop, no stagger, no beat, no `resolveHit`** (design §7; Scour's tick
  rule). The head's own stub in `bladeSegments` is unchanged and its blow
  goes through `resolveHit` as ever.
- **The root**: when `t >= end` with both alive, `n = foe.stacks("entangle")`;
  if `n > 0`: `hold = u.rootPer × n`; `if (!(foe.pin > hold)) foe.pinV =
  [foe.vx, foe.vy]; foe.pin = max(foe.pin, hold); foe.pinMax = max(...)`.
  `tickStasis` turns the pin into the weapon lock; **do not set `pinFree`**.
  A window ended by either death roots nobody and restores `reachMul`.
- **The next cast waits** for the wither to finish (0.4s) — one vine on
  screen at a time.
- The card line goes in as `ult.tip` exactly.

## 2. STAGES AND GATES

Each stage is one link, one builder stage, one gate that can fail. The base
is the chain tip at the time of the build — `sc-leaf` (awaiting Rick's eye)
or `sc-trunk` (the build of record) per CLAUDE.md §0; **the builder names it
and does not guess**, and says whether it carries the Winnowing hit-stop
patch.

**Stage 0 — THE CONTROL.** `tools/vine_price.py --seek 2 --track 1
--grow-time 0.3 --grow-cap 3.0 --turn 4 --blade 19 --seeds 20 --arms A,D`
UNMODIFIED on the pinned 151 against the base. Arm A must read ~1.5% and arm
D ~55% (design §5.1). **Read every later gate against THIS run, never against
the design's decimals** (CLAUDE.md §4.2b; v64 §3aa moved a gate 7.8pp).

**Stage 1 — the relic, ultimate STUBBED.** Bindweed: Gravemourn's chain
profile at `dmg 19` (a placeholder — stage 5 owns it), `aff verdant`, `onHit
{entangle:2}`, `ult.charge 1e9`, name, blurb, card line, a verdant flail
silhouette (first cut: a bramble-knot head on a green-barked haft; the redraw
is a later claim). `app/main.js`'s GAME line does NOT move yet.
Gate: `engine_ab` identical on all 34 others; `verify` reads the new relic in
0–5% (the design's 1.5%); `shell_identity`; `tip_audit` sees the 70-char line
in pixels.

**Stage 2 — the seek and the growth.** The window, the turn, `drive = 0`,
`reachMul` toward the foe's rim, the restore. No bites, no root.
Gate: a probe over ≥96 fights reads **~12 head blows in windows against ~5.4
outside, `reachMul` peak ~2.3 mean, and the relic at ~43% at blade 19**
(design §5.1's seek+growth arm, read against a stage-0-style reproduction of
that arm: `--bite-dmg 0 --bite-per 0 --arms C`). `engine_ab` on the 34.
**FILM IT HERE** (CLAUDE.md §4.0): thirty seconds of the vine turning and
reaching on placeholder art, before anything else is built — the sway and
the grow-to-reach are the whole picture and a probe cannot see either.

**Stage 3 — the bites.** The segment test, the cooldown, the bite's damage
path, the entangle application with `src`, the tag count.
Gate: probe reads **~7 bites a cast, ~14 damage a cast, the foe at ~3.1
stacks on an average window frame, touch ~20% of window frames**; relic at
~49% at blade 19 against the reproduction of arm C. Bookkeeping asserted per
fight: stacks applied = bites. `engine_ab` on the 34. If bites went through
`resolveHit`, the gate writes the gap and the knock is stripped.

**Stage 4 — the root and the wither.** The pin write, its conditions, the
restore of `reachMul` over the wither, the next cast waiting.
Gate: **~0.9s of root a cast, ~80% of windows rooting**; no root on a corpse
or after the caster's death; no cast opens under a wither; relic at ~55% at
blade 19 against arm D's reproduction. **A CHECK THAT COUNTS FRAMES IN WHICH
AN EVENT IS POSSIBLE IS NOT COUNTING THE EVENT** — count transitions.

**Stage 5 — THE BLADE.** Wide direct measurement on the pinned runtime, both
sides, n ≥ 1000 a point, on two seed blocks, at 17 / 18 / 19 — **no
bisection** (v48, v56, v66). Expect 17.5–18.5. If the band does not land
inside 17–19.5, move `turn` inside 3–5 FIRST and say so; the design priced 4
vs snap at 12 points.
Gate: `verify` 30–70 on all 35; every relic in band; the type ladder printed
(greatswords ~79%, bows ~38% in the design — write the spread down as
Thornshear's was; it is open item 12/32 and not this build's to fix).

**Stage 6 — the picture, the voice and the carry.** Design §8.1 and §8.2 are
the spec: the greening cast, the leaf scale, the bite flash and tag, the
green rim tell, the wither, the floor-root picture on the pinned ball (and
`_drawField`'s hexagon skipped for it), the silhouette, the particle field
in BOTH copies with the sha re-stamped. Four voices rendered as a spread of
four each in an `OfflineAudioContext` and MEASURED against §8.2's registers;
pick on the numbers, send the clips. Director: the cast files an `ult` beat,
the root files a beat (a ball stopping dead is a moment), bites file nothing;
the fatal case is the head's blow and `resolveHit` files it. **Bites do NOT
set `hitStop`** (v67). Move `app/main.js`'s `GAME` line. `shell_identity`,
`render_ab` where the base is untouched, `chain_audit --builder
bindweed_build.py`, and one whole fight watched end to end.

## 3. WHAT THE DESIGN MEASURED THAT THE BUILD SHOULD NOT RE-BUY

- The §1 as first written (a live chain with no seek) is +1pp at any width,
  growth or cadence: the vine does not reach the foe (design §3).
- Blind growth to 2.5–3× is WORSE than none (the head overshoots); growth
  that stops at the foe's rim is +6 to +8 (design §4).
- Turn rate: snap 67 / 4 rad/s 55.5 / 2 rad/s 34.5 at blade 20 (design §5).
- Window 6s reads 41, 10s reads 65; charge 18 reads 42 — the whole is
  proportional to window share. Do not "fix" the band with either.
- Root 0 / 0.3 / 0.5 s a stack reads 51 / 54 / 58 at blade 20 — a knob, not
  the fighter.
- The blade curve is ~2.7 points a damage point and does not bend between 14
  and 24 (design §6).

## 4. WHAT IS OPEN, AND WHOSE

1. **Rick's veto of the cell and the reach** (design's open decision 1). Check
   `CLAIMS.md` before stage 1.
2. **The art and the sound** — specced by Cowork in §8; Rick overrules from
   the stage-6 clips if he wants to.
3. **The turn rate inside 3–5** — the build's, declared.
4. **The type spread** — Rick's, open item 12/32.
5. **`_drawField`'s held-ball hexagon** on a pin without `pinFree` — the root
   wants its own picture; if the block cannot be skipped cleanly, stop and
   say so (design open decision 6).
6. **`s.snap`, `maxLive`, `frame_probe`** — the standing chain-wide items are
   not this brief's.

---

*Tools: `tools/vine_price.py` (the live price, five arms, every knob). Runs
in `06-docs/v68/runs/`.*

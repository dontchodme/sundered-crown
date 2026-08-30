# v44 — a true stun turns the Crucible's black hole off

Rick, 2026-08-29:

> small change to grudgebearer. currently when its true stunned it black hole
> effect still happens. a true stun should turn it off.

`forgehold_build.py`, `sc-paradox-arc.html` → `sc-paradox-crucible.html`.

---

## 1. Why it was never wired

The forge tick opens with

```js
f.stun = 0;
```

argued out in v39 when the sweep was measured never arriving: *"an ultimate
made of rotation that a stun can hold still is a promise the screen breaks, so
while the forge is lit the stun burns off."* That is right about the wheel and
indiscriminate about everything else — it erases a TRUE stun exactly as
readily as a hitstun. So a hexed, rooted or held Grudgebearer went on dragging
its quarry across the floor with a full black hole drawn over it.

The distinction the engine already has is `breakSpin`, marked at the
application sites rather than kept in a timer. It had one reader: Bloodmill's
wind-up. Nothing had ever asked it a second question.

## 2. Priced before it was built

`tools/forgestun_probe.py` wraps `breakSpin` — the exact set of true stuns, no
second source of truth, no change to the sim — and counts. 576 fights, 819
Crucible casts, on the build of record:

```
foe            casts  stunned    rate   mean t   strike  fizzle
axiom             42       36  85.7%     1.27       40       2
spellbreaker      46       38  82.6%     1.28       44       2
foregone          30       24  80.0%     1.58       29       1
paradox           30       23  76.7%     2.01       24       6

overall  121/819 casts eat a true stun (14.77%)
288/481 stun events land after minT 1.05s
20 of the other 24 relics never true-stun a lit Crucible at all
```

The four are the game's four hex appliers, all runic. Thornwake, Heartwood and
Lastlight *can* reach the code path — the root and the Harrowing's burst are
true stuns — but their ultimates are one-shot events and 0 of 40 seeds each
put one inside a lit 4-second window.

So: four pairings, four fifths of the time, and nothing anywhere else. That is
what made it worth asking Rick a question rather than picking a reading.

## 3. The spread, and what he chose

| | what a true stun does | cost |
|---|---|---|
| A | **cancels the cast** — mirrors `breakSpin` on the wind-up | vs three relics the strike stops landing; those pairings move hard |
| B | **pull off, window still running** | counter scales with the stun: 0.20s for hex, 2.32s for a Stasis hold |
| C | **pull off, window PAUSED** | purely a delay, nothing lost |

> **"Pull off, clock pauses."**

So the Crucible still gets its full 4.0s of pull, still has to clear `minT`
before the hammer can connect, and still lands — 40 of 41 strikes against Axiom
after the change.

**The wheel was deliberately left alone.** `f.stun = 0` is untouched, so a held
Crucible keeps swinging and can still connect. Rick's sentence named the black
hole and nothing else, and the line stopping the wheel would have to cross is
separately argued. If the wheel should stop too that is a second decision.

## 4. The second field, and why v39's objection survives it

v39 refused a parallel `hardStun` clock: *"a second source of truth about being
stunned and the two would drift the first time somebody added a stun."*

`forgeHold` is not that. It is not a stun clock — it is the Crucible's own
record of what the pull owes. It cannot read `f.stun`, because the forge erases
`f.stun` one step later and there is nothing there to read. It is written only
through `breakSpin`, which is already the one hook every true stun calls, now
carrying the stun's duration as a third argument; read only inside the forge
tick; and zeroed when the forge lights. `windCap` passes no duration, because
running out of runway is not a stun.

**That third argument has a trap in it and it was sprung immediately.**
`forgestun_probe.py`'s wrapper was `function (f, why)` and forwarded two
arguments, so it silently dropped the duration and measured the OLD behaviour
on the NEW build — reporting numbers identical to the control, digit for digit,
which is what gave it away. It forwards `...rest` now and says why.

## 5. The picture

`dim` is a presentation-only 0..1 on the wind `ultFx`, eased over 0.10s rather
than snapped: hex re-stuns every 1.15s for 0.20s, so a hard cut would strobe
the whole set-piece three times inside one cast and read as dropped frames.

It folds into `r` in both wind branches — the one term every alpha in each of
them is already scaled by — so one multiply takes the floor pool, the glow, the
event horizon, the lensed rim, the streamers, the wheel of heat and the dust
down the pull, together, and nothing else in either function can see it.

The set-piece's own clock stops with the forge's. Without that, `ultFx.life`
(cap + 0.4) would run out during a long hold and the black hole would come back
from the pause invisible.

Measured by drawing **one frame twice**, `dim` forced to 1 and left at 0 —
same world state, same positions, same camera (the shake is a `Math.random` in
the draw path and is zeroed for the pair, v43's trap):

```
seed 2813689682, t=21.64s, forge.t=1.77, fx.t=3.72 (art fully up)

                          arena mean   blown%   near caster
black hole ON                 0.1110    0.19%        0.2813
HELD                          0.1005    0.08%        0.1863
the black hole going out     -0.0105   -0.10%       -0.0950
```

A third of the light out of the caster's neighbourhood and half the blown
pixels. Grudgebearer's ball goes from a washed-out white-orange sphere back to
a legible brown ball, and the HUD's CRUCIBLE chip correctly stays lit.

## 6. What it costs, and it is wall time

Hex re-stuns every 1.15s **per stack**, so at five stacks the hold is very
nearly continuous. The longest lit Crucible measured went **5.0s → 15.4s**. The
charge does not rebuild while the forge is lit, so against Axiom that is
roughly one ultimate's worth of fight spent holding one open.

```
                        winrate (n=200)        mean fight
grudgebearer vs         before    after     before   after
  axiom                  80.0%    66.5%      49.6s   52.5s
  spellbreaker           60.5%    60.0%      51.5s   53.2s
  foregone               45.5%    48.0%      39.6s   40.1s
  paradox                40.0%    43.0%      40.9s   41.7s
```

Nothing caps the hold today. Rick's option was "nothing is lost", and a ceiling
would mean something is — so it is his call, flagged rather than added.

## 7. Gates

```
engine_ab   grudgebearer + the 6 relics with no true stun, 40 seeds x 21
            pairings                          PASS  840/840 bit-identical
engine_ab   grudgebearer + all 7 true-stunners, 40 seeds x 28 pairings
            differs, and the differences are EXACTLY the four hex pairings:
              grudgebearer|spellbreaker  38/40      24 pairings bit-identical
              grudgebearer|axiom         36/40      non-grudgebearer moved:
              grudgebearer|paradox       35/40        NONE
              grudgebearer|foregone      34/40
verify      12000 matches            12/13, the known thirteenth (§0)
            mean 48.8s · 0/12000 timeouts · spread 14.9pp
            worst pairing Lightkeeper/Farwarden 74.6s (was 76.9s)
post_identity                        PASS  325,708 px identical, max delta 0
forgestun_probe on the new build     14.44% incidence, unchanged
cinema_clip seed 3102132398          verdict panel held 2.40s of the tail
```

Every band came out slightly better than the pace change left them: spread
16.4 → 14.9pp, worst pairing 76.9 → 74.6s, mean 49.5 → 48.8s.

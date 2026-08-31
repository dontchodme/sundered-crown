# v48 — VESPER / SENTINEL. The pink scythe, and §1 priced: two of its sentences turned out to be one decision, and the sentence Rick worried least about is the one that was inert.

**2026-08-31, Cowork.** Designed and priced here while Claude Code builds
Thornshear. `tools/beam_probe.py`, 14/14, runtime-only.

```
tools/scythe_survey.py     the type, and the ward swept        16/16
tools/row_price.py         the cell, by delivered effect
tools/beam_probe.py        §1 PRICED BEFORE A BUILDER OPENED   14/14
02-chain/sc-paradox-ignition.html   the tip these numbers were measured on
```

**READ THIS FIRST: every number in this document was measured on the
PRE-THORNSHEAR tip.** Vesper builds off Thornshear, so the roster it fights
will have twenty-six relics in it and not twenty-five. Nothing here is
load-bearing enough to be invalidated by one relic, but the probes are cheap
and the build brief's first instruction is to re-run them.

---

# 1. §1, IN RICK'S WORDS

> *"pink sycthes ult — when the ult fires the scythe charges up (with a loud
> glowing animation) and then fires a targeted beam (thick, at least half the
> thickness of an artifact) the beam has limited range and points at the tip.
> the beam slowly rotates to track the enemy ball. while it persists it does
> rapid ticks of damage that push enemies towards its tip where it does bonus
> damage. the beam uses the scythes banked shield to increase its duration."*

**"Pink" is the school naming itself.** `AFFINITIES.vigil.core` is `#F06BB8`.

---

# 2. THERE IS NO BEAM IN THIS GAME

`kind: "beam"` exists on Benediction (Aureole) and Bloodprice (Goreshard), and
**`fireUlt` has no `kind === "beam"` branch.** It is a set-piece label and a
particle spec; both those ultimates are instantaneous hits dressed as a shaft
of light. Nothing in this game persists, tracks, or pushes.

So every geometric sentence of §1 was priced by **overlaying** the proposed
beam on real trajectories rather than by building it: the fight is the shipped
simulation, the beam is a test applied frame by frame, and nothing is written
back. The proof that the overlay is truly non-invasive is in the tables — the
ward-banked column is identical across all eight arms, because all eight watch
the same fights.

Both hooks §1 needs already exist: **`breakSpin`** for the wind-up and
**`spendWard`** for the pool.

---

# 3. THE POOL AT THE CAST IS A MEDIAN OF ZERO

```
relic                       casts  MEDIAN   mean   empty   >= 45   at cap
Bulwarden (v41's control)     258     0.0   12.0     55%      7%       2%
a vigil scythe                286     0.0   12.3     57%      8%       1%
```

**57% of casts find an empty shell.** `tickCharge` is `f.charge += dt; if
(f.charge >= u.charge) fireUlt(...)` — **a cast is a metronome** — and
`scythe_survey` §4 measured the ward up 42% of the fight. The two are
uncorrelated by construction, so a duration read off the pool at the instant
of the cast is a duration of zero more often than not.

**The Bulwarden row is a control and it reproduces a published number.** v41:
*"the pool at the cast is a MEDIAN OF ZERO over 88 casts."* Here, median 0.0
over 258. An instrument that reproduces someone else's number before it
reports a new one is an instrument worth believing.

**And the project has already solved this once.** Aegis was changed to *"feed
the wall while it stands"* for exactly this measurement. Rick took the same
shape here.

> **RICK'S CALL: the beam DRINKS THE WARD CONTINUOUSLY while it runs**, rather
> than reading the pool at the cast.

Measured, the loop closes: **a four-second beam banks 8.1 points of ward while
it runs — about 2.0 a second** — against the 12.3 that would have been sitting
there at the cast. So the blade's own blows during the cast are what keep the
beam alive, and the longer it lasts the more it is fed.

---

# 4. "SLOWLY ROTATES TO TRACK" AND "RAPID TICKS WHILE IT PERSISTS" ARE ONE DECISION

```
arm                             on target  mean run  longest  breaks  near the tip
turn 0.8  range 300  tip            16.2%     0.24s    1.22s     3.0        30.5%
turn 1.6  range 300  tip            23.4%     0.28s    1.54s     3.5        36.2%
turn 3.2  range 300  tip            42.3%     0.43s    2.05s     4.2        45.7%
turn 6.0  range 300  tip            59.5%     0.62s    2.82s     4.2        48.4%
turn 1.6  range 180  tip            14.9%     0.23s    0.97s     2.8        45.8%
turn 1.6  range 520  tip            34.3%     0.39s    1.54s     3.8        20.6%
turn 1.6  range 300  TIP FROZEN     26.2%     0.29s    1.34s     3.9        44.2%
turn 1.6  range 300  CENTRE         28.3%     0.34s    2.08s     3.6        41.0%
turn 3.2  range 520  CENTRE         73.8%     1.14s    3.78s     3.5        18.4%
```

**At the rate §1 asks for, the beam holds the ball for 0.28 seconds at a time
and breaks 3.5 times in a four-second window.** That is a lighthouse sweeping
past, not a lance holding on — so "while it persists it does rapid ticks"
describes a thing that does not persist.

## 4.1 THE TIP MOUNTING IS FREE, WHICH IS THE ONE PIECE OF GOOD NEWS

The blade tip is 138 units from the caster's centre and orbits at 3.2 rad/s.
Firing from the caster's **centre** instead buys 4.9 points; **freezing the
weapon's spin** for the duration buys 2.8. Against a turn-rate range that moves
the same number by 43 points, the orbit is a rounding error.

**So §1 keeps "points at the tip" for nothing.** The sentence that costs is the
next one.

---

# 5. THE PUSH IS INERT, AND IT IS INERT FOR THE SAME REASON

```
push (u/s^2)   on target  mean run   position along the beam   near the tip
0                  23.4%     0.28s                     0.56          36.2%
150                24.7%     0.30s                     0.57          36.3%
400                27.2%     0.31s                     0.58          38.0%
900                27.4%     0.31s                     0.59          38.2%
```

**Six times the force moves the ball from 0.56 to 0.59 of the way down the
beam.** You cannot push a thing along a line for 0.3 seconds.

The push and the tracking rate are not two knobs. They are one: the push only
has somewhere to act if the beam holds, and at the rate §1 asks for it does
not.

---

# 6. RICK'S CALL: LEAN INTO THE LIGHTHOUSE

Offered three ways — fast tracking so the rest of §1 works as written; slow
tracking with the damage redesigned around sweeping; or a lock-on that catches
and holds. He took the second.

> **The beam stays slow. Damage becomes PER PASS rather than per tick, and the
> tip bonus fires when a pass catches the ball out at the far end.**

So the unit of the mechanic is the **pass**, and the whole design re-prices
against it:

```
arm                             passes  per second  mean pass  longest  passes reaching the tip
turn 0.0  range 300   STATIC       2.2        0.56      0.21s    0.79s                     40%
turn 0.4  range 300                2.7        0.67      0.21s    1.02s                     46%
turn 0.8  range 300                3.0        0.74      0.24s    1.22s                     49%
turn 1.6  range 300                3.5        0.88      0.28s    1.54s                     60%
turn 1.6  range 180                2.8        0.69      0.23s    0.97s                     73%
turn 1.6  range 420                3.8        0.94      0.35s    1.54s                     45%
turn 0.8  range 180                2.3        0.59      0.20s    0.96s                     62%
turn 1.6  range 300  thick 26      3.7        0.92      0.30s    1.56s                     62%
```

## 6.1 THE HALL SWEEPS THE BEAM AS MUCH AS THE BEAM SWEEPS THE HALL

**A beam that does not turn at all is still crossed 2.2 times in four
seconds.** Tracking at 1.6 takes that to 3.5 — real, and about 60% on top of
what the ball was going to do by itself.

That is worth having in the design's own words rather than buried: *"slowly
rotates to track"* is doing less than the sentence implies, and the honest
description of this ultimate is a slow line laid across a room that a
ballistic ball keeps blundering through. **It is also a much better thing to
build the art around**, because it is what a viewer will actually see.

## 6.2 "LIMITED RANGE" IS WHAT MAKES THE TIP BONUS REACHABLE

```
range 180  ->  73% of passes reach the tip zone   (2.8 passes)
range 300  ->  60%                                (3.5 passes)
range 420  ->  45%                                (3.8 passes)
```

**Range trades pass COUNT against tip RATE, cleanly, and that is the sweep's
main axis.** Rick wrote "limited range" as a constraint on the ultimate; it
turns out to be the thing that makes his own bonus fire.

**Thickness is the knob that buys contact where the turn rate must not.**
Half-width 17 -> 26 — a beam 52 wide against a 68-wide relic — takes the mean
pass from 0.28s to 0.30s and passes from 3.5 to 3.7. §1 asked for "at least
half the thickness of an artifact", which is 34; the sweep should start there
and look up.

---

# 7. THE NAMES, AND MY FIRST SPREAD MISSED THE REGISTER

**VESPER.** Rick's, from a second spread of four. The evening star and the
prayer said at nightfall — a vigil kept as the light goes. `AFFINITIES.vigil.core`
is `#F06BB8`, the pink of a sky just after sundown, so the name and the colour
are one fact.

**SENTINEL.** Rick's, from the first spread. The watcher that stands and
turns — and it names the relic's posture where Reprisal, Bulwark and Aegis all
name a thing done, which is a deliberate difference rather than a slip.

**THE FIRST FIGHTER SPREAD WAS REJECTED WHOLE, AND V43 §15 SAYS WHY.** All
four of Longwatch / Duskwarden / Beaconward / Watchfire were
[modifier][guardian role], because that is what Farwarden, Lightkeeper and
Bulwarden are. **I generalised from three when the roster is twenty-five** —
the identical error that cost v43 twelve rejected ult names. Sanctified has
Aureole and Censer; runic has Paradox, Axiom and Foregone. Single evocative
nouns were in register the whole time, and the second spread was four of those.

**Reading the whole roster was free and I did not do it. Second time this
project has paid for that.**

---

# 8. WHAT IS STILL RICK'S

Five of the seven are answered — the cell, the ult mechanics, the two forks,
and both names. **Two are open:** the scrunch card (72 characters, `verify.py`
enforces it) and the art and sound spreads, which should be rendered before he
is asked anything.

**And the art has an unusually clear brief for once**, because §6.1 says what
the thing actually looks like: a slow line laid across a dark hall that a ball
keeps blundering into, four times in four seconds, brightest at the far end.

---

# Open decisions

1. **THE WIND-UP IS UNPRICED.** §1's first sentence is a charge-up and this
   probe did not measure it. v44's number is the nearest thing — 14.77% of
   Crucible casts eat a true stun, all from the four hex appliers — and
   `breakSpin` is the same hook. **The scythe's own number wants measuring at
   build time**, because a wind-up that is broken is a cast that is lost and
   this ultimate has no fallback.
2. **THE TICK RATE IS UNPRICED.** `CONFIG.combat.hitCd` is 0.45s per segment
   and nothing in this game ticks damage off a volume except a status. "Rapid"
   has no precedent here and it is a legibility question as much as a balance
   one.
3. **A PASS IS A NEW UNIT AND NOTHING IN THE DIRECTOR KNOWS ABOUT IT.** Rule 3,
   sixth relic running: the legible moment of this ultimate is a pass that
   reaches the tip, and `cinePlan` will score it as empty air unless it files a
   beat.
4. **`STATUS.ward` IS STILL UNMOVED** and `scythe_survey` §4.3 measured up to
   +13.4 points sitting in `bank`. Chain-wide, still Rick's, and this relic
   will be tuned against whatever it is at the time.

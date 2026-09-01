# v61 — GLOAMWIRE AND CROSSWEAVE, BUILT. The design reproduces on a runtime and a roster it was never measured on — 50.8% against a predicted ~51% — and the only thing that went wrong four times was the instrument, three times in the same way: reading state after the step that destroys it.

**2026-09-01.** Built from `06-docs/v61/gloamwire-design-v61.md` and
`06-docs/v61/GLOAMWIRE-BUILD-BRIEF.md`, both Cowork's. `tools/gloamwire_build.py`
stages 1-3, `tools/gloamwire_relic_probe.py`, `tools/gloamwire_sweep.py`.

```
02-chain/sc-gloamwire.html    the 31st relic, ULT STUBBED at charge 1e9
02-chain/sc-volley.html       the fan and the magazine, NO strand
02-chain/sc-crossweave.html   the strand, the shove — and no art at all
04-experiments/_gloamwire-knock0.html   the control for the strand's inertness
```

**THIS DOCUMENT IS A BUILD RECORD AND NOT A DESIGN.** Every mechanic, every
number and every one of Rick's choices is in the design doc. CLAUDE.md section 3
now opens with a rule 0 saying why that separation exists, and this cell is the
reason.

---

# 0. WHY THERE ARE TWO v61 DESIGNS, AND WHAT IT COST

`06-docs/v61/CONFLICT-READ-FIRST-v61.md` is the whole of it. Two sessions
designed `umbral x bow` on the same day, could not see each other, and **Rick
answered a full set of design questions in both** — the second collision on
consecutive relics, after v60's Ravelbone against the red hammer.

Rick's ruling, and it is the rule now rather than a decision about one cell:

> *"you do not design ults ever. cowork and i handle that and you build them
> from the repo. if you cant find them you need to stop and say so."*

The losing document is `quiver-design-v61-SUPERSEDED.md`, renamed and not
deleted (v60's rule), because it holds measurements the winner does not: a
10,804-arrow bank ledger with zero unclassified, the wall at 83.4%, and the
finding that a bow's wall arrivals are **perimeter-proportional across all four
walls** where Cindercleave's scythe puts 3.9% on the roof.

**The failure was not the design, it was the search.** The second session read
v40, v57 and v60 — the places a design would be *cited* — and concluded from
silence that none existed. `gloamwire-design-v61.md` was already on disk. The
check that works is enumerating every design doc **by title**, because a design
doc is named after a relic whose name is exactly the thing you do not have:

```bash
find 06-docs -name "*.md" | sort | xargs -I{} sh -c 'printf "%-52s %s\n" {} "$(head -1 {})"'
```

`06-docs/CLAIMS.md` is the cross-session half, proposed by
`CONFLICT-READ-FIRST-v61.md` section 4 and now written.

---

# 1. THE THREE STAGES, AND WHAT EACH GATE PROVED

```
stage 1   sc-gloamwire.html    engine_ab 3480/3480 · verify 10/13 · net_lab 6/6
stage 2   sc-volley.html       engine_ab 3480/3480 · probe 4/4
stage 3   sc-crossweave.html   engine_ab 3480/3480 · probe 10/10 · knock-0 2790/2790
```

**THE BASE IS `sc-garrote.html` AND THE BRIEF SAYS `sc-breach.html`.** The brief
was written before Ravelbone landed; its own stage 0 says to chain from the
newest link and declare it. So every `engine_ab` runs over **30** other relics
rather than 29, and every win rate in the design was measured with one fewer
relic in the hall.

**AND IT IS THE THIRTY-FIRST RELIC.** The design doc says thirty-second,
counting design order with Bloodmirror at thirtieth; `CONFLICT-READ-FIRST-v61.md`
flagged the drift and asked for it to be settled once. It is settled on the
built count — CLAUDE.md section 0 calls Ravelbone the thirtieth, and Bloodmirror
is in no link.

## 1.1 Gate 1 is the one that ports the design, and it holds

The brief's instruction was to **stop** if this failed, because what would be
refuted is the cell's identity rather than a tuning number. `net_lab --stage 1`
on the pinned Chromium 151 at 31 relics against the design's Chromium 141 at 29:

```
                                   design      built     gate
curse pool, umbral bow               54.2       54.5      within 6
time to a third memory              13.1s      12.9s      within 2s
```

**Two runtimes, two rosters, and the school's pool table comes back in the same
order with the same numbers.**

> **BUT THE IDENTITY CLAIM IS MEASURED ON A BODY THIS RELIC DOES NOT SHIP
> WITH.** Design section 2 calls the umbral bow the third-deepest pool in the
> school — that is Ironhail's blade of **16.23**. At the shipped blade the same
> row reads **33.5**, second-weakest, below Twinshade, because the pool
> remembers the SIZE of the blow that made it and this blade is barely half.
> It is not a defect and the design accounts for it downstream: `dmgMul 1.4` is
> what buys it back, and the design's own section 7 figure for the stubbed pool
> (33.8) reproduces here at 33.5. **"Best pool-per-second body in the school"
> describes a relic with twice this blade, and that sentence should not travel
> without this one.**

## 1.2 Gate 2, and the cap that could have made every later number a lie

`CONFIG.shot.maxLive` is 64 and `spawnShot` **shifts the oldest off the front**
at the cap. A triple shot at twice the cadence is nine times an ordinary bow's
projectile load in principle.

```
evictions   0    over 15,990 arrows
```

Asserted, not assumed, and printed either way. A nonzero count would have meant
the cap was deleting shots the build thought it had bought.

## 1.3 Gate 3, and the four outcomes balance exactly

```
both                865   16.2%
arrow only          243    3.4%
lightning only     1005   18.9%
miss               3217   60.4%
                   -----
                   5330   against 5330 volleys
```

**Arrow-only is 3.4% and that is correct rather than low.** Above the crossover
at `strandW = shot.r = 24` a ball an arrow can touch is already inside the
segment, so what survives is entirely volleys that lost an arrow first. Gate 3
item 4 says not to tune it up; the probe asserts the reason and not the number.

---

# 2. THREE DEPARTURES FROM THE BRIEF, AND THE FIRST IS THE ONLY ONE THAT MATTERS

**1. `tickNet` RUNS IMMEDIATELY BEFORE `tickShots`, NOT BESIDE THE OTHER WINDOW
TICKERS — AND THE BRIEF ASKS FOR BOTH.** Its section 3a says to put the ticker
with `tickWinnow`, `tickGrasp`, `tickBreach` and `tickBallista`, and in the same
paragraph says the strand test must run before `tickShots` or *"hit by both"* is
unreachable. **In this build those are incompatible**: `tickShots` runs at line
7338 and every one of those window tickers runs after it.

The requirement wins over the address, because the requirement has a reason
attached and it is a silent one: `tickShots` splices dead arrows out of
`this.shots`, so a strand tested afterwards has lost its endpoints, the third of
Rick's three outcomes never fires, and **no probe in the repo would report
anything at all.**

**2. THE FAN LIVES IN `tickFire`, NOT IN `spawnShot`.** The brief puts it in
`spawnShot` guarded on `angle === undefined`, because an explicit angle is
another mechanic asking for exactly one shot — Quarrelstorm passes fourteen of
them. Putting the loop at the only call site that fires the ORDINARY stream gets
the same result and removes the hazard instead of guarding it: every other
caller of `spawnShot` reaches no new code at all.

**3. THE STRANDS BELONG TO THE VOLLEY, NOT THE WINDOW.** The magazine can empty
while its last volley is still crossing the room. Lightning that stopped
existing because a counter reached zero would be a bar that vanished in mid-air
with the arrows still flying, so `tickNet`'s strand loop deliberately does not
test `f.ultNet`.

---

# 3. THE INVARIANT THAT DID NOT FIT IN ONE PAGE

Gate 3 item 3 asks that **at `strandKnock 0` the win rate be identical to the
no-strand arm, to the digit** — a strand that records a classification and
shoves nothing cannot change a fight.

The first cut of that check compared knock 0 against the **shipped** arm and
failed, which is not an invariant at all: that difference is the shove's price.
The real control is a cross-build A/B, so it is one:

```
sc-volley.html  against  04-experiments/_gloamwire-knock0.html
all 31 ids, 2790 matches            2790/2790 identical field for field
```

And the mistake measured something worth keeping. **The shove costs 2.5pp**
(53.3% at knock 0 against 50.8% at 260), the same sign as design section 6.2's
monotone −9pp across 0 → 400. It is a cost bought for the look, and the design
says it buys back about a point of blade.

---

# 4. WHAT THE ULTIMATE DOES, MEASURED ON THE PIN

```
                              design (Cr141, 29)     built (pin, 31)
win rate                              ~51%                50.8%
shoves a fight                        22.3                 22.9
arrow-only                           1-6%                  3.4%
evictions                             0.0                    0
volleys a fight                       36.6                 44.4
```

**Volleys a fight is the one number that moved**, 36.6 to 44.4, and the window
runs 11.7s a fight across 2.06 casts against a magazine that should empty in
4.1s. Both have the same cause and it is not a defect: `tickFire` returns early
on `f.stun > 0`, so a locked bow does not spend its magazine, and the window
stretches to whatever the fight allows. The payload is invariant under a
magazine by construction — that is the whole reason Rick took a count over a
duration — so a longer window is more wall clock and not more arrows.

---

# 5. THE BLADE

`dmg 9.2` was the design's placeholder, measured on Chromium 141 at 29 relics.
Gate 3 item 6 says to sweep it on the pin, and `gloamwire_sweep.py` does it the
way CLAUDE.md says twice: **a curve first, then a wide direct measurement, and
never a bisection.**

## 5.1 The curve, to find the region and to ask whether it bends

240 fights a point, side A. Not the answer -- Gravemourn's curve reads 67.3% at
dmg 47.2 and **60.6% at 52.0**, and a bracket chosen inside a bend is chosen
wrong.

```
   dmg     win      dur   timeouts
  5.00    5.8%     48.2          0
  7.00   30.4%     46.8          0
  9.20   50.0%     43.6          0
 11.50   69.2%     39.8          0
 14.00   84.6%     36.6          0
 16.23   86.2%     34.0          0
```

**Monotone, no bend, and steep: about 8.6pp a damage point through the
crossing.** That steepness is the argument for paying for the wide pass -- half
a point of blade is four points of win rate.

It also shows open item 24 in one column: **mean duration falls 48.2s to 34.0s
across the range**, so anything tuned here off raw `dealt` reads backwards,
because a bigger blade shortens the fight and the weapon delivers less of it.

## 5.2 The wide direct measurement

Three blades x both sides x two seed blocks x 1020 fights a cell = **12,240
fights**.

```
    dmg   A-side   B-side   blockA   blockB   POOLED
   8.60    45.3%    44.7%    44.3%    45.7%    45.0%
   9.20    53.3%    51.2%    51.4%    53.1%    52.3%
   9.80    57.6%    58.6%    58.1%    58.1%    58.1%
```

```
side asymmetry        +0.6pp      (Cindercleave measured about -1.3pp)
worst block disagreement 1.8pp    (two n=702 readings once differed by 4.3)
monotone              yes
50% crossing          9.01
```

**`dmg` 9.2 -> 9.0.** And the honest statement of the precision is an interval,
not the decimal: the slope here is ~11pp a damage point and the SE at n=4080 is
about 1.1pp, so the answer is **8.9 to 9.1** and 9.0 is the middle of it.

> **THE DESIGN'S PLACEHOLDER WAS NOT REFUTED.** 9.2 reads 52.3% -- inside
> `verify`'s band, about 2 SE above the field, and predicted from a different
> runtime and a roster with one fewer relic in it. This is a correction of a
> fifth of a damage point, and it is worth applying only because the curve is
> steep enough that a fifth of a point is two points of win rate. **Both
> readings agree that the design got this right.**

## 5.3 And `verify` reads the tuned relic three and a half points lower

```
verify --n 40, 18,600 fights, 31 relics      12/13
Gloamwire                                    46.5%
roster spread     Heartwood 38.8 .. Slagheart 59.3   20.5pp
overall mean duration                        47.9s
```

**12/13, and the one failure is the KNOWN thirteenth check** — Lightkeeper /
Farwarden at 76.3s, which fails on every build in this repo and has since v48.
No Gloamwire pairing is over the band. *"Both sides can win every matchup"* now
passes, where at the stubbed blade fourteen pairings were 40/0.

**The roster spread NARROWED to 20.5pp** from the 20.8pp Ravelbone left.

But `verify` puts this relic at **46.5%** where the sweep's own interpolation
put dmg 9.0 at ~50%, and that gap should be stated rather than smoothed:

- `verify` runs an appended relic as **side B in all 30 of its pairings**, and
  the sweep measured the side asymmetry at only +0.6pp. It does not explain 3.5.
- It is 1200 fights, so its SE is about 1.4pp and the gap is ~2.5 of them.
- **And this instrument has disagreed with itself by more.** CLAUDE.md records
  two measurements of one arm 6.6 points apart at n=378 and 4.3 apart at n=702;
  Cindercleave's cheap pass read 47.6% where three wide blocks read 52.5%.

So the honest reading is that the blade is somewhere in **8.9 to 9.2** and both
instruments agree the relic is mid-band. It is not worth another 12,000 fights
to move a number whose own interval already contains both answers.

> **AND A SIM-TOUCHING CHANGE IN STAGE 4 RE-OPENS IT.** v54's Deadfall became
> one mine and v56's Grasp gained a pin, both during what was nominally an art
> round, and both moved the sheet. If Rick's art round changes anything the
> simulation reads, this measurement is void and `gloamwire_sweep.py` is four
> minutes for the curve and about six for the wide pass.

---

# 5a. THE STRAND'S ART, AND RICK'S ONE-LINE REJECTION OF THE STAGE-3 CLIP

Shown the stage-3 fight, Rick: *"theres no electricity connecting the arrow
tips. this isnt the ult"* — and he is right in the strongest sense. Every number
in section 1 was green and what was on screen was a bow firing three arrows.
The brief put the art in stage 4 and the mechanic in stage 3, and a clip taken
between those two shows a relic that does not exist.

`drawStrands` runs UNDER `drawShots`, so the arrows read on top of the thing
that connects them, and it uses `tickNet`'s pairing rule EXACTLY: adjacent in
the fan, both alive, a dead arrow breaks its links. If the two ever disagree a
viewer sees lightning that cannot shove, or a shove with no lightning.

**IT IS DRAWN TIP TO TIP AND TESTED CENTRE TO CENTRE**, and that is declared in
the code rather than hidden. The two differ by about `s.r` at each end — 24
units — against a strand that connects at `R + strandW` = 124. Breach's rule is
that a beam drawn WIDER than it tests is a lie; this is drawn SHORTER than it
tests, by a fifth of its own reach, which is the safe direction of that error.

**FOUR REGISTERS, BECAUSE RULE 2 ASKS FOR A SPREAD.** `strandArt` selects:
`bolt` crackles, `chain` is the same bolt with beads at its vertices,
`filament` is three continuous arcs under tension, and `bar` is a clean
two-stroke beam and the control for the other three. **A spent strand goes dim
rather than dark** — `strandSpent` is already the latch that says this bar has
had its one shove, so which bars are still live is countable for free, which is
Breach's five-chip idea arriving without being asked for.

**AND IT IS PRESENTATION-ONLY ON THE STRONGEST CONTROL THE PROJECT HAS**: an
`engine_ab` including Gloamwire itself, which no earlier stage could run because
every earlier stage changed the simulation. **2790/2790 identical across all 31
ids.**

Three house rules it would have broken if it had been careless, all named in the
code: no `this.rng()` (the flicker is `shellHash` on quantised sim time —
derived, not accumulated, so it does not strobe against the frame interpolator
and does not re-invalidate the blade); no `createRadialGradient` per segment per
frame; and no `shadowBlur`. Those last two are precisely what took
Cindercleave's capture to 0.19 frames a second.

---

# 5b. EXTRA PROJECTILE SPEED, AND IT IS A COST

Rick, after the art landed: *"lets also give the arrows extra projectile
speed."* Built as a RESCALE of the vector `spawnShot` already computed rather
than a fresh one — Marrowdraw's construction, so direction stays the type's
business and only magnitude is the window's.

900 fights an arm, side A, at the shipped blade:

```
   mul   px/s     win  parried  landed   wall  shoves  blows
  1.00    380   49.9%     8.6%    7.7%  83.8%    23.0   20.3
  1.35    513   42.2%     7.5%    6.9%  85.7%    22.1   19.9
  1.70    646   40.9%     6.7%    6.5%  86.8%    22.1   19.8
  2.10    798   38.9%     6.3%    6.2%  87.4%    22.4   19.4
```

**Monotone DOWN, and the mechanism is the wall.** The parry falls exactly as
predicted — a faster arrow crosses a spinning blade's swept area in fewer frames
— and it does not matter, because `wall` climbs 83.8% -> 87.4% at the same time.
An arrow that spends less time in the air gives the quarry fewer frames to
wander into it and reaches the stone sooner. **Landed falls 7.7% -> 6.9%.**

That is v40 open decision 2 arriving from a direction nobody expected: *anything
that moves the landed rate is worth roughly ten times anything that moves what
an arrow does when it lands* — and extra speed moves the landed rate DOWN.

**Rick took 1.35 with the table in front of him**, which is a picture bought
with points, like Cindercleave's shove at −2.3 and Garrote's window at −14.7.

> **AND THE TWO INSTRUMENTS DISAGREE ABOUT HOW MUCH IT COST.** The speed sweep
> says −7.7pp at dmg 9.0 (n=900 an arm); the re-run blade curve reads dmg 9.20
> at **49.6%** under `speedMul` 1.35 (n=240 a point) where the same blade read
> 50.0% at `speedMul` 1.0. If the cost were 7.7 points, 9.2 should read about
> 44%. Five points apart, and CLAUDE.md records two readings of one arm 6.6
> points apart above the n≈700 floor. **The wide pass adjudicates it without
> either**: the crossing was 9.01 at `speedMul` 1.0, so a real 7.7-point cost
> puts it near 9.7 and a negligible one leaves it near 9.2.

---

# 6. FIVE OF THIS SESSION'S FINDINGS WERE THE INSTRUMENT, AND THREE WERE THE SAME MISTAKE

Recorded because v60's open decision 5 is that a session's own error rate is the
argument for its checks, and because two of these reached a printed table.

**THE PATTERN: READING STATE AFTER THE STEP THAT DESTROYS IT.**

1. **"Zero arrows against 2.04 casts."** The probe read `s.net` inside a
   `spawnShot` wrapper. `tickFire` calls `spawnShot` and only *then* writes
   `net`, `volley` and `idx` on to the shot it pushed — which is the right shape
   for the build and means the wrapper sees a plain arrow every time.

2. **A post-step scan loses arrows that die on their birth step.** A bow fires
   from 88 units at a quarry that can be 146 away; those are exactly the arrows
   that mattered. Registered at birth in a `tickFire` wrapper instead.

3. **AND THE THIRD COST A CONTROL THAT COULD NOT PASS.** At a strand reach past
   the arena diagonal the miss rate must be zero, and it read **11.9%**. The
   first explanation offered was `killFlight` — the match stays open while a
   fatal ball flies, so the archer fires into a tail where the quarry is already
   dead. **That was measured and refuted: 0 such volleys.** The real cause is
   the same one twice over — `tickNet` latches a spent strand on an arrow and
   `tickShots` splices that arrow out in the SAME step, so a post-step scan
   cannot see a latch on any arrow that died on the frame its strand fired. Read
   inside `tickNet`, it is **0 of 4419**.

   Correcting it moved the real numbers toward the design rather than away:
   shoves a fight **20.1 → 22.9** against a predicted 22.3, arrow-only 4.6% →
   3.4%. The lost latches were lost measurements.

4. **AND A 2x DISAGREEMENT THAT WAS TWO STATISTICS OF ONE QUANTITY.** The probe
   printed a curse pool of 80.4 beside the design's 40.8. Design section 7's
   figure is a TIME AVERAGE sampled every 0.25s; the probe's was the value
   standing at the final step, nearer the design's own `peak` column of 99.2.
   Caught before it was written down.

**5. AND A FIFTH, WHICH IS A CHECK ASSERTING A BALANCE CLAIM IT COULD NOT
   SUPPORT.** `[4c]` asserted that the shove is a COST, on the design's measured
   sign of -9pp across knock 0 -> 400. At blade 9.2 it read **-2.5pp** and
   passed; at blade 9.0 it read **+9.2pp** and failed. **An 11.7-point swing out
   of a two-tenths change to the blade is not a sign flip in the mechanic** — it
   is n=120 an arm against CLAUDE.md's floor of n~700 for ranking anything on
   this roster. The check has been converted to a printed reading with its own
   under-powering stated, because the invariant half of that gate item *is*
   testable and does pass: the knock-0 A/B, 2790/2790.

> **The rule all five share is the one the design doc already wrote for
> itself:** *a control has to be able to come back wrong* — and the corollary
> this build adds is that **a control has to be able to come back RIGHT.** The
> reach control could not, for two different reasons in succession, and each
> time the failure looked like a finding about the mechanic.

---

# 7. TWO DOCUMENT ERRORS FOUND BY BUILDING

1. **THE ULT TIP BUDGET IS 72, NOT 40.** Both the brief (open decision 1) and
   the design (open decision 5) say the card copy does not fit and needs Rick.
   `verify.py` line 89 is `u.tip.length > 72`; the 40 is the STATUS tip figure —
   itself 48 in code with 40 in the comment above it, which CLAUDE.md section 0
   already records as folklore. **`"24 volleys of 3 strung arrows; the strand
   shoves"` is 48 characters and fits**, and it is in the build.

   **But characters are the wrong unit and `tip_audit` is the real gate.** The
   scrunch panel is 536px on one line at 25px and a 48-character tip can be
   583px. That measurement has not been run.

2. **`chain_audit.py`'s COMMAND LINE IN CLAUDE.md SECTION 5 READS AS A RELIC ID
   AND A TIP STRING.** Both arguments are BUILD PATHS — `--relic` is the link
   the inserts were made in and `--tip` the build of record. Read the other way
   it dies on `read_text` with a bare traceback naming a path that was never a
   path. Corrected in place.

---

# Open decisions

1. **STAGE 4 IS ENTIRELY RICK'S AND NONE OF IT IS INVENTED HERE.** The art, the
   animation, the sound and the director's beat — four of his seven things.
   **A stage-3 build shoves the quarry with nothing drawn and nothing audible**,
   so it is measurable and it is not watchable. Do not film it and conclude
   anything about legibility.

2. **THE SOUND IS THE HARD ONE AND THE DESIGN SAID SO FIRST.** Three arrows and
   two strands, 24 times in 4.1 seconds, is ~120 events in a four-second window.
   `_burst` does not loop its 0.6s noise buffer and `_tone` ends on an
   exponential ramp over its whole length, so **a held note does not exist in
   this toolkit** — anything that must last is re-struck. A per-arrow voice will
   be mud. Render it in an `OfflineAudioContext` and measure it; a broken sound
   is invisible to every other tool in this repo.

3. **THE STRAND'S WIDTH IS BALANCE-FREE AND THE ARTIST SHOULD BE TOLD SO.**
   Design section 4.2: arrow contacts sit at 7.0-7.5 a fight across a doubling
   of `strandW`. The bar can be drawn at whatever reads on a phone. **This is
   the rare case where the picture is free**, and it is the cheapest thing in
   the design to get right.

4. **THE BLOOM HAS NOT BEEN MEASURED AND CROSSWEAVE IS A FULL-FRAME CANDIDATE.**
   72 arrows and 48 strand segments inside four seconds, in violet, under a
   chain whose `adapt: 50` normalises against the frame's own mean. CLAUDE.md
   section 4.1b-1d: measure the art and the post chain SEPARATELY, and remember
   that alpha is invisible to the bloom while AREA is not.

5. **THE BEAT IS NOT FILED AND `cinePlan` HAS NO IDEA WHAT A STRAND IS.**
   CLAUDE.md section 3 rule 3, and five relics have already had to file one by
   hand. Crossweave's best moment is a volley that lands BOTH — an arrow number
   and a ball thrown sideways on the same frame — and the director will
   currently score four seconds of the loudest thing in the game as empty air.

6. **THE BLURB IS MINE AND SHOULD BE REPLACED.** *"Three shafts and the dark
   strung between them. What the arrows miss, the lightning still moves."*
   Offered rather than chosen, and written to read like a placeholder so it
   cannot quietly become permanent.

7. **`tip_audit` HAS NOT BEEN RUN ON THIS RELIC.** Open item 4 says it does not
   check ult tips at all, which is the other half of section 7.1 above.

8. **AND THE 2% FLOOR IS A PROPERTY OF THE RELIC, NOT A STAGE-1 ARTEFACT.**
   Gloamwire wins 3.2% of its fights with Crossweave stubbed — the sharpest
   ultimate-dependence on the roster, against a field median ultimate worth
   +20.4pp. Rick chose it knowingly (design section 8). A charge delay, a hex
   lock at the wrong moment or any future change to `cadMul` hits this relic
   harder than any other in the game, and design section 8 asks for that to be
   said on the card rather than discovered in six versions' time.

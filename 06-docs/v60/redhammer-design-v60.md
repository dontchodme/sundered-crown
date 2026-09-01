# v60 — THE RED HAMMER, PRICED BEFORE A BUILDER WAS OPENED. The direction Rick took was refuted by the first gate written to test it, and the repair he chose has a measured optimum that is NOT the number the game already uses for the same verb.

**2026-09-01.** `tools/wallslam_lab.py` against `02-chain/sc-breach.html` — the
build of record, 29 relics. Runtime only. **Nothing is written to any build,
and no builder has been opened.**

```
tools/wallslam_lab.py        NEW   7/7 (at the repaired arm)   6/7 as shipped
06-docs/v60/wallslam-lab.json      the events, machine-readable
06-docs/v60/cell-survey-at-breach.json
06-docs/v60/row-price-warhammer-pin0.json
05-reference/v60/warhammer-row-at-breach.png
```

---

# 0. THE CELL, AND IT IS RICK'S

Rick: *"red hammer is in the repo. lets build it."* — `bloodsworn x warhammer`,
the warhammer row leader, open since the grid had eleven relics in it.

`cell_survey` on the tip: 29 relics, 42 cells, **13 open**. Filling this one
puts bloodsworn on 5 of 6 types and the warhammer on 5 of 7 schools.

`row_price --type warhammer --pin 0`, shipped weights, 280 fights an arm, 3/3:

```
cell                     status       win     lift    >=2 stacks
bloodsworn x warhammer   hemorrhage  56.1%   +22.1%       65%
runic x warhammer        hex         44.3%   +10.4%       31%
verdant x warhammer      entangle    40.7%    +6.8%       60%
```

Both of `row_price`'s columns pick bloodsworn, which they do not always do.
Two things in that run are worth more than the ranking:

> **IT IS THE ONLY CHANNEL ON THE ROW THAT IS POSITIVE AGAINST RANGED.**
> +10.0%, against runic −6.0% and verdant −10.0%. Open items 12 and 32 are two
> relics losing four fights in five to bows; this is the first cell measured
> whose channel points the other way. Not a fix for them, and not evidence
> about them — but it is the opposite sign on the same axis.

> **AND HEMORRHAGE COSTS THIS CELL 50 BLADE DAMAGE A FIGHT** — 303 against a
> no-channel 353 — while lifting the win rate 22.1%. That is open item 24's
> confound visible on the cell rather than argued about: the bleed shortens the
> fight, so the blade delivers less of it. **Anything tuned off raw `dealt`
> here reads backwards.**

## 0.1 THE ART IS RICK'S TOO, AND IT IS A CHOSEN STATE NOW

`_whBarbed` is the most confusable art on its type — nearest sibling dwarven,
50.8% ink diff, **inkIoU 0.762, the closest pair of 21 on the warhammer** — and
it is built the way Rick rejected on `_whEaten` two builds ago: six hooks and a
return spur as separate closed paths stroked on top of `_whBase`.

Asked with that number in front of him, he took **"leave it, it's fine."** So
open item 34's first instance is closed as a decision. The relic being built
into this cell inherits that silhouette deliberately. **Do not re-raise it and
do not quote 50.8% as an open defect.** Dwarven's bolt bosses and `_scBuilt`
are untouched by this and are still unasked.

---

# 1. THE DIRECTION, AND WHAT IT RESTED ON

Four directions were priced and put to him, each grounded in one of the three
numbers that make a warhammer a warhammer and that **none of the four shipped
warhammer ultimates reads**: `knockMul 2.3` (the only value above 1.0 in the
roster, and the Crucible works *against* it by pulling in), `mass 5.0` (top of
the bind ladder), `spin 1.6` (3.9s a revolution, the slowest weapon there is).

He took **the knockback**: the hammer throws the quarry into a wall and the
wall pays, scaled by how hard it arrived.

**The engine already has the event.** `move()` clamps a ball at `n + R`,
reflects it, sets `bounced`, spawns fx and plays `"wall"`. So this ultimate is
CINDERCLEAVE's shape — *a test nobody is running, plus a rule about how often
it may fire* — and there is no new collision anywhere in it.

Three predictions were registered in `wallslam_lab.py`'s docstring **before the
lab was run**, with `pass_probe`'s rule attached: if a gate fails, THE DESIGN
CHANGES, NOT THE NUMBER.

---

# 2. TWO HELD, AND THE CONTACT RATE IS THE BEST THIS GAME HAS GONE IN WITH

288 fights, 9,119 blows, 6,510 arrivals attributed.

```
P1  THE SPREAD IS REAL     p10 440  median 850  p90 1300 px/s  ratio 2.96   (registered 1.6)
P3  NOT A FLOOR MECHANIC   floor 39.6%   W 28.8%   E 28.2%   roof 3.4%
```

```
                arrivals   blows   contact   median latency
warhammer           2196    2414    91.0%        0.41s
everything else     4314    6705    64.3%        0.29s
```

**Nine blows in ten put the quarry into a wall inside 1.5s.** BREACH shipped on
7.76 jet hits a fight against the blade's own 7.47; this is a second contact
rate of 0.91 per blow before anything has been built.

> **AND THE ROOF TAKES 3.4%.** Open item 37 measured gravity nearly erasing the
> north wall for CINDERCLEAVE's tears at 3.9%. Same hall, completely different
> object, same answer. **It is a property of the arena and not of that relic**,
> and the next design that distributes anything over the four walls should
> expect it rather than re-measure it.

---

# 3. P2 IS REFUTED. THE HAMMER'S KNOCKBACK DOES NOT REACH THE WALL

```
knockMul 1     n=6705   pre 664  ->  departure 645   delta  -20   |dv| 165.0
knockMul 2.3   n=2291   pre 694  ->  departure 636   delta  -76   |dv| 379.5

arrival  warhammer 850 px/s   against everything else 833   +2.0%   (registered 25%)
```

The impulse is real and exactly 2.3x. **`|dv|` comes back at 165.0 and 379.5,
to the decimal** — `CONFIG.combat.knock x knockMul`. That is gate `[2b]`, and it
exists for one reason:

> **SPEED IS THE WRONG INSTRUMENT FOR AN IMPULSE, AND A REFUTED PREDICTION IS
> WORTH NOTHING UNTIL THE INSTRUMENT IS PROVEN.** The first reading of this was
> "the warhammer's departure is 636 against 645, so `knockMul` does nothing" —
> which is false. The knock points AWAY from the attacker and the victim was
> moving TOWARD it, because that is why they touched. So a bigger impulse
> **reverses** a ball rather than speeding it up, and the median speed change is
> **−76 at knockMul 2.3 against −20 at 1.0**: the hammer's blow leaves the
> quarry momentarily *slower*, and more so than a light weapon does. `|dv|` has
> no such problem. Without `[2b]` this document would have reported a real
> refutation for an entirely wrong reason.

What kills it is `move()`, and it is two separate mechanisms:

- **The reversal above.** Most of the impulse is spent cancelling the incoming
  velocity rather than adding to it.
- **Speed is governed, not conserved.** `move()` clamps to `[250, 1300]` every
  step and relaxes toward an energy-derived target at `relax 0.62`. Whatever
  survives the reversal is pulled back toward the same target every ball in the
  hall is pulled toward.

It washes out on a clock, and the clock is shorter than the flight — median
latency to a wall is **0.41s**:

```
0.00-0.15s   +12.3%      0.35-0.70s    +8.1%
0.15-0.35s   +12.1%      0.70-1.50s   -28.9%
```

**So the spread P1 found is the room's spread, not the hammer's.** Scale a
payload on raw arrival speed and a viewer cannot tell a hammer blow from
gravity.

---

# 4. THE REPAIR IS RICK'S, AND `launch` IS A PERMISSION AND NOT A PUSH

Offered four repairs, he took **`launch`** — the engine's existing licence to
exceed the speed ceiling, which Grudgebearer's forge strike already uses.

The thing that decides the build is in the engine's own comment: *"`launch`
raises the vmax clamp and the relax term spends the next second and a half
paying it back."* **It raises a ceiling and adds no velocity.** The base knock
departs at ~640 px/s against a ceiling of 1300, so `launch` on its own moves
nothing at all. The Crucible pairs it with a separate impulse of `launch: 2400`,
and the red hammer must do the same. The size of that impulse is the knob, and
nobody had priced it.

Swept by injection — runtime only, warhammer blows get an extra impulse along
the engine's own knock bearing plus `launch` 1.2s:

```
kick    arrival wh   other    P2 gain   <0.15s    <0.35s   floor%  contact%  latency  swing gap
0 ship      850       833      +2.0%    +12.3%    +12.1%   39.6%    91.0%    0.41s     3.54s
250         882       842      +4.7%    +15.3%    +11.9%   38.8%    92.0%    0.37s     3.57s
500         937       848     +10.5%    +25.5%    +25.9%   35.0%    91.6%    0.33s     3.77s
800        1143       842     +35.7%    +56.8%    +48.5%   34.0%    94.6%    0.29s     3.78s
1200       1427       854     +67.1%    +79.1%    +74.0%   30.1%    94.1%    0.26s     3.56s
1800       1955       877    +122.9%   +133.3%   +123.9%   28.5%    94.1%    0.22s     3.78s
2400       2445       883    +176.9%   +184.3%   +164.1%   26.3%    94.6%    0.20s     3.43s
```

**P2 clears at kick 800.** Below ~500 the permission alone changes nothing,
which is the "not a push" sentence showing up as a number.

## 4.1 THE STRONGEST ARM IS THE WORST ONE, AND ITS VALUE IS THE CRUCIBLE'S

```
kick 0      ratio 2.96   p90 1300   <- clipped at speedMax 1300
kick 800    ratio 3.65   p90 1981      headroom
kick 1200   ratio 3.20   p90 2350      headroom
kick 2400   ratio 1.70   p90 2787   <- clipped at vmax 2795
```

`vmax` under `launch` is `speedMax x 2.15 = 2795`. At kick 2400 the arrivals
pile against it and **P1's spread collapses from 3.65 to 1.70** — barely over
the registered 1.6. The arm that reads loudest has almost no range left to
scale on.

> **THE SHIPPED BUILD WAS ALREADY CLIPPING AND NOBODY KNEW.** p90 at kick 0 is
> **exactly 1300**, which is `speedMax`. P1 passed at 2.96 while its top decile
> sat on a wall it could not cross.
>
> **AND COPYING THE GAME'S OWN CONSTANT WOULD HAVE REPRODUCED THE DEFECT ONE
> CEILING HIGHER.** `launch: 2400` is the Crucible's number for the same verb on
> the same weapon type, and it is the single worst value in the sweep for this
> mechanic. The reason the two differ is that the Crucible pays ONCE, at the end
> of a charge, where this window pays on every blow it lands — a value chosen
> for a one-shot set-piece is not a value for a rate.

**The measured recommendation is kick 800, launch 1.2s**: clears P2 at +35.7%,
the widest spread of any arm at 3.65, no clipping, floor share down to 34.0%,
contact up to 94.6%. Rick's to accept — this is a picture decision as much as a
number one, and 1200 is the same shape louder.

## 4.2 AND THE THROW IS VERY NEARLY FREE, WHICH IS THE TYPE AND NOT THE TUNE

The gap to the hammer's own next landed blow does not trend across the sweep —
3.54, 3.57, 3.77, 3.78, 3.56, 3.78, 3.43. **v51 §4.3's "knockback eating its own
window" does not bite here**, and a two-point read of it (3.54 -> 3.78) was
reported inside this session as if it did, off noise.

The reason is `spin 1.6`. At 3.9 seconds a revolution the quarry is back long
before the weapon is ready either way, so throwing it harder costs almost
nothing. **That is a property of this type and it would not survive being
carried to another one** — the same mechanic on a twinblade at `spin 5.7` would
pay for every pixel.

---

# 5. WHAT IS NOT DECIDED

Nothing has been built. §1 is a direction and a repair, not yet sentences. What
the builder still needs from Rick, and rule 2 says all of it is his:

1. **THE ULT NAME** and **THE FIGHTER NAME.**
2. **THE SCRUNCH CARD WORDING** — and `tip_audit` measures it in PIXELS, not
   characters. The panel is 536px on one line at 25px; `verify`'s comment says
   40 characters and the line under it enforces 48. Measure it there.
3. **THE KICK**, 800 or louder — §4.1.
4. **WHAT THE WALL ACTUALLY PAYS.** Damage, hemorrhage, or both, and whether
   the window is a count (BREACH's five) or a clock.
5. **THE ART AND THE SOUND**, which are first cuts of nothing yet.

# Open decisions

1. **THE KICK IS 800 ON THE MEASUREMENT AND THE MEASUREMENT IS ABOUT SPREAD,
   NOT ABOUT FEEL.** 800 maximises the range the payload can scale on; 1200
   reads roughly twice as hard and still keeps 3.20. Nobody has watched either.
   §4.0 — film before you tune, if the ultimate is a picture.

2. **THE WINDOW PAYS ON EVERY BLOW IN THE LAB AND NO REAL WINDOW WOULD.** The
   injection kicks every warhammer blow in the fight, which is the right stress
   test for the physics and the wrong shape for the relic. Every number in §4
   is an upper bound on contact and a fair reading of arrival speed.

3. **THE FLOOR IS STILL A THIRD OF IT.** 34.0% at kick 800. If the art wants a
   wall crack, a third of them are underfoot — and `wallCrack` already exists in
   the engine for the killing-blow flight, with a `nx`/`ny` that knows which
   plane it hit. It is the obvious thing to reuse and nobody has looked at it.

4. **`launch` HAS THREE WRITERS ALREADY** — the forge at 1.8s, another at 1.8s,
   and a shard burst at 1.4s on `n >= 3`. A fourth writer that fires on every
   blow of a window is a different kind of user from three that fire on
   set-pieces. No interaction was found (`killFlight` is armed only by the forge
   and the shards, and `move()` clears it on the first bounce), but nobody has
   asked what two overlapping `launch` grants should mean.

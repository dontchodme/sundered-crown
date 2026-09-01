# v59 — CINDERCLEAVE AND BREACH: the twenty-ninth relic, and the first ultimate in this game that gives the HALL a weapon. The design's one falsifiable prediction was published before the build existed and it reproduces; the registered prediction that failed was in the check rather than in the relic.

**2026-08-31, Claude Code.** Built to `06-docs/v57/cindercleave-build-brief-v57.md`
off the v58 tip. Four stages, three of them shipped as their own links, and
every gate below was run on the file it names.

```
02-chain/sc-cindercleave.html   STAGE 1   the 29th relic, ultimate STUBBED at charge 1e9
02-chain/sc-thepass.html        STAGE 2   THE PASS AND THE TEAR — holes open, sized, drawn,
                                            and they do not fire
02-chain/sc-breach.html         STAGE 3   THE JETS — the front, the taper, the Sunder, and
                                            the count of five
```

```
pass_probe              11/11    280 fights, 6,649 passes. THE STAGE GATE, and it is green
breach_relic_probe      25/25    at the SHIPPED blade — 168 fights, a constructed pair,
                                   four voices, and the render path CALLED
engine_ab           3024/3024    identical on the 28 others, every field, every seed,
                                   on the final file
chain_audit             19/19    every insert survives — after the tool was fixed
post_identity            PASS    325,708 px identical, max delta 0
verify --n 40           12/13    29 relics, 16,240 fights, Cindercleave 47.9%, roster
                                   spread 19.0pp. The thirteenth is the KNOWN
                                   duration-band failure — Farwarden/Axiom 75.1s, the same
                                   pairing at the same time as on the previous tip, and no
                                   Cindercleave pairing is in it. Do not credit this build
                                   with it either way
cindercleave_sweep         —     the floor 18.8%, a monotonic curve, and the blade
                                   settled at 19.75 by a WIDE DIRECT measurement
```

**THE BLADE IS 19.75** and it is a measured row rather than a fitted number.
The app's `GAME` pointer moves with the build of record — v48's carry that
nothing in `tools/` can check.

---

# 0. TWO BOOKKEEPING DEPARTURES FROM THE BRIEF, BOTH DECLARED

**IT IS THE TWENTY-NINTH RELIC AND THE BRIEF SAYS THIRTIETH.** `WEAPONS` holds
28 on `sc-gnawed.html`. Counted, Cindercleave is 29, and every `engine_ab` run
below is over 28 others rather than 29. Nothing in the design moves.

**AND IT IS BUILT OFF `sc-gnawed.html`, NOT `sc-grasp.html`.** The brief was
written before v58, which redrew the umbral warhammer on top of Grasp and is
the build of record; `sc-grasp.html` is one link behind it. `_whGnawed` is
render-only (`engine_ab` 3024/3024), so nothing this relic was priced against
moved. The builder REFUSES to write against a source with no `_whGnawed` in
it, so the chain cannot silently be re-rooted one link back.

---

# 1. THE STAGE GATE IS GREEN, AND THAT IS THE MOST IMPORTANT LINE IN THIS FILE

`06-docs/v57/cindercleave-design-v57.md` §3.2 published a distribution measured
in a LAB, before any of this existed: how deep a scythe's blade actually goes
into a wall, pass by pass. Rick's size mechanic — *"a graze to the wall makes a
small one but a full slash makes a larger one"* — is built entirely on that
spread being real. If it is not, `k` is a knob with no range on it and the
count, the size and the blade are all being tuned against a lab that does not
describe the game.

`pass_probe.py`, 280 fights, 6,649 passes:

```
             0.0-0.1  ########                        8.2%
             0.1-0.2  ########                        7.7%
             0.2-0.3  ########                        7.5%
             0.3-0.4  ########                        7.6%
             0.4-0.5  ########                        7.5%
             0.5-0.6  ########                        7.7%
             0.6-0.7  ########                        7.8%
             0.7-0.8  ########                        7.9%
             0.8-0.9  #########                       9.0%
             0.9-1.0  ############################## 29.2%

                        BUILT              LAB (design §3.2)
      median            0.646              0.63
      quartiles         0.32 / 0.65 / 0.94 0.30 / 0.63 / 0.92
      sd                0.327              0.32
      past 0.9          29.2%              27.4%
      under 0.30        23.4%              —
```

**Every one of them inside the band the brief registered.** Two instruments,
written months and a repository apart, describing the same physics.

> **AND THE OTHER HALF OF THE STAGE'S CLAIM IS EXACT.** *One pass is one vent*
> — 6,686 passes opened, 6,649 vents torn, **37 still in the blade when the
> fight ended, and 0 unaccounted for.** The orphans are the engine's own rule
> rather than a defect: `step()` returns from its `over` branch before
> `tickBreach` is reached, so a cut in progress on the frame the match ends is
> never finished, and there is nothing left to tear into. The first cut of
> that check asserted `opens == tears` and failed on 37 of 6,686 — which is
> `gravemourn_relic_probe`'s lesson for the fourth time: **a probe that
> encodes its own model of a rule fails on every legitimate case the engine
> handles differently.**

> **THE WALL DISTRIBUTION IS NOT EVEN, AND NOBODY HAS MEASURED THAT BEFORE.**
> E 2153, W 2165, S 2071 — and **N 260.** The ceiling takes 3.9% of the tears
> where the other three take 32% each, because gravity is real and a ball
> spends very little of a fight against the roof. That has a consequence for
> Rick's aim rule: (0, 1) — straight DOWN into the room — is only ever
> available from the north wall, so it is drawn **81 times in 6,649**, 1.2%.
> *"All eight compass bearings present in the game"* is true and one of them
> is very nearly absent. Open decision 4.

---

# 2. WHAT THE RELIC IS

```
CINDERCLEAVE  dwarven x scythe, the 29th relic. `onHit:{ sunder: 1 }`, and
              every physical stat is the SCYTHE'S, copied off Thornwake,
              Lastlight, Foregone and Vesper — all four already carried that
              line byte for byte. `SHAPES.scythe` routes `dwarven` to
              `_scBuilt`, which has drawn this cell since before there was a
              relic in it
BREACH        a LICENCE, not a clock. For up to 14s the scythe cuts the walls
              and THE FIFTH CUT ENDS IT. Each cut tears a hole sized by how
              deep the blade went; a hole fires a travelling jet into the room
              every 1.1s for 9s, dealing 9 and applying 1 Sunder. Foe only
```

## 2.1 The cell cannot be argued on the channel, and that is what named the ultimate

`sunder_survey` measured dwarven's channel on all six types at their own
shipped damage. The roster splits in half at the status's OWN duration —
`gap / dur` reads 0.66, 0.67, 0.69 and then 1.02, 1.05, 1.26, with **nothing at
all between 0.69 and 1.02.** The scythe misses that line by **0.24 seconds** and
sits at 1.23 stacks when it lands a blow, with 42% of its blows landing on
zero.

Dwarven's other four all treat the stack as something to SPEND or make more of.
Nothing in the school HOLDS it, and holding it is what this body needs. Breach
does the third thing: **it fills the gaps.**

> **AND THAT IS MEASURED ON THE BUILT RELIC, NOT INHERITED FROM THE LAB.**
> `breach_relic_probe [7]`: the quarry sits at a **mean 3.75 Sunder stacks
> while holes are open**, against the 1.23 `sunder_survey` measured for this
> body unhelped. 210 of 432 jet hits raised the stack and **the rest landed on
> a quarry already at the cap of six** — which is the ultimate doing exactly
> what it is for, and which is why the first cut of that check (">50% of hits
> must raise it") was the wrong assertion and failed on a working relic.

---

# 3. THE PICTURE, AND THREE OF ITS FAULTS DIED ON THE FIRST SHEET

`breach_sheet.py` photographs a REAL match at the first frame that satisfies
each of eight predicates. `05-reference/v59/breach-states-*.png`.

**THE JET READS, AND THE FIRST CUT OF IT DID NOT.** At `k` 1.5 the frame was
right the first time — an amber wedge crossing the hall, tapering from the
wall, a white crescent at the head, Rick's reference frame delivered. At `k`
0.8 the same object was **a smear**: a 15px band of low-alpha amber that a
viewer would read as a lighting artefact.

Three changes, and the constraint on all three is that **`half` IS the hit box**
— `tickBreach` and `drawVents` call the same `halfAt` expression, so a beam
drawn wider than it tests would be a jet that looks like it connected and did
not, which is the one thing this ultimate must never do:

```
THE HOLE      0.66 of `half` -> 1.15. At k 0.8 the first cut drew a 12 x 6
              pixel ellipse on a 540-wide frame. The hole is PICTURE and
              nothing else — the beam's width is the hit box and is untouched
THE GLOW      what was added to the small jets is LIGHT, not width. §7a rules
              out carrying it in white (dwarven and sanctified are the closest
              pair in the game and were separated on VALUE), so the halo is the
              Crucible's own `#FF6A1A`
THE ANCHOR    the body ran as a fixed 360-unit slug and read as a projectile.
              It runs from the WALL to the head while the front is inside the
              hall and the tail follows it off afterwards — which is what
              "tapers to nothing at its origin" means and what stops a spent
              jet sitting across the room as a bar
```

And the alphas came DOWN after that, not up: two jets crossing under `lighter`
saturated toward white in the middle, which is the exact thing §7a says can be
got wrong permanently.

## 3.1 The count reads, which is open decision 1 answered rather than deferred

Design §5c: *a viewer should be able to tell the fourth tear from the fifth
BEFORE the fifth lands, or the ultimate ends without having promised it.* That
is Grasp's four-knuckles problem one relic on.

Five chips ride the caster's shell and go dark one per tear.
`05-reference/v59/breach-count-tell.png` is the same shell at 5, 4, 3, 2 and 1,
and the countdown is legible at every step. **It is Rick's to accept or
replace** — the alternative he was not offered is marks on the scythe itself.

> **A SPENT CHIP IS ALMOST INVISIBLE** (alpha 0.30 on `#5A3A1C`), so "1 left"
> reads as *one chip* rather than as *one of five*. Deliberate — fewer marks is
> closer to the end — but "1 of 5" carries more, and it is a one-line change.

## 3.2 The dwarven scythe was looked at before stage 1, which the brief asked for

`05-reference/v59/scythe-row-colour.png` and `scythe-dwarven-zoom.png`.
`_scBuilt` is a grey steel crescent with three rivets on its back, a brown
haft, a strut, and **a square bracket plate carrying four bolts at the collar.**

> **IT IS THE CONSTRUCTION RICK JUST REJECTED, AND THE NUMBER SAYS IT IS
> FINE.** The bracket and the bolts are separate stroked shapes sitting on top
> of `_scBase` — which is exactly what made the umbral warhammer's spikes read
> as *"triangles layered behind the hammer"* two builds ago. The brief's own
> open decision 6 said to look at this on a real frame and to treat 71.5%
> distinct as unverified until then; looked at, the silhouette IS distinct
> (the bracket is unique in the row) and it is built the way `_whEaten` was.
> **This is open item 34 with a third instance and it is Rick's.**
>
> **AND IT IS NOT DWARVEN-COLOURED.** The crescent is `p.steel`, which is
> dwarven's `#6A6E74` grey, so a forge school's scythe is a grey blade on a
> brown stick. The warhammer's amber does not reach it. Open item 36 is the
> same sentence about umbral.

---

# 4. WHAT THE BUILD REFUSES TO DO

Every one of these is a "WHAT NOT TO DO" from the brief that would leave every
number right and the relic wrong, which is this project's own defect class.
`cindercleave_build.refuse()` greps the shipped source of `tickBreach`,
`tearVent` and `jetHit` — **with the comments stripped first, because this file
explains itself in that source** — and will not write if any of them is broken:

```
not a shot            `spawnShot` shifts the oldest live entry out at maxLive 64
                      and `tickShots` lets a BLADE parry one. A jet of heat a
                      scythe can parry is a different mechanic
not on `m.ultFx`      ONE SLOT, and the opponent casting anything erases it —
                      measured at 0.0% survival against Ironhail (v54 §2a)
`k` drives width and life only     everything-at-once is +6.1pp and is four
                      knobs riding one scalar, which leaves the bisection
                      nothing to grab
{wall, u} in arena space           the inset walks 0 -> 140 from t=21s, so an
                      absolute (x, y) torn early is buried in stone by t=60
the pass IS the cooldown           no `tearCd`, no `cutCd`
the bearing is hashed              `shellHash`, never `this.rng()` — a relic not
                      in the match must not perturb the draw order of one that is
```

And one more, asserted at runtime rather than in the text: **the shipped `ult`
block carries every number the run printed.** That is v56's own failure — a
builder that logged a new rhythm and shipped the old one because stage 3
rewrote only the line carrying `charge`.

> **AND IT FIRED ON ITS OWN EXPLANATION THE FIRST TIME IT RAN.** The relic's
> comment says *"STUBBED AT `charge:1e9` IN STAGE 1"*, and the check read
> `charge: 1e9` out of the PROSE and refused to write a build whose code said
> 15. Third session running for that sentence. It strips comments now.

---

# 5. THE THREE REGISTERED PREDICTIONS

```
(2)  the built pass reproduces the lab's depth distribution     STRUCK — §1
(3)  the 14s cap ends fewer than 1 window in 50                 STRUCK — 0 of 108
(1)  the built relic lands 48-53% against the field             see §6
```

> **(3) LOOKED REFUTED AT 12% AND THE FAULT WAS IN THE CHECK.** The first cut
> of `breach_relic_probe [2]` classified every window that did not reach five
> tears as "the cap ended it" — and of 108 windows, **6 ended because the
> CASTER DIED and 7 because the MATCH did.** Neither is a guard rail failing.
> Separated, the cap ends **0 of 108**. The brief's instruction if this failed
> was "the DESIGN changes, not the number", so a check that cannot tell three
> endings apart was one step from redesigning a mechanic that works.

---

# 6. THE BLADE IS 19.75, AND THE CHEAP PASS THAT BRACKETED IT WAS WRONG BY FIVE POINTS

## 6.1 The floor, and the ultimate is worth what the lab said

```
  blade 21, NO ULTIMATE (charge 1e9)    18.8%   n=336
  blade 21, with BREACH                 47.3%   n=336
  the ultimate is worth                +28.6pp on the same blade
```

The lab measured **+28.5%**. That is the closest a lab-to-build carry has come
in this chain — Shroudmaul's `held` came in 45% over its lab, because
`grab_lab` held its charge clock while its window ran and the engine does not.
Nothing here had that hazard: `vent_count_lab` ran the real `step()`.

## 6.2 The curve, and it does not bend

```
  12.00  21.4%     18.00  43.5%     24.00  61.9%     30.00  75.6%
  15.00  36.3%     21.00  47.6%     27.00  64.9%
  monotonic — 50% bracketed by 21.00 and 24.00
```

**Gravemourn's bends** — 67.3% at dmg 47.2 and 60.6% at 52.0, because a bigger
blow throws the quarry out of reach of a weapon that lands 5.6 times a fight.
This one does not, which is the one thing a cheap wide pass is FOR and the
reason it was run first.

## 6.3 And then the wide measurement refuted its own bracket

`cindercleave_sweep --only 2`, n=1008 a point on TWO independent seed blocks
and on BOTH sides:

```
   blade   A blk1  A blk2  B blk1   pooled
   18.50    47.8%   48.7%   43.5%    46.7%
   19.12    46.8%   48.2%   45.6%    46.9%
   19.75    49.9%   50.3%   49.3%    49.8%   <- SHIPS HERE
   20.38    53.7%   52.1%   49.2%    51.7%
   21.00    53.4%   52.0%   52.1%    52.5%
   24.00    63.1%   57.3%   58.4%    59.6%
```

**The curve read 47.6% at blade 21 and the wide measurement reads 52.5%.**
Five points, same number, same build. `verify --n 40` read Cindercleave at
**51.6%** at that blade independently, and agrees with the wide measurement.

> **THE CURVE IS THE OUTLIER AND IT IS SAMPLE SIZE, NOT SIDE.** The first
> reading of this gap credited it to `verify` running an appended relic as side
> B in all 28 of its pairings while every sweep in `tools/` runs it as side A.
> That was wrong: the wide side-A blocks read 53.4% and 52.0% at the same
> blade, so the real asymmetry at 21.00 is about **−1.3pp**. The five points
> were n=168 a point against n=1008 on each of three blocks. **CLAUDE.md's
> "nothing below n≈700 ranks anything on this roster" applies to the pass that
> CHOOSES THE BRACKET as much as to the one that reads the answer** — and a
> bracket that is wrong sends a wide measurement to the wrong place, which is
> what happened here and cost 15,120 fights.

**WHAT SHIPS IS THE MEASURED ROW AND NOT THE FITTED NUMBER.** The interpolated
crossing is 19.81. 19.75 is the only row whose three independent readings sit
inside one point of each other (49.9 / 50.3 / 49.3), the honest precision on
this roster is half a damage point, and 21.00 reproduced its earlier run to the
decimal on all three blocks — which is the reproducibility control.

> **AND `verify` READS THE SHIPPED RELIC AT 47.9%, WHICH IS A FOURTH BLOCK AND
> NOT A CONTRADICTION.** It is one seed set, side B only, n=1120 — and the wide
> table's own side-B block read 49.3% at the same blade. Pooling all four
> readings at 19.75 gives **49.3%**, which is 0.7pp under 50 against a slope of
> 2.4pp per damage point: **a third of a damage point, inside the precision
> this roster can express.** The blade is NOT re-tuned on it. Re-tuning on a
> single n=1120 block is the exact mistake that put Shroudmaul's blade a whole
> point wrong, and the instrument designated to settle this — two blocks, both
> sides, n≥1000 — has already answered.

**REGISTERED PREDICTION (1) IS STRUCK.** *"At blade 21, n 5, period 1.1, life
9.0, dmg 9, half 14 and front 1100, the built relic lands 48-53%."* It lands
**52.5%**. The blade came down because the band is aimed at 50%, not because
the prediction missed. All three registered predictions hold.

## 6.4 The type ladder, and this relic does NOT have the hole the last two had

```
  twinblade   63.5%      warhammer  51.0%
  greatsword  53.6%      flail      46.9%
  scythe      53.1%      bow        46.7%      TYPE SPREAD 16.9pp
```

Against **Thornshear's 43.6pp** and **Shroudmaul's 40.1pp**. No type is under
46%, and `verify`'s per-relic band is a perfectly good instrument for this
relic. Open items 12 and 32 argue that the band is the wrong instrument for a
CONCENTRATED relic; this is a third data point saying the concentration is a
property of those two relics rather than of the band.

## 6.5 And the second contact rate is the same size as the first

```
  blade blows       7.47 a fight     <- the scythe's own slow rate
  JET HITS LANDED   7.76 a fight     <- out of 68.3 jets fired
  jet damage        97.9 a fight, 26% of everything the relic delivers
  MEAN SUNDER       3.72 while holes are open, against 1.23 unhelped
  holes a cast      4.54 of 5        casts a fight 2.07
```

*"It is a second contact rate running underneath a slow weapon"* is the design
doc's sentence, and it is a measurement: **the ultimate lands as many payments
a fight as the blade does**, and 74% of what the relic delivers is still the
blade. It carries the body across `sunder_survey`'s 5.0s line — 1.23 stacks to
3.72 — for as long as the holes are open.

---

# 7. THE SHADES DECISION, TAKEN THE OTHER WAY

Design §4.8 asked for a rule and offered *"a jet catches shades like any other
body"* as its placeholder. **This build takes the other answer**, and it is a
decision rather than convenience:

**THE ROSTER PRECEDENT IS QUARRY-ONLY.** Every payload in this game that
resolves outside `resolveHit` reads the real fighter and nothing else — the
Deadfall's mines test `g.src === "a" ? this.b : this.a` and no copy has ever
set one off. `tickShadeHits` exists precisely because the ordinary hit loop
does not offer a copy as a target.

**AND NOTHING PRICED IT.** Every number in `06-docs/v57/` is measured against
the real quarry, and `spent` is ONE payment per firing — so a jet that swept
three bodies would either pay once into whichever it met first, which makes a
Twinshade window a SHIELD, or pay three times, which is a damage multiplier
nobody measured.

> **THE CHECK CAN FAIL, WHICH IS WHAT MAKES IT A CHECK.**
> `breach_relic_probe [6]` counts the frames on which a copy was
> *geometrically inside a jet's swept path* using the same predicate
> `tickBreach` uses: **3,075 opportunities, 0 caught.** A "no shade is ever
> hit" that never had the chance would have been worth nothing.

---

# 8. THE FOUR VOICES

Rendered and measured in an `OfflineAudioContext`, because `SFX.play` returns
on its first line headless and swallows its exceptions — v42 shipped a silent
ultimate through every green check in this repo.

```
                        peak   audible   <120Hz   >300Hz
  the cast             0.405     1.55s     0.69     0.50    ignition, no resolve
  the wall tears       0.321      1.2s     0.34     0.77    rock, then heat
  a hole spits         0.143      1.0s     0.29     0.81    quiet: up to 5 a second
  and it connects      0.495      1.2s     0.44     0.69    the payment
```

> **AND THE JET RENDERED AT PEAK 0.000 THE FIRST TIME, WHICH WAS THE PROBE.**
> `SFX_JS` schedules at `currentTime = 1.0` inside a `secs`-long buffer, so
> the window actually rendered is `secs - 1.0` — and the first cut of the case
> list asked for 1.0 seconds, which renders NOTHING. That is
> indistinguishable from the silent ultimate the check exists to catch, and it
> is the reason the check earns its place even when it is the probe that is
> wrong.

`_burst`'s 0.6s ceiling is asserted on the SOURCE and not on the render
(CLAUDE.md §4.5: it does not loop its noise buffer, so a longer one plays
silence into its tail and the waveform looks exactly like a sound that ended).
8 bursts across the four voices, longest 0.55s.

---

# 9. THE TOOL THAT WAS AUDITING NOTHING

`chain_audit.py` reported **"ALL 1 INSERTS SURVIVE"** against a builder with
nineteen. Open item 31 said this would happen again and it did, one costume
along: the tuple-table discovery ran only `if not out`, so a builder carrying
BOTH shapes — one `*_NEW` constant for its fx spec and eighteen edits in
`(label, old, new)` tables — had the constant found, `out` come back non-empty,
and the eighteen never looked at.

Both passes run now and the results are merged. **19/19.** *A green
`chain_audit` that audited nothing is the exact failure mode the tool was
written for*, and this is the fourth time its discovery has been too narrow.

---

# Open decisions — Rick's

1. **THE COUNT TELL.** §3.1. Five chips on the shell, going dark one per tear.
   It reads; whether it is the right OBJECT is a taste call, and the
   alternative is marks on the scythe. A spent chip is also nearly invisible,
   so "1 left" reads as one rather than as one of five.

2. **THE DWARVEN SCYTHE IS BUILT THE WAY THE UMBRAL WARHAMMER WAS.** §3.2. A
   bracket and four bolts stroked on top of the base — the construction
   rejected two builds ago — and a grey blade in a forge school. Nothing is
   measured and nobody has complained; open item 34 now has three instances.

3. **SHADES.** §7. Taken as quarry-only, against the design doc's placeholder,
   for a reason. Reversible in one line and the check moves with it.

4. **THE NORTH WALL TAKES 3.9% OF THE TEARS**, so the one bearing only it can
   produce — straight down into the room — is drawn 1.2% of the time. Rick's
   aim rule is *"all 8 directions are possible"* and all eight are; one of
   them is a rarity. Not a defect and not free to change: weighting the walls
   would mean inventing where a scythe cuts.

5. **THE JET AT `k` 0.5 IS SMALL ON PURPOSE AND MAY BE TOO SMALL.** Shape
   questions go to a sheet; SCALE questions need the video. The sheet says it
   reads; a phone screen is Rick's call.

6. **NOBODY HAS WATCHED IT.** `07-shorts/v59/breach-first-cut.mp4`. Rule 2,
   and every relic in this chain has had at least one thing moved by a person
   watching that no probe had a number for.

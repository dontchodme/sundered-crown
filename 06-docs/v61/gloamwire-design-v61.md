> # ⚠ READ `CONFLICT-READ-FIRST-v61.md` BEFORE ANYTHING IN THIS FILE
>
> **1. THERE IS A SECOND v61 DESIGN FOR THIS CELL.** `quiver-design-v61.md`,
> written in another session on the same day, gives the umbral bow a completely
> different ultimate — *the misses come back*. Rick made a full set of design
> choices in BOTH conversations and neither session could see the other. This is
> the Ravelbone/redhammer collision of `06-docs/v60`, one cell along. **Do not
> build from either until Rick has chosen.**
>
> **2. EVERY NUMBER BELOW IS MEASURED ON `sc-breach.html` — 29 RELICS — AND THE
> BUILD OF RECORD IS NOW `sc-garrote.html` AT 30.** Bloodmirror and Ravelbone
> landed after this session's measurements were taken. The design's *structure*
> (§4's geometry is algebra, not a sweep) survives a roster change; every WIN
> RATE in it does not, and the composition table in §6 must be re-run before the
> blade is believed. `tools/net_lab.py` re-runs all of it.
>
> **3. THE RELIC NUMBER IN THIS FILE DISAGREES WITH `quiver-design-v61.md`.**
> This doc calls the umbral bow the 32nd, counting design order (Bloodmirror
> 30th, Ravelbone 31st); the bow-row survey calls it the 31st CELL, counting
> what is built (Bloodmirror is designed and not in any link). Both are
> defensible and they must not both ship. v57's own drift is the precedent.

# v61 — GLOAMWIRE AND CROSSWEAVE. The umbral bow, and the finding that the cell's own file was wrong about it: v40 published *"curse delivers zero on a bow — +0±0, identical to baseline in every column"*, and under the reworked curse the same cell is worth **+19.0pp**.

**2026-09-01, Cowork.** Rick: *"lets design another one. umbral bow"* — the cell
taken by name rather than off a spread, after being offered and declined twice
(v57 §4 for the 29th, and again among the four for the 31st).

Everything below is **runtime injection against `02-chain/sc-breach.html`** —
the build of record, 29 relics, Cindercleave and Breach in it, Bloodmirror and
Ravelbone not. **Nothing was written to any build.** New tool: `tools/net_lab.py`.

```
THE THIRTY-SECOND RELIC          GLOAMWIRE      umbral x bow
                                 CROSSWEAVE     a magazine of 24 triple-shot
                                                volleys at twice the cadence,
                                                each volley strung with two
                                                bars of purple lightning
grid after it                    umbral 5 of 6 types · bow 6 of 7 schools
the only cell left on the row    runic x bow
```

`tools/net_lab.py` runs every table below end-to-end — stages 0 to 7, 41 checks,
all passing — and reproduces each one within noise at a third of the seeds. It is
the instrument, not a transcript: **run it on the pin before building anything**
(build brief, Gate 1).

**THE HARNESS IS NOT THE PINNED ONE AND IT IS DECLARED UP FRONT** (v57 open
decision 4, honoured). Chromium **141.0.7390.37** against the repo's pinned
151.0.7922.34; `cdn.playwright.dev` is still blocked from Cowork. So the
reproduction control was run first, and it is in §1.

---

# 0. THE REPRODUCTION CONTROL, AND WHAT IT CAUGHT ABOUT v57'S OWN NUMBERS

v57 §1 publishes the bow row as `no-channel floor 40.0%` and
`umbral x bow +14.6%`. Reproduced here on 29 relics, `row_price`'s own seed
base, 28 foes x 6 seeds = 168 fights an arm:

```
                                 here     v57 (27 relics)
no channel (the floor)          40.5%               40.0%
umbral x bow                    59.5%   +19.0pp    +14.6pp
```

**The floor lands within half a point across two Chromiums and two rosters.**
The lift is 4.4pp apart against a per-cell SE of 3.9pp and two relics of field
difference. The instrument agrees with itself.

## 0.1 AND `row_price`'s WORLD HAS NO ULTIMATES IN IT, WHICH HAS NEVER TRAVELLED WITH THE NUMBER

`row_price.CH2_JS` takes `noult` and `main` passes it **`True` on both arms**
(lines 215 and 217), so every ultimate in the game is stubbed at `charge:1e9`
for the whole table. That is a legitimate instrument — it isolates the channel —
but it is not the shipped game, and five surveys have quoted its column without
the caveat. The same cell, same fights, ultimates left alone:

```
                            ults ALL stubbed    shipped world
no channel (the floor)               40.5%            23.8%
umbral x bow                         59.5%            55.4%
lift                                +19.0pp          +31.5pp
dwarven x bow (shipped Ironhail)         —            54.2%
```

**The LEVELS agree and the FLOORS do not.** 59.5 against 55.4 is one SE; 40.5
against 23.8 is sixteen points, and all of it is Quarrelstorm — worth +19.6pp on
the shipped relic and +25.6pp carried on the curse arm. Any cross-row comparison
drawn from `row_price` is a comparison between weapons that cannot cast.

> **The honest summary of the cell: an umbral bow lands at 55.4% in the shipped
> world against a field mean of 50.0%, and swapping sunder for curse on
> Ironhail's own body is +1.2pp.** The cell was never chosen for being stronger
> than dwarven. v57 §Open decision 2 called the bow row a coin flip and it is.

---

# 1. WHAT v40 GOT RIGHT, AND THE ONE LINE THAT IS NOW FALSE

v40 §4.1 is titled **"CURSE DELIVERS ZERO, AND THE OCCUPANCY TABLE SAYS IT IS
THE BEST SCHOOL"** and it was correct when it was written: the old curse
subtracted `maxHpLoss` per application, `hp` only followed when `maxHp` was
driven under it, and at Ironhail's 16.23 a hit that column read `+0±0`.

**That mechanic no longer exists.** `STATUS.curse` is now `maxStacks:3, dur:99,
echo:0.08` and a stack remembers `dmgBase`. Measured on the same body:

```
arm (donor ult OFF, foes' ults ON)      win     blows    dealt
none                                   9.5%      12.6      287
curse                                 29.8%      12.5      342     +20.2pp
sunder                                34.5%      11.8      334     +25.0pp
```

Everything else in v40 survives and is load-bearing below: the shot block is a
property of the TYPE (asserted, 5 relics, 1 distinct block), an arrow and a
swing deal the same base damage (`shot.dmgMul` 1.0, asserted), and **82% of
every arrow loosed ends on a wall**.

---

# 2. THE CELL'S IDENTITY IS TIMING, AND IT IS THE BEST POOL-PER-SECOND BODY IN THE SCHOOL

Every umbral body, `onHit:{curse:1}`, donor ult suppressed, foes' ults on,
pool sampled every 0.25s of sim, 168 fights a row:

```
body           shape        dmg   blows   pool   peak    1st    3rd   at cap
gravemourn     flail      24.03     6.6   61.9  122.9   7.8s  21.9s     48%
shroudmaul     warhammer  21.00     8.4   60.6  116.3   8.1s  19.6s     56%
GLOAMWIRE      bow        16.23    12.5   54.2   99.2   5.1s  13.1s     71%
nightfell      greatsword 12.27    13.8   43.9   88.3   4.9s  14.9s     70%
twinshade      twinblade   8.30    15.5   31.0   65.1   5.4s  15.4s     71%
```

**Third-deepest standing pool in the school, reached in half Gravemourn's
time.** Twinshade's uptime (71%) on nearly Gravemourn's depth. 0 of 168 fights
failed to fill it.

And the memories are made **at range**: 64% of its blows are arrows and 63% of
its damage. Every other umbral relic has to close before it can remember
anything; this one starts remembering at 5.1s from across the room.

Two routes to the echo agree, which is the section's own control:
`pool x 0.08 = 4.34/blow`, and the paired damage against the no-channel arm is
`+55.2 over 12.5 blows = +4.40/blow`.

---

# 3. THE DESIGN, IN RICK'S WORDS

> *"a simple ult.*
>
> *purple bow gains a triple shot. each arrow connected by a string of purple
> lightning. Enemies hit by an arrow take extra damage. enemies hit by only the
> lightning take no damage but take extra knockback. Enemies hit by both take
> both"*

and, on seeing the fire-rate field exists:

> *"can we also give the ult increased fire rate?"*

Every number below was measured against that and nothing was proposed before it.

## 3.1 WHAT WAS ALREADY SPENT, CHECKED BEFORE ANYTHING WAS DRAWN

CLAUDE.md §4.8 — look at the superset first.

```
umbral's four ultimates    Revenant  carries the pool out on hands
                           Deadfall  parks it in mines on the floor
                          Triplicate three bodies feeding one pool
                             Grasp   denies the swing; pool-blind

the bow row's five         Quarrelstorm  a nova of arrows
                              Reprisal   one heavy arced shot
                            Benediction  a beam that heals
                               Thicket   seeds that root in walls
                             Bloodhunt   homing bolts that fork
```

"Fire more arrows" is taken five ways. Nothing on the row has ever addressed
the wall, and this design does not either — it is worth saying plainly, because
v40 open decision 2 has now survived six bow relics.

---

# 4. THE GEOMETRY DECIDES WHETHER THE DESIGN EXISTS, AND IT IS ALGEBRA BEFORE IT IS A SWEEP

```
an arrow connects at    R + shot.r  = 34 + 24 = 58
a strand connects at    R + strandW = 34 + strandW
```

A strand's endpoints **are** its arrows, so any ball inside `R + shot.r` of an
arrow is inside `R + strandW` of the segment whenever `strandW > shot.r`.
**Therefore "hit by the arrow alone" is identically zero above `strandW = 24`,
and "hit by the lightning alone" is identically zero below it — by construction,
not by balance.** The crossover is at `strandW = shot.r = 24` exactly.

Swept, parallel arrows 130 apart, `dmgMul` 1.0, **knock 0**, 168 fights a row:

```
 strandW  reach    both   arrow only   light only   miss     win
       0     34      6%          14%           2%    78%   61.9%
      12     46      7%          13%           2%    77%   61.9%
      18     52      9%          11%           3%    77%   61.9%
      24     58     15%           5%           3%    76%   61.9%   <- the line
      30     64     18%           2%           5%    75%   61.9%
      40     74     18%           2%           7%    73%   61.9%
      60     94     19%           1%          12%    68%   61.9%
```

**The win column is identical to the digit down the whole sweep and that is the
instrument's own control**, not a bug: at `knock 0` a strand records a
classification and touches nothing, so every arm is the same fight. When the
column moves in a later table, the shove moved it.

**So there is no setting that gives three balanced outcomes.** The design is a
dial between two regimes: *arrows with a lightning bonus* below the line,
*a lightning net with arrow bonuses* above it. **Rick took above the line**, over
equal-width and a hairline.

**The control that says the strand test can fire at all:** at a reach past the
arena diagonal (520x800 -> 953) the miss rate must go to zero.

```
 strandW  reach   light only   both   miss
     300    334          63%    20%    17%
    1000   1034          80%    20%     0%
    3000   3034          80%    20%     0%
```

## 4.1 FAN AGAINST PARALLEL, AND WHY THE FAN WAS TAKEN

A fan's gap grows with range; a parallel net's does not. Both at `strandW 30`:

```
shape           gap    both   arrow   light   miss     win
parallel  70     70     15%      2%      2%    80%   69.0%
parallel 130    130     18%      2%      5%    75%   61.9%
parallel 200    200     16%      3%     11%    71%   56.5%
fan  17 deg      46     15%      2%      2%    82%   62.5%
fan  34 deg      88     16%      3%      4%    77%   65.5%
fan  52 deg     126     17%      4%      6%    73%   68.5%
```

**Rick took the fan.** It is the only shape whose behaviour changes over the
arrow's flight, and it is the strongest of the wide options.

## 4.2 AND THE STRAND'S WIDTH TURNS OUT TO BE A PURE SHOVE DIAL

Contacts counted as EVENTS with their own ranges — arrow contacts and strand
contacts separately, `dmgMul` 1.0, knock 260:

```
  fan  strandW   arrow contacts   strand contacts     win
  34d       60              7.2              11.5     68%
  34d       90              7.1              15.1     61%
  52d       60              7.2              12.6     67%
  52d       90              7.0              16.4     61%
  52d      120              7.3              21.5     64%
  69d       60              7.5              13.1     74%
```

**Arrow contacts do not move — 7.0 to 7.5 across a doubling of the strand.**
Widening the lightning adds shoves and takes nothing away. So how thick it is
drawn is a LOOK decision and the balance is indifferent to it.

Arrow contacts by range: **12-16% inside 100 units, 43-46% at 100-200, 40-42%
beyond 200.** The volley damages at every range.

---

# 5. THE FIRE RATE, AND THE ONE DECISION THAT MAKES IT AFFORDABLE

`tickFire` already reads `f.w.ult.cadMul` inside a window and multiplies the
cadence by it — Marrowdraw uses it at **4** to go *drastically slower*. Below 1
is faster. Nothing new is needed in the engine except the gate (§7).

**THE CEILING THAT COULD HAVE MADE THIS SWEEP LIE, MEASURED AND NOT ASSUMED.**
`CONFIG.shot.maxLive` is 64 and `spawnShot` SHIFTS the oldest off the front when
it is reached. A triple shot at 4x is nine times an ordinary bow's projectile
load. **Evictions: 0.0 at every rate, up to 205 arrows a fight.** The cap is
never the thing being measured here.

```
                        rate   volleys   arrows landed   shoves    win
8-SECOND WINDOW           1x      31.6             7.0     16.4     61%
                          2x      49.0            10.1     23.5     88%
                          4x      68.5            12.4     30.0     98%

MAGAZINE OF 24 VOLLEYS    1x      35.9             8.0     18.1     65%
                          2x      36.6             8.1     18.8     79%
                          4x      38.7             7.6     18.1     76%
```

**Under a magazine the payload is invariant** — 8.0/8.1/7.6 arrows landed,
18.1/18.8/18.1 shoves — the same magazine simply arrives sooner. The window
collapses 8.2s -> 4.1s -> 2.0s.

**The +13pp that remains is not payload, and it was pre-registered as a reason
this might not be free:** nets landing 0.17s apart do not let a shoved ball
recover between them. A duration multiplies everything and costs +37pp.

**Rick took the magazine.** It is also the shape he chose for Breach — *"3-5 and
then its done"*.

---

# 6. THE COMPOSITION, AND WHAT IT COMMITS THE RELIC TO

Four separate strength clauses now: three arrows for one, extra damage on the
arrow, double cadence, and the shove. `dmg` is what pays. Magazine 24 at 2x,
fan 52 deg, `strandW` 90, knock 260, 140 fights a cell:

```
arrow damage       blade 16.23   blade 13.0   blade 10.0   blade 7.0
normal  (1.0x)             79%          66%          46%         13%
  +40%  (1.4x)             86%          72%          60%         25%
  +80%  (1.8x)             89%          91%          75%         40%
```

The other five bows ship at **12.73 - 16.23**. Every configuration that keeps
all four clauses puts this relic below the row.

**Rick took all four clauses at blade ~9**, over dropping the fire rate
(blade ~11.5) and dropping the extra damage (blade ~10.3).

## 6.1 THE MAGAZINE SIZE

Blade 9.2, arrows x1.4, fan 52 deg, `strandW` 90, 2x rate, knock 260:

```
volleys   window   arrows   arrow hits   shoves   pool     win
     12     2.0s       36          5.7     13.1   39.2     25%
     18     3.1s       54          8.1     18.1   39.0     36%
     24     4.1s       72          9.9     22.3   40.8     51%
     30     5.1s       90         11.6     26.0   41.0     63%
     36     6.1s      108         12.3     28.2   40.6     66%
```

**Rick took 24**, from a ladder of three. 51% against a field mean of 50.0%, and
it agrees with §6's independent grid, which put blade 9.2 at ~50%.

## 6.2 THE SHOVE IS A COST, AND TWO EARLIER PASSES DISAGREED ABOUT IT

```
knock   strand contacts   separation     win
    0              23.9          269     58%
  130              22.8          270     56%
  260              22.3          271     51%
  400              22.2          274     49%
```

**Monotone down, 9 points across the sweep, and separation never moves.** A
shoved ball is displaced out of the path of the volleys still in the air. Two
earlier passes at a different composition read +4pp twice and +0.7pp once — all
inside one SE, all now superseded by four monotone arms at the shipped shape.

This is **not** a reason to cut Rick's clause. Read the other way, the shove
**buys back about a point of blade**: the relic reaches the field at 9.2 with it
and would need ~8.4 without. It is a look that pays for itself.

---

# 7. CROSSWEAVE IS THE FIRST UMBRAL ULTIMATE THAT LEGITIMATELY RAISES THE POOL

v49 §5b closed this by measurement and generalised it: *"a capped top-K pool is
already full. An ultimate cannot ADD to this pool. It can only SPEND it."* Two
caps and three rules of what an ult-applied stack might remember all landed
inside the noise.

**That was measured on ultimates with NO BLOW behind them** — Dirge and Eclipse
applied Curse from an `apply` field. Crossweave's arrows are real blows at
**1.4x the blade**, so they push memories the blade cannot make, and `resolveHit`
already does it with no new code: `foe.pushCurse(dmgBase, n)` where `dmgBase` is
post-crit, post-jitter, pre-echo.

```
curse pool with Crossweave        40.8
curse pool with it stubbed off    33.8      +21%
```

**The rule in v49 §5b should be amended rather than repealed:** an umbral
ultimate cannot add to the pool *by applying curse*; it can add to it by
*landing a bigger blow than the blade*. Crossweave is the only ultimate in the
game that does.

---

# 8. WHAT THE ULTIMATE IS WORTH, AND THE RISK IN THE NUMBER

`ult_price`'s method — the same 168 fights with `charge` at 1e9:

```
win with Crossweave         51%
win with it stubbed         2%
Crossweave is worth      +48.8pp
```

```
lastlight   Harrowing    +49.6
GLOAMWIRE   CROSSWEAVE   +48.8
censer      Consecration +24.8
                  median +20.4
gravemourn  Dirge         -3.2   (retired)
```

**Second-largest ultimate in the game, and the relic wins 2% of fights without
it.** That is what Rick chose and the measurement confirms the choice rather
than questioning it — but it is the sharpest ultimate-dependence on the roster
and it should be stated on the card, not discovered in a sweep six versions
later. A charge delay, a hex lock at the wrong moment, or any future nerf to
`cadMul` hits this relic harder than any other.

---

# 9. THE SETTLED SHEET

```
  { id:"gloamwire", name:"Gloamwire", aff:"umbral", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:9.2, spin:2.8,
    mode:"ranged", mass:1.6,
    shot:{ cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0,
           tip:"Fires along its facing · shots can be clanked" },
    onHit:{ curse:1 },
    ult:{ name:"Crossweave", charge:15, kind:"net",
          volleys:24, n:3, spread:0.90, cadMul:0.5,
          dmgMul:1.4, strandW:90, strandKnock:260,
          tip:"<24 volleys of 3 strung arrows; the strand shoves>" },
    blurb:"<Rick's, or offered>" },
```

`dmg 9.2` is a **PLACEHOLDER** in this project's sense (CLAUDE.md §4.9) and must
be swept in `gloamwire_build.py`. Every other number is measured above.
`charge 15` is the roster mode and v55b's default, taken as a positive choice.

The `shot` block is Ironhail's, Farwarden's, Aureole's, Vinesower's and
Marrowdraw's **byte for byte** — the type owns it, asserted in `net_lab` [0].

---

# How this check lied, this session

**TWO INSTRUMENTS PRODUCED CONFIDENT, WELL-FORMATTED, WRONG TABLES, and both
were caught by a control rather than by reading the output.**

1. **A REPRODUCTION CONTROL FAILED FOR THE WRONG REASON AND THE EXPLANATION WAS
   ALMOST BELIEVED.** The first arm suppressed the DONOR's ultimate and read a
   9.5% floor against v57's published 40.0%. The temptation was to write up a
   30-point disagreement between two builds. The actual cause was that
   `row_price` stubs EVERY ultimate and this arm stubbed one — §0.1, which
   turned a failed control into the session's second finding.

2. **A VOLLEY WAS THE WRONG UNIT AND IT HALVED A NUMBER.** The first range table
   binned each volley by its FIRST contact, so a volley shoved at 250 and then
   hit by an arrow at 90 was filed as "no damage at 250" and its arrow was never
   counted. It reported an 8-14% damage share where the volley accounting says
   21%, and it read as a clean finding — *"the ultimate stops damaging past 200
   units"* — that was entirely an artifact. **Fixed by recording contacts as
   EVENTS with their own ranges** and reconciled against the volley accounting
   in `net_lab` [5].

3. **AND A CONTROL THAT COULD NEVER HAVE FAILED.** The 21% miss at `strandW 300`
   was first "explained" by a `hadStrand` counter, which came back **100% at
   every width** — a strand exists on the frame its volley is born, always, so
   the counter could not discriminate anything. The sharp form is a REACH past
   the arena diagonal, and it passed at 0%.

> The rule all three share: **a control has to be able to come back wrong.**
> `hadStrand` could not. The donor-ult arm and the volley-first binning both
> could, and both did.

---

# Open decisions

1. **`dmg 9.2` IS A PLACEHOLDER AND MUST BE SWEPT.** §6.1 puts the magazine-24
   configuration at 51% against a 50.0% field, from a 140-fight grid and a
   168-fight ladder that agree — but on Chromium 141, not the pinned 151, and
   `verify.py`'s band is 30-70%. `gloamwire_build.py` sweeps it on the pin.

2. **THE ART DOES NOT EXIST YET, AND IT IS THE CHEAPEST CELL ON THE GRID TO MINT
   IN.** `SHAPES.bow`'s umbral branch already draws *both tips eaten off* and
   v40 §3 measured it at 54.5% from its nearest sibling, `inkIoU` 0.537 — the
   10th-closest pair of 21, the most distinct of the four open bow cells at the
   time. Nothing has been re-measured since Shroudmaul's `_whGnawed` moved the
   school's look. **The strand and the volley have no art at all**, and v43's
   lesson (CLAUDE.md §4.0) says film before tuning when the ultimate is a
   picture. This one is entirely a picture.

3. **THE SOUND.** Three arrows and two strands, 24 times in 4.1 seconds, is
   ~120 sound events in a four-second window. `_burst` does not loop its 0.6s
   noise buffer and `_tone` has no held note (CLAUDE.md §4.5). A per-volley
   voice at 5.9 casts a second needs a decision Rick has not been asked for.

4. **DOES CROSSWEAVE DECLARE ITSELF TO THE DIRECTOR?** CLAUDE.md §3 rule 3 — a
   hit-heavy ultimate that `cinePlan` cannot see scores its best moment as empty
   air. Five relics have filed a beat by hand. This one's best moment is
   probably the first volley that lands both, and nothing in the beat system
   knows what a strand is.

5. **THE TIP DOES NOT FIT YET.** The budget is 40 characters (`verify.py`).
   *"24 volleys of 3 strung arrows; the strand shoves"* is 48. Rick writes the
   card copy (§3 rule 2) and has not been offered a spread.

6. **`STATUS.curse.tip` STILL SHIPS THE PRE-REWORK WORDING.** Open since v55,
   quoted again in v57 open decision 5. Rick chose his own line — *"Hits reflect
   8% of the damage that cursed, stacks 3 times"* — and to widen the reminder
   popup 596 -> 760 to fit it. Still not in `sc-breach.html`.

7. **v40 OPEN DECISION 2 HAS NOW SURVIVED SIX BOW RELICS.** 82% of every arrow
   ends on a wall, ten times the leverage of any status on the row, and
   Gloamwire does not address it either. It should stop being filed as an open
   decision on individual relics and become a type-level question or be closed.

8. **`row_price`'s ULT-FREE WORLD SHOULD BE PRINTED IN ITS OWN HEADER.** §0.1.
   The tool is fine; the quoting is not. Five surveys have carried its column
   into cross-cell arguments without it. One line in the tool's output.

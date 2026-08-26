# v42 — THE BLOODSWORN BOW. §1 in Rick's words, and what the probe found before anything was built.

**2026-08-20.** Bloodsworn × bow, the twenty-fourth relic. Rick's call from four
measured candidates, against a grid where — for the first time in the project —
**the double-gap heuristic had nothing to say**: five schools at 3 of 6, two at
4, four types tied at 3.

---

# 1. THE DESIGN, IN RICK'S WORDS

> *"red bow slows down its shots drastically for a duration and begins shooting
> larger balista shots. The shots gain a homing effect that will seek out its
> opponent. when the shots hit they pierce the enemy ball fly through and fork
> into 2 shots which turn around and try to home in and hit again. the forks
> apply bleed*
>
> *the balista shot can be clanked nullifying the fork and destroying the bolt"*

Nothing was started before this existed. `redbow_probe.py` — 14/14, injection
runtime-only, no build written to — was run before a builder was opened,
because v41 built §1 literally and had it refuted inside an hour at the cost of
a build.

---

# 2. WHY IT IS THE ANSWER TO WHAT THE TYPE SURVEY MEASURED

`bow_survey` §2, re-run on the 23-relic tip: **a bow lands 8.3% of what it
fires and 81% of every arrow ever loosed ends on a wall.** v40 closed on that
number — *"the wall is the type's constraint and no relic addresses it"* — and
then Vinesower's Thicket addressed it by MONETISING the misses: seeds that
reach a wall root and lash out.

**This ultimate attacks the same 81% from the other end. It stops missing.**

```
turn rad/s   landed   parried    wall    flight s   hits/s   dmg/s     ttk
  0.00        7.1%     9.3%     82.9%      0.28      0.279    5.63    34.3s
  1.00       11.4%    11.8%     75.8%      0.34      0.398    7.49    29.0s
  2.00       18.1%    14.6%     63.7%      0.75      0.536    9.50    22.7s
  4.00       35.8%    24.8%     35.4%      0.96      0.934   14.80    16.2s
 12.00       40.9%    34.5%     21.3%      0.78      1.033   16.51    14.8s
```

Damage pinned 14.0, ultimates suppressed, five foes one per shape, five seeds,
2085 arrows on the baseline row. **The wall falls from 82.9% to 21.3%.** It is
the largest single movement any mechanic in this project has made in the
column the type survey named as the type's own constraint.

And the cell needed none of it: bloodsworn is already the strongest channel on
the bow at **+53±23 damage in a paired 20-second window (+52%)**, against
sanctified's +38 and umbral's +0. **This is the first relic in the chain whose
ultimate is not being asked to fix its own cell.**

---

# 3. §1'S TWO PHYSICAL CHANGES DO COMPLETELY DIFFERENT JOBS, AND ONE OF THEM IS NOT A BALANCE KNOB

The hypothesis going in was that **`r` is the knob that gives §1's clank clause
its teeth**, because `r` is literally on both sides of the engine's ledger: the
hit test is `dist < R + s.r` and the parry test is `dist < s.r + width/2 + pad`.
A bigger bolt is easier to hit with AND easier to bat out of the air, and which
of the two grows faster decides whether the counterplay is real.

**It was wrong. Both sides grow together and the ratio is flat.**

```
  r      landed   parried   parried per landed
  24      7.1%     9.3%          1.31
  32      8.5%     8.9%          1.04
  40      9.6%    10.2%          1.06
  48      9.6%    10.9%          1.13
  60     10.1%    13.0%          1.28
```

**"Larger ballista shots" is a LOOK knob**, in the sense v41 settled for
Aegis's `turn`: it moves the picture and it does not move the balance. Which is
a licence, not a disappointment — the bolt can be drawn at whatever size reads
best in the hall, and nothing downstream is balanced on the number.

**The teeth are in the SPEED.**

```
 speed  home   landed  parried   wall    parried per landed   flight
  380    2.0    18.1%   14.6%   63.7%          0.81            0.75s
  300    2.0    20.2%   21.4%   52.2%          1.06            1.01s
  220    2.0    23.2%   27.1%   41.1%          1.17            1.22s
  150    2.0    27.5%   26.8%   29.7%          0.97            1.35s
```

A slow bolt spends longer in the air, and the two things that happen to it
there pull opposite ways: a blade has more time to find it, and the homing has
more time to work. Between 380 and 220 the blade wins — the foe bats 1.17
bolts for every one that lands, against 0.81 at full speed. Past that the
homing catches back up. **§1's "slows down drastically" is the sentence that
hands the foe the counterplay §1's last line promises.**

---

# 4. THE FORK COMES BACK

A fork leaves at the bolt's heading with the ball behind it, so it cannot
return inside a turning radius of `v/w`. At 220 units/s that is 220 units at
1 rad/s and 55 at 4 — and 55 is smaller than the ball.

```
fork turn   radius   connects   batted    wall   ran out
   0.0        inf      36.6%     34.7%   25.5%     0.9%
   1.0        220      36.4%     30.9%   26.8%     3.2%
   2.0        110      38.4%     37.1%   13.8%     7.6%
   4.0         55      51.9%     41.0%    0.9%     1.9%
   8.0         28      56.3%     40.8%    0.0%     1.0%
```

**Above 4 rad/s no fork ever reaches a wall.** Every one of them ends on the
enemy or on the enemy's blade. The remaining 2–4% of each row is still in
flight when the match ends; nothing is unaccounted for.

`arm` is the pierce. A fork is born inside the ball it just came through and
may not hit anything for `forkArm` seconds — which is exactly *"pierce the
enemy ball, fly through"*, expressed in a field the engine already has rather
than in a new one.

**A bolt that KILLS does not fork.** 6 of 112 landed bolts were lethal and
none of them forked, which is the right answer — a blade does not stick into a
corpse, and neither should a fork chase one.

---

# 5. "THE BALISTA SHOT CAN BE CLANKED, NULLIFYING THE FORK" IS ALREADY THE ENGINE'S RULE

`tickShots` resolves in the order the viewer would: **parried, then landed,
then spent on a wall.** A batted bolt sets `dead` in the parry branch and never
reaches the hit branch, and the fork hangs off the hit branch. So the last
sentence of §1 costs nothing to build and cannot be broken by accident.

Asserted both ways: structurally, that the parry branch precedes the hit branch
in the source; and behaviourally, that **111 bolts were batted out of the air
and forked nothing**, while 106 that landed on a live foe produced exactly 212
forks.

---

# 6. THE COUNTERPLAY IS THE FOE'S PROPERTY, AND THE BALLISTA MAKES IT MATTER FOUR TIMES MORE

v40 open decision 5: *"a bow's matchup spread is unpriced."* Here it is, priced.

```
 foe            shape        today par  today land    bal par  bal land
 Dawnbringer    greatsword      13.5%       6.2%       35.3%     21.6%
 Widowmaker     twinblade       12.2%       4.4%       25.7%     20.2%
 Gravemourn     flail            4.5%       9.4%       24.7%     26.0%
 Thornwake      scythe           9.8%       6.1%       20.0%     30.7%
 Grudgebearer   warhammer        6.0%       9.8%       16.2%     31.2%
```

A greatsword bats **more than a third** of the ballista bolts out of the air.
A warhammer bats a sixth. Today that spread is 4.5%–13.5% of a stream nobody
is counting; under the ballista it is 16%–35% of the ultimate itself.

**Whether that is a matchup or a formality is a design question**, and it is
the same shape of question as v41's picture/hitbox gap: real counterplay that
is unevenly distributed by something the viewer can see (the length and width
of the other weapon) rather than by something they cannot.

---

# 7. A CORRECTION TO THE NUMBERS THE CELL WAS CHOSEN AGAINST

The candidate set was priced on `verify.py --n 12` — 3036 fights — and **that
pass was materially wrong on individual relics.** At `--n 40` (10120 fights,
13/13):

```
                n=12    n=40
  Spellbreaker  39.8%   45.8%      the "weakest relic in the game" was noise
  Emberedge     44.7%   51.7%
  Slagheart     47.7%   52.3%
  Widowmaker    51.9%   46.6%
  Grudgebearer  56.4%   60.0%
```

The two claims the choice leaned on both move: runic is **not** the weakest
school (47.2%, and umbral is 47.0%), and the bow is **not** the strongest type
(52.4%, behind the warhammer's 52.7%). Neither reverses the choice — bloodsworn
at 48.7% and a bow at second rather than first make the cell slightly *better*
than it was sold — but the rule is worth writing down:

**A CELL CHOICE PRICED ON FEWER THAN 40 SEEDS IS PRICED ON NOISE.** The n=12
pass also failed a check (`Axiom vs Twinshade 0/12`) that passes cleanly at
n=40. Five relics moved by more than five points.

---

# Open decisions

1. **CLOSED. THE THREE FORKS WERE PUT TO RICK PRICED, AND ALL THREE SETTLED.**
   The bolt **hunts** (3-4 rad/s, from three priced options); the forks carry
   the bleed and **the bolt does not** (`boltBleed 0`, and see the README §8 —
   the option he first chose turned out to be inert and the measurement sent it
   back to him); and **forks can be batted** like anything else, the Harrowing's
   rule. A fourth fork nobody had thought to name was settled too: how strong
   the relic is BETWEEN casts, which is what `cadMul` x `dmgMul` actually
   chooses once the blade bisects to compensate.
2. **`r` IS A LOOK KNOB** (§3). Stated here so it does not get swept later as
   though it were a balance one.
3. **The matchup spread is now the ultimate's own spread** (§6). v40 od 5,
   priced, and inherited by whoever tunes this relic.
4. **A fork's "hit" at turn 0 is not the sentence §1 wrote.** 36.6% of forks
   connect with NO homing at all, because they are born inside the ball and the
   ball moves into them after the arm window. The build probe must measure the
   angle a fork actually turns before it connects, or "turns around and homes
   back" will be scored by hits that never turned.
5. **Every type-level measurement still wants a `--noult` pass.** v38 od 5,
   v39 od 5, v40 od 6, v41. Unmoved.

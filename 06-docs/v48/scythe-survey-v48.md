# v48 — THE SCYTHE ROW, SURVEYED, AND THE WARD SWEPT AT LAST. Two of my own hypotheses refuted, and vigil od 4 answered after four sessions.

**2026-08-31, Cowork.** Rick: *"while code works. lets do another."* Thornshear
is with Claude Code; this is the 27th relic's plan, priced on the same tip
(`sc-paradox-ignition.html`, untouched — `02-chain` has not moved).

`tools/scythe_survey.py`, `tools/row_price.py`, `tools/curse_probe.py`.

**The scythe's first survey, and the first time a VIGIL cell has been priced
at all** — `cell_survey` prints vigil as a dash on every row, because the
school has no `onHit` channel, so no vigil cell has ever been ranked against
its own type.

---

# 0. THE CELL, AND HOW IT WAS CHOSEN THIS TIME

v47's standing complaint was that `cell_survey`'s occupancy column had
mispriced three cells. `row_price.py` is the column it was missing: one
model-free A/B per open cell, the school's channel live against the same
weapon with the channel deleted, **against the whole roster**, 240 fights an
arm. Both thin rows, every open cell, damage pinned at 24:

```
cell                     occupancy(>=2)   delivered lift
vigil x scythe            — no channel —        +19.2%
bloodsworn x scythe               45%           +11.7%
bloodsworn x warhammer            45%           +11.2%
dwarven x scythe                  28%            +7.9%
runic x warhammer                 15%            +3.3%
umbral x warhammer                68%            +0.8%
umbral x scythe                   65%           -0.4%
verdant x warhammer               44%           -0.8%
```

**Umbral tops the occupancy column on both rows and sits at or below zero on
both by delivered effect** — the fourth and fifth row where the two disagree.
That thread is its own document (`curse-finding-v47.md`): curse delivers 3% of
what its tip says, and Rick has taken the rework to the next session.

The four off-arms come back at exactly 17.5% each — the same weapon with no
school, four times — which is the internal check that the lift column means
what it says.

**Rick took vigil x scythe.**

---

# 1. THE ROW AND THE BLOCK

```
                bloodsworn   dwarven     runic  sanctified   umbral    verdant     vigil
scythe                   ·         ·  Foregone   Lastlight        ·  Thornwake         ·

type          reach  width   spin   mass  blades    mode          dmg
bow              54      9    2.8    1.6       1  ranged    12.7-16.2
flail            96     22    2.2    3.6       1   chain    25.0-44.1
greatsword      116     14    3.4    3.0       1   swing     7.4-15.8
scythe          104     11    3.2    2.4       1    spin    17.5-31.4
twinblade        62      8    5.7    1.1       2    spin     8.3-11.9
warhammer        76     26    1.6    5.0       1    spin    20.1-28.8

ward   maxStacks 1  dur 5  bank 0.55  cap 90  shatter 0.4  knock 210
```

**The widest damage spread of any three-relic type: x1.79, 17.50 to 31.35.**
Lastlight pays for the Harrowing and Thornwake does not.

---

# 2. THE BLADE

```
type          live blade  contacts/s   mean gap   rad/s  contacts/rad
bow                 59.8       0.116      8.65s    3.10        0.0373
flail               13.2       0.140      7.15s    2.55        0.0550
greatsword         125.3       0.257      3.89s    3.79        0.0678
scythe             113.8       0.195      5.13s    3.68        0.0530
twinblade           68.9       0.217      4.60s    6.41        0.0339
warhammer           83.7       0.190      5.26s    1.83        0.1041
```

**The scythe lands a blow every 5.13 seconds against a ward that lives 5.0.**
That was the survey's opening hypothesis and §4 refutes it.

---

# 3. THE CLEANEST MASS LADDER IN THE GAME

```
foe           type          mass  clanks/min    won  deadlock   lost  stagger eaten
ironhail      bow            1.6        14.8   100%        0%     0%         0.032s
widowmaker    twinblade      1.1        19.5   100%        0%     0%         0.025s
lastlight     scythe         2.4        17.8     0%      100%     0%         0.055s
emberedge     greatsword     3.0        24.7     0%        0%   100%         0.080s
gravemourn    flail          3.6        14.7     0%        0%   100%         0.070s
censer        warhammer      5.0        17.8     0%        0%   100%         0.095s
```

**It beats everything lighter, deadlocks the mirror, and loses to everything
heavier — 100% each way, no ambiguity anywhere.** Against the twinblade, which
loses every bind in the game (v47 §3), and the flail, which misses beating a
greatsword by six thousandths (v43 §12), the scythe is the one type where a
bind is a genuine matchup. Mass 2.4 sits third of six and the outcome is
decided entirely by which side of it the foe is on.

---

# 4. THE WARD, AND BOTH OF MY HYPOTHESES WERE WRONG

## 4.1 THE 5-SECOND CLOCK IS NOT THE PROBLEM

The survey opened on the claim that the ward's 5s duration is the same order as
the scythe's 5.13s contact interval, so the plate would lapse constantly and
throw its pool away. Measured:

```
type            gap  plate up  mean pool   peak  raises/min  EXPIRIES/min  shatters/min
bow           3.13s       57%       34.7     90         6.9           1.5           4.1
flail         5.67s       34%       21.3     90         5.8           0.6           4.8
greatsword    3.78s       56%       30.8     90         6.9           1.3           4.6
scythe        5.29s       42%       25.1     90         6.2           0.9           4.7
twinblade     4.15s       60%       33.3     90         6.1           1.7           3.6
warhammer     6.37s       39%       26.1     90         5.8           0.9           4.4

type            banked   ABSORBED   THROWN AWAY ON EXPIRY    kept
bow               7824       4824                    1287     79%
flail             3739       3145                     282     92%
greatsword        7944       5172                     911     85%
scythe            6350       5098                     549     90%
twinblade         7561       4709                    1408     77%
warhammer         5628       4216                     649     87%
```

**The plate ends by being SHATTERED four to five times a minute and by
expiring less than twice.** The scythe keeps 90% of everything it banks. The
clock is not the leak.

## 4.2 AND THE FIRST CUT OF THIS SECTION MEASURED IT WRONG, TWICE

Both errors are worth keeping because both were caught by arithmetic rather
than by inspection.

**A SHATTER LOOKS EXACTLY LIKE AN EXPIRY FROM OUTSIDE.** `shatter()` writes
`f.shield = 0; f.shieldMax = 0; delete f.status.ward` — the same three writes
`tickStatus` makes when the clock runs out. The first cut counted both as
expiries and added an already-ABSORBED pool to the thrown-away column. It
reported the scythe keeping 60% where it keeps 90%.

**AND `banked` WAS GATED ON `mul === undefined`.** A shot routes through
`resolveHit` with `mul` SET, so the gate counted none of a bow's banking while
the bow banked normally. The gate is right for "was this an ordinary melee
blow" and wrong for "did this blow bank".

**Both were caught by the same check, which is now permanent: absorbed plus
thrown away cannot exceed what was banked.** It read 1.93x on the bow row and
nowhere else, which is what pointed at the gate. A conservation identity is
the cheapest instrument in this repo and nothing else in `tools/` has one.

## 4.3 VIGIL OD 4, ANSWERED — AND `thrown away` IS NOT WASTE

`STATUS.ward.bank 0.55 / cap 90` have been unswept since Vigil and restated in
v41, v42, v43 and v47. A 2x2x2 around the shipped point, whole roster, 240
fights a cell:

```
  bank   cap   dur  plate up  mean pool  absorbed  thrown away   kept     win
  0.55    90   5.0       42%       24.6     29494         4184    88%   40.8%  <- ships
  0.55    90   7.0       44%       24.9     31540         1625    95%   39.6%
  0.55    90   9.0       45%       25.4     32706          517    98%   38.3%
  0.55   140   5.0       42%       24.9     29753         4343    87%   41.2%
  0.85    90   5.0       45%       37.3     42836         8237    84%   45.8%
  0.85    90   7.0       50%       38.1     46658         3302    93%   50.0%
  0.85   140   5.0       46%       40.0     45067         9274    83%   47.5%
  0.85   140   7.0       51%       41.3     49736         3873    93%   54.2%
  0.35    90   5.0       39%       15.8     19150         2286    89%   33.8%
```

**Three answers:**

1. **`cap 90` is not the constraint.** Raising it alone moves the win rate
   40.8% -> 41.2% and the mean pool 24.6 -> 24.9. Half of vigil od 4 is
   answered and the answer is "that knob does nothing where it is set."
2. **`bank` is the live knob and nobody has touched it.** 0.35 -> 33.8%,
   0.55 -> 40.8%, 0.85 -> 45.8%.
3. **`dur` HAS NO FIXED SIGN.** At bank 0.55 lengthening it *costs* 1.2
   points; at bank 0.85 it *gains* 4.2, and at 0.85/140 it gains 6.7. A small
   plate expires having done its job; a big plate needs time to be worth
   breaking. **That interaction is why a star sweep could not have found this**
   — the best cell beats the sum of its own single-knob moves by nine points.

**AND THE THROWN-AWAY COLUMN IS NOT A WASTE METRIC.** The arm that throws away
least — dur 9.0, 98% kept — is the **worst arm in the sweep at 38.3%.** A
plate that expires unspent is a plate nobody had to break. This is v42 §3c
arriving from the other side for the third time in the project: *when a brief
becomes a number, ask what the worst thing that scores well on it looks like.*
The number this section was built to produce turned out to be the number not
to optimise.

**The best cell measured is +13.4 points over shipped.** It is NOT this
relic's to set: `STATUS.ward` is chain-wide and moves Farwarden, Lightkeeper
and Bulwarden with it. Rick's call, and it wants the per-type sweep run on all
four vigil donors before anything moves.

---

# 5. THE TRAPS, ASSERTED

- An expiring ward ZEROES the pool. **It is the only status in the game whose
  effect can be thrown away unspent.**
- The plate eats damage first and the OVERFLOW carries through, so a large hit
  is not wasted on a thin plate.
- **Every landed blow re-clocks the ward**, so the plate's life is the type's
  contact interval rather than its own duration.
- The bank runs AFTER `hurt` in `resolveHit`, so a blow never banks against
  itself.
- The blade is a rigid function of `f.theta`. No lag term, unlike the flail.
- Damage-over-time goes UNDER the ward by design, which hands the two DoT
  schools a real answer to vigil.

---

# Open decisions

1. **DOES `STATUS.ward` MOVE?** §4.3. `bank` is worth up to +13.4 points and
   the change is chain-wide across four vigil relics. Rick's, and it wants a
   per-type sweep first — the bow already carries a 2.5 patch that v43 read as
   a fix for a BOW and not for weight, and that patch was made without any of
   these numbers.
2. **NOTHING IN `tools/` HAS A CONSERVATION CHECK EXCEPT THIS ONE.** §4.2. It
   caught two independent instrument bugs in one run. Every probe that counts
   a quantity into buckets should have one, and none of them do.
3. **THE SHATTER/EXPIRY AMBIGUITY IS IN THE ENGINE, NOT JUST THE PROBE.** Both
   paths write the same three fields, so nothing outside can tell a plate that
   was broken from one that lapsed — including the director, and including
   `verify`. v41's "a kill by ward SHATTER files no beat" is the same hole seen
   from the camera's side, and it is still open.
4. **CURSE.** Deferred to next session at Rick's call; the finding and the
   probe are in the repo.

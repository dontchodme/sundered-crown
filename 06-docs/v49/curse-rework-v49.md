# v49 — THE IMPALE-SHAPED CURSE, MEASURED BEFORE IT IS BUILT. It works, it is worth about 3x what it should be at the rates first reached for, and the two ultimates it breaks are the two worst in the game.

**2026-08-31, Cowork.** Rick's design, off Path of Exile's Impale: *a Curse
stack remembers the damage of the hit that applied it; every later hit deals a
share of everything remembered; stacks cap at 3-6 and a new stack displaces
the weakest.* He asked for the balance and for a counter-proposal. This is the
balance, run on `02-chain/sc-thornshear.html` — 26 relics, shipped damage,
ultimates ON, whole roster.

New tools, runtime injection only, nothing written to any build:
`tools/echo_probe.py`, `tools/echo_probe2.py` (the corrected arms, §5),
`tools/field_and_ult.py`, `tools/ultstack_probe.py`, `tools/ult_price.py`.

---

# 0. WHAT IMPALE ACTUALLY IS, AND WHERE THIS DIVERGES

PoE: the debuff records **10% of the physical damage** of the hit that applies
it. Each later hit **from any source** deals that amount as a separate
reflected hit; all impales on a target contribute. Default cap **5**, and each
impale **lasts 5 hits or 8 seconds** — every hit against an impaled enemy
spends one hit-charge from every impale. Impale damage is reflected, so it
**cannot stun or apply on-hit effects**.

Three divergences in the design as stated, and all three make it stronger:

1. **No hit-charges.** PoE's impale is a five-shot magazine. Rick's stack pays
   out forever, so the ramp never comes back down.
2. **No expiry.** Curse's `dur` is 99 — it never falls off inside a fight.
3. **Displacement instead of decay.** "New stacks drop the weakest" is not a
   PoE rule. It means the pool converges on **the wielder's K biggest blows**,
   not its recent ones. That is a better rule than PoE's and it is where the
   interesting behaviour lives (§4, §5).

`resolveHit`'s existing order is already right for this: `dmg` is computed and
rounded, `this.hurt(foe, dmg, self)` lands it, `self.dealt += dmg` records it,
and the `onHit` loop runs ~90 lines later. So the blow's own damage is
available at the moment its stack is applied, and the echo is priced off the
stacks that existed **before** the blow — the PoE rule that a fresh impale
does not pay on its own hit — for free.

---

# 1. THE HIT BUDGET DECIDES EVERYTHING, AND NOBODY HAS EVER PUBLISHED IT

Every relic against the whole roster, shipped damage, ults on, 75 fights each:

```
relic          shape        dmg   hits/fight   p10  med  p90   dmg/hit
thornshear     twinblade   11.8         59.4    47   59   74       6.5
twinshade      twinblade    8.3         25.7    19   26   32      12.8
nightfell      greatsword  15.8         14.5    10   14   19      25.7
grudgebearer   warhammer   23.5          7.3     5    7   10      58.0
gravemourn     flail       44.1          5.6     3    6    8      65.5
```

**The roster spans 5.6 to 59.4 landed blows a fight — 10.6x.** The three
umbral relics happen to sit at three points on it: 5.6, 14.5, 25.7.

This is the number the cap has to be chosen against, and it rules out the top
of the range Rick offered. **Gravemourn lands 6 blows in a median fight and 3
in its worst tenth.** A 6-stack cap is not a cap for that relic; it is a
target it does not reach on its own blade. A 3-stack cap is filled by its
third blow — half its fight at full strength.

---

# 2. THE FIELD, WHICH IS THE ONLY YARDSTICK ANY DONOR NUMBER HAS

Every pairing, 5 seeds, 125 finished fights a relic:

```
field mean 50.0%   sd 6.4%   range 38.4%..62.4%   binomial SE 4.5% a relic

nightfell   46.4%      twinshade  44.0%      gravemourn  40.0%
```

**Umbral is the bottom school: 43.5% against a 50.0% field, so the deficit to
close is about 6.5 points.** Anything that moves a donor 20 points has not
fixed umbral, it has replaced one imbalance with a bigger one.

---

# 3. THE ARMS

Donor against 25 foes, 6 seeds, 150 fights an arm, shipped damage, ults ON.
`none` deletes curse; `bottom` is v47's proposed fix — the same 13 a stack
taken off current health instead of the ceiling.

```
donor          none   shipped   bottom    K3 r8%   K3 r15%   K5 r8%
gravemourn    41.3%     43.3%    66.7%     51.3%     54.0%    54.0%
nightfell     41.3%     43.3%    87.3%     52.0%     68.7%    61.3%
twinshade     18.0%     43.3%    84.7%     48.7%     65.3%    53.3%
```

**a. v47's own recommended fix is far more broken than v47 priced it.**
`bottom` reads +9.9pp in v47 because that table pinned damage at 24 and
suppressed ultimates. At shipped damage with ults on it is **+23 to +44
points** and puts nightfell at 87%. The v47 number was not wrong, it was
measured on a flattened field and must not be read as a shipped-game estimate.
*(The three donors landing on exactly 43.3% in the `shipped` column is a
coincidence — a second seed base gives 44.0 / 37.3 / 44.7. SE is ~4pp per
cell; the arms are paired on seed and opponent, so the differences are worth
more than the levels.)*

**b. The rates first reached for are about 3x too generous.** K3 at 15% puts
nightfell at 69%. **K3 at 8% lands all three umbral relics at 49-52%, which is
the field** (§2: mean 50.0%).

What the channel delivers, at K3 r8%:

```
donor         blows   of which shade   base dmg   echo dmg   uplift
gravemourn      5.2              0.0        312         37     12%
nightfell      13.1              0.0        308         62     20%
twinshade      24.2              9.3        310         80     26%
```

---

# 4. THE TWO-ARCHETYPE CLAIM IS HALF RIGHT, AND THE HALF THAT IS WRONG IS NOT TUNABLE

The design is meant to reward *many small hits* and *few big hits* alike. It
does not, and the reason is arithmetic rather than tuning.

With uniform damage `d`, cap `K`, rate `r` and `N` blows, total echo is
`r·d·[K(K+1)/2 + K(N−1−K)]` and base is `N·d`. **`d` cancels.** Relative
uplift is a function of blow COUNT and nothing else — it rises with `N` and
saturates at `r·K`. Measured, K3 r15%:

```
gravemourn    5.1 blows a fight   +22% damage
nightfell    12.3 blows a fight   +36%
twinshade    22.2 blows a fight   +47%
```

**Archetype 1 gets ~2.1x the relative payoff of archetype 2**, and a bigger
cap widens it. **Any proportional per-hit bonus behaves this way. There is no
rate that fixes it, and K is the only knob that narrows it — smaller is
fairer.**

What the design DOES buy archetype 2 is the pool itself. Because displacement
keeps the K biggest blows, pool size tracks hit size almost exactly:

```
pool held (K3 / K5)   gravemourn 97 / 120    nightfell 61 / 85    twinshade 36 / 50
```

**Nearly 3x.** That is a real, measured, archetype-2-favouring quantity — it is
just not what a per-hit percentage cashes. §6 is about cashing it.

---

# 5. IT BREAKS TWO ULTIMATES, NOT THREE — AND THE FIRST PASS OF THIS SECTION WAS WRONG

**CORRECTION, and the error is worth more than the paragraph it replaces.**
The first pass named Gravemourn's **Dirge**, Nightfell's **Eclipse** and a
Twinshade ultimate called **Interment**. Interment is not in the game — it was
Nevermend's v36 ult and it did not ship. Twinshade's ultimate is
**Triplicate**: `kind:"split"`, no `dmg` and no `apply`, and its own comment
says so — *"it does not damage, it does not apply, it does not reach for the
foe at all — it puts two more of this relic on the floor."*

The probe's echo was guarded on `self === donor`, so every blow landed by a
**shade** was invisible to it. Shades are real `Fighter` objects carrying
`onHit:{curse:1}`, resolved on the shade and credited to the caster afterwards
in `tickShadeHits`. They neither fed the pool nor cashed it, and what the
first pass read as "9.9 ult-applied stacks a fight remembering nothing" was
Twinshade's own daughters swinging. **Twinshade's reported −5.3pp was that
bug.** Corrected, the echo is priced on the TARGET — any blow landing on a
cursed fighter pays it and remembers its own damage, which is also PoE's rule
— and Twinshade **gains** 5.4pp instead. 9.3 of its 24.2 blows a fight are
shade blows.

**So Triplicate is the ultimate the rework helps most in the whole game:**
three bodies feeding and cashing one shared pool is exactly the fantasy, and
it needs no rewrite at all.

What genuinely breaks is the two ultimates that apply Curse from the `apply`
field. K3, rate 8%, ults on, 125 fights a donor:

```
donor        ult remembers   stacks/fight   displaced   ever paid   echo from ult   from blade
gravemourn              14            3.9         3.8         0.4               1           35
nightfell               11            3.2         3.2         0.0               0           61
```

**Every ult-applied stack is evicted before it pays.** An ultimate's stack has
no blow to remember, and whatever stands in for one is smaller than the
wielder's own blade.

## 5b. AND THE CHEAP FIX DOES NOT WORK — TWO CAPS, THREE RULES

`tools/ultstack_probe.py`, same 150 fights an arm:

```
                    what an ult-applied stack remembers
donor            ult's dmg    wielder's blade    a copy of the pool's best
K=3, rate 8%
gravemourn           51.3%              51.3%                        52.0%
nightfell            52.0%              52.0%                        54.0%
K=6, rate 5%
gravemourn           50.0%              52.0%                        52.7%
nightfell            53.3%              52.0%                        54.0%
```

**0.7 to 2.7 points, all of it inside the noise.** At K=6 the stacks finally
survive — 2.4 of 6 kept on gravemourn — and it still buys nothing.

The reason is structural and generalises past this mechanic: **a capped top-K
pool is already full.** The blade reaches the ceiling on its own in 93-100% of
fights, so a stack an ultimate adds is at best a duplicate of a value the blade
already put there. It adds pool; it adds no information.

**An ultimate cannot ADD to this pool. It can only SPEND it.**

## 5c. AND BOTH OF THEM ARE ALREADY THE WORST ULTIMATES IN THE GAME

Rick's guess, tested. `tools/ult_price.py` — every relic against the other 25,
5 seeds, then the SAME 125 fights with only that relic's `charge` set to 1e9.
Paired, so the difference is the ultimate. 6500 fights.

```
relic         ultimate        kind        with   without    worth   flips
gravemourn    Dirge           pull       42.4%     45.6%    -3.2%      50
slagheart     Ironbloom       latch      48.8%     48.8%    +0.0%      56
heartwood     Rootfast        freeze     40.0%     38.4%    +1.6%      36
farwarden     Reprisal        aimedshot  56.8%     54.4%    +2.4%      61
emberedge     Slagburst       detonate   37.6%     35.2%    +2.4%      53
lightkeeper   Bulwark         nova       52.0%     48.8%    +3.2%      48
nightfell     Eclipse         nova       42.4%     35.2%    +7.2%      49
...
censer        Consecration    nova       62.4%     37.6%   +24.8%      61
twinshade     Triplicate      split      44.8%      8.8%   +36.0%      49
lastlight     Harrowing       harrow     54.4%      4.8%   +49.6%      68

mean worth +18.9%   median +20.4%   paired SE ~5.7pp on a single relic
```

**Dirge is the only ultimate in the game with a negative point estimate** —
Gravemourn wins 3.2 points MORE with it deleted — and it is not a rarity
artifact: it fires **1.86 times a fight, first cast at 17.2s, never-cast in 0%
of fights.** Eclipse at +7.2 is 1.3 SE from zero against a +20.4 median.

So yes: **the two ultimates the rework breaks are the two worst curse-carrying
ultimates in a game whose median ultimate is worth +20 points, and one of them
is worth less than nothing.** Breaking them costs almost exactly nothing, and
a spender would be the first thing either has ever done.

**The bigger finding is that they are not alone.** Seven ultimates —
Dirge, Ironbloom, Rootfast, Reprisal, Slagburst, Bulwark, Eclipse — are
statistically indistinguishable from not existing. Five of them have nothing
to do with curse. Nothing in `tools/` had ever asked this question; it is
v47's complaint about statuses, one object class along.

---

# 6. THE COUNTER-PROPOSAL — KEEP THE ECHO, ADD A SPENDER

Two payoffs on one pool, because the pool has two properties and a per-hit
percentage only cashes one of them.

```
THE ECHO   per hit, proportional     ->  pays hit RATE      -> archetype 1
THE TOLL   per cast, absolute        ->  pays hit SIZE      -> archetype 2
```

**The echo** is Rick's mechanic at **K = 3, rate 8%**, permanent, displacement
kept. K3 because gravemourn's blade cannot fill more (§1) and because a small
cap is what narrows the archetype gap (§4).

**The toll** is the fix for §5: an umbral ultimate stops *applying* curse and
starts *spending* it — it detonates the remembered damage, at some multiple of
the pool, and empties it. That is worth 97 to gravemourn and 36 to twinshade
on the same cast, so **the ultimate is where the big slow hitter collects**,
and the pool number on the chip becomes a thing the viewer watches climb
toward a cast rather than a counter that only ever goes up.

There is precedent in the chain for both halves of the rule that makes this
safe. **Slagburst: consumed THEN priced** — a detonation whose damage is also
multiplied by the stacks it just ate pays itself twice and goes exponential.
So: the toll reads the pool, empties it, then deals; and the echo's own damage
is **never** what a stack remembers — the stack remembers the blow's base
damage or the loop compounds. Same reason PoE makes impale damage a reflected
hit that cannot apply on-hit effects.

---

# 7. THE LEGIBILITY PROBLEM, WHICH IS SMALLER THAN IT LOOKS

Rick's worry. The budget is **≤40 characters** (`verify.py` enforces it; the
arena panel fits ~42 at 25px), and the convention is an effect clause, verb
first, real numbers, "per stack".

```
"Adds 8% of a remembered blow per stack"     38    fits
"Hits echo 8% of each remembered blow"       36    fits
"Each hit re-deals 8% of a stack's blow"     38    fits
```

**But the tip is not what should teach this, and that is the actual answer.**
Every other status is a constant — 1.5/s, 11%, 0.2s — and its chip can afford
to count stacks because the stack count is the whole state. Curse's state is a
NUMBER, and the number moves. So:

- **The tag prints the REMEMBERED TOTAL, not the pending echo and not the
  stack count.** *(Corrected — the first pass said the pending echo, and
  measured that is far too small a number to watch.)*

  ```
  relic         blade   blows   pool held   peak pool   ECHO/BLOW   peak   echo/fight
  gravemourn     22.5     6.9          60         106         5.2      8           36
  nightfell      13.0    14.3          53          88         4.1      7           59
  twinshade       8.3    23.9          42          66         3.4      5           80
  ```

  **The pending echo peaks at 5 to 8 across the whole school.** A HUD number
  that tops out at 8 is not worth a viewer's attention. **The pool is** — it
  holds 42 to 60 and peaks at 66 to 106, it fills in three blows on every
  relic, and it is the number BOTH ultimates read: Gravemourn's hands carry it
  away and Nightfell's sigils are stamped with it. `CURSE 96` followed by a
  detonation for 96 is a story a viewer can follow. `CURSE 8` is not.

  There is no persistent chip in this build — the readout is the transient
  `statusTag` at the point of contact, so that is where the number goes.
- **The art has to be re-cut, because the shipped art is now a lie.** Motes
  that leave and never return said "maximum life, gone for good." Nothing
  leaves any more. Three motes that ARRIVE, orbit, brighten with what they
  hold, and flash into the impact on every blow — countable at phone size, and
  it says the mechanic rather than saying a status is present.
- **The health bar's frosted dead cap goes**, with `maxHp` untouched.

---

# 8. WHAT THIS COSTS TO SHIP

`STATUS.curse` loses `maxHpLoss` and gains a rate and a cap of 3; `Fighter`
gains a pool and `apply` loses its `maxHp` line; `resolveHit` gains the echo
before `hurt` and the remember after `dealt`; `_stCurse` and the health-bar
cap are redrawn; Dirge and Eclipse are
rewritten as spenders and lose their `apply` fields; the three umbral blurbs
and Twinshade's stated thesis ("it does not empty you — it makes you smaller")
are rewritten; `tip_audit.py`'s `FIELDS` table drops `maxHpLoss`. **Every win
rate in `verify.py` moves, and all three umbral blades were tuned under a
curse that no longer exists — they have to be re-swept.** Triplicate needs
nothing.

---

# 9. WHAT THIS INSTRUMENT CANNOT TELL YOU

- The echo is paid as a **separate `hurt()`** after the blow, not folded into
  the blow's damage number. So in these runs it does not scale hit-stop,
  knockback or hitstun, is not stopped by an Aegis wall, and rolls no crit of
  its own. A real build folds it in and all four follow — **every number here
  is a floor.**
- SE is ~4pp a cell. K3 r8% vs K5 r8% is inside the noise; K3 r8% vs K5 r15%
  is not. Do not rank settings one point apart off this table.
- Nothing here measures how the rework reads on video, which is §7's claim and
  is a filmstrip's job, not a probe's.

## How this check lied, this session

**A GUARD WROTE A FINDING.** `self === donor` looks like "the donor's blows"
and is not: `resolveHit`'s `self` is whichever BODY swung, and Twinshade puts
three bodies on the floor. The probe reported a confident, specific,
well-formatted −5.3pp and a dead ultimate that does not exist in the game.
Nothing about the output looked wrong; the roster did. **The defence is to
name the ultimate from `AC.WEAPONS` before writing a sentence about it**, and
to price a per-target effect on the TARGET rather than on an assumed attacker
— which is also the rule PoE states and the one this instrument now uses.

---

# Open decisions

1. **CAP AND RATE.** K = 3 at 8% is what the measurement supports; Rick
   floated 3-6. 6 is measurably wrong for the flail (§1) and measurably worse
   for the archetype balance (§4). Rate is the free knob once K is fixed.
2. **DIRGE AND ECLIPSE BECOME SPENDERS, OR THEY STAY DEAD.** §5b closed the
   "add better stacks" option by measurement, and §5c says the cost of
   breaking them is near zero — Dirge is worth −3.2 points and Eclipse +7.2
   against a +20.4 median. What is still open is the spend multiple and
   whether a spender empties the pool or leaves a floor. **Triplicate is not
   in this decision** and should not be touched.
3. **DOES THE POOL EXPIRE?** `dur` is 99 today, so a fight-long memory is the
   default and it is what makes umbral a late-game school. PoE expires impales
   in 8 seconds or 5 hits. Permanence is stronger, simpler, and more in
   keeping with the school's name; it also makes long fights snowball, which
   is untested.
4. **WHAT DOES A STACK REMEMBER — BASE OR FINAL DAMAGE?** Post-crit is the
   interesting answer (a crit parks a big memory and displacement keeps it),
   post-echo is the exponential one and must never ship.
5. **ALL THREE UMBRAL BLADES.** 44.10 / 15.83 / 8.30 were swept under the
   shipped curse. None of them is a valid number under any of this, and
   Twinshade's is the least valid — its ultimate now multiplies a channel that
   works.
6. **THE OTHER FIVE DEAD ULTIMATES.** §5c: Ironbloom, Rootfast, Reprisal,
   Slagburst and Bulwark are indistinguishable from not existing and have
   nothing to do with curse. That is a bigger backlog than this rework and it
   is the first time anything has measured it.

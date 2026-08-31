# v47 — CURSE DELIVERS 3% OF WHAT IT SAYS. Three shipped relics have carried a dead channel since the roster was built.

**2026-08-31, Cowork.** Found while pricing cells for the 27th relic. Rick,
looking at umbral topping the occupancy column and sitting at zero by
delivered effect: *"explain what needs to be fixed about umbral?"* This is
that, measured.

`tools/curse_probe.py`, five donors, one per umbral type plus the two thin
types its open cells sit on, whole roster, ultimates suppressed, damage pinned.

---

# 1. THE NUMBERS

```
donor         type          stacks landed  nominal hp  ACTUALLY TAKEN  wasted  kept
gravemourn    flail                   5.4          70               2      67    3%
nightfell     greatsword              7.8         101               2     100    2%
twinshade     twinblade               7.7         100               2      99    2%
thornwake     scythe                  6.2          80               2      78    3%
grudgebearer  warhammer               6.3          82               3      80    3%
```

**Curse strips seventy to a hundred points off a 400 hp ceiling over a fight
and removes two or three points of health doing it.**

---

# 2. THE MECHANISM, AND IT IS STRUCTURAL RATHER THAN A TUNING MISS

```js
apply(key, n){
  ...
  if (key === "curse") this.maxHp = Math.max(60, this.maxHp - def.maxHpLoss * n);
}

// tickStatus, last line
f.hp = Math.min(f.hp, f.maxHp);
```

`apply` lowers the CEILING. The only thing that turns a lower ceiling into
lost health is that clamp, and **the clamp fires only where the bar is above
the ceiling.**

```
donor           applications  mean hp% at apply  landed above 50%  landed below 25%
gravemourn              1029                79%               93%                0%
nightfell               1499                77%               92%                0%
twinshade               1484                76%               92%                1%
thornwake               1183                79%               93%                1%
grudgebearer            1214                78%               92%                1%
```

**The bar sits at 79% of its own ceiling when a stack lands**, so dropping the
ceiling by 13 takes nothing at all. The ceiling would have to fall more than
84 points in one step to reach the bar, and it falls 13 at a time while the
bar keeps falling faster.

**AND THE ORDER IN `resolveHit` MAKES IT UNAVOIDABLE.** `this.hurt(foe, dmg,
self)` runs first; `foe.apply(k, n)` runs about five thousand characters
later, at the bottom of the same function. **You cannot apply a curse stack
without first landing the blow that puts the bar below the ceiling** — and
every blow after that widens the gap. The channel defeats itself by
construction, and it does so more thoroughly the better the relic carrying it
is doing.

---

# 3. IT DOES ONE THING, AND NOBODY HAS EVER COUNTED IT

`get desperate(){ return this.hp / this.maxHp <= CONFIG.desperation.at; }`
and `desperation: { at: 0.25, dmg: 1.35, spin: 1.30 }`.

Curse lowers the DENOMINATOR, so a cursed foe crosses that line later in
absolute health and spends less of the fight buffed:

```
donor            foe desperate, no curse    with curse    change
gravemourn                          2.5%          1.3%     -1.1%
nightfell                          11.3%          7.5%     -3.7%
twinshade                          10.0%          6.4%     -3.6%
thornwake                           3.5%          2.0%     -1.5%
grudgebearer                        4.8%          2.9%     -1.9%
```

**Real, never counted, and not enough to save the channel.** It is also the
only reason curse's delivered effect is positive at all rather than zero.

---

# 4. THE FIX, PRICED

The identical nominal amount taken off the BOTTOM of the bar instead of the
top — same applier, same rate, same stacks, same everything else:

```
donor           no channel   curse as shipped    lift   same hp as damage    lift
gravemourn            6.2%               4.7%   -1.6%               13.0%   +6.8%
nightfell            63.0%              69.3%   +6.2%               77.1%  +14.1%
twinshade            62.5%              63.0%   +0.5%               72.9%  +10.4%
thornwake            16.1%              16.7%   +0.5%               25.0%   +8.9%
grudgebearer         19.3%              19.3%   +0.0%               28.6%   +9.4%

                                        +1.1%                              +9.9%
```

**8.6x, on the same applications.**

---

# 5. WHY NO TOOL HAS EVER CAUGHT IT

- **`cell_survey`'s occupancy column ranks curse FIRST on every row it appears
  on** — 65-81% of the fight at two or more stacks, 89-91% refresh. Curse has
  a 99-second duration, so occupancy measures "has been hit twice by now" and
  nothing else. It is the loudest possible signal for the deadest possible
  channel, and it is the reason this survived four sessions of cell surveys.
- **`tip_audit.py` checks a tip against its own data fields.** Curse's tip
  says *"Permanently takes 13 max hp per stack"* and the field is
  `maxHpLoss: 13`. **The tip is accurate.** It just describes a ceiling, and
  every reader has taken it to describe health.
- **`verify.py` has no check that a status delivers anything.** Nothing in the
  repo compares nominal effect to delivered effect for any status, which is
  the general form of this defect and applies to all eight.

---

# 6. WHAT IT IS NOT

It is not a picture fault (v42's silent ultimate, v43's stuck hold) — there is
nothing to see. It is not a dead knob (`shot.life`, `tickFire`'s mode gate) —
the code all runs and the field is read. **It is a THIRD class: a mechanic
that executes correctly, is measured by its own tools as working, and whose
effect is cancelled by an interaction nobody modelled.** Naming it matters
because the defence is different: not a rendered check, not a grep for
readers, but **an A/B of every status against its own deletion**, which is
exactly what `row_price.py` now does for cells and nothing does for statuses.

---

# Open decisions

1. **DOES CURSE GET FIXED, AND HOW?** Chain-wide — three shipped relics
   (Gravemourn, Nightfell, Twinshade) and every win rate in `verify`. Rick's
   call, and there are at least three shapes: current-health damage of the
   same size; keeping the ceiling mechanic but applying the stack BEFORE the
   blow that carries it; or leaving the ceiling and adding a second term.
2. **EVERY OTHER STATUS WANTS THE SAME A/B.** §5. Nothing in `tools/` has ever
   asked whether a status delivers what it nominally delivers; curse is the one
   where the gap is 97%, and nobody knows the number for the other seven.
3. **`cell_survey` SHOULD NOT PRINT AN OCCUPANCY RANKING IT CANNOT SUPPORT.**
   Fifth row it has now mispriced. `row_price.py` is the replacement column and
   is not yet wired into it.

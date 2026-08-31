# v50 — DIRGE AND ECLIPSE, REBUILT ON THE POOL. Gravemourn has exactly one shape available to it; Nightfell has three, and that is the reason the two ultimates should not be the same one.

**2026-08-31, Cowork.** v49 §5c: Dirge is worth **−3.2 points** and Eclipse
**+7.2** against a field median of **+20.4**, and both apply a Curse that the
rework deletes. Rick: *"lets rebuild the purple ults my rework broke."* This is
the design, priced.

`tools/umbral_ult_lab.py`, runtime injection only, nothing written to any
build. Base curse in every arm is the v49 recommendation — **K=3, echo 8%,
permanent, displacement kept, priced on the target** so shade blows count.

---

# 1. WHAT THE REBUILD IS ALLOWED TO KEEP

Both ultimates resolve through **one shared, generic path** in `fireUlt`: a
radius test, then `knock`, `freeze`, `heal`, `dmg` and `apply` in order.
`kind:"pull"` adds a 620 impulse toward the caster before it; `kind:"nova"`
adds nothing. **The art is dispatched per relic ID, not per kind** — four
relics share `kind:"nova"` and the file's own comment says not one of them may
share a picture.

**So the set-pieces, the radii, the charges and the pictures all stand.** The
rebuild changes a payload, not a kind. That is the cheapest possible shape for
this work and it is why `apply:{curse:3}` — one field, on two relics — is the
whole of what has to go.

---

# 2. THE CONTROL, AND WHY THE WIN COLUMN IS NOT THE DESIGN COLUMN

`strip` is each ultimate with its damage, its knock and its picture intact and
**only** its worthless `apply:{curse:3}` removed. Every other arm is `strip`
plus one payload, so the **worth** column reads as what the rebuild buys.

The **win** column will be re-swept away. All three umbral blades were tuned
under a curse that no longer exists, so the tuner absorbs the level; what it
cannot absorb is the SHAPE. Read `worth` against the field median of +20.4%.

---

# 3. THE TABLE

150 fights an arm, 25 foes x 6 seeds, ults ON, shipped damage.

```
GRAVEMOURN — flail, 44.1 blade, 5.6 blows a fight, pool 104, 1.7 casts
arm                win   worth   pool at cast   spend dmg   echo dmg   blade dmg
strip            50.7%   +0.0%              0           0         36         311
det x0.6         63.3%  +12.7%            105          97         15         271
det x1.0         76.0%  +25.3%            104         151         13         249
det x1.5         80.0%  +29.3%            103         214         13         221
keepbest x1.0    81.3%  +30.7%            113         168         19         241
deepen +2        54.0%   +3.3%              0           0         41         311
deepen +3        54.0%   +3.3%              0           0         41         311
amplify x2/8s    54.0%   +3.3%              0           0         49         310
mirror           53.3%   +2.7%              0           0         43         311

NIGHTFELL — greatsword, 15.8 blade, 14.5 blows a fight, pool 59, 2.3 casts
arm                win   worth   pool at cast   spend dmg   echo dmg   blade dmg
strip            52.0%   +0.0%              0           0         61         308
det x0.6         66.0%  +14.0%             60          80         32         284
det x1.0         78.0%  +26.0%             59         131         28         250
det x1.5         86.0%  +34.0%             58         184         24         221
keepbest x1.0    79.3%  +27.3%             61         136         37         242
deepen +2        62.0%  +10.0%              0           0         88         293
deepen +3        65.3%  +13.3%              0           0         94         289
amplify x2/8s    60.7%   +8.7%              0           0         83         296
mirror           56.7%   +4.7%              0           0         68         305
```

---

# 4. THE HEADLINE, AND IT IS NOT THE ONE THIS SESSION EXPECTED

**GRAVEMOURN HAS ONE SHAPE.** Every payload that leaves the pool in place —
deepen, amplify, mirror — is worth **+2.7 to +3.3 points**, which is the dead
band Dirge is already in. Give Gravemourn a deeper pool and it has 5.6 blows a
fight to fill it with and cash it with; the extra slots are still empty when
the fight ends. **The flail's ultimate must SPEND, or it is Dirge again under
a new name.**

**NIGHTFELL HAS THREE.** The same amplify family is worth +8.7 to +13.3 to it
— three to four times what it is worth to the flail — because Nightfell lands
**2.6x the blows** and a deeper pool is a thing it has the contacts to exploit.
That is §1 of v49 showing up as a design constraint rather than a table.

**And the split this session predicted was half wrong.** Detonation is the
strongest arm on BOTH relics (+25.3 / +26.0 at x1.0), and it is *better* on
Nightfell despite Nightfell holding a pool 44% smaller — 2.3 casts against 1.7,
and a flail already dealing 311 blade damage has less room for another 150.
**If the choice were made on the win column alone, both relics would detonate
and the school would have two of the same ultimate.**

`roster-expansion` §5.8's rule is the one that decides it: *a relic that wants
a mechanic another relic already owns is either the wrong relic or the
taxonomy is wrong.* One pool, two verbs:

```
GRAVEMOURN   SPENDS the memory   lump sum, biggest pool, fewest blows   +25.3%
NIGHTFELL    DEEPENS the memory  a rate, most blows, most casts         +13.3%
```

+13.3 is not a weak ultimate. It sits with Bloodhunt (+10.4), Exsanguinate
(+12.0) and Quarrelstorm (+13.6), all shipped.

---

# 5. THE TWO PAYLOADS, WRITTEN OUT

**GRAVEMOURN.** `kind:"pull"` stands, radius 320 stands, charge 16 stands, the
620 impulse stands, `dmg:14` stands. `apply:{curse:3}` is deleted and replaced
by a spend: **read the pool, empty it, then deal `M x pool`.**

Consumed THEN priced, per Slagburst — a spend whose damage is also multiplied
by the stacks it just ate pays itself twice and goes exponential. Routed
through `hurt()`, so a ward eats it like anything else.

```
M = 1.0    +25.3%, one point above the field median. The recommendation.
M = 0.6    +12.7%  a second-tier ultimate
M = 1.5    +29.3%  and 214 damage a fight through one channel
keepbest   +30.7%  the spend leaves the largest entry standing, so the echo
                   survives the cast (19 against 13). Better number, softer
                   picture: the memory is spent DOWN rather than emptied.
```

**NIGHTFELL.** `kind:"nova"` stands, radius 250, charge 15, `dmg:11`,
`knock:150` all stand. `apply:{curse:3}` is deleted and replaced by:
**the target's Curse cap rises by 3, permanently, for the rest of the fight.**

3 to 6 to 9. Nothing is added — the relic's own blade fills the new slots
within a few blows, which is the one thing v49 §5b proved a full pool has room
for. The echo goes from 61 to 94 damage a fight and the blade barely moves.

---

# 6. THE TUNING HAZARD THIS CREATES, AND IT IS NEW

**`dmg` now moves three channels at once.** The pool is made of blade damage,
the echo is a share of the pool, and the spend is a multiple of it. Halve
Gravemourn's blade and the blade damage halves, the pool halves, the echo
halves and the detonation halves — **the spend channel is quadratic in
`dmg`.** At `det x1.0` the spend is already 37% of Gravemourn's total output.

Every previous relic in this game had a blade the tuner could move without
touching the ultimate. These two do not. `tune.py` will find a fixed point,
but it is a different surface and a sweep that assumes monotonic, linear
response will land in the wrong place. **Sweep wide and plot it before
trusting a single pass.**

---

# 7. TIPS AND NAMES

Ult tips are ≤72 characters, full sentences, name > effect with numbers.

```
GRAVEMOURN
  "Reels the target in, then spends every blow Curse remembers"      59
  "Drags the target in and collects everything Curse remembers"      59
  "Pulls the target in, then deals all remembered Curse damage"      59
NIGHTFELL
  "Nova: 11 damage — Curse remembers 3 more blows, permanently"      59
  "Nova: 11 damage, knockback, and Curse remembers 3 more blows"     60
```

Names — Dirge and Eclipse are both still *available* rather than obviously
wrong. Dirge is a lament and this is a reckoning; Eclipse is literally the
dark deepening, which is now exactly what it does.

```
GRAVEMOURN   The Tolling · Arrears · Requiem · Exhumation · keep Dirge
NIGHTFELL    keep Eclipse · Umbra · Longnight · The Deepening
```

---

# 8. WHAT THIS INSTRUMENT CANNOT TELL YOU

- Every arm is a **payload** change on the existing resolution path. Nothing
  here draws anything, and both set-pieces will need a filmstrip before
  anyone claims the spend reads on screen.
- SE is ~4pp a cell; the arms are paired on seed and opponent, so the `worth`
  column is worth more than the `win` column. `det x1.0` vs `keepbest x1.0`
  (25.3 vs 30.7) is about 1 SE apart and should not be ranked off this table
  alone.
- The blades are the shipped ones. Every number here moves when they are
  re-swept, and §6 says that sweep is not the usual one.

---

# Open decisions

1. **NIGHTFELL: DEEPEN, OR DETONATE TOO?** Detonation is worth twice as much
   (+26.0 against +13.3) and makes the school's two ultimates the same
   ultimate. Deepening is differentiated, mid-table, and is the only shape
   Gravemourn cannot have. Rick's call — this is a taxonomy decision, not a
   balance one.
2. **DOES THE SPEND EMPTY THE POOL, OR LEAVE ITS LARGEST ENTRY?** Emptying is
   cleaner to draw and to say. Keeping the largest is worth ~5 points more and
   keeps the echo alive after the cast.
3. **THE MULTIPLE.** x1.0 lands on the field median. x1.5 is a 214-damage
   channel and a genuine finisher; x0.6 is a second-tier ultimate.
4. **NAMES.** §7.
5. **DOES DEEPENING STACK WITHOUT LIMIT?** 3 to 6 to 9 to 12 over a long
   fight, and nothing in the measurement ran long enough to find where that
   stops being interesting. A hard ceiling of 9 is one line and is untested.

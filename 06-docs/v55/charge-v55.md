# v55b — CHARGE IS UNPRICED. Twenty-seven relics span 13 to 18 seconds against ultimates worth -1.9% to +48.1%, correlation +0.17 — and charge is the strongest single knob on the sheet, worth 3 to 5 points of win rate a second. Slagheart pays the second-longest charge in the game for the only ultimate that is worth less than nothing.

**2026-08-31, Cowork.** `tools/ult_price.py` and a charge sweep, against
`02-chain/sc-nightfell.html`. Runtime only. Written because Rick asked how
charge times are decided, before writing the 29th relic's §1.

---

# 1. HOW IT WORKS, AND IT IS ONE LINE

```js
f.charge += dt;
if (f.charge >= f.w.ult.charge){ f.charge = 0; this.fireUlt(f, foe); }
```

Pure wall time. No contribution from damage dealt, damage taken, hits landed,
distance travelled or status applied. `w.ult.charge` is a per-relic number of
seconds and nothing else reads it.

Three relics gate the REBUILD rather than the threshold — the Crucible,
Ironbloom and the bow window return early while their own window burns, so the
clock is owed from the resolution rather than from the cast. Daybreak
deliberately does not (`"the window IS the payoff, and the next ult is owed
from the cast like any other"`). That is the whole of the mechanism.

---

# 2. THERE IS NO RULE BY SCHOOL AND NONE BY TYPE

```
                 bow   flail  greatsword  scythe  twinblade  warhammer   school mean
bloodsworn        15      16          14       ·         14          ·          14.8
dwarven           15      17          14       ·          ·         18          16.0
runic              ·      16          13      15         13          ·          14.2
sanctified        14       ·          14      15          ·         15          14.5
umbral             ·      16          15       ·         18          ·          16.3
verdant           15       ·          15      15         16          ·          15.2
vigil             16       ·          15      16          ·         16          15.8
type mean       15.0    16.2        14.3    15.2       15.2       16.3

range 13-18   mean 15.2   sd 1.23   n = 27
total variance 40.7 — SCHOOL explains 14.0 (34%), TYPE explains 14.3 (35%)
```

Both "explanations" come from seven and six groups fitted to 27 points over a
five-second spread; neither survives being called a rule. The honest
description of the table is **"about fifteen, with drift."**

---

# 3. AND IT IS NOT SET BY WHAT THE ULTIMATE IS WORTH

Every ultimate A/B'd against its own deletion, paired on seed and opponent,
150 fights an arm, at each relic's shipped blade:

```
worth      relic          ultimate         charge        worth    relic         charge
-1.9%      slagheart      Ironbloom            17       +25.0%    nightfell         15
+0.6%      lightkeeper    Bulwark              15       +25.0%    vesper            16
+0.6%      heartwood      Rootfast             15       +25.6%    paradox           16
+6.4%      farwarden      Reprisal             16       +26.9%    vinesower         15
+6.4%      emberedge      Slagburst            14       +27.6%    grudgebearer      18
+8.3%      widowmaker     Exsanguinate         14       +31.4%    redflail          16
+12.8%     censer         Consecration         15       +34.0%    dawnbringer       14
+12.8%     marrowdraw     Bloodhunt            15       +35.3%    gravemourn        16
+14.7%     thornwake      Bramblesnare         15       +36.5%    foregone          15
+16.7%     bulwarden      Aegis                16       +47.4%    twinshade         18
+17.9%     ironhail       Quarrelstorm         15       +48.1%    lastlight         15
+19.2%     thornshear     The Winnowing        16
+21.2%     spellbreaker   Unmaking             13       mean +21.0%   median +21.8%
+21.8%     aureole        Benediction          14       paired SE ~5.3% a relic
+21.8%     oathwound      Bloodprice           14
+23.7%     axiom          Corollary            13
```

**Pearson r between charge and worth = +0.17.** Lastlight's Harrowing is the
most valuable ultimate in the game at a dead-average 15. Slagheart's Ironbloom
is the only negative one at 17.

A caveat that matters: `worth` is measured at the SHIPPED blade, so a relic
whose blade was bisected to make room for a big ultimate reads as more
ult-dependent — correctly. That is what "how much of this relic lives in its
ultimate" means, and it is the quantity charge should be priced against.

---

# 4. WHICH WOULD BE FINE IF CHARGE WERE A WEAK KNOB. IT IS THE STRONGEST ONE.

Charge swept on four relics spanning the worth range, 26 foes x 5 seeds a
point, `OFF` = charge 1e9:

```
charge            8      11      15      20      28      42     OFF    worth (§3)
lastlight     83.8%   63.1%   50.8%   33.1%   20.0%   16.2%    5.4%       +48.1%
gravemourn    82.3%   70.8%   57.7%   53.1%   40.0%   19.2%   12.3%       +35.3%
grudgebearer  70.8%   53.8%   50.8%   43.8%   47.7%   33.1%   23.8%       +27.6%
slagheart     59.2%   63.1%   46.9%   53.8%   51.5%   52.3%   50.8%        -1.9%

casts a fight  ~3.0-4.0  ~2.1-3.0  ~1.6-2.1  ~1.1-1.6  ~0.8-1.0  ~0.3-0.5
fights that
ever cast        100%     100%     ~99%     ~98%    79-95%    28-52%
```

**Three to five points of win rate per second of charge in the 8-15 band**, for
an ultimate worth having. That is more leverage than any blade bisection in
the chain's history has needed. Slagheart's row is flat because there is
nothing on the other end of the lever.

**And a v51 claim is now stale.** The Gravemourn brief (§3.2) recorded *"charge
is NOT a balance lever here: at 42 the ult fires in a quarter of fights and the
relic still wins 61.5%."* That was measured at blade 44.10, before stage 2b
bisected it to 24.03. At the shipped blade, charge 42 puts Gravemourn on
**19.2%**. Charge's leverage is not a property of the relic; it is a property
of **how much of the relic's win rate lives in its ultimate**, and bisecting a
blade transfers exactly that.

---

# 5. THE SECOND THING CHARGE DECIDES, AND NOBODY HAS EVER PRICED IT

```
charge   casts a fight   fights that never see the ultimate
    15        1.6 - 2.1                                  0%
    20        1.1 - 1.6                              1 - 4%
    28        0.8 - 1.0                             5 - 21%
    42        0.3 - 0.5                            48 - 72%
```

Every ultimate in this game is a **set-piece built to be filmed**. At 42 the
majority of clips cut from a match would contain no ultimate at all. That is a
shorts problem before it is a balance problem, and it is not represented
anywhere in the pipeline — `shorts_build.py` and `cinema_clip.py` both select
on beats, so a fight with no cast simply yields a duller clip and nothing
reports it.

---

# 6. WHAT THIS DOES NOT SAY

- The sweep is four relics, not 27. The shape (steep for a valuable ult, flat
  for a worthless one) is consistent across all four and the mechanism is
  obvious, but the per-second figure is not established for the other 23.
- `worth` and the sweep are both measured against the whole roster with every
  other relic's ultimate LIVE. A roster-wide charge change would move the
  field it is measured against.
- Nothing here says 15 is wrong. It says 15 was not derived, and that two
  relics sit visibly off the line it should have been derived from.

---

# Open decisions

1. **SLAGHEART.** Ironbloom is worth -1.9% at charge 17 — the only ultimate in
   the game that a relic is better off without, carrying the second-longest
   charge. Three ways out and they are not the same size: cut the charge (a
   ~4-point move at best, given the flat sweep), rework the ultimate, or
   accept it and move the value into the blade. This is a relic-level decision
   and it is Rick's.

2. **PRICE CHARGE ONCE, CHAIN-WIDE.** The natural rule is that charge should
   pay for `worth`: an ultimate worth +48% should not cost the same as one
   worth +0.6%. Deriving the curve is one sweep across all 27 and it would
   move several relics. It is also the largest single rebalance the chain has
   ever attempted and it would invalidate every blade bisection at once, so it
   wants its own version, not a corner of a fighter build.

3. **THE 29TH RELIC'S CHARGE.** Not blocked by either of the above. The
   default is 15-16 and this cell's donor sits at 18. The umbral warhammer's
   first cast arrives with the fullest pool in the school (v55 §5), and charge
   is what buys that — a longer charge is not only a cost here, it is what
   makes the ultimate hit harder. That trade has never been available before
   and it should be swept rather than defaulted.

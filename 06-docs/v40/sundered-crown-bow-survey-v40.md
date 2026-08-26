# v40 — THE LOOK AT FOUR BOW CELLS, and a type whose thesis had never been tested

**2026-08-20.** Rick: *"alright lets build another one. how about a bow this
time?"* → the type is chosen, the school is not, and the survey ran before the
choice. Same discipline as v39, pointed at one row instead of the whole grid.

```
tools/bow_survey.py        NEW   25/25   — 4 open bow cells, deep
05-reference/v40/bow-survey.txt         — the run
05-reference/v40/bow-survey.json        — the numbers
NOTHING WAS BUILT. Injection is runtime-only; no build was written to.
```

v39's `cell_survey` is the right instrument for *which type* and the wrong one
for *which school on this type*. It scored the bow row on stack occupancy, and
occupancy on this type turns out to be almost uncorrelated with delivered
effect: the school it ranks highest delivers **exactly zero**.

---

# 1. THE ROW

Four cells open. Twenty-one relics, three of them bows, and all three share one
`shot` block byte for byte — **the shot is a property of the TYPE**, which is
why this document can talk about "a bow" at all.

```
                bow      flail  greatsword   scythe   twinblade  warhammer  school
bloodsworn        ·   Threshmaw   Goreshard        ·  Widowmaker         ·     3/6
dwarven    Ironhail   Slagheart   Emberedge        ·           ·  Grudgeb.     4/6
runic             ·           ·       Axiom Foregone   Spellbr.         ·     3/6
sanctified  Aureole           ·  Dawnbringer Lastlight        ·     Censer     4/6
umbral            ·  Gravemourn   Nightfell        ·   Twinshade         ·     3/6
verdant           ·           ·   Heartwood Thornwake        ·          ·     2/6
vigil     Farwarden           ·  Lightkeeper        ·          ·         ·     2/6
```

**Verdant is the thinnest school in the game that has a channel at all.** Vigil
is also at two and has no `onHit` channel (v39 §2), so verdant is the only
2/6 cell here where a status design is even available.

---

# 2. WHAT A BOW ACTUALLY DOES, AND NOBODY HAD LOOKED

The bow is the only `mode:"ranged"` type, it has the **shortest reach in the
game** (54), and v39 measured it as having the **highest contact rate** in the
game. Nothing in the tree explains how both are true. Decomposed, over every
non-bow foe, ults suppressed, damage not pinned:

```
bow           hits/s   arrow   stick  dmg arrow  landed  parried   wall  spent   sep
Ironhail       0.271     64%     36%        62%    7.7%     9.6%  82.2%   0.0%   203
Farwarden      0.282     61%     39%        59%    8.0%     9.9%  81.8%   0.0%   189
Aureole        0.278     63%     37%        61%    7.7%     9.8%  81.9%   0.0%   202
```

**A bow lands 7.7% of what it fires.** 92,422 arrows, every one accounted for:
landed + parried + wall + spent + evicted + in flight, zero unexplained, zero
classified by a sink the probe did not know about.

**82% of every arrow ever loosed ends on a wall.** `spent` is 0.0% because a
shot travels 380 × 3.4 = 1292 units in its life and no wall is that far away —
the life cap has never once fired in this game.

## 2.1 So the wall is the type's real constraint, and it is not close

Anything that moves the landed rate is worth roughly ten times anything that
moves what an arrow does when it lands. §6 puts a number on that: driving the
parry to nearly zero — five stacks of hex, foe stunned 86% of the fight —
converts **+3.1%** into landed. The other 82% was never the parry's to give.

## 2.2 The parry is real, and it belongs to the FOE

`tickShots` bats a shot out of the air on any blade segment it touches, and
`segs` is empty while that fighter is stunned. Damage pinned and every channel
deleted, so two relics of one shape are the same weapon:

```
foe shape      reach width  spin blades   parried  landed   wall
twinblade         62     8   5.7      2     12.0%    5.8%  81.8%
greatsword       116    14   3.4      1     11.0%    8.6%  80.0%
flail             96    22   2.2      1      7.2%   10.3%  81.5%
scythe           104    11   3.2      1      6.2%    7.9%  85.9%
warhammer         76    26   1.6      1      5.9%   10.7%  83.4%
```

Every relic of one shape parries **identically** — which is the correct answer
and is asserted as a check, because a difference would be a per-relic field
reaching the shot path that nothing in the tree documents.

A twinblade eats twice the arrows a warhammer does. **A bow's matchup spread is
a property of the other weapon's geometry and the roster has never priced it.**

## 2.3 THE TYPE'S OWN THESIS IS TRUE, and this is the first time it was tested

Ironhail's comment has claimed since it was written: *"hits from anywhere, dies
up close — and the collapsing hall turns that into an arc for free."* Binned by
time, a bin counting only matches still running at the end of it:

```
bin        matches  fired  landed  parried   wall  melee/s  shot dmg    sep  inset
0-10s           54   1330    7.1%     9.8%  78.0%    0.065       71%    252      0
10-20s          54   1326    8.8%     9.8%  82.9%    0.117       68%    205      5
20-30s          54   1240    7.3%     8.6%  83.9%    0.093       64%    183     38
30-40s          54    976   10.6%     6.9%  84.4%    0.138       67%    164     75
40-50s          39    254   11.8%    12.6%  80.3%    0.251       44%    148    102
```

**The arrow carries 71% of the damage in the opening and 44% at the end.** The
melee rate quadruples, 0.065 → 0.251. Separation halves, 252 → 148. The arc is
real, it is large, and it is free — the hall does it, not the relic.

A bow is two weapons in sequence, and **which one a relic's ultimate should
serve is now a question with a number attached** rather than a matter of taste.

---

# 3. THE ART

Palette held, only `p.key` varies — v39's rule, learned when an alpha mask
reported the dwarven bow had no art and was flatly wrong. Controls: the render
is deterministic to 0.0e+00, a nonsense key differs from the nearest real
school by 14.6%, and no bow is measured clipped in either draw state.

```
open cell         nearest sibling    diff  inkIoU   ink px   rank on the type
bloodsworn x bow  dwarven           43.4%   0.739    82779   closest pair #5 of 21
runic x bow       dwarven           41.7%   0.723    50510   closest pair #4 of 21
umbral x bow      dwarven           54.5%   0.537    47251   closest pair #10 of 21
verdant x bow     dwarven           37.6%   0.830    73738   closest pair #2 of 21
```

All four have real art and it is written, not stubbed: barbs and tip-hooks
(bloodsworn), limbs cut into five pieces held by the string alone (runic), both
tips eaten off (umbral), a living branch that leafs with a vine for a string
(verdant).

**Every one is nearest to dwarven and that is not four coincidences.** The
dwarven branch is the smallest ornament on the shape, so it sits closest to the
bare recurve all seven share. This column reads *how much the branch adds*. It
is not a confusability score — at arena size two relics collide by PALETTE, and
that is a count:

```
open cell         same-school relics it would stand beside     mirror pairs
bloodsworn x bow  Widowmaker, Goreshard, Threshmaw                        3
runic x bow       Spellbreaker, Axiom, Foregone                           3
umbral x bow      Gravemourn, Nightfell, Twinshade                        3
verdant x bow     Thornwake, Heartwood                                    2
```

v39 open decision 3 ruled runic out of its own marquee fight for exactly this.
**Verdant is the only one of the four that can carry a marquee fight against
its own school.**

---

# 4. THE FOUR CLOCKS, AS DELIVERED EFFECT

Each school's channel carried on Ironhail's body, damage pinned 14.0, ults
suppressed, 20 seeds. `net` is a **paired 20-second window** against the same
weapon with the channel deleted, with a 95% error bar — see §4.2 for why both.

```
   school x bow        status       hits/s  mean   >=2   cap  hp@20s  net (95%)   net%   dTtk
-> bloodsworn x bow    hemorrhage    0.291  1.87   57%   37%     140     +46±12    49%    -5s
-> runic x bow         hex           0.321  1.17   31%    6%      95      +2±11     2%    -0s
-> umbral x bow        curse         0.306  4.62   78%   31%      94       +0±0     0%    -0s
-> verdant x bow       entangle      0.306  1.72   53%   33%      97      +3±11     3%    +0s
   dwarven x bow       sunder        0.294  2.17   51%   14%     114     +22±10    23%    -6s
   sanctified x bow    smite         0.298  1.31   37%   14%     126     +32±13    34%    -5s
   vigil x bow         — no onHit channel —
```

```
-> bloodsworn   dot 2.73 hp/s. Costs the archer +14±9 damage taken — the only
                channel besides smite that does.
-> runic        0.86 locks/s. Foe's weapon shut 30.4% vs 14.1% = +16.3%. Worth
                nothing in damage and the entire value is DENIAL.
-> umbral       156 max hp eaten a fight, cap in 86% of them — and +0 delivered.
-> verdant      foe spin -22.4%, move -10.3% time-weighted. Foe parries 8.9%
                against 8.9% without: the mechanism does not exist. See §5.
```

## 4.1 CURSE DELIVERS ZERO, AND THE OCCUPANCY TABLE SAYS IT IS THE BEST SCHOOL

v39's `cell_survey` ranks umbral 66-81% on every type, "immune to the type axis
entirely", top of the table everywhere. On the bow it delivers **+0±0**: not
small, not noisy, *identical to baseline in every column*.

`apply` subtracts `maxHpLoss` per APPLICATION — not per stack gained, and not
capped by `maxStacks` — and `hp` only follows when `maxHp` is driven under it.
So what curse delivers is **13 against the weapon's own damage per hit**:

```
  dmg/hit  13 : dmg  maxhp eaten   hp@20s   base    net    ttk   base   dTtk
      8.0      1.62          198       75     54    +22    51s    54s    -3s
     14.0      0.93          156       94     94     +0    39s    40s    -0s
     20.0      0.65          119      125    128     -3    32s    32s    -1s
     28.0      0.46           98      166    165     +2    25s    26s    -0s
    16.2*      0.80          142      115    116     -2    36s    34s    +1s     * unpinned
```

**The pin that makes every other row in this project comparable is the one
number curse's row is entirely about.** Below ~13 damage a hit, curse is a
second weapon; above it, curse is decoration. Ironhail hits for 16.23.

That is not a bow finding. It is a **`cell_survey` finding**, and umbral's row
on all six types is suspect until somebody re-measures it as delivered effect.

## 4.2 A RETRACTION THIS SECTION HAD TO MAKE

The first cut of the defensive ledger ran at 5 seeds and reported that **all
five** live arms cost the archer 12-23 more damage taken, and it read as a law
about carrying any offensive channel on a bow. At 20 seeds it is hemorrhage and
smite alone; hex, entangle and sunder all fall inside the error bar.

```
   school x bow         took@20s   base  extra (95%)
-> bloodsworn x bow           91     77        +14±9
-> runic x bow                79     77        +2±10   inside the error bar
-> umbral x bow               77     77         +0±0   inside the error bar
-> verdant x bow              78     77        +1±11   inside the error bar
   sanctified x bow           90     77        +14±9
```

The error bar is printed now, on every paired difference, for exactly that
reason. **Curse is the control that makes the table readable at all** — it
moves no column to the digit, so movement in the other rows is the channel and
not the seed. What the two dot channels do to contact is *not established here*
and is left as an open question rather than a story.

## 4.3 THE WINDOW, AND ANOTHER REFUTED GUESS

`hp/s over a whole fight` was the natural column and it is wrong. The first
explanation offered for that — contact is BACK-LOADED because the hall
collapses — was measured and is dead: 2.6 / 3.0 / 2.9 hits in the first three
ten-second bins, flat.

The real reason is a **ceiling**. The foe's pool is fixed, so whole-fight hp/s
is very nearly `hp0/ttk`, and once a channel is strong enough to kill,
everything extra shows up only as a shorter fight:

```
bloodsworn   window +49%   whole fight +28%
sanctified   window +34%   whole fight +20%
dwarven      window +23%   whole fight +14%
```

Every `net` in this document is windowed.

---

# 5. THE TWO FEEDBACK LOOPS. ONE REAL, ONE DEAD.

Stacks **pinned** on the foe rather than earned, with no channel on either
weapon, so contact rate cannot confound the answer. Curse and hemorrhage are in
the table as nulls; curse moves nothing to the digit at every level, which is
what makes the other two rows readable.

**ENTANGLE → PARRY: REFUTED.** The hypothesis was that entangle slows spin 13%
a stack, spin is what parries arrows, so a verdant bow would be self-feeding.
Four stacks is a 52% cut to the foe's spin and moves the parry **-0.4%** and
the landed rate **-0.1%**. The parry is not spin-limited: the blade OCCUPIES
the space whether it is turning fast or slow, and an arrow crossing that space
is caught either way.

**HEX → PARRY: REAL, and worth less than it looks.**

```
   stacks   fired  parried  landed   wall  foe stun
        0    1477     8.3%    8.1%  83.5%     14.9%
        3    1465     5.8%   10.0%  83.8%     58.2%
        5    1449     2.7%   11.2%  86.0%     86.5%
```

Five stacks holds the foe stunned 86% of the fight and takes the parry to
nearly nothing — and buys **+3.1%** landed. The arrows the parry was eating
were mostly going to miss anyway. **Suppressing the parry is worth about a
tenth of what suppressing the wall would be**, and that is the sentence this
whole survey exists to have produced before a design was written.

---

# 6. THE TRAPS v39 LEFT, BOTH ASSERTED

1. **`tickFire` still gates on `f.w.shot`, not on mode.** v39 open decision 4,
   still open, now demonstrated rather than argued: a `shot` block hung on a
   melee greatsword fired **69 arrows in 30 seconds**. The probe put the roster
   back and checks that it did.
2. **`hitStop` still freezes every clock in `tickStatus`.** One free step costs
   a status exactly `dt`; ten frozen steps cost it nothing. **A bow fight is
   frozen 9.8% of its steps**, so that share of every clock in §4 is bought and
   not spent.

---

# Open decisions

1. **THE SCHOOL, AND THEN THE DESIGN IN RICK'S WORDS.** §1 of v38 and v39, held
   to again. Four measured candidates, no proposal in this document.
2. **The wall is the type's constraint and no relic addresses it.** 82% of
   arrows. Ten times the leverage of any status effect measured here. Whatever
   is built should be priced against that number and not against the clock.
3. **`cell_survey`'s umbral row is suspect on all six types.** §4.1. Occupancy
   said best-in-game; delivered effect says zero. Nobody has re-run the other
   five types as delivered effect.
4. **What the two dot channels do to the archer's damage taken is unexplained.**
   §4.2. +14±9 on hemorrhage and smite, desperation refuted as the cause, and
   the contact columns move too little to account for it.
5. **A bow's matchup spread is unpriced.** §2.2. A twinblade eats 12.0% of its
   arrows and a warhammer 5.9%, and no tuning pass has ever seen that column.
6. **Every type-level measurement in the project still wants a `--noult` pass.**
   v38 od 5, v39 od 5, unmoved.

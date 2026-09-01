# v61 — THE PURPLE BOW IS THE THIRTY-FIRST CELL, and the row was re-measured on the tip before anybody was asked for a design. 84,153 arrows, 17/17. The type's constraint has not moved in twenty-one relics: 82% of every arrow ever loosed in this game ends on a wall, and no relic has ever addressed it.

**2026-09-01.** Rick: *"purple bow is in there. lets get it."* → the cell is
chosen. `tools/bow_survey.py --game ../02-chain/sc-garrote.html
--skip clock,cursepin,loop`, on the build of record, 30 relics.
Runtime only. **Nothing was written to any build.**

```
05-reference/v61/bow-survey-at-garrote.txt    the run, 17/17
05-reference/v61/bow-survey-at-garrote.json   the numbers
```

---

# 1. THE ROW, AND WHAT IS LEFT OF IT

```
                     bow       flail  greatsword      scythe   twinblade   warhammer  school
bloodsworn    Marrowdraw   Threshmaw   Goreshard           ·  Widowmaker   Ravelbone     5/6
dwarven         Ironhail   Slagheart   Emberedge Cindercleave          ·  Grudgebearer  5/6
runic                  ·     Paradox       Axiom    Foregone Spellbreaker          ·    4/6
sanctified       Aureole           · Dawnbringer   Lastlight           ·      Censer    4/6
umbral                 ·  Gravemourn   Nightfell           ·   Twinshade  Shroudmaul    4/6
verdant        Vinesower           ·   Heartwood   Thornwake  Thornshear           ·    4/6
vigil          Farwarden           · Lightkeeper      Vesper           ·   Bulwarden    4/6
```

**Two open bow cells: runic and umbral.** Taking umbral puts the school on 5 of
6 and the bow on 6 of 7 — the type is one cell from retired and the school is
one cell from finished, and the two cells are the same cell.

The five bows share **one `shot` block byte for byte** — the shot is a property
of the TYPE — and every one of them has spent its ultimate somewhere different:

```
Ironhail    dwarven     volley       a nova of 14 arrows
Farwarden   vigil       aimedshot    one heavy shot, the ward spent on it
Aureole     sanctified  beam         a shaft of light that heals
Vinesower   verdant     seedfall     8 seeds; those that reach a WALL root
Marrowdraw  bloodsworn  ballista     an 8s window of homing, forking bolts
```

Volume, one big one, a beam, the wall, and homing. **That is the design space
already spent, and it is worth reading before anything is proposed.**

---

# 2. THE CONSTRAINT HAS NOT MOVED IN TWENTY-ONE RELICS

Ults suppressed, damage not pinned, every non-bow foe, 90s cap. 84,153 arrows,
**every one accounted for and zero classified by a sink the probe did not know
about**:

```
bow           hits/s   arrow   stick   landed  parried    WALL   spent    sep
Ironhail       0.308     63%     37%     8.5%     9.1%   82.0%    0.0%    196
Farwarden      0.316     60%     40%     8.6%     8.7%   82.6%    0.0%    182
Aureole        0.310     64%     36%     8.6%     8.5%   82.5%    0.0%    194
Vinesower      0.310     62%     38%     8.4%     8.2%   83.1%    0.0%    187
Marrowdraw     0.300     63%     37%     8.2%     9.1%   82.2%    0.0%    194
```

**A bow lands 8.4% of what it fires and gives 82% of it to the stone.** v40
measured 82% on 21 relics at `baseHP` 300 and an 80s timeout; the long-fight
pace, nine more relics and a re-measured roster have moved it by **less than
one point**. `spent` is still 0.0% — a shot travels 1292 units in its life and
no wall is that far away, so the life cap has never once fired in this game.

> **v40 open decision 2, still open and now twenty-one relics old:** *the wall
> is the type's constraint and no relic addresses it. Anything that moves the
> landed rate is worth roughly ten times anything that moves what an arrow does
> when it lands.* Vinesower is the closest anything has come, and it spends
> **8 seeds of its own** on the wall rather than the ~16 ordinary arrows a
> window's worth of firing already puts there.

## 2.1 The parry belongs to the FOE, and the spread is 3.2x

Damage pinned 14.0, every channel deleted, so two relics of one shape are the
same weapon and the only thing varying is the foe's geometry:

```
foe shape      reach  width  spin  blades   parried  landed   wall
greatsword       116     14   3.4       1     14.4%    5.6%  79.9%
twinblade         62      8   5.7       2     12.0%    7.7%  80.3%
scythe           104     11   3.2       1      9.0%   11.5%  79.2%
warhammer         76     26   1.6       1      7.6%    9.6%  82.5%
flail             96     22   2.2       1      4.6%   10.4%  84.8%
```

**A greatsword eats three times the arrows a flail does**, and there are seven
greatswords and four flails. Still unpriced by any tuning pass — v40 open
decision 5, unmoved. And v40 §5 measured what suppressing the parry is worth:
five stacks of hex, the foe stunned 86% of the fight, buys **+3.1% landed**.
The arrows the parry eats were mostly going to miss anyway.

## 2.2 The arc is real, it is larger than it was, and it now runs a sixth bin

Damage pinned, channels deleted, 10s bins, a bin counting only matches still
running at the end of it:

```
bin        matches  fired  landed  parried   wall  melee/s  shot dmg    sep  inset
0-10s           75   1928   10.3%     9.7%  76.2%    0.089       73%    231      0
10-20s          75   1824    9.8%     9.3%  80.4%    0.096       71%    214      0
20-30s          75   1799    7.1%    11.2%  82.8%    0.097       62%    199     16
30-40s          75   1770    6.8%    10.8%  82.0%    0.136       56%    171     54
40-50s          75   1632    9.4%     8.0%  85.4%    0.170       59%    151     90
50-60s          54    600    8.8%    11.8%  81.0%    0.214       52%    120    122
```

**The arrow carries 73% of the damage in the opening and 52% at the end**, the
melee rate goes 0.089 -> 0.214, and separation halves 231 -> 120. Under the
long-fight pace the hall gets a whole extra bin to close in, so the second half
of the type's own thesis — *dies up close* — is bigger than it was when v40
measured it at five bins.

**A bow is two weapons in sequence, and which one this ultimate serves is a
question with a number attached.**

---

# 3. WHAT THE SCHOOL BRINGS, AND IT IS FLAT

`curse` since v53 is a memory: `maxStacks` 3, `dur` 99, `echo` 0.08 — a stack
remembers the damage of the blow that applied it and every later blow against
that fighter, **from any source**, is enlarged by 8% of everything remembered.

v60 §4 grafted it onto every type's donor. Total echo delivered over a fight:

```
greatsword 111    twinblade 117    warhammer  99
bow        114    scythe    101    flail       82
```

**82 to 117 across every weapon in the game — the flattest channel there is**,
and the bow sits in the middle of it. So **an umbral cell cannot be argued for
or against on which weapon it lands on**, and the interesting question is not
what curse does on a bow. It is what an ultimate does with a pool that takes
**35 seconds to reach 90% of its final size** on this type.

---

# 4. THE CELL'S PRICE, AND ITS ART

```
                v57      v60     tier      art (ink diff from nearest sibling)
umbral x bow   +14.6    +15.6     +16       54.5%   inkIoU 0.537   #10 of 21
```

v60 §2 measured the error bar rather than assuming it: **a cell price at 270
fights has a 95% interval about ±8pp wide and a DIFFERENCE between two cells
needs ~12pp to be real.** umbral x bow shares its tier with
`bloodsworn x warhammer` (Ravelbone, just built) and `runic x bow`. It is not
being taken on a decimal and should not be written up as if it were.

The art is **already written and is not a stub**: both limb TIPS are eaten off
with `destination-out`, a gap bitten out of one limb, and a translucent shadow
flame added back at each tip. v60 §5 rendered it in its own palette beside the
sibling the column calls nearest and it is *"clearly its own object beside the
dwarven bow"* — the one place on the board where the ink column and the eye
agree.

> **AND IT IS THE GRAMMAR RICK REJECTED ON THE WARHAMMER, WHICH IS OPEN ITEM 34
> WITH A FOURTH INSTANCE.** `_whEaten` was purely subtractive and he said the
> silhouette *"just isnt working for me"*; `gnawed_build` replaced it with a
> shape whose spikes are on the type's own OUTLINE. The umbral bow is
> subtractive in exactly the same way. **It has one argument the hammer did not
> have** — its own comment: *"the tips are what the string is anchored to. It
> should not be able to fire, and it does"* — which makes the absence a
> mechanical claim rather than an ornament. That is Rick's to accept or send
> back, and it is cheaper to ask now than after a build.

---

# 5. THE TRAPS, ASSERTED RATHER THAN ASSUMED

1. **`tickFire` still gates on `f.w.shot`, not on `mode`.** A `shot` block hung
   on a melee greatsword fired **66 arrows in 30 seconds**. v39 open decision 4,
   still open. The probe put the roster back and checks that it did.
2. **`hitStop` still freezes every clock in `tickStatus`**, and a bow fight is
   frozen **9.7%** of its steps — so that share of every clock above is bought
   and not spent.

---

# 6. WHAT IS NOT IN THIS DOCUMENT

**No design.** §1 of v38, v39 and v40, held to again: the school is chosen, the
row is measured, and the mechanic is Rick's.

`bow_survey`'s sections [5] and [6] were skipped and are **not** re-measurable
as written. [5]'s clock table and [6]'s feedback loops were built against the
PRE-REWORK curse — `maxHpLoss`, deleted in v53 — and §4.1 of v40 is a
measurement of a status that no longer exists. There is an **uncommitted**
working-tree edit to `bow_survey.py` that rewrites [5b] to read the live pool
and echo instead; it has never been run. It is not this document's evidence and
it was skipped deliberately.

---

# Open decisions

1. ~~**THE MECHANIC, IN RICK'S WORDS.**~~ **WITHDRAWN, AND IT WAS NEVER THIS
   SESSION'S TO ASK.** Three candidate mechanics were offered off this survey
   and Rick picked one; `gloamwire-design-v61.md` had already been written for
   the same cell that morning. CLAUDE.md §3 rule 0 now forbids it outright:
   Claude Code does not design ultimates, and a survey that ends in a spread of
   mechanics is designing. **The measurements in §1-§5 stand** — they are
   observation of the shipped build and were what this document was for.
   The design that ships is GLOAMWIRE / CROSSWEAVE.

2. **THE ART.** §4. The subtractive grammar is a fourth instance of open item
   34 and the only one with a mechanical argument behind it. Accept or redraw,
   and it is cheaper to answer before stage 1.

3. **THE PARRY SPREAD IS STILL UNPRICED.** §2.1, v40 open decision 5, unmoved
   for twenty-one relics. A greatsword eats 14.4% of the arrows loosed at it
   and a flail 4.6%, and there are seven greatswords in the roster. Any bow
   relic's win-rate spread is partly this and no tuning pass has ever seen the
   column.

4. **`bow_survey` [5] AND [6] MEASURE A DELETED STATUS.** §6. Either the
   uncommitted rewrite lands and is run, or those two sections should say in
   their own output that their curse row is a ghost.

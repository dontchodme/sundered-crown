# v62 — DUSKREAVE AND SCOUR, THE UMBRAL SCYTHE. THE TICKS ARE HITS: THEY COLLECT THE CURSE ECHO AND THEY APPLY CURSE, BOTH, AND THE RELIC MEASURES ABOVE THE FIELD.

**THIS TITLE AND THIS BLOCK WERE REWRITTEN ON 2026-09-02 BY v63.** The original
title called the curse clause "the dead clause"; that was §3's finding and it
was overturned by §11 (Rick's correction, measured). The block below is the
state as of the v63 check; everything under it is the v62 record and is NOT a
linear read — three of its sections were withdrawn by later ones. **Read
`HANDOFF-v62.md` §8 for the reading order, and `../v63/duskreave-check-v63.md`
for what the check found.**

**NOT A BUILD BRIEF. DO NOT BUILD FROM THIS.** Settled: the cell, the mechanic,
the geometry (§9a), the blade (21, §12/§17), the names (Duskreave / Scour), the
cast (10s duration), the tick rate (7/s, §15), and the curse verb — **the
ticks are hits on the `resolveHit` path; each one COLLECTS the foe's curse echo
and each one APPLIES curse, exactly as Rick's §1 says (§11, §17).** The apply
clause is measured free under the shipped rule (+0.6pp, noise) and Rick has
held it through four rounds; it is not open. **Everything else was ruled later
the same day — the build brief is `../v63/DUSKREAVE-BUILD-BRIEF.md`.**

**Cowork, 2026-09-01.** Against `02-chain/sc-garrote.html`, the build of record,
**30 relics**, Chromium **141.0.7390.37** — byte-identical to the runtime v57,
v59 and v60 quote, so every number here is directly comparable to theirs.
~1,500 fights. Nothing written to any build.

## The names, 2026-09-01

**The relic is DUSKREAVE.** From four candidates — Barrowgale, Wraithcoil,
Duskreave, Hollowgyre. *Reave* is to tear away and plunder, and it is the root
'reaper' comes from: the only one of the four carrying the scythe in its name.

**The ultimate is SCOUR.** From four — Undertow, Scour, Squall, Attrition. One
hard syllable meaning to grind away by abrasion, which is the fifteen-ticks-a-
cast texture rather than the wind that carries it. Sits beside Grasp and Breach.

## Why this cell

`umbral × scythe` is the **last open scythe**. Taking it retires the scythe row
the way the greatsword row is already retired, and it leaves umbral with no open
cell at all. Ten cells remain in the game after this one.

**Priced at the tip.** `cell_ults_on.py`, 10 cells, 4 arms each, 270 fights an
arm, 11,600 fights, against `sc-ravelbone.html` (30 relics):

```
cell                     FIELD ULTS OFF        FIELD ULTS ON      v60      move
                        floor    lift        floor    lift
vigil x twinblade       33.1%  +47.9pp       10.7%  +45.5pp      +49.3     -1.4
vigil x flail           15.9%  +32.8pp        7.2%  +21.0pp      +31.1     +1.7
dwarven x twinblade     33.1%  +24.8pp       10.7%  +29.0pp      +25.8     -1.0
sanctified x twinblade  33.1%  +24.1pp       10.7%  +22.4pp      +28.1     -4.0
runic x bow             41.4%  +12.4pp       18.6%  +19.7pp      +13.0     -0.6
sanctified x flail      15.9%  +12.4pp        7.2%   +4.5pp       +9.6     +2.8
verdant x flail         15.9%   +8.3pp        7.2%   +2.4pp       +8.1     +0.2
runic x warhammer       38.6%   +6.9pp       16.9%   +5.2pp       +6.7     +0.2
UMBRAL X SCYTHE         53.4%   +6.6pp       39.0%   +6.2pp       +8.1     -1.5
verdant x warhammer     38.6%   +3.4pp       16.9%   +0.7pp       +4.4     -1.0
```

**REPRODUCTION CONTROL, and it could have failed.** Ten cells re-measured on a
build two relics newer than v60's. Largest move **4.0pp**, against a 270-fight
SE of ~4.3pp that v60 §2 measured directly. The column reproduces.

**And v60 §2's warning still governs the reading of it:** a difference under
~12pp at this n is not a difference. `umbral × scythe` sits in the bottom tier
with four others and the decimals between them mean nothing. It was taken for
the row it closes, not for its price.

## Rick's §1, verbatim (2026-09-01)

> the scythe conjures a purple tornado thats crackling with electricity. the
> tornado paths along the bottom of the arena. the tornado sucks up enemy
> projectiles. if the enemy fighter gets stuck in the tornado its dragged down
> into it. taking rapid ticks of damage that apply curse.

Three clauses can be priced before anything is designed on top of them. Two
survive. One does not.

---

# 1. "PATHS ALONG THE BOTTOM OF THE ARENA" — THE FLOOR IS THE BUSIEST BAND IN THE GAME, AND HEIGHT IS THE KNOB

The arena is **520 × 800**. Gravity is **900**, `floorBounce` **0.97**, ball
radius **34** — so a ball's centre cannot go below **y = 766**. 696 fights,
both fighters sampled every 0.05s:

```
y   0-50    0.1%
y  50-100   0.7%  ##
y 100-150   1.4%  ####
y 150-200   2.6%  ########
y 200-250   3.0%  #########
y 250-300   4.1%  ############
y 300-350   5.3%  ################
y 350-400   6.4%  ###################
y 400-450   7.6%  #######################
y 450-500   8.9%  ###########################
y 500-550  10.5%  ################################
y 550-600  11.6%  ###################################
y 600-650  12.8%  ######################################   <- peak
y 650-700  12.5%  #####################################
y 700-750   9.9%  ##############################
y 750-800   2.6%  ########                                 <- ball radius floor
```

**CONTROL:** a uniform arena gives 25.0% below y=600. The measurement gives
**37.8%**, biased toward the floor exactly as gravity predicts. Had it come
back flat the instrument would have been reading the wrong field.

> **THE CLAUSE IS SOUND AND IT HANDS THE DESIGN ITS FIRST KNOB.** A tornado on
> the floor sits under the densest part of the fight. But *how tall it is*
> decides how often it touches anybody:
>
> ```
> reaches y >= 700  (a low churn on the floor)        12.5% of fight-time
> reaches y >= 650  (waist high)                      25.0%
> reaches y >= 600  (a third of the arena)            37.8%
> ```
>
> That is a 3x range on contact from one number, and it is Rick's to pick once
> the mechanic is settled.

---

# 2. "SUCKS UP ENEMY PROJECTILES" — TWENTY-ONE OF THIRTY RELICS NEVER FIRE ANYTHING, EVER

Owner is `shot.own`, the string `"a"`/`"b"`. 696 fights, a fixed six-relic
panel, sampled every 0.05s:

```
relic          name          type        ultimate         % of fight with own shot up   mean   max
ironhail       Ironhail      bow         Quarrelstorm                          72.8%    1.40    16
aureole        Aureole       bow         Benediction                           68.9%    1.04    24
vinesower      Vinesower     bow         Thicket                               68.2%    1.01    24
farwarden      Farwarden     bow         Reprisal                              62.7%    0.92    24
marrowdraw     Marrowdraw    bow         Bloodhunt                             62.2%    0.95    24
thornshear     Thornshear    twinblade   The Winnowing                         33.4%    7.96    55
redflail       Threshmaw     flail       Bloodmill                             28.7%    4.95    41
lastlight      Lastlight     scythe      Harrowing                             11.8%    1.03    12
slagheart      Slagheart     flail       Ironbloom                              6.8%    0.36     9
--- and then nothing ---
every greatsword (7), every warhammer (5), four of six scythes,
Twinshade, Spellbreaker, Paradox, Foregone                        0.0%    exactly
```

**CONTROL, and the first draft of this probe FAILED it.** The first version
guessed the owner field, fell back to "count every shot" when the guess missed,
and returned 8–13% for every melee relic in the game — the panel's own bow,
read back as the greatsword's projectiles. That reading is discarded. The
control now is that a relic with nothing ranged in its kit must return
**exactly 0.0%**; twenty-one do.

> **THE CLAUSE IS REAL BUT IT IS NOT LOAD-BEARING.** It fires in **9 matchups
> of 29** (10 once Gloamwire is built), and it is genuinely busy in only the
> five bows, where something is in the air two-thirds of the fight. Against
> twenty-one relics it does nothing at all.
>
> That is not a fault. It costs nothing, it is a real counter to the bow row,
> and Thornshear at 55 shots in the air is a spectacle worth eating. **It just
> cannot be the reason the ultimate is worth anything**, and no composition
> should price it as though it were.

---

# 3. "RAPID TICKS OF DAMAGE THAT APPLY CURSE" — THIS IS THE DEAD CLAUSE, AND THE ENGINE HAS A COMMENT ABOUT IT

Curse does not count stacks. It **remembers blows**, and it keeps the three
biggest ones:

```js
pushCurse(v, n){
  for (let i = 0; i < n; i++) this.cursePool.push(v);
  this.cursePool.sort((a, b) => b - a);
  if (this.cursePool.length > STATUS.curse.maxStacks)
    this.cursePool.length = STATUS.curse.maxStacks;
}
curseEcho(){ return this.curseSum() * STATUS.curse.echo; }   // echo = 0.08
```

A new memory is kept **only if it beats the smallest of the three already
there.** And the engine says what happens to a caller that applies curse
without a memory, in a comment sitting on `apply`:

> *"a caller that applies curse without handing `pushCurse` a memory refreshes
> the clock and adds nothing. Deliberate — an ultimate that 'applies 3 Curse
> stacks' out of nowhere is exactly the dead clause v49 measured at +0.0."*

**So the bar was measured.** Umbral curse grafted onto the scythe donor — the
same graft `row_price` and `cell_ults_on` use — 8 foes × 8 seeds, the foe's
pool traced every 5s:

```
    t (s)   mean stacks   % at 3 stacks   bar = the 3rd largest
        5          1.16             3%                    27.0
       10          1.84            25%                    29.8
       15          2.31            50%                    29.7
       20          2.64            73%                    31.1
       25          2.72            77%                    31.8
       30          2.91            93%                    35.3
       40          2.94            97%                    36.9
       50          2.83            92%                    39.2
       60          2.33            67%                    44.5

    time to a full pool: median 15.0s, mean 18.2s
    60 of 64 fights filled it
```

**CONTROL:** a memory of `1e9` must always be kept and a memory of `0` must
never be kept once the pool is full. Both held. Had either missed, the model of
`pushCurse` above would be wrong and every number under it with it.

> **THE FINDING. By fifteen seconds the bar is ~30 damage and it only climbs.**
> A tick small enough to be called *rapid* is 3–8. It cannot enter the pool
> after the first three real blows land, and the memories it puts there before
> then are displaced by the first scythe hit that connects. **As written, the
> clause is worth zero for all but the opening seconds of a fight** — the
> +0.0pp v49 measured, arrived at from a different direction.

**AND THE TWO VERBS EITHER SIDE OF IT ARE TAKEN.** The engine is explicit that
umbral's ultimates are distinguished by what they do to the pool:

- **Gravemourn's Revenant MOVES a memory** — `foe.cursePool.length = 0` and the
  memories fly out as hands.
- **Nightfell's Deadfall COPIES one** — `curseSum()` and nothing else, read-only,
  with a comment warning that a build which re-applies curse from a mine *"would
  also hand this relic Gravemourn's verb."*
- **Shroudmaul is pool-independent** by Rick's own ruling, 2026-08-31.

So the tornado needs a curse verb that is neither *move*, nor *copy*, nor
*apply-and-add-nothing*. §4 is the four readings, priced where arithmetic can
price them.

---

# 4. THE FOUR READINGS OF CLAUSE THREE — RICK'S RULING

Measured baseline: a full pool averages **~105 total** (three memories of
~35), so an ordinary blow lands with **~8.4** of echo on top of it.

**A. THE TORNADO'S TICKS ADD UP TO ONE MEMORY.** It totals what it deals to a
fighter held inside it and, on release, pushes **one** memory of that total.
Twenty ticks of 4 becomes a single **80** — bigger than anything a scythe
lands, and the largest thing in the pool.
*Arithmetic:* pool 105 → ~153, echo per hit **8.4 → 12.2 (+45%)**.
*Verb:* it MAKES a memory. Not move, not copy, not apply. Nothing else does it.
*Cost:* one accumulator on the drag.

**B. FEWER, HARDER TICKS.** Keep "apply curse" literally by making each tick
big enough to clear the bar — roughly one a second at 30+. Every tick that
lands is a real memory.
*Arithmetic:* the pool becomes all tornado, sum ~90–120, echo **~7–9.6**.
*Cost:* "rapid" is gone. A grinder becomes a mauling, and the ult's damage
budget goes up sharply for the same echo.

**C. DROP THE CURSE CLAUSE. THE TORNADO IS DAMAGE AND CONTROL.** The relic is
umbral by its blade's own `onHit`, exactly as Shroudmaul is.
*Arithmetic:* echo unchanged at 8.4; the ultimate is priced on the drag alone.
*Cost:* honest and cheap, and the school's signature does not appear in the
set-piece.

**D. RAISE THE CEILING WHILE IT STANDS** — the Bloodmirror precedent, cap 3 → 5.
**This one is offered and argued against.** Echo is 8% of the *sum*, so two
extra memories of 5 add **0.8 damage per hit**. It is the answer that worked
for bleed because bleed's problem was a count; curse's problem is a size.
*Arithmetic:* pool 105 → 115, echo **8.4 → 9.2 (+9%)**.

---

---

# 5. RICK RULED B — "FEWER, HARDER TICKS" — AND PRICING IT CORRECTED TWO THINGS THIS DOC HAD ALREADY TOLD HIM

**Rick, 2026-09-01, from four readings:** every tick is big enough to be its
own curse memory. The word *rapid* goes; the tornado mauls rather than grinds.

## 5a. THE "~30 DAMAGE" BAR IN §3 WAS THE WRONG NUMBER TO ACT ON

§3 measured the bar as the *third-largest* memory, ~30, and said a tick needs
to clear it. That is the threshold to **enter** the pool. It is not the
threshold to **change** it. 100 fights, steady state, scythe donor:

```
    natural pool, no tornado:   50.0  /  38.4  /  30.8      sum 119.3
    echo at 8%:                 9.54 added to every blow that lands
    CONTROL: descending by construction — PASS
```

A tick of 30 ties the bottom memory and displaces nothing. **The real
thresholds are 40 (moves the pool) and 50 (takes the pool entirely).** This
correction is recorded rather than quietly folded in, because the ruling in §4
was made against the wrong number and it survives the right one.

## 5b. THE ANCHORS THAT BOUND THE TICK, MEASURED

```
    fighter health                       400
    a scythe's whole-fight output        ~405 damage over ~45s
    blows a scythe lands in a fight      8 (Thornwake, blade 31.35)
    an ultimate at charge 15 fires       2x a fight
```

**A fighter's entire fight is one health bar.** That is the sentence that
prices this ultimate. An ult that fires twice and is worth 25–30% of a bar a
cast is in line with the field; one worth 40% a cast is most of the fighter.

## 5c. THE LADDER

```

      tick  ticks/catch  dmg/cast  % health bar  2 casts          pool after  echo/blow  vs 9.54  echo over 8 blows
        30            2        60          15%      30%        [50, 38, 31]       9.54    +0.00               +0.0
        30            3        90          22%      45%        [50, 38, 31]       9.54    +0.00               +0.0
        30            4       120          30%      60%        [50, 38, 31]       9.54    +0.00               +0.0
        40            2        80          20%      40%        [50, 40, 40]      10.40    +0.86               +6.9
        40            3       120          30%      60%        [50, 40, 40]      10.40    +0.86               +6.9
        40            4       160          40%      80%        [50, 40, 40]      10.40    +0.86               +6.9  <-- overshoots a health bar
        50            2       100          25%      50%        [50, 50, 50]      12.00    +2.46              +19.7
        50            3       150          38%      75%        [50, 50, 50]      12.00    +2.46              +19.7
        50            4       200          50%     100%        [50, 50, 50]      12.00    +2.46              +19.7  <-- overshoots a health bar
        60            2       120          30%      60%        [60, 60, 50]      13.60    +4.06              +32.5
        60            3       180          45%      90%        [60, 60, 60]      14.40    +4.86              +38.9  <-- overshoots a health bar
        60            4       240          60%     120%        [60, 60, 60]      14.40    +4.86              +38.9  <-- overshoots a health bar

    A cast worth 25-30% of a health bar puts the ultimate in line with a
    fighter whose ENTIRE fight output is one health bar and who casts twice.
```

> **THE FINDING UNDER B, AND IT IS NOT THE ONE THE CLAUSE PROMISES.** At every
> rung the ticks are worth five to seven times the curse they enable. Tick 50 x
> 2 delivers **100 damage** and **+19.7** of echo across the rest of the fight.
> **The tornado is a damage engine whose curse is genuine but small.** That is
> a fine relic and it is not what "rapid ticks that apply curse" sounds like,
> so it is written down here rather than discovered at build time.
>
> **And the budget caps the catch at two or three ticks, not eight.** The
> drag is short and heavy. Rick's instinct — fewer, harder — lands in the right
> place; the measurement only says how few.

---

---

# 6. RICK REVERSED B — "LOTS OF TICKS FOR LESS DAMAGE" — AND THE REVERSAL SELECTS READING A

**Rick, 2026-09-01, on being shown the tick ladder:** *"ive changed my mind.
lots of ticks for less damage."* That is his §1's grinder, restored on purpose
after seeing what the heavy-tick version costs.

**It closes B by its own terms.** A tick small enough to be one of many cannot
clear 30.8, so under B each tick would apply nothing. Of the four readings in
§4 only two survive a grinder: **A** (the drag totals itself into one memory)
and **C** (no curse from the tornado at all). D was argued against in §4 and
the reversal does not revive it.

```
READING A — THE DRAG TOTALS ITSELF INTO ONE MEMORY ON RELEASE

    natural pool  [50.0, 38.4, 30.8]  sum 119.3  echo 9.54/blow
    health 400 · a cast at 25-30% of a bar = 100-120 damage

     drag total   % bar  the memory            pool after  echo/blow  vs 9.54  over 8 blows
             60    15%          60          [60, 50, 38]      11.87    +2.33         +18.7
             80    20%          80          [80, 50, 38]      13.47    +3.93         +31.5
            100    25%         100         [100, 50, 38]      15.07    +5.53         +44.3
            120    30%         120         [120, 50, 38]      16.67    +7.13         +57.1
            150    38%         150         [150, 50, 38]      19.07    +9.53         +76.3

    SAME BUDGET, READING B (the one just reversed), best rung:
            100    25%       50 x2          [50, 50, 50]      12.00    +2.46         +19.7

    A BEATS B ON CURSE AT IDENTICAL DAMAGE, because the memory is the
    WHOLE DRAG rather than one tick of it.

    AND THE TICK COUNT IS FREE UNDER A — only the total is remembered:
      10 ticks x 10 dmg = 100 total  ->  identical memory, identical echo
      12 ticks x  8 dmg =  96 total  ->  identical memory, identical echo
      20 ticks x  5 dmg = 100 total  ->  identical memory, identical echo
      25 ticks x  4 dmg = 100 total  ->  identical memory, identical echo
```

> **THE REVERSAL MAKES THE DESIGN BETTER, NOT WORSE, AND THAT IS WORTH SAYING
> PLAINLY.** At an identical 100-damage cast, A delivers **+5.53** of echo a
> blow against B's **+2.46** — because the memory is the whole drag rather than
> the largest tick of it. The grinder is the *better* curse engine under A.
>
> **AND THE TICK COUNT BECOMES FREE.** Only the total is remembered, so 25
> ticks of 4 and 10 ticks of 10 produce the same pool, the same echo and the
> same damage. Tick count is a pure feel-and-animation choice with no balance
> attached — which is the first knob in this relic that Rick can set on looks
> alone.
>
> **ONE CAVEAT, RECORDED BEFORE IT IS BUILT.** A memory of 100 is twice the
> largest blow any scythe lands. It would be the biggest single entry any
> curse pool in the game has held, and the echo it creates — 8 damage a blow on
> its own — is a school signature rather than a rider. That is a feature and it
> is also the first place to look if the relic prices high.

---

---

# 7. THE CURSE VERB IS SETTLED: EACH TICK APPLIES CURSE, AND WHAT IT APPLIES IS THE DRAG'S RUNNING TOTAL

**Rick, 2026-09-01, asked to confirm A or C: "each tick applies curse."** He
has now given that clause three times — as §1, as the reversal in §6, and here
against two named alternatives. **It is a ruling, not a misreading**, and this
session's job was to find the version of it that is true.

**His second answer in the same breath settles which version.** He also chose
**100 damage a cast**, on a question that said in its own text *"under A this
number is also the curse memory."* Only one mechanic satisfies both answers.

```
EACH TICK APPLIES CURSE — THE THREE WAYS IT CAN BE TRUE

    natural pool [50.0, 38.4, 30.8]  echo 9.54/blow
    a cast deals 100 (Rick, this session). 12 ticks of ~8.

    reading                                              pool at release  echo/blow  vs 9.54   over 8
    1. each tick pushes its own 8                           [50, 38, 31]       9.54    +0.00     +0.0
    2. each tick pushes the running total                   [96, 88, 80]      21.12   +11.58    +92.6
    3. running total, replacing its own                     [96, 50, 38]      14.75    +5.21    +41.7

    [1] is the dead clause: 8 never beats 30.8. Pool untouched.
    [2] the last three totals crowd out every natural memory. Runaway.
    [3] one memory that GROWS on every tick. Pool updates every tick, the
        number on screen climbs, and it ends at exactly the cast budget.

    [3] IS THE ONLY READING THAT SATISFIES BOTH OF RICK'S ANSWERS:
        'each tick applies curse'  AND  'a cast is worth 100'.


TWO CASTS — CURSE LASTS THE WHOLE FIGHT (dur 99), SO THE FIRST MEMORY IS STILL THERE

    after cast 1              [96, 50, 38]  echo  14.75/blow  +5.21
    after cast 2             [100, 96, 50]  echo  19.68/blow  +10.14

    A second cast pushes the FIRST cast's memory down but does not delete it.
    The pool ends the fight holding two tornado memories and one blade memory.
```

> **THE RULING. Every tick applies curse. The memory a tick applies is the
> drag's RUNNING TOTAL, and it replaces the one that tick's predecessor left.**
> The pool updates on every single tick, the number on the foe climbs while the
> tornado holds them, and it comes to rest at exactly the cast's damage budget.
>
> It is literally Rick's sentence, it is not the dead clause, it is not
> Gravemourn's verb and it is not Nightfell's. **This relic's verb is that it
> GROWS a memory.**

## 7a. THE BUILD NOTE THAT DECIDES WHETHER THIS SHIPS RIGHT

`pushCurse` appends and sorts; it has no replace. **A builder that appends the
running total on every tick gets reading [2] — a pool of `[96, 88, 80]`, echo
21.12, a runaway that crowds every natural memory out of the game.** The drag
must hold its own memory and swap it, not stack it. This is the single place
this ultimate can be built wrong while looking right, and it will not show up
as an error — only as a relic that prices 10 points high.

## 7b. TWO CASTS, BECAUSE CURSE LASTS THE WHOLE FIGHT

`dur` is 99 against a 120s timeout, so cast one's memory is still there when
cast two lands:

```
    after cast 1     [96, 50, 38]   echo 14.75/blow   +5.21
    after cast 2    [100, 96, 50]   echo 19.68/blow  +10.14
```

**The fight ends with the pool holding two tornado memories and one blade
memory.** That is the relic's signature and it is also the first number to
check when it is priced: +10.14 a blow is a doubling of the field's echo.

---

---

# 8. RICK TOOK A DURATION OVER A COUNT, AND `tornado_lab.py` PRICES WHAT THAT COSTS. SWEEP SPEED TURNS OUT TO BE FREE AND WIDTH IS THE ONLY KNOB THAT MOVES ANYTHING.

**Rick, 2026-09-01:** fast blur (~4.5 ticks a second), a tornado a third of the
arena tall, and **a stretch of seconds** rather than a fixed number of passes —
breaking a pattern he had taken twice running (Breach's five vents, Crossweave's
24-volley magazine).

**A duration makes delivered damage variable**, so how many seconds buys the
100-damage budget had to be measured. `tools/tornado_lab.py` replays 80 real
fights, sweeps a band of a given width along the floor through the foe's actual
position track, and counts contact.

## 8a. THE CONTROL FAILED FIRST, AND THE FAILURE WAS THE POINT

The first control compared an **edge-rule** sweep — a ball is caught when its
rim crosses y=600 — against §1's **centre-rule** histogram. Ball radius is 34,
so the two rules differ by 34px of arena, and the sweep came back **51.5%**
against the histogram's **37.8%**. Both numbers were correct; the comparison
was not. The control now compares a full-width sweep against a no-sweep
measurement of the same tracks under the same rule: **51.5% vs 51.5%, PASS.**

For the record, on these tracks the centre rule gives **42.7%** where §1's
histogram gave 37.8% — §1 measured *both* fighters across a wider panel. Both
stand; they are different populations.

## 8b. SWEEP SPEED IS FREE

```
    120 px/s -> 17.3%      200 px/s -> 17.3%      300 px/s -> 17.4%
```

**Contact does not move with sweep speed at all.** A band that crosses the
arena slowly and one that races cover the same ground per second of cast. So
sweep speed joins tick rate on the list of knobs Rick can set on looks alone.
**Width is the only geometry that changes the number.**

## 8c. THE SIZING TABLE

```
SIZING A DURATION CAST TO THE 100-DAMAGE BUDGET

      width  % of arena   contact   cast   ticks   dmg/tick for 100    what it looks like
         90        17%    17.3%     8s     6.2               16.1                sparse
         90        17%    17.3%    10s     7.8               12.8                sparse
         90        17%    17.3%    12s     9.3               10.7                sparse
        120        23%    20.9%     8s     7.5               13.3                sparse
        120        23%    20.9%    10s     9.4               10.6                sparse
        120        23%    20.9%    12s    11.3                8.9                  fast
        160        31%    26.0%     8s     9.4               10.7                sparse
        160        31%    26.0%    10s    11.7                8.5                  fast
        160        31%    26.0%    12s    14.0                7.1                  blur
        200        38%    30.8%     8s    11.1                9.0                  fast
        200        38%    30.8%    10s    13.9                7.2                  fast
        200        38%    30.8%    12s    16.6                6.0                  blur

    sweep SPEED does not matter: 17.3% / 17.3% / 17.4% at 120 / 200 / 300 px/s.
    Only WIDTH and DURATION move contact. Speed is a free feel knob, like tick rate.
```

> **THE FINDING. A 10-SECOND CAST AT 5 DAMAGE A TICK DELIVERS 39–70, NOT 100.**
> To bank the full budget at 5 a tick the cast has to run **14 to 26 seconds**
> depending on width — a third to half of a 45-second fight, against Breach's
> nine.
>
> **The fix costs nothing Rick chose.** He picked a tick *rate*, not a tick
> *count* — "~20 ticks" was this session's estimate of what a cast would hold,
> and it was wrong. Hold the rate at 4.5/s, hold the budget at 100, and let
> **tick damage float to 7–9**. A 160-wide tornado on a 10-second cast then
> delivers ~12 ticks of 8.5, which still reads as a blur, and lands the budget.
>
> **THE VARIANCE IS THE REAL COST AND IT IS NOT SMALL.** Contact is an average
> over 80 fights. A cast that catches a ball early and holds it delivers well
> over 100; one that never connects delivers nothing, and under §7 that means
> **no curse memory at all.** A count guarantees the budget; a duration gambles
> it. Rick has the trade and took it — the open question is only whether the
> upside gets a ceiling.

---

---

# 9. THE GEOMETRY IS SETTLED. THE CURSE VERB IS NOT, AND §7 IS WITHDRAWN.

## 9a. SETTLED, 2026-09-01

```
    tornado height      a third of the arena — top at y=600
    tornado width       160  (31% of the arena's width)
    cast                a STRETCH OF SECONDS, 10s, not a count of passes
    tick rate           fast blur, ~4.5 a second — pure feel, no balance
    sweep speed         free, measured: contact is flat from 120 to 300 px/s
    damage a cast       100, a quarter of a health bar
    damage a tick       ~8.5, so that ~12 ticks of average contact make 100
    projectiles         the tornado eats them; kept as flavour, never priced
```

## 9b. §7 IS WITHDRAWN. RICK: "THE MEMORY DOES NOT GROW."

§7 read his two answers — *"each tick applies curse"* and *"a cast is worth
100"* — as a memory that grows tick by tick to the cast budget. **He has
rejected that**, and the reading goes with it.

**What that leaves is the arithmetic, unchanged and unarguable:**

- Curse is not a stack count. `pushCurse(v, n)` keeps the **three largest**
  remembered blows and drops anything smaller.
- The three natural memories on a scythe fight, measured over 100 fights, are
  **50.0 / 38.4 / 30.8**.
- A tick of ~8.5 never clears 30.8. It cannot enter the pool.
- `apply("curse", n)` without a memory sets `stacks` to `cursePool.length` and
  changes nothing else. The engine's own comment: *"an ultimate that 'applies 3
  Curse stacks' out of nowhere is exactly the dead clause v49 measured at
  +0.0."*

**So "each tick applies curse" with a fixed, tick-sized memory has no
mechanical effect. That is not a reading — it is the engine.**

> **THIS SESSION HAS NOW OFFERED THREE MECHANICS FOR THIS CLAUSE AND RICK HAS
> DECLINED ALL THREE.** Accumulate-on-release (§4A), one-memory-per-tick at 40+
> (§4B, ruled then reversed), and a growing memory (§7). A fourth invented
> mechanic is not what is missing. **What is missing is what Rick wants a tick's
> curse to DO**, and that is his to say — `CLAUDE.md` §3 rule 2 lists the ult
> mechanics among the seven things that are his, and §3 rule 0 is explicit that
> a spread of mechanics is designing.
>
> **AND "IT IS FOR THE LOOK" IS A LEGITIMATE ANSWER.** The relic is umbral by
> its blade's own `onHit`, exactly as Shroudmaul is by Rick's ruling of
> 2026-08-31. A tornado that pops the curse tag on every tick while the blade
> does the pool work is a coherent relic, it costs nothing to build, and it is
> the honest version of the sentence as written.

---

---

# 10. "HOW IS IT NOT DOING ANYTHING CURRENTLY?" — RUN RATHER THAN ASSERTED. SEVENTY-NINE TICK-SIZED CURSES MOVE DAMAGE BY 0.1 IN 381; SEVENTY-SEVEN BIG ONES MOVE IT BY 12.5.

Rick asked the fair question. This document had asserted the answer twice from
a code comment and an arithmetic argument, which is not the same as measuring
it. `tools/tick_ab.py` measures it.

Three arms on identical fights, an umbral scythe on the scythe donor, two
10-second windows a fight ticking 4.5 times a second — the tornado's exact
cadence. The only difference between arms is **the size of the number handed to
`pushCurse`**. Paired on seed and opponent, **320 fights an arm**:

```
    arm         memories pushed        final pool   echo/blow   damage dealt   win rate
    OFF                       0      [72, 54, 45]       13.55          381.3      55.9%
    TICK 8.5                 79      [73, 54, 44]       13.70          381.3      55.0%
    BIG 60                   77      [74, 63, 60]       15.76          393.8      65.6%

    TICK 8.5 vs OFF:   echo +0.15   damage  +0.1   win -0.9%   identical fights 103/320
    BIG 60   vs OFF:   echo +2.21   damage +12.5   win +9.7%   identical fights   3/320
```

**POSITIVE CONTROL: PASS.** The BIG arm has to move or the injection is not
reaching the fight. It moves 12.5 damage and 9.7 points of win rate.

**AND THE SESSION'S FIRST RUN OF THIS WAS WRONG.** At 120 fights an arm the
TICK arm read **+5.0% win rate** and it was written down as a possible real
effect. At 320 it reads **−0.9%**. The n=120 number was noise and did not
survive; the echo column, being a direct read of state rather than an outcome,
was stable at both n. **Outcome columns in this engine need three times the
fights that state columns do.**

> **THE ANSWER, IN ONE SENTENCE.** The three curse slots are a top-three
> leaderboard of the biggest blows landed on that fighter; applying curse
> submits a score to it. A tick submits **8.5** to a board whose lowest entry is
> **31** — the submission is accepted, immediately discarded, and the board is
> unchanged. **Seventy-nine of them in a fight are worth 0.1 damage out of 381.
> In a third of the fights they changed nothing whatsoever — the two arms ran
> byte-identical from first frame to last.**
>
> **It is not that curse is weak. It is that the number of applications is not
> what curse counts.** The same seventy-seven applications carrying 60 instead
> of 8.5 are worth 12.5 damage and nearly ten points of win rate. **The size of
> the remembered blow is the only thing that matters, and a tick is small by
> definition.**

---

---

# 11. RICK WAS RIGHT AND THIS SESSION HAD BEEN MEASURING THE WRONG DIRECTION FOR FOUR ROUNDS. THE TICKS DO NOT FEED CURSE — THEY CASH IT, ON EVERY TICK, AND THAT IS WORTH +29.7 WIN POINTS INSTEAD OF +17.8.

**Rick, 2026-09-01:** *"lets say the scythe has done 100 damage on its last 3
hits ... so when the tornado fires and is dealing 10 damage per tick. its
dealing 10 + the 24 from curse. thats a huge payoff."*

**He is right, and §3 through §10 of this document asked only the other
question.** Every one of them measured whether a tick ADDS to the pool. None
asked whether a tick COLLECTS from it. The engine is explicit, in a comment on
the echo line itself:

> *"PRICED ON THE TARGET AND NOT ON AN ASSUMED ATTACKER. There is no
> `self === owner` guard and there must never be one ... It is also PoE's rule
> — hit by any source."*

**An ultimate that lands twenty hits collects the echo twenty times.** On a
school whose channel pays per-hit, a rapid-tick ultimate is a multiplier, and
that is the whole design. It was in Rick's §1 from the first message.

## 11a. ONE CORRECTION TO HIS MODEL, AND IT IS IN HIS FAVOUR

> *"after 3 hits those 100 damage hits should have fallen off and now the last
> 3 curse hits have memories of 10 damage. so the next tick gets +2.4 damage."*

**They do not fall off.** `pushCurse` sorts descending and truncates — it keeps
the three **largest** memories ever landed, not the three most recent — and
curse's `dur` is 99 against a 120-second timeout, so they last the fight.

**A memory of 10 never displaces a memory of 100.** In his own example the echo
stays at **+24 on every tick for the whole cast**, and does not decay to +2.4.
The ultimate is better than the version he was arguing for.

**And it makes §3–§10 consistent rather than wrong.** A tick is too small to
enter the pool (§10, measured at +0.1 damage in 381) *and* too small to dilute
it. Both follow from the same rule. The tick's job was never to feed the pool.

## 11b. THE MEASUREMENT, AT THE TORNADO'S REAL SIZE

`tools/tornado_full.py` joins this session's two halves: the 160-wide band
sweeping the floor from §8, and the two damage paths from §11c. The tornado
ticks **only while it is actually touching the foe**, two 10-second casts a
fight, 4.5 ticks a second, base tick **5**. 320 fights an arm:

```
    arm       ticks/fight   contact   tornado dmg   of which echo   per cast   win rate   vs NONE
    NONE              0.0      0.0%           0.0             0.0        0.0      56.9%     +0.0%
    HURT             19.2     26.2%          96.1             0.0       48.0      74.7%    +17.8%
    HIT              16.0     25.9%         176.2            96.3       88.1      86.6%    +29.7%
    DRAIN            19.8     25.9%          99.1             0.0       49.5      67.5%    +10.6%
```

**CONTROL 1 — CROSS-INSTRUMENT, AND IT COULD HAVE FAILED.** Contact measured
**26.2%** here against the **26.0%** `tornado_lab.py` predicted from position
tracks alone, by different code on different fights. Two independently written
instruments agreeing to two tenths of a point.

**CONTROL 2 — DRAIN.** Emptying the pool before reading the echo must collapse
HIT onto HURT. 99.1 against 96.1. **PASS** — the arms differ by the echo and
nothing else.

> **THE ECHO IS +83% ON TOP OF THE TICKS' OWN DAMAGE, and it nearly doubles the
> ultimate per cast: 48 to 88.** In win rate it is the difference between a
> +17.8 ultimate and a **+29.7** one — for reference, Crossweave measured +48.8
> and Harrowing more.
>
> **AND RICK'S ORIGINAL NUMBERS WERE ALREADY RIGHT.** At a base tick of **5** —
> his "lots of ticks for less damage", not the 8.5 §8 recommended — the HIT
> path delivers **88 a cast** against a budget of 100. §8c's "let tick damage
> float to 7–9" was an artifact of assuming the wrong damage path and **is
> withdrawn.** The ticks are small because the curse is the payload. That is
> what the sentence said.

## 11c. THE BUILD NOTE THAT DECIDES WHICH ULTIMATE GETS BUILT

**There are two damage paths in this engine and they are 12 win points apart.**

- **`resolveHit`** is the full pipeline: crit, jitter, `dmgTakenMul` (Sunder),
  **the curse echo**, Aegis, hit-stop, knockback, `onHit` status. Damage is
  folded into `dmg` *above* the Aegis block, so a wall eats it and a ward
  absorbs it.
- **`hurt(foe, dmg, src)`** is raw: shield absorption, then `foe.hp -= dmg`.
  **No echo. No sunder. No aegis.**

**Sentinel's beam — the closest precedent for a ticking ultimate in the game —
uses `hurt`.** `beamHit` calls `this.hurt(foe, dmg, f)` and collects nothing.
**A builder following the nearest precedent will build the +17.8 tornado
without noticing there was a choice.** The brief must say, in as many words:
**the tornado's ticks are hits and go through `resolveHit`.**

## 11d. THE VERB, SETTLED BY THE MEASUREMENT RATHER THAN BY A SPREAD

Umbral's ultimates are told apart by what they do to the pool:

```
    Gravemourn / Revenant     MOVES memories out of it     (empties, slings them as hands)
    Nightfell  / Deadfall     COPIES its value             (read-only curseSum)
    Shroudmaul / Grasp        IGNORES it                   (Rick's ruling, 2026-08-31)
    THE TORNADO               CASHES IT, REPEATEDLY        (the echo, 16 times a fight)
```

**It is the fourth verb, it is distinct from all three, and it came out of
Rick's §1 without a word being changed.** "Rapid ticks of damage that apply
curse" is literally true on the `resolveHit` path — each tick does call
`apply`, pushing a memory of 5 that the pool discards — and the value is in the
collection, not the application.

---

---

# 12. §11c's BLADE CLAIM IS WITHDRAWN. A HEAVIER BLADE DOES NOT MAKE THE TORNADO HIT HARDER — IT MAKES THE FIGHT SHORTER, AND THE TWO CANCEL EXACTLY.

§11 predicted a loop: bigger blade -> bigger memories -> every tick hits
harder. `tools/blade_sweep.py`, 320 fights an arm across the scythe row's real
range:

```
  blade    no ult   with tornado   ult worth   echo/fight   tornado dmg   pool sum
  17.25     10.6%          58.8%     +48.1pp         79.7         175.6       89.9
  21.00     29.4%          71.6%     +42.2pp         89.6         179.1      104.9
  24.00     35.3%          79.4%     +44.1pp         94.4         179.3      112.5
  27.00     53.8%          84.1%     +30.3pp         94.8         173.2      125.6
  31.35     60.0%          88.1%     +28.1pp        100.3         177.3      136.4
```

**CONTROL: the no-ult column must rise with the blade. PASS**, 10.6% to 60.0%.

**The pool does rise as predicted — 90 to 136 — and the echo with it, 80 to
100. And the tornado's total damage does not move at all: 176 to 177 across the
whole range.** A heavier blade kills faster, so there are fewer ticks, and the
richer echo is collected fewer times. The two effects cancel to within 1%.

> **THE PRACTICAL CONSEQUENCE IS THE OPPOSITE OF THE PREDICTION. The ultimate is
> worth MORE on a light blade** — +48.1pp at 17.25 against +28.1pp at 31.35 —
> because the blade alone already wins 60% of fights at the top of the range.
> A light blade with a strong ultimate is the composition this relic wants,
> and that is Bloodmirror's shape rather than Thornwake's.

---

# 13. "LETS CHANGE IT TO A ROLLING WINDOW OF THE LAST 3 HITS" — MEASURED. IT IS NEARLY A NO-OP FOR THE EXISTING GAME AND IT SPECIFICALLY BREAKS THE RELIC BEING DESIGNED IN THIS DOCUMENT.

**Rick, 2026-09-01.** The shipped rule keeps the three **biggest** blows ever
landed, forever. The proposal keeps the three **most recent**, whatever their
size. `tools/curse_fifo.py` installs it at runtime and measures it.

**UNIT CHECK — the rule change must be visible or nothing below it means
anything.** Three memories of 100 then three of 5:

```
    top3   after 3x100: [100, 100, 100]   after 3x5: [100, 100, 100]   sum 300
    fifo   after 3x100: [100, 100, 100]   after 3x5: [    5,   5,   5]  sum  15
    PASS
```

## 13a. THE PREDICTION THIS SESSION MADE WAS WRONG

The reasoning written before the run: v49 chose a small cap to narrow the gap
between a 5.6-blow flail and a 25.7-blow twinblade, so FIFO should invert that
— a weapon that hits often would flush its own pool and lose the channel.

```
    type           blows   POOL top3   POOL fifo   echo/blow top3   fifo   total echo top3   fifo
    greatsword      14.4        38.8        34.8             3.10   2.78                45     40
    twinblade       13.9        43.3        39.2             3.46   3.14                48     44
    warhammer        8.1        84.3        77.0             6.75   6.16                55     50
    scythe           7.2        85.4        81.4             6.83   6.51                49     47
    flail            5.7        44.0        43.1             3.52   3.45                20     20
    bow             14.6        58.6        51.4             4.69   4.11                68     60

    spread across weapons — top3: 20-68 (3.4x)    fifo: 20-60 (3.0x)
```

**Nothing inverts.** Pools drop 5–12% and the spread across weapons barely
moves. **The reason is that consecutive blows from one weapon are similar in
size** — a scythe's hits are all 25 to 35 — so "the last three" and "the
biggest three" are nearly the same three. FIFO only bites where hit sizes
differ sharply, and in the shipped game almost nothing does that.

## 13b. WHAT IT COSTS THE FOUR BUILT UMBRAL RELICS

```
    relic         ultimate       top3      fifo      move
    gravemourn    Revenant      52.0%     49.4%     -2.6pp
    nightfell     Deadfall      51.4%     46.8%     -4.6pp
    twinshade     Triplicate    48.9%     44.8%     -4.0pp
    shroudmaul    Grasp         54.3%     54.3%     +0.0pp
```

Small, all negative, and at ~350 fights an arm the first three sit at the edge
of the noise floor §10 established. **Shroudmaul at exactly +0.0 is a control
that came back right**: Rick ruled Grasp pool-independent on 2026-08-31, and a
change to the pool rule moves it by nothing at all.

## 13c. AND THE THING IT DOES BREAK IS THE TORNADO

`tools/tornado_fifo.py`, the tornado at its settled geometry, 320 fights an arm:

```
    rule  ticks apply?   ticks   echo/fight   tornado dmg   echo 1st tick   echo last tick   win
    top3  yes             15.2        102.6         178.4             4.8              9.5   89.1%
    top3  no              15.3        100.1         176.9             4.8              9.6   90.3%
    fifo  yes             17.4         47.0         134.1             4.7              3.4   78.8%
    fifo  no              15.4         98.7         175.7             4.7              9.2   89.4%
```

**CONTROL: under top-3 a memory of 5 is discarded, so push and no-push must
agree. 178.4 vs 176.9. PASS.**

**The first-tick and last-tick echo columns are the whole story.** Under the
shipped rule the echo *climbs* across a cast, 4.8 to 9.5, because the blade
keeps landing memories bigger than anything the tornado can push. Under FIFO it
*falls*, 4.7 to 3.4, because the tornado floods the pool with its own 5s and
evicts the blade's 50s.

> **A ROLLING WINDOW TURNS THE TORNADO INTO ITS OWN COUNTER.** Echo halves
> (103 -> 47), the ultimate loses a quarter of its damage (178 -> 134) and ten
> points of win rate (89.1% -> 78.8%). **Rick's own arithmetic predicted this
> exactly** — *"after 3 hits those 100 damage hits should have fallen off ... so
> the next tick gets +2.4 damage"* — it just was not the rule the engine had.
>
> **AND THE FIX IS ONE CLAUSE, NOT A RULE CHANGE.** `fifo / no` recovers
> everything: 98.7 echo, 89.4% win, indistinguishable from the shipped rule.
> **If the tornado's ticks collect the echo without applying curse, a rolling
> window costs this relic nothing.** The clause that has to go is the one §10
> already measured at +0.1 damage in 381.

## 13d. THE OPERATIONAL FLAG

`CLAIMS.md` has **`umbral × bow` — Gloamwire / Crossweave, BUILDING, Claude
Code, `tools/gloamwire_build.py`** open right now. A change to curse's core rule
lands underneath that build. Two design collisions in two days already cost two
relics' worth of work; **a rule change under a live build is the same failure
with a different shape.** If the window goes in, it should go in after
Crossweave lands, with its own claim and its own doc.

---

---

# 14. "HOW CAN IT POSSIBLY BE −52" — ONE CAST, TICK BY TICK, SAME FIGHT AND SAME SEED UNDER BOTH RULES

`tools/tick_trace.py`. thornwake vs dawnbringer, seed 13001, the first cast.
Identical contact, identical everything but the pool rule.

```
SHIPPED RULE — keep the three BIGGEST, forever
 tick      t     pool before   echo   deals    pool after the push of 5
    1  12.45            [34]      3       8                   [34, 5]
    2  12.68         [34, 5]      3       8                [34, 5, 5]
    3  12.90      [34, 5, 5]      4       9                [34, 5, 5]
    4  14.25     [35, 34, 5]      6      11               [35, 34, 5]
    5 .. 17          unchanged     6      11               [35, 34, 5]
   18  21.90    [38, 35, 34]      9      14              [38, 35, 34]

 ONE CAST: 18 ticks, 193 damage, 103 of it echo (53%)

ROLLING WINDOW — keep the three MOST RECENT
 tick      t     pool before   echo   deals    pool after the push of 5
    1  12.45            [34]      3       8                   [34, 5]
    2  12.68         [34, 5]      3       8                [34, 5, 5]
    3  12.90      [34, 5, 5]      4       9                 [5, 5, 5]
    4  14.25      [5, 5, 35]      4       9                [5, 35, 5]
    5  14.92      [5, 35, 5]      4       9                [35, 5, 5]
    6  15.15      [35, 5, 5]      4       9                 [5, 5, 5]   <- the 35 is evicted
    7 .. 15        [5, 5, 5]      1       6                 [5, 5, 5]

 ONE CAST: 15 ticks, 106 damage, 31 of it echo (29%)
```

> **THE ANSWER IS TICK 6.** The pool holds the blade's **35**. The tornado
> pushes a **5**. Under a rolling window the oldest entry is shifted out — and
> the oldest entry is the blade's 35. **The tornado has traded a 35-damage
> memory for a 5-damage one, and it does that on every tick.**
>
> By tick 7 the pool is `[5, 5, 5]` and stays there for the rest of the cast.
> The echo it collects falls from 6 to 1 and never recovers, because the
> tornado outpaces the blade: fifteen ticks in ten seconds against a scythe
> that lands eight blows in a whole fight.
>
> **193 damage becomes 106, in the same cast of the same fight.** It is not
> that applying curse costs 52. **It is that the tornado is the largest consumer
> of the curse pool in the game — sixteen hits a fight — and under a rolling
> window it is also the largest destroyer of it. It pays itself in its own
> small change.**
>
> **Under the shipped rule none of this happens**, because a memory of 5 is
> simply discarded once three bigger ones exist. Note the shipped trace holds
> `[35, 34, 5]` — the tornado's own 5 IS in there, harmlessly, occupying a slot
> the blade had not yet filled, contributing 0.4 of the 6. **On today's rule
> "each tick applies curse" is free and can stay in the design exactly as
> written.**


---

# 15. RICK IS RIGHT AND §9a IS WITHDRAWN. TICK RATE IS NOT A FREE KNOB — IT IS THE STRONGEST ONE IN THE RELIC, AND IT IS WHY A ROLLING WINDOW GETS WORSE THE MORE THE DESIGN LEANS INTO ITSELF.

**Rick, 2026-09-01:** *"but the ticks hit faster than the blades hit. much
faster. which means more activations of curses extra damage."*

**§9a called tick rate "pure feel, no balance". That is withdrawn.** It was
written while this document still believed the ticks fed the pool and were paid
once on release. On the `resolveHit` path **every tick collects the echo**, so
the tick rate multiplies the ultimate's damage directly. This is the second
thing in this session Rick has corrected from the design side against a
measurement that had not been run yet.

## 15a. THE LADDER AT A FIXED 5 DAMAGE A TICK

```
    ticks/s   ticks/fight   base dmg   echo dmg   total   echo share   the ult is worth
        1.5           6.3       31.6       46.4    78.0         59%            +18.8pp
        3.0          11.1       55.5       77.1   132.6         58%            +27.2pp
        4.5          14.9       74.7       98.2   172.9         57%            +30.0pp
        7.0          19.0       95.1      113.7   208.8         54%            +35.9pp
       10.0          23.3      116.6      125.5   242.1         52%            +37.2pp
       15.0          27.9      139.5      134.1   273.6         49%            +40.6pp
```

**A tenfold change in tick rate is worth 22 win points.** For comparison, the
entire blade range of the scythe row — 17.25 to 31.35 — is worth 49 points on
its own and moves the ultimate's lift by 20. **Tick rate belongs in the same
tier as the blade, and it was written down as a looks decision.**

## 15b. RICK'S CLAIM ISOLATED — AND THE CONTROL THAT FAILED

A second ladder held the cast's TOTAL base damage at ~100 and varied only how
many hits it was split into. **Its control failed**: the base drifted 95 to 134
because the expected-tick estimate that sets `base = total / expected` is only
approximate. The absolute numbers are therefore not quotable.

**But the ratio is immune to that drift, and the ratio is what the claim is
about:**

```
    ticks/s   base dmg   echo dmg   ECHO PER UNIT OF BASE DAMAGE
        1.5      134.5       34.1                           0.25
        3.0      123.4       60.2                           0.49
        4.5      120.5       83.1                           0.69
        7.0       95.1      113.7                           1.20
       10.0       98.0      136.2                           1.39
       15.0       96.4      160.8                           1.67
```

> **SPLITTING THE SAME DAMAGE INTO SIX TIMES AS MANY HITS MULTIPLIES THE ECHO
> IT COLLECTS BY 6.6x.** Not the damage — the same damage. The relic is a
> machine for converting hit COUNT into damage, on a school that pays per hit,
> and that is the sentence Rick wrote in his §1 before any of this was measured.

## 15c. AND IT SETTLES THE ROLLING WINDOW

```
    rule    ticks/s   ticks   echo/fight   echo PER TICK      win
    top3        4.5    14.7        102.6            6.99    87.5%
    top3       10.0    22.5        136.9            6.08    98.2%
    fifo        4.5    17.6         47.5            2.69    78.9%
    fifo       10.0    29.8         55.3            1.85    93.2%
```

**A rolling window does not reduce how often the tornado activates the echo —
it reduces what each activation is worth.** Going from 4.5 to 10 ticks a second
under FIFO buys 69% more ticks and only 16% more echo, because the per-tick
value collapses from 2.69 to 1.85. Under the shipped rule the same change buys
53% more ticks and 33% more echo, with the per-tick value nearly intact.

> **THE COST OF THE WINDOW SCALES WITH THE ENGINE.** At 4.5 ticks a second it
> takes 55 echo out of the relic. At 10 it takes 82. **The faster the tornado
> goes — the more it becomes the thing Rick designed — the more a rolling window
> charges for it.**

---

---

# 16. "HOW CAN IT POSSIBLY DO ANYTHING BUT BENEFIT THE RELIC" — UNDER THE SHIPPED RULE IT CANNOT, AND RICK IS RIGHT. UNDER A ROLLING WINDOW IT CAN, AND THE REASON IS THAT `shift()` DROPS THE OLDEST AND NOT THE SMALLEST.

`tools/push_monotone.py`, run against the real `Fighter.pushCurse` in the build
and against the proposed replacement, on the same starting pools:

```
SHIPPED RULE — push, sort descending, truncate to 3
       pool before  push       pool after   sum before   sum after   change
      [35, 20, 10]     5     [35, 20, 10]           65          65       +0
        [35, 5, 5]     5       [35, 5, 5]           45          45       +0
      [50, 38, 31]     5     [50, 38, 31]          119         119       +0
      [50, 38, 31]    50     [50, 50, 38]          119         138      +19
                                                    worst change:       +0

ROLLING WINDOW — push, shift the oldest out
       pool before  push       pool after   sum before   sum after   change
      [35, 20, 10]     5      [20, 10, 5]           65          35      -30
        [35, 5, 5]     5        [5, 5, 5]           45          15      -30
      [50, 38, 31]     5      [38, 31, 5]          119          74      -45
      [50, 38, 31]    50     [38, 31, 50]          119         119       +0
                                                    worst change:      -45
```

> **THE ANSWER IS THAT THE TWO RULES DIFFER IN KIND, NOT IN DEGREE.**
>
> **The shipped rule is monotone.** `sort` then `truncate` means a value too
> small to belong is discarded and nothing is lost. **Applying curse can only
> help or do nothing, ever, at any pool size — worst case across every trial is
> +0.** Rick's intuition is exactly correct for the game as it stands.
>
> **A rolling window is not monotone.** `shift()` removes the OLDEST, and the
> oldest is not the smallest. Pushing a 5 onto `[50, 38, 31]` yields
> `[38, 31, 5]` and the pool falls by 45. **The push is not an addition, it is a
> REPLACEMENT, and what it replaces is chosen by arrival time rather than by
> size.**
>
> That is the whole of §13 and §14 in four lines. It is not that curse behaves
> oddly for the tornado; it is that a recency rule makes every push a trade, and
> Scour's ticks are the smallest things on the board making that trade twenty
> times a cast.
>
> **And the last row matters too:** even a GOOD push is worth less under a
> window. Pushing 50 onto `[50, 38, 31]` is +19 under the shipped rule and +0
> under the window.

---

# 17. THE SHIPPING CONFIGURATION, MEASURED WHOLE — AND IT COMES IN HOT

Every table before this one moved one axis with the others at defaults: the
rate ladder ran on Thornwake's 31.35 blade, the blade sweep at 4.5 ticks a
second. **The combination Rick settled had never been run.** 986 fights an arm,
against all 29 other relics:

```
    blade 21 · 7 ticks/s · base tick 5 · 160 wide · 10s casts · ticks apply curse

    arm                            win     ticks    base    echo   total   per cast
    no ultimate                  26.6%       0.0     0.0     0.0     0.0        0.0
    SCOUR, ticks apply curse     82.4%      22.8   113.8   112.2   226.0      113.0
    SCOUR, ticks do not apply    81.7%      23.2   115.8   109.4   225.1      112.6

    SCOUR IS WORTH +55.8pp        of which the apply clause is +0.6pp — noise
```

**CONTROL: `blade_sweep` put a 21 blade with no ultimate at 29.4%; this run,
different seeds and a different code path, says 26.6%. PASS.**

**AND THE APPLY CLAUSE IS CONFIRMED FREE AT THE SHIPPING NUMBERS.** +0.6pp
against a ~4.3pp error bar. It stays in, exactly as Rick's §1 wrote it.

> **THE FLAG: +55.8pp WOULD MAKE SCOUR THE STRONGEST ULTIMATE IN THE GAME.**
> Crossweave measured +48.8 and was second only to Harrowing. Scour at this
> configuration clears both. The cast delivers **113 damage against a budget of
> 100**, and it does it twice.
>
> **This is not a mistake in the design — it is the two knobs Rick raised in the
> same breath.** 4.5 to 7 ticks a second was measured at +6pp on its own, and
> the blade moved from Vesper's weight to Bloodmirror's. Together they land
> above the field. **The trim, if he wants one, is one number:** 7 ticks at base
> **4** is 90 a cast, or 4.5 ticks at base 5 is 87 — either lands Duskreave
> beside Crossweave rather than above Harrowing.

---

# Open decisions

**ALL FIVE ITEMS BELOW WERE RESOLVED LATER ON 2026-09-02 — see `../v63/DUSKREAVE-BUILD-BRIEF.md`.** Rick kept 7 ticks/s (+59), ruled the last-3 window in (after Gloamwire; Scour then ~+40), gave the card line, sent an animation reference, and left the sound to a rendered spread.

**Rewritten 2026-09-02 by v63.** The block this replaces was written before
§14–§17 and its item 2 asked whether the ticks should apply curse at all —
"the ticks should COLLECT and not APPLY." **That is not open.** Rick ruled it
three times over, §17 measured the apply clause free (+0.6pp), and the relic
ships with both, as his §1 wrote it. The blade (item 3) and the names (item 5)
were also settled after the block was written: 21, Duskreave, Scour.

1. **THE TRIM.** §17, and `../v63/duskreave-check-v63.md` §3 for the corrected
   number and a priced ladder. Scour measures above every ultimate in the game.
   Trim, or accept it as the strongest. Rick's.

2. **THE ROLLING WINDOW.** §13–§16. Nearly a no-op for the shipped game, and it
   costs this relic a quarter of its damage because its ticks apply curse — and
   Rick has ruled that the ticks apply curse. Not ruled. Should not land under
   Code's live Gloamwire build in any case (§13d).

3. **THE CARD, THE ANIMATION, THE SOUND.** Rick's, all three. Blank.

4. **THE `resolveHit` NOTE IS NECESSARY AND NOT SUFFICIENT.** §11c said the
   ticks must go through `resolveHit` for the echo. v63 §4 adds what
   `resolveHit` ALSO does on every call — knockback away from the caster,
   hit-stop that freezes the world, hit-stun, a director beat — none of which a
   7-tick-a-second drag can carry. The brief has to say which parts of the
   pipeline a tick takes and which it must not.

5. **OUTCOME COLUMNS NEED n>=300 IN THIS ENGINE.** §10. Still true.

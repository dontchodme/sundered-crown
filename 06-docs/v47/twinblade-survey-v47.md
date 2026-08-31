# v47 — THE TWINBLADE ROW, SURVEYED. The most live edge in the game, turned the least efficiently, on a weapon that loses every bind it takes.

**2026-08-30, Cowork.** Rick: *"lets get started on another fighter. this time
lets design and plan here and let code build it."* So the split is explicit:
this document and the design beside it are the plan; `tools/` carries the two
instruments; Claude Code builds.

`tools/twinblade_survey.py --game ../02-chain/sc-paradox-ignition.html`

```
cell_survey        7/7      the grid re-measured on the live tip — 17 cells open
verify --n 40     12/13     12000 fights, the known thirteenth (duration band)
twinblade_survey  12/12     [1] and [6]
                   3/3      [2] two blades, and the control that refuted the framing
                   2/2      [3] the clank ladder
                   2/2      [4] entangle by the foe's mode
                   1/1      [5] the four open channels, against the whole roster
```

**Nothing was carried from the project record.** `pace_build.py` moved the
simulation — baseHP 400, seals 21/49, Grudgebearer nerfed — so every v43-era
number was stale and the grid, the win rates and the channels were all
re-measured at `sc-paradox-ignition.html`.

---

# 0. THE GRID, ON THE LIVE TIP

25 relics, 7 schools x 6 types, **17 cells open**.

```
                     bow       flail  greatsword      scythe   twinblade   warhammer   school
bloodsworn    Marrowdraw   Threshmaw   Goreshard           ·  Widowmaker           ·      4/6
dwarven         Ironhail   Slagheart   Emberedge           ·           · Grudgebearer     4/6
runic                  ·     Paradox       Axiom    Foregone Spellbreaker           ·     4/6
sanctified       Aureole           · Dawnbringer   Lastlight           ·      Censer      4/6
umbral                 ·  Gravemourn   Nightfell           ·   Twinshade           ·      3/6
verdant        Vinesower           ·   Heartwood   Thornwake           ·           ·      3/6
vigil          Farwarden           · Lightkeeper           ·           ·   Bulwarden      3/6
type                   5           4           7           3           3           3
```

**The double-gap heuristic has something to say for the first time in three
sessions.** Three schools sit at 3 and three types sit at 3, and six of those
nine intersections are open. Rick took **verdant x twinblade** from four
priced candidates.

The 40-seed re-price, for the record — the roster after the pace change:

```
school mean      type mean
dwarven    53.8   warhammer   54.0
sanctified 53.6   flail       52.2
vigil      51.1   bow         51.8
runic      48.9   scythe      50.9
bloodsworn 47.6   twinblade   48.5
umbral     47.6   greatsword  46.0
verdant    46.2
```

**Verdant is the weakest school in the game and the twinblade is the
second-weakest type.** Vinesower 44.6% and Heartwood 44.2% are two of the four
lowest relics on the board. That does not make the cell wrong — a new relic's
blade is bisected to ~50% regardless — but it sets what the ultimate has to do.

---

# 1. THE TYPE'S BLOCK

```
type          reach  width   spin   mass  blades    mode   arc          dmg
bow              54      9    2.8    1.6     [0]  ranged     -    12.7-16.2
flail            96     22    2.2    3.6     [0]   chain     -    25.0-44.1
greatsword      116     14    3.4    3.0     [0]   swing   1.5     7.4-15.8
scythe          104     11    3.2    2.4     [0]    spin     -    17.5-31.4
twinblade        62      8    5.7    1.1  [0,0.5]   spin     -     8.3-11.9
warhammer        76     26    1.6    5.0     [0]    spin     -    20.1-28.8
```

Four ladders, and the twinblade is at one end of all four: **the lightest, the
fastest, the shortest of the melee types, and the lowest damage ceiling in the
game.** The single softest blow belongs to Axiom (7.42, a greatsword) — the
twinblade is low by its ceiling, not by its floor, and that check was written
the other way round and had to be corrected.

---

# 2. THE MOST LIVE EDGE IN THE GAME, TURNED THE LEAST EFFICIENTLY

Read off `bladeSegments` — the function the hit test actually calls — over real
fights at pinned damage with ultimates suppressed:

```
type         blades  live blade  total edge  contacts/s  per blade  cooling   rad/s  contacts/rad
bow               1        60.9        60.9       0.123        219       8%    3.17        0.0388
flail             1        13.2        13.2       0.189        313      11%    2.65        0.0713
greatsword        1       127.5       127.5       0.286        584      17%    3.90        0.0733
scythe            1       115.8       115.8       0.234        526      14%    3.84        0.0609
twinblade         2        69.8       139.6       0.273    278/263    8%/8%    6.47        0.0422
warhammer         1        85.5        85.5       0.204        452      12%    1.91        0.1068
```

**139.6 units of live edge — more than the greatsword's 127.5 — on the shortest
reach in the game.** Delivered as two opposed 70-unit segments, each with its
own independent 0.45s `hitCd`, and both of them land: 278 against 263 blows, so
the weaker blade carries 48.6% of the type's contacts.

**And it is the least efficient melee weapon in the game per radian turned.**
0.0422 contacts a radian against a warhammer's 0.1068. It turns 3.4x as fast as
a warhammer to land 1.34x the blows.

## 2.1 THE SECOND BLADE IS NOT THE TWINBLADE'S — IT IS SPIN MODE'S

This section was written to say "two blades is what makes this type." **The
control refuted it**, which is the only reason the control was there.

```
arm                           contacts/s   dealt/s   taken/s  clanks/min    win
twinblade  [0, 0.5]  ships         0.273      5.57      4.25        21.2  85.0%
twinblade  [0]       one           0.158      3.60      5.95        14.2  25.0%
greatsword [0]       ships         0.286      5.89      4.53        24.5  82.5%
greatsword [0, 0.5]  two           0.307      6.17      3.76        25.4  92.5%
scythe     [0]       ships         0.234      5.15      5.69        17.7  30.0%
scythe     [0, 0.5]  two           0.388      7.85      3.73        25.4  92.5%
warhammer  [0]       ships         0.204      5.36      5.77        16.7  30.0%
warhammer  [0, 0.5]  two           0.383      9.85      3.33        24.7  95.0%

a second opposed blade is worth      twinblade  x1.73   spin
                                     scythe     x1.65   spin
                                     warhammer  x1.87   spin
                                     greatsword x1.07   swing
```

**A second opposed blade is worth x1.65-1.87 to any SPINNING weapon and x1.07
to a swinging one**, and the twinblade is the middle of the three spin arms.
The gain belongs to full rotation: `mode:"swing"` recomputes `theta` from the
AIM every frame, so an opposed blade points away from the quarry for most of
the arc. None of them doubles, because `hitCd` is per segment at 0.45s and the
two blades share passes.

**So what makes the twinblade the twinblade is not the second blade.** The
second blade is what buys back the shortest reach in the game: it lifts contact
rate to 0.273, within 5% of a greatsword's 0.286, on a weapon covering a
fraction of the ground.

---

# 3. IT LOSES EVERY BIND IN THE GAME

Outcome read off the EFFECT — whose `spinDir` reversed, who ate the stagger —
and the mass model's exponent and threshold read out of the shipped
`resolveClank.toString()` rather than copied (v43 §12's rule):

```
foe           type          mass  margin   thr  clanks/min    won  deadlock   lost  stagger eaten
ironhail      bow            1.6  0.3081  0.16        16.5     0%        0%   100%         0.071s
lastlight     scythe         2.4  0.5804  0.16        23.9     0%        0%   100%         0.115s
emberedge     greatsword     3.0  0.6925  0.16        29.2     0%        0%   100%         0.122s
gravemourn    flail          3.6  0.7648  0.16        19.0     0%        0%   100%         0.117s
censer        warhammer      5.0  0.8583  0.16        16.7     0%        0%   100%         0.108s
spellbreaker  twinblade      1.1  0.0000  0.16        28.0     0%      100%     0%         0.062s
```

**100% lost against every other type, and the only bind it does not lose is the
mirror, which is 213/213 deadlocks.** The flail misses a greatsword win by six
thousandths (v43 §12); the twinblade misses every one of them by 0.15 to 0.70.

This is the sharpest version of the mass ladder anywhere in the game, and it is
the fact the ultimate's first sentence turns out to interact with — see the
design doc §1.

---

# 4. ENTANGLE IS NOT A FLAT CHANNEL. IT IS A MATCHUP CHANNEL.

`spinMul` multiplies `tickWeapon`'s `spin` for every mode — but a bow's CADENCE
is `tickFire`'s `S.cadence` and never reads spin. So the hypothesis was that
entangle is worth much less against ranged. It is worth **nothing** against
ranged.

Verdant grafted onto the donor, channel live against channel deleted, four foes
per mode:

```
foe mode     n   foe blows/s off->on   change   taken/s off->on   change
ranged       4        0.265 -> 0.268      +1.2%      5.52 -> 5.68     +2.8%
swing        4        0.275 -> 0.223     -18.9%      6.98 -> 5.59    -19.9%
spin         4        0.178 -> 0.164      -8.3%      4.05 -> 3.71     -8.4%
chain        4        0.132 -> 0.139      +5.0%      3.20 -> 3.05     -4.6%
```

And the CEILING — the same ladder held at cap, which is what an ultimate that
pinned it would be buying. The forced arm is verified against the status table:
with the act modifier divided out and desperate frames dropped it reads
**0.480 against a predicted 1 + (-0.13 x 4) = 0.480**, and the unentangled
control reads 1.000.

```
foe mode     foe blows/s off -> cap   change   taken/s off -> cap   change
ranged            0.265 -> 0.274       +3.3%        5.55 -> 5.60     +1.0%
swing             0.276 -> 0.184      -33.1%        6.97 -> 4.58    -34.2%
spin              0.178 -> 0.150      -16.0%        4.04 -> 3.49    -13.7%
chain             0.132 -> 0.119       -9.9%        3.20 -> 2.71    -15.2%
```

**A third of a greatsword's output at cap, a sixth of a spinner's, a tenth of a
chain's, and nothing at all against a bow.** Seven greatswords, five bows: this
channel is concentrated, and any relic built on it will have a wide win-rate
spread across the roster by construction.

---

# 5. THE CELL, RE-PRICED — AND OCCUPANCY HAS NOW MISPRICED A THIRD CELL

One A/B per channel, live against the same weapon with the channel deleted,
**against all 24 other relics** rather than a five-relic field — because §4
showed the worth is decided by the foe's mode, and a foe field that misweights
the modes decides the table by itself:

```
school      status      dealt/s   taken/s     win     vs no channel at all
dwarven     sunder         7.84      4.57   78.1%          +17.0%
sanctified  smite          5.82      4.87   69.8%           +8.7%
verdant     entangle       6.91      4.78   68.8%           +7.6%
vigil       ward           6.60         —       —   bank readout only
```

`cell_survey` ranked verdant x twinblade **the busiest open cell on the board**
— 0.318 hits/s, 18.8 applications a fight, 59% of the fight at two or more
stacks, 37% at cap. By delivered effect it is **the weakest of the three foe
channels on its own type.**

**That is the third cell the occupancy column has mispriced** — the umbral row
(v40 §4.1), runic x flail (v43 §4), and now this one. It is a rate-and-matchup
proxy being read as a quantity, for the third session running, and **the tool
still does not say so in its own output.** This is now a standing defect in
`cell_survey.py` rather than a surprise, and it should either grow a delivered-
effect column or stop printing occupancy as if it ranked anything.

**What it means concretely: the school's channel will not carry this relic, so
the ultimate has to.** Same position the Stasis Field was in, where the ult was
measured worth about nine points of blade.

---

# 6. THE TRAPS, ASSERTED

- Each blade carries its own `hitCd`, indexed by segment.
- A stunned twinblade lands nothing — `tickHits` skips on `self.stun`.
- Both segments are rigid functions of `f.theta`. Unlike the flail there is no
  lag term: `|headAng - theta|` has no analogue here.
- `_clankPair` CONTINUES past a buried blade rather than returning, so one
  blade being blocked cannot mask the other genuinely crossing.
- `tickFire`'s cadence never reads spin — entangle cannot slow a bow's rate of
  fire, and §4 is that fact arriving as a measurement.
- Entangle reaches the weapon through `spinMul`, which floors at 0.15.

---

# Open decisions

1. **`cell_survey`'s occupancy column has now mispriced three cells.** §5. It
   is the wrong readout for a status that is a rate, and worse for one whose
   value depends on the foe's mode. Chain-wide, and Rick's call whether the
   tool grows a delivered-effect column or loses the ranking claim.
2. **VERDANT IS THE WEAKEST SCHOOL IN THE GAME AT 46.2%** and two of the four
   lowest relics on the board are verdant. New. Nothing in the project has
   looked at the school as a school since the pace change.
3. **THE GREATSWORD IS THE WEAKEST TYPE AT 46.0% AND CARRIES SEVEN RELICS** —
   28% of the roster in the type that wins least. New, and it interacts with
   §4: greatswords are also what entangle hurts most.
4. **A SECOND OPPOSED BLADE IS WORTH x1.65-1.87 TO ANY SPIN-MODE WEAPON.** §2.1.
   Nothing in the game uses that except the twinblade, and the finding says the
   twinblade is not special for it — it is available to the scythe and the
   warhammer for the asking.
5. **Every type-level measurement still wants a `--noult` pass.** v38 od 5
   through v43 od 9, unmoved. This survey suppresses ultimates by setting
   `charge` to 1e9, which is the same workaround the last four used.

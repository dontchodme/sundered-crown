# v59 — WHAT A RELIC IS MADE OF. v57's open decision 1 asked why the two strongest open cells keep being declined; the answer is that the ranking column measures the wrong half of a relic, and the half nobody has measured is whether the ultimate and the school's status FEED each other. The registered prediction that got this session started came back refuted at r = +0.08, and the thing that replaced it is better.

**2026-09-01, Cowork.** `budget_probe.py` (four arms x 27 relics) and
`cell_price.py`, both new, both runtime-only, against
`02-chain/sc-nightfell.html` — the build of record, 27 relics, neither
Shroudmaul nor Cindercleave in it. ~28,000 fights. Nothing is written to any
build.

**THE HARNESS CONTROL, run first, per the repricing's open decision 4.** This
session is Chromium **141.0.7390.37** — byte-identical to the v57 session, so
every number here is directly comparable with that document and with nothing
older. `docs/RUNTIME-DRIFT.md` still applies to anything rendered on the repo's
pinned 151.

Two further controls, both green before anything below was read:

```
determinism   dawnbringer and widowmaker were measured twice, once in a
              two-worker split and once single-process, and returned
              53.8/28.4/36.5 and 45.7/41.3/21.2 both times. Identical
the graft     thornwake rebuilt from parts — verdant deleted and re-grafted,
              Bramblesnare live — comes back 47.7% against the real relic's
              48.1% at 260 fights. The injection reproduces the relic
```

---

# 0. THE NUMBERING IS OFF BY ONE AND IT HAS PROPAGATED

`06-docs/v43` calls Paradox the twenty-fifth relic. `v48/scythe-survey` calls
Vesper's cell *"the 27th relic's plan"* and `02-chain/sc-vesper.html`'s own
header says **27 relics**. The build of record has **27**. So Thornshear is 26,
Vesper is 27, and v56 is right that **Shroudmaul is the 28th**.

**Cindercleave is therefore the 29th, not the 30th**, and
`cindercleave-design-v57.md`'s title says 30th. The relic Rick is picking now
is the **30th**. One line, three documents and a memory note, and it costs
nothing to fix except that nobody notices it while it keeps being copied.

---

# 1. THE MEASUREMENT

Every built relic played the whole roster four ways, paired on (foe, seed),
26 foes x 8 seeds = 208 fights an arm:

```
A   shipped                everything live
B   no ultimate            this relic's charge -> 1e9
C   no channel             this relic's onHit and onSelf deleted
D   neither                both, so the channel can be read WITHOUT its ultimate
```

`A - C` is the channel's worth **to the finished relic**. `B - D` is the same
channel's worth **with the ultimate switched off**. The gap between them is the
only new quantity in this document and it is the whole finding.

## 1.1 THE REGISTERED PREDICTION, AND IT IS REFUTED

Written down before the probe reached its third relic:

> *Every relic is bisected until it lands near the field, so channel + ultimate
> + blade is a fixed total. A cell whose channel delivers a lot is a cell with
> less room for an ultimate.*

```
r(chanShare, ultShare) over all 27   =   +0.082
```

**Nothing. Not weakly negative — nothing.** Gravemourn has the second-largest
channel in the game AND the third-largest ultimate. The crowding story is dead
and the cell table cannot be rescued by it.

The prediction's own falsifier also fired: shipped win rates span **38.5%
(Heartwood) to 60.1% (Marrowdraw)**, mean 50.9%, sd 5.5. The stated red line
was "more than ~20 points" and it is 21.6. **The roster is levelled to a band,
not to a point**, and any argument that treats the total as fixed is arguing
from a 21-point interval.

---

# 2. WHAT IS ACTUALLY THERE — THE ULTIMATE FEEDS THE STATUS, OR IT DOES NOT

```
relic         school      type        ship   CHAN    ULT   CHAN alone  FEED   ultimate
gravemourn    umbral      flail      54.8%  +47.6% +39.9%      +8.7%  +38.9  Revenant
twinshade     umbral      twinblade  51.9%  +28.8% +44.7%      +6.7%  +22.1  Triplicate
vesper        vigil       scythe     59.6%  +38.0% +40.9%     +17.3%  +20.7  Sentinel
oathwound     bloodsworn  greatsword 44.7%  +34.6% +22.1%     +16.3%  +18.3  Bloodprice
nightfell     umbral      greatsword 47.1%  +31.2% +15.4%     +15.9%  +15.4  Deadfall
axiom         runic       greatsword 43.8%  +38.5% +19.7%     +23.6%  +14.9  Corollary
vinesower     verdant     bow        53.8%  +23.1% +29.8%      +8.2%  +14.9  Thicket
marrowdraw    bloodsworn  bow        60.1%  +33.2% +22.1%     +21.2%  +12.0  Bloodhunt
redflail      bloodsworn  flail      46.2%  +17.3% +30.8%      +6.3%  +11.1  Bloodmill
spellbreaker  runic       twinblade  46.2%  +32.2% +20.7%     +24.5%   +7.7  Unmaking
lastlight     sanctified  scythe     51.4%  +14.4% +41.3%      +6.7%   +7.7  Harrowing
thornwake     verdant     scythe     48.1%   +3.8% +12.0%      -3.4%   +7.2  Bramblesnare
grudgebearer  dwarven     warhammer  55.3%  +20.7% +24.0%     +14.4%   +6.3  Crucible
aureole       sanctified  bow        54.3%  +23.1% +18.3%     +16.8%   +6.2  Benediction
ironhail      dwarven     bow        58.7%  +29.3% +17.8%     +24.0%   +5.3  Quarrelstorm
censer        sanctified  warhammer  52.9%  +19.7%  +9.1%     +14.4%   +5.3  Consecration
thornshear    verdant     twinblade  42.3%  +16.8% +17.3%     +12.0%   +4.8  The Winnowing
heartwood     verdant     greatsword 38.5%  +16.8%  +8.2%     +13.5%   +3.4  Rootfast
lightkeeper   vigil       greatsword 44.7%  +35.1%  +4.3%     +33.7%   +1.4  Bulwark
foregone      runic       scythe     52.4%  +12.5% +25.5%     +12.5%   +0.0  Converse
farwarden     vigil       bow        57.2%  +49.0%  +2.9%     +49.5%   -0.5  Reprisal
paradox       runic       flail      55.3%  +11.1% +22.6%     +13.0%   -1.9  Stasis Field
emberedge     dwarven     greatsword 49.5%  +28.4%  +3.4%     +32.2%   -3.8  Slagburst
bulwarden     vigil       warhammer  51.4%  +25.0% +13.0%     +28.8%   -3.8  Aegis
slagheart     dwarven     flail      55.3%   +5.3%  +7.7%      +9.6%   -4.3  Ironbloom
dawnbringer   sanctified  greatsword 53.8%  +17.3% +25.5%     +22.1%   -4.8  Daybreak
widowmaker    bloodsworn  twinblade  45.7%  +24.5%  +4.3%     +31.2%   -6.7  Exsanguinate
```

**The top of that column is every ultimate in the game that applies or spends
its own school's status, and the bottom is every one that ignores it.** Nobody
arranged this; the column was computed and then read.

- **Revenant's hands apply curse.** Curse on the flail is worth +47.6% with the
  ultimate running and **+8.7% without it**. Thirty-nine points of what looked
  like a channel is an ultimate.
- **Triplicate** puts three cursing bodies in the hall, **Sentinel** drinks the
  ward, **Bloodprice** and **Corollary** each apply three stacks, **Thicket's**
  vines entangle. All top eight.
- **Exsanguinate is a nova that also applies three Hemorrhage** — and it is the
  WORST feed in the game at −6.7. Applying the status in a burst is not feeding
  it. Widowmaker's bleed is worth MORE with its ultimate switched off, because
  the ultimate spends time not swinging.
- **Slagburst and Crucible consume their stacks**, so deleting the channel
  costs them less, not more. Spending is not feeding either.

> **A cell's ranking has never included this, and it is the difference between
> a fighter that reads as one idea and a blade with two accessories bolted on.**
> It is also the only column in this project that separates the four relics
> Rick has been happiest with from the four he has not mentioned since.

## 2.1 AND IT IS WHY THE OLD COLUMN CANNOT BE READ AS QUALITY

`row_price`'s lift adds a channel to a body that was tuned WITHOUT it.
`A - C` deletes a channel from a body that was tuned AROUND it. Two cells have
now been measured both ways:

```
cell                     donor lift, before it was built   shipped channel share
verdant x twinblade      +7.6%   (v47)                     +16.8%
vigil x scythe           +19.2%  (v48)                     +38.0%
```

**Both about 2x.** Two points is two points and nobody should build on it, but
it is the only calibration the project has ever had between the column it picks
cells with and the thing that column is supposed to predict. Register it and
add to it every time a cell is filled.

---

# 3. THE VIGIL PAIR — v57's OPEN DECISION 1, CLOSED, AND RICK WAS RIGHT

The instruction was: *either they are next, or the ranking column needs a second
axis that explains why they are not.* Here is the axis, and it is not the one
this session went looking for.

```
school      status      channel ALONE, fastest type -> slowest        swing
vigil       ward        bow +50%  grea +34%  warh +29%  scyt +17%    -32.2pp
bloodsworn  hemorrhage  bow +21%  grea +16%  twin +31%  flai  +6%    -14.9pp
dwarven     sunder      bow +24%  grea +32%  warh +14%  flai +10%    -14.4pp
verdant     entangle    bow  +8%  grea +13%  twin +12%  scyt  -3%    -11.5pp
runic       hex         grea +24% twin +25%  scyt +12%  flai +13%    -10.6pp
sanctified  smite       bow +17%  grea +22%  warh +14%  scyt  +7%    -10.1pp
umbral      curse       grea +16% twin  +7%  flai  +9%               -7.2pp
```

**Ward is the most weapon-speed-sensitive status in the game by a factor of
two.** `vigil x twinblade`'s celebrated +50.0pp is not a strong cell — it is
ward measured on the fastest weapon in the game, which is where ward always
looks biggest. The column has been reporting the same fact about vigil four
times and reading it as four discoveries.

And the design half is worse. **Three of vigil's four ultimates already spend
the banked shield** — Aegis reflects it, Reprisal fires it, Sentinel drinks it.
A fourth vigil cell has the most crowded ultimate space on the board, not the
richest. Rick declined those cells three times without being able to name why,
and the naming took 28,000 fights.

> Both vigil cells stay open and should stop being offered as *"the strongest
> open cells in the game."* They are the two cells where the most of the
> fighter is decided before anybody designs it.

## 3.1 THE CONTACT-RATE LAW SURVIVES ITS OWN CONTROL

v57 (Cindercleave §1) found delivered lift falling off a cliff once a type's
contact gap exceeds its status's duration, on one row. Across all 24
decaying-channel relics, with the ultimate suppressed so no feed can flatter it:

```
r(contact gap, channel alone)   =   -0.530
```

Independent instrument, whole grid, same sign. **That one is real.**

## 3.2 AND THE CURSE PREDICTION IS REFUTED

Registered before the data: *curse has `dur` 99 and cannot decay, so it should
be the one channel that gets STRONGER on a slow weapon.* The raw column looked
like a triumph — umbral's flail at +47.6% against dwarven's +5.3% on the same
type — and **arm D killed it.** With the ultimate off, curse on the flail is
+8.7%, greatsword +15.9%, twinblade +6.7%: still the flattest school in the
grid at −7.2pp, which is what `dur` 99 predicts, but flat at a LOW level and
NOT rising with weight. **The inversion was Revenant, not curse**, and without
the fourth arm this document would have recommended a cell on it.

---

# 4. THE 30th RELIC — bloodsworn x scythe

Four cells were offered with the feed axis attached. Rick took **bloodsworn x
scythe**, over `verdant x warhammer` (the recommendation), `runic x warhammer`
and `vigil x twinblade`.

`cell_price.py`, Thornwake standing in, whole roster as foes with **their own
ultimates live** — see §4.1, this is not the world `row_price` measures in —
260 fights an arm:

```
arm                                        win     hits
no channel, no ultimate                  38.8%      7.9
  + hemorrhage                           48.8%      7.2    +10.0
  + Bramblesnare instead                 43.1%      8.0     +4.3
  + both                                 61.2%      7.3    +22.4   parts add to 14.3
controls
  entangle + Bramblesnare (= thornwake)  47.7%      8.0    real relic is 48.1%
  curse, no ultimate                     42.7%      7.2     +3.9
  sunder, no ultimate                    43.5%      7.4     +4.7
  ward, no ultimate                      67.7%      8.5    +28.9
```

**Bleed is the strongest foe channel available on this weapon** — more than
twice curse or sunder, beaten only by a shield that is already Vesper's. The
cell was ranked third of four going in and the number says Rick picked the
strongest one on the board.

**And `w.aff` is inert.** Setting the donor's affinity to bloodsworn versus
leaving it verdant returns 43.1% both times, bit for bit. The field is
cosmetic; every tool in `tools/` that sets it has been setting nothing.

## 4.1 EVERY CELL THIS PROJECT HAS EVER PRICED WAS PRICED IN A WORLD WITH NO ULTIMATES

`cell_price.py` put the scythe row's no-channel floor at **43.1%** where
`cell-repricing-v57.md` §2 says **52.7%**. That read as a 9.6-point
disagreement between two tools on one build. **It is not a disagreement. It is
a different world, and the world is the finding.**

`row_price.CH2_JS` takes a `noult` flag, and `row_price` passes it **true in
both arms** — and it applies to `pinIds`, which is every weapon in the game,
not just the donor. Reproduced here to the decimal:

```
thornwake, channel deleted, 260 fights
  EVERY relic's ultimate suppressed         52.7%   <- row_price's floor, and v57's
  only the DONOR's ultimate suppressed      43.1%
  hemorrhage, every ultimate suppressed     66.9%   <- row_price's ON arm, exactly
```

`row_price --type scythe --pin 0` was re-run this session and returns
bloodsworn +14.2%, dwarven +11.2%, umbral +7.3% — v57's table, unchanged. The
arithmetic is honest inside its own world and the cross-row floor argument in
v57 §2 stands as written.

**But the world has no ultimates in it, and no document that quotes the column
says so.** Two consequences:

- **The number moves.** Hemorrhage on the scythe is +14.2pp with the field's
  ultimates off and **+18.1pp with them on** (61.2 against 43.1). Not enormous,
  not nothing, and never measured before.
- **It is blind to §2 by construction.** The only new axis in this document is
  whether an ultimate feeds a channel. `row_price` computes every cell in a
  world where no ultimate exists anywhere. **It cannot see the feed at all** —
  and that is a better answer to *"why has this column never explained Rick's
  picks"* than anything in §3.

> An earlier draft of this section reported the 9.6 points as a defect in one
> of the two tools. That was wrong, it was published for about twenty minutes,
> and the thing that caught it was reading `row_price`'s call site instead of
> its docstring. **A tool's flags are part of its result.**

## 4.2 THE CONSTRAINT THE DESIGN HAS TO SOLVE

```
smite       { maxStacks: 4, dur: 3.2, dps: 1.5 }
hemorrhage  { maxStacks: 4, dur: 3.2, dps: 1.5 }
```

**Byte-identical apart from the name.** The only difference anywhere in the
game is that bloodsworn applies **2 per hit** where sanctified applies 1. And
Lastlight — sanctified's scythe — is already on this row.

So the 30th relic's status is Lastlight's status at double rate, on Lastlight's
weapon. Nothing in the numbers separates them. **The ultimate is the entire
separation**, and that is the sentence the §1 has to answer.

Two adjacencies, named before anything is designed:

```
BLOODSWORN'S FOUR ULTIMATES ALL SHOOT SOMETHING
  Bloodmill throws spikes · Bloodhunt fires homing bolts ·
  Exsanguinate is a nova · Bloodprice is a beam.  Four for four
THE SCYTHE ROW CONTAINS NO BURST AT ALL
  Converse leaves sigils and rewinds · Harrowing sprays scythes that stick
  and burst · Bramblesnare roots · Sentinel sweeps a slow beam ·
  Breach tears wall vents
```

The two halves of this cell pull opposite ways. **Whichever one the §1 breaks
is the thing that makes the relic new**, and §2's table says the ones that pay
are the ultimates that feed the status rather than deliver it in a lump —
Exsanguinate applies three Hemorrhage in a burst and is the worst feed measured.

---

# 5. WHAT NOT TO DO WITH THIS DOCUMENT

- **Do not read §2's FEED column as a design target on its own.** It is a
  correlation over 27 points with no control for what else those ultimates do.
  It says the question is worth asking at the cell stage; it does not say a
  bigger number is a better relic.
- **Do not quote the donor lift and the shipped channel share as one quantity.**
  §2.1. They differ by about 2x on the two cells where both exist.
- **Do not compare a `row_price` number with a shipped win rate.** §4.1. The
  first is measured with every ultimate in the game switched off.
- **Do not treat 21.6 points of shipped spread as a levelled roster.** §1.1.
- **Nothing here has been seen in motion**, because nothing here is about
  motion. The standing item still stands for everything that is.

---

# Open decisions

1. **THE §1 FOR THE 30th RELIC.** Rick's, and everything downstream waits on
   it. §4.2 is the constraint it has to answer: this relic's status is
   Lastlight's at double rate on Lastlight's weapon.

2. **SHOULD `row_price` PRICE CELLS WITH THE FIELD'S ULTIMATES ON?** §4.1. Off
   is a defensible choice — it isolates the channel from 27 confounders — but
   it is an unstated one, it moves this cell's number by 3.9pp, and it is the
   reason the column has never been able to see §2. At minimum the tool should
   print `noult` in its own header. At most it should run both arms and report
   the gap, which is the feed, for a cell that does not exist yet.

3. **`w.aff` IS INERT AND EVERY SURVEY TOOL SETS IT.** §4. Harmless today.
   Worth a one-line comment in `row_price` so the next person does not spend an
   hour wondering whether the graft is changing more than the channel — this
   session did.

4. **SMITE AND HEMORRHAGE ARE ONE STATUS WITH TWO NAMES.** §4.2. That is a
   defensible design — the schools differ by application rate and by fiction —
   but it has never been written down, and two of seven schools sharing a
   status is the kind of thing that should be a decision rather than an
   accident.

5. **THE FEED COLUMN SHOULD BE A TOOL.** `budget_probe.py` is four arms and
   ninety lines and it ran the whole roster in twenty-nine minutes. If it lived
   in `tools/` it would answer "what is this relic made of" for every relic
   built from here on, and the calibration in §2.1 would grow a point per
   build instead of staying at two.

6. **THE TWO VIGIL CELLS.** §3. Closed as an open decision — they are not
   under-rated, they are the most spoken-for cells on the board — but they are
   still empty, and at some point the grid wants finishing.

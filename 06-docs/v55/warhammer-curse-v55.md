# v55 — UMBRAL x WARHAMMER, THE CELL BEFORE THE ULTIMATE. The echo is nearly type-invariant and the POOL is not, so this cell cannot be argued on damage — it is an ultimate decision. The recommendation's own headline claim was refuted by the check written to test it.

**2026-08-31, Cowork.** `tools/wh_curse_survey.py`, `tools/row_price.py`, and
`tools/cell_survey.py` against `02-chain/sc-nightfell.html` — the build with
all three umbral stages in it. Runtime only. Nothing is written to any build.

Rick has taken **umbral x warhammer** for the 29th relic, from four priced
cells. Twenty-seven relics fill 27 of 42 cells; the grid's two thinnest lines —
umbral at 3 of 6 types, warhammer at 3 of 7 schools — cross at exactly this
one, and filling it puts both on 4.

---

# 1. HOW THE CELL WAS PRICED, AND THE KNOB THAT WAS DECIDING IT

`row_price` A/Bs a school's channel against the same weapon with the channel
deleted, against the whole roster. It **pins every relic's damage** so a
harder-hitting arm cannot win by ending the fight sooner. The pin defaulted to
14 and has never been swept.

Curse was reworked hours ago: a stack now remembers **the damage of the blow
that applied it**, and every later hit pays 8% of the pool. Blow size IS the
mechanic — so a pin on damage is a pin on the thing being measured. Swept, 520
fights an arm:

```
warhammer row, delivered lift          pin 8    pin 36    change
bloodsworn  hemorrhage  flat 1.5/s     +28.7     +9.8     -18.9
runic       hex                         +9.0     +5.2      -3.8
umbral      curse       8% of a memory   +8.1     +8.7      +0.6
verdant     entangle                     +2.7     +7.3      +4.6
```

Hemorrhage is a **fixed rate** and its share of the fight collapses as the
blade grows. Curse is a **proportion of a memory** and holds. The real
warhammers ship at 20.1, 23.5 and 28.77 — nowhere near 14 — so the default pin
was ranking the row at a weight class the row does not fight in.

**Every cell ranking in this project's history has been read off pin 14.**
That is now a known, unswept parameter in four surveys, and it is the fifth
time a lab default has left as a claim (v52 §3d).

The fifteen open cells at pin 14, for the record — but read the caveat above
before treating the order as settled:

```
vigil x twinblade      +25.0    dwarven x twinblade    +12.5
bloodsworn x scythe    +19.2    umbral x scythe        +11.1
vigil x flail          +18.3    umbral x bow           +11.1
bloodsworn x warhammer +17.3    sanctified x twinblade  +9.1
runic x bow            +16.8    umbral x warhammer      +7.7
dwarven x scythe       +15.4    runic x warhammer       +1.4
sanctified x flail      +0.0    verdant x warhammer     -1.0
verdant x flail         -1.9
```

Cross-row comparison is indicative and not exact: each row is measured on its
own donor, so the floors differ. Within a row it is clean.

---

# 2. THE POOL AT WEIGHT

Umbral's channel injected onto every type's donor at **its own shipped
damage**, ultimates suppressed everywhere (Revenant *takes* pool entries and
Deadfall *copies* the sum — a live ult measures the ult, not the pool), 26
foes x 6 seeds a row. Read off wrapped `pushCurse` and `curseEcho`, not
sampled per step.

```
type       donor          dmg  blows  displ  entry  biggest   pool   peak  echo  /dealt  fillAt
twinblade  widowmaker    11.9   16.4    82%   19.6     39.0   45.9   95.5    72   18.3%   15.8s
bow        ironhail      16.2   14.0    79%   22.6     42.8   60.9  104.6    70   18.1%   10.3s
greatsword dawnbringer   10.4   17.5    83%   16.6     34.4   41.6   83.9    67   18.6%   13.9s
scythe     thornwake     31.4    7.7    61%   45.6     74.4   80.2  177.0    59   14.5%   22.0s
warhammer  grudgebearer  23.5    9.1    67%   35.2     62.8   73.6  148.4    59   15.5%   18.4s
flail      gravemourn    24.0    7.1    59%   35.9     60.3   61.3  136.5    41   13.8%   23.8s
```

`displ` is the share of applications that **displace** an existing entry — the
rework's own verb, and the only term in the design that scales with hit size.
The fast types run at 79-83%: almost every blow they land is throwing another
one out. The slow types run at 59-67%, so a slow type's pool is closer to a
record of its fight than a rolling window of its last few seconds.

## 2b. And the same six with every relic pinned to 14

```
type       donor          dmg  blows  displ  entry  biggest   pool   peak  echo  /dealt
twinblade  widowmaker    14.0   15.5    81%   22.0     44.0   50.8  106.1    74   17.9%
bow        ironhail      14.0   14.8    80%   20.0     39.8   54.6   95.0    66   18.2%
greatsword dawnbringer   14.0   15.6    81%   21.5     41.3   53.9  103.3    75   18.3%
scythe     thornwake     14.0   10.7    72%   22.5     40.7   44.9   98.4    48   16.4%
warhammer  grudgebearer  14.0   11.5    74%   22.0     42.1   48.1  100.2    51   16.6%
flail      gravemourn    14.0    9.0    67%   22.6     40.9   42.0   94.3    37   15.4%
```

**At equal blade the FAST types have the bigger pools.** More blows means more
draws from the damage jitter and the crit tail, and the pool keeps only the
best three — so a fast weapon is running more lottery tickets into a
max-of-three. Weight reverses it:

```
              pool @ shipped   pool @ pin 14   ratio     what the pool is made of
scythe                  80.2            44.9    1.79x    weight
warhammer               73.6            48.1    1.53x    weight
flail                   61.3            42.0    1.46x    weight
bow                     60.9            54.6    1.12x    both
twinblade               45.9            50.8    0.90x    rate
greatsword              41.6            53.9    0.77x    rate
```

---

# 3. WHAT WAS REFUTED, AND IT WAS THIS DOC'S OWN HEADLINE

The cell was recommended to Rick on the sentence *"the warhammer puts the
biggest single numbers in the game into a pool that remembers the three
biggest blows."* The check written to falsify it — `wh_curse_survey` check 1 —
**is red and stays red in the tool.**

```
mean pool entry     scythe 45.6  >  flail 35.9  ~  warhammer 35.2  >  bow 22.6
```

Thornwake ships at 31.35 and Slagheart at 42.5. **The warhammer is not the
heaviest blade in the game and it is not even the heaviest in its own half of
the mass ladder.** What is true is narrower and more useful: the warhammer's
entries match the flail's within noise (35.2 against 35.9) while it lands
**28% more of them** (9.1 blows against 7.1), which is why its pool is 20%
larger than the flail's — and against the umbral relic that already exists,
that is the whole difference. It is not a heavier blade than Gravemourn. It is
the same blade, landing more often.

---

# 4. THE ECHO IS NEARLY TYPE-INVARIANT. THE POOL IS NOT.

```
                pool (what the ULTIMATES read)      echo (what the CHANNEL pays)
across six types      41.6 - 80.2  =  1.93x            13.8% - 18.6% of damage = 1.34x
```

Heavy types hold a big pool and have few blows to cash it on; fast types hold a
small pool and cash it constantly. The product very nearly cancels: **curse
pays between 13.8% and 18.6% of a fighter's damage whatever it is bolted to.**

This is the finding that decides how the rest of the design has to go.

> **The cell cannot be argued on the channel.** Choosing umbral x warhammer
> buys almost no extra echo over umbral x anything. What it buys is a **pool
> that is 77% bigger than Nightfell's and 20% bigger than Gravemourn's**, and
> the pool is read by ultimates and by nothing else. Every point of difference
> this relic has from the three that exist has to come out of its ultimate.

---

# 5. AND IT IS THE CELL WHERE v52 §5'S SCHOOL RISK IS SMALLEST

v52 §5 registered the cost of routing a whole school through one pool:
*"umbral becomes a school where nothing works until Curse is stacked. A relic
that loses its first exchange loses its ultimate as well."*

Measured — the donor's own charge timer, curse injected, ultimates live:

```
type       donor         casts/fight   first cast at   stacks then   POOL THEN
warhammer  grudgebearer         1.57          19.7s          2.45        66.8
flail      gravemourn           1.73          17.2s          1.69        43.8
twinblade  widowmaker           2.86          15.2s          2.33        31.5
greatsword dawnbringer          2.82          15.4s          2.54        30.1
```

**The warhammer's first cast arrives with 2.2x the pool behind it that
Nightfell's does and 1.5x Gravemourn's.** It casts least often and it casts
fullest, which is the same sentence twice: a slow charge on a slow weapon
spends its charge time filling the thing the ultimate is going to spend. The
school's structural weakness is a property of contact rate, and this is the
type that trades contact rate away in the first place.

Register it as a prediction for the build to falsify: *an umbral warhammer
should have the flattest ult-value-against-first-exchange curve in the school.*

---

# 6. THE THREE RELATIONSHIPS TO THE POOL ARE TAKEN. THIS CELL UNLOCKS THE FOURTH.

```
TWINSHADE    FILLS    Triplicate multiplies the applier — three bodies, one shared pool
GRAVEMOURN   MOVES    Revenant takes an entry, deals it, and re-parks it. Conserved
NIGHTFELL    READS    Deadfall copies the sum onto the floor and writes nothing back
```

That was deliberate — v52 §3e: *"three relics, three relationships to one
mechanic."* A fourth umbral relic that spends, copies or fills is the fourth
relic in a school of three ideas.

What is left is the one the law forbade. v52 §3e, stated as a general result
across three separate designs:

> **An ultimate cannot MINT a memory. The pool holds the blade's biggest
> blows, so anything an ultimate applies is smaller than what is already in
> there — unless it out-hits the blade, and a thing that out-hits the blade is
> the relic.**

**The warhammer is the one type where the exception is in character.** The
admission price — what a blow must exceed to enter a full pool, measured at
the moment of the push:

```
blade   blows  entry  biggest   pool   peak  echo  /dealt   ADMITS   Revenant hand   Deadfall charge
 10.0    10.9   15.7     28.6   34.6   69.6    34   16.5%     14.4            11.5               2.1
 14.0    10.7   21.6     40.7   45.9   95.1    45   16.1%     19.4            15.3               2.8
 18.0    10.2   27.3     48.0   59.2  117.1    54   16.2%     24.8            19.7               3.5
 23.5     9.1   35.2     62.8   73.6  148.4    59   15.5%     31.2            24.5               4.4
 28.0     8.4   40.1     67.4   81.9  159.3    61   15.2%     36.2            27.3               5.5
 34.0     7.6   47.5     77.5   92.0  182.3    61   14.6%     42.2            30.7               5.5
```

At a shipped blade of ~23 a single blow of **31 or more displaces something**,
and one of ~63 becomes the pool's largest memory outright. A warhammer whose
ultimate is one enormous descending blow is the only relic in the game that
can put a number in that range on the board **without ceasing to be its own
weapon** — which is precisely the clause the law was written around.

The two right-hand columns are the warning that goes with it. **Neither shipped
ultimate's tuning transfers.** Revenant's hand is one pool entry at `handMul`
1.0; on this pool it carries 24.5 rather than Gravemourn's ~20.4. Deadfall's
charge is `stamp x0.3 / 5`; on this pool it is 4.4 rather than Nightfell's 3.6.
A design that reuses either constant is tuned against the wrong relic.

---

# 7. THE TRAPS, AND TWO OF THEM ARE NEW SINCE THE LAST BUILD

**a. `ultFx` IS ONE SLOT AND IT IS NOW A CHAIN-WIDE OPEN ITEM.** v54 §2a: every
window ultimate sets `ultFx.life` from `ult.dur`, and the opponent casting
**anything** overwrites it. Deadfall survived only because it was rebuilt onto
`f.ultDeadfall`. Ironhail's 1.3s Quarrelstorm leaves an eight-second window
with **no art at all for 100% of its frames**. Nobody has looked at what the
other six window ultimates lose. If this relic's ultimate is a window, it
hangs off the FIGHTER from the first line of code.

**b. `atSelf` ON THE FX SPEC.** v54 §2b: `drawUltOver` puts a `burst` field at
`[u.tx, u.ty]` — at the QUARRY — which is right for a nova and wrong for
anything that resolves on the caster. The flag now lives on the spec in
`src/render/fx.js`. Set it or the picture says the ultimate landed on somebody
it never touched.

**c. THE MEMORY IS `dmgBase`, NEVER `dmg`.** v51 §2.4. If a minted stack
remembers a blow's total *including the echo that blow paid*, curse compounds
inside one fight. An ultimate that mints is the most likely place in the whole
design to get this wrong, because the minting blow is exactly the one a
designer wants to be "worth what it hit for."

**d. THE ECHO IS PRICED ON THE TARGET.** v51 §4.3. Do not guard on
`self === owner`; Twinshade's shades are real `Fighter` objects and a guard on
the caster makes 9.3 blows a fight invisible.

**e. WARHAMMER MASS AND THE CLANK LADDER.** The warhammer is the top of the
mass ladder and the type most likely to be interrupted mid-swing by a clank.
`wh_survey.py`'s `CLANK_JS` measures outcome off the EFFECT rather than the
event; this cell's windup has never been measured with a status on it.

**f. AND THE ADJACENCY THAT HAS TO BE NAMED BEFORE THE ART IS DRAWN.** Censer
(sanctified) and Bulwarden (vigil) are the other two warhammers. Umbral's
warhammer art is 78.6% distinct from its nearest sibling (bloodsworn's,
unbuilt) and comfortably clear of both, and is the 3rd most distinct of the
fifteen open cells — but the two novas in this row are both *held overhead and
brought down*, and so is any minting blow. **The silhouette is free; the
gesture is not.**

---

# 8. WHAT THIS SURVEY CANNOT TELL YOU

- Nothing here prices an ultimate. Every number is the CHANNEL with ultimates
  suppressed, which is the only way to see the pool at all.
- The blade sweep is the pool against a blade, not a win rate against a blade.
  The relic's blade gets bisected after its ultimate exists, and §4.5 of the
  v51 brief applies with more force here than it did there: `dmg` moves the
  blade, the pool, AND anything the ultimate mints. Three channels, superlinear.
- The 26-foe field is the whole roster at 6 seeds — 156 fights a row. SE on a
  win rate is ~4pp; nothing in §1's lift table separates two cells inside 5
  points.
- `STATUS.curse.tip` still reads *"Hits reflect 8% of the damage that cursed"*
  in the shipped build, and the v51 brief specified *"Adds 8% of a remembered
  blow per stack"* (38/40). One of the two is wrong and `tip_audit` cannot tell
  which; it is a copy decision, not a build one.

---

# Open decisions

1. **THE §1 — RICK'S, AND IT IS THE BLOCKER.** Everything above is the room;
   the ultimate is his. The one structural steer this survey earns: the three
   relationships to the pool are taken, and this is the only cell in the game
   where a fourth — **an ultimate that MINTS a memory** — is in character
   rather than a violation. It is not the only option, and a good §1 that
   spends or reads instead is worth more than a mediocre one that mints.

2. **THE PIN, AND IT IS NOW A CHAIN-WIDE ITEM.** `row_price --pin` defaults to
   14 and every cell ranking in this project was read off it. The warhammer row
   reorders across the range. Re-running the other four rows at their own shipped
   weights is a ~5-minute job and it may move cells that have already been passed
   over. Not this relic's blocker; it is the next survey's.

3. **`STATUS.curse.tip`.** The build ships the pre-rework wording. 40 characters,
   already written in the v51 brief, one line to change.

4. **THE OTHER SIX WINDOW ULTIMATES.** v54 §2a is an open item and nobody owns
   it. Aegis, the Thicket, the ballista, the Stasis Field, the Winnowing and the
   Sentinel all set `ultFx.life` from `ult.dur`. Most survive because a viewer
   reads a sim object instead — that is an argument, not a measurement.

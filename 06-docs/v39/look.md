# v39 — THE LOOK AT TWENTY-TWO CELLS, and an instrument that was wrong twice

**2026-08-20.** Rick: *"lets keep it rolling. next fighter"* → the survey ran
before the cell was chosen, which is the change from v38.

v38 probed the bloodsworn × flail cell AFTER it had been chosen, and the probe
turned up two things that would have changed the pricing had they been known a
step earlier: the cell's art already existed, and the school's status could not
sustain on the type. So this time the look-first probe ran across the whole
grid first, and the choice was made against it.

```
tools/cell_survey.py          NEW   7/7   — all 22 open cells
tools/runic_scythe_probe.py   NEW   8/8   — the chosen cell, deep
05-reference/v39/runic-scythe-5x.png
05-reference/v39/runic-scythe-arena.png
NOTHING WAS BUILT. Injection is runtime-only; no build was written to.
```

---

# 1. THE GRID

Seven schools × six types = 42 cells, 20 filled, **22 open**. Read out of
`AC.WEAPONS` in the build rather than from a roster table in a document —
three docs already quote one that has drifted.

```
                bow      flail  greatsword   scythe   twinblade  warhammer  school
bloodsworn        ·   Threshmaw   Goreshard        ·  Widowmaker         ·     3/6
dwarven    Ironhail   Slagheart   Emberedge        ·           ·  Grudgeb.     4/6
runic             ·           ·       Axiom        ·  Spellbr.          ·     2/6
sanctified  Aureole           ·  Dawnbringer  Lastlight        ·     Censer     4/6
umbral            ·  Gravemourn   Nightfell        ·   Twinshade         ·     3/6
verdant           ·           ·   Heartwood  Thornwake         ·         ·     2/6
vigil     Farwarden           ·  Lightkeeper        ·          ·         ·     2/6
type              3           3           7        2           3         2
```

**The greatsword is full at seven. The scythe and the warhammer have two
each.** Runic, verdant and vigil have two relics each. So the roster wants a
scythe or a warhammer, in one of those three schools — which is six cells, and
the choice was made from those.

# 2. THE CHANNELS, AND A SCHOOL THAT HAS NONE

```
school       relics  channel               stacks    dur
bloodsworn        3  onHit hemorrhage:2         4    3.2
dwarven           4  onHit sunder:1/2           6    5.0
runic             2  onHit hex:1                5    2.6   <- shortest in the game
sanctified        4  onHit smite:1              4    3.2
umbral            3  onHit curse:1              8   99.0
verdant           2  onHit entangle:2           4    2.8
vigil             2  onSelf ward:1              1    5.0   <- NO onHit channel
```

**Vigil has no onHit channel at all.** Ward is `onSelf`, banked out of damage
dealt, and Farwarden already had to carry `ward: 2.5` because the constant was
authored on a greatsword and a bow deals a third as much a blow. Any vigil cell
is therefore a design about banking rather than about a foe status, which is a
different job from the other twenty-one open cells and worth knowing before
one is chosen.

`blessing` is applied by nobody — no weapon, no `ult.apply`. It is applied by a
MECHANIC, at the spark-collect site, with a literal `f.apply("blessing", 1)`.
The first cut of this probe reported it as an orphan status; the check was too
narrow, not the table.

# 3. THE ART IS SETTLED, AND v38'S FRAMING OF THAT WAS TOO GENEROUS

**All 22 open cells have their own dispatch branch and draw materially
different pixels from every sibling on their type. 22/22.** Art cannot
discriminate the choice, and that is a useful negative result: v38 called the
bloodsworn flail arriving with real art "unusual", and it is not — it is the
rule.

The bow is the exception worth recording: it does all seven schools **inline on
`p.key`** with no named `_bow*` helper, so a branch-name census sees zero
branches there and is wrong.

## The instrument was wrong twice, and the second one is the interesting one

**(a) It measured a clipped bow.** The canvas was sized from `reach`, and
`_artBox`'s own comment says that lies about a bow — the render ran off the top
and bottom of its own canvas and the whole row was scored against a crop. The
canvas is grown from a measured bounding box now and "no shape is measured
clipped" is a check.

**(b) An ALPHA MASK CANNOT SEE THE DWARVEN BOW.** Its branch draws a riveted
plate and six bolts, and every one of them lands **on top of** the riser and
the limbs, which are already inked. **0.12% of coverage. Unmistakable to the
eye.** The probe reported "no own art" and it was flatly wrong.

That is the same mistake v38 caught the weapon matrix making — the matrix
scored `flailHead` IoU 1.000 and called it "the flattest cell in the game"
because it measured the outer SILHOUETTE, and the difference between a bitten
crescent and seven hooked barbs is interior. An alpha mask fixes the
silhouette problem and reintroduces the same blindness one layer in.

**The fix is to hold the PALETTE CONSTANT and vary only `p.key`.** Every school
is drawn in one school's colours, so a pixel that differs differs because the
DISPATCH drew something else there. Interior ornament and added geometry both
land in it.

```
shape        own art   pixel diff, palette held      canvas
bow            7/7     mean 56%   min 34% dwar/sanc   179px
flail          7/7     mean 79%   min 50% umbr/verd   156px
greatsword     7/7     mean 88%   min 46% bloo/umbr   268px
scythe         7/7     mean 87%   min 60% bloo/sanc   348px
twinblade      7/7     mean 78%   min 32% dwar/umbr   143px
warhammer      7/7     mean 88%   min 51% bloo/dwar   253px
```

Controls, and the table means nothing without them: **the render is
deterministic** (same key twice, 0.0e+00 difference, on all six shapes) and
**the comparator is sensitive** (a nonsense key differs from the nearest real
school by at least 63.5%).

The absolute verdict column that was in the first cut is gone. With the palette
held, a moved edge costs pixels, and every cell landed in one bucket — a column
that cannot discriminate.

# 4. THE CLOCK ON THE TYPE — 42 CELLS AT ONE PIN

Damage pinned at 14.0 across every relic and ultimates suppressed, both
corrections v38 had to make. **The filled cells are measured too**, or the open
ones are numbers with no scale — v38's 41% was only meaningful against the 52%
and 59% beside it.

The instrument reads bloodsworn × flail at **39%** against v38's **41%** on a
different foe set. That agreement is the only reason to trust the other 41 rows.

```
                 >=2 stacks   what the school's clock does to a low-contact type
umbral   (curse 99s)  66-81%   immune to the type axis entirely
verdant  (entangle)   41-66%   healthy everywhere
bloodsworn (hem 3.2)  39-64%   the flail is its floor
dwarven  (sunder 5)   34-56%
sanctified (smite)    15-42%   thin on every heavy
runic    (hex 2.6)    15-36%   THE SHORTEST CLOCK IN THE GAME
vigil                    —     no onHit channel
```

`runic × flail` and `sanctified × flail` are both **15%** — thinner than the
cell v38 called thin enough to be the design's central constraint.

---

# 5. THE CHOSEN CELL: RUNIC × SCYTHE

Rick's call, from four measured candidates. Runic 2 relics → 3, scythe 2 → 3.

## 5.1 The art exists and is unmistakable

`_scConjured` fires; a nonsense key falls to `_scBase`. A blue crescent on a
haft of **detached floating shards** with a ring-and-triangle sigil at the
pommel — Axiom's own grammar, *"blade-shards held in formation by nothing at
all."*

**The hazard is the runic mirror.** At 1:1 against Spellbreaker it is two blue
balls carrying blue floating shards: v28's "same-affinity pairs read as one
smudge", recurring. Against Thornwake it reads perfectly. It cannot be the
marquee fight against its own school.

## 5.2 HEX IS NOT A QUANTITY, IT IS A RATE — and that reframes the cell

Every other school's status is a quantity: smite and hemorrhage deal damage per
stack per second, sunder multiplies what is taken, curse eats max hp, entangle
slows. For those, time-weighted occupancy **is** the delivered effect.

```
f.hexClock += dt * hx;
if (f.hexClock >= STATUS.hex.stunEvery){ f.hexClock = 0;
  f.stun = Math.max(f.stun, STATUS.hex.stunFor); ... }
```

The clock accrues at dt × STACKS, so five stacks do not lock harder, they lock
**five times as often** — and `Math.max` means two overlapping locks are one
lock. Occupancy is a proxy twice removed.

Measured on the lock itself. `net` is A/B'd against the same matchup with
`onHit` deleted, so it is hex's own contribution and not hitstun's:

```
carried on          hits/s   mean   >=2  fires/s   lock    net  hitStop
hex x bow            0.352   1.25   35%    0.941  31.1% +17.7%    9.5%
hex x twinblade      0.301   1.16   30%    0.862  31.0% +15.4%   10.3%
hex x greatsword     0.303   1.29   32%    0.928  37.3% +15.2%   11.6%
hex x scythe         0.196   0.75   18%    0.555  24.8% +10.1%    9.4%   <- cell
hex x warhammer      0.217   0.82   20%    0.606  28.4%  +9.9%    9.6%
hex x flail          0.191   0.64   16%    0.470  22.6%  +8.5%    8.4%
```

**18% at two stacks, and the foe's weapon is nevertheless shut for a quarter of
the fight.** The scythe delivers 57% of what the twinblade delivers on half the
contacts, because one stack already fires every 1.15s and the ladder is a rate
multiplier rather than a gate.

**So an ultimate that drives hex to its CAP is worth far more here than an
ultimate that merely applies it** — the cap is 5, which is a 5× lock rate, and
this cell reaches it 1% of the time.

## 5.3 `hitStop` FREEZES THE HEX CLOCK, and nothing had noticed

`step()` returns on `if (this.hitStop > 0)` **before** `tickStatus`, so the
clock does not advance while the hall is frozen — **9.4% of a scythe fight.**
The status whose entire job is stopping weapons is itself stopped by the
impacts that apply it.

This surfaced as a failing check at exactly that ~15% and read like a broken
rule. Now asserted correctly: fires are the integral of stacks over UNFROZEN
time divided by `stunEvery`, agreeing to **0.97% over 937 observed fires**.

## 5.4 `tickFire` GATES ON `f.w.shot`, NOT ON MODE

`relicShot()` gates on `mode === "ranged"`. `tickFire` does not use it — it
reads `f.w.shot` and returns only if the field is absent. **A `shot` field left
on a melee weapon fires a bow at cadence, forever.**

The probe left one on after its bow row and the five rows after it came back
**1.9× inflated** — 0.356 hits/s against the 0.204 the same cell measures
clean. It was caught by disagreeing with two other measurements, not by
inspection. This is a live trap for any relic that ever wants a `shot` field
without being ranged.

---

# Open decisions

1. **THE DESIGN, IN RICK'S WORDS — §1, and nothing starts without it.** Held to
   again. The probe ships a placeholder nova and the literal name PLACEHOLDER
   so that nothing in it can read as a proposal.
2. **Vigil's four open cells are a different job.** No onHit channel. Whoever
   takes one is designing a banking relic, and `ward`'s per-relic bank
   multiplier is the only precedent.
3. **The runic mirror reads as one smudge.** §5.1. Three runic relics now, so
   3 of 210 pairings. Small, but it rules out the marquee fight.
4. **§5.4 is a bug with no owner.** `tickFire` should call `relicShot()`. It is
   inert today because no melee weapon carries a `shot` — which is exactly the
   condition that will stop holding.
5. **Every type-level measurement in the project still wants a `--noult` pass.**
   v38 open decision 5, unmoved.

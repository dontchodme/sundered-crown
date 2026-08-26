# v41 — THE WARHAMMER ROW, SURVEYED BEFORE THE CELL WAS CHOSEN

**2026-08-20.** Rick: *"lets start on the next fighter"* → `cell_survey` re-run
on the v40 tip → the type from the roster gap → `wh_survey.py` → the cell.

```
tools/wh_survey.py     NEW   23/23   — the five open warhammer cells
out/wh_survey_v41.json         the numbers, machine-readable
NOTHING WAS BUILT BY THIS TOOL. Injection is runtime-only.
```

The v39 rule held: **the survey ran before the cell was chosen.** The v40 rule
held on top of it: `cell_survey` answers *which type*, and it is the wrong
instrument for *which school on this type*, so the type got its own probe.

---

# 0. WHY THE WARHAMMER

`cell_survey` on `sc-vinesower-frame.html` — 22 relics, 42 cells, **20 open**.

```
                bow      flail  greatsword     scythe   twinblade  warhammer  school
bloodsworn        ·  Threshmaw   Goreshard          ·  Widowmaker          ·   3/6
dwarven    Ironhail  Slagheart   Emberedge          ·           ·  Grudgeb.   4/6
runic             ·          ·       Axiom   Foregone Spellbreak.          ·   3/6
sanctified  Aureole          · Dawnbringer  Lastlight           ·     Censer   4/6
umbral            · Gravemourn   Nightfell          ·   Twinshade          ·   3/6
verdant   Vinesower          ·   Heartwood  Thornwake           ·          ·   3/6
vigil     Farwarden          · Lightkeeper          ·           ·          ·   2/6
type              4          3           7          3           3          2
```

**The greatsword is full at seven. The warhammer is alone at two — two behind
everything else.** Vigil is alone at two on the school axis. The two thinnest
rows in the game cross at one cell.

---

# 1. THE TYPE NOBODY HAD LOOKED AT

Two relics in twenty-two, and both inherited their block from a table rather
than from a brief. Read out of `AC.WEAPONS`:

```
type          reach  width   spin   mass  knockMul    mode  blades        dmg
bow              54      9    2.8    1.6         1  ranged       1  12.7–16.2
flail            96     22    2.2    3.6         1   chain       1  25.0–44.1
greatsword      116     14    3.4    3.0         1   swing       1   7.4–15.8
scythe          104     11    3.2    2.4         1    spin       1  17.5–31.4
twinblade        62      8    5.7    1.1         1    spin       2   8.3–11.9
warhammer        76     26    1.6    5.0       2.3    spin       1  27.9–28.8
```

Three things are the type and nothing else in the game has them:

- **`mass 5.0`** is the top of a `mass^1.7` ladder, and the ladder decides who
  keeps swinging after a bind.
- **`knockMul 2.3`** is the only value above 1.0 in the entire roster — a 379
  impulse where everything else throws 165 — and it is carried by the type with
  the **second shortest reach in the game.**
- **`spin 1.6`** is the slowest weapon there is: 3.9 seconds per revolution.

`PASS  both warhammers share one physics block, field for field`
`PASS  knockMul 2.3 is the highest in the game`
`PASS  mass 5.0 is the top of the ladder — next is flail at 3.6`

---

# 2. THE CLANK LADDER — 734 OF 734

Grudgebearer's blurb has claimed for twenty relics that it *"wins every clank
in the game."* Nobody had ever measured it. Outcome is read off the EFFECT —
whose `spinDir` reversed, who ate the stagger — never recomputed from the mass
formula the game owns, so a future change to the mass model moves these numbers
and a future change to the probe cannot.

```
foe           type         mass clanks/min   won  deadlock  lost  stun taken  stun dealt
emberedge     greatsword    3.0       25.3  100%       0%     0%        17.2        47.0
spellbreaker  twinblade     1.1       20.6  100%       0%     0%         3.5        66.6
lastlight     scythe        2.4       17.5  100%       0%     0%        12.7        48.3
slagheart     flail         3.6       14.2  100%       0%     0%        16.1        30.8
aureole       bow           1.6       11.4  100%       0%     0%         3.7        30.9
```

**734 binds, 734 won, zero deadlocks, against every type in the game including
the 3.6-mass flail.** The stagger is 4.2:1 in its favour. The blurb was true
and is now a measurement.

*Design consequence: a mechanic that keys off winning binds is FREE on this
type, and a mechanic that adds mass buys literally nothing.*

`PASS  the instrument does not move the simulation — 4 seeds, field for field`

---

# 3. THE HEADLINE — THE HAMMER THROWS ITS QUARRY OUT OF ITS OWN REACH, AND THE ULTIMATE SLOT IS WHERE THAT GETS PAID FOR

`knockMul` swept on the donor alone, pinned seeds, **shipped damage held at
27.93 across the whole sweep** so the win column prices the shove and nothing
else. Ultimates suppressed.

```
 knockMul  impulse  hits/min   dmg/s   win  mean sep  sep at hit  sep +0.25s    push  hit gap
      1.0      165      11.1    8.59   63%     188.5        52.2        65.2   +13.0     4.52
      1.6      264      10.3    7.90   55%     189.4        53.2        64.3   +11.2     5.05
      2.3      379       9.7    7.18   47%     190.0        53.0        74.6   +21.6     5.33
      3.0      495      10.2    7.72   48%     187.7        51.4        76.7   +25.3     4.97
```

A landed blow opens the gap by **+22 units on a 76 reach**. The shipped setting
lands **12% fewer contacts** than 1x would and gives up **16 points of win
rate**. The 27.93 damage this type carries is not a statement about how hard it
hits. **It is compensation for how far it throws.**

The cost does not keep growing — 3x is no worse than 2.3x, because the hall is
finite and closing and the room hands back what the hammer throws away. Where
exactly the floor sits moved between a 6-seed and a 12-seed run and this survey
does not claim to have pinned it.

## And then the framing was refuted by the two shipped relics

The sweep suppresses ultimates. Switch them back on and run **both** warhammers.
Crucible carries `pullBase/pullMax/pullRamp` and drags the foe in. Consecration
is a nova that knocks it further out.

```
relic         ult             knockMul  hits/min   dmg/s   win   the shove is worth
Grudgebearer  Crucible             1.0      10.2   11.17   58%
Grudgebearer  Crucible             2.3      10.4   11.75   65%                  +7%
Censer        Consecration         1.0      10.1    7.46   58%
Censer        Consecration         2.3       8.7    6.51   42%                 −17%
```

**Same type. Same shove. Opposite ultimates, opposite sign.** The relic whose
ultimate takes the shove back is paid +7% for carrying it; the relic whose
ultimate adds to it is still down 17%.

**This is the brief for the third warhammer**, and it was measured before the
cell was chosen: *the ultimate either answers the reach, or the relic eats it.*

---

# 4. A HYPOTHESIS THAT WAS WRONG, KEPT AS A CHECK SO IT STAYS WRONG

`step()` returns on `hitStop > 0` **before** `tickStatus` — v39 found that on
the scythe and called it 9.4% of a fight. `impact.stopPerDmg` prices the freeze
off the DAMAGE of the blow, and this type lands the second-hardest blow in the
game. So the heaviest type should freeze its own status clock hardest, and
every clock `cell_survey` publishes is measured at a pinned 14 damage where
that could not appear.

**It is false.**

```
type          dmg/blow  stop/blow  frozen (pinned)  frozen (shipped)  contacts/s  Δ
greatsword        11.2      0.070            11.3%             11.4%       0.496  +0.1%
twinblade          9.7      0.066            10.2%             10.6%       0.459  +0.5%
scythe            24.3      0.098             9.4%              9.3%       0.431  −0.1%
warhammer         28.4      0.107             9.4%              9.1%       0.431  −0.3%
bow               15.1      0.078             9.0%              9.1%       0.532  +0.1%
flail             37.2      0.127             8.0%              8.0%       0.424  −0.0%
```

`stopMax` caps the freeze at 0.13 and `hitStop` is a **max**, not a sum. So what
fills a fight with freeze is how OFTEN blows land, not how big they are: **the
type with the biggest blow in the game freezes the hall least.**

Two things fall out, both useful:

- **The instrument is calibrated.** 9.3% here against v39's independently
  measured 9.4% — a different tool, a different session, a different probe.
- **`cell_survey`'s pinned clocks need no shipped-damage correction on this
  type.** −0.3%. The correction I expected to have to apply does not exist.

---

# 5. THE FIVE OPEN CELLS, AS DELIVERED EFFECT

`self.dealt` counts what `resolveHit` paid out and **nothing else** — it is
blind to every damage-over-time status and to curse's bite out of the ceiling,
which is half the channels being compared. The readout here is the foe's own
health, ceiling captured before curse can move it. Shipped damage, ultimates
suppressed, same seeds on and off, 60 fights a row.

```
cell                    status         hp/s  vs control   win  hits/min  taken/s  max hp eaten
— no channel —                         6.93                52%      10.7     6.42
bloodsworn x warhammer  hemorrhage     7.65      +10.3%   57%       9.7     6.43           0.0
runic x warhammer       hex            6.86       −1.1%   53%      10.9     6.26           0.0
umbral x warhammer      curse          6.98       +0.7%   57%      10.7     6.17          84.3
verdant x warhammer     entangle       6.66       −4.0%   42%      10.2     6.76           0.0
```

**The no-channel control is not a floor.** Two of the four open foe statuses are
worth less than no channel at all on this type — and the worst of them is the
one that SLOWS THE QUARRY. §3 is why: a relic whose problem is a foe it keeps
throwing out of reach does not want that foe returning more slowly. The
`hits/min` column is the mechanism rather than the story.

## Vigil is not a foe status and does not belong in that table

`onSelf.ward`'s value is a per-relic **bank multiplier** — `resolveHit` banks
`dmg * STATUS.ward.bank * n`. Lightkeeper carries 1.0 on a greatsword,
Farwarden 2.5 on a bow, and the vigil doc's open decision 4 says the constants
do not survive the type axis. This is the heavy end of that axis.

```
mult  banked/s  absorbed/s  mean pool  held  at cap  breaks/fight  burst  break push   win
 1.0      3.94        2.46       14.3   46%    0.6%          2.20   11.2       +44.4   77%
 1.6      5.64        3.12       22.0   51%    5.3%          1.47   17.1       +23.6   75%
 2.3      7.13        3.54       29.9   53%   11.7%          0.98   23.7       +19.6   83%
 3.0      7.64        3.87       34.4   54%   16.6%          0.78   29.1       +24.8   80%
```

- **No hand-patch needed at the heavy end.** At 1.0 the plate already holds 14.3
  and eats 2.46 dmg/s, against a control win of 52%. Farwarden's 2.5 was
  compensation for a bow; this type banks fine at 1.0.
- **The pool ceiling of 90 is nearly unreachable** — 0.6% of the fight at 1.0.
- **THE PLATE BREAKING IS A SECOND SHOVE.** `shatter` throws the attacker at
  `W.knock * knockMul` = 210 × 2.3 = **483, more than the 379 of the hammer's
  own blow** — and measured, +44 units 0.25s after a break. The engine's own
  comment already anticipated this cell: *"so the vigil warhammer throws you
  across the hall and the vigil bow only pops."*

**So this cell doubles down on the one thing §3 says the type cannot afford**,
and it is still the strongest raw channel on the row. That is the design
problem, stated in numbers, before anything was designed.

---

# 6. THE TRAPS

- `PASS` the warhammer is `mode:"spin"`, not `"swing"` — it has no `arc`.
- `PASS` no warhammer carries a `shot` field. v39 od 4 is still live: `tickFire`
  gates on the FIELD, not on the mode, so a `shot` left on a melee weapon fires
  a bow at cadence forever.
- `PASS` contact is geometry, not cooldown — one blade at `hitCd 0.45` allows
  2.22 contacts/s and the row lands 0.43.
- **And one that is not a bug:** damage-over-time does not route through
  `hurt`'s shield gate. Hemorrhage and smite go UNDER a ward, by design. A vigil
  hammer's plate is no answer to bloodsworn or sanctified.

---

# Open decisions

1. **`STATUS.ward.bank 0.55 / cap 90` still have not been swept on their own.**
   This survey shows the heavy end does not need Farwarden's patch; it does not
   show that 0.55/90 are right. Vigil od 4, now with data on both ends of the
   type axis and nothing in the middle.
2. **The 12-seed and 6-seed runs disagree about where the knock cost bottoms
   out** (1.6x, then 2.3x). The saturation is real at both; the floor is not
   pinned. `--seeds 24` would settle it and was not run.
3. **`cell_survey`'s umbral row is still suspect** (v40, unmoved). This survey's
   §5 is a second instrument on one type and agrees curse is unremarkable in the
   moment — 84.3 max hp a fight is where its value actually is, and no
   occupancy table can see that.
4. **Every type-level measurement still wants a `--noult` pass** — v38 od 5,
   v39 od 5, v40 od 6. §3 and §5 here run `noult` by default and §3 runs both,
   which is the first time the pair has been reported side by side.
5. **The stagger asymmetry in §2 is unpriced.** 4.2:1 is enormous and no relic
   in the game reads `stun` as a resource.

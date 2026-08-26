# v43 — THE FLAIL ROW, SURVEYED BEFORE THE ULTIMATE WAS DESIGNED

**2026-08-21.** Rick: *"next fighter please"* → `cell_survey` re-run on the v42
tip → every relic re-priced at **40 seeds** → four candidates → **runic × flail**
→ `flail_survey.py`.

```
tools/flail_survey.py   NEW   26/26   — the flail row, seven sections
out/flail_survey_v43.json             the numbers, machine-readable
out/flail_survey_v43.txt              the run
cell_survey             7/7           the grid on the v42 tip — 18 cells open
verify.py --n 40       13/13          11040 fights, so the choice is not
                                      priced on noise (v42 rule 7)
NOTHING WAS BUILT. Injection is runtime-only; no build was written to.
```

The v39 rule held: **the survey ran before the cell was chosen.** The v40 rule
held on top of it: `cell_survey` answers *which type*, and it is the wrong
instrument for *which school on this type*, so the type got its own probe.
**And this survey refuted the sentence the cell was chosen on**, which is §6.

---

# 0. WHY THIS CELL

18 open cells, four schools at 3 of 6 and four types at 3. The double-gap
heuristic has nothing to say for the second session running, so the shortlist
was priced and the choice was made on the design job.

```
                     bow       flail  greatsword      scythe   twinblade   warhammer  school
bloodsworn    Marrowdraw   Threshmaw   Goreshard           ·  Widowmaker           ·   4/6
dwarven         Ironhail   Slagheart   Emberedge           ·           · Grudgebeare   4/6
runic                  ·           ·       Axiom    Foregone Spellbreake           ·   3/6
sanctified       Aureole           · Dawnbringer   Lastlight           ·      Censer   4/6
umbral                 ·  Gravemourn   Nightfell           ·   Twinshade           ·   3/6
verdant        Vinesower           ·   Heartwood   Thornwake           ·           ·   3/6
vigil          Farwarden           · Lightkeeper           ·           ·   Bulwarden   3/6
type                   5           3           7           3           3           3
```

Re-priced at `--n 40` on the v42 tip — 24 relics, 276 pairings, 11040 fights,
13/13, spread 12.2pp:

```
school        n    mean                        type          n    mean
sanctified    4   52.57                        warhammer     3   52.60
dwarven       4   52.52                        bow           5   51.26
vigil         3   50.57                        scythe        3   50.47
umbral        3   48.67                        greatsword    7   49.60
bloodsworn    4   48.58                        flail         3   48.53
runic         3   48.20                        twinblade     3   47.33
verdant       3   47.77
```

**Runic × flail is the sixth school by win rate crossed with the fifth type**,
and `cell_survey` calls it the thinnest cell it has ever measured — 15% of the
fight at two or more stacks, **0% at cap**, against the shortest status clock in
the game. Rick took it from four.

---

# 1. THE TYPE NOBODY HAD LOOKED AT, AND THE ONE THAT IS NOT ATTACHED TO THE BALL

Three relics in twenty-four. `mode:"chain"` has exactly one member, `CONFIG
.chain` is read by nothing else, and `bladeSegments` returns something
structurally different for it than for the other five types.

```
type          reach  width   spin   mass  knockMul    mode  blades        dmg
bow              54      9    2.8    1.6         1  ranged       1  12.7–16.2
flail            96     22    2.2    3.6         1   chain       1  25.0–44.1
greatsword      116     14    3.4    3.0         1   swing       1   7.4–15.8
scythe          104     11    3.2    2.4         1    spin       1  17.5–31.4
twinblade        62      8    5.7    1.1         1    spin       2   8.3–11.9
warhammer        76     26    1.6    5.0       2.3    spin       1  20.1–28.8

CONFIG.chain  follow 5.2  spring 26  damp 0.9955  extend 7  maxAngVel 15
              hilt 0.46  sag 1.1
```

`PASS  all three flails share one physics block, field for field`
`PASS  chain is a mode of one — no other type shares a line of it`
`PASS  the flail carries the hardest blow in the game — 44.1, next type 31.35`
`PASS  mass 3.6 is second on the ladder — 5, 3.6, 3, 2.4, 1.6, 1.1`

---

# 2. THE HEADLINE — THE HEAD IS THE WEAPON, AND IT IS THIRTEEN UNITS LONG

Every other type's live segment runs from the shell to the tip of the blade.
A chain's is a stub around the head. Read off `bladeSegments` — the function
the hit test actually calls — and not off `reach`, because for this type those
are two different numbers and that is the entire point.

```
type          live blade  contacts/s  tip / head  reach  extension   taut   lag rad  lag max
bow                 61.4       0.106        91.4     54       1.00   100%      0.00     0.00
flail               13.2       0.152        89.4     96       0.88    36%      0.53     1.71
greatsword         128.4       0.269       158.4    116       1.00   100%      0.00     0.00
scythe             116.5       0.196       146.5    104       1.00   100%      0.00     0.00
twinblade           70.4       0.257       100.4     62       1.00   100%      0.00     0.00
warhammer           85.7       0.183       115.7     76       1.00   100%      0.00     0.00
```

**13.2 units against 61 to 128, and the number is `width × 0.6`. The flail's
reach of 96 does not appear in its live edge at all.**

The head roams a band that runs from the shell out to a measured 119 units — a
51.8 chain hung off a 44.2 haft, both turning — and **occupies one 13-unit stub
of that band at any instant.** The type covers the most ground and is live in
the least of it. That is why it is paid 25–44 damage a blow.

`PASS  the flail's live blade is the shortest in the game by a long way`
`PASS  it is 0.6 x its WIDTH and has nothing to do with its reach`
`PASS  every rigid weapon's segment IS its reach, shell to tip` — which is what
makes the flail's number mean something rather than being a number.

## And it is the only contact point in the game that is not the facing

`headAng` is pulled toward `theta` by a spring, pushed by gravity, damped, and
thrown out by centrifugal extension. **Mean |headAng − theta| is 0.53 rad and
the maximum is 1.71 — most of a right angle behind where the weapon points.**
Every other type reads 0.00 by construction. The head is at full extension
**36% of the time**.

---

# 3. A STUN DOES NOT LOCK THIS WEAPON. THE HYPOTHESIS WAS THAT IT DROPS IT, AND THAT IS HALF RIGHT

`tickWeapon`'s chain branch runs **during** a stun with `drive = 0` — the head
coasts, sags and pulls in on a slack chain — where every other mode sits behind
`else if (f.stun > 0){ /* weapon locked */ }` and resumes exactly where it
stopped. Hex is a 0.20s weapon stun, so this is the school-to-be pointed at the
type's own peculiarity.

**The first instrument was underpowered and its answer was noise.** Contacts in
a 2s window: the flail expects 0.15 of one, and the arms came back with the
stunned side *ahead* on two types. Replaced by the ARC the weapon turns
through, which is the same question with a usable variance, and by the PATH the
live edge travels, which is that question with the radius left in.

```
type        mode       arc/s  swing lost  x stun  path lost  x stun   ext at t0  floor  at +1s
bow         ranged      2.46       0.214   1.07x      0.214   1.07x
flail       chain       1.94       0.181   0.91x      0.214   1.07x        0.86   0.58    0.89
greatsword  swing       3.54       0.090   0.45x      0.090   0.45x
scythe      spin        2.87       0.185   0.92x      0.185   0.92x
twinblade   spin        4.94       0.207   1.03x      0.207   1.03x
warhammer   spin        1.43       0.212   1.06x      0.212   1.06x
```

**The instrument is calibrated by the rigid rows, not by the flail row.** Four
types whose facing is an integral of their own spin lose 0.92–1.07× of a 0.20s
stun and not a millisecond more. That is the control; without it the flail's
number is a number.

**THE HYPOTHESIS IS REFUTED. A stun costs the flail the same SWING it costs
everything else** — 0.91×, inside the rigid band. The head coasts through the
stun and the coast pays for the respin.

**What it costs instead is REACH.** Path 1.07× against swing 0.91×; the head
pulls in from 0.86 extension to a floor of 0.58 and **takes 1.08s to climb back
to where it was.** For a rigid weapon the radius is a constant and the two
columns are the same number *by construction*, which is what makes the flail's
gap readable. So a 0.20s hex stun is a **~1.28s event of shortened reach on
this type, roughly six times the stun** — and it is bounded, which matters as
much: the head does come back, in 220 of 233 dips inside the window.

## And a new engine fact fell out of the control row

**The greatsword reads 0.45×, and it is the only type in the game whose facing
is not an integral of its own spin.** `mode:"swing"` recomputes
`theta = aim + sin(swingPhase) * arc` every frame, and `aim` keeps tracking a
moving ball while the fighter is stunned. **A stunned greatsword's blade keeps
turning.** It lands nothing — `tickHits` skips on `self.stun > 0` — but the
picture, and every measurement taken off `theta`, moves. Nothing in the tree
had recorded that.

---

# 4. THE FLAIL IS HEAVIER THAN THE GREATSWORD AND CANNOT CASH IT

Outcome read off the EFFECT — whose `spinDir` reversed, who ate the stagger —
never recomputed from the mass formula, and then **checked against it**. The
decisive threshold is a literal inside `resolveClank`, so the tool reads it off
the shipped source rather than copying it.

```
foe           type         mass  margin  clanks/min   won  deadlock  lost  stun taken  stun dealt  bind→hit
emberedge     greatsword    3.0   0.154        21.7    0%      100%    0%        18.0        25.8      1.55
spellbreaker  twinblade     1.1   0.765        14.6  100%        0%    0%         2.9        31.8      2.56
lastlight     scythe        2.4   0.332        15.7  100%        0%    0%        11.1        24.5      2.28
aureole       bow           1.6   0.598         6.7  100%        0%    0%         2.6        10.4      3.33
censer        warhammer     5.0   0.272        15.6    0%        0%  100%        25.0        13.3      2.08
slagheart     flail         3.6   0.000        11.3    0%      100%    0%        14.7        15.0      2.94
```

`margin` is `|shareA − shareB|` out of `mass^1.7`, and a bind is decisive above
**0.16**.

**The flail against the greatsword is 0.1537. It misses by 0.0063.** 112 binds,
100% of them deadlocks — the second-heaviest weapon in the game cannot win a
bind against a 3.0, by six thousandths of a threshold. It loses binds to
**exactly one weapon**, the 5.0 warhammer, 96 of 96, at 25s of stagger taken
against 13s dealt.

`PASS  the effect and the mass model agree on every foe` — which is what makes
the margin column a prediction rather than a restatement of the outcome.

**`bind→hit` is the recovery of §3 priced on the fight**: greatsword 1.55s,
warhammer 2.08s, scythe 2.28s, twinblade 2.56s, flail 2.94s, bow 3.33s from a
bind to this relic's next landed blow.

---

# 5. THE FOUR OPEN CHANNELS AS DELIVERED EFFECT — AND `cell_survey` WAS WRONG ABOUT THIS ROW

Shipped damage, ultimates suppressed, same seeds on and off. Sections 2–4 pin
damage because they compare TYPES; this one compares schools on one type, where
the pin would only take away the compensation this type is paid for its contact
rate. The readout is **the foe's own health**: `self.dealt` counts what
`resolveHit` paid out and is blind to every damage-over-time status.

```
cell                    status     hp/s  vs control   win  hits/min  taken/s
— no channel —                     7.29               57%       7.7     6.69
runic x flail           hex        8.17     +12.1%    70%       8.9     5.61
sanctified x flail      smite      7.85      +7.7%    50%       7.9     6.84
verdant x flail         entangle   8.86     +21.6%    65%       9.4     6.64
```

**The cell `cell_survey` calls the thinnest in the game is the second-strongest
channel on its own row by delivered effect, and the only one of the four that
cuts damage TAKEN.** Occupancy is a proxy twice removed for a status that is a
rate (v39 5.2), and this is the second time that has bitten.

## Vigil is not a foe status, and this is the middle of its axis

`onSelf.ward`'s value is a per-relic bank multiplier — Lightkeeper 1.0 on a
greatsword, Farwarden 2.5 on a bow because ward was authored on a greatsword
and a bow deals a third as much a blow, and v41 measured the warhammer at 1.0.

```
mult  banked/s  absorbed/s  mean pool  held  at cap  breaks/fight  burst   win
 1.0      4.54        2.24       14.7   43%    2.0%          1.23   14.2   85%
 1.6      6.18        3.02       23.8   47%    5.6%          0.78   23.6   82%
 2.3      7.05        3.50       30.1   48%   12.1%          0.65   31.7   78%
 3.0      7.91        3.62       34.9   50%   17.5%          0.40   35.8   80%
```

**The flail banks fine at 1.0**, like the warhammer and unlike the bow — 14.7 of
pool held 43% of the fight off the hardest blow in the game. Farwarden's 2.5 was
a patch for a bow and not for weight. Vigil od 4 now has both ends of the type
axis and one point in the middle; `STATUS.ward.bank 0.55 / cap 90` are still
unswept on their own.

---

# 6. HEX ON THE FLAIL — AND THE SENTENCE THE CELL WAS CHOSEN ON IS HALF WRONG

The cell was taken on: *"hex is a rate, not a quantity — one stack fires a 0.2s
weapon stun every 1.15s and five stacks fire five times as often. An ultimate
that pins hex at its cap is worth 5× the lock, and this cell never reaches it."*

**The rate half is exactly right. The `worth` half named the wrong column.**

```
arm             hits/s   gap  mean   >=2   cap  fires/s   lock  foe hits/s  taken/s  hp/s     net   win
no channel       0.128  6.82  0.00    0%    0%    0.000  14.4%       0.294     6.69  7.29           57%
shipped hex:1    0.148  5.94  0.40    7%    0%    0.290  20.4%       0.274     5.61  8.17  +12.1%   70%
pinned at 1      0.151  5.91  1.00    0%    0%    0.783  28.7%       0.224     5.15  8.34  +14.5%   78%
pinned at 2      0.143  5.81  2.00  100%    0%    1.596  42.7%       0.235     5.42  8.34  +14.5%   75%
pinned at 3      0.160  5.76  3.00  100%    0%    2.407  57.9%       0.182     4.22  8.74  +20.0%   90%
pinned at 4      0.168  5.60  4.00  100%    0%    3.190  71.5%       0.138     3.24  9.04  +24.1%   92%
pinned at 5      0.156  5.96  5.00  100%  100%    4.011  86.1%       0.111     2.86  8.69  +19.3%   92%
```

**THE LADDER CANNOT START.** The flail lands a blow every **5.94 seconds** and
hex expires in **2.6**. So **75% of every hex this cell applies lands on a foe
with no stacks at all**, and **71% of the gaps between its own blows are longer
than the status it carries.** The relic is not building a ladder that tops out
low; it is re-lighting the bottom rung from cold, three times in four.

**AND THE LOCK IS DEFENSIVE.** Driving the ladder to its cap takes the lock from
29% to 86% and the foe's landed blows from 0.224/s to **0.111/s** — **62% fewer
blows than against no channel at all, and 57% less damage taken.** The damage
this relic DEALS does not order itself across the rungs (+14, +15, +20, +24,
+19) and should not be expected to: **a locked weapon does not make this weapon
swing faster. It stops the other one.**

So the ultimate has a measured target, and it is not the one the cell was
chosen on. *5× the lock* is real. What it buys is the foe not swinging.

---

# 7. THE TRAPS

- `PASS` `chain` is the only mode whose branch runs during a stun.
- `PASS` a stunned fighter still lands no blows — the head moves, it does not
  hit. `tickHits` skips on `self.stun > 0`.
- `PASS` **no flail carries a `shot` field**, and v39 od 4 is still live:
  `tickFire` gates on the FIELD, not on the mode, so a `shot` left on a melee
  weapon fires a bow at cadence forever. Bloodhunt came within one line of it in
  v42.
- `PASS` **hex is one of the three TRUE stuns that break a wind-up**, and
  Bloodmill — the wind-up that rule was written for — lives on this type. A
  runic flail is the first relic that would deal one of the three stuns that
  cancel it, from the same type.

---

# Open decisions

1. **THE DESIGN, IN RICK'S WORDS — §1, and nothing starts without it.** This
   survey designs nothing and proposes nothing. It says what the type is, what
   the school does on it, and where the numbers are; it does not say what the
   ultimate should be.
2. **THE GREATSWORD DEADLOCK IS SIX THOUSANDTHS FROM BEING A WIN.** §4. Nothing
   in the game reads that margin and no relic has ever been designed against it.
   It is named here, not touched — moving `0.16` is a change to every bind in
   the game.
3. **`cell_survey`'s occupancy column has now mispriced two cells** — the umbral
   row (v40 §4.1, still suspect) and this one. Occupancy is the wrong readout
   for a status that is a rate, and the tool does not say so in its own output.
4. **A STUNNED GREATSWORD'S BLADE KEEPS TURNING.** §3. Inert for damage, live
   for the picture and for anything measured off `theta`. Seven relics.
5. **`STATUS.ward.bank 0.55 / cap 90` are still unswept.** Vigil od 4, now with
   three points on the type axis and none on the constants themselves.
6. **Every type-level measurement still wants a `--noult` pass.** v38 od 5, v39
   od 5, v40 od 6, v41 od 4, v42. §§2–6 here run `noult` by default and none of
   them runs both.

> # SUPERSEDED — RICK CHOSE GLOAMWIRE. DO NOT BUILD FROM THIS FILE.
>
> **2026-09-01.** Two v61 designs were written for `umbral x bow` on the same
> day by two sessions that could not see each other — the second collision in
> two relics. Rick's ruling: *"find the one build by cowork in the repo and
> build that one."* **`gloamwire-design-v61.md` and `GLOAMWIRE-BUILD-BRIEF.md`
> are what ships.** Read `CONFLICT-READ-FIRST-v61.md` for both sides.
>
> **AND THIS DOCUMENT SHOULD NOT HAVE EXISTED.** CLAUDE.md §3 now opens with
> rule 0: Claude Code does not design ultimates. The mechanic below was picked
> by Rick off a spread of three that this session invented, which is designing,
> and it cost him a second full set of design decisions about one relic in one
> day. Kept rather than deleted (v60's rule) for the measurements only.
>
> **WHAT IS STILL WORTH READING, because it is observation of the shipped build
> and not of any ultimate** — `CONFLICT-READ-FIRST-v61.md` §3 asks for it to be
> kept wherever it can be found:
>
> - §2, the bank ledger: **10,804 arrows, zero unclassified**, the wall at
>   83.4% on the current tip.
> - §2.2: wall arrivals are **perimeter-proportional across all four walls**
>   (E 32.6 / W 32.0 / S 18.0 / N 16.2), which is the opposite of Cindercleave's
>   3.9% roof and is explained by `grav: 0`.
> - §2.3: they form **a ring at 86% of uniform** spread, against a Monte Carlo
>   baseline.
> - §4: the hall closes **9.6 units** under a wall object across an 8s window,
>   and `plantVine`'s `{wall, u}` is the engine's own answer to it.
> - §5: three of this lab's own findings were the lab measuring itself.
>
> `tools/quiver_lab.py` and `05-reference/v61/quiver-*.json` are kept with it.

# v61 — THE MISSES COME BACK, and the two knobs the design appeared to have are both free. The aim rule is worth nothing on balance and the quill's weight is worth nothing across a factor of two, which means every remaining choice in this ultimate is made for the picture — and it means the one number that is NOT free is the blade. Three findings in this lab were the lab measuring itself.

**2026-09-01.** `tools/quiver_lab.py`, new, against `02-chain/sc-garrote.html`.
Rick chose the cell (*"purple bow is in there. lets get it"*), the mechanic
(**the misses come back**, off a priced spread of three), the art (**keep it**)
and the aim rule (**back the way it came**). Runtime only.
**NOTHING is written to any build.**

```
05-reference/v61/quiver-bank.json        [1] the bank, 100 fights, 10,804 arrows
05-reference/v61/quiver-release.json     [2] the three aim rules
05-reference/v61/quiver-weight2.json     [2] the weight, n=200 an arm
05-reference/v61/quiver-fieldults.json   [2] the same arm in the SHIPPING world
```

---

# 1. THE MECHANIC

A cast opens a window. **The bow fires nothing new.** Every ordinary arrow that
ends on a wall while the window is open stays there — stuck in the stone,
remembering — and when the window closes they all come back at once, each along
its own flight reversed.

That is the whole of it, and the reason it is worth building is one number
`bow_survey` has printed since v40 and nothing has ever spent: **82% of every
arrow ever loosed in this game ends on a wall.** v40 open decision 2, twenty-one
relics old — *the wall is the type's constraint and no relic addresses it.*
Vinesower is the closest anything has come and it spends **eight seeds of its
own** on the wall; this spends what the weapon was throwing away anyway.

---

# 2. THE BANK, OBSERVED BEFORE ANYTHING WAS INJECTED

100 fights, every non-bow foe, ults suppressed, 10,804 arrows, **zero
unclassified**. The ledger reproduces `bow_survey` to the point: landed 7.3%,
parried 9.0%, **wall 83.4%**.

## 2.1 A window banks a volley, and it banks one nearly every time

Every window POSITION a cast could have had, at 0.25s resolution — 15,929 of
them — rather than a mean times a duration:

```
   min    p10    p25   median    p75    p90    max    mean
     0     11     13       16     18     19     24    15.2
```

**A window that banks nothing is 0.1% of positions.** For scale, Ironhail's
entire ultimate is a nova of fourteen arrows; this one is a median of sixteen
and it costs the relic nothing to load.

## 2.2 It comes from all four walls, and that was not the obvious answer

```
E        2940   32.6%          perimeter share of a 520x800 hall: 30.3%
W        2883   32.0%                                             30.3%
S (floor)1625   18.0%                                             19.7%
N (roof) 1457   16.2%                                             19.7%
corner    104    1.2%
```

**Almost exactly perimeter-proportional.** That is worth stating because the
last relic to put something on a wall found the opposite: `cindercleave` gives
the north wall **3.9%** of its tears, because a scythe has to be against the
stone and gravity keeps a ball off the roof. An arrow has `grav: 0` and flies
straight out of a spinning bow, so it has no such bias. **The release surrounds
the fight.** Nothing has to be weighted, and nothing about where a bow cuts has
to be invented.

## 2.3 And it is a ring, not a clump

Mean pairwise distance between the arrows banked in one window: **420 units**,
p10 314, p90 467. Sixteen points thrown uniformly at the perimeter of this hall
give **486** (Monte Carlo, 4,000 draws). So the bank is at 86% of uniform —
there is real clustering, because the archer sprays from wherever it is
standing, and it is mild. **A viewer sees a ring closing, not a fan.**

## 2.4 How far the quarry was, when each arrow stuck

```
  p10    p25   median    p75    p90
  187    265      367    490    613
```

Against a hall diagonal of 954. A quill has a **median 367 units** to cross.

---

# 3. THE RELEASE, AND BOTH OF ITS KNOBS ARE FREE

The mechanic injected on Ironhail's body carrying **curse** — the cell exactly
as `row_price` priced it — window 8s, charge 15s, released all at once.
**The floor is the same body with the same window opening and closing and
nothing coming out of it**, so the difference is the ultimate and nothing else.

## 3.1 The aim rule is a picture decision

25 foes x 6 seeds an arm, floor **55.3%**:

```
arm       win%     lift    quill hit rate   parried   quill dmg/fight
back     90.0%   +34.7        19.0%          19.6%          153
normal   88.7%   +33.3        18.7%          21.6%          140
aimed    90.0%   +34.7        23.4%          27.6%          171
```

**The three are one number.** n=150 an arm, SE ~4pp, and v60 §2 established
that a difference needs ~12pp at this scale to be real. The *per-arrow* rates
do separate — n≈3,600 arrows an arm — so `aimed` genuinely lands a quarter more
of its quills and genuinely eats a third more parries, because an arrow flying
at the quarry flies into the quarry's own blade. **None of it reaches the win
rate, because the extra damage is overkill.**

This is `grab_lab`'s result one relic along: *any arrangement delivering the
same held seconds is worth the same*. Here it is *any arrangement delivering
the same quills*. **Rick took `back`** — each quill retraces its own flight,
reversed — which is the literal reading of his own sentence and the only one of
the three that aims at nobody.

## 3.2 And so is the weight, across a factor of two

25 foes x 8 seeds an arm, floor **55.0%**:

```
dmgMul   win%     lift    quill dmg/fight   quill hits/cast
 0.40   77.0%   +22.0            91              2.5
 0.55   77.5%   +22.5           112              2.5
 0.70   79.5%   +24.5           126              2.5
 1.00      —    +34.7 (n=150)   153              2.4
```

**Between 0.40 and 0.70 the ultimate does not change value**, 2.5pp across the
range against an SE of 3.5pp — while the damage it delivers rises 38%. The
geometry is identical at every weight (2.5 quill hits a cast, by construction),
so what the extra damage buys is overkill on a quarry that was going to die
anyway. It is only at full weight that the curve breaks out.

**So the weight is chosen for the number that floats over the ball, and the
blade pays.** That is v43's *"how much of Paradox IS the field"* on a new relic
and it is open item 16's question a second time.

## 3.3 And in the world the relic ships into, 0.55 IS the field median

Everything above is `row_price`'s world — every ultimate in the hall switched
off — because that is where the +15.6 that chose this cell was measured. It is
not the world the relic ships into. Re-run with the field keeping their
ultimates and only the shooter's own off, 25 foes x 8 seeds an arm:

```
arm            win%     lift    quill dmg/fight
none          34.5%        —          0
back@0.55     55.5%    +21.0         99
back@1.00     76.0%    +41.5        142
```

**The floor falls 55.0% -> 34.5%** when the field gets its ultimates back —
20.5 points, inside the 13-22 v60 §3 measured on six cells, and the reason is
that body has no ultimate of its own against a field that all have theirs.

And now the comparison is like for like. `ult_price`'s **field median is
+20.4**, measured in exactly this world. **At `dmgMul` 0.55 this ultimate is
worth +21.0 — the field median to within a fifth of a point.** At full weight
it is **+41.5**, which would make it comfortably the strongest ultimate in the
game.

> **So the weight is not a taste after all, and the number is 0.55.** §3.2 is
> still true and still the reason this was cheap to settle: between 0.40 and
> 0.70 nothing moves on the balance sheet, so the design was free to be placed
> wherever the roster wanted it, and the roster wanted the median.

**The lift widens with the weight far faster in this world than in the other**
(+22.5 -> +34.7 there, +21.0 -> +41.5 here), which is what a lift does when it
is applied to a lower floor and is not evidence of anything else.

---

# 4. THE COLLAPSE, AND THE ENGINE HAD ALREADY ANSWERED IT

`collapse` runs at 4.2 units/s from 21s, so a wall travels 33.6 units across an
8s window against an arrow radius of 24. Measured, per quill, as the inset when
the arrow stuck against the inset when the quiver loosed:

**the wall arrives a mean 9.6 units, worst 33 — and 8.4% of quills (1,400 of
16,641) were swallowed outright**, the hall having closed by more than an arrow
radius on top of them.

**The build does not have to solve this, because `plantVine` already did.** A
vine is stored as `{wall, u}` — a wall identity and a normalised position ALONG
that wall — and `tickVines` recomputes its position every frame from the
CURRENT inset, under a comment reading *"THE PLANT RIDES THE WALL IN."* A quill
stored the same way is never outside the room, never needs clamping, and never
has to be counted as swallowed. **The lab clamps because a lab is not a build;
the build should ride the wall in, and then this section describes a problem
that does not exist in the shipped relic.**

---

# 5. THREE OF THIS LAB'S OWN FINDINGS WERE THE LAB

Recorded because `06-docs/v60` §5's open decision 5 is that a session's own
error rate is the argument for its checks, and because two of these three would
have reached a design document.

1. **"100% of quills are clamped by the collapse"** — false, and it could never
   have read anything else. A spent arrow's centre is already inside `n + r` by
   construction, so a release margin of `r + 2` moves nearly every quill
   whether the hall moved or not. **A boolean cannot measure a distance.**
   Replaced with the inset difference, which is 9.6 units and is the mechanic.

2. **"342 banked arrows are lost between the wall and the volley"** — false. A
   fight that ends inside its own window never reaches its release, so its
   quiver is STRANDED, which is the last window and not a leak. The check now
   balances `banked = released + stranded` and passes.

3. **"+34.7 is a field-median ultimate"** — withdrawn before it was written
   down. `ult_price`'s field median of +20.4 is measured with every OTHER
   ultimate live; this lab's floor had none of them. v60 §3 measured that gap
   at 13-22 points of floor. §3.3 runs the arm in the right world instead of
   quoting a number from the wrong one.

---

# 6. REGISTERED PREDICTIONS

Written before a builder exists, so the stage gates can refute them. Ravelbone
§5a is the argument for doing this at all: **every instrument in the repo was
green about a relic ten points off its own design's prediction, and only the
registered number could see it.**

1. **A cast banks 12-14 quills and releases them.** 13.4-13.8 a cast with the
   field's ultimates off and **12.2-12.6 with them on** — an archer that is
   being hit fires less — against a 15.2 sliding-window mean measured on a
   fight with no windows in it at all. A built relic outside 11-15 means the
   window is not catching what this document thinks it catches.

2. **A released quill lands 19-21% of the time**, against the 8.4% an ordinary
   arrow lands. If the built number is near 8%, the release is a re-roll of the
   same shot and the ultimate is not doing what §1 says.

3. **2.4-2.6 quill hits a cast, at every weight.** The geometry does not depend
   on the damage; if it moves with `dmgMul`, something is reading the weight
   that should not be.

4. **At `dmgMul` 0.55 the ultimate is worth +21.0 in the shipping world**,
   against `ult_price`'s field median of +20.4. This is the number the stage-2
   gate exists to refute, and it is the one Ravelbone §5a says is the only
   instrument that can see a design that missed its price.

5. **The blade moves a little, and the DIRECTION is a prediction rather than a
   plan.** The lab puts this body at **55.5%** against 25 non-bow foes at the
   type's own `dmg` 16.23, so the answer is probably just below it. Two
   cautions, both earned: the lab excludes bow-on-bow entirely and `verify`
   does not, and Ravelbone's open item 43 is this exact sentence written
   confidently in the wrong direction one relic ago. **What settles a blade on
   this roster is a wide direct measurement at n >= 1000 a point, on both
   sides, repeated on a second block — never a bisection.**

---

# Open decisions

1. **THE NAMES.** The fighter and the ultimate, and the scrunch card wording.
   Rule 2, and none of them is in this document.

2. ~~**WHAT THE WEIGHT SHOULD BE.**~~ **ANSWERED BY §3.3 rather than
   deferred: 0.55**, because it is free on the balance sheet across 0.40-0.70
   and the shipping world puts it on the field median there. What is still
   open is only whether Rick wants a heavier number floating off the ball at
   the cost of being the strongest ultimate in the game.

3. **DOES THE QUIVER FIRE IF THE CASTER DIES INSIDE ITS OWN WINDOW?** Unbuilt
   and unasked. The arrows are in the wall and not in the bow, and the school's
   own precedent is Deadfall, whose mines wait forever. 8.4% of banked quills
   sit in a window the fight ended inside (§5.2), so this is not a corner case
   — it is one window in twelve.

4. **DOES THE RELEASE COME AT ONCE OR IN ORDER?** All sixteen on one frame is
   what was measured. Firing them in the order they stuck, a few frames apart,
   is the same balance and a different set-piece — and Deadfall's own lesson
   was that *at most one charge falls per frame* because a loop that fires a
   whole figure in one step leaves nothing to watch.

5. **THE QUILL IN THE WALL IS THE TELEGRAPH AND IT MUST NOT BE `m.ultFx`.**
   Open item 25. A window ultimate whose art hangs off the single `ultFx` slot
   is erased the moment the opponent casts anything — measured at 0.0% survival
   against Ironhail. This relic's window state must carry its own art, which is
   Deadfall's fix and is one field.

6. **THE RELEASE IS THE LOUDEST THING THIS RELIC DOES AND `_burst` DOES NOT
   LOOP.** §4.5, live and chain-wide. Sixteen arrows leaving stone at once
   wants more than 0.6s and the toolkit cannot hold a note.

# v53 — STAGE 1 BUILT. Curse stops eating maximum life and starts remembering, the roster is bit-identical everywhere it should be, and the one relic the registered prediction named is the one it got wrong.

**2026-08-30, Claude Code.** The build of `06-docs/v49/curse-rework-v49.md`,
under the plan in `06-docs/v51/umbral-build-brief-v51.md` §2. Cowork designed
and priced; this is stage 1 and stage 1b of three.

```
in    02-chain/sc-vesper.html      27 relics          NOT sc-thornshear — §1
out   02-chain/sc-curse.html       27 relics, curse remembers
new   tools/curse_build.py         the builder
      tools/curse_check.py         the probe, 16 checks
      tools/umbral_sweep.py        stage 1b, three blades
edit  tools/chain_audit.py         it could not see this builder at all — §6
```

---

# 1. IT IS BUILT OFF VESPER, NOT OFF THORNSHEAR, AND THAT IS A DEVIATION FROM THE BRIEF

The brief's §0 table says `sc-thornshear.html -> sc-curse.html`. Thornshear
was the build of record when the brief was written; **Vesper has landed since
and is the tip.** Building off Thornshear would have silently un-shipped the
twenty-seventh relic — the exact class of drift `docs/ARCHITECTURE.md` §1 and
CLAUDE.md §0's "THE CARRY IS NOT DONE WHEN THE CHAIN IS" exist to prevent.

Every measurement behind this stage was taken on 26 relics. The twenty-seventh
is vigil, carries no curse, and touches nothing the rework touches, so the
design survives the move intact. **What moves with it is one number in every
gate: `engine_ab` must be identical on TWENTY-FOUR non-umbral relics, not
twenty-three.** It is.

`curse_build.py` refuses to run on a source with no `"sentinel"` in it, so
this cannot be quietly undone by passing the old `--src`.

---

# 2. WHAT THE BUILD DOES

| | |
|---|---|
| `maxStacks` | 8 -> **3** |
| `maxHpLoss` | **deleted**, not zeroed |
| `echo` | **0.08** of everything remembered, added to every later blow |
| `dur` | 99, unchanged |
| tip | `"Adds 8% of a remembered blow per stack"` — 38/40 |
| Dirge, Eclipse | `apply:{curse:3}` deleted; tips lose the clause |

Three edits in `resolveHit`, in the order the brief specifies: the echo is read
off the stacks that **already exist**, `dmgBase` is taken **pre-echo**, and the
echo is folded into `dmg` **above the Aegis block** so a wall eats it, a ward
absorbs it, hit-stop scales with it and knockback carries it.

## 2.1 THE STACK COUNT IS DERIVED FROM THE POOL, WHICH THE BRIEF DID NOT ASK FOR

Brief §2.2 asks that `stacks("curse")` and `cursePool.length` always agree, and
says to assert it. **A convention that two call sites must both fire is not
agreement, it is a promise**, and the assertion would only ever catch the
promise being broken after the fact.

So `apply()` derives curse's stack count from the pool length. The memory IS
the stack: a caller that applies curse without handing `pushCurse` a memory
refreshes the clock and adds nothing. That is deliberate and it is the same
sentence v49 measured — an ultimate that "applies 3 Curse stacks" out of
nowhere was worth +0.0, because a stack with nothing to remember is not a
stack. `curse_check [3]` asserts the invariant anyway, over 790,247 frames,
because the derivation is the line that could be edited away.

## 2.2 THE ECHO IS ROUNDED

Every damage number in this engine is an integer — `Math.round` upstream, crit
and jitter folded in before it, and `float()` prints the result over a ball. An
unrounded echo puts `96.32` on screen. One line, and it is why `curse_check`'s
central identity can be an exact equality rather than a tolerance.

## 2.3 TWO READERS OF A DEAD FIELD ARE DELETED, NOT LEFT AGAINST A CONSTANT

`maxFrac` in `drawGlassRelic` is 1 forever now. The frosted dead-cap block and
the graduation-mark suppression beside it are **gone**, not commented out —
brief §2.5. This project already carries two dead knobs in its open items
(`shot.life`, `s.snap`) and both are there because a reader that cannot fire
teaches the next person they are watching something they are not.

## 2.4 `_stCurse` IS RE-CUT, BECAUSE THE SHIPPED ART BECAME A LIE

Motes that left and never returned said *maximum life, gone for good*. Nothing
leaves any more. **One mote per remembered blow**, sized by that entry's share
of the pool, running its cycle from 1.85R inward to 1.02R and repeating — the
old motion exactly reversed, with the wisp trailing outward behind the mote
instead of downward after it. The count IS the stack count, capped at 3 and
countable at phone size.

Every position stays a pure function of `(side, index, m.t)` through
`shellHash`. Never `this.rng()`.

## 2.5 THE TAG PRINTS THE POOL, AND THE TEACHING PANEL DOES NOT

`statusTag` grew an optional fifth argument. Curse is the only status with a
number worth reading at the point of contact; every other one is a rate whose
stack count is already drawn on the ball. `CURSE 96` at the impact, then a
detonation for 96, is a story a viewer can follow — and it is the **pool sum**,
not the pending echo, because the echo peaks at 5-8 and the pool is what both
ultimates read.

The first time curse lands in a match the teaching panel fires instead, and it
carries the name and the tip and no number. Deliberate: the panel teaches, the
repeat tags report. It means the number is missing exactly once per match.

---

# 3. THE GATES

```
curse_check.py          16/16
engine_ab (24 relics)   2760/2760 matches identical, field for field
chain_audit             13/13 inserts survive
tip_audit               0 effect fields the tips never mention
post_identity           325,708 px identical, max delta 0
verify --n 40           12/13  — and see §3.2
row_price --type flail  ran clean; it cannot see curse — see §3.3
```

## 3.1 EVERY UMBRAL WIN RATE MOVED, AND NOTHING ELSE MOVED MORE THAN 2.2pp

`verify --n 40` on both builds, 14,040 matches each:

```
  Gravemourn    51.4% -> 61.1%   +9.7
  Nightfell     45.8% -> 50.0%   +4.2
  Twinshade     45.6% -> 49.0%   +3.4
  ...
  every other relic                -2.2 .. +1.9
```

**The small deltas on the other twenty-four are arithmetically necessary and
not evidence of anything.** `engine_ab` proves non-umbral against non-umbral is
bit-identical over 2760 matches; a relic's roster-wide win rate includes its
matches against the three relics that just got stronger, so it must fall.

## 3.2 THE REGISTERED PREDICTION IS HALF STRUCK, AND GRAVEMOURN IS THE HALF

Brief §6: *after layer 1 the three umbral relics land inside the field band
(50.0% mean, 6.4% sd) with no ultimate changes beyond the two stripped `apply`
fields.*

Nightfell lands at **50.0%** and Twinshade at **49.0%** — dead centre, and the
prediction holds for both. **Gravemourn lands at 61.1% and is now the strongest
relic in the game**, 3.6pp clear of the next one. It gained the echo *and* lost
a payload `ult_price` measured at **-3.2**, so it was paid twice.

That is what stage 1b's blade re-sweep is for and it is not a defect. It is
recorded here because the prediction was registered in order to be falsified,
and half of it was.

The roster spread went **19.0pp -> 21.5pp** (Goreshard 39.5 .. Gravemourn
61.1). `verify`'s 30-70% band still passes on every relic.

## 3.3 THE THIRTEENTH CHECK FAILS ON BOTH BUILDS, ON THE SAME PAIRING, AT THE SAME SECOND

```
  sc-vesper.html   FAIL  Slagheart/Threshmaw 32.2s .. Lightkeeper/Farwarden 77.3s
  sc-curse.html    FAIL  Gravemourn/Slagheart 30.7s .. Lightkeeper/Farwarden 77.3s
```

**77.3s on both, to the digit, on a vigil-against-vigil pairing containing no
umbral relic at all.** CLAUDE.md §0 already names this as known and accepted;
this is the cleanest demonstration of it the project has, because the control
was run in the same session on the same runtime. **Do not credit this build
with it either way.**

## 3.4 `row_price` CANNOT BE THE GATE THE BRIEF ASKS IT TO BE

Brief §6 asks for *"row_price shows curse delivering effect, not occupancy"*.
`row_price` prices **open** cells — cells with no relic in them yet — and
umbral x flail is Gravemourn's. Curse never appears in its output and cannot.

It was run anyway and corroborates the kill from a tool that had no idea it was
being asked: **`max hp removed: 0 of 400`** on every row. Its own check failed
on the sanctified-against-verdant flail disagreement, which is open item 8 and
is about `cell_survey`, not about this build.

**`curse_check [8]` is the delivered-effect measurement for curse.**

---

# 3.5 STAGE 1b — THREE BLADES RE-SWEPT, AND ONLY ONE OF THEM MOVED

`umbral_sweep.py`, 7566 fights. Three passes per relic: a wide curve, an
escalating bisection inside the bracket the curve measures, and a wide
confirmation either side of the answer.

```
                shipped    swept    applied
  gravemourn      44.10    39.79      39.79
  nightfell       15.83    15.90    UNCHANGED
  twinshade        8.30     8.38    UNCHANGED
```

**THE OTHER TWO ARE NOT APPLIED, AND THAT IS THE MEASUREMENT'S OWN ANSWER
RATHER THAN A SHORTCUT.** +0.07 and +0.08 are a quarter of one percent on a
quantity this instrument locates to about a damage point. `verify --n 40` —
1040 fights a relic, the widest instrument in the repo — independently put the
two at **50.0%** and **49.0%** at the numbers they already ship. Writing 15.90
claims two digits nothing here can see.

**A change smaller than the error bar is not a tune, it is churn that looks
like one.**

## 3.5-0 AND THE GATE IS GREEN. `verify --n 40` ON THE BLADED BUILD

```
                stage 1   stage 1b        and the field
  Gravemourn      61.1%      51.6%        spread  21.5pp -> 18.0pp
  Nightfell       50.0%      50.8%        Goreshard 40.0 .. Slagheart 58.0
  Twinshade       49.0%      49.3%        every relic inside 30-70%
```

**All three umbral relics are inside the field band and the roster spread is
now NARROWER than the build this started from** (19.0pp on `sc-vesper.html`).
Gravemourn came off the top of the table and landed 1.6pp from target, which
is inside the sweep's own precision of where it aimed.

Nightfell and Twinshade both drifted UP slightly without their blades being
touched — because the relic they lose to most often got weaker. That is the
fixed point in §3.5c resolving itself, and it resolved in the direction the
joint pass flagged but at a tenth of the size it claimed.

`engine_ab` is still 2760/2760 identical on the 24 after the blade change, as
it must be: Gravemourn is not one of the 24.

## 3.5a §4.5 WAS RIGHT AND THE CURVE IS NOT MONOTONIC

Gravemourn's pass-1 curve:

```
   28.00  24.0%      37.60  45.2%      47.20  67.3%
   32.80  37.5%      42.40  51.9%      52.00  60.6%
```

**More blade makes it worse past about 47.** Mean duration falls 44.2s -> 36.7s
across that range, so the relic is killing faster and winning less — which is
the shape you get when a bigger blow throws the quarry further out of reach of
a weapon that only lands 5.6 times a fight. That is v51 §4.3's
"knockback eating its own window" showing up on the BLADE rather than on the
ultimate, and nobody had looked for it there.

The brief registered the superlinear response as a prediction before it was
seen. It is the reason pass 1 exists: a bisection started from a guessed
bracket cannot see a curve bend, and would have been perfectly happy to
converge inside the wrong one.

## 3.5b THE SHAPE AT THE ANSWER, WHICH IS WHAT THE WIN COLUMN CANNOT SAY

```
  relic         echo share   pool mean   peak   pool up   pool full
  gravemourn         11.2%         111    303       77%        41%
  nightfell          17.8%          62    189       89%        69%
  twinshade          21.6%          37     95       91%        70%
```

Monotone in blows-per-fight, in both directions at once, and the design says
both should be: **the relic that lands often is the one made mostly of echo**
(21.6% against 11.2%), and **the relic that lands rarely is the one with the
deepest pool** (111 against 37), because displacement converges on the biggest
blows and Gravemourn's are enormous. One mechanic, two archetypes, and the
numbers separate them cleanly.

## 3.5c THE JOINT PASS FOUND A FIXED POINT PROBLEM AND THEN FOUND ITS OWN LIMIT

Each relic is swept against a field that CONTAINS the other two, so three
relics tuned one at a time and then applied together is a fixed point nobody
checked. `umbral_sweep` now checks it — all three answers measured with all
three in place. At n=364 it reported Gravemourn -3.0pp and Nightfell +6.0pp off
target and flagged both.

**Then the same table refuted the flag.** Nightfell measured 50.3% at 15.96 and
56.0% at 15.90 — 0.06 of a damage point apart, both at n=364, 5.7 points apart.
A roster win rate is 26 pairings of correlated fights, not 364 independent coin
flips, so its real precision is far worse than the binomial figure and **a 3pp
verdict at n=364 is a verdict about seeds.** The joint pass now takes its own,
much larger sample and says why in the code beside it.

This is CLAUDE.md §0's bisection lesson arriving a second time, in a tool
written to respect it. Being told not to trust a tail was not enough; the
confirmation had to be measured against itself.

**AND THE WIDE INSTRUMENT REFUTED THE FLAG.** `verify --n 40` — 1040 fights a
relic against the joint pass's 364 — put the three at 51.6 / 50.8 / 49.3, all
within 1.6pp of target. The joint pass called Nightfell +6.0pp off; it is
+0.8pp off. **The flag was right about the direction and wrong about the size
by a factor of seven**, which is exactly what a 3pp verdict at n=364 is worth.
The check stays, because a fixed point genuinely does need checking; what
changed is that it now takes a sample that can answer the question it asks.

---

# 4. [8] IS TWO DIFFERENT QUANTITIES AND THE BRIEF NAMES THE ONE THAT DOES NOT GIVE 100%

Brief §5.8: *for every status, damage delivered with the channel minus damage
delivered with it deleted. Curse's ratio goes from 3% to ~100%.*

Those are not the same measurement. Measured three ways on the built relic:

```
  the echo as a share of all damage delivered   8.7%    exact, one arm, no A/B
  the A/B on raw `dealt`, as worded            +3.2%    confounded — see below
  the same A/B normalised to damage RATE      +10.2%
```

**THE RAW-`dealt` A/B IS CONFOUNDED BY FIGHT LENGTH, AND IT INVERTS.** Delete a
damaging status and the fight runs *longer*, so the blade delivers more and the
difference comes back negative:

```
  smite        6.26 -> 6.93 dealt/s   raw dealt   -28.1%   normalised  -10.7%
  hemorrhage   5.60 -> 6.14           raw dealt   -25.1%   normalised   -9.6%
```

An instrument that reports smite as delivering less than nothing is measuring
something else (§4.6). `curse_check` therefore prints the exact share, the
normalised A/B and the win-rate delta, and fails only on a channel that moves
none of them.

**Which reading "~100%" meant is open decision 1.**

## 4.1 AND ALL EIGHT CHANNELS ARE MEASURED FOR THE FIRST TIME

```
  status       dealt/s(on)  (off)    delta    win(on) win(off)   delta
  smite             6.26     6.93    -10.7%     47.2%   40.3%     +6.9pp
  hemorrhage        5.60     6.14     -9.6%     50.0%   19.4%    +30.6pp
  entangle          7.56     7.11     +5.9%     52.8%   25.0%    +27.8pp
  hex               6.51     5.98     +8.1%     43.1%   20.8%    +22.2pp
  curse             7.94     7.13    +10.2%     47.2%   33.3%    +13.9pp
  sunder           10.24     8.85    +13.6%     54.2%   55.6%     -1.4pp
  blessing          4.92     4.85     +1.4%     33.3%   33.3%     +0.0pp
  ward              5.66     5.68     -0.4%     37.5%    9.7%    +27.8pp
```

**BLESSING READ AS DEAD, AND THE INSTRUMENT WAS WRONG, NOT THE CHANNEL.** It
HEALS. A damage rate and a win rate are blind to it by construction — §4.6
again, in the same tool, one check later. On the channel it actually has it
restores **711 hp over 24 fights** against 0 with `hps` zeroed. `curse_check`
now measures it that way, on foes chosen to carry no `dps` status so the whole
hp delta across `tickStatus` is attributable.

**SUNDER AND WARD ARE WORTH LOOKING AT.** Sunder moves damage rate by +13.6%,
the largest in the table, and win rate by **-1.4pp**. Ward moves damage rate by
-0.4% and win rate by **+27.8pp**. Both are coherent — sunder is an amplifier
on a fight it also shortens, ward is defence and buys no damage at all — but
neither has ever been priced before and neither is a number anyone has looked
at. Not a defect. Open decision 3.

---

# 5. WHAT `curse_check` ASSERTS, AND WHY THE CENTRAL ONE IS EXACT

`resolveHit` is wrapped so the pool is photographed either side of every blow,
`hurt` is wrapped so the damage that actually arrived is counted, and this
identity is asserted on **every single curse application**:

```
  pushed  ==  damage that arrived  -  round(pool sum BEFORE the blow * echo)
```

1264 applications, **0 bad**. It holds only if the memory is `dmgBase` and the
echo is read off the stacks that already existed; a build that remembered `dmg`
fails it on the second blow of the first fight.

The clean arm excludes vigil foes on purpose — a ward absorbs inside `hurt` and
an aegis eats before it. That is not a hole, it is check [5], which asserts the
**harder** identity `arrived + eaten == pushed + echo` on exactly the relics [1]
leaves out: 18/18 through a wall, 232/232 into a plate.

```
  [1] the memory is dmgBase, never the echo        1264 applications, 0 bad
  [2] top K, and the trim drops the weakest        0 bad, K=3
  [3] stacks("curse") == cursePool.length          790,247 frames, 0 bad
  [4] a fresh stack does not pay on its own blow   144 first-stack blows, 0 bad
  [5] an Aegis wall eats the echo                  18/18
  [5b] a Ward absorbs it                           232/232
  [6] a shade FEEDS the pool                       211 of 443 shade blows
  [6b] a shade CASHES it                           1601 damage of echo
  [7] maxHp never moves                            186 bodies, 0 moved
  [8] curse delivers what its tip promises         8.7%, exact
  [8b] no channel delivers nothing                 all eight move something
  [9] the re-cut art draws without throwing        2758 calls, 0 exceptions
  [9b] the mote count IS the stack count           2758/2758
```

## 5.1 [9] EXISTS BECAUSE VESPER'S DID NOT

Two picture faults shipped through 27 probe checks, a 280-match `engine_ab`,
`chain_audit` and `post_identity`, and died on the first rendered frame — and
the probe's own check passed on one of them **because it was regexing the
drawing function's source for a call it never resolved.** A string does not
resolve a reference.

This build re-cut `_stCurse` to read `f.cursePool` and `f.curseSum()` — fields
that did not exist an hour earlier, on an object the renderer only ever sees
through `drawStatus` — and **deleted a block out of `drawGlassRelic` whose
neighbours still use the variables it declared.** Both are exactly that fault
class. So [9] drives real matches to a cursed fighter and calls `_stCurse`,
`drawGlassRelic` and the whole `renderer.draw` against a real 2D context.

## 5.2 AND TWO OF THE CHECKS WERE WRONG BEFORE THEY WERE RIGHT

**A CHECK THAT CANNOT TELL CODE FROM THE COMMENT EXPLAINING IT FIRES ON ITS OWN
EXPLANATION.** `noOwnerGuard` searched `resolveHit` for `self === owner` and
found it — inside the paragraph this build wrote saying there must never be
one. The builder had made the identical mistake an hour earlier, refusing to
write because its own comment quoted the field it deletes. Both now strip
comments before matching. **This will happen again to anything that greps
shipped source, because this codebase explains itself in the file.**

**"maxHp NEVER MOVES" IS NOT "maxHp IS ALWAYS 400."** The first cut of [7]
asserted the constant and failed on Twinshade: a shade is **born** at
`baseHP * u.hp` = 160 and is a real Fighter. A probe that reads the roster's
ceiling off a constant reports the summon mechanic as a curse regression. What
the deleted channel could do was MOVE a ceiling mid-fight, so the ceiling is
now photographed the first frame each body exists and asserted against itself
from then on.

---

# 6. `chain_audit` COULD NOT SEE THIS BUILDER AT ALL

It printed **"no *_NEW inserts found in curse_build.py — nothing to audit,
which is itself a failure"**, which is the correct message and reads as clean
to anyone moving fast.

It discovers inserts by finding module-level `*_NEW` string constants.
`curse_build.py` keeps its edits in one table of `(label, old, new)` tuples,
which is an ordinary shape and one the tool cannot see. **This is the THIRD
time its discovery has been too narrow** — its own comments document the raw
string case and the computed-insert case, each added the same way.

Two additions, both fallbacks that only run when the earlier passes find
nothing, so no existing builder changes behaviour:

- any module-level sequence of tuples whose last element is a multi-line string
  is an insert table by any name, and the tuple's first element becomes the
  label so the report still says WHICH edit went missing
- **marker lines containing `%PLACEHOLDER%` are skipped.** A builder templates
  its inserts, so a marker chosen from a templated line can never match a built
  file and always reports unresolved. Two of thirteen did.

13/13 now.

---

# 7. WHAT IS NOT DONE

- **F1, the film gate.** Brief §0: thirty seconds on the new motes and the
  `CURSE nn` tag. `_stCurse` is measured to draw without throwing and to draw
  the right number of motes; **nobody has watched it.** That is §4.1's whole
  point and it is the next thing.
- **Stage 1b's numbers are not in the builder yet** — see the sweep section
  filed beside this doc.
- **Stages 2 and 3** — Gravemourn's and Nightfell's ultimates.
- **`app/main.js`'s `GAME` line** still names Vesper. It moves in the stage 1
  commit; CLAUDE.md §0 warns that no tool can see it.

---

# Open decisions — Rick's and cowork's

1. **WHICH READING OF [8] DID "3% -> ~100%" MEAN?** §4. The sentence defines an
   A/B difference and quotes a figure only the direct share can produce. The
   direct share is 8.7%. Nothing is blocked on the answer; the check ships
   measuring all three.
2. **IS BUILDING OFF VESPER RIGHT?** §1. It is the tip and the brief predates
   it. Redoing it on Thornshear is cheap but un-ships a relic.
3. **SUNDER AND WARD HAVE NEVER BEEN PRICED AND NOW HAVE BEEN.** §4.1. Sunder
   is the biggest damage-rate channel in the game and costs 1.4pp of win rate;
   ward buys no damage and 27.8pp of win rate. Neither is a defect. Whether
   either wants looking at is not this build's call.
4. **GRAVEMOURN IS THE STRONGEST RELIC IN THE GAME AT 61.1%** until 1b lands.
   The blade sweep is the answer the brief specifies; if the answer it returns
   is a very large cut, that is a statement about how much of the relic the
   echo now is, and it is worth reading before it is applied.

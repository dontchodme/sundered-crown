# v56 — SHROUDMAUL IS BUILT, AND GRASP IS THE FIRST ULTIMATE IN THIS GAME THAT DEALS NOTHING AND HAS TO EARN ITS PAYOFF. Four stages, all four green — and the brief registered three predictions to falsify, of which one landed exactly and two are refuted by the same single cause: `grab_lab` held its charge clock while its own window ran, and the engine does not.

**2026-08-31, Claude Code.** Built to
`06-docs/v56/SHROUDMAUL-BUILD-BRIEF.md`, off the designs in
`06-docs/v55/warhammer-curse-v55.md`, `06-docs/v56/grab-v56.md` and
`06-docs/v55/charge-v55.md`.

```
02-chain/sc-nocard.html      27 relics                       the build this started from
02-chain/sc-revenant.html    stage 1  Gravemourn's ultimate is REVENANT again
02-chain/sc-shroudmaul.html  stage 2  the 28th relic, ultimate stubbed at charge 1e9
02-chain/sc-grasp.html       stage 3  GRASP + stage 3b's blade   BUILD OF RECORD
```

---

# 0. THE BRIEF SAID BUILD OFF `sc-nightfell.html` AND THAT IS ONE VERSION STALE

`SHROUDMAUL-BUILD-BRIEF.md` §1 names `02-chain/sc-nightfell.html` as *"the
build of record, 27 relics"*. It has not been since `cardstrip_build.py` ran
earlier the same day: **`sc-nocard.html` is**, and the difference is the fight
card, its 545 lines of renderer and every constant it put in the clock.

Building off Nightfell would have put the card back into the chain tip — which
the brief's own §8 forbids in as many words (*"Do not let the fight card back
in"*). So stage 1 is built off `sc-nocard.html`. Nothing else in the brief is
affected: every anchor it names is upstream of the card's removal.

---

# 1. STAGE 1 — REVENANT, AND IT IS THE ONLY STAGE THAT CAN BE PROVEN INERT

`tools/revenant_rename.py`. One string and five comments.

```js
ult: { name: "Revenant", ... }        // was "Grasp"
```

Rick took *Grasp* at build time over the v51 brief's REVENANT; the 28th relic's
entire §1 is grasping, the collision is on the **verb**, and it is inside the
same school. So the grabbing word goes to the relic that grabs.

**GATE: `engine_ab` 2808/2808 IDENTICAL, all 27 relics.** A name is not read by
the simulation, and the brief made this its own commit for exactly that reason:
if the bits had moved, the finding would have been in the harness and not in
the relic, and it is worth knowing that before three stages of new objects are
in the world. They did not move.

## 1a. AND THE COMMENTS MOVED WITH IT, WHICH IS NOT TIDINESS

Five paragraphs elsewhere in the build defined themselves BY REFERENCE to
Gravemourn's ultimate by name — the SFX cast voice (*"like Grasp's it does not
resolve"*), `tickDeadfall`'s header (*"the Winnowing's kunai and Grasp's
hands"*), `tickSling`'s own restore, and both halves of the blade's history.
Stage 3 puts a **different** ultimate called GRASP into the same file, so every
one of those sentences would silently have started naming the wrong relic.

CLAUDE.md settled this class one build ago when the card was cut: *"a comment
defining a thing against something that no longer exists is worse than no
comment in a codebase that teaches through them."* Here it is worse still — the
thing it names would exist, and be something else. **The builder refuses to
write if the string survives anywhere in the output.**

> **AND IT FIRED ON ITS OWN EXPLANATION, INSIDE FIVE MINUTES OF BEING
> WRITTEN.** The paragraph explaining the rename quotes the old name, so the
> refusal caught it. That is `curse_check` and `curse_build`'s bug for the third
> time in three sessions. It is fixed by EXCISING the one block the builder just
> wrote, by identity, rather than by pattern-matching around it.
>
> **AND THE LINE-BY-LINE COMMENT STRIPPER IN THIS REPO IS NOT ENOUGH.** Every
> earlier version drops lines containing `/*`, `*/`, `//` or a leading `*` —
> and the INTERIOR of a block comment in this codebase is plain indented prose
> with none of those on it. `shroudmaul_build`'s §4.5 refusal fired on its own
> paragraph (*"`f.pin` is the Stasis Field's only exclusive verb"*) for exactly
> that reason. Both strippers now remove the block AS A BLOCK.

Nothing outside the build needed to move: `cinema_vo.py` and `hook_vo.py` read
relic NAMES and not ult names, and `grasp_price.py` never contained the string.
`gravemourn_build.py`'s `ULT_NAME` is deliberately left as it was — it is the
record of what that chain link built, the same way `06-docs/v53` is.

---

# 2. STAGE 2 — THE 28TH RELIC

`tools/shroudmaul_build.py --stage 2`.

```
id          shroudmaul       umbral x warhammer
blades/reach/width/artW/spin/mode/mass/knockMul   THE WARHAMMER'S, copied off
                             Grudgebearer, Censer and Bulwarden. Not invented.
onHit       curse: 1         the school's other three
dmg         23.5             Grudgebearer's, as a start
ult         STUBBED at charge 1e9
```

**THE SILHOUETTE IS NOT NEW WORK AND THAT WAS TRUE WHEN THE CELL WAS PRICED.**
`SHAPES.warhammer` already routes `umbral` to `_whEaten` — a hammer with bites
taken out of it and lit rims where the material stops. It exists, it is 78.6%
distinct from its nearest sibling, and it was the 3rd most distinct of the
fifteen open cells.

**GATES:** `engine_ab` 2808/2808 identical on the 27 (a 28th relic cannot reach
a match it is not in), the page loads with 28 relics and no console errors, and
nothing in the game or in `tools/` hardcodes a roster count — the picker is a
`<select>` populated from `WEAPONS` and `roster_sheet` blocks by `rows[i:i+3]`.
The intro card, which the brief also names, no longer exists.

**Stubbing rather than omitting is deliberate.** The `ult` object is read by
`verify`, `tip_audit`, the scrunch panel and half of `tools/`, and a relic with
no `ult` at all is a shape none of them have ever been handed. `charge: 1e9` is
the same OFF the v55b charge sweep used.

**THE FLOOR CAME IN AT 27.5% AGAINST A REGISTERED 27.1%** (378 fights,
`shroudmaul_sweep --only 0`). That is the first of the brief's three
predictions and it lands dead on.

---

# 3. STAGE 3 — GRASP

`tools/shroudmaul_build.py --stage 3`. Thirteen edits.

```
name        Grasp        charge 15      kind "grip"      dmg 0
dur         8.0s         the window
radius      200          THE MEASURED OPTIMUM AND THE ONE NUMBER THAT IS NOT FREE
cadence     2.0s         THE COOLDOWN. Rick's, off the second clip — §6a-3
grabStun    1.0s         writes `f.stun` DIRECTLY. THREE TIMES the squeeze
squeeze     0.30s        how long the FIST is shut — presentation only, and it
                         is NOT the stun. §6a-2
n           3            grabs to the crush. It paid for the cooldown — §6a-3
trueStun    2.2s         AND IT IS A REGISTERED TRUE-STUN SITE — the fourth
endOnTrue   the window ends on the crush. Rick's clause, worth -10.8 points
apply       NONE         no damage, no curse, no pin, ever
tip         "Grabs repeatedly; the third grab is a true stun, then it fades"  62/72
blade       23.5 -> 21.0    (stage 3b)
```

## 3.1 The four things the brief said would bite, and none of them did

All four are asserted on the TEXT by the builder, which refuses to write, and
again at runtime by `grasp_relic_probe`. They are checked rather than left to a
sweep because **all four look fine in every win rate this repo can produce.**

```
takeHitstun   NEVER. It caps at stunMax 0.26s and divides each application by
              1 + 0.55 x stunDR, so five grabs become one grab and a rumour —
              with every invariant intact and no probe failing. The grabs write
              `f.stun` directly, the way `u.freeze` does. 0 calls in 907,001 ticks
f.pin         NEVER. -3.3 points at IDENTICAL held seconds, and the Stasis
              Field's only exclusive verb. 0 writes in 907,001 ticks
damage/curse  NEVER. 0 hurts, 0 hp moves, 0 pool moves in 907,001 ticks
shades        NEVER. Structural rather than a guard: the loop reads `this.a`
              and `this.b` and nothing else, so there is no `if` to get wrong.
              0 shade states moved across 5,809 ticks with shades on the floor
```

## 3.2 The true-stun register is four now, and only the fifth grab is on it

Rick's own rule, already in the engine in his own words: *"Hitstun shouldnt
stop the windup. but true stuns from ults/abilities should."* There is no flag
— every source writes the same `f.stun` — so the distinction is drawn at the
APPLICATION SITES, and the engine's comment enumerates them. It now says four,
in the same place, so the count stays nameable:

```
hex                     STATUS.hex.stunFor    Spellbreaker, Axiom
ult freeze              u.freeze              Thornwake, Rootfast
the Harrowing's burst   u.stunBase            Lastlight
GRASP'S FIFTH GRAB      u.trueStun            Shroudmaul
```

**The four ordinary grabs DELAY a wind-up and do not cancel it**, which is what
makes the escalation legible in the one place a viewer can read it. Adding the
whole window would have turned a rhythm into a lockout. `grasp_relic_probe [4]`
asserts `breakInTick == breakTrue == crushes` and photographs the effect at the
call: **17 wind-ups caught over 162 fights — 5 forges, 11 spike storms and 1
winding Sentinel — and all 17 taken.**

> **AND THE PROBE ASKS WHAT THE ENGINE DOES RATHER THAN WHAT THE BRIEF SAYS.**
> The brief names *"the Crucible's forge, Bloodmill's spin-up and Reprisal"* as
> the three wind-ups. **`breakSpin` does not touch Reprisal's draw and never
> has** — `f.ultDraw` is not in that function. A probe that had written down
> the brief's model would have reported a defect that is not there, which is
> `gravemourn_relic_probe`'s mistake three times in one session.

---

# 4. THE THREE PREDICTIONS, AND TWO OF THEM ARE REFUTED BY ONE CAUSE

The brief registered: *"at n 5, radius 200, window 8.0, grab 0.5 and true 2.0,
the built relic delivers 6.5-7.0 held seconds a fight and lands within one SE
of +24.9% over its own no-ultimate floor; and the blade bisects to somewhere in
21-23.5 rather than moving far."*

```
                        REGISTERED        MEASURED       verdict
the floor               27.1%             27.5%          LANDS
held seconds a fight    6.5 - 7.0         9.66           REFUTED
lift over the floor     +24.9%            +28.0 / +34.7  REFUTED
the blade               21 - 23.5         19.92          REFUTED, just
```

## 4.1 AND ALL THREE MISSES ARE ONE CAUSE, WHICH IS NOT THE HOLD

`grasp_relic_probe [11]` reports **held seconds A CAST as well as a fight**, and
that is what separates the mechanic from the confound:

```
                    grab_lab (n=5)      the built relic
held a cast              3.70s               3.74s        the MECHANIC. Exact.
casts a fight            1.84                2.58         +40%
held a fight             6.8s                9.66s
```

**The hold is right to within a hundredth of a second. The relic simply casts
40% more often than the lab's did**, and the reason is in the lab:

> `grab_lab.py` drives its own window off match time and advances its charge
> clock **only while `winT === null`** — that is, the charge does not rebuild
> during the eight seconds the window is open. **`tickCharge` does not work that
> way.** `f.charge += dt` runs every step regardless, and only THREE relics in
> the game gate the rebuild — the Crucible, Ironbloom and the bow window (v55b
> §1). So the built relic is handed eight seconds of free charge per cast that
> the lab never gave it, and **every arm in `06-docs/v56/grab-v56.md` is
> measured on a cast rate this build does not have.**

The lab's *relative* readings are unaffected — every arm shares the error — so
the held-seconds law, the monotonic `n` ladder and the reach optimum all
survive. What does not survive is any ABSOLUTE number taken off it.

**THE FIX WAS THE BLADE AND NOT A GATE**, which is the brief's own instruction
(§4.2: *"Expect the built relic to read slightly stronger than the doc and
re-bisect rather than arguing with it"*). Gating the rebuild would have been a
mechanic the design never asked for, on a relic where two of the three
gating precedents are ultimates that own their own resolution window. **It is
worth naming as a fork rather than a defect — see the open decisions.**

## 4.2 The held-seconds law itself

Nothing here re-fits it — `shroudmaul_sweep --only 2` does, and it has not been
run at a useful sample yet. What IS measured is that the per-cast hold matches
the lab to within 1%, which is the half of the law this build could break and
did not.

---

# 5. STAGE 3b — THE BLADE, AND THIS CURVE DOES NOT BEND

`umbral_sweep.py --relics shroudmaul --lo 12 --hi 26`, **4617 fights**.
`umbral_sweep` is now a four-relic tool.

```
pass 1, the curve, n=162 a point
  12.00   9.3%     18.00  32.1%     24.00  64.8%
  14.00  24.7%     20.00  47.5%     26.00  66.0%
  16.00  32.7%     22.00  53.1%

pass 2, escalating bisection inside 20.00 .. 22.00      -> 20.42
pass 3, wide confirmation, n=702 a point, SIDE A ONLY
  19.92  50.0%     20.42  50.4%     20.92  52.1%        -> 19.92
```

**MONOTONE, WHICH THE SCHOOL'S OTHER FLAIL IS NOT.** Gravemourn reads 67.3% at
47.2 and **60.6% at 52.0** — more blade, worse relic, because a bigger blow
throws the quarry out of reach of a weapon that lands 5.6 times a fight. The
sweep was still run wide first, because a bisection cannot tell you which of
those two shapes it is standing on. Third build in a row to need that.

## 5a. AND 19.92 IS WRONG BY A DAMAGE POINT. THE CONFIRMATION WAS MONOTONIC AND STILL NOT ENOUGH

`umbral_sweep`'s pass 3 is n=702 a point with the relic always on side A, and
the seed block it happened to draw reads about four points high. **Everything
else measured that day disagreed with it:**

```
umbral_sweep pass 3, side A, n=702           50.0%   at blade 19.92
shroudmaul_sweep type ladder, side A, n=702  45.2%
an independent side-A block, n=702           45.7%
verify --n 40, side B, n=1080                45.4%
```

So it was re-measured DIRECTLY and WIDE — **both sides, n=1080 a point, on two
independent seed blocks:**

```
block 1   19.92  45.4%    21.00  49.1%    22.00  54.1%    23.00  59.2%
block 2   20.68  47.9%    21.18  52.0%    21.68  52.6%
```

Both monotonic, both crossing 50% at about **21.0**, and block 1 reproduces
`verify`'s 45.4% at 19.92 to the decimal. **Shipped at a round 21.0, because
the honest precision is ±half a damage point.**

**AND `verify --n 40` ON THE SHIPPED BUILD READS SHROUDMAUL AT 50.2%** over
1080 fights, against 45.4% at 19.92. The correction is confirmed by the
instrument that did not tune it.

> **THIS IS v48'S LESSON FOR THE SECOND TIME, AND NOW IT HAS A PRESCRIPTION.**
> A bisection converges on the noise in its own tail — that was v48, and the
> repo's answer was "confirm it with one wide direct measurement". **A
> three-point confirmation is only as good as the ONE seed block it is drawn
> on**, and two n=702 readings of this same number differed by **4.3 points**.
> What settles a blade on this roster is a wide direct measurement at
> **n ≥ 1000 a point, on BOTH SIDES, repeated on a second block.**

> **AND BOTH SIDES MATTERS BECAUSE OF WHERE A NEW RELIC SITS IN THE ARRAY.**
> `verify` pairs `i < j`, so a relic appended to `WEAPONS` is **side B in all
> 27 of its pairings**, while every sweep in `tools/` runs it as side A.
> Measured, the asymmetry itself is small — shroudmaul −1.9pp, grudgebearer
> +2.6pp, nightfell −0.3pp — so it is *not* the explanation here. It is
> measured both ways so that the question cannot arise, and the array position
> is worth knowing before the next relic is appended.

**AND THE SURFACE HERE IS THE SIMPLE ONE**, which has not been true in this
school before. `dmg` moves the blade and the pool and stops — v51 §4.5's
superlinear warning does not apply, because the ultimate carries no damage and
reads nothing. The one knob that moves the ultimate is `n`.

**WHAT THE CUT BUYS:** measured at 19.92 the echo is **16.6%** of everything
Shroudmaul delivers, the pool means **75** and peaks at **214**, and it is **up 87% of the
fight and full 63%** — the deepest pool in the school, which is the cell's whole
argument (v55 §4) surviving the bisection.

## 5.1 And the grab count, priced on the built relic

`shroudmaul_sweep --only 1`, 378 fights an arm, at blade 23.5:

```
n = 2   45.8%   +18.3%      n = 5   55.6%   +28.0%   <- shipped
n = 3   51.9%   +24.3%      n = 6   65.1%   +37.6%
n = 4   54.8%   +27.2%
```

Monotonic across Rick's own 2-to-6 range, and **n=4 and n=5 are 0.8 points
apart** — well inside the instrument. Open decision 1 is not settled by this and
would need n≈700 an arm to be.

> **AND TWO MEASUREMENTS OF THE SAME ARM CAME BACK 6.6 POINTS APART.** "As
> shipped" read 62.2% at one seed block and 55.6% at another, both n=378. That
> is v53 §3.1 for the fourth time: **a roster win rate is 27 pairings of
> CORRELATED fights, not N independent flips, and nothing below n≈700 ranks
> anything on this roster.**

---

# 5b. AND THE TYPE LADDER IS THE SECOND-WIDEST IN THE GAME

`shroudmaul_sweep --only 4 --n 26`, **702 fights**, by the foe's TYPE:

```
greatsword  67.0%   worst dawnbringer 35%   best axiom 77%
flail       45.2%   worst gravemourn  38%   best redflail 62%
twinblade   41.3%   worst twinshade   35%   best widowmaker 54%
warhammer   41.0%   worst grudgebearer 38%  best bulwarden 42%
scythe      36.5%   worst lastlight   23%   best thornwake 54%
bow         26.9%   worst ironhail    15%   best marrowdraw 38%

overall 45.2%    TYPE SPREAD 40.1pp    (Thornshear's is 43.6pp)
```

**This is open item 12's shape, and it is a second instance rather than a
coincidence.** The mechanism is the ultimate: `radius` 200 is the one number in
GRASP that is not free, and a bow spends the fight OUTSIDE it. A greatsword is
contact-rich and reach-poor — it comes to the hammer, gets held, and is hit
while it is held. Thornshear reads 18.6% against the five bows at an overall
47.0%; Shroudmaul reads **26.9% at an overall 45.2%**, and neither is visible to
`verify`'s per-relic band.

Whether that is the relic (rock-paper-scissors a viewer can learn, and
Grudgebearer is already 80% into Axiom) or a problem is Rick's, exactly as item
12 is. **It is the same question twice now**, which is an argument that the
per-relic band is the wrong instrument for a concentrated relic.

> **AND THIS RUN IS WHAT CAUGHT THE BLADE BEING A POINT LOW.** It reads **45.2%
> at n=702** where `umbral_sweep`'s confirmation read **50.0% at n=702** on the
> same build, the same field and the same side. That gap is what sent the blade
> back for the wide two-sided re-measurement in §5a, and 19.92 became 21.0.
> **n≈700 is a floor and not a guarantee.**

> **THE LADDER ABOVE IS AT BLADE 19.92** and has not been re-run at 21.0. The
> shape is a property of `radius` 200 against how far each type stands off, so
> a damage point should move the level and not the order — but that is an
> argument and not a measurement.

---

# 6. THE ART, AND THE FIRST SHEET REFUTED THREE THINGS THE FIRST BUILD CLAIMED

`grasp_sheet.py` — six panels, off a real match, `deadfall_sheet`'s pattern.
`05-reference/v56/grasp-states-*.png`.

**THE ULTIMATE DEALS NO DAMAGE, SO THERE IS NO NUMBER ON SCREEN, NO HEALTH BAR
MOVING AND NO HIT STOP SCALED TO A BLOW. If the hand does not read, nothing
happened.** That is what makes this the one set-piece in the game whose art is
not decoration on a mechanic but the only evidence of it.

## 6a. THE CRUSH HAD NO FRAMES AT ALL, AND ONLY A RENDER COULD SAY SO

`grasp_relic_probe [P]` calls `drawGrip` against a real 2D context in every
state and counts the frames each state was drawn in. The first build:

```
2692 frames    reaching 1225    holding 1201    THE CRUSH 0
```

The fifth grab **ends the window on the frame it lands** — that is "then
dissipates" and it is the balance clause — so `f.ultGrasp` is null from that
instant. Drawn off `ultGrasp` alone, the payoff of an eight-second window was a
hand VANISHING at the exact moment it closed, and the two seconds the quarry
spends held had nothing on screen.

**Every number was right.** The true stun landed, the beat was filed, the win
rate did not move by a thousandth, and Rick's §1 asks for *"a unique animation
for the true stun grab"* in as many words.

The fix is `f.graspCrush`, presentation only — **and it is ticked in
`tickPresentation`, not in `tickGrasp`.** v54's lesson one relic along:
**ANYTHING PRESENTATION THAT IS SPAWNED BY AN IMPACT BELONGS IN
`tickPresentation`**, because the crush sets `hitStop` and `step()` returns
through `decayImpactOnly` for as long as that runs. Deadfall's blast froze on
the floor 96.2% of the time for exactly this reason. `graspFade` moved with it.
Now: **reaching 1718, holding 1674, crush 1269, fading 218.**

## 6a-2. AND THE GESTURE ITSELF WAS WRONG — RICK, WATCHING THE FIXED CRUSH

> *"the hand currently reaches out and latches on and stretches with the balls
> movement. it should reach out. squeeze. cause massive hitstun. let go."*

**THE FIRST BUILD DREW THE STUN INSTEAD OF THE GRIP.** It put the hand on the
quarry for `grabStun` — **0.5s of a 0.6s cadence, so the limb was attached 83%
of the time** — and the hand tracked the ball for all of it. The sheet had
already found the consequence and reported it as a curiosity: the "drawn back"
panel could not be photographed at all, because the predicate asks for an open
hand two thirds of the way through a cadence and those cannot both be true.

**A LATCH SAYS THE BALL IS BEING HELD, AND THE BALL IS NOT.** `f.pin` is
refused on measurement — −3.3 points at identical held seconds — and the whole
design note says the hand grips the **weapon**. The picture was contradicting
the one thing the mechanic is most careful about, and it did it for 83% of
every window.

The gesture is now a PUMP on the cadence, with the hitstun outliving it:

```
SQUEEZE   `ult.squeeze` 0.18s — the fist shut, at the quarry, tether taut
LET GO    it opens and withdraws over squeeze x 0.9
REACH     it extends again as the cadence timer runs down
```

The stun the grab writes is unchanged at 0.5s — **four times the squeeze** —
so the quarry stays locked with its weapon stopped while the hand is already
leaving. The crush squeezes twice as long and lets go the same way, and
`graspCrush` no longer lasts `trueStun`: the hand is gone about 0.7s after the
fifth grab while the quarry is held for 2.0.

> **AND IT IS PRESENTATION-ONLY, PROVEN RATHER THAN ASSERTED.** `engine_ab`
> against the previous build **210/210 identical field for field, with
> Shroudmaul itself in the roster** — the one comparison that could have caught
> a stray write. `held` a cast is 3.71s before and after.

> **THE PROBE'S STATE COUNTER IS THE MEASUREMENT OF THE CHANGE.** Before:
> reaching 1596, *holding* 1475 — the hand shut for 48% of its own frames.
> After: **reaching 2437, squeezing 634** — 17%. That ratio is the difference
> between a hand that grabs and a hand that has grabbed.

## 6a-3. AND THEN THE RHYTHM, WHICH IS THE FIRST TIME THIS DESIGN'S FREE TRADE HAS BEEN SPENT

Rick, on the corrected gesture: *"its still pretty confusing what the ult is
actually doing by just watching it. can we add a cooldown for how often it can
grab but make the stun longer?"*

**Measured, the shipped rhythm was worse than it looked.** `grasp_rhythm_lab.py`:

```
cadence 0.6, grabStun 0.5, n 5, window 8.0

the whole ultimate resolved in 4.79s — 61% of its own window
five grabs a mean 1.13s apart
the quarry locked 51% of that, in half-second pieces
```

Five near-identical half-second events inside five seconds, and a dead back
third. Nothing was on screen long enough to be read as a cause.

**AND THIS IS THE ONE TRADE THE DESIGN GIVES AWAY FOR FREE.** `grab_lab` fitted
`lift = +3.1 + 2.62 x held` with residuals SMALLER than the measurement error,
so cadence, grab hold, true-stun length, window and grab count are five ways of
writing one number: **any arrangement delivering the same held seconds is worth
the same.** No other ultimate in this game has that property, and until now
nothing had spent it.

Two rounds, 162 fights an arm, `held` a fight is the balance and the four
columns to its right are the legibility:

```
arm                                held  grabs   gap   fill   lock  crush
as shipped                         9.53   4.84  1.13s   61%    51%    91%
A  cad 1.2, stun 0.8              11.49   4.46  1.79s   89%    54%    69%
B  cad 1.5, stun 1.0              12.61   4.18  2.03s   99%    59%    53%
D  cad 1.8, stun 1.2, n 4         12.97   3.59  2.37s   92%    60%    74%
F  cad 2.2, stun 1.5, n 3, true 3.5  15.23  2.78  2.87s   76%   63%    85%
```

> **ROUND 1 IS ENTIRELY ABOVE THE LINE, AND THE REASON IS A REAL PROPERTY OF
> THE MECHANIC: A LONGER COOLDOWN DOES NOT COST GRABS.** The cadence timer sits
> EXPIRED between grabs and closes the instant the quarry is in reach — it is a
> hand that is WAITING, not a hand on a metronome (`grab_lab`'s own arm, and
> the reason `tickGrasp` does not reset the timer on a miss). So slowing it
> SPACES the grabs without losing many, and the longer stun then multiplies.
> **The whole overshoot has to come out of `n`.**

Round 2, with `n` paying for it:

```
arm                                held  grabs   gap   fill   lock  crush
as shipped                         9.53   4.84  1.13s   61%    51%    91%
H  cad 1.8, stun 0.9, n 3          9.05   2.85  2.41s   65%    47%    90%
I  cad 2.0, stun 1.0, n 3, true 2.2  10.06  2.83  2.62s  70%   49%    87%   <- built
J  cad 1.5, stun 0.8, n 4         10.10   3.69  2.09s   82%    49%    80%
K  cad 2.2, stun 1.2, n 2, true 2.5   8.97  1.93  2.88s  42%   49%    93%
L  cad 2.5, stun 1.4, n 2, true 2.8  10.09  1.92  3.28s  47%   52%    92%
N  cad 1.6, stun 0.8, n 3, true 2.4   9.51  2.84  2.19s  60%   46%    89%
```

**Arm I ships.** Three beats about two and a half seconds apart, each locking
the quarry for a full second, and the third is the crush:

```
cadence   0.6 -> 2.0      grabs a cast   4.84 -> 2.83
grabStun  0.5 -> 1.0      gap            1.13s -> 2.62s
n         5   -> 3        window used    61% -> 70%
trueStun  2.0 -> 2.2      squeeze        0.18s -> 0.30s
```

`lock` is deliberately not maximised. **It is a ceiling, not a maximum**: at
100% the quarry never moves between grabs and the ultimate reads as one long
freeze, which is the Crucible's verb and the one thing this relic may not be.
K and L reach the longest gaps and fill under half the window — the ultimate
finishes and the window sits empty, which is the shipped build's fault pointed
the other way.

> **AND THE BLADE DOES NOT MOVE, WHICH IS THE HELD-SECONDS LAW CONFIRMED ON THE
> BUILT RELIC.** Two independent seed blocks, both sides, n=1080 each, at the
> shipped `dmg` 21.0: **49.1% and 50.9%.** A completely different arrangement
> at the same held seconds is worth the same, exactly as `grab_lab` predicted —
> and this is the first time the claim has been tested by changing the shape
> rather than by fitting a line through it.

> **THE BUILDER PRINTED THE NEW NUMBERS AND SHIPPED THE OLD ONES.** `dur`,
> `radius`, `cadence`, `grabStun`, `n`, `trueStun` and the tip are written by
> the STAGE-2 insert and baked into `sc-shroudmaul.html`; stage 3 rewrites only
> the line carrying `charge` and `squeeze`. So `--stage 3` logged
> `cadence 2 grabStun 1 n 3` and produced a relic still reading
> `cadence:0.6, grabStun:0.5, n:5`, and every gate downstream measured the old
> rhythm while the log claimed the new one. **Caught only because the probe
> printed `n=5` two minutes later.** That is CLAUDE.md §4.9's twelve lost values
> in a different costume. The split is right — stage 2 owns the relic's data,
> stage 3 owns its mechanism — so the fix is an assertion: `ult_matches()`
> refuses to write unless the shipped `ult` block carries every number the run
> just printed, and it names the rebuild.

## 6b. THE HAND WAS 40px AND READ AS A SCRIBBLE

`GRIP_SCALE` shipped at 1.35, which put the hand at ~40px on a 540 frame.
Photographed, it was a white starburst on the ball — which is **Rick's own
complaint about Revenant's first cut arriving from the other direction**
(*"the hands dont read as hands. not detailed enough"*). At that scale a
phalanx is 2px against a 1.4px dark gap, so the two passes that MAKE a skeleton
legible merge into one blob.

**2.8**, which is ~110px — the number v53 measured as too large for one of
THREE hands in flight, and about right for the only object of its kind on the
screen. **Still a first cut**: it is a SIZE question, and v53 settled that a
size question cannot be answered off a sheet.

## 6c. THE FOURTH SEPARATION WAS CLAIMED IN THE COMMENT AND NOT BUILT

`drawGrip`'s header claimed the crush is told from a hold four ways. Three were
built — clench, scale and tether tension — and photographed side by side the
two were the same picture at a slightly different size. The fourth is now
colour: **the bone goes white-hot and nothing else changes.** §4.1c is why that
is safe here where it was not for Daybreak or the Harrowing — alpha is
invisible to the bloom and what blows the chain out is AREA, and a skeleton is
separated strokes.

## 6d. AND THE COUNT WAS INVISIBLE BECAUSE IT WAS THE SAME COLOUR AS THE ARM

`u.n` marks on the tether, `G.grabs` of them lit, so a viewer can see the crush
coming (§7b). The first cut drew lit DOTS in `pal.glow` — the colour the bone
beside them is drawn in — laid on the same curve. **A bright dot on a bright
line reads as a thicker line.** They are RUNGS across the limb now, hot white
against its purple, and an unlit one is a dark bar rather than an absence.

## 6e. AND THE SHEET HAD ALREADY FOUND THE LATCH WITHOUT KNOWING IT

The sheet's first predicate for a drawn-back hand **never matched**, and the
reason turned out to be §6a-2 rather than a quirk of the predicate: `grabStun`
0.5 against `cadence` 0.6 meant the hand was CLOSED 83% of the time, so "an
open hand two thirds of the way through a cadence" could not exist. It was
written up as a curiosity about the numbers. Rick watched the clip and named it
as the defect it was. **A predicate that cannot be satisfied is evidence about
the thing, not about the predicate** — and that is worth more than the panel
would have been.

---

# 7. THE SOUND

Three voices, all rendered and measured in an `OfflineAudioContext` through
`buildChain` — the signal path that actually ships. `SFX.play` returns on its
first line headless and swallows its exceptions, and v42 shipped a silent
ultimate through every green check in this repo.

```
shroudmaul         the hand growing   peak 0.389  audible 1.60s  <120Hz 0.755
shroudmaul-grab    a grab closing     peak 0.201  audible 1.10s  <120Hz 0.481
shroudmaul-crush   the crush          peak 0.561  audible 1.40s  <120Hz 0.617
```

**THE CRUSH HAS TO NOT BE A GRAB**, because there are four of the second kind a
cast and the one thing a viewer must learn is which of the two just happened —
Vesper's pass-against-tip pair is the precedent and it is the same problem one
relic along. Measured: **2.19x the peak and +0.15 of the energy below 120 Hz.**

> **AND THE FIRST SEPARATION METRIC WAS THE WRONG ONE.** It asked for 1.6x on
> `audible` and got 1.27x from two sounds that are plainly different, because
> `audible` measures the SIGNAL CHAIN'S tail and both voices fill it. What
> separates a clamp from a collapse is LEVEL and WEIGHT.

No burst exceeds 0.6s (CLAUDE.md §4.5).

---

# 8. A CHAIN-WIDE FINDING THAT IS NOT THIS BUILD'S: **THE KILLING BLOW USUALLY DOES NOT GET A CUT**

Found by reading `cinema_clip`'s own log on the first rendered clip:
`no killing blow on this seed (timeout finish); using the last cut` — on a
fight that ended `hp=[20, 0]`, with a `fatal: true` beat correctly filed at
55.23s by an ordinary hammer blow through `resolveHit`.

**The beat is filed. It just never becomes a CUT.** Measured over ~78 kills a
relic on the current tip:

```
shroudmaul     73/78   93.6%  of kills rendered with no killing-blow cut
nightfell      65/76   85.5%
gravemourn     62/78   79.5%
grudgebearer   55/71   77.5%   <- untouched by this build, 27 relics old
```

The mechanism: `CINE.floor` is **1.9** and the median killing blow scores
**1.24**. A kill is scored like any other beat and mostly does not clear the
bar.

**THIS IS NOT GRASP'S AND IT IS NOT NEW.** Grudgebearer has been in the game
since the roster's first half and reads 77.5% on the same instrument.
Shroudmaul is worst of the four, which is consistent with a relic whose fights
run long and whose most dramatic moments are not the finish — but the
instrument reads everything as broken, so the ordering is not worth much.

What IS worth something is the absolute level: **CLAUDE.md open item 3 records
Dawnbringer at 22.1% blind as the current worst**, and every relic measured
here is three to four times that. Either the director drifted under the
long-fight pace (baseHP 400, mean fight 49.5s, so a kill competes with far more
material) or the two measurements are not the same quantity. **Nobody has
looked, and the one-line answer — a kill is always a cut — is chain-wide and
therefore Rick's.**

---

# 9. THE GATES

```
engine_ab     stage 1   2808/2808 IDENTICAL, all 27 relics
              stage 2   2808/2808 IDENTICAL, the 27
              stage 3   2808/2808 IDENTICAL, the 27, at the shipped blade
grasp_relic_probe        20/21, 162 fights — the one red is §4's registered
                         prediction, measured and diagnosed
umbral_sweep             4617 fights, bisected to 19.92 — REFUTED by §5a
wide two-sided direct    7560 fights over two seed blocks, blade 23.5 -> 21.0
shroudmaul_sweep         floor 27.5% against a registered 27.1%
verify --n 40            12/13 with 28 relics. Roster spread 18.5pp (Axiom
                         39.3 .. Farwarden 57.8), NARROWER than the 19.0pp the
                         umbral package started from. Shroudmaul 50.2%.
                         The one FAIL is the KNOWN thirteenth check —
                         Lightkeeper/Farwarden at 75.7s, and NO Shroudmaul
                         pairing is over the band. Do not credit this build
                         with it either way (CLAUDE.md §0)
render path              drawGrip CALLED against a real 2D context in all four
                         states, 4879 frames, no throw
sound                    three voices rendered and measured
app/main.js              GAME moved to 02-chain/sc-grasp.html. CLAUDE.md §0
                         names this as the carry step nothing checks
```

**`chain_audit` could not audit this build and says so.** It reads inserts from
module-level string constants in the builder; this one keeps its edits in `S2`
and `S3` lists, so the tool found only `FX_NEW`. Nothing downstream of stage 3
exists to clobber an insert, and the stage-2 relic block was verified present in
the tip by hand. **It is a tool limitation and worth fixing before the next
relic**, because a green `chain_audit` that audited nothing is exactly the
failure mode it was written for.

---

# 10. WHAT THIS BUILD DOES NOT KNOW

- **`shroudmaul_sweep --only 2,3` has not been run.** The held-seconds law
  re-fit on the built relic, and the reach curve. §4 checks the half of the law
  that this build could have broken (held A CAST) and nothing checks the other
  half. `--only 4`, the type ladder, HAS been run — see §5b, and it is a
  finding.
- **Nobody has watched the relic.** The art and the sound are first cuts.
  `07-shorts/v56/grasp-first-cut.mp4` and `05-reference/v56/grasp-states-*.png`
  exist for that; three of the six things the sheet already found were invisible
  to every probe in the repo, and the sheet cannot answer a scale question.
- **`n` is not settled.** 4 and 5 are 0.8 points apart at n=378.
- **Sentinel's beam and this hand have never been measured against the bloom
  together.** Open item 17 is Vesper's; this adds a second large lit object to
  the same school-adjacent problem, and `ult_fx_capture` has no `shroudmaul`
  entry either.
- **`crowdMul` is unset**, as it is for Deadfall, Revenant and the Winnowing.
  Four times the same question now (open items 15 and 27).

---

# Open decisions

1. **`n` — 4 OR 5, AND IT IS STILL OPEN.** +27.2% against +28.0% at n=378 a
   point, which is inside the instrument twice over. Settling it honestly costs
   ~1400 fights an arm. **Built at 5**, which is the brief's instruction.

2. **DOES THE CHARGE REBUILD DURING THE WINDOW?** §4.1, and it is the fork this
   build had to pick a side of. As built it does, like 25 of 28 relics — which
   is why the relic casts 2.58 times a fight against the lab's 1.84 and why the
   blade paid 3.6 points for it. Gating the rebuild (the Crucible's, Ironbloom's
   and the bow window's behaviour) would reproduce `grab_lab` exactly and put
   the blade back near 23.5. **It is not a defect either way**: more casts is
   more set-pieces per fight, which v55b §5 argues is a shorts problem worth
   caring about. Named because the numbers in `grab-v56.md` are all measured on
   the other branch.

3. **THE RHYTHM, AND THERE ARE SIX MORE ARMS ON THE SHELF.** §6a-3 ships arm
   I. Every arm in round 2 is balance-neutral, so swapping is a one-line change
   to `ULT` and a rebuild of both stages — **N** is the same shape a little
   tighter (gap 2.19s, held 9.51), **J** keeps four grabs and fills 82% of the
   window, **L** is two grabs 3.3s apart and the clearest of all of them at the
   cost of half the window standing empty. Nothing measures which reads best.

4. **THE GESTURE, ROUND 2.** §6a-2 rebuilt it on Rick's note — reach, squeeze,
   let go — and it has been photographed but not watched in motion. The one
   number in it that is a guess is `ult.squeeze` 0.18s against a 0.6s cadence:
   long enough to read as a squeeze, short enough that the hand is visibly
   leaving before the next reach. Free on the held-seconds line, so it is a
   picture decision entirely.

5. **THE HAND'S SIZE.** `GRIP_SCALE` 2.8 — ~110px on a 540 frame, the largest
   object this game draws. Refuted at 1.35 by the first sheet; not confirmed at
   2.8 by anything. v53 spent three rounds on this question for Revenant and a
   sheet answered none of them.

6. **THE ONE-TO-GO TELL.** Rungs across the tether, `u.n` of them, lit as
   the grabs land. §7b's question — can a viewer see the crush coming before it
   lands — has no measured cost and a real effect on whether the escalation
   reads as earned.

7. **THE THREE VOICES.** First cuts. Measured to be audible and to separate;
   not auditioned. Rule 2 says the ult sound is Rick's, and v43 landed it in one
   round trip by offering a spread — `sentinel_hum_lab.py` is the pattern and it
   has not been run for this relic.

8. **THE TYPE LADDER.** §5b. 67.0% into greatswords and 26.9% into bows, a
   40.1pp spread that no per-relic band in this repo can see. Open item 12
   asked this once about Thornshear; this is the second time and the same
   question. Either it is the relic or the band is the wrong instrument.

9. **THE KILLING BLOW'S CUT.** §8. Chain-wide, three to four times worse than
   the figure CLAUDE.md records, and one line to change. Not this relic's.

10. **THE BLURB HAS NOT BEEN PUT TO RICK.** *"Bone under the iron, and it did not
   start there. What it takes hold of does not get to swing back."* Rule 2 names
   the fighter name and the scrunch wording; the blurb has never been on that
   list and probably should be.

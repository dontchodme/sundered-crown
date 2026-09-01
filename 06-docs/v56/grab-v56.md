# v56 — THE SKELETAL HAND, PRICED. The whole ultimate collapses to ONE number — total seconds the foe is held — at r2 0.79 with residuals inside the noise floor. Rick's §1 as written lands on +20.4% against a field median of +21.8%, and "then dissipates" turns out to be the balance knob rather than a cost. It is not a curse ultimate, and it collides with a relic that shipped this morning.

**2026-08-31, Cowork.** `tools/grab_lab.py` against
`02-chain/sc-nightfell.html`, Grudgebearer standing in as an umbral warhammer
with its own Crucible suppressed. **26 foes x 27 seeds = 702 fights an arm**,
which is v53 §3.1's floor and not the n~200 this lab started at. Runtime only.

Rick's §1, verbatim:

> *for a duration the artifact grows an etherial skeletal hand that reaches out
> and grabs nearby enemies. the grab does no damage and doesn't apply curse but
> it does apply massive hit stun. if it grabs several times in one trigger (2-6
> depending on balance) it true stuns for extra duration and then dissipates.*

**Nothing in this game has a zero-damage ultimate, and nothing has a payoff
that must be EARNED inside its own window.** Both are new and both work.

---

# 0. FIRST, THE ENGINE ALREADY HAS THE VOCABULARY — AND "MASSIVE HIT STUN" IS NOT IN IT

```
takeHitstun()   what a BLOW does. stunBase 0.10 + 0.0035/dmg, CAPPED AT 0.26s,
                and each application shortens the next (stunDR 0.55). It cannot
                be massive; the ceiling is a quarter of a second
f.stun          the weapon is locked — tickHits skips, the head stops turning,
                the swing does not advance. The BALL KEEPS MOVING; moveMul
                floors at 0.45 and speedMin is 250. This is what u.freeze
                writes, and it is what the two shipped tips call "roots"
f.pin           the ball is HELD — `move()` returns on it. Written by exactly
                ONE relic in the game, Paradox's Stasis Field, and by nothing
                else
```

And the true-stun distinction is **Rick's own**, already implemented, quoted in
the engine: *"Hitstun shouldnt stop the windup. but true stuns from ults/
abilities should."* It is not a flag on a timer — every source writes the same
`f.stun` — so it is drawn at the **application sites**, and there are exactly
three: hex, `u.freeze`, and the Harrowing's burst. Five relics of twenty-seven.

**So the §1 maps onto the architecture already there, with no new field:** the
ordinary grabs write `f.stun` from a site that is NOT in the true-stun set
(they delay a wind-up, they do not cancel it), and the final grab writes it
from a site that IS. That is the whole of "massive hit stun, then a true stun,"
and it costs one entry in a list a viewer can already learn.

---

# 1. THE ULTIMATE IS ONE NUMBER, AND EVERY KNOB IS A ROUTE TO IT

Fourteen arms, 702 fights each, `held` = total seconds of hold delivered per
fight:

```
arm                       win   casts  grabs  /cast  true   held  blows   foe   pool     lift
FLOOR — no ultimate     27.1%    0.00    0.0   0.00  0.00    0.0    8.2  17.4   59.6    +0.0%
§1 as written  n=4      47.4%    1.87    7.3   3.97  1.75    6.3    9.4  16.0   62.8   +20.4%
n=2  dissipates         41.6%    2.01    4.0   2.00  1.97    4.9    9.0  16.4   62.3   +14.5%
n=3  dissipates         45.4%    1.93    5.7   2.99  1.85    5.6    9.3  16.5   62.5   +18.4%
n=5  dissipates         52.0%    1.84    8.7   4.92  1.62    6.8    9.4  15.8   63.4   +24.9%
n=6  dissipates         53.3%    1.77    9.8   5.81  1.42    7.0    9.5  15.7   63.3   +26.2%
grabs only, never true  50.0%    1.66   12.4   7.86  0.00    6.2    9.4  15.9   63.4   +22.9%
n=3  no dissipate       59.1%    1.66   12.5   1.00  3.61   11.7    9.7  15.3   63.7   +32.1%
n=4  no dissipate       58.3%    1.69   12.8   1.46  2.56   10.2    9.6  15.5   64.0   +31.2%
n=4  + PIN the ball     44.2%    1.87    7.3   3.98  1.76    6.3    9.3  16.4   61.9   +17.1%
n=4  radius 140         41.9%    1.79    6.6   3.83  1.46    5.5    9.2  16.7   62.7   +14.8%
n=4  radius 300         43.2%    1.91    7.5   3.99  1.83    6.5    9.0  16.3   62.0   +16.1%
n=4  grab hold 0.8s     48.4%    1.84    7.1   3.97  1.72    7.8    9.3  15.8   62.9   +21.4%
n=4  true stun 4.0s     55.8%    1.89    7.4   3.97  1.77    9.9    9.6  15.5   63.8   +28.8%
```

Regressed on `held` alone:

```
lift = +3.1 + 2.62 x held seconds      r = +0.889   r2 = 0.79
residual sd 2.7pp against a per-arm SE of 5.3pp
```

**The residuals are smaller than the measurement error.** Window length, grab
cadence, how long one grab holds, how long the true stun holds, how many grabs
it takes, and whether the window survives the payoff are not six knobs — they
are six ways of writing one:

> **2.6 points of win rate per second the foe spends held.**

This is the most useful thing in the document, because it means **the SHAPE of
the mechanic is free.** Every arrangement that delivers the same held seconds
is worth the same, so the arrangement can be chosen entirely for what it looks
like, and the balance settled afterwards on a single scalar. No other ultimate
in this game has had that property.

The one family that departs from the line is REACH, and it departs in the
direction that says something:

```
radius 140    held 5.5s   predicted +17.5   actual +14.8    -2.7
radius 200    held 6.3s   predicted +19.5   actual +20.4    +0.8
radius 300    held 6.5s   predicted +20.1   actual +16.1    -4.0
```

Same seconds, less value. **A hold is only worth what the hammer can reach.**
At 300 the hand catches the foe out at the far wall and holds it somewhere the
wielder then has to walk to; the blows column falls from 9.4 to 9.0 while the
grabs column rises. The optimum is about **200 — roughly 2.6x the warhammer's
own reach of 76, or three ball diameters.** Far enough to be a reach; near
enough that what is caught is caught in front of the hammer.

---

# 2. THE §1 AS WRITTEN IS ALREADY THE RIGHT SIZE

```
field of 27 ultimates    mean +21.0%   median +21.8%
§1 as written, n=4                     +20.4%
```

That is not a near miss, it is the median. The §1 arrived correctly sized with
placeholder numbers, which has not happened before in this project.

---

# 3. "THEN DISSIPATES" IS THE BALANCE KNOB, AND IT IS ALREADY IN HIS OWN SENTENCE

```
n=3   window ENDS on the true stun     +18.4%
n=3   window RUNS ON, counter resets   +32.1%      the clause is worth 13.7 points
n=4   ends                             +20.4%
n=4   runs on                          +31.2%                            10.8 points
```

Without it the ultimate is +31 to +32, which is sixth of twenty-eight —
Bloodmill, Daybreak, Grasp, Converse, Triplicate and the Harrowing territory —
and the blade would have to be bisected hard to pay for it. With it, +20.4.

**The reward truncating the window is what keeps the relic honest**, and it is
a rule a viewer can see happen rather than a number in a tooltip: the hand
closes, it holds, it is gone. Keep it.

---

# 4. THE GRAB COUNT IS THE TUNING KNOB, AND RICK'S OWN 2-TO-6 IS EXACTLY THE USEFUL RANGE

```
n = 2   +14.5%        n = 5   +24.9%
n = 3   +18.4%        n = 6   +26.2%
n = 4   +20.4%        never   +22.9%   (grabs only, no true stun at all)
```

Monotonic, twelve points across his own stated range, and no other knob has to
move to travel it. A low count is a hand that closes early and leaves; a high
one is a hand that keeps working and rarely finishes.

**The true stun is not worth anything BEYOND its seconds.** "Grabs only" is
+22.9% at 6.2s held and n=6 is +26.2% at 7.0s — both on the line. The
escalation earns its place as a picture and as a rhythm, not as a payload, and
that is worth knowing before somebody tries to buy value by lengthening it.

---

# 5. PIN IS REFUTED, WHICH SETTLES THE ONE FORK THAT WOULD HAVE COST SOMETHING

```
n=4, stun only     held 6.3s    +20.4%
n=4, stun + pin    held 6.3s    +17.1%     -3.3 at identical hold
```

Holding the BALL as well as the weapon is worth **less than nothing**, and it
is consistent with the reach result: a pinned ball cannot be knocked toward the
wielder, and this relic needs the foe to arrive. It is also the Stasis Field's
only exclusive verb. **Do not write `f.pin`.** The grab locks the weapon and
lets the ball drift, which is both the cheaper build and the better one.

There is a picture problem inside that and it should be said out loud: a
skeletal hand closing around a ball that then keeps drifting is not obviously
legible. The answer is that the hand grips the **weapon**, not the ball — which
is what `f.stun` actually models, and what the frame will show.

---

# 6. IT IS NOT A CURSE ULTIMATE. IT IS NOT ANY-SCHOOL'S ULTIMATE.

The attractive story was that a hold buys uninterrupted swings, and swings are
what fill the pool — so an ultimate that never touches the pool would still be
umbral's, at one remove. **Measured, that is not true.**

```
the hold's effect on the pool it was supposed to feed
blows landed    8.2 -> 9.4      +1.2 blows a fight
pool held       59.6 -> 62.8    +5.4%
```

And the same hold bolted to six different schools, each A/B'd against its own
floor (n=208, so read the spread and not the order):

```
dwarven x sunder      +19.2%        runic x hex          +17.8%
bloodsworn x hemo     +15.9%        sanctified x smite   +15.4%
umbral x curse        +13.5%        verdant x entangle   +12.5%
```

A 6.7-point spread against a 4.9pp standard error. **No school-specific
advantage is detectable, and umbral is not at the top of the list.** The
ultimate is school-agnostic, and the relic's umbral identity would live
entirely in its blade.

## Which is a design decision, not a defect, and it cuts both ways

```
TWINSHADE    FILLS the pool
GRAVEMOURN   MOVES  an entry out and back
NIGHTFELL    READS  the sum onto the floor
THIS ONE     ————   nothing
```

v52 §3e made a virtue of *"three relics, three relationships to one mechanic."*
A fourth with no relationship weakens that claim.

**Against which:** v52 §5 registered the school's real risk as *"umbral becomes
a school where nothing works until Curse is stacked. A relic that loses its
first exchange loses its ultimate as well."* This ultimate does not care what
the pool holds. It is the only umbral ultimate that is worth full value in the
first ten seconds of a fight, and it is the school's own hedge against the
thing v52 was worried about.

**A cheap way to have both, and it is UNMEASURED.** Keep "no damage, no curse
applied" exactly as written, and make the pool the CONDITION rather than the
payload — *the number of grabs the hand needs is 6 minus the foe's curse
stacks*, so a cursed quarry is closed on faster. That is a fifth relationship —
the pool as a fuel gauge for control rather than a source of damage — and it
costs no damage and no application. Predicted to land near n=4 in practice
(2.45 stacks at the first cast, v55 §5) and therefore near +20%; **predicted,
not measured, and one arm would settle it.**

---

# 7. THREE COLLISIONS, AND ONE OF THEM SHIPPED THIS MORNING

## 7a. THE NAME. Gravemourn's ultimate is called GRASP.

`w.ult.name` on the built relic reads **"Grasp"**, tip *"Lengthens the chain;
every hit throws a cursed hand"* — Rick's own pick at build time, over the
brief's REVENANT. This §1's entire action is grasping.

Renaming the new one does not fix it: the collision is on the **verb**, and it
is in the same school. Two ways out, and the cheap one is better:

- **Give Gravemourn back REVENANT** — Rick's own name from the v51 spread, and
  a better fit for it than for anything else: *that which comes back* is what a
  hand that takes a memory, deals it and re-parks it actually does. One string,
  one tip, `tip_audit`, done — and it frees the whole grip/clutch/grasp
  register for the relic whose ultimate IS a grip.
- Or make this one not a grab, which is a rewrite of the §1 and unwarranted.

## 7b. THE ART. Grasp is already made of ethereal purple hands, in this school.

And they are not a placeholder: Rick rejected the first cut — *"the hands dont
read as hands. not detailed enough"* — and the shipped version was measured at
37px on a 540 frame and 75px on a phone, deliberately legible **as a hand**.

Two umbral relics whose signature object is an ethereal hand will read as the
same ultimate on a phone, in a purple palette, unless the difference is
structural. It can be, and the differences are all available at once:

```
GRASP        MANY hands, SMALL, AIRBORNE, thrown off blows, converging on the
             quarry at speed and closing into fists. Smoke and afterimage
THIS ONE     ONE hand, LARGE, TETHERED — it grows FROM the artifact and stays
             attached to it, reaches, opens, closes, holds. Bone
```

One versus many, tethered versus airborne, bone versus smoke, and reaching
versus striking. **The tether is the strongest of the four** and it is free:
nothing else in the game connects the wielder to the quarry with a limb, and it
is on screen for the whole window rather than for 1.8s of flight. This is the
v52 §4 problem — Converse and Deadfall both mark the floor — and it wants the
same treatment: an art constraint written down before either is drawn again.

## 7c. THE MECHANIC. This makes six relics that stop the foe, and two of them are warhammers.

```
Crucible       grudgebearer   pull + freeze + consume Sunder + damage   WARHAMMER
Bramblesnare   thornwake      1.6s root + 10 damage
Rootfast       heartwood      1.3s root + 9 damage
Stasis Field   paradox        a zone, and the only `pin` in the game
Harrowing      lastlight      stunBase + stunPer on the burst
hex            2 relics       0.2s weapon stun, a flicker
```

The engine says it in its own voice, three lines from where a second hold would
have gone: *"The Crucible owns freeze; a second hold would make two of the
sixteen the same relic."*

**What separates this one, and it is real:** every hold in that list is a
single event attached to damage. This is a WINDOW of repeated, zero-damage
grabs whose payoff has to be earned. The Crucible pulls the foe in and cashes
it; this reaches out and simply will not let go. Different verb, different
rhythm, and — measured — a completely different value curve, because the
Crucible's worth is in what it consumes and this one's is in a single scalar of
time.

But it is the **second warhammer in a roster of twenty-eight whose ultimate
stops the other fighter moving**, and that has to be a decision rather than an
accident.

---

# 8. THE TRAPS FOR THE BUILD

**a. A ZERO-DAMAGE ULTIMATE CAN NEVER FILE A FATAL BEAT — AND MAY FILE NONE.**
v53 §4: half of Gravemourn's kills rendered a clip with no killing blow,
because the hand filed `kind:"ult"` and `cinema_clip` finds the finish with
`plan.find(c => c.fatal)`. This ultimate is worse placed: it does no damage at
all, so if the grabs file no beat the director cannot see the ultimate happen
**even though it is the most visually distinctive thing in the fight.** Rule 3,
ninth relic running: the cast files a beat, the true stun files a beat, and the
probe asserts both.

**b. FOE ONLY, AND TWINSHADE IS THE TEST.** "grabs nearby enemies" is plural in
a 1v1 game — except against Triplicate, where there are three bodies. A hand
that grabs a shade is a hand wasted on a copy that is about to expire, and
`tickShadeHits` is where v51 §4.3's bug lived. Decide it, then assert it.

**c. `stunDR` MUST NOT BE IN THIS PATH.** The grabs write `f.stun` directly;
they are not `takeHitstun`. Route them through `takeHitstun` and diminishing
returns will eat the second grab onward and the mechanic will quietly become
one grab and a rumour. This is the single easiest way to build it wrong, and
the symptom is a `held` column that does not move when the knobs do.

**d. THE HAND IS PER-MATCH STATE AND IT IS ALSO ONE OBJECT.** Not `shots` —
`spawnShot` shifts a live entry out at `maxLive` 64. And unlike Grasp's hands
there is only ever one, tethered to a fighter, so it hangs off `f.` like
`f.ultBeam` and `f.ultDeadfall`, NOT off `m.ultFx`. v54 §2a: `ultFx` is one
slot and the opponent casting anything erases it. A window ultimate whose art
is its whole point cannot live there.

**e. THE WINDOW MUST SURVIVE HIT-STOP.** The lab skips its own logic while
`m.hitStop > 0` because the sim is frozen; the build has to make the same
choice deliberately, or grabs will fire during frames where nothing else in the
game is moving.

---

# 9. WHAT THIS LAB CANNOT TELL YOU

- **It never tested a true stun that actually cancels a wind-up.** The lab
  writes `f.stun` from an unregistered site, so every arm above measures hold
  duration only. The wind-up-cancel half — which is the difference between
  "true stun" and "a long stun" — affects the Crucible, Bloodmill and Reprisal
  and is worth an unknown amount.
- Section 6's six-school table is n=208. The spread is inside noise; that is
  evidence of no effect, not proof of one.
- The `held` model is fitted on arms that all share one relic, one blade and
  one charge. It is a within-relic law, not a general one.
- Nothing here says whether a grab READS. A hand that reaches, closes and holds
  for half a second is 60 frames; whether a viewer can tell a grab from a
  true-stun grab is the same filmstrip question v54 §2c nearly shipped wrong.
- Grudgebearer is standing in. Its mass, `artW` and windup are the warhammer's,
  but its blade is 23.5 and the real relic's will be bisected.

---

# Open decisions

1. **GRAVEMOURN'S ULTIMATE NAME.** Recommend giving it back **REVENANT**, its
   name in the v51 brief and Rick's own from that spread, so that "grasp" is
   free for the relic that grasps. One string and one tip. If Grasp stays, this
   §1 needs a different verb and the art problem in §7b gets harder, not easier.

2. **THE GRAB COUNT.** 2 to 6, worth +14.5% to +26.2%, monotonic. **4 or 5** is
   the field median. This is the whole balance decision and nothing else has to
   move with it.

3. **DOES THE POOL GATE IT?** §6's unmeasured option — grabs needed = 6 minus
   the foe's curse stacks — buys the relic a relationship to its own school's
   mechanic without adding damage or applying curse. One arm settles it.

4. **REACH.** 200, from a measured optimum, against a warhammer reach of 76.
   Worth naming because it is the one number that is NOT free: 140 and 300 both
   cost 4 to 6 points at the same held seconds.

5. **DOES IT GRAB SHADES?** §8b. A rule, not a tuning knob.

6. **THE NAME AND THE TIP.** Not started. The tip has 72 characters and the
   thing to get into it is that the hold is earned and then spent — the mechanic
   is legible in a way most of this roster's are not.

7. **CHARGE.** v55b: charge is worth 3-5 points a second on a good ultimate and
   was never derived for anybody. This relic's is 16 by default and its cell's
   donor sits at 18. Unlike every other relic in the chain a longer charge here
   does NOT make the ultimate stronger — the hold does not scale with the pool —
   so the usual v55 argument does not apply and 15-16 is probably right.

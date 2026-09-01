# v60 — THE BARBED WIRE RING, PRICED. Rick's §1 collapses to one scalar, and the scalar is not the one this session predicted: it is BLOWS THE OPPONENT DOES NOT LAND, at r² 0.89, validated on four arms the line never saw. The extra swings bought by "massive rotational speed" are worth r² 0.01 — nothing. And both halves of the bleed sentence are inert, for the same reason Bloodmirror hit yesterday.

**2026-09-01, Cowork.** `wire_lab.py`, new, runtime-only, against
`02-chain/sc-shroudmaul.html` — the pushed tip, 28 relics, neither Cindercleave
nor Bloodmirror in it. Grudgebearer stands in as a bloodsworn warhammer with its
own Crucible suppressed, **exactly as `grab_lab` used it for the umbral one**, so
this document's numbers and v56's are directly comparable. **27 foes x 26 seeds =
702 fights an arm**, 26 arms, ~18,000 fights. Nothing is written to any build.

**HARNESS CONTROL, run first** (repricing-v57 open decision 4). This session is
Chromium **141.0.7390.37** — byte-identical to the v57 and v59 sessions. The
warhammer row at `--pin 14` against `sc-nightfell.html` returns bloodsworn +15.0,
umbral +7.3, runic +1.9, verdant −0.8: **v57's table to the decimal, all four
cells.** `docs/RUNTIME-DRIFT.md` still applies to anything rendered on the
repo's pinned 151.

Rick's §1, verbatim:

> *the hammer gains massive rotational speed. It also gets a barbed wire ring
> around it that matches its hit range. enemies caught in the barbed wire are
> stunned, gain a bleed stack, and are held until the hammer comes around and
> connects. the connection deals massive knockback and causes the barbed wire
> ring to explode and expire, applying bleed again.*

---

# 0. THE ONE THING IN IT THAT NOTHING ELSE IN THE GAME DOES

**The hold's length is not a number. It is however long the head takes to come
around.** Every other hold in this roster is a duration field — Bramblesnare's
1.6s, Rootfast's 1.3s, Grasp's grab and true-stun timers, the Crucible's freeze.
This one falls out of the rotation, so winding the hammer faster *shortens* the
hold and buys the payoff sooner. Measured, monotonically, across the spin sweep:

```
spin x2.0    5.3s held        spin x9.0    3.0s held
spin x3.4    4.8s held        spin x12.0   2.4s held
spin x6.0    4.1s held
```

That is the whole design in one line — **the weapon is its own timer** — and it
is free, because `mode:"spin"` is what a warhammer already is.

---

# 1. THE ULTIMATE IS ONE SCALAR, AND THE REGISTERED PREDICTION IS REFUTED

Registered before the full run:

> *The hold is short by construction, so v56's law (+2.6 win points per second
> held) makes it worth little. Most of the value will be in the extra blows the
> fast spin lands — a damage ultimate in a control ultimate's costume.*

**Wrong, and not marginally.** Regressed across all 22 tuning arms:

```
predictor                       r       r²    what it means
FOE BLOWS NOT LANDED        +0.942   0.89    the whole thing
catches                     +0.684   0.47
connects                    +0.606   0.37
held seconds                +0.514   0.26    v56's currency. Not this one's
OWN blows                   -0.088   0.01    the extra swings are worth NOTHING
```

```
lift = +8.2 + 8.25 x (blows the opponent did not land)
residual sd 2.0pp against a per-arm SE of 2.7pp
```

**The residuals are smaller than the measurement error**, and the line was then
shown four arms it had never seen — the two bleed repairs in §3 and their
combination:

```
arm                        foe denied   predicted   actual   residual
explosion consumes, 8/stk         2.8       +31.3    +29.9      -1.4
explosion consumes, 14/stk        3.2       +34.6    +36.6      +2.0
ceiling 4 -> 8                    2.5       +28.9    +27.3      -1.6
ceiling 8 AND consume             3.0       +33.0    +31.7      -1.3
```

**Every held-out residual is inside one standard error.** This is the first law
in this project that has been validated out of sample rather than fitted and
quoted.

## 1.1 AND THE OBVIOUS CONFOUND WAS CHECKED, BECAUSE IT WOULD HAVE INVERTED THE READING

A relic that wins sooner faces fewer blows *as a consequence* of winning. Fight
length does move — r(lift, duration) = **−0.732**, floor 45.4s down to 40.4s on
the strongest arm. So the column was recomputed as a RATE:

```
foe blows per second       floor 0.365/s   -> 0.297-0.345/s across the arms
r(lift, foe blows per second denied)  =  +0.815     r² 0.66
```

**Two thirds of the effect survives normalising for fight length.** The
ultimate genuinely suppresses the opponent's rate of attack; it does not merely
end the fight before the opponent can swing.

## 1.2 WHICH MEANS, HONESTLY, THAT IT IS A CONTROL ULTIMATE

The currency is the same one Crucible and Grasp are paid in. **"Massive
rotational speed" earns its place as a picture and as the clock that sets the
hold — not as damage.** Own blows move 8.4 → 9.1 across the entire spin sweep
and have no relationship to the win rate at all.

It still pays on its own account: **spin with no ring at all is +18.7**, and the
law predicts +18.9 from the blows that arm denies. It just does not pay by
hitting more often. It pays by being a bigger, faster obstacle.

---

# 2. THE §1 AS WRITTEN IS ONE NOTCH ABOVE THE FIELD, NOT AT IT

```
§1 as written, placeholder numbers          +27.8%
field of 27 built ultimates    mean +20.1   median +19.7   Q3 +25.5
```

Sixth of twenty-eight. v56's Grasp arrived at +20.4, dead on the median; this
one arrives above the third quartile, **so the blade will have to pay for it**
where Shroudmaul's barely did. That is a bisection problem, not a design
problem, and §5 says which knob is cheapest to give back.

---

# 3. BOTH HALVES OF THE BLEED SENTENCE ARE INERT

```
explosion applies 1 stack                   64.5%    +27.8%
explosion applies 4 stacks                  64.5%    +27.8%     identical
no bleed on the catch at all                62.8%    +26.1%     -1.7, inside noise
```

**Applying one stack and applying four are the same number to the decimal.**
`hemorrhage` is `{ maxStacks: 4, dur: 3.2, dps: 1.5 }` and the hammer's own
`onHit` already puts on **2 per blow**, so the bar is full before the ultimate
casts and every application the ring makes is a clock refresh.

This is `bloodmirror-build-brief-v59.md` §3.1 again, one relic later, in the
same school: *"Rick's sentence describes a mechanic the game currently
forbids."* Two repairs were priced and **neither is the obvious one**:

```
ceiling 4 -> 8 while the ring stands  (Bloodmirror's answer)   +27.4    +0 vs §1
explosion CONSUMES the stacks,  8 damage a stack               +29.9    +2.1
explosion CONSUMES the stacks, 14 damage a stack               +36.6    +8.8
ceiling 8 AND consume                                          +31.8    +4.0
```

**Bloodmirror's ceiling trick transfers nothing** — Bloodletting mills at 0.22s
and needs headroom; this hammer lands 8.6 blows a fight and cannot fill 4, let
alone 8.

**And consuming is a damage knob wearing an interaction's clothes.** Note that
`connect dmg x2` — plain extra damage, no bleed involved — is **+33.6**, and
consume-at-14 (~56 bonus damage on a 23.5 blade) is +36.6. They are the same
curve. The consume buys a real thing, but it is legibility, not strength: the
payoff would scale with the fight the hammer has actually had.

> **It also collides with Crucible for the third time.** *"Pulls the foe in and
> consumes Sunder"* is the dwarven warhammer's tip. *"Catches the foe and
> consumes Hemorrhage"* is the same sentence with a different noun, on the same
> weapon. §4.

---

# 4. THE COLLISIONS — THERE ARE THREE AND THEY ARE ALL WITH THE SAME TWO RELICS

```
                 CRUCIBLE (dwarven warhammer)   GRASP (umbral warhammer)   THIS ONE
stops the foe    pull + freeze                  repeated grabs             ring catch
spins faster     spinMul 3.4                    —                          yes
consumes         Sunder                         —                          only if §3
```

v56 §7c already said it about the second one: *"the second warhammer in a
roster of twenty-eight whose ultimate stops the other fighter moving, and that
has to be a decision rather than an accident."* **This is the third, on seven
warhammers**, and §1.2 says the measured currency is the same for all three.

**What actually separates it, and it is real:** Crucible's hold is a freeze with
a cash-out, Grasp's is a counter that must be earned, and this one's is a hold
whose length is set by the weapon's own rotation and which **ends with the
weapon arriving**. It is the only hold in the game that resolves itself with a
hit rather than with a timer, and it is the only ultimate whose area is exactly
the weapon's own reach, drawn.

Whether that is enough is Rick's call and it is open decision 1.

---

# 5. THE KNOBS

## 5a. THE RING'S RADIUS IS THE STRONGEST LEVER AND ALSO THE LEGIBILITY RISK

```
radius   lift     catches   connects   share of catches that PAY OFF
  76    +34.5%      1.50       0.70                 47%
 110    +27.8%      1.62       1.21                 75%
 150    +22.6%      1.78       1.66                 93%
 220    +21.8%      1.84       1.80                 98%
```

**Smaller is stronger and less legible, and the two trade against each other
directly.** At 76 the caught ball drifts out of the head's path — `f.stun` locks
the weapon, not the ball, `moveMul` floors at 0.45 — so **more than half of all
catches never get the hammer the §1 promises.** The ring just holds until the
window runs out, which is worth a lot and looks like a bug.

**"Matches its hit range" reads as 110, not 76**, and this is the happy part:
the head sits at `reach` 76 from the ball centre and the foe's ball is `ballR`
34, so a blow lands at about 110 between centres. Rick's own sentence points at
the number where three quarters of catches pay off. **Take 110.**

## 5b. MASSIVE KNOCKBACK IS REAL, AND 2x IS ALL OF IT

```
a normal blow's knock (x1)   +25.2         x2   +30.1         x5   +29.8
```

+4.9 for the first doubling and **nothing after it**. A warhammer's `knockMul`
is already 2.3, so 2x on top is 760 — comfortably the hardest single knock in
the game outside Revenant's 700 hands, and it costs no more than 5x would.

## 5c. ROTATION

```
x2.0  +25.5    x3.4  +22.8    x6.0  +27.8    x9.0  +30.9    x12.0  +29.5
```

**Flat to noise across a six-fold range** (SE 2.7pp, spread 8.1pp). The
ultimate is not sensitive to this, so **pick it for the picture** — which is the
same freedom v56 found and the same freedom v59 found, and it is becoming this
project's most reliable result. x3.4 is Crucible's and should be avoided for
that reason alone; **x6 to x9** is a hammer that has clearly stopped being a
hammer and started being a machine.

## 5d. THE WINDOW

```
4s  +19.1        8s  +27.8        12s  +30.9
```

Diminishing, and 8s is where the §1 sits.

---

# 6. "EXPLODE AND EXPIRE" IS THE BALANCE KNOB, AND IT IS ALREADY IN RICK'S OWN SENTENCE

```
the ring expires on the connect (as written)     +27.8%
the window runs on, ring re-arms                 +45.9%     the clause is worth 18.1 points
```

Second relic running where the reward truncating its own window is what keeps
the relic honest — v56 §3 measured 10.8 to 13.7 points for the same clause on
Grasp. Without it this ultimate is above everything in the game except
Triplicate, Harrowing and Revenant. **Keep it**, and note it is a rule a viewer
watches happen rather than a number in a tooltip.

---

# 7. PINNING THE BALL COSTS NOTHING AND BUYS THE PAYOFF

```
                        lift      held    connects
stun only (as written)  +27.8%     4.1s      1.21
stun + pin the ball     +27.5%     2.7s      1.39
```

**Identical in value** (0.3pp against a 2.7pp SE) and **+15% more connects**. The
foe stops drifting out of the head's path, so the promised hammer actually
arrives. This is the opposite of v56's finding — there, pinning cost 3.3pp at
identical hold, because Grasp needed the foe to be knockable *toward* the
wielder. Here the wielder is the thing coming around, so holding the ball still
is free.

**Against it:** `f.pin` is written by exactly one relic in the game, Paradox's
Stasis Field, and v56 §5 called it *"the Stasis Field's only exclusive verb."*
Spending it here is a real cost paid in another relic's identity, for a
legibility gain. Open decision 3.

---

# 8. WHAT THIS LAB CANNOT TELL YOU

- **Nothing here has been seen in motion.** A ring at the hammer's own hit
  range, spinning at 6-9x, is either the clearest object in the game or an
  unreadable blur, and no number above distinguishes those. v43 §13 and v54 §2c
  both stand: **film it before tuning it.**
- The connect is detected as `|theta − bearing| ≤ 0.25 rad`, which is the lab's
  stand-in for the engine's own `tickHits`. The real one has `hitCd` 0.45 and a
  head width; connect counts will move in the build.
- Grudgebearer is standing in. Its `dmg` is 23.5 and the real relic's will be
  bisected, and §2 says downward.
- The 22-arm fit shares one relic, one blade and one charge. It is a
  within-relic law, exactly as v56's and v59's were.
- **Charge was not swept.** 16 throughout. v55b: nobody's was ever derived, and
  unlike Grasp this ultimate does scale with cast count.
- Shades are untested. Triplicate puts three bodies in the hall and a ring at
  hit range will catch whichever is nearest.

---

# 9. RICK'S RULINGS, AND THE SNAG MEASURED

All four open questions above were answered the same session. Two of the answers
looked contradictory as they were put — *"the wire snags, doesn't stun"* removes
the hold, *"freeze the ball too"* refines it — and **they combine into a design
neither option offered**:

> **The ball is held. The weapon is not.** You are caught in the wire, you cannot
> leave, and you can still fight back.

**It is a verb nothing in this game uses.** The engine's own comment at `this.pin`
— *"unable to move (ball and weapon)"* — confirms Paradox writes both halves;
Crucible and Grasp write the weapon half. **Ball held, weapon free is unused.**

```
                     ball        weapon      can the foe act?
CRUCIBLE             pulled      LOCKED      no
GRASP                free        LOCKED      no
STASIS FIELD         HELD        LOCKED      no
GARROTE              HELD        free        YES — it just cannot leave
```

Which retires §4's collision without weakening anything, and makes a better
fight: the quarry is not a statue waiting to be hit, it is tethered and swinging
while a hammer winds up beside it.

## 9.1 THE NUMBERS, 702 FIGHTS AN ARM

```
arm                                       lift    connects   held
ring that only cuts, no hold at all      +19.6%       1.17    4.3s
SNAG — ball held, weapon free            +24.0%       1.38    2.8s
  + explosion consumes bleed,  8/stack   +30.3%       1.35    2.8s
  + explosion consumes bleed, 14/stack   +35.3%       1.30    2.8s
  + explosion consumes bleed, 20/stack   +38.4%       1.28    2.7s
  + consume 14 at spin x9                +37.3%       1.39    1.8s
the stun version, for comparison         +27.8%       1.21    4.1s
field of 27 built ultimates    mean +20.1   median +19.7   Q3 +25.5
```

- **Snagging costs 3.8 points against stunning** — 1.4 SE. That is the entire
  price of the unique verb.
- **The hold itself is worth +4.4** (+24.0 against +19.6). A ring that only cuts
  is a median ultimate; a ring that holds you is a good one. **The pin is not
  decoration.**
- **The consume is linear at +0.73 win points per point of per-stack damage**,
  dead straight across 0 to 20. It is now the balance dial, and it is a better
  one than a stun duration because a viewer watches it happen.
- **Spin stays free**: x9 with consume-14 is +37.3 against x6's +35.3, inside
  noise. Third relic running where the arrangement is free at constant value.

## 9.2 THE LAW TRANSFERS, WITH A NAMED BIAS

§1's line was fitted on stun arms. Against the six snag arms — a different
mechanic — it predicts with a **mean residual of −1.9pp**, five of six inside one
SE. It runs slightly optimistic, which is what it should do: a snagged foe keeps
swinging, and the line was fitted where being held meant being unable to act.

## 9.3 THE OTHER TWO RULINGS

**Radius 110**, the hammer's real hit range, over the stronger 76 — 3 catches in
4 pay off instead of fewer than half. **And the explosion consumes**, over
leaving the bleed as picture only.

## 9.4 NAMED

**RAVELBONE**, and its ultimate **GARROTE** — both Rick's, from spreads of four.
Build stages, engine traps and the probe are in
`sundered-crown-ravelbone-build-brief-v60.md`.

---

# Open decisions

1. **~~Three warhammers that stop the other fighter.~~** CLOSED by §9 — the snag
   holds the ball and leaves the weapon, which none of the other three do.

2. **~~The bleed.~~** CLOSED — the explosion consumes. §9.1 for the ladder; **the
   per-stack number is still open** and 8 is the recommendation, settled after the
   blade bisection because the two trade directly.

3. **~~Pin the ball?~~** CLOSED — yes, and it turned out to be the mechanic
   rather than a refinement of it.

4. **~~Radius.~~** CLOSED — 110.

5. **DOES RAVELBONE KEEP ITS SPIN DIRECTION THROUGH A LOST CLANK?** New, found
   while writing the brief. `resolveClank` grants that immunity off `f.ultSpin`,
   which is Twinshade's field. A hammer that reverses mid-window never comes
   around and the snag it is holding pays nothing — so it should be granted
   deliberately from Ravelbone's own field rather than inherited by accident.

6. **CHARGE.** 16 by default, never swept, and this ultimate scales with casts.

7. **DOES THE RING SNAG SHADES?** A rule, not a knob.

8. **THE COLLAPSE AGAINST A HELD BALL.** Completely unmeasured.

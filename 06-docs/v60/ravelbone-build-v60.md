# v60 — RAVELBONE, THE 30TH RELIC. The brief's central instruction is not sufficient on this engine and the line that would have deleted the relic is in Paradox's bookkeeping; the stage-2 gate then missed by two sigma, and what it caught was that the thing built was not the thing priced.

**2026-09-01.** `tools/ravelbone_build.py`, `tools/garrote_relic_probe.py`,
`tools/garrote_sheet.py`, `tools/wire_channel.py`.

```
02-chain/sc-ravelbone.html   STAGE 1   the 30th relic, GARROTE stubbed at charge 1e9
02-chain/sc-wire.html        STAGE 2   the ring: snag, hold, connect, throw.
                                       NO consume yet
02-chain/sc-garrote.html     STAGE 3   BUILD OF RECORD. The explosion consumes
                                       Hemorrhage, and the RING expires while
                                       the window runs on
```

**THE HEADLINE IS THAT THE ULTIMATE WAS BUILT WRONG AND THE GATE FOUND IT.**
The connect ended the ring AND the wind-up together, because they were one
field. Rebuilding the design's own arm table on the built relic showed the
wind-up alone is worth **+24.3** — the registered number to the decimal — and
that adding the ring **COST 8.1 points**, because it cut the window from 16.0s
a fight to 5.6s. Rick took `expire:"ring"`; the shipped relic measures
**+32.9** against the design's registered **+29.9**.

Rick chose **RAVELBONE ALONE** from the three routes in
`CONFLICT-READ-FIRST-v60.md`, with the red hammer's kick folded into the
connect. `redhammer-design-v60.md` is renamed `-SUPERSEDED` and not deleted,
because two things in it are load-bearing for the build that won.

---

# 0. THREE CORRECTIONS TO THE BRIEF, ALL BOOKKEEPING

**IT IS THE THIRTIETH RELIC AND THE BRIEF SAYS THIRTY-FIRST.** The brief was
written expecting Bloodmirror to land first. Bloodmirror is neither built nor
in this repo. `WEAPONS` holds 29 on `sc-breach.html`, so counted, Ravelbone is
30 and every `engine_ab` in the gates runs over 29 others.

**AND IT IS NOT BLOODSWORN'S LAST OPEN CELL.** Counted on the tip, bloodsworn
holds twinblade, greatsword, flail and bow. This puts it on 5 of 6 and leaves
**bloodsworn × scythe open** — which is the cell Bloodmirror is designed into,
and is why the brief's sentence reads as it does. The warhammer goes to 5 of 7
schools, which is untouched.

**AND THE DESIGN DOC IS OUT OF DATE ABOUT `f.pin`.** §7 says *"`f.pin` is
written by exactly one relic in the game, Paradox's Stasis Field"* and calls
spending it here *"a real cost paid in another relic's identity"*. **That
stopped being true in v56.** Grasp's squeeze writes `foe.pin = u.squeeze` for
0.30s, three pulses a window, on the build the wire lab itself was measured
against. So the exclusivity argument was already spent once before this relic
asked for it, and the cost is smaller than the doc prices it.

---

# 1. THE BRIEF'S CENTRAL INSTRUCTION IS NOT SUFFICIENT, AND OBEYING IT EXACTLY WOULD HAVE DELETED THE RELIC

Brief §3, in bold: **"Write `f.pin`. Do NOT write `f.stun`."** That is the whole
separation — ball held, weapon free, the one verb nothing else in this game
uses — and it is worth 3.8 measured points to give up the stun version.

`tickWire` does not write `f.stun`. **It does not have to.**

```js
// tickStasis, and this loop runs for BOTH fighters on EVERY frame,
// OUTSIDE the `ultField` guard below it
if (f.pin <= 0) continue;
f.pin  = Math.max(0, f.pin - dt);
f.stun = Math.max(f.stun, f.pin);        // <- here
```

**Any relic that writes `pin` is handed a weapon lock by Paradox's
bookkeeping.** Garrote would have locked the weapon it was built to leave free;
the caught fighter would have stopped swinging; the entire design would have
been invisible on screen — and a probe asserting *"tickWire never writes
f.stun"* would have passed, because tickWire does not. **THE WRITE IS SOMEWHERE
ELSE.**

The fix is `f.pinFree`, a flag saying what KIND of hold this is, read by the
two places that care. It is 0 for both existing writers, so `engine_ab` is the
proof rather than the comment.

> **AND THE SECOND READER IS A PICTURE FAULT WITH EVERY NUMBER CORRECT.**
> `_drawField`'s held-ball block hardcodes `AFFINITIES.runic` — it is the
> Stasis Field's hexagon — and it fires on `f.pin > 0`. Unguarded, **a
> bloodsworn wire snag draws Paradox's hexagon around the ball it caught.**
> §4.1's own defect class, and no numeric check in this repo could have seen
> it. `garrote_relic_probe [X]` reads the guard off `_drawField`'s source.

> **SHROUDMAUL HAS THAT SECOND FAULT LIVE, TODAY.** Grasp's squeeze writes
> `pin` and sets no flag, so a runic hexagon is drawn on the quarry for 0.30s a
> squeeze, three squeezes a window, in an UMBRAL relic's set-piece. It is not
> this build's to fix — `pinFree` makes the fix one line — and CLAUDE.md's own
> Shroudmaul paragraph says nobody has watched the relic. **Open item 41.**

---

# 2. TWO CONTRADICTIONS INSIDE THE ENGINE'S OWN PROSE

**`ballCollision` DOES gate on `pin`, and two comments say it does not.** The
`Fighter.pin` declaration says *"`ballCollision` is deliberately NOT gated — a
held ball can still be shouldered out of the way, which is what the probe
measured"*, and brief §3 quotes it. The code says the opposite and says so at
length:

```js
const pa = a.pin > 0, pb = b.pin > 0;
const wa = pa ? 0 : (pb ? 1 : 0.5), wb = pb ? 0 : (pa ? 1 : 0.5);
```

*"A HELD BALL IS AN IMMOVABLE OBJECT."* The declaration is **stale** — it
predates a change whose own comment records Rick finding the bug in a clip
(*"It STUCK to the thing it had just frozen and slid along it"*).

**It matters for this relic and it is not obviously bad.** A Ravelbone that
shoulders its own catch takes the whole impulse at 2×, so the hammer bounces
off the thing it is holding. That could push the wielder away before the head
comes around — or hold the pair together. Unmeasured. **Open item 42.**

---

# 3. THE CONNECT IS THE MERGE, AND IT IS NOT THE BRIEF'S `knock x2`

The wire lab priced the throw as a multiple of a normal blow: **x1 +25.2, x2
+30.1, x5 +29.8** — +4.9 for the first doubling and nothing after it. It
measured the knockback for VALUE and never for whether it READS, and the red
hammer measured exactly that and refuted it: the impulse is real and exactly
`knock × knockMul`, but most of it is spent CANCELLING the incoming velocity,
and `move()` governs speed rather than conserving it.

So the connect is **the ordinary knock plus `kick` 800 under `launch` 1.2s**.
`launch` is a permission and not a push — it raises the vmax clamp and adds no
velocity, which is why below about kick 500 it changes nothing at all.

> **AND THE GAME'S OWN CONSTANT FOR THE SAME VERB IS THE WORST VALUE IN THE
> SWEEP.** The Crucible's `launch: 2400`, on the same weapon type, piles
> arrivals against `vmax` 2795 and collapses the arrival spread from 3.65 to
> 1.70. The Crucible pays ONCE at the end of a charge; this pays per event.
> Copying it would have reproduced a clipping defect one ceiling higher — and
> the shipped build was already clipping, with p90 arrival at exactly
> `speedMax` 1300.

**THE SNAG IS WHY IT LANDS HERE AND DID NOT THERE.** A ball just released from
a hold has no incoming velocity to cancel, so this is the one case in the game
where the whole impulse goes into departure.

**AND THE RELEASE IS WRITTEN ABOVE THE ORDINARY KNOCK, NOT BESIDE THE KICK.**
Nulling `pinV` is what actually saves the impulse, so the payload block would
work today either way — and would break silently the first time anyone
reordered the two. The order is the guarantee.

---

# 4. THE PROBE REPORTED FIVE DEFECTS AND ALL FIVE WERE THE PROBE

`garrote_relic_probe` reported, in its first cuts: 294 connects that did not
move the ball, 0 cast beats against 111 casts, 4637 stunned held frames, and
6470 frozen weapons. **Every one of them was the instrument.**

```
[8a]  294 connects "did not move the ball"    the connect sets hitStop 0.14s = 17
                                              frames of `decayImpactOnly`, in
                                              which `move()` never runs. The check
                                              was measuring the freeze its own
                                              event caused, and would have failed
                                              identically on a perfect build and
                                              on the broken one the brief warns of
[8b]  and 294 again after waiting for it      `step()` tests the freeze at the TOP
                                              and returns through the path that
                                              DECREMENTS it, so the step that
                                              takes `hitStop` to zero is a step
                                              whose `move()` never ran. The first
                                              frame reading "not frozen" is still
                                              a frame that did not move
[11]  0 cast beats against 111 casts          a frame flag cannot tell the cast's
                                              beat from the catch's. Attribute a
                                              beat to the CALL that filed it
[4a]  2 catches "lengthened the weapon lock"  sampled across the whole step, so a
                                              blow landing elsewhere in it counted
[4b]  6470 "frozen" weapons while held        1983 were hit stops (nobody's weapon
                                              turns), 4637 were ordinary hitstun
                                              carried in at the catch, and the last
                                              222 were stun expiring INSIDE a step
```

**A CHECK THAT COUNTS FRAMES IN WHICH AN EVENT IS POSSIBLE IS NOT COUNTING THE
EVENT.** `gravemourn_relic_probe`'s lesson and v56's crush probe's — **five
separate times inside one file**, which is enough instances to stop calling it a
recurrence and start calling it **the default failure mode of a probe on an
engine whose every impact opens with a freeze**.

> **AND THE BRIEF SPECIFIED TWO OF THEM.** §6 check 8, called *"the most
> important check in this document"*, says to read the ball's position **two
> frames after the connect**. On this engine that window is entirely inside the
> hit stop the connect itself sets, and even waiting for `hitStop <= 0` is one
> frame too early. **The check as specified cannot pass on a correct build.**
>
> **THE BUILD WAS SETTLED BY A TRACE AND NOT BY THE CHECK.** Three connects
> followed frame by frame: departure at 1077/-1487, 711/-1674 and 1918/1140 —
> **|v| up to 1836 px/s against a `speedMax` of 1300**, which is `launch` doing
> exactly what it is for — and the quarry a third of the way across the hall
> twenty frames later. When a check on the most important sentence in a design
> fails, read the thing itself before believing either side.

> **[4] ALSO HAD TO STOP READING THE SOURCE.** Because the stun write is in
> `tickStasis`, the only honest test of "ball held, weapon free" is the
> observable one: the caught fighter's weapon must still be TURNING and must
> still LAND BLOWS. It does both.

---

# 4a. THE CONSUME EATS 1.81 STACKS AND THE DESIGN ASSUMED FOUR

Design §3's whole argument for the consume is that the bleed is inert *because
the bar is already full*: `hemorrhage` caps at 4, the hammer's own `onHit` puts
on 2 a blow, so *"the bar is full before the ultimate casts"*. §5 prices the
consume off that — 8 a stack, *"~56 damage on the connect"*.

**Measured on the built relic, over 308 connects: the quarry is carrying 1.81
stacks when the hammer arrives.**

```
mean stacks eaten       1.81      against the 4 the pricing assumes
mean burst              14.5      against ~32
mean connect            42.6      against ~56
and without the consume 29.8      so the consume is worth +12.8 a connect
```

The reason is in the same paragraph, read the other way: `hemorrhage` has
`dur: 3.2` and this hammer lands **8.6 blows a fight**, roughly one every five
seconds. **The bar is full for about three seconds after each blow and empty
for the two after that**, and a connect arrives whenever the head comes around
rather than on the beat of a blow. The inertness measurement (1 stack and 4
stacks returning 64.5% to the decimal) is not wrong — it was measured on the
ring APPLYING stacks, where the cap bites. The consume READS the pool, where
the clock bites instead.

> **SO THE CONSUME IS ABOUT HALF THE KNOB THE DESIGN PRICED**, and its linear
> rate of +0.73 win points per point of per-stack damage is a rate per point of
> `consume`, not per point of delivered burst. Nothing about the recommendation
> changes — 8 is still the start and it still settles after the bisection — but
> **do not carry "~56 damage on the connect" into stage 4's arithmetic.**

> **AND THE QUARRY ENDS A CONNECT CARRYING TWO STACKS, WHICH IS RICK'S SENTENCE
> BUILT WITHOUT ANYBODY AIMING AT IT.** The consume empties the pool, and the
> hammer's own `onHit:{hemorrhage:2}` lands further down `resolveHit` on the
> quarry it just emptied. §1: the connection *"causes the barbed wire ring to
> explode and expire, **applying bleed again**."* The first cut of the probe's
> check 12 asserted zero stacks afterwards and reported 308 defects of 308.

---

# 5. WHAT IS MEASURED SO FAR

```
STAGE 1   engine_ab   3248/3248 identical across all 29 relics
          verify      12/13, the FAIL being the KNOWN thirteenth check
                      (Lightkeeper/Farwarden 74.4s). No Ravelbone pairing is
                      over the band
          floor       Ravelbone with no ultimate: 32.7%
STAGE 2   verify      12/13, same known FAIL, same 74.4s pairing
          THE RING    Ravelbone: 47.0%          LIFT +14.3
          probe       24/25 (garrote_relic_probe)
STAGE 3   probe       26/27, the lone FAIL being the registered connects-per-
                      cast band — 0.91 against 0.8-0.9
          verify      12/13, same known FAIL, same 74.4s pairing.
                      Roster spread 20.8pp, Heartwood 37.2 .. Farwarden 58.0
          engine_ab   360/360 identical, RAVELBONE INCLUDED, against the same
                      build without the `expire` knob — so the knob is proven
                      inert at its default rather than assumed to be
```

**AND THE CLIP EXISTS.** `07-shorts/v60/garrote-first-cut.mp4` — ravelbone vs
axiom, seed 10007, the full fight from zero, three casts of Garrote, 4183
frames. `cinema_clip` reported *"no killing blow on this seed (timeout finish);
using the last cut"*, which is **open item 29 and not this relic's** — the
fight ended `hp=[14, 0]` at 64.65s.

## 5a. THE STAGE-2 GATE FAILED, AND IT IS THE ONLY GATE IN THIS BRIEF THAT COULD HAVE

The brief's own words: *"A stage-2 build that lands near **+24% ± 3** over its
own no-ultimate floor is the gate; if it does not, **the consume will paper over
whatever is wrong with the ring** and nobody will find it until the bisection
misbehaves."*

**Measured: +14.3** by `verify`, and **+16.2 ± 2.5** by `wire_channel` on the
same build with the charge toggled — two instruments agreeing, and the small
difference is the side-A/side-B asymmetry (`verify` pairs `i < j`, so an
appended relic is side B in all its pairings).

**AND THE HONEST SIZE OF THE MISS IS TWO SIGMA, NOT TEN POINTS.**
`cell-error-v60.md` §2 measured the error bar on exactly this kind of quantity
rather than assuming it: the SE on a lift is ~3pp at 540 fights, and **a
DIFFERENCE between two lifts carries ~6pp**. Against `wire_lab`'s own stated
2.7pp, the gap is

```
registered   +24.0  +/- 2.7      (wire_lab, 702 fights an arm)
measured     +16.2  +/- 2.5      (wire_channel, 754 fights an arm)
difference    -7.8  +/- 3.7      ~2.1 sigma
```

So this is a real discrepancy worth chasing and it is **not** a broken relic.
Stating it as "ten points" would be the same error `cell-error-v60.md` was
written to stop — and that document has this project's own instance of it:
`bloodsworn x warhammer` itself moved **+16.3 to +10.7 between two seed
blocks**.

It is not `verify`'s side-B asymmetry: that costs about 1.3pp and it applies to
the floor and to the ring alike, so it cancels in the difference. And it is not
the ring failing to fire — every contact number came in AT or ABOVE the lab's:

```
                       LAB (wire_lab)      BUILT
connects per cast          ~0.75            0.91      the registered band is 0.8-0.9
catches                     1.62            1.90      a fight
window used                   --            2.70s     of its own 8s, because the
                                                      connect ends it
mean hold                     --            1.85s
```

**So the ring catches more, holds, and connects more often than the lab's did,
and delivers ten points less.** That is a coherent thing to be wrong and it is
worth finding before anything is tuned.

**THE CANDIDATE NOBODY HAS RULED OUT IS THE STAND-IN'S CHANNEL.** `wire_lab`
uses *"Grudgebearer standing in as a bloodsworn warhammer with its own Crucible
suppressed"* — and Grudgebearer's `onHit` is **`{sunder: 1}`**, not
`{hemorrhage: 2}`. Sunder is measured as **the biggest damage-rate channel in
the game** (open item 23, +13.6%); Hemorrhage costs this cell **fifty blade
damage a fight** while lifting its win rate, because the bleed shortens the
fight. If the lab's floor arm and its ring arms were both carrying Sunder, then
every lift in `wirering-design-v60.md` is a lift measured on a different
channel, and the whole arm table would need re-reading before the +24 means
anything here.

## 5b. AND THE CHANNEL IS REFUTED — IN THE WRONG DIRECTION

`wire_channel.py`, four arms at 754 fights each on `sc-wire.html`:

```
channel       ult    win      SE     dur     dealt   casts
hemorrhage    off   31.4%   1.69   45.2s      269    0.00
hemorrhage    ON    47.6%   1.82   44.7s      291    1.99
sunder        off   30.6%   1.68   45.8s      326    0.00
sunder        ON    42.6%   1.80   45.7s      358    2.03

    LIFT through hemorrhage (shipped)   +16.2  +/- 2.5
    LIFT through sunder     (the lab)   +11.9  +/- 2.5
```

**Sunder lifts LESS, not more.** If `wire_lab`'s stand-in was carrying Sunder,
it should have measured BELOW the hemorrhage number, not eleven points above
it. **The yardstick is eliminated and the gap is still there** — and the
shipped lift of +16.2 ± 2.5 agrees with `verify`'s +14.3, which is the two
instruments confirming each other.

> **THE HYPOTHESIS WAS WORTH TESTING AND IT WAS WRONG, WHICH IS THE POINT OF
> WRITING IT DOWN BEFORE RUNNING IT.** It had a mechanism (opposite-signed
> channels, open items 23 and 24), it had a number attached, and one run
> settled it. What it also produced for free is the first side-by-side pricing
> of the two channels on ONE relic at ONE blade: **Sunder delivers 358 damage a
> fight against Hemorrhage's 291 and wins five points less often**, which is
> open item 24's confound in its cleanest form yet.

## 5c. FOUND IT. THE WIND-UP IS THE WHOLE ULTIMATE, AND THE RING SPENDS IT

`wire_channel.py --decompose`, the design's own arms rebuilt on the built
relic, 754 fights each:

```
arm                        win      SE   casts  window   blows  foe blows
the floor, no ultimate    31.4%   1.69    0.00   0.00s    7.96     16.42
the WIND-UP alone         55.7%   1.81    1.99  15.99s    9.19     14.83
the ring, spin x1         36.7%   1.76    2.01   8.22s    7.97     16.15
EVERYTHING, as shipped    47.6%   1.82    1.99   5.67s    8.66     15.33

    the WIND-UP alone      +24.3  +/- 2.5      <- the registered number, exactly
    the ring, spin x1       +5.3  +/- 2.4
    EVERYTHING, as shipped +16.2  +/- 2.5      <- and the two together are WORSE
```

**The wind-up alone is +24.3, which is the registered +24 to the decimal. Adding
the ring COSTS 8.1 points.** The two are sub-additive by **13.4**.

**AND THE `window` COLUMN SAYS WHY.** `dur` is 8.0s and the relic casts ~2.0
times a fight, so a full window is 16.0s of ultimate a fight — which is exactly
what the wind-up-alone arm gets, because with `radius` 0 nothing can ever be
caught. **The shipped relic gets 5.67s.** The connect expires the ring, the ring
and the window are the same object, and so **the ring cuts the wind-up off after
about a third of it.**

> **THE DESIGN'S CAUSAL STORY IS INVERTED ON THE BUILT RELIC.** §1.2 says
> *"'Massive rotational speed' earns its place as a picture and as the clock
> that sets the hold — not as damage"*, and prices OWN blows at r² 0.01. It is
> right that the spin does not pay by hitting more often — own blows move 7.96
> → 9.19, worth little — and **wrong that the spin is not the payload**. A
> hammer at 6× is a bigger, faster obstacle, and being an obstacle is what this
> ultimate is paid for.

> **AND THE DESIGN'S OWN LAW PREDICTED IT AND WAS NOT ASKED.**
> `lift = +8.2 + 8.25 × (blows the opponent did not land)`:
>
> ```
>                    foe blows   denied   predicted   measured
> the WIND-UP alone      14.83     1.59       +21.3      +24.3
> EVERYTHING shipped     15.33     1.09       +17.2      +16.2
> ```
>
> **Both inside the ~3pp the law's own residuals allow.** The law is not
> refuted by this build — it is CONFIRMED by it, and it is what says the ring is
> giving blows back to the opponent by ending the window early. The law was
> fitted across arms that all shared one window length, so it could not see the
> thing that actually moves it.

## 5d. AND THE ARM NOBODY MEASURED IS THE ONE RICK'S SENTENCE DESCRIBES

The lab has two arms for this clause and neither is the obvious third:

```
the ring expires on the connect (as written)   +27.8%     <- ring AND window end
the window runs on, ring RE-ARMS               +45.9%     <- two changes at once
the window runs on, ring does NOT re-arm        ------     never measured
```

**Rick's §1 says "causes the barbed wire ring to explode and expire."** It says
the RING expires. Nothing in his sentence stops the hammer spinning. The build
ends both because they are one field — `self.ultWire = null` — and that is a
BUILD decision that was never a design decision.

So the third arm is worth pricing before the blade is: the ring gets its one
catch and blows apart, the wind-up runs out the rest of its 8 seconds, and the
window still cannot re-arm — which keeps the +18.1-point restraint clause the
design says makes this relic honest.

**IT IS BUILT AND PRICED.** `ravelbone_build.py --expire ring|window`, and the
default is `window` because that is what shipped. `engine_ab` **360/360
identical, Ravelbone included**, between the build with the knob and the build
without it — so the knob is proven inert at its default rather than assumed to
be.

Both at STAGE 3, matched seeds, 754 fights an arm:

```
                        expire:"window"     expire:"ring"
the floor                   31.4%              31.4%      <- reproduced exactly
the WIND-UP alone           55.7%              55.7%      <- reproduced exactly
the ring, spin x1           39.5%              38.9%
EVERYTHING                  49.6%              64.3%
    LIFT                    +18.2              +32.9
    window used a fight      5.60s             15.31s     of 15.99s available
    foe blows                14.98              14.22     against a floor 16.42
```

## 5d.1 AND `expire:"ring"` REPRODUCES THE DESIGN. `expire:"window"` DOES NOT

This is the part that stops it being a preference. The design's own stage-3
number — the arm with the consume at 8 a stack — is **+29.9** (§3's repair
table).

```
                    registered   measured    gap        sigma
expire:"ring"          +29.9       +32.9     +3.0       0.8    inside noise
expire:"window"        +29.9       +18.2    -11.7       3.2    not
```

**`expire:"ring"` lands on the design's own prediction and the shipped
behaviour misses it by three sigma.** So the lab's arms were almost certainly
measuring a window that OUTLIVED its ring — which also makes its experimental
design coherent, because *"the window runs on, ring RE-ARMS, +45.9"* then
changes exactly one thing (the re-arming) rather than two.

**THE REJECTED ARM IS KEPT AS A CONTROL**, because both numbers in the table
above should stay reproducible:
`04-experiments/_garrote-expire-window.html` is the shipped build with the one
knob flipped, and it rebuilds to the same sha every time
(`ravelbone_build.py --stage 2/3 --expire window`).

**RICK TOOK `expire:"ring"`, 2026-09-01, with the pair measured in front of
him.** It is the shipped arm and the whole chain is rebuilt on it;
`sc-garrote.html` carries the sha of the variant that measured +32.9, so the
build that shipped is the build that was measured.

> **SO THIS IS A BUILD MISREADING BEING CORRECTED, NOT A BALANCE PREFERENCE.**
> "The ring explodes and expires" was implemented as "the ring and the window
> end together" because they were one field, and nothing in Rick's sentence or
> in the design says the hammer stops turning. **The registered prediction was
> not refuted — it was never tested**, because the thing built was not the
> thing priced.

> **AND THE LAW UNDER-PREDICTS THE RING ARM, WHICH IS NEW.**
> `lift = +8.2 + 8.25 × denied` gives **+26.4** for 2.20 blows denied against a
> measured **+32.9** — 6.5 points out, where the shipped arm and the wind-up
> arm both sat inside the law's own ~3pp residual. The law was fitted on arms
> that all shared one window length; the arm that changes window length is the
> one it misses. **Do not use it to price this knob.**

## 5d.2 WHAT IT COSTS IS THE PICTURE, AND THAT PART IS REAL

Under `expire:"ring"` the ring blows apart on the connect and the hammer keeps
turning at 6× for the remaining **~9.7 seconds** of its window with nothing at
its reach. The set-piece's payoff has visibly happened and the ultimate is
still running.

**That is the picture contradicting the mechanic**, which is the fault v56's
latch had and the one this project is most careful about. It is also the
cheapest kind of fault to fix — the window is still `f.ultWire`, `wireFade` is
still driven off it, and `W.spent` is exactly the flag a tell would read.

**IT IS PHOTOGRAPHED AND IT IS AS BAD AS IT SOUNDS.**
`05-reference/v60/garrote-states-tail.png` is that frame on a real match:
**there is no tell in the arena at all.** The ring is gone, the hammer is
turning, and a viewer sees a fast hammer rather than an ultimate. The name is
in the HUD and nowhere else. Open item 45, and it is Rick's — he took this arm
with the cost named, and now he has the frame.

---

# 6. WHAT SHIPPED

```
GARROTE   charge 16 · dur 8.0s · radius 110 · spinMul 6 · connectKnock 1
          kick 800 · launch 1.2s · consume 8 · expire "ring"
          tip "Holds the foe where it stands, then throws it and consumes
               Hemorrhage"    69/72 characters
RAVELBONE bloodsworn x warhammer · dmg 23.5, THE TYPE'S OWN AND NOT BISECTED
```

```
STAGE 1   engine_ab   3248/3248 identical across all 29 relics
          verify      12/13, the known Lightkeeper/Farwarden 74.4s
          floor       32.7% with no ultimate
STAGE 2   verify      12/13, same known FAIL.  THE RING +14.3 by verify
STAGE 3   probe       26/27 (garrote_relic_probe), the lone FAIL being the
                      registered connects-per-cast band — 0.91 against 0.8-0.9
          engine_ab   360/360 identical WITH RAVELBONE IN THE ROSTER against
                      the same build without the `expire` knob
          decompose   +32.9 over its own floor, against a registered +29.9
          verify      12/13, the known Lightkeeper/Farwarden 74.4s.
                      RAVELBONE 62.8% — THE TOP OF THE ROSTER — and the spread
                      is 26.0pp, Heartwood 36.7 .. Ravelbone 62.8
```

**AND THAT 62.8% IS THE POINT AT WHICH THE BLADE IS OWED, NOT A PROBLEM.**
`verify`'s band is 30-70% so it passes, but Ravelbone is now the strongest
relic in the game and the roster spread is the widest this project has carried
— 26.0pp against 20.8pp on the same build with `expire:"window"`, and against
the 18.5pp the umbral package shipped at. **The relic is untuned by
construction**: `dmg` is 23.5, the warhammer's own value and a bisection START,
and `TUNED_RB` is `None`.

> **THE DESIGN SAID THIS WOULD HAPPEN AND IT IS FINALLY SAYING IT ABOUT THE
> RIGHT BUILD.** §2: *"this one arrives above the third quartile, so the blade
> will have to pay for it where Shroudmaul's barely did. That is a bisection
> problem, not a design problem."* On `expire:"window"` the relic sat at 49.6%
> and there was nothing for the blade to give back; on the shipped arm there
> is.

**THE BLADE IS NOT BISECTED AND `TUNED_RB` IS `None`.** `--stage 4` exists and
REFUSES to run, with the reason printed. What settles a blade on this roster is
a wide direct measurement at n >= 1000 a point, on both sides, repeated on a
second block — never a bisection.

**AND THE RELIC IS NOW STRONG RATHER THAN WEAK**, which is the opposite of
where the day started: +32.9 over its own floor against a field of 27 built
ultimates whose mean is +20.1 and whose Q3 is +25.5. The design said the blade
would have to pay and by more than Shroudmaul's did; it now has more to pay
with. **The brief's "expect the answer BELOW 23.5" is finally a live
prediction rather than one measured against the wrong build.**

**The floor and the wind-up arms reproduce to the decimal across two separate
runs on two separate builds**, which is the cleanest control this measurement
could have had: the two variants differ in exactly one thing.

> **AND THE LAW UNDER-PREDICTS THE RING ARM, WHICH IS NEW.**
> `lift = +8.2 + 8.25 × denied` gives **+26.4** for 2.20 blows denied against a
> measured **+32.9** — 6.5 points out, where the shipped arm and the wind-up
> arm both sat inside the law's own ~3pp residual. The law was fitted on arms
> that all shared one window length; the arm that changes window length is the
> one it misses. **Do not use it to price this knob.**

---

## 5e. THE SUSPECT THAT WAS ELIMINATED ON THE WAY

Design §1.2, and it is not the +24: ***"spin with no ring at all is +18.7."***

**The whole built ultimate measures +16.2.** If the built wind-up is worth
anything like +18.7 on its own, then the ring is worth nothing and the design's
causal story is inverted; if the built wind-up is worth far less, the wind-up
is not doing what the lab's did and that is the ten points.

`wire_channel.py --decompose` rebuilds the design's own arm table on the built
relic — the floor, the wind-up alone (`radius` 0, so nothing can be caught),
the ring with `spinMul` 1, and everything as shipped — and reports **`foe
blows`** beside each, because the design's law is
`lift = +8.2 + 8.25 × (blows the opponent did not land)` at r² 0.89, validated
out of sample. **If the built arms move the win rate without moving that
column, the law does not describe this build**, and that is a larger finding
than the blade.

> **DO NOT PROCEED TO THE BISECTION UNTIL THIS IS UNDERSTOOD.** Stage 3 is
> built because it is a link in the chain rather than a tune; the blade is not
> touched and `TUNED_RB` is still `None`.

> **DO NOT PROCEED TO THE BISECTION UNTIL THIS IS UNDERSTOOD.** Stage 3 is
> built because it is a link in the chain rather than a tune; the blade is not
> touched and `TUNED_RB` is still `None`.

> **AND THE RELIC IS ALREADY IN BAND, WHICH IS WHY THIS IS EASY TO MISS.**
> 47.0% sits comfortably inside `verify`'s 30-70%, and the roster spread went
> from 25.8pp at stage 1 to **20.7pp** at stage 2 — the relic stopped being the
> outlier. Every check in this repo is green about a relic that is ten points
> off the number its own design predicted. **This is open items 12 and 32's
> shape one step further out: the instrument cannot see it, and only the
> registered prediction could.**

> **THE FLOOR CAME IN FOUR POINTS UNDER THE LAB'S.** `wire_lab`'s floor arm —
> Grudgebearer standing in as a bloodsworn warhammer with its Crucible
> suppressed, against `sc-shroudmaul.html` — read **36.8%**. The built relic
> reads **32.7%**, and about 1.3pp of that is `verify` running a newly appended
> relic as side B in all 29 of its pairings. **~3 points are real** and they are
> the stand-in not being the relic.
>
> **THIS PUTS THE BRIEF'S BLADE PREDICTION IN QUESTION.** §7 says to start the
> bisection at 23.5 and *"expect the answer BELOW it"*. A lower floor means the
> ultimate has more room, not less, and the direction is now an open question
> rather than a registered expectation. **Do not carry the "downward" claim
> into stage 4 as if it had survived.**

---

# Open decisions

1. **THE CONSUME'S PER-STACK NUMBER**, and it is stage 3. 8 is the
   recommendation, linear at +0.73 win points a point. Settle it AFTER the
   bisection — `dmg` moves the blade and the Hemorrhage the consume eats, so it
   lowers the burst twice.
2. **THE TIP IS A FIRST CUT AND IT IS RICK'S.** Shipped:
   *"Wire ring holds the foe where it stands; the hammer comes around"*, 64
   characters. It says the hold and the arrival and it does not say the throw
   or (yet) the consume. `tip_audit` measures PIXELS, not characters, and it
   has not been run on this string.
3. **`spinMul` 6 IS A PICTURE CHOICE AND NOBODY HAS WATCHED IT.** The sweep is
   flat to noise from x2 to x12, so the number is free; 6 was taken because the
   registered prediction names it. x9 is the same shape louder. §8.6's strobe
   question — a desperate un-entangled Ravelbone at x9 turns at 18.7 rad/s,
   about three revolutions a second — is unanswered at either value.
4. **NOBODY HAS WATCHED ANY OF IT.** The ring, the cinch, the wire to the
   caught ball, and four voices are all first cuts. **The held ball with a
   moving weapon is a picture this game has never drawn**, and brief §9 says
   in as many words that if it reads as a frozen one the design is not on
   screen. Rule 2, and §4.0: film it before tuning it.
5. **THE COLLAPSE AGAINST A HELD BALL** is still completely unmeasured — brief
   §8.5, and the one thing in that document nobody priced.
6. **`crowdMul` IS UNSET**, as it is for Grasp, Deadfall and the Winnowing.
   Open item 15 for the fourth time.

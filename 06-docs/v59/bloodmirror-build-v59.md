# v59 — BLOODMIRROR AND BLOODLETTING, BUILT. The oldest design in the project, built at last — and by the time it was on screen Rick had changed the mechanic twice, so the relic that shipped is worth about **twice** the one that was priced. Every absolute number in `06-docs/v59/` is now on the other branch; the relative ones all survived.

**2026-09-01, Claude Code.** Built from `spectre-design-v59.md` and
`bloodmirror-build-brief-v59.md` (Cowork, 2026-09-01) in four links off
`sc-crossweave.html`. `bloodmirror_build.py`, `tipfix_build.py`,
`bloodletting_relic_probe.py`, `bloodletting_sheet.py`, `bloodmirror_sweep.py`,
all new.

```
02-chain/sc-tipfix.html        stage T — the four tip-surface changes
02-chain/sc-bloodmirror.html   stage 1 — the 32nd relic, ultimate STUBBED
02-chain/sc-bloodletting.html  stage 2 — BLOODLETTING
```

---

# 0. WHAT SHIPPED, AND FOUR THINGS IN IT ARE NOT IN THE DESIGN

```
BLOODMIRROR   bloodsworn x scythe, the THIRTY-SECOND relic (the brief says the
              thirtieth; it was written against a 29-relic tip and then spent a
              day in a chat transcript while Ravelbone and Gloamwire were built
              ahead of it)
BLOODLETTING  the scythe throws THREE bloody spectral copies of itself in a fan.
              They fly 0.55s, stick, DRIFT slowly on, and mill a 138 disc each
              for 4.5s — and WHILE ONE STANDS, Hemorrhage stacks to 8 instead
              of 4, for the blade too
```

**RICK CHANGED THE MECHANIC AFTER SEEING IT, TWICE, AND BOTH ARE HIS TO
CHANGE.** The design and the brief are written for ONE copy that STICKS IN
PLACE. What ships is three copies that drift. That is not drift in the build —
it is `06-docs/v59/`'s §1 being superseded by the person who wrote it, on the
strength of a rendered clip, which is CLAUDE.md §4.0 working exactly as
intended. It does mean:

> **Every absolute number in `spectre-design-v59.md` and
> `bloodmirror-build-brief-v59.md` is on the other branch.** The one-scalar law
> survives — `lift = +5.6 + 0.245 × spectre damage` — and three copies simply
> move the input to it. The ceiling numbers survive: a ceiling is a ceiling and
> the count is not on it. The blade does not survive at all.

Four things came off watching:

| | Rick, verbatim | what it changed |
|---|---|---|
| art | *"the grey triangle at the tip of bloodsworn scythe. lets get rid of it. everything else is great"* | `_scBarbed`'s tip hook deleted |
| art | *"go with the ring, and make the pool stronger"* | a landing ring; the pool's alphas roughly doubled |
| art | *"the scythe should rotate around its center axis. not the end of its handle"* + *"increase the rotational speed by a lot"* | centre pivot, `spinMul` 4 |
| **mechanic** | *"lets have it shoot out 3 copies of itself"* + *"a small amount of movement so they slowly continue to float"* | `n` 3, `spread` 0.34, `drift` 26 |

---

# 1. STAGE T — THE ONLY STAGE THAT CAN BE PROVEN INERT, WHICH IS WHY IT WENT FIRST

`tip-surface-v59.md`'s four changes. Two are in the build (curse's tip gains
*", stacks 3 times"*; `_tagFirst`'s box 596 → 760, Rick's width from a spread of
four) and two are in `tools/` (`verify`'s status cap 48 → 72; `tip_audit`
measuring the face the box is actually drawn in).

```
engine_ab   3720/3720 identical, all 31 relics
verify      12/13, the thirteenth the known Lightkeeper/Farwarden 76.3s
tip_audit   reproduces §1.1 within 3px on every status
```

`tip_audit` now **refuses to report at all** if `'Atkinson Hyperlegible Next'`
did not load, because a canvas that silently substitutes a face is this tool's
own historical failure in a new costume, and every number would look plausible.
Its budget is read out of the build (`_tagFirst`'s `const w = NNN * k` minus the
two 30px insets) rather than being the literal 536 it carried — which was
`596 − 60` written down by hand, and stage T moves the box.

## 1.1 AND THE BOX IS ALREADY BROKEN AT THE DELIVERY RESOLUTION

Not this change's defect, and this change makes it worse. `_tagFirst`'s box is
sized in DEVICE pixels and drawn in ARENA units — `k = 1 / this.scale` and
`this.scale = this.aw / 520` — so **it gets wider as the render gets smaller**:

```
aw (arena px)   box at 596      box at 760      A.w − w − 6
1080                287             366             148
 540                574             732            −218   <- the shorts format
 453                684             872            −358   <- the app at phone size
```

`clamp(v, a, b)` is `v < a ? a : v > b ? b : v`, so when `a > b` it returns `a`
and the box runs off the right edge rather than failing. **Nobody has ever
looked at a first-application pop-up at 540.** The builder prints this table on
every run. Open decision 1.

---

# 2. STAGE 1 — THE THIRTY-SECOND RELIC, AND ITS ART WAS OLDER THAN IT

`reach 104, width 11, artW 46, spin 3.2, mass 2.4, blades [0], mode "spin"` —
asserted against all five shipped scythes before a byte was written, because
every number in the design was measured on Thornwake's body and is only
transferable if the type really does own them. It does.

```
engine_ab   3720/3720 identical on the 31 (twice — once before the art change
            and once after it, which is v58's proof that `SHAPES` is
            render-only)
verify      11/13 with 32 relics — the band failure is the STUBBED relic and
            the brief says not to tune to it
```

**THE REGISTERED PREDICTION FOR THIS STAGE LANDED.** The brief: *"Bloodmirror
with no ultimate lands near 23% at blade 21."* Measured on a roster it was never
priced against, with two relics in it that did not exist when it was written:
**21.5%**.

## 2.1 THE ART, AND WHAT LOOKING AT IT EARLY ACTUALLY FOUND

Brief open decision 6 says look at the bloodsworn scythe early, because v57 puts
this cell at 59.0% from its nearest sibling — the closest pair on the row. That
is not what was wrong with it.

`SHAPES.scythe` has routed `bloodsworn` to `_scBarbed` since before the cell had
anything in it. Photographed beside sanctified at zoom, the flair was a **sixth
shape**: a grey triangle hung off the crescent's outer end point, reading as a
detached object rather than as part of the weapon — `_whEaten`'s fault on a
second row. Rick took it off and kept everything else.

**AND THE BARBS ARE ON THE WRONG SIDE OF THE BLADE, WHICH THE ENGINE ALREADY
KNEW.** `_scOuter`'s own comment, from a 2026-08-14 measurement nobody had acted
on:

> `q + n*eps` is INSIDE the shipped crescent at **1921 of 1921** interior
> samples. **0 of 37** call sites move toward the side their own comment names.
> ALL of them are inverted, not some.

`_scBarbed` says *"the blade cuts on the INSIDE of the curve, so the barbs go on
the OUTSIDE, where they drag on the way out."* They fan across the concave face
instead. The one-character fix moves six of the seven scythes — bloodsworn 3.16%
of the frame, umbral 6.96%, vigil 7.87%, runic 0.00% as the control that does
not call it. Rick was shown the shipped-against-flipped sheet for all seven
(`05-reference/v59/scythe-normal-flip.png`) and answered *"everything else is
great."*

> **THE INVERSION IS NOW A CHOSEN STATE ON THE SCYTHE ROW**, the way `_whBarbed`
> became one on the warhammer row. Do not re-raise it and do not "fix" it.

Removing a shape can only lose separation, and it did, slightly: the row's mean
IoU went 0.550 → 0.566. He took that trade with the picture in front of him.

---

# 3. STAGE 2 — THE CEILING IS THE MECHANIC, AND IT IS SCOPED SO THAT ITS FAILURE MODES ARE UNREACHABLE

Design §3.2 and brief §3.2 name three silent failures of a global
`STATUS.hemorrhage.maxStacks`: a Marrowdraw in the same fight inherits a window
it never cast; the cap is left at 8 for the NEXT match; it is restored on
`m.over` but not on a window merely expiring. *"Assert all three. The third is
the one a probe usually misses."*

**None of the three is reachable, and that is structural rather than checked
for.** `f.bleedCap` is a property of the fighter BEING BLED, and `tickSpectre`
**recomputes it from scratch on every frame** — both fighters, whether or not
anybody has cast anything — instead of raising it and restoring it. There is no
paired write to forget. A fighter's cap is a pure function of whether the other
fighter has a copy standing right now.

```
[5]  the global never moves                     0 frames off 4
[5b] no other bloodsworn relic ever sees it     8 matches of the other four,
                                                run BEFORE and AFTER two
                                                Bloodmirror matches: 0 frames
[5c] a fresh match starts at the status's own   0 fighters born wrong
[5d] and it comes down on a window EXPIRING     0 expiries left it up
```

`apply()` reads `this.bleedCap` for hemorrhage and `def.maxStacks` for
everything else. Since `bleedCap` is 4 on every fighter in every match with no
standing copy in it, that line is the identity it replaced everywhere else —
and `engine_ab` proves it rather than the comment asserting it: **3720/3720
identical on the 31 with the whole ultimate in the build.**

## 3.1 AND A FIGHTER ALREADY ABOVE THE CEILING IS NOT TRIMMED

Design §6.4 offered trim-instantly or leave-to-decay and called trimming *"the
version that looks like a bug"*. Left to decay — but the engine expires a status
**as a whole**, not a stack at a time, so "decay on its own 3.2s clock" means
the whole 8 goes at once 3.2s after the last application, and a quarry still
being hit keeps refreshing that clock. In practice this relic lands ~7.5 blows
across ~40s, so the gap is usually wider than 3.2s and the leak is bounded. It
is not what the design pictured. Open decision 2.

## 3.2 WHAT THE CEILING LOOKS LIKE, AND IT HAD NO REPRESENTATION AT ALL

Design §7c: *"the stack readout going past four is the only evidence on screen
that the ceiling moved."* `_stBleed` drew `Math.min(4, n)` drips — **eight
stacks looked exactly like four**, and no probe in this repo could have said so.
That is v54 §2c, the precedent that cost a build.

Two things carry it now: the drip count is clamped to the fighter's own ceiling
rather than to four, and the status tag prints the count while — and only while
— `bleedCap` is above the status default, for the BLADE's applications as well
as a copy's, because Rick's ruling is that the blade feeds the raised ceiling
and a number appearing on some applications and not others is worse than none.
Every other match in the game draws exactly what it drew before.

**AND THE ODD NUMBERS DO NOT EXIST.** §7c asks for the readout photographed at
5, 6, 7 and 8. Every application in this school is TWO — the copies' `bleed` and
the blade's `onHit:{hemorrhage:2}` — so a quarry goes 2, 4, 6, 8. 5 and 7 are
unreachable by arithmetic, not by luck. The sheet says so in its own output
rather than reporting them as missing panels.

---

# 4. THE FOUR PICTURE CHANGES, AND ALL FOUR CAME OFF A PERSON LOOKING

## 4.1 THE STICK DID NOT READ

§7c: *"if it does not read, the ultimate looks like a missed shot."*
Photographed off a real match, the landing frame was a thin red line arriving in
a busy frame with nothing marking the arrival. Every number was right.

A double ring now snaps out to the disc's edge over 0.22s. **A ring and not a
burst**, and that is a distinction rather than a preference: a burst says
something HIT, and nothing was hit — the copies land on empty floor. A ring says
*this is now a place*.

It is aged in `tickPresentation` and not in `tickSpectre`. The landing does not
set `hitStop` itself, but a blade blow on the same frame does, and a clock on
the normal path freezes for exactly the frames the viewer is staring hardest at
— Deadfall's blast, 96.2% of the time.

## 4.2 THE POOL WAS INVISIBLE IN TWO FRAMES OF THREE

Raised on Rick's word. **It costs the post chain nothing**, which is why it
could simply be turned up rather than redesigned: it is drawn in the WORLD pass,
not the emissive one, so none of it reaches the bloom and §4.1b's *"take away
AREA, not alpha"* does not apply in either direction. It gained a soft
continuous rim so the extent is a readable edge — deliberately not dashed,
because `garrote_sheet` photographed one of those reading as a range indicator,
which is the one thing a hazard must not look like.

## 4.3 IT ORBITED AN INVISIBLE BALL

Rick: *"the scythe should rotate around its center axis. not the end of its
handle."* It was drawn the way a HELD weapon is — pivot at the ball's centre,
weapon offset `R − 6` along the radius — so the handle end traced a circle.

**AND THAT PIVOT WAS DOING A SECOND JOB NOBODY HAD NOTICED.** At `R − 6` the tip
swept exactly `R + reach` = 138 = the disc, so the drawn sweep and the hit box
were the same circle *for free*. Centred, the sweep is `artScale × 0.555 × L`,
and only `artScale` **2.26** puts the tip back on the rim. Rick was shown both
and took 2.26. The builder prints both numbers on every run:

```
sweep 138.0 at artScale 2.26 (100% of the disc)   the blade fills it
      artScale 2.26 is the one that puts the tip back on the rim
```

A picture claiming a smaller hazard than the one that exists is the hardest kind
of bug in this repo to see, because both halves stay internally consistent.

`spinMul` 4 (12.8 rad/s) is his too: at the weapon's own 3.2 an unheld object
reads as drifting rather than milling — a held weapon gets its sense of speed
from the ball swinging it, and these have no ball.

## 4.4 AND THEN THERE WERE THREE

`n` 3 in a fan of ±0.34 rad, `drift` 26 px/s along each copy's own fired
bearing. **This is a mechanic change and it is priced nowhere.** The design's
own arms table has *"two spectres, half life"* at +16.2 against the centre's
+11.2 — inside the noise — and nothing anywhere prices three at FULL life.

Each copy is its own hazard with its own cooldown, so a quarry in an overlap is
bitten by each. That is the plain reading of "three copies of itself" and the
only one that needs no rule written for it, and it is measured:

```
65.5% of all ticks landed on a quarry standing in more than one disc
```

Breach's `spent` is one payment per firing precisely because sweeping several
bodies with one hazard is either a shield or a multiplier. Here the multiplier
is deliberate and the blade is what pays for it. Open decision 3.

---

# 5. THE REGISTERED PREDICTION, REFUTED — AND THE DECOMPOSITION IS THE FINDING

Brief §9: *"the built relic delivers **10.5–11.0 ticks a fight**."*

```
                         ONE copy      THREE copies (shipped)
ticks a fight              13.12               23.42
  casts a fight             1.93                1.75
  ticks a cast              6.81               13.38
  in-flight ticks          16.5%               21.7%
  overlap ticks               —                65.5%
spectre damage a fight      39.4                70.2
```

**Even at one copy it was out of band**, by +22%, and the excess is
attributable: 16.5% of ticks land while the copy is still in the air. `hitFly`
is `true` because the brief's own §2 table says so, and `spectre_lab.py`'s
default is `hitFly=True` as well — so the 10.5–11.0 was not measured on a
no-fly arm and the gap is somewhere else. The most likely remainder is that the
prediction was derived for MEDIUM's `life 4.5` from a lab whose centre ran
`life 6.0`, and nobody can now check that without re-running the lab.

At three copies it is 2.2× the band. Under the design's own law that is roughly
**+9.4pp of lift** over what was priced, and the blade absorbs it.

**The band was NOT moved to make the check pass.** It is registered to be
falsified and it was.

---

# 6. THE BLADE

`bloodmirror_sweep.py`. **There is no bisection in it**, deliberately: CLAUDE.md
says twice that a bisection converges on the noise in its tail, and the second
time it cost a whole damage point.

```
[0] THE CURVE — 248 fights a point, side A, with three copies

      dmg     win     dur
     3.00   31.5%    44.8
     5.00   31.5%    44.1
     7.00   41.5%    43.8
     9.00   49.2%    43.0
    12.00   63.3%    41.6
    16.00   70.2%    39.9
    21.00   77.4%    37.8      <- what stage 2 shipped at

    monotone: YES     the 40-60% region is dmg 7 to 9
```

**The bottom of the curve is FLAT** — 31.5% at both dmg 3 and 5 — which is this
relic saying that with a near-zero blade it is entirely its ultimate. The brief
expected the answer in 20–22 and the one-copy build crossed at about 16; three
copies put it near **9**.

The wide direct measurement — three points, both sides, two seed blocks,
1054 fights a point a side a block — is in `bloodmirror-blade.json`.

---

# 7. THE PROBE, AND IT WAS WRONG FIVE TIMES BEFORE THE BUILD WAS

`bloodletting_relic_probe.py`, one check per sentence of §4, plus `[P]` calling
`drawSpectre` against a live 2D context with a copy in the air, one standing and
one dissolving. **24/25**, the one failure being §5's registered prediction.

Five of its own defects, and three are the same defect:

1. **[1c] measured a duration against `m.t`** and reported 24 of 24 landings
   "off the clock". `step()` returns early for as long as `hitStop` runs, so the
   copy's own clock stops while the match's does not, and **every impact in this
   engine opens with a freeze**. Fixed by reading `S.t`.
2. **[8] counted frames on which the match was over and a copy still existed**,
   which is not a tick — and reported 6 violations, every one of them a tick
   that KILLED, because the state after the step is the state the tick created.
   Counted in the hook now, with the state as it was.
3. **[8] also counted "a tick on a corpse"** the same way, for the same reason.
4. **[2] expected the copies to drift on frozen frames** — 5,501 phantom
   unexplained frames, all hit stops.
5. **[1c] bounded the throw at exactly `flight × speed`** when a copy's clock
   can overrun by one step.

> **A CHECK THAT COUNTS FRAMES IN WHICH AN EVENT IS POSSIBLE IS NOT COUNTING THE
> EVENT.** Five times in one file in v60, twice in v56, and three more times
> here. It is the default failure mode of a probe on an engine whose every
> impact opens with a freeze.

---

# 8. TWO THINGS FOUND ON THE WAY THAT BELONG TO OTHER RELICS

**THE LAST TWO RELICS SHIPPED WITH NO PARTICLE FIELD.** `SPECS` carries 29
entries in both `src/render/fx.js` and the inlined copy, and neither has
`ravelbone` or `gloamwire`. `ULTFX.sync` returns on a missing spec — it is not
an error, which is exactly why it ships. CLAUDE.md predicted this precisely when
the 26th spec went in: *"an ultimate with no field among twenty-five that have
one is a picture fault with no number attached to it."* Bloodmirror's spec is in
both copies and the builder refuses to write unless the two tables are byte
identical afterwards. Open decision 4.

**AND `_stBleed`'s CLAMP WAS A LATENT BUG THAT ONLY THIS RELIC COULD EXPOSE.**
`Math.min(4, n)` was correct for every fight ever played on this engine and
wrong the instant something could exceed four.

---

# 9. GATES

```
stage T   engine_ab 3720/3720 · verify 12/13 · tip_audit §1.1 · chain_audit 2/2
stage 1   engine_ab 3720/3720 (x2) · verify 11/13 (both expected) · floor 21.5%
          against a registered ~23%
stage 2   engine_ab 3720/3720 · bloodletting_relic_probe 24/25 · chain_audit
          14/14 · four voices rendered and audible, longest burst 0.55s
FILM      07-shorts/v59/bloodletting-first-cut.mp4 — watched, and it produced
          four changes
```

---

# Open decisions — Rick's

1. **`_tagFirst`'s BOX OVERFLOWS AT THE DELIVERY RESOLUTION AND ALWAYS HAS.**
   §1.1. At 540 wide the box is 574 arena units in a 520-unit hall *at the old
   width*, and stage T makes it 732. The clamp degenerates silently. Nobody has
   photographed a first-application pop-up at anything but 1080. It is not this
   change's defect and this change makes it worse.

2. **STACKS ABOVE FOUR DO NOT DECAY ONE AT A TIME.** §3.1. The design's
   placeholder pictured a gentle run-down; the engine expires a status as a
   whole, and a quarry still being hit keeps refreshing the clock at 8. Bounded
   in practice, and not what was pictured.

3. **THE OVERLAP IS AN UNPRICED MULTIPLIER.** §4.4. 65.5% of ticks are paid more
   than once. The alternatives are one payment per volley (Breach's `spent`) or
   a shared cooldown across the three copies, and both are a different relic.
   The blade currently absorbs it.

4. **RAVELBONE AND GLOAMWIRE HAVE NO PARTICLE FIELD.** §8. Two relics, silent,
   and the fix is one spec each in two files.

5. **NOBODY HAS WATCHED THE THREE-COPY BUILD.** The first cut was one copy. The
   ring, the pool, the centre-axis spin and the three copies have been
   photographed (`05-reference/v59/bloodletting-states-*.png`) and only the
   one-copy version has been rendered as a fight. §4.0, and every round of
   looking so far has moved something no probe had a number for.

6. **THE BLADE IS NEAR 9 AND THE RELIC IS NOW MOSTLY ITS ULTIMATE.** §6. At dmg
   3–5 it still wins 31.5%. That is a legitimate relic — Thornshear and
   Twinshade are both shaped that way — and it is a choice about what a fight
   with this relic looks like, which design §5 says is Rick's rather than the
   bisection's.

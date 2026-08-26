# v38 — THE BLOODSWORN FLAIL, AND THE SPIKE STORM. §1 FIRST.

**2026-08-20.** Rick, having held the axe and the staff back until the current
six types are filled: **the bloodsworn × flail cell.** The twentieth relic.

The look-first probe ran before any of this and is written up separately
(`-bloodsworn-flail-look-v38`). What it found that bears on the design: the
cell's art already exists and has never been reachable; hemorrhage holds ≥2
stacks for only 41% of a fight on this type against 52% and 59% for the
school's other two relics; and the cause is the status CLOCK, not the chain.

---

# 1. THE DESIGN, IN RICK'S WORDS

    "red flails ult

     the flail head begins to spin around the chain super fast (think about a
     person spinning a flail as hard as they can) then when it reaches full
     speed the flail shoots razor sharp spikes in a nova in every direction for
     several seconds. volies not 1 shot. the spikes dont bounce but expire when
     they hit anything. the spikes also apply bleed on each hit."

    "slight change to that. the spikes should shoot off in a clockwise fashion
     going around the flail head. several per second over the duration"

And on the weapon itself:

    "the tips of the flail are red dots. can we change those to red razor sharp
     points? fits the bloody theme better imo"

    "flail head looks good but lets shorten those spikes a bit."

Interview answers: the caster **keeps fighting throughout** — it moves and the
head still deals contact damage during both phases · the wind-up is broken by a
**stun budget** · **40 spikes a second** · the sweep follows **the head's real
speed**, 15 rad/s.

## Three readings of the prose that are load-bearing

- **"then when it reaches full speed"** — a PHYSICAL trigger, not a timer.
  `f.headAngVel` is the head's angular speed and `CONFIG.chain.maxAngVel` is
  literally 15. Releasing at that ceiling means the viewer watches the
  condition arrive. Reprisal is the precedent: "the bow fires when its facing
  comes round." It also makes the telegraph **free** — the head visibly
  spinning up IS the charge meter, the same virtue Ward's plate brightness has,
  and no second HUD element is needed.

- **"the spikes dont bounce but expire when they hit anything"** — this is the
  engine's DEFAULT and it is an argued default, not an accident. From
  `tickShots`: *"the wall. An arrow is spent on it: a ricocheting arrow is chaos
  the viewer cannot attribute to anything."* Ironbloom's `shardBounce: 3` is the
  exception. **The projectile half of this ultimate costs nothing to build.**

- **"clockwise"** — CANNOT be a fixed screen direction, and this is a
  correctness problem rather than a taste one. `this.spinDir = side === 0 ? 1 : -1`,
  so the relic spins one way as fighter a and the other as fighter b; and lines
  5906–07 flip `spinDir` on clank outcomes, so it reverses mid-fight. A
  hardcoded clockwise sweep would run backwards out of the spin in half of all
  matches and visibly reverse relative to the head. **The spray follows the
  head's own rotation, always.**

---

# 2. WHAT IT IS, MECHANICALLY

```
PHASE 1   WIND-UP. The ult drives the head's angular velocity toward
          CONFIG.chain.maxAngVel (15 rad/s) from a cruise of ~2.2. Release
          fires when the head ACTUALLY REACHES the threshold — an emergent
          duration, not a constant.
          The caster is NOT interrupted: it moves, and the head still deals
          contact damage. Rick's answer, and the same one Triplicate got.
          BROKEN BY A STUN BUDGET — §3.

PHASE 2   THE SPRAY. Razor spikes at 40 a second for the duration. The
          emission angle IS the head's angle, so at 15 rad/s the arm turns
          2.39 times a second and consecutive spikes are 21 degrees apart.
          Spikes: no bounce, spent on anything — wall, foe, or a spinning
          weapon that parries them. Each applies hemorrhage on hit.
```

## Why the rate had to be chosen and could not be defaulted

The sweep is only VISIBLE when spikes leave faster than the head turns past
them. Schematic, real arena, spikes spent on the wall:

```
  rate    degrees between spikes   what it reads as
   6/s            143              a slow scattergun. no pattern at all.
  14/s             61              a dotted arm; you cannot read its direction.
  24/s             36              a rotating pinwheel.
  40/s             21              a solid rotating blade of spikes.   <-- taken
```

**"Follow the head exactly" at 6 a second destroys the effect Rick asked for.**
The two knobs are not independent and the first draft of this document treated
them as if they were.

`CONFIG.shot.maxLive` is 64 and the overflow path is `this.shots.shift()` —
it drops the OLDEST silently. At 40/s with spikes slow enough to fill the hall,
peak live is ~48 in the schematic. **That is under the cap and not by much, and
the foe's own shots share the array.** Measure the overflow on the real build
before believing any of it.

## What this ultimate is FOR, and it was not designed for the reason it works

The look-first probe measured the relic's actual hole: at one contact every
~6.6 seconds against a 3.2-second bleed window, the foe is clean more often
than it is bleeding — ≥2 stacks for 41% of the fight against 52% (twinblade)
and 59% (greatsword). Hemorrhage caps at 4 stacks, so what a spike storm buys
is not DEPTH, it is **uptime at the cap**, which is precisely what the chain
cannot produce on its own. Rick designed this before seeing those numbers.

---

# 3. THE INTERRUPT, AND THE MEASUREMENT THAT CHANGED THE ANSWER

The first answer given was "can be broken — the cast is lost". Measured before
building it, 80 matches, 2,461 seconds:

```
  0.745 hitstun events a second taken — 22.9 a match
  stunned for 19.1% of all frames
  gaps between stuns: median 0.63s   p25 0.23s   p75 1.75s

  a wind-up that must go UNINTERRUPTED, from a random moment:
    0.4s -> 75%    1.0s -> 53%    1.6s -> 38%
    0.6s -> 66%    1.2s -> 47%    2.0s -> 30%
```

**`takeHitstun` runs on every blow landed from anything.** Hex is not special,
it is only more of it. And `drive = f.stun > 0 ? 0 : spin * f.spinDir` already
stops the head being driven while stunned — that behaviour is free and exists
today. So "broken by a hex" wired to `stun > 0` silently becomes "broken by
anything", and **roughly half of all casts would do nothing.** The Harrowing's
dud rate that this project went back and fixed was 11.5%.

Those figures are a CEILING, and the honest caveat is that they flatter the
design: they assume a cast begins at a moment unrelated to the fighting, and a
charge bar fills BECAUSE of an exchange, so real casts start in busier weather.

**Rick's answer: a stun budget.** The cast survives some accumulated stunned
time inside the wind-up and breaks past it. Generic, tunable to any dud rate,
and it costs the one thing worth recording: **a viewer cannot see why one cast
broke and another did not.** That is a real legibility debt on a relic whose
whole telegraph is otherwise visible, and it should be paid with presentation —
the spin-up visibly losing speed, and something that reads as "the wind is
going out of it" — rather than left as hidden state.

**The budget is not a number yet, and it cannot be derived from the table
above.** Stun stops the drive, so being stunned LENGTHENS the wind-up, which
exposes it to more stun: a feedback loop, not a fixed window. The dud rate has
to be measured on a real implementation and the budget swept against it. That
is the first instrument of the build, not an afterthought.

---

# 4. THE ART — WHAT SHIPPED BEFORE ANY OF THIS

`SHAPES._fhBarbed`'s seven tips were filled `p.core` circles at radius `0.13r`
centred `0.08r` INSIDE the barb's own vertex, so they spanned 1.73r–1.99r
against a barb terminating at 1.94r. **The dot was not decorating the point, it
was blunting a point that was already there.** Removing it is most of the fix.

The replacement is v37 §8.3 applied again — *"the taper is most of what makes
it read, and no stroke has one"*:

- a FILLED path, never a stroke; a stroke has a cap and a cap is a blunt end
- edges CONCAVE. Convex reads as a thorn, straight as a triangle, concave as
  honed.
- the point continues the barb's OWN TANGENT at the vertex (`P1 - C1` for a
  quadratic), which is 1.07 rad off radial. These barbs hook hard, and a point
  that ignored that would read as a spike glued onto a hook rather than a hook
  that has been sharpened.
- a second needle sharing the apex in `p.glow`, as the light on the edge.
  Candidate E was the control and the highlight earns its place — without it
  the red reads as a dull smear at 1:1.

Length was laddered at 1:1 after Rick asked for shorter: 0.42 / 0.36 / 0.30 /
0.24 / 0.18. **0.30 taken** — still a real point, and the red stops dominating
the silhouette. Below 0.24 it stops being a spike and becomes a red cap, which
is the shipped dot's failure with extra steps.

**And the tip is now load-bearing twice over.** The relic throws razor spikes;
the spikes it throws should be the barbs it wears. One path function, used for
the tip and for the projectile — share the routine, bespoke nothing, because
here they are genuinely the same object.

---

# 5. THE CHAIN LENGTH QUESTION, ANSWERED AND CLOSED

Rick: *"can we also try making ALL flails have slightly longer chains? what does
that do to balance?"*

`CONFIG.chain.hilt` swept 0.50 → 0.30 — chain 48 → 67 out of reach 96, a 40%
change. Full 171-pairing grid, n=24, with a control confirming the 136
non-flail pairings are bit-identical at every value:

```
 hilt  chain   GRAVE   SLAG  spread    dur  clank   hits   t/o
 0.50   48.0   48.6%  52.5%   20.1pp   31.9    8.1   14.8     0
 0.46   51.8   50.0%  50.5%   20.4pp   32.3    8.2   14.8     0  <- shipped
 0.42   55.7   51.9%  48.6%   21.3pp   32.4    8.1   14.8     0
 0.38   59.5   52.5%  54.9%   20.8pp   32.1    8.2   14.9     0
 0.34   63.4   50.7%  51.6%   20.6pp   32.4    8.3   14.9     0
 0.30   67.2   48.1%  52.1%   21.8pp   32.1    8.2   14.8     0
```

**No detectable balance effect.** Both flails wander ±2–3pp with no direction,
inside the noise at this sample size; duration, clanks, hits and timeouts are
flat and there are no timeouts anywhere.

**And the picture does not move either, which is the more useful half.** Mean
head-to-ball distance runs 84.8 → 86.4px across the whole sweep — 1.6 pixels.
The extension curve is why: `target = chainLen * (0.44 + 0.56*swing)`, and at
speed `swing ≈ 1`, so the chain is thrown taut 83–88% of the time whatever its
length. **A longer chain is a longer TAUT chain.**

It also runs the opposite way from intuition. Angular lag falls 0.56 → 0.41 rad
as the chain lengthens, because gravity's term is `sag / max(1, headR)` —
divided by the live chain length. **A longer chain sags less and looks
STIFFER.** The build's own comment predicts this and it took the table to
believe it.

`hilt` is therefore the wrong knob for the thing Rick was reaching for. `sag`
(1.1), `spring` (26), `damp` (0.9955) and the `0.44` extension floor are the
ones that control droop, overshoot and slack, and none has ever been swept.

---

# Open decisions

1. **THE STUN BUDGET IS UNSET AND CANNOT BE GUESSED.** §3. First instrument of
   the build; sweep it against a measured dud rate and pick a target. What IS
   the target? The Harrowing settled at 11.5% and that was judged too high.
2. **The budget is invisible.** §3. What does a wind-up losing its wind look
   like? Nothing in the game currently shows a cast degrading.
3. **THE NAMES.** Both are unset. The relic and the ultimate.
4. **`onHit` stacks a hit.** Both shipped bloodsworn relics apply 2. On a type
   that contacts every 6.6s, 2 gave the 41% figure. 3 or 4 caps the foe on a
   single contact and makes the ladder 4-or-nothing.
5. **`dmg` is unset and MUST be swept**, not derived. v37 §6 found the twinblade
   knob eight times more sensitive than Lastlight's because lifesteal compounded
   it; nothing here compounds, but nothing here has been measured either.
6. **Spike damage, spike speed, duration, and stacks per spike — all unset.**
   40/s over several seconds is a lot of hits; each one routes through
   `resolveHit` with crit, jitter and the sunder multiplier.
7. **`maxLive` overflow is unmeasured at 40/s.** §2.
8. **Does the spray count as this relic's contact rate?** The look-first probe
   found the four "many small objects" ultimates inflate their relic's measured
   hits/s by +0.04–0.08. This will be the fifth and the largest. Every
   type-level number involving it must be taken with `--noult`.
9. **Still open from v37:** `01-live` is on sixteen relics against nineteen —
   twenty once this lands.

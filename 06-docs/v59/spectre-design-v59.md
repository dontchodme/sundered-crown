# v59 — THE 30th RELIC, bloodsworn x scythe, and RICK'S §1 PRICED. The sentence says "hits rapidly applying bleed" and the game forbids it: Hemorrhage caps at four stacks, so a spectre ticking five times a second saturates the ceiling in under a second and everything after is upkeep. Turning the bleed on is worth z = -0.93 under that ceiling and z = +2.67 above it — the same comparison, twice, with only the cap changed. That is the design.

**2026-09-01, Cowork.** `spectre_lab.py` (25 arms), `paired_bleed.py`,
`bleed_cap.py`, `cap_window.py`, `knock_check.py`, `blade_sweep.py` and
`compose_sweep.py`, all new, all runtime-only, against
`02-chain/sc-nightfell.html`. Chromium **141.0.7390.37**, identical to the v57
session. Nothing is written to any build.

**Thornwake stands in** — same shape, mass, reach and 5.24s contact gap. Its
entangle is replaced with hemorrhage at bloodsworn's own weight (2 a hit) and
Bramblesnare is stripped to a bare cast, so the only thing the ultimate does is
Rick's §1. **The 26 other relics keep their own ultimates**: this is the real
field, not `row_price`'s ultimates-off world (`budget-v59.md` §4.1).

**Every headline below is PAIRED** on (foe, seed) at 520 fights and reported
with its z. The unpaired sweep that opened the session could not separate the
bleed from the tick damage at 260 fights, and reading it as an answer rather
than as noise would have got the whole design backwards.

```
THE CELL      bloodsworn x scythe. Bleed is the strongest foe channel available
              on this weapon — +10.0pp against curse's +3.9 and sunder's +4.7,
              beaten only by a shield that is already Vesper's
THE ULTIMATE  the scythe throws a bloody spectral copy of itself. It flies a
              short way, sticks, and mills — and while it stands, Hemorrhage
              stacks past four
```

---

# 0. RICK'S §1, AND THE FOUR RULINGS ON IT

> *the scythe throws out a bloody spectral copy of itself. the copy flies a
> short duration and then sticks in place. rotating around its center axis and
> dealing damage to any enemy in its area. the spectral scythe deals reduced
> damage but hits rapidly applying bleed.*

```
RULED   the ultimate RAISES THE BLEED CEILING while it stands — cap 4 -> 8,
        for the blade too, not only the spectre                        §3
HIS     from four ways of breaking the cap, over a second pool, a
        school-wide change, and leaving it alone
OPEN    knockback — measured, real, not in his sentence                §4.2
OPEN    what the relic is made of — the blade follows from it          §5
```

---

# 1. THE WHOLE ULTIMATE IS ONE NUMBER

23 arms, lift regressed on the damage the spectre delivers in a fight:

```
lift = +5.6 + 0.245 x spectreDamage      r2 = 0.80
residual sd 2.9pp against a per-arm SE of 3.1pp
```

**The residuals are smaller than the measurement error**, which is the same
result GRASP had on held seconds and it buys the same thing: tick rate, damage
a tick, disc radius, how long it stands and how far it throws are **five ways
of writing one quantity**, so once the total is set *the arrangement is free
and every remaining choice can be made for the picture.*

```
arm                    spectre dmg    lift          arm              spectre dmg   lift
tick 0.90s                    12     +6.5           radius 104              31    +10.0
tick 0.55s                    19     +7.7           radius 172              64    +21.9
dmg 2 a tick                  24    +11.5           radius 206              81    +28.8
life 3s                       29    +13.5           life 9s                 60    +21.9
THE CENTRE                    47    +11.2           life 13s                74    +26.2
flight 0.2s                   48    +20.0           tick 0.12s              77    +25.4
two spectres, half life       54    +16.2           dmg 9 a tick            94    +25.4
```

Three things that are therefore **free** and should be chosen by eye:

- **Whether it bites while flying.** +12.7 against +11.2, inside the noise.
- **One spectre or two at half the life.** +16.2 against +11.2, inside the noise.
- **The tick rate itself**, at a fixed total. The rate is the picture.

And one that is **not** free: **the disc is 138 and it is not a knob.** "A copy
of itself" fixes it — the ball is 34 and the scythe reaches 104. 104 reads
+10.0 and 206 reads +28.8, so if this relic ever needs to be stronger the
radius is the lever that shows on screen; it is also the one that would make
the ultimate stop being a copy of the weapon.

**A long throw costs it.** Flight 1.1s halves the time the foe spends inside
(13.1% against 26.1%) because the spectre spends its life in transit rather
than standing. Throw it a short way.

---

# 2. THE CENTRE, AND THE FLOOR

```
this relic with no ultimate at all            48.8%
a bare cast that does nothing                 50.0%     +1.2   noise
the centre  (disc 138, tick 0.22, 4 a tick,
             bleed 1, life 6.0, flight 0.55)  60.0%    +11.2
```

---

# 3. THE CEILING IS THE DESIGN

## 3.1 THE BLEED HALF OF THE §1 DOES NOTHING, AND THE REASON IS A CONSTANT

Paired against the same spectre with its bleed deleted, 520 fights:

```
adding 1 Hemorrhage a tick        -2.5pp   discordant 197 (92/105)   z = -0.93
adding 2 Hemorrhage a tick        +0.8pp   discordant 194 (99/95)    z = +0.29
```

**Nothing, twice.** `STATUS.hemorrhage` is `{ maxStacks: 4, dur: 3.2, dps: 1.5 }`
— a hard ceiling of **6 damage a second**. A spectre ticking every 0.22s
reaches four stacks in under a second and every application after that only
refreshes a clock. The relic's own blade already applies 2 a hit.

> **Rick's sentence describes a mechanic the game currently forbids.** Not a
> weak one — a forbidden one. "Rapidly" is exactly the word the cap deletes.

The control that proves it is a ceiling and not indifference: the same spectre
with **no direct damage at all**, bleeding only, is worth +8.6 over the floor.
The bleed does work. It just cannot do any more of it.

## 3.2 MOVE THE CEILING AND THE SAME COMPARISON INVERTS

The clean test is **"does having bleed at all beat having none"**, run at each
ceiling against an otherwise identical spectre, paired at 520 fights:

```
                                              vs the same spectre with NO bleed        z
cap 4, applying 1 a tick                                 -2.5pp                     -0.93
cap 4, applying 2 a tick                                 +0.8pp                     +0.29
cap 8, applying 1 a tick                                 +6.9pp                     +2.67
```

**Same comparison, two ceilings, opposite answers.** And once the ceiling is up
the escalation keeps paying, where under it the same escalation bought nothing —
paired against cap 8 at 1 a tick:

```
2 a tick    +4.0pp   discordant  69 (45/24)   z +2.53
3 a tick    +5.2pp   discordant  77 (52/25)   z +3.08
```

> **A correction, kept because the shape of the mistake is worth more than the
> number.** The first version of this section read *"doubling the bleed at cap 8
> is +11.9pp, z +5.57"*, and that arm was **cap 8 AND bleed 2 measured against
> the centre — cap 4 and bleed 1.** It was the ceiling and the doubling
> together, quoted as the doubling. v58 §1.1 is a whole section on not quoting
> one instrument as another and this document did it two hours later. The
> head-to-head runs above are what replaced it, and the claim survived at a
> third of the size.

## 3.3 THE FOUR WAYS TO BREAK IT, AND RICK'S

```
cap raised for the WHOLE FIGHT      +9.4pp   z +4.74    what was measured first
cap raised WHILE IT STANDS          +7.9pp   z +4.35    <- RICK'S
cap 12 while it stands              +9.0pp   z +4.82
```

Rick's window-scoped version delivers **84% of the whole-fight version**, and
that gap is the reason it was measured rather than assumed: the first number in
front of him was +9.4 for something that returns +7.9.

He took it over a separate uncapped pool for the spectre, over moving
`STATUS.hemorrhage.maxStacks` for the whole school, and over leaving the
ceiling alone. **The blade feeds it too** — that is his ruling, and it is what
makes the window read as the fighter opening up rather than as an object
landing.

## 3.4 AND IT IS WHAT SEPARATES THIS RELIC FROM HARROWING

Lastlight is sanctified x scythe — the same weapon, and `smite` is **byte
identical to `hemorrhage`** apart from its name (`budget-v59.md` §4.2). Its
ultimate *"sprays scythes that stick and bite, then burst"*. Both designs are a
scythe that leaves the wielder and stops.

```
HARROWING   TWELVE, small, stuck to the BODY, burdening it, ONE burst
THE SPECTRE ONE, large, anchored in the HALL, milling, and it takes the quarry
            to a stack count nothing else in the game can reach
```

**Without §3 the separation is a sprite. With it, the two relics do different
things to the same status.**

---

# 4. THE TWO FORKS

## 4.1 IT MUST NOT CUT THE CASTER — AND THIS IS NOT A BALANCE TERM

```
the spectre mills both balls     -16.5pp   discordant 204 (59/145)   z = -6.02
```

That is **below the no-ultimate floor**: 47.1% against 48.8%. A scythe has to
fight near what it left behind, so a shared hazard is a self-inflicted wound
for the whole window. Same answer Breach gave at v57 §4.7 (+28.5% to +3.8%),
found independently, and six standard errors is not a number to tune against.
**Foe only.**

## 4.2 KNOCKBACK IS REAL, THE AMOUNT IS NOT

```
knock 60      +6.3pp   z +2.35
knock 120     +7.9pp   z +2.98
knock 240     +6.3pp   z +2.32
```

Flat across a 4x range, so **any** knockback buys about seven points and no
particular amount buys more. And it is not buying time in the disc — ticks fall
from 11.7 to 10.9 and dwell from 26.1% to 23.1% when the foe is shoved. The
value is somewhere else: a second thing in the hall interrupting the other
ball's rhythm.

**It is not in the §1.** If it is taken, take the smallest — 60 buys what 240
buys and pushes the quarry out of the caster's own reach less.

---

# 5. WHAT THE RELIC IS MADE OF

The recommended build reads **75.8% at Thornwake's own 31.35**, so the blade
comes down a long way and the question v57 §3.5 asked about Cindercleave asks
itself again here: the count does not decide the relic's strength — the
bisection does — it decides **what the relic is made of.**

```
recommended build, blade swept, 364 fights an arm
  blade        31.35   28.00   25.00   22.00   19.00   16.00
  with it      75.8%   73.6%   68.1%   68.4%   60.2%   48.4%
  without it   48.9%   40.7%   29.1%   28.0%   15.1%    6.6%
```

**At a blade near 16 the ultimate is worth about 42 points** — which would be
the SECOND largest ultimate share in the game, just under Twinshade's Triplicate
at +44.7 and clear of Vesper's Sentinel at +40.9. That is a legitimate relic and
it is also a choice: this fighter would be an ultimate with a scythe attached.

The composition table in §5.1 is the alternative, and the decision is Rick's.

## 5.1 THREE COMPOSITIONS, AND THE BLADE FOLLOWS FROM THE CHOICE

`compose_sweep.py`, 364 fights an arm, the blade swept under each:

```
                                              16      19      22      25      28    lands 50% at
FULL    4 a tick · life 6.0 · knock 60     48.4%   60.2%   68.4%   68.1%   73.6%        ~16
MEDIUM  3 a tick · life 4.5 · no knock     32.7%   44.0%   51.9%   63.7%   68.4%        ~21.5
LIGHT   2 a tick · life 3.5 · tick 0.30    25.8%   36.5%   39.3%   51.4%   58.0%        ~24.5
no ultimate at all                          6.6%   15.1%   28.0%   29.1%   40.7%
```

What each one IS, at its own bisected blade — the ultimate's share of the
finished relic, against a roster that runs +2.9 (Reprisal) to +44.7
(Triplicate), mean +20.1:

```
FULL     blade ~16    ultimate worth ~42 points    the lightest scythe in the
                                                   game and the second most
                                                   ultimate-heavy relic in it
MEDIUM   blade ~21.5  ultimate worth ~24 points    Cindercleave's neighbourhood
LIGHT    blade ~24.5  ultimate worth ~22 points    Foregone's neighbourhood — a
                                                   heavy scythe with an accent
```

**All three land in the same place and none of them is stronger than the
others.** The choice is what a fight with this relic looks like: a light blade
that waits for its window, or a scythe that already hits hard and gets a good
window on top.

---

# 6. THE TRAPS

**6.1 THE SPECTRE HANGS OFF THE FIGHTER OR THE MATCH, NEVER OFF `m.ultFx`.**
v54 §2a, chain-wide: `m.ultFx` is one slot and the opponent casting anything
overwrites it. Deadfall survived only by being rebuilt onto `f.ultDeadfall` and
Breach was told to start on `f.ultBreach`. **The spectre outlives nothing and
owns nothing else** — one object, per-fighter, `f.ultSpectre`.

**6.2 DO NOT BUILD IT ON `shots`.** v57 §4.6, the same reasoning: `spawnShot`
shifts the oldest live entry out at `maxLive` 64, and `tickShots` lets
`bladeSegments` **parry** a shot with melee's defence winning ties. A spectral
scythe that the quarry can parry is a different mechanic and nobody has decided
it is this one.

**6.3 THE CEILING MUST COME BACK DOWN, AND `maxStacks` IS GLOBAL.**
`AC.STATUS.hemorrhage.maxStacks` is one number shared by every fighter in the
match and by the four other bloodsworn relics in the field. The lab moves it
and restores it per match, and asserts it is 4 on the way out. **A build must
scope it** — per-fighter, the way v53 scoped the curse pool — or a Marrowdraw
in the same fight inherits the window. Write the assertion before the feature.

**6.4 AND DECIDE WHAT HAPPENS TO STACKS ABOVE 4 WHEN THE WINDOW CLOSES.** They
can be trimmed instantly, or left to decay on their own 3.2s clock. Not
measured, cheap to measure, and it is visible on screen either way. Placeholder:
leave them; a window that reaches into the seconds after it closes is what a
bleed should do.

**6.5 NO TICK ON A CORPSE, NONE AFTER `m.over`, NONE DURING `m.hitStop`.**
The sim is frozen during hit-stop and so is the hall — v57 §4.5. The lab does
this and it is not free: a spectre that keeps milling through hit-stop gets
extra ticks for nothing.

**6.6 THE BEAT.** Rule 3, eleventh relic running. v53 §4: 30 of 58 Gravemourn
kills rendered a clip with no killing blow because a hand filed `kind:"ult"`
and `cinema_clip` finds the finish with `plan.find(c => c.fatal)`. **The
spectre deals damage and can therefore kill, so it MUST be able to file a fatal
beat.** The cast files a beat, the landing files its own, and the individual
ticks file none — the Thicket's `_cineVine` rule, and at five ticks a second
there is no other defensible answer.

**6.7 THE SOUND IS RENDERED AND MEASURED IN AN `OfflineAudioContext`.**
`SFX.play` returns on its first line headless and swallows its exceptions; v42
shipped a silent ultimate through every green check in the repo. **Four voices,
and the third is the hard one:** the throw, the landing, the mill *while it
stands*, and the window closing. The mill has to survive being heard for six
seconds without becoming a wash — the Winnowing's rung problem, held rather
than repeated.

**6.8 SHADES.** `tickShadeHits` is where v51 §4.3's bug lived and Twinshade
puts three bodies in the hall for six seconds. A disc that mills everything
inside it will sweep all three. Decide the rule, write it in the comment,
assert it. Placeholder: a shade is caught like any other body.

---

# 7. THE ART

## 7a. THREE ADJACENCIES, NAMED BEFORE ANYTHING IS DRAWN

```
HARROWING    §3.4. Same weapon, same status, and the closest thing in the game.
             Twelve small white scythes stuck to a BODY against one large red
             scythe standing in the HALL
BLOODMILL    bloodsworn already throws bleeding things — Redflail winds up and
             throws spikes for 5s. Those FLY AWAY; this one STOPS
THICKET      and BREACH, and DEADFALL: the three things already anchored in the
             arena. All three are attached to a WALL or to a floor a fighter
             already walked. §7b is why that matters
```

## 7b. NOTHING IN THIS GAME HAS EVER OCCUPIED OPEN SPACE

Thicket's vines root to walls, Breach's vents are torn in walls, Deadfall's
sigils are stamped where a blow landed, and the Stasis Field rings its own
caster. **The spectre is the first object the two balls have to navigate
around** — a hazard in the middle of the floor that belongs to neither of them.

That is the strongest thing in the §1, it is free, and it is what a viewer will
actually notice. It also implies the framing: the camera has to be able to see
the spectre and both fighters at once, which is a `cinema_clip` question and
not only a renderer one.

## 7c. FOUR STATES, AND THE MIDDLE TWO ARE THE ULTIMATE

```
THE THROW    the copy leaves the weapon. 0.55s, and it is a COPY — the same
             silhouette, red and ghosted
THE STICK    it stops. This is the frame that tells the viewer it is staying,
             and if it does not read, the ultimate looks like a missed shot
THE MILL     six seconds of rotation. Most of the ultimate, and the state that
             has to hold up without becoming wallpaper
THE CEILING  the window's own signature: while it stands, the quarry can carry
             more bleed than anything else in the game can put on it. §3 says
             this is the mechanic, so it has to be VISIBLE — the stack readout
             going past four is the only evidence on screen that the ceiling
             moved
```

**7c's last line is the one to get right.** v54 §2c is the precedent that cost a
build: Deadfall's arming state was invisible at alpha 0.16 and no probe in this
repo could have said so. The ceiling is worth +7.9pp and a viewer cannot see a
constant. **Photograph the stack readout at 5, 6, 7 and 8 off a real match
before tuning anything.**

## 7d. FILM BEFORE YOU TUNE

v43 §13. This ultimate is a thing you watch stand there for six seconds; the
clip is a test, not a deliverable that comes after the numbers.

---

# Open decisions

1. **WHAT THE RELIC IS MADE OF.** §5. At the recommended build the blade
   bisects to about 16 and the ultimate carries roughly 42 points — the most
   ultimate-heavy relic in the game. The alternative is a lighter spectre and a
   heavier scythe. Rick's, and the blade follows from it rather than the other
   way round.

2. **KNOCKBACK.** §4.2. +6.3pp at 60, and the amount does not matter. Not in the
   §1. Rick's.

3. **THE NAMES.** The relic and the ultimate, four each, in the register
   bloodsworn already uses — Marrowdraw, Redflail, Oathwound, Widowmaker are
   concrete two-part compounds, and v43 §15 is the standing warning against
   inferring a register from a subset.

4. **STACKS ABOVE 4 WHEN THE WINDOW CLOSES.** §6.4. Trim or decay. A rule, not
   a knob, and the build needs an answer in a comment either way.

5. **SHADES.** §6.8. Same.

6. **CHARGE.** 15, the roster mode, and v55b established nobody's was ever
   derived. Unlike Grasp this ultimate DOES scale with cast count — more
   spectres is more damage — so charge is a real knob here and has not been
   swept. One lab, and it should happen before the bisection rather than after.

7. **THE DISC IS 138 BECAUSE IT IS A COPY.** §1. If the relic ever needs
   strength, radius is the cheapest place to find it and the first place that
   breaks the fiction. Worth writing down now, while nobody is under pressure.

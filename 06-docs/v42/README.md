# v42 — MARROWDRAW / BLOODHUNT. The twenty-fourth relic, the first shot in this game that steers, and a hole in the director that belonged to seven relics.

**2026-08-21.** Rick: *"lets go. next fighter"* → survey the grid, price the
cell, §1 in his words, price §1 BEFORE building it, build, refute, rebuild,
sweep, tune.

```
02-chain/sc-marrowdraw.html          <- THE RELIC
built off 02-chain/sc-bulwarden.html
01-live UNTOUCHED, still on sixteen

cell_survey          7/7      the grid on the v41 tip — 19 cells open
bow_survey          25/25     the bow row, re-run on 23 relics
marrowdraw_probe    14/14     §1 PRICED BEFORE A BUILDER WAS OPENED
marrowdraw_relic_probe 29/29  one check per sentence of §1, against the build
marrowdraw_sweep      —       cadMul x dmgMul, dmg bisected in every cell
engine_ab       2530/2530     IDENTICAL on the other twenty-three
```

---

# 1. THE RELIC

**MARROWDRAW.** Rick's, from four offered. The draw of a bow, and marrow for
the bone the bolt is turned from. `draw` is the one archery word the roster had
not spent — Farwarden's Reprisal *holds* a draw and never says so, which is the
closest thing to a collision and is not one. The id matches the name.

**BLOODHUNT.** Rick's, from four offered. *"It hunts"* was his own word for the
homing when he chose how hard it should track, and `blood-` is the school's
existing ultimate family (Bloodmill, Bloodprice). **`quarrel` was ruled out
before the four were offered**, because Ironhail's Quarrelstorm already owns it
— the same trap Bulwark was for Aegis in v41, caught a step earlier this time.

```
dmg 15.25   reach 54   spin 2.8   mass 1.6   onHit hemorrhage:2
shot cadence 0.34   speed 380   r 24   life 3.4      (the TYPE's, byte for byte)

BLOODHUNT  charge 15   dur 8.0   cadMul 4.0   dmgMul 1.6
           r 44   speed 220   home 3.0   life 5.0   boltBleed 0
           fork 2   forkSpread 0.9   forkHome 4.0   forkLife 2.2
           forkArm 0.18   forkDmg 0.5   forkRMul 0.55
```

---

# 2. THE CELL WAS NOT CHOSEN ON A GAP, BECAUSE FOR THE FIRST TIME THERE WAS NONE

`cell_survey` on the v41 tip: 24 cells filled, 19 open, and **the double-gap
heuristic that picked the last three relics had nothing to say.** Five schools
at 3 of 6, two at 4; four types tied at 3, the bow at 4, the greatsword full.

So the choice was made on the design job, from four measured candidates —
runic × flail (the thinnest cell ever measured here), umbral × scythe (the one
cell with no clock problem), verdant × twinblade (the slowing status on the
fastest weapon), and **bloodsworn × bow**, which Rick took.

## 2.1 A CORRECTION TO THE NUMBERS THAT CHOICE WAS PRICED ON

The candidates were priced on `verify.py --n 12` and **that pass was materially
wrong on individual relics.** At `--n 40`:

```
              n=12    n=40
Spellbreaker  39.8%   45.8%     the "weakest relic in the game" was noise
Emberedge     44.7%   51.7%
Slagheart     47.7%   52.3%
Widowmaker    51.9%   46.6%
```

Both claims the choice leaned on move: runic is **not** the weakest school
(47.2%, umbral is 47.0%) and the bow is **not** the strongest type (52.4%,
behind the warhammer's 52.7%). Neither reverses the choice — bloodsworn at
48.7% and a bow at second make the cell slightly *better* than it was sold —
but the rule is now on the record:

**A CELL CHOICE PRICED ON FEWER THAN 40 SEEDS IS PRICED ON NOISE.** The n=12
pass also failed a check (`Axiom vs Twinshade 0/12`) that passes cleanly at 40.

---

# 3. §1 IN RICK'S WORDS

> *"red bow slows down its shots drastically for a duration and begins shooting
> larger balista shots. The shots gain a homing effect that will seek out its
> opponent. when the shots hit they pierce the enemy ball fly through and fork
> into 2 shots which turn around and try to home in and hit again. the forks
> apply bleed*
>
> *the balista shot can be clanked nullifying the fork and destroying the bolt"*

Nothing was started before this existed. **And nothing was built before it was
priced** — v41 built §1 literally and had it refuted inside an hour at the cost
of a build, so `marrowdraw_probe.py` ran first, runtime-only, on the v41 tip.

---

# 4. THE JOB IS THE TYPE'S, BECAUSE THE SCHOOL DOES NOT HAVE ONE

`bow_survey` §5, re-run on 23 relics: **bloodsworn is the strongest channel on
the bow by half again**, +53±23 damage in a paired 20-second window (+52%),
against sanctified's +38, dwarven's +19, and umbral's +0.

**This is the first relic in the chain whose ultimate is not being asked to fix
its own cell.** So the ultimate is free to be about the TYPE, and the type has
exactly one problem: `bow_survey` §2 measures **a bow landing 8.3% of what it
fires, with 81% of every arrow ending on a wall.** v40 closed on that number —
*"the wall is the type's constraint and no relic addresses it"* — and then
Vinesower's Thicket addressed it by MONETISING the misses.

**Bloodhunt attacks the same 81% from the other end. It stops missing.**

```
turn rad/s   landed   parried    wall    hits/s   dmg/s     ttk
  0.00        7.1%     9.3%     82.9%    0.279    5.63    34.3s
  1.00       11.4%    11.8%     75.8%    0.398    7.49    29.0s
  2.00       18.1%    14.6%     63.7%    0.536    9.50    22.7s
  4.00       35.8%    24.8%     35.4%    0.934   14.80    16.2s
 12.00       40.9%    34.5%     21.3%    1.033   16.51    14.8s
```

Damage pinned 14.0, ultimates suppressed, five foes one per shape, five seeds,
2085 arrows on the baseline row. It is the largest movement any mechanic in
this project has made in the column its own type survey named as the
constraint.

---

# 5. §1'S TWO PHYSICAL CHANGES DO DIFFERENT JOBS, AND ONLY ONE IS A BALANCE KNOB

The hypothesis going in was that **`r` is where §1's clank clause gets its
teeth**, because `r` is literally on both sides of the engine's ledger — the
hit test is `dist < R + s.r` and the parry test is `dist < s.r + width/2 + pad`.
A bigger bolt is easier to hit with AND easier to bat out of the air.

**It was wrong. Both sides grow together and the ratio is flat.**

```
  r      landed   parried   parried per landed
  24      7.1%     9.3%          1.31
  40      9.6%    10.2%          1.06
  60     10.1%    13.0%          1.28
```

**"Larger ballista shots" is a LOOK knob**, in the sense v41 settled for
Aegis's `turn` — and that is a licence rather than a disappointment, because it
means the bolt can be drawn at whatever size reads in the hall with nothing
downstream balanced on it. **The teeth are in the SPEED:**

```
 speed  home   landed  parried  parried per landed   flight
  380    2.0    18.1%   14.6%          0.81           0.75s
  300    2.0    20.2%   21.4%          1.06           1.01s
  220    2.0    23.2%   27.1%          1.17           1.22s
  150    2.0    27.5%   26.8%          0.97           1.35s
```

A slow bolt is longer in the air, and the two things that happen to it there
pull opposite ways: a blade has more time to find it, and the homing has more
time to work. Between 380 and 220 the blade wins. **§1's "slows down
drastically" is the sentence that hands the foe the counterplay §1's last line
promises**, and there is an interior maximum — past 220 the homing catches up.

---

# 6. "THE BALISTA SHOT CAN BE CLANKED, NULLIFYING THE FORK" WAS ALREADY THE RULE

`tickShots` resolves in the order the viewer would: **parried, then landed,
then spent on a wall.** A batted bolt sets `dead` in the parry branch and never
reaches the branch a fork hangs off. §1's last sentence cost zero lines.

Asserted structurally *and* behaviourally, over 18 fights and six foes: **46
bolts batted out of the air and 49 that landed on a live foe produced exactly
98 forks** — two times forty-nine, and none of the batted ones in it.

Two things fall out of the same branch and are checks rather than comments:
**a bolt that kills forks nothing** (4 of 53 landed bolts were lethal), and
**`arm` is the pierce** — a fork is born inside the ball the bolt just went
through and may not hit anything for `forkArm`, expressed in the field
`tickShots` already gates both hit branches on for the Harrowing's blades.

---

# 7. THE FORKS COME BACK, AND THEY TURN TO DO IT

A fork leaves at the bolt's heading with the ball behind it, so it cannot
return inside a turning radius of `speed / forkHome` — 55 units at 4 rad/s,
which is smaller than the ball.

```
fork turn   radius   connects   batted    wall   ran out
   0.0        inf      36.6%     34.7%   25.5%     0.9%
   2.0        110      38.4%     37.1%   13.8%     7.6%
   4.0         55      51.9%     41.0%    0.9%     1.9%
   8.0         28      56.3%     40.8%    0.0%     1.0%
```

**Above 4 rad/s no fork ever ends on a wall.** Every one ends on the enemy or
on the enemy's blade.

**AND THE PROBE ALMOST SCORED THAT SENTENCE WITH HITS THAT NEVER TURNED.**
v42's design document predicted this before the build existed: 36.6% of forks
connect with NO homing at all, because they are born inside the ball and the
ball moves back into them. The relic probe's first cut recorded every fork with
age 0 and turn 0 — forks are pushed straight into `m.shots` by the fork branch
and never pass through `spawnShot`, so the wrappers never saw them born.
Registered properly: **forks that connect have turned a median of 0.70 rad
first, up to 5.62** — most of a full circle — and the earliest connection is at
0.300s against a 0.18s arm.

---

# 8. "THE FORKS APPLY BLEED" COULD NOT BE BUILT AS WRITTEN

The first build read it as an EXTRA application on top of the weapon's own
`onHit`. **It swept BYTE-IDENTICAL at forkBleed 0, 1, 2 and 3** — same damage,
same win rate, same fork share to the digit. v41's wall-feed signature exactly,
and caught the same way: by two configurations agreeing too well.

`STATUS.hemorrhage.maxStacks` is **4**, `onHit` is **2**, and `resolveHit`
fills the ladder in the same call. Measured: **86% of fork hits arrive with the
quarry already at cap**, and `apply` clamps the rest away with `Math.min`.

Rick, given the three ways out: **the bolt stops carrying the school.**
`boltBleed 0` hands `over.onHit` an empty object — a channel `resolveHit`
already honours for Ironbloom's splinter, *"a splinter sunders ONCE, where the
head that threw it sunders twice"* — so the bolt lands as pure damage and the
forks are the only part of the ultimate that bleeds. Which is §1's sentence,
made true.

Rejected: raising hemorrhage's cap (a change to the SCHOOL, not the relic —
Threshmaw, Goreshard and Widowmaker all get stronger and four documents stop
being right), and leaving it as it was.

**`forkBleed` is not shipped.** A dead knob is worse than no knob —
`shot.life: 3.4` has been dead config on four bows since v40 and is still an
open decision.

---

# 9. THE DIRECTOR WAS BLIND TO EVERY BLEED-OUT KILL IN THE GAME

**This is not a Marrowdraw finding.** It was found while probing this relic and
fixed here because this relic is the one that has to film, but it belongs to
seven.

`tickStatus` does `f.hp -= def.dps * st.stacks * dt` and files no beat, so a
fight that ends on a bleed tick carries no fatal beat at all — `cinePlan`
scores no killing blow and `cinema_clip` falls back to "the last cut".

Measured as *the share of wins with no beat on the step the quarry's hp crossed
zero*, over 23 opponents × 6 seeds:

```
Dawnbringer  44.1%        Ironhail     0.0%
Widowmaker   31.1%        Axiom        0.0%
Threshmaw    26.2%        Nightfell    0.0%
Lastlight    25.7%        Bulwarden    0.0%
Marrowdraw   23.8%
Goreshard    20.9%
Aureole      19.4%
```

**Every school carrying a status with a `dps` is between a fifth and nearly
half. Every school without one is exactly zero.** That is a control separating
cleanly, not a trend. Dawnbringer has been in `01-live` since v37 ending nearly
half its fights on a blow the camera was never told about.

## The fix is v41's rule, for the fourth time and from a fourth direction

**A FATAL TICK FILES A BEAT. AN ORDINARY ONE DOES NOT.** Triplicate needed the
distinction, the Thicket needed it (*"a lash is not a beat … THE FATAL ONE IS
KEPT"*), Aegis needed it in v41 when 21% of Bulwarden's wins were landed by a
reflection the director could not see. A bleed ticks 120 times a second and
filing those would hand the director a fight made of the loser standing still.

After: **Marrowdraw is 0 blind out of 47 wins**, and every hemorrhage relic is
zero. `engine_ab` is still 2530/2530 — a beat is written to a list the
simulation never reads, and that is the proof rather than this sentence.

**The attribution is the other fighter**, which is sound rather than lazy: a
status does not record who applied it, the only `dps` statuses are hemorrhage
and smite, only bloodsworn and sanctified carry them, and neither school has a
summon. The relic probe asserts that precondition rather than trusting this
paragraph.

## What is left, named

**Dawnbringer is still 22.1%**, and the residue is a different hole: Daybreak's
spark burn calls `hurt()` directly. So does `_traceHit`. v41 named `hurt()` and
`shatter()` as beatless paths and asked which of them are endings; this session
answers for `tickStatus` and leaves those two measured and open.

---

# 10. THE ART TOOK THREE CUTS AND THE THIRD ONE CAME FROM A REFERENCE

**Cut one was a dart** — a 3:1 shaft, a fat triangular head, two vanes nearly
as wide as the bolt was long. Rick: *"the balista shots look a little
cartooney. can we go for a longer slimmer and more realistic look?"*

**Cut two was 20:1 and still wrong**, and the diagnosis is the useful part
because it is not about length: *"they look like cartoony rockets."* A bright
white nose cone plus two solid saturated fins is a rocket at any aspect ratio.
**Slimming a rocket makes a slimmer rocket.**

**Cut three was drawn from a reference Rick supplied**, and every element of it
fights the rocket read: the shaft is nearly all of the object at about 33:1 and
carries a TWIST; the head is small and dark, a short leaf barely wider than the
shaft; the fletching is FEATHER — three dark vanes with barbs, set at the nock;
and the only bright metal is a small cap at the very end. **The value structure
is inverted from cut two — the shaft is the light thing and the ENDS are dark**,
which is also why it reads at arena scale: two dark tips at a known separation
on a pale line is a length cue.

**And the trail is the mechanic.** It is a polyline through positions the bolt
really occupied, so a bolt that curved draws a curve. Every other projectile in
this game draws a straight streak along its current heading, which is correct
for them and would have been a lie here.

`marrowdraw_bolt_zoom.py` exists because none of this is decidable from a
filmstrip at 30% scale — a bolt is about 130px in a 1080-wide hall, and every
look decision about it was being made from a picture in which it is nine
pixels. It photographs the shipped `drawShots` on the real arena and crops in.

---

# 11. WHAT THE SWEEP SOLVED

`cadMul` and `dmgMul` are not separable — at cadMul 4 the window fires a
quarter as many shots, so anything under 4.0 in `dmgMul` is a DPS cut bought
back by the landed rate. **Every cell bisected `dmg` against all 23 opponents
before its telemetry was read** (v40's rule, and v41 open decision 2 for why
the field and not a subset).

```
 cadMul  dmgMul    dmg     win   bolts/cast  landed  parried   wall   window
    2.0     1.6  10.81   51.7%        7.9    30.2%    28.6%   37.9%    45.7%
    3.0     2.2  11.38   48.7%        5.3    27.3%    26.6%   43.8%    47.3%
    4.0     1.6  14.75   50.4%        4.3    26.3%    29.3%   42.4%    34.6%
    2.0     4.0   8.56   60.9%        7.6    26.3%    24.0%   45.5%    66.7%
```

**The framing that made the choice decidable:** across the whole grid a bolt
lands for 24–26 damage whatever the pair is, because the blade bisects to
compensate. So the pair does not choose how hard a bolt hits — **it chooses how
strong the relic is between casts.** Rick took 4.0 / 1.6: the blade lands
inside the type's own 12.73–16.23, so Marrowdraw is a real bow that gets a
hunting window rather than a relic that is barely a bow between them.

The final bisection, at the shipping numbers, 40 seeds × 23 pairings:

```
  dmg 16.00 -> 54.3%      dmg 14.50 -> 46.0%
  dmg 15.62 -> 51.0%      dmg 13.00 -> 40.8%
  dmg 15.25 -> 49.6%   <- ships, over 920 fights
```

---

# 12. THE ULTIMATE SHIPPED SILENT AND NOTHING IN THE REPO COULD SAY SO

Rick, after the first clip: *"a sound effect to signify it triggering."*

**There wasn't one.** The ult voice called `this.tone()` and `this.noise()`,
neither of which exists — the helpers are `_tone(t, {…})` and `_burst(t, {…})`
— so the branch threw a `TypeError` on its first cast.

**Three separate things conspired to hide it**, and any one of them alone would
have been survivable:

1. `SFX.play` wraps its entire body in a `try { … } catch`, so the throw was
   swallowed at the call site.
2. `play` returns on its first line when `!this.on || !this.ok || !this.ctx`,
   which is **every headless run in this repository**.
3. A sound that throws and a sound that is quiet look identical from outside.

So it passed a 14-check pre-build probe, a 29-check relic probe, a full sweep, a
13/13 verify and a rendered clip. **The only instrument that could ever have
caught it was a person listening.**

`marrowdraw_relic_probe [10]` is the check that should have existed. It stubs
`_tone` and `_burst`, forces `on`/`ok`/`ctx` truthy, plays every sound this
relic makes and **counts the oscillators** — a branch that throws on its first
line makes zero, and one that throws halfway makes some but not all, so the
expected count is the number of calls the branch is written with. Proved
against a deliberately sabotaged copy: the real build makes 8 and the sabotaged
one makes 0, while the Aegis control makes 6 in both.

**This generalises past sound.** Any subsystem that (a) is wrapped in a
try/catch and (b) is inert headless is a place where broken code ships looking
exactly like working code. Sound is the one this project has; it should not be
assumed to be the only one.

## The sound that ships

**A bang, then a low guttural growl** — Rick's, verbatim, replacing a windlass
that was the right idea about the wrong half of the mechanic. A machine being
cranked describes the SHOT; this ultimate is about the thing doing the
shooting.

**And the first growl was a fart.** Rick: *"the growl frankly sounds like a
fart. its way off. it should be lower rumblier and much longer."* He is right
and the diagnosis is mechanical rather than a matter of taste — that first cut
was three **sawtooths** at 57–66 Hz gliding **downward** with a **4.5 Hz** beat,
which is very nearly the textbook recipe for the sound he named. A low buzzy
tone that slides down is a raspberry, and 4.5 Hz is a burble rate.

Three things had to change and none of them was a parameter tweak:

* **Noise, not sawtooth.** A growl is turbulence shaped by throat resonances.
  An oscillator is a buzzer whatever you do to it.
* **The pitch must not slide down.** The sub sags 12% over four seconds where
  the first one fell 22% in one.
* **Much slower, irregular modulation.** Two LFOs at 1.05 and 1.73 Hz, summed
  so the amplitude wanders instead of flapping. A single LFO at any rate reads
  as a tremolo pedal.

**`_tone` and `_burst` could not have carried it, and one of them was already
failing quietly.** `_noiseBuffer` is 0.6 seconds and `_burst` does not loop, so
**every `_burst` longer than 0.6s in this game has been playing silence for its
tail** — including the 0.95s bed in the growl this replaces. `_growl` is a new
builder: two looping noise sources at 0.46 and 0.31 playback rate (so the
buffer's own period is never audible), a lid at 620 Hz, three throat formants
at 105/205/420 Hz, a near-stable 30 Hz sub, and a 4.6s envelope held for 60% of
its length because an exponential release spends its last third under the
audible floor.

## AND THE SECOND GROWL WAS INAUDIBLE, WHICH THE CHECK CERTIFIED AS CORRECT

Rick, on the clip: *"bloodhunt made no sound in that video."*

It did. It was as loud as the entire mix. **And 97.7% of its energy in the
finished clip was between 20 and 60 Hz** — subwoofer only. No laptop, no phone,
no earbud reproduces a note of that, so "measured loud" and "made no sound"
were both true at once. A pure 30 Hz sine at gain 0.9 next to noise through
bandpasses at Q 4.5 puts the sine ~20 dB over the body it was meant to sit
under.

**THE CHECK WAS COMPLICIT.** "Lower" had been encoded as *share of energy below
180 Hz*, and a 30 Hz sine maxes that out. The test was passed most convincingly
by the exact degenerate answer it existed to prevent. **A metric a broken
output scores perfectly on is not a check.**

## AND THE THIRD GROWL WAS ROLLING THUNDER, WHICH IS ALSO A RECIPE

Rick: *"it sounds like rolling thunder. want me to get you inspiration?"*

Yes, and that ended it. **Thunder IS filtered noise with a slow irregular
envelope** — chasing "lower and rumblier" the sub had gone to a quarter and the
body had become almost entirely noise, which took the PITCH out. A growl is a
VOICED sound: folds giving a low fundamental with a harmonic series, shaped by
a throat, with noise on top rather than instead. Cut one had pitch and no noise
(a fart); cut three had noise and no pitch (thunder).

Three tries, three different wrong sounds, each from translating an adjective
into synthesis parameters. **The bolt art took three cuts and a reference image
ended it in one; the sound took three cuts and a reference recording ended it
in one.** That is not a coincidence and it belongs in rule 2.

## THE FOURTH GROWL WAS FITTED TO THE REFERENCE AND STILL WRONG

`growl_lab` measured four separate growls in Rick's recording and fitted
`_growl` to their mean: **6.4 points of total band error across six bands, and
7.4 Hz of roughness against the reference's 7.5.** Isolated out of the
delivered mp4 by subtraction it landed within 9.3 points.

Rick: *"this is still really far off."*

**THAT IS THE MOST INFORMATIVE RESULT IN THE WHOLE SEQUENCE.** A spectrum match
that close, still wrong, means band shares and a modulation rate do not capture
what makes a growl a growl. The missing thing is cycle-to-cycle **jitter and
subharmonic chaos** — what separates a biological voice from an oscillator, and
what none of the four attempts had. It was a gameable metric one level up from
the two gameable metrics before it, and it took four cuts to see that the
problem was the CLASS of sound, not the parameters.

## SO THE GROWL WAS SCRAPPED, AND THE PROCESS WAS THE REAL FIX

The evidence across the session is unambiguous:

```
  landed on the FIRST attempt    the lock, the fork's split, the ballista
                                 string, the ratchet, the iron clamp
  failed FOUR times              one sustained biological voice
```

A percussive sound is **an envelope plus a rough band** — both specifiable,
both measurable, and *approximately right still sounds right*; it just sounds
like a slightly different object. A voice is carried by fine structure over
time, its average spectrum barely constrains it, and approximately right lands
in the uncanny valley. **That is a rule about what to attempt, not about how
hard to try.**

**And the process changed, which mattered more than the sound.** Four growl
cuts were four serial round trips: write a sound I cannot hear, render a
25-second clip, wait, get one adjective back. `cast_lab.py` replaced that with
a SPREAD — six characters in one file, then three depths of the winner. **Two
round trips, both landing**, against four that did not.

## WHAT SHIPS: AN IRON CLAMP

Rick's, from six offered, then from three depths of it, then "lower and
louder".

```
  4400 Hz tick   0.03s     the metal-on-metal contact
   594 Hz body   0.13s     the clack
    92 -> 38 Hz  0.55s     the thump
  ring: 139 / 209 / 302 / 443 Hz over 1.4-2.3s
        ratios 1 : 1.51 : 2.18 : 3.20
```

**The ring is what makes it iron, and its ratios are the check.** Integer
ratios would be a bell playing a pitch; real struck metal is inharmonic, and
`marrowdraw_relic_probe [10]` asserts at least two partials sit more than 0.10
from a whole number. It also asserts the attack lands inside 60 ms and that
there is still 9% of the peak at 0.6 s — a thud fails the first, a swell fails
the second. **None of those three can be won by a sound that merely has the
right average spectrum**, which is precisely the trap four cuts of growl kept
walking into.

**The 4.4 kHz tick is scaled down far less than everything else.** Dropping it
with the rest is what would turn a lower clamp into a cardboard box — and 39%
of the sound sits in 200–600 Hz, so unlike the growl it survives a laptop.

## And the brief is a CHECK, not a claim

`marrowdraw_relic_probe [10]` renders every sound this relic makes in an
**OfflineAudioContext** and measures it, which catches the silent case whatever
caused it — a throw inside `play`'s own try/catch still produces an empty
buffer — and turns "lower, rumblier, much longer" into three numbers:

```
                      peak   audible   <120Hz   thru 300Hz HP   heave
  the cast           0.572      3.40s    65.6%          61%     0.67
  CONTROL Crucible   0.506      0.75s    90.9%          22%     0
  CONTROL Aegis      0.272      0.45s    59.2%          55%     0
```

`heave` is how much the level wanders after the transient; **every other cast
voice in the game is 0 by construction**, because they are all single decaying
envelopes. The controls are what make the row above mean anything.

**And the fork got its own.** Rick: *"give the fork its own sound."* The pierce
and the split were silent, so the half of the ultimate that happens after the
hit was carried entirely by the picture. One call per PIERCE and not one per
fork — two forks are one event, and firing it twice reads as two impacts a
frame apart.

---

# 13. THE HUNTER'S EYES

Rick: *"can we also give the ball itself an animation when its bloodhunting?
maybe piercing red hunters eyes floating above it?"*

**Why the ball needed one.** Every other window ultimate in this game puts
something on the CASTER a viewer can point at — Bloodmill spins the head, Aegis
stands a wall in front of it, the Thicket roots the hall. Bloodhunt's whole
expression was out in the air on objects that are only there half the time, and
between bolts the relic looked exactly like a bow having a quiet moment. **The
window is eight seconds long.**

Three eyes, slit-pupilled, in a shallow arc above the shell, and:

**They look at the quarry.** The pupils track the foe, so the picture on the
caster says the same thing the bolts say — *this weapon has stopped firing at a
direction and started firing at a fighter.* It is the homing, stated on the
ball, a second before the first bolt proves it.

**They blink out of sync.** A row of steady lights reads as a status icon; a
row that blinks at slightly different times reads as something alive. The phase
offset per eye is what stops three of them reading as one object with three
lamps on it. `ph = (t·0.42 + i·0.37) mod 1`, deterministic off `m.t` the way
`SHAPES._t` is — `life` is not in `LERP_FIELDS` and an accumulated phase would
strobe against the frame interpolator.

**They sit at R+36 and not R+25**, which is the first cut: the eyes are drawn
before the relic, so the bow won every overlap and its barbs swept through them
twice a second.

`marrowdraw_eyes.py` photographs them, because a ball is 34 world units in a
520-wide hall and none of this is decidable from a filmstrip. It also **solves
for the blink frame rather than guessing at it** — the blink is 4.5% of a 2.4s
cycle, `ph` is invertible, and the first cut nudged the clock by a second and
caught every eye wide open.

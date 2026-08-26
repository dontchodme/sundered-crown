# v43 — PARADOX / STASIS FIELD. The twenty-fifth relic, the first thing in this game that stops a ball, and a sound that landed on the first attempt because it was offered as a spread.

**2026-08-21.** Rick: *"next fighter please"* → survey the grid, price the cell
at 40 seeds, survey the TYPE, §1 in his words, price every sentence of §1
BEFORE a builder was opened, build, refute, rebuild, sweep, tune, film.

```
02-chain/sc-paradox.html             <- THE RELIC
02-chain/sc-paradox-frame.html       <- THE BUILD OF RECORD
built off 02-chain/sc-marrowdraw.html
01-live UNTOUCHED, still on sixteen

cell_survey             7/7      the grid on the v42 tip — 18 cells open
verify --n 40 (v42 tip) 13/13    11040 fights, so the cell was not priced on noise
flail_survey           26/26     the flail row, seven sections, before the design
runic_flail_probe      12/12     §1 PRICED BEFORE A BUILDER WAS OPENED
paradox_relic_probe    31/31     one check per sentence of §1, against the build
paradox_sweep            —       need x bleed x blow, dmg bisected in every cell
engine_ab          2760/2760     IDENTICAL on the other twenty-four
chain_audit            12/12     every insert survives to the tip
frame_probe            11/11
verify.py --n 40       13/13     12000 fights, Paradox 47.7%, 0 timeouts
07-shorts/v43/stasis-v-heartwood.mp4   seed 25064, 23.0s, three holds and the
                                       window lands the last blow
```

---

# 1. THE RELIC

**PARADOX.** Rick's, from four offered. A trap that folds in on itself, which
is what a zone you can neither see the edge of nor choose to leave actually is,
and it sits beside Axiom as the same kind of word without being it.

**STASIS FIELD.** Rick's, and **his own words rather than one of the twelve
offered across three spreads** — two of which he rejected outright. That is the
"offer a spread, not a guess" lesson arriving from the other end: a spread is
cheap, and being wrong about the REGISTER is what costs. My first two spreads
were both abstract logic nouns because runic's three ultimates are; the roster's
other twenty-one are concrete. **`hex-*` was ruled out before the first spread**,
the way `quarrel` was in v42 — the school's status is literally called Hex and
the hold measurably OVERWRITES 61% of its fires, so a hex- name would tell a
viewer the ultimate is the status when it is the thing that eats it.

```
dmg 35.00   reach 96   width 22   spin 2.2   mass 3.6   mode chain
onHit hex:1                                  (the TYPE's and the SCHOOL's, byte for byte)

STASIS FIELD  charge 16   dur 9.0   rad 200   arcs 6
              need 0.6   bleed 0.5   blow 0.5   pin 2.0
```

---

# 2. THE CELL, AND THE SENTENCE IT WAS CHOSEN ON WAS HALF WRONG

18 open cells on the v42 tip; four schools at 3 of 6 and four types at 3, so the
double-gap heuristic has nothing to say for the second session running. Every
relic was re-priced at **40 seeds** first — v42's rule 7 — and runic × flail was
taken from four candidates, on this:

> *the thinnest cell ever measured here — 15% of the fight at two or more
> stacks and 0% at cap. Hex is a rate, not a quantity, so an ultimate that pins
> it at its cap is worth 5x the lock.*

**The rate half is exactly right. The `worth` half named the wrong column, and
`flail_survey` §6 is the correction.** Driving hex to its cap takes the lock
from 29% to 86% and the foe's landed blows from 0.294/s to **0.111/s** — 62%
fewer, 57% less damage taken — while the damage this relic DEALS does not order
itself across the rungs at all. **Hex on this type is a defensive channel.** A
locked weapon does not make this weapon swing faster; it stops the other one.

And `cell_survey` was wrong about the row in the other direction too: the cell
it calls the thinnest in the game is **the second-strongest channel on its own
row by delivered effect (+12.1%) and the only one of four that cuts damage
taken.** Occupancy is a proxy twice removed for a status that is a rate (v39
5.2), and that has now mispriced two cells.

---

# 3. THE TYPE'S CONSTRAINT — THE HEAD IS THE WEAPON, AND IT IS THIRTEEN UNITS LONG

`flail_survey` §2, and it is the whole reason this relic's ultimate is what it
is. Read off `bladeSegments` — the function the hit test actually calls:

```
type          live blade  contacts/s  extension   taut   lag rad   lag max
bow                 61.4       0.106       1.00   100%      0.00      0.00
flail               13.2       0.152       0.88    36%      0.53      1.71
greatsword         128.4       0.269       1.00   100%      0.00      0.00
scythe             116.5       0.196       1.00   100%      0.00      0.00
twinblade           70.4       0.257       1.00   100%      0.00      0.00
warhammer           85.7       0.183       1.00   100%      0.00      0.00
```

**13.2 units against 61 to 128, and the number is `width × 0.6`. The flail's
reach of 96 does not appear in its live edge at all.** The head roams a band out
to a measured 119 units and occupies one 13-unit stub of it at any instant. The
type covers the most ground in the game and is live in the least of it, which is
why it is paid 25–44 damage a blow.

It is also **the only contact point in the game that is not the facing**: mean
|headAng − theta| is 0.53 rad, max 1.71, against 0.00 for every rigid weapon.

**And its own clock is slower than its own status.** It lands a blow every 5.94
seconds against a 2.6-second hex, so 75% of every hex it applies arrives on a
foe with no stacks. The ladder is not topping out low; it is being re-lit from
cold three times in four.

Both of those are one problem: **this weapon cannot reliably touch anything.**

---

# 4. §1 IN RICK'S WORDS

> *"blue flail gains a medium sized hexagonal shaped chain of lightning
> surrounding the flails ball. the flail gains extra hit stun. enemies that stay
> inside the hexagon (that is inside the beams of lightning with the flail head)
> for too long are true stunned. unable to move (ball and weapon) for 2ish
> seconds."*

Nothing was started before this existed, and **nothing was built before every
sentence of it was priced** — `runic_flail_probe.py`, 12/12, runtime-only on the
v42 tip. Three of the four came back needing a decision only a measurement could
make, and one of them could not be built as written.

## 4.1 "FOR TOO LONG" COULD NOT BE TWO SECONDS

Continuous residence inside the hexagon, episodes still open at the end DROPPED
because a censored episode is not evidence about how long a residence lasts:

```
shape  radius   share  episodes/min   mean    p50    p90    max   >=1.0s  >=2.0s
hexT      130   12.8%          37.8   0.20   0.16   0.41   1.00     0.1%    0.0%
hexT      200   32.3%          46.2   0.41   0.34   0.79   1.95     4.5%    0.0%
hexT      320   63.2%          42.4   0.85   0.61   1.87   5.71    28.3%    8.7%
```

**At the shipping radius the median stay is 0.34 seconds and the longest of 1058
was 1.95. Not one reached two.** Even at 320 — a hexagon 640 across, in a hall
520 wide — only 8.7% do. The quarry enters and leaves **46 times a minute**.

**Because nothing in this game steers.** A ball is ballistic: gravity, wall
bounces, and a speed that relaxes toward a cruise it never falls below. There is
no seeking, no avoidance and no decision, so "stay inside" is not a thing a foe
does — it is a thing that happens to it.

Rick took the fork: **a CHARGE that fills while the quarry is inside and bleeds
while it is out.** It says the same sentence on screen and it is the version
that can happen — 6.2 holds a minute where the continuous rule lands 0.0.

**`bleed` is the counterplay and it is the only one this design can have.** That
is a measurement rather than a shrug: every other relic's counterplay is a thing
the foe's weapon does — a bolt can be batted, a wall can be gone round — and a
foe cannot choose to leave a zone in a game with no steering. So the one lever
on how forgiving this is, is how fast the charge comes back.

## 4.2 THE HEXAGON IS A LOOK KNOB, WHICH IS A LICENCE

```
radius    circle R   hex static   hex turning   circle 0.866R   hex vs circle
   160       25.8%        21.5%         21.5%           19.4%          -16.5%
   200       38.0%        32.4%         32.3%           29.8%          -14.8%
   320       70.7%        63.5%         63.2%           59.7%          -10.6%
```

A hexagon covers **83% of its own circumcircle by area and collects 81% of what
the circumcircle collects.** Whether it turns with the weapon changes the share
of the fight by **0.06%**. So the shape is a picture and the RADIUS is the
mechanic. v42's "larger ballista shots" finding, again, and a licence there too.

**And §1's own parenthesis put a floor under the size before anybody picked a
number**: the head is inside the beams, and the head reaches 115 units from the
shell. Rick took 200 from four measured options — the quarry is inside 32.3% of
the fight, and the hall is 520 across.

## 4.3 "THE FLAIL GAINS EXTRA HIT STUN" WAS REPLACED RATHER THAN BUILT

```
x hitstun  stun/blow  foe locked  my blows/s  foe blows/s   hp/s  taken/s   win
      1.0      0.240       20.6%       0.151        0.261   8.14     6.49   67%
      2.0      0.469       21.8%       0.143        0.253   8.16     6.57   56%
      3.0      0.702       23.1%       0.141        0.244   7.91     6.55   65%
```

The multiplier reaches the weapon — mean hitstun a blow goes 0.240s → 0.702s —
**and it buys two and a half points of lock and moves damage taken by nothing.**
The reason is the type: this weapon lands a blow every six seconds, and tripling
the stagger of a blow that rare is tripling almost nothing.

Rick's call, from three priced options: **a landed blow feeds the CHARGE
instead.** The sentence keeps its intent — your blows shut them down harder —
and the hardest blow in the game starts mattering to the mechanic rather than to
a ladder that cannot build. **A dead knob is worse than no knob**, and
`shot.life: 3.4` has been dead config on five bows since v40.

## 4.4 AND THE BEST SENTENCE IN §1 IS THE LAST ONE

Three arms on identical seeds, 179 holds, read over the 3 seconds from the
moment the hold lands. **Arm 1 is exactly what `u.freeze` already does.**

```
arm                my blows  foe blows   dealt   taken   sep at trigger
control               0.532      0.713   29.92   19.37              136
weapon only           0.605      0.356   34.97   10.26              136
weapon AND ball       0.676      0.318   42.35    8.11              136
```

A locked weapon is **defensive** and the engine already has it. Pinning the ball
as well is **offensive**, and it is the half this cell needs: **+21% damage on
top of the lock and +42% on nothing**, because a 13-unit head against a target
that has stopped moving is a different weapon.

**And the first cut of that section said the opposite.** It pinned at a fixed
clock time wherever the foe happened to be and read **−12%** — a true fact about
a pin and a false one about *this* pin, which only ever triggers on a foe
already inside the hexagon. Firing it where the mechanic would fire it flips the
sign. Kept as a check.

---

# 5. WHAT HAD TO BE INVENTED, AND IT IS ONE LINE

`f.stun` IS THE WEAPON HALF and it is already a TRUE stun in this school's
hands: hex is one of exactly three sources that break a wind-up, so a hold that
writes `f.stun` inherits that with no special case.

**THE BALL HALF DID NOT EXIST.** `moveMul` floors at 0.45, `speedMin` is 250,
and `fireUlt`'s `u.freeze` — the thing two viewer-facing tips call *"roots"* —
writes `foe.stun` and touches the ball not at all. **Bramblesnare and Rootfast
both say "roots" in a tip and mean "weapon locked".**

So `f.pin` is new, and it is one line in one function: `move` returns on it.

## 5.1 A HELD BALL IS AN IMMOVABLE OBJECT

`_ballPair` gives both halves of the separation and the whole of the impulse to
the other ball — the equal-mass exchange with one mass sent to infinity —
because a held ball that could be shouldered across the hall would be a hold the
viewer can watch being broken by the thing that cast it. **Byte-identical when
nobody is held**, and `engine_ab` is the proof of that rather than this
sentence.

## 5.2 AND IT RESUMES EXACTLY WHAT IT WAS DOING

A ball that cannot move can still be PUSHED — knockback from every blow it eats,
a bind it loses, a shade shouldering it — and none of that can be spent while
the hold runs. **The first build let it all accumulate and the ball launched on
release at up to 165 units/s per blow banked.** Measured, put to Rick, and
refused: *"ball should just resume when the stun ends. no banked knockback and
no loss of momentum after the stun."*

So `move` restores the captured vector on the first frame the ball is allowed to
move again, and drops it. `paradox_relic_probe [6]` asserts the restored vector
is byte-identical to the captured one over 23 releases, and reports what was
being thrown away: **737 units/s on the way in against 567 at capture.**

---

# 6. WHAT THE SWEEP SOLVED

`need` and `bleed` are not separable — between them they set how often the field
fires, and a `need` of 0.6 with a 2/s bleed and a `need` of 1.2 with none land
the hold at nearly the same rate and are completely different mechanics. **Every
cell bisected `dmg` against all 24 opponents before its telemetry was read.**

```
 need  bleed     dmg    win  holds/cast  holds/min   held  window share  hits/s held   free
 0.60   0.25   35.06  48.3%        1.37       3.68  13.6%         27.4%        0.263  0.138
 0.60   0.50   31.00  49.2%        1.39       3.53  13.4%         25.1%        0.245  0.133
 0.90   0.50   40.75  51.7%        0.75       1.97   6.8%         16.6%        0.296  0.125
 1.20   1.00   40.75  47.5%        0.23       0.59   2.2%          2.9%        0.176  0.133
```

**One number is constant across the whole grid and it is the point of the
relic: a blow lands on a held quarry at 0.24–0.30 a second against 0.12–0.14
free.** The hold roughly doubles the connect rate of a 13-unit head, whatever
else is set.

**The framing that made it decidable:** the bisection compensates, so the pair
does not choose how hard Paradox hits — the blade lands between 31 and 41
whatever you pick, all inside the type's own 25–44. It chooses **how much of
Paradox IS the field**, from 3% of its damage to 27%, and how often a
nine-second window catches anything at all. Rick took **0.6 / 0.5 / 0.5**: 1.54
holds a cast, so every window catches something and most catch twice.

The final bisection, 40 seeds × 24 opponents, 960 fights a step:

```
  dmg 37.00 -> 54.7%      dmg 34.94 -> 50.5%
  dmg 35.50 -> 50.8%      dmg 34.84 -> 49.6%
  dmg 35.12 -> 50.3%      dmg 34.75 -> 49.3%
  dmg 35.00    <- ships           34.00 -> 49.2%
```

**It moved UP from 33.75 when §7 was fixed**, which is the right direction: a
caster welded to the ball it had just frozen was landing blows it should not
have been able to reach.

**And the baseline is the interesting number.** A runic flail with hex and NO
ultimate at all needs **42.4** to break even — the top of the entire type,
Gravemourn's own number. So the Stasis Field is worth about nine points of
blade, and it is the difference between a relic at its type's ceiling and one in
the middle of it.

---

# 7. AND THE FIRST CUT OF THE HOLD STUCK TO ITS QUARRY, WHICH RICK FOUND IN THE CLIP

> *"9 seconds into that video. really weird physics on paradox colliding with
> the stunned opponent."*

He is right, and it is the one thing about the hold that was structurally
wrong. A held ball keeps the vector it was captured with — §5.2, and his own
call — but **a held ball's velocity is a MEMORY, not a motion**, and
`_ballPair` was feeding it straight into the relative-velocity term. With the
stored vector pointing away from the caster, `p` came out near zero or the
wrong sign, so the caster did not bounce off. **It stuck to the thing it had
just frozen and slid along it.**

Measured, the two builds, 36 fights, at exactly the quantity the eye was
seeing:

```
                 hold frames in contact   contacts   mean     longest
first build                        6.9%         89   0.097s     2.067s
ships                              0.8%         88   0.014s     0.142s
```

**2.067 seconds is the entire hold.** One whole freeze spent welded to the
quarry.

Two lines. The exchange reads a held ball's velocity as **zero**, and against
an immovable object it fires **only when the two are actually approaching** —
the equal-mass branch swaps normal components whatever the sign, which is its
own quirk and is left exactly alone, but doubling that quirk against something
that cannot move drives the caster back in one frame after the next. Both are
byte-identical in any match without a hold in it, and `engine_ab` is 2760/2760
again.

`paradox_relic_probe [6]` carries it as a permanent check with his sentence
quoted in it.

**AND NOTHING IN THE REPO COULD HAVE FOUND IT.** It moves no win rate worth
seeing, files no error, breaks no invariant any probe was asserting, and the
relic probe was 30/30 with it live. It is a PICTURE fault — the second one this
project has had that only a person watching could see, after v42's silent
ultimate.

---

# 8. THE ART TOOK TWO CUTS AND THE SECOND ONE WAS RICK'S IDEA

**Cut one read as a wobbly polygon**, not as lightning. The diagnosis is the
useful part: one sine is a wobble. What separates a wobble from an arc is
high-frequency detail on top of a low-frequency wander, so the beams are three
frequencies summed and windowed by `sin(pi·t)` so both ends pin to the vertex
exactly and the corners stay corners. Four strokes rather than one — a bloom,
the school's blue, a near-white core, and a second core on a different phase —
because light is many strokes and a line is one.

**Cut two is Rick's:** *"how about we add lightning lines that connect from the
hexagons edges to the center?"* And he is right about what was wrong. **A ring
hung in the hall with nothing joining it to the relic reads as a thing the HALL
is doing; the same ring wired back to the shell reads as a thing the RELIC is
doing**, and this is the caster's ultimate.

**They flicker, and that is the point.** Six permanent spokes are a wheel — a
drawn diagram. An arc is intermittent, so each spoke is gated on its own phase
and four or five of the six are lit at any moment. The gate is deterministic off
`m.t`, the way `SHAPES._t` is: an accumulated phase would strobe against the
frame interpolator, and lightning is the worst possible thing to learn that on.
They start at the shell, not the centre — a line drawn to `f.x, f.y` impales the
ball.

## 8.1 THE CHARGE IS THE PICTURE

There is no bar and no number. The beams brighten, thicken and go jagged as the
charge fills, and settle back when the quarry gets clear. **This ultimate spends
most of its nine seconds doing nothing that lands**, which is the exact case
rule 1 exists for: if the window does not say what it is doing, it reads as a
window in which nothing happened.

`paradox_field.py` photographs it at four moments of its own cycle, and the
frames are **solved for** rather than guessed at — the run steps until the
charge is inside the band the pane asks for. The first cut of the cold pane
caught the field at `F.t = 0.01` and photographed an empty hall, which read as
"the field is invisible when the charge is cold". It was not; it was not up yet.

---

# 9. THE SOUND LANDED ON THE FIRST ATTEMPT, AND THAT IS THE PROCESS AND NOT LUCK

v42's cast voice took **four serial round trips to fail** and two spreads to
land. This one was offered as a spread first: `field_lab.py` renders six casts
into one wav and four holds into another, through the shipping chain at a
non-zero `currentTime`. **Rick: "first option on both."** One round trip, and
the sound that ships is the one that was written first — which is not an
argument that the first guess was good, it is an argument that the spread is how
you find out cheaply.

```
the cast   a capacitive snap, a fast down-glide, then a field that BUZZES
           four times at an irregular 0.36-0.39s
the hold   a bright tick, a short body, a drop, and then nothing at all
```

## 9.1 A FIELD CANNOT BE HELD WITH THESE HELPERS, SO IT IS RE-STRUCK

`_tone` ends on `exponentialRampToValueAtTime(0.0001)` over its whole length, so
a "sustained" 1.35s tone is **1% of its own level by 0.85s in**. v42 said this
in one line — *"an exponential release spends its last third under the audible
floor"* — and it is why `_growl` had to be a new builder.

**A relic build does not get to add one.** So the field pulses instead: four
strikes of 108 / 162 / 324 Hz, a harmonic stack rather than a cluster, which
reads as ELECTRICAL rather than as the drone Rick rejected for the score. The
324 is what survives a laptop.

## 9.2 TWO KNOWN AUDIO BUGS ARE NOT FIXED HERE, DELIBERATELY

`_burst` does not loop its 0.6s noise buffer, so **every `_burst` longer than
0.6s in this game plays silence for its tail** (v42 §12). `_tone`'s frequency
automation is un-anchored (v42 3d), measured at 0.4–3.4 points of band shift
across four shipped voices.

Both bite exactly what a sustained electrical hum needs. **Fixing either is a
chain-wide change to shipped sound on twenty-four relics and is Rick's call, not
a slip-in** — so this relic's voice is written INSIDE the safe envelope instead:
every burst under 0.6s, the sustain carried by `_tone`, and
`paradox_relic_probe [10]` renders the result and measures it.

## 9.3 AND THE FIRST METRIC FOR "IS IT A STATE OR AN EVENT" WAS GAMEABLE

The check divided late-window level by the sound's own PEAK, and the cast scored
**worse than the Aegis control for having a louder attack** — a metric that
rewards a quiet transient is v42 §3c arriving from the other side. Replaced by
`audible` against the two controls, rendered over the same 3.0s and thresholded
the same way: **cast 2.45s, Aegis 1.50s, Converse 1.50s, hold 1.20s.**

---

# 10. THE DIRECTOR, AND A NUMBER THAT IS NOT THIS RELIC'S FAULT

**The Stasis Field deals no damage.** Nothing about a hold is a hit, so nothing
else in the frame files anything and `cinePlan` would score the most legible
moment of the ultimate as empty air. A hold files a beat now — rule 3, fifth
relic running — written to a list the simulation never reads.

**And then the pick tool came back with one candidate out of 340.** Measured
rather than assumed, over 48 fights each on the same foes and seeds:

```
relic          any cut   FATAL cut   mean cuts   best beat
axiom              62%         23%        1.06        2.04
gravemourn         56%         23%        0.62        2.00
redflail           46%         19%        0.48        2.23
PARADOX            38%         12%        0.52        1.82
thornwake          38%         10%        0.44        1.77
foregone           23%          8%        0.27        2.17
```

**A fatal cut is rare for every melee relic in this game.** Paradox is on the
low side of a band that runs 8% to 23%, and the reason is structural rather than
this relic's: `cineScore`'s big multipliers are closing speed and flight
distance, and a melee relic that lands one blow every six seconds has neither.
It is named here, not fixed — `CINE.floor` is a chain-wide number.

---

# 11. WHAT THE PROBES CAUGHT THAT NOTHING ELSE WOULD HAVE

- **A blow on a Twinshade COPY fed the charge while the real quarry was already
  held** — one frame in six thousand. `!foe.shade` is the guard, and reading
  `f.shade` is how every branch in this build asks whether a body is a relic or
  a picture of one.
- **The killing blow fed a charge with nowhere to go.** Two frames in seven
  thousand, found by a check that asserts the field stops asking when the quarry
  is dead.
- **The builder wrote unbalanced comment delimiters once** and the only signal
  was the page failing to load — a twenty-second Playwright timeout with a
  stack trace. `one()` counts `/*` against `*/` now.
- **`chain_audit` could not see this builder's inserts at all**, because its
  regex did not allow a raw-string prefix and every `*_NEW` here is `r'''`. It
  reported *"no *_NEW inserts found"*, which is the right message for the wrong
  reason and would have been read as a pass by anyone in a hurry. One character.
- **`verify.py` fails an ult tip over 72 characters** and nothing in this project
  had ever hit it. The first card was 73.

## 11.1 AND ONE CHECK WAS WRONG THREE TIMES BEFORE IT WAS RIGHT

The claim was *"a stun does not lock a flail, it DROPS it"* — the chain branch
runs during a stun where every other mode sits behind `else if (f.stun > 0){ /*
weapon locked */ }`.

1. **Contacts in a 2s window.** The flail expects 0.15 of one, and two types
   came back with the stunned arm AHEAD. Underpowered, not wrong — noise.
2. **The arc the weapon turns through, over 2s.** Divergence: the two arms are
   identical up to the stun and chaotic after it, and at 2s the calibration row
   stopped holding.
3. **The same arc over 1.0s**, with the extension horizon left long because
   recovery is slower than the thing that caused it and is read off one arm.
   Four rigid types come back at 0.92–1.07x of a 0.20s stun. That is the
   control, and without it the flail's number is a number.

**And the hypothesis was then refuted.** A stun costs the flail the same SWING
it costs everything else — 0.91x, inside the rigid band. The head coasts through
it and the coast pays for the respin. **What it costs is REACH:** path 1.07x
against swing 0.91x, extension from 0.86 to a floor of 0.58, and **1.08 seconds
to climb back** — so a 0.20s hex stun is a ~1.28s event of shortened reach on
this type, roughly six times the stun.

**A new engine fact fell out of the control row.** The greatsword reads 0.45x,
and it is the only type in the game whose facing is not an integral of its own
spin: `mode:"swing"` recomputes `theta = aim + sin(swingPhase) * arc` every
frame, and `aim` keeps tracking a moving ball while the fighter is stunned.
**A stunned greatsword's blade keeps turning.** It lands nothing, and every
measurement taken off `theta` moves. Nothing in the tree had recorded that.

---

# 12. THE FLAIL IS HEAVIER THAN THE GREATSWORD AND CANNOT CASH IT

`flail_survey` §4, and it belongs to the type rather than to this relic. Outcome
read off the EFFECT and then checked against the mass model, whose decisive
threshold is a literal inside `resolveClank` and is read off the shipped source
rather than copied:

```
foe           type         mass  margin  clanks/min   won  deadlock  lost  bind→hit
emberedge     greatsword    3.0   0.154        21.7    0%      100%    0%      1.55
censer        warhammer     5.0   0.272        15.6    0%        0%  100%      2.08
slagheart     flail         3.6   0.000        11.3    0%      100%    0%      2.94
```

**The flail against the greatsword is 0.1537 and the threshold is 0.16. It
misses by six thousandths**, over 112 binds, 100% of them deadlocks — the
second-heaviest weapon in the game cannot win a bind against a 3.0. It loses
binds to exactly one weapon, the 5.0 warhammer, 96 of 96.

---

# Open decisions

1. **THE CARD IS STILL A PLACEHOLDER.** *"For 9s, rings itself in lightning —
   linger inside and freeze for 2s"* (67 of 72 allowed). Rick's wording is one
   of the seven things this project asks him for and it has not arrived.
2. **A HELD WEAPON IS STILL A LEGAL THING TO BIND AGAINST.** `_clankPair`
   returns only when BOTH sides are stunned, so the caster can spend a hold it
   cast clanking a weapon that has stopped — 22 binds over 27 holds. It is
   priced INTO the +42% (the pin was measured with it live) and it is named
   rather than fixed, because `A.pin > 0 || B.pin > 0` is a change to the bind
   and the bind belongs to every relic.
3. **`_burst` DOES NOT LOOP AND `_tone` IS UN-ANCHORED.** §9.2. Both are live,
   both are measured, and both are chain-wide changes to twenty-four shipped
   voices.
4. **PARADOX GIVES THE DIRECTOR A FATAL CUT IN 12% OF ITS FIGHTS.** §9. Inside
   the 8–23% band every melee relic lives in, and the reason is that
   `cineScore`'s multipliers are closing speed and flight distance. Chain-wide.
5. **THE GREATSWORD DEADLOCK IS SIX THOUSANDTHS FROM BEING A WIN.** §12.
   Nothing in the game reads that margin.
6. **A STUNNED GREATSWORD'S BLADE KEEPS TURNING.** §11.1. Seven relics.
7. **`cell_survey`'s occupancy column has now mispriced two cells** — the umbral
   row (v40 §4.1) and this one. It is the wrong readout for a status that is a
   rate and the tool does not say so in its own output.
8. **`STATUS.ward.bank 0.55 / cap 90` are still unswept.** Vigil od 4, now with
   three points on the type axis — `flail_survey` §5 measured the flail banking
   fine at 1.0, like the warhammer and unlike the bow.
9. **Every type-level measurement still wants a `--noult` pass.** v38 od 5, v39
   od 5, v40 od 6, v41 od 4, v42.

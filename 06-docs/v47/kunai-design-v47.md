# v47 — THORNSHEAR / THE WINNOWING. §1 in Rick's words, and §1 PRICED — four sentences, four measurements, two refutations, and one of the refutations is the sentence the whole relic turns out to be.

**2026-08-30, Cowork.** The split is Rick's and explicit: **Cowork plans and
prices, Claude Code builds.** Nothing here was written before it was measured,
and nothing in the build brief beside this document should be started before
`tools/kunai_probe.py` has been re-run at the tip.

```
tools/twinblade_survey.py    the type, before the design existed        20/20
tools/kunai_probe.py         §1 priced BEFORE A BUILDER IS OPENED       11/11
02-chain/sc-paradox-ignition.html   the build of record, 25 relics
```

---

# 1. §1, IN RICK'S WORDS

> *"green twinblade forgoes its blades for leaf kunai. the kunai shoot off in
> both directions rapidly as a projectile. the kunai ricochet off walls and
> clanks and turn to try to hit again. kunai grow and empower after they
> ricochet and gain bonus damage and high knockback."*

Amended twice, unprompted, within the hour:

> *"the kunai ricochet shouldnt be steering. natural and predictable ricochet
> physics"*

> *"instead of 2 kunai. lets do a fan of kunai and really turn the number of
> projectiles up so the ricochet shots have a better chance of connecting"*

**The first amendment is the more important of the two and it is a correction
of me.** I had told him "turn to try to hit again" would be the first steering
thing in the game. It would not — `tickShots` has carried `s.home` since
Bloodhunt, with a rate limit and a curved trail, and the comment in it names
exactly which sentence it is breaking. He read the correction and went the
other way anyway: no homing, pure reflection. That is the right call for this
relic and §5 below is why.

---

# 2. WHAT IS ALREADY OWNED, AND WHAT IS ACTUALLY NEW

**Read the whole roster before trusting a subset** — v43 §15, applied to
mechanics rather than to names:

```
Quarrelstorm   Ironhail    a NOVA of 14 arrows, spread 6.283 = a full circle
Ironbloom      Slagheart   9 shards, shardBounce 3, life 2.6, r 11 —
                           "shrapnel bounces the hall"
Harrowing      Lastlight   12 scythes, bounce 2, that stick and burst
Bloodhunt      Marrowdraw  an 8s window of homing bolts that pierce and FORK
Thicket        Vinesower   8 seeds that root where they land
```

**A fan of projectiles is Quarrelstorm's. Bouncing projectiles are
Ironbloom's. A sustained firing window is Bloodhunt's.** Built literally and
without the fourth sentence, this ultimate is a recombination of three things
already on the board.

**The fourth sentence is unclaimed, and nothing else in the game comes near
it.** Ironbloom's shards are constant across their three bounces. The
Harrowing's scythes are constant. Bloodhunt's forks get **weaker** — `forkDmg
0.5`, `forkRMul 0.55`. So the only precedent for a projectile changing after it
resolves once is one that decays.

> **A kunai that grows, hits harder and shoves harder every time it comes off
> something is the first thing in this game that gets STRONGER the longer it
> stays in the air.**

That is the relic. Everything else in §1 is delivery. The build should spend
its art budget accordingly — §8.

---

# 3. SENTENCE 1 — "FORGOES ITS BLADES." THE BILL IS 4.46 DMG/S, AND I HAD IT WRONG.

A 4-second window at t=12s, same seeds, `w.blades` emptied against blades live.
Emptying `blades` is what the sentence means in this engine: `bladeSegments`
returns nothing, so `tickHits` lands nothing, `_clankPair` finds no crossing,
and `tickShots` has no segment to parry with. One mutation reaches all four,
which is why it is the right one — three separate suppressions would be three
chances to disagree.

```
4s window          my blows   dealt   clanks/min   stagger eaten   foe blows   taken
blades live           0.188    2.76         20.0          0.139s       0.182    2.77
blades gone           0.000    0.00          0.0          0.067s       0.273    4.47
```

**I expected the avoided binds to be a saving.** `twinblade_survey` §3 measured
this type losing 100% of every bind it takes, so a relic with no blades out
looked like a relic that stops being thrown around. **Refuted.** Damage taken
goes UP, 2.77 -> 4.47 a second, because a bind you LOSE still costs the foe a
swing. Twenty binds a minute were worth more as interruption than they cost as
stagger.

> **THE ULTIMATE'S BILL IS 4.46 DAMAGE A SECOND: 2.76 of output it stops
> dealing plus 1.70 of damage it starts taking.** Everything below is graded
> against that number.

---

# 4. SENTENCE 2 — "IN BOTH DIRECTIONS", AND THE FAN. FREE, AND ONE TRAP.

```
arm                             mode  shots loosed  per second
no w.shot (ships)               spin             0       0.000
w.shot grafted on               spin            69       1.874
```

**`tickFire` gates on `f.w.shot`, not on mode.** v39 open decision 4, inert for
six sessions because no non-bow has ever carried a shot. This design is what
makes it load-bearing, and a twinblade with a `shot` fires with no special case
anywhere in the engine.

**And `spawnShot(f, angle)` already takes an angle** — `const a = angle ===
undefined ? f.theta : angle`. Both directions, and any fan width, are
`spawnShot(f, f.theta + off)` in a loop. Nothing about the projectile system
changes.

## 4.1 THE TRAP, AND IT IS THE PICTURE-FAULT KIND

```js
spawnShot(f, angle){
  const S = f.w.shot;
  if (this.shots.length >= CONFIG.shot.maxLive) this.shots.shift();
```

**`maxLive` is 64 and `spawnShot` honours it by DELETING THE OLDEST LIVE
SHOT.** On a bow that is invisible — a shot near the cap is a shot about to
die on a wall anyway. On a bouncing kunai with a three-second life it is **one
vanishing in mid-air**: no error, no invariant broken, no win rate moved, and
only a person watching can see it. That is v42's silent ultimate and v43's
stuck hold, a third time, and it is entirely foreseeable rather than
discovered.

**The Bloodhunt fork branch already solves it and says why** — *"maxLive is a
ceiling on objects in flight and spawnShot honours it by shifting the oldest
out. THIS path must not."* It declines to spawn instead. **So must this.**

---

# 5. SENTENCE 2b — "REALLY TURN THE NUMBER OF PROJECTILES UP" IS REFUTED. THE FAN IS A LOOK KNOB.

Every arm below is the same 4s cast, same seeds, 16 foes across all four modes,
bounce 3, life 3.0, speed 420, r 10, blades off for the window:

```
arm                                loosed  refused  peak  landed  hits/cast  after a bounce
fan 1  cadence 0.10  (2/volley)      7094        6    64    1742      18.15          70.8%
fan 3  cadence 0.15                  8634     6270    64    1960      20.42          70.6%
fan 5  cadence 0.25                  8270     6970    64    1839      19.16          69.8%
fan 9  cadence 0.45                  7722     7704    64    1776      18.50          73.3%
fan 9  cadence 0.90  (18/volley)     7326     1296    64    1736      18.08          68.8%
fan 5  cadence 0.60  spread 1.6      6720        0    60    1681      17.51          72.8%
```

**A nine-fold range of fan width lands within x1.17 of itself.** More kunai is
not more damage.

**The reason is the type.** `twinblade_survey` §2 measured this weapon turning
**6.47 rad/s**, the fastest in the game by 66%. The volleys are loosed off
`me.theta`, so between two volleys 0.25s apart the weapon has turned 1.6
radians. **The spin is what sprays them; the fan only widens a volley that was
already sweeping.**

This is v43 §4.2's finding arriving in a different costume — the hexagon was a
picture and the RADIUS was the mechanic. **Here the fan is a picture and the
BOUNCE is the mechanic**, and that is a licence: pick the fan for how it looks,
because it does not decide anything else.

What did move it:

```
bounce budget 0 -> 3       1034 -> 1839 landed      +78%
kunai radius 10 -> 20      1839 -> 2000 landed       +9%
life 3.0 -> 6.0            1839 -> 2083 landed      +13%
speed 420 -> 260           1839 -> 1767 landed       -4%
```

---

# 6. SENTENCE 3 — "RICOCHET OFF WALLS." THE STRONGEST SENTENCE IN §1.

The census, over the shipped code paths, with the kunai allowed to resolve past
the end of the cast rather than counted while still in the air:

```
foe mode    loosed   landed  parried    wall  expired  in flight  peak/64  refused
ranged        1910    23.2%    14.1%    0.2%    43.0%      19.5%       64     1930
swing         2230    21.0%    28.7%    0.0%    26.6%      23.7%       64     1600
spin          2150    21.8%    20.3%    0.0%    34.6%      23.3%       64     1640
chain         1980    23.2%    12.4%    0.1%    34.3%      29.9%       64     1800
ALL           8270    22.2%    19.3%    0.1%    34.3%      24.1%       64     6970
```

**v40 measured 82% of every arrow in this game spent on a wall. A bouncing
kunai spends 0.1%.** The sentence takes the modal fate of every projectile in
this game and turns it into the mechanic.

**And it moves the death somewhere no projectile here has ever died: EXPIRY, at
34.3%.** The source carries `bow_survey` §4's finding in a comment — *"a shot
travels 1292 units in its life and the longest wall is 800, so `life` has never
once expired in this game."* `shot.life: 3.4` has been dead config on all five
bows since v40, and v43 refused to add a sixth dead knob while that one was
unchased. **This ultimate makes two dead knobs load-bearing at once.**

## 6.1 THE FIRST CUT OF THIS CENSUS WAS WRONG AND THE ERROR IS WORTH KEEPING

It stopped counting at the end of the cast window and classified **66.3% of
every kunai as "in flight"** — a census that never saw two thirds of its own
population, with every share in it wrong. The fix is a tail: keep stepping,
blades back on, nothing more loosed, until the last kunai has resolved.

**A census with an open category that large is not a census.** Anything that
reports a residual over a few percent is measuring its own horizon.

---

# 7. SENTENCE 4 — "GROW AND EMPOWER AFTER THEY RICOCHET." CONFIRMED, AND IT IS THE RELIC.

This is the sentence that was flagged as most likely to break, on the exact
precedent of v43's *"enemies that stay inside the hexagon for too long"* —
which measured **0.0 events a minute** and had to be replaced with a charge.

It measures the opposite.

```
bounces used, over every kunai that resolved
       0       1       2       3      4+
   17.8%   23.7%   39.2%   19.3%    0.0%          mean 1.60

69.8% OF EVERY LANDED KUNAI ARRIVES HAVING BOUNCED AT LEAST ONCE.
1034 landed with no bounce budget -> 1839 with three.  +78%.
```

**Seven in ten connections are ricochets.** The growth is not decoration on top
of an ultimate; it is what the ultimate mostly does.

**One hard constraint: a budget above 3 is inert.** `bounce 6` and `bounce 3`
return identical numbers at life 3.0 — nothing reaches a fourth bounce, because
`life` runs out first (each bounce costs 12% of speed: `s.vx *= 0.88`). **The
binding constraint is life, not the budget**, so the growth schedule has
exactly three rungs unless life goes up. At life 6.0 the landed count rises to
2083 and the post-bounce share to 73.7%.

**The schedule should therefore be designed for three rungs and priced at four**
— see the build brief's sweep.

---

# 8. SENTENCE 4b — "HIGH KNOCKBACK." FREE ON A CLOCK, PAID FOR ON ITS OWN CONDITION.

v41's warhammer survey found that type throwing its quarry out of its own
reach, and the twinblade has the shortest reach in the game. The first
instrument applied one synthetic shove at a fixed clock time:

```
knock  separation at  peak separation  time to touch again  never touched
    0            321              616                2.83s            38%
  450            321              593                2.61s            31%
```

**Nothing. Flat, and slightly the wrong way.** That is v43 §7 exactly — the pin
that read -12% fired on a clock and +42% fired on its own condition. **An
instrument that fires where the mechanic does not measures something else.**
This weapon cannot reach past 130 units and already sits at a mean separation
of 321 in a 520x800 hall: it is *already* out of reach, and one shove cannot
take it further out.

Fired where the mechanic fires it — on every landed kunai, along the kunai's
own travel, the way `s.knock` already works:

```
knock   landed   dmg/cast   separation in window   peak   blades touch again   never
    0     1839      290.3                    293    533                1.40s     52%
  120     1808      283.8                    325    563                2.34s     51%
  260     1648      263.3                    329    573                2.41s     51%
  420     1716      266.5                    341    577                2.53s     43%
  700     1740      270.0                    352    597                2.71s     37%
```

**Knockback shoves the quarry out of its own kunai stream**, and it is the
ULTIMATE that pays: -7% of the ult's own damage, and the dead time before the
blades reconnect after the cast nearly doubles, 1.40s -> 2.71s.

**Rick took 260**, which is the middle of the measured band: separation 293 ->
329, blades back at 2.41s.

---

# 9. THE PARRY. RICK TOOK THE LITERAL READING, AND IT IS THE BOLDER ONE.

`tickShots`' parry calls itself *"the piece that makes ranged fair AND
legible"* and it is the only answer any relic in this game has to a
projectile. §1 says the kunai ricochet off **clanks**. Three readings were
priced and put to him:

```
                                     what it costs
deflect, no growth       a blade resets a kunai's aim, nothing more
deflect AND empower      the only counterplay to this ultimate feeds it
parry kills it           ~1 in 5 kunai handed to melee foes, half of §1 lost
```

> **"Deflect and empower."**

**So a blade that bats a kunai makes it bigger, harder and heavier.** It reads
brutally well — the enemy's own defence feeding the thing killing them — and it
is the sharpest expression of §7's finding, which is that this relic is the
first thing in the game that gets stronger for staying in the air.

**IT HAS A COST AND IT IS ALREADY MEASURED.** Parry rate by foe mode: **swing
28.7%, spin 20.3%, ranged 14.1%, chain 12.4%.** A greatsword bats away nearly a
third of every kunai loosed at it, and a foe cannot choose not to have a
spinning weapon.

**AND IT POINTS THE SAME WAY THE SCHOOL DOES, WHICH IS THE REAL RISK.**
`twinblade_survey` §4: entangle is worth **-33.1%** of a swinging foe's blows
at cap and **+3.3%** against a bow. So the channel is worth most against
greatswords, and now the ultimate is too.

> **REGISTERED PREDICTION, to be falsified at build time: this relic's
> win-rate spread across the roster will be the widest of any relic in the
> game, strongest against the seven greatswords and weakest against the five
> bows.** If the finished relic's per-foe spread is inside the existing band,
> that prediction was wrong and the concentration argument in this document
> should be struck rather than explained away.

---

# 10. THE NAMES, AND WHAT IS STILL OPEN

**THORNSHEAR.** Rick's, from four offered. Thorn plus shear, the same
construction as Thornwake, and it names the two blades rather than the
ultimate — which is right for a relic whose ultimate is the thing it does when
the blades are gone.

**THE WINNOWING.** Rick's, from four offered. The harvest step where the crop
is thrown into the air and the wind sorts it: things flying, scattering and
coming down. The register was read off all twenty-five ult names rather than
off verdant's three, which is v43 §15's rule doing its job.

**ONE COLLISION, FLAGGED BEFORE HE CHOSE AND TAKEN ANYWAY.** Lastlight's ult is
**the Harrowing**, and harrowing and winnowing are both agricultural processes
ending in -ing. In a roster of twenty-five they will read as a pair. That is
his call, on record, and it is not to be relitigated at build time — but the
CARD and the callout should lean on what the Winnowing does rather than on the
word, because the word is doing less work than usual.

Of the seven things this project asks him for, **five are answered** — the
cell, the ult mechanics, the two forks, and both names. **Two are open:**

- **the SCRUNCH CARD.** 72 characters including the numbers; `verify.py`
  enforces it and v43 hit the limit for the first time in the project.
- **the ult ANIMATIONS and the SOUND.** Both as spreads, rendered, before he is
  asked anything — v43 §8's rule, which landed the Stasis Field's voice in one
  round trip against v42's four.

**And §5 says the fan is a look knob**, so the fan width, spread and cadence
belong in the animation spread rather than in the sweep. That is the licence
the measurement bought.

---

# Open decisions

1. **THE THREE-RUNG CEILING.** §7. Nothing reaches a fourth bounce at life 3.0
   because each bounce costs 12% of speed. Either the growth schedule is three
   rungs, or `life` goes up and the ultimate lasts visibly longer in the air.
   Priced either way in the build brief's sweep; the choice is a picture
   decision as much as a balance one.
2. **A PARRY NOW EMPOWERS, AND THE SCHOOL AND THE ULT NOW POINT THE SAME WAY.**
   §9. Named with a registered prediction rather than pre-emptively fixed,
   because a spread that turns out to be inside the existing band is not a
   problem and should not be pre-solved.
3. **`spawnShot` SHIFTS AT `maxLive` AND EVERY OTHER CALLER STILL DOES.** §4.1.
   This build must decline instead — but Quarrelstorm looses 14 at once and
   Ironbloom 9, and neither declines. Chain-wide, not fixed here.
4. **THE CENSUS TAIL IS A GENERAL LESSON.** §6.1. Any probe in `tools/` that
   counts objects with a lifetime needs a horizon past the event, and nothing
   in the repo checks for an oversized residual.
5. **`cell_survey`'s occupancy column has now mispriced a third cell** — see
   the survey doc §5. Third session running.

# v40 — VINESOWER / THE THICKET. The twenty-second relic, and the wall spent.

**2026-08-20.** Rick: *"alright lets build another one. how about a bow this
time?"* → survey, choice, §1 in his words, build, sweep, tune.

```
02-chain/sc-vinesower.html         <- THE RELIC
02-chain/sc-vinesower-frame.html   <- THE BUILD OF RECORD
built off 02-chain/sc-foregone.html                  d2a36d41f4803520
01-live UNTOUCHED, still on sixteen

bow_survey            25/25    the four open bow cells, before the choice
verdant_bow_probe      7/7     the chosen cell, deep
vinesower_probe        38/38    one check per sentence of §1, the camera, the reach
vinesower_pick          —       which fight is worth filming, cut list AND garden
vinesower_sweep         4/4     staged, and the override proved against a rebuild
engine_ab           2100/2100  IDENTICAL on the other twenty-one
verify.py --n 30     13/13     Vinesower 50.3%, spread 15.9pp, 0/6930 timeouts
chain_audit          18/18     every insert survives to the tip
07-shorts/v40/vinesower-v-grudgebearer.mp4  seed 3928777967, 45.0s, won on 3%
                                          NO FIGHT CARD — the scrunch, and only it
```

---

# 1. THE RELIC

**VINESOWER.** Rick's, offered against four of mine and better than all of
them for a reason none of mine had: it names BOTH halves of the relic. The bow
**sows** — that is the ultimate, and no other relic in the game does it — and
what grows is a **vine**, which is the part that fights. Quickthorn, Coppice
and Briarcast each named the planting or the plant; this names the act and its
consequence in one word, in the `-er` register the roster already runs on.

The id matches the name. `oathwound` displays as Goreshard and `redflail` as
Threshmaw; two drifts are two traps and a third was not worth the twenty
minutes it took to avoid.

Verdant × bow. Physics are Ironhail's, Farwarden's and Aureole's exactly: all
four bows now share one `shot` block byte for byte and the TYPE owns it. The
school owns Entangle 2 and the green, and `SHAPES.bow`'s verdant branch has
drawn this relic since before it existed.

```
dmg 15.6   reach 54   spin 2.8   mass 1.6   mode ranged   onHit entangle:2
THICKET  charge 15   seeds 8   sprout 1.0   vineLife 9.2   maxVines 10
         reach 205   turn 5.2rad/s   aware x1.7   windup 0.20s
         whipDmg 2   whipCd 1.4   whipKnock 260   lash 0.30s
```

---

# 2. §1 IN RICK'S WORDS, AND WHAT IT DOES TO THE SURVEY'S HEADLINE

> *"for a duration the bow fires out seeds instead of arrows. the seeds deal
> normal damage if they hit another ball. or disappear if clanked. however if
> they stick to the wall they take root. after a short time the bloom into a
> flowering plant with a vine whip that reaches out and strikes at the enemy
> if they come close enough. vine whips should have good but limited range so
> several can swipe at the enemy at the same time. the vines cannot be damaged
> or removed by the enemy. the vines stay for a duration and then wither and
> die. the vines should have knockback. the vines should have their own unique
> whipping sound effect."*

The survey's headline was that **82% of every arrow this game has ever fired
ends on a wall**, that the wall is worth ten times any status on this type,
and that nothing in twenty-one relics addressed it.

**This ultimate does not mitigate that number. It spends it.** 83.9% of seeds
root — the survey predicted 82.2% for arrows and the two agree without either
being told about the other. The waste channel is the payload.

---

# 3. WHAT WAS FREE, AND IT WAS TWO OF THE NINE SENTENCES

A seed is a `shot` with one flag. "Disappear if clanked" is what the parry
already does to any projectile; "normal damage if they hit another ball" is
what the hit branch already does through `resolveHit`. **No code was written
for either**, and the probe proves the branch ORDER by standing a seed on a
blade AND past the wall line at once and checking that nothing roots.

"The vines cannot be damaged or removed by the enemy" is free in the strongest
available sense: a vine is not in `a` or `b`, so `tickHits`, `tickClank` and
`tickShots` cannot see one. There is nothing to exempt. Handed the foe a full
ultimate charge every frame for 45 seconds, **zero vines were removed by
anything but their own clock or the cap**.

## The zero-burden argument, kept structurally

All state is `m.vines` and `f.ultBloom`, empty and null on every other relic.
`tickVines` returns on its first line. **engine_ab 2100/2100 identical on the
other twenty-one ids** is the proof.

## The one thing that had to be invented

**A vine is a WALL and a position ALONG it, not an (x, y).** `CONFIG.collapse`
walks `m.inset` 0 → 140 over a fight, so a plant rooted at 10s would be buried
outside the room by 40s and lashing from off-screen. Recomputing the
perpendicular coordinate from the current inset every frame costs two lines
and turns the collapse into part of the mechanic — the survey measured
separation halving 252 → 148 as the walls close, so the garden closes on the
fight exactly as the fight compresses. Asserted: **every plant, every frame,
6.00 units from its own current wall.**

---

# 4. THE SWEEP HAD TO BE REWRITTEN TWICE AND BOTH REWRITES ARE THE FINDING

## 4.1 Stage A was measuring truncated gardens

The first cut swept `reach` × `vineLife` at the placeholder `dmg`, the relic
won **92-100% of every cell**, and nothing in the grid reached 2.2 armed
plants in reach at once. That read like a hard ceiling and was written up as
one, with a perimeter argument behind it:

```
in-reach ~= 2*sqrt((reach+R)^2 - d^2) * N / 2640
```

**It was a confound.** Fights ending in twenty seconds were being scored on
gardens that had not finished growing. `dmg` is bisected to a near-even relic
before the read stages now, and the same grid reaches **2.28**. The ceiling
was the measurement.

## 4.2 Stage B was pricing a ratio against a denominator it had pinned

The second cut swept `whipDmg` × `whipCd` at that hold and reported the vine
SHARE — 61-74%, unreachable at any setting. Also arithmetic rather than
balance: a share measured against a blade that is not the shipping blade is a
statement about the blade. **Every cell bisects `dmg` to an even relic and
reports the share at that point.**

## 4.3 And then the two stages turned out not to be separable

At the garden stage A picked — 26 plants, 20 whips a cast — the ultimate won
at **every** `whipDmg` down to the bisection floor, because what wins is
twenty hit stuns, not the damage on them. So stage A hands stage B three
CANDIDATE gardens and B solves garden × price jointly, over a cooldown axis
widened to 3.2s specifically to buy fewer, harder whips.

```
   garden whipDmg  whipCd  dmg@50%    win  vine dmg  several  whips/cast
    90/20       2     3.2    12.12    62%       35%      56%        15.0
    90/26       2     1.4     9.12    50%       51%      72%        20.9
   110/14      14     3.2     2.38    75%       90%      22%         8.1
```

**The whip does 2 damage.** That is not a weak vine, it is where the value
sits: every lash is a `resolveHit`, so it is also a hit stun, a knockback and
two stacks of Entangle. The vines do not kill the quarry, they hold it —
which is the sentence this school has been built on since Thornwake.

---

# 4b. THE VINES WERE DRIVING THE CAMERA. RICK CAUGHT IT OFF A CLIP.

> *"the vines shouldnt trigger the director at all i think"*

He was right and the size of it is the surprise. Every lash goes through
`resolveHit`, and `resolveHit` files a CINEMA beat — so ~15 two-damage whips a
cast were being handed to the director as dramatic events, and its crowd rule
was grouping them into "volleys". The first shortlist this session produced
read `volley — 20 blows traded, for 164` on fights whose blows were plants.

The same sixteen fights, with the guard live and with it defeated by one line
on the prototype:

```
                  beats  hit beats  lashes   cuts  volley cuts
guard live          451        274     436     12            6
guard defeated      884        707     436     27           24
```

**61% of the hit beats this relic handed the director were lashes, and 24 of
its 27 cuts were volleys the vines had manufactured.** The camera was filming
the garden instead of the fight.

`_cineVine` is set only around the Thicket's own strike, exactly the way
`_cineShot` is set around a projectile's, and it suppresses the beat and
nothing else — the lash still crits, stuns, entangles, shakes the hall and
makes its own noise. The same 436 lashes land either way.

**THE FATAL ONE IS EXEMPT, and that is a deviation from what Rick said.**
Measured first: **a lash lands the killing blow in 30% of Vinesower's kills.**
Under a literal reading those fights would carry no KILL cut at all and the
clip would simply stop. "Do not let fifteen small hits drive the camera" is a
different claim from "do not film the finish" — but it is his call, and it is
open decision 1.

## And the clip tool could not have done the two-step render it advertises

`cinema_clip.py --capture-only` then `--encode-only` deletes the frames it is
about to read: the `for f in tmp.glob("*"): f.unlink()` at the top of `main()`
ran unconditionally. Its own `--help` documents the split flow. It has been
broken for as long as it has been needed, because the flag only matters at
resolutions where one pass does not fit. Guarded now.

---

# 4c. THREE NOTES OFF THE SECOND CLIP, AND ALL THREE MOVED THE BUILD

> *"the vines should have motion and tracking. currently they look stationary
> and damage the enemy ball when it happens to run into them. i was picturing
> living vines that reach out and slash"*
>
> *"i also think it may be spawning too many of them. how about instead of
> firing for a duration it loads up a fixed number of seeds and fires them
> until they deplete."*
>
> *"also with less vines i think we can afford to make them longer"*

## The first was a mechanic, not an art problem

A vine used to resolve the instant the quarry crossed `reach`. **The strike had
no duration** — so nothing on screen ever reached, and the only honest reading
of the picture was a hazard you walked into. Adding motion to the art would
have been decoration over a mechanic that did not have any.

It has three states now and they have three silhouettes:

* **WATCHING.** The head tracks the quarry from `reach × 1.7` out, at
  5.2 rad/s, and the stem leans after it. Measured: a plant that can see the
  quarry points **16.4° off it** and is **77% committed** toward it. A
  stationary plant — the thing in the clip Rick was looking at — sits at 90°
  with lean 0.
* **COILING.** 0.20s of wind-up, the leaves folding back along the stem and
  the flower brightening, with its own sound. Every slash is preceded by one
  and the probe asserts it: **0 uncoiled slashes of 265.**
* **SLASHING.** It releases on the bearing its head is pointing **at the
  moment of release**, not where the quarry was when it decided. So the
  wind-up can be left, and **17% of slashes now whiff** — which is the thing
  that makes the ones that land read as aimed rather than as proximity.

## The second is a better design than the one it replaced

`dur` is gone; `seeds` is a magazine. A duration is a number the viewer cannot
see, and it was silently eating seeds: **12.0s of every window was spent
stunned and 16.5s frozen**, and under a clock those were seeds nobody could
watch go missing. Now every loaded seed is fired or the match ended on it, and
the probe reconciles the two: **266 fired + 46 still in an open magazine = 312
loaded.**

## The third is a trade, and it is priced

**8 seeds instead of ~20 plants, and reach 205 instead of 90.** The perimeter
arithmetic is why one buys the other:

```
in-reach ~= 2*sqrt((reach+R)^2 - d^2) * N / 2640
```

Halving the count wants the reach up by about the same factor to hold the read,
and the read held: **54% of strikes still have 3+ distinct plants inside 0.6s.**

**IT COSTS COVERAGE.** The garden reaches 67% of the hall where 26 short vines
reached 42%. That is what "less vines, longer" spends, it is reported rather
than optimised away, and it is the clause of §1 — "good but **limited**
range" — most under strain in this build. When 250 and 205 finished level on
the read after pricing, the tie broke on reach for exactly that reason.

---

# 5. WHAT THE RELIC IS MADE OF

```
source                   damage   share    hits   share
the arrow / the seed        44%             36%
the bow itself (melee)      28%             21%
THE VINES                   28%             43%
```

Two fifths of the contacts and a bit over a quarter of the damage, at **50.3%
across 231 pairings** — and the roster's spread is 15.9pp, the tightest it has
been.
v38 found a third of Bloodmill was a mechanic nobody designed by asking
exactly this; v39 shipped without asking it.

## Several at once, as a number

"At the same time" is not simultaneity to the 1/120th — with independent
cooldowns two plants coinciding to the frame is rare even when four are
lashing at one ball. Measured as DISTINCT plants striking within 0.6s:

```
  1 plant  22.6%     2 plants 32.1%     3 plants 23.3%
  4 plants 16.0%     5 plants  3.8%     6+        2.2%
```

**54% of strikes have three or more distinct plants inside one perceptual
beat** — off eight seeds, where the first build needed twenty-six plants to
manage 56%. §4c is the trade that bought it.

---

# 6. A CARD THAT WAS TELLING THE VIEWER A NUMBER THE WEAPON DID NOT HAVE

The first build's tip said `Fires seeds for 5s`. The sweep moved `dur` to 8.1
and the tip went on saying 5s, because **nothing in `verify.py` checks that a
number in an ultimate's tip is a number the ultimate has** — it only asks that
a tip exists. `tip_audit.py` does exactly this for STATUS tips and there is no
equivalent for ultimates. The tip is substituted from `%DUR%` now and
`vinesower_probe` asserts every number in it against the ult's own fields.

**That check belongs in `tip_audit.py`, for all twenty-two relics.** It is not
there yet.

---

# 7. THE TRAPS v39 LEFT, RE-ASSERTED ON A BUILD THAT ADDED A `shot` AND A CLOCK

1. **`tickFire` still gates on `f.w.shot`, not on mode.** A `shot` hung on a
   melee greatsword fires 56 arrows in 30s. Vinesower did NOT trip it — it is
   `mode:"ranged"` and no melee relic carries a `shot`.
2. **`hitStop` still freezes every clock in `tickStatus`** — and the new vine
   clock obeys the same rule: one free step costs it exactly `dt`, ten frozen
   steps cost it nothing.

---

# Open decisions

1. **A FATAL LASH STILL FILES A BEAT.** §4b. Rick said the vines should not
   trigger the director *at all*; 30% of this relic's kills are landed by a
   vine, and under a literal reading those fights lose their KILL cut. The
   exemption is one `|| fatal` and it is trivially reversible.
2. **ENTANGLE ON THE WHIP IS MINE, NOT RICK'S.** §4.3. It is what routing
   through `resolveHit` produces, and at 15 whips a cast it is the largest
   thing in this relic that §1 did not ask for. The alternative is a second
   damage path, which this codebase has refused four times.
3. **`tip_audit.py` should check ULT tips against their own data.** §6. One
   relic's tip is fixed; twenty-one are unaudited.
4. **`dur` is 8.1 seconds.** A fifth of a fight spent firing seeds instead of
   arrows. Swept, not chosen — it is what fills `maxVines` at the bow's
   cadence — but it is long for a window and nobody has watched a clip.
5. **A POSTING CUT EXISTS NOW — but no VO.** v39 shipped without one at all;
   this one has `07-shorts/v40/thicket-v-widowmaker.mp4`, seed 12199668,
   picked by `vinesower_pick.py` on cut list AND garden. Still no voiceover:
   `cinema_vo.SPOKEN` has no entry for "Vinesower" or "Thicket", both compounds
   Kokoro will run into one cluster, and the 338 MB models are not in the tree.
6. **`01-live` is SIX relics behind.** v27 open decision 1, the oldest open
   thing in the project.
7. **`shot.life: 3.4` is still dead config on every bow.** v40 survey od 3.
   The Thicket does not use it either — a seed reaches its wall in 11% of it.
8. **The runic mirror problem is now a verdant one too.** Three verdant
   relics; Vinesower should not be shown against Thornwake or Heartwood.
9. **`cell_survey`'s umbral row is suspect on all six types.** v40 survey od 3.

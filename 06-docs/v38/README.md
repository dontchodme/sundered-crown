# v38 — THRESHMAW and BLOODMILL. The twentieth relic.

**2026-08-20.** The bloodsworn × flail cell, designed from Rick's words and
built the same session. The design capture is
`-bloodsworn-flail-design-v38`; the look-first probe that ran before any of it
is `-bloodsworn-flail-look-v38`. This is what shipped and what it cost.

```
02-chain/sc-redbarb.html    428860147c4570da   the razor tips, art only
02-chain/sc-redflail.html   07d4c845732cfe72   <-- BUILD OF RECORD CANDIDATE
built off 02-chain/sc-twinshade-scrunch.html 859692484ce77e0f
01-live UNTOUCHED

flail_relic_probe   17/17    on the tuned build
engine_ab           1710/1710 IDENTICAL field for field on the other 19, twice
                              (once for the art, once for the relic)
verify.py --n 40    13/13    0/7600 timeouts, spread 14.7pp, mean 38.1s
director_diag       Bloodmill 15.53x -> 2.16x ex-kill; Triplicate 1.69x unmoved
flail_sweep override checked against a real rebuild: 380/380 identical
```

Tools written: `flail_probe.py`, `contact_rate_probe.py` (restored + `--noult`),
`chain_len_sweep.py`, `barb_probe.py`, `barb_build.py`, `windup_probe.py`,
`flail_build.py`, `flail_relic_probe.py`, `flail_sweep.py`, `flail_strip.py`.

---

# 1. WHAT IT IS

```
id redflail · Threshmaw · bloodsworn · flail · reach 96 width 22 spin 2.2
mass 3.6 · mode chain · onHit {hemorrhage:2} · dmg 25.0 (swept)

ult BLOODMILL · kind "spinstorm" · charge 16
    PHASE 1  WIND-UP. The drive ramps 1x -> 6.9x over `ramp` 0.9s and the head
             fires when it ACTUALLY reaches 0.97 of CONFIG.chain.maxAngVel.
             The caster keeps fighting throughout. Measured wind-up: median
             0.75s, min 0.36, max 2.94.
    PHASE 2  THE SPRAY. 40 spikes a second for 5s, emission angle = f.headAng,
             so the sweep IS the spin. ~155 spikes a storm, peak 45 live
             against CONFIG.shot.maxLive of 64.
    BROKEN BY true stuns only -- hex, ult freeze, the Harrowing's burst.
tip "Winds the head up, then throws bleeding spikes for 5 seconds"   60 of 72
```

## What was free, and it is the larger half

*"the spikes dont bounce but expire when they hit anything"* is `tickShots`'
**default**. `s.bounce` undefined skips the bounce branch; the spent branch
kills a shot on any wall. Spinning weapons already parry shots and the build
already argues why — *"an ultimate that cheated the rules its own weapon lives
under would teach the viewer that the rules are decorative."* **Nothing about
the projectile had to be written.** Ironbloom's `shardBounce: 3` is the
exception, not the rule, and Rick's sentence described the rule.

## What was new

A two-phase ultimate whose release condition is a **physical state of the
weapon** rather than a clock, and a **continuous emitter**. Every volley in the
game before this was a single burst.

## The zero-burden argument, kept structurally

    ALL STATE LIVES IN `f.ultSpin`, WHICH IS null ON EVERY OTHER RELIC.

`tickSpinStorm` returns on its first line when neither fighter has one. The one
edit not behind that guard is the chain drive multiplier and it is an exact
identity at rest: `(f.ultDraw || f.ultForge ? ... : f.ultSpin ? ... : 1)` —
three nulls give 1, the expression that was already there. `engine_ab`
1710/1710 is the proof; the probe asserts it directly as well, 0 frames of
`ultSpin` across 57 matches among the other nineteen.

---

# 2. THE WIND-UP WAS 0.21 SECONDS AND THE FIX WAS NOT A FLOOR

First build: `spinMul` applied as a step change, exactly as Reprisal does it.
Measured wind-up **median 0.21s — twenty-five frames.** The release condition
was correct; there was simply nothing to watch.

The cause is in `CONFIG.chain`: **`spring` is 26 against `follow` 5.2**, so the
spring drags the head onto a new drive almost immediately. A step change is
absorbed before the eye can see it.

The obvious fix is a minimum-duration floor — `draw`, which is what Reprisal
carries. **That was the wrong fix here** and the difference matters: a floor
would mean the head reaches full speed and then *waits*, so "when it reaches
full speed" stops being true. Instead the DRIVE ramps, 1x to 6.9x over 0.9s,
and the release stays physical. Median wind-up is now **0.75s**, p10 0.56,
p90 0.92.

The negative control is Gravemourn: on the same chain with no such ultimate,
`|headAngVel|` means 2.30 and peaks at 11.42, and spends **0.0%** of frames
above 90% of the ceiling. The release condition is not a state ordinary play
visits.

---

# 3. WHAT BREAKS IT — AND THE MEASUREMENT THAT CHANGED THE ANSWER TWICE

The first answer was "any interruption loses the cast". Measured before
building it — 80 matches, 2,461 seconds — the caster takes **0.745 hitstun
events a second** and a 1.2s uninterrupted window exists only **47%** of the
time. `takeHitstun` runs on every blow from anything, so that rule would have
lost roughly half of all casts.

The second answer was a stun budget. Rick's third and final one is the right
one: *"Hitstun shouldnt stop the windup. but true stuns from ults/abilities
should."*

**That distinction is not in `f.stun`** — every source writes the same field —
so it is drawn at the APPLICATION SITES, and there are exactly three:

```
  hex                     STATUS.hex.stunFor        Spellbreaker, Axiom
  ult freeze              u.freeze                  Thornwake, Heartwood
  the Harrowing's burst   u.stunBase + u.stunPer    Lastlight
```

Five relics of twenty, so **the counter is nameable** — a viewer can learn who
shuts this down, which a budget could never have offered. Ordinary hitstun and
the clank stun are deliberately not in that list: they still zero the chain
drive, so being beaten on DELAYS the wind-up. Delay is not cancellation.

Marking sites rather than adding a parallel `hardStun` timer is deliberate: a
second clock would be a second source of truth about being stunned and the two
would drift the first time anybody added a stun.

**The negative control is the point of the harness block.** Sixty hard
hitstuns applied back to back during a wind-up, cast survives. Without it, a
build where everything cancels passes every positive check.

Measured on 188 natural casts:

```
  released 162 (86%)
   16   8.5%  wind:  the hex takes the wind out of it
   10   5.3%  storm: the hex takes the wind out of it
    6   3.2%  storm: the blades burst and the wind goes out of it
    3   1.6%  wind:  it never gets up to speed
    2   1.1%  wind:  the blades burst and the wind goes out of it
```

Only the wind-phase rows are duds — a storm cut short already fired. **21 of
188 = 11.2%, and 18 of those 21 are a named counter.** The Harrowing's rate was
11.5% and undiagnosed; this is the same number with a reason attached. The hang
guard fires 1.6% of the time, so hitstun almost never defeats the wind-up
outright.

---

# 4. WHAT THE RELIC IS ACTUALLY MADE OF — AND IT IS NOT WHAT THE DESIGN CLAIMED

At the type's own damage (43.3, the mean of the two shipped flails) Threshmaw
won **75.4%**, against Gravemourn's 43.8% and Slagheart's 50.1% on identical
physics. `decomp.py` isolates the channels one at a time, dmg held constant:

```
  everything on                   75.4%
  spikes deal ~0 damage           61.8%    -13.6pp
  storm does not speed the arm    67.8%     -7.6pp
  no ultimate at all              54.7%    -20.7pp
```

Two findings, and the second one is uncomfortable.

**(a) A THIRD OF THE ULTIMATE IS A MECHANIC NOBODY DESIGNED.** `spin` feeds
`f.theta += spin * dt * f.spinDir` as well as the head, so for the whole storm
the melee weapon swings 6.9x faster. That came free with the existing `spinMul`
hook and is worth **7.6pp**. It is now a separate knob, `stormMul`, defaulting
to `spinMul` so it is inert until somebody sweeps it — and it is an open
decision, because Rick's words describe the head winding up and say nothing
about the arm still being flailed at seven times speed for five seconds
afterwards.

**(b) THE HEMORRHAGE UPTIME IS WORTH ESSENTIALLY NOTHING.** Spike damage is
13.6pp and the arm speed-up 7.6pp; together they are 21.2 against a total of
20.7, which leaves the bleed and the hitstun the spikes apply at **−0.5pp,
inside the noise.**

That contradicts the design's own stated rationale. The look-first probe found
the relic's hole — hemorrhage held ≥2 stacks only 41% of a fight against 52%
and 59% for the school's other two — and the argument for this ultimate was
that it buys uptime at the cap. **It does buy the uptime. The uptime does not
buy the fight.** The likely reason is that during the storm the foe is already
pinned at 4 stacks by the melee, which is 6 dps of a 300 hp pool overlapping
damage that was landing anyway.

This is recorded rather than smoothed over. The ultimate is still good and the
relic still reads; what is false is the sentence that justified building it.

---

# 5. THE BLADE — 25 AGAINST THE TYPE'S 43.3, AND THAT IS A SHAPE THIS ROSTER HAS

Swept on pinned seeds, 19 foes × 40 seeds = 760 matches a candidate:

```
   dmg   43.3   36    30    28    26    25    24    22
   win   75.4  69.3  58.4  56.7  53.3  48.9  50.4  47.0
```

SE is about 1.8pp, so 25 and 24 are one point rather than two. **25 taken.**

`flail_sweep.py` prints its own warning at the bottom of that table — *"a
column that only reaches 50% far below those is not a tuned flail, it is an
ultimate with a flail attached"* — and the honest answer is that this IS that,
and it is legitimate. **Lastlight carries 17.5 on the scythe profile where
Thornwake carries 31.35: 56%. This is 58%.** Two relics whose ultimate is most
of what they are, both paying for it in the blade, arrived at independently.

Whole roster at 25 / spikeDmg 3.0, n=40, all 190 pairings:

```
  Threshmaw 48.2%   spread 15.0pp   mean duration 38.2s   0 timeouts
```

`verify.py --n 40`: **13/13**, 0/7600 timeouts, every relic in band
(Gravemourn 44.9% .. Grudgebearer 60.9%, spread 16.1pp), every pairing 18–70s,
overall mean 38.1s.

**The sweep's runtime override was checked against a real rebuild**: 380
matches, identical field for field. An instrument standing in for another
instrument is a guess with a table around it until it is compared.

---

# 6. THE ART, AND THE SOUND

## The tips

`_fhBarbed`'s seven tips were filled `p.core` circles of radius 0.13r centred
0.08r INSIDE the barb's own vertex — spanning 1.73r to 1.99r against a barb
terminating at 1.94r. **The dot was capping a point that already existed.**

The replacement is v37 §8.3 applied again: a FILLED path (a stroke has a cap
and a cap is blunt at any width), CONCAVE edges (convex reads as a thorn,
straight as a triangle, concave as honed), continuing the barb's own tangent at
the vertex — 1.07 rad off radial, because these barbs hook hard and a radial
point would read as a spike glued onto a hook. Length laddered at 1:1 and taken
at **0.30r** after Rick asked for shorter; below 0.24 it stops being a spike.

`_needle` is factored out because **the spikes this relic throws are the barbs
it wears**. A barb's tip is cut from the barb's own Bézier and a thrown spike is
not, so the construction is not shared — only the look, which is all they have
in common.

## Bloodmill's voice — four branches

Rick: *"something guttural and bloody"*.

**Guttural is not simply low** — a low sine is a heartbeat. What makes a sound
guttural is BEATING: two detuned sawtooths a few hertz apart, whose difference
frequency the ear hears as a growl rather than as two notes. The detune here is
**proportional**, so the beat rate climbs with the pitch and the growl tightens
into a whine as the head comes up to speed. The wind-up, stated in the one
dimension the ear reads better than the eye.

Three stages rather than one ramp, because `_tone`'s gain only ever decays — a
swell has to be built from overlapping events each starting louder than the
last. Timed to `ult.ramp` so sound and picture arrive together.

`redflail-release` is a wet snap with no ring-out. `redflail-mill` is one quiet
beat every 0.23s — forty spikes a second cannot each have a voice, that is a
machine gun, not a mill — varied by `p.n`, the real spike count, so it is
deterministic and a render reproduces. `redflail-break` is the wind-up run
backwards: the pitch falls where it rose and it ends wet and short.

**Mill gains were set from the render, not from taste.** At 0.085/0.075 the
mill was inaudible under the wind-up — twenty-two events that may as well not
have been written.

---

# 7. TWO CORRECTIONS THAT OUTLIVE THIS RELIC

**(a) The published contact-rate table counted ultimates as contact.** Two
flails with byte-identical physics returned 0.141 and 0.196 hits/s with damage
pinned; with ultimates suppressed, 1.6% apart. `contact_rate_probe.py` pinned
damage and even guarded on within-type spread, but never suppressed the ult, so
the guard was reading the ult. Restored to the tree with `--noult`. Corrected
ordering puts the **flail last, not fifth**, and turns v36's reach-dominance
finding into a tie.

**(b) Six instruments stepped 1/60 where `CONFIG.physics.dt` is 1/120.** v37
found this and it recurred here: `flail_probe` and the restored
`contact_rate_probe` both shipped wrong and were fixed before any number in
these documents was quoted. Every tool written this session reads dt from
CONFIG.

---

# 8. THE DIRECTOR, AND THE FIX v37 BUILT COULD NOT HAVE WORKED HERE

Rick, on watching the first clip: *"this ult needs the same new rules as the
last one. directior will probably always see this ult as a big exchange and we
need to tell it to only highlight big exchanges relitive to how many hits this
ult usually produces."*

He was right and it was far worse than Triplicate ever was:

```
                        before     after
  Bloodmill, all cuts   15.53x      3.92x
  Bloodmill, ex-kill    14.08x      2.16x
  Triplicate, ex-kill    1.69x      1.69x    unchanged, to the digit
```

**78% of every cut in a fight landed inside 19% of its seconds.** Triplicate's
was 4.59x when Rick called it distracting.

## Why v37's exception was inert, and how that was found

`o.crowd` read `this.shades.length > 0`. **A spike storm has no shades**, so
`crowdVolleyMin` was never consulted. Swept at 8, 14, 20, 28 and 40 it returned
**15.53x at every value, to the digit** — the same signature v37 got, and the
same lesson: a knob that moves nothing does not need a bigger number, it is not
connected. The build's own comment had predicted the case — *"False in every
match without a summon in it, which until this relic was all of them."*

Connected, it still plateaued at 11.90x, because **12 of the 23 non-kill
in-window cuts were single hits** and a grouping rule cannot touch a single hit.

## The score bar is the right tool here and was the wrong one there

v37 built exactly this for Triplicate and correctly abandoned it. The
distributions say why:

```
  crowded    mean 0.68  med 0.50  p95 2.07  | >= floor 6.29%  2.57 beats/s
  ordinary   mean 0.53  med 0.46  p95 1.29  | >= floor 0.65%  0.80 beats/s
```

A Triplicate's beats score IDENTICALLY to ordinary ones and are merely 2.7x more
frequent — *"no level can thin a population that differs only in rate."* A
storm's beats score genuinely higher and nearly TEN TIMES as many clear the bar.
**Same symptom, opposite cause, opposite fix.**

## Three things this got wrong before it got it right

1. **A percentile is useless at n≈14.** A storm contributes about fourteen
   crowded beats to a match, so a p90 is the twelfth of fourteen and moves in
   whole-sample steps: swept, it went 13.37x → 12.08x and stopped. It is a
   MEDIAN times a multiplier now, which is also the more faithful reading of
   "relative to how many hits this ult usually produces" — that is a statement
   about the centre of a distribution, not its tail.
2. **Folding the strength into `o.crowd` set Triplicate's to zero** and
   silently reverted v37's fix to 4.59x. `crowd` is a boolean the volley rule
   reads; `crowdMul` is a separate strength each ultimate declares. A relic can
   want the volley rule and not the score bar, and Triplicate is that relic.
3. **Volleys carried a boolean**, so a volley inside a storm reached the filter
   with `crowd === true` and was judged at median×1 — the exception doing
   nothing for exactly the beats it was built for.

Also: the first cut of the crowd condition wrote `shades[0].owner === f` inside
the fighter loop, which looked tidier and put Triplicate back to 4.59x. **Do not
tighten a condition another relic depends on without measuring that relic.**

## The value, swept

```
  crowdMul      5      7      9     10     11     13
  ex-kill    5.18x  3.45x  2.59x  2.16x  0.86x  0.86x
```

**10 taken** — the last value above parity. v37's argument transfers exactly:
1.00x would be wrong, because the ultimate does put more real spectacle on the
floor; what it no longer does is out-bid the rest of the fight.

## THE CLANK LOCK, and it costs nothing

Rick: *"make bloodmill grant immunity to losing clanks so it never reverses
direction while its casting"*. A clank flips the loser's `spinDir` — and both,
when it is not decisive — so a flip mid-cast reverses the spray inside one
ultimate. That is the same incoherence that made a fixed screen direction
impossible to build against.

**It buys direction, not safety**: the clank stun is untouched. Threshmaw was
48.2% before it and **48.3%** after.

---

# 9. THE POSTING SHORT

`07-shorts/v38/threshmaw-v-twinshade.mp4` — 57s, 1080x1920, -15.0 LUFS, cold
open + card + bm_lewis VO, `--shorts` delivery encode. Seed 18392971: two
Bloodmills and a Triplicate, none broken, the two set-pieces 1.4s apart.

`cinema_vo.SPOKEN` gained `Threshmaw -> "Thresh maw"` and
`Twinshade -> "Twin shade"`; both are compounds Kokoro otherwise runs into one
cluster. The line renders at 3.96s against a 4.0s card.

**One finding from picking the seed, and it is an open decision.** In a
Threshmaw v Twinshade fight **65% of all beats are crowded**, because both
relics crowd the floor and `crowdMul` takes the max across them — so Bloodmill's
bar is applied to beats that are really Triplicate's. Cut counts across 120
seeds:

```
  crowdMul 0 (off)   0 cuts x11   1 x62   2 x42   3 x4   4 x1
  crowdMul 10        0 cuts x51   1 x61   2 x8
```

The kill-cut rate is 12% at every value, so the exception is not what makes this
matchup thin — that is the matchup. But halving the cut count of the marquee
fight is a real cost and nothing has been decided about it.

---

# 10. THE CARD CAME OUT, AND THE SCRUNCH TOOK THE JOB

Rick, on the first posting cut: *"this still has the old intro card after the
cold open. the idea was to cut that and let the scrunch handle it so the action
never stops."*

**`--cold-open` never removed the card, it MOVED it** — which is precisely what
v32 §6 measured when the departure spike moved with it. Dropping `--intro`
entirely removes it, and the scrunch was already built to take over: it arms on
the first clank, eases the hall to `k=0.7` over 0.42s, holds 3.0s, eases back,
and **nothing in the simulation stops**.

**The panel carries more than the card did.** The card was two names and a tip
behind an 80% scrim over 58% of the frame. The scrunch panel is both relics,
both statuses and both ultimates with their full descriptions — the legend for
everything that is about to happen — under a fight that is still running.

```
  threshmaw-v-twinshade.mp4          57.0s   card + cold open
  threshmaw-v-twinshade-nocard.mp4   52.9s   no card, VO on the scrunch (10.6s)
  threshmaw-v-twinshade-open.mp4     52.9s   no card, VO over the opening  <- POSTING
```

**The 4.1s difference is exactly the freeze.**

The change exposed a second thing: the voiceover was hardcoded to `adelay=300`,
300ms into a card that no longer exists. `cinema_clip` now takes `--vo-at`,
either seconds or `clank`. `clank` is MEASURED, not computed — the director
dilates, so the wall second of the first clank cannot be derived from its sim
time. On seed 18392971 it is 10.58s of video.

## Rick's call, and it is a registered prediction

*"i think i like the scrunch coming after the v/o i feel like both might feel
like information overload. we will have to wait and see how analytics look."*

**The posting cut is `-open`**: voiceover at 0.3s over live action, scrunch panel
at 10.6s. The reasoning is separable and should be checked separately —

- the VO early because week one put the drop-off in seconds 1–6, and a deep read
  over a moving fight is a stronger hook there than an unnamed one
- the scrunch late because the two together are two blocks of information in the
  same breath, and the panel is a legend for things that have not happened yet

**Registered before the pull, in the week-one convention:** this cut removes the
card, so v32's estimate applies — killing the freeze should move r(6) from ~0.28
to **~0.45+** and leave the post-0:05 conditional tail unchanged at **0.43**.
**If the tail moves too, something else changed and it must be found before the
card removal is credited.** That prediction is v32's, carried forward unaltered.

The competing hypothesis Rick named — that VO and scrunch together are overload
— is NOT tested by this video, because only one of the two cuts is going out. If
the numbers disappoint, `-nocard` is the A/B that was already rendered.

---

# Open decisions

1. **`stormMul` is 6.9 and worth 7.6pp of a mechanic nobody designed.** §4a.
   Should the arm keep flailing at seven times speed through the spray, or drop
   back once the spikes are flying? Lowering it is 7.6pp that has to come back
   from somewhere, most likely the blade.
2. **The design's stated rationale is falsified.** §4b. Hemorrhage uptime buys
   no winrate. The relic works; the sentence that justified it does not, and
   nothing has replaced that sentence.
3. **`spikeDmg` 3.0 is unswept as an independent knob.** It was held at 3.0
   through the blade sweep. Worth about 8pp across 3.0 → 1.2.
4. **The wind-up's `ramp` is 0.9 and untested against the break rate.** A longer
   ramp is a longer telegraph AND a longer window for hex to land. Those trade
   directly and neither has been swept.
5. **`maxLive` peaks at 45 of 64 and the foe's shots share the array.**
   Threshmaw against a bow, both firing, is the case that has not been driven.
6. **No custom set-piece art.** Bloodmill has a sound and spikes; it does not
   have a `drawUltUnder`/`drawUltOver` branch, so the banner treatment is the
   generic one. Every other set-piece in the game has its own.
7. **The chain-length question is answered and closed.** `hilt` 0.50 → 0.30
   moves no balance number and moves mean head-to-ball distance by 1.6px,
   because the chain is thrown taut 83–88% of the time whatever its length —
   and a longer chain LAGS LESS (0.56 → 0.41 rad) because gravity's term is
   divided by chain length. `sag`, `spring`, `damp` and the 0.44 extension
   floor are the knobs that control the look, and none has been swept.
8. **Two crowding ultimates on one floor.** §9. 65% of beats crowded, and the
   max rule applies Bloodmill's bar to Triplicate's beats. Options: take the
   crowding SOURCE into account per beat, or accept it. Unmeasured either way.
9. **Only one of the two posting cuts is being tested.** §10. `-nocard` exists
   and is rendered; it is the A/B if the overload hypothesis needs answering.
10. **The short is 540-source upscaled to 1080x1920.** Every video on the channel
   is, so raising it now confounds the retention experiment week one is still
   running. Worth doing deliberately, between experiments.
11. **Promote to the chain tip and to live?** `01-live` is on sixteen relics
   against twenty here. v27 open decision 1, now four relics wide and by a
   distance the oldest open thing in the project.

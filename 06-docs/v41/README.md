# v41 — BULWARDEN / AEGIS. The twenty-third relic, and a shield that was guarding the wrong side.

**2026-08-20.** Rick: *"lets start on the next fighter"* → survey the grid,
survey the type, choose the cell, §1 in his words, build, refute, rebuild,
sweep, film.

```
02-chain/sc-bulwarden.html         <- THE RELIC
02-chain/sc-bulwarden-frame.html   <- THE BUILD OF RECORD
built off 02-chain/sc-vinesower.html
01-live UNTOUCHED, still on sixteen

cell_survey        7/7      the grid, re-run on the v40 tip — 20 cells open
wh_survey         23/23     the five open warhammer cells, before the choice
bulwarden_probe   44/44     one check per sentence of §1, plus the two refutations
bulwarden_sweep     —       reflect x feed, then floor x dur, blade bisected per cell
engine_ab       2310/2310   IDENTICAL on the other twenty-two
verify.py --n 30  13/13     Bulwarden 48.2%, spread 14.7pp, 0/7590 timeouts
chain_audit       12/12     every insert survives to the tip
07-shorts/v41/aegis-v-vinesower.mp4   seed 9794, 22.4s, won on NOTHING (0 hp left)
                                      NO FIGHT CARD — the scrunch, and only it
```

---

# 1. THE RELIC

**BULWARDEN.** Rick's, from four offered. Bulwark and warden: the wall, and the
one who keeps it — and it kept the word he reached for in §1 without taking it
off Lightkeeper, whose ultimate is already called Bulwark. It lands in the
register vigil already owns (Lightkeeper, Farwarden). The id matches the name.

Vigil × warhammer — **the double gap**: vigil was the thinnest school at 2 of 6
and the warhammer the thinnest type at 2 of 6, and `wh_survey.py` priced all
five open cells on the row before this one was chosen. Physics are
Grudgebearer's and Censer's exactly; all three warhammers now share one block
byte for byte and the TYPE owns it.

```
dmg 20.1   reach 76   spin 1.6   mass 5.0   knockMul 2.3   onSelf ward:1
AEGIS  charge 16   dur 9.0   floor 40   bankMul 1.0   feed 2.0
       arc 2.8 (blocked)   artArc 1.5 (drawn)   bend 0   r 26
       reflect 0.60   turn 3.0 rad/s
```

---

# 2. WHAT THE TYPE SURVEY FOUND, AND WHY IT IS THE BRIEF

Full text in `sundered-crown-warhammer-survey-v41.md`. Two things, both new:

**The hammer wins 734 of 734 binds.** Every type, no deadlocks, stagger 4.2:1
in its favour. Grudgebearer's blurb has claimed that for twenty relics and
nobody had measured it.

**And its own knockback costs it the fight.** `knockMul 2.3` is the only value
above 1.0 in the roster; a landed blow opens the gap by +22 units on a 76
reach, which is 12% of its contacts and 16 points of win rate — *unless the
ultimate takes the shove back*. Crucible pulls and is paid **+7%** for carrying
it. Consecration knocks and is still down **17%**. Same type, same shove,
opposite ultimates, opposite sign.

Aegis is a third answer and it is neither: **it does not fix the reach, it
stops needing it.** For nine seconds the relic has a damage channel that pays
out when the foe comes to IT.

---

# 3. §1 IN RICK'S WORDS

> *"Bulwark: The ult conjures a shield in front of the ball. the shield rotates
> with the weapon and blocks incoming damage. it also reflects a portion of the
> damage it blocked back to its attacker"*

Three forks it left open, all three his: the name (**Aegis**, Lightkeeper
untouched), the shield's hp (**the banked plate plus a floor**), and where the
arc rides (**on the head's side** — the literal reading).

**And then the probe refuted the third one inside an hour**, which is §4.

## What the engine gave free

`spendWard()` already existed and is already not `shatter()` with a flag —
Reprisal spends the pool as damage on one shot, and Aegis spends the same pool
as a wall. `f.spendFx`/`f.spendA` already animate plates leaving the shell
along a bearing, so the wall is visibly made of the armour that was on the ball
a frame earlier. Every projectile routes through `resolveHit`, so "blocks
incoming damage" catches an arrow and a swing in one branch and none of the
four bow relics needed a special case.

## The one thing that had to be invented

**A DIRECTION.** Every existing defence in this game is a POOL — ward, and
nothing else — and a pool does not care where a blow came from. Aegis is
decided at the CONTACT POINT, against the victim's own facing. `resolveHit` is
the only function in the engine that knows where a blow landed, which is why
the branch is there and not in `hurt()`.

**Zero burden, structurally:** all state is `f.ultAegis`, `null` on every other
relic. `engine_ab` 2310/2310 identical is the proof, not this paragraph.

---

# 4. THE SHIELD WAS GUARDING THE SIDE THE HAMMER ALREADY GUARDS

The first build shipped §1 literally: the arc rode `theta`, sweeping ahead of
the hammer. Over 67 casts it **blocked six blows and used 3.8% of the wall it
raised.**

The reason, measured over 531 incoming blows and six foes:

```
share of blows a 1.5-rad arc would cover
  riding the head            6.0%
  a quarter-turn off        27.3%
  opposite the head         35.3%
  pointed at random         23.9%
```

**A wall riding the weapon is four times worse than a wall pointed at random**,
because a weapon pointing AT the attacker *clanks* instead of being hit — and
this type wins every clank in the game. Incoming blows arrive a mean of 114°
from where the weapon points. The shield was posted on the one side that was
already covered.

Rick, given the table: *"how about this. the shield tracks the enemy ball and
always tries to face them."* **TRIES** is the load-bearing word — the turn is
rate limited at `turn` rad/s, so a quarry moving faster than that gets round
the edge, and the counterplay is something a viewer can see.

## And tracking did not beat it either, which is the second finding

```
  TRACKING THE FOE at 1.5 rad    26.4%
  TRACKING THE FOE at 2.2 rad    50.9%
```

**Facing the ball is not facing the blow.** A blow lands on the attacker's
BLADE, and a blade is long — a greatsword reaches 116 — so the contact point
sits a mean of 56° off the line to the attacker's centre. The arc has to be
wider than the thing it is facing. Width, not aim, is the fix.

---

# 4b. AND THEN THE PICTURE AND THE HITBOX CAME APART

Rick: *"we are way off base here art wise. Id like to see an actual shield. a
floating pink kiteshield."*

The first shield was the ward's own five plates, off the shell and out in
front, and the argument for it was continuity. That is an argument about where
the wall came from and it cost the thing the wall IS.

The kite is drawn instead — flat top with two corners, straight shoulders, a
taper, a point, a boss and two rivets, and it drains from the top. **And then
the geometry refused to cooperate:** a FLAT shape of length L at radius rr
subtends `2·atan(L/2/rr)`, which at rr 60 is about 85° however long it is
drawn. Bend it round the ball and it covers the full arc honestly — and stops
being a kite.

Four renders, one decision, and it is **Rick's, with the cost stated**: the
shield DRAWS at `artArc` 1.5 and BLOCKS at `arc` 2.8. Blows that visibly miss
it are stopped by it, roughly twice as often as blows that visibly hit it.

**This is the only place in the build where the picture is not the mechanic**,
and `bulwarden_probe [4]` asserts the gap is the size it is supposed to be, so
it is a decision on the record rather than something a later reader finds.

---

# 5. THE MAGAZINE WAS 80% FLOOR, AND THE CONTROL THAT PROVED IT WAS BROKEN

The wall is "the banked plate plus a floor". Measured over 88 casts:
**the pool at the cast is a MEDIAN OF ZERO**, mean 8.4 of a 90 cap.
`STATUS.ward.dur` is 5 seconds and the plate expires four times a fight, while
the ultimate fires on a charge timer that knows nothing about it. The relic
banks real armour — peak 44 a fight — and simply never happens to be holding
any when it casts.

Rick: *"feed the wall while it stands."* So while Aegis is up, `onSelf.ward`
banks into the WALL instead of the plate, at `feed` × the usual share. The 5s
clock stops mattering, and the ultimate rewards the one thing `wh_survey` says
this type is worst at — landing contacts. The shell gets nothing while the wall
stands, which is the cost: the relic comes out of its own ultimate bare.

**The first control run said the feed was worth nothing, and the control was
the bug.** The feed read `u.feed || 1`, so a configured feed of ZERO silently
measured as ONE — two configurations came back byte-identical across 100
fights, which is what caught it. With a real control:

```
floor 40, dur 9, reflect 0.6      eaten/cast   breaks/cast   reflect share
  feed 0                              36.7          0.56          17.2%
  feed 2                              42.1          0.43          19.5%
```

**+15% absorbed and 23% fewer breaks.** The mechanic earns its place; the
instrument nearly hid it.

---

# 5b. THE SHIELD LANDS 21% OF THIS RELIC'S KILLS AND THE DIRECTOR COULD NOT SEE THEM

Found the way the Thicket's version was found — off a clip with no ending.
`cinema_clip` reported *"no killing blow on this seed (timeout finish)"* on a
fight that ends 4 v 0, and fell back to "the last cut", which was 1.7 seconds
into a 42-second fight.

`hurt()` files no CINEMA beat, and the reflection calls `hurt()` directly. So
every fight decided by the shield handing a blow back was invisible to the
director. Measured: **7 of 34 wins, 21%.**

A fatal return now files a beat. **An ordinary one still does not** — it is two
events a cast and it is not a blow this relic struck, so filing it would have
the camera cut to a moment where the caster did nothing. That is the Thicket's
rule, arrived at independently, and it is the third relic to need it.

---

# 6. WHAT THE SWEEP SOLVED

`arc` was settled by the picture. What was open was what a block is worth and
what a landed blow puts back, and then the magazine against the window. Every
cell bisects `dmg` to a near-even relic before its telemetry is read — v40's
rule, because a share measured against a blade that is not the shipping blade
is a statement about the blade.

At the shipped numbers, per cast:

```
casts a fight   1.78       blocks a cast    2.27
eaten a cast    43.6       returned         26.2
wall spent      90%        broken           0.47
the shield is 17.9% of everything this relic delivers
```

120 fights, six foes, at the shipped numbers.

---

# Open decisions

1. **The picture is not the hitbox** (§4b). Rick's call, cost stated, asserted
   in the probe. It is the only such gap in the build and it should not become
   a precedent without being argued again.
2. **CLOSED. `dmg` was bisected on a five-foe subset and then checked against
   the whole field**, which disagreed: 20.9 read 50% on the subset and **55.2%
   on all 253 pairings**. Three full passes settled it — 19.6 → 47.0%,
   20.1 → **48.2%**, 20.9 → 55.2% — and 20.1 ships. The lesson is the general
   one: a subset bisection is a starting point and the full field is the
   answer, and the two were 5 points apart here.
3. **`turn` is a LOOK knob, not a balance knob.** Between 1.6 rad/s and instant
   the block rate moves by under 0.1 a cast. It stays because "tries to face
   them" is Rick's sentence and the wall swinging round is the animation, but
   nothing here is balanced on it.
4. **A kill by ward SHATTER still files no beat.** The same hole the reflection
   had, and it belongs to Lightkeeper and Farwarden too. Measured at 0 of 34
   wins on this relic, so it is not urgent — and it is exactly the kind of zero
   that stops being zero when somebody tunes the pool.
5. **`STATUS.ward.bank 0.55 / cap 90` have still never been swept.** Vigil od 4,
   now with data at both ends of the type axis and nothing in the middle. The
   cap is reached 0.6% of the time at bank 1.0 — a ceiling nothing touches.
6. **`cinePlan` scores a killing blow and then does not always cut to it.**
   Seeds 9732 and 8430 both carry a fatal beat with `'the killing blow'` in its
   `why` and neither becomes a cut, so `cinema_clip` falls back and produces a
   clip with no ending. Pre-existing, relic-independent, and it silently costs
   good seeds. `bulwarden_pick` should score on the PLAN's cut list rather than
   on its own telemetry.
7. **No VO.** `cinema_vo.SPOKEN` has no entry for "Bulwarden" or "Aegis", and
   the 338 MB models are not in the tree (`FETCH-KOKORO.md`).
8. **The fight card is still in the build.** v40 rule 1, unmoved: guarded in the
   clip tool, still written by `introcard_build.py` and still on every Match as
   `m.introT`.
9. **Rule 3's shared `cineFloor` is still not built.** v40's first pickup item,
   and this relic did not need it — Aegis files at most two beats a cast — but
   the four crowding mechanics that do need it are unchanged.

# v57 — CINDERCLEAVE, the 30th relic, and BREACH. The §1 is a lava design on the surface and a SUNDER design underneath, and that is not a reading — it is the largest single number in the file: the beams' damage is worth +1.9pp and the sunder they apply is worth +10.0pp on top of it.

**2026-09-01, Cowork.** `tools/sunder_survey.py`, `tools/sunder_knob_lab.py`,
`tools/vent_size_lab.py` and `tools/vent_count_lab.py` against
`02-chain/sc-nightfell.html`. Runtime only. Nothing is written to any build.
The harness caveat and its reproduction control are in
`sundered-crown-cell-repricing-v57.md` and apply to every number here.

Rick took **dwarven x scythe** for the 30th relic from four priced cells (v57
repricing). He then supplied the §1, ruled on the two decisions the labs put to
him, proposed the size mechanic and the count mechanic himself, and named both.

```
CINDERCLEAVE   dwarven x scythe. Blade 21, bisection start. A dwarven branch of
               the scythe art EXISTS and is 71.5% from its nearest sibling —
               3rd most distinct of the fifteen open cells. Whether it is any
               GOOD is a separate question and open decision 6
BREACH         a licence, not a clock: for up to 14s the scythe can cut the
               walls, and the FIFTH cut ends it. Each cut tears a hole sized by
               how deep the blade went. A hole fires a travelling jet of heat
               into the room every 1.1s for 9s, dealing 9 and applying 1 Sunder
```

---

# 1. THE CELL — AND SUNDER'S DURATION IS A THRESHOLD, NOT A SLOPE

`sunder_survey.py`, dwarven's channel injected onto each type's donor at its
OWN shipped damage, ultimates suppressed, 26 foes x 10 seeds an arm. Read off a
wrapped `dmgTakenMul` — the exact multiplier every blow was amplified by — and
not sampled per step, which is the proxy v39 §5.2 and v47 both caught being
wrong.

```
type       donor          dmg  blows   gap  stk@blow  0 stk  6 stk  meanMul   lift
greatsword dawnbringer   10.4   16.7  3.34      2.92    21%    26%    1.322  +26.2%
twinblade  widowmaker    11.9   15.9  3.43      2.68    24%    21%    1.295  +25.8%
bow        ironhail      16.2   13.6  3.30      2.36    25%    15%    1.260  +19.6%
----------------------- sunder's own duration is 5.0s -------------------------
scythe     thornwake     31.4    7.8  5.24      1.23    42%     2%    1.136  +11.2%
warhammer  grudgebearer  23.5    9.4  5.12      1.36    40%     4%    1.150   +7.7%
flail      gravemourn    24.0    7.6  6.28      0.99    50%     1%    1.109   +8.5%
```

`gap / dur` reads **0.66, 0.67, 0.69 — then 1.02, 1.05, 1.26.** Nothing lands
between 0.69 and 1.02. A weapon that swings faster than the status decays
compounds toward the cap in 78-89% of fights; a weapon slower than it starts
from zero on 40-50% of its blows and reaches six stacks about one fight in five.

**The scythe misses the line by 0.24 seconds.**

Two controls, both green: the pin-14 arm reproduces `row_price` exactly at
+13.8% and the shipped arm at +11.2% — two independently written injections,
identical numbers.

**The registered prediction came back RED and is recorded as refuted.** It was
*"sunder's delivered lift rises with contact rate"*; the warhammer has a
shorter gap than the scythe and delivers less (+7.7% against +11.2%). Within
the slow half the order is inside noise. The fast/slow split is not.

So, as v55 §4 found for umbral x warhammer: **the cell cannot be argued on the
channel.** But here the failure names the design.

## 1b. THE TWO WAYS ACROSS THE LINE, PRICED BEFORE A §1 EXISTED

`sunder_knob_lab.py`, thornwake donor, 260 fights an arm:

```
arm                       blows  stk@blow  0 stk  6 stk  meanMul    win    lift
no channel at all           8.4      0.00   100%     0%    1.000  52.7%   +0.0%
apply 1  (shipped)          7.8      1.23    42%     2%    1.136  63.8%  +11.2%
apply 2  (Slagheart's)      7.5      2.07    44%    16%    1.227  67.7%  +15.0%
apply 3                     7.4      2.74    42%    33%    1.301  74.6%  +21.9%
hold 7.0s                   7.6      1.72    32%     5%    1.190  62.7%  +10.0%
hold 10.0s                  7.4      2.34    23%    10%    1.258  66.9%  +14.2%
hold forever (ceiling)      7.0      2.92    15%    16%    1.322  68.5%  +15.8%
```

The hold arms move `STATUS.sunder.dur` GLOBALLY, so the four dwarven foes get
it too and those numbers are a floor, not an estimate. Even so: **an undecaying
stack reaches six on 16% of blows against a fast type's 15-26%** — so holding
the stack does convert the body, and applying more converts it further and
cheaper.

Dwarven's four shipped ultimates all treat the stack as something to SPEND or
make more of — Crucible consumes it, Slagburst detonates it, Ironbloom's
shrapnel applies more, Quarrelstorm ignores it. **Nothing in the school holds
it, and holding it is what this body needs.** Breach does not hold it either.
It does the third thing: it fills the gaps.

---

# 2. RICK'S §1, AND THE FOUR RULINGS ON TOP OF IT

> *for a duration the scythe can collide with the walls of the arena. When it
> does it tears open a hole where lava/heat beams periodically spew out and
> damage enemy fighters caught in their blast.*
>
> *The vents should be able to be torn in all directions. some flowing parallel
> or perpendicular to the battlefield. but also some torn in diagonals.*

```
RULED  the beams APPLY SUNDER                                     §3.1
RULED  "everything should shoot into the room. but all 8
        directions are possible"                                  §3.4
HIS    vent size varies with how hard the blade hit the wall      §3.2
HIS    a COUNT instead of a clock — 3 to 5 holes, then done       §3.5
NAMED  CINDERCLEAVE, and BREACH
```

---

# 3. THE PRICING

Every lab stands Thornwake in for the unbuilt relic — same shape, same mass,
same reach — pulls Thornwake from the foe field, replaces its Bramblesnare, and
leaves the 26 foes their own ultimates. **Beam damage goes through `hurt`
scaled by the quarry's own `dmgTakenMul` and never through `resolveHit`, so it
carries no crit and no parry.** Every lift below is a FLOOR.

## 3.1 THE LARGEST NUMBER IN THE FILE

```
                              vents  beams  hits    win    lift
no ultimate at all                —      —     —  43.5%       —
beams apply 1 Sunder            9.9   62.0   6.3  71.9%  +28.5%
beams apply NOTHING            11.2   71.5   7.3  61.9%  +18.5%
beams apply 2 Sunder            9.9   61.4   6.3  73.1%  +29.6%
```

The no-sunder arm lands **more** beams and is ten points worse. The beams'
damage is worth +1.9pp over the floor in the first pass at n=52 and +18.5%
here; the sunder is worth +10.0pp on top of the same beams. Doubling the
application is worth +1.1pp — flat, and not a knob.

> **BREACH IS NOT A DAMAGE ULTIMATE. It is a second contact rate running
> underneath a slow weapon**, and it carries the relic across §1's 5.0s line
> for as long as the holes are open. The lava is what it looks like. Filling
> the gaps between a scythe's slow blows is what it does.

## 3.2 A GRAZE AND A SLASH ARE DIFFERENT THINGS — MEASURED, 2,780 PASSES

Rick asked whether vent size could vary with how hard the blade met the wall.
The prior question is whether the physics makes the distinction at all. Depth
of the deepest crossing in a pass, as a fraction of the weapon's reach:

```
0.0-0.1  #########                      8.3%
0.1-0.2  ########                       7.9%
0.2-0.3  #########                      8.6%
0.3-0.4  ########                       7.8%
0.4-0.5  #######                        6.9%
0.5-0.6  ########                       7.9%
0.6-0.7  #########                      8.5%
0.7-0.8  ########                       7.7%
0.8-0.9  #########                      8.8%
0.9-1.0  ############################  27.4%   <- the buried slash
median 0.63   quartiles 0.30 / 0.63 / 0.92   sd 0.32
```

Nearly flat from a scrape to three-quarters, with a fat spike at full burial. A
quarter of passes are the full slash and a quarter are under 0.30 of the blade.
**The range is real and "graze" is not an edge case.**

Depth and dwell are NOT the same measurement (r = +0.49). Depth is the one a
viewer can read off a single frame; dwell is not. Use depth.

What the size should drive, 260 fights an arm:

```
flat (control)          +27.3%
size -> width           +30.0%
size -> life            +31.5%
size -> damage          +28.8%
size -> period          +30.4%
size -> width + life    +32.7%   <- RICK'S, and the recommendation
size -> width + damage  +31.5%
size -> everything      +38.8%
grazes tear nothing     +33.5%
```

Everything-at-once is strongest and is four knobs riding one scalar, which is
how a relic becomes untunable — the bisection would have nothing to grab.
**Width is what a viewer reads as size; life is what makes a deep cut still
matter a minute later.**

## 3.3 THE BEAM IS A JET WITH A FRONT, AND THE PICTURE COSTS ABOUT FOUR POINTS

Rick's reference frame: a jet that tapers to nothing at its origin, swells
along its length, and carries a bright crescent FRONT at the head. That is not
a line switching on, and v40's Thicket finding is the precedent in his own
words — *"the vines look stationary and damage the enemy ball when it happens
to run into them"*. A strike with no duration reads as a hazard you walked
into.

So the beam resolves **when the front reaches you**:

```
instant bar (control)        7.2 hits  +32.7%
front 1800 units/s           6.3       +29.2%
front 1100 units/s           5.9       +27.3%
front  650 units/s           5.3       +26.2%
front  350 units/s           4.5       +21.9%
taper, instant               6.2       +28.1%
taper + front 1100           5.1       +28.5%
```

Everything from 650 to 1800 is inside one SE of everything else in that range;
only the instantaneous bar and the 350 arm separate. **So the speed is free and
should be chosen for the look.** 1100 units a second crosses the hall in about
0.9s — fast enough to read as an eruption, slow enough that leaving works.

The taper pays for itself twice: it is Rick's frame, and it means the HOLE can
be small while the beam is wide, so vent size shows where the camera is looking
instead of on a wall it often is not.

## 3.4 RICK'S AIM RULE IS THE BEST ARM MEASURED AND IT IS FREE

> *"everything should shoot into the room. but all 8 directions are possible"*

It resolves without a special case: a hole fires along the perpendicular or one
of the two diagonals that lean into the hall, never along the wall it was torn
from. **Four walls x three bearings puts all eight compass directions in the
game while no single hole ever fires into empty stone.**

```
into the room, 3 bearings a wall   7.0 hits  81.9%  +38.5%   <- Rick's
even eight, parallels included     5.1       71.9%  +28.5%
straight across only               8.2       80.0%  +36.5%
```

It beats the even eight by ten points and it beats perpendicular-only, which is
the arm the numbers alone would have recommended. The two bearings he cut were
the two spending themselves on empty wall.

## 3.5 THE COUNT, AND IT IS THE STRUCTURAL FIX

> Rick: *"can we achieve better balance by only letting it open a set number of
> vents? so instead of a duration it can open 3-5 and then its done?"*

The clock version has a defect the sweep could see and did not name: **the
window's worth is contact rate, and contact rate is the noisiest thing in the
game.** A cast spent near a wall tore twice what a cast spent mid-arena tore,
so two casts of the same ultimate in the same fight were not the same
ultimate. A count deletes that.

```
                 holes a cast   win @ blade 31.35 / 26 / 22
clock, 8s             5.89        81.9%  /   —    / 56.9%
3 holes               2.97        62.3%  / 53.5%  / 44.2%
4 holes               3.77        71.2%  / 53.8%  / 45.0%
5 holes               4.59        75.0%  / 56.9%  / 53.1%
6 holes               5.37        79.6%  / 66.2%  / 56.9%
```

**MORE HOLES IS STRONGER AT A FIXED BLADE** — Rick asked and the answer is an
unambiguous yes, monotonically. What the count does NOT decide is the relic's
final strength, because the blade is bisected afterward either way. It decides
what the relic is made of: three holes and a blade near 24-25 is a heavy scythe
with an accent; five holes and a blade near 21 is a moderate scythe that lives
on its ultimate. **Rick took five.**

The safety cap is a guard rail and not a mechanic: with 14s behind it, the cap
ended the window in 0.01 fights out of one. The ball always finds a wall. "Five
holes" can be written in the tip and meant.

## 3.6 THE BLADE

```
n=5   blade  26     24     22     21*    20     19     18     16
      win  56.9%  58.5%  53.1%    —    48.5%  42.7%  40.4%  37.3%
```

**Start the bisection at 21 and expect the answer in 20-22.** The curve is
steep below 22 — three points of blade for ten points of win rate — and
flat-to-noisy above it, which is its own finding: **over about 22 the ultimate
is carrying the relic and the blade stops mattering.**

## 3.7 THE SWEEP AROUND THE CENTRE, FOR THE BISECTION'S SAKE

```
beam damage      6 / 9 / 13        +26.9 / +38.5 / +38.1%
vent life        6 / 9 / 13s       +28.1 / +38.5 / +39.6%
fires every      0.8 / 1.1 / 1.5s  +38.8 / +38.5 / +27.7%
window           6 / 8 / 10s       +31.9 / +38.5 / +40.8%
holes at once    5 / 8             +32.3 / +38.5%
charge           15 / 18           +38.5 / +27.7%
```

**Four knobs each move it about eleven points, and that is the headline for
the build.** GRASP collapsed onto one scalar at r² 0.79 and its arrangement was
therefore free; Breach does not. Beam hits landed gets r² 0.33, and the arms
furthest off the line are the ones that change what a hit *does*. **Breach is
two numbers — hits landed, and what a hit is worth — and both have to be tuned.**

---

# 4. THE TRAPS

**4.1 THE BLADE IS ALREADY THROUGH THE WALL.** `bladeSegments` runs from the
ball's surface out to `R + reach` and the ball's own centre is clamped at
`n + R`, so a scythe against a wall has up to 104 units of blade *inside* it on
most of every rotation. "The scythe can collide with the walls" is not a new
collision — it is a test nobody was running. The design's real question is
therefore never *whether* it tears but *how often it is allowed to*, and the
count answers it.

**4.2 RESOLVE THE TEAR AT THE END OF THE PASS, NOT THE START.** Tearing on the
frame the blade first crosses the plane samples the SHALLOWEST moment of the
cut — the size mechanic would have almost no range — and it needs an arbitrary
cooldown to stop a pinned ball tearing one a frame. Track the pass, keep the
deepest crossing, resolve when the blade leaves. **One pass is one vent, 10-11
a fight, and the weapon's own rotation is the spacing rule.** Measured, exactly:
`10.7 passes, 10.7 vents`.

**4.3 A VENT IS `{wall, u}` IN ARENA SPACE AND NEVER AN (x, y).** v40 §3.3,
non-negotiable here: `CONFIG.collapse` walks the inset 0 -> 140 from t=21s, so
an absolute position torn early is outside the hall by the end of the fight.
Recompute the position every frame from the CURRENT inset, exactly as
`tickVines` does.

**4.4 THE VENTS HANG OFF THE FIGHTER OR THE MATCH, NEVER OFF `m.ultFx`.**
v54 §2a, a chain-wide open item: `m.ultFx` is one slot and the opponent casting
anything overwrites it. Deadfall survived only by being rebuilt onto
`f.ultDeadfall`. Start on `f.ultBreach` for the licence and a match-owned list
for the holes — the holes OUTLIVE the licence and outlive the caster's window,
so they cannot live on the window's object.

**4.5 THE HOLES OUTLIVE THE WINDOW AND MUST NOT OUTLIVE THE MATCH.** They are
discarded on `m.over`, they do not fire at a corpse, and their clock does not
run while `m.hitStop > 0` — the sim is frozen and so is the hall.

**4.6 DO NOT BUILD THE JET ON `shots`.** `spawnShot` shifts the oldest live
entry out at `maxLive` 64 and — the real hazard — `tickShots` lets
`bladeSegments` PARRY a shot, with melee's defence winning ties. A jet of heat
that a scythe can parry is a different mechanic and nobody has decided it is
this one. Ten holes firing every 1.1s would also flood the shot list.

**4.7 THE CASTER IS NOT IMMUNE BY ACCIDENT — DECIDE IT.** Measured: beams that
burn the caster too take the relic from +28.5% to **+3.8%**, because a scythe
has to fight near walls to tear anything and therefore stands in its own fire.
That is not a balance term, it is a different relic. Placeholder: foe only.

**4.8 SHADES.** `tickShadeHits` is where v51 §4.3's bug lived and Twinshade
puts three bodies in the hall for six seconds. A jet crossing the hall will
sweep all three. Decide the rule, write it in the comment, assert it.

**4.9 THE BEAT.** v53 §4: 30 of 58 Gravemourn kills rendered a clip with no
killing blow because a hand filed `kind:"ult"` and `cinema_clip` finds the
finish with `plan.find(c => c.fatal)`. Breach can kill — its jets deal damage —
so unlike Grasp it CAN file a fatal beat, and it must. Rule 3, tenth relic
running: **the cast files a beat and each tear files its own; the individual
firings do not** — the Thicket's `_cineVine` rule.

**4.10 THE SOUND IS RENDERED AND MEASURED IN AN `OfflineAudioContext`.**
`SFX.play` returns on its first line headless and swallows its exceptions; v42
shipped a silent ultimate through every green check in the repo. Four voices
here — the wall tearing, a hole opening, a jet firing, the jet's roar while it
crosses. Render all four.

---

# 5. THE ART

## 5a. THREE ADJACENCIES, NAMED BEFORE ANYTHING IS DRAWN

```
THICKET      ALREADY PUTS THINGS ON THESE WALLS. Vinesower plants vines as
             {wall, u}, they persist, they wait, they strike. The separations:
             a vine REACHES INTO THE ROOM at a quarry that comes close and
             tracks it; a vent fires a FIXED LINE across the whole hall whether
             or not anyone is near. A vine is a limb, a vent is a hole. Green
             and organic against molten and geometric. The fixed bearing is the
             strongest of the four and it is free
BENEDICTION  a shaft of light, sanctified, on the quarry
SENTINEL     a slow beam tethered to the wielder, vigil, and one build old
```

Breach is the third linear effect in the game. The separator that is free and
strong is **multiplicity**: those two are one line owned by a wielder, this is
up to five fixed lines the HALL is firing.

## 5b. THE PALETTE, AND THE WHITE CORE IS A REAL RISK

Dwarven is `core #9C6326`, `glow #E8A34E`, `dark #2E1B0A`. That value was
chosen deliberately: sanctified and dwarven were the closest pair in the game
at CIEDE2000 8.05, they were separated on VALUE rather than hue to reach 21.19,
and the table's own comment is *"a forge is not a treasury."*

**A white-hot beam is the single thing that walks that back**, because
sanctified is `core #FFF6E2` on `glow #FFFFFF`. Rick's reference is right in
shape and hot in value. The resolution: **the white is the FRONT, not the
LENGTH** — a thin crescent at the head, with the body of the jet carried in
amber to orange and the tail falling to dark.

And the forge palette already exists in the renderer: the Crucible's `heat()`
runs `#FFB347` and `#FF6A1A` on a radial falloff. It is dwarven-coded, shipped
and measured. Build the jet's body out of it rather than a new ramp.

## 5c. FOUR STATES, AND ONE OF THEM IS THE MECHANIC

```
THE CUT      the blade sweeps through the stone. This is where the SIZE is
             decided and the frame has to show the depth
THE TEAR     the wall opens BEHIND the blade as it leaves. Sized
THE HOLE     dormant between firings, glowing, aimed. This is most of its 9s
THE JET      the front crosses the hall. 0.9s
```

The count is the other thing the art has to carry: **a viewer should be able to
tell the fourth tear from the fifth before the fifth lands**, or the ultimate
ends without having promised it. Grasp's four-knuckles problem, one relic on.
Marks on the scythe, or the hall's glow deepening per tear — a decision, not an
accident.

## 5d. FILM BEFORE YOU TUNE

v43 §13, and v54 §2c is why it is not optional: Deadfall's arming state was
invisible at alpha 0.16 and no probe in this repo could have said so. Breach
has five holes, four states each, and a jet that has to read against the hall's
own bloom. **Photograph it off a real match before tuning anything.**

---

# Open decisions

1. **THE FIVE-HOLE TELL.** §5c. Whether a viewer can see the last tear coming.
   No measured cost, real effect on whether the ending reads as earned.

2. **SHADES.** §4.8. A rule, not a knob, and the build needs an answer in a
   comment either way. Placeholder: a jet catches shades like any other body.

3. **CHARGE.** 15, the roster mode. v55b established nobody's was ever derived.
   Charge 18 costs 10.8pp here, so unlike Shroudmaul this relic IS sensitive to
   it — it is a real knob and 15 is a choice, not a default.

4. **DOES A HOLE FIRE ONCE THE CASTER IS DEAD?** Thicket's answer is yes —
   *"it withers on its own clock"*, v40 §3.3, and Rick ruled it. The same
   answer is probably right here and it is worth being deliberate about,
   because a hall still venting after the kill is a strong final image.

5. **THE TIP.** Mechanic-first, Rick's standing rule. Draft:
   *"Cuts the walls open — five vents that spit heat and Sunder"* (54/72).

6. **THE DISTINCTNESS NUMBER DOES NOT MEASURE WHETHER THE ART IS GOOD, and
   this relic should not lean on it the way the header does.** `cell_survey [3]`
   scored umbral x warhammer at 78.6% from its nearest sibling and this brief
   and v56's both wrote "THE SILHOUETTE IS NOT NEW WORK" off that number —
   and Rick rejected `_whEaten` outright at build time (*"the hammer with
   blocks attached to it just isnt working for me"*), then designed a
   replacement from reference images. **The ink mask measures separation from
   the other six schools on the same shape. It says nothing about whether the
   shape is any good.** Cindercleave's 71.5% is a lower number than the one
   that was just rejected. Look at `_scytheEaten`'s dwarven branch on a real
   frame before stage 1 rather than after stage 3b, and treat the header's
   claim as unverified until then.

7. **`STATUS.curse.tip` STILL SHIPS THE PRE-REWORK WORDING.** Open since v55,
   nothing to do with this relic, one line.

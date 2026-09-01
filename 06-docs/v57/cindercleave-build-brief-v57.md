# v57 — BUILD BRIEF FOR CLAUDE CODE. CINDERCLEAVE, the 30th relic, and its ultimate BREACH. Four separable stages, and the second one exists because it is the half most likely to be built wrong and the only half that can be checked against a published distribution before any beam is drawn.

**Read `06-docs/v57/cell-repricing-v57.md` (why this cell) and then
`06-docs/v57/cindercleave-design-v57.md` (the cell at weight, the ultimate
priced, the traps, the art) before this file.** They carry the measurements;
this one carries only what to do with them.

**The split, Rick's:** Cowork designs and prices, Code builds. Four instruments
are in `tools/`, all runtime-only, none writes to a build:

```
tools/sunder_survey.py      the amplifier at weight, six types      3/4 — one is a recorded refutation
tools/sunder_knob_lab.py    apply-more against hold-longer          4/4
tools/vent_size_lab.py      the pass distribution; what size drives 4/4
tools/vent_count_lab.py     the design centre, the count, the blade 6/6
```

```
CINDERCLEAVE  dwarven x scythe. Blade 21 to start. `_scytheEaten`'s dwarven
              branch ALREADY EXISTS — 71.5% distinct from its nearest sibling.
              LOOK AT IT ON A FRAME BEFORE STAGE 1; the number is separation,
              not quality, and a HIGHER one was just rejected on `_whEaten`
BREACH        a LICENCE, not a clock. For up to 14s the scythe cuts the walls;
              the FIFTH cut ends it. Each cut tears a hole sized by how deep
              the blade went. A hole fires a travelling jet into the room every
              1.1s for 9s: 9 damage and 1 Sunder, foe only
```

---

# 0. THE STAGES — WHERE TO START, WHERE TO STOP, AND WHAT MUST BE GREEN BETWEEN

```
 #    IN                      OUT                    WHAT CHANGES
 0    --                      --                     CONFIRM Shroudmaul's 3b landed.
                                                       This builds on top of it
 1    sc-grasp.html           sc-cindercleave.html   the 30th relic exists, its
                                                       ultimate STUBBED at charge
                                                       1e9. Blade 21
 2    sc-cindercleave.html    sc-thepass.html        THE PASS AND THE TEAR. Holes
                                                       open, sized, drawn — and
                                                       they do not fire yet
 3    sc-thepass.html         sc-breach.html         THE JETS. Front, taper, sunder,
                                                       the count of five
 F    --                      --                     FILM. Before you tune
 3b   sc-breach.html          sc-breach.html         blade bisected from 21
STOP
```

**GREEN BEFORE THE NEXT STAGE STARTS**

```
after 1   engine_ab IDENTICAL on the 29 in every match not containing Cindercleave
          verify --n 40 completes with 30 relics
          the roster sheet, the picker and the intro card all FIT 30
          Cindercleave with no ultimate lands near 33% (vent_count_lab's floor
            is 43.5% at blade 31.35; at blade 21 expect materially lower)
after 2   pass_probe 7/7 (§5a) — and this is the stage's whole point
          ONE PASS IS ONE VENT: 10-11 passes a fight, 10-11 vents, equal to
            within 0.05
          the depth distribution matches design §3.2: median 0.63, sd 0.32,
            27% of passes above 0.9. IF THIS DOES NOT REPRODUCE, STOP — the
            size mechanic has no range and the design changes
          engine_ab IDENTICAL on the 29 in any match with no Cindercleave cast
after 3   breach_relic_probe 12/12 (§5b)
          five holes a cast, and the 14s cap ends fewer than 1 window in 50
          engine_ab IDENTICAL on the 29 in any match containing no cast
after 3b  Cindercleave inside the field band; the scythe row and dwarven re-swept
```

**IF A GATE IS RED, STOP AND REPORT.** Stage 2 exists as its own commit for one
reason: §3.2's distribution is a **published prediction made before the build
existed**, and it is the only part of this design that can be falsified without
a single beam being drawn. If the built pass does not reproduce it, everything
downstream — the size mechanic, the count, the blade — is being tuned against a
lab that does not describe the game.

**FILM BEFORE YOU TUNE.** v43 §13; v54 §2c is why it is not optional. This
ultimate has five holes, four states each, and a jet crossing a hall that
already blooms.

**STOP AFTER 3b.** Naming is done. The intro-card copy is Rick's.

---

# 1. THE CHAIN

```
built off   02-chain/sc-grasp.html                <- Shroudmaul's 3b output
builders    tools/cindercleave_build.py           <- new, ALL STAGES
produces    02-chain/sc-cindercleave.html         stage 1 alone
            02-chain/sc-thepass.html              stage 2 on top
            02-chain/sc-breach.html               stage 3 on top
probes      tools/pass_probe.py                   <- new, STAGE 2
            tools/breach_relic_probe.py           <- new, STAGE 3
sweep       tools/cindercleave_sweep.py           <- new
            tools/dwarven_sweep.py                <- new; five relics after this
01-live     UNTOUCHED. Not a target.
```

`chain_audit.py --builder cindercleave_build.py` after every carry. **It
defaults to `twinshade_build.py` and will happily audit the wrong inserts and
pass.**

---

# 2. STAGE 1 — THE RELIC

```
id          cindercleave     Rick's, from a spread of four
aff         dwarven          onHit { sunder: 1 }, like three of the school's four
                             (Slagheart is the exception at 2)
shape       scythe           `_scytheEaten`'s dwarven branch exists and is 71.5%
                             from Lastlight's. LOOK AT IT ON A REAL FRAME
                             BEFORE STAGE 1 — v56 called `_whEaten` "not new
                             work" off a HIGHER number (78.6%) and Rick
                             rejected it outright at build time. The ink mask
                             measures separation from siblings, not quality
dmg         21               THE BISECTION START, not a shipped number. §3.6 of
                             the design doc: 20 reads 48.5% and 22 reads 53.1%
reach/mass  the scythe's — 104 / 2.4 / spin 3.2. Do not invent a fifth set
charge      15               roster mode. UNLIKE Shroudmaul this relic IS charge
                             sensitive: 18 costs 10.8 points
tip         "Cuts the walls open — five vents that spit heat and Sunder"  (54/72)
```

The ultimate is stubbed at `charge: 1e9` for this stage. Nothing else.

---

# 3. STAGE 2 — THE PASS AND THE TEAR, AND THIS IS THE STAGE THAT DECIDES THE DESIGN

## 3.1 The two things that are NOT what they look like

**THE BLADE IS ALREADY THROUGH THE WALL.** `bladeSegments` runs from `R - 4` to
`R + reach` and `move()` clamps the ball's centre at `n + R`. A scythe against a
wall therefore has up to 104 units of blade inside the stone on most of every
rotation. **There is no new collision to write** — only a test nobody was
running, and a rule about how often it is allowed to fire.

**RESOLVE AT THE END OF THE PASS.** Tearing on the frame the blade first crosses
the plane samples the shallowest moment of the cut, which would leave the size
mechanic with almost no range, and it needs an arbitrary cooldown to stop a
pinned ball tearing one a frame. Instead:

```
a pass OPENS      when any blade end crosses a wall plane
a pass ACCUMULATES the deepest crossing and the dwell, per frame
a pass RESOLVES   when no blade end is beyond the plane — or at passMax 1.2s,
                  the guard for a ball that is genuinely pinned
```

**One pass is one vent. The weapon's own rotation is the spacing rule.**
Measured in the lab at exactly `10.7 passes, 10.7 vents`.

A pass that changes wall closes and a new one opens — corners are two passes,
deliberately.

## 3.2 The size

```
pen01   = clamp(maxPen / (w.reach * f.reachMul), 0, 1)
k       = lerp(0.5, 1.5, pen01)
half    = 14 * k        THE WIDTH — what a viewer reads as size
life    = 9.0 * k       THE LIFE — what makes a deep cut matter a minute later
```

**`k` DRIVES WIDTH AND LIFE AND NOTHING ELSE.** Damage and period stay flat.
Driving all four is +6.1pp stronger and is four knobs riding one scalar, which
leaves the bisection nothing to grab (design §3.2).

Normalise by REACH and not by pixels, or the scalar stops meaning anything the
day reach changes.

## 3.3 A vent is `{wall, u}`

v40 §3.3, and non-negotiable: `CONFIG.collapse` walks the inset 0 -> 140 from
t=21s, so an absolute `(x, y)` torn early is outside the hall by the end of the
fight. Store the wall and the fraction along it in ARENA space and recompute
the position every frame from the CURRENT inset — `tickVines` is the pattern
and it is forty lines away.

## 3.4 The bearing — Rick's rule, and it is not a knob

> *"everything should shoot into the room. but all 8 directions are possible"*

```
pick = the eight compass bearings, keeping only those with d . n > 0
     = the perpendicular and the two diagonals that lean into the hall
     = three per wall, four walls, ALL EIGHT present in the game
```

Never the two that run along the wall the hole was torn from. That is worth
**ten points** against an even eight and it also beats perpendicular-only
(design §3.4). Draw the bearing from an integer hash of a per-vent sequence
number, **not `this.rng()`** — the house rule since Ironbloom's splinters is
that a relic not in the match must not perturb the draw order of one that is.

## 3.5 The licence

```
kind        "breach" (new)
charge      15
n           5            Rick's, from three offered
cap         14.0s        A GUARD RAIL, NOT A MECHANIC. It ended the window in
                         0.01 fights out of one. Do not tune it and do not put
                         it in the tip
ends on     the fifth tear, the cap, death, or m.over
```

**THE HOLES OUTLIVE THE LICENCE.** They keep their own 9s clock and go on firing
after the window has closed. So the licence lives on `f.ultBreach` and the holes
live on a MATCH-owned list — they cannot hang off the window's object, and they
must not hang off `m.ultFx` (v54 §2a: one slot, the opponent overwrites it,
Ironhail's 1.3s Quarrelstorm leaves an eight-second window with no art for 100%
of its frames).

---

# 4. STAGE 3 — THE JETS

```
period      1.1s      per hole
warm        0.35s     the hole glows before its first firing
life        9.0 x k
dmg         9         flat. NOT scaled by k
half        14 x k    the beam's half-width at full bloom
speed       1100      units a second — 0.9s across the hall. FREE: everything
                      from 650 to 1800 is inside one SE (design §3.3)
taper       0.25 -> 1.0 of `half` over the first 55% of the hall's diagonal
apply       1 Sunder per hit, FOE ONLY
resolves    ONCE per firing, when the FRONT sweeps past the quarry's projection
            — the interval [previous front, this front] — so a fast front cannot
            step over a ball between frames
```

**THE FRONT IS THE MECHANIC AND NOT THE DECORATION.** Rick's reference frame is a
jet with a bright crescent head, and v40's Thicket finding is his own sentence:
a strike with no duration reads as *"a hazard you walked into"*. Resolving the
whole line at once is +4.2pp stronger and it is the version he already rejected
once, on a different relic.

**DO NOT BUILD THE JET ON `shots`.** `spawnShot` shifts the oldest live entry at
`maxLive` 64, and `tickShots` lets `bladeSegments` PARRY a shot with melee's
defence winning ties. A jet of heat a scythe can parry is a different mechanic
and nobody has decided it is this one. Five holes at 1.1s would also flood the
list.

**THE SUNDER IS THE ULTIMATE.** Design §3.1: the same beams with no sunder land
MORE hits and are ten points worse. If a probe ever shows the pool of
applications flat while the knobs move, that is the symptom — check that the
jets are applying to the quarry and not the caster (v51 §4.3: do not guard on
`self === owner`).

---

# 5. THE PROBES — ONE CHECK PER SENTENCE

## 5a. `tools/pass_probe.py`, STAGE 2

1. **A pass opens on a crossing and resolves on the leaving**, never twice at
   once, and a wall change closes one and opens another.
2. **One pass is one vent** — counted off the engine's own events, equal to
   within 0.05 over 260 fights.
3. **10-11 passes a fight** at blade 21 with the licence live.
4. **The depth distribution reproduces design §3.2** — median 0.63 ± 0.05,
   sd 0.32 ± 0.05, 27% ± 4 above 0.9. **THIS IS THE STAGE GATE.**
5. **`pen01` is normalised by reach**, asserted by moving `reachMul` and
   showing the distribution does not move.
6. **A vent rides the collapse** — its drawn position is on the wall at t=0 and
   still on the wall at t=60, with the inset at 140.
7. **The bearing is never along the wall it was torn from**, over every vent in
   260 fights, and all eight bearings appear across the four walls.

## 5b. `tools/breach_relic_probe.py`, STAGE 3

1. **The licence ends on the fifth tear**, counted off events, not recomputed.
2. **The cap ends fewer than 1 window in 50.** If it ends more, `n` is not
   reachable and the design changes.
3. **Holes outlive the licence** — assert a hole still firing after
   `f.ultBreach` is null.
4. **A jet resolves once per firing**, and on the frame the FRONT reaches the
   quarry, not the frame it opens.
5. **A quarry that leaves in time is missed** — construct it and assert it.
6. **Foe only**, and asserted in a Twinshade match (§4.8 of the design doc).
7. **Every jet hit applies exactly 1 Sunder** and the stack count moves.
8. **Nothing fires after `m.over` or on a corpse**, and nothing ticks while
   `m.hitStop > 0`.
9. **Per-match state** — cast Cindercleave, then run six other-relic matches
   AFTER it in the same page session and assert nothing of theirs moved. This
   is `gravemourn_relic_probe [9d]`'s pattern.
10. **The cast files a beat, each tear files its own, the firings do not** —
    and unlike Grasp this ultimate CAN file a fatal beat, so assert that a
    jet kill produces a clip with a killing blow (v53 §4).
11. **Report holes a cast, jets fired, jet hits landed and mean Sunder stacks
    every run.** Breach is TWO scalars — hits landed and what a hit is worth —
    and one number will not tune it.
12. **THE SOUND IS RENDERED AND MEASURED IN AN `OfflineAudioContext`.**
    `SFX.play` returns on its first line headless and swallows its exceptions;
    v42 shipped a silent ultimate through every green check in the repo. Four
    voices: the wall tearing, the hole opening, a jet firing, the roar while it
    crosses.

---

# 6. THE GATES

```
engine_ab      IDENTICAL on the 29 in matches containing no Cindercleave cast
chain_audit    --builder cindercleave_build.py
verify --n 40  completes with 30; the duration-band check is KNOWN to fail at
               the tip — do not credit this build with it either way
tip_audit      Breach's tip 54/72
row_price      dwarven x scythe now filled; re-run the row AT --pin 0 (v57
               repricing, open decision 3)
frame_probe / post_identity
roster fit     30 relics through the roster sheet, the picker and the intro card
```

**REGISTERED PREDICTIONS, this build's job to falsify:**

1. *At blade 21, n 5, period 1.1, life 9.0, dmg 9, half 14 and front 1100, the
   built relic lands **48-53%** against the field.*
2. *The built pass reproduces the lab's depth distribution — median 0.63,
   sd 0.32 — within noise.*
3. *The 14s cap ends fewer than 1 window in 50.*

If (2) fails, stop at stage 2 and report: the size mechanic is the thing being
falsified, not the tuning. If (1) fails but (2) and (3) hold, bisect — the lab
resolves jet damage through `hurt` and not `resolveHit`, so it carries no crit
and no parry and **every lab number is a floor**. Expect the built relic to read
stronger than the doc and bisect down rather than arguing with it.

---

# 7. THE ART — AND THE PALETTE IS THE PART THAT CAN BE GOT WRONG PERMANENTLY

Full brief in design §5. The three things that must be settled before a pixel:

**7a. THE WHITE IS THE FRONT, NOT THE LENGTH.** Dwarven is `#9C6326` core on
`#E8A34E` glow and that VALUE is load-bearing: sanctified and dwarven were the
closest pair in the game at CIEDE2000 8.05 and were separated on value, not
hue, to reach 21.19 — *"a forge is not a treasury."* Sanctified is `#FFF6E2` on
`#FFFFFF`. A white-hot jet body walks that back. Keep the white to a thin
crescent at the head; carry the body in the Crucible's existing `heat()` ramp
(`#FFB347`, `#FF6A1A`), which is already dwarven-coded, shipped and measured.

**7b. THE THICKET IS ALREADY ON THESE WALLS.** Vinesower plants `{wall, u}`
vines that persist, wait and strike. Separations, and the first is the
strongest and is free: a vent's bearing is FIXED and crosses the whole hall,
where a vine reaches into the room and tracks; a hole against a limb; molten
geometry against green growth. Breach is also the third linear effect after
Benediction and Sentinel — the free separator there is **multiplicity**: those
are one line owned by a wielder, this is five lines the HALL is firing.

**7c. FOUR STATES, AND THE COUNT HAS TO READ.** The cut (where the size is
decided — the frame must show the depth), the tear (the wall opens BEHIND the
blade as it leaves), the dormant hole (most of its nine seconds), the jet.
And a viewer should be able to tell the fourth tear from the fifth **before**
the fifth lands, or the ending arrives without having been promised — Grasp's
four-knuckles problem, one relic on.

---

# 8. WHAT NOT TO DO

- **Do not tear on the first crossing frame.** §3.1.
- **Do not add a tear cooldown.** The pass IS the cooldown. §3.1.
- **Do not store a vent as an (x, y).** §3.3.
- **Do not let `k` drive damage or period.** §3.2.
- **Do not build the jet on `shots`.** §4.
- **Do not hang the holes on `m.ultFx` or on the window object.** §3.5.
- **Do not make the jets burn the caster** — measured, +28.5% -> +3.8%, and it
  is a different relic, not a balance term.
- **Do not scale sunder application with size or damage.** 2 stacks a hit is
  worth +1.1pp over 1; it is not a knob.
- **Do not touch `01-live`.** Eleven relics behind.
- **Do not fix `_burst` or `_tone`.** Twenty-nine shipped voices.
- **Do not let the fight card back in.**

---

# Open decisions — Rick's, and the build can start without any of them

1. **THE FIVE-TEAR TELL.** §7c. A picture decision with no measured cost and a
   real effect on whether the ending reads as earned.

2. **SHADES.** Does a jet catch Twinshade's copies? A rule, not a knob, and the
   comment needs an answer either way. Placeholder: yes, like any other body.

3. **DOES A HOLE KEEP FIRING AFTER THE CASTER DIES?** Thicket's answer is yes
   and Rick ruled it there. A hall still venting after the kill is a strong
   final image; it is also damage after death, which nothing else in the game
   does. Placeholder: yes, matching Thicket.

4. **`row_price --pin` SHOULD DEFAULT TO 0**, and this build's row re-run is the
   natural place to change it. v57 repricing, open decision 3. One line.

5. **SLAGHEART, OPEN SINCE v55b.** Ironbloom is still the only ultimate in the
   game worth less than nothing (-1.9%) and carries the second-longest charge.
   Not this relic's problem; it has now been open for two builds.

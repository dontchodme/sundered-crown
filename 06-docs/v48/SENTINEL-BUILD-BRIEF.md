# v48 — BUILD BRIEF FOR CLAUDE CODE. VESPER and the SENTINEL, priced and ready — but NOT before Thornshear lands.

**Read `06-docs/v48/scythe-survey-v48.md` and then
`06-docs/v48/vesper-design-v48.md` before this file.**

---

# 0. THE ORDER, AND THE FIRST TWO ITEMS ARE NOT NEGOTIABLE

**1. THORNSHEAR LANDS FIRST.** The chain is linear. Vesper builds off the
Thornshear tip, not off `sc-paradox-ignition.html`. Do not start this until
`sc-thornshear-frame.html` exists and passes its own gates.

**2. RE-RUN THE PROBES AT THAT TIP BEFORE YOU BELIEVE ANY NUMBER IN THESE
DOCS.** Every measurement in the design was taken against a twenty-five relic
roster; Vesper fights twenty-six. The probes are cheap:

```
python3 scythe_survey.py --game ../02-chain/sc-thornshear-frame.html
python3 row_price.py --type scythe --game ...      # the cell, re-priced
python3 beam_probe.py --game ...                   # every sentence of §1
```

**If a number has moved, the design doc is wrong and it is yours to say so.**

**3. FILM IT ON PLACEHOLDER NUMBERS BEFORE YOU TUNE ANYTHING.** v43 §13, and
this ultimate is more of a picture than the Stasis Field was. A beam that
reads as a teleport under 60fps interpolation, a pass that is too brief to
see, a tip flare nobody can locate, a sweep so slow the viewer thinks it is
stuck — every one of those passes every probe in this repo and is obvious in
half a second of clip.

**4.** Build. **5.** Probe. **6.** Sweep and bisect. **7.** Film properly.
**8.** Rick's two remaining inputs — the card, and the art and sound spreads.

---

# 1. THE CHAIN

```
built off   02-chain/sc-thornshear-frame.html      <- NOT the ignition tip
builder     tools/vesper_build.py                  <- new
produces    02-chain/sc-vesper.html                the relic alone
            02-chain/sc-vesper-frame.html          the tip
probe       tools/vesper_relic_probe.py            <- new
sweep       tools/vesper_sweep.py                  <- new
id          vesper    — the id matches the name, as it does on all 26
01-live     UNTOUCHED.
```

`chain_audit.py --builder vesper_build.py` after every carry. It defaults to
`twinshade_build.py` and will audit the wrong inserts and pass.

---

# 2. WHAT IS SETTLED

**The cell:** vigil x scythe, taken on delivered effect (+19.2%, the strongest
channel on its row) rather than on occupancy.

**The names:** the fighter is **VESPER**, the ultimate is **THE SENTINEL**.

**The block** is the type's, byte for byte:

```
reach 104   width 11   spin 3.2   mass 2.4   blades [0]   mode spin
onSelf ward:1                               (the school's, byte for byte)
dmg <BISECTED>
```

**The ultimate:**

```
kind        sentinel     a wind-up, then a slowly turning beam from the blade tip
charge      15-17        the roster band
windup      SWEEP        unpriced — see §4.1
dur         ~4.0s base   EXTENDED BY THE WARD, drunk continuously — see §3.2
turn        ~1.6 rad/s   RICK'S: slow. The design is the lighthouse, not the lance
range       180-300      SWEEP — this is the main axis, see §3.3
half        17-26        beam 34-52 wide; §1 asked for "at least half a relic" = 34
damage      PER PASS     not per tick. Rick's call
tipFrom     ~0.75        the far quarter, where the bonus fires
tipMul      SWEEP
push        CUT or token — measured inert at these contact durations (design §5)
```

---

# 3. THE FOUR THINGS THAT DECIDE THIS BUILD

## 3.1 THE UNIT IS A PASS, NOT A FRAME

Rick took the slow beam knowing it crosses rather than holds. So the mechanic
is: **a pass begins when the ball enters the beam and ends when it leaves; a
pass deals its damage once; a pass that reached the far quarter at any point
deals the bonus.** Do not implement this as a per-frame tick with a cooldown —
that is the lance design, and it is not the one that was chosen.

Measured at turn 1.6 / range 300: **3.5 passes in a four-second window, mean
pass 0.28s, longest 1.54s, 60% of passes reaching the tip zone.**

## 3.2 THE WARD IS DRUNK CONTINUOUSLY, NOT READ AT THE CAST

**The pool at the cast is a median of ZERO and 57% of casts find an empty
shell.** Charge is wall time; the ward is up 42% of the fight; the two are
uncorrelated. Reading `spendWard` once at the cast builds an ultimate that is
inert more than half the time.

**The precedent is in the tree and it is Aegis**: *"feed the wall while it
stands"*, added for this exact measurement. Follow its shape.

Measured: a four-second beam banks **8.1 points of ward while it runs, about
2.0 a second**. So the drink rate is the knob that decides whether the beam is
self-sustaining, and it should be swept against the base duration rather than
picked.

## 3.3 RANGE TRADES PASS COUNT AGAINST TIP RATE, AND THAT IS THE SWEEP

```
range 180  ->  2.8 passes,  73% reach the tip
range 300  ->  3.5 passes,  60%
range 420  ->  3.8 passes,  45%
```

Nothing else in the design has a trade this clean. **Sweep range against
tipMul**, because between them they set what share of the ultimate's damage is
the bonus — which is the number to put to Rick, the way v43 put "how much of
Paradox IS the field" rather than a win rate.

## 3.4 THE TIP MOUNTING IS FREE AND THE PUSH IS NOT WORTH BUILDING

Firing from the caster's centre instead of the orbiting blade tip buys 4.9
points of time-on-target; freezing the weapon's spin buys 2.8. **Keep the tip.**

The push moves the ball from 0.56 to 0.59 of the way down the beam at six
times the force. **Build it as a token shove for the picture or not at all**,
and do not spend a sweep axis on it — but if it ships, it must not be a dead
knob, so either give it a measurable job or cut it (v40's `shot.life` is the
standing warning).

---

# 4. THE PROBE — ONE CHECK PER SENTENCE OF §1

`tools/vesper_relic_probe.py`. At minimum:

1. **The beam exists as geometry the hit test agrees with** — the drawn beam
   and the tested volume are the same object. v43's hexagon check, exactly:
   *"the drawn beams and the tested boundary are the same object."*
2. **A pass is counted once.** Entering, leaving and re-entering is two passes;
   a frame inside a pass is not a pass.
3. **The tip bonus fires on the pass's furthest reach**, not on where it
   happened to be at the last frame.
4. **The origin tracks the blade tip**, and the beam's direction is rate
   limited — a quarry that out-turns it gets round the outside, and that is a
   failure the viewer can watch.
5. **The ward drains while the beam runs and refills from the blade's own
   blows**, and the beam ends when the pool and the base duration are both
   spent. Assert the loop closes: a fight where the caster lands nothing during
   the beam gets the base duration and no more.
6. **A pass on a Twinshade COPY files nothing** — `!foe.shade`. v43 §11 caught
   exactly this, one frame in six thousand.
7. **A lethal pass ends the beam** rather than continuing to sweep a corpse.
8. **The wind-up is broken by a true stun** — `breakSpin`, the same hook the
   Crucible uses — and the probe measures how often, on this relic, against the
   four hex appliers.
9. **THE SOUND IS RENDERED AND MEASURED IN AN OfflineAudioContext.** v42
   shipped a silent ultimate through every green check in the repo. This one
   needs at least three voices — the wind-up, the sweep, the tip hit — and the
   sweep is a SUSTAIN, which this toolkit cannot do: `_tone` ends on an
   exponential ramp over its whole length and `_burst` does not loop its 0.6s
   noise buffer. **Write inside the envelope like v43 did** — re-strike rather
   than hold — or the beam is silent for most of its own duration.
10. **THE PASS FILES A BEAT.** Rule 3, sixth relic running. A pass that reaches
    the tip is the legible moment of this ultimate and nothing else in the
    frame knows it happened.

---

# 5. THE SWEEP

`vesper_sweep.py`. **Bisect `dmg` against all 26 opponents in every cell before
reading that cell's telemetry.**

**Axes, in order of measured leverage:** `range` x `tipMul` (§3.3), then the
drink rate x base duration (§3.2), then `half` and `turn`.

**Do not sweep the push.** Design §5.

**The framing to put to Rick**, the way v43 put its own: the bisection
compensates, so the pair does not choose how hard Vesper hits. **It chooses
what share of the Sentinel is the TIP** — a short beam that mostly pays at the
far end, against a long one that mostly pays in the middle.

**And take the two cheap wins nobody has taken** (v43 §14.1, unmoved through
v47): a bisection should escalate its sample rather than spending 960 fights on
step one, and nothing in `tools/` is parallel.

---

# 6. THE GATES

```
engine_ab       IDENTICAL on the other 26 in any match with no cast in it
chain_audit     --builder vesper_build.py
verify --n 40   the thirteenth check (duration band) is KNOWN to fail at the
                tip — do not credit this relic with it either way
tip_audit       and verify's 72-character ult-tip limit
frame_probe
post_identity   the picture is unchanged where the ult is not running
```

---

# 7. WHAT NOT TO DO

- **Do not build the lance.** Rick chose the lighthouse with the numbers in
  front of him. A per-frame tick with a hit cooldown is the other design.
- **Do not read the ward at the cast.** §3.2 — median zero.
- **Do not fire from the caster's centre.** It is worth 4.9 points and it
  throws away "points at the tip", which §1 asked for and which is free.
- **Do not add homing to the ball, only to the beam's bearing.** The beam turns
  at a rate; the ball is ballistic, and that is the whole counterplay.
- **Do not touch `STATUS.ward`** as part of this build. It is worth up to +13.4
  points (scythe_survey §4.3), it is chain-wide across four relics, and it is
  Rick's.
- **Do not touch `01-live`.** Do not fix `_burst` or `_tone`. Do not let the
  fight card back in.

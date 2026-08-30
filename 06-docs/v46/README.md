# v46 — THE IGNITION OPEN. A fight now starts as a shot.

**2026-08-29.** Rick watched `05-reference/v46-ignition/ignition-open-both-solo.mp4`
— the "both" variant out of `tools/ignition_lab.py`, one of four the lab
rendered off one seed — and said *"lets make it happen capn"*. This is that,
moved out of the lab's capture-time monkey patches and into the build.

```
02-chain/sc-paradox-ignition.html   <- THE BUILD OF RECORD
built off 02-chain/sc-paradox-crucible.html by tools/ignition_build.py
src/render/open.js                  <- the module, inlined byte for byte
tools/ignition_probe.py             <- the picture, measured, 11/11
01-live UNTOUCHED, still on sixteen, still not a target
```

---

## 1. WHAT SHIPPED

The first **2.35 seconds** of every fight are now a shot, in three parts, all
of them a pure function of `m.t`:

| | |
|---|---|
| **the camera** | fighter A at 2.25x easing to 2.02x, a hard cut at 0.85s to fighter B, then a pull wide from 1.55s to 2.35s that lands just before a ~2.3s first clank arms the scrunch |
| **the ignition** | A flares at 0.10s and B at 0.95s — staggered ONTO the cut, which is the whole difference between "both" and the ignition-only variant — each in its own affinity palette: a white core strike for three frames, an expanding ring, a corona that overshoots and settles, 0.90s each |
| **the swell** | every `shadowBlur` in the hall powers on: 0.30 -> overshoot 1.42 -> exactly 1.0 over 0.95s |

Then it hands the lens back and the build is, frame for frame, the build it was
made from.

**Four hooks, all in `Renderer.draw`, all one line.** The numbers live in
`SWBOpen.LOOK` in the module, not in the builder's glue — `post_build.py`'s
rule, for the reason it states: a second copy of "which opening" in the glue is
how a build ships something nobody picked.

---

## 2. THE THREE DECISIONS THAT ARE NOT THE LAB'S

### 2.1 THE CLOCK IS SIM TIME, AND THE LAB'S WAS WALL TIME

The lab was right to use wall time and this would be wrong to. During the
opening there are no cuts, so `CINE.timeScale` is 1 and the two clocks are the
same number — inside a five-second capture harness. In the build they are not
interchangeable, for three reasons the lab never had to face:

1. **The post chain draws every frame four times** (readouts, emissive, world,
   composite). A pure function of `m.t` is idempotent; a wall-clock one would
   advance four times per frame. This project has paid for that lesson twice —
   `post_build.py`'s camera shake, which presented as juddering **physics**,
   and `fx.js`, which is aged off `ultFx.t` for exactly this reason.
2. **The app's rAF and the capture's fixed cadence must agree.** A dropped
   frame in the app is then fewer samples of the same shot, not a different
   shot, and the mp4 is byte-identical either way.
3. **No `Math.random` anywhere.** The handheld drift is the engine's own
   two-frequency formula from `CINE.update`, evaluated at `m.t`.

Check 10 of the probe is the receipt: a frame drawn three times at one sim time
is one frame, hash for hash.

### 2.2 THE FLARE IS DRAWN OVER THE COMPOSITE, SO IT DOES NOT BLOOM

`fx_build.py` hooks inside `drawUltOver` **precisely so its fields reach the
bloom.** This hooks after `POSTFX.frame` for the opposite reason: the flare
Rick approved was drawn after the composite in the lab, so it is unbloomed, and
that is what was approved.

It is also the safer of the two. `CLAUDE.md` §4.1b and §4.1c are both about
white art handed to this chain — a radial gradient from `#FFFFFF` centred on a
body already at 0.892 luma did not light the ball, it **erased** it. The flare's
core is `#FFFFFF` at 0.95 alpha. Putting it in the emissive pass would be that
mistake a third time, on purpose.

### 2.3 THE SUBJECT-FIT CLAMP — THE ONE THING ADDED TO THE LOOK

`Renderer.draw`'s feasibility clamp — both relics' magnified bodies must fit
the usable frame — is **why an opening shot could not exist before**: at spawn
separation (~503 su) it pulls any asked zoom back to ~1.0. The opening stands
it down for its 2.35s, exactly as the lab's `__openShot` gate did.

But that clamp was bought with a probe that found **8/8 wall-adjacent
set-pieces clipping relic body, by 137–376px**, and standing it down gives that
guarantee up. Measured, with only the lean clamp the lab had:

```
worst subject margin, swept over 12 pairings x the whole opening
    -12.5px   spellbreaker v twinshade, 0.74s, subject A
     -4.5px   ironhail v oathwound (the approved seed), 1.4s, subject B
```

Small — 4px of a 1625px design frame is under two device pixels at 540 wide —
but it is the ball being cut, and inside a shot that has to hold its zoom the
renderer's usual answer (pull back) is not available. So the opening
re-establishes the guarantee for **the one relic being filmed**, with the same
solve and the same precedence the renderer uses for a cut: the subject-fit
clamp wins over the lean clamp.

> **AND IT COSTS ALMOST NOTHING OF WHAT WAS APPROVED.** On the approved seed it
> moves the camera on **1 of 115 samples, by 4.4px** — 2.2px at the delivery
> width. Swept over 24 pairings afterwards, the worst margin is +0.0px: the
> clamp binding, which is what it is for.

---

## 3. WHAT IT DOES NOT DO, AND ONE OF THEM IS A QUESTION FOR RICK

**THE OPENING IS SILENT.** The clip Rick approved had no ignition sound —
`SFX` events come from the sim and the sim knows nothing about this — so
shipping one unasked would be shipping something he has not heard. The ult
sound is one of the seven things that are his (Rule 2), and a strike this loud
visually wants a voice. **Offered as a spread when he wants it**, not decided
here.

**A DIRECTOR CUT INSIDE THE OPENING LOSES THE CAMERA.** Measured: `cinePlan`
schedules a first cut before 2.35s on **2 of 120 pairings (1.7%)**, at 1.62s
and 1.64s. The opening wins those — the cut still runs, its time dilation and
its audio duck still apply, and the lens is handed back mid-cut. It is rare
enough to leave alone and it is now a number rather than a hope.

**AND IT ONLY REACHES A SHORT THAT STARTS AT ZERO.** `cinema_clip` measures
`--lead` backwards from the killing blow, so an ordinary clip starts thirty
seconds into the fight and never sees the opening. `--full` starts at 0.0 and
films everything, which at the current pace is a ~50s fight plus the verdict
hold. **Whether shorts now open at zero is an editorial decision and it is
Rick's**, not a thing this build should decide by itself. The app shows the
opening on every fight either way.

---

## 4. THE VERIFICATION

```
IS IT THE SAME OPENING?     18/19    PIXEL-IDENTICAL to the lab's own
                                     implementation at identical clocks -- §4.1
ignition_probe.py            11/11   the picture, one check per sentence
engine_ab.py --n 10         150/150  identical field for field, 6 relics
render_ab.py  after release  20/20   PIXEL-IDENTICAL at 3,6,12,22,31s
render_ab.py  in the window  12/16   DIFFERS at 0.3/1.0/2.0s, identical at
                                     2.34s -- which is after the shot releases
post_identity.py             PASS    325,708 px identical, max delta 0
chain_audit.py               PASS    fx, post and this builder's inserts all
                                     survive to the tip
verify.py --n 40             12/13   the same 12/13 as the tip it was built
                                     from, and the same FAIL: Lightkeeper/
                                     Farwarden 74.6s against a 70s pairing
                                     ceiling. Winrate spread 14.9pp, overall
                                     mean 48.8s, 0/12000 timeouts -- every
                                     number unmoved. See §0.
```

### 4.1 THE ONE THAT MATTERS: IS IT THE SAME OPENING?

Everything above says the build is sound. Only one measurement says it is the
picture **Rick approved**, and the first attempt at it was misleading.

Rendering the lab's `both` off the old tip and the build's own opening off the
new one, through the same 60fps harness, and diffing 324 frames:

```
identical frames 131/324, mean |delta| 1.43/255, worst 7.10 at t=0.22s
```

That reads like a real difference and it is not one. **The lab harness
evaluates the opening one frame BEHIND the sim**: `_sub()` steps the match to
frame *i+1* and then calls the driver with `this.wall`, which is still frame
*i*. The build evaluates at the sim time of the frame being drawn. Shifting the
comparison by a frame in either direction makes it worse (2.82 -> 4.28 and
5.72), which is what says the alignment is right and the offset is inside the
16.7ms.

So the two were put side by side with the clock removed as a variable — same
page, same match, same sim state, same rasteriser, `m.shake` pinned — the build's
`SWBOpen` against the lab's driver at **identical** clock values:

```
t     0.00  0.05  0.10  0.14  0.20  0.30  0.50  0.70  0.85  0.86
      0.95  1.00  1.20  1.54  1.56  1.80  2.00  2.20      max |delta| 0
t     2.34                                    mean 0.0786, 1.14% of frame
```

**Eighteen of nineteen instants are byte-for-byte identical**, including every
flare frame, both seams and the whole pull. The nineteenth is the last 10ms:
the module hands the lens back once `z <= 1.02`, where the lab left `CINE.zoom`
at 1.0005 and let the renderer's own branch run one more frame at a zoom of
five ten-thousandths. The build's version is the cleaner of the two.

`tools/out-ignition/` holds both renders. The still-frame A/B was a throwaway;
its result is this section.

**`engine_ab` coming back identical is necessary and proves nothing about the
picture** — `Fighter`, `Match` and `Sfx` contain no reference to a canvas,
which is exactly why a renderer change returns 150/150 whether it was harmless
or a disaster. That is what `ignition_probe.py` is for, and why every one of
its checks is about pixels or about the transform that makes them.

Two of its checks earned their place by failing first:

- **check 3** asserted the subject was at frame centre and found it 467px away.
  It was not a bug: the LEAN clamp binds on 45 of 115 samples, and the same
  clamp, at the same overscan, is in the approved clip. The check was measuring
  an intention rather than a property. It now measures the property that
  matters — the subject is not cropped — and it swept the roster to find the
  −12.5px in §2.3, which one seed would never have shown.
- **check 7** read the swell's dimming as a missing flare. Switching the whole
  module off changes the camera, the flare and the swell at once. Suppressing
  **one contributor at a time** (`CLAUDE.md` §4.1c) separates them: the flare
  puts **+0.1206** luma on relic A's own disc, and the swell puts **−0.0030**
  at 0.07s and **+0.0039** at 0.30s.

---

## 5. THE APP POINTER WAS STALE, AND IT IS NOT ANY MORE

`app/main.js` still read `02-chain/sc-paradox-arc.html` — one build behind, so
the app has been showing a game **without** the Crucible true-stun change since
that shipped. It is now on `sc-paradox-ignition.html`.

`docs/ARCHITECTURE.md` §1's guarantee is that the app cannot show Rick
something the mp4 will not, and a pointer nobody moves is the quiet way that
guarantee stops being true. It is one line in one file and it needs to move in
the same commit as every future build of record.

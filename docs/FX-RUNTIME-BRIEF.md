# THE EFFECTS RUNTIME — brief for the ult and ability animation work

**Written 2026-08-29 in Cowork, off the repo at commit `46e37edc`. Rick plans
with Cowork, Claude Code builds. This file is the plan; the building is not
described here beyond its gates.**

**REVISED the same day.** Rick asked whether 60 fps should be the target since
that is all TikTok takes. It should, and chasing that into the delivery path
turned up §5.1 — which outranks everything in §3 and moves to the front of
Stage 0.

Goal, in Rick's words: **"state of the art ult and ability animations."**

Read `CLAUDE.md`, then `docs/RENDER-LAYERS.md`, then this. It supersedes
`docs/RENDERER-BRIEF.md` §3's implicit claim that the post chain finishes the
job, and it corrects that file's §4.

---

## 0. THE POST CHAIN IS DONE AND IT CANNOT GIVE YOU MORE

The renderer arc did what it was asked to do, and the honest measurement of how
much that was is already in this repo:

> Daybreak's caster disc, 0.499 bare → 0.905 at the peak. **Only +0.041 of that
> was the bloom.** — `CLAUDE.md` §4.1b

**Roughly a tenth.** The other nine tenths were the art. The chain ships bloom
at LOW; trails and grade were each chosen off a sheet, each looked worse in
motion, and each ships OFF. That is not a failure of the chain — it is the
chain arriving at its ceiling, which is exactly what "composite first" was
supposed to find out cheaply, and it did.

> **A post chain makes light out of what the art already draws. It cannot draw
> anything.** Every further gain is in the art layer.

That is the pivot this brief is standing on, and it is why the answer to
"upgrade the graphics further" is not another pass in `post.js`.

---

## 1. WHAT THE ULT ART ACTUALLY IS, COUNTED

Measured off `02-chain/sc-paradox-frame.html` by brace-matching the two
methods, not estimated:

```
drawUltOver     1,167 lines    19 per-relic branches   13 shared-helper calls
drawUltUnder      480 lines    17 per-relic branches   14 shared-helper calls
                -----------                            ------------------
                1,647 lines    19 set-pieces           27 shared calls
```

**Twenty-seven calls into a shared vocabulary across sixteen hundred lines and
nineteen set-pieces.** Seventeen of the twenty-seven are `_jag`. There is no
shared substrate: every ultimate reinvents its own rings, its own fade and its
own clock.

The vocabulary that is actually in use, inside `drawUltOver` alone:

```
45  c.arc()          52  shadowBlur =        10  createRadialGradient
40  c.stroke()       76  globalAlpha =       24  c.lineTo
30  c.fill()          2  c.ellipse()          1  Math.random
```

**Forty-five arcs and forty strokes.** The medium is: stroke a circle, set
`shadowBlur`, set `globalCompositeOperation = "lighter"`, fade it out on a
linear `k = t / life`. That is `_ult()`'s entire contribution — one clamped
ratio — and it is the only timing structure any of the twenty-five have.

Look at `05-reference/post/ult-filmstrip-all25.png` with this list in hand and
the filmstrip stops looking like twenty-five ultimates. It looks like one
technique applied twenty-five times, in six palettes.

### What the medium cannot reach, and why each matters

| missing | consequence on screen |
|---|---|
| **particles** | nothing flies, tumbles, drags or dies. Sparks are placed, not thrown. `this.sparks` exists in the sim and the ults barely touch it. |
| **an envelope** | `k = t/life` is a ramp. No anticipation, no snap, no hold, no overshoot, no settle. **This is most of what "state of the art" means in VFX and it costs nothing to fix.** |
| **screen-space distortion** | no shockwave warp, no heat shimmer, no refraction. The single strongest "modern" cue and the chain has no displacement pass. |
| **depth** | every layer is flat in one plane at one scale. |
| **camera authority** | see §3.4. An ultimate is not guaranteed a shot. |

### And the structure is why eight of them shipped blank to the tools

`ult_fx_capture.py`'s docstring names it: eight ultimates branch on `phase`
with no fallback, so a synthetic block drew **nothing**, and two tools reported
that as a low score rather than as a blank. Five more (`paradox`, `twinshade`,
`foregone`, `marrowdraw`, `redflail`) do not read `ultFx` at all.

Catching that took three probes. **A set-piece that can be blank is a property
of nineteen independent branches with no shared floor** — and the third
picture-fault class this project has found. It is a structural fault, not eight
bugs.

---

## 2. THE IDEA

> **Stop hand-drawing set-pieces. Build a small deterministic effects runtime,
> and re-express the ultimates as data on top of it.**

Four capabilities, one shared vocabulary, twenty-five short declarative specs
instead of nineteen bespoke branches. `post.js` already owns a WebGL2 context,
the shader plumbing, ping-pong framebuffers, a resize path and — the part that
matters most — **an identity test that compares every channel of every pixel
against the 2D canvas and must report zero.** The hard, boring half of this is
built and proven. The runtime is a second consumer of it, not a second copy.

The Canvas 2D path stays. It is the control, permanently, exactly as
`RENDERER-BRIEF.md` §9 says.

---

## 3. THE FOUR LAYERS, IN ORDER OF RETURN PER LINE

### 3.1 THE ENVELOPE — no new technology, the largest perceived gain

Replace `k = t / life` with a shared shaping module: **anticipation → snap →
hold → decay**, with overshoot, per stage, authored as numbers.

Every one of the nineteen branches keeps its geometry and gets a real clock.
A ring that snaps out in 90 ms, overshoots 8%, holds for two frames and decays
over 400 ms is a different animation from the same ring on a linear ramp, and
it is the same forty lines of drawing code.

**Do this first, on three relics, and film it.** It is ~150 lines, it touches
no new API, and it is the cheapest possible test of the whole thesis: if
better timing does not read as better animation on a phone, nothing further
down this list will save it. If it does, it re-prices everything below.

### 3.2 THE PARTICLE RUNTIME — the real new capability

A GPU particle system in `src/render/fx.js`, sharing `post.js`'s context.
State in a texture, ping-pong integrated, spawned from `ultFx` events, drawn
into the emissive layer the bloom already reads (`roMode 3`).

This is what buys the vocabulary that is currently unreachable: embers with
drag, debris with gravity and tumble, sparks with a real lifetime curve,
sustained fields with curl noise, dissolve and accretion.

Budget it in **thousands** of particles, not hundreds. The current art can
afford about a dozen sprites per frame because each one is a Canvas2D call
with a `shadowBlur`; a texture-state system is one draw call for the lot.

### 3.3 THE DISPLACEMENT PASS — one shader, three effects

One more FBO in the existing chain: effects write a screen-space displacement
buffer, the composite samples through it.

Shockwave on a nova. Heat shimmer off Slagburst. Refraction through Paradox's
hexagon. Radial smear on a kill. **This reads as "modern" more than any amount
of glow does**, and against the chain that already exists it is one shader and
one target.

It also has a real trap and it should be built expecting it: displacement over
the arena rect will drag the letterbox and the damage floats unless it sits
inside the same layer split `readouts_build.py` already made for the bloom.
`docs/RENDER-LAYERS.md` §4 is the map; use it rather than rediscovering it.

### 3.4 THE ULTIMATE OWNS THE CAMERA — the cheapest big win in this document

Measured, from the build's own `CINE` comment and `cinema_rate_probe.py`:

```
floor 1.90     none 41%    one 37%    two 16%    3+ 7%    mean 0.90 cuts/match
```

**Forty-one percent of matches contain zero cuts.** An ultimate — which
`sundered-crown-ult-model.md` argues is *the only thing a relic owns alone* —
currently plays at whatever framing the fight happens to be sitting at, and
five relics have had to file a beat by hand just to be *seen* (Rule 3).

**The camera language already exists in full.** `TIER_KILL` carries seventeen
fields — `lead dropFrom dropTo ramp freeze whip peak settle rest hold slow out
gapRate gapLead bias bars wash`. There is nothing to invent; there is only a
caller missing. An ultimate should be able to ask for that vocabulary directly:
a push-in on the cast, a freeze on the connect, a dilation across the payload —
**declared in the ult's spec, not negotiated with `cinePlan`'s scoring.**

This is a handful of fields and it will do more for "does this read as a
set-piece" than layers 3.2 and 3.3 combined. It is also the one that makes the
still-unbuilt shared `cineFloor` (open item 2, six relics deep) less urgent,
because an ult stops depending on the floor at all.

---

## 4. WHAT THIS BUYS BESIDES PRETTINESS — AND IT IS THE STRONGER ARGUMENT

`sundered-crown-ult-model.md` §2 is unambiguous about what limits this game:

> The ultimate is the only thing that does not factor, and it is therefore the
> only thing that sets how big the roster can be. **Decide how many set-pieces
> you are willing to build. Call it N. The roster is N cells.**

Today a set-piece is ~60 hand-written lines against raw Canvas2D with no shared
floor, and it takes most of a session. **That cost is N.**

An effects runtime where a set-piece is a declarative spec against a shared
vocabulary — spawn this emitter with that envelope on that camera move — makes
an ultimate an evening's work instead of a session's, and makes a *blank* one
impossible because an unspecified ult falls through to its school's default.

> **This is not a graphics project. It is the thing that moves the roster
> ceiling.** Nineteen bespoke branches is why the grid has 25 of 48 cells.

Pitch it that way when it needs justifying, because that is the honest reason
it is worth four sessions.

---

## 5. THE BUDGET — 60 IS THE TARGET, AND THE DELIVERY PATH IS THE REAL PROBLEM

### 5.0 SIXTY, AND `RENDERER-BRIEF.md` §4 IS WRONG — DELETE IT

Rick, 2026-08-29: *"if tiktok only supports 60fps video shouldn't that be our
target?"* **Yes, and it settles the question from the outside.** Checked
against the platforms rather than assumed: TikTok accepts 23–60 fps and 60 is
the ceiling; YouTube lists 24, 25, 30, 48, 50, 60 and names nothing above it.
There is no deliverable above 60 to render for.

That file promised 120 fps as "the free win nobody has taken." Two independent
things now say no — the platform has no slot for it, and the measurement came
back the other way anyway:

```
before the chain, at 120 Hz, on the Intel UHD:   7.36 ms of an 8.33 ms budget
bloom only, at the app's 453x805:                8.05 ms — 48% of 60 fps
```

**Target 60.** Delete §4 of that brief in the same commit that starts this
work — a brief carrying a promise its own repo has refuted is how the next
session budgets wrong.

### 5.0a BUT 120 Hz WAS NEVER ABOUT DELIVERY, AND THE THING IT WAS ABOUT SURVIVES

`CONFIG.physics.dt` is 1/120 and the render is 60, so **every output frame
skips a sim step.** The picture is sampled at half the rate the physics runs.
That does not go away at 60 fps delivery — it stops being an argument for
120 fps playback and becomes the argument for **motion blur**.

`RENDER-LAYERS.md` §5c already diagnosed exactly this from the other end, as
the trail beading artefact: *"the fix is to accumulate at the sim's 120 Hz
rather than the render's 60."* Right diagnosis, and at 60 fps delivery it is
strictly cheaper than it looked, because sub-frame accumulation is 2–4 extra
**draws per output frame**, not a doubled output rate — and offline it costs
wall-clock and nothing else.

> **For a 60 fps deliverable, motion blur is better than 120 fps would have
> been.** It puts the sim's extra temporal information into the frame TikTok
> actually shows, instead of into frames TikTok will throw away.

### 5.0b AND IT SHARPENS THE TIER QUESTION RATHER THAN DISSOLVING IT

The app is realtime-constrained. **The mp4 is not** — `shorts_build.py`
captures offline at 3–4 minutes for ~2,800 frames, where a 30 ms frame costs
wall-clock and nothing else.

With 120 fps off the table, the video's extra budget can now only be spent on
things that improve a **60 fps frame**: sub-frame motion blur, more particles,
a better bloom. It cannot be spent on more frames. So the divergence question
is unavoidable, and `docs/RENDERER-BRIEF.md` §5's constraint still stands:

> **THE APP AND THE VIDEO MUST NOT DIVERGE.**

The resolution is one runtime at **two named quality tiers**, the tier is an
explicit setting like every other look in `post.js`, and the app displays which
tier it is showing. A tier the app silently picks is the divergence wearing a
different hat.

---

### 5.1 THE FINDING THAT OUTRANKS THIS WHOLE DOCUMENT

> **SUPERSEDED IN DETAIL BY `docs/DELIVERY-QUALITY-BRIEF.md`, 2026-08-29.**
> Rick: *"spare no expense on video quality."* That brief is the plan and it
> runs FIRST. It also corrects this section on one point: raising `--w` is
> **not** a free quality win, because `shadowBlur` is in device space and every
> glow in the game is twice as wide relative to the frame at 540 as at 1080.
> `--w` is a look knob. The summary below stands; the "render minutes, not
> engineering" line does not.

Chasing the fps question into the delivery path turned up something bigger than
anything in §3. Read straight out of the two tools:

```
cinema_clip.py   --w  default 540   -> AC.setResolution(540, 960)
                 --q  default 0.80  -> toDataURL('image/jpeg', 0.80)
shorts_build.py  --w  default 540
                 encode: scale=1080:1920:flags=lanczos
                         libx264 -preset veryfast -crf 23 -pix_fmt yuv420p
CLAUDE.md §5     the canonical clip command passes --w 540
```

**A shipped short is rendered at 540x960, JPEG'd at quality 0.80, upscaled 2x
to 1080x1920, x264'd at `veryfast`/CRF 23, and then re-encoded again by the
platform.** Four lossy generations, and three quarters of the pixels are gone
before TikTok ever sees the file.

Nothing in the repo defends `540`. It appears in exactly three places — two
argparse defaults and the canonical command in `CLAUDE.md` — with no comment,
no measurement and no note. It is almost certainly a capture-speed default from
an iteration loop that became the shipping path, which is the same shape as
`post_build.py`'s wrong `--src` and `shot.life: 3.4`: **an undefended number
that quietly became policy.**

Why this outranks §3: **thin bright strokes on near-black are the worst case
for every stage of that path.** JPEG at 0.80 rings around high-contrast edges;
`yuv420p` halves the chroma resolution of exactly the saturated blues and reds
the schools are built on; a 2x lanczos upscale cannot invent the detail back;
and `veryfast` spends its bit budget badly on precisely the fine, fast-moving,
high-frequency content this brief proposes to *add more of*.

> **Adding particles and distortion upstream of a 540p JPEG upscale is paying
> for detail the delivery path is designed to destroy.** Fix the path first or
> the FX work cannot be seen.

And the fix is render minutes, not engineering:

| change | costs | buys |
|---|---|---|
| `--w 1080` | ~4x capture pixels; 3–4 min → maybe 12–16 | the actual resolution of the deliverable |
| `--q 0.95` or PNG | disk, and some write time | no DCT ringing on the ult art before x264 sees it |
| `-preset slow` | encode minutes | free quality at the same CRF |
| `-crf 18` | a bigger file nobody keeps | a clean source for the platform's re-encoder |

**Price it, do not assume it.** One clip, both ways, same seed, four frames
compared — this repo's own standard from `APP-FEATURES-BRIEF.md` §2.

### 5.2 AND THE MEASUREMENT NOBODY HAS TAKEN

`08-analytics/` pulls **retention** off real posts, so the platform round trip
is already part of this workflow. **The picture round trip is not.** Nobody has
posted a clip, downloaded it back, and compared it frame for frame with the
local mp4.

That is the only measurement that can price the grain setting, the particle
density, and every thin-stroke decision in §3 — because the deliverable is not
the file `shorts_build.py` writes, **it is what the platform's encoder does to
it**, and this project's whole doctrine is to measure the thing that actually
ships. It is one post, one download, and one contact sheet.

### 5.3 STILL MEASURE THE FRAME BUDGET FIRST

`post_cost.py` exists and the one number that prices §3 is the frame budget on
the machine that owns the chain, at 60 fps, at the app's size and at
1080x1920 — **which §5.1 may be about to change.** Get it after the capture
resolution is settled, not before.

---

## 6. DETERMINISM — THE CONSTRAINT THAT KILLS THE OBVIOUS IMPLEMENTATION

Every particle system anyone has ever written calls `Math.random`. **This one
must not.**

`(build, relics, seed)` names a fight, `render_ab.py` hashes frames,
`cinema_clip` must reproduce a clip from its seed, and `ult_live_probe.py`
already had to pin `Math.random` around each draw because two sites in the draw
path use it (camera shake; Unmaking's flicker — one call, in `drawUltOver`).

Requirements, and they are not negotiable:

1. Particle randomness comes from a **seeded stream keyed on
   `(ultFx.seed, emitterIndex, particleIndex)`** — the same mulberry32 the sim
   uses, never the global.
2. Integration steps on a **fixed dt**, not on wall-clock frame time. A
   particle field that depends on how fast the GPU ran is a clip that cannot be
   rebuilt from its seed.
3. `post_identity.py` and `render_ab.py` both extend to cover it: two runs of
   the same seed produce **bit-identical** frames, and the runtime with no
   emitters registered is invisible to the pixel.

Rule 3 of §7 below is that gate and it is the one that must not be waived.

---

## 7. THE STAGES AND THEIR GATES

Every stage ends with **Rick watching a played clip, not a still.** That is not
ceremony — `RENDER-LAYERS.md` §5b records two effects chosen off sheets and
rejected in motion, and `CLAUDE.md` §4.0 is the same rule one level down.

### Stage 0 — clear the debts and get the number *(half a session)*

- `post_build.py`'s `--src`/`--out` defaults still point at the pre-`ultcarry`
  link. **A bare run silently builds a tip with none of the ult art fixes, and
  nothing errors.** Two strings, then `chain_audit.py --builder post_build.py`
  and `engine_ab.py`. Named in `BUILD-CHAIN.md` §3 and `APP-FEATURES-BRIEF.md`
  §0.1 and still open — and it is the exact trap `CLAUDE.md` §4.10 warns about.
- `tools/README.md` says 62 files over ~200 and is missing three of the four
  newest chain links.
- **`git status` before anything.** `src/render/post.js` and
  `02-chain/sc-paradox-frame.html` both carry mtime `1787974707495` — the same
  millisecond, and later than commit `46e37edc`. Identical mtimes across two
  files is a checkout signature rather than an edit, but the tree state should
  be confirmed rather than assumed before a new arc starts on top of it.
- **THE DELIVERY PATH — now its own brief, `docs/DELIVERY-QUALITY-BRIEF.md`,
  and its nine steps replace this bullet. It goes first, ahead of every FX line
  in this document, and its §1 must be settled before its §3.** In outline: One clip rendered both ways off the same seed:
  `--w 540 --q 0.80 / veryfast / crf 23` against `--w 1080 --q 0.95 /
  slow / crf 18`. Four frames each, side by side, plus the wall-clock cost
  and the file size. **If the second is visibly better, that is the shipping
  default and `CLAUDE.md` §5's canonical command changes with it.** No FX work
  can be reviewed honestly through a 2x upscale of a 540p JPEG.
- **The platform round trip, §5.2.** Post one, download it back, contact-sheet
  it against the local file. One post, and it prices every thin-stroke and
  grain decision in §3.
- `post_cost.py` at 60 fps, at the app's size and at whatever capture
  resolution §5.1 settles on. **Everything below is priced off this number**,
  which is why it comes after the resolution question and not before.

### Stage 1 — the envelope, on three relics *(one session)*

Pick three with different shapes — a nova, a beam, a sustained field. Rebuild
their timing only. Nothing else changes.

**Gate:** side-by-side played clips, old timing and new, same seed. A spread,
not a recommendation (Rule 2). If Rick cannot tell them apart on a phone, stop
and re-plan — that answer is worth a session and it arrives cheap.

### Stage 2 — the particle runtime, on ONE relic *(one to two sessions)*

**Slagburst.** It is an explosion, which is the purest particle case, and it is
currently one of the thinnest set-pieces in the filmstrip.

**Gates:** §6.3 bit-identity across two runs · `engine_ab` 192/192 · frame cost
measured against Stage 0's number · Rick watches it move.

### Stage 3 — displacement *(one session)*

One shader, three uses. Gate: the letterbox and the damage floats do not move.

### Stage 4 — migrate the roster, one relic per commit

Old art kept as the control. A filmstrip and a played clip per relic. This is
the long tail and it is interruptible at any point — which is the reason to
build the runtime before touching relic twenty.

---

## 8. WHAT NOT TO DO

- **Do not port the relic bodies.** `drawGlassRelic` and the status routines
  are not the problem and do not get prettier as triangles.
  `RENDERER-BRIEF.md` §2 was right.
- **Do not build a general-purpose particle editor.** Twenty-five specs is a
  file, not a tool.
- **Do not touch the sim.** If the picture needs something the sim does not
  expose, say so and stop. That is Rick's call.
- **Do not run this and the module extraction together.** Same reasoning as
  `RENDERER-BRIEF.md` §9: it turns a safe change into a risky one.
- **Do not delete a single `draw*` method** until its replacement has been
  watched in motion and approved.

---

## 9. RICK'S CALLS — Rule 2

Priced from measurement where a measurement exists; **offered as a spread, not
a recommendation.** v43 landed its sound in one round trip that way; v42 took
four.

1. **Re-animate the twenty-five, or build the runtime and spend it on new
   cells?** §4 says the runtime pays for itself on the *next* relics regardless.
   Re-animating the existing roster is Stage 4 and it is the long tail.
   *Suggested: build the runtime, migrate opportunistically, and let the first
   new relic be the one that proves it.*
2. **Same look executed properly, or a new direction?** Everything above
   assumes the first — the palette, the schools and the shapes stay, and what
   changes is timing, density and motion. A new direction is a different
   project and a much larger one. **This cannot be settled in prose; it needs
   Stage 1's clips.**
3. **One quality tier or two?** §5.0b. With 120 fps off the table the video's
   spare budget can only buy a better 60 fps frame — sub-frame motion blur,
   more particles, a better bloom. If the app and the mp4 get different tiers,
   that has to be a named setting the app displays, not a silent fallback.
4. **What does a short actually cost to render?** §5.1 trades wall-clock for
   picture: 3–4 minutes becomes maybe 12–16 at full resolution and a slow
   preset. For a clip posted once that looks obviously right, but it is Rick's
   throughput and therefore Rick's call — and the numbers to decide on are one
   contact sheet away.

---

## 10. WHAT IS NOT ESTABLISHED HERE

- **The frame budget on the real machine at 60 fps is unmeasured.** Every cost
  claim in this document is conditional on Stage 0.
- **§5.1 is read off the code, not off a picture.** That a shipped short is
  540x960 JPEG-0.80 upscaled 2x is certain — it is four argparse defaults and
  one ffmpeg line. That fixing it is *visibly* better is a prediction, and the
  Stage 0 contact sheet is what turns it into a measurement. Do not change the
  shipping default on the argument alone.
- **Why `--w 540` was chosen is unknown.** No comment, no doc, no measurement
  anywhere in the repo. Capture speed is the obvious guess and it is a guess;
  if there is a reason it should be written down this time either way.
- **Nothing has been measured through the platform's encoder**, §5.2. Every
  claim about what survives to a viewer's phone is currently inference.
- **The GPU is named only as "the Intel UHD"** in `RENDER-LAYERS.md`. Whether
  `yert` has anything else available, and what Playwright's headless capture
  actually renders on, is unchecked and changes §5 materially.
- **No particle count has been priced.** "Thousands" in §3.2 is the right order
  of magnitude for a texture-state system and it is not a measurement.
- **Whether the envelope alone is enough** is the entire question Stage 1
  exists to answer, and this document does not know it.
- **`drawIntro` still returns early and replaces the whole frame**, so none of
  this applies while `m.introT > 0`. That is Rule 1's dead fight card, still in
  the build for a sixth session.

# PRISTINE DELIVERY — brief for Claude Code

**Written 2026-08-29 in Cowork. Rick plans with Cowork, Claude Code builds.**

Rick: *"the clips need to be as pristine as possible for tiktok. i want to
spare no expense on video quality."*

**Spare no expense means render minutes and disk, not correctness.** Every
change below is either measured here or has a named measurement attached to it.
Nothing in this file may be shipped on the argument alone.

Read `CLAUDE.md`, then `docs/FX-RUNTIME-BRIEF.md` §5, then this. **This file
takes priority over that one.** No FX work can be reviewed honestly until the
delivery path is settled, because the path currently destroys exactly the kind
of detail the FX work adds.

---

## 0. THE SHORT VERSION

```
today:   render 540x960 -> JPEG q0.80 -> upscale 2x -> x264 veryfast crf23
                        -> TikTok re-encodes to ~1.5-2.5 Mbps

wanted:  render 1080x1920 -> lossless -> no resample -> x264 veryslow crf16
                          -> TikTok re-encodes to ~1.5-2.5 Mbps
```

**And §1 is why the first line of that is not simply worse than the second.**
It is also a *different picture*, and going straight to the second without
looking is how this project acquires its fourth picture fault.

---

## 1. THE FINDING THAT GATES EVERYTHING — `shadowBlur` IS IN DEVICE SPACE

`Renderer`'s constructor states the engine's central rendering invariant:

```js
this.W = 1080; this.H = 1920; this.k = canvas.width / 1080;
/* ... Everything downstream keeps drawing in design pixels, which is why
   every hand-tuned 188, 66 and 12 in the HUD still means what it meant. */
```

**That comment is wrong, and it is wrong in 129 of 132 places.**

`shadowBlur` is specified in the coordinate space of the output bitmap and is
**not** transformed by the CTM. So `c.shadowBlur = 22` is 22 *device* pixels
regardless of `k` — while every length beside it is a design pixel that `k`
scales. Halve the capture width and every glow in the game becomes **twice as
wide relative to the frame.**

### Measured, on the pinned runtime — CONFIRMED 2026-08-28

Same design-space content, same `shadowBlur = 20`, only the backing store
changes. The disc is measured separately and subtracted, so the number below is
the blur alone — `CLAUDE.md` §4.1c's "decompose by suppressing one contributor
at a time", applied to the instrument itself:

```
                     disc        disc      BLUR ONLY    BLUR ONLY
                 (device px)  (DESIGN px)  (device px)  (DESIGN px)
  k = 1.000 (1080)    39          39           16           16
  k = 0.500 ( 540)    19          38           16           32     2.00x
  k = 0.419 ( 453)  16.5        39.3           15         35.8     2.24x
                                  ----         ----
                              scales, as    constant, as
                              design px     device px
                              should
```

The blur is a constant sixteen **device** pixels at every resolution while the
disc beside it scales. In frame terms the glow doubles at 540 and is **2.24x**
at the app's 453 — not the 2.4x this brief estimated before measuring.

Re-run it with `tools/shadowblur_probe.py`, which exists now and ran on
Chromium 151.0.7922.34, the pinned pair. It also counts the call sites, so the
finding and the size of the fix come from the same command. Written to
`05-reference/shadowblur.json`.

### What this costs today

`shadowBlur` is assigned **132 times** in the build — 58 of those zero it, so
**74 are live**, 52 of them in `drawUltOver`.

**And the count of sites that honour `k` is zero, not three.** Three sites read
`22 * k`, `26 * k` and `8 + k * 16`, and in all three `k` is the ultimate's own
`t / life` ratio — a number between 0 and 1 — not the resolution scale. Nothing
in the build is resolution-independent here. `this.k` appears in a `shadowBlur`
expression exactly **0** times.

Someone did know once, and the note is still in the build:

> `shadowBlur` is in device pixels and the CTM does not touch it, so the
> buffer wants 30/D. — `sc-paradox-frame.html:11547`

That is the sealed-walls soft pass, where the author hit the property on a
downscaled offscreen buffer, worked around it locally with `30 / D`, and never
generalised it to the one `k` that scales the whole frame.

So the three surfaces this project judges its picture on have never shown the
same glow:

```
the bloom spread Rick chose LOW from    post_spread.py renders at 1080x1920
the app he watches fights in            453x805      -> glow 2.24x wide
the clip that actually ships            --w 540      -> glow 2x wide
```

**The look of record was chosen at a resolution nothing ships at.** That is not
a theory about why something looks off; it is arithmetic off the three numbers.

It also re-reads a line in `CLAUDE.md` §4.1b — *"turning the chain off left the
ball a featureless white blob"* — which was measured on a 1080 spread, at half
the relative `shadowBlur` reach the shipped 540 clip has. The conclusion may
still hold. The measurement behind it was taken on a different picture.

### Therefore

> **`--w` IS A LOOK KNOB, NOT A QUALITY KNOB.** Changing it changes the art. It
> cannot be raised quietly as a quality fix, and I said otherwise before
> measuring — that was wrong.

### What the fix is NOT — measured live, 2026-08-28

`shadowblur_probe.py --census` traps the setter through one drawn frame per
relic. A static count prices the EDIT; only the census prices the PICTURE, and
they disagree in three ways that change the plan:

**1. Ten of the twenty-five ultimates write no `shadowBlur` at all**, so the
helper cannot touch them. Per frame the roster spans 0 to 38 writes:

```
spellbreaker 36   lightkeeper 36   widowmaker 30   slagheart 20
grudgebearer 18   thornwake 18     heartwood 18    ... and then
0: dawnbringer ironhail censer emberedge twinshade redflail
   foregone bulwarden marrowdraw paradox
```

**Daybreak is one of the zeroes** — `CLAUDE.md` §4.1b's own subject. Its corona
is a radial gradient under `lighter`, exactly as §4.1b describes. `--w` does
not widen it and no `_blur` helper narrows it. The concern in §1 above that
"turning the chain off left the ball a featureless white blob" was measured on
a different picture stands unchanged for a different reason than expected: that
art was never in `shadowBlur`'s space at all.

**2. The bigger half of the fix is not on the renderer's context.** Across the
roster, 200 of the offscreen writes come from `drawGlassRelic` — the relic
body's own halo, `shadowBlur = 8 + hpFrac * 26`. `_ballBuf` (:13790) bakes each
body into a canvas sized `ceil(rad * 2 * k)`, scales by that same `k`, and
draws it back 1:1, so that halo is device-space **on the frame** exactly as the
main canvas is. It is on screen for **both relics on every frame of every
fight**, ult or not — which makes it the most-seen instance of this bug in the
game and the one nothing in this brief had noticed.

And `drawGlassRelic` is a module-level function taking `c`, **not** a `Renderer`
method, so `this.k` is not in scope there. `_blur(px)` cannot simply be dropped
in; the factor has to be threaded through its `o` bag. "129 mechanical
replacements" does not describe this half of the edit.

**3. The bloom is NOT affected and does not need touching.** Checked in
`post.js`: the mip pyramid halves from the frame size and `uTexel` is `1/w` of
each level, so `levels: 5` reaches 1/32 of the frame at any resolution and
`scatter` is in texels of a relative mip. The bloom's reach is frame-relative.
Rick's LOW is LOW at 540 and at 1080 alike — the only surface in the chain that
was already right.

### And what it buys, priced before it is built

`blurscale_spread.py` renders the fix at runtime — a property descriptor over
`[#cv, AC.renderer._bbuf]`, no file in `02-chain/` touched — against the same
frame at 540 and 1080. On the arena, `mean` luma:

```
                540 ships     540 + _blur      1080
  dawnbringer      0.1310        0.1302       0.1173
  lastlight        0.1257        0.1244       0.1232
  foregone         0.0853        0.0843       0.0847
```

**The fix moves the right way and it is small.** It closes roughly a twentieth
of the dawnbringer gap and most of the lastlight and foregone ones. The bulk of
what separates a 540 capture from a 1080 one is resolution itself — thin strokes
and fine geometry that a 2x lanczos upscale cannot put back — and that is
step 3's, not step 2's.

> **So step 2 is a CORRECTNESS fix, not the picture win.** It is worth doing
> first because it makes the three surfaces agree and because it is free at
> k = 1 — but do not sell it to Rick as the thing that makes the clip look
> better. Step 3 is that.

### AND RICK WATCHED IT — 2026-08-28. STEP 2 IS PARKED.

Two full clips, paradox v heartwood seed 25064, identical except for the fix.
Rick: *"i truthfully cant tell the difference between them."*

**That is the gate answering, and it answers NO.** The prediction was 0.6% of
arena mean and the eye agrees with the number, which is the outcome this
project should want from a cheap test: the measurement and the person said the
same thing before 74 edits were made rather than after.

What survives:

- **Do not ship the `_blur` helper for the way it looks.** It does not look
  like anything.
- The one argument left is that the app, the bloom spread and the clip show
  three different glow widths, so every FUTURE look decision is made on a
  picture that is not the one that ships. That is real and it is invisible
  today. It is a reason to fix this the next time a look call is being made,
  not a reason to spend a session now.
- **Step 3 does not depend on it after all.** The k = 1 identity means raising
  `--w` to 1080 needs no sequencing: at 1080 the helper is a no-op, so there is
  nothing for it to cancel. The fix-then-raise ordering in §7 was insurance
  against a picture changing twice, and with the fix parked the insurance is
  not needed.

> **The cheap test earned its keep and the expensive one was not run.** Two
> clips and a sentence from Rick closed a nine-step item that this brief had
> priced at 129 edits and an `engine_ab` pass. `CLAUDE.md` §6: six percent of
> a session changes a decision, and it is the cheap six percent.

The k = 1 identity is **asserted, not assumed**: 1080 patched and 1080 unpatched
come back bit-identical for all three relics, so §7's sequencing (fix, then
raise `--w`) holds and Rick reviews one change rather than two.

Sheets: `05-reference/post/blurscale-spread-dawnbringer-lastlight-foregone-540.png`
and the `-crop` variant.

### The fix, and it is one line repeated

Make glow resolution-independent by honouring the invariant the constructor
already claims:

```js
_blur(px){ this.ctx.shadowBlur = px * this.k; }     // one helper
```

129 mechanical replacements. `Renderer` is not the sim, so `engine_ab` proves
it free by construction — but it **changes every glow in the game at every
resolution except 1080**, so it is a Rule 2 spread, not a refactor.

**Sequence matters.** Fix `shadowBlur`, *then* raise `--w`, and the two changes
cancel: at `k = 1` the helper is a no-op, so a 1080 capture looks exactly as it
does today and every smaller surface finally matches it. Do them in the other
order and Rick reviews a picture that changes twice.

---

## 2. THE PATH AS IT STANDS — FOUR LOSSY GENERATIONS

| # | stage | where | what it costs |
|---|---|---|---|
| 1 | `AC.setResolution(540, 960)` | `cinema_clip.py:418`, `--w` default `540` (:333) | three quarters of the pixels |
| 2 | `toDataURL('image/jpeg', 0.80)` | `cinema_clip.py:91`, `--q` default `0.80` (:334) | DCT ringing on every high-contrast edge, 4:2:0 chroma |
| 3 | `scale=1080:1920:flags=lanczos` | `shorts_build.py` encode | resampling detail that no longer exists |
| 4 | `libx264 -preset veryfast -crf 23` | same | bits spent badly on fast fine detail |
| 5 | the platform re-encodes to ~1.5–2.5 Mbps | TikTok | see §4 |

`CLAUDE.md` §5's canonical command passes `--w 540`, so the documented way to
make a clip is the lossy way. **`540` is defended nowhere** — two argparse
defaults and one doc line, no comment, no measurement. Same shape as
`post_build.py`'s wrong `--src` and `shot.life: 3.4`: an undefended number that
became policy.

---

## 3. THE TARGET PIPELINE

### 3.1 Capture at native

`--w 1080` → `AC.setResolution(1080, 1920)` → `k = 1.0` → **no resampling
anywhere in the renderer.** This is the resolution the art was designed in.
Do it *after* §1's fix.

### 3.2 Lossless frames — and there is a landmine

```js
document.getElementById('cv').toDataURL('image/jpeg', q).slice(23)
```

`.slice(23)` is the length of `"data:image/jpeg;base64,"`. The PNG prefix
`"data:image/png;base64,"` is **22**. A naive swap to PNG keeps the 23 and
silently drops the first base64 character of **every frame** — a corrupt file
with no error anywhere. Use `s.slice(s.indexOf(',') + 1)`.

Then `.jpg` → `.png` at `cinema_clip.py:270`, `:292`, `:413`, `:486` and in
`shorts_build.py`'s glob and `-i` pattern.

**Cost:** PNG encode in-canvas is slow and base64 adds 33%. Measure it. If it
dominates, the better answer is to skip image compression entirely and pipe raw
RGBA to ffmpeg's stdin (`-f rawvideo -pix_fmt rgba -s 1080x1920`) — that is
both the most pristine option and possibly the fastest. Do PNG first because it
is a four-line change; treat rawvideo as the follow-up if the number says so.

### 3.3 Delete the upscale — conditionally

Drop `scale=1080:1920:flags=lanczos` when the capture is already 1080.
**Conditionally**, keyed on the capture width, or every non-1080 capture breaks.
Resampling a correct-size image is pure loss.

### 3.4 Two files, not one

| file | settings | purpose |
|---|---|---|
| **master** | `-c:v libx264 -preset veryslow -crf 0` (or FFV1) | archival, review, filmstrips, the thing FX work is judged on. Local, gitignored. |
| **delivery** | below | the only file that is uploaded |

```
-c:v libx264 -profile:v high -level 4.2 -preset veryslow -crf 16
-pix_fmt yuv420p
-x264-params aq-mode=3
-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv
-movflags +faststart
-c:a aac -b:a 256k -ar 48000
```

Why each, so none of it is cargo:

- **`aq-mode=3`** biases bits toward dark regions. The arena floor is `#07050C`.
  Default is `aq-mode=1`. This is the single most content-specific knob
  available and it is aimed exactly at this game. **A/B it — do not assume it.**
- **`-crf 16`, `-preset veryslow`** — the platform re-encodes from decoded
  frames, so the source only has to be visually lossless. Below ~16 buys
  nothing; `veryslow` is free quality in exchange for minutes.
- **`yuv420p`** is forced by delivery compatibility. It halves the chroma
  resolution of precisely the saturated blues and reds the schools are built
  on. Nothing to do about it, everything to design around — §4.
- **The colour tags** stop players and the platform guessing. Untagged video
  gets interpreted differently in different places.
- **`-color_range tv`** is the one to be careful with. The canvas is full-range
  sRGB; limited-range delivery maps 0–255 into 16–235. `#07050C` is luma ~5 and
  the white cores are 255, so **both ends of this game's range sit exactly
  where a double conversion crushes.** Render a black-to-white ramp through the
  whole pipeline once and read it back. Get this wrong and the blacks flatten
  everywhere and nobody will be able to say why.
- **`-movflags +faststart`** puts the moov atom first; helps ingest.

### 3.5 Do not use H.265

Both sources checked say the same thing: TikTok's clean path is H.264, and
HEVC triggers extra processing. There is no upside here — the file is small
either way.

---

## 4. THE CEILING, AND WHY IT IS AN ART CONSTRAINT AND NOT JUST AN ENCODER ONE

TikTok transcodes everything server-side to H.264 and delivers 1080p at roughly
**1,500–2,500 kbps**, applying temporal noise reduction and 4:2:0 chroma along
the way. Two independent third-party guides agree; TikTok publishes no spec, so
treat the exact numbers as approximate and the shape as reliable.

Three consequences, and the third is the one that matters most:

1. **Beyond visually lossless, more source bitrate buys nothing.** The platform
   decodes to frames and re-encodes. Hand it a clean picture, not a big file.
2. **60 fps at a fixed bitrate is half the bits per frame of 30.** Still right
   for this content — it is fast motion, and TikTok itself recommends 60 for
   fast scenes — but it is a trade, not a free win, and it should be named.
3. **The art has to survive ~2 Mbps plus temporal denoising plus 4:2:0.** What
   dies: fine grain, dense small high-contrast particles, thin saturated
   chroma-carried lines. What lives: broad shapes, luma-carried contrast,
   coherent motion.

> **That last point feeds straight back into `FX-RUNTIME-BRIEF.md` §3.** A
> particle system that reads as gorgeous in the master and dissolves into mush
> at 2 Mbps is not an upgrade. Bias the FX work toward luma contrast and
> coherent shapes over fine chroma detail — and **measure it through the
> platform** rather than trusting either of us.

---

## 5. THE ACTUAL "SPARE NO EXPENSE" MOVE — SUB-FRAME MOTION BLUR

`CONFIG.physics.dt` is 1/120 and output is 60 fps, so **every delivered frame
throws away one sim step.** `RENDER-LAYERS.md` §5c already asked for the fix
from the other direction: *"accumulate at the sim's 120 Hz rather than the
render's 60."*

Render both sim steps and average them into one output frame. N=2 is exactly
sim-aligned — no interpolation, no invented state, and offline it costs one
extra draw per frame and nothing else.

This is the highest-value item in this document after §1, because:

- it puts the sim's extra temporal information into the frame the viewer sees;
- it is **the** fix for the beading artefact that killed trails, so the trails
  decision is worth re-opening once it exists;
- motion blur compresses *better* — it removes exactly the high-frequency
  frame-to-frame difference that eats a 2 Mbps budget. **It improves the
  picture and lowers the bitrate cost at the same time**, which almost nothing
  else here does.

Determinism is unaffected: averaging introduces no randomness.

### BUILT AND MEASURED — 2026-08-28

`cinema_clip.py --motion-blur N`. Each output frame is the mean of N
sub-frames, accumulated incrementally so no divide is needed at the end.

**IT WAS NOT PROVABLY FREE.** `CINE.pump` is not linear in `raw`: it advances
the director's phase clock, and below `timeScale 0.02` it calls
`m.decayImpactOnly(raw * 0.85)`, which touches MATCH state. `run_pass` prints
the fight as four numbers so the arms can be diffed, and on
paradox v heartwood 25064:

```
  N=1   over=True  t=46.4083  clanks=17  hp=[17, 0]
  N=2   over=True  t=46.4083  clanks=17  hp=[17, 0]
```

**Identical — the fight is untouched.** Only the verdict-hold tail differs, by
two frames, because it waits on an event rather than a frame count. (46.4083 is
also `CLAUDE.md` §4.2b's recorded value for this seed on the pinned pair, so
the runtime is intact.)

### AND THEN RICK WATCHED IT: "THE BLUR ON IT SEEMS TOO STRONG"

He is right, and the reason is not the strength. **N = 2 does not make a smear.
It makes a double exposure.**

Two samples across a frame interval draw a fast relic TWICE at half opacity.
There is no continuum between the two positions because there is no third
sample to put there, so the eye reads an echo rather than motion. Turning it
down does not fix that — it only thins the second copy.

The measurement says the same thing and it is the tell. Edge energy against the
blend weight S is **not monotonic**:

```
   S           0.00     0.25     0.50     0.75     1.00
  frame 400      0%    -4.9%    -8.0%    -8.4%    -6.1%
  frame 300      0%    -6.3%   -10.0%   -10.8%    -7.9%
  frame 120      0%    -8.5%   -13.7%   -14.5%    -8.5%
```

It bottoms out near S = 0.75 and comes back UP at S = 1.0. A real shutter angle
cannot do that — more exposure is always more blur. A two-sample pair can,
because an EQUAL-weight pair reads as two distinct edges while an unequal one
reads as one edge plus a faint ghost, and a gradient metric prefers the ghost.
**The non-monotonicity is the proof that this is not blur.**

> **So `--shutter` is misnamed if it is read as an angle, and its help says so.**
> It controls how much of the earlier copy survives — 50% at 1.0, 25% at 0.5,
> 12.5% at 0.25. That is a ghost-opacity knob, not an exposure.

**What a real one needs.** 8–16 samples across the interval, i.e. drawing the
world at times BETWEEN sim steps. The engine can already do that:
`CINE.drawLerped(renderer, m, alpha)` draws an interpolated frame and the
capture loop already calls it. What is missing is a snapshot outside a cut —
`CINE.pump` only takes one when `interp && this.cut`. So sub-frame sampling is
free exactly during cuts and needs a snapshot path everywhere else.

> **What §5 got right and what it got wrong.** Right: the sim carries temporal
> information the picture throws away, and putting it back is the highest-value
> item here after §1. Wrong: that N=2 is enough to do it, and that it costs
> "one extra draw per frame and nothing else." The honest number is 8–16 draws
> per output frame plus a snapshot path in `CINE` — which is a change to the
> director, and therefore Rick's call rather than a capture-tool flag.

---

## 6. THE UPLOAD PATH — FREE, AND NOT IN THE CODE

Not Claude Code's work, but part of "pristine", and it costs nothing:

- **Upload from desktop web at tiktok.com, not the phone.** Both sources checked
  say the mobile app re-encodes on device before upload; cellular is worse than
  wifi.
- **Turn on "Allow high-quality uploads"** in TikTok's app settings.
- **Never cross-post** from another app — that is a guaranteed double encode.

Third-party guidance, not TikTok's own documentation. Cheap to follow, and §7's
round trip is what would actually confirm it.

---

## 7. THE ORDER, AND THE GATES

Every stage ends with Rick looking at frames. `CLAUDE.md` §4.1: when a person
catches what no tool could, the deliverable is a measurement of what they saw.

```
1  shadowblur_probe.py           DONE 2026-08-28. Confirmed on the pinned pair;
                                 --census added; §1 corrected on three points
1b blurscale_spread.py           DONE. The step-2 spread, rendered without
                                 touching the build. Sheets in 05-reference/post
2  the _blur(px) helper          PARKED 2026-08-28. Two clips in front of
                                 Rick: "i truthfully cant tell the difference
                                 between them." Not a picture win; do not
                                 spend the 74 edits on looks alone
3  --w 1080 default              NO LONGER GATED ON 2. The helper is a no-op
                                 at k=1 (asserted bit-identical), so there is
                                 nothing to sequence against
4  lossless frames               mind the .slice(23); measure the encode time
5  drop the conditional upscale
6  master + delivery encodes     A/B aq-mode=3 on and off, same seed
7  the range ramp                one black-to-white ramp, read back, before anything ships
8  sub-frame motion blur         BUILT 2026-08-28, --motion-blur N. Fight
                                 telemetry identical at N=1 and N=2, so it is
                                 a picture change and not a fight change.
                                 -3.9% edge energy, -8.5% on fast frames
9  THE ROUND TRIP                post one, download it back, contact-sheet it
```

**Gate on every step:** `engine_ab` 192/192 · `post_identity.py` · four frames
off the finished mp4, looked at · and for steps 2, 3 and 8, a played clip in
front of Rick, because those three change the picture.

**Step 9 is the only one that measures the deliverable.** `08-analytics/`
already pulls retention off real posts, so the platform round trip is in this
workflow — the *picture* round trip has never been done, and until it is, every
claim in §4 including mine is inference.

---

## 8. WHAT IS NOT ESTABLISHED HERE

- ~~**§1 is measured in this container's Chromium, not on the pinned pair.**~~
  **SETTLED 2026-08-28.** `tools/shadowblur_probe.py` reproduces it on
  Chromium 151.0.7922.34 through `scpage.py`. Same result, and the site count
  came back 0-not-3, which makes the fix bigger rather than smaller.
- **Still measured on a test disc, not on real ult art.** 2.00x at 540 and
  2.24x at 453 are the reach of one blurred circle. What a 2x-wider glow does
  to a set-piece built of forty-five overlapping additive arcs is not a
  multiply, and only a frame can say. That is `ult_bloom_probe.py`'s pattern
  and it is the natural gate on step 2's spread.
- **TikTok's transcode bitrates are third-party figures.** TikTok publishes no
  encoding spec. The shape is corroborated across two sources; the numbers are
  not authoritative.
- **`aq-mode=3`, `-preset veryslow` and `-crf 16` are reasoned, not measured
  on this content.** They are the right first hypotheses and each is one A/B.
- **PNG encode cost is unmeasured** and may make rawvideo the right answer
  immediately rather than as a follow-up.
- **Whether `--w 540` had a reason is unknown.** No comment, no doc anywhere.
  Capture speed is the obvious guess and it is a guess. Write down the answer
  either way this time.

---

## APPENDIX — THE §1 MEASUREMENT, VERBATIM

This ran in Chromium and produced the table in §1. Port it into
`tools/shadowblur_probe.py` against the pinned runtime via `scpage.py`; the
`page.evaluate` body is unchanged. It needs no game — it is a property of the
canvas, which is why it is trustworthy and why it must be re-run where the
build actually renders.

```js
() => {
  const D = 1080, R = 40, BLUR = 20;
  function run(k, blur){
    const n = Math.round(D * k);
    const cv = document.createElement('canvas'); cv.width = n; cv.height = n;
    const c = cv.getContext('2d');
    c.setTransform(k, 0, 0, k, 0, 0);          // exactly what draw() does
    c.fillStyle = '#000'; c.fillRect(0, 0, D, D);
    if (blur){ c.shadowColor = '#FFFFFF'; c.shadowBlur = BLUR; }
    c.fillStyle = '#FFFFFF';
    c.beginPath(); c.arc(D / 2, D / 2, R, 0, Math.PI * 2); c.fill();
    const d = c.getImageData(0, 0, n, n).data, cy = (n / 2) | 0;
    let last = 0;
    for (let x = 0; x < n; x++) if (d[(cy * n + x) * 4] > 8) last = x;
    return last - n / 2;                        // device px from centre
  }
  const out = {};
  for (const k of [1.0, 0.5, 453/1080]){        // clip, half-clip, the app
    const bare = run(k, false), glow = run(k, true);
    out['k=' + k.toFixed(3)] = {
      discDevicePx: bare,
      blurOnlyDevicePx: glow - bare,
      blurOnlyDesignPx: +((glow - bare) / k).toFixed(1)
    };
  }
  return out;
}
```

**Measure the disc separately and subtract it.** The first version of this test
measured total reach and reported "shadowBlur IS scaled" — wrong, because the
disc radius scales and the blur does not, and one number over both could not
tell them apart. That is `CLAUDE.md` §4.1c happening to the instrument instead
of to the art, and it is the reason the third column exists.

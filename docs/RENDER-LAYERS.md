# THE RENDER LAYER — what `draw(m)` draws, in what order, and what may bloom

**Step 1 of `docs/RENDERER-BRIEF.md` §8.** Read before writing a line of the
post chain. Everything below is read out of the build of record
(`02-chain/sc-paradox-frame.html`) or measured off the live renderer; nothing
here is inferred from the shape of the code.

---

## 1. THE FRAME, MEASURED

Read off `renderer` in a running page, not computed by hand:

```
W x H          1080 x 1920      design space, always
k              backing/1080     the ONE place the backing store differs
hud            152              BAND.pos = "top"
arenaTop       176              = hud + 24
scale          2.03076923       = min(1056/520, 1732/800) -- WIDTH-bound
aw x ah        1056 x 1624.62   CONFIG.arena is 520 x 800 sim units
pad            12               = (W - aw) / 2
FRAME.foot     0                shipped at zero; Rick rejected 340 twice
```

Which puts every band in the frame at a fixed y, and **they do not overlap**:

```
   y 6 .. ~100     HUD          drawBar x2: sigil r42 at cy 52, charge bar 48..63
   y 104 .. 174    TUG plate    fillRect(0, y-8, W, h+14), y = arenaTop-56-8
   y 176 .. 1800.6 ARENA        the clip rect. +70px bleed while a cut runs.
   y 1846.6        footer       one line of text
```

**The arena rect is the seam the whole post chain hangs on.** It is
`(12, 176) -> (1068, 1800.6)` and the HUD sits entirely above it. That is
geometry, not draw order — a pass restricted to that rect cannot touch the HUD
even if it wanted to.

---

## 2. THE CALL ORDER, EXACTLY

`draw(m)` runs in **four transform regimes**. Knowing which one a layer is in
matters more than knowing its name, because it decides what a post pass has to
undo to find it.

```
=== A. DESIGN SPACE ============================ c.setTransform(k,0,0,k,0,0)

  SHAPES._t = m.t                     presentation clock; the sim cannot read it
  if (m.introT > 0 && !_introScene) -> drawIntro(m); RETURN   <-- whole frame
  scrunch: pad/aw/ah/scale shrink by scrunchK(m), restored at the bottom
  c.save()
  fillRect(0,0,W,H) #07050C           the ground
  drawHud(m)                          UNLESS _introScene.  drawBar x2, _ultSigil

=== B. ARENA-LOCAL PX ===================== translate(pad+shake, arenaTop+shake)
                                          punch zoom (hitStop), clip to arena
                                          rect (-70 bleed during a cut),
                                          CINE camera translate/scale
  drawArena(m)                        hall floor, walls, wall glow

=== C. SIM UNITS ============================== c.scale(scale, scale)

   1  drawMotes(m)                    lighter
   2  drawUltUnder(m)                 lighter x2, 12 radial gradients
   3  drawFx(m)                       lighter
   4  drawShadeFire(m)                lighter          "an aura, under everything"
   5  drawSplitHold(m)                lighter
   6  drawShades(m)                   the copies, under the real pair
   7  drawDrips(m)
   8  drawVines(m, false)             the garden is ON the wall
   9  drawFighter(m, m.b)             lighter x2  (relic body, cracks, liquid,
  10  drawFighter(m, m.a)              status, weapon, aegis, field, window)
  11  drawDrains(m)                   lighter x2   "a mote's last act is going IN"
  12  drawShots(m)                    lighter x5
  13  drawStuck(m)                    lighter
  14  drawSparks(m)                   lighter
  15  drawVines(m, true)              lighter x3   a lash is a strike, so it is over
  16  drawUltName(m)                  lighter x4
  17  drawUltOver(m)                  lighter x16, 52 shadowBlur  <-- the big one
  18  drawRings(m)                    lighter
  19  drawFloats(m)                   TEXT. damage numbers, sized in device px
  20  drawTags(m)                     TEXT. status names at the contact point
  21  drawCineStreaks(m)              lighter, only while CINE.streak > 0.01
  c.restore()

=== D. BACK TO DESIGN SPACE =====================================

  drawCine(m)         tracer  lighter, clipped to arena rect
                      wash    DARKENING radial scrim, clipped
                      flash   lighter, clipped
                      bars    OPAQUE #05040A letterbox, clipped, h*0.115 each
  kill flash          lighter, clipped to arena rect, only while m.finisher > 0
  drawArenaFrame()    gold border + corner flourishes
  drawClock(m)
  drawBanner(m)
  drawFooter(m)       suppressed for the whole scrunch
  drawTug(m)          paints an OPAQUE plate across the full width at y 104..174
  drawResult(m)       only when m.over, and not when the scrunch panel has it
  c.restore()
  if scrunched: restore pad/aw/ah/scale, setTransform, drawScrunchPanel(m, k)
```

---

## 3. EMISSIVE vs UI — AND THE EVIDENCE, NOT THE OPINION

The classification is not a judgement call for most of it. **A layer that sets
`globalCompositeOperation = "lighter"` is telling you it is light.** Counted
across the whole `Renderer`:

```
drawUltOver  16    drawShots    5    drawUltName 4    drawVines 3
drawCine      2    drawUltUnder 2    drawFighter 2    drawDrains 2
_drawBalWindow 2   and one each in 14 more
```

### Bloom SHOULD reach these

Everything in regime **C** except items 19 and 20, plus `drawArena`'s wall
glow, plus `drawCine`'s tracer and flash, plus the kill flash.

**All of them are already inside the arena rect** — the cine overlays and the
kill flash clip to it explicitly, and regime C is inside the same clip. There
is no emissive art anywhere else in the frame. That is the single fact that
makes a composite-first post chain cheap here.

### Bloom MUST NOT reach these

| layer | regime | why |
|---|---|---|
| `drawHud` / `drawBar` / `_ultSigil` | A | readout. Above the arena rect, so free. |
| `drawTug` | D | opaque plate; a bloomed health bar reads as a bug |
| `drawArenaFrame`, `drawClock`, `drawBanner`, `drawFooter`, `drawResult` | D | chrome |
| `drawScrunchPanel` | D | the card |
| **`CINE.bars`** | **D** | **letterbox. It is INSIDE the arena rect.** |
| **`drawFloats`** | **C** | **damage numbers. INSIDE the world transform.** |
| **`drawTags`** | **C** | **status names at contact. Same.** |

**The last three are the whole difficulty.** A pass over the arena rect gets
the first four for free by geometry, and then bloom bleeds light into a black
letterbox and smears the damage numbers.

### `CINE.wash` and the vignette — MEASURED, and smaller than it was billed

`tools/post_grade_probe.py`, four conditions on the same cut frames, mean luma
inside the arena rect:

```
frame  tier   wash   A base    B vig  C stack  D yield      A-C     A-D
  150    T2  0.300   42.940   43.078   41.419   42.263    1.521   0.677
  704    T3  0.420   22.397   27.012   21.591   22.264    0.806   0.133
 1686    T2  0.300   45.945   46.854   44.733   45.413    1.212   0.532
```

The un-yielded vignette costs **1.18 of 37.09 — 3.2%**. The yield recovers
62% of that and is kept, because it is one multiply.

**But B is BRIGHTER than A at every frame.** The scrim darkens far more than
the vignette does: 4.6 luma against 0.9 at frame 704. This was never two
darkenings fighting for the same job — it is a garnish on top of something
much stronger, and the note below (written before the measurement) overstated
it. Left standing as a record of the difference between a reason and a story.

### The original note on `CINE.wash`, written before it was measured

`wash` is a darkening radial scrim centred on the point of contact, and its
comment records why: a full-frame scrim at 0.75 was invisible and a full-frame
additive flash at 0.55 blew the picture to beige, both from "treating the frame
as the subject". **A post chain's vignette and grade want to do that same job.**
Two of them stacked will over-darken. Decide which owns it before adding the
second; do not add a vignette and leave `wash` running.

---

## 4. WHAT THIS MEANS FOR THE SEAM

Three buckets, not two:

```
WORLD    regime B + C, minus drawFloats/drawTags       -> offscreen, post-processed
         + CINE tracer/flash + kill flash
OVERLAY  CINE wash, CINE bars                          -> composited after, flat
UI       drawHud, drawTug, frame, clock, banner,       -> composited after, flat
         footer, result, scrunch panel, floats, tags
```

`drawFloats` and `drawTags` are called from inside the regime-C block, so
splitting them out means **moving two call sites** — a change to `Renderer`,
which is allowed (`Renderer` is not the sim, and `engine_ab` proves it), but it
is a change and it should be one commit on its own with a filmstrip.

The alternative is to accept bloomed damage numbers. It is not obviously wrong
— they are already stroked in `#000000BB` and might survive it — **and that is
a picture question, so it is Rick's, and it should be shown as a spread rather
than argued.**

> **ANSWERED 2026-08-27 — and then reopened the same day by a second relic.**
>
> On the bloom spread (`bloom-spread-paradox-heartwood-25064.png`) every damage
> float still read at MID, and the conclusion written here was that the split
> was optional. **That was true of Paradox and false in general.**
>
> `chosen-spread-ironhail-dawnbringer-4412.png`, same settings, different art:
> the `18` and its SMITE tag at t=16.2 and the `17` and its SMITE at t=25.9 are
> **gone**, and the ultimate-name callout smears into an illegible shape.
> Paradox's ult art is thin blue lightning on a dark hall — close to the ideal
> case for a threshold. Ironhail and Dawnbringer are warm and broad and their
> relic bodies are already near white, so the same threshold catches the
> bodies rather than the effect.
>
> **So the split is REQUIRED, not optional.** Floats, tags and the ult-name
> callout have to leave the bloom's source, whatever register is finally
> chosen — a readout that survives one relic and not another is not a setting
> that can be tuned, it is a layering mistake.
>
> The lesson is the older one in `CLAUDE.md` §4.8: *if you generalise from a
> subset, look at the superset first.* One extra sheet, four minutes, would
> have caught this before a decision was recorded.

---

## 5. THE COST THAT IS ALREADY BEING PAID

`shadowBlur` is assigned **132 times** — 111 inside `Renderer`, 21 in the
top-level helpers — and `weaponGlow` maintains `_glowCache`, a bounded Map of
pre-blurred sprites cleared past 400 entries. `drawUltOver` alone sets
`shadowBlur` 52 times.

**That is the budget a real bloom pass would be spending instead of adding to.**
Whether it comes out ahead is a measurement (`tools/hud_cost.py` is the existing
pattern), not a promise — brief §7 gate 3.

---

## 5a. THE CHAIN IS IN THE BUILD

`tools/post_build.py` inlines `src/render/post.js` and adds `POSTFX` plus ONE
hook at the top of `Renderer.draw` — the single method every path into the
picture goes through, so the live loop, `AC.__draw` and `CINE.drawLerped` are
all covered without a second code path.

```
sc-paradox.html
  -> cineexport_build   CINE on the export surface
  -> readouts_build     renderer.roMode, the readout split
  -> post_build         the chain, inlined, ON
  -> frame_build        the tip
```

`#cv` stays the one canvas every tool reads. `POSTFX.frame` draws the readouts,
copies them off, draws the world, composites, and puts the result back on
`#cv` — so `cinema_clip`'s `toDataURL`, `verify`'s non-blank check and
`render_ab`'s hash all keep working without learning a new name.

**And there is exactly ONE chain.** `POSTFX` is exported on `AC` and the app
shell *drives* it. The shell used to own its own instance, which was right
while the chain was not in the build and became a defect the moment it was:
two blooms, two grades, and an app showing a picture the mp4 cannot contain.
`npm run post` asserts the shell has not built a second one.

Without WebGL2, `POSTFX.on` goes false, `draw` runs exactly as before, and it
says so once in the console. A silent fallback is how a clip ships missing an
effect and nobody finds out.

---

## 5b. THE POST CHAIN AS IT STANDS, 2026-08-27

```
bloom    LOW    thr 0.80  int 0.35      SWBPost.SPREAD.DEFAULT
trails   LONG   0.24s tail              SWBPost.TRAILS.DEFAULT
cut ramp GENTLE cutGain 0.6             SWBPost.CUTRAMP.DEFAULT
grade    MID    vig 0.38 grain 0.022   SWBPost.GRADE.DEFAULT
```

**What it costs, measured on the real GPU** (`tools/post_cost.py`, Intel UHD,
D3D11 — not SwiftShader, which is what Playwright would have measured):

```
                    453x805 (what the app draws)   1080x1920 (capture)
  2D draw only          7.02                          13.08
  + chain, no effects   8.52  (+1.50)                 15.97  (+2.89)
  + ALL (as chosen)     8.52  (+1.49)                 23.07  (+9.99)

  live:    51% of the 60fps budget, 102% of 120
  capture: offline, so 138% of 60fps means the render takes about 28 s
           longer over ~2,800 frames — not dropped frames
```

**At live size the whole chain is lost inside the plumbing floor.** The upload,
two copies and the readback are +1.50 ms; adding bloom, trails and grade on
top brings it to +1.49. The three effects together cost nothing measurable
there. At capture size they cost real time, and it does not matter, because
that path is not realtime.

**Bloom was MID for about an hour.** MID was chosen when Paradox was the only
evidence on the sheet. Added to it, Ironhail v Dawnbringer — relic bodies
already near white — fuses both fighters into one mass at MID by t=25.9 and
loses them entirely at HIGH. LOW is the only setting on the two-pairing sheet
where both relics stay separable on both kinds of art, and it is subtler on
Paradox's lightning than MID was. That is the price, and it was paid
deliberately.

**The readouts are no longer part of that trade.** They leave the bloom's
source at `renderer.roMode` 1 and are composited back untouched, so they read
at every setting — the structural fix, not a number.

Both chosen off filmstrips in `05-reference/post/`, both masked to the arena
rect at the bright pass AND at the composite — masking only the bright pass
stops the HUD contributing light but not light being blurred OUT onto it.

**THE RAMP IS DRIVEN BY THE DIRECTOR'S OWN NUMBER.** `CINE.wash` peaks at
each tier's amplitude — 0.30 for a T2, 0.42 for a T3, 0.55 for a kill — and
rises and falls across the beat, so one field carries both the envelope and
the tier. `amount = intensity * (1 + cutGain * wash / 0.55)`, zero outside a
cut. A second envelope written in the post chain would be a copy that drifts
the first time the director is retuned.

**AND CUTS ARE RARE.** Measured while building the ramp sheet: seed 25064 has
ONE cut in 47 s of video and ironhail/dawnbringer 4412 has none; of 72 fights
across three pairings, 42 had any cut and 8 had a kill. `CINE`'s own comment
says zero cuts in a match is a correct answer. The ramp is a garnish on a rare
moment rather than something most frames see — which is the honest reason
GENTLE is enough.

**THE TWO SETTINGS ARE NOT INDEPENDENT.** Trails were first judged against a
MID bloom. When bloom came down to LOW the sheet was re-rendered rather than
re-read, and the answer changed: under MID the long tails competed with the
bloom's own glow and the arena read as busy; under LOW they are the brightest
moving thing in the frame and read as speed. **A look chosen against a base
that has since moved is a look chosen for the wrong picture.**

**One artefact is known and was taken knowingly.** At 60fps a fast arc beads:
a flail head travels much further between frames than its own width, and a
persistence buffer can only know where it was, not where it went. The tent
softens it; it does not remove it, and the artefact scales with how many
frames of history are held — LONG holds about fourteen where SHORT held four,
so it is more visible now than it was, on the flail's arc especially.

The fix is to accumulate at the sim's 120 Hz rather than the render's 60, and
`tools/post_cost.py` has priced it: the frame is already **7.36 ms against an
8.33 ms budget at 120 Hz before the chain** on this Intel UHD. That makes it a
real trade rather than a cleanup — and it is the strongest evidence in the
repo against brief §4's claim that 120 fps is free for the asking.

---

## 6. WHAT IS NOT ESTABLISHED HERE

- **The 120 fps claim in brief §4 is unchecked.** `CONFIG.physics.dt` is 1/120
  and the loop is `rAF`-capped at 60, but `LERP_FIELDS` and `CINE.pump` have
  not been read yet and the brief says to check before assuming it is free.
- **`drawIntro` returns early and replaces the entire frame.** None of the
  above applies while `m.introT > 0`. The intro card is also rule 1's dead
  fight card, still in the build.
- Nothing here has been checked against the SCRUNCH path beyond noting that it
  shrinks four layout fields and hands them back.

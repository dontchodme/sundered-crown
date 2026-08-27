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

### The one honest note on `CINE.wash`

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

## 6. WHAT IS NOT ESTABLISHED HERE

- **The 120 fps claim in brief §4 is unchecked.** `CONFIG.physics.dt` is 1/120
  and the loop is `rAF`-capped at 60, but `LERP_FIELDS` and `CINE.pump` have
  not been read yet and the brief says to check before assuming it is free.
- **`drawIntro` returns early and replaces the entire frame.** None of the
  above applies while `m.introT > 0`. The intro card is also rule 1's dead
  fight card, still in the build.
- Nothing here has been checked against the SCRUNCH path beyond noting that it
  shrinks four layout fields and hands them back.

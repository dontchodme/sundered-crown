# THE RENDERER — brief for the first Claude Code session

**Goal, in Rick's words: "top of the line crispy beautiful animations."**

This is the brief. Read `CLAUDE.md` first, then this, then start at §5.

---

## 1. WHY THIS IS SAFE TO DO FIRST

`docs/ARCHITECTURE.md` put the renderer at phase 5, behind the module
extraction. That ordering was wrong and this file supersedes it, for one
reason that survives checking:

> **The simulation does not know a screen exists.** `Fighter`, `Match` and
> `Sfx` — lines 5382–9810 of the build of record — contain zero references to
> `document`, `canvas` or `getContext`.

So a total renderer rewrite **cannot change a fight**. `engine_ab` comes back
2760/2760 by construction, not by luck. That makes this the *safest* large
change in the plan, and there is no reason it should wait behind the riskiest
one.

What it does need is the thing that now exists: **the app**, as the place to
look at it. Numbers cannot review this work.

---

## 2. THE SIZE OF THE THING, MEASURED BEFORE PROMISING ANYTHING

`class Renderer` is **~6,800 lines across 60+ methods**, plus ~1,250 lines of
top-level helpers. Some of the heavier pieces:

```
drawUltOver          ~1160 lines    per-relic ultimate art, over the fight
drawUltUnder          ~460          per-relic ultimate art, under it
drawGlassRelic        ~360          the relic body, cracks, liquid, headspace
drawDrains            ~200          drawShadeFire ~155   drawVines ~195
drawUltName           ~250          drawIntro + _introCard ~230
seven status routines               ward smite bleed sunder entangle curse hex
drawWeapon, drawShots, litWeapon, weaponGlow, grainSprite, glassCracks,
glassVents, drawShatter, drawSparks, drawTug, drawHud, drawBar, ...
```

**Porting that to WebGL draw-call by draw-call is months, and most of it buys
nothing.** A hand-tuned Canvas 2D path for a cracked glass relic does not get
prettier by being expressed in triangles.

---

## 3. THE APPROACH: COMPOSITE FIRST, PORT SECOND (MAYBE NEVER)

Keep every existing `draw*` method exactly as it is. Render the game to an
offscreen canvas, then **run that image through a WebGL2 post chain** before it
reaches the screen.

This buys the entire "crispy" list across all 8,000 lines of art at once,
without touching one of them:

| effect | what it does here |
|---|---|
| **bloom** | real additive bloom on ult art, weapon glow, the brink pulse — replacing pre-blurred `weaponGlow` / `_glowCache` sprites |
| **motion trails** | persistence framebuffer; a ball at 1200 u/s currently draws as a hard disc with no smear |
| **chromatic aberration** | on impact, ramped by the director's own tier |
| **filmic grade + tonemap** | one place, instead of per-draw colour choices |
| **vignette + grain** | `grainSprite` already exists; this makes it a pass |
| **120 fps** | see §4 — this one is free and nobody has taken it |

Individual art pieces can migrate to native WebGL later, one at a time, each
reviewable on its own. Most will not need to.

---

## 4. THE FREE WIN NOBODY HAS TAKEN

**`CONFIG.physics.dt` is 1/120, and the render loop is capped by `rAF` at 60.**

On a 120 Hz display the renderer can run at 120 fps with **exactly one sim step
per frame** — no accumulator remainder, no interpolation error, the crispest
possible motion. The engine has been ready for this the whole time; the display
has just never asked for it.

Check `LERP_FIELDS` and `CINE.pump` before assuming it is free. It probably is.

---

## 5. WHERE THE CODE GOES, AND THE CONSTRAINT THAT DECIDES IT

**THE APP AND THE VIDEO MUST NOT DIVERGE.** If the app has bloom and the mp4
does not, that is a picture fault by construction — and it would break the one
guarantee Electron was chosen for (`docs/ARCHITECTURE.md` §1).

So the post chain is **not app-only code.** It is a self-contained module that
both paths use:

```
src/render/post.js        the compositor. No engine imports. Takes a source
                          canvas + a state object, returns composited pixels.
app/ui/post-dev.js        loads it into the running app for iteration, with an
                          A/B toggle. THE OLD PIXELS ARE THE CONTROL.
tools/post_build.py       LATER: inserts it into the chain like every other
                          feature in this project, so cinema_clip.py renders
                          through it too.
```

Iterate in the app. When Rick approves it, the builder puts it in the chain.
**Do not write the builder first** — this project's own §13 lesson is that when
the deliverable is a picture, you film before you tune.

---

## 6. HOOK IT TO THE DIRECTOR, DO NOT APPLY IT FLATLY

`CINE` already knows when something matters — it computes cuts, tiers, time
dilation and zoom before frame 1 (`cinePlan`, `cineTier`, `cineCamera`). A post
chain at constant intensity wastes that.

Aberration and bloom should **ramp with the cut tier**, so a fatal blow looks
like one. `TIER_KILL` already carries `lead`, `dropFrom`, `dropTo`, `ramp`.

---

## 7. THE GATES

1. **`engine_ab` stays 2760/2760.** Trivially true — but run it, because "it
   cannot have changed the sim" is exactly what someone says right before they
   find out they wired the post chain into a shared canvas the sim reads.
2. **Side-by-side filmstrips at every step.** Old renderer and new, same seed,
   same frame indices, one image. This is the real review and it is Rick's.
3. **Frame cost measured, not felt.** `tools/hud_cost.py` is the existing
   pattern. A post chain that adds 8 ms is not free at 120 fps — it is the
   whole budget.
4. **The A/B toggle ships.** Not a dev flag that gets deleted; the control has
   to stay available or later comparisons have nothing to compare to.

---

## 8. WHAT TO DO FIRST, IN ORDER

1. **Read the render layer and write down what it draws, in what order.** Not
   all 6,800 lines — the `draw(m)` method's call order, and which layers are
   emissive (bloom should reach them) versus UI (it must not — a bloomed HUD
   reads as a mistake).
2. **Get one pass working end to end** — source canvas → framebuffer → a single
   trivial shader → screen — with the A/B toggle, before any effect exists.
   The plumbing is where this goes wrong, not the maths.
3. **Bloom first**, because it is the one that will make Rick say yes or no to
   the whole approach.
4. Then trails, then the director hook, then grade/vignette/grain.
5. **Ask about the look.** Rule 2 in `CLAUDE.md`: the ult animations are one of
   the seven things Rick gives input on. Offer a spread — three bloom
   intensities rendered on the same seed — not one guess. v43 landed its sound
   in one round trip that way; v42 took four.

---

## 9. WHAT NOT TO DO

- **Do not edit any file in `02-chain/`.** Every one carries a `GENERATED by`
  stamp. A previous session wrote twelve tuned damage values into generated
  HTML and lost all twelve on the next rebuild.
- **Do not start the module extraction.** It is not a prerequisite (§1) and
  starting it here turns a safe change into a risky one.
- **Do not delete the Canvas 2D path.** It is the control, permanently.
- **Do not touch the sim to "help" the renderer.** If the picture needs
  something the sim does not expose, say so and stop — that is Rick's call.

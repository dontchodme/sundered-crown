# v63 — THE UMBRAL SCYTHE SILHOUETTE, REDRAWN FROM RICK'S REFERENCES. `_scMoon`.

**DESIGNED — Cowork, 2026-09-02 04:35 UTC. Rick chose arm A, THE MOON. The
spec is §4 and `06-docs/v63/scmoon_spec.js`; build notes for Code are §5.**
Cowork owns this redraw (CLAIMS.md, 03:58 UTC); Claude Code's
`tools/umbral_scythe_lab.py` candidates (A–F, G–J) are **superseded**.
`_scEaten` is out.

References, Rick's: `06-docs/v63/ref-scythe-1.jpg` (neon blue-violet crescent,
hot magenta edge, faceted hub with a gem, jointed shaft, hex pommel gem),
`ref-scythe-2.jpg` (chrome sickle, pink glowing blade, big ring hub with a hot
core, two prongs, knuckled shaft), `ref-scythe-3.jpg` (black spined blade,
purple edge, chain-wrapped shaft).

---

## 1. What the three references share — the read Code's spread missed

Code's spread kept `_scBase`'s crescent (a ~90° hook, a third of the weapon's
footprint) and varied what hung off it. Rick, shown it: none of these. The
references disagree with `_scBase` at the level of PROPORTION, not decoration:

- **The blade is big.** In all three the blade is roughly half the weapon's
  footprint — a long band sweeping 150–180°, its tip curling back toward the
  shaft. Not a short hook on a long pole.
- **A hub at the junction.** Ref 1 a faceted plate with a gem; ref 2 a ring
  with a hot core; ref 3 a bulb. The type has a 5px collar.
- **A jointed shaft with a pommel.** Knuckles on 1 and 2, chain on 3; a gem or
  spike at the butt on all three.
- **A hot edge on a near-black body.** All three. `_whGnawed` already took the
  umbral hammer near-black; this is the second umbral weapon to go there.

## 2. The spread — `tools/umbral_scythe_moon_lab.py`, `05-reference/v63/umbral-scythe-moon-candidates.png`

Four blades on ONE hub, shaft and surface treatment, so the sheet varies the
one thing Rick asked about. Plus the shipped `_scEaten` as the control.

```
    A  MOON     a thin band sweeping ~175°, tip curling back to the shaft (ref 1)
    B  TALON    longer, shallower, needle tip; RING hub with two prongs (ref 2)
    C  REAPER   broad blade, five spines grown from its back; chained shaft (ref 3)
    D  WANE     the moon plus a hooked spur off the hub (what all three share)
    E  SHIPPED  _scEaten, the control
```

Construction, every arm:

- **The honed edge is a single cubic** (it carries the glow stroke, so it must
  be clean). **The back edge is the honed edge pushed out along its outward
  normal by a width profile `w(t)`** — so the blade's width is one function,
  not a second hand-placed curve that can disagree with the first.
- **One closed path per blade, spines included** — honed edge root→tip, back
  edge tip→root with any spine lifted off it as three vertices on the outline.
  v58's rule (a limb goes INTO the outline, never behind it).
- **The hub is drawn after the blade and the blade's root sits inside it**, so
  the join is hidden at every zoom.
- Surface, shared: near-black body (`_ink(p.dark, 18–30)`), a cold steel rim
  on the back, the honed edge lit twice (wide soft `core`, tight `glow`), gem
  cores on the hub and pommel drawn `lighter`. The school mark (tarnish) rides
  the hub plate.
- **The blade's reach is printed by the lab** because art is free to the sim
  but not to the eye. Sim reach 1.00 L; shipped crescent 1.02 L; A/D 1.08 L,
  B 1.06 L, C 1.10 L. All pulled in from a first cut at 1.13–1.15 L.

The sheet's right column is a **real fight frame** (duskreave vs lastlight,
seed 33581, t=7.04s, blade broadside, relic clear of the walls) at the 540×960
the game delivers, cropped and shown at 2× nearest — the same frame for every
arm, since art cannot move the sim. Code's lab cut its ship-size column as
untrustworthy; this one is a frame, not a scaled zoom, and passes the check
Code named (the weapon is smaller than the zoom panel beside it).

Seen at ship size: the moon (A/D) reads as a large hook, the hot edge and the
cold rim carry it, the dark body is a band between them. The pommel gem sits
inside the ball and is invisible in play — cosmetic at zoom only.

## 3. Rick's choice — A, THE MOON (2026-09-02 ~04:30 UTC)

From the four, as-is. A thin blade sweeping ~175°, its tip curling back toward
the shaft; the faceted hub with a lit gem; the jointed near-black shaft with a
hex gem at the butt. Named `_scMoon` here for the builder; the name is a
function name, not a fiction, and Code may keep it.

## 4. The spec — `06-docs/v63/scmoon_spec.js`, CHECKED

The standalone `SHAPES._scMoon(c, L, W, p)` — no lab helpers, only `_ink`,
`_shade`, `_litN` and `_makerMark`, which every scythe grammar already calls.
It is the file beside this one, verbatim, and it is what Code pastes.

**It was checked, not assumed** (`tools/scmoon_check.py`,
`05-reference/v63/duskreave-moon-spec-check.png`):

```
  spec vs lab arm A, through litWeapon at zoom 3.2:   0 pixels differ (>8/255)   PASS
  control, lab arm A vs shipped _scEaten:        146,916 pixels differ            PASS (the diff can see)
  three world angles (-0.55, 0.9, 2.4 rad):            the lit face mirrors with _litN, the
                                                       glow stays on the honed edge
  a real fight frame, duskreave vs lastlight,
  seed 33581, t=7.04s, 540x960:                        05-reference/v63/duskreave-moon-arena.png
```

So the function in the spec file draws exactly the picture Rick chose from,
and the instrument that says so was shown a difference it could see.

Runtime: this container's Playwright Chromium (`chromium-1194`), not the
repo's pinned 151. It is a canvas-2D picture with no sim in it; Code's
`--arena` frame on the pinned build is the reproduction that matters.

## 5. Build notes for Code

1. **Paste `_scMoon` into `SHAPES` beside `_scEaten`** (from
   `scmoon_spec.js`, comment and all) and **route `umbral` to it** in
   `SHAPES.scythe`'s dispatch: `if (key === "umbral") return SHAPES._scMoon(c, L, W, p);`
2. **Delete `_scEaten`** — v58's precedent (`_whEaten` deleted, `_whGnawed` in
   its place), and nothing else calls it. `_gsEaten` and `_tbEaten` are
   separate functions and are untouched.
3. `duskreave_build.py`'s refusal #4 checks that `SHAPES.scythe` routes
   `umbral` to `_scEaten` — it must now check for `_scMoon`, or the builder
   refuses its own build.
4. Gates: **engine_ab must be identical** (the function touches nothing the
   sim reads; a non-zero diff means something was pasted into the wrong
   scope); the art A/B on all 33; `silhouette_probe` will now SEE this grammar
   (no destination-out, so nothing goes white-on-white — §2b of the build log
   no longer applies to the umbral panel).
5. **Film it and show Rick** — `duskreave_sheet.py --arena` on the pinned
   Chromium. The shape is his; the SIZE question (is the hub gem too bright at
   540, does the cold rim survive the bloom) is one a sheet cannot answer and
   he has not been asked.
6. Not this build's: the pommel gem sits inside the ball in play and is
   visible only at zoom. Left in — it costs nothing and the intro/zoom shots
   see it. The `_scOuter` inverted-normal item is not inherited (the moon does
   not call it) and is not fixed.

# v91 — NIGHTGLASS / BACKLASH. THE UMBRAL STAFF, the 44th cell. Its spell is a shadow that comes off the walls; its ultimate is a shroud that throws every blow it takes back at the foe, cursing.

**DESIGNED — Cowork, 2026-09-27. Build from `NIGHTGLASS-BUILD-BRIEF.md`; do
not design this cell elsewhere; claimed in `06-docs/CLAIMS.md`.** Rick accepts
or rejects from this file. Lab: `tools/overlays/staff_umbral.js`; runs in
`06-docs/v91/runs/`. The row: `06-docs/v89/STAFF-ROW-v89.md`.

## Why this cell

Umbral's status is a MEMORY, not a rate: curse remembers the blow that
applied it and reflects 8% of the remembered blows onto every later hit
(v49). The umbral bow (Gloamwire) sits at the top of the roster off a carry
its stream feeds. The umbral bow body at blade 7.3 is **0.3%** — the school's
channel does nothing on a bow that cannot land a big blow. A staff whose
spell lands more, and whose ultimate is the school's own idea (a blow
remembered and returned) turned on the caster, is the cell.

---

# 1. §1 (Cowork)

> **SHADEBOLT (the spell).** The staff throws a bolt of shadow every 0.34s
> along its facing, at an arrow's speed. It does not die on the wall — it
> ricochets, twice, and every landing curses.
>
> **BACKLASH (the ultimate).** For 8s the caster is shrouded. Every blow it
> takes is remembered and thrown straight back: half the damage, at once, as
> a blow of its own that curses the foe with its memory.

Two clauses: the ricochet (the spell — the misses come back, umbral's oldest
sentence, v61); the reflection (the ultimate — the school's mechanic, which
remembers blows and reflects them, applied to the blows the caster TAKES).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141.0.7390.37, `sc-leaf`, Ironhail's bow as
`umbral × staff` (`onHit {curse:1}`, own ultimate off), the spell as
`shot {cadence 0.34, speed 380, r 22, life 4.0, grav 0}` with `bounce 2` on
every shot (the engine's own wall bounce: the kunai's, 0.88 a wall). The
reflection watches `hp + shield` each window frame and, when it drops, deals
`refl ×` the drop through `m.hurt` and pushes the blow into the foe's curse
pool. The row's control (v89 §4) reproduced v75 to the fight. Arm A is the
umbral BOW body at the staff's blade.

# 3. THE RICOCHET IS TWO MORE SHOTS FOR THE PRICE OF ONE

Blade 14, 330 an arm (`runs/umbral_14`):

```
arm                                            win     hits in/out   bounces/cast   thrown back/cast
A  bow body                                   14.5%       — / 17.8
S  shadebolt (bounce 2)                       88.2%     9.1 / 17.1       47
U  shadebolt + Backlash (refl 0.5)            95.5%     8.5 / 16.0       48            28 of 54 taken
W  plain ARROW + Backlash                     38.2%     6.4 / 10.8        0            35 of 67
X  shadebolt + Backlash at refl 1.0           98.2%     7.6 / 15.5       50            49 of 49
```

**A bolt that bounces twice lands 26 blows a fight where the arrow lands
18** — and its blade is the same, so at 14 the spell alone is 88%. The
blade comes down (§4). Backlash on the plain arrow is +24 (W), and at full
reflection (X) the spell is untouchable; **refl 0.5 is kept**: at the blade
the row lands on it is +28 (§3.1), and a shroud that returns EVERYTHING
turns the close range — the type's whole weakness — into a place the foe
cannot go at all.

## 3.1 Settled — blade 7.3, 660 an arm (`runs/settle_umbral`)

```
A  bow body                0.3%
S  Shadebolt              18.0%     +18       14.6 / 22.2 hits in/out · 43 bounces a cast
U  + Backlash             45.5%     +28       13.6 / 21.4 · 35 thrown back of 67 taken a cast · foe at 3.0 curse on a window frame (the pool full)
```

The foe is at a FULL curse pool on every window frame: every reflected blow
is a memory, and the pool of three keeps the last three (v63's rule), so
the shroud's blows are the ones the pool holds and every later shadebolt
lands them again at 8% each.

# 4. THE BLADE

```
blade    spell (S)    whole (U)
 7.3     18.0%        45.5%
 8       26.7%        58.5%
10       53.9%        80.0%
14       88.2%        95.5%
```

**Crossing near 7.6** (45.5 at 7.3, 58.5 at 8 — the block spread at 660 is
~3pp, v87). The body is ~20%. Expect 7.5–7.8 on 151. A blade of 7.6 on a
bolt that lands 36 times a fight is the lowest blade in the game
(Crossweave's 7.25 is the only neighbour, and it is a bow's).

**Type spread** (U, 660): scythe 61, warhammer 56, bow 54, flail 51,
**twinblade 27, greatsword 26**. Worst Starwarden 0, Dawnbringer 5,
Spellbreaker 5; best Gloamwire 90, Cindercleave 80, Bloodmirror 75. The
twinblades are the counter: many small blows, each reflected at half, and a
curse pool they refresh faster than the shroud fills it.

# 5. DECLARED

- **The spell** — `shot: { cadence 0.34, speed 380, r 22, life 4.0, grav 0,
  dmgMul 1.0, bounce 2 }`. `spawnShot` copies `bounce` onto the shot; the
  wall branch of `tickShots` already bounces a shot with `bounce > 0` (0.88 a
  wall, `s.a` rewritten, `snap` for the art). Clankable. `onHit {curse:1}`.
- **The ultimate** — `f.ultShroud = { t0, end, pool }`. `hurt()` is the hook:
  when the victim has `ultShroud` live and `src` is the foe, after the damage
  lands, `back = round(dmg · refl)` (`refl 0.5`) is dealt to the foe through
  `hurt(foe, back, self)`, then `foe.pushCurse(back, 1); foe.apply("curse", 1,
  self)`. Damage-over-time ticks count (a bleed on the shrouded caster is
  thrown back tick by tick — measured in, and the picture is a shroud that
  answers everything). A reflected blow does NOT reflect again (the foe has
  no shroud; if both are Nightglass, the reflection is not re-reflected —
  guard on `src.ultShroud`).
- Charge 16, window 8. Nothing waits.

# 6. NAMES, CARD, PICTURE, SOUND

**NIGHTGLASS** — a rod headed with black glass: it reflects. From:
Nightglass, Duskrod, Gloamcandle, Umbra.
**SHADEBOLT** (the spell). From: Shadebolt, Ricochet, Gloaming, Umbral Shot.
**BACKLASH** — what you give it, you get. From: Backlash, Recoil, Reflection,
Shroud.
**Card (67):** `Shrouded: half of every blow it takes is thrown back, and it curses`
**Shot tip (40):** `Bolts ricochet off two walls · clankable`

## 6.1 The picture

- **The staff**: a black rod with an obsidian head, a dim violet `core`
  inside the glass; the bolt leaves from the glass.
- **The spell**: a dark bolt with a short violet trail; on each wall it
  `snap`s and leaves a small dark splash (`spawnFx` 5 motes) — the viewer
  sees it turn.
- **Cast**: the glass goes black-bright; a shroud is drawn on the ball — a
  soft dark disc r 48 with a violet rim (alpha 0.5) that breathes.
- **A blow taken**: the shroud flashes at the point of contact and a dark
  shard (a bolt-shaped streak, 0.15s) leaps from the caster to the foe; the
  reflected damage floats in violet at the foe; the curse tag ticks.
- **Close**: the shroud lifts as smoke (0.4s).
- Silhouette: a staff whose head is a mirror the foe's colour never shows in.
  Field: dark motes drawn INTO the shroud, both copies.

## 6.2 The sound

- **Cast**: a reversed cymbal into a low glass tone, 0.4s.
- **A blow taken**: the game's own hit voice, then 60ms later a dark echo of
  it (the same voice, an octave down, filtered) — the reflection IS the
  echo, and it is the only voice the mechanic needs.
- **Close**: the glass tone fading up and out.

# 7. Open decisions

1. Rick's accept/reject. refl 1.0 (98% at 14) is the untaken monster; refl
   0.35 is unpriced and is the fallback if 0.5 reads as unfair.
2. The blade — 7.5–7.8, wide on 151.
3. Twinblades and greatswords at 26–27% — Rick's.
4. Whether ticks reflect (§5). Measured IN; taking them out is a one-line
   guard and a small re-price.

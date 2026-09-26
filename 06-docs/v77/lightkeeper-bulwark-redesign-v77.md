# v77 — LIGHTKEEPER / BULWARK, REDESIGNED. The ward becomes a wall of light in front of the sword: arrows die on it, foes bounce off it, and every block banks ward. The nova with extra knockback was +1.4 of feed.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0);
claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Labs:
`overlays/bulwark.js` (rejected), `overlays/wall.js` (taken); runs in
`06-docs/v77/runs/`.

## Why

Bulwark is `kind:"nova"` with `knock` — a v5 one-liner on a school whose
name is a wall. Feed +1.4 (v59 §2). The greatsword aims (`mode:"swing"`),
so it always has a FRONT — which is where a bulwark goes.

# 1. §1 (Cowork)

> For a duration a wall of light stands in front of the sword, as wide as
> the blade is long. Arrows die on it. An enemy that runs into it bounces
> off and cannot pass. Every arrow the wall stops and every time it turns
> the enemy back, the shield grows.

Two clauses: the wall (a barrier 220 wide, 50 ahead of the ball, turning
with the facing); the bank (**the feed** — ward from blocking, the thing
a wall is for).

# 2. THE HARNESS, AND THE CONTROL

Lightkeeper as shipped on `sc-trunk`, Chromium 141. **SHIP reads 48.5%
(330; the nova live), A 38.8%.**

# 3. A BLADE THAT BLOCKS WAS COLDIRON'S, AND WAS REJECTED

`bulwark.js` — the blade itself blocks (mass 12 for the window, so every
bind is won; arrows touching the blade die; blocks bank 10):

```
A 38.8%   SHIP 48.5%   B block only 50.9%   C + bank on blocks 71.5%   D + full-damage banking 81.5%
```

Winning binds is **Coldiron / Temper's** (v73) mechanic and a second relic
on it would blur both. Rejected on identity, not on price.

# 4. THE WALL (`runs/wall_base`, `wall_bank*`)

```
arm                                            win    blocks/cast  arrows/cast  banked/cast  shield on a window frame
A   no ultimate                               38.8%
SHIP the nova                                 48.5%
B   the wall, no bank                         38.8%     6.7          1.4           —           10.4
C   the wall, bank 10 a ball / 5 an arrow     79.1%     7.0          1.4          67.0         38.0
C   bank 4 / 4                                62.7%     6.9          1.4          31.3         21.0
C   bank 3 / 3   (taken)                      60.6%     6.8          1.4          23.9         18.3
```

**The foe runs into the wall seven times a window** — and being turned
back is worth nothing on its own (B = A). The bank is everything: +40 at 10
a block, +22 at 3. Taken at **3** so the blade stays a greatsword's: 60.6%
against a shipped 48.5, and the blade comes from 10.54 to about **9.5**
(the row: Axiom 7.42 – Heartwood 12.65) — the build settles it wide to the
shipped rate.

# 5. DECLARED, NAMES, CARD, PICTURE, SOUND, BRIEF

- **The wall** is a segment centred `50` ahead along `theta`, half-length
  110, perpendicular to the facing; it moves with the ball and turns with
  the aim every frame. **Arrows** within `r + 6` of it are removed (the
  strand endpoint rule for a net's arrows: a killed arrow is `stuck`, not
  spliced, so `tickNet` keeps its anchors). **A foe** within `R + 8` of it,
  not pinned, once per 0.4s, is knocked 500 along the wall's normal away
  from the caster's side; no damage, no beat, no hit stop.
- **The bank**: +3 ward per block (ball or arrow) — the vigil branch's three
  writes.
- Names kept: LIGHTKEEPER / BULWARK. **Card (71):** `A wall of light: arrows
  die on it, foes bounce off it, blocks bank ward`.
- **Picture**: a vertical bar of vigil pink light, 220 long, 6 wide with a
  soft 14-unit halo, standing 50 ahead of the ball and swinging with the
  aim; a block flashes the bar white for 2 frames (source-over) and a ward
  "+3" floats on the caster; an arrow dying on it leaves a short scorch
  on the bar for 0.3s. Cast: the bar rises out of the ball's shield ring
  over 0.25s; close: it folds back into the ring. Field: motes along the
  bar, both copies.
- **Sound**: cast — a shield-raise (a rising metallic slide, 0.4s); a ball
  block — a deep gong (share <120 Hz ≥ 0.4, ≤0.3s); an arrow — a short
  tink; close — the slide reversed.
- **Brief**: Stage 0 control on 151 (`--arms A,SHIP,C --P bankBall=3
  bankShot=3`). Stage 1 — nova out, `f.ultWall` in, the wall test, arrows,
  the shove; gate: ~6.8 blocks and ~1.4 arrows a cast, relic ~39% (arm B —
  the control that can fail: the wall alone must be worth nothing).
  Stage 2 — the bank; gate: ~24 ward a cast, relic ~61% at 10.54. Stage 3
  — the blade, wide on 151 at 9 / 9.5 / 10 to the shipped rate; tip_audit.
  Stage 4 — picture, voice, carry; nova's field spec out, the wall's in;
  `engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight
  watched.

# 6. Open decisions

1. Rick's veto. 2. The blade target (shipped 48.5 or 50). 3. Whether the
wall should stop the FOE'S BLADE too (it does not; a blade reaches through
it — the wall is for arrows and bodies) — a design line, Rick's if he wants
it otherwise.

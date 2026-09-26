# v70 — LODESTONE / REBUTTAL. THE RUNIC WARHAMMER, THE 37TH CELL. The walls are runed: whoever touches one is hexed and hurled back at the hammer — and the hurl is the picture, the hex is the fighter.

**DESIGNED — Cowork, 2026-09-26 (~13:00 UTC). Build from
`LODESTONE-BUILD-BRIEF.md`; do not design this cell elsewhere; claimed in
`06-docs/CLAIMS.md`.** Cowork's end to end (Rick: *"do it all"*); Rick vetoes
from this file. Lab: `tools/ult_overlay.py` + `overlays/rebound.js`; runs in
`06-docs/v70/runs/`.

## Why this cell

Third on the v68 table: body **22.7%** with the field's ultimates live (13.6
floor + 9.1 hex). Closes the warhammer row to 7 of 7 — the second type
finished after the greatsword — and puts runic on 5 of 6.

## What the cell is made of

**The warhammer**: reach 76, spin 1.6, mass 5.0, **knockMul 2.3** — it
throws what it hits into a wall, and then has to wait 3.9s for the head to
come round again while the foe comes back. That is the type's own
contradiction and every hammer ultimate so far answers it by HOLDING the foe
(Crucible pulls, Grasp grips, Garrote wires, Canopy roots itself). **Runic**
— hex `{5 stacks, 2.6s, a 0.2s weapon stun every 1.15s per stack}`: at five
stacks the foe's weapon stops every 0.23s. Corollary and Unmaking are bolts,
Converse leaves sigils and rewinds, the Stasis Field rings the caster. Runic
draws on stone (sigils) and answers (Converse, Corollary): this is the
school that argues.

---

# 1. §1 (Cowork, 12:05 UTC)

> For a duration the four walls of the hall are runed. Every time the enemy's
> ball touches a wall the rune under it flares, hexes them, and hurls them
> straight back at the hammer. The hammer's own knock throws them into the
> wall in the first place, so the fight becomes a rally: hit, wall, hurled
> back, hit. The walls do no damage — they hand the enemy back.

Three clauses: runed walls (a tell on all four); a touch hexes (**the feed**
— hex applied by the room, continuously, on the slowest weapon in the game
whose own blows can never keep hex up); a touch hurls the foe at the caster
(the hammer's knock answered by the hall).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141, `sc-trunk`, Grudgebearer's hammer as `runic ×
warhammer` (`onHit {hex:1}`, own ultimate off), 330 / 660 fights an arm.
**Arm A reproduces `cell_ults_on` to the fight: 22.73% = 75/330.** A wall
touch is the foe's centre within 1.5 units of the CURRENT inset plus R — the
hall closes and the runes close with it (v64 lesson 3).

# 3. THE HURL IS WORTH NOTHING AND THE HEX IS WORTH THIRTY

`runs/rebound_C_full.txt` (blade 23.5, 660 an arm):

```
arm                                    win    casts  hits in/out  flings/cast  hex/cast  foe stk
A  no ultimate                        21.4%            —  / 11.7
B  hurl only                          23.6%   3.14   6.2 / 6.4       8.2          —       1.08
H  hex on touch only, no hurl         53.2%   3.68   6.2 / 8.0       8.4         8.4      3.95
C  hurl + hex  (THE WHOLE)            57.3%   3.49   7.5 / 7.5       8.4         8.4      4.02
```

**The foe touches a wall 8.4 times in an 8-second window** — once a second —
and being thrown back at the hammer does not get it hit any more often (B:
6.2 blows in windows against 6.4 out; the head comes round when it comes
round). **The hex is the fighter**: 8.4 stacks a cast, the foe at **4.0
stacks on an average window frame** — its weapon stunned 0.2s every 0.29s,
about 70% of the time. v59 §2's column, again: an ultimate that puts the
school's status on continuously is worth thirty points on a channel that is
worth nine on its own.

The hurl adds **+4** on top of the hex and is kept as the picture: a rune
flaring and the foe hurled across the hall at 700 px/s is what the viewer
sees; the hex tag ticking to 5 is what they read. A bite on the hurl (4
damage) is worth another +12 (`runs/rebound_base`: 72.1%) and is **not
taken** — "-4" popping on every wall would be noise over the one number
that matters, and the whole would need a blade near 19. Hurl speed 500–900
is inside noise; 700 taken. Cadence 1.0s instead of 0.5 costs 7 and halves
the rally; 0.5 taken.

# 4. THE BLADE

```
blade    body (A)    whole (C)          n
 23.5     21.4%       57.3%           660
 22.0     17.1%       50.3%           660
 21.0     15.2%       49.7 / 48.5%    660 × 2
```

**Crossing near 21.5–22; ~2 points a damage point.** A hammer's blade
(Bulwarden's 20.1 is the row floor), body 15–17%.

**Type spread** (C, blade 22): greatsword 73, flail 59, scythe 45, bow 44,
twinblade 43, **warhammer 30**. Worst **Gloamwire 0%** (its net's strand
SHOVES — the foe never reaches a wall under its own steam, and a hurled foe
is the net's), Paradox 25, Shroudmaul 25 (holds beat hurls: a held foe is
not on a wall). Best Threshmaw 90, Axiom 85, Heartwood 85. 43pp; item
12/32.

# 5. DECLARED

- **Wall touch**: foe centre within `inset + R + 1.5` on any side, foe
  alive and not pinned, once per 0.5s. The engine clamps the ball at
  `n + R` so this is a contact test, not a proximity one.
- **The hurl**: `foe.vx, vy = 700 × unit(caster − foe)` — an ASSIGNMENT
  (the wall answers with its own throw), not an impulse; the caster's own
  knock is what put the foe there. No damage. **No `resolveHit`, no beat,
  no hit stop** (a rally would freeze the world eight times a window).
- **The hex**: `foe.apply("hex", 1, f)` per touch, the real status.
- The runes are on the CURRENT inset — they walk in with the seals.
- Charge 16, window 8. The next cast does not wait for anything.
- The caster's own wall touches do nothing (the runes know their master).

# 6. NAMES, CARD, PICTURE, SOUND

**LODESTONE** — the hammer the hall throws you back to. From: Lodestone,
Theorem, Postulate, Gambit. **REBUTTAL** — every time the foe reaches a wall,
the wall answers; the runic register of Corollary and Converse. From:
Rebuttal, Recoil, Repulse, Retort.
**Card (68):** `The walls are runed: a foe that touches one is hexed and hurled back`

## 6.1 The picture

- **Cast**: a rune chain lights along all four walls (runic `core` on the
  inset line, 0.3s draw from the caster's nearest wall outward) and stays
  lit for the window — the tell is the hall itself. The hammer head carries
  a rune glyph while the walls are lit.
- **A touch**: the rune segment under the foe FLARES (a 60-unit span, 0.15s,
  `glow`, source-over), a lightning bar snaps from wall to ball for one
  frame, and the foe leaves at 700 with a short rune-streak trail (drawn,
  not spawned). The hex tag on the foe prints its count.
- **Close**: the wall runes go dark from the far wall inward, 0.4s.
- **No new object in the hall** — everything is on the walls or the foe.
- Silhouette: a runic warhammer has no art — a rune-etched square head on a
  dark haft, first cut. Field spec: rune motes along the lit walls, both
  copies, sha re-stamped.

## 6.2 The sound

- **Cast**: a rising four-note rune chime, one per wall, 0.5s total.
- **A touch**: a sharp electric snap (≤80ms, peak ≤0.5) with the hex's own
  stun voice underneath if it lands; pitch steps up with the stack count.
- **Close**: the chime reversed, quiet.

# 7. Open decisions

1. Rick's veto. If the hurl reads as the foe being "controlled" rather than
   thrown, arm H (hex only, walls flare and stun) is one flag at 53%.
2. The blade — 21.5–22, wide on 151 after reproducing A (~21%) and C (~57%
   at 23.5).
3. Gloamwire 0% / warhammers 30% — item 12/32.
4. Whether a hurled foe should carry a brief `stunDR`-free hitstun on
   arrival — priced NO (it is a throw, not a hit); the build does not add
   one.

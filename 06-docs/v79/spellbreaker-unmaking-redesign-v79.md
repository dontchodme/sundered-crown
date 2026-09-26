# v79 — SPELLBREAKER / UNMAKING, REDESIGNED. Hexes stun the foe's weapon twice as long, and every hit hexes twice. The bolt was Corollary with a different number, on a school whose status IS the unmaking of a weapon.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0); claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Lab: `overlays/unmaking.js`; runs in `06-docs/v79/runs/`.

## Why
`kind:"bolt"`, 20 damage, 3 Hex — the same bolt as Axiom's Corollary (18, 3 Hex). Feed +7.7. Spellbreaker is the fastest hex applier in the game (a twinblade at 18 hits a fight) and hex is a WEAPON stun: a school status that literally unmakes the enemy's weapon for 0.2s at a time. The ultimate should make that true.

# 1. §1 (Cowork)
> For a duration Spellbreaker's hexes bite deeper: every stun a hex lands on the enemy's weapon lasts twice as long, and every hit Spellbreaker lands hexes twice.

Two clauses: `hex.stunFor` 0.2 → 0.4 for the window (on the foe — see §4); +1 hex per hit (**the feed**).

# 2. THE HARNESS, AND THE CONTROL
Spellbreaker as shipped on `sc-trunk`, Chromium 141. **SHIP 49.7% (330), A 20.9% — the bolt is +28.8, the strongest shipped ultimate in the redesign list.**

# 3. PRICED (`runs/unmaking_*`)
```
arm                                                   win     hits in/out   foe hex on a window frame
A   no ultimate                                      20.9%     —  / 26.0
SHIP the bolt                                        49.7%
B   the foe's weapon SHRINKS 12% a hit (min 40%)     27.0%    12.5 / 14.4    (foe reach 0.84)
C   shrink + double hex                              32.1%    13.1 / 15.4        2.93
C   shrink + double hex + stuns x3                   62.7%    15.7 / 16.9        3.28
D   double hex + stuns x3, no shrink                 61.5%    15.3 / 16.6        3.25
D   double hex + stuns x2  (taken)                   55.2%    14.8 / 16.3        3.22
```
**Shrinking the enemy's reach is worth +6 and stun length is worth +30** — a foe at 3.2 hex whose weapon stops 0.4s every 0.36s has no weapon. ×3 is 62.7 and the blade would leave the row; **×2 is 55.2 against a shipped 49.7** and the blade (8.81) comes to about **8.4**, the row floor.

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND
- `stunFor` is read in `tickStatus`'s hex branch from `STATUS.hex`; the build reads it through the FOE's `f.hexStunMul` (1 default; 2 while the caster's window is open — recomputed each frame, Bloodletting's rule) so a runic foe's hexes on Spellbreaker are untouched. The lab set the global; DECLARED, and the build's gate re-prices.
- +1 hex in `resolveHit` on a blow by a caster with `ultUnmake`.
- Names kept: SPELLBREAKER / UNMAKING. **Card (68):** `Hexes stun the foe's weapon twice as long, and every hit hexes twice`.
- **Picture**: the bolt art is retired. Cast: rune-script runs along both blades and stays (runic `core` glyphs, 0.3s). A hex stun on the foe already draws; make the DOUBLE-LENGTH stun visible — the foe's weapon greys out (desaturated, alpha 0.6) for the stun's length, so a longer stop is a longer grey. The hex tag counts by two. Field: rune motes off the blades, both copies.
- **Sound**: cast — a glass crack into a hum, 0.4s; a stun — hex's own snap, lengthened to match (0.4s tail); close — the hum cutting out.

# 5. BUILD BRIEF
Stage 0 control on 151 (`--arms A,SHIP,D --P stunMul=2`). Stage 1 — bolt out, `f.ultUnmake` in, `hexStunMul` on the foe; gate: measured stun length on the foe's weapon 0.40 ±0.01 inside windows and 0.20 outside (asserted), relic ~45% at 8.81 (arm D without the double hex — run `--P stunMul=2 hexExtra=0`). Stage 2 — the double hex; gate: hex applied = 2 × hits in windows, foe at ~3.2 on a window frame, relic ~55%. Stage 3 — the blade, wide on 151 at 8.3 / 8.5 / 8.8 to the shipped rate. Stage 4 — picture, voice, carry; bolt's field spec out; `engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched.

# 6. Open decisions
1. Rick's veto. 2. The blade target. 3. ×2 or ×3 — ×3 needs a blade under the row.

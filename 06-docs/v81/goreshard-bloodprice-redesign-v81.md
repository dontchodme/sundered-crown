# v81 — GORESHARD / BLOODPRICE, REDESIGNED. The foe pays in blood: the sword hits harder for every stack of Hemorrhage on the enemy. The beam with three Hemorrhage was Benediction's shape with a bleed on it.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0); claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Lab: `overlays/bloodprice.js`; runs in `06-docs/v81/runs/`.

## Why
`kind:"beam"`, 16 damage, 3 Hemorrhage. Feed +18.3 — the three stacks were doing the work, not the beam. Oathwound / Goreshard is the ONE id/name mismatch on the roster (learnings: read display names from the build). A blood price is paid by the one who bleeds.

# 1. §1 (Cowork)
> For a duration the enemy's blood is the sword's edge: every blow Goreshard lands hits harder for every stack of Hemorrhage the enemy is carrying — nearly a third more per stack.

One clause: `dmg × (1 + 0.30 × foe hemorrhage stacks)` on every blow in the window (cap 4 → up to +120%). The feed is the school's own status made into the sword's damage: a sword that wants the foe bleeding, on a school that applies 2 a hit.

# 2. THE HARNESS, AND THE CONTROL
Goreshard as shipped on `sc-trunk`, Chromium 141. **SHIP 37.6% (330), A 20.0%.**

# 3. PRICED (`runs/bloodprice_*`)
```
arm                                              win    blows/cast  foe bleed on a window frame
A   no ultimate                                 20.0%
SHIP the beam                                   37.6%
B   +12% a stack                                30.3%    2.4          2.29
C   +12% a stack + 1 extra bleed a hit          29.7%    2.5          2.24     (the extra bleed is +0: the cap is 4 and 2 a hit fills it)
B   +25% a stack                                35.5%    2.3          2.31
B   +30% a stack  (taken)                       42.4%    2.4          2.36
```
The foe carries 2.3 stacks on an average window frame, so a blow lands at ~+70%. **42.4 against a shipped 37.6 with the blade untouched at 9.17** — Goreshard sits low in the band today (v59: 44.7%) and this puts it nearer the middle; the build confirms wide and nudges the blade only if Rick wants the shipped rate exactly.

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND
- In `resolveHit`, for a blow by a caster with `ultPrice`: `dmg *= 1 + 0.30 × foe.stacks("hemorrhage")` read BEFORE this blow's own application (the blow pays on the stacks it found, then bleeds). One line. The lab wrote `w.dmg` each frame; the build scales in the hit.
- Names kept: GORESHARD / BLOODPRICE. **Card (69):** `Its blows hit harder the more the foe bleeds: +30% a Hemorrhage stack`.
- **Picture**: the beam art is retired. Cast: the blade darkens to arterial red for the window; the blade's glow SCALES with the foe's current stack count (0 → 4 maps alpha 0.2 → 0.8), so "harder the more you bleed" is on the sword itself; the damage float on a scaled blow is drawn larger. Field: blood motes off the blade, both copies.
- **Sound**: cast — a wet drawn-blade hiss, 0.4s; a scaled blow — the sword's strike voice pitched DOWN by the stack count (bigger = lower); close — nothing.

# 5. BUILD BRIEF
Stage 0 control on 151 (`--arms A,SHIP,B --P perStack=0.30`). Stage 1 — beam out, the multiplier in; gate: measured multiplier on every window blow = 1 + 0.3 × stacks-before-the-blow (asserted against a log), relic ~42% at 9.17. Stage 2 — the blade: confirm 9.17 wide on 151 or nudge to the shipped rate at Rick's word. Stage 3 — picture, voice, carry; beam's field spec out; `engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched.

# 6. Open decisions
1. Rick's veto. 2. 42 or the shipped 38 — the blade target. 3. Whether Bloodletting's cap (8) should apply here too — not priced; two payoffs on one ultimate.

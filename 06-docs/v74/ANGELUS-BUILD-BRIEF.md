# ANGELUS / ASCENSION — BUILD BRIEF (v74). The sanctified twinblade, the 41st relic.

**Cowork, 2026-09-26. DESIGNED. Build from this and
`sanctified-twinblade-design-v74.md`; do not design (rule 0). Rick's veto
before stage 1 — check CLAIMS.md.**

## 0. THE RELIC

> For a duration the relic rises and hangs in the air. Its two blades become
> two shafts of light reaching the floor, sweeping the hall as they turn;
> a shaft through the enemy is a light hit, and every hit heals the one
> above.

```
the cell     sanctified x twinblade     fighter ANGELUS      ultimate ASCENSION
the card     "Rises into the air; its blades become shafts of light. Each hit heals"   69
the blade    ~9.3 (stage 5)             Widowmaker's twinblade profile; onHit {smite:1}
the window   8s every 16s
the rise     to (W/2, 300) over 0.35s; pinned there (pinFree 1, re-armed); released to rest on close
the shafts   reachMul 10 on both blades, spin x 0.5, damage x 0.4 in resolveHit off f.ultRise; drawn to the wall/floor, not past
the heal     apply("blessing", 1, f) per shaft hit landed
```

Priced (design §3.1–4, y 300, 660 an arm): body 28.5% → **62.7%** at 11.95;
**53.9%** at 10. Shafts +15, heal +19. 5.2 shaft hits and 5.2 blessing a
cast. At the ceiling the same relic reads 85% by being unreachable —
design §3; do not "improve" the hang height upward.

## 1. IN THE ENGINE

- `f.ultRise = { t0, end, y }`. `tickRise`: the ease-up, the pin top-up,
  the reachMul, spin and damage scales, the heal on `hits` delta.
- `bladeSegments` unchanged (it reads `reachMul`); the renderer clips the
  drawn shaft at the inset.
- `_drawField`'s hexagon skipped for `pinFree`.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic widowmaker --cell
sanctified:twinblade --mech overlays/ascend.js --arms A,C --P hangY=300
--seeds 20` on 151: A ~28%, C ~63%.
**1 — stubbed relic** at 11.95, sanctified, smite 1; engine_ab on 40;
verify 25–35%; tip_audit.
**2 — the rise and the shafts** (arm B). Gate: the caster at y 300 ±1 on
≥99% of window frames after the rise, 0 knock taken, ~5 shaft hits a cast
at 0.4 (no shaft hit at full damage, asserted), relic ~44% at 11.95. FILM
IT. Run `harrow_bloom_probe` on the placeholder shafts now (design §6.1).
**3 — the heal** (arm C). Gate: blessing = shaft hits, ~36 hp a cast healed
measured in `tickStatus`, relic ~63%.
**5 — the blade.** Wide on 151 at 9 / 9.5 / 10. Expect 9–9.5. Ladder
printed (twinblades ~19%, hammers ~81% — the inverted counter; Rick's).
**6 — picture, voice, carry** per design §6; bloom gate ≤ +0.03 measured.
Beats: the rise files `ult`; shaft hits file as blows. Field in both
copies. Move `GAME`. `shell_identity`, `render_ab`, `chain_audit --builder
angelus_build.py`, one fight watched.

## 3. NOT TO RE-BUY

Ceiling / 200 / 300 → 71 / 64 / 43 shafts-only; the extra smite is +5 and
not taken.

## 4. OPEN

1. Rick's veto (hang height is the lever). 2. The blade. 3. Bloom. 4.
Twinblades at 19%. 5. Rise time.

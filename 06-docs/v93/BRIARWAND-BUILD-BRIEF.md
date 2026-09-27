# BRIARWAND / BLOOM — BUILD BRIEF (v93). The verdant staff, the 46th relic.

**Cowork, 2026-09-27. DESIGNED. Build from this and
`verdant-staff-design-v93.md`; do not design (rule 0). Rick's accept before
stage 1 — check CLAIMS.md. The type is `06-docs/v89/STAFF-ROW-v89.md` §1/§6.**

## 0. THE RELIC

> A staff that throws fans of three thorns. For 8s a cloud of pollen drifts
> after the foe; inside it the foe is entangled and bitten.

```
the cell     verdant x staff        fighter BRIARWAND     spell THORNBURST     ultimate BLOOM
the card     "A pollen cloud drifts after the foe: inside it, entangle and bites"   66
the body     the bow's physics, shape "staff"
the spell    shot { cadence 0.42, speed 440, r 16, life 1.2, grav 0, dmgMul 0.6, fan 3, spread 0.28 } · onHit { entangle: 2 }
the blade    ~16.5 (stage 5)
the window   8s every 16s
the cloud    r 110 from the caster's centre at cast, toward the foe at 90 px/s, clamped to the inset; foe inside: every 0.4s hurt 2.5 + entangle 1, no knock, no stop
```

Priced (design §3.1, 660 an arm): bow body 21.5% → spell **23.3%** → whole
**53.8%** at 17; 36.7% at 15. Bloom +31; the drift is the mechanic (a fixed
cloud is +0).

## 1. IN THE ENGINE

- `tickFire`: when `S.fan`, spawn `fan` shots at `theta + k·spread` (the
  volley loop is the template). `f.ultBloom = { t0, end, x, y, next, bites }`;
  `tickBloom` in the fighter tick. The renderer draws the cloud from state.
- Beats: cast files `ult`; every bite of a window files ONE `hit` beat per
  cast at the first bite (rule 3 — `hurt` is invisible to the director);
  thorns file as shots do.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic ironhail --cell verdant:staff --mech
overlays/staff_verdant.js --arms A,S,U --P blade=17 thornMul=0.6 life=1.2
tick=2.5 --seeds 20` on 151: A ~22%, S ~23%, U ~54%.
**1 — stubbed relic** at 17, verdant, entangle 2, the bow's shot,
`shape:"staff"`; engine_ab on the 34; verify; tip_audit.
**2 — the spell** (arm S). Gate: exactly 3 shots per cadence at θ−0.28, θ,
θ+0.28 (asserted), ~27 thorn blows a fight, relic ~23%. FILM a fan.
**3 — the cloud** (arm U). Gate: cloud speed 90 exactly, foe inside ~57% of
window frames, ~12 bites a cast, foe at ~3.7 entangle on a window frame,
relic ~54%. FILM the cloud drifting.
**5 — the blade.** Wide on 151 at 16.3 / 16.5 / 16.8. Ladder printed (bows
~27%).
**6 — picture, voice, carry** per design §6. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder briarwand_build.py`, one fight watched.

## 3. NOT TO RE-BUY

thorns 0.45 / life 0.8 → 3.9% at 15 (worse than the bow); bite 1.5 → +12;
a cloud that does not drift → +0 (28% inside against 57%).

## 4. OPEN

1. Rick's accept. 2. The blade. 3. Bows at 27. 4. The spread (taste).

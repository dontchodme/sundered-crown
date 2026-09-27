# NIGHTGLASS / BACKLASH — BUILD BRIEF (v91). The umbral staff, the 44th relic.

**Cowork, 2026-09-27. DESIGNED. Build from this and
`umbral-staff-design-v91.md`; do not design (rule 0). Rick's accept before
stage 1 — check CLAIMS.md. The type is `06-docs/v89/STAFF-ROW-v89.md` §1/§6.**

## 0. THE RELIC

> A staff that throws bolts of shadow that ricochet off the walls. For 8s it
> is shrouded: half of every blow it takes is thrown straight back, cursing.

```
the cell     umbral x staff        fighter NIGHTGLASS     spell SHADEBOLT     ultimate BACKLASH
the card     "Shrouded: half of every blow it takes is thrown back, and it curses"   67
the body     the bow's physics, shape "staff"
the spell    shot { cadence 0.34, speed 380, r 22, life 4.0, grav 0, dmgMul 1.0, bounce 2 } · onHit { curse: 1 }
the blade    ~7.6 (stage 5)
the window   8s every 16s
the shroud   in hurt(): victim has ultShroud and src is the foe -> back = round(dmg x 0.5) dealt to the foe (src = the caster), pushCurse(back, 1), apply curse 1
             ticks count; a reflected blow is never re-reflected (guard on src.ultShroud)
```

Priced (design §3.1, 660 an arm): bow body 0.3% → spell **18.0%** → whole
**45.5%** at 7.3; 58.5% at 8. Backlash +28 at the blade; refl 1.0 reads 98% at
14 and is not taken.

## 1. IN THE ENGINE

- `spawnShot`: copy `S.bounce` onto the shot (the wall branch already
  bounces it). `f.ultShroud = { t0, end, taken, back }`. The hook is in
  `hurt()` — the one function every source of damage goes through — after
  the pool and the hp are debited. `pushCurse` + `apply` exactly as
  `resolveHit` does for an onHit curse.
- Beats: cast files `ult`; every reflected blow of ≥ 4 files a `hit` beat at
  the foe with `ranged:false` (rule 3 — the director cannot see `hurt`).

## 2. STAGES

**0 — control.** `ult_overlay.py --relic ironhail --cell umbral:staff --mech
overlays/staff_umbral.js --arms A,S,U --P blade=7.3 --seeds 20` on 151:
A ~0%, S ~18%, U ~46%.
**1 — stubbed relic** at 7.3, umbral, curse 1, the bow's shot, `shape:"staff"`;
engine_ab on the 34; verify; tip_audit.
**2 — the spell** (arm S). Gate: ~43 bounces a cast-equivalent (≈ 130 a
fight), ~37 blows a fight (14.6/22.2 in/out), relic ~18%. FILM a bolt
turning twice.
**3 — the shroud** (arm U). Gate: back = round(0.5 × taken) on every blow
taken inside a window (asserted per blow), foe at 3.0 curse on a window
frame, relic ~46%; no reflection outside a window; no double reflection in
the mirror match.
**5 — the blade.** Wide on 151 at 7.4 / 7.6 / 7.8. Ladder printed
(twinblades ~27%).
**6 — picture, voice, carry** per design §6. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder nightglass_build.py`, one fight watched.

## 3. NOT TO RE-BUY

refl 1.0 → 98% at 14; Backlash on the plain arrow +24 at 14; the ricochet
alone at 14 → 88%.

## 4. OPEN

1. Rick's accept. 2. The blade. 3. refl 0.35 as the fallback. 4. Ticks.

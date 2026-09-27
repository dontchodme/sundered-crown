# CROZIER / RADIANCE — BUILD BRIEF (v95). The sanctified staff, the 48th relic.

**Cowork, 2026-09-27. DESIGNED. Build from this and
`sanctified-staff-design-v95.md`; do not design (rule 0). Rick's accept
before stage 1 — check CLAIMS.md. The type is
`06-docs/v89/STAFF-ROW-v89.md` §1/§6.**

## 0. THE RELIC

> A staff that throws needles of light no blade can parry. For 8s every
> needle grows as it flies into a shaft that hits three times as hard.

```
the cell     sanctified x staff        fighter CROZIER     spell LANCE     ultimate RADIANCE
the card     "Every lance grows as it flies: the farther, the bigger and harder"   65
the body     the bow's physics, shape "staff"
the spell    shot { cadence 0.34, speed 560, r 16, life 2.5, grav 0, dmgMul 1.0, pierce: true } · onHit { smite: 1 }
             pierce: tickShots skips the blade-segment loop for the shot; the ball test is unchanged
the blade    ~14.3 (stage 5)
the window   8s every 16s
the growth   a shot spawned in-window carries grow.born; each step k = min(1, (t - born) / 0.4); r = 16 + 54 k; dmgMul = 1 + 2 k
```

Priced (design §3.1, 660 an arm): bow body 28.2% → spell **18.2%** (a fast
shot lands less) → whole **52.1%** at 14.5; 69.4% at 17. Radiance +34.
**Sanctum (a smiting, healing ring on the caster) priced +42 and is
REJECTED as Benediction's — do not build it here.**

## 1. IN THE ENGINE

- `spawnShot`: copy `pierce`; in-window, `grow`. `tickShots`: the guard on
  the segment loop; the growth before the move. `f.ultRadiance = { t0, end }`.
- Beats: cast files `ult`; lances file as shots do. A grown landing of
  `dmg ≥ 20` is worth a `crit:true` on its beat so the director films it.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic ironhail --cell sanctified:staff
--mech overlays/staff_sanct.js --arms A,S,Z --P blade=14.5 gT=0.4 gR1=70
gMul=3 --seeds 20` on 151: A ~28%, S ~18%, Z ~52%. Read `lanceHits`, not
`hits in/out` (v89 §4).
**1 — stubbed relic** at 14.5, sanctified, smite 1, the bow's shot,
`shape:"staff"`; engine_ab on the 34; verify; tip_audit.
**2 — the spell** (arm S). Gate: zero lances clanked over a probe of 100
fights (asserted — the segment loop never runs on a pierce), ~7.6 lance
blows a fight, relic ~18%. FILM a lance passing a greatsword.
**3 — the growth** (arm Z). Gate: r and dmgMul exactly on the ramp at every
step (asserted), ~12 grown a cast, ~3.2 lance blows a cast, relic ~52%.
FILM a needle becoming a shaft; **§4.1b/c bloom gates as numbers** (design
§6.1).
**5 — the blade.** Wide on 151 at 14 / 14.3 / 14.6. Ladder printed
(twinblades ~70%).
**6 — picture, voice, carry** per design §6. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder crozier_build.py`, one fight watched.

## 3. NOT TO RE-BUY

Sanctum +56 / +42 (rejected); growth over 1.0s / ×2.5 → +10; the lance at
380 lands 3.0 a cast against 2.4 (a slower lance is a better weapon).

## 4. OPEN

1. Rick's accept. 2. The blade. 3. The growth's two knobs. 4. The speed.

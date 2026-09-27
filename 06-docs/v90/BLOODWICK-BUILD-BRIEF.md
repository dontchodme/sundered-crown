# BLOODWICK / GYRE — BUILD BRIEF (v90). The bloodsworn staff, the 43rd relic.

**Cowork, 2026-09-27. DESIGNED. Build from this and
`bloodsworn-staff-design-v90.md`; do not design (rule 0). Rick's accept before
stage 1 — check CLAIMS.md. The type is `06-docs/v89/STAFF-ROW-v89.md` §1/§6.**

## 0. THE RELIC

> A staff that throws globules of blood that bend toward the foe. For 8s the
> globules orbit it instead, and lunge as one when the foe comes close.

```
the cell     bloodsworn x staff     fighter BLOODWICK     spell BLOODSEEKER     ultimate GYRE
the card     "Its blood orbits it, then lunges as one when the foe comes close"   64
the body     the bow's physics (reach 54, width 9, spin 2.8, mass 1.6, mode ranged), shape "staff"
the spell    shot { cadence 0.34, speed 300, r 22, life 3.0, grav 0, dmgMul 1.0, home 1.0 } · onHit { hemorrhage: 2 }
the blade    ~8.5 (stage 5)
the window   8s every 16s
the orbit    up to 6 shots held at r 95, 4.0 rad/s, life refreshed, home 0, clankable
the lunge    all orbiters loosed at the foe when it is within 230: speed 520, home 8, life 2.0
the close    orbiters loosed toward the foe at the spell's speed and home
```

Priced (design §3.1, 660 an arm): bow body 5.0% → spell **15.9%** → whole
**50.5%** at 8.5. The lunge is the payload (+31); the orbit alone is +2–4.
**A seeker at home 2.2 reads 96% with no ultimate — do not "fix" the bend.**

## 1. IN THE ENGINE

- `shape:"staff"` (art, stage 6). `spawnShot`: copy `S.home` onto the shot
  when the profile has it (the field `tickShots` already turns on).
- `f.ultGyre = { t0, end, orb: [], phase }`. In `tickShots`, before the
  move: an orbiter is placed (position + tangential velocity) rather than
  advanced; on spawn inside the window with `orb.length < 6`, the shot joins.
  The lunge test once a step; the close in the window's own close.
- Beats: cast files `ult`; the lunge files one `ult` beat at the caster
  (rule 3); shots file as ever.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic ironhail --cell bloodsworn:staff
--mech overlays/staff_blood.js --arms A,S,U --P blade=8.5 home=1.0 --seeds 20`
on 151: A ~5%, S ~16%, U ~50%.
**1 — stubbed relic** at 8.5, bloodsworn, hemorrhage 2, the bow's shot,
`shape:"staff"` on the bow's art; engine_ab on the 34; verify in band;
tip_audit.
**2 — the spell** (arm S). Gate: ~22 blows a fight (8.6/13.6 in/out on the
harness clock), every shot's `home` 1.0 and turning ≤ home·dt a step
(asserted), relic ~16%. FILM a globule curving.
**3 — the orbit** (arm V). Gate: ≤ 6 orbiters, each within 1px of the lane
on every window frame after joining, orbit-only relic ~+3.
**4 — the lunge** (arm U). Gate: ~7 lunged a cast, ~5.3 blows a window, foe
at ~3.2 hemorrhage on a window frame, relic ~50%.
**5 — the blade.** Wide on 151 at 8.3 / 8.5 / 8.7 — the curve is 20 points
between 8 and 9. Ladder printed (greatswords ~29%).
**6 — picture, voice, carry** per design §6. Field in both copies. Move
`GAME`. `shell_identity`, `render_ab`, `chain_audit --builder
bloodwick_build.py`, one fight watched.

## 3. NOT TO RE-BUY

home 2.2 → 96% at 14, 40% at 7; orbit without lunge +2–4; Gyre on the plain
arrow +50 at 14 (the ultimate does not need the spell, the spell needs the
blade).

## 4. OPEN

1. Rick's accept. 2. The blade. 3. home 0.7 as the fallback if the bend reads
as tracking. 4. Greatswords.

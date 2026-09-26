# PORTCULLIS / ONSLAUGHT — BUILD BRIEF (v72). The vigil flail, the 39th relic.

**Cowork, 2026-09-26. DESIGNED. Build from this and
`vigil-flail-design-v72.md`; do not design (rule 0). Rick's veto before
stage 1 — check CLAIMS.md.**

## 0. THE RELIC

> For a duration the ward hardens the shell and the ball is the weapon: it
> charges the enemy, every slam hits for a quarter of the shield it carries
> and knocks them back, and every slam banks more shield. The head keeps
> swinging.

```
the cell      vigil x flail          fighter PORTCULLIS      ultimate ONSLAUGHT
the card      "The shell charges the foe. Each slam hits for the shield and banks more"   71
the blade     ~23 (stage 5)          Gravemourn's flail profile; onSelf {ward:1}
the window    8s every 16s
the charge    vx,vy += unit(foe) x 600 x dt each window frame (not while pinned), clamped at speedMax
a slam        d < 2R + 3, once per 0.5s: hurt 0.25 x shield (ward first), knock 500 away, bank +8 ward (the vigil branch's three writes)
```

Priced (design §4.1): body 28.0% → **54.4%** at 24.03; 47.6% at 22; 37.7% at
20. Bank +20, slam +3, charge +3. 3.7 slams a cast, 29 ward banked a cast.

## 1. IN THE ENGINE

- `f.ultRam = { t0, end, cd }`. `tickRam`: the accel, the contact test, the
  slam's three parts. `ballCollision` runs as ever.
- A slam files a `hit` beat (design open decision 3).
- Nothing writes `stun` or `pin`.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic gravemourn --cell vigil:flail
--mech overlays/ram.js --arms A,D --P ramDmg=0 --seeds 20` on 151: A ~28%,
D ~54%.
**1 — stubbed relic** at 24.03, vigil, ward 1; gate: engine_ab on 38,
verify 20–35%, tip_audit.
**2 — charge + slam, no bank** (arm C). Gate: ~3.6 slams a cast, ~11 damage
a cast, relic ~34%. FILM the charge and a slam.
**3 — the bank** (arm D). Gate: ~29 ward banked a cast, shield ~18 on a
window frame, relic ~54%. Slams = banks, asserted.
**5 — the blade.** Wide on 151 at 22 / 23 / 24. Expect 22.5–23.5.
**6 — picture, voice, carry** per design §7; the plated shell's fill tracks
the shield (asserted against `shield / cap`). Field in both copies. Move
`GAME`. `shell_identity`, `render_ab`, `chain_audit --builder
portcullis_build.py`, one fight watched.

## 3. NOT TO RE-BUY

The head-as-shield (+10) and the swell-and-burst (+5, burst negative) —
design §3. A flat 10 on the slam is +13 and not taken.

## 4. OPEN

1. Rick's veto. 2. The blade. 3. The slam beat. 4. Bows at 35% — Rick's.

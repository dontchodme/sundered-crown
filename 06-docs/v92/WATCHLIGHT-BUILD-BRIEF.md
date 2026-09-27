# WATCHLIGHT / BEACON — BUILD BRIEF (v92). The vigil staff, the 45th relic.

**Cowork, 2026-09-27. DESIGNED. Build from this and
`vigil-staff-design-v92.md`; do not design (rule 0). Rick's accept before
stage 1 — check CLAIMS.md. The type is `06-docs/v89/STAFF-ROW-v89.md` §1/§6.**

## 0. THE RELIC

> A staff that throws heavy bolts of light that shove. For 8s it sets down a
> lantern that fires at the foe on its own; every hit banks ward.

```
the cell     vigil x staff        fighter WATCHLIGHT     spell WARDBOLT     ultimate BEACON
the card     "Sets down a lantern that fires at the foe. Every hit banks ward"   63
the body     the bow's physics, shape "staff" · onSelf { ward: 2.5 } (Farwarden's)
the spell    shot { cadence 0.34, speed 400, r 26, life 3.4, grav 0, dmgMul 1.0, knock 420 }
the blade    ~9.3 (stage 5)
the window   8s every 16s
the lantern  placed at the caster at cast (clamped to the inset); every 1.2s a shot from it at atan2(foe - lantern), NO lead:
             speed 420, r 22, life 3.0, grav 0, dmgMul 0.6, knock 150, own = caster, lamp: true; clankable; banks ward through resolveHit
```

Priced (design §3.1, 660 an arm): bow body 5.6% (22.9% at ward 2.5) → spell
**20.5%** → whole **49.7%** at 9.3; 58.2% at 10. Beacon +29; the bank +17; the
shove free. **A lantern at 0.5s reads 97% — do not "fix" the cadence
downward.**

## 1. IN THE ENGINE

- `spawnShot`: copy `S.knock`. `f.ultBeacon = { t0, end, x, y, next, fired,
  refused }`; a `tickBeacon` in the fighter tick pushes the lantern's shot
  (the fork block in `tickShots` is the template for a shot pushed by hand).
  The renderer draws the lantern from `ultBeacon` (a pure function of state).
- Beats: cast files `ult`; lantern shots file as shots do (they have `x0,
  y0, t0`), so the director sees them.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic ironhail --cell vigil:staff --mech
overlays/staff_vigil.js --arms A,B,S,U --P blade=9.3 every=1.2 bMul=0.6
knock=420 --seeds 20` on 151: A ~6%, B ~23%, S ~21%, U ~50%.
**1 — stubbed relic** at 9.3, vigil, ward 2.5, the bow's shot, `shape:"staff"`;
engine_ab on the 34; verify; tip_audit.
**2 — the spell** (arm S). Gate: every landing adds 420 along the shot's
velocity to the foe (asserted), ~25 blows a fight, relic ~21%. FILM a shove.
**3 — the lantern** (arm U). Gate: 6–7 lantern shots a window, ~4.5 blows a
window, shield ~31 on a window frame, relic ~50%; the lantern never fires
outside a window or after a death.
**5 — the blade.** Wide on 151 at 9.1 / 9.3 / 9.6. Ladder printed
(twinblades ~35%).
**6 — picture, voice, carry** per design §6. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder watchlight_build.py`, one fight watched.

## 3. NOT TO RE-BUY

every 0.5s → 97 (direct) / 92 (lead) at 13, on the plain arrow too; knock
220 vs 420 is +3 at 330 and 0 at 660.

## 4. OPEN

1. Rick's accept. 2. The blade. 3. every 1.5s as the fallback. 4. knock 600 if
the spell should pay.

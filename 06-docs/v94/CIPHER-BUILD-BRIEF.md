# CIPHER / CONVERGENCE — BUILD BRIEF (v94). The runic staff, the 47th relic.

**Cowork, 2026-09-27. DESIGNED. Build from this and
`runic-staff-design-v94.md`; do not design (rule 0). Rick's accept before
stage 1 — check CLAIMS.md. The type is `06-docs/v89/STAFF-ROW-v89.md` §1/§6.**

## 0. THE RELIC

> A staff that throws rune bolts; a bolt that reaches a wall hangs there as
> a sigil that hexes whoever touches it. For 8s every rune leaves its wall
> and hunts the foe.

```
the cell     runic x staff        fighter CIPHER     spell GLYPH     ultimate CONVERGENCE
the card     "Every rune on the walls leaves it and hunts the foe, hexing"   59
the body     the bow's physics, shape "staff"
the spell    shot { cadence 0.34, speed 380, r 22, life 3.4, grav 0, dmgMul 1.0, sigil: { life 4.0, hex 2 } } · onHit { hex: 1 }
             spawn with bounce 1; on the spent bounce: vx = vy = 0, life 4.0, r 22 UNCHANGED, sigil, over.onHit { hex: 2 }
the blade    ~11 (stage 5)
the window   8s every 16s
the recall   at cast, hanging sigils get fuse = t + 0.25 k in laid order; in-window, a new sigil gets fuse = t + 0.5;
             at fuse: home 3, 380 toward the foe, life 3.0, sigil false, flown true (never re-read as a sigil)
```

Priced (design §3.1, 660 an arm): bow body 9.5% → spell **31.2%** → whole
**50.5%** at 11; 39.7% at 10. Convergence +19; the wall-stop +22.
**Detonating the sigils instead is +0 — not taken.**

## 1. IN THE ENGINE

- `spawnShot`: `bounce 1` when `S.sigil`. The wall branch of `tickShots`:
  on the spent bounce, the sigil conversion (five assignments). A sigil is
  otherwise a shot. `f.ultConverge = { t0, end }`; a `tickConverge` sets
  fuses and launches.
- Beats: cast files `ult`; runes file as shots do once flown; the wall-stop
  files nothing.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic ironhail --cell runic:staff --mech
overlays/staff_runic.js --arms A,S,Y --P blade=11 --seeds 20` on 151: A ~10%,
S ~31%, Y ~50%.
**1 — stubbed relic** at 11, runic, hex 1, the bow's shot, `shape:"staff"`;
engine_ab on the 34; verify; tip_audit.
**2 — the spell** (arm S). Gate: every bolt that reaches a wall becomes a
sigil with vx = vy = 0 and life 4.0 (asserted), ~25 sigils a
cast-equivalent, ~1.75 hanging when a window opens, relic ~31%. FILM a wall
of runes.
**3 — the recall** (arm Y). Gate: every hanging sigil launches in laid order
0.25s apart, every in-window sigil launches 0.5s after it is laid, ~5.4
launched a cast, ~5.7 blows a window, foe at ~2.6 hex on a window frame,
relic ~50%; no sigil ever re-forms from a flown rune (asserted).
**5 — the blade.** Wide on 151 at 10.8 / 11 / 11.2. Ladder printed.
**6 — picture, voice, carry** per design §6. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder cipher_build.py`, one fight watched.

## 3. NOT TO RE-BUY

Sequence (detonate, r 150) +0, r 220 +6; a sigil with r 26 sits in the wall
and dies at once (measured — keep r 22).

## 4. OPEN

1. Rick's accept. 2. The blade. 3. home 6 (unpriced). 4. sigil life.

# CULVERIN / IRONFALL — BUILD BRIEF (v96). The dwarven staff, the 49th relic.

**Cowork, 2026-09-27. DESIGNED. Build from this and
`dwarven-staff-design-v96.md`; do not design (rule 0). Rick's accept before
stage 1 — check CLAIMS.md. The type is `06-docs/v89/STAFF-ROW-v89.md` §1/§6.**

## 0. THE RELIC

> A staff that lobs iron slugs that fall. For 8s it also lobs shells high
> onto where the foe will be; they burst and sunder.

```
the cell     dwarven x staff        fighter CULVERIN     spell SLUG     ultimate IRONFALL
the card     "Lobs shells that fall on where the foe will be, bursting and sundering"   70
the body     the bow's physics, shape "staff"
the spell    shot { cadence 0.55, speed 470, r 28, life 3.0, grav 700, dmgMul 1.6 } · onHit { sunder: 1 }   -- no new field
the blade    ~13.2 (stage 5)
the window   8s every 16s
the shell    every 1.0s: T 0.85, g 1000, target = foe + v_foe T, v = (target - caster)/T - (0, gT/2);
             a shot from the caster's centre: r 26, life T, grav g, dmgMul 1.3, shard, pop 8, popR 90, shell: true; clankable; walls kill it
```

Priced (design §3.1, 660 an arm): bow body 22.3% → spell **24.1%** → whole
**47.9%** at 13; 38.5% at 12. Ironfall +24; the burst +0 (kept for the
picture). **Direct aim reads 89% — do not "fix" the lead. Every 0.7s reads
72% at 14 — do not "fix" the rate.**

## 1. IN THE ENGINE

- Nothing new for the spell. `f.ultIronfall = { t0, end, next, fired }`; a
  `tickIronfall` pushes the shell (the fork block is the template; the
  shard pop already exists). The renderer draws the landing ring from the
  shell's `t0 + T` and its own velocity (a pure function).
- Beats: cast files `ult`; shells file as shots do; a burst that lands
  files a `hit` beat through `resolveHit` as ever.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic ironhail --cell dwarven:staff --mech
overlays/staff_dwarf.js --arms A,S,U --P blade=13 every=1.0 sMul=1.3
popR=90 --seeds 20` on 151: A ~22%, S ~24%, U ~48%.
**1 — stubbed relic** at 13, dwarven, sunder 1, the bow's shot,
`shape:"staff"`; engine_ab on the 34; verify; tip_audit.
**2 — the spell** (arm S). Gate: cadence 0.55 exactly, every slug's `vy`
grows by 700·dt a step (asserted), ~14 blows a fight at 1.6×, relic ~24%.
FILM a slug arcing and dropping.
**3 — the shells** (arm U). Gate: ~7.3 shells a cast, every shell's life
0.85 and its velocity the solved one (asserted), ~2.8 blows a window, foe at
~3.1 sunder on a window frame, relic ~48%. FILM the landing ring and the
burst.
**5 — the blade.** Wide on 151 at 13 / 13.2 / 13.5. Ladder printed.
**6 — picture, voice, carry** per design §6. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder culverin_build.py`, one fight watched.

## 3. NOT TO RE-BUY

Direct aim 89%; every 0.7s at 1.6 → 72% at 14; no burst −1.5 (popR 60) / +0
(popR 90).

## 4. OPEN

1. Rick's accept. 2. The blade. 3. popR 120 (unpriced). 4. Greatswords.

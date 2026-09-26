# COLDIRON / TEMPER — BUILD BRIEF (v73). The dwarven twinblade, the 40th relic.

**Cowork, 2026-09-26. DESIGNED. Build from this and
`dwarven-twinblade-design-v73.md`; do not design (rule 0). Rick's veto before
stage 1 — check CLAIMS.md.**

## 0. THE RELIC

> For a duration the twin blades are cold iron, as heavy as a warhammer:
> every bind the twinblade takes it wins, each win sunders the enemy, and
> sunder stacks past its limit while the iron holds.

```
the cell      dwarven x twinblade      fighter COLDIRON      ultimate TEMPER
the card      "Blades of cold iron: it wins binds, and each win sunders past the cap"   69
the blade     ~9.3 (stage 5)           Widowmaker's twinblade profile; onHit {sunder:1}
the window    8s every 16s
the mass      massMul 5.0/1.1 for the window at every w.mass read (declared list)
a won bind    apply("sunder", 2, f) in resolveClank when decisive and the winner has ultIron
the cap       the foe's sunderCap = 9 while the caster's window is open (per-fighter, recomputed each frame), 6 otherwise
```

Priced (design §3–4, 660 an arm): body 35.2% → **73.9%** at 11.95 with cap
12; **50.2 / 48.8%** at blade 9 with cap 9. Mass +21, sunder on bind +5,
cap +7 (at 9). 3.1 binds a window, 2.7 won.

## 1. IN THE ENGINE

- `f.ultIron = { t0, end }`; `f.massMul` (1 default) at every `w.mass` read
  — `resolveClank`, `move`, `decayImpactOnly`'s gravity, `ballCollision`,
  the burden term, `massRef` derivations if any; builder-asserted.
- `resolveClank`: after `aWins` — `if (decisive && winner.ultIron)
  loser.apply("sunder", 2, winner)`.
- `apply`: `const cap = key === "sunder" ? this.sunderCap : ...` beside
  the hemorrhage line; `sunderCap` recomputed in `tickIron` for both
  fighters each frame.
- Stacks above 6 when the window drops run out on the 5s clock (not
  trimmed — Bloodletting's rule).

## 2. STAGES

**0 — control.** `ult_overlay.py --relic widowmaker --cell
dwarven:twinblade --mech overlays/anvil.js --arms A,D --P blade=9 winCap=9
--seeds 20` on 151: A ~17%, D ~50%.
**1 — stubbed relic** at 11.95, dwarven, sunder 1; engine_ab on 39; verify
30–40%; tip_audit.
**2 — the mass** (arm B). Gate: 2.7 of 3.1 binds won a window (0 of 2.9
without — the control that can fail), relic ~56% at 11.95; the gravity
consequence measured (fall rate ×1.37 in-window). FILM a bind won.
**3 — sunder on the win** (arm C). Gate: ~5.4 stacks a cast from binds,
relic ~62%.
**4 — the cap** (arm D, cap 9). Gate: stack peak ~8.0, no stack above 9
ever (asserted), no fighter above 6 while no window is open except by the
clock, relic ~74% at 11.95 / ~50% at 9.
**5 — the blade.** Wide on 151 at 8.8 / 9.3 / 9.8. Expect 9–9.5. Ladder
printed (hammers ~37% — deadlocks; Rick's).
**6 — picture, voice, carry** per design §6. Beats: cast files `ult`; a won
bind files the clank's own beat. Field in both copies. Move `GAME`.
`shell_identity`, `render_ab`, `chain_audit --builder coldiron_build.py`,
one fight watched.

## 3. NOT TO RE-BUY

Sunder-on-bind without the mass is +0 (arm S). Cap 12 is +12 and needs a
blade under the row. Mass is the fighter.

## 4. OPEN

1. Rick's veto (cap 6 fallback). 2. The blade. 3. The `massMul` site list.
4. Hammers — Rick's.

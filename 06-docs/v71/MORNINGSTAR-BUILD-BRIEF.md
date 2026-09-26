# MORNINGSTAR / ZENITH — BUILD BRIEF (v71). The sanctified flail, the 38th relic.

**Cowork, 2026-09-26. DESIGNED. Build from this and
`sanctified-flail-design-v71.md`; do not design (rule 0). Rick's veto before
stage 1 — check CLAIMS.md.**

## 0. THE RELIC

> For a duration the flail's head becomes a sun. An enemy in its light is
> smitten and burned for as long as it stays there, and every burn heals the
> one swinging it. The head still hits like a flail head.

```
the cell      sanctified x flail      fighter MORNINGSTAR     ultimate ZENITH
the card      "The head becomes a sun: its light smites foes, and each burn heals it"   69
the blade     24.03 — UNCHANGED (stage 5 confirms)    Gravemourn's flail profile; onHit {smite:1}
the window    8s every 16s
the light     disc radius 100 on the HEAD; foe lit when centre within 100 + R
a tick        every 0.4s while lit: hurt 3 (ward first, nothing else), smite +1, then blessing +1 on the caster
```

Priced (design §3.1): body 7.6% → **50.2 / 50.6%** on two blocks of 660 at
blade 24.03. Smite +11, burn +8, heal +24. 6 ticks a cast.

## 1. IN THE ENGINE

- `f.ultSun = { t0, end, cd }`. `tickSun`: the lit test on `headX/Y`, the
  cooldown, the three writes. Blessing heals through the existing
  `tickStatus` branch.
- Nothing else changes: no `resolveHit`, no stun, no pin, no knock.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic gravemourn --cell sanctified:flail
--mech overlays/sun.js --arms A,D --P sunR=100 blessOnTick=1 --seeds 20` on
151: A ~7.6%, D ~50%.
**1 — stubbed relic** at 24.03, sanctified, smite 1; gate: engine_ab on 37,
verify 5–10%, tip_audit.
**2 — the light and the smite** (arm B). Gate: foe lit ~20% of window
frames, ~6 ticks a cast, relic ~18%. FILM IT — and run `ult_fx_capture` +
`harrow_bloom_probe` on the placeholder art before anything is tuned
(design §6.1: this school blew the bloom out twice).
**3 — the burn** (arm C). Gate: ~18 damage a cast, relic ~26%.
**4 — the heal** (arm D). Gate: ~6 blessing stacks a cast, ~36 hp healed a
cast measured off `hp` deltas in `tickStatus`, relic ~50%. Blessing =
ticks, asserted.
**5 — the blade.** Confirm 24.03 wide on 151 (both sides, two blocks); move
only if the band misses. Ladder printed (Farwarden ~0 — item 12/32).
**6 — picture, voice, carry** per design §6. **Bloom gate**: arena-mean
lift ≤ +0.02, caster's disc ≤ 0.90 — measured, not asserted. Beats: cast
files `ult`; ticks file nothing; fatal tick files as smite's does. Reuse
the `spark collect` heal voice. Field in both copies. Move `GAME`.
`shell_identity`, `render_ab`, `chain_audit --builder morningstar_build.py`,
one fight watched.

## 3. NOT TO RE-BUY

Radius 70/100/130 → 50/56/63 (clock heal); the trail variant 59–65; heal on
a clock is +4 over heal-on-tick and not taken; the blade is the type's own.

## 4. OPEN

1. Rick's veto (the trail is one flag). 2. Bloom numbers — measured at the
build. 3. Farwarden 0% — Rick's.

# ORACLE / FORESIGHT — BUILD BRIEF (v75). The runic bow, the 42nd relic — the last cell.

**Cowork, 2026-09-26. DESIGNED. Build from this and
`runic-bow-design-v75.md`; do not design (rule 0). Rick's veto before stage
1 — check CLAIMS.md.**

## 0. THE RELIC

> For a duration the bow foresees: a rune marks where the enemy will be
> when the next arrow lands, every arrow of the stream flies to it, and an
> arrow that lands hexes twice.

```
the cell     runic x bow            fighter ORACLE       ultimate FORESIGHT
the card     "Every arrow flies to where the foe will be, and each hit hexes twice"   68
the blade    ~12 (stage 5)          Ironhail's bow profile; onHit {hex:1}
the window   8s every 16s
the aim      theta turned at 6 rad/s toward lead = foe + v_foe x (d / shot.speed); spin does not advance theta in-window
the hex      +1 hex in resolveHit on a shot landed by a caster with ultSight (2 with the channel)
```

Priced (design §3.1–4, 660 an arm): body 31.1% → **73.2%** at 16.23;
59.7% at 13; **51.4%** at 12. Aim +37, double hex +5. 3.9 arrow hits a
cast. **Direct aim (no lead) reads 97.6% — do not "fix" the lead.**

## 1. IN THE ENGINE

- `f.ultSight = { t0, end }`. `tickWeapon`: while `ultSight`, theta turns
  toward the lead instead of `theta += spin·dt` (the ranged branch).
  `resolveHit`: the extra hex on a shot. The renderer draws the sigil at
  the lead point each frame (a pure function of state; no rng).

## 2. STAGES

**0 — control.** `ult_overlay.py --relic ironhail --cell runic:bow --mech
overlays/aim.js --arms A,C --seeds 20` on 151: A ~31%, C ~73%.
**1 — stubbed relic** at 16.23, runic, hex 1; engine_ab on 41; verify
30–40%; tip_audit.
**2 — the aim** (arm B). Gate: ~3.8 arrow hits a cast in windows against
~1.1 a window-equivalent outside (12.2 / 11.7 in/out a fight), theta
within 6·dt of the lead bearing on every window frame after the first
half-second (asserted), relic ~68%. FILM the sigil sliding.
**3 — the double hex** (arm C). Gate: hex applied = 2 × arrow hits in
windows, foe at ~2.8 on a window frame, relic ~73%.
**5 — the blade.** Wide on 151 at 11.5 / 12 / 12.5. Expect 11.5–12. Ladder
printed (hammers ~39%).
**6 — picture, voice, carry** per design §6. Beats: cast files `ult`;
arrows file as ever. Field in both copies. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder oracle_build.py`, one fight watched.

## 3. NOT TO RE-BUY

Turn 4 / 6 / snap → 60 / 75 / 77; no lead → 98; a pin on the arrow is +0.

## 4. OPEN

1. Rick's veto. 2. The blade. 3. Hammers. 4. The grid is full — what next
is Rick's.

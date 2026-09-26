# LODESTONE / REBUTTAL — BUILD BRIEF (v70). The runic warhammer, the 37th relic.

**Cowork, 2026-09-26. DESIGNED. Build from this and
`runic-warhammer-design-v70.md`; do not design (rule 0). Rick's veto comes
before stage 1 — check CLAIMS.md.** The build owns the blade.

## 0. THE RELIC

> For a duration the four walls are runed. Every time the enemy touches a
> wall the rune flares, hexes them, and hurls them straight back at the
> hammer. The walls do no damage — they hand the enemy back.

```
the cell        runic x warhammer          fighter LODESTONE      ultimate REBUTTAL
the card        "The walls are runed: a foe that touches one is hexed and hurled back"   68
the blade       ~22 (stage 5)              Grudgebearer's hammer profile; onHit {hex:1}
the window      8s every 16s
a touch         foe centre within inset + R + 1.5 on any side, alive, not pinned, once per 0.5s
the hex         apply("hex", 1, f)
the hurl        foe.vx, vy = 700 x unit(caster - foe)   (assigned; no damage, no beat, no hit stop)
```

Priced (design §3–4, 660 an arm, Chromium 141): body 21.4% → **57.3%** at
23.5; **50.3%** at 22; **49.7 / 48.5%** at 21. 8.4 touches a cast, the foe
at 4.0 hex stacks on an average window frame. Hex is +32 of the +36; the
hurl +4 and the picture.

## 1. IN THE ENGINE

- `f.ultRunes = { t0, end, cd }`; null elsewhere.
- `tickRunes`: the touch test against `m.inset` (the CURRENT hall), the
  cooldown, `foe.apply`, the velocity assignment. The caster's own touches
  are ignored. Nothing writes `f.stun` or `f.pin`; nothing goes through
  `resolveHit`.
- The runes are a picture on the inset line and walk with it.

## 2. STAGES

**0 — control.** `ult_overlay.py --relic grudgebearer --cell runic:warhammer
--mech overlays/rebound.js --arms A,C --seeds 20` on 151: A ~21%, C ~57%.
**1 — stubbed relic** at 23.5, runic, hex 1; gate: engine_ab on 36, verify
15–25%, tip_audit.
**2 — the hex on touch** (no hurl). Gate: ~8.4 touches a cast, ~4.0 stacks
on a window frame, relic ~53% (arm H). FILM the walls flaring.
**3 — the hurl.** Gate: a hurled foe leaves at 700 ±1 on the frame of the
touch (asserted), relic ~57% (arm C). engine_ab on 36. Freeze census: the
hurl must add ZERO freezes.
**4 — (none; three stages)**
**5 — the blade.** Wide, both sides, two blocks, 21 / 22 / 23 on 151.
Expect 21.5–22. Gate: verify 30–70 on 37; ladder printed (Gloamwire ~0 —
item 12/32).
**6 — picture, voice, carry** per design §6. Beats: cast files `ult`; a
touch files nothing (the director would cut to a wall eight times a
window — measure `beat_dist` if in doubt). Field in both copies. Move
`GAME`. `shell_identity`, `render_ab`, `chain_audit --builder
lodestone_build.py`, one fight watched.

## 3. NOT TO RE-BUY

The hurl alone is +2 (design §3); a bite on the hurl is +12 and not taken;
speed 500–900 is noise; cadence 1.0 costs 7.

## 4. OPEN

1. Rick's veto (hex-only fallback at 53%). 2. The blade. 3. The spread —
Rick's. 4. No arrival hitstun — declared.

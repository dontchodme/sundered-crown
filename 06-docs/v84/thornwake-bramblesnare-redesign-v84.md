# v84 — THORNWAKE / BRAMBLESNARE, REDESIGNED. Every blow leaves a bramble where it landed: a foe in one is rooted on the way in, entangled and bitten while it stays. The 1.6-second root was Rootfast with a different number.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0);
claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Lab:
`overlays/bramble.js`; runs in `06-docs/v84/runs/`.

## Why

`kind:"freeze"` — root 1.6s, 10 damage, 3 Entangle. Heartwood's Rootfast is
the same kind at 1.3s and 9 damage: one ultimate with two names (v68 §9).
Bramblesnare gets the BRAMBLES; Rootfast (v85) keeps the root. Thornwake
is a scythe that reaps — a bramble grows where the scythe cut.

# 1. §1 (Cowork)

> For a duration every blow the scythe lands leaves a bramble on the floor
> where it landed. An enemy that steps into a bramble is snared — rooted for
> a moment — and while it stays in one it is entangled and bitten by the
> thorns.

Three clauses: the bramble (a patch r 80 at the hit point, 6s); the snare
(a 0.6s pin on ENTRY — the school's root, spent per patch rather than once
per cast); entangle +1 and 2 damage every 0.5s inside (**the feed**).

# 2. THE HARNESS, AND THE CONTROL

Thornwake as shipped on `sc-trunk`, Chromium 141. **SHIP 47.9% (330), A
33.9%.**

# 3. PRICED (`runs/bramble_base`)

```
arm                                        win    casts  patches/cast  ticks/cast  dmg/cast  roots/cast
A   no ultimate                           33.9%
SHIP the 1.6s root                        47.9%
B   entangle + bite in a bramble          51.2%    3.04    1.36           5.7        11.5        —
C   + rooted on entry  (taken)            59.7%    3.07    1.32           7.8        15.5       2.9
```

1.3 brambles a cast (the scythe lands a blow every ~6s), the foe in one for
7.8 ticks a cast, snared 2.9 times. **The snare is +8 and it is the
school's verb where it reads** — a foe stopping dead as it steps into
thorns. 59.7 against a shipped 47.9: the blade from 31.35 to about **29**
(the scythe row 9.5–31.35).

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND

- A bramble is `{x, y, t0}` at the FOE's position on a landed blow; life
  6s; the hall's close does not clip it. Inside = foe centre within 80 +
  R of any bramble. On ENTRY (not inside last frame, inside now):
  `pin 0.6` (Grasp's write; ball and weapon). Inside: `entangle +1` and
  `hurt 2` every 0.5s — no knock, no hit stop, no beat (Scour's rule).
  Brambles outlive the window (a patch planted at 7.9s lives to 13.9s).
- Names kept: THORNWAKE / BRAMBLESNARE (it snares now). **Card (66):**
  `Blows leave brambles: a foe in one is rooted, entangled and bitten`.
- **Picture**: a tangle of dark-green thorn strokes on the floor (verdant
  `dark` with `core` highlights, r 80, source-over, alpha 0.5), growing
  out from the hit point over 0.3s and browning in its last second; the
  snare — four thorn shoots up the foe's rim for the pin's length (the
  Tendril root picture, reused); the entangle tag counts. Cast: the
  scythe's blade greens for the window. Field: leaf motes off each
  bramble, both copies.
- **Sound**: cast — a rustle-and-creak, 0.4s; a bramble opening — a dry
  crackle; the snare — a short creak and crack (Tendril's root voice,
  reused); a bite — a soft snap.

# 5. BUILD BRIEF

Stage 0 control on 151 (`--arms A,SHIP,C`). Stage 1 — freeze out,
`m.brambles[]` in, the tests, entangle + bite; gate: ~1.3 brambles a cast,
~5.7 ticks, relic ~51% at 31.35 (arm B). Stage 2 — the snare on entry;
gate: ~2.9 snares a cast counted as TRANSITIONS, relic ~60%. Stage 3 — the
blade, wide on 151 at 28 / 29 / 30 to the shipped rate. Stage 4 — picture,
voice, carry; `_drawField`'s hexagon must not draw on the snare (the
Tendril root picture instead); `engine_ab`, `shell_identity`, `render_ab`,
`chain_audit`, one fight watched.

# 6. Open decisions

1. Rick's veto. 2. The blade target. 3. Bramble life 6s outliving the
window — a design line; 8s (the window) is one number away.

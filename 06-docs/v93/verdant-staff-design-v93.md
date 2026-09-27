# v93 — BRIARWAND / BLOOM. THE VERDANT STAFF, the 46th cell. Its spell is a fan of thorns; its ultimate is a cloud of pollen that drifts after the foe and entangles whatever stands in it.

**DESIGNED — Cowork, 2026-09-27. Build from `BRIARWAND-BUILD-BRIEF.md`; do
not design this cell elsewhere; claimed in `06-docs/CLAIMS.md`.** Rick accepts
or rejects from this file. Lab: `tools/overlays/staff_verdant.js`; runs in
`06-docs/v93/runs/`. The row: `06-docs/v89/STAFF-ROW-v89.md`.

## Why this cell

Verdant's status slows (entangle: −13% swing, −6% move a stack, 4 stacks,
2.8s). It is worth most where it is CONTINUOUS (Bindweed's bites, v68;
Bramblesnare's patches, v84) and least on a bow that lands one arrow every
few seconds (the verdant bow body at blade 17 is 21.5%). A staff whose spell
lands MANY small hits and whose ultimate keeps the foe entangled without
needing to land anything is the cell.

---

# 1. §1 (Cowork)

> **THORNBURST (the spell).** Every 0.42s the staff throws not one thorn but
> a FAN of three — one along the facing and one either side at 0.28 rad —
> fast (440) and short-lived (1.2s: they reach ~500 and stop). Each is 0.6 of
> a blow; each that lands entangles 2.
>
> **BLOOM (the ultimate).** A cloud of pollen leaves the staff (r 110) and
> drifts after the foe at 90 px/s for 8s. A foe inside the cloud is
> entangled +1 and bitten for 2.5 every 0.4s.

Two clauses: the fan (the spell — three chances a cast, each smaller); the
cloud (the ultimate — a zone that MOVES, which no floor in the game does:
Consecration's discs, Bramblesnare's patches and Deadfall's sigils all wait).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141.0.7390.37, `sc-leaf`, Ironhail's bow as
`verdant × staff` (`onHit {entangle:2}`, own ultimate off), the spell as
`shot {cadence 0.42, speed 440, r 16, life 1.2, grav 0, dmgMul 0.6}` with two
more `spawnShot(caster, a ± 0.28)` on every cadence. The cloud is a point
that steps toward the foe each frame; inside it, `m.hurt` and `apply` on the
tick. The row's control (v89 §4) reproduced v75 to the fight. Arm A is the
verdant BOW body at the staff's blade.

# 3. THE FIRST FAN WAS WORSE THAN THE BOW

Blade 15, 330 an arm (`runs/verdant_15`): three thorns at **0.45**, life
**0.8** (range ~350), the cloud biting 1.5:

```
arm                                        win     hits in/out   thorns/cast   ticks/cast   in the cloud
A  bow body                               14.5%       — / 19.3
S  thornburst 0.45 / 0.8                   3.9%    10.8 / 16.7       52
U  + Bloom (bite 1.5)                     16.1%    11.2 / 17.1       51            13.2         59% of the window
W  plain arrow + Bloom                    31.2%     7.5 / 12.0        0            12.6         58%
X  + Bloom that does not drift            10.0%    11.1 / 16.7       51             6.7         28%
```

**27 thorn hits a fight at 0.45 is 12 arrows, and the bow lands 19**: the
fan was a worse weapon than the arrow (−11). The cloud is the right shape —
the foe is inside it 59% of the window when it drifts and 28% when it does
not (X: **the drift is the mechanic**) — but a bite of 1.5 every 0.4s on a
foe already entangled is +12 (W). Both were turned up: thorns to **0.6**
with life **1.2** (range ~500), the bite to **2.5**:

```
thornMul 0.6, life 1.2, bite 2.5        blade 15     blade 17     blade 20
S  thornburst                            12.1%        23.3%        41.5%
U  + Bloom                               36.7%        53.8%        69.7%
```

## 3.1 Settled — blade 17, 660 an arm (`runs/settle_verdant`)

```
A  bow body               21.5%
S  Thornburst             23.3%     +2 — the fan is the bow's equal, three thorns for one arrow: 27 thorn blows a fight (10.6/16.8 in/out), 53 thorns a cast-equivalent
U  + Bloom                53.8%     +31 — 12.4 bites a cast, 31 damage a cast, the foe inside 57% of the window and at 3.7 entangle on a window frame
```

The foe at **3.7 of 4 entangle stacks on the average window frame** is the
payload: −48% swing, −22% move for eight seconds, without the staff having
to land anything. The bite is the visible part of it.

# 4. THE BLADE

```
blade    spell (S)    whole (U)
15       12.1%        36.7%
17       23.3%        53.8%
20       41.5%        69.7%
```

**Crossing near 16.5.** Body ~20%. Expect 16.3–16.8 on 151 — inside the
bow row's range (Vinesower is 15.6).

**Type spread** (U, 660): **greatsword 79**, flail 68, scythe 51, twinblade
46, warhammer 45, **bow 27**. Worst Aureole 15, Farwarden 20, Marrowdraw 25;
best Emberedge 90, Goreshard 90, Heartwood 85. **The only staff the
greatswords do not beat, and the only one the bows do**: the fan is short
(500) and a bow outranges it; a greatsword has to come to it and is
entangled on the way.

# 5. DECLARED

- **The spell** — `shot: { cadence 0.42, speed 440, r 16, life 1.2, grav 0,
  dmgMul 0.6, fan 3, spread 0.28 }`. `tickFire` calls `spawnShot(f, theta +
  k·spread)` for `k = −1, 0, +1` when the profile has `fan` (the volley loop
  in `tickFire` is the template; `spawnShot` is untouched). Each thorn is a
  shot: clankable, `onHit {entangle:2}`, `maxLive` respected.
- **The ultimate** — `f.ultBloom = { t0, end, x, y, next }`. At cast the
  cloud is at the caster's centre. Each step it moves toward the foe by
  `min(dist, 90·dt)`. If `|foe − cloud| < 110 + R` and `t ≥ next`: `next = t +
  0.4`, `hurt(foe, 2.5, caster)`, `foe.apply("entangle", 1, caster)`. No knock,
  no stop (`over.stop 0` on the bite — the bite is a tick). The cloud is not a
  shot: nothing clanks it and walls do not stop it (it is clamped to the
  inset).
- Charge 16, window 8. Nothing waits.

# 6. NAMES, CARD, PICTURE, SOUND

**BRIARWAND** — a wand of briar; it throws its own thorns. From: Briarwand,
Seedcaller, Thornrod, Greenwitch.
**THORNBURST** (the spell). From: Thornburst, Briarfan, Thornspray, Bramble.
**BLOOM** — the pollen comes off it and goes looking. From: Bloom, Pollen,
Sporedrift, Miasma.
**Card (66):** `A pollen cloud drifts after the foe: inside it, entangle and bites`
**Shot tip (40):** `Throws a fan of three thorns · clankable`

## 6.1 The picture

- **The staff**: a living rod, bark and green `core`, a bud at the head; the
  thorns leave from the bud.
- **The spell**: three slim thorns (r 16, drawn long and narrow) fanning
  from the bud — the fan IS the picture; at 1.2s they drop and fade (no wall
  splash: a thorn that reaches its range simply falls).
- **Cast**: the bud opens; a cloud detaches — a soft disc r 110, verdant
  `glow` at alpha 0.22 with a brighter drifting inner texture (12 slow motes
  circling inside it), and it visibly leaves the caster and goes after the
  foe.
- **A bite**: a small green flash on the foe inside the cloud, the entangle
  tag ticks, the bite's number floats small.
- **Close**: the cloud thins to nothing over 0.5s.
- Field: pollen motes, both copies.

## 6.2 The sound

- **Cast**: a soft exhale into a rustle, 0.4s (the bud opening).
- **The cloud**: a very quiet sustained rustle while the foe is inside it
  (peak ≤ 0.12) — like v75's sigil, the one continuous voice, quiet on
  purpose.
- **A bite**: a short vegetable snap, pitched by entangle count.
- **Close**: the rustle fading.

# 7. Open decisions

1. Rick's accept/reject. A cloud that does not drift is +0 — the drift is
   the design.
2. The blade — 16.3–16.8, wide on 151.
3. Bows at 27 — Rick's; the fan's range (life 1.2) is the knob and is priced
   at 0.8 (worse) and 1.2 only.
4. The fan's spread (0.28) is a taste number: unpriced either side.

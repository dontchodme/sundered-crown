# v90 — BLOODWICK / GYRE. THE BLOODSWORN STAFF, the 43rd cell. Its spell is blood that bends toward the foe; its ultimate keeps that blood at home and throws it all at once.

**DESIGNED — Cowork, 2026-09-27. Build from `BLOODWICK-BUILD-BRIEF.md`; do not
design this cell elsewhere; claimed in `06-docs/CLAIMS.md`.** Rick accepts or
rejects from this file. Lab: `tools/overlays/staff_blood.js`; runs in
`06-docs/v90/runs/`. The row: `06-docs/v89/STAFF-ROW-v89.md`.

## Why this cell

The staff row (v89) opens with the school whose status is a RATE on the foe
(hemorrhage, 1.5/s a stack, 4 stacks): the bloodsworn bow (Marrowdraw) is the
row's strongest bow body, and a staff that lands MORE hits feeds it. The
bloodsworn bow body at blade 8.5 is **5.0%** — a bow cannot use a blade that
low; the spell is what makes the cell a relic.

---

# 1. §1 (Cowork)

> **BLOODSEEKER (the spell).** The staff throws a globule of blood every 0.34s
> along its facing, as a bow would an arrow — slower than an arrow (300), and
> it BENDS toward the foe as it flies (1.0 rad/s: a curve, not a hunt). Each
> that lands hemorrhages 2.
>
> **GYRE (the ultimate).** For 8s the globules do not leave: they orbit the
> caster's ball (r 95, four radians a second, up to six of them). When the foe
> comes within 230 they all lunge at once (520 px/s, homing hard) and each
> that lands hemorrhages. When the window shuts, whatever is still orbiting is
> loosed as ordinary seekers.

Two clauses: the bend (the spell, the fighter outside its window); the orbit
and the lunge (the ultimate — the close range, which kills every ranged
relic, becomes the window's strength).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141.0.7390.37, `sc-leaf`, Ironhail's bow as
`bloodsworn × staff` (`onHit {hemorrhage:2}`, own ultimate off), the spell as
`shot {cadence 0.34, speed 300, r 22, life 3.0, grav 0}` plus `home` on every
shot. The row's control (v89 §4) reproduced v75 to the fight. Arm A is the
bloodsworn BOW body at the staff's blade.

# 3. THE SPELL WAS THE FIGHTER, UNTIL IT WAS TURNED DOWN

Blade 14, 330 an arm (`runs/blood_14`):

```
arm                                              win     hits in/out   orbited/cast   lunged/cast
A  bow body                                     31.2%       — / 16.9
S  seeker, home 2.2                             96.4%     7.8 / 16.0
U  seeker 2.2 + Gyre                            97.3%     9.4 / 15.1       10.8           6.5
V  seeker 2.2 + Gyre, orbit only (no lunge)     83.0%     6.1 / 16.9       11.9           0
W  plain ARROW + Gyre                           81.5%    12.4 / 9.4        11.0           6.7
```

**A seeker that turns at 2.2 rad/s wins 96 of 100 with no ultimate**, and
Gyre on top of it is +1: there is no room. (v87: seeking is the strongest
property in the game; here it is a basic attack fired a hundred times a
fight.) At blade 7 the same seeker is 40.0% and Gyre +16 (`runs/blood_7`);
at blade 5, 11.8% and +15. The turn was cut instead of the blade:

```
home 1.0                       blade 8      blade 9      blade 10
S  the spell                    8.8%        18.2%        28.8%
U  + Gyre                      42.4%        63.3%        68.2%
V  + orbit only                12.4%        20.3%          —
```

At home 1.0 the globule BENDS (a turn radius of 300 at 300 px/s — it curves
toward a foe it is already nearly pointed at, and misses one it is not) and
Gyre is worth +34 to +45. **The lunge is the payload**: the orbit alone is
+2 to +4 (V), the moat is a picture.

## 3.1 Settled — blade 8.5, 660 an arm (`runs/settle_blood`)

```
A  bow body                5.0%
S  Bloodseeker            15.9%     +11        8.6 / 13.6 hits in/out
U  + Gyre                 50.5%     +45        15.4 / 12.9 · 11.4 orbited, 7.0 lunged, 5.3 blows in a window; foe at 3.2 hemorrhage on a window frame
```

# 4. THE BLADE

```
blade    spell (S)    whole (U)
 8        8.8%        42.4%
 8.5     15.9%        50.5%
 9       18.2%        63.3%
10       28.8%        68.2%
```

**Steep — 20 points between 8 and 9.** Crossing near **8.4**. The body at
that blade is ~15%: this is a relic that is its ultimate (Bindweed's shape,
v68: 1.5% → 54%). Expect 8.3–8.6 on 151.

**Type spread** (U, 660): flail 70, warhammer 59, scythe 54, bow 51,
twinblade 50, **greatsword 29**. Worst Dawnbringer 5, Lightkeeper 5, Axiom 10;
best Thornshear 90, Bloodmirror 80, Gravemourn 75.

# 5. DECLARED

- **The spell** — `shot: { cadence 0.34, speed 300, r 22, life 3.0, grav 0,
  dmgMul 1.0, home 1.0 }`. `spawnShot` copies `home` onto the shot (the field
  `tickShots` already reads for Bloodhunt's bolts — rate-limited turning,
  `s.a` written with the velocity). Clankable as any shot. `onHit {hemorrhage:2}`.
- **The ultimate** — `f.ultGyre = { t0, end, orb: [], phase }`. While it runs,
  a shot spawned by the caster with fewer than `maxOrb` (6) in orbit is
  taken into orbit: `home 0`, and each step `tickShots` places it at
  `caster + orbitR·(cos, sin)(phase + i·2π/n)` with the tangential velocity
  (`orbitR 95`, `orbitW 4.0`, life refreshed). When `|foe − caster| < lungeR`
  (230) and the foe is alive, every orbiter is loosed at the foe at `lungeV`
  520 with `home 8`, life 2.0. At close (clock, death, over) the orbiters are
  loosed toward the foe at the spell's own speed and home. Orbiters are
  clankable while orbiting — a blade through the ring is the counterplay,
  and it reads.
- Charge 16, window 8. Nothing waits.

# 6. NAMES, CARD, PICTURE, SOUND

**BLOODWICK** — a candle of blood; the staff is the wick. From: Bloodwick,
Veinwarden, Redwick, Haemyr.
**BLOODSEEKER** (the spell). From: Bloodseeker, Sanguine, Bloodlet, Vein.
**GYRE** — the blood circles, then strikes. From: Gyre, Bloodmoat, Orbit,
Sanguine Ring.
**Card (64):** `Its blood orbits it, then lunges as one when the foe comes close`
**Shot tip (40):** `Globules bend toward the foe · clankable`

## 6.1 The picture

- **The staff**: a dark rod with a head of red glass in which a flame gutters
  (`core` bloodsworn); the globule leaves from the flame.
- **The spell**: a fat drop of blood, r 22, with a short trailing tail drawn
  from its velocity; it visibly curves.
- **Cast**: the flame flares to twice its size for the window; a thin ring at
  r 95 (`glow`, alpha 0.35) shows the orbit's lane.
- **Orbit**: drops circling the ball at the lane, each with its tail; six of
  them at 4 rad/s is the tell.
- **Lunge**: every drop streaks out at once — a burst of tails toward the
  foe; `shake` 8, a bloodsworn `ring` at the caster.
- **Close**: the flame drops back, the lane fades 0.3s, the loose drops fly.
- Field: red motes drifting inward along the lane, both copies.

## 6.2 The sound

- **Cast**: a wet ignition — a low whump into a candle-hiss, 0.35s.
- **Orbit**: nothing continuous (v75's rule: continuous voices are quiet or
  absent); a soft tick as each drop takes its slot.
- **Lunge**: one sharp wet crack (the release), then the spell's own hit voice
  per landing, pitched by count.
- **Close**: the hiss cut short.

# 7. Open decisions

1. Rick's accept/reject.
2. The blade — 8.3–8.6, wide on 151. The curve is steep; settle both sides.
3. `home 1.0` is the design's one taste number that measurement CHOSE (it
   took the spell from 96% to a body): a slower bend (0.7) is unpriced and
   is the fallback if the curve reads as tracking.
4. Greatswords at 29% — Rick's.

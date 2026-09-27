# v92 — WATCHLIGHT / BEACON. THE VIGIL STAFF, the 45th cell. Its spell is a bolt of light that shoves; its ultimate sets down a lantern that keeps firing at the foe while the staff sweeps.

**DESIGNED — Cowork, 2026-09-27. Build from `WATCHLIGHT-BUILD-BRIEF.md`; do
not design this cell elsewhere; claimed in `06-docs/CLAIMS.md`.** Rick accepts
or rejects from this file. Lab: `tools/overlays/staff_vigil.js`; runs in
`06-docs/v92/runs/`. The row: `06-docs/v89/STAFF-ROW-v89.md`.

## Why this cell

Vigil banks what it deals as a plate (ward: 0.55 of damage dealt, cap 90,
40% shatter). On a bow the bank has to be 2.5× (Farwarden's `onSelf {ward:
2.5}`: an arrow deals ~11 and lands three in a window, so at 1× the pool is
a rumour — Farwarden's own comment). **The staff keeps the bow's 2.5**, and
that number is worth +17 alone at the staff's blade (§3). The vigil bow body
at blade 9.3 is 5.6% at ward 1 and 22.9% at ward 2.5.

---

# 1. §1 (Cowork)

> **WARDBOLT (the spell).** The staff throws a heavy bolt of light every
> 0.34s along its facing — wider than an arrow (r 26, 400 px/s) — and a foe
> it lands on is SHOVED (knock 420). Every landing banks ward.
>
> **BEACON (the ultimate).** The staff sets a lantern down where it stands.
> For 8s the lantern fires a wardbolt of its own at the foe every 1.2s —
> aimed at where the foe IS, at 420, lighter than the staff's (0.6) — and
> every lantern hit banks ward to the caster like its own.

Two clauses: the shove (the spell — a ranged relic that keeps the foe off
it); the lantern (the ultimate — a second source of fire that AIMS, so the
staff can keep sweeping while something else does the pointing).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141.0.7390.37, `sc-leaf`, Ironhail's bow as
`vigil × staff` (`onSelf {ward}`, own ultimate off; the harness's channel is
ward 1 and the module sets **2.5**, Farwarden's), the spell as `shot {cadence
0.34, speed 400, r 26, life 3.4, grav 0}` with `knock` on every shot. The
lantern pushes a shot into `m.shots` from a fixed point aimed at the foe;
its hits go through `resolveHit` with the caster as `self`, so the bank is
the engine's own. The row's control (v89 §4) reproduced v75 to the fight.
Arm A is the vigil BOW body at ward 1; **arm B is the bow at ward 2.5**, the
fair baseline for the spell.

# 3. A TURRET THAT AIMS IS ORACLE'S MONSTER WITH A LANTERN ON IT

Blade 13, 330 an arm (`runs/vigil_13`):

```
arm                                                     win     hits in/out   lantern shots/cast   shield on a window frame
A  bow body, ward 1                                    30.3%       — / 21.3
B  bow body, ward 2.5                                  54.8%     9.8 / 13.9
S  wardbolt (knock 220), ward 2.5                      58.8%     9.9 / 14.1
U  + Beacon, every 0.5s, 0.7, aimed direct             97.0%    22.7 / 11.8        14.6                 52.9
W  plain arrow + the same Beacon                       97.0%    22.5 / 11.8        14.5                 52.0
X  + Beacon aimed at the LEAD point                    92.1%    20.2 / 12.5        14.7                 48.2
```

A lantern firing twice a second at where the foe is lands 13 blows a window
(the staff lands 3) and the relic is 97% — **on the plain arrow too**: the
ultimate did not need the spell. Leading the aim (v75's prophecy) is 92%:
still no room. **The lantern was slowed, not un-aimed** — the picture is a
lamp that watches the foe and shoots, and a lamp that sweeps is a second
staff:

```
blade 10, every 1.2s, 0.6                    S           U
knock 220                                   27.6%       55.8%
knock 420                                   30.9%       58.2%
blade 8,  every 1.2s, 0.6, knock 220        10.9%       34.8%
```

At every 1.2s the lantern fires ~6.6 a window and lands 4.5; Beacon is +28.
**Knock 420 was taken** (a real shove, and +3 at 330).

## 3.1 Settled — blade 9.3, 660 an arm (`runs/settle_vigil`)

```
A  bow body, ward 1                5.6%
B  bow body, ward 2.5             22.9%     the bank is +17
S  Wardbolt, knock 420            20.5%     −2 against B: at 660 THE SHOVE IS FREE — kept for the picture (v69's root and canopy)
U  + Beacon                       49.7%     +29 over S       20.2 / 14.3 hits in/out · 6.6 lantern shots, 4.5 blows a window · shield 31 on a window frame
```

# 4. THE BLADE

```
blade    spell (S)    whole (U)
 8       10.9%        34.8%       (knock 220)
 9.3     20.5%        49.7%
10       30.9%        58.2%
13       58.8%        97.0%       (every 0.5s — not this design)
```

**Crossing near 9.3.** Body ~20%. Expect 9.2–9.6 on 151.

**Type spread** (U, 660): **bow 67**, warhammer 58, scythe 53, flail 48,
greatsword 40, twinblade 35. Worst Starwarden 0, Lightkeeper 5, Dawnbringer
15; best Vinesower 90, Gloamwire 75, Aureole 70. A vigil relic that beats
bows: the lantern's aimed bolts meet an arrow stream that cannot aim back.

# 5. DECLARED

- **The spell** — `shot: { cadence 0.34, speed 400, r 26, life 3.4, grav 0,
  dmgMul 1.0, knock 420 }`. `spawnShot` copies `knock` (the field the foe
  branch of `tickShots` already applies along the shot's velocity for
  Reprisal). Clankable. `onSelf { ward: 2.5 }` — Farwarden's constant, the
  bow row's, and the staff's.
- **The ultimate** — `f.ultBeacon = { t0, end, x, y, next }`. At cast the
  lantern is placed at the caster's centre (clamped inside the inset). Every
  `every` 1.2s while the window runs and both are alive, a shot is pushed
  from `(x, y)` at `atan2(foe − lantern)` — no lead — with `speed 420, r 22,
  life 3.0, grav 0, dmgMul 0.6, knock 150`, `own` the caster's, `lamp: true`
  (the art). It is a shot in every other respect: clankable, walls kill it,
  `resolveHit(caster, …)` lands it and banks ward at 2.5. `maxLive` is
  respected (refused, counted).
- Charge 16, window 8. Nothing waits.

# 6. NAMES, CARD, PICTURE, SOUND

**WATCHLIGHT** — the light that watches. From: Watchlight, Lamplighter,
Palewatch, Lanternwarden.
**WARDBOLT** (the spell). From: Wardbolt, Lightshove, Plateshot, Beam.
**BEACON** — a lamp set down that keeps the watch. From: Beacon, Lantern,
Watchfire, Sentry-lamp.
**Card (63):** `Sets down a lantern that fires at the foe. Every hit banks ward`
**Shot tip (40):** `Bolts of light shove the foe · clankable`

## 6.1 The picture

- **The staff**: a pale rod with a lantern-cage head; a warm vigil `core`
  burns in the cage. The bolt leaves from the cage.
- **The spell**: a broad, short bolt of light (r 26, drawn wider than it is
  long) with a bright head; on a landing the foe visibly jolts (knock 420 is
  bigger than Reprisal's 260) and the plate float ticks.
- **Cast**: the cage opens; a lantern is LEFT on the floor where the caster
  was — a small cage r 20 with the same core, a ground ring r 28 under it —
  and the caster moves on without it. The lantern is the tell.
- **A lantern shot**: the lantern flares, and a smaller bolt leaves it
  straight at the foe with a short trail.
- **Close**: the lantern gutters and goes out over 0.4s; the cage on the
  staff closes.
- Field: pale motes rising from the lantern, both copies.

## 6.2 The sound

- **Cast**: a lamp being set down — a wooden knock into a glass chime, 0.35s.
- **A lantern shot**: the staff's own shot voice, filtered brighter and
  quieter (it is the smaller bolt), pitched by the lantern's count.
- **A shove**: the game's hit voice with a low thump under it when
  `knock ≥ 400` (one flag on the play).
- **Close**: the chime reversed, short.

# 7. Open decisions

1. Rick's accept/reject. Direct aim at 0.5s is 97%; lead aim is 92%; the
   cadence is the knob (1.2s here). Every 1.5s is unpriced and is the
   fallback if the lantern reads as too much.
2. The blade — 9.2–9.6, wide on 151.
3. The shove measures free at 660. If Rick would rather the spell PAY,
   knock 600 is unpriced.
4. Twinblades at 35 — Rick's.

# v95 — CROZIER / RADIANCE. THE SANCTIFIED STAFF, the 48th cell. Its spell is a needle of light no blade can parry; its ultimate lets every needle grow into a shaft the farther it flies.

**DESIGNED — Cowork, 2026-09-27. Build from `CROZIER-BUILD-BRIEF.md`; do not
design this cell elsewhere; claimed in `06-docs/CLAIMS.md`.** Rick accepts or
rejects from this file. Lab: `tools/overlays/staff_sanct.js`; runs in
`06-docs/v95/runs/`. The row: `06-docs/v89/STAFF-ROW-v89.md`.

## Why this cell

Sanctified smites (a rate, 1.5/s a stack) and is blessed (a heal). The
sanctified bow (Aureole) sits mid-roster. The cell's problem was not the
body — the sanctified bow body at blade 14.5 is 28.2%, the row's best — it
was finding an ultimate that is not already one of the school's five (a
sun, a halo, holy ground, a dawn, shafts of light on a riser). **The first
ultimate priced here was Benediction with a staff in it and was rejected
for that** (§3).

---

# 1. §1 (Cowork)

> **LANCE (the spell).** The staff throws a needle of light every 0.34s along
> its facing — the fastest shot in the game (560), and the thinnest (r 16).
> No blade can parry it: it passes the foe's weapon and lands only on the
> foe. A landing smites.
>
> **RADIANCE (the ultimate).** For 8s every lance GROWS as it flies: over
> its first 0.4s (220 px) it swells from a needle (r 16) to a shaft (r 70)
> and its blow from 1× to 3×. The farther it has come, the bigger it is and
> the harder it lands. Up close it is still a needle.

Two clauses: the pierce (the spell — the one shot in the game a greatsword
cannot bat down); the growth (the ultimate — range, the type's own game,
paid for the first time: a ranged relic that is rewarded for being far).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141.0.7390.37, `sc-leaf`, Ironhail's bow as
`sanctified × staff` (`onHit {smite:1}`, own ultimate off), the spell as
`shot {cadence 0.34, speed 560, r 16, life 2.5, grav 0}`. **The pierce is the
module's**: the engine sees each lance as `r 1` and armed (so neither its
blade test nor its ball test reaches it) and the module runs the ball test
at the true radius and lands it through `resolveHit`. **Instrument caveat
(v89 §4):** the harness's `hits in/out` cannot see those landings; read
`lanceHits` (per cast). The row's control (v89 §4) reproduced v75 to the
fight. Arm A is the sanctified BOW body at the staff's blade.

# 3. A FAST SHOT LANDS LESS, AND THE FIRST ULTIMATE WAS SOMEBODY ELSE'S

Blade 14, 330 an arm (`runs/sanct_14`, `runs/sanct_14b`):

```
arm                                                        win     lance blows/cast   blows a fight
A  bow body                                               24.2%          —              17.3 arrows
S  lance (r 1 to the engine, r 16 to the module)          14.8%         2.43              7.6 lances
```

**The lance lands 7.6 a fight where the arrow lands 17** — at the same
blade it is ten points UNDER the bow. It is not the parry: with the engine's
own ball test (`r 16`, parryable) it lands the same 7 (`runs/dbg`: 39
against the arrow's 53 in three fights, and the pierce recovers nothing).
It is the speed and the size: a slow, fat arrow is walked into over its 3.4s
in the air; a needle at 560 is where it was aimed and nowhere else. **A fast
shot is a worse shot in this engine, and the row now knows it.** The lance
is kept — at a higher blade it is a sniper (46% at 20, 58% at 24: `runs/
sanct_blade_20`, `_24`) — and the pierce is kept for the picture and the
one matchup it changes (greatswords bat away a third of every arrow stream).

Then the first ultimate — SANCTUM, a ring of holy ground r 170 that travels
with the caster: a foe inside repelled (600 px/s²), smitten +1 and burned
1.5 every 0.4s, the caster blessed +1 every 0.5s while a foe is inside:

```
blade 14                                          win
U  lance + Sanctum                                71.2%      +56 — foe inside 41% of the window, 8.5 blessings a cast
X  Sanctum without the push                       65.5%      the push is +6
Y  Sanctum without the heal                       40.9%      the heal is +30
W  Sanctum on the plain arrow                     75.8%
```

Turned down (tick 1.0, bless every 1.0s) and decomposed again at blade 17
(`runs/sanct_17_decomp`): +42 whole, the push **+0**, the heal +16, the
smiting ground +26. A ring on the caster that smites foes inside it and
blesses her while one is **is Benediction (v82) with a staff in it** —
same radius, same two clauses — and the push, the one thing that was new,
measured nothing. **Rejected.** The replacement is the lance's own:

```
RADIANCE — the lance grows in flight              blade 17     grown/cast    lance blows/cast
S  the spell                                       33.0%                          2.39
Z  r 16 → 60, ×2.5, over 1.0s of flight            42.7%        12               2.66       +10: 1.0s is 560 px, most lances land or die before they grow
Z  r 16 → 70, ×3.0, over 0.4s of flight            69.4%        11.7             3.15       +36 — taken
```

## 3.1 Settled — blade 14.5, 660 an arm (`runs/settle_sanct`)

```
A  bow body               28.2%
S  Lance                  18.2%     −10 against the arrow: the fast shot's price · 7.6 lance blows a fight
Z  + Radiance             52.1%     +34 · 11.8 lances grown a cast, 3.2 lance blows a cast (8.8 a fight): a third more landings and each up to 3x
```

# 4. THE BLADE

```
blade    spell (S)    whole (Z)
14.5     18.2%        52.1%
15       17.6%        54.5%
17       33.0%        69.4%
```

**Crossing near 14.3.** Body ~18%. Expect 14–14.6 on 151 — a blade in the
bow row's range on a shot that lands half as often, so each landing is
the row's heaviest.

**Type spread** (Z, 660): **twinblade 70**, flail 56, bow 51, warhammer 49,
scythe 46, greatsword 46. Worst Duskreave 10, Lightkeeper 25, Farwarden 25;
best Twinshade 85, Widowmaker 80, Slagheart 80. **Inverted counters**
(Angelus's shape, v74): the twinblades' many small blades, which bat arrows
down, cannot touch a lance.

# 5. DECLARED

- **The spell** — `shot: { cadence 0.34, speed 560, r 16, life 2.5, grav 0,
  dmgMul 1.0, pierce: true }`. In `tickShots`, the blade-segment loop is
  skipped for a shot with `pierce` (one guard; the ball test is unchanged
  and lands it at `R + r`). Not clankable — the one shot in the game that is
  not. `onHit {smite:1}`.
- **The ultimate** — `f.ultRadiance = { t0, end }`. A shot spawned inside the
  window carries `grow: { born: t }`; each step before its tests, `k =
  min(1, (t − born) / 0.4)`, `r = 16 + 54·k`, `dmgMul = 1 + 2·k`. A shot
  spawned outside the window never grows, and a grown shot in flight when
  the window shuts keeps growing (it was cast in the window).
- Charge 16, window 8. Nothing waits.

# 6. NAMES, CARD, PICTURE, SOUND

**CROZIER** — a bishop's staff. From: Crozier, Reliquary, Sunspire, Evenstar.
**LANCE** (the spell). From: Lance, Needle, Sunlance, Shaft.
**RADIANCE** — the light grows as it goes. From: Radiance, Effulgence,
Brightening, Zenith (taken, v71).
**Card (65):** `Every lance grows as it flies: the farther, the bigger and harder`
**Shot tip (35):** `Needles of light no blade can parry`

## 6.1 The picture

- **The staff**: a gilt rod with a crook at the head (the crozier's curl), a
  sanctified `core` bead in the curl; the lance leaves from the bead.
- **The spell**: a thin bright line (r 16, drawn as a 60-px streak) — it
  crosses the hall in a third of a second and passes THROUGH a blade with a
  small white flick where it crossed (the pierce reads as "it went through").
- **Cast**: the bead flares; a thin halo ring on the staff head.
- **A grown lance**: the streak widens as it flies — by 220 px it is a shaft
  of light r 70 with a soft bloom (**§4.1b/c's gates: peak alpha 0.55, bloom
  radius ≤ 1.3× r, never white at centre**) — the growth is the tell and the
  viewer sees it lengthen and brighten.
- **A hit**: the smite tag, a flare sized to the shaft.
- **Close**: the bead dims; shafts in flight finish.
- Field: light motes streaming outward along the lances, both copies.

## 6.2 The sound

- **The spell**: a very short bright tick (the needle), pitched high; on a
  pierce the same tick with a glassy after-ring.
- **Cast**: a rising choir swell, 0.4s (the school's register: Zenith,
  Daybreak).
- **A grown lance landing**: the hit voice with a low bloom under it that
  scales with `k`.
- **Close**: the swell reversed.

# 7. Open decisions

1. Rick's accept/reject. Sanctum is priced (+42 turned down, +56 raw) and
   rejected as Benediction's; if Rick wants the ring anyway, it is a
   different cell's ultimate and the numbers are in `runs/`.
2. The blade — 14–14.6, wide on 151.
3. The growth's 0.4s / ×3 are two knobs (1.0s / ×2.5 is +10; 0.4s / ×3 is
   +36); the ladder between is unpriced.
4. Whether the spell should be SLOWER (380 lands 3.0 a cast against 560's
   2.4 — `runs/dbg`) — a slower lance is a better weapon and a worse picture.

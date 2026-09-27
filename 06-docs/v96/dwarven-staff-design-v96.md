# v96 — CULVERIN / IRONFALL. THE DWARVEN STAFF, the 49th cell. Its spell is an iron slug that falls; its ultimate lobs shells onto where the foe is going to be.

**DESIGNED — Cowork, 2026-09-27. Build from `CULVERIN-BUILD-BRIEF.md`; do
not design this cell elsewhere; claimed in `06-docs/CLAIMS.md`.** Rick accepts
or rejects from this file. Lab: `tools/overlays/staff_dwarf.js`; runs in
`06-docs/v96/runs/`. The row: `06-docs/v89/STAFF-ROW-v89.md`.

## Why this cell

Dwarven's status is a multiplier on damage taken (sunder: +11% a stack, 6
stacks) — the status that cannot confound a "did it land" measurement,
which is why Ironhail is the donor for every cell in this row. The dwarven
bow body at blade 13 is 22.3%. Dwarven is iron, forges and siege; a staff
that is artillery is the school's.

---

# 1. §1 (Cowork)

> **SLUG (the spell).** The staff lobs an iron slug every 0.55s along its
> facing: fast off the staff (470) but heavy — it FALLS (700 px/s²) — and big
> (r 28), and it hits for 1.6 of a blow. Slow to reload; each that lands
> sunders.
>
> **IRONFALL (the ultimate).** For 8s the staff also fires a SHELL every
> second, lobbed high to come down on where the foe will be 0.85s later.
> A shell that strikes the foe in flight hits for 1.3 of a blow; a shell
> that reaches its mark bursts (r 90, 8 damage) and sunders whatever is
> under it.

Two clauses: the slug (the spell — the only basic attack in the game with
gravity: a lob, not a line); the shell (the ultimate — aimed artillery
with a lead, the row's one aimed thing, and deliberately worse than direct).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141.0.7390.37, `sc-leaf`, Ironhail's bow as
`dwarven × staff` (`onHit {sunder:1}`, own ultimate off), the spell as
`shot {cadence 0.55, speed 470, r 28, life 3.0, grav 700, dmgMul 1.6}` — all
of it fields `spawnShot` and `tickShots` already read. The shell is a shot
pushed from the caster with a velocity solved for the lead point at a
flight time of 0.85s under 1000 px/s², `life 0.85`, and the engine's own
shard pop at life's end (`shard, pop 8, popR 90` — Slagburst's). The row's
control (v89 §4) reproduced v75 to the fight. Arm A is the dwarven BOW body
at the staff's blade.

# 3. THE SLUG IS THE BOW'S EQUAL, AND THE BURST IS A PICTURE

Blade 14, 330 an arm (`runs/dwarf_14`): shells every 0.7s at 1.6:

```
arm                                              win     hits in/out   shells/cast   sunder on a window frame
A  bow body                                     28.5%       — / 17.1
S  slug                                         28.5%     5.2 / 8.7
U  slug + Ironfall (lead)                       71.8%     8.3 / 7.7       10.6            3.4
W  plain arrow + Ironfall                       74.5%     9.4 / 9.4       10.6            3.7
X  Ironfall aimed at where the foe IS           89.4%     9.1 / 7.5       10.5            3.6
Y  Ironfall with no burst                       70.3%     8.2 / 7.6       10.6            3.3
```

**The slug lands 14 blows a fight at 1.6 where the arrow lands 17 at 1.0 —
the same relic (28.5 = 28.5)**, heavier and rarer: a ranged relic whose
every landing is a hit the viewer feels (a slug at blade 13 with ×1.6 lands
21 a blow, the row's biggest ordinary blow). **Direct aim is 89%** — the
lead is kept because it is worse (v75 §3, the prophecy). **The burst is
+1.5** — a shell that reaches its mark has usually missed, and 90 px is
not enough lead error; it is kept for the picture (the shell comes down
and bursts on the stone: v69's root and canopy). The shell rate was cut
0.7 → 1.0s and its strike 1.6 → 1.3 so the body is a body:

```
every 1.0s, strike 1.3, burst r 90        blade 12     blade 13
S  slug                                    15.5%        25.8%
U  + Ironfall                              38.5%        49.4%
Y  no burst                                35.8%        49.7%
```

## 3.1 Settled — blade 13, 660 an arm (`runs/settle_dwarf`)

```
A  bow body               22.3%
S  Slug                   24.1%     +2 — 14 blows a fight (5.5/8.4 in/out), each 1.6x
U  + Ironfall             47.9%     +24 — 7.3 shells a cast, 2.8 blows a window, foe at 3.1 sunder on a window frame
```

# 4. THE BLADE

```
blade    spell (S)    whole (U)
12       15.5%        38.5%
13       25.8%        49.4%   (330)  ·  24.1% / 47.9% (660)
14       28.5%        71.8%   (every 0.7s — not this design)
```

**Crossing near 13.2.** Body ~24%. Expect 13–13.5 on 151 — in the bow
row's range (Ironhail's own is 16.23 on an arrow at 1.0).

**Type spread** (U, 660): flail 56, scythe 56, warhammer 50, twinblade 48,
bow 47, greatsword 34. Worst Lightkeeper 15, Nightfell 25, Duskreave 25;
best Vinesower 75, Thornshear 75, Cindercleave 70. The flattest spread in
the row (22pp).

# 5. DECLARED

- **The spell** — `shot: { cadence 0.55, speed 470, r 28, life 3.0, grav 700,
  dmgMul 1.6 }`. **No new field.** `spawnShot` already copies `grav` and
  `dmgMul`; `tickShots` already integrates `s.vy += s.grav·dt`. A slug fired
  downward hits the floor and dies; one fired upward arcs. Clankable.
  `onHit {sunder:1}`.
- **The ultimate** — `f.ultIronfall = { t0, end, next }`. Every 1.0s while
  the window runs and both are alive: `T = 0.85, g = 1000`, `target = foe +
  v_foe·T`, `v = (target − caster)/T − (0, g·T/2)`; a shot pushed from the
  caster's centre with that velocity, `r 26, life T, grav g, dmgMul 1.3,
  shard, pop 8, popR 90` (the pop is `resolveHit` with `pop / dmg` as the
  multiplier, sundering — Slagburst's path, unchanged), `shell: true` (the
  art). Clankable, walls kill it (a lob from under the ceiling dies on the
  ceiling — measured in). `maxLive` respected.
- Charge 16, window 8. Nothing waits.

# 6. NAMES, CARD, PICTURE, SOUND

**CULVERIN** — an early cannon. From: Culverin, Bombard, Petard, Forgerod.
**SLUG** (the spell). From: Slug, Ironshot, Ingot, Lob.
**IRONFALL** — it comes down. From: Ironfall, Siege, Barrage, Cannonade.
**Card (70):** `Lobs shells that fall on where the foe will be, bursting and sundering`
**Shot tip (40):** `Lobs a heavy slug that falls · clankable`

## 6.1 The picture

- **The staff**: a short iron rod with a bell-mouthed head (the cannon's
  muzzle), a dwarven ember `core` in the mouth; the slug leaves from the
  mouth with a puff of 6 dark motes.
- **The spell**: a dull iron ball (r 28, no trail, a faint heat shimmer
  behind it) that visibly drops; it hits stone with a heavy `spawnFx` and no
  bounce.
- **Cast**: the mouth glows; every shell leaves with a bigger puff and a
  short ember trail, climbing, then coming down; a small iron ring (r 90,
  alpha 0.25) is drawn on the floor at the lead point for the shell's
  flight — the viewer sees where it will land before it lands (v75's rune).
- **A burst**: the ring flashes, 14 orange motes, `shake` 5 (the shard pop's
  own fx).
- **Close**: the mouth dims.
- Field: ember motes falling, both copies.

## 6.2 The sound

- **The spell**: a deep short thud on leaving (a cannon at a distance) and a
  stone crack on landing — the heaviest basic-attack voice in the game, on
  purpose (it fires half as often as an arrow).
- **Cast**: a mechanical ratchet into a low boom, 0.4s.
- **A shell**: the thud pitched down, then a whistle on the way down, then
  the burst (a bass hit with a stone rattle).
- **Close**: the ratchet reversed.

# 7. Open decisions

1. Rick's accept/reject. Direct aim (89%) is the untaken monster; every
   0.7s is +43 and was turned down to +24.
2. The blade — 13–13.5, wide on 151.
3. The burst measures +0 and is kept for the picture; `popR` 120 is
   unpriced and would make it pay (and read).
4. Greatswords at 34 — Rick's.

# v73 — COLDIRON / TEMPER. THE DWARVEN TWINBLADE, THE 40TH CELL. The lightest weapon in the game turns to iron for eight seconds, wins the binds it always lost, and every win sunders the foe past the cap.

**DESIGNED — Cowork, 2026-09-26 (~17:15 UTC). Build from
`COLDIRON-BUILD-BRIEF.md`; do not design this cell elsewhere; claimed in
`06-docs/CLAIMS.md`.** Cowork's end to end; Rick vetoes from this file. Lab:
`overlays/anvil.js`; runs in `06-docs/v73/runs/`.

## Why this cell, and what it is

Body **33.6%** with the field's ultimates live (9.7 + sunder's 23.9 — sunder
is the strongest channel on the fastest weapon, v59 §3's law), so the
ultimate needs +16 and has to be about something other than damage rate.
Closes the twinblade row to 6 of 7 and puts dwarven on 6 of 6 — **the third
school finished**.

**The twinblade** (v47): mass **1.1**, spin 5.7, reach 62, two blades each
with its own 0.45s `hitCd` — the most live edge in the game, and **it loses
every bind it takes**: `resolveClank` weighs `mass^1.7`, 1.1 against 3.0
is a 0.18 / 0.82 share, and the loser's weapon is knocked back and
staggered while the winner powers through. Twenty binds a minute (v47).
**Dwarven** — sunder `{6 stacks, 5s, +11% damage taken a stack}`. Crucible
and Slagburst SPEND it, Breach and Ironbloom apply it from hazards,
Quarrelstorm ignores it. The school is iron, forge and wall.

---

# 1. §1 (Cowork, 16:30 UTC)

> For a duration the twin blades are forged into cold iron. They are as heavy
> as a warhammer, so every bind the twinblade takes, it wins — the enemy's
> weapon is thrown back instead of its own — and each bind it wins sunders
> the enemy. While the iron holds, sunder stacks past its limit.

Three clauses: **mass** (1.1 → 5.0 for the window — the type's one weakness
deleted, and the fastest weapon becomes the heaviest); a won bind applies
sunder 2 (**the feed**, from the one event a twinblade had never profited
from); the sunder cap lifted 6 → 9 for the window (Corona's uncapped ruling,
bounded).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141, `sc-trunk`, Widowmaker's twinblade as
`dwarven × twinblade` (`onHit {sunder:1}`, own ultimate off). **Arm A
reproduces `cell_ults_on` to the fight: 33.64% = 111/330.** A won bind is
read off `f.clanks` and the engine's own share rule (`mass^1.7`, decisive
past 0.16).

# 3. THE MASS IS THE FIGHTER

Blade 11.95 (Widowmaker's), 660 an arm (`runs/anvil_full`):

```
arm                                            win    casts  hits in/out  binds/cast  won/cast  sunder/cast  foe stk  stack peak
A  no ultimate                                35.2%            —  / 18.9
S  sunder on a won bind, no mass (control)    33.6%   3.59   8.2 / 10.5     2.9        0.0        —          2.86
B  mass 5 only                                56.4%   3.52  10.3 / 10.4     3.1        2.7        —          3.26      4.4
C  mass + sunder 2 on a won bind              61.7%   3.47   9.8 / 10.1     3.1        2.7       5.4         4.60      5.6
D  + the cap lifted to 12                     73.9%   3.27   8.8 /  9.3     3.0        2.6       5.2         6.74      9.5
```

**Mass alone is +21.** The control says why: with the twinblade's own mass
it wins **0.0** of its 2.9 binds a window; at mass 5 it wins **2.7 of 3.1**,
and every one of those is the foe's weapon thrown back and staggered
instead of its own. The type's whole disadvantage, reversed, on the weapon
that binds most. Sunder on the win is +5; the cap lift is +12 — the foe
peaks at 9.5 stacks, +105% damage taken, and that is too much at any blade
inside the row (blade 9 still reads 58%; `runs/anvil_b9`).

**Cap 9 instead of 12** (`runs/anvil_cap9_*`): peak 8.0, and the blade
lands inside the row:

```
blade   cap    whole (D)
 10      9      53.3%
  9      9      50.2 / 48.8%   (two blocks)
```

# 4. THE BLADE — inside the row

**Crossing near 9.3** — Spellbreaker's 8.8, Twinshade's and Starwarden's
8.3 are the row; body ~17–21% at 9–10. Expect 9–9.5.

**Type spread** (D, blade 9): greatsword 66, bow 54, flail 48, twinblade 48,
scythe 43, **warhammer 37** — mass 5 against mass 5 is a deadlock, not a
win, so the hammers are the one row the iron does not beat. Worst Ravelbone
15 (the wire holds the ball; a bind needs a swing), Threshmaw 25,
Bloodmirror 25. Best Goreshard 85. 29pp — the narrowest in the batch.

# 5. DECLARED

- **Mass**: `w.mass` read at cast → the lab wrote the weapon; the build
  gives `Fighter` a `massMul` (1 everywhere else) multiplied at every
  `w.mass` read — `resolveClank`'s shares, `move`'s gravity term,
  `ballCollision` if it reads mass, the burden term — and the builder
  refuses if any read lacks it. **Declare the gravity consequence**: a
  mass-5 ball falls `(5/2.68)^0.5 = 1.37×` faster; the lab priced it in.
- **A won bind** applies `sunder 2` through `foe.apply` inside
  `resolveClank`, only when `aWins` is decisive and the winner has
  `ultIron`. Nothing else in the clank changes.
- **The cap** is `STATUS.sunder.maxStacks` read at `apply` — per-fighter,
  the way `bleedCap` is: `f.sunderCap` on the foe BEING sundered, recomputed
  every frame from whether the caster's window is open (Bloodletting's
  rule: no paired write to forget; stacks above the cap when it drops run
  out on sunder's own 5s clock).
- Charge 16, window 8. Nothing waits.

# 6. NAMES, CARD, PICTURE, SOUND

**COLDIRON** — the iron of the old stories, that nothing fey can bear;
the row's names are Ironhail, Emberedge, Cindercleave. From: Coldiron,
Pigiron, Blacktemper, Forgebrand.
**TEMPER** — a blade is tempered, and the dwarves have one. Crucible's
register. From: Temper, Anvil, Quench, Ironclad.
**Card (69):** `Blades of cold iron: it wins binds, and each win sunders past the cap`

## 6.1 The picture

- **Cast**: the two blades QUENCH — a flash of forge-orange along each edge
  that cools to black iron over 0.3s (dwarven `dark` fill, `steel` edge
  gone matte); the blades draw 1.4× thicker for the window (the mass,
  visible). The ball does not change.
- **A won bind**: the engine's own clank picture already throws the loser's
  weapon back; add an ANVIL RING — a short radial spark burst at the
  contact point (drawn, 6 sparks, no rng) — and the sunder tag on the foe
  ticking up. A tag past 6 prints in dwarven's `core` rather than the
  default, so "past the cap" is a colour.
- **Close**: the blades cool from black back to steel over 0.4s; no debris.
- Silhouette: a dwarven twinblade — two broad riveted cleavers, first cut
  (open item 34's construction rule: rivets ON the outline, not on top).
- Field: forge sparks off the blades at every won bind, both copies.

## 6.2 The sound

- **Cast**: a quench hiss into a low iron ring, 0.5s.
- **A won bind**: an anvil strike (a hard metallic hit with a 0.3s ring,
  peak ≤ 0.6) over the engine's clank voice; pitch steps up with the
  sunder count.
- **Close**: the ring dying, 0.4s.

# 7. Open decisions

1. Rick's veto. If the cap lift is unwanted, arm C (cap 6) reads 61.7% at
   11.95 and lands near blade 10.5.
2. The blade — 9–9.5, wide on 151 after reproducing A (~35%) and D (~50%
   at 9, cap 9).
3. `massMul`'s reach — every read of `w.mass` is a declared site; the build
   lists them.
4. Hammers at 37% — the one row iron does not beat; Rick's.

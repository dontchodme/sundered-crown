# v75 — ORACLE / FORESIGHT. THE RUNIC BOW, THE 42ND CELL — THE LAST OPEN CELL. Every arrow flies to where the foe will be — and aiming at where it IS was worth twenty points more, which is why the prophecy leads.

**DESIGNED — Cowork, 2026-09-26 (~19:45 UTC). Build from
`ORACLE-BUILD-BRIEF.md`; do not design this cell elsewhere; claimed in
`06-docs/CLAIMS.md`.** Cowork's end to end; Rick vetoes from this file. Lab:
`overlays/aim.js`; runs in `06-docs/v75/runs/`.

## Why this cell, and what it is

The last empty coordinate on the 7 × 6 grid: body **33.6%** with the field's
ultimates live (hex +20.6 on a weapon that lands 20 arrows a fight). Closes
the bow row to 7 of 7 and runic to 6 of 6 — **every type and every school
finished; 42 of 42.**

**The bow** (v40): arrows leave along `f.theta` every 0.34s at 380 as the
weapon spins at 2.8 — a stream that sweeps the room and hits when the
sweep happens to cross the foe. The one aimed shot in the game is
Reprisal's, and it is one shot. **Runic** — hex; Corollary and Unmaking
bolts, Converse's sigils and rewind, the Stasis Field, Rebuttal's runed
walls. The school knows things in advance (Foregone, Corollary).

---

# 1. §1 (Cowork, 19:00 UTC)

> For a duration the bow foresees. A rune appears on the floor where the
> enemy is going to be when the next arrow lands, and every arrow of the
> stream flies to that rune instead of wherever the bow happens to be
> pointing. An arrow that lands hexes twice.

Two clauses: the aim (the facing turned at 6 rad/s toward the LEAD point —
foe position plus velocity times time of flight); the double hex (**the
feed**, +1 on every arrow that lands inside the window).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141, `sc-trunk`, Ironhail's bow as `runic × bow`
(`onHit {hex:1}`, own ultimate off). **Arm A reproduces `cell_ults_on` to
the fight: 33.64% = 111/330.** The lead is `foe + v_foe × d/380`; grav is 0
on this bow so the aim is `atan2`.

# 3. THE AIM IS THE FIGHTER, AND THE LEAD IS A CHOICE THAT COSTS

Blade 16.23 (Ironhail's), 330 an arm (`runs/aim_base`):

```
arm                                              win    casts  arrow hits/cast  hits in/out  foe hex
A  no ultimate                                  33.6%                             —  / 19.9
B  aim (lead, turn 6)                           67.3%   3.07     3.8           12.2 / 11.7    2.09
C  aim + a second hex on every hit              74.5%   3.09     4.0           12.8 / 11.6    2.87
D  aim + a 0.25s pin on every hit (stasis)      67.3%   3.13     3.7                          2.05
```

**+34 for aiming the stream**, +7 more for the double hex, and a stasis on
the arrow is worth nothing (not taken). The mode-`swing` finding from
August on the last type that had never had it.

Then the knob nobody expected (`runs/aim_turn4`, `_snap`, `_nolead`):

```
aim                              win     arrow hits/cast
lead, turn 4                    59.7%      3.4
lead, turn 6   (taken)          74.5%      4.0
lead, snap                      76.7%      4.5
NO lead — aim at where it IS    97.6%      7.5
```

**Aiming at where the foe IS lands twice as many arrows as aiming at where
it WILL be.** The foe's motion is a bounce, not a line — 380 px/s over a
300-unit range is 0.8s of flight, and a ball at cruise has hit a wall by
then — so linear foresight overshoots and direct aim does not. Direct aim
is 98% at the type's blade and no blade in the row can carry it. **The
prophecy is kept BECAUSE it is worse**: it is the picture (a rune drawn
where you are about to be, and the arrows already on their way), it is
what the school does, and its price is the balance.

## 3.1 The whole, decomposed — blade 16.23, 660 an arm (`runs/aim_full`)

```
A  no ultimate     31.1%
B  the aim         68.2%     +37
C  + double hex    73.2%     +42      3.9 arrow hits a cast, the foe at 2.8 hex on a window frame
```

# 4. THE BLADE

```
blade    body (A)    whole (C)
 16.23    31.1%       73.2%
 13.0     14.8%       59.7%
 12.0     13.8%       51.4%
```

**Crossing near 11.8** — Farwarden's 12.7 and Gloamwire's 9.5 are the
row's floor; the body is ~14%. Expect 11.5–12.

**Type spread** (C, blade 12): bow 69, flail 69, greatsword 48, scythe 46,
twinblade 45, **warhammer 39**. Worst Shroudmaul 15, Duskreave 15, Bulwarden
20 (holds and a shield). Best Vinesower 90, Threshmaw 90. 30pp — narrow.
A bow that beats bows is new on the roster.

# 5. DECLARED

- **The aim**: `f.theta` turned at 6 rad/s toward `atan2(lead − f)` each
  window frame, `lead = foe + v_foe × (|foe − f| / shot.speed)`; the spin
  does not advance theta while the window runs (Tendril's construction).
  `tickFire` is untouched — the stream fires on its own cadence along the
  aimed facing. **Grav-0 bows only**: this bow's `shot.grav` is 0; if the
  build's profile has gravity it uses `ballisticAngle` as `ultDraw` does.
- **The double hex**: in `resolveHit`, when a SHOT owned by a caster with
  `ultSight` lands: `foe.apply("hex", 1, f)` in addition to the channel's.
- Charge 16, window 8. Nothing waits.
- No stasis, no pin, no stun beyond hex's own.

# 6. NAMES, CARD, PICTURE, SOUND

**ORACLE** — it knows where you will be. From: Oracle, Augur, Sibyl, Seer.
**FORESIGHT** — the runic register of Foregone and Corollary. From:
Foresight, Augury, Prophecy, Sequence.
**Card (68):** `Every arrow flies to where the foe will be, and each hit hexes twice`

## 6.1 The picture

- **Cast**: a rune-eye opens on the bow's ball (a sigil ring, runic
  `core`, 0.25s) and stays for the window.
- **The rune on the floor**: drawn at the lead point every frame — a small
  runic sigil (r 14, `glow`, alpha 0.5) with a thin sight-line from the
  bow to it. The sigil is THE tell: the viewer sees where the arrow is
  going before the foe gets there. It slides as the prediction moves.
- **The arrows** carry a rune glyph on the shaft and a short `core` trail
  (drawn from velocity) for the window; the stream is the same stream.
- **A hit**: the hex tag ticks by two; a rune flare on the foe.
- **Close**: the eye shuts, the sigil fades over 0.3s.
- Silhouette: a runic bow — a recurve etched with a sigil at the grip,
  first cut. Field: rune motes along the sight-line, both copies.

## 6.2 The sound

- **Cast**: a rune-eye "open" — a filtered inhale into a soft chime, 0.4s.
- **The sigil**: a very quiet sustained shimmer (re-struck, 2–3 kHz band,
  peak ≤ 0.15) while it is drawn — the only continuous voice in the batch,
  and quiet on purpose.
- **A hit**: the bow's own arrow voice plus a hex snap; pitch by count.
- **Close**: the chime reversed.

# 7. Open decisions

1. Rick's veto. Direct aim (98%) is the untaken monster; a slower turn on
   direct aim is unpriced and would be the fallback if the prophecy sigil
   reads as a miss.
2. The blade — 11.5–12, wide on 151 after reproducing A (~31%) and C
   (~73% at 16.23).
3. Hammers at 39% — Rick's.
4. **THE GRID IS FULL.** Every cell has a design or a relic. What the grid
   does next — the redesign list (v68 §9), the type-spread question (item
   12/32, now with fifteen data points), and whether N was ever meant to
   be 42 — is Rick's.

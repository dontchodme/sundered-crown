# v74 — ANGELUS / ASCENSION. THE SANCTIFIED TWINBLADE, THE 41ST CELL. The relic rises and hangs in the air; its two blades become two shafts of light that sweep the hall beneath it, and every hit of the light heals it — and hung at the ceiling it was untouchable, which was the wrong fighter.

**DESIGNED — Cowork, 2026-09-26 (~18:30 UTC). Build from
`ANGELUS-BUILD-BRIEF.md`; do not design this cell elsewhere; claimed in
`06-docs/CLAIMS.md`.** Cowork's end to end; Rick vetoes from this file. Lab:
`overlays/ascend.js`; runs in `06-docs/v74/runs/`.

## Why this cell, and what it is

Body **30.3%** with the field's ultimates live (smite +20.6 on the fastest
weapon). Closes the twinblade row to 7 of 7 (**the fourth type finished**)
and puts sanctified on 6 of 6 (**the fourth school**). The ultimate needs
+20 and the school's two verbs are LIGHT and HEAL; the type's are speed
and two blades.

---

# 1. §1 (Cowork, 17:40 UTC)

> For a duration the relic rises off the floor and hangs in the air. Its two
> blades become two shafts of light that reach all the way to the floor and
> sweep the hall as the blades turn. A shaft that passes through the enemy
> is a hit, lighter than a blade's, and every hit of the light heals the one
> hanging above.

Three clauses: the rise (the caster pinned in the air, weapon free —
Canopy's self-root, up instead of down); the shafts (`reachMul` 10 on two
blades at half spin, at 0.4 damage — the blades ARE the light); the heal
(blessing +1 on every shaft hit — **the feed**, on the school's second
status, earned by landing the first).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141, `sc-trunk`, Widowmaker's twinblade as
`sanctified × twinblade` (`onHit {smite:1}`, own ultimate off). **Arm A
reproduces `cell_ults_on` to the fight: 30.30% = 100/330.**

# 3. AT THE CEILING IT IS UNTOUCHABLE, AND THAT IS NOT THE FIGHTER

Hung at the top of the hall (`inset + R + 6`), blade 11.95, 330 an arm
(`runs/ascend_base`):

```
A 30.3%    B shafts only 70.6%    C + heal on hit 84.8%    D + smite 2 a hit 92.7%
```

**+40 from the shafts alone** — and the shafts land only 4.4 hits a window.
The forty points are the caster hanging where no blade can reach it for 24
seconds of a 60-second fight. Eight seconds in which the foe can do nothing
is not a set-piece, it is a pause, and a relic that wins by hiding is the
wrong fighter for a game people watch.

So it hangs LOWER — inside the hall, where a jumping ball's blade reaches
it (`runs/ascend_y200`, `_y300`, shafts + heal):

```
hang y      shafts only    + heal
 ceiling       70.6%        84.8%
  200          63.9%        85.5%
  300          43.3%        60.6%     <- taken: reachable, and the light is the fighter
```

At y = 300 (of 800; the hall's top third, above the inset even at full
close) the caster is hit while it hangs, the shafts are worth +13, and the
heal is worth +17 — **the mechanic is the payload, not the position.**

## 3.1 The whole, decomposed — y 300, blade 11.95, 660 an arm (`runs/ascend_y300_full`)

```
arm                                     win    casts  hits in/out   shaft hits/cast  bless/cast  foe smite
A  no ultimate                         28.5%            —  / 18.8
B  rise + shafts                       43.9%   3.56  18.4 / 11.0       5.1              —          2.90
C  + blessing on every shaft hit       62.7%   3.80  19.7 / 11.9       5.2             5.2         2.93
D  + smite 2 a hit                     67.7%   3.75  19.3 / 11.8       5.1             5.1         3.34

D − A  +39   the shafts +15, the heal +19, extra smite +5 (not taken — the heal is the school's answer and one payoff reads)
```

**Five shaft hits a cast, and five blessing stacks — ~36 hp healed a cast.**
The shafts land at 0.4 of the blade (4.8 a hit) and hit a foe anywhere on
the floor beneath.

# 4. THE BLADE

```
blade    body (A)    whole (C)
 11.95    28.5%       62.7%
 10.0     15.2%       53.9%
```

**~4.5 points a damage point; crossing near 9.3** — the row (Twinshade 8.3,
Spellbreaker 8.8, Coldiron ~9.3). Expect 9–9.5.

**The type spread is INVERTED against every other cell in this batch** (C,
blade 10): **warhammer 81**, flail 68, bow 68, scythe 54, greatsword 35,
**twinblade 19**. A hanging target is punished by fast blades that reach it
(Twinshade 5%, Starwarden 15%) and beats the slow heavy weapons that can't
(Censer and Lastlight 95%). The batch's other seven all lose to bows; this
one beats them. 62pp — the widest — and the first cell whose counters are
the fast ones; item 12/32 gets a data point from the other side.

# 5. DECLARED

- **The rise**: at cast the caster is moved to `(W/2, 300)` and pinned
  there (`pin`, `pinFree 1`, re-armed each frame; released to rest on
  close). **Moved, not flown** in the lab; the build eases it up over 0.35s
  and the shafts light when it arrives (the lab's price counts the full
  window as live — the build's gate re-prices at its own rise time). A
  pinned caster is immovable, takes hits, takes no knock.
- **The shafts** are the two blades at `reachMul 10` (620 units — past the
  floor from y 300; `bladeSegments` reads it), spin × 0.5, damage × 0.4 in
  `resolveHit` off `f.ultRise` (the Canopy rule: scale in the hit, not on
  the weapon). Everything else about a blade blow — smite 1, hit stop,
  knock, the beat, binds — is the blade's. **A shaft that reaches the far
  wall is drawn to the wall, not past it.**
- **The heal**: `f.apply("blessing", 1, f)` per shaft hit that lands,
  through the existing `tickStatus` heal.
- Charge 16, window 8.
- The caster's own ball does not fall while pinned; on close it drops.

# 6. NAMES, CARD, PICTURE, SOUND

**ANGELUS** — the bell rung at dawn, noon and dusk; the word carries the
angel. From: Angelus, Seraph, Matins, Aureate.
**ASCENSION** — it rises. The school's Harrowing is a descent; this is the
other way. From: Ascension, Rapture, Assumption, Aloft.
**Card (69):** `Rises into the air; its blades become shafts of light. Each hit heals`

## 6.1 The picture (§4.1b/c: sanctified's light is a bloom risk — measured at stage 6)

- **The rise**: the ball lifts to y 300 over 0.35s on a drawn column of
  light that fades once it hangs; a halo ring (source-over, r 1.1 × R,
  sanctified `glow`, NOT `lighter`) marks it hanging.
- **The shafts**: each blade drawn as a shaft — a soft-edged bar of light
  10 units wide with a hot 3-unit core, alpha 0.55, from the ball to the
  floor or wall; the shaft's foot throws a small pool of light on the
  floor where it lands. Under `lighter` ONLY the core; the body of the
  shaft is source-over. `harrow_bloom_probe`: arena-mean lift ≤ +0.03
  (two 600-unit bars are the largest light source this game will have
  drawn; the gate is a number, not a hope).
- **A shaft hit**: the blade's own flash, plus a blessing tag on the
  caster and a thin thread up the shaft to the ball (Zenith's "what it
  burns heals" line, along the light).
- **Close**: the shafts shorten to blades over 0.3s, the halo goes, the
  ball drops.
- Silhouette: a sanctified twinblade — two slim leaf-blades with a halo
  guard, first cut. Field: light motes drifting down the shafts, both
  copies.

## 6.2 The sound

- **The rise**: a choir swell (three re-struck tones a fifth and octave
  apart, 0.6s) — the one voice in the game allowed to be a chord.
- **A shaft hit**: a bright glassy tap, 70ms, quiet; blessing count in the
  pitch.
- **Close**: the chord resolving down and the ball's landing thud.

# 7. Open decisions

1. Rick's veto. If a hanging relic reads as hiding even at y 300, the
   ceiling numbers say the position is the lever: y 200 reads 86% and the
   floor (no rise, shafts from the ground) is unpriced.
2. The blade — 9–9.5, wide on 151 after reproducing A (~28%) and C (~63%
   at 11.95, y 300).
3. The bloom gate (+0.03) — a floor, measured at the build.
4. Twinblades at 19% — the inverted counter; Rick's (item 12/32).
5. The rise time (0.35s) shortens the live window by ~4%; the stage-2 gate
   prices it.

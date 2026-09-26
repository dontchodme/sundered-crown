# v71 — MORNINGSTAR / ZENITH. THE SANCTIFIED FLAIL, THE 38TH CELL. The head becomes a sun on a chain: its light smites whoever it falls on, and every burn heals the bearer.

**DESIGNED — Cowork, 2026-09-26 (~14:30 UTC). Build from
`MORNINGSTAR-BUILD-BRIEF.md`; do not design this cell elsewhere; claimed in
`06-docs/CLAIMS.md`.** Cowork's end to end; Rick vetoes from this file. Lab:
`tools/ult_overlay.py` + `overlays/sun.js`; runs in `06-docs/v71/runs/`.

## Why this cell

Tied for least-decided on the v68 table with the verdant flail: body **6.9%**
with the field's ultimates live (smite +3.3 on a weapon that lands a blow
every 6.6s against a 3.2s status). Puts the flail row at 6 of 7 and
sanctified at 5 of 6.

## What the cell is made of

**The flail**: the head is the weapon, 13.2 units of it, roaming a band out
to ~119 around the caster and live in one stub of it (v43). Tendril (v68)
answered that by making the chain reach; this cell answers it the other way
— **by making the head's LIGHT the weapon**, so the ground the head covers is
the ground that burns. **Sanctified** — smite `{4, 3.2s, 1.5 dps a stack}`,
byte-identical to hemorrhage at half the application rate (v59 §4.2), and
**blessing** `{5, 6s, heals 1.2 a second a stack}`, the school's own second
status, which only Daybreak's sparks and Benediction touch today. Daybreak
sprays sparks that heal when collected, the Harrowing sprays scythes,
Benediction is a beam that heals 28, Consecration a nova. **The school's
verbs are LIGHT and HEAL**, and — CLAUDE.md §4.1b/c — sanctified is the
school that has blown the bloom out twice by painting white light over a
white body. §6.1 is written against that.

---

# 1. §1 (Cowork, 13:20 UTC)

> For a duration the flail's head becomes a sun. Everything the head swings
> through is lit, and an enemy standing in that light is smitten and burned
> for as long as it stays in it. Every burn the light lands heals the one
> swinging it. The head still hits like a flail head; the light is the rest
> of the weapon.

Three clauses: the light is a disc around the head (the roaming band made
live); in it the foe takes smite + a burn tick (**the feed**); each burn
blesses the caster (**the school's second status, tied to the first** — the
same shape as Corona's burn feeding the ward: the payoff is earned by
landing the mechanic, not by standing there).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141, `sc-trunk`, Gravemourn's flail as `sanctified
× flail` (`onHit {smite:1}`, own ultimate off), 330 / 660 fights an arm.
**Arm A reproduces `cell_ults_on` to the fight: 6.97% = 23/330.** Ticks pay
through `m.hurt` (ward first); smite and blessing are the real statuses
through `apply`.

# 3. THE LIGHT, THE BURN AND THE HEAL — each is a third

Blade 24.03 (Gravemourn's), radius 70, 330 an arm (`runs/sun_base`):

```
arm                                         win    casts  lit%   ticks/cast  dmg/cast  bless/cast
A  no ultimate                              7.0%
B  smite only                              16.4%   3.03   14%     4.3          —          —
C  smite + burn (3 a tick)                 28.5%   2.97   14%     4.2        12.7         —
D  + blessing, 1 a second while it burns   50.3%   3.36   14%     4.3        13.0        7.5
T  the TRAIL instead (the head's path)     59.1%   3.21   32%     8.3        24.8        7.4
```

The foe is in a 70-light **14%** of the window. Smite alone is +9, the burn
+12 more, and **the heal is +22** — healing is the biggest single channel in
the school and nobody has priced it on a set-piece before. A trail of light
along the head's path (its last 1.5s as a ribbon of 30-discs) lights the
foe twice as often and reads 59%; it is not taken — it is the tip ribbon
the engine already draws, made into a hazard, and a sun on a chain is the
picture.

**Radius** (`runs/sun_r*`, blessing on time): 70 → 50.3, **100 → 55.8** (lit
21%), 130 → 63.0 (lit 29%). 100 taken: the light reaches a third of the way
across the hall from the head, and the head is out to 119 — so the lit
ground is most of the caster's half of the room.

**The heal tied to the burn** (`blessOnTick`): 100 → **51.5%** against 55.8
on a clock. Four points for a rule that reads — *what it burns, heals* — and
that cannot pay while the light lands on nothing. Taken.

## 3.1 The whole, decomposed — blade 24.03, radius 100, 660 an arm (`runs/sun_settled_full`)

```
arm                                   win     casts  hits in/out  lit%   ticks  dmg    bless   foe stk
A  no ultimate                        7.6%              —  / 8.5
B  smite only                        18.5%    3.01   3.4 / 4.9    20%    5.9     —       —      2.68
C  smite + burn                      26.1%    2.95   3.3 / 4.7    20%    5.8   17.5      —      2.67
D  THE WHOLE                         50.2%    3.23   3.8 / 5.2    20%    6.0   17.9     6.0     2.70

D − A  +42.6   smite +11, the burn +8, the heal +24
second block (seed0 9001): D = 50.6%
```

**6 ticks a cast: 18 damage, 6 smite stacks (the foe at 2.7 on an average
window frame), and 6 blessing stacks on the caster — ~36 hp healed a cast
at 1.2/s/stack over 6s.** The heal is the biggest number in the relic and it
is the school's.

# 4. THE BLADE DOES NOT MOVE

```
blade      body (A)     whole (D)
 24.03       7.6%       50.2 / 50.6%
 26.0       11.1%       53.2%
```

**The crossing is the type's own 24** — the first cell in the batch whose
blade is untouched. The build confirms on 151 and leaves it unless the band
misses.

**Type spread** (D): twinblade 67, greatsword 65, warhammer 52, flail 52,
scythe 40, **bow 28**. Worst **Farwarden 0%** (a ward bow: the ticks are
absorbed by the shield and the heal has nothing to feed on), Lastlight 20,
Gloamwire 20. Best Axiom 90, Spellbreaker 85, Thornshear 80. 39pp — item
12/32.

# 5. DECLARED

- **The light** is a disc of radius 100 centred on the HEAD (`f.headX/Y`),
  live while the window is open; a foe is lit when its centre is within
  100 + R.
- **A tick** every 0.4s while lit: `hurt(foe, 3, f)` (ward first; no crit,
  sunder, jitter, knock, hit stop, stagger or beat — Scour's rule) and
  `foe.apply("smite", 1, f)`; then `f.apply("blessing", 1, f)`. Blessing's
  tick heals through the engine's own `tickStatus` branch (line 8775).
- The head's own blow is untouched.
- Charge 16, window 8. Nothing waits.
- **The light is a picture that cannot be a white disc** (§6.1).

# 6. NAMES, CARD, PICTURE, SOUND

**MORNINGSTAR** — the flail's own name in the real world, and the dawn's
star. From: Morningstar, Lucent, Dayspring, Solace.
**ZENITH** — the sun at its height. From: Zenith, Radiance, Noontide, Halo.
**Card (69):** `The head becomes a sun: its light smites foes, and each burn heals it`

## 6.1 The picture — and the bloom rule comes first

- **The sun is a RING, not a disc.** Daybreak's corona was a `#FFFFFF`
  gradient under `lighter` on a 0.89-luma body and it ERASED the ball
  (§4.1b); the Harrowing's 398px white disc fogged the whole arena (§4.1c).
  So: the head is drawn as a small hot core (r ≤ 14, `glow #FFF3C4`-ish in
  sanctified's palette, source-over) and the LIGHT is a **ring at radius 100
  with the hole cut in the path** — a 10-unit band at alpha 0.35 — plus
  eight thin rays from the core to the ring that turn with the head's
  tumble. Interior alpha ≤ 0.05. `ult_bloom_probe` and `harrow_bloom_probe`
  gate stage 6: arena-mean lift from the chain **≤ +0.02** and the caster's
  disc never past 0.90.
- **The cast**: the head ignites over 0.25s — the ring expands from the
  head to 100.
- **A lit foe**: the smite tag counts up; a tick draws a brief spark-fall
  onto the foe (drawn, 4 sparks, no rng).
- **The heal**: a blessing tag on the caster, and a thin gold thread from
  the foe's tick point to the caster's shell for 0.15s — the "what it burns,
  heals" read, one line per tick.
- **Close**: the ring contracts into the head over 0.3s and the head cools.
- Silhouette: a sanctified flail — a faceted gold head on a pale haft,
  first cut. Field: ember motes drifting up off the ring, both copies.

## 6.2 The sound

- **Cast**: a bright swell, 0.5s, a rising fifth in a sustained-by-restrike
  tone — the sun coming up.
- **A tick**: a soft chime, 60ms, quiet (peak ≤0.35), pitch by smite count.
- **A heal**: Daybreak's spark-collect voice (`spark`, `collect:true`)
  already exists and already means "healed" — REUSE it, pitched by blessing
  count; do not write a second heal voice.
- **Close**: the swell reversed, quiet.

# 7. Open decisions

1. Rick's veto. The trail (59%) is the one-flag alternative if a sun on a
   chain reads wrong.
2. The blade stays at 24 unless the pinned runtime misses the band.
3. Farwarden 0% — a ward bow blanks a tick ultimate; item 12/32.
4. The bloom gate numbers (≤ +0.02 lift) are a floor from §4.1c's tables,
   not a measurement of THIS art — the build measures and may move them
   with the number written down.

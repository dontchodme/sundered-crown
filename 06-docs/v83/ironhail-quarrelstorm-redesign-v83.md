# v83 — IRONHAIL / QUARRELSTORM, REDESIGNED. Iron hail: bolts drop from the top of the hall onto the foe, and each one that lands sunders. The arrow nova was fourteen arrows once; the name of the relic is the ultimate.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0); claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Lab: `overlays/hail.js`; runs in `06-docs/v83/runs/`.

## Why
`kind:"volley"` — a nova of arrows, feed +5.3. Ironhail is the relic's name and nothing on it hails. Dwarven's verbs are iron, forge and wall; Breach uses the walls, Ironbloom the head; the ceiling is unused.

# 1. §1 (Cowork)
> For a duration iron falls. Every third of a second a bolt drops from the top of the hall onto where the enemy is, and lands a moment later; an enemy still standing there when it lands is struck and sundered. The bow keeps firing.

Two clauses: the hail (a drop every 0.4s at the foe's position, landing 0.3s later, hitting within 60 of the spot for 4); sunder +1 per landed bolt (**the feed**).

# 2. THE HARNESS, AND THE CONTROL
Ironhail as shipped on `sc-trunk`, Chromium 141. **SHIP 55.8% (330), A 39.4%.**

# 3. PRICED (`runs/hail_*`)
```
arm                                                      win    drops/cast  landed/cast  dmg/cast  sunder/cast
A   no ultimate                                         39.4%
SHIP the arrow nova                                     55.8%
B   fall 0.55s, hit r 40, 5 damage                      44.8%    9.9          2.0          9.9         —
C   B + sunder                                          48.5%    9.4          1.9          9.4        1.9
C   fall 0.3s, hit r 60, 6 damage                       70.0%   19.0          5.9         35.6        5.9
C   fall 0.3s, hit r 60, 4 damage  (taken)              61.5%   19.3          6.1         24.5        6.1
```
A bolt that takes 0.55s to fall lands on a ball that has left (20%); at 0.3s and a 60-unit splash, **6 of 19 land** and the foe takes ~6 sunder a cast. 61.5 against a shipped 55.8: the blade from 16.23 to about **15.3** (the bow row 9.5–16.2).

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND
- A drop every 0.4s of the window at `(foe.x, foe.y)`, landing at +0.3s; a landing pays `hurt(foe, 4, f)` (ward first, no crit/sunder-mul/knock/stop) and `foe.apply("sunder", 1, f)` if the foe's centre is within 60 + R. Drops in the air when the window closes still land. **No `rng`** — the drop point is the foe's position, deterministic.
- Names kept: IRONHAIL / QUARRELSTORM. **Card (74 → trim at build to ≤72; measure in pixels):** `Iron hail: bolts drop from above onto the foe; each one that lands sunders` — a 68-char alternate: `Iron hail falls on the foe from above; every bolt that lands sunders`.
- **Picture**: at each drop a small target rune on the floor at the foe's spot (dwarven `dark`, r 14) and a bolt streaking down from the top inset to it over 0.3s (drawn from time, no object state); on landing a dust-and-spark puff (drawn, 6 sparks, no rng) and the sunder tag ticks. Cast: the bow's limbs glow forge-orange for the window. Field: iron-spark motes on landings, both copies.
- **Sound**: cast — a forge-bellows huff, 0.4s; a landing — a short iron thud (≤0.15s), pitched by sunder count; a miss — a quieter thud; close — nothing.

# 5. BUILD BRIEF
Stage 0 control on 151 (`--arms A,SHIP,C --P fallT=0.3 hitR=60 dropDmg=4`). Stage 1 — nova out, `m.hail[]` in; gate: ~19 drops a cast, ~6 landed, ~24 damage, relic ~57% without sunder (run `--arms B --P fallT=0.3 hitR=60 dropDmg=4`). Stage 2 — the sunder; gate: sunder = landings; relic ~62%. Stage 3 — the blade, wide on 151 at 15 / 15.5 / 16 to the shipped rate; tip_audit. Stage 4 — picture, voice, carry; nova's field spec out; `engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched.

# 6. Open decisions
1. Rick's veto. 2. The blade target. 3. Whether the hail should also fall on the CASTER's own path (it does not — the sky knows its master; Consecration's rule).

# v78 — CENSER / CONSECRATION, REDESIGNED. Every blow consecrates the ground it lands on: a foe on holy ground is smitten, and Censer is healed there. The nova with three Smite was a burst; a censer spreads.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0);
claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Lab:
`overlays/holyground.js`; runs in `06-docs/v78/runs/`.

## Why

`kind:"nova"`, 12 damage, 3 Smite, knock — feed +5.3. A censer is swung to
spread incense over ground; the hammer that carries the name never touched
the floor. Sanctified's verbs are LIGHT and HEAL and the school has no
ground hazard (Breach's vents and Deadfall's sigils are dwarven and umbral).

# 1. §1 (Cowork)

> For a duration every blow the hammer lands consecrates the ground where
> it landed: a circle of holy ground that lasts. An enemy standing on holy
> ground is smitten for as long as it stands there. Censer standing on holy
> ground is healed.

Three clauses: the ground (a disc r 90 at each blow's landing point, 8s
life); the smite (**the feed**, +1 every 0.5s on the ground); the heal
(blessing +1 a second while Censer stands on it).

# 2. THE HARNESS, AND THE CONTROL

Censer as shipped on `sc-trunk`, Chromium 141. **SHIP 50.3% (330), A
38.5%.**

# 3. PRICED (`runs/holyground_*`)

```
arm                                              win    discs/cast  foe on ground  ticks/cast  bless/cast
A   no ultimate                                 38.5%
SHIP the nova                                   50.3%
B   smite + 2 damage a tick                     54.2%    1.3          19%           3.9          —
C   + the heal                                  65.5%    1.3          20%           4.0         2.6
D   + discs planted under the caster too        84.5%    6.6          48%           8.9         6.9
C   r 70, 1 damage                              61.5%
C   r 90, NO damage  (taken)                    57.9%    1.3          20%           4.1         2.6
```

The hammer lands 1.3 blows a window, so holy ground is a disc or two — and
that is right for a censer swung slowly. Discs under the caster's own feet
(D) make it a field relic at 85% and are not taken. **The tick's damage is
dropped**: holy ground smites the unholy and heals the faithful and does
nothing else, and at 57.9% against a shipped 50.3 the blade comes from
28.77 to about **26.5** (the hammer row 20–29).

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND

- A blow's landing point is the FOE's position at the hit; the disc lives
  8s and does not move; the hall's close does not clip it (holy ground
  under a closed wall is simply unreachable).
- On the ground: `foe.apply("smite", 1, f)` every 0.5s; `f.apply("blessing",
  1, f)` every 1.0s while the caster's centre is within a disc. No damage,
  no knock, no beat.
- Names kept: CENSER / CONSECRATION. **Card (70):** `Its blows make holy
  ground: foes on it are smitten, and it heals there`.
- **Picture**: a disc of pale gold on the floor (sanctified `glow` at alpha
  0.18, a brighter rim, a faint cross-hatch of light inside — source-over,
  no `lighter`: this is FLOOR, the bloom must not read it); it blooms out
  from the impact point over 0.3s and fades over the last second of its
  life. A foe on it carries the smite tag; Censer on it carries the
  blessing tag and a soft up-drift of motes. Cast: the hammer head lights
  (a hot core, not a white one — §4.1b). Field: incense motes rising from
  each disc, both copies.
- **Sound**: cast — a thurible swing (a chain-rattle into a low bell,
  0.5s); a disc opening — a soft bell tone, pitch by disc count; the smite
  tick — nothing new (smite's own); the heal — the `spark collect` voice,
  reused.

# 5. BUILD BRIEF

Stage 0 control on 151 (`--arms A,SHIP,C --P tickDmg=0`). Stage 1 — nova
out, `m.holyGround[]` in (discs with `x, y, t0`), the tests; gate: ~1.3
discs a cast, foe on ground ~20% of window frames, ~4 smite a cast, relic
~54% at 28.77 (arm B without damage — reproduce with `--arms B --P
tickDmg=0`). Stage 2 — the heal; gate: ~2.6 blessing a cast, relic ~58%.
Stage 3 — the blade, wide on 151 at 26 / 26.5 / 27 to the shipped rate;
tip_audit. Stage 4 — picture, voice, carry; bloom measured (a floor disc
must add ≤ +0.01 arena-mean lift); nova's field spec out; `engine_ab`,
`shell_identity`, `render_ab`, `chain_audit`, one fight watched.

# 6. Open decisions

1. Rick's veto. 2. The blade target. 3. Discs under the caster's own feet
(D, 85%) is the one-flag "field" version if a censer that only marks its
blows reads too sparse.

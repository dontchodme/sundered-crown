# v86 — DAWNBRINGER / DAYBREAK, REDESIGNED. The sun rises up the hall: a line of light climbs from the floor over the window, and everything below it is in the dawn. Rick's first relic; its sparks were the school's first light and the first bloom fight.

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0); claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file — this one above all.** Lab: `overlays/dawn.js`; runs in `06-docs/v86/runs/`.

## Why
`kind:"radiant"` — for 5s its hits spray sparks, 5 damage to foes, healing when collected. Feed −4.8, and the corona that erased the ball (CLAUDE.md §4.1b). It is the only ultimate on the roster whose name is a TIME OF DAY, and nothing on screen was a dawn.

# 1. §1 (Cowork)
> For a duration the sun rises. A line of light climbs the hall from the floor to the top over the whole duration, and everything below the line is in the dawn: an enemy standing in it is smitten and burned for as long as it stays there.

Two clauses: the dawn line (y from the floor to the ceiling over 8s — a horizontal line, everything below lit); smite +1 and 2 damage every 0.5s to a lit foe (**the feed**). The heal is a flag (§3).

# 2. THE HARNESS, AND THE CONTROL
Dawnbringer as shipped on `sc-trunk`, Chromium 141. **SHIP 57.0% (330), A 13.6% — Daybreak is +43, the second-strongest shipped ultimate on the list.**

# 3. PRICED (`runs/dawn_*`)
```
arm                                                   win    casts  foe lit (window)  ticks/cast  dmg/cast  bless/cast
A   no ultimate                                      13.6%
SHIP the sparks                                      57.0%
B   the dawn: smite + 2 a tick  (taken)              54.8%   3.34     61%             10.0        20.0        —
C   + blessing every 1s while Dawnbringer is lit     80.9%   3.55     60%              9.9        19.9       5.7
C   blessing every 3s                                71.8%
C   blessing every 2s, only while the foe is lit     71.5%
```
The foe is below the dawn line **61%** of the window — the line starts at the floor where the balls spend most of the fight and climbs past them — for 10 ticks a cast. **B is at parity with the sparks (54.8 against 57.0) with the blade untouched at 10.4.** Every heal variant is +17 or more and would take the blade under the row; not taken, and it is Rick's flag: *"healing when collected"* was his sentence.

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND
- The line: `lineY = H − k·H`, `k = (t − t0) / dur` (floor at cast, ceiling at close). Lit = `foe.y > lineY`. Every 0.5s while lit: `foe.apply("smite", 1, f)` and `hurt(foe, 2, f)` (ward first, nothing else, no beat). The caster gets nothing (B).
- Names kept: DAWNBRINGER / DAYBREAK. **Card (72):** `The sun rises up the hall: foes below the dawn line are smitten and burn`.
- **Picture — and §4.1b/c govern it**: the lit region is a WASH, not a light source — sanctified `glow` at alpha 0.10 below the line, source-over, NOTHING under `lighter`; the line itself is a 4-unit band at alpha 0.6 with a soft 12-unit gradient above it (the horizon); the ball is not touched by any of it (the Daybreak corona is gone). A lit foe carries the smite tag and a faint upward mote drift. Cast: the line appears at the floor with a 0.3s brightening. Close: the line reaches the top and the wash fades over 0.5s. **Bloom gate: arena-mean lift ≤ +0.02 with the whole hall lit at 7.9s** — measured; a wash over the full arena is exactly the Harrowing's failure shape (§4.1c).
- **Sound**: cast — a slow swell rising over the whole 8s (re-struck tones stepping up a scale, one per second — the only voice in the roster tied to the window's clock); a tick — nothing new (smite's); close — the top note held and released.

# 5. BUILD BRIEF
Stage 0 control on 151 (`--arms A,SHIP,B`). Stage 1 — sparks out (`_burst` and the corona), `f.ultDawn` in; gate: foe lit ~61%, ~10 ticks a cast, ~20 damage, relic ~55% at 10.4 (parity with SHIP ±3). Stage 2 — the blade: confirm 10.4 wide on 151. Stage 3 — picture (bloom measured — this is the relic that started §4.1b), voice, carry; sparks' field spec out; `engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched.

# 6. Open decisions
1. **Rick's veto — his first relic.** 2. The heal: one flag, +17, and a blade under the row; his. 3. Line speed — the floor-to-ceiling rise in 8s means the last second lights the whole hall; a rise to 80% of the height instead is one number.

# 7. Ruled at build time (recorded by Claude Code, not designed)
**Rick, 2026-09-26:** no vetoes, build all nineteen, and **CHARGE 16** (the window, 8, is stated above). This doc did not state the charge, and 16 is what every run in `runs/` was priced at (`P` in each json). Items 2 and 3 are built as written, with no heal and the full floor-to-ceiling rise, unless Rick flags otherwise before this build starts.

**Rick, 2026-09-27, for the whole batch: THE CHARGE IS THE GAME'S EQUIVALENT — 14.** The lab's 16 counted hit-stop freezes; the engine charges only in unfrozen time. At 16 the built Daybreak read 48.3% (10 under the sparks, 5 under this doc's arm B on 151); at 14 it reads 52.5% against arm B's 53.5%, the blade untouched at 10.4 (v97).

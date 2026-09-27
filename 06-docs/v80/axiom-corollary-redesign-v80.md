# v80 — AXIOM / COROLLARY, REDESIGNED. Every blow is followed by its corollary: the same blow again, half a second later, wherever the foe is — and it hexes. The bolt was Unmaking with a different number; the name always meant "what follows".

**DESIGNED — Cowork, 2026-09-26. Build from §5; do not design (rule 0); claimed in `06-docs/CLAIMS.md`. Rick vetoes from this file.** Lab: `overlays/corollary.js`; runs in `06-docs/v80/runs/`.

## Why
`kind:"bolt"`, 18 damage, 3 Hex — Unmaking's twin. Feed +14.9 (the three hex). A corollary is what follows from what was already shown: a blow that lands lands again.

# 1. §1 (Cowork)
> For a duration every blow Axiom lands is followed by its corollary: half a second later a rune-echo of the same blow strikes the enemy again, for the same damage, wherever it has got to — as long as it is still within reach of the sword — and the echo hexes.

Two clauses: the echo (a queued strike at +0.5s, 1.0 × the blow's damage, through the ward, landing if the foe is within 200 + R of Axiom); +1 hex on each echo (**the feed**).

# 2. THE HARNESS, AND THE CONTROL
Axiom as shipped on `sc-trunk`, Chromium 141. **SHIP 39.7% (660), A 20.0%.**

# 3. PRICED (`runs/corollary_*`)
```
arm                                        win (660)   echoes/cast  landed/cast  echo dmg/cast  hex/cast
A   no ultimate                            20.0%
SHIP the bolt                              39.7%
B   echo at 0.5 x, no hex (330)            23.3%        2.75         1.74          12.5          —
C   echo at 0.5 x + hex (330)              33.3%        2.84         1.80          13.0         1.8
C   echo at 1.0 x + hex  (taken)           37.6%        2.73         1.73          24.5         1.7
```
Axiom lands 2.7 blows a window and 63% of the echoes find the foe still in reach. **At a full echo the redesign is at parity with the bolt (37.6 against 39.7, inside noise) with the blade untouched at 7.42** — the lightest blade in the game stays where it is. The hex is +10 of it.

# 4. DECLARED, NAMES, CARD, PICTURE, SOUND
- On a blow landed inside the window, queue `{at: t + 0.5, dmg: the blow's damage as dealt}`; at `at`, if both alive and the foe within 200 + R: `hurt(foe, dmg, f)` (ward first; **no crit, no sunder multiplier, no knock, no hit stop** — the echo is a rune, not a swing) and `foe.apply("hex", 1, f)`. **The echo files a `hit` beat** — a second strike on the same number is a moment the director should see. A queued echo past the window still lands (it was earned).
- Names kept: AXIOM / COROLLARY. **Card (68):** `Every blow is followed by its corollary: the same blow again, hexing`.
- **Picture**: the bolt art is retired. On a landed blow a rune is stamped on the foe at the hit point (runic `core`, r 12); at +0.5s it FLARES and a ghost of Axiom's blade sweeps through the foe from the same bearing the blow came from (drawn, 0.15s, alpha 0.5); the number floats in runic `glow`. Cast: the blade's edge lights with a rune line. Field: rune motes on each echo, both copies.
- **Sound**: cast — a rune-chime, 0.3s; the echo — the sword's own strike voice, reversed (a rising "whoom"), quieter; the hex — its snap.

# 5. BUILD BRIEF
Stage 0 control on 151 (`--arms A,SHIP,C --P echoMul=1.0 --seeds 20`). Stage 1 — bolt out, `f.ultEcho` queue in; gate: echoes = blows in windows, ~63% landed, ~24 echo damage a cast, relic ~28% at 7.42 without hex (run `--arms B --P echoMul=1.0`). Stage 2 — the hex; gate: hex = echoes landed; relic ~38%. Stage 3 — the blade: confirm 7.42 wide on 151 (parity); tip_audit. Stage 4 — picture, voice, carry, the echo beat; bolt's field spec out; `engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched.

# 6. Open decisions
1. Rick's veto. 2. Echo reach 200 — a foe knocked out of reach by the blow itself escapes the corollary 37% of the time; that is the type's own knock and a lever if wanted. 3. Whether the echo should carry the blow's crit (it does not).

# 7. Ruled at build time (recorded by Claude Code, not designed)
**Rick, 2026-09-26:** no vetoes, build all nineteen, and **CHARGE 16, WINDOW 8**. This doc stated neither, and those are the numbers every run in `runs/` was priced at (`P` in each json). The other open items are built as written: reach 200 (item 2); the echo does NOT carry the blow's crit (item 3, and §4 "no crit"); a queued echo past the window still lands (§4). `overlays/corollary.js` differs from the prose on the last two (it copies `me.dealt`, crit included, and drops the queue at window close), so the build's gates read against a lab run of the prose reading, made on 151.

**Rick, 2026-09-26, at stage 3: THE BLADE STAYS 7.42.** Built, the relic does not hold parity with the bolt on 151. The lab's fixed cast schedule gave the echo ~15% more windows than the engine's charge clock does, and its SHIP arm already ran on the engine's clock. Measured at 1320 fights a point on two seed blocks: bolt 40.2%, Corollary at 7.42 34.1% (34.9% after the review fixes), 7.9 38.6%, 8.4 39.8%, 8.9 45.5%. Asked "as strong as today, or weapon damage unchanged", he kept the blade (v88 §4). Also found at build time, and built as this doc writes it rather than as the lab ran it: the echo's target is the foe (§4 `hurt(foe, …)`), so a blow on a Twinshade shade echoes onto Twinshade.

**Rick, 2026-09-27, for the whole batch: THE CHARGE IS THE GAME'S EQUIVALENT — 14.** The lab's 16 counted hit-stop freezes (the harness's step clock); the engine charges only in unfrozen time, so an engine charge of 16 gave ~15% fewer casts than this doc was priced with. At 14 the built Corollary reads 40.0% against the bolt's 40.2%: the parity this doc priced, with the blade Rick kept at 7.42. Built as corollary_build stage 6 (v88 §8).

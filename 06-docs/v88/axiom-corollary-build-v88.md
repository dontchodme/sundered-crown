# v88 — AXIOM / COROLLARY, BUILD. STAGES 1-3 DONE (sim built, blade kept at 7.42); STAGE 4 (picture, voice, beat, field) IN PROGRESS. Claude Code has it.

Claude Code on **DESKTOP-DERRAFT**, claimed 2026-09-26 22:35 UTC (`CLAIMS.md`, the BUILD
row under Corollary's). The input is `06-docs/v80/axiom-corollary-redesign-v80.md` §5 with
its §7 rulings, and nothing else (rule 0). Builder `tools/corollary_build.py`, probe
`tools/corollary_probe.py`, the prose-reading lab `tools/overlays/corollary_prose.js`. Runs in
`runs/`. This doc is written as the build goes.

```
sc-leaf.html          the base: the build of record since Rick passed its gate 4 (2026-09-26)
  -> sc-echo.html       stage 1  the echo, no hex     corollary_build --stage 1   96ec0dee4aa16031
  -> sc-corollary.html  stage 2  the echo hexes       corollary_build --stage 2   71d414dc0b098485 (one character)
                        stage 3  the blade            7.42 KEPT, Rick's ruling -- no link
```

**The app pointer has not moved** (`app/main.js` reads `sc-leaf`). It moves after stage 4,
when Rick has seen the clip.

## 0. What this build stands on

**The base is `sc-leaf`**, named and asserted by the builder (Starwarden, Crossweave's
nova, and the Winnowing's `s.over.stop = 0.02 * s.rung`). The v68–v86 batch was priced on
`sc-trunk`; `sc-leaf` differs only in Thornshear's kunai, which reaches one of Axiom's 33
pairings.

**Rick's rulings for this build** (v80 §7): charge 16 and window 8, the numbers it was
priced at (the doc stated neither). At stage 3 he kept the blade at 7.42 over parity with
the bolt (§4 below).

**Three places where the doc and its lab part. The doc is built** (rule 0: the doc is the
input). All three are in `corollary_build.py`'s docstring and in v80 §7:
1. *"A queued echo past the window still lands (it was earned)"* (§4). The lab clears its
   queue at the close.
2. *"no crit"* (§4) and *"(it does not)"* (§6.3). The lab copies `me.dealt`, crit included.
   The build takes EXACTLY the crit's extra back out: the echo is `dmg - (dmgBase -
   dmgNoCrit)`, never below zero, where `dmgNoCrit` is the same blow rounded before the
   multiply (a new const in `resolveHit`, read by nothing else).
3. *`hurt(foe, dmg, f)` and "the foe within 200 + R of Axiom"* (§4). The echo always
   strikes the FOE, Axiom's opponent, which is also what the lab does. A blow on one of
   Twinshade's shades echoes onto Twinshade.

**And one difference that is the engine's convention, not a reading.** The window, the
half second and the charge run on the window tickers' clock, which stops through a hit stop
exactly as `tickWinnow`'s and `tickCharge`'s do. The lab counted every step, freezes
included. Consequences: the built Axiom casts ~3.5 times a fight where the lab's fixed
schedule gave ~4.2, and an echo lands 0.5s of FIGHT after its blow, which is a median 0.675s
on the match clock (the blow's own hit stop always falls inside the half second).

**THE RUNTIME IS PROVED, on this PC, before any number below** (Chromium 151.0.7922.34,
playwright 1.62.0, Python 3.13.15):
- seed 25064 Paradox v Heartwood on the v43-era build reproduces `docs/RUNTIME-DRIFT.md`'s
  151 line exactly: Paradox, hp 17, 46.41s, 17 clanks. **A +1 ULP `Math.pow` flips it** to
  Heartwood 44 / 45.5s, so the check can fail.
- `shell_identity` 200/200 on sc-trunk against yert's committed app json, then 200/200 on
  sc-leaf after `npm run identity` here.
- **engine_ab sc-trunk → sc-leaf, 33 others, n=8: 4224/4224** (`runs/engine_ab_trunk_to_leaf_33.txt`)
  and **verify on sc-leaf 10/13** with the known Axiom-vs-Thornshear red and the two clock
  bands (`runs/verify_leaf.txt`): v67's numbers, both reproduced here.

## 1. Stage 0: the control on 151, on sc-leaf

`ult_overlay.py --game ../02-chain/sc-leaf.html --relic axiom --mech overlays/corollary.js
--P echoMul=1.0 --seeds 20` (33 foes × 20 seeds = 660 fights an arm; seed0 2207 as published,
2317 for the second block).

```
arm                                  published 141 (660)   151 on sc-leaf        echoes  landed  echo dmg / cast
A     no ultimate                    20.0%                 18.9%
SHIP  the bolt                       39.7%                 41.1 / 39.2 -> 40.2   (1320)
C     the lab as written, hex        37.6%                 37.3%                 2.73    1.73    24.35   (pub. 2.73 1.73 24.47)
```

The control reproduces: every mechanical column to the digit, and the win rates inside the
batch's tier (v87 :42, under ~5pp at 660 is not a difference).

**The gates read against the doc's reading, not the lab's**, so the lab was also run with
readings 1 and 2 (`overlays/corollary_prose.js`, the lab with exactly those two changes;
reading 3 is the lab's own behaviour already):

```
arm                               block 1   block 2   pooled (1320)   blows  echoes  landed  echo dmg  late / cast
B   the prose reading, no hex      32.1      32.3      32.2           2.87   2.85    1.80    22.82     0.16
C   the prose reading, hex         37.6      36.1      36.8           2.95   2.94    1.85    23.48     0.18
```

**The design's stage-1 reference "relic ~28% at 7.42 without hex" has no run behind it**
(no B arm at echoMul 1.0 in `v80/runs/`). On 151 the arm it names reads 32.2%, and per v87
:40 the gate reads against the 151 run.

## 2. Stage 1: the echo, no hex — `sc-echo.html`

`corollary_build.py --stage 1 --src ../02-chain/sc-leaf.html --out ../02-chain/sc-echo.html`:
src `65afa5222caf2084` (the LF text of the committed sc-leaf; the file's own CRLF bytes hash
`f571ae583407971a`), out `96ec0dee4aa16031`, +6505 characters, written LF. Seven anchored
edits:
- Axiom's ult block (`kind:"echo"`, charge 16, dur 8, delay 0.5, reach 200, hex 0, the doc's
  68-character card);
- `ultEcho`/`echoTally` on the fighter;
- the `kind === "echo"` cast branch, which opens the window, resolves nothing and returns;
- `dmgNoCrit` beside the crit multiply in `resolveHit`;
- the queue beside `self.hits++` in `resolveHit`;
- `tickEcho` with the other window tickers, before `tickHits`;
- `tickEcho` itself: `hurt` only, and the number floated in the runic glow.

**No insert draws the match RNG itself**, and the builder refuses if one does. What an echo
does reach through `hurt` is the WARD's rule: an echo that empties a ward shatters it, and
the shatter throws 40 sparks off the stream (120 draws), sets its 0.10 stop and knocks the
attacker, exactly as for any other damage that breaks a ward. That is deterministic, and it
is what v80 §4's "ward first" asks for.

**The bolt is gone for Axiom only.** `kind:"bolt"` is still Spellbreaker's Unmaking, and no
line of that code moved. Axiom's bolt ART (the construction lines and the proof, keyed on
`u.w === "axiom"`) and its `SPECS.axiom` beam field still play at the cast in stages 1-3;
stage 4 retires them.

**Probe, `corollary_probe.py --game ../02-chain/sc-echo.html`: 10/10** (`runs/probe_stage1.txt`;
396 fights, Axiom on both sides, all 33 foes). Per cast: blows 3.24, echoes 3.16, landed 1.92
(60.7%), echo damage 22.3, crit blows 0.28; 286 late echoes resolved and 177 landed; 69 blows
on a Twinshade shade, all echoed onto Twinshade; 119 wards broken by an echo. Check [2]
rebuilds each crit blow's uncritted value from the blow's own captured crit and jitter draws,
so an off-by-one fails it. Check [5] allows a freeze inside `tickEcho` only in a tick where a
ward broke.

**The relic at 7.42, same (foe, seed) sets as stage 0: 32.4 / 30.3, pooled 31.4%**
(`runs/built_echo_*`), against the prose lab's arm B at 32.2%. In tier.

## 3. Stage 2: the hex — `sc-corollary.html`

`corollary_build.py --stage 2`: out `71d414dc0b098485`. The diff against `sc-echo` is one
character (`hex:0` → `hex:1`); the hex path was written at stage 1 and ran at zero.

**Probe `--hex`: 10/10** (`runs/probe_stage2.txt`). Hex applied = echoes landed, 1.91 a cast.

**The relic at 7.42: 34.2 / 35.6, pooled 34.9%** (`runs/built_corollary_*`), against the prose
lab's arm C at 36.8%. In tier (-1.9). It runs a little under the lab for the clock reason in
§0: fewer casts.

**engine_ab sc-leaf → sc-corollary** (one run across both stages, the Starwarden precedent):
- **the 33 others, n=8: 4224/4224 identical** (`runs/engine_ab_leaf_to_corollary_33.txt`).
  That includes `dmgNoCrit` in every relic's `resolveHit`.
- **Axiom with 8 others, n=8: 64 of 288 differ**, which is exactly Axiom's 8 pairings × 8
  seeds and is the pass.

**verify --n 40 on sc-corollary: 11/13** (`runs/verify_corollary.txt`). The two reds are the
known clock bands (the pairing ceiling, 98.4s Farwarden/Starwarden, and the overall mean,
60.8s). **Axiom vs Thornshear 0/40 is gone**: "both sides can win every matchup" passes
again. Every relic is in 30-70%. **Axiom is 33.5%, now the lowest in the roster and inside
the band** (it was 38.4% on sc-leaf). That is the cost Rick accepted at stage 3. The spread
is 30.6pp.

**tip_audit: 1 effect field the tips never mention**, the same as sc-leaf (the ward's bank).
Nothing new.

**chain_audit `--builder corollary_build.py --relic ../02-chain/sc-corollary.html --tip
../02-chain/sc-corollary.html`: ALL 8 INSERTS SURVIVE.** This is meaningful only after this
build's fix to `chain_audit.py` (§5).

## 4. Stage 3: the blade — 7.42 KEPT (Rick), parity not held

v80 §5: "confirm 7.42 wide on 151 (parity)". Measured against the shipped bolt, which the
harness runs on the engine's own charge (arm SHIP), on the same (foe, seed) sets, two blocks,
**on the first build of stages 1-2** (before the review fixes in §5, which moved the 7.42
point from 34.1 to 34.9):

```
                                  block 1   block 2   pooled (1320)
SHIP  the shipped bolt, sc-leaf    41.1      39.2      40.2
Corollary at 7.42                  33.3      34.8      34.1     -6.1
          at 7.9                   38.5      38.6      38.6
          at 8.4                   39.7      40.0      39.8
          at 8.65                  40.5       -        40.5   (660)
          at 8.9                   45.8      45.3      45.5
```

**At 7.42 the built Corollary is 6.1 under the bolt it replaces.** That is outside the tier,
about three standard errors. Parity sits at about 8.4-8.65. The design's parity (37.6 against
39.7) was priced in a lab whose fixed cast schedule gave the echo ~15% more windows than the
engine does, while its SHIP arm already ran on the engine's clock. The build removes that
advantage.

v80 said both "at parity with the bolt" and "the blade untouched at 7.42", and on 151 those
two no longer hold together. **Rick was asked and kept 7.42** (2026-09-26). Axiom ships
weaker than it does today, at 33.5% in verify, inside the band and at the bottom of it.

## 5. What the review found, and what changed

Three independent reviewers (doc fidelity, engine interactions, zero burden) read the first
build of stages 1-2. Every finding below was fixed before this commit, and the links were
rebuilt from scratch:
1. **An echo could land on a Twinshade shade that had already rejoined.** `dropSplit` removes
   a shade with hp > 0, so `alive` stays true. The echo hurt and hexed an orphan and floated
   its number over empty floor. Reproduced on 5 seeds by two reviewers. The fight was
   unaffected (identical traces with those echoes dropped).
2. **The echo targeted the body the blow landed on.** The doc's `hurt(foe, …)` and the lab
   both use the foe. Fixed by reading 3 in §0, which also removes finding 1 at its root.
3. **Stripping the crit as `round(dmg / critMul)` was off by one on ~1 crit echo in 8**, and
   wrong when an Aegis ate part of a crit. Fixed with `dmgNoCrit`, and probe [2] made exact.
4. **`chain_audit` could not fail on this build.** Its markers were comment prose (this
   codebase writes block comments with no leading `*`), and its one-line placeholder rows were
   skipped. A tip with the ultimate reverted to the bolt, the ticker call deleted and the queue
   disabled printed "ALL 5 INSERTS SURVIVE".
   **Fixed in `tools/chain_audit.py`**: a marker is now a line the insert ADDS (never a line
   already in its anchor), CODE first and comment text only as a fallback, and `main` takes the
   first candidate the relic build actually contains. Checked five ways:
   - Corollary: 8/8.
   - the reverted-ultimate tip: 2 LOST.
   - the deleted-ticker tip: 1 LOST.
   - Starwarden: 37/37 (was 35, 2 unresolved).
   - Gloamwire: 23/23 (was 21) and Winnow 2/2, with the fallback-to-comment inserts named.
5. **Two claims were wrong** and are corrected here: "tickEcho draws no RNG" (the ward's
   shatter does, above), and "src, the committed sc-leaf, byte for byte" (it is the LF text's
   hash).
6. **For stage 4:** a fatal echo files no beat yet. 3 of 7 Axiom wins in one 12-fight sample
   ended on an echo with no KILL cut (axiom v twinshade seed 4101 at 85.23s). v80 §4's echo
   beat is stage 4's; until it lands, no clip is cut from sc-echo or sc-corollary.

## 6. Stage 4 (in progress)

Rick, 2026-09-26: **"you pick i overrule"**. Code makes the picture and sound choices v80 §4
leaves open, picked on measurements, and sends one clip; Rick changes what he wants. The picks
and the numbers behind them go here.

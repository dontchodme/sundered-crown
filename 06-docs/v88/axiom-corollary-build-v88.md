# v88 — AXIOM / COROLLARY, BUILD. STAGES 1-4 BUILT AND GATED; THE CLIP IS WITH RICK ("you pick i overrule"). The app pointer waits on him.

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
  -> sc-corollary-fx.html stage 4 picture, voice, beat, field   corollary_build --stage 4   4f6f503cec8072ca
```

**The app pointer has not moved** (`app/main.js` reads `sc-leaf`). It moves when Rick has seen
the stage-4 clip and has nothing to overrule.

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

### 6a. The plumbing (Code's, not art)

`corollary_build.py --stage 4` does these things:
- **Retires the bolt's art** as two whole spans: drawUltUnder's construction lines (22 lines)
  and drawUltOver's proof (42 lines). It asserts that nothing in the output keys on
  `u.w === "axiom"`.
- **Swaps the field spec in both copies** (`sync_fx`, cindercleave's pattern): `axiom` (the
  bolt's beam) out, `'axiom-echo'` in, the whole inlined module compared to `src/render/fx.js`
  before and after, and both stamps re-cut.
- **Routes every echo through one new method, `echoShown(f, tgt, q, landed)`.** It is called
  for a landed echo and for one that found the foe out of reach. Everything it does is
  write-only:
  - **the beat:** one `hit` beat per landed echo with the number `hurt` was handed,
    `fatal: true` when it kills, and `echo: true`;
  - **the kill's flash:** `finisher` on a fatal echo, not `killStop` (v80: "no hit stop");
  - **the rune motes:** armed on `m.ultFx` ONLY when the slot is free or already Axiom's, so
    they never erase the opponent's set-piece (open item 25);
  - the voices and the picture's record (6b, 6c).

**Checked on a plumbing-only build** (voices and picture empty):
- engine_ab sc-corollary → it, **all 34 relics WITH Axiom, n=4: 2244/2244 identical**. That
  proves presentation only.
- corollary_probe 11/11. New check **[11]: one hit beat per landed echo, fatal iff it killed,
  none for a miss** (2728 beats, 37 fatal).

**What the director does with a fatal echo is its own policy, and it is left alone.** A kill
cut needs the fatal beat to clear `CINE.floor` 1.90 like any cut. `cineScore` prices a kill on
closing speed, pace and the winner's remaining hp. On Axiom v Twinshade over seeds 4090-4129
(plumbing build), the 5 fights won on an ECHO score 1.14-1.67, and the 35 won on an ordinary
blow score 0.53-2.09, **of which only 2 clear the floor**. The echo's beat carries honest
kinematics, the same fields the Aegis return and Scour file, and it scores like a blow. So
seed 4101, which ends on an echo, still has no KILL cut: neither would most blow kills in this
pairing. The fight now HAS its killing beat (rule 3), and whether the director films it is
the director's tuning, not this build's.

### 6b. The voices (picked on the numbers; `tools/corollary_voice_lab.py`)

Every render runs through `Sfx.buildChain` in an OfflineAudioContext, scheduled at t=1.0,
with render.py's deterministic noise, and is judged on the worst of 12 noise draws. "Audible" =
first to last 5 ms RMS window above 2% of the voice's own loudest. The controls reproduce the
stage-4 smoke: rune-crack 0.608 / 450 ms; hit at dmg 11.6 (the mean echo) 0.443 / 80 ms.
- **Cast — "a rune-chime, 0.3s": BAR** (of four). One struck bar: modes 1 : 2.76 : 5.40 on
  1319 Hz, a 20 ms mallet tick and a body an octave under. Audible 300 ms, peak 0.364 at 7 ms,
  register 0.35 against rune-crack. It is a new `w === "axiom"` arm placed BEFORE the shared
  rune-crack fallback, which ten other relics still use unchanged. Runner-up NOTE.
- **Echo — "the sword's own strike voice, reversed (a rising whoom), quieter": MIRROR** (of
  five). The `hit` voice's own numbers at the echo's damage, run backwards: its sine RISES
  46 Hz → the hit's pitch while it swells, peaking 130-171 ms after landing (the 0.15s ghost).
  A literal buffer reversal is impossible here: it needs an async render, and every clip
  rebuilds the synth synchronously, so it would be SILENT in every clip. So the swell is built
  from `_tone` re-struck at the chirp's own cycle starts, which sum to one rising sine. Measured
  register 0.98 against the hit (the literal reversal: 1.00), energy centre late (0.60), and
  **-6 dB under the hit** (short-term 0.47-0.53 of it) at every damage from p1 to p99, because
  it scales with the echo's dmg as the hit scales with a blow's. Runner-up RESTRIKE.
- **Hex — "its snap": SNAP** (of five). **No hex voice existed anywhere** (v79 and v75 also
  assume one), so this is a new top-level `kind: "hex-snap"`, the runic SCHOOL's voice, ready
  for Spellbreaker and Oracle. A finger-snap band (2.6 kHz, 22 ms) on a 1.3 kHz body: audible
  25 ms, rise under 1 ms, centroid 3.35 kHz (two octaves under the wall tick, the commonest
  sound in a fight), level between 3x the wall tick and the hit on every draw. It plays on
  the echo's hex application only, on the same frame as the echo voice. Runner-up CRACK.
- Calls live in `echoShown` (one echo voice per landed echo, a snap when the echo hexes), with
  plain-number opts. `SFX.play` is a no-op headless and draws nothing, so the voices cannot move
  a fight. The 19 reference renders are in `05-reference/v88/*.wav`, which is gitignored with
  every wav (the lab rebuilds them in ~3 minutes).

### 6c. The picture (picked on the numbers; `05-reference/v88/corollary-picture-sheet.png`)

Measured on real fights, 540x960, post chain on: legibility is mean |dL| over the mark's own
footprint, from two frames that differ only in the mark. It was taken on a RUNIC foe
(Spellbreaker, the same hue), a WHITE sanctified foe (Aureole) and an ordinary one
(Grudgebearer).
- **The rune: a triangle in a ring** (the charge sigil's own figure; `_glyph` is Unmaking's and
  would stamp one mark for two ultimates). r 12, **separated by VALUE**: the school-dark outline
  under a core stroke, not `lighter` (lighter measured a quarter of the legibility on white).
  **Seated at 20 from the foe's centre**, not the exact hit point, which sits on the rim (median
  39 against ballR 34): 1.54x the legibility on white.
- **Pending: a clock runs round it** for the half second, so the flare lands as the ring closes.
- **The flare: "leave"** — it expands, whitens and goes (0.25s): 0.235 / 0.069 / 0.261,
  against 0.08 for a plain ring.
- **The ghost: the real blade through `litWeapon` at alpha 0.5**, in the WORLD pass, drawn over
  both fighters (drawn with them, the foe's shell clips it exactly where it goes through). Its
  pivot is a virtual Axiom on the blow's bearing and distance, sweeping a 0.75 half-arc in the
  blow's own swing direction, which is the smallest arc that goes through the foe every time
  over 21 real blows.
- **A miss** (out of reach): the triangle goes and the ring breaks into three arcs that part and
  drop — no flare, no ghost, no number. It reads as the rune failing, not the picture failing.
- **The cast: ten rune marks along one inset edge of the blade, held for the window** and fading
  0.45s after it (Breach's precedent). Once the bolt art is gone, this is the window's only tell.
- **The motes: `'axiom-echo'` burst, n 200, births spread over 0.25s**, so the field peaks after
  the ghost has gone. **Bloom** stays under the batch's only floor (Morningstar's: arena lift
  ≤ +0.02, disc ≤ 0.90). The flare peaks at lift +0.0046 and whitens a white foe's disc to 0.69
  for 0.25s.
- **Frame cost (RTX 3070, Electron 44, 453x805, chain on):** the ghost is one more greatsword
  draw, 3.1-3.9 ms, the same as Axiom's own blade. The peak echo frame is ~4.6 ms against 4.77
  of headroom, which is why the motes spread their births.
- Presentation only: no rng, no spawnFx, no Math.random, and nothing the sim reads. The picture
  lab confirmed 6 whole fights field-for-field identical with the picture in.

### 6d. Stage 4's gates — every one able to fail

`corollary_build.py --stage 4 --src ../02-chain/sc-corollary.html --out ../02-chain/sc-corollary-fx.html`:
out `4f6f503cec8072ca`, +20731 characters. `src/render/fx.js` stamp `60e2c86423c7de24` →
`060d6c89f9c3451d` (the page's inlined copy and both stamps with it). The older links keep the
old stamp, as Starwarden's did.
- **engine_ab sc-corollary → sc-corollary-fx, ALL 34 relics WITH Axiom, n=6: 3366/3366
  identical** (`runs/engine_ab_corollary_to_fx_34.txt`). Picture, voice, beat and field move no
  fight.
- **corollary_probe --hex: 13/13** (`runs/probe_stage4.txt`):
  - [11] one hit beat per landed echo, fatal iff it killed (2728 beats, 37 fatal);
  - [12] one echo voice per landed echo and one snap per hex applied, counted at the call;
  - [13] each voice rendered ALONE through the shipped chain is audible (cast 0.447, echo 0.217,
    snap 0.343 peak), and the cast is not rune-crack (Spellbreaker's cast, still rune-crack,
    renders 0.619).
- **render_ab**:
  - the default pairs (no Axiom) print **24/24 frames pixel-identical**;
  - the control, axiom v lightkeeper 88212 at five frames inside Axiom's windows, prints
    **0/5 identical**, which is the check failing where it must.
- **shell_identity on sc-corollary-fx** (`SWB_GAME`, the pointer not moved): **200/200
  identical**, app Chromium 152 against headless 151. The json was restored to sc-leaf's
  afterwards, because the pointer has not moved.
- **chain_audit**:
  - relic and tip sc-corollary-fx: ALL 23 INSERTS SURVIVE (4 marked by comment text, named);
  - relic sc-corollary → tip sc-corollary-fx: all 10 stage-1/2 inserts survive (the stage-4 rows
    are, correctly, not in the stage-2 relic).
- **tip_audit**: 1, the same as sc-leaf.
- **verify --n 40: 11/13**, identical to sc-corollary: both reds are the clock bands and Axiom
  is 33.5%.

### 6e. The clip (Rick's to overrule)

`_corollary_pick.py` (the window scored on the whole sentence: landed, missed, late, hex, kill)
picked **axiom v lightkeeper, seed 88212**: cast at 74.83, 8 blows, 6 landed, 2 missed, 1 late,
6 hex, and the fight ends on Axiom's win at 86.07. Filmed with the director on:

    python cinema_clip.py --game ../02-chain/sc-corollary-fx.html --a axiom --b lightkeeper       --seed 88212 --at 73.63 --window 12.43 --fps 60 --w 540 --out ../07-shorts/v88/corollary-window.mp4

15.9s, 953 frames, AAC audio (mean -20.9 dB, max -2.1 dB), sent to Rick 2026-09-26. The mp4 is
gitignored; this command rebuilds it.

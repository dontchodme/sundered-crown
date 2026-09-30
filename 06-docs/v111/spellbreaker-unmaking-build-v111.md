# v111 — SPELLBREAKER / UNMAKING (REDESIGN), BUILD. STAGES 0-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, stages 0-5 fixed after an adversarial review; carried onto `sc-aureole-fxout`, the bolt's field spec out of both `fx.js` copies: §7): stage 1 is arm A fight for fight on both blocks; the hex window is the lab's mechanism (probe 6/6 on every stage from 2 on, read inside the hooks, with the stage pinned, the hex cadence rebuilt call by call and every field of both fighters, the shades and the match snapshotted around the ticker, the second hex and the cast; eleven mutants, each caught by its own check alone); the built relic reads 4-6 over its lab arms by the window clock, attributed with controls; **THE BLADE IS 7.5, THE MEASURED POINT NEAREST THE SHIPPED RATE: 49.2% both sides against the shipped bolt's 48.6%** -- under the brief's grid and the twinblade row's floor, so it is flagged for Rick, with the row's floor (8.30, `--alt-row`) and the 50% crossing (7.7, `--alt50`) built beside it. **Stage 6, the picture and the voice, is built (`sc-spellbreaker-b7.5-fx`, §5):** fifteen rows byte-exact to the two labs'; the Unmaking written in runes along both blades at the cast and unwritten at the close, rune motes shed off them, HEX +2 on every blow's second hex, and the foe's weapon greyed (grayscale, alpha 0.6) for each doubled stun's own 0.4 s; a glass crack into a C4 hum at the cast, the hex snap drawn out into a 0.4 s sizzle on each doubled stun, the hum cut at a clock close (none on a death); the bolt's art out, and no `fx.js` field (the motes are drawn; the bolt's `SPECS.spellbreaker` is the orchestrator's to take out at the carry). engine_ab 4218/4218 with Spellbreaker in; the probe 8/8, its two new checks (the voices, the picture's hook, 74 fights drawn) each failed by its own mutants; render_ab 24/24 with a control at 0/6; chain_audit 23/23 with a control; compose6 0 FAIL on 23 tips. verify --n 40 (stage 5; stage 6 moves no fight): 10/13, the base's three red checks, one new element in one (Spellbreaker v Bloodmirror 0/40, flagged). The clip is with Rick; the carry is the orchestrator's.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`, the BUILD row under the
redesign's). Input: `06-docs/v79/spellbreaker-unmaking-redesign-v79.md` and its runs, and nothing else
(rule 0). Builder `tools/spellbreaker_build.py` (6543119d4a9d0d1c; 005dc3e1d6af74c5 through stage 5), probe
`tools/spellbreaker_probe.py` (05f85277955137f9; 26434231bb955cf8 through stage 5), the clip's pick
`tools/_spellbreaker_pick.py` (1a2ac1070793473d), runs in `runs/` (`runs/commands.txt` names every command as it ran; the pre-review
runs are in `runs/prev/`). **A REDESIGN, not a new relic:** Spellbreaker ships in the base; its bolt (Unmaking) is replaced by the design's hex window,
and the roster stays 38. Built on DESKTOP-DERRAFT, Chromium 151.0.7922.34, Python 3.13, playwright 1.62.

```
sc-tendril-t3.html                 the base: the chain tip (Bindweed stage 5)                       5a6216e3b629fad4
  -> sc-spellbreaker-stub.html      stage 1  the bolt out, the Unmaking's block in, stubbed (1e9)     e1d4849ac78025e5
  -> sc-spellbreaker-stun.html      stage 2  the stun x2 on the foe, charge 14 (the brief's stage 1)  1dcdb0876f870b89
  -> sc-spellbreaker-unmaking.html  stage 3  the second hex, hexExtra 0 -> 1 (the brief's stage 2)   1231102e48184843
  -> sc-spellbreaker-b7.5.html      stage 5  the blade, 8.81 -> 7.5, nearest the shipped rate        da7936dccd8f5f15   (stage 6 goes on it)
  -> sc-spellbreaker-b7.5-fx.html   stage 6  the picture and the voice (presentation)                ceeff797e5739e0c   THE FINAL LINK
     sc-spellbreaker-b8.3.html      stage 5 --alt-row: 8.30, the twinblade row's floor (brief st. 3)  dade2e086be0a8cb   Rick's choice; not the carry
     sc-spellbreaker-b7.7.html      stage 5 --alt50: 7.7, the 50% crossing                            586b23089cf9674c   Rick's choice; not the carry
```

The links are in the batch's scratch (`<scratchpad>/batch/spellbreaker/links/`); the orchestrator
carries them onto the chain in the handoff's order by rebuilding them with this builder on the tip of
the day. **Every link rebuilds byte-identical** from the bare base with the final builder
(`runs/stage6_rebuild.txt`, the seven, stage 6's included; stages 1-5's before it, `runs/rebuild_final.txt`),
and no name is on `02-chain/`. The stage numbers are the builder's: its
stages 2 and 3 are the brief's stages 1 and 2, and its stage 5 is the brief's stage 3 (the blade); the
brief's stage 4 (picture, voice, carry) is the batch's stage 6, built here (§5).

### After the adversarial review (2026-09-29): what changed

The review (four should-fix findings, two notes) was taken whole; nothing in it was shown wrong.

1. **The probe could not fail "every hit hexes twice"** on a link that had lost its second hex: [4]
   built its expectation from the link's own `hexExtra`, and [6] accepted 0 or 1 on any link. **Fixed:**
   the stage is pinned (`--stage`, or inferred from the blade), [4] expects the stage's `hexExtra` and
   requires the hex applied on a live body in windows to be exactly 2 a blow; the reviewer's own mutant
   (the final with `hexExtra:0`, `r1-hexonce`) now fails [4] alone (§3).
2. **Probe [5] watched a fixed list of fields**, not the hex clock, the reach, the stun-DR, the charge or
   the burden, and [2] never checked how often hexes proc. **Fixed:** [5] snapshots every own field of
   both fighters, every shade and the match around every tickUnmake call and around the second-hex
   insert (bracketed by accessors), and checks the hex clock between tickStatus calls; [2] rebuilds the
   hex cadence call by call; the stun gate needs 200 clean runs each side of the window. The reviewer's
   two stage-2 controls (`q2-hexclock`, `q2-shrink`) are now caught by [5], and four more mutants (r2-r5)
   each fail their own check alone (§3).
3. **The builder's scan missed stun, status, hex-clock and reach writes**, so §1's claim was false.
   **Fixed:** the scan refuses them (and `stunDR`, `charge`, `burden`, any other `apply()`), with the two
   design lines allowed by exact text; 27 negative copies refuse (§1).
4. **The blade went against the redesign blade policy**: 8.30 (the row's floor, +83 wins) was carried
   where the measured point nearest the shipped rate is 7.5 (+8). **Fixed:** the carry is 7.5; 8.30 is
   `--alt-row` and 7.7 `--alt50`, both flagged for Rick (§4, §6).
5. (note) **The second hex landed on the killing blow's corpse.** **Taken:** the lab's `foe.alive` guard
   (reading 6).
6. (note) **The second-hex block split Deadfall's comment from its code.** **Taken:** it now sits before
   that comment (§1).

Notes 5 and 6 change the page from stage 2 on, and **move no fight**: the fixed links replay the
pre-review links' fights exactly -- the stage-5 grid at 8.81, 8.3, 7.7 and 7.5 on both blocks
(`runs/n1_inert.txt`, 5920 fights), the built SHIP arms and both clock controls (`runs/built_same.txt`),
and the probe's 444 fights on the final (the same digest). So every measurement of §2 and §4 stands; the
pre-review run files are kept in `runs/prev/`.

## 0. What this build stands on

- **The relic** is Spellbreaker as it ships (base line 945): the runic twinblade, blade 8.81, blades
  [0, 0.5], reach 62, width 8, artW 30, spin 5.7, mode spin, mass 1.1, onHit hex 1. Every physical stat,
  the channel and the blurb stay; only the ult block changes, and at stage 5 the blade. The builder
  asserts all of it BY CONTENT, never by which relic is last: the row, the shipped Unmaking verbatim, the
  shipped blade, `Fighter.apply(key, n, src)`, `stacks`, `breakSpin(f, reason, trueFor)`, `STATUS.hex`
  as priced (5 stacks, 2.6s, a stun every 1.15s over stacks, 0.20s), tickStatus's hex proc to the
  character, resolveHit's onHit loop and blow count, that no code keys on `kind "bolt"`, and that
  step()'s window tickers stop in a hit stop (Tendril's ticker call is the anchor). Names kept (design
  §4): SPELLBREAKER / UNMAKING; the card is the design's 68 characters, `Hexes stun the foe's weapon
  twice as long, and every hit hexes twice`.
- **The reference, the shipped relic's rate on the base** (`relic_rate`, both sides, two blocks, 1480
  fights, `runs/rr_shipped_*`): **48.6%** (720 of 1480; 48.5 / 48.8; side A 49.1, side B 48.2), mean
  74.6s. This is "the shipped rate" the brief settles the blade to. The design's 49.7 is the bolt on
  Chromium 141, side A only; on 151 the lab's own SHIP arm reads 52.3 / 52.4 (side A).
- **The charge is 14.** The design names none: its lab priced every arm at the harness default, 16 on
  the lab's clock (`"charge": 16.0` in every `v79/runs/unmaking_*.json`). Rick's batch ruling converts
  it. Measured for this fighter by `runs/labx.py` (written by `runs/make_labx.py`), a scratch copy of `ult_overlay.py` that counts, before each
  lab step, the frozen ones (`m.hitStop > 0 || m.latch || m.splitHold`) in total and inside windows, and
  keeps every fight's row (`runs/lx_*`; 660 fights an arm a block; its arms read ult_overlay's to the
  fight): arm D0 (stun x2, no second hex) 12.43% / 12.37% of lab steps frozen (13.33% / 13.29% inside
  windows), so the lab's 16 is the engine's 14.01 / 14.02; arm D (the taken arm) 12.31% / 12.25%
  (12.97% / 13.00% inside windows), 14.03 / 14.04; arm A 12.54% / 12.45%. **14 on every arm and
  block.** The shipped bolt's 13 goes with the bolt.
- **The window is 8 seconds.** The prose says "for a duration"; every priced arm used the harness's
  `P.dur` 8, and the build takes the lab's number. It runs on the window tickers' clock (the batch's
  convention: the number is the design's, the clock the engine's); §2 measures what that clock makes of
  it (9.2s of match time) and what that is worth (5-7 points at 8.81, 9 at the carry's 7.5).
- **The lab is `overlays/unmaking.js` through `ult_overlay.py --relic spellbreaker`** with no `--cell`
  (a redesign): arm A is the relic with its ultimate suppressed, SHIP the bolt live, B the shrink, C the
  shrink and the second hex, **D the taken arm: the second hex and the stun multiplier, no shrink.**
  **Flagged: the lab's own default is `stunMul` 1** (the overlay's `P.stunMul ?? 1`), not the settled
  x2; every settled run passed `--P stunMul=2`, and every lab arm here does too (the brief's own stage-0
  command). `hexExtra` defaults to 1, the design's.
- **The roster** is the 34-relic roster minus the donor, 33 foes (`runs/foes33.txt`), which is exactly
  the published json's `byFoe`. The four relics built since (Morningstar, Ironwood, Portcullis,
  Bindweed) are foes in `relic_rate` and `verify`, not in the lab's arms.
- **The ultimate it replaces, found whole in the base, and what became of each piece** (line numbers
  are the final link's, `sc-spellbreaker-b7.5.html`; the base's are the same above the row and 5-77
  lower below it):
  - the ult block `kind:"bolt", charge:13, dmg:20, apply:{hex:3}` (base line 948): **replaced** by
    `kind:"unmake"` (line 953);
  - **no cast branch, no ticker, no fighter field and no life-cycle of its own**: the bolt was fireUlt's
    generic tail (`inRange && u.dmg`: the hurt, the float, the burst, the ring, then `u.apply`'s hex 3).
    No code keys on `kind "bolt"` (Axiom's Corollary left it in v88; the builder asserts it), and the
    tail **stays whole**: its damage clause and its `u.apply` loop serve five other ult blocks
    (Widowmaker, Thornwake, Censer, Oathwound and Heartwood carry `apply:`). **So nothing in the
    simulation is retired beyond the block;**
  - **the presentation, kept by stages 1-5 and the brief's stage 4's to retire** (the batch's stage 6, built:
    §5 retires the bolt's branch, its seat and its life, answers the cast with its own voice, keeps the charge
    rune and the banner scatter, and leaves the field spec to the carry; nothing in the simulation reads any of
    it; the line numbers here are the b7.5's, the fx link's are §5g's): the charge rune
    `ULTSIG.spellbreaker` (line 579, "a rune that comes APART"); fireUlt's banner seat `onTarget`
    (`spellbreaker:1`, line 16271: the name lands on the quarry, where the bolt struck); the ultFx
    record's `life` entry `spellbreaker: 1.4` (16299); drawUltOver's `u.w === "spellbreaker"` branch
    (21849: the jagged bolt with its glyphs, the cage of rings that closes on the target and comes apart;
    it draws `Math.random()` for its flicker); the banner's letter scatter (`b.w === "spellbreaker"`,
    28974 and 29147); the cast voice (Spellbreaker has no arm in `SFX.play("ult")` and falls through to
    rune-crack, 7429); and the field spec, the inlined `fx.js` copy's `SPECS.spellbreaker` (32322-32324):

        spellbreaker: { mode: 'beam', n: 1200, sp: [40, 200], grav: -40,
                        drag: 1.6, life: [0.25, 0.70], heavy: 0.0,
                        size: [0.6, 1.8], spawn: 0.35, up: 0 },

    The brief: "Stage 4 — picture, voice, carry; bolt's field spec out". The disk `src/render/fx.js`
    carries the same entry; this build touches neither copy (`tools/fx_remove.py` takes it out of both
    at the carry, the batch's procedure).
- **Readings** (in the builder's docstring; where the build had to choose):
  1. **The window is 8s** (above).
  2. **The charge is the lab's 16 converted**, 14 (above).
  3. **The stun multiplier is the foe's own field** (§4): `f.hexStunMul`, 1 on every fighter,
     recomputed for BOTH fighters on every window-ticker frame as a pure function of whether the OTHER
     fighter's Unmaking is open (Bloodletting's rule, "recomputed and never restored"): a fresh Match
     starts at 1, and a close puts it back on its own frame. So a runic foe's hexes on Spellbreaker are
     untouched (§4). The lab set the global `STATUS.hex.stunFor`, which doubled every hex stun in the
     match, Spellbreaker's own from a runic foe included: DECLARED by §4.
  4. **The field is the two fighters'**: a Twinshade shade keeps 1, where the lab's global doubled its
     stuns too. The probe counts those procs (356 on shades in its 444 fights on the final, all at x1).
  5. **Every stun a hex lands**: both reads of the hex proc, the weapon's stun and `breakSpin`'s
     true-stun length, are `STATUS.hex.stunFor x f.hexStunMul`. A stun that lands in the window keeps its
     length after the close (it is the weapon's clock, as the lab's was).
  6. **The second hex goes where the blow's own hex goes**: resolveHit's struck body, after the blow's
     onHit, on every blow the caster lands while its window is open **on a body the blow left alive**
     (`foe.alive`, the lab's own guard, `if (hex && foe.alive)`: the killing blow gets the channel's hex
     alone, and no second hex lands on a corpse; added after the review, note 1, and it moves no fight:
     `runs/n1_inert.txt`). The lab applied it at the end of the frame to the OPPONENT when the caster's
     hit count rose; on a blow on the opponent the two leave the same stacks at the next tickStatus
     (nothing reads hex in between), and only a blow on a shade differs (counted by the probe, §3).
     `apply`'s source is a side letter (Rick's ruling 4; hex has no reader of its source).
  7. **The window closes on its clock or EITHER death** (the lab's); the multiplier drops on the close's
     frame; no second hex after it.
  8. **No cast waits.** The design asks none, and a cast cannot find its window open: the charge is 14
     of unfrozen time against a window of 8 on the same clock (probe [6] asserts it on every cast). No
     clause joins the cast's `if (f.charge >= f.w.ult.charge && !f.ultCorona` prefix.
  9. **No shrink**: arm D is the taken arm (§3, "D double hex + stuns x2 (taken)"). x2, not x3 (§3;
     §6.3 is Rick's, and x3 "needs a blade under the row").
  10. **The card** is the design's own 68 characters.
  11. **The bolt is out** (brief stage 1): the ult block only (above). Its picture, voice and field spec
      are the brief's stage 4: this build's stage 6 (§5, the builder's readings 13-20).
  12. **The Unmaking is a stun length and an apply() and nothing else**: the ticker and the second hex
      hurt nobody, move nobody, stop nothing, file nothing and draw no rng.
  13. **The design's "foe hex on a window frame" column is the lab's per-CAST second-hex count.** v79 §3's
      table heads its last column "foe hex on a window frame" and prints 3.22 for arm D; that is
      ult_overlay's `hex` column, `S.hex` over casts, the number of second hexes a cast (per-cast unless a
      key starts `f_`). The foe's actual stacks on a window frame, read by a scratch copy of the overlay
      that only counts (`runs/unmaking_x.js`, `runs/lxm_*`), are **2.50** in the lab (2.45 on unfrozen frames).
      The brief's stage-2 gate "foe at ~3.2 on a window frame" is read as that column; both are reported.
- **Names:** the kind is `"unmake"`, the ticker `tickUnmake`, the fields `ultUnmake`, `unmakeTally` and
  `hexStunMul`; none was in the base (the builder greps them).

## 1. Stages 1, 2, 3 and 5 (stage 6: §5)

- **Stage 1** replaces Spellbreaker's ult block, exactly once, with the Unmaking's block at charge 1e9
  (`dur 8, stunMul 2, hexExtra 0`, the card). The row is edited in place (a redesign: nothing is appended
  to WEAPONS). The bolt's block is gone; nothing reads the new block's fields.
- **Stage 2** (the brief's stage 1: "bolt out, `f.ultUnmake` in, `hexStunMul` on the foe") sets charge
  14 and adds: the fighter fields `ultUnmake`, `unmakeTally` and `hexStunMul = 1` AFTER the stable line
  `this.vineTally = null;`; the cast branch `if (u.kind === "unmake"){` (opens `{t: 0, dur}`, resolves
  nothing) BEFORE `    if (u.kind === "tendril"){`; the ticker call `this.tickUnmake(dt);` AFTER
  `    this.tickTendril(dt);               // TENDRIL (v68)`; the method `tickUnmake` BEFORE
  `  tickWinnow(dt){`; the hex proc's two reads x `f.hexStunMul` (the proc's block replaced exactly once);
  and the second hex, inert at `hexExtra` 0, right after resolveHit's onHit loop, BEFORE the unique
  comment line `    /* ---- THE BLOW LEAVES A FIGURE ON THE FLOOR. Rick: "when it lands a hit` that
  opens Nightfell's Deadfall block (the review's note 2: the pre-review build anchored on the Deadfall
  `if` itself and split that comment from its code). The second hex lands only on a body the blow left
  alive, `if (U.hexExtra > 0 && foe.alive)`, the lab's own guard (the review's note 1; reading 6).
- **Stage 3** (the brief's stage 2) flips `hexExtra` 0 -> 1.
- **Stage 5** (the brief's stage 3) moves the blade 8.81 -> **7.5**, the measured point nearest the
  shipped rate (§4). `--alt-row` writes 8.30 (the twinblade row's floor, the brief's lowest grid point;
  written `8.30`, the same double as 8.3, because Twinshade's and Starwarden's rows carry the line
  `blades:[0,0.5], reach:62, width:8, artW:30, dmg:8.3,` character for character and `chain_audit`
  watches single lines, so the audit could not watch a carry written `8.3`:
  `runs/prev/chain_audit_control_plain83.txt`), and `--alt50` writes 7.7. The carry's line `dmg:7.5,`
  is on no other row of any chain tip.
- **The builder's guards**: it refuses to overwrite a link, a name outside `sc-spellbreaker*` or one
  already on `02-chain/`, a base without Tendril's ticker (sc-trunk), a stage on the wrong stage, both
  alternatives at once, an anchor that is not there exactly once, and a page that does not parse (`node
  --check`); it writes LF. It strips comments before it checks the ult block (exactly one `unmake`, no
  `bolt`), the card, the blade, the `Math.random` count, and every insert (the lines an edit adds, its
  re-emitted anchors aside) for `rng()`, `spawnFx`, `ultFx`, a write to the shared weapon (`w.dmg`,
  `w.spin`, `w.reach`, `w.blades`, `w.mass`; compound assignments, `++` and `--` count), a write to or an
  alias of a shared module table (`STATUS`, `CONFIG`, `AFFINITIES`, `WEAPONS`, `SHAPES`; Lightkeeper's
  third review), a call or write that hurts, heals, knocks, pins, moves, turns, stops or files a beat,
  and (added after the review's finding 3) **any write to a `stun`, `stunDR`, `hexClock`, `reachMul`,
  `charge` or `burden`, any write to, alias of, `delete` or `Object.assign` of a `.status`, and any
  `apply()` call** -- except the two lines the design asks for, allowed BY EXACT TEXT and only in their
  own edit: the hex proc's `f.stun = Math.max(f.stun, STATUS.hex.stunFor * f.hexStunMul);` and the second
  hex's `foe.apply("hex", U.hexExtra, self === this.a ? "a" : "b");` (each must appear exactly once
  there). From stage 2 it asserts that both reads of the hex stun carry the fighter's `hexStunMul`.
  **Tested** (`runs/builder_negtest.txt`): 27 copies, each adding ONE forbidden line to tickUnmake, the
  cast branch or the second-hex insert -- the pre-review ten (`foe.vx *= 0.99`, `this.rng()`, `f.w.dmg =
  9`, `f.w.spin += 1`, `this.hurt(...)`, a hit stop, `STATUS.hex.stunFor = 0.4`, the same through an
  alias, `CONFIG.chaos.critMul *= 1.1`, `foe.theta += 0.1`) and seventeen more: the review's four
  (`foe.stun = Math.max(foe.stun, 0.1)`, `foe.status.hex = {...}`, `foe.hexClock += 0.5`, `foe.reachMul =
  Math.max(0.4, foe.reachMul - 0.0005)`), `foe.status["hex"].t = 9`, a status through an alias, `delete
  foe.status.hex`, `foe.stunDR = 0`, `f.charge += 1`, `foe.burden = 1`, `foe.apply("chill", 1)`, the
  allowed stun line copied into tickUnmake, a stun and a hex clock in the cast branch, and a 12% shrink,
  an extra `apply` and a stun in the second-hex insert. All 27 refuse and write nothing; the clean copy
  writes the stage-2 link unchanged. The refusals of `runs/rebuild_final.txt` write nothing either.
- **It composes** (`runs/compose_s5.txt`): stages 1-5 apply and parse on 23 tips, the base, every newer
  link of the batch line on `02-chain/` up to `sc-aureole-fxout` and `sc-censer-fxout` (42 relics), and
  the in-flight builds' scratch tips; every tip takes the same 85 changed lines (md5 83845082c07f).
- **Stage 6** (the brief's stage 4) is §5: fifteen rows, the labs' own, on the b7.5, with a scan of its own
  (§5e). On the final builder the 27 negative copies above refuse as before
  (`runs/stage6_builder_negtest_s1to5.txt`: 27 refuse, none writes; the clean copy writes the stage-2 link).

## 2. Stage 0, and the stages against it — the window clock, measured

`ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic spellbreaker --mech overlays/unmaking.js
--arms A,SHIP,D --P stunMul=2 --seeds 20 --foes <33>`, seed0 2207 and 2317, 660 fights an arm a block,
Spellbreaker side A (`runs/s0_*`); arm D0 is the brief's `--P stunMul=2 hexExtra=0` (`runs/s0D0_*`).
The built links run `ult_overlay.py --relic spellbreaker --arms SHIP` on the same foes and seeds (the
same seed formula and side; `runs/built_*`, `runs/pf_stub_*`). **The fixed links play the pre-review
links' fights exactly** (`runs/built_same.txt`: every field of every SHIP arm, the built stages 2 and 3
and both clock controls, both blocks, against `runs/prev/`), so this table did not move with the review.

```
                                   lab on 151 (1 / 2)   published 141   lab at the engine's window   BUILT (1 / 2)                 the build on the lab's clock
A    no ultimate                   25.0 / 27.6          20.9                                         stage 1: 25.0 / 27.6          identical, fight for fight
SHIP the bolt (as shipped)         52.3 / 52.4          49.7
D0   stun x2, no second hex        46.1 / 46.1          -               dur 9.23: 48.9 / 48.8        stage 2: 50.5 / 51.7          45.6 / 45.3
D    stun x2 + the second hex      54.4 / 55.0          55.2            dur 9.19: 59.1 / 56.5        stage 3: 60.6 / 60.9          55.5 / 53.8
```

- **Published against 151.** Replayed on the design's own base (`sc-trunk`, the design's 33 foes x 10,
  `runs/pub151_*`): A 21.8, SHIP 51.5, B 24.2, C 29.1, D 53.3, against the published 20.9, 49.7, 27.0,
  32.1, 55.2: every arm within 3.0 points at n = 330, so the runtime reproduces the design's numbers. On
  the base (38 relics), 660 a block, the lab reads A 25-28 and D 54-55 (the design's 55.2).
- **Stage 1 is arm A fight for fight on both blocks** (`runs/stage1_vs_A.txt`, from `labx.py`'s
  per-fight rows): 660 of 660 fights the same winner, the same duration to the step, the same blows in and
  out of windows and the same casts (0); wins 165 / 165 and 182 / 182; blows a fight 26.477273 and
  26.596970 on both; every foe's rate identical. Both sides too: `relic_rate` on the stub reads 17.8 /
  23.6 (side A 19.5 / 23.2, side B 16.2 / 24.1; `runs/rr_stub_*`), the redesign with no ultimate.
- **The mechanism, lab against built** (block 2207, side A, the lab's own 660 fights; the lab's arm D
  through the counting copy `runs/unmaking_x.js`, the built stage 3 through the probe in lab mode, `--sides A
  --seedstep 11 --foes <33> --seeds 20 --seed0 2207`; `runs/lxm_D_2207.txt`, `runs/probe_lab_unm_2207.txt`):

```
                                               lab D (8s of lab clock)   BUILT stage 3 (8s of window clock)   the build on the lab's clock
casts a fight                                  4.54                       4.61                                 4.47
blows a fight, in windows / outside            14.92 / 16.24              17.74 / 14.50                        14.68 / 16.35
blows in a window a cast (the lab's "unmade")  3.22                       3.85                                 3.28
second hex a cast (the lab's "hex")            3.22                       3.77 (killing blows out)             3.23
hex a blow in a window on a live body          2 (by construction)        2.000                                2.000
the foe's hex stacks on a window frame         2.50 (2.45 unfrozen)       2.52                                 2.45
the foe's weapon stunned, window frames        63.0% (59.7% unfrozen)     60.6%                                58.9%
window steps frozen                            13.0% (the census)         13.6%                                13.7%
a window, in match time                        8.00s                      9.21s                                7.99s
win                                            54.4%                      60.6%                                55.5%
```

**The built relic reads 4-6 over every lab arm from stage 2 on (D0 +4.4 / +5.6, D +6.2 / +5.9), and the
window clock is all of it, measured both ways.** The engine's 8s are 8 seconds of the window tickers' clock, which stops in a hit
stop; 13.6% of window steps are frozen, so a built window lasts 9.21s of match time where the lab's
lasted 8 step-seconds, and it holds 17.7 of her blows instead of 14.9. (1) **The build on the lab's
clock reads the lab:** a scratch variant of each built link whose `tickUnmake` also runs on every frozen
step (the latch, the split hold and the hit stop: `runs/clock_variant.py`, `ctl/ctl-lab-stun.html`
33de3230bbf44c0f and `ctl/ctl-lab-unm.html` 63c36a2badc9d148, rebuilt from the fixed links; never links) reads 45.6 / 45.3 against the
lab's D0 46.1 / 46.1, and 55.5 / 53.8 against D's 54.4 / 55.0 (`runs/ctl_*`), with a 7.99s window and
3.28 blows a cast against the lab's 3.22. (2) **The lab at the engine's window reads the build:** the
lab's own arms run at `dur` = 8 / (1 - the probe's frozen share inside windows) = 9.23 (D0) and 9.19
(D) read 48.9 / 48.8 and 59.1 / 56.5 (`runs/labw_*`), against the built 50.5 / 51.7 and 60.6 / 60.9,
with 3.55-3.73 blows a cast against the built 3.73-3.85: three of the four within 1.5-2.9 points, and
2317's arm D 4.4 under (one 660-fight block's standard error is ~1.9; the lab at the longer window still
counts window frames inside a hit stop, which the engine's window never has, and adds its second hex at
the frame's end). This is the clock v99 §4, v100 §2 and v101 §2 measured on Canopy, Onslaught and Tendril; here it
pushes up, through more blows in a longer window. The mechanism is the lab's: the foe's stacks on a
window frame agree to 0.02 (2.52 against 2.50), and its stunned share to 0.9 points once the lab's
frozen frames are set aside (60.6% against 59.7%: a lab window frame inside a hit stop counts a stun
that the engine's window clock never sees). Nothing is mis-built. **The engine's convention and every designed number are kept**; stage 5 prices it.
**At the carry's blade the clock is worth more:** m1-frozen (§3), the final with its window on the lab's clock, reads
**40.1% both sides** (593 of 1480, `runs/rr_m1clock_b7.5_*`) against the final's 49.2% on the same fights, -9.1
points, where stage 3 at 8.81 lost 5.1 / 7.1 (side A). That is why the shipped rate lies under the brief's grid:
the design's "about 8.4" was priced on the lab's clock.

**The brief's gates, stage by stage:**
- **The brief's stage 1** (built stage 2, `sc-spellbreaker-stun`): "measured stun length on the foe's
  weapon 0.40 ±0.01 inside windows and 0.20 outside (asserted)": **0.4000s** over 4542 clean runs inside
  (every one 48 steps), **0.2083s** over 16069 outside (every one 25 steps: the engine's own countdown,
  0.2 - 24/120 leaves 1.4e-17, so the base's hex stun has always been 25 steps; Spellbreaker's own hex
  stuns read the same 0.2083). MET. "Relic ~45% at 8.81": the built link reads 50.5 / 51.7 by the clock;
  on the lab's clock 45.6 / 45.3.
- **The brief's stage 2** (built stage 3, `sc-spellbreaker-unmaking`): "hex applied = 2 x hits in
  windows": **2.000** on every blow in a window that leaves the body alive (the channel's 1 and the
  second 1, read inside resolveHit; [4] requires it exactly), and the channel's 1 alone on the killing
  blow, the lab's own guard (158 of 7710 window blows in the probe's 444 fights). "Foe at ~3.2 on a window
  frame": the lab's column (reading 13) reads **3.70** second hexes a cast both sides (3.78 blows a cast;
  3.77 / 3.85 on the lab's fights; the lab 3.22, the difference the clock); the foe's actual stacks on a
  window frame are **2.48** (the lab's 2.50). "Relic ~55%": 60.6 / 60.9 by the clock; on the lab's clock
  55.5 / 53.8.

## 3. The probe (`spellbreaker_probe.py`, one check per sentence, read inside the hooks)

It wraps `tickUnmake`, `fireUlt`, `tickStatus` (and, inside it, the hex proc's own `breakSpin` call),
`tickWeapon`, `resolveHit` and `step` on the Match prototype, plays Spellbreaker against every other
relic from both sides (37 foes x 6 seeds x 2 sides = 444 fights; `--sides A --seedstep 11 --foes <33>
--seeds 20 --seed0 2207` plays the lab's own fights), and prints N/N; a check whose event never happened
fails ("a check that never ran is not a pass").

**The stage is pinned, not read off the link** (the review's finding 1). What the probe expects comes
from `--stage 2|3|5` and the builder's numbers, never from the link's own ult block: stage 2 (the brief's
stage 1) expects no second hex, stages 3 and 5 the design's `hexExtra` 1. With no flag it infers the stage
from the BLADE (not the shipped 8.81: stage 5) and, at the shipped blade only, from `hexExtra`, and prints
which; so the carried final needs no flag, and a final that has lost its second hex is still held to 1.
Each design number is held by the check of its own sentence (dur by [1], stunMul by [3], hexExtra by [4],
the charge and the blade by [6]), so a mutant that moves one number fails one check.

- **[1] "For a duration"**: the window's clock advances by exactly dt a call; `tickUnmake` is asked
  exactly once on every unfrozen step and never on a frozen one; the window closes at `dur` on the window
  clock or at either death, never before and never after; only Spellbreaker carries `ultUnmake`; `dur` is
  the design's 8.
- **[2] "every stun a hex lands on the enemy's weapon lasts twice as long"**: every hex proc (the one
  `breakSpin(f, "the hex takes the wind out of it", len)` in tickStatus) runs exactly `STATUS.hex.stunFor
  x` the fighter's own `hexStunMul`, and leaves the weapon's stun exactly max(the stun before, len); a
  proc at x2 on the foe inside a window, at x1 outside and x1 on Spellbreaker must each happen. **The
  cadence is rebuilt call by call** (the review's finding 2: only the LENGTH may move): in every
  tickStatus call the hex clock goes from c0 to c0 + dt x stacks, and a proc happens exactly when that
  reaches `stunEvery` (1.15), when the clock goes to 0. The realised stun (the proc until the weapon's
  stun reaches 0, counted in tickStatus calls, for runs nothing else touched) is the brief's gate, 0.40 ±
  0.01 inside and 0.20 ± 0.01 outside, **over at least 200 clean runs each** (the pre-review gate took any
  number above 0).
- **[3] the foe's own field (§4)**: after every tickUnmake call, each fighter's `hexStunMul` is exactly
  the OTHER fighter's `stunMul` while the other's window is open and 1 otherwise (so Spellbreaker's own is
  1 always: a runic foe's hexes untouched); a shade's is 1; a fresh Match's is 1; the field moves nowhere
  but in tickUnmake; `stunMul` is the design's 2.
- **[4] "every hit Spellbreaker lands hexes twice"**: each of her blows applies, on the body it struck,
  exactly the channel's `apply("hex", 1)` and then, while her window is open and the blow left the body
  alive, `apply("hex", the stage's hexExtra, side letter)`, in that order and nothing else, the stacks
  (min 5) and the clock (2.6) the engine's; outside the window, or on the killing blow, the channel's 1
  alone; **the hex her blows apply on a live body in windows, divided by those blows, is exactly 1 +
  hexExtra (2 from stage 3)** (the review's finding 1); the link's `hexExtra` is the stage's; and the
  blow's damage is the blade's own, rebuilt from the captured crit and jitter draws, in the window and out.
- **[5] nothing else, field by field** (the review's finding 2): around every tickUnmake call, EVERY own
  field of both fighters and every shade (a primitive by value; an object by its JSON, with a Fighter or
  the Match inside it by identity; a long history array -- a trail, a blade tip's path -- by its length and
  its first and last entries; the three shared tables a fighter points at, `w`, `aff` and `slM`, by
  identity on every call and by their JSON at every fight's start and end) and every own field of the
  match (a primitive by value, an array by its length, an object by identity) is snapshotted, and only
  `ultUnmake`, `unmakeTally` and `hexStunMul` may
  move -- a hex clock, a reach, a stun, a stun-DR, a charge, a burden, a position, an hp, a status, the
  match's clock, hit stop, shots, beats or end may not; **the second-hex insert is bracketed the same
  way**, from its own `self.ultUnmake` read (the insert's `if`, the one read of that field in resolveHit)
  to the `self.ultDeadfall` read that follows it (Deadfall's `if`), both caught by accessors installed on
  the caster for the length of her resolveHit, and only her tally (blows +1, extra + the hex it applied)
  and, through an `apply()` that [4] audits, the struck body's statuses may move; **a fighter's hex clock
  may move only inside its own tickStatus** (checked between every two calls); and no hurt, beat, rng or
  shot.
- **[6] the bolt is out**: a cast that spawns a shot, hurts anybody, applies any status, moves an hp or a
  ward, does not open `{t: 0, dur}`, lands on an open window, or moves ANY field of either fighter, a
  shade or the match beyond fireUlt's shared prologue (the caster's `ultsFired` +1 exactly; the match's
  `banner`, `events`, `shake`, `hitStop`, `beats` and `ultFx`) and the window it opens (`ultUnmake`,
  `unmakeTally`); an ult block that is not the design's (kind `unmake`, charge 14, the builder's) or still
  carries the bolt's dmg / apply; a blade that is not the stage's (8.81 at stages 2-3; 7.5, 8.30 or 7.7 at
  stage 5).

Printed besides: every number by side, and in the json a digest of every fight (won or lost, and its
length in steps), so a mutant's changed fights can be counted.

**Results** (`runs/probe_*.txt`, `runs/probe_table.txt`; the probe as it now stands, every link fixed; the
pre-review probe's runs are in `runs/prev/`):

```
link                       stage          checks  casts  blows in / out   blows a cast  2nd hex a cast  hex a live blow  foe hex/frame  foe stunned in / out   window (match)  frozen  win (444 fights)
sc-spellbreaker-stun       2              6/6     4.47   16.72 / 14.20    3.74          0.00            1.000            1.92           51.0% / 38.9%          9.25s           13.9%   50.0%
sc-spellbreaker-unmaking   3              6/6     4.60   17.36 / 14.82    3.78          3.70            2.000            2.48           60.3% / 42.7%          9.20s           13.5%   60.6%
sc-spellbreaker-b7.5       5 (the final)  6/6     4.73   18.85 / 15.64    3.99          3.93            2.000            2.54           61.0% / 44.7%          9.22s           13.7%   48.2%
sc-spellbreaker-b8.3       5 --alt-row    6/6     4.68   18.09 / 15.21    3.87          3.80            2.000            2.49           60.2% / 44.2%          9.22s           13.7%   53.8%   (Rick's)
sc-spellbreaker-b7.7       5 --alt50      6/6     4.77   18.70 / 15.50    3.92          3.86            2.000            2.54           61.1% / 44.8%          9.21s           13.6%   47.7%   (Rick's)
```

"2nd hex a cast" is now under "blows a cast" by the killing blows (123 of 8369 window blows on the final,
each with the channel's hex alone); "hex a live blow" is [4]'s exact ratio, 1 + hexExtra.

- **The stun, realised, on the final link:** 0.4000s over 4072 clean runs inside windows (0.4000..0.4000),
  0.2083s over 19550 outside, and 0.2083s over 1319 on Spellbreaker herself (no x2 on her, ever); 34,875
  procs on the foe at x2 (16.6 a cast), 13 at x1 inside a window (the cast's own step: the foe's
  tickStatus runs before `tickUnmake` recomputes the field), 356 on shades, all x1. **The cadence** was
  rebuilt on all 7,941,846 tickStatus calls (c0 + dt x stacks; a proc and the clock to 0 at 1.15), and the
  hex clock never moved between two of a fighter's tickStatus calls.
- **Nothing else, field by field, on the final:** 3,943,822 tickUnmake calls moved no field of either
  fighter, a shade or the match beyond `ultUnmake`, `unmakeTally` and `hexStunMul`; the second-hex insert
  was bracketed on all 8369 of her blows in a window and 6944 outside (never open-ended, never unread);
  2098 casts moved nothing beyond fireUlt's prologue and the window they open.
- **By side** (the final link): side A 48.6%, side B 47.7% in the probe's fights; 3.95 / 4.03 blows a
  cast; the foe's hex on a window frame 2.54 / 2.54; stunned 60.9% / 61.0% of window frames (43.8% /
  45.5% outside); 4.74 / 4.71 casts. The mechanism is the same from either side (see §4 on the win-rate
  split).
- **The same fights as before the review:** the final's 444-fight digest (winner and length to the step)
  equals the pre-review b7.5 link's, fight for fight; only `extra` moved (8369 -> 8246, the 123 killing
  blows).
- **Lab mode** (the lab's 660 fights, side A, `runs/probe_lab_unm_2207.txt`): stage 3 6/6, 60.6% (=
  `built_unm_2207`, the same fights), 3.85 blows and 3.77 second hexes a cast (246 killing blows in
  windows), foe hex 2.52 on a window frame, stunned 60.6%, 13.6% of window steps frozen, a window 9.21s
  of match time. The stage-2 lab-mode run is the pre-review probe's (`runs/prev/probe_lab_stun_2207.txt`,
  6/6, 50.5%, the same fights: `runs/built_same.txt`). The clock control on stage 3 in lab mode
  (`runs/probe_lab_ctlunm_2207.txt`) fails [1] and only [1], as it must (its `tickUnmake` runs on
  frozen steps), 55.5% (= `ctl_unm_2207`), 3.28 blows and 3.23 second hexes a cast, a window 7.99s of
  match time; m1-frozen below is the same control on the final.
- **The mutants** (`runs/probe_mutants.txt`; scratch copies of the final link made by `runs/mutants.py`,
  each breaking ONE sentence in a way that changes fights; each must fail its own check, by a violation,
  and no other; m1-m6 are the build's own, r1-r5 were added after the review):

```
mutant        what it breaks (one sentence)                                          probe   fails        win     fights changed (of 444)
(the final)   -                                                                      6/6     none         48.2%   -
m1-frozen     "for a duration": tickUnmake also runs on every frozen step (the lab's    5/6     [1] alone    34.5%   442
              clock: the latch, the split hold, the hit stop)
m2-stunlen    "every stun ... twice as long": the weapon's stun ignores the field        5/6     [2] alone    17.3%   444
              (breakSpin's length still reads it)
m3-global     §4 "the FOE's hexStunMul": the lab's global, the caster's own hex           5/6     [3] alone    47.1%    36
              stuns doubled too while her window is open
m4-hexout     "every hit hexes twice" in the window: the second hex outside it too       5/6     [4] alone    52.3%   444
m5-drag       "nothing else": the window drags the foe, 0.5% of its velocity a frame      5/6     [5] alone    46.4%   432
m6-boltkept   "the bolt is out": the cast still hurts for the bolt's 20                   5/6     [6] alone    56.1%   332
r1-hexonce    "every hit hexes twice": the block's hexExtra 1 -> 0 (the review's r1)      5/6     [4] alone    38.5%   444
r2-hexclock   "nothing else": the ticker runs the foe's hex clock, +0.01 a window       5/6     [5] alone    57.0%   444
              frame (about half as fast again as its own dt x stacks)
r3-shrink     "nothing else" / §3's arm D: the rejected shrink in the ticker, 0.0005      5/6     [5] alone    66.9%   444
              of reach a window frame, never restored (the review's)
r4-shrinkhit  "nothing else", at the second-hex insert: the lab's arm-B shrink, 12%       5/6     [5] alone    62.2%   443
              a blow in the window, never restored
r5-cadence    "twice as LONG": the foe's hex clock runs x hexStunMul in the window, so    5/6     [2] alone    55.6%   444
              hexes proc twice as often (the cadence, not the length)
```

  **The review's own two stage-2 controls** (`runs/review_stage2.py`: the fixed stage-2 link plus one line
  in tickUnmake, exactly as the review built them; judged against the stage-2 link's digest,
  `runs/probe_mutants_review.txt`): **q2-hexclock** (`foe.hexClock += 0.5` a window frame) fails **[5]**
  by 3.8 million violations, and [2] as not exercised -- it leaves 6 clean stun runs in windows, under
  the 200-run floor the review asked for (its "MET on 6 clean runs") -- win 66.9% against 50.0%, 444 of
  444 fights changed; **q2-shrink** (`foe.reachMul = Math.max(0.4, foe.reachMul - 0.0005)`) fails
  **[5] alone**, 69.4%, 444 changed. Both win rates are the review's to the decimal. The pre-review probe
  passed both 6/6.

Every m / r mutant changes fights (counted fight by fight against the final link's digest, won or lost and
the length to the step) and fails its own check and no other (`runs/probe_mut_*.txt`; the mutant links'
shas are in `runs/mutants_build.txt`). m3 moves only the fights in which a runic foe hexes Spellbreaker
inside her window, which is why it changes 36 and not 444; m2's 17.3% is the second hex without the long
stun, the design's "stun length is worth +30". r2 first ran at the review's size, +0.5 a frame (`runs/probe_mut_r2-hexclock-0.5.txt`): it failed [5] by 4.1
million violations and [2] as not exercised, because a proc on almost every frame leaves 3 clean stun runs
in windows to measure; at +0.01 the stun is still measurable and [5] catches it alone. The probe moves no
fight: the final's 444 fights and m1's, played with no hooks at all, give the probe's digests to the fight
(`runs/plain_digest_b7.5.txt`, `runs/plain_digest_m1.txt`).

## 4. Stage 5: the blade — 7.5, the measured point nearest the shipped rate

**The target is the design's own, the shipped rate** (§5: "Stage 3 — the blade, wide on 151 at 8.3 / 8.5
/ 8.8 to the shipped rate"; §3: "x2 is 55.2 against a shipped 49.7 and the blade (8.81) comes to about
**8.4**, the row floor"). The shipped rate on 151 is the bolt's **48.6%** on these same fights (§0).
**The pick is the measured point nearest it** (the batch's redesign blade policy: "the target is the
relic's shipped win rate measured BOTH SIDES on the base ... and the pick is the measured point nearest
it"), and the 50% crossing is recorded beside it.

**Changed after the review (finding 4).** The pre-review build carried 8.30, the twinblade row's floor
(54.3%, +83 wins, ~4 standard errors over the target), and kept 7.5 as "Rick's choice under the row",
reading v79 §3 / §6.3 as leaving a blade under the row to Rick. The review was right: no v79 sentence
bounds the x2 blade by the row -- §6.3's "x3 needs a blade under the row" is about the x3 option, and §3
only predicts that x2 "comes to about 8.4, the row floor" -- and the row's numbers (8.3-11.95) are v76's
and the base's, not the design's (rule 0). **The carry is now 7.5**; 8.30 is kept, built and proved as
`--alt-row`, and 7.7 as `--alt50`.

Both sides (`relic_rate.py --game sc-spellbreaker-unmaking.html --relic spellbreaker --n 10 --seed0 X
--set dmg=Y`, each seed from both sides, every other relic a foe, 10 seeds a foe a side, 740 fights a
block, seed0 2207 and 2317; 8.81 is the link itself; `runs/stage5_rr_*`, table `runs/stage5_table.txt`).
The grid ran on the pre-review stage-3 link (29c3ea7b9e3e5f91); **the fixed links reproduce it exactly**
(`runs/n1_inert.txt`: the fixed `sc-spellbreaker-unmaking` at 8.81 and the three stage-5 links, with no
`--set`, give the grid's 8.81, 8.3, 7.7 and 7.5 rows field for field on both blocks, 5920 fights), so the
review's two notes move no fight and the grid stands:

```
blade                        block 1   block 2   pooled (1480)     side A   side B   mean     against the shipped 720   against 50%
8.81 SHIPPED (the bolt)      48.5      48.8      48.6 (720)        49.1     48.2     74.6s    the target
8.81 the Unmaking            59.6      58.6      59.1 (875)        63.1     55.1     81.8s    +155                      +135
8.8  the brief's grid        60.4      58.5      59.5 (880)        63.9     55.0     81.7s    +160                      +140
8.5  the brief's grid        55.5      58.4      57.0 (843)        58.8     55.1     82.7s    +123                      +103
8.3  the brief's grid        55.3      53.2      54.3 (803)        56.6     51.9     83.4s    +83                       +63     <- Rick's: the row's floor (--alt-row)
8.2                          52.2      53.8      53.0 (784)        53.5     52.4     83.6s    +64                       +44
8.1                          54.1      53.2      53.6 (794)        53.8     53.5     83.9s    +74                       +54
8.0                          55.5      54.5      55.0 (814)        57.6     52.4     84.3s    +94                       +74
7.9                          51.2      53.0      52.1 (771)        52.0     52.2     84.4s    +51                       +31
7.8                          50.7      51.2      50.9 (754)        53.6     48.2     84.7s    +34                       +14
7.7                          49.2      50.3      49.7 (736)        51.4     48.1     84.8s    +16                       -4      <- Rick's: 50% (--alt50)
7.6                          49.3      49.5      49.4 (731)        49.7     49.1     85.3s    +11                       -9
7.5                          49.2      49.2      49.2 (728)        50.9     47.4     85.5s    +8                        -12     <- THE BLADE: nearest the shipped rate
7.4                          45.9      48.5      47.2 (699)        49.7     44.7     85.6s    -21                       -41
7.2                          45.5      43.0      44.3 (655)        42.0     46.5     86.3s    -65                       -85
7.0                          42.6      42.0      42.3 (626)        42.4     42.2     86.6s    -94                       -114
```

- **The brief's grid is all above the target.** At the shipped blade the Unmaking reads 59.1 against the
  shipped 48.6; the design's "about 8.4" was priced on the lab's clock, side A, where the built relic
  reads 5-7 lower at 8.81 and 9.1 lower at 7.5 (§2, m1 both sides). The line through the fifteen points
  (9.0 points a unit of blade; residuals within ±2.5, the largest 8.0's +2.5) puts **the shipped rate at
  7.57 and 50% at 7.72**.
- **The brief names no knob to move first.** The shrink is the arm §3 passed over, and "x2 or x3" is
  Rick's (§6.3), and x3 goes the other way. It is said here: no knob moved.
- **The twinblade row is 8.3-11.95** (Twinshade and Starwarden at 8.3; Widowmaker 11.95; v76 §3 names it
  "the twinblade row: 8.3–11.95"). The shipped rate lies 0.73 of a blade under the row's floor, which is
  also the brief's lowest grid point. The design gives no bound on the x2 blade (the review's finding 4:
  §3 and §6.3 speak of the row only for x3), so the blade policy decides: **the carry is 7.5, the measured
  point nearest the shipped rate: 49.2% (728 of 1480, +8 wins, +0.5 points over the shipped 48.6; one
  point's standard error is ~1.3), side A 50.9, side B 47.4, mean 85.5s** -- 7.6 reads +11 and 7.4 -21.
  It is UNDER the brief's grid and UNDER the twinblade row, and that is flagged for Rick (§6). Nothing was
  bisected: the brief's three points and 8.81 were read first, then 8.2, 8.1, 8.0 and 7.9-7.0 to place
  the crossings.
- **Rick's two other choices, each one number away and each built, proved and probed:**
  - **the twinblade row's floor and the brief's lowest point: blade 8.30**, 54.3% (803 of 1480, +83 wins
    over the shipped rate), side A 56.6, side B 51.9, mean 83.4s: `--stage 5 --alt-row`,
    `sc-spellbreaker-b8.3` (dade2e086be0a8cb) -- the pre-review carry;
  - **50%, the batch's standard for a new relic: blade 7.7**, 49.7% (736, -4 from half; 7.8 reads +14),
    side A 51.4, side B 48.1, mean 84.8s: `--stage 5 --alt50`, `sc-spellbreaker-b7.7` (586b23089cf9674c).
- **The built links are the measured relics** (`runs/stage5_rr_proof_*.txt`, on the fixed links):
  `relic_rate` on `sc-spellbreaker-b7.5` with no knob set reproduces the `--set dmg=7.5` run on both
  blocks exactly (49.19% / 49.19%, side A 53.78 / 48.11, side B 44.59 / 50.27, mean 85.768649s /
  85.244216s, all 37 foes and every type); so do `sc-spellbreaker-b8.3` against `--set dmg=8.3` (55.27% /
  53.24%, mean 83.639568s / 83.232135s) and `sc-spellbreaker-b7.7` against `--set dmg=7.7` (49.19% /
  50.27%, mean 84.671986s / 84.988230s).
- **Against the reference:** Spellbreaker as shipped reads 48.6% both sides on the base (side A 49.1,
  side B 48.2); the redesign at 7.5 reads 49.2% (50.9 / 47.4), at 8.3 54.3%, at the shipped 8.81 59.1%.
  Her fights run longer: 85.5s against the bolt's 74.6s (the foe's weapon spends 60% of a window
  stopped, and a lighter blade takes longer to kill).
- **The side split.** At 7.5 side A reads 3.5 over side B; over the fifteen points the split averages
  +3.0 (from -4.5 to +8.9; one point's split has a standard error of ~2.6, and the points share their
  fights, so they are not independent readings). The stub (no ultimate) splits +1.2 and the shipped bolt
  +0.9. The probe reads the mechanism the same from both sides (§3), so the split is in the fights, not
  the build. Reported, not chased.

**The ladder at 7.5** (40 fights a foe, both blocks, both sides; `runs/ladder_b7.5.txt`), beside the
shipped bolt's (the pre-review ladder at 8.3 is `runs/prev/ladder_b8.3.txt`):

```
by type       Unmaking 7.5   the bolt 8.81
greatsword    68.6%          64.3%     +4.3
bow           60.4           57.5      +2.9
flail         46.4           42.5      +3.9
warhammer     45.0           46.7      -1.7
twinblade     35.6           45.0      -9.4
scythe        34.3           35.4      -1.1
```

By foe: best Redflail 92.5%, Farwarden and Axiom 87.5, Lightkeeper 85, Marrowdraw 82.5, Nightfell 80;
worst **Bloodmirror 0% (0 of 40)**, Twinshade, Vinesower and Morningstar 10, Shroudmaul 17.5, Foregone
and Duskreave 22.5. The largest moves against the bolt: Bindweed +35.0 (17.5 -> 52.5), Nightfell +30,
Vesper, Portcullis and Thornwake +20, Censer +17.5; Shroudmaul -25.0, Duskreave and Morningstar -22.5,
Vinesower -20, Dawnbringer, Twinshade and Bloodmirror -17.5, Starwarden -15. Stopping a weapon pays
against the slow heavy heads (greatswords, flails) and nothing against the scythes; at the lighter blade
the twinblades (Twinshade 10%, Bloodmirror 0%) and the fast scythes run away from her, which is the
price of the blade the policy picks (flagged, §6).

### 4a. The gates on the final link (`sc-spellbreaker-b7.5`, re-run after the review)

- **engine_ab sc-tendril-t3 -> sc-spellbreaker-b7.5, the 37 others (every base id but Spellbreaker's,
  `runs/ids37.txt`), n=6: 3996/3996 identical** (`runs/engine_ab37_b7.5.txt`; 37/37 distinct winners,
  3996 distinct seeds, 21.5-115.1s). The redesign moves no other relic's fight. **Control:** the same gate
  with Spellbreaker IN (`--ids spellbreaker,axiom,grudgebearer,twinshade --n 6`): **18 of 36 differ**,
  exactly Spellbreaker's 18 fights (3 pairings x 6 seeds); the other three pairings' 18 fights are
  identical (`runs/engine_ab_control_with_spellbreaker.txt`).
- **verify --n 40 on sc-spellbreaker-b7.5 (38 relics, 703 pairings, 28120 fights): 10/13, the base's
  three red checks and no new red check** (`runs/verify_b7.5.txt`; the base's, `06-docs/v101/runs/verify_t3.txt`,
  10/13 with the same three). Spellbreaker **48.9%** (the base's verify read the bolt at 49.9%); every
  relic in 30-70% (Heartwood 30.7 .. Gloamwire 63.9). The reds, and whose: (1) "both sides can win every
  matchup": Heartwood v Twinshade 0/40 and Heartwood v Bindweed 0/40 (the base's, Heartwood's) **and,
  new at this blade, Spellbreaker v Bloodmirror 0/40** -- hers: at 7.5 she never beats Bloodmirror in
  verify's 40 fights, as in relic_rate's 40 (§4's ladder, 0 of 40; at the pre-review 8.3 she took 2 of
  40 there and the pairing was not red, `runs/prev/verify_b8.3.txt`); flagged for Rick with the blade
  (§6); (2) "every pairing mean duration in 18-70s", Gravemourn/Ironhail 38.6s .. **Spellbreaker/Starwarden
  104.3s** (the band was red on the base at Farwarden/Starwarden 100.0s; her longer fights make its long
  end); (3) "overall mean duration in 28-54s", **61.4s** against the base's 60.8s (her fights run ~11s
  longer than the bolt's). No timeouts in 28120 fights.
- **tip_audit:** identical to the base's (`runs/tip_audit_b7.5.txt`, `runs/tip_audit_base.txt`), but for
  the file name. It audits the STATUS tips, which this build does not touch: Hex still says "0.2s weapon
  stun, more often per stack", true outside a window; inside one the ultimate's own card says the rest
  ("Hexes stun the foe's weapon twice as long"). The card (68 characters, under the 72 budget) is the
  builder's check.
- **chain_audit** `--builder spellbreaker_build.py`, with relic = tip = sc-spellbreaker-b7.5: **ALL 10
  INSERTS SURVIVE**, the blade (`S5`, `dmg:7.5,`, on no other row of any tip) among them
  (`runs/chain_audit_b7.5.txt`). **Controls:** the same relic against `sc-spellbreaker-unmaking` as the
  tip (Spellbreaker back at 8.81) reads `LOST S5` and exits 1 (`runs/chain_audit_control_blade.txt`);
  against the base, all 10 LOST (`runs/chain_audit_control_base.txt`). (Why `--alt-row` writes `8.30`:
  a builder copy whose carry wrote `8.3` read "ALL 10 INSERTS SURVIVE" on the 8.81 tip, its marker found
  in Twinshade's and Starwarden's rows: `runs/prev/chain_audit_control_plain83.txt`.)
- **The builder:** every link rebuilds byte-identical, the refusals write nothing
  (`runs/rebuild_final.txt`); 27 negative copies refuse (`runs/builder_negtest.txt`); stages 1-5 compose
  on 23 tips (`runs/compose_s5.txt`).
- **The probe** 6/6 on stages 2 and 3, the final and both alternatives; eleven mutants, each its own check
  alone, and the review's two stage-2 controls caught (§3).

## 5. Stage 6: the picture and the voice — `sc-spellbreaker-b7.5-fx`

Design §4 (the picture, the sound) and its §5 brief stage 4, "picture, voice, carry; bolt's field spec out;
`engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched", this build's stage 6. Picked on
measurements under Rick's "you pick i overrule" by two labs (the picture lab's scratch, `sb_rows.py`, and
`tools/spellbreaker_voice_lab.py` 3a119da162e2dd1a), and built as `spellbreaker_build.py --stage 6` on the final
stage-5 link (the b7.5): **fifteen anchored edits (voice 3, picture 12)**, byte-exact to the labs' own row
files (voice `rows_final.json` 090b35214e0efe05, picture 6a3c73a527df3e45; copied as
`runs/stage6_voice_rows.json` and `runs/stage6_picture_rows.json`). The reports the two labs returned, as the
orchestrator relayed them, are the files: their first 4999 and 7000 characters are the files' own JSON
(`{"rows": [...]}`, compact), read at the opening, a middle row and the last characters before the relay's
cut, and a one-character change to any of those fails the check (`runs/stage6_check_inline.txt`).

```
sc-spellbreaker-b7.5.html          stage 5  the blade (the base of stage 6)                     da7936dccd8f5f15
  -> sc-spellbreaker-b7.5-fx.html  stage 6  the picture and the voice (presentation)          ceeff797e5739e0c
```

- **The rows, reproduced** (`runs/stage6_gen_s6.txt`; the generator is `runs/gen_s6.py`, the pattern's: rows
  == files, the stamps, no nested anchor, merge by anchor line, a table written with triple-quoted strings,
  refusing a builder that already carries S6): the picture rows alone give the picture lab's stamp,
  **176458b0df4a79cd** (its `sb-final.html`, byte for byte); the voice rows alone the voice lab's end-to-end
  page, **149b777b7f1ccb90**; both sets, either order and all fifteen reversed, **ceeff797e5739e0c**, the fx
  link. No two rows share an anchor line, so none is merged; no row's anchor sits inside another row's anchor
  or code, and no two anchors' spans overlap. **Eleven re-emit their anchor and four replace it**: three
  consumed, all Spellbreaker's own -- drawUltOver's bolt branch, the banner seat map's narrowest token
  `spellbreaker:1, ` and the life map's ` spellbreaker: 1.4,` (Thornwake's and Emberedge's seats and the other
  life entries on the same lines are left to their own builds) -- and drawWeapon's dim line, replaced by its
  own text with the grey's alpha in it. Twenty-three new names (`tickUnmaking`, `drawUnmaking`, the `_unmk*`
  methods and the renderer's `_unmkGreying` flag, `UNMAKING_RUNES`, the eleven `unmk*` fields, a tag's `unmk`,
  the two voice ids), each free on the base on identifier boundaries and each in the page after.
- **Composition.** The Sfx row goes BEFORE the shared rune-crack fallback, which it re-emits unchanged, so the
  eleven other relics that still fall through keep it (Lastlight, Ironhail, Lightkeeper, Farwarden, Aureole,
  Censer, Oathwound, Heartwood, Gloamwire, Portcullis, Bindweed, on the b7.5) and another relic's arms anchored
  there apply in either order. The two voice rows on the sim path ride on stage 2's own lines (after the hex
  proc's `breakSpin` call in tickStatus; before the window's close line in `tickUnmake`); the picture's fields
  follow stage 2's fields, and `tickUnmaking` follows `tickUnmake`'s end; its call and methods sit beside shared
  lines (`tickPresentation`'s first call, `drawTree`'s world-pass call, the fx banner comment, `shellHash`,
  `drawWeapon`, the per-blade `f.ultDraw` test) and re-emit them. **compose6** (`runs/stage6_compose6.txt`,
  **0 FAIL**): stages 1, 2, 3, 5 and 6 on the same 23 tips as `compose_s5` -- the base, every newer link of the
  batch line on `02-chain/` up to `sc-aureole-fxout` and `sc-censer-fxout` (42 relics), and the in-flight
  builds' scratch tips. On every tip the change set of stages 1-5 is the base's (md5 83845082c07f, 85 lines)
  and **the change set of stage 6 alone is the base's, md5 2e2d2e985dab (409 lines), on all 23** -- no tip
  takes different lines (Aureole's Censer-tip life-map blank line has no counterpart here: the line that
  carries Spellbreaker's life token keeps Thornwake's and Gravemourn's on every tip). The picture lab also carried its rows with the voice rows onto 12 tips (and 62 orders
  of its own rows), both orders equal (`runs/stage6_picture_order.txt`).
- The picture sheet is `05-reference/v111/spellbreaker-picture-sheet.png` (03755781683bccbb); the voice lab's
  wavs are `05-reference/v111/spellbreaker-*.wav` (25 files, 4.0 MB, raw level; gitignored).

### 5a. The picture

Every number here is the picture lab's: headless Chromium 151 at 540x960 with the post chain on (m1 and m2,
the second on the final bytes, identical: 10 fights, 95 frames, white, dark and ordinary foes;
`runs/stage6_picture_m2_summary.txt`), on its shipped-look page (the rows, with the bolt's `SPECS.spellbreaker`
taken out of the inlined `fx.js` as the carry will: 27f6d27e31a936f7, which is `fx_remove.py`'s own cut of its
rows page, byte for byte).

- **The script** (v79: "rune-script runs along both blades and stays (runic `core` glyphs, 0.3s)"): five runes
  a blade from an eight-stave alphabet (`UNMAKING_RUNES`, angular staves, the look of a carved futhark), drawn
  IN each blade's own frame after its shape: written hilt to tip over the cast's 0.3 s behind a bright writing
  point (a glow in the school's glow and a white core), standing for the window, and **unwritten tip to hilt
  over 0.2 s** at the close -- a clock close, a death or the verdict. Each rune rides its shard's own drift and
  cant (the numbers `_twinConjured` hands the conjured blade's shards), so the script is in the weapon rather
  than painted over it, sized off the blade's profile; `core` over a keyline in the silhouette's ink with a
  glow line (the conjured blade's middle IS core, and core on core is nothing).
- **The rune motes** ("rune motes off the blades"): small runes of the same alphabet shed off both blades while
  the window is open (8 a unit of the presentation clock a blade, at most 48 alive), left where they were shed
  and drifting outward, turning, fading in and out over their 0.55 s; placed by `shellHash` on their count (no
  RNG); in the world pass under both balls, source-over, clipped to the live hall -- nothing under `lighter`
  and nothing the bloom sees. They outlive the window by their own life.
- **The grey** ("the foe's weapon greys out (desaturated, alpha 0.6) for the stun's length, so a longer stop is
  a longer grey"): while a DOUBLED hex stun runs, the whole weapon is drawn through the canvas's own
  `grayscale(1)` -- every school, every type, the glow sprite and the lit blit alike -- at the design's alpha
  0.6, where a plain stun keeps the base's 0.42 dim in its colours. It keys on the HEX PROC, not on the stun
  (`f.stun` has many writers: clashes, pins, freezes): a drop in the fighter's `hexClock` (nothing else resets
  it; the builder asserts the base's three writers) with the `hexStunMul` last seen, which is the factor the
  proc read. It lasts that stun's own `stunFor x mul`, counted down with the fighter's stun (frozen through a
  hit stop as the stun is, gone when it is, never past its own length under a longer stun). So an x1 proc
  never greys a weapon, and a doubled stun is grey for exactly its 0.4 s.
- **The tag** ("the hex tag counts by two"): a step her `unmakeTally.extra` rose is a step a blow of hers
  landed its second hex; the HEX tag that blow pushed is relabelled `HEX +2`. Not the killing blow (no second
  hex), not the match's first hex (its teaching panel prints no count), never a tag on her own ball.
- **The bolt's art is retired** ("the bolt art is retired"): drawUltOver's `u.w === "spellbreaker"` branch (the
  jagged bolt with its glyphs and the cage of rings that closed on the target; it drew `Math.random`, and the
  page's count goes 13 -> 12), the banner's seat on the quarry (`onTarget`: the name now lands on her, the
  default seat; on her in 66 of 66 casts) and the life entry 1.4 (the cast's record falls to the map's own 1.5
  and nothing draws from it). **Kept, declared:** the charge rune `ULTSIG.spellbreaker` (a rune coming apart:
  the name's, not the bolt's) and the banner's letter scatter (the name's arrival).
- **The silhouette is left alone:** Spellbreaker's resting blades read |dL| 0.289, 1st of the 5 twinblades
  (Widowmaker 0.171, Starwarden 0.156, Twinshade 0.151, Thornshear 0.144; `runs/stage6_picture_sil.txt`).
- **The art hangs off the Fighter** (`unmkFade`, `unmkAge`, `unmkOut`, `unmkMotes`, `unmkMoteAcc`, `unmkMoteN`,
  `unmkSeenX` on her; `unmkGrey`, `unmkHC`, `unmkMul`, `unmkStun` on every fighter, as the weapon the Unmaking
  greys), never off `m.ultFx` (open item 25); `tickUnmaking` drives it in `tickPresentation` (half-seconds, as
  every `life` there), and `drawUnmaking` / `_unmkMotes` / `_unmkScript` / `_unmkGreyed` draw it, one method a
  component, so each can be measured alone.
- **Bloom** (the design's gate, <= +0.02): the picture's share of the chain's arena lift **max +0.0000** (min
  -0.0002); the raw luma it adds (chain off) at most +0.0011 -- the script and the grey are drawn with the
  weapon, the motes on the floor, all in the world pass. **Three controls, each failing:** the grey as LIGHT (a
  white `lighter` disc of the foe's reach at 0.35 over a greyed weapon) lifts +0.0741 (past 0.02 on 7 of 23
  greyed frames) and pushes the foe's disc past 0.90 on 14/23; a white-hot `lighter` glow on her while the
  script stands, her disc past 0.90 on 66/79 window frames; a white `lighter` disc over the greyed foe, 21/23.
- **No disc erased:** the art moves her disc at most +0.0003 and a foe's at most 0.0009 (tags aside), and no
  frame is newly past 0.90 (hers 3 with / 3 without of 95; the foe's 7 / 9). By the foe's school: dwarven
  0.0000, sanctified 0.0009, umbral 0.0007, verdant 0.0003 at most.
- **Legibility** (median |dL| of each component's own pixels, out of a hit stop / in one): **the script 0.210
  standing / 0.207 in a stop**, 0.148 while it writes (0.101 in the cast's own stop), 0.211 / 0.195 unwriting;
  the motes 0.201 / 0.209; HEX +2 0.254; **the grey 0.042 in luma and 0.069 in chroma against a plain stun**
  (0.059 in a stop).
- **The grey, compared** (`runs/stage6_picture_greycmp.txt`, 48 greyed frames, 12 foes, 7 schools, each
  against the same frame's plain stun and its unstunned weapon): **A, the design's words, `grayscale(1)` at
  0.6: |dL| 0.044, |dC| 0.075 against the plain stun** (0.158 / 0.107 against the free weapon; the base's own
  plain stop reads 0.181 / 0.084 against it); B (grayscale, contrast 0.6) 0.036 / 0.072; C (grayscale,
  brightness 0.7) 0.029 / 0.072; D 0.034 / 0.071; E (grayscale at the plain stun's 0.42) 0.001 / 0.077. A is
  the best of five on both, and the pick. **Flagged: the grey is mostly a colour cue** -- it reads least on the
  near-white sanctified weapons (dL 0.062, dC 0.016: the alpha carries it there).
- **Whole fights** (the lab's verify, `runs/stage6_picture_verify.txt`: 18 fights, 16 with Spellbreaker on both
  sides -- Twinshade's copies and the runic hexers Paradox and Axiom among them -- and 2 without, each as the
  base, the rows, the shipped look, and the shipped look drawn through the renderer): **the simulation
  identical to the base in all 18**, hash at the kill, steps and result. **Control:** a copy that nudges her 1e-9
  at each relabel differs on all 16 of hers and on neither of the 2 without. Drawn through the kill and 3 s of
  the verdict: **35,959 frames, nothing thrown**; 1356 x2 procs -> **1336 grey starts, and 20 whose stun a
  Grudgebearer Crucible zeroed on the same step**; no grey without a stun, **no grey from an x1 proc**; every
  clean run **grey length == stun length, 197 of 197** (47 steps from the proc's); **HEX +2 on 314 of 315 second
  hexes** -- the 315th the match's first hex tag, its teaching panel (tagdbg: Spellbreaker v Twinshade 2207,
  t 24.483); the script's unwrite after a clock close 0.19 s (median; 0.375 at most, through hit stops), and at
  the kill to 0 in 0.19 s; the cast's record `life` 1.5 on all 83 casts.
- **The lab's own render_ab**: 77/77 frames pixel-identical on 11 pairs without Spellbreaker; two Spellbreaker
  pairs 2/7 and 2/7, the five inside a window differing (`runs/stage6_picture_renderab.txt`); its own
  `engine_ab` on the shipped look, 38 relics, **4218/4218** (`runs/stage6_picture_engine_ab38.txt`); the stages
  1-5 probe on its shipped look 6/6, the digest equal to stage 5's (`runs/stage6_picture_probe.txt`).
- **Frame cost: not measured** (deferred by the orchestrator; no Electron is launched while Rick is on the PC). §6.

**Readings declared** (the builder's docstring, 13-20; the art and the sound are Code's picks):
13. The picture reads the window off `ultUnmake && alive && !over` and keeps its own state on the fighter; the
    script is written over 0.3 s at the cast and unwritten over 0.2 s at a clock close, a death or the verdict.
14. The grey keys on the hex proc (a drop in `hexClock`, the factor last seen), never on the stun; the whole
    weapon through `grayscale(1)` at 0.6 for that stun's own length, counted down with the stun.
15. The tag: the HEX tag a second-hex blow pushed reads `+2`; not the killing blow, not the teaching panel.
16. The motes are drawn (no field), by `shellHash`, world pass, under both balls, source-over.
17. The voices on the sim path are two lines: the stun voice after the hex proc's `breakSpin` when
    `hexStunMul > 1`, and the close voice before the window's close line on a clock close with both alive;
    the cast's voice is `fireUlt`'s own prologue call.
18. No close voice on a death: the death voice has that moment; a window open at the fight's end closes in the
    picture only.
19. No `fx.js` field; the bolt's `SPECS.spellbreaker` is the orchestrator's to take out.
20. The bolt's art is retired with the bolt (its branch, its seat on the quarry, its life); the charge rune
    and the banner scatter are kept.

### 5b. No new `fx.js` field: the motes are drawn, and the bolt's spec goes out of both copies by the orchestrator

The design asks for "rune motes off the blades, both copies". A SPECS field fires once, at the cast, from the one
`m.ultFx` slot, where the caster stood. The picture lab measured what that slot gives this relic over 161
Unmaking windows (16 foes x 2 seeds, both sides; `runs/stage6_picture_fxprobe.txt`):
- the slot is Spellbreaker's a median **0.67 s** of the window clock (max 0.72; the window is 8 s): a field
  borne on it could exist for **7.0%** of the window; the opponent's cast took it in 31 windows, and it expired
  in 130;
- the motes come OFF THE BLADES and she moves: her blades' hub stands a median **193 units** from the field's
  spawn point (p10 58, p90 414), and after the first second a median 201 (p90 423) -- **more than a blade's tip
  (96 units) away on 80%** of those samples. A field spawned at the cast would shed where her blades no longer
  are.

So the motes are DRAWN, off the blades themselves, in the world pass (5a): the Zenith, Canopy, Tendril,
Quarrelstorm, Ascension, Bulwark, Consecration and Benediction precedent. **Rick's to overrule.**

The bolt's own spec, `SPECS.spellbreaker` (mode `beam`), is the brief's "bolt's field spec out". `fx.js` is
shared by every build in the batch, so this builder never edits it, and stage 6 refuses to write if its inlined
copy moved (reading 19). The orchestrator takes the entry out of both copies with `fx_remove.py --relic
spellbreaker` at the carry (no `--keep-comment`: no comment of its own sits above it -- the line above is
Oathwound's entry -- and the `BEAMS AND BOLTS` section header over Aureole's and Oathwound's stays). Its exact
text:

```
    spellbreaker: { mode: 'beam', n: 1200, sp: [40, 200], grav: -40,
                    drag: 1.6, life: [0.25, 0.70], heavy: 0.0,
                    size: [0.6, 1.8], spawn: 0.35, up: 0 },
```

The fx link's lines 32629-32631; `src/render/fx.js` on disk today (487c9de9dff7f374, Aureole's beam already
out) still carries it. **Tried in scratch twice** (`runs/stage6_fx_remove_scratch.txt`, `runs/fxout_scratch.sh`;
`fx_remove.py --fxjs` on copies, the real `fx.js` untouched, 487c9de9dff7f374 before and after):
- on the fx link, with `fx.js` at the stamp its inlined copy carries (28fc58641370a1a9, extracted from the page,
  its sha256 checked against the stamp): the block comes out whole, only the block and the two stamps move (->
  6a5b82c9a7612645, the picture lab's cut too), the page becomes b2ff3a5cd67fd631;
- **the carry, dry, on the newest real tip:** stages 1, 2, 3, 5 and 6 on `02-chain/sc-aureole-fxout`
  (da5eafafcfae06c2; its stage 5 d8e16ff49c9d63e1 is the voice lab's own carry tip) -> e2a4fd8ea4eed06f, then
  `fx_remove` with a copy of today's `fx.js` (487c9de9dff7f374 -> 7dc0123af735c83e): the page 9243277a756e84b6.

The page is safe without it (`ULTFX.sync` returns on a missing spec, the fx link's line 32988); the picture lab's `engine_ab` (4218/4218) and
whole-fight identity ran on its own spec-out page. **Until the carry, the stage-6 link still fires the bolt's
beam particles at every cast (from where she stood, toward her quarry), and so does the clip (5f).**

### 5c. The voice

Every number here is `tools/spellbreaker_voice_lab.py`'s (3a119da162e2dd1a; its final run, round 8, Chromium
151.0.7922.34; `runs/stage6_voice_lab.txt`; every render an OfflineAudioContext at 48 kHz through
`Sfx.buildChain`, a candidate rendered from its arm's own text). Its controls reproduce the six published
numbers (rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, hit@11.6 0.443 / 80 ms), and levels are read against
Spellbreaker's own blow at 7.5 (its loudest 50 ms 0.1060-0.1114 over 12 draws), the wall tick and the school's
`hex-snap` (0.0340-0.0425).

- **The cast, "a glass crack into a hum, 0.4s" -- DRONE, of 5.** The crack: three 6 kHz clicks at 0 / 4 / 11
  ms (a fracture running) and a glass rod struck at G6 (1567.98 Hz) with a bar's modes 1 : 2.76 : 5.40 -- 23.1
  dB tonal, its 2.76 mode 145 cents off any harmonic (glass, not a bell). Into **a C4 triangle hum (261.63 Hz)
  coming in at level 25 ms after it**, re-struck in phase on every whole cycle nearest 4 ms (a held note does
  not exist in this synth), each strike 30 ms: held within 0.9 dB (flutter 0.1) at -10.0 dB re the crack's top,
  releasing 30 dB over its last 0.1 s. **Audible 400 ms, gone by 405**; its top 0.0766, -2.8 dB re the blow at
  7.5 (quietest draw); the crack +30.2 dB and the hum +8.4 dB over the score; 109 synth calls. Register at most
  **0.66** (rune-crack) against rune-crack, the runic and twinblade casts with voices of their own (Axiom,
  Foregone, Paradox; Widowmaker, Twinshade, Thornshear, Starwarden), BAR, hex-snap, the blow, the death voice
  and Angelus's cast and close. REED (an E4 square, 0.76) and BUZZ (an A3 saw, 0.79) pass too; the tiebreak
  (the most distinct register, to 0.05, then the fewest calls) picks DRONE. SWELL is out (its hum moves 3.6 dB:
  not held), GLASS out (a 660 Hz hum: not low; it moves 7.2 dB). **Four controls each fail:** CRACK (the crack
  alone: audible 40 ms, no hum), HUM (the hum alone: not struck, no crack), CLICKS (the clicks without the
  glass: 5.6 dB tonal, clicks not glass), and rune-crack itself (not glass; no held hum).
- **A stun, "hex's own snap, lengthened to match (0.4s tail)" -- SIZZLE, of 5.** The school's snap played as
  itself (`this.play("hex-snap")`), its 2.6 kHz band re-struck every ~15 ms (+/-20%) and its ping rung on
  under it (a 2500 Hz triangle) at the snap's own proportions (ring over train solved to the snap's ping over
  its band in RMS, 0.996), held through the stun and falling 20 dB at its end. **The snap is there at its own
  level** (register 1.00 over its first 30 ms, its peak within 0.5 dB of the snap's); **the tail is the snap's
  own sound** (register 0.68 against it, 60-400 ms), unbroken to the stun's end (CONT -30.6 dB, no gap before
  300 ms): **audible 395-425 ms, gone by 430**; its loudest 50 ms -8.4 dB re the snap's (-8.2 re the blow, +10.9
  re the wall tick); heard +18.0 dB over the score in its tail; 30 synth calls, 1.0 ms main thread (it fires a
  median 16 times a window). Register at most 0.67 (Thornshear's cast). STRETCH is out (the snap's own lines
  lengthened: not struck, its peak at 17 ms), RING out (the ping alone rung on: tail register 0.28), RATTLE out
  (0.49, and a gap), ECHO (the snap itself re-struck every ~10 ms) passes every gate of sound but costs 126
  synth calls, 4.5 ms of main thread a stun, over the 40-call budget (round 6). **Two controls fail:** PLAIN
  (the snap alone: 25 ms, not lengthened) and TAIL (the ring without the snap: not the snap). The rule grew over
  seven rounds, each said in the lab's docstring (the per-kind length cap, ECHO's envelope, its re-strike
  interval, the cost gate, SIZZLE's ring solved to the snap's own proportion).
- **The close, "the hum cutting out" -- CUT, of 4.** The cast's hum held 0.2 s, and its strikes simply stop: it
  dies with the last one's 30 ms ring. The hum's own (262 Hz, register 0.97 with the cast's hum, -0.0 dB re its
  held level), **cut 23 ms after it starts to fall (30 dB) with no fade before it (-0.1 dB)**; audible 230 ms;
  heard +8.4 dB; register at most 0.19. SAG (sagging a fourth, cut 17 ms) and CLICK (a relay's click) pass; the
  tiebreak (register, then calls) picks CUT; STUTTER is out (it fades before it stops, -14.6 dB). **Two controls
  fail:** FADE (a 196 ms fade, not a cut) and the cast itself (it cracks).
- **Wiring** (reading 17). The cast is `fireUlt`'s own prologue call, `SFX.play("ult", { w: f.w.id })`:
  Spellbreaker had no arm and fell through to rune-crack, so the three arms go in BEFORE that fallback, which is
  re-emitted unchanged. **The stun voice** plays in tickStatus right after the hex proc's `breakSpin`, `if
  (f.hexStunMul > 1)` -- read as the proc's own two lines read it (`> 1`, not `!== 1`: a body without the field
  stays silent; a shade keeps its 1, reading 4). **The close** plays before the window's own close line, on a close BY ITS CLOCK with
  both alive; **a close by a death is silent** (reading 18), and a window still open when the fight ends closes
  in the picture only.
- **The Sfx row, applied to `Sfx.prototype.play`'s own source:** the arms equal their candidates (worst
  8.9e-08); 138 other voices unchanged through the patched play (worst 2e-07: every hit weight and crit, the
  heal chime at n 0-6, 92 ult ids and every kind `play()` names); `ult/spellbreaker` is no longer rune-crack
  (0.730 apart) and the bare fallback still is (4e-08). Main-thread cost a call: the cast 2.0 ms, the stun 1.0
  ms, the close 0.9 ms. With Angelus's, Aureole's, Censer's and Lightkeeper's Sfx rows (the batch line's other
  arms): both orders render every arm alike (worst 1.3e-07).
- **The lab's wire run** (the tickStatus and tickUnmake rows applied to the prototypes' own sources beside the
  originals; 148 fights, Spellbreaker both sides x every foe, seeds 111601-2): **148/148 identical** (both
  fighters' hp, positions, velocities, charges, facing, stun, hex clock, `hexStunMul`, hex stacks, the tallies,
  the winner, and a digest of every step), every other SFX call identical in order and options. **712 casts, 712
  cast voices; 11,726 hex procs at x2 (all on the foe), 11,726 stun voices; silent: the 7878 x1 procs on the
  foe, 642 on Spellbreaker, 112 on shades; 639 clock closes, 639 close voices, and none on the 17 closes her
  death made or the 56 windows the fight's end cut off.** **Control:** the rows plus one sim write (the stunned
  fighter nudged 1e-9 on a stun voice) leave 0/148 fights identical.
- **End to end**, the three rows applied as text (da7936dccd8f5f15 -> 149b777b7f1ccb90, +5685 chars) and loaded
  fresh: the three new voices through the page's own `SFX.play` equal the candidates (worst 6.0e-08); 138 other
  voices unchanged (1.5e-07); 74/74 fights identical to the unpatched page's, and in every one cast voices =
  casts, stun voices = lengthened procs, close voices = clock closes. The same on the carry tip (stages 1-5 on
  `sc-aureole-fxout`, d8e16ff49c9d63e1): 82/82.
- **A real window** (Spellbreaker v Ironhail, side B, seed 111601; the cast at 30.89 s, a clock close at 40.20
  s, 26 stun voices), each event over the fight's own sounds and the score, in the third-octave where it stands
  highest: **the crack +29.5 dB at 1.6 kHz; the hum +15.3 dB at 252 Hz; the stun tails a median +20.6 dB; the
  close's held hum +8.6 dB at 252 Hz.** The AFTER control (0.8 s past the close, no new voice) reads NOT heard
  for every voice; the LEVEL control (each voice 20 dB under) reads lower for every event heard.
- **Flagged for the batch:** every voice lab so far used `ult/spellbreaker` as its rune-crack control; after
  this row it is not rune-crack. A later lab must use an id with no arm (this lab used `__fallback__`).

### 5d. The probe's stage 6: [7] the voices, [8] the picture's hook

`spellbreaker_probe.py` is now 05f85277955137f9 (stages 1-5's was 26434231bb955cf8, kept in scratch as
`s6/spellbreaker_probe.pre6.py`). Checks [1]-[6] test and print what they did: the new code rides in the same
wrappers under counters of its own, and **every name [1]-[6] counts keeps its number of `inc` sites**
(`runs/stage6_counter_clash.txt`, PASS: 71 names kept, 40 added, none inside an old template). Two checks are
new, one for each half of stage 6, and **the link itself switches each one on** (the stun's arm,
`spellbreaker-stun`, in `AC.SFX.play.toString()`; `tickUnmaking` on the Match), so the same probe still reads
[1]-[6] alone on a link without stage 6. Once a fight is over it steps 2 s more of the verdict (the step's `over`
path, the presentation clock only) for these two checks alone.

- **[7] the voices.** `SFX.play` is wrapped for the run (put back after it) and every call recorded with where
  it was made. Spellbreaker's three arms are read; **a ward's shatter plays its own crit HIT voice inside
  `hurt()`**, which is not one of them, and so it cannot pass or fail [7]; nor can another relic's cast. It
  fails:
  - a Spellbreaker cast without exactly one cast voice (w "spellbreaker"), inside `fireUlt`, or the cast voice
    anywhere else;
  - **a tickStatus call whose voices are not exactly one stun voice for each hex proc [2] saw at more than x1**
    -- the proc's own factor, read inside its `breakSpin` -- **and none for a proc at x1**, on any body (the foe
    in and out of a window, Spellbreaker, a shade);
  - **a tickUnmake call whose voices are not exactly the close voice for each window closing by its clock with
    both alive, and never on a close by a death** (the windows [1] reads, with its own close rule);
  - any of them in the picture's hook, a drawn frame or the verdict;
  - and every one of the run is accounted for: cast voices = casts, stun voices = the x2 procs, close voices =
    clock closes; and x1 procs, a death close and the verdict must each have been seen silent (NOT EXERCISED
    otherwise).
- **[8] the picture's hook.** `tickUnmaking` (the picture's one call on the step path) is wrapped. It fails a
  call that changes either fighter or a shade (every own number, flag and string but `unmk*`, every array's
  length, every status, the window, the tally, the weapon row and its ult) or the match (every own number, flag
  and string, every array's length, every shot's x, y, vx, vy and life; the tags by membership), or draws the
  RNG, or plays a voice. And the picture as declared, **rebuilt from what the simulation did** -- never from the
  picture's own fields (readings 13-15):
  - **the script:** not up (`unmkFade` 1) in an open window (`ultUnmake`, the match live, the caster alive), its
    write clock not the presentation clock since the cast, up with none, or a close that is not a fade to 0 over
    exactly 0.4 of its clock (0.2 s) -- by the clock, on a death or at `over`;
  - **the motes:** a mote born outside a window, off her blades (further from her centre than the ball, the
    blade and its width), or not at the rebuilt shedding rate (8 a clock unit a blade), past its 1.1 or the cap
    of 48;
  - **the tag:** every HEX tag pushed by a blow of hers that laid the second hex (read in `resolveHit`, where [4]
    audits the second hex) must read `+2` at the next picture call, the match's first hex tag (its teaching
    panel) must be left alone, and **no other tag may ever be relabelled**;
  - **the grey:** on each fighter, rebuilt from the hex procs **tickStatus ran** (the proc [2] reads, with its
    own factor) -- never from the hex clock the picture watches: an x2 proc starts it at stunFor x mul, clamped
    to the fighter's stun; it counts down with the stun, never rises but at such a proc, and is 0 whenever the
    stun is. So an x1 proc never greys a weapon;
  - the foe carrying the script or the motes; a fresh Match's fighter carrying any of it; the script up or a
    mote alive after 2 s of the verdict.
- **The drawn subset** (`--drawn N`): the first seed's fights, both sides, every foe, drawn through the renderer
  (`AC.__draw`, the post chain off, 270x480) every Nth step while the picture shows (the script, a mote or a
  grey) and every 60th otherwise, through the kill and the verdict; [8] fails a drawn frame that throws, draws
  the match's RNG, changes the simulation or a tag. It runs on any link, so the base's draws are its control.
  A frame costs ~72 ms here at idle priority with Rick on the PC, so the subset runs apart, at `--drawn 24`
  (the default 6 took 456 s for 6 fights).

### 5e. Stage 6's gates — every one able to fail

- **engine_ab b7.5 -> fx, ALL 38 WITH Spellbreaker, n=6: 4218/4218 identical** (`runs/stage6_engine_ab38.txt`;
  703 pairings, 38/38 distinct winners, 4218 distinct seeds, 22.7-121.8s; the ids `runs/ids38.txt`).
  Presentation moves no fight, Spellbreaker's own included. **Control:** the b7.5 against `mP1` (below: its
  picture nudges the foe 1e-9 at a HEX +2 relabel) with Spellbreaker, Farwarden, Dawnbringer and Twinshade at
  n=6: **FAIL, 18/36 differ** -- Spellbreaker's 18 (she is in 3 of the 6 pairings); the other 18 fights have no
  Unmaking and are identical (`runs/stage6_engine_ab_control.txt`).
- **spellbreaker_probe (05f85277955137f9): 8/8 on the fx link** (`runs/stage6_probe_fx.txt`): 444 fights,
  Spellbreaker both sides x 37 foes x 6 seeds. **[1]-[6] print every line the b7.5 prints**, and all 71 of their
  counters, the tallies, the win rate (48.2%) and the per-fight digest are equal (`runs/stage6_probe_cmp.txt`,
  PASS): 4.73 casts a fight; 3.99 blows and 3.93 second hexes a cast, 2.000 hex a blow on a live body in windows
  (8246 blows); the doubled stun 0.4000 s over 4072 clean runs and the plain 0.2083 s over 19,550; 13.7% of
  window steps frozen; a window 9.22 s of match time. **The new probe on the b7.5 itself** (`--drawn 0`) reads
  6/6, every line as `runs/probe_b7.5.txt` (the stages 1-5 probe's own run) and all 71 counters, the tallies and
  the digest equal, and says "stage 6: not on this link" (`runs/stage6_probe_b7.5.txt`). Then:
  - **[7] the voices:** **2098 cast voices for 2098 casts**, each inside `fireUlt`; **34,875 stun voices for
    34,875 hex procs at x2** (all on the foe, in windows), **and none for the 26,958 at x1** (24,693 on the foe
    outside windows, 13 on a cast's own step before the recompute, 1896 on Spellbreaker, 356 on shades);
    **1891 close voices for 1891 clock closes, and all 42 death closes silent**; silent through 2 s of the
    verdict in all 444 fights (165 with the sim's window still open);
  - **[8] the picture:** 8,663,362 `tickUnmaking` calls, none of which changed the simulation, drew the RNG,
    played a voice or moved a tag; 888 fresh fighters clean; the script up, its write clock exact, on every one
    of the 4,142,509 calls in an open window, in 2098 windows (148,923 of those calls writing, the first 0.3 s);
    **every close a 0.2 s unwrite**: 1889 by the clock, 5 on Spellbreaker's death, 204 at `over` (165 with the
    sim's window still open; the arithmetic of [1]'s 1891 clock closes and 42 death closes: the other 37 death
    closes and 2 clock closes fell on the step the match ended, where the picture sees `over`); 551,866 motes
    born at the rebuilt rate, each checked on her blades, and motes still drifting on 262,385 calls after a
    close; **HEX +2 on all 8240 second hexes' tags** (6 more second hexes pushed the match's first hex tag, its
    teaching panel, left alone; no second hex without a tag; no other tag ever relabelled); **the grey: 34,875
    starts, one at each x2 proc** (258 of them onto a stun already zeroed on the same step, so no grey), on for
    2,288,353 calls and 249,329 more in hit stops, and **an x1 proc never starts one**: 22,295 calls followed a
    proc and found no grey, the rebuilt value too (the x1 procs on an ungreyed weapon and those 258; the probe
    prints the count as "after an x1 proc", which is those two together); after 2 s of the verdict the script and the motes gone in all 444 (208 up at `over`); 155 fights
    end with a doubled stun running, its grey frozen with it;
  - **the drawn subset** (`runs/stage6_probe_fx_drawn.txt`, the first seed, 74 fights, `--drawn 24`): 8/8; **23,211 frames through the renderer** (17,012 with the picture up, 2684 of them
    in a hit stop and 10,020 with a weapon greyed; 528 in the verdict), none of which threw, drew the match's RNG or
    changed the simulation or a tag; and the 74 drawn fights' digest is the undrawn run's, fight for fight (1509 s
    in the page at idle priority). **The base, drawn** (the b7.5, the same subset on 6 foes, 12 fights;
    `runs/stage6_probe_b7.5_drawn.txt`): its drawn check passes on 1972 frames (every 60th step: nothing of stage
    6's to show), and [2] reads NOT EXERCISED, as it must on 12 fights (its 200-run floor).
- **The probe's controls**, scratch copies of the fx link with one edit each (`runs/mutants6.py`, their hashes
  in `runs/stage6_mutants_build.txt`; the first seed, both sides, every foe, 74 fights; the table is
  `runs/stage6_mutant_table.txt`), each failing its own check and passing the others:

```
mutant           sha16             breaks  probe  fails (count)                 fights vs the clean link   win   how
mV1-closedeath   3cf453b0f91652eb  [7]   7/8    [7] 5x                         identical (74)              58.1  the close voice on EVERY close, a death's too
mV2-stunx1       3d7c8a70dbbc7542  [7]   7/8    [7] 4814x                      identical (74)              58.1  the stun voice on EVERY hex proc, x1 too
mP1-picwrite     e100235213985f12  [8]   7/8    [8] 1382x                      72 of 74 differ             43.2  tickUnmaking nudges the foe 1e-9 at a HEX +2 relabel
mG1-greyx1       00222f5de489f387  [8]   7/8    [8] 206960x                    identical (74)              58.1  the grey on EVERY hex proc (a plain stun greyed)
mD1-drawwrite    504e0e6086faf7fd  [8]   6/8    [8] 2631x [2]  n.e.            12 of 12 differ             50.0  drawUnmaking nudges side a 1e-9 when it draws (drawn only)
```

- The clean fx link on the same 74 fights reads 8/8 (`runs/stage6_probe_fx_s1.txt`, 58.1%), and mV1, mV2 and mG1
  leave its fights and win rate exactly as they are: a voice and a grey are presentation, so the three
  presentation-only faults are caught by the checks that read the presentation, and by nothing else.
- mV1 fails on the death closes ("the Unmaking's ticker played ["spellbreaker-close"], want []", 5 in the 74
  fights): **the check that no close voice ever sounds on a death**.
- mV2 fails on the plain procs ("a tickStatus on dawnbringer (out) played ["spellbreaker-stun"], want [] (procs
  at x[1])", 4814): the check that only a doubled stun is voiced.
- mG1 fails where a plain stun greys ("dawnbringer's grey 0.1917, the procs and its stun rebuild 0 (stun 0.1917,
  a proc at x1)", 206,960): the grey rebuilt from the sim's own procs, not from the hex clock the picture watches.
- mP1 fails on every call where the picture relabels a tag ("the picture wrote the simulation: vx ..."), read on
  the call itself; its fights move (72 of 74; 43.2% against 58.1%; the `engine_ab` control above), and [1]-[6]
  still pass, because they rebuild every frame from its own state.
- mD1 is caught only by the drawn subset ("a drawn frame changed the simulation: vy ..."), on the frames that
  draw the motes: the check that a DRAW writes nothing, which the headless hooks cannot see. Its drawn
  fights move (12 of 12 against the clean drawn run); its [2] reads NOT EXERCISED on its 12 fights, the 200-run
  floor, as on the base's drawn control of the same 12 (above).
- **render_ab:** the other relics' pairs (paradox:heartwood:25064, twinshade:lastlight:991,
  bulwarden:vinesower:70707, axiom:grudgebearer:31337, at 0.5 / 6 / 12 / 22 / 31 / 40s) are **24/24
  pixel-identical** (`runs/stage6_render_ab_others.txt`). **Control:** Spellbreaker v Vesper 111075 (the clip's
  fight) at 79.5 / 81 / 83 / 85 / 87 / 88.5, inside the window that runs 79.175-88.942, is **0/6 identical**
  (`runs/stage6_render_ab_control.txt`; the frame's mean luma 20.554 -> 20.204 at 79.5, the bolt's lit set-piece
  gone from the cast, then -0.02 to +0.13 as the script, the motes and the grey stand).
- **chain_audit** `--builder spellbreaker_build.py`, relic = tip = the fx link: **ALL 23 INSERTS SURVIVE**, stages
  1-5's ten (the blade among them) and stage 6's thirteen that add code (`runs/stage6_chain_audit.txt`); the two
  token removals (the banner seat, the life entry) add no code and so are not inserts the tool can read, and the
  retired bolt branch is found by its comment (its code is shorter than the tool's floor). **Control:** the same
  relic with the b7.5 as the tip loses all 13 of stage 6's and exits 1 (`runs/stage6_chain_audit_control.txt`).
  The builder watches what the tool cannot, on every stage-6 build: `spellbreaker: 1.4`, a `spellbreaker` seat in
  `onTarget` and `u.w === "spellbreaker"` must be gone, and the bolt art's one `Math.random` with them.
- **tip_audit:** identical to the b7.5's, line for line, but the file name (`runs/stage6_tip_audit_fx.txt` against
  `runs/tip_audit_b7.5.txt`). Stage 6 adds no status and changes none; the card is unchanged.
- **The builder's own guards** (`runs/stage6_rebuild.txt`, `runs/stage6_builder_negtest.txt`; the builder
  6543119d4a9d0d1c; 005dc3e1d6af74c5 through stage 5, kept in scratch as `s6/spellbreaker_build.pre6.py`):
  - **all seven links rebuild byte-identical from the bare tip**, `sc-tendril-t3`, LF, no CR -- the six of
    stages 1-5 as they were, and the fx link;
  - **stage 6 refuses** to run twice (its names are in its own output), on Rick's two other links (b8.3, b7.7),
    on stages 3, 2 and 1, on the bare tip, over an existing link, to a name not `sc-spellbreaker*`; stage 5 and
    stage 3 refuse on the fx link; `--alt50` and `--alt-row` refuse with stage 6 (13 refusals, none writes a file);
  - **its scan of stage 6's ADDED code** (a re-emitted anchor aside) refuses **35 scratch copies of the builder**,
    each with one forbidden line written into a stage-6 row: in `tickUnmaking` a ball moved (`f.vx`), the RNG, a
    stun, the hex clock, the one `ultFx` slot, the shared weapon (`f.w.reach`), a module table written and one
    aliased (`STATUS.hex`), a tag pushed, a hit stop, the tally written, the window closed, a beat, a voice, an
    `apply`, a status deleted and one written, `Math.random`, the sim's shots spliced and written through an
    index, `hexStunMul` written; in the draw methods the match's clock, a ball, `Object.assign` on a fighter, the
    canvas name rebound to a fighter; in the fields row a charge and a voice; **the stun voice on every proc and
    the close voice on every close** (each a second line on the sim path); in the Sfx arms a module table and a
    voice through `SFX`; the synth struck in drawWeapon; a turn in the blade's script call; the sim's ticker
    called from the presentation call; a status tag filed from the floor call. **A harmless line in a draw method
    writes its page** (a different one, b1365040184a371d), and the unmutated copy writes the fx link,
    ceeff797e5739e0c;
  - on stage 6 it also refuses if the inlined `fx.js` moved, if the bolt's art is still drawn, seated or given
    its life, if the rune-crack fallback is not kept once after Spellbreaker's three arms, if the stun voice does
    not follow the hex proc's own `breakSpin` or the close voice does not stand just before the window's close
    line, if a `Math.random` moves other than the bolt art's one, if the picture reads the hex stun other than as
    its grey, if the base's hex clock has a writer beyond its three (the grey's proc test), and unless each arm,
    call, pass and method is wired exactly once and `tickUnmaking` follows `tickNovaFx` in `tickPresentation`.
    The generator (`runs/gen_s6.py`) was run once (it wrote the S6 table, eb35a9a8f4d37571) and refuses a
    builder that already carries S6; the wiring, the scans and readings 13-20 are hand edits after it, said
    here, and every check in this section ran on the final builder or on links it writes byte for byte.
- **compose6** (§5; `runs/stage6_compose6.txt`, `runs/compose6.sh`): 0 FAIL on 23 tips.
- **shell_identity** is not run here: the app's json is shared, and the orchestrator runs it on the carried link.
- **The labs' own gates** (§5a, §5c): the picture -- bloom share +0.0000, with three controls that fail;
  whole-fight identity on 18 fights x 3 (the rows, the shipped look, drawn), with a 1e-9 control that differs on
  all 16 of hers; 77/77 other-relic render frames on 11 pairs, with two Spellbreaker controls at 2/7; `engine_ab`
  4218/4218 on its shipped look. The voice -- the 148/148 wire run, with a sim-write control at 0/148; 74/74 end
  to end, 82/82 on the carry tip.

**What the design's stage 4 asked for, and where it went** (§5: "picture, voice, carry; bolt's field spec out;
`engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched"): the picture and the voice (§5a,
§5c), the bloom measured, +0.0000; the bolt's field spec out of both copies -- the orchestrator's at the carry,
tried in scratch (§5b); `engine_ab` 4218/4218 with Spellbreaker in; `render_ab` with a control; `chain_audit` 23/23
with a control; `shell_identity` the orchestrator's; one fight watched, the clip (§5f).

### 5f. The clip (Rick's to overrule)

`tools/_spellbreaker_pick.py` (1a2ac1070793473d; from `_ironwood_pick.py`, by way of `_aureole_pick.py`) scores a window
against v79 §4 as built. A window qualifies only if it shows everything: the cast voice (the crack into the hum) and
the script written, **a blow's second hex** (a HEX +2 tag), **a doubled stun** (its lengthened snap, the foe's
weapon grey), and **a close BY ITS CLOCK with both alive**, with its close voice (the hum cut, the script
unwritten; a death's close or a kill is the death voice's and the verdict's); and nothing taking the screen: no
cast or banner of the foe's, not the scrunch card, and no kill inside the clip. Twinshade is left out (a second
body taking hexes and greys) and so are the runic foes, Spellbreaker's own school (Axiom, Foregone, Paradox: the
same blue, their own hexes stun HER weapon plainly, and they cast in the same runes). Scored on the second hexes,
the doubled stuns, the share of window frames with the foe's weapon grey, and her blows.

It ran 33 foes x 4 seeds (`runs/stage6_pick.txt`: of the 132 fights' best windows, 17 show everything). The pick is
**Spellbreaker v Vesper (the vigil scythe), seed 111075**:
- the cast at 79.175; the window closes by its clock at 88.942: 8 s on the window clock, 9.77 s of match time;
- **10 second hexes, each HEX +2** (81.81 to 88.13), **26 doubled stuns, each its sizzle**, the foe's weapon grey on
  82.8% of the window's frames, 213 hit-stop steps;
- no banner, card or kill in the clip; the fight runs on past the clip's end (90.75, both alive; the kill is at
  93.60).

The runner-up, Bulwarden 111001, scored 0.1 lower (9 second hexes, 34 doubled stuns, grey 95.6%).

    python cinema_clip.py --game <scratch>/batch/spellbreaker/links/sc-spellbreaker-b7.5-fx.html \
      --a spellbreaker --b vesper --seed 111075 --at 77.98 --window 12.77 --end-at-window --fps 60 \
      --w 540 --out ../07-shorts/v111/unmaking-window.mp4

`--at` is the cast less 1.2, `--window` the window's 9.77 s of match time plus 1.2 and 1.8 (the window clock stops
in the freezes, so 8 + 3 would end the clip before the close).

The clip (`runs/stage6_clip_check.txt`, `stage6_clip_log.txt`, `stage6_clip_timeline.txt`):
- **12.77 s, 766 frames**, 1:1 with the match (the director's T3 cut is the kill at 93.60, outside the clip);
- 540x960 h264 at 60 fps, AAC 48 kHz stereo, 2.53 MB (4a265fe94f2b603e);
- **AAC mean -20.9 dB, max -0.8 dB; -18.9 LUFS integrated, LRA 1.2 LU, true peak -0.6 dBFS.** The same window filmed
  on the b7.5 (no stage-6 voice; 10e5ef74a53ee989) reads mean -20.9, max -0.9, -19.0 LUFS, true peak -0.9: the
  loudest sample is the fight's own on both (the clip's at 89.56 s, after the last new voice has ended), and the new
  voices add 0.1 LU and no peak;
- the fight's state at the clip's end (t 90.75, hp 132 / 123.4, 37 clanks) is the headless fight's
  (`stage6_clip_timeline.txt`);
- **the new voices are in the mix** (`runs/stage6_clip_audio.txt`): both tracks decoded, each voice read in its own
  band over its own time, with minus without: the cast's hum +4.7 dB, **the close +23.4**, **the 26 stun sizzles a
  median +17.6** (+3.9 to +44.5; 25 of 26 over the band's no-voice spread). The crack on the cast's frame reads -2.0,
  because the b7.5's cast fills that band with rune-crack. **Control:** the same readings at five times with no
  stage-6 voice come back within 1.6 dB in the hum's band and 5.0 dB in the sizzle's (the two renders differ
  everywhere at about -40 dB broadband, before the cast too; not traced here, and it is why the stun tails are
  counted against that spread).

Five frames, checked through the pipeline (the post chain and the director), matched to the fight's own event times
by the HUD's clock; tiled in `05-reference/v111/unmaking-clip-5frames.png` (b50168ef1774cc15, 2700x960):
- 1.39 s (HUD 79.4): the cast, 0.2 s after it (79.175): the banner "Unmaking" on HER, the script writing along both
  blades, the foe's scythe already grey (its first doubled stun, 79.300);
- 4.17 s (82.2): a doubled stun (82.042, its sizzle): the scythe grey, the script standing on both blades, rune motes
  drifting off them, HEX +2 at the last blow's impact;
- 5.60 s (83.6): a blow and its second hex (83.517): HEX +2 at the impact, the scythe grey;
- 8.83 s (86.8): a second hex (86.775): HEX +2 on the foe, the grey held through repeated doubled stuns, motes;
- 11.04 s (89.0): 0.08 s after the clock close (88.942, the hum cut): the script unwriting, the last doubled stun's grey
  running out (off at 89.125).

**The white column of sparks from her toward the foe in the cast's frames (from 1.2 s) is the bolt's own
`SPECS.spellbreaker` field** (a `beam` is shed toward the quarry), still on this link until the carry's
`fx_remove.py` (5b). The clip is `07-shorts/v111/unmaking-window.mp4` (gitignored). **Rick's to overrule.**

### 5g. Where each event hangs (the fx link)

The lines, in `sc-spellbreaker-b7.5-fx.html` (grep the quoted text on a carried link):

```
the cast       fireUlt 16452: the shared prologue (the banner, its seat map `onTarget` 16470 without Spellbreaker now,
               SFX.play("ult", { w: f.w.id }) 16479, this.ultFx; the life map line 16498 without ` spellbreaker: 1.4,`),
               then `if (u.kind === "unmake"){` 16855: `f.ultUnmake = { t: 0, dur: u.dur };` 16860, returns
the window     `this.tickUnmake(dt);` 9038 (after tickTendril); `tickUnmake(dt){` 13756: the close voice 13769, the close
               13770 (the clock or a death); the field recomputed at its end
a stun         tickStatus 9517: the hex proc's stun 9656, its breakSpin 9660-9661, the stun voice 9670
the second hex resolveHit: the onHit loop's tag call 14973 (`statusTag(hx, hy, k, first, ...)`), the second hex under
               `if (U.hexExtra > 0 && foe.alive){` 14989 (`foe.apply("hex", U.hexExtra, ...)` 14990)
the voices     Sfx arms: `} else if (w === "spellbreaker"){` 7429, `"spellbreaker-stun"` 7455, `"spellbreaker-close"` 7477,
               before the shared `} else {  // rune-crack` 7488
the picture    fields after `this.hexStunMul = 1;` (`this.unmkFade = 0;` 7789 ...); `this.tickUnmaking(dt);` 9080, right
               after tickNovaFx in `tickPresentation` 9078; `tickUnmaking(dt){` 13804 (after tickUnmake, before
               tickWinnow); `if (__world) this.drawUnmaking(m);` 19575 (the world pass, after drawTree);
               `const UNMAKING_RUNES = [` 18000 (before shellHash); `drawWeapon(m, f){` 24174: the grey's re-entry just
               inside it, the dim line with the grey's alpha 24200, the script call 24372 (before `if (f.ultDraw){`);
               `drawUnmaking(m){` 24416, `_unmkScript` 24455 (before the fx banner comment)
the bolt's art drawUltOver's `u.w === "spellbreaker"` branch gone: its comment at 22069; ULTSIG `spellbreaker(c, t, cf, P)`
  (retired)    579 and the banner scatter (`b.w === "spellbreaker"` 29281, 29454) kept; fx SPECS.spellbreaker still inline
               at 32629-32631 (the orchestrator's, 5b)
```

## 6. What is left, and whose

- **Rick:**
  - **the clip** (§5f, `07-shorts/v111/unmaking-window.mp4`) and every art and sound pick in §5 -- the script
    written along both blades (0.3 s) and unwritten at the close (0.2 s), the rune motes, the grey (the
    design's `grayscale` at 0.6), HEX +2, the bolt's art retired with the charge rune and the banner scatter
    kept; DRONE for the cast (a glass crack into a C4 hum), SIZZLE for a doubled stun (the snap with a 0.4 s
    tail), CUT for the close (the hum's strikes stopping) -- under "you pick i overrule";
  - **the grey is mostly a colour cue** (§5a): 0.042 in luma and 0.069 in chroma against a plain stun, least on
    the near-white sanctified weapons; the four other greys tried read no better on both (B-E). The design's
    words are kept; a stronger grey would be a design change;
  - **no `fx.js` field** (§5b): the design's "rune motes off the blades, both copies" are drawn off the blades
    instead, because the one ultFx slot is hers for 7.0% of a window and her blades' hub stands a median 193
    units from where a field would spawn;
  - **a close by a death is silent** (the death voice has it; reading 18), and **a doubled stun running at
    the kill stays grey through the verdict** (its stun is frozen there, as the plain stun's dim is: 155 of 444
    fights end with one); both are readings the design leaves open;
  - **the blade**, unchanged from stage 5 (§4): the final is **7.5**, the measured point nearest the shipped
    rate (49.2% both sides against the shipped 48.6%), under the brief's grid (8.3 / 8.5 / 8.8) and the
    twinblade row's floor (8.3); built beside it, **8.30** (the row's floor, 54.3%, `--alt-row`) and **7.7** (the
    50% crossing, 49.7%, `--alt50`). At 7.5 the twinblades and the fast scythes run away from her (Twinshade
    10%, Bloodmirror 0 of 40, Vinesower and Morningstar 10%), and verify adds her first 0/40 pairing,
    Spellbreaker v Bloodmirror, to its already-red "both sides can win" check. Stage 6 is presentation and
    moves none of it (§5e); a different blade is one number in the builder, and stage 6 goes on whichever
    stage-5 link `BLADE` names;
  - x2 or x3 (§6.3): built at x2, as taken; the veto (§6.1).
- **The orchestrator (ALL DONE at the carry, §7):**
  - the carry: stages 1, 2, 3, 5 and 6 re-applied onto the tip of the day with this builder (`compose6`: the
    same change sets on every tip tried, up to `sc-aureole-fxout` and `sc-censer-fxout`; §5), proved with
    `engine_ab`; `chain_audit` watches 23 inserts, the blade and all thirteen of stage 6's that add code; the
    two token removals (the banner seat and the life entry) and the bolt branch's code are watched by the
    builder itself on every stage-6 build;
  - take the bolt's `SPECS.spellbreaker` out of both copies of `fx.js` with `fx_remove.py --relic
    spellbreaker` at the carry (§5b, its exact text; tried in scratch on the fx link and, dry, on
    `sc-aureole-fxout`). Until then a Spellbreaker cast still fires the bolt's beam particles, and the clip
    shows them;
  - `shell_identity` on the carried link (the app's json is shared; not run here);
  - the probe on the carried link (the probe-on-the-chain rule): `--stage 5` pins it (the stage-6 checks
    switch on by themselves), and `--drawn 24` keeps the drawn subset affordable;
  - **for the batch's later voice labs:** `ult/spellbreaker` is no longer rune-crack once this row is on the
    line; a lab that used it as its rune-crack control must use an id with no arm (`__fallback__`);
  - the app pointer (`app/main.js` GAME) waits for Rick's check of the whole batch.
- **Not measured here:** the picture's frame cost in the app (deferred: no Electron while Rick is on the PC). A
  later session with the app, or the orchestrator.
- **Standing, not this build's:**
  - verify's three red checks are the base's (Heartwood v Twinshade and v Bindweed 0/40; the
    pairing-duration band and the overall mean, both red on the base); Spellbreaker's longer fights
    lengthen the last two, and the one element that is hers (v Bloodmirror 0/40) is listed under Rick;
  - the base's hex stun has always lasted 25 steps (0.2083s), not 0.20, by the countdown's float residue
    (§2); the design's 0.40 lands at 48 steps exactly.
- **Next in this build:** nothing. Stages 0-6 are done in scratch; the carry is the orchestrator's.

## 7. The carry onto the chain, and the bolt's field spec out

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Aureole with the
same builder, one stage at a time (`--src` the previous link), and one more link that takes the retired
bolt's particle field out:

```
sc-aureole-fxout.html                 the batch line's tip (Aureole, fx out)       da5eafafcfae06c2
  -> sc-spellbreaker-stub.html         stage 1                                      eda1cae1aa1e7307
  -> sc-spellbreaker-stun.html         stage 2                                      16794b6daa5ac8ad
  -> sc-spellbreaker-unmaking.html     stage 3                                      dcb811df32e1a5e2
  -> sc-spellbreaker-b7.5.html         stage 5                                      d8e16ff49c9d63e1
  -> sc-spellbreaker-b7.5-fx.html      stage 6                                      e2a4fd8ea4eed06f
  -> sc-spellbreaker-fxout.html        SPECS.spellbreaker out of both fx.js copies  9243277a756e84b6
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail, Widowmaker, Lightkeeper, Censer and Aureole (redesigned on the chain since), n=6:
  **3168/3168 identical** (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-aureole-fxout` against the carried stage-6 link, every relic on the tip but
  Spellbreaker (41), n=6: **4920/4920 identical** (`runs/carry_engine_ab_tip.txt`).

**The bolt's field spec out: `tools/fx_remove.py --relic spellbreaker`**, the entry's three lines (no
comment of its own sits above it): **fx.js 487c9de9dff7f374 -> 7dc0123af735c83e**, the stamp stage 6's
dry carry predicted (`runs/fxout/fx_remove.txt`).

**Gates on `sc-spellbreaker-fxout`** (`runs/fxout/`; Rick asked for minimum usage from 22:35 to 03:00,
so the gates after engine_ab were stopped and re-run at 03:05 by `fxout_rest.sh`):
- engine_ab against `sc-spellbreaker-b7.5-fx`, all 42 relics, n=6: **5166/5166 identical**;
- `spellbreaker_probe.py` on the carried link: **8/8** -- it met every relic carried since its scratch
  base and needed no change;
- render_ab: the other relics' four pairs **24/24 identical**; **the control, Spellbreaker v Vesper
  111075 through the cast (79.21-79.61s), 0/5 identical** -- the bolt's spray is gone;
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold;
- **shell_identity 200/200** (app Chromium 152 vs headless 151; the json restored).

**The clip, re-filmed on `sc-spellbreaker-fxout`** (the §5 command, `--game` the carried link):
`07-shorts/v111/unmaking-window.mp4` (2.51 MB, 12.8s; `runs/fxout/clip.txt`).

**The blade** stays 7.5 on this link. Rick, 2026-09-29, after this build: "you pick the blades. do
whatevers best for balance" -- every batch blade is settled in one balance pass on the final roster
(the point nearest 50% both sides), which will choose among 7.5, the 50% crossing 7.7 and the row's
floor 8.3 as measured there.

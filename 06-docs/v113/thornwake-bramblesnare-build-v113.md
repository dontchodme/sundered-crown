# v113 — THORNWAKE / BRAMBLESNARE (REDESIGN), BUILD. STAGES 0-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-spellbreaker-fxout`, the old freeze's field spec out of both `fx.js` copies: §7): stage 1 is arm A fight for fight on both blocks; the brambles are the lab's mechanism (probe 8/8 on every stage from 2 on, read inside the hooks, every number pinned by the stage, "nothing else" snapshotted whole; 13 mutants, each caught by its own check); the built relic sits over its lab arms by the window clock, attributed with controls both ways; **THE BLADE IS 26.5 — the measured point nearest 50% both sides (Rick's ruling, 2026-09-29): 50.9% (753 of 1480), against the shipped freeze's 47.8% on the same seeds.** The design's own target (the shipped rate) is measured beside it. The charge is 14 (the lab's 16 on the game's clock). **Stage 6, the picture and the voice, is built (`sc-thornwake-b26.5-fx`, §5):** sixteen rows byte-exact to the two labs'; each bramble a tangle of thorned canes on the floor that grows out of the hit point and browns in its last second, leaves lifting off it; Tendril's root picture ported for the snare (shoots clenching the held ball's rim, Paradox's hexagon kept off it), a thorn flash at each bite, the ENTANGLE tag counting, the scythe's blade greening for the window; a rustle and creak at the cast, a dry crackle as each bramble opens, Tendril's root voice at each snare, a soft snap at each bite, and no close voice; the freeze's art and voice out, and no `fx.js` field (the leaves are drawn; the freeze's `SPECS.thornwake` is the orchestrator's to take out at the carry, **and `fx_remove.py` refuses on it as it stands**: §5b). engine_ab 4218/4218 with Thornwake in; the probe 10/10, its two new checks (the voices, the picture's hook, 74 fights drawn) each failed by its own mutants; render_ab 24/24 with a control at 0/6; chain_audit 24/24 with a control; the carry dry on six tips. The clip is with Rick; the carry is the orchestrator's.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`, the BUILD row under the
redesign's); built 2026-09-30. Input: `06-docs/v84/thornwake-bramblesnare-redesign-v84.md` (its §5 is the
build brief), its runs (`06-docs/v84/runs/bramble_base.*`) and its lab `tools/overlays/bramble.js`, and
nothing else (rule 0). Builder `tools/thornwake_build.py`, probe `tools/thornwake_probe.py`, runs in `runs/`.
**A REDESIGN, not a new relic:** Thornwake ships in the base; its ultimate (Bramblesnare, the 1.6s root) is
replaced by the design's, and the roster stays 38. Built on DESKTOP-DERRAFT, Chromium 151.0.7922.34, Python
3.13, playwright 1.62.

**Revised 2026-09-30 after the adversarial review, before stage 6. That round only this doc changed**, plus one new run file
(`runs/lab_patches_vs_hitsin.txt`) and the scratch tool that wrote it. No link, builder, probe or earlier run
moved, and every link still rebuilds byte-identical. §0 and §5 now quote `SPECS.thornwake` verbatim, as its
three lines, together with the two-line FREEZE comment that `fx_remove.py` removes along with it. §2 now
explains why the lab's bramble count sits below its blows in windows: the lab never plants on the killing
blow. The review's other notes (the Twinshade shade plant, and the gates reading high because of the clock) are
already covered below: the shade plant is reading 3 and is flagged to Rick in §6, and the clock is §2's
controls.

**Stage 6 added 2026-09-30** (§5; the earlier sections stand as revised, with pointers to §5 where stage 6 retires
or keeps what they list). The builder gained its S6 table (written once by a generator from the labs' row files),
the `--stage 6` wiring, readings 17-22 and stage 6's own scans, and one fix to an old check: its refusal of a
non-LF source could never fire (it read the source with `read_text`), and now does; no link moved, and every link
still rebuilds byte-identical. The probe gained [9] and [10], the verdict's 2 s and `--drawn`, run only where a
link carries stage 6, so stages 2-5 still read 8/8 line for line. New: `tools/_thornwake_pick.py`, the fx link in
scratch, the clip `07-shorts/v113/bramblesnare-window.mp4`, the five-frame tile
`05-reference/v113/bramblesnare-clip-5frames.png`, and the `runs/stage6_*` files.

```
sc-tendril-t3.html                the base: the chain tip (Bindweed stage 5; 38 relics)                         5a6216e3b629fad4
  -> sc-thornwake-stub.html        stage 1  the freeze out, the new block in, stubbed (1e9)                      684e6e75ea68e928
  -> sc-thornwake-bramble.html     stage 2  the brambles: entangle + bite; charge 14 (the brief's stage 1)       f49eefcd6f87c226
  -> sc-thornwake-snare.html       stage 3  the snare on entry, rootFor 0 -> 0.6 (the brief's stage 2)          800daceb906ef28e
  -> sc-thornwake-b26.5.html  stage 5  the blade, 31.35 -> 26.5: nearest 50% both sides (Rick's ruling)  fd5031063ecb6807   THE FINAL LINK
    -> sc-thornwake-b26.5-fx.html  stage 6  the picture and the voice (presentation; §5)           d306822d6914c08c   THE FX LINK
```

The links are in the batch's scratch (`<scratchpad>/batch/thornwake/links/`); the orchestrator carries them
onto the chain by rebuilding them with this builder on the tip of the day. **Every link rebuilds
byte-identical** from the bare base with the final builder (`runs/stage6_rebuild.txt`, the fx link among them;
stages 1-5 before it: `runs/rebuild_final.txt`), and no
`sc-thornwake*` name is on `02-chain/`. The stage numbers are the builder's: its stages 2 and 3 are the
brief's stages 1 and 2, its stage 5 is the brief's stage 3 (the blade), the brief's stage 4 (picture, voice,
carry) is the batch's stage 6 (§5, built), and **there is no stage 4** (the brief has two mechanism stages).
**The carry, dry** (`runs/carry_dry.txt`; with stage 6, `runs/stage6_carry_dry.txt`, §5): stages 1, 2, 3 and 5 apply on the batch line's newest tips
(`sc-spellbreaker-fxout` 9243277a756e84b6, `sc-aureole-fxout` da5eafafcfae06c2, 42 relics), on
`sc-ironhail-fxout` and `sc-coldiron-temper-fx`, and on Heartwood's in-flight scratch final
(`sc-heartwood-b11`, the other freeze redesign) — and Heartwood's builder applies on this build's links: both
orders, every anchor exactly once, the page parsing.

## 0. What this build stands on

- **The relic is Thornwake as shipped** (base line 847), and only its ult block moves (stage 5 then moves its
  blade): the verdant scythe, blades [0], reach 104, width 11, artW 46, **blade 31.35**, spin 3.2, mode spin,
  mass 2.4, onHit entangle 2, its blurb. The builder asserts, BY CONTENT and never by which relic is last:
  the row and its scythe profile, the shipped Bramblesnare block verbatim, the shipped blade,
  `hurt(foe, dmg, src)`, `Fighter.apply(key, n, src)`, `alive`, `resolveHit` and its `self.hits++`, `beat`,
  `fireUlt`, `tickStasis`'s weapon lock, `move()`'s hold and its resume (the Stasis clamp), `STATUS.entangle`,
  that `Match` refuses a mirror, that `step()` returns in a hit stop before the window tickers and runs them
  after the moves and before the hit loops, and that every name it adds is free on the base on identifier
  boundaries. **Names kept** (§4): THORNWAKE / BRAMBLESNARE; the card is the design's 66 characters, `Blows
  leave brambles: a foe in one is rooted, entangled and bitten`.
- **The reference: the shipped relic's rate on the base** (`relic_rate`, both sides, two blocks, 1480
  fights, `runs/stage5_rr_shipped_*`): **47.8%** (708 of 1480; 46.9 / 48.8; side A 48.9, side B 46.8), mean
  57.7s. The design's 47.9 is the freeze on Chromium 141, side A only, 33 foes; on 151 the lab's own SHIP arm
  reads 48.0 / 49.7 (side A).
- **The ultimate it replaces, found whole in the base, and what became of each piece** (line numbers are the
  final link's, the base's in brackets):
  - **the ult block** `kind:"freeze", charge:15, radius:260, dmg:10, apply:{entangle:3}, freeze:1.6`:
    **replaced** by `kind:"bramble"` (line 856 [850]). Radius, damage, entangle and stun are out of the row;
  - **no cast branch, no ticker, no fighter field of its own**: there is no `u.kind === "freeze"` anywhere.
    The root was `fireUlt`'s GENERIC TAIL (`u.radius`, `u.dmg`, `u.apply`, `u.freeze` -> `foe.stun`,
    `breakSpin`), and that tail **stays whole**: Heartwood's Rootfast still casts through it on this base
    (the builder prints `kind "freeze" on this base: thornwake, heartwood` at stage 1; Heartwood is being
    redesigned too, v112, and either may be carried first), and its damage and `apply` clauses serve other ult
    blocks. **So nothing in the simulation is retired beyond the row's four fields;**
  - **the presentation, kept by stages 1-5 and retired or kept by stage 6 (§5)** (nothing in the simulation reads
    any of it): `drawUltUnder`'s floor roots running caster to quarry (line 21154 [21012]) and `drawUltOver`'s
    thorns on the pinned quarry (21836 [21694]), both keyed `u.w === "thornwake"` — the freeze's picture, which STILL PLAYS AT
    EVERY CAST on these links; the `ultFx` record's `life` entry `thornwake: 2.4` (16358 [16233]); `fireUlt`'s
    `onTarget` entry `thornwake:1` (16330 [16205]: the cast banner stands on the quarry); the banner's letter
    "cinch" (29036 / 29103 [28894 / 28961]); the charge rune `ULTSIG.thornwake` (509 [509], "a thorn ring
    that CLOSES as the charge fills"); the cast voice, the `"thornwake"` arm ("creak and cinch", 6324 [6315]);
    and the field spec, the inlined `fx.js` copy's `SPECS.thornwake` (lines 32443-32445 [32301-32303];
    `src/render/fx.js` 188-190), read from the base's inlined copy. Its exact text is these THREE lines, each
    with its own leading spaces (4, 17, 17), LF-ended — 184 bytes, sha256[:16] `8945c09d54396250`, and
    byte-identical in the base, in every link of this build and in `src/render/fx.js` as it is on disk today
    (in this file each block below carries 4 more spaces, the list item's code-block indent; rendered, it is exact):

    ```
        thornwake: { mode: 'fall', n: 1100, sp: [30, 120], grav: 110, drag: 1.0,
                     life: [0.80, 1.80], heavy: 0.02, size: [0.6, 1.9],
                     spawn: 0.85, up: 0 },
    ```

    Directly above it is a two-line comment that explains the freeze (32441-32442 [32299-32300]; fx.js
    186-187), again exact, 4 and 7 leading spaces:

    ```
        /* A FREEZE HOLDS, so its frost settles slowly and lasts -- the same
           reason the art is long: the hold it explains is still in force. */
    ```

    `tools/fx_remove.py`'s `spec_block()` takes that comment out WITH the entry, because it closes on the line
    just above the entry and is not a section header, unless `--keep-comment` is passed. Run on the base's
    inlined copy, on the final link and on the disk `fx.js`, `spec_block(…, "thornwake")` returns the same five
    lines (331 bytes, sha256[:16] `29a0904df7aad6db`). The comment describes the freeze, which this redesign
    removes, so it should go with the entry. This build touches neither copy of `fx.js`: `tools/fx_remove.py`
    takes a retired spec out of both at the carry, which is the batch's procedure.
- **The lab is `tools/ult_overlay.py` + `overlays/bramble.js` without `--cell`** (a redesign): the relic's
  own ultimate is suppressed in every arm but SHIP. **A** = Thornwake with no ultimate, **SHIP** = the
  shipped freeze (engine charge 15), **B** = entangle + bite in a bramble, **C** = B + the snare on entry
  (taken). The relic plays side A against **the design's roster: the 34-relic roster minus the donor**, which
  is Thornwake itself: 33 foes (`runs/foes33.txt`, exactly the published json's `byFoe`). Morningstar,
  Ironwood, Portcullis and Bindweed (built since) are foes in `relic_rate` and `verify`, not in the lab's
  arms. The runs use `tw_lab.py` (scratch, written by `make_lab.py`: `ult_overlay.py` with two additions and
  nothing else changed — the census below, and one row a fight in its json, so a built link can be compared
  fight by fight).
- **Lab defaults against the settled numbers: none differs.** `bramble.js` defaults `patchR 80`,
  `patchLife 6`, `tickCd 0.5`, `tickDmg 2`, `rootFor 0.6` — §4's numbers exactly, and every published arm ran
  them (`bramble_base.json`: `P` is only `charge 16, dur 8`). The harness's `P.charge` 16 and `P.dur` 8 are
  what the design priced (no prose names a charge). Two lab details the build does NOT copy, both declared
  below: the entangle's source is the Fighter in the lab (a side letter here, Rick's ruling 4), and the lab
  plants at the opponent on a blow that landed on a Twinshade shade (reading 3).
- **THE CHARGE IS 14: the lab's 16 on the game's clock.** Rick's batch ruling reads a design's charge on the
  lab's step clock, which counts hit-stop freezes, and converts it per fighter. **The census** (`tw_lab.py`:
  before each lab step, whether it is frozen — `m.hitStop > 0 || m.latch || m.splitHold` — on the whole arm
  and inside the lab's windows; the precedent is `06-docs/v99/runs/ironwood/tree_freeze.js` and
  `v101/runs/vine_census.py`), 660 fights an arm a block (`runs/s0_ASBC_*`):

  ```
  arm C (taken), block 2207   10.72% of lab steps frozen (483,079 of 4,505,796); 12.13% inside windows, 9.80% outside
  arm C (taken), block 2317   10.74% of lab steps frozen (485,683 of 4,521,267); 12.06% inside windows, 9.88% outside
                              engine charge = round(16 x (1 - 0.1073)) = round(14.28) = 14
  arm B                       10.99% / 11.04% -> 14.24 / 14.23
  arm A / SHIP                11.16% / 11.13% and 11.18% / 11.13% (no windows) -> 14.21-14.22
  ```

  The shipped 15 was the freeze's own engine charge and goes with it.
- **Readings** (in the builder's docstring; where the build had to choose):
  1. **The charge** is the lab's 16 converted: 14 (above).
  2. **The window is 8s** (the lab's `P.dur`; §4 "a patch planted at 7.9s lives to 13.9s"), on the window
     tickers' clock.
  3. **The landing point is the struck ball's centre** (§1 "where it landed", §4 "at the FOE's position on a
     landed blow"), planted in `resolveHit` beside `self.hits++`, the count the lab watched. For every blow on
     the opponent it is the lab's point (nothing moves a ball between `tickHits` and the step's end). A blow on
     one of Twinshade's shades plants at the shade, where it landed (Consecration's reading, v109); the lab
     planted at Twinshade. Two blows on one step plant two brambles (the lab: one). Only Twinshade's fights
     can differ (the probe counts 18 shade plants in 444 fights).
  4. **Brambles outlive the window and act for their whole life** (§4 explicit, and the lab: its tests run
     while the window is open OR any patch lives). A bramble still alive at the next cast acts in that window.
  5. **Brambles outlive their planter**: the lab tests the foe against the patches with no check on the
     caster, so in a kill flight (the caster slain, the match held open while it flies) the brambles still
     bite. The prose does not say otherwise.
  6. **Entry is the transition on the TESTED frames** (the lab's `wasIn`): a frame is tested while the window
     is open or one of the caster's brambles lives; `brambleIn` keeps the last tested frame's answer. A bramble
     planted under a foe that was in none is an entry, so the blow that plants it snares on the next tested
     frame (§4's "not inside last frame, inside now"; the lab's reading).
  7. **The snare is Grasp's write**, the lab's `H.pin` to the letter: `pinV` captured iff the hold standing is
     not longer than 0.6; `pin`/`pinMax` max'd; `pinFree` NOT touched, so `tickStasis` locks the weapon ("ball
     and weapon", §4).
  8. **The thorns' cadence is the lab's**: one cooldown per caster, 0 at every cast, run down on every tested
     frame inside or not; a bite on the first inside frame it is clear. Entangle first, then the bite (the
     lab's order). `apply`'s source is a side letter (Rick's ruling 4); `hurt`'s stays the Fighter (a ward's
     shatter reads it).
  9. **A bite that kills files its own fatal hit beat** (Rick's standing rule for a side-channel kill; §4's
     "no beat" is Scour's rule, whose fatal tick files). No other bite files one, and nothing sets a hit stop
     (a ward the bite breaks shatters inside `hurt`, as every ward does).
  10. **The window closes on its clock or either death** (the lab's). The brambles stay.
  11. **No cast waits.** The design asks none; 14 of unfrozen time against a window of 8 on the same clock
      cannot overlap (the probe's [8] asserts it on every cast); old brambles never hold a cast (the lab's).
      The stable prefix `if (f.charge >= f.w.ult.charge && !f.ultCorona` is not touched.
  12. **The target is the opponent**, never a shade: the thorns test, snare and bite the opponent only.
  13. **Nothing else:** the scythe swings as ever; no knock, no move, no hit stop, no stun write, no beat but
      a killing bite's. The builder's scan enforces it on the added code (below); the probe's [6] on the run.
  14. **The card** is the design's own, 66 characters; the names are kept.
  15. **The freeze is out** of the row; the generic tail stays for Heartwood (above).
  16. **What stayed for stage 6** (above); stage 6 retires the freeze's art and voice and keeps the charge sigil
      and the banner's letters. Readings 17-22 are stage 6's (§5).
- **Names:** kind `"bramble"`, fighter fields `ultBramble` / `brambleCd` / `brambleIn` / `brambleTally`, match
  fields `brambles` / `brambleT` (§5's "`m.brambles[]` in"), methods `tickBramble` (the clock, the window, the
  tests) and `plantBramble` (a bramble); all free on the base, on every link in `02-chain/` and on every
  in-flight scratch link (grep). Links prefixed `sc-thornwake`, none in `02-chain/`.
- **The clock:** the window, the brambles' lives and the thorns' cooldown run on the window tickers' clock,
  which stops in a hit stop (every batch build's convention); the lab ran all three through freezes (§2). The
  snare's own 0.6s is `tickStasis`'s, on the normal step path, which the lab shared.
- **The builder's scan is a whitelist** (the Spellbreaker review's finding 3, applied from the start): the
  added code (each re-emitted anchor taken out) may write only the window, the thorns' two fields, the tally,
  the match's brambles and their clock, and Grasp's three fields on the foe; call no simulation or
  presentation verb but the design's three (the entangle line, the bite line, a killing tick's beat); draw no
  RNG, take no ultFx slot, write no shared weapon and no pinFree, set no hit stop, stun nothing, delete
  nothing. **20 negative copies of the builder**, each with one forbidden line in the thorns' insert, all
  refuse for their reason; the unmodified copy builds stage 2's link byte-identical
  (`runs/builder_negatives.txt`; re-run on the stage-6 builder, `runs/stage6_builder_negatives_s1to5.txt`). Stage 6's own
  scan is §5e.

## 1. Stages 1-3, and stage 5 (stage 6: §5)

**Stage 1** replaces the shipped Bramblesnare block with the new one, stubbed at charge 1e9 (the clock never
reaches it and `fireUlt` never runs for this relic): the freeze's radius, damage, entangle and stun are out
of the row. Nothing reads the ult block's other fields, so this link is the lab's arm A (§2). **Stage 2**
(the brief's stage 1, "freeze out, `m.brambles[]` in, the tests, entangle + bite") adds the fighter fields
after `this.vineTally = null;`, the match's `brambles` / `brambleT` after `this.sparks = [];`, the
`kind === "bramble"` cast branch before Corollary's `"echo"` (it returns before the generic tail), the
one-line plant in `resolveHit` after `self.hits++; self.dealt += dmg;`, `tickBramble` called after
`this.tickTendril(dt);` (after the moves, before the hit loops) and defined, with `plantBramble`, before
`tickWinnow`, and charge 14, with the snare written but 0. **Stage 3** (the brief's stage 2) is one number,
`rootFor:0` -> `rootFor:0.6`. **Stage 5** (the brief's stage 3) is the blade, 31.35 -> 26.5 (§4).

`tickBramble`, each unfrozen step: `brambleT += dt`; a bramble goes when `brambleT - t0 >= patchLife` (6);
for Thornwake: the window's `t += dt`, closing at `dur` or on either death; then, while the window is open or
one of its brambles lives, the cooldown `-= dt` and the test — INSIDE is the foe alive with its centre within
80 + R of one of Thornwake's brambles; an entry (inside, and not on the last tested frame) pins the foe 0.6
(Grasp's write); inside with the cooldown clear: entangle +1 (side letter), then `hurt(foe, 2, Thornwake)`,
the cooldown 0.5; a bite that kills files its fatal hit beat. `plantBramble(f, q)`, from `resolveHit` on every
blow Thornwake lands with its window open: `{x: q.x, y: q.y, t0: brambleT, side}` onto `m.brambles`.

## 2. Stage 0 and the stages against it — the window clock, measured

`tw_lab.py --game ../02-chain/sc-tendril-t3.html --relic thornwake --mech overlays/bramble.js --arms
A,SHIP,B,C --seeds 20 --foes <33>`, seed0 2207 and 2317, 660 fights an arm a block (the brief's `--arms
A,SHIP,C`, plus arm B, the brief's stage-1 gate; `bramble.js` unmodified, every default the settled number).
The built links run `--arms SHIP` (the link's own ultimate) on the same foes, seeds and side
(`runs/built_*`).

```
                                          lab on 151 (block 1 / 2)   pooled   published 141 (330)   BUILT (block 1 / 2)                     pooled
A    no ultimate                          37.3 / 37.3                37.3     33.9                  stage 1: 37.3 / 37.3   IDENTICAL, fight for fight
SHIP the shipped freeze (engine 15)       48.0 / 49.7                48.9     47.9
B    entangle + bite (charge 16)          50.5 / 49.8                50.2     51.2                  stage 2 (charge 14): 53.2 / 52.9        53.1
C    + the snare on entry (taken)         63.8 / 63.8                63.8     59.7                  stage 3 (charge 14): 65.6 / 64.8        65.2
C    at blade 26.5 (the final's)          50.3 / 49.7                50.0                           stage 5 (charge 14): 53.2 / 53.5        53.3
```

Lab mechanism on 151, a cast (`runs/s0_ASBC_*`, both blocks): arm B 3.02 / 3.03 casts a fight, 1.35 brambles,
5.80 / 5.78 bites, 11.6 damage; arm C 3.08 / 3.10 casts, 1.32 brambles, **2.89 snares** (the lab's `roots`,
which counts TRANSITIONS: `!wasIn && root`), 7.68 / 7.65 bites, 15.3 damage. Blows in windows 4.33 (B) and
4.40 (C) a fight.

**Stage 1 is arm A fight for fight** on both blocks (`runs/stage1_vs_A_perfight.txt`, `perfight_cmp.py`):
660 / 660 fights, 246 / 246 wins in each block, 6,932 / 6,987 blows, and not one fight differs in winner,
duration to the step, blows in or out of windows, or casts; every foe's rate identical.

**The built relic reads over its lab arm, +2.9 at stage 2, +1.4 at stage 3 and +3.3 at the final blade, and the gap is the clock.**
The engine's 8s are 8 seconds of the window tickers' clock, and 12.3-12.8% of window steps are frozen (the
probe's census), so a window is ~9.17s of match time where the lab's was 8 step-seconds. The same holds for
the brambles' 6s of life (~6.7s of match time: about 11% of their steps are frozen, 12% inside the window and
~10% after it) and the thorns' 0.5s cadence. The lab ran all three through freezes, and it tested, snared
and bit on frozen steps too. Four controls, each able to come back wrong (`runs/lab_dur917_*`,
`runs/lab_len_*`, `runs/built_ctl-labclock-*`):

```
                                                                block 1 / 2    pooled   against
the lab at the engine's window (dur 9.17): B                    51.8 / 50.2    51.0     built stage 2 53.1   (the lab at dur 8: 50.2)
the lab at the engine's window (dur 9.17): C                    62.1 / 63.9    63.0     built stage 3 65.2   (the lab at dur 8: 63.8)
the lab at the engine's lengths (9.17 / life 6.74 / cd 0.56): B 49.5 / 53.6    51.6     built stage 2 53.1
the lab at the engine's lengths (9.17 / life 6.74 / cd 0.56): C 66.4 / 68.3    67.3     built stage 3 65.2
the build on the lab's clock: stage 2                           50.8 / 50.2    50.5     lab B 50.2
the build on the lab's clock: stage 3                           59.2 / 63.8    61.5     lab C 63.8
```

The "build on the lab's clock" is a scratch copy of each link (`tools/clock_variant.py`, in scratch) in which
`tickBramble` is ALSO called on every frozen step — the hit stop, the latch, the split hold — so the window,
the brambles' lives and the thorns' cooldown run through freezes and the thorns test, snare and bite on frozen
steps, as the lab's `onFrame` did; nothing else changes (the charge stays 14). The "lab at the engine's
lengths" stretches each of the lab's three clocks to what the engine's unfrozen seconds come to in match time.
Both directions agree, each within 2 SE of 1320 fights (1.9 points between two pooled rates): **the build on
the lab's clock reads the lab's numbers (50.5 / 61.5 against 50.2 / 63.8), and the lab at the engine's
lengths reads the built ones (51.6 / 67.3 against 53.1 / 65.2).** The window's length alone does not carry
it (the lab at 9.17 with the design's life and cadence: 51.0 / 63.0); the snare arm moves with the brambles'
life (the lab at the engine's lengths snares 3.40-3.43 a cast, the built stage 3 3.28, the lab at 8 2.89).
**The whole gap is the clock, and nothing is mis-built.** The build keeps the engine's convention (every
window in the batch runs on the window tickers' clock) and every designed number; Rick's batch ruling
converted the charge only.

**The mechanism against the lab** (the probe, 444 fights both sides x 37 foes; the lab side A x 33 foes):
stage 2 — 3.05 casts a fight, 1.59 brambles a cast (lab 1.35; the lab at 9.17 1.51), 5.86 bites (5.80), 11.7
damage (11.6); stage 3 — 3.07 casts, 1.60 brambles (1.32; at 9.17 1.50), **3.28 snares a cast, counted as
transitions** (2.89; the lab at 9.17 3.23-3.27), 7.71 bites (7.68), 15.4 damage (15.3); blows in windows 4.93
a fight (4.40; the lab at 9.17 4.90-4.96).

**The two bramble counts are not the same count, and the matched figure is blows in windows.** The lab's
`patches` never counts the blow that kills. On the kill step the harness closes the window (`!foe.alive`)
before it calls `onFrame`, so `onFrame` sees the window shut and plants nothing, while `hitsIn` still counts
the blow (it is tallied before the close). The build plants in `resolveHit` with the window open, so the
killing blow plants too; that bramble never acts, because the fight is over. So built brambles a cast equal
built blows in windows a cast, while the lab's `patches` sits below its `hitsIn`. From the per-fight rows of
the scratch `s0_ASBC_*` and `lab_dur917_*` jsons (`runs/lab_patches_vs_hitsin.txt`, `runs/tools/patches_count.py`): in every lab fight `hitsIn - patches` is 0 or 1. The 1 falls in 156-221
of Thornwake's wins a block and in only 1-7 of its losses, which leaves 0.08 (B) to 0.11 (C) of a bramble a cast
uncounted. Compared like for like, as blows in windows a cast:

```
                       lab, dur 8 (hitsIn / patches)     lab, dur 9.17 (hitsIn / patches)    built (blows in windows = brambles)
B / stage 2            1.43 / 1.35                        1.59-1.62 / 1.50-1.52               1.59
C / stage 3            1.42-1.43 / 1.32                   1.61-1.62 / 1.50                    1.60 (the final: 1.61)
```

At the engine's window length, the lab's blows in windows equal the build's plants. About 0.1 of the 0.24-0.28
bramble-a-cast gap between the built links and the lab at 8 is this counting difference. The rest is the clock.

**The brief's gates, read:**
- stage 1 (the brambles, entangle + bite): "~1.3 brambles a cast, ~5.7 ticks, relic ~51% at 31.35 (arm B)" —
  lab on 151 1.35 / 5.79 / 50.2; built 1.59 / 5.86 / 53.1. The longer built window plants more (the lab at
  9.17 plants 1.50-1.52). The lab's count also leaves out the killing blow (above), so on the matched count,
  blows in windows, the lab at 9.17 reads 1.59-1.62 against the built 1.59;
- stage 2 (the snare): "~2.9 snares a cast counted as TRANSITIONS, relic ~60%" — the lab's own `roots` column
  IS a transition count (2.89 on 151, 2.92 published); built 3.28 transitions (the lab at the engine's window
  3.23-3.27); relic: lab C 63.8 on 151 (59.7 published on 141), built 65.2.

**Published (Chromium 141) against 151.** The design's own run, replayed on 151 with its lab as published
(`sc-trunk`, seed0 2207, 10 seeds, the 33 foes, 330 fights an arm; `runs/pub151_base.*`):

```
arm                        published 141   on 151   foes' rates identical   mechanism a cast (brambles, snares, bites, damage) 141 -> 151
A                          33.9            35.2      6/33
SHIP                       47.9            45.8      8/33
B entangle + bite          51.2            49.4     12/33                   1.36 -> 1.36   -      5.73 -> 5.78   11.45 -> 11.57
C + the snare (taken)      59.7            64.8      8/33                   1.32 -> 1.37   2.92 -> 2.98   7.75 -> 7.96   15.51 -> 15.92
```

The runtime is an input: the same seeds are different fights on 151 (6-12 of 33 foes' rates identical). The
mechanism reproduces to the second digit; the taken arm reads 5.1 higher on 151 (63.8 on 20 seeds of the base).

## 3. The probe (`thornwake_probe.py --stage N`, one check per sentence, read inside the hooks)

The probe wraps `step`, `tickBramble`, `plantBramble`, `resolveHit`, `tickCharge`, `fireUlt`, `move` and
`tickHits`, and runs Thornwake both sides against every other relic, 6 seeds (444 fights). **Every number is
pinned by `--stage`, from the builder** (window, charge, radius, life, cadence, entangle, bite, snare, blade),
never read off the link under test. The checks READ THE ENGINE'S OWN ANSWER where one sentence feeds
another, so each fails alone: [3] rebuilds the brambles and INSIDE from the geometry; [4] and [5] take INSIDE
from the engine (`brambleIn`) and check what follows from it. The eight checks:
- **[1] "for a duration"**: exactly one `tickBramble` on every unfrozen step and none on a frozen one; `t`
  advancing by dt a call; a clock window exactly the calls the clock takes to reach 8 (960); a close on
  either death; a cast opening a fresh window with the thorns' cooldown clear; only Thornwake carrying
  `ultBramble`.
- **[2] "every blow the scythe lands leaves a bramble on the floor where it landed"**: every blow in the
  window plants exactly one bramble `{x, y}` = the struck ball's centre, `t0` = the brambles' clock, the
  caster's side; none from a blow outside the window; the brambles on every step exactly the step's plants
  and expiries (nothing else adds one); no bramble on another side.
- **[3] "r 80 ... life 6s ... outlives the window; the hall's close does not clip it"**: after every tick the
  brambles are EXACTLY the survivors of `brambleT - t0 < 6` (same objects, same order, none moved, none
  early, none late); the thorns tested exactly while the window is open or one of the caster's brambles
  lives; INSIDE exactly "the foe alive and its centre within 80 + R of one of the caster's brambles". Its
  coverage demands brambles acting AFTER the window closed.
- **[4] "snared — rooted for a moment" (ball and weapon)**: on an entry (per the engine's inside) at rootFor
  0.6: pin = max(pin, 0.6), pinMax likewise, pinV a fresh `[vx, vy]` iff no longer hold stood (else the old
  one kept), pinFree untouched; no pin write anywhere else (and at stage 2, none at all while entries are
  still counted); a ball the snare holds never moves in `move()`, never lands a blow, and enters its hit
  loop with its weapon locked (from the step after the snare, once `tickStasis` has run).
- **[5] "while it stays in one it is entangled and bitten"**: the cooldown `-= dt` on exactly the tested
  frames; a bite exactly when inside with the cooldown clear; a bite is entangle +1 by side letter THEN
  hurt(foe, 2, Thornwake) once, taking exactly 2 off hp + shield, the cooldown then 0.5; no application or
  hurt on any other frame or body.
- **[6] "no knock, no hit stop, no beat", and nothing else**: every blow of Thornwake's rebuilt exactly from
  its captured crit and jitter draws, in the window and out (the scythe is the scythe); around every
  `plantBramble` and every `tickBramble` on which the geometry expects a snare or a bite, every close and
  every 16th live call, no RNG and no field of either fighter, a shade or the match changed but the
  sentence's own; the foe never moved, the caster never moved and the hit stop never touched except by a
  ward's own shatter (which bursts the pool at Thornwake, flings it, draws the RNG for its sparks and stops
  the world, as every ward break does; counted).
- **[7] a killing bite files exactly one fatal hit beat** at the foe (`bramble: true`); no other frame of the
  thorns files one.
- **[8] the charge on the game's clock, the window 8**: a cast exactly on the frame the live charge clock
  reaches 14, never with the window open; the row's charge, window, radius, life, cadence, entangle, bite,
  snare, kind and blade the pinned stage's.

Results (`runs/probe_*.txt`, 444 fights each; the stage links are re-run with the final probe):

```
link                    stage  checks  casts  blows in/out   brambles  bites  dmg    snares  frozen  killing bites  wards broken  shade plants
                                         a fight          a cast    a cast a cast  a cast  (window)
sc-thornwake-bramble    2      8/8     3.05   4.84/5.81     1.59      5.86   11.7   0.00    12.8    19             111           25
sc-thornwake-snare      3      8/8     3.07   4.93/5.88     1.60      7.71   15.4   3.28    12.3    29             183           11
sc-thornwake-b26.5      5      8/8     3.31   5.32/6.15     1.61      8.17   16.3   3.46    12.3    24             163           18
```

The final (`runs/probe_final.txt`): 3.31 casts a fight; 5.32 blows a fight in windows, 6.15 outside; a cast
plants 1.61 brambles, bites 8.17 times for 16.3 damage and snares 3.46 times (every snare a transition);
**1807 brambles expired, each after 719-720 steps of the brambles' clock** (6s); 3,650 of 11,992 bites and
1,445 of 5,077 snares came after the window closed; 24 killing bites, each with its one fatal beat; 163 wards
broken by a bite (the ward's own shatter, counted); 18 shade blows planted at the shade; 54 re-snares on a
held ball (25 under a longer hold, whose `pinV` was kept); 360,117 snared steps held still and 355,142 snared
hit loops quiet; 12.3% of window steps frozen (the census); 2,360 plant calls and 115,926 ticker calls
snapshotted whole, clean; no bite from a slain caster's brambles in these 444 fights.

**Three passes, and what each found** (the probe's own history, kept in `runs/probe_pass1/` and
`runs/probe_pass2/`):
1. **Pass 1 on the final: 7/8.** [4] failed once: "a snared foregone with its weapon free (stun 0, pin
   0.6)". A RE-SNARE on the very step the ball's old hold ran out: `tickStasis` had already run that step (pin
   to 0), so the weapon lock the new pin buys starts next step — exactly as for a fresh snare, which the probe
   already exempted, and as in the lab, which pinned after the whole step. The check was over-strict, not the
   build: it now exempts the snare's own step on every snared ball (30 such steps in the final's fights) and
   still demands the lock on every later held step.
2. **Pass 2: the final 8/8, and mutant m3 failed [3] AND [5].** [5] had read the probe's own predicted
   "tested" (from its rebuilt bramble list), so a broken list also broke the cadence check. [4] and [5] now read
   the ENGINE's answers (the tally's `tested`, and `brambleIn`), and a broken list fails [3] alone.
3. **Pass 3: m3 failed [3] and [5], [5] now only as NOT EXERCISED** — [5]'s coverage had demanded bites
   AFTER the window, which is [3]'s sentence ("outlives the window"; [3]'s own coverage demands the foe inside
   a bramble after the close). The coverage moved to [3] alone (a Python-side change: no check's reading
   moved), and the final and the mutants run before that change (m1-m5) were probed again with the final
   probe. Every result below is the final probe's.

**Controls** (`runs/probe_mutants.txt`; `tools/mutants.py`, in scratch, writes them from the final): each
mutant changes fights (the probe's own 444: wins, blows, casts, brambles, bites or snares against the
final's), fails the check named for it, and nothing else — m11 aside, which cannot change a fight.

```
the final (--stage 5): 8/8; wins 213/444, blows in/out 2360/2732, casts 1468, brambles 2360, bites 11992, snares 5077

m1-window-labclock       ede9e3a831b0aefc  want [1]  fails [1] {1: 350692}  wins 207/444 blows 2102/2979 casts 1458 brambles 2102 bites 11472 snares 4219  fights CHANGED  -> OK
      [1] e.g. tickBramble ran 1x on a frozen step
m2-every-other-blow      73f8035e4cd29ad7  want [2]  fails [2] {2: 1133}  wins 160/444 blows 2288/2687 casts 1454 brambles 1155 bites 7536 snares 3311  fights CHANGED  -> OK
      [2] e.g. a blow in the window planted 0x (0 -> 0)
m3-cleared-at-close      3cf01018a9262c54  want [3]  fails [3] {3: 1785}  wins 182/444 blows 2468/2619 casts 1452 brambles 2468 bites 8423 snares 3643  fights CHANGED  -> OK
      [3] e.g. the brambles after the tick: 0, want 3 survivors of 3
m3b-radius-plus10        c52caefcf8d7c7e1  want [3]  fails [3] {3: 245503}  wins 235/444 blows 2417/2655 casts 1461 brambles 2417 bites 12396 snares 4992  fights CHANGED  -> OK
      [3] e.g. inside true, the geometry says false
m4-weapon-free           ca3731586a583544  want [4]  fails [4] {4: 435}  wins 178/444 blows 2304/2622 casts 1428 brambles 2304 bites 11652 snares 4942  fights CHANGED  -> OK
      [4] e.g. the snare wrote pinFree 0 -> 1
m5-entangle-2            c4d0650f7b1b5b8c  want [5]  fails [5] {5: 11889}  wins 217/444 blows 2392/2688 casts 1473 brambles 2392 bites 11889 snares 5023  fights CHANGED  -> OK
      [5] e.g. applications [["entangle",2]], want [["entangle", 1]]
m6-bite-hitstop          d0230d2a74cc60de  want [6]  fails [6] {6: 23602}  wins 216/444 blows 2433/2735 casts 1443 brambles 2433 bites 12146 snares 5092  fights CHANGED  -> OK
      [6] e.g. the hit stop -0.008333333333333309 -> 0.05 with no ward broken
m6b-bite-knock           465173536a599d4c  want [6]  fails [6] {6: 24209}  wins 223/444 blows 2447/2749 casts 1481 brambles 2447 bites 12209 snares 5157  fights CHANGED  -> OK
      [6] e.g. the thorns moved the foe
m7-charge16              d1b82ff00102b710  want [8]  fails [8] {8: 304199}  wins 202/444 blows 1985/3055 casts 1238 brambles 1985 bites 9820 snares 4136  fights CHANGED  -> OK
      [8] e.g. the row's charge is 16, the stage's 14
m8-row-no-snare          6f5b535be7a81858  want [4, 8]  fails [4, 8] {4: 6629, 8: 1}  wins 155/444 blows 2246/2638 casts 1420 brambles 2246 bites 8685 snares 0  fights CHANGED  -> OK
      [4] e.g. an entry counted 0 snares
      [8] e.g. the row's rootFor is 0, the stage's 0.6
m9-blade-shipped         800daceb906ef28e  want [8]  fails [8] {8: 1}  wins 280/444 blows 2190/2612 casts 1365 brambles 2190 bites 10519 snares 4482  fights CHANGED  -> OK
      [8] e.g. the blade is 31.35, the stage's 26.5
m10-snare-every-frame    b0023fcc6755d68f  want [4]  fails [4] {4: 2973966}  wins 362/444 blows 2602/2858 casts 1455 brambles 2602 bites 17024 snares 997238  fights CHANGED  -> OK
      [4] e.g. 1 entries counted, want 0
m11-kill-no-beat         c66ca48a65db4867  want [7]  fails [7] {7: 24}  wins 213/444 blows 2360/2732 casts 1468 brambles 2360 bites 11992 snares 5077  fights UNCHANGED (a beat cannot change a fight)  -> OK
      [7] e.g. a killing bite filed 0 beat(s), 0 fatal

EVERY MUTANT FAILS ITS OWN CHECK(S), ONLY THOSE, AND CHANGES FIGHTS (m11 aside, a beat)
```

`m8` is the final with its stage-3 number undone (a link that lost its snare; byte-identical to stage 2's link
at blade 26.5), `m9` the final with its blade undone (byte-identical to stage 3's link, 800daceb906ef28e):
the pinned stage catches both. `m11` (a killing bite files no beat) is the only control for [7]; a beat is read
by the director alone, so it cannot change a fight, and the table says so.

## 4. Stage 5: the blade — 26.5, nearest 50% both sides (Rick's ruling)

The brief's stage 3: "the blade, wide on 151 at 28 / 29 / 30 to the shipped rate". **Rick's ruling
(2026-09-29, after the design was written: "you pick the blades. do whatevers best for balance.") replaces
that target with the measured point whose win rate BOTH SIDES is nearest 50%**, for every redesign; the
design's own target, the shipped rate, is measured beside it. **The design gives the build no knob to move
before the blade** (§6.3's bramble life, 6s against 8s, is "a design line", Rick's), so no knob moved. Both
sides (`relic_rate.py`: each seed played from both sides; every other relic a foe, 10 seeds a foe a side, 740
fights a block; seed0 2207 and 2317; `runs/stage5_rr_*`, table `runs/stage5_table.txt`), charge 14, on stage
3's link with `--set dmg=`, a fixed grid read after (the brief's 28 / 29 / 30, widened down in whole and then
half steps over 24-28 when 28 read 55), no bisection:

```
point                                          block 2207  block 2317   pooled    wins/fights   side A   side B   mean dur   (link)
SHIPPED Bramblesnare (the 1.6s root), 31.35, ch 15   46.9       48.8       47.8      708/1480      48.9     46.8     57.7s   sc-tendril-t3 (the base)
24     (charge 14)                               42.0       42.3       42.2      624/1480      43.0     41.4     61.9s   stage 3 --set dmg=24
24.5   (charge 14)                               44.9       43.0       43.9      650/1480      45.4     42.4     61.6s   stage 3 --set dmg=24.5
25     (charge 14)                               45.3       45.7       45.5      673/1480      44.9     46.1     61.3s   stage 3 --set dmg=25
25.5   (charge 14)                               50.1       44.9       47.5      703/1480      47.6     47.4     61.0s   stage 3 --set dmg=25.5
26     (charge 14)                               50.9       46.4       48.6      720/1480      47.6     49.7     60.7s   stage 3 --set dmg=26
26.5   (charge 14)                               51.8       50.0       50.9      753/1480      52.4     49.3     60.5s   stage 3 --set dmg=26.5
27     (charge 14)                               53.0       51.6       52.3      774/1480      52.3     52.3     59.7s   stage 3 --set dmg=27
27.5   (charge 14)                               53.6       52.2       52.9      783/1480      52.8     53.0     59.4s   stage 3 --set dmg=27.5
28     (charge 14)                               55.7       55.0       55.3      819/1480      56.1     54.6     59.3s   stage 3 --set dmg=28
29     (charge 14)                               58.5       57.3       57.9      857/1480      59.2     56.6     58.7s   stage 3 --set dmg=29
30     (charge 14)                               61.2       60.4       60.8      900/1480      63.6     58.0     58.0s   stage 3 --set dmg=30
31.35  (charge 14) the shipped blade             64.5       62.3       63.4      938/1480      63.8     63.0     57.3s   sc-thornwake-snare (stage 3)
26.5   (charge 14) = THE FINAL                   51.8       50.0       50.9      753/1480      52.4     49.3     60.5s   sc-thornwake-b26.5 (stage 5)

THE 50% CROSSING (Rick's ruling, charge 14): the measured point nearest 50.00% is blade 26.5: 753 of 1480 = 50.88% (one SE 1.30 points); in wins from the target: 24 -116, 24.5 -90, 25 -67, 25.5 -37, 26 -20, 26.5 +13, 27 +34, 27.5 +43, 28 +79, 29 +117, 30 +160, 31.35 +198
  linear between the bracketing points 26 (48.6) and 26.5 (50.9): 26.30
THE SHIPPED REFERENCE: Thornwake as shipped on the base (the freeze), 708 of 1480 = 47.84% both sides
THE DESIGN'S OWN TARGET (the shipped rate on 151): the measured point nearest 47.84% is blade 25.5: 703 of 1480 = 47.50% (one SE 1.30 points); in wins from the target: 24 -84, 24.5 -58, 25 -35, 25.5 -5, 26 +12, 26.5 +45, 27 +66, 27.5 +75, 28 +111, 29 +149, 30 +192, 31.35 +230
  linear between the bracketing points 25.5 (47.5) and 26 (48.6): 25.65
```

- **The final, 26.5: 50.9% (753 of 1480) both sides**, against the shipped freeze's **47.8%** (708 of 1480) on the
  same seeds. 26.5 is the measured point nearest 50%: 753 of 1480 at `--set` (+13 wins from half; 26 is -20).
  **The crossing is ~26.3**, under the brief's "28 / 29 / 30": the brief aimed its three at the shipped rate
  from a 59.7 priced on Chromium 141, and arm C reads 63.8 on 151 (§2); the built relic reads 63.4 both
  sides at 31.35. 26.5 is inside the scythe row (9.5-31.35, §3).
- **The design's own target, the shipped rate (47.8% on 151), is nearest at 25.5** (47.5%, 703 of 1480, -5
  wins; the line through 25.5 and 26 crosses it at 25.65). Rick's ruling chose 50%, so the carry is 26.5;
  25.5 is one number away (`--set dmg=25.5`).
- **The stage-5 link is the measured relic:** `relic_rate` on `sc-thornwake-b26.5` with NO knob set reproduces stage 3 `--set dmg=26.5` EXACTLY on both blocks: 51.76% / 50.00%, every one of the 37 foes' rates, both sides' rates, the timeouts and the mean duration (60.9455s / 60.1244s) to the last digit (`runs/stage5_table.txt`, the PROOF lines: EXACTLY THE SAME; EXACTLY THE SAME).
- Side A and side B at the final: side A 52.4%, side B 49.3% (740 fights each, pooled over the blocks); block 2207 51.8%, block 2317 50.0%; mean 60.5s.

**The ladders** (40 fights a foe: 10 seeds x 2 sides x 2 blocks; `runs/stage5_table.txt` has every foe):

```
LADDER -- Thornwake / Bramblesnare REDESIGNED, THE FINAL (sc-thornwake-b26.5: charge 14, blade 26.5 -- Rick's ruling, nearest 50%), both sides
(40 fights a foe: 10 seeds x 2 sides x 2 blocks, relic_rate seed0 2207 + 2317). Pooled: 50.9%
by type  greatsword 62%  twinblade 61%  flail 50%  warhammer 50%  scythe 44%  bow 38%
by foe   gloamwire 20.0  bloodmirror 32.5  ironhail 35.0  aureole 37.5  cindercleave 37.5  bindweed 40.0  farwarden 40.0  ironwood 40.0  shroudmaul 40.0  duskreave 42.5  paradox 42.5  censer 45.0  dawnbringer 45.0  oathwound 45.0  slagheart 45.0  vinesower 45.0  widowmaker 47.5  foregone 50.0  lastlight 50.0  marrowdraw 50.0  redflail 50.0  vesper 50.0  bulwarden 52.5  gravemourn 57.5  portcullis 57.5  ravelbone 57.5  emberedge 60.0  morningstar 60.0  twinshade 60.0  spellbreaker 60.0  grudgebearer 62.5  heartwood 62.5  thornshear 62.5  axiom 70.0  nightfell 72.5  starwarden 75.0  lightkeeper 82.5

LADDER -- the redesign at the shipped blade 31.35 (sc-thornwake-snare, stage 3: charge 14), both sides
(40 fights a foe: 10 seeds x 2 sides x 2 blocks, relic_rate seed0 2207 + 2317). Pooled: 63.4%
by type  greatsword 76%  twinblade 74%  flail 65%  scythe 65%  warhammer 55%  bow 46%
by foe   ironhail 35.0  marrowdraw 40.0  gloamwire 42.5  aureole 47.5  shroudmaul 47.5  grudgebearer 50.0  ironwood 50.0  farwarden 55.0  paradox 55.0  vinesower 55.0  bulwarden 57.5  censer 57.5  cindercleave 57.5  bloodmirror 62.5  morningstar 62.5  redflail 62.5  spellbreaker 62.5  widowmaker 62.5  emberedge 65.0  lastlight 65.0  vesper 65.0  axiom 67.5  duskreave 67.5  gravemourn 67.5  portcullis 67.5  ravelbone 67.5  bindweed 70.0  foregone 70.0  slagheart 70.0  dawnbringer 72.5  twinshade 72.5  nightfell 77.5  oathwound 80.0  heartwood 82.5  thornshear 82.5  lightkeeper 85.0  starwarden 87.5

LADDER -- Thornwake as SHIPPED (sc-tendril-t3: the freeze, charge 15, blade 31.35), both sides
(40 fights a foe: 10 seeds x 2 sides x 2 blocks, relic_rate seed0 2207 + 2317). Pooled: 47.8%
by type  greatsword 65%  warhammer 50%  twinblade 50%  flail 48%  scythe 45%  bow 28%
by foe   gloamwire 17.5  ironhail 17.5  farwarden 25.0  twinshade 25.0  aureole 27.5  cindercleave 35.0  marrowdraw 35.0  paradox 37.5  bulwarden 40.0  gravemourn 40.0  bloodmirror 42.5  vesper 42.5  duskreave 42.5  redflail 42.5  vinesower 42.5  shroudmaul 45.0  dawnbringer 47.5  slagheart 47.5  thornshear 47.5  ironwood 47.5  lastlight 50.0  morningstar 50.0  censer 52.5  emberedge 52.5  grudgebearer 52.5  bindweed 55.0  foregone 55.0  widowmaker 55.0  oathwound 60.0  portcullis 60.0  starwarden 60.0  nightfell 62.5  spellbreaker 62.5  ravelbone 65.0  axiom 72.5  lightkeeper 75.0  heartwood 82.5
```

At 26.5 the type spread is 25 points (greatsword 62% .. bow 38%), narrower than the shipped freeze's 37 (65 ..
28), at a blade 4.85 lighter: the brambles lift Thornwake's worst matchups most (bows 28 -> 38; Ironhail 17.5
-> 35, Farwarden 25 -> 40, Twinshade 25 -> 60) and hold it roughly level against the greatswords and hammers
(65 -> 62, 50 -> 50). Its worst matchups are Gloamwire (20%), Bloodmirror (32.5), Ironhail (35); its best
Lightkeeper (82.5), Starwarden (75), Nightfell (72.5). The design printed no ladder; the type spread is item
12/32, Rick's.

### 4a. The gates on the final — every one able to fail

- **engine_ab sc-tendril-t3 -> sc-thornwake-b26.5, the 37 others (every base id but Thornwake), n=6:
  3996/3996 identical** (666 pairings, 37/37 distinct winners, 3996 distinct seeds, 21.5-115.1s;
  `runs/engine_ab37.txt`, ids in `runs/ids37.txt`). The redesign moves no other relic's fight. **Control:** the
  same gate with Thornwake in (thornwake, grudgebearer, aureole, gravemourn, n=6): **18 of 36 differ** — the
  count of Thornwake's own fights (3 pairings x 6), and the 37-relic gate shows no other fight moves
  (`runs/engine_ab_control.txt`).
- **verify --n 40 on sc-thornwake-b26.5 (38 relics): 10/13** (`runs/verify_final.txt`; 28,120 fights, 40 seeds x 703
  pairings, 2713s). **Thornwake 52.4%** (verify pairs `i < j` over the roster, so Thornwake, 4th, is side B
  against the 3 relics before it and side A against the 34 after); every relic in 30-70% (Heartwood 30.1 ..
  Gloamwire 63.8, spread 33.7pp); no timeouts. **The three reds, and none is Thornwake's:** the two clock
  bands (every pairing 18-70s — Farwarden/Starwarden 100.0s; overall 28-54s — 60.9s), red on every link since
  the minute pace; and "both sides can win every matchup" on **Heartwood v Twinshade 0/40 and Heartwood v
  Bindweed 0/40** — not Thornwake's pairings: the base's own two (v101 §4 reports exactly these on
  `sc-tendril-t3`), and engine_ab above proves no other relic's fight moved. Item 12/32, Rick's.
- **tip_audit:** identical to `sc-tendril-t3`'s below the header (`runs/tip_audit_final.txt`,
  `runs/tip_audit_base.txt`). The card is not a status tip; its 66 characters are the builder's check.
- **chain_audit** `--relic sc-thornwake-b26.5 --tip sc-thornwake-b26.5 --builder thornwake_build.py`: **ALL 10
  INSERTS SURVIVE** (`runs/chain_audit.txt`). **Controls:** the base as the tip loses all 10 and exits 1
  (`runs/chain_audit_control.txt`); stage 3's link as the tip loses only S5, the blade, and exits 1
  (`runs/chain_audit_control_blade.txt`) — the blade is watched like every other insert.
- **thornwake_probe --stage 5 on the final: 8/8** (§3), stage 3 8/8, stage 2 8/8.
- **Stage 1 = arm A fight for fight** on both blocks (§2). **The stage-5 link is the measured relic** (above).
- **The builder:** every link rebuilds byte-identical from the bare base (`runs/rebuild_final.txt`, builder
  sha256[:16] in the file), and it refuses to run twice, out of order, over a link or under another name; its
  scan refuses all 20 negative copies (`runs/builder_negatives.txt`); the dry carry applies on five later tips
  and Heartwood's builder applies on this final (`runs/carry_dry.txt`).

## 5. Stage 6: the picture and the voice — `sc-thornwake-b26.5-fx`

Design §4 (the picture, the sound) and its §5 brief stage 4, "picture, voice, carry; `_drawField`'s hexagon must
not draw on the snare (the Tendril root picture instead); `engine_ab`, `shell_identity`, `render_ab`,
`chain_audit`, one fight watched", this build's stage 6. Picked on measurements under Rick's "you pick i
overrule" by two labs (the picture lab's scratch, `stage6-picture/tw_rows.py`, and `tools/thornwake_voice_lab.py`
216c329d6c8c3568), and built as `thornwake_build.py --stage 6` on the final stage-5 link (the b26.5): **sixteen
anchored edits (voice 4, picture 12)**, byte-exact to the labs' own row files (voice `rows_final.json`
a539532139eb01b7, picture f80fbfe244abacde; copied as `runs/stage6_voice_rows.json` and
`runs/stage6_picture_rows.json`).

```
sc-thornwake-b26.5.html          stage 5  the blade (the base of stage 6)                        fd5031063ecb6807
  -> sc-thornwake-b26.5-fx.html  stage 6  the picture and the voice (presentation, +28,549 chars) d306822d6914c08c
```

- **The rows, reproduced** (`runs/stage6_gen_s6.txt`; the generator is `runs/tools/gen_s6.py`, the pattern's:
  rows == files, the stamps, no nested anchor, merge by anchor line, a table written with triple-quoted
  strings, refusing a builder that already carries S6): the picture rows alone give the picture lab's stamp,
  **65a84cedda239548** (its `tw-final.html`, byte for byte); the voice rows alone the voice lab's end-to-end
  page, **8f8d06e90d66fc3f**; both sets, either order and all sixteen reversed, **d306822d6914c08c**, the fx
  link. No two rows share an anchor line, so none is merged; no row's anchor sits inside another row's anchor
  or code, and no two anchors' spans overlap. **Eleven re-emit their anchor and five replace it**, all five
  Thornwake's own: the synth's arm keyed on this relic (the freeze's "creak and cinch", four lines),
  drawUltUnder's and drawUltOver's `u.w === "thornwake"` branches (the freeze's roots and thorns), and the
  narrowest tokens of the life map (`thornwake: 2.4, `) and the banner-seat map (`thornwake:1, `), which leave
  the other entries on those lines to their own builds. Twenty-six new names (`tickBrier`, `drawBrier`,
  `drawBrierTop`, the seven `_brier*` methods, the thirteen `brier*` fields, the three voice ids), each free on
  the base on identifier boundaries — `brier`, never `bramble`, which is the simulation's.
- **Composition.** The voice rows ride on four of stage 2's own lines (the fighter's fields, plantBramble's
  count, the snare's count and the bite's cooldown re-arm) and the Sfx row replaces only Thornwake's own arm,
  so the shared rune-crack fallback is untouched; the picture's call and methods sit beside shared lines
  (`tickPresentation`'s first call, the world pass's `drawTree` and `drawTreeTop`, drawWeapon's `if
  (f.ultDraw){`, `_drawField`'s guard, `drawMotes`, `tickWinnow`) and re-emit them. The hexagon's row is a
  `return` inserted BEFORE the guard `if (f.pin > 0 && !f.pinFree`, touching no existing line: on a tip that
  carries Tendril's picture, whose own row extends that guard (`&& !(f.twineHeld > 0)`), both apply in either
  order. **The carry, dry, stages 1-6** (`runs/stage6_carry_dry.txt`): on `sc-spellbreaker-fxout` (the newest
  02-chain tip, 42 relics), `sc-aureole-fxout`, `sc-ironhail-fxout`, `sc-coldiron-temper-fx`, `sc-tendril-fx`
  (Tendril's own picture and voices) and Heartwood's scratch `sc-heartwood-b11`, every stage applies and **stage
  6's change on each tip is its change on the base**: fifteen hunks, byte-identical on five tips; on
  `sc-spellbreaker-fxout` thirteen byte-identical and two where the same token comes out of a shared map line
  that Spellbreaker's own stage 6 had already shortened. Heartwood's builder (stages 1-5) applies on this fx
  link. The picture lab also carried its rows onto 18 tips (the 02-chain line and nine scratch pictures,
  forward == reverse on each) and with Heartwood's nine picture rows in both orders (the same multiset of lines:
  two rows share an anchor with Heartwood's and land in the other order; `runs/stage6_picture_order.txt`); the
  voice lab co-applied its Sfx rows with Heartwood's, Bindweed's, Spellbreaker's and Widowmaker's in both orders.
- The picture sheet is `05-reference/v113/thornwake-picture-sheet.png` (81a9e4d5ea646b85, 2200x3255); the voice
  lab's wavs are `05-reference/v113/thornwake-*.wav` (29 files, raw level; gitignored).

### 5a. The picture

Every number here is the picture lab's: headless Chromium 151 at 540x960 with the post chain on (m3, on the
final bytes: 10 fights, 139 frames, white, dark and ordinary foes; `runs/stage6_picture_m3_summary.txt`), on
its shipped-look page (the rows, with `SPECS.thornwake` taken out of the inlined `fx.js` as the carry will:
f0a988952fee0d80, the page `fx_remove`'s own `spec_block` would cut; 5b).

- **A bramble is floor** (v84 §4: "a tangle of dark-green thorn strokes on the floor (verdant `dark` with
  `core` highlights, r 80, source-over, alpha 0.5), growing out from the hit point over 0.3s and browning in
  its last second"): seven long canes arching through it — each starts within half the radius of the hit
  point, sets off outward and bends one way or the other until it reaches the edge — and a short offshoot off
  each, thorns along them all, in the school's `dark` with a `core` seam at 0.5, inside the simulation's own
  radius (`patchR`, read off the caster, so the edge is where the test is). Placed once, by `shellHash` on the
  bramble's own planting step and position, so a bramble is the same tangle for its whole life and no RNG is
  drawn. It **grows** out of the hit point over 0.3 s of the PRESENTATION clock (a clip circle widening), so
  it grows through the planting blow's own hit stop; it **browns** over the last second of its life on the
  simulation's clock (`patchLife - (brambleT - t0)`, to `#2A2012` / `#6E5B2E`) and is gone the step the
  simulation removes it; after the verdict the tangles fade over 0.3 s. **Leaves lift off every bramble**, four
  a bramble, 30 units, turning and fading (the design's field, drawn: 5b). The world pass, under both balls,
  source-over: nothing under `lighter`, nothing the bloom sees, and no ball's disc can be painted over.
- **The snare** (§4: "four thorn shoots up the foe's rim for the pin's length (the Tendril root picture,
  reused)"): Tendril's root picture is not on this base (it is on `sc-tendril-fx`), so it is ported into this
  relic's own method, `_brierRoot`, the same picture: four stalks rise out of the bramble the ball is caught in
  (from 1.55 R under its centre — the bramble, not the hall's floor, which is Tendril's), grow in 0.12 s,
  clench round the rim in 0.1 s more, hold for the pin, dry through its last 30%, and wilt 0.2 s after it lets
  go; `dark` strands with a `core` seam and `core` tips, the caster's school on whatever ball it holds. The
  stalks are floor (under both balls), the clench is over them. **Paradox's hexagon is kept off a ball the snare
  holds**: `brierHeld` is presentation state, 1 exactly while the snare's pin holds (from the step the tally's
  `snares` rises to the pin's end), and a `return` inserted before `_drawField`'s guard skips the hexagon (the
  method's last block) for such a ball; `pinFree` stays 0, so the weapon stays locked.
- **A bite** (§4, "a soft snap"): four thorns flash out of the foe's rim on the side of the bramble it stands in
  (underneath when it stands on the centre), glow over a dark edge, 0.12 s (Tendril's flash). **The ENTANGLE
  tag counts** (Tendril's rule): a bite whose count is not the one last printed tags ENTANGLE and the count on
  the foe, one tag up at a time, none while the count sits at its cap; a tag already up there (the scythe's own
  blow tags it) takes the count instead.
- **The cast** (§4: "the scythe's blade greens for the window"): the verdant scythe's crescent
  (`SHAPES._scCrescent`, the blade `_scGrown` fills pale) filled green over its steel — `core` at the edge to
  `dark` at the heel — with its edge and inner thorns relit in `core`, drawn in `drawWeapon`'s own blade frame
  after the shape, so it rides the blade and the foe's shell clips it as it clips the blade. Up over 0.25 s at
  the cast, down over 0.3 s at the close, a death or the verdict (`tickBramble` never runs once `over` is set,
  so the picture reads the window as closed at the kill). The cast banner now stands on the caster.
- **The freeze's art is retired:** drawUltUnder's floor roots running caster to quarry and drawUltOver's nine
  glowing thorn vines on the pinned quarry (nothing pins at the cast now, so they fell on a free ball); the
  record's life entry 2.4 ("the art has to still be on screen while the hold it is explaining is in force")
  goes, so the cast's record takes the map's own 1.5; the onTarget seat goes, so the banner stands on the
  caster. Kept: the charge sigil `ULTSIG.thornwake` ("a thorn ring that CLOSES as the charge fills" — it reads
  as the snare) and the banner's letters keyed on the id (the name is kept); neither is the freeze's.
- **All of it off the fighter** and never `m.ultFx` (one slot, which the opponent's cast takes: open item 25):
  thirteen `brier*` fields on the fighter (the blade's green, its clocks, one picture record a bramble
  `{b, age, g}` holding the simulation's own bramble by reference, read and never written, the tally's snares
  and ticks as last seen, the tag's count, the bite flashes, and on the held ball the shoots' state), driven in
  `tickPresentation` (`tickBrier`), which watches `brambleTally.snares` and `.ticks` rise, so `tickBramble`
  makes no call for the picture.

The lab's rounds (its `STATE.md`, copied as `runs/stage6_picture_STATE.md`): v1's tangle read as a spoked wheel;
v2 made it seven arching canes and offshoots grown by a clip circle; v3 made the canes arch (a turn of 0.07-0.17
a step) instead of looping, and dropped a shade under the tangle that measured 0.026 of legibility. Looked at on
white, dark and ordinary foes each round (its `snaps/_look*.png`, in the lab's scratch).

**The measurements** (m3; the controls must fail and do):

```
BLOOM   the picture's share of the chain's arena-mean lift     +0.0000 (max; gate +0.02)   floor alone +0.0000
        art on a foe's disc (tags out)                         <= 0.0047 (sanctified, white), umbral 0.0036, dwarven 0.0030,
                                                               runic 0.0031;  on the caster's 0.0014
  CONTROL 1  a white lighter wash r 300 at every bramble       lifts +0.047, over 0.02 on 103/139       FAILS, as it must
  CONTROL 2  a white-hot glow on the caster while green        caster's disc past 0.90 on 92/104        FAILS, as it must
  CONTROL 3  the snare as a filled white disc over the foe     foe's disc past 0.90 on 35/54 snared      FAILS, as it must
LEGIBILITY (median |dL| of the component's own pixels, out of a hit stop / in one)
  the tangle 0.138 / 0.112   growing 0.092   browning 0.139   leaves 0.158 / 0.120
  the snare's stalks 0.198   stalks + clench + flash over the ball 0.235 / 0.219   a bite's flash 0.252
  the blade's green 0.142 / 0.079 (0.147 at the close)   the ENTANGLE tag 0.245
```

- **The scythe's silhouette** (`runs/stage6_picture_sil_final.out`): Thornwake's resting blade reads |dL| 0.164,
  fourth of the seven scythes (Lastlight 0.231 .. Cindercleave 0.113); the redesign moves no body stat.
- **Identity, the lab's** (`runs/stage6_picture_verify.out`): 15 fights x 3 (the rows, the shipped look, drawn)
  identical at the kill to the base, with a sim-write control (the foe nudged 1e-9 where the picture tags)
  differing on all 13 Thornwake fights; drawn through the kill and the verdict, 22,510 draws, none thrown, the
  picture's brambles the simulation's on every frame, the held ball the model's on 12,726 frames, **the hexagon
  off on 147/147 snares** (the same call with `brierHeld` put to 0, the control, drew it on all 147), 367 bites and 18 new tags, the
  green cooling 0.29-0.575 s after a close, the brambles gone within 0.29 s of the verdict, the weapon row
  unwritten. render_ab on its shipped look: 84/84 other-relic frames on 12 pairs pixel-identical, two Thornwake
  controls at 2/7; engine_ab 4218/4218 on its shipped look.
- **Frame cost** (the lab's Electron run, RTX 3070, the PC busy, interleaved; `runs/stage6_picture_cost.out`):
  the picture's own calls a median 0.8-1.5 ms a frame, p90 1.6-3.0 ms while brambles stand, 0.0 at rest (three
  fights: Aureole, Gravemourn, Lastlight; the third exited with nothing on stderr in the first run and was run
  again alone, `runs/stage6_picture_cost_ll.out`). The whole frame's medians with and without the rows move by
  the busy PC's own noise (-3 to +15 ms, their p90s both ways); the picture's own share is the number above.
  Reported, not a gate; the orchestrator's shell run is the app's.

### 5b. No new `fx.js` field: the leaves are drawn, and the freeze's spec goes out of both copies by the orchestrator

§4 asks for "leaf motes off each bramble, both copies". A `SPECS` field fires once, at the cast, where
Thornwake stands, from the one `ultFx` slot. The picture lab measured that slot against this window
(`runs/stage6_picture_fxprobe.out`, 105 windows on 16 foes x 2 seeds, both sides): **the slot is Thornwake's for
a median 0.65 s of the 8 s window** (max 0.72; 7.4% of the window's clock; the opponent's cast took it 18 times,
it expired 87); the brambles are planted a median 3.95 s into the window, and only 12 of 190 while the slot was
still Thornwake's; **a bramble stands a median 200 units from where the field is drawn** (more than its own
radius on 85%); and 35.6% of the brambles' lives fall after the window has closed. A field at the cast cannot
be leaves off each bramble. So the leaves are drawn, off every bramble for its whole life (5a), and **stage 6
adds no field: `fx_spec` is NONE** (Bindweed, Canopy, Zenith, Onslaught, Consecration and the Unmaking did the
same). The builder refuses a stage-6 build whose edits touched the inlined `fx.js` copy.

**`SPECS.thornwake` — the FREEZE's frost — is retired at the carry** by the orchestrator's `tools/fx_remove.py
--relic thornwake`, in both copies, never by this builder. Its exact text is the three lines quoted in §0 (184
bytes, sha256[:16] `8945c09d54396250`, byte-identical in the base, in every link including the fx link, and in
`src/render/fx.js` on disk), with the two-line FREEZE comment above it that `spec_block()` takes out with it
(five lines, 331 bytes, `29a0904df7aad6db`); on the fx link they are lines 32953-32957.

**FOR THE ORCHESTRATOR: `fx_remove.py --relic thornwake` REFUSES on this relic as it stands**
(`runs/stage6_picture_fx_diag.out`, the picture lab's): run `--dry` on the base (the b26.5, no stage-6 rows),
on the rows' page and on `sc-spellbreaker-fxout` + Thornwake's stages 1-5, each with a scratch copy of its own
inlined module, it prints the right five-line block and then **"REFUSING TO WRITE -- the page moved somewhere
other than the block and the stamps", rc 1**. The cause is its own check, not the page: its difflib alignment
takes the five-line removal one line early, because the line above the block, Vinesower's last line `spawn:
0.85, up: 0 },`, is the same text as Thornwake's own last line, so it compares a rotation of the block (and
Heartwood's entry below ends with the same line: its own removal will meet it). `--keep-comment` passes (dry:
stamp 28fc58641370a1a9 -> 34a920f4e29e8c21) but leaves the stale FREEZE comment in both copies. The picture
lab computed, in scratch, the page the removal should write (its `spec_block` imported read-only; the five lines
out of the inlined copy and the stamps moved; a multiset-of-lines check) — the shipped look it measured on,
f0a988952fee0d80. Which way to take the spec out (fix the alignment check, or `--keep-comment` and the comment
by hand) is the orchestrator's; this build touches neither `fx.js` nor `fx_remove.py`.

### 5c. The voice

`tools/thornwake_voice_lab.py` (216c329d6c8c3568; its docstring carries every number and the rounds), on
Chromium 151.0.7922.34 and the b26.5, wire seeds 113601-113602 (148 fights), end to end 113651 (74), and the
same stage 5 carried onto `sc-spellbreaker-fxout` (f7c32e86063abb8d, 82 fights). Every render through
`Sfx.buildChain` in an OfflineAudioContext at 48 kHz; noise-built sounds judged on the worst of twelve draws;
a candidate is its arm's own text, rendered, then the row applied to `Sfx.prototype.play`'s own source and
rendered again (to 1e-5). Its controls reproduce the published numbers first (rune-crack 0.608 / 450 ms; BAR
0.364 / 300 ms; the hit at 11.6 0.443 / 80 ms), and each voice's rule has controls that must fail it.

```
cast     8 NEEDLES  narrow bandpass grains (Q 8, 30 ms) ~60 a second, centres wandering 2310-3900 Hz, swelling to the middle;
                    under them a 330 Hz timber (a sine and its 2.76 mode at 0.4) pulsed slowing 45 -> 28 a second (a bough
                    bending: a creak is stick-slip). The rustle alone: noise (TONAL 7.0 dB), centred 3215-3752 Hz, its loudest
                    ms 117 ms in; the creak alone: 37 pulses a second (PULSED 0.74), -2.9 dB re the rustle; each owns a band
                    (+37 / +40 dB). Audible 395 ms; TOP -3.1 dB re the blow; heard +30.3 dB over the score. Register at most
                    0.77 (Scour's woosh); 0.65 against Thornshear's and Heartwood's casts, 0.62 against the creak it replaces.
                    Of 8: SPINES (0.78) passes and loses the tiebreak; THORNS, BURRS, LEAVES, BOUGH, BRUSH, BRIAR out.
crackle  5 KNOTS    8 ms bandpass clicks (Q 6) ~33 a second at centres 1185-2160 Hz, spaced x (1 + 0.45 sin 2.4k), thinning:
                    10 clicks, IRREG 0.30, DEPTH 20.6 dB; dry (B500 0.022, LOW 0.002, TONAL 2.3 dB); audible 280 ms (the
                    bramble's 0.3 s growth); TOP -11.1 dB re the blow it lands with; heard +17.6 dB after the blow's body;
                    register at most 0.73 (Scour's tick). Of 6: SPLINTERS, SNAPS, OPEN, EMBERS, TWIGS out.
snare    (reused)   Tendril's root, its nine-line body transcribed (not on this base): equal to Tendril's own arm to 1.5e-07
                    over 12 draws (a copy one constant 1e-4 off: 4.7e-05, the control); audible 355-370 ms, TOP -2.5 dB re
                    the blow, half its power under 120 Hz, the crack at 206 ms. Register at most 0.85 (Cindercleave's cast)
                    -- REPORTED, not gated: the design names it.
bite     1 STEM     a 10 ms bandpass snap at 1.1 kHz (Q 1.2) over a sine falling 620 -> 420 Hz: rise 1 ms, one snap, audible
                    65 ms; TOP -11.0 dB re the blow, +11.0 re the wall tick; the snap's first 10 ms centred at 678 Hz at
                    most (soft); heard +12.8 dB; register at most 0.39 (fork). Of 4: PRICK, PAD pass and lose; KNOT out.
```

- **The four events and where they fire** (the fx link's lines; 5g): the cast is fireUlt's own prologue voice
  (`w: f.w.id`, unchanged), so once a cast; the arm keyed `"thornwake"` that it plays is REPLACED — the freeze's
  "creak and cinch" goes with the freeze (Widowmaker's v106 precedent) and the shared rune-crack fallback is
  not touched. The crackle is one `SFX.play` in `plantBramble` after the count (once a bramble, on the landing
  blow's frame, the blow's hit voice on the same frame); the snare one after `T.snares++` (the frame the pin is
  written); the bite one after the cooldown's re-arm, the line every bite starts with (not after `T.ticks++`,
  the voice lab's first anchor: a smite ticker repeats that line on the batch line's newer tips; round 4). A
  killing bite snaps too. On an entry frame with the cooldown clear the snare and the bite land together, the
  snare first. **There is no close voice** (v84 names none; the brambles outlive the window) and none when a
  bramble expires (the picture browns it).
- **In play** (the voice lab, 148 fights): 490 casts -> 490 cast voices; 856 brambles -> 856 crackles; 1781
  snares -> 1781 snare voices; 4287 bites -> 4287 bite voices (all 9 killing bites among them); a cast brings
  1.75 crackles, 3.63 snares and 8.75 bites; 148/148 fights identical and every other voice call identical, the
  sim-write control 1/148; end to end 74/74 and 82/82. In a real window (v Twinshade, 113601, cast at 15.17 s:
  2 crackles, 7 snares, 14 bites) the cast stands +32.6 dB over the fight and the score in its own third-octave,
  the crackles +9.0 / +14.2, the bites a median +14.0, the snares' creak +10.5 and their crack +32.9.
- **For Rick's listen** (the lab's own note): the snare is Tendril's root as the design asks, and it is heavy —
  -2.5 dB re the blow, half its power under 120 Hz — and where Tendril plays it at most once a window,
  Thornwake plays it about 3.5 times a cast (the probe: 3.46).

### 5d. The probe's stage 6: [9] the voices, [10] the picture's hook

`thornwake_probe.py` (ada558edf2f1672a; 602bf4bbdc7a5551 through stage 5, kept in scratch as
`s6/thornwake_probe.pre6.py`) runs each stage-6 check only where the link carries it — the voices detected by
the crackle's arm (`thornwake-crackle`) in `AC.SFX.play.toString()`, the picture by `tickBrier` on the Match —
so the same probe still gates stages 2-5 at 8/8, every line as before; `--stage 6` pins stage 5's numbers and
demands both. Once a fight is over it steps 2 s more of the verdict (the step's `over` path: only the
presentation clock runs) for [9] and [10] alone; [1]-[8] read none of those steps.

- **[9] the voices fire exactly on their events and nowhere else.** `AC.SFX.play` is wrapped (a no-op headless:
  the call is recorded before its first line returns), each call tagged with where it was made. Evidence: a
  Thornwake cast playing anything but exactly one cast voice inside fireUlt; a plantBramble call whose voices
  are not exactly one crackle; a tickBramble call whose voices are not EXACTLY the snares it wrote and the bites
  it bit, in the order it did them; a Thornwake voice no design names; any of them in the picture's hook, a
  drawn frame, the verdict, another relic's cast or any other part of a step. **There is no close voice**: a
  window closing by its clock or BY A DEATH must play nothing beyond that call's snares and bites (each seen,
  or NOT EXERCISED). Every voice of the run is accounted for: cast voices = casts, crackles = brambles, snare
  voices = snares, bite voices = bites. A ward's shatter plays its own crit HIT voice inside hurt(); it is not
  one of Thornwake's and is read past.
- **[10] the picture's hook writes nothing of the simulation's.** `tickBrier` (tickPresentation: through hit
  stops, twice a normal step, and in the verdict) is wrapped: evidence is any change across it to either
  fighter or a shade (every own number, flag and string but its `brier*` fields, every array's length, every
  status, the pin's velocity, the window, the tally) or to the match (every own number, flag and string, every
  array's length, every bramble, every shot) — and, on every 8th busy call and every call where the tally's
  snares or bites rose, [6]'s whole-state snapshot to depth 4 with only `brier*`, the tags and the teaching flags
  left out — an RNG draw or a voice. THE TAGS: the old ones kept in order (the oldest may go: statusTag keeps
  ten), each unchanged but an ENTANGLE tag's count; new ones ENTANGLE only; the teaching flag only entangle's,
  only on. And the picture as declared, REBUILT: the blade's green 1 exactly while the window is open (the
  match live, the caster alive) and 1 - t/0.6 of the presentation clock after it; the caster's picture records
  exactly the simulation's brambles of its side, by identity; the foe carrying none of the caster's picture;
  `brierHeld` (the one picture field another method reads) only on a ball a Bramblesnare snare pinned and only
  while its pin holds, and on at the first picture call after the snare; everything the picture shows gone
  after 2 s of the verdict; every field at rest in a fresh Match.
- **`--drawn N`**: on the first seed, both sides, every foe, each fight is also drawn through the renderer
  (`AC.__draw`, the post chain off, 270x480) every Nth step while the picture shows and every 60th otherwise,
  through the kill and the verdict; [10] fails a drawn frame that throws, draws the match's RNG, changes the
  simulation or a tag, or plays a Thornwake voice. It runs on any link, so the base's draws are its control.

### 5e. Stage 6's gates — every one able to fail

- **engine_ab b26.5 -> fx, ALL 38 WITH Thornwake, n=6: 4218/4218 identical** (`runs/stage6_engine_ab38.txt`;
  703 pairings, 38/38 distinct winners, 4218 distinct seeds, 22.7-114.9s; the ids `runs/ids38.txt`).
  Presentation moves no fight, Thornwake's own included. **Control:** the b26.5 against `mP1` (below: its picture
  lengthens the snare's pin by 0.05 s) with Thornwake, Paradox, Aureole and Gravemourn at n=6: **FAIL, 18 of 36
  differ** — Thornwake's 18 (it is in 3 of the 6 pairings); the other 18 fights have no Bramblesnare and are
  identical (`runs/stage6_engine_ab_control_mP1.txt`). **And what engine_ab cannot see:** `mV1` (a voice at every
  close) and `mP2` (an invisible field written by the picture) read **36/36 identical** on the same four
  (`runs/stage6_engine_ab_mV1.txt`, `runs/stage6_engine_ab_mP2.txt`): only the probe's [9] and [10] catch them.
- **thornwake_probe --stage 6 (ada558edf2f1672a): 10/10 on the fx link** (`runs/stage6_probe_fx.txt`): 444 fights,
  Thornwake both sides x 37 foes x 6 seeds, 9.3 minutes in the page. **[1]-[8] print every line the b26.5
  prints**, and all 34 of their counters, the 19 tallies, the row and the clock window are equal
  (`runs/stage6_probe_cmp.txt`, PASS): 3.31 casts a fight, 1.61 brambles, 3.46 snares and 8.17 bites a cast,
  48.0%, 12.3% of window steps frozen. **The new probe on the b26.5 itself** reads 8/8, every line as
  `runs/probe_final.txt` (the stages 1-5 probe's own run) and all 34 counters, the tallies and the row equal, and
  says "stage 6: not on this link" (`runs/stage6_probe_b26.5.txt`). Then:
  - **[9] the voices:** **1468 cast voices for 1468 casts**, each inside fireUlt; **2360 crackles for 2360
    brambles**, each inside plantBramble; **5077 snare voices for 5077 snares and 11,992 bite voices for 11,992
    bites** (all 24 killing bites voiced), every one of the 2,839,712 tickBramble calls playing exactly its own
    snares and bites in order (a snare then its bite on 4014 calls); **no close voice: 1214 clock closes and all
    45 death closes silent**; silent through 2 s of the verdict in all 444 fights;
  - **[10] the picture:** 6,240,652 `tickBrier` calls, none of which changed the simulation, drew the RNG or
    played a voice (596,905 of them against the whole-state snapshot too; 496,273 in a hit stop, 214,008 in the
    verdict); the tags' rule kept (679 ENTANGLE tags pushed, 2029 counts written onto a tag already up, no other
    tag touched; the teaching flag never set by the picture: 0 calls, the scythe's own entangle tags first); **the blade's
    green exact on every call** — 1 on 2,754,234 calls in an open window, fading on 104,228, 0 on 3,382,190; the
    picture's brambles the simulation's, by identity, on 2,297,595 calls; `brierHeld` on at the next picture call
    after 5047 snares (the rest found the ball dead or its pin already off by then) and never on a ball no
    Bramblesnare snare pinned, over 772,322 held calls; everything gone after 2 s of the verdict for all 888
    fighters; 888 fresh fighters at rest;
  - **the drawn subset** (`runs/stage6_probe_fx_drawn.txt`, the first seed, 74 fights, `--drawn 24`): 10/10;
    **16,854 frames through the renderer** (13,159 with the picture up, 1952 of them in a hit stop, 2725 with a
    ball held, 608 in the verdict), none of which threw, drew the match's RNG, changed the simulation or a tag,
    or played a voice; every counter of the drawn run (drawing aside) and its tallies equal the undrawn run of the
    same 74 fights (`runs/stage6_probe_fx_s1.txt`, 10/10); 8 minutes in the page at idle priority.
    **The base, drawn** (the b26.5, the same 74 fights; `runs/stage6_probe_b26.5_drawn.txt`): 9/9, its drawn check
    passing on 8666 frames (every 60th step: nothing of stage 6's to show).
- **The probe's controls**, scratch copies of the fx link with one edit each (`runs/tools/mutants6.py`, their hashes
  in `runs/stage6_mutants_build.txt`; the first seed, both sides, every foe, 74 fights; the table is
  `runs/stage6_mutant_table.txt`), each failing its own check and passing the other nine:

```
mutant           sha16             probe  fails (count)   tallies vs the clean link   how
clean fx link    d306822d6914c08c  10/10  -               -                           (45.9% on these 74)
mV1-closevoice   5f7ef9c0e558ca77  9/10   [9]  410x       equal                       a crackle at EVERY window close, a death's too
mP1-picwrite     5d7136d66644538b  9/10   [10] 782x       differ                      the snare's picture lengthens the pin 0.05 s
mP2-invisible    b635dcf9223e6d19  9/10   [10] 22,859x    equal                       tickBrier stamps `lastBrier` on the fighter
```

- mV1 fails on every close ("the thornwake-crackle voice played in tickBramble", and the call's own list against
  its snares and bites): 410 = 2 x 205, the 196 clock closes and **the 9 death closes** of the 74 fights, each read
  twice. **The check that no close voice ever sounds, on a death least of all**; its fights are the clean run's
  (a voice is presentation), so nothing but [9] sees it.
- mP1 fails on every snare the picture sees ("the picture wrote the simulation: pin 0.6 -> 0.65"), read on the
  call itself; its fights move (the run's tallies differ; the `engine_ab` control above), and [1]-[8] still pass,
  because they rebuild every frame from its own state.
- mP2 fails from its first call ("the shape 702 -> 704 fields": a field the simulation never reads, on both
  fighters); its fights are the clean run's, so neither engine_ab nor [1]-[8] can see it.
- **render_ab:** the other relics' pairs (paradox:heartwood:25064, twinshade:lastlight:991,
  bulwarden:vinesower:70707, axiom:grudgebearer:31337, at 0.5 / 6 / 12 / 22 / 31 / 40s) are **24/24
  pixel-identical** (`runs/stage6_render_ab_others.txt`). **Control:** Thornwake v Grudgebearer 113075 (the clip's
  fight) at 31.3 / 33 / 35 / 36.5 / 38 / 39.3, inside the window that runs 31.092-39.575, is **0/6 identical**
  (`runs/stage6_render_ab_control.txt`; the frame's mean luma 28.477 -> 27.546 at 31.3, the freeze's lit art gone
  from the cast and the green in its place, then -0.11 to +0.36 as the tangles, the shoots and the flashes stand).
- **chain_audit** `--builder thornwake_build.py`, relic = tip = the fx link: **ALL 24 INSERTS SURVIVE**, stages
  1-5's ten (the blade among them) and stage 6's fourteen that add code (`runs/stage6_chain_audit.txt`); the two
  token removals (the banner seat, the life entry) add no code and so are not inserts the tool can read, and the
  two retired drawUlt branches are found by their comments (their code is shorter than the tool's floor).
  **Control:** the same relic with the b26.5 as the tip loses all 14 of stage 6's and exits 1
  (`runs/stage6_chain_audit_control.txt`). The builder watches what the tool cannot, on every stage-6 build:
  `thornwake: 2.4`, a `thornwake` seat in `onTarget`, `u.w === "thornwake"` and the creak and cinch must be gone.
- **tip_audit:** identical to the b26.5's, line for line, but the file name (`runs/stage6_tip_audit_fx.txt` against
  `runs/tip_audit_final.txt`). Stage 6 adds no status and changes none; the card is unchanged.
- **The builder's own guards** (`runs/stage6_rebuild.txt`, `runs/stage6_builder_negatives.txt`; the builder
  83503639e24a4184; 6f2fdad5f407b335 through stage 5, kept in scratch as `s6/thornwake_build.pre6.py`):
  - **all five links rebuild byte-identical from the bare tip**, `sc-tendril-t3`, LF — the four of stages 1-5 as
    they were, and the fx link;
  - **stage 6 refuses** to run twice (its names are in its own output), on stages 3 and 2, on the bare tip, over
    the existing fx link (untouched), to a name not `sc-thornwake*`, on a CRLF copy of the b26.5, on a base where
    `tickBrier` is already taken and on one without the freeze's voice to replace; stages 5, 3 and 1 refuse on the
    fx link (12 refusals, none writes a file). **The CRLF refusal was dead until this stage**: the builder read its
    source with `read_text`, which turns CRLF into LF, so a CRLF copy BUILT on the first run of this list; it now
    reads bytes, refuses, and no link moved (§6: seven other builders carry the same dead check);
  - **its scan of stage 6's ADDED code** (a re-emitted anchor aside; run on every stage, before any edit)
    refuses **27 scratch copies of the builder**, each with one forbidden line written into a stage-6 row: in
    `tickBrier` a pin, a ball's velocity, the thorns' cooldown, a hit stop, the brambles' array, an invisible
    field on the foe, the other fighter's picture field, the RNG, `Math.random`, the one `ultFx` slot, a voice, a
    hurt, an entangle, a beat, the shared weapon row, a module table written (`STATUS.entangle.tip`), a status
    deleted, a picture record written through an index, the tags' array, the synth struck; in the drawing methods
    the match ended, a tag pushed, a fighter's field written, the canvas name rebound to a fighter; **a second
    line on the crackle's sim path**; a second line in a one-line row; code in a retiring row. The unmutated copy
    writes the fx link, d306822d6914c08c (`runs/stage6_builder_negatives.txt`). The 20 copies of stages 1-5 still
    refuse on the stage-6 builder, and their clean copy still writes stage 2's link
    (`runs/stage6_builder_negatives_s1to5.txt`);
  - on stage 6 it also refuses if the inlined `fx.js` moved, if the freeze's voice or art is still in the page, if
    the rune-crack fallback is not kept once after the four arms, if a voice line is not where it belongs (the
    crackle after plantBramble's count, the snare after the pin's, the bite as the cooldown re-arms and before
    the entangle), if the hexagon's return is not just before `_drawField`'s guard (read by the guard's own
    prefix, so Tendril's extended guard on later tips passes), if a `Math.random` is added or taken away, if
    fireUlt's cast voice moved, and unless each arm, call, pass and method is wired exactly once and `tickBrier`
    follows `tickNovaFx` in `tickPresentation`. The generator (`runs/tools/gen_s6.py`) was run once (it wrote the
    S6 table, 56a82df7ce311cf0) and refuses a builder that already carries S6; the wiring, the scans, readings
    17-22 and the LF fix are hand edits after it, said here, and every check in this section ran on the final
    builder or on links it writes byte for byte.
- **The carry, dry, stages 1-6** (§5; `runs/stage6_carry_dry.txt`): six tips, every stage applies, stage 6's change
  the base's on each.
- **shell_identity** is not run here: the app's json is shared, and the orchestrator runs it on the carried link.
  (The picture lab ran the Electron shell once on its own scratch page, writing its own identity json and never
  the app's: 274/274 identical, a sim-write control at 268/274, `runs/stage6_picture_ident.out` and
  `runs/stage6_picture_ident_ctl.out`; that is the lab's, not this gate.)
- **The labs' own gates** (§5a, §5c): the picture — bloom share +0.0000, with three controls that fail; whole-fight
  identity on 15 fights x 3, with a 1e-9 control that differs on all 13 of Thornwake's; 84/84 other-relic render
  frames on 12 pairs, with two Thornwake controls at 2/7; `engine_ab` 4218/4218 on its shipped look. The voice —
  the 148/148 wire run, with a sim-write control at 1/148; 74/74 end to end, 82/82 on the carry tip.

**What the design's stage 4 asked for, and where it went** (§5: "picture, voice, carry; `_drawField`'s hexagon must
not draw on the snare (the Tendril root picture instead); `engine_ab`, `shell_identity`, `render_ab`,
`chain_audit`, one fight watched"): the picture and the voice (§5a, §5c), the bloom measured, +0.0000; the hexagon
kept off a snared ball, Tendril's root picture ported in its place (147/147 in the lab's drawn run; `brierHeld` in
[10]); `engine_ab` 4218/4218 with Thornwake in; `render_ab` with a control; `chain_audit` 24/24 with a control;
`shell_identity` the orchestrator's; one fight watched, the clip (§5f); and the freeze's field spec out of both
copies at the carry, the orchestrator's (5b, with its `fx_remove` refusal).

### 5f. The clip (Rick's to overrule)

`tools/_thornwake_pick.py` (c9f47baa8a65acb2; from `_ironwood_pick.py`, by way of `_spellbreaker_pick.py`) scores a
window against v84 §4 as built. A window qualifies only if it shows everything: **the cast voice** (the rustle and
creak) and the blade greening, **at least two brambles** (each its crackle and its tangle growing out of the hit
point), **a snare** (its creak-and-crack, the shoots clenching the foe's rim), **three bites** (the soft snap, the
thorn flash, the ENTANGLE count), and **a close BY ITS CLOCK with both alive** (the green fading off the blade; a
death's close or a kill is the death voice's and the verdict's); and nothing taking the screen: no cast or banner
of the foe's, not the scrunch card, and no kill inside the clip. Twinshade is left out (a second body the brambles
do not test) and so are the verdant foes, Thornwake's own school (Bindweed, Heartwood, Ironwood, Thornshear,
Vinesower: the same green, their own entangles and vines). Scored on the brambles, the snares, the bites, the bites
after the close (the brambles outlive the window) and the share of window frames with the foe held.

It ran 31 foes x 4 seeds (`runs/stage6_pick.txt`: of the 124 fights' best windows, 3 show everything; the next
nine in the table each lose on a foe's cast inside the clip). The pick is **Thornwake v Grudgebearer (the dwarven
warhammer), seed 113075**, Thornwake side A (`runs/stage6_clip_timeline.txt`, the fight headless, every stage-6 event in match time):
- the cast at 31.092 (the banner on Thornwake); the window closes by its clock at 39.575: 8 s on the window clock,
  8.48 s of match time (59 hit-stop steps);
- **two brambles** (31.483, 33.592), **six snares** (31.625, 32.817, 33.717, 35.967, 37.692, 38.867), the foe held on
  42.4% of the window's frames; **fourteen bites** in the window (2 each) and **one after the close**
  (39.625: the brambles outlive the window); the first bramble goes at 37.900, the second at 39.875 (6 s on the
  brambles' clock); the green gone at 39.867, 0.29 s after the close;
- no banner, card or kill in the clip; the fight runs on past the clip's end (41.375, both alive, hp 241 / 258; the
  kill is at 48.02).

The runner-up, Slagheart 113001, scored 2.0 lower (two brambles, three snares, nine bites, two after the close).

    python cinema_clip.py --game <scratch>/batch/thornwake/links/sc-thornwake-b26.5-fx.html \
      --a thornwake --b grudgebearer --seed 113075 --at 29.89 --window 11.48 --end-at-window --fps 60 \
      --w 540 --out ../07-shorts/v113/bramblesnare-window.mp4

`--at` is the cast less 1.2, `--window` the window's 8.48 s of match time plus 1.2 and 1.8 (the window clock stops
in the freezes, so 8 + 3 would end the clip before the close).

The clip (`runs/stage6_clip_check.txt`, `stage6_clip_log.txt`, `stage6_clip_timeline.txt`):
- **11.48 s, 689 frames**, 1:1 with the match (the director's cut is the kill at 48.02, outside the clip);
- 540x960 h264 at 60 fps, AAC 48 kHz stereo, 2.14 MB (9a2b6cbdc6429c6d);
- **AAC mean -22.1 dB, max -1.7 dB; -19.8 LUFS integrated, LRA 2.1 LU, true peak -1.5 dBFS.** The same window filmed
  on the b26.5 (its cast the freeze's creak and cinch, and no bramble, snare or bite voice; 0d8fc5b6e8a2b09e) reads
  mean -22.6, max -0.9, -20.3 LUFS, LRA 1.8, true peak -0.6: the new voices add 0.5 LU and no peak -- the loudest
  sample of each is the fight's own, at 39.69 / 39.60 of match time (just after the close), not a stage-6 voice;
- the fight's state at the clip's end (t 41.375, hp 241 / 258, 12 clanks) is the headless fight's
  (`stage6_clip_timeline.txt`);
- **the new voices are in the mix** (`runs/stage6_clip_audio.txt`): both tracks decoded to mono 48 kHz, each voice
  read in its own band over its own time, with minus without: the cast's rustle (2.4-3.9 kHz) **+25.2 dB** and its
  creak (330 Hz) +7.9 (the b26.5's cast has its own triangle sweep in that band); **the 2 crackles +24.6 and +24.8**
  (1.2-2.2 kHz, past the blow's body); **the 6 snares**: the creak a median +35.8, the crack a median +65.4 (all 6
  over the no-voice spread); **the 15 bites a median +11.5** (+6.1 to +43.1; 10 of 15 over the spread). **Control:**
  the same four bands at two times before the cast, no stage-6 voice sounding, come back within 9.0 dB (the two
  renders differ everywhere at a low level before the cast too, as Spellbreaker's did; not traced here, and it is why
  each voice is counted against that spread).

Five frames, checked through the pipeline (the post chain and the director), matched to the fight's own event times by
the HUD's clock; tiled in `05-reference/v113/bramblesnare-clip-5frames.png` (305fb1a7fbded762, 2700x960):
- 1.40 s (HUD 31.3): 0.2 s after the cast: the banner "Bramblesnare" on Thornwake, the scythe's blade green, its
  crescent and thorns relit;
- 1.81 s (31.7): the first bramble (31.483) growing under the foe, which it snared at 31.625: thorn strokes and the
  shoots round its lower rim, ENTANGLE 4 (the first bite's count, written onto the blow's own tag); a crop at 1.95 s
  shows the clench closed round the rim;
- 3.91 s (33.8): two brambles standing, the tangles plain on the floor, the foe snared again (33.717), ENTANGLE;
- 7.71 s (37.6): the blade still green; the first bramble in its last second, the second standing;
- 9.81 s (39.7): 0.125 s after the clock close: the green fading off the blade, the second bramble browned in its last
  second, and a bite (39.625, after the close) flashing its thorns on the foe's rim.

**The white motes falling round the hall in the cast's frames are the freeze's own `SPECS.thornwake`
field** (its frost, `mode: 'fall'`, 1100 particles), still inline on this link until the carry takes it out (5b —
and `fx_remove` refuses as it stands). The clip is `07-shorts/v113/bramblesnare-window.mp4` (gitignored). **Rick's to
overrule.**

### 5g. Where each event hangs (the fx link)

The lines, in `sc-thornwake-b26.5-fx.html` (grep the quoted text on a carried link):

```
the cast       fireUlt 16595: the shared prologue (the banner, its seat map `onTarget` 16613 without Thornwake now,
               SFX.play("ult", { w: f.w.id }) 16622, this.ultFx; the life map line 16641 without `thornwake: 2.4, `),
               then `if (u.kind === "bramble"){` 16718: `f.ultBramble = { t: 0, dur: u.dur };`, returns
the window     `this.tickBramble(dt);` 9091 (after tickTendril); `tickBramble(dt){` 13805: the close 13817 (the clock
               or a death; no voice)
a snare        13839 `T.snares++;`, the snare voice 13844
a bite         13848 `f.brambleCd = u.tickCd;`, the bite voice 13857, then the entangle 13858 and the hurt 13861; a
               killing bite's fatal beat 13872 (`bramble: true`)
a bramble      resolveHit 14958 `this.plantBramble(self, foe)`; `plantBramble(f, q){` 13884: the count 13886, the
               crackle 13892
the voices     Sfx arms: `} else if (w === "thornwake"){` 6324 (the cast, NEEDLES; the creak and cinch gone),
               `"thornwake-crackle"` 6358, `"thornwake-snare"` 6380, `"thornwake-bite"` 6402; the shared
               `} else {  // rune-crack` 7518, untouched
the picture    fields after `this.brambleTally = null;` (`this.brierGreen = 0;` 7832 ...); `this.tickBrier(dt);` 9133,
               right after tickNovaFx in `tickPresentation` 9131; `tickBrier(dt){` 13916 and `_brierCanes` 13994
               (before tickWinnow); `if (__world) this.drawBrier(m);` 19708 (the world pass, after drawTree);
               `this.drawBrierTop(m);` 19765 (after drawTreeTop); `drawBrier(m){` 20806 ... `_brierBlade` 21012
               (before drawMotes); the hexagon's return 23726 in `_drawField(m, f){` 23589, just before its
               guard; the blade's call 24746 in drawWeapon (before `if (f.ultDraw){`)
the freeze's   drawUltUnder's branch gone (its comment at 21706); drawUltOver's gone (its comment at 22381); kept: the
  art          charge sigil ULTSIG `thornwake(c, t, cf, P)` 509 and the banner's letters (`thornwake: 64` 29548,
               `b.w === "thornwake"` 29615); fx SPECS.thornwake still inline at 32953-32957 (the orchestrator's, 5b)
```

## 6. What is left, and whose

- **Rick:**
  - **the clip** (§5f) — the picture and the four voices are Code's picks under "you pick i overrule": the
    tangles, the snare's shoots (Tendril's picture, ported), the bite's thorn flash, the blade's green; NEEDLES,
    KNOTS, STEM, and the snare, Tendril's root as the design asks — heavy (-2.5 dB re the blow, half its power
    under 120 Hz) and about 3.5 a cast where Tendril plays it at most once a window (§5c);
  - the blade: **26.5** under his ruling (50.9% (753 of 1480) both sides); the design's own target, the shipped
    rate (47.8%), is **25.5** (47.5%), one number away; the brief's 28-30 read 55-61 on 151;
  - the bramble's life (§6.3): 6s outliving the window, or 8s (the window), "one number away" — not moved;
  - the ladder's shape (item 12/32): at 26.5 greatsword 62% to bow 38%, worst Gloamwire 20%, Bloodmirror
    32.5, Ironhail 35 (§4);
  - the landing point on a blow that strikes a Twinshade shade: at the shade, where it landed (the prose;
    Consecration's reading), not at Twinshade (the lab);
  - a slain Thornwake's brambles still bite during its kill flight (the lab's; 0 such bites in the
    probe's 444 fights);
  - the blurb, "Longest true reach. Roots its quarry until the swing can barely come around.", still
    describes the freeze; the design names no new one.
- **The orchestrator (ALL DONE at the carry, §7):**
  - the carry (stages 1, 2, 3, 5 and 6 with this builder on the tip of the day; dry on six tips, §5) and its
    engine_ab, and `shell_identity` on the carried fx link (not run here: the app's json is shared);
  - **`SPECS.thornwake` out of both `fx.js` copies at the carry — and `fx_remove.py --relic thornwake` refuses
    as it stands** (§5b: its difflib check aligns the removal one line early, Vinesower's last line being the
    same text as Thornwake's; `--keep-comment` passes but leaves the FREEZE comment). Fix the check, or take the
    comment out by hand; either way the five lines of §0 go (`29a0904df7aad6db`), and Heartwood's own removal
    will meet the same line;
  - the app pointer waits for Rick.
- **Code, minor (its own, no design in it):**
  - the snare's arm `thornwake-snare` carries Tendril's root body transcribed, because `bindweed-root` is not on
    this base; on a tip that carries it the two arms are the same voice (1.2e-07) under two ids. Pointing the
    snare at `bindweed-root` on the chain is a later tidy, not needed for the sound;
  - the LF refusal was dead in this builder (it read the source with `read_text`, which turns CRLF into LF);
    fixed at stage 6 (`read_bytes`), and it now refuses a CRLF copy of the base. Seven other batch builders
    carry the same dead check (`read_text` then `"\r\n" in s0`: aureole, coldiron, heartwood, ironhail,
    lodestone, oracle, spellbreaker); no link is wrong for it (every tip is LF), and each wants the same one-line
    fix when it is next opened.

## 7. The carry onto the chain, and the old freeze's field spec out

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Spellbreaker with the
same builder, one stage at a time (`--src` the previous link), and one more link that takes the retired
freeze's particle field out:

```
sc-spellbreaker-fxout.html         the batch line's tip (Spellbreaker, fx out)   9243277a756e84b6
  -> sc-thornwake-stub.html         stage 1                                       c5f2ec768388893d
  -> sc-thornwake-bramble.html      stage 2                                       4819b017a36af953
  -> sc-thornwake-snare.html        stage 3                                       67c375588606d705
  -> sc-thornwake-b26.5.html        stage 5                                       f7c32e86063abb8d
  -> sc-thornwake-b26.5-fx.html     stage 6                                       98bb5948e0bd6ace
  -> sc-thornwake-fxout.html        the old freeze's field out of both fx.js copies 65464e514ea28b9e
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail, Widowmaker, Lightkeeper, Censer, Aureole and Spellbreaker (redesigned on the chain since), n=6: **2976/2976 identical** (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-spellbreaker-fxout` against the carried stage-6 link, every relic on the tip but
  Thornwake (41), n=6: **4920/4920 identical** (`runs/carry_engine_ab_tip.txt`).

**The field spec out: `tools/fx_remove.py`** -- SPECS.thornwake (the freeze's frost), with its own FREEZE comment: the freeze it explains is retired: **fx.js 7dc0123af735c83e -> d08802c3e71e9f2b**
(`runs/fxout/fx_remove.txt`).

**Gates on `sc-thornwake-fxout`** (`runs/fxout/`, full power):
- engine_ab against the carried stage-6 link, all 42 relics, n=6: **5166/5166 identical**;
- `thornwake_probe.py --stage 6` on the carried link: **10/10** -- it met every relic carried since its scratch base;
- render_ab: the other relics' four pairs **24/24 identical**; **the control, Thornwake v Grudgebearer 113075 through the cast (31.12-31.52s), 0/5
  identical** -- the old field is gone;
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold;
- **shell_identity 200/200** (app Chromium 152 vs headless 151; the json restored).

**The clip, filmed on `sc-thornwake-fxout`** (the §5 command, `--game` the carried link):
`07-shorts/v113/bramblesnare-window.mp4` (1.88 MB, 11.5s; `runs/fxout/clip.txt`).

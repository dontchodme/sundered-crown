# v108 — IRONHAIL / QUARRELSTORM, BUILD. STAGES 0-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-coldiron-temper-fx`, the nova's field spec out of both `fx.js` copies: §7), REVISED AFTER THREE REVIEWS: stage 1 is arm A fight by fight; the mechanism is the lab's; the built relic reads ~3.5 under the lab by the window clock (measured both ways: a bolt's 0.3s of fall is ~0.34s of match time, so fewer land); THE BLADE HOLDS AT THE SHIPPED 16.23: the design's target is the shipped rate (v83 §5 stage 3), and on 151 the redesign reads it there (61.4% both sides against the shipped 62.0; 16.5 reads 62.5, an exact tie in wins, broken to the blade that does not move), so stage 3's link, `sc-ironhail-sunder`, is the final. Rick's other choice under §6.2, 50%, is blade 14 (49.5%, `sc-ironhail-b14`, gated). STAGE 6, the picture and the voice, is built on the final as `sc-ironhail-sunder-fx` (presentation only: engine_ab 4218/4218 over all 38 relics, Ironhail included; probe 11/11): the limbs in the forge, a rune and a falling bolt a drop, a thud a landing pitched by the foe's count, a quieter one a miss, and no close voice. The carry is stages 1, 2, 3 and 6; the nova's field spec leaves both copies of `fx.js` at the carry (`tools/fx_remove.py`, link `sc-ironhail-fxout`, §7).

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`). Input:
`06-docs/v83/ironhail-quarrelstorm-redesign-v83.md` (its §5 is the build brief) and its runs
(`06-docs/v83/runs/hail_*`, `tools/overlays/hail.js`), and nothing else (rule 0). Builder
`tools/ironhail_build.py`, probe `tools/ironhail_probe.py`, runs in `runs/`. **A REDESIGN:** Ironhail
ships in the base, and its ultimate, Quarrelstorm's nova of fourteen arrows, is replaced by the hail.
The roster does not grow (38 relics on this tip).

**Built IN SCRATCH on the chain tip** (the batch's parallel builds): the links below are not in
`02-chain/`. The orchestrator carries them onto the chain one relic at a time by re-running the
builder with `--src <tip>` and proves the carry with `engine_ab`. **The carry is stages 1, 2, 3 and 6**;
stage 3's link is the final mechanism, and stage 6 (the picture and the voice) goes on it. The builder asserts its base by content, never by which relic is last,
and its anchors compose (§4, "re-applies").

**Revised after the adversarial review** (four findings, all taken): (1) the first draft set the blade
at 14 for 50%, the batch's standard for a new relic; the design's own target is the shipped rate
(§5 stage 3 "to the shipped rate"; §4 here), so the final is now the blade held at 16.23 and 14 is Rick's
other choice; (2) probe check [8] now rebuilds the bow's fire cadence frame by frame (a bow at half its
cadence in the window had passed 9/9; it now fails [8] alone, §3); (3) the ladder's wide block splits
are stated (§4); (4) stage 1 against arm A is now compared fight by fight, not only by the totals: 660 of 660 fights identical in each block (§2). A last pass found the 16.23 / 16.5 comparison an exact tie in wins (8 either side of the shipped 917 of 1480), not "16.5 0.1 nearer" as the rounded percentages had it; the tie is broken to the blade that does not move (§4).

**Revised again after the second review** (one should-fix and two notes, all taken). The review found the
build itself correct; the fixes are in the probe and a run file. The builder is unchanged (sha16
`13d0df8b674c873d`) and all four links rebuild from it to the same shas, by the reviewer and again here
(`runs/rebuild_check5.txt`), so no link moved and no fight gate (relic_rate, engine_ab, verify) could
move:
(1) probe check [1] now ties the hail's clock to the step, counting the `tickHail` calls as [8] counts
`tickFire`'s: exactly one on every unfrozen step, none on a frozen one. The reviewer's `r-double` (the
hail ticked twice a step: a 4.6s window, 64.8% of bolts landed, Ironhail 77.5%) had passed 9/9 and now
fails [1] alone; `r-half` (every other step), which had failed only by accident, now fails [1] on its own
count (§3); (2) [7] now reads what the fatal beat says -- kind `hit`, the caster's side, the foe's spot,
`dropDmg` -- and the reviewer's `r-beatside` (the kill credited to the loser) now fails [7] alone (§3);
(3) `tip_audit` on the final was rerun with its exit code recorded (§4).

**Revised a third time, after the third review** (one should-fix and two notes, all taken). The review
again found the build correct and the probe short; the builder is unchanged (sha16 `13d0df8b674c873d`)
and all four links rebuild from it to the same shas (`runs/rebuild_check6.txt`), so no link, no fight
and no fight gate moved:
(1) the probe read WHO a bolt hurt on the foe's side only and never anybody's hp, so the reviewer's
`c-caster` (the hail also strikes its caster, which v83 §6.3 and reading 9 forbid: Ironhail 57.7%, 8
deaths to its own hail) and `c-chip` (each landing takes a point more off the foe, outside `hurt()`
and past the ward) both passed 9/9. Check [4] now requires each hail call's hurts to be exactly its
landings' `[foe, dropDmg, caster]` and rebuilds every fighter's hp, ward and ward pool after the call
with `hurt()`'s own arithmetic, the ward's shatter burst on the caster included; [5] now requires the
call's sunders to be exactly its landings' `[foe, sunder, side letter]`, so a sunder on the caster is
no longer an unlisted "other status". Both of the reviewer's mutants, and this build's `c-selfsunder`,
now fail their own check alone (§3); the three links still read 9/9 with every mechanism number
unchanged; (2) reading 10's "no bolt in the air at a close" is true of clock closes only, and is
reworded (§0); (3) the brief's gates are now set against the built links too, with the misses marked
(§2, §6).

**Stage 6, the picture and the voice** (§5), built on the final after the third review: fifteen
edits byte-exact to the picture lab's and the voice lab's row files, written into the builder as
`S6` with a `--stage 6` that goes on the final once. The probe gains [10] (the voice) and [11] (the
picture), each switched on from the page, each failed by its own controls; engine_ab over all 38
relics, render_ab, chain_audit and tip_audit read it as presentation only. The clip is
`07-shorts/v108/quarrelstorm-window.mp4` (§5e). Readings 15-21 are the builder's.

```
sc-tendril-t3.html            the base: the chain tip (Bindweed stage 5)                    5a6216e3b629fad4
  -> sc-ironhail-stub.html    stage 1  the hail's block, stubbed (charge 1e9); the nova out  7f9904956105811d
  -> sc-ironhail-hail.html    stage 2  the hail, no sunder; charge 14 (brief stage 1)       d3d9062fd77e6cea
  -> sc-ironhail-sunder.html  stage 3  the sunder, sunder 0 -> 1 (brief stage 2)            1bedab05b9803465
                                       = THE FINAL: stage 5 (brief stage 3) holds the blade at the
                                         shipped 16.23, the shipped rate; it writes nothing
  -> sc-ironhail-sunder-fx.html  stage 6  the picture and the voice, on the final        b8ff2014a954be3f
                                         (brief stage 4; the nova's field spec is the orchestrator's)
  -> sc-ironhail-b14.html     NOT THE CARRY: Rick's other choice under §6.2, 50%: blade 14   dadb773b6f8d4555
                                         (`--stage 5 --alt50`; this build's first draft, gated in §4)
     (no stage 4: the brief's stage 4 is the picture and the voice, this doc's stage 6)
```

## 0. What this build stands on

- **The relic is Ironhail as shipped**, and only its ult block moves (stage 1); the blade holds at
  16.23 (stage 5, §4): the dwarven bow (reach 54, width 9, artW 44, spin 2.8, ranged, mass 1.6), its shot (cadence 0.34,
  speed 380, r 24, life 3.4), onHit sunder 1 and its blurb. The builder asserts, BY CONTENT: the row
  (bow, ranged, sunder 1, the shot), the shipped Quarrelstorm block verbatim, `kind:"volley"` used by
  Ironhail alone, the shipped blade 16.23, `hurt(foe, dmg, src)`, `Fighter.apply(key, n, src)`,
  `alive`, `beat`, `fireUlt`, `spawnShot`, `STATUS.sunder`, and that `step()` returns in a hit stop
  before the window tickers; and that every name it adds is free on the base.
- **The arms.** The lab is `tools/ult_overlay.py` + `overlays/hail.js` without `--cell` (a redesign):
  the relic's own ultimate is suppressed in every arm but SHIP. **A** = Ironhail with no ultimate,
  **SHIP** = the shipped nova, **B** = the hail, **C** = the hail + sunder. The relic plays side A
  against the design's roster: the 34-relic roster minus the donor, which is Ironhail itself (33 foes,
  `runs/foes33.txt`).
- **Lab defaults against the settled numbers (flagged):** `hail.js` defaults `fallT` 0.55, `hitR` 40
  and `dropDmg` 5, the REJECTED first pricing (`hail_base`: B 44.8, C 48.5; "a bolt that takes 0.55s
  to fall lands on a ball that has left"). The settled point is `fallT 0.3, hitR 60, dropDmg 4` (§3
  "(taken)"), and every arm this build reads passes it. `dropCd` defaults to the settled 0.4. The
  lab's `hurt` and `apply` sources are the Fighter; the build's `apply` source is a side letter.
- **The charge is 14: the lab's 16 on the game's clock** (Rick's batch ruling). The design names no
  charge; every `hail_*` run cast every 16 seconds of the lab's step clock (the harness's default),
  which counts hit-stop freezes. The census (`runs/s0_census_C_*`, `runs/hail_census.py`: a scratch
  copy of `ult_overlay.py` that counts, before each lab step, whether it is frozen --
  `m.hitStop > 0 || m.latch || m.splitHold` -- on the whole arm and inside windows; its arm C reads
  the same as stage 0's to the fight):

  ```
  arm C, block 2207   10.70% of lab steps frozen (429,440 of 4,014,104); 12.21% inside windows, 9.76% outside
  arm C, block 2317   10.76% of lab steps frozen (433,203 of 4,026,773); 12.39% inside windows, 9.75% outside
                      lab 16 -> engine 16 x (1 - 0.107) = 14.29 / 14.28 -> 14
  ```
  (The shipped Quarrelstorm charged 15 on the engine's clock.)
- **Readings** (in the builder's docstring):
  1. **The cadence is 0.4s.** §1's prose says "every third of a second"; the clause line under it
     ("a drop every 0.4s"), §4 ("A drop every 0.4s of the window") and every `hail_*` run say 0.4,
     and 0.4 is what was priced. **Flagged for Rick.**
  2. **The window is 8s** ("for a duration"; every run used the harness's 8).
  3. **The charge** is the lab's 16 converted (above).
  4. **The hit test** is the foe's centre strictly within `hitR + R` of the spot on the landing
     frame (§4 "within 60 + R"; the lab's `<`).
  5. **A landing is flat:** `hurt(foe, dropDmg, f)` and nothing else -- ward first, no crit, no
     jitter, no sunder multiplier, no act multiplier, no knock, no stop but a ward's own shatter
     inside `hurt` (§4; the lab's `H.hurt`). `f.hits` and `f.dealt` stay the bow's.
  6. **The sunder lands on every landing**, after the hurt, a killing one included (the lab's; the
     brief's gate "sunder = landings").
  7. **`apply`'s source is a side letter** (Rick's ruling 4); `hurt`'s is the caster Fighter (a
     ward's shatter bursts at it).
  8. **A landing that kills files its own fatal hit beat**, marked `hail` (Rick's ruling 5); no other
     landing, drop or miss files one.
  9. **The target is the opponent**, never a Twinshade shade (the lab's `foe`), and **the hail never
     falls on the caster** (§6.3's default: "it does not -- the sky knows its master"); the probe's
     [4] holds it since the third review (the call's hurts are exactly its landings' on the foe, and
     every hp is rebuilt).
  10. **Drops in the air still land** however the window closed (§4): a landing needs a live foe, not
      a live caster. At 0.4 / 0.3 it does not bind in a fight: the last bolt of a clock window lands
      at 7.9s, so in the probe's 444 fights no bolt was in the air at a clock close; at a death close
      the bolts in the air never resolved, the fight ending first (162 of 21,945 drops on the final,
      174 of 22,919 on stage 2, 193 of 23,313 on the 50% alternative: `T.drops` minus landed and
      missed in `runs/probe_*.json`; none resolved late, `T.late` 0). The probe forces a clock close
      with a bolt in the air (§3).
  11. **The window closes on its clock or either death** (the lab's); nothing drops after the close.
  12. **No cast waits.** The design asks none; at 14 against a window of 8 on the same clock a cast
      cannot find its window open (the probe asserts it, [9]). The bolts in the air are the match's.
  13. **The card is the design's own 68-character alternate**, `Iron hail falls on the foe from above;
      every bolt that lands sunders`. Its first line is 74, over verify's 72-character cap.
      **Measured in pixels** (§4 "measure in pixels"; `runs/card_px_b14.txt`, the page's own fonts
      and wrap code): 539px on one line (16th widest of 38), two lines in the ult bar's 390px
      (nothing dropped) and 21px in two lines on the scrunch panel. (The 74 also fits in pixels, 601px
      in two lines; the character cap is what refuses it.)
  14. **The nova is out** (brief stage 1): `kind:"volley"` was Ironhail's alone (grep: `u.shots` and
      `u.kind === "volley"` had no other reader; the cinema's `"volley"` cut is an unrelated kind), so
      its cast branch in `fireUlt` is **retired**. `spawnShot` stays: every bow fires through it.
  15. **The cast voice** is the cast's own `SFX.play("ult", {w: "ironhail"})` in `fireUlt`'s generic
      head, which fell through to rune-crack: an arm is ADDED before that shared fallback (the bellows
      huff) and the fallback line is re-emitted unchanged for the relics that still fall through.
  16. **The landing voice** plays once per landed bolt, in `tickHail` after its hurt and its sunder,
      pitched by the count the foe then carries (the number its tag shows, 1-6); a killing landing
      thuds too, under the death voice.
  17. **The miss voice** plays once per missed bolt, on its landing frame, on the miss line's own test
      read first (the anchor guards it: if that line changes, the row stops applying).
  18. **The close has no voice** (v83 §4: "close -- nothing").
  19. **The picture** is drawn from the match's bolts (`m.hail`, read) and the fighter's own `quarrel*`
      fields (never `m.ultFx`, open item 25); a bolt that resolves is found by `hailTally` rising, so
      `tickHail` makes no call for the picture. The limbs read `ultHail && !over` and cool at the
      verdict; a bolt the kill leaves in the air fades on `quarrelEnd`. **One sunder tag on the foe at a
      time** (Tendril's and Temper's rule): a landing with a tag already up sets its count in place; a
      killing landing tags nothing (the shatter owns that frame).
  20. **"Field: iron-spark motes on landings, both copies" is DRAWN**, not an `fx.js` field (§5c: a
      SPECS field fires once, at the cast edge, on the one ultFx slot, which Ironhail holds for a median
      0.62s of its 8s window). The nova's field spec (`SPECS.ironhail`) is the brief's "nova's field
      spec out": it leaves both copies by the orchestrator's `sync_fx_remove`; this builder edits neither.
  21. **The nova's art is retired with the nova:** `drawUltUnder`'s floor dust and `drawUltOver`'s
      release flash (keyed on the ultFx slot's `"ironhail"`), the charge rune's eight heads (now three
      bolts onto a crossed rune) and the banner's fan (the letters now fall).
- **What stays, for stage 6** (the brief's stage 4, "nova's field spec out"), all presentation and
  read by nothing in the simulation: the release flash keyed `ultFx.w === "ironhail"` in
  `drawUltOver` (fourteen arrow streaks), the floor dust in `drawUltUnder`, the charge rune's eight
  heads (`ULTSIG.ironhail`), the banner's converging-fan letters, the `ultFx` life entry (1.3), the
  cast voice (the default rune-crack: there is no `"ironhail"` arm) and `SPECS.ironhail` in
  `src/render/fx.js`. Until then the cast still plays the nova's picture over the hail. **Stage 6
  (§5) retires all of it but two:** the `ultFx` life entry (1.3) stays as the cast's record, with
  no art keyed on it now, and `SPECS.ironhail` leaves both copies of `fx.js` by the orchestrator's
  `sync_fx_remove` (§5c).
- **Names:** kind `"hail"`, fighter fields `ultHail` / `hailTally`, match field `m.hail`, ticker
  `tickHail`; all free on the base (the builder refuses a stage 1 whose base carries any). Links
  prefixed `sc-ironhail`, none in `02-chain/`.
- **The clock:** the window, the drop cadence and every bolt's fall run on the window tickers' clock,
  which stops in a hit stop (every batch build's convention). The lab ran all three through freezes
  (§2).

## 1. Stages 1-3

**Stage 1** replaces the shipped Quarrelstorm block with the hail's, stubbed at charge 1e9 (the clock
never reaches it and `fireUlt` never runs for this relic), and retires the `volley` branch. Nothing
reads the ult block's other fields, so this link is the lab's arm A (§2). **Stage 2** (the brief's
"nova out, `m.hail[]` in") adds `ultHail` / `hailTally` after `this.vineTally = null;`, `m.hail` after
`this.shots = [];`, the `kind === "hail"` cast branch before Corollary's `"echo"`, `tickHail` called
after `this.tickTendril(dt);` (after `ballCollision`, before `tickHits`) and defined before
`tickWinnow`, and charge 14, with the sunder written but 0. **Stage 3** is one number, `sunder:0` →
`sunder:1`. **Stage 5** is the blade, and it holds at the shipped 16.23 (§4): stage 3's link is the
final, and the builder's `--stage 5` refuses to write unless asked for Rick's other choice
(`--alt50`, blade 14).

`tickHail`, each unfrozen step, in two halves:
- **the bolts in the air** (`m.hail`, each `{x, y, t, side}`): `t += dt`; on the frame `t` reaches
  `fallT` the bolt resolves: a live foe whose centre is within `hitR + R` of the spot takes
  `hurt(foe, dropDmg, caster)` and `apply("sunder", sunder, side)`, and a killing landing files its
  fatal `hail` beat; otherwise it is a miss, and a miss does nothing;
- **the windows** (`f.ultHail = {t, dur, cd}`): `t += dt`; the window closes at `dur` or on either
  death; otherwise `cd -= dt`, and at `cd <= 0` a bolt drops at the foe's `(x, y)` of that frame and
  `cd = dropCd`. The cast opens `{t: 0, dur, cd: 0}`, so the first bolt drops on the cast frame.

## 2. Stage 0 and the stages against it — the window clock, measured both ways

`ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic ironhail --mech overlays/hail.js
--arms A,SHIP,B,C --P fallT=0.3 hitR=60 dropDmg=4 --seeds 20 --foes <33>`, seed0 2207 and 2317, 660
fights an arm a block (`runs/s0_ASBC_*`; the brief's stage 0 names A, SHIP and C, and B is its stage-1
reference). The built links run `--relic ironhail --arms SHIP` on the same foes and seeds, so the
built ultimate is the one that plays (`runs/built_*`).

```
                          lab on 151 (1 / 2)   pooled   published 141   lab at the engine's clock   build on the lab's clock   BUILT (1 / 2)             pooled
A    no ultimate          35.6 / 36.7          36.2     39.4                                                                   stage 1: 35.6 / 36.7      identical, fight for fight
SHIP the nova (shipped)   58.9 / 60.0          59.5     55.8
B    the hail             50.5 / 49.4          50.0     (not run)       47.1 / 46.1 -> 46.6         52.6 / 48.8 -> 50.7        stage 2: 46.7 / 45.5      46.1
C    + the sunder         63.9 / 61.5          62.7     61.5            60.9 / 59.1 -> 60.0         63.0 / 62.6 -> 62.8        stage 3: 59.1 / 59.7      59.4
```

- **Stage 1 is arm A fight for fight** on both blocks. `ult_overlay`'s json keeps only totals, so the
  first draft compared all 33 foes' rates, the win and the blows a fight (16.236364 / 16.221212),
  identical (`runs/stage1_vs_A.txt`); the review asked for the fights themselves. `runs/perfight_overlay.py`
  (made by `runs/make_perfight.py`: `ult_overlay.py` plus one row a fight in its json, nothing else
  changed; `runs/perfight.sh`) ran arm A on the base and the stub's own ultimate on `sc-ironhail-stub`,
  33 foes x 20 seeds a block: **660 of 660 fights identical in each block** -- the winner, the duration
  to the step, the blows in and out of windows and the casts (0) -- 235 / 235 and 242 / 242 wins
  (`runs/stage1_vs_A_perfight.txt`, `runs/pf_*`).
- **Published (141) against 151 is the runtime, not the tip.** The published run's own 330 fights
  (sc-trunk, seed0 2207, 10 seeds) replayed on 151 (`runs/s0_trunk151_n10`) read A 35.2 / SHIP 56.7 /
  C 64.2 against the published 39.4 / 55.8 / 61.5, with only 7-9 of 33 foes' rates identical: the
  same fights come out differently on the new runtime. On 151 the tip reads what sc-trunk reads to
  within a point on every arm (block 2207, 20 seeds, `runs/s0_trunk151_2207`: A 34.7 / SHIP 58.0 /
  C 63.0 against the tip's 35.6 / 58.9 / 63.9). On 151 the hail with its sunder is worth +26.5 over
  A, where the nova is worth +23.3.
- **The brief's gates, against the lab AND the built links** (the third review: an earlier draft set
  them against the lab only). Its stage 1 (here stage 2): "~19 drops a cast, ~6 landed, ~24 damage,
  relic ~57% without sunder"; its stage 2 (here stage 3): "sunder = landings; relic ~62%". The built
  mechanism is the probe's (444 fights, both sides), the built rate `ult_overlay`'s (the table above,
  side A, 1320 fights):

  ```
  gate                     brief    lab on 151 (arm)       BUILT link                       verdict on the built link
  stage 2  drops a cast    ~19      19.0  (B)              18.18  (sc-ironhail-hail)        met (-4%)
  stage 2  landed a cast   ~6       6.1   (B)              4.76                             MISS, RED (-21%): the window clock
  stage 2  damage a cast   ~24      24.5  (B)              19.05                            MISS, RED (-21%): the window clock
  stage 2  relic           ~57%     50.0  (B)              46.1                             MISS, RED: the 57 was an estimate (the lab
                                                                                             reads 50.0), and -3.9 more is the window clock
  stage 3  sunder=landings  =       5.98 = 5.98 (C)        4.72 = 4.72 (sc-ironhail-sunder)  met, to the digit
  stage 3  relic           ~62%     62.7  (C)              59.4                             MISS, RED (-2.6): the window clock
  ```

  **Two causes, both measured, neither a mis-build.** (a) The 57 was an estimate: no `hail_*` run
  priced arm B at the taken point, and the lab's own arm B reads 50.0 on 151, so no build of the
  design could meet it. (b) The rest is the window clock (below): a bolt's 0.3s of fall is ~0.34s of
  match time, so ~21% fewer bolts land, and every landing is the damage and the sunder. The lab at the
  engine's clock reads the built mechanism and the built rates (B 46.6, C 60.0; 4.97 / 4.85 landed and
  19.9 / 19.4 damage), and a scratch build on the lab's clock reads the lab's rates (B 50.7, C 62.8):
  controls 1 and 2 below. Stage 5 then prices the relic as built: at the shipped blade it reads the
  shipped rate both sides (§4), which is the design's stage-3 target.
- Lab mechanism on 151 (arm C, pooled): 2.68 casts; 18.95 drops, 5.98 landed (31.5%) and 23.9 damage
  a cast; 5.6 blows in windows and 9.1 outside a fight.

**The built relic reads ~3.5 under the lab from stage 2 on, and it is the window clock.** The engine's
8s are 8 seconds of the window tickers' clock, and 12.6% of window steps are frozen (the probe), so a
built window lasts 9.10s of match time, a bolt drops every ~0.456s of match time and, above all, **a
bolt's 0.3s of fall is ~0.34s of match time**. The foe has longer to leave the spot: 26.4% of bolts
land against the lab's 31.5%, 4.7 landings a cast against 6.0, and every landing is the damage and
(at stage 3) the sunder. Unlike Canopy, Onslaught and Tendril, whose longer windows held more of their
mechanism, this window holds no more bolts (20 at most either way); it only lengthens the fall. Two
controls, each able to come back wrong:
1. **The lab at the engine's clock** (`runs/lab_scaled_BC_*`: every timing in match seconds, x 1 /
   (1 - 0.123), the frozen share inside windows: dur 9.12, dropCd 0.456, fallT 0.342) reads B 46.6
   against the built 46.1 and C 60.0 against the built 59.4, with the built mechanism: 17.9 drops,
   4.97 / 4.85 landed (27.8 / 27.0%) and 19.9 / 19.4 damage a cast (the probe: 18.0-18.2 drops,
   4.72-4.76 landed, 18.9-19.1 damage).
2. **A scratch build on the lab's clock** (`runs/clock_variant.py lab`, `runs/ctl-lab-*`: `tickHail`
   also called on every frozen step -- the latch, the split hold and the hit stop -- so the window,
   the cadence and every fall run through freezes as the lab's `onFrame` did) reads B 50.7 against
   the lab's 50.0 and C 62.8 against the lab's 62.7.

A third control splits the clock (`clock_variant.py fall`, `runs/ctl-fall-*`: only the bolts in the
air fall through freezes; the window and the cadence stay on the window clock): B 47.8, C 64.2. The
fall's clock is the landings; with it the build lands the lab's share, and the longer window then
buys the sunder more bow time (+1.4 over the lab-clock variant at C; at B the difference is inside the
block spread). The mechanism is the lab's, nothing is mis-built, and the build keeps the engine's
convention and every designed number. Stage 5 prices it with the blade.

## 3. The probe (`ironhail_probe.py`, one check per sentence, read inside the hooks)

Wraps `tickHail`, `fireUlt`, `tickWeapon`, `tickFire`, `resolveHit` and `step`; Ironhail against every
other relic, both sides, 6 seeds (444 fights), plus a second pass of 16 fights (in no tally) that
closes one window a fight by its clock on the frame after a drop, so a bolt is in the air at a close.
The checks follow the link's own numbers, so the same probe gates stages 2, 3 and 5.

```
[1] the window: dur on the window clock (tickHail once on every unfrozen step, never on a frozen one; dt a call), closes on either death; only Ironhail's
[2] a bolt every dropCd (cd - dt <= 0, then cd = dropCd) at the foe's (x, y), the first on the cast frame
[3] each bolt falls dt a call and resolves on the call its fall reaches fallT, the window open or closed
[4] struck iff a live foe within hitR + R of the spot: hurt(foe, dropDmg, caster) once, nobody else hurt; every hp and ward rebuilt; a miss nothing
[5] each landing sunders: apply('sunder', sunder, side letter) once, on the foe only; none on a miss (none at sunder 0)
[6] nothing else: no move, no push, no stop but a ward's own shatter, no rng, no shot, no other status
[7] a killing landing files one fatal hail beat (hit, the caster's side, the foe's spot, dropDmg); nothing else files one
[8] the bow keeps firing: its spin, its fire (asked once a step; cadence rebuilt) and every blow its own, in the window and out
[9] the nova is gone: a cast spawns no shot, opens {t 0, dur, cd 0}, never on an open window
```

Every check counts what it saw, and a check that never ran is a FAIL ("not exercised"). [8] rebuilds
every Ironhail blow (a shot or the bow) from its captured crit and jitter draws, and **since the first review
it rebuilds the bow's fire frame by frame**: the step wrapper counts the `tickFire` calls (exactly one
on every unfrozen step, none on a frozen one), and the `tickFire` wrapper captures `fireCd`, the stun,
the aimed draw and the engine's cadence multiplier `cm` before the call, then requires the engine's
arithmetic exactly: a skipped frame (dead, over, stunned, drawing) looses nothing and leaves `fireCd`;
otherwise `want = fireCd - dt`, and above zero nothing is loosed and `fireCd === want`, at or under
zero exactly one ordinary shot (`spawnShot(f)` with no angle, counted at `spawnShot`, not by
`shots.length`, which `maxLive` can pin) and `fireCd === want + cadence x cm`. Coverage needs fire
frames in windows and out and the once-a-step count. The review's own mutant (`r3-halfbow`, the bow
at half its cadence while the hail falls, Ironhail 50.7% -> 35.1%) had passed 9/9; it now fails [8]
alone (`runs/probe_review-r3-halfbow.txt`).

**Since the second review, [1] ties the hail's clock to the step.** The per-call checks (the window,
the cadence and every fall advance `dt` a call) are the window clock only if `tickHail` is asked once a
step, and nothing checked that: the reviewer's `r-double` (the ticker line written twice) ran a window
in 4.58s of match time, dropped a bolt every 0.2s that fell for 0.15s, landed 64.8% of them and won
77.5%, and passed 9/9. The step wrapper now counts the `tickHail` calls the way it counts `tickFire`'s:
exactly one on every unfrozen step and none on a frozen one, and [1]'s coverage needs the count
(`hailStepOk`). On every link the hail is asked once on exactly the steps the bow is (the two counts
agree to the step). **And [7] now reads what the fatal beat says**, not only that one is filed: kind
`hit`, the caster's side (0 for `a`, 1 for `b`), the foe's `(x, y)` before the call and `dmg = dropDmg`.
The cinema finds the killing blow with `plan.find(c => c.fatal)` and cuts to its side and spot, so a
beat with the wrong side would cut to the wrong fighter; the reviewer's `r-beatside` (the kill credited
to the loser) had passed 9/9. (Probe sha16 `7140a7f8fee704be` after the second review, `83ee400a493213a1` before it.)

**Since the third review, [4] rebuilds who is struck and by how much, and [5] reads whom a sunder
lands on.** [4] had proved only that the foe got exactly one `hurt(foe, dropDmg, caster)`; it filtered
the hurts to the foe, and nothing compared anybody's hp. So a hail that also struck its caster (the
reviewer's `c-caster`: 1,528 bolts on the caster, 6,112 damage, Ironhail dead to its own hail 8 times,
57.7%) and a landing that took a point more off the foe outside `hurt()` and past the ward (`c-chip`:
23.39 damage a cast for 18.87) both read 9/9, though §6.3 ("it does not"), §4 ("`hurt(foe, 4, f)` ...
and nothing else") and readings 5 and 9 forbid them. The `tickHail` wrapper now keeps, for each call,
the list of its landings in the order the engine resolves them, and requires:
- **the call's hurts to be exactly its landings' `[foe, dropDmg, caster]`, in order**: a hurt on the
  caster, on anybody else, a second hurt or a hurt with no landing fails [4];
- **every fighter's hp, ward and ward pool after the call to be exactly the rebuilt ones**: from the
  values captured before the call, each landing runs `hurt()`'s own operations in the engine's order
  (the ward absorbs `min(shield, dmg)` first; a ward that reaches zero shatters, zeroing ward and pool
  and bursting the caster, if alive, for `Math.round(pool x STATUS.ward.shatter)`; the rest comes off
  hp), and the comparison is exact (`===`), both fighters, every hail call, a landing or not. Any hp
  taken outside `hurt()`, any damage but `dropDmg`, any burst but the ward's own fails [4]. Coverage
  needs landing calls whose hurt list matched, landing calls whose hp matched, and at least one ward
  burst rebuilt on the caster;
- **the call's sunders to be exactly its landings' `[foe, sunder, side letter]`** (none at sunder 0):
  a sunder on the caster, which the "other status" filter of [6] had let through because it is the
  sunder, now fails [5] (this build's `c-selfsunder`: each landing sunders the caster too).
Probe sha16 `400e8424f60238c0` (the second review's version, `7140a7f8fee704be`, is kept as
`runs/probe_before_review3/ironhail_probe_r2.py`).

- **sc-ironhail-hail (stage 2): 9/9** (`runs/probe_hail.txt`). 2.84 casts a fight; 18.18 drops,
  4.76 landed (26.4%) and 19.05 damage a cast, sunder 0; 18 killing landings, each with its one fatal
  beat; 101 wards broken by a landing, and no other stop; 12.6% of window steps frozen, a clock window
  9.09s of match time; 51.4 shots loosed in windows and 70.8 outside a fight (the fire rebuilt on
  930,407 frames in windows and 1,276,721 outside; asked once on each of 2,592,891 unfrozen steps,
  and `tickHail` asked once on each of the same 2,592,891 and on no frozen one);
  16 forced closes, 16 bolts resolved after them, 3 landed; who is struck (the third review's [4]):
  6,145 landing calls whose hurts were exactly `[foe, 4, caster]`, every fighter's hp, ward and pool
  rebuilt exactly on all 2,592,891 hail calls, 52 ward bursts on the caster among them.
- **sc-ironhail-sunder (stage 3, THE FINAL): 9/9** (`runs/probe_sunder.txt`). 2.75 casts; 18.00
  drops, 4.72 landed (26.4%), 18.87 damage and **4.72 sunder** a cast (sunder = landings); 27 killing
  landings; 96 wards; 12.6% frozen, a clock window 9.09s; 6.2 blows in windows and 9.0 outside, 49.3
  shots loosed in windows and 69.4 outside a fight (the fire rebuilt on 893,612 + 1,250,779 frames;
  the fire and `tickHail` each asked once on each of 2,508,777 unfrozen steps, on no frozen one);
  5,896 landing calls whose hurts were exactly `[foe, 4, caster]` and whose sunders were exactly
  `[foe, 1, side]`, every hp, ward and pool rebuilt exactly on all 2,508,777 hail calls, 53 ward bursts
  on the caster among them; Ironhail 61.7% on the probe's fights.
- **sc-ironhail-b14 (the 50% alternative): 9/9** (`runs/probe_b14.txt`). 2.89 casts; 18.17 drops,
  4.83 landed (26.8%), 19.32 damage and 4.83 sunder a cast; 24 killing landings; 91 wards; 12.7%
  frozen, 9.10s; 7.1 blows in windows and 9.3 outside; `tickHail` once on each of 2,612,779 unfrozen
  steps; 6,304 landing calls whose hurts and sunders were exactly the landings', every hp, ward and pool
  rebuilt exactly on all 2,612,779 hail calls, 52 ward bursts on the caster among them; Ironhail 50.7%.
- The probe's mechanism numbers were unchanged by the first review's [8], by the second review's [1]
  and [7], and again by the third review's [4] and [5], on all three links, to the digit (each output
  differs from the one before only by the new "who is struck" line and the two checks' wording). The
  first draft's runs are kept in `runs/old_probe/`, the runs from before the second review in
  `runs/probe_before_review2/`, and those from before the third in `runs/probe_before_review3/`.
- **Controls on the final, under the probe as it now stands** (`runs/probe_mutants4.txt`, made by
  `runs/mutants_summary4.py`; the mutants by `runs/mutants2.py`, `runs/mutants3.py` and
  `runs/mutants4.py`, each a scratch copy of sc-ironhail-sunder breaking one sentence; every one rerun
  under the third review's probe, sha16 `400e8424f60238c0`; the final reads 9/9 and 61.7% on the same
  fights):

  ```
  m1-frozen     the window ticks through a hit stop           66.9%   fails [1] only (598,824: per call and per step)
  m2-cadence    a bolt every 0.36s                            64.2%   fails [2] only (24,487)
  m3-fall       a bolt lands 0.27s after it drops             62.8%   fails [3] only (21,977)
  m4-sundermul  a landing multiplied by the foe's sunder      65.3%   fails [4] only (16,119: the dmg, the call's list, the hp)
  m5-missund    a miss sunders too                            65.8%   fails [5] only (31,844: the miss, the call's list)
  m6-stop       a landing stops the world 0.05s               64.6%   fails [6] only (5,728)
  m7-nobeat     a killing landing files no beat               61.7%   fails [7] only (27)   (presentation: no fight moves)
  m8-bowquiet   the bow silent while the hail falls           30.6%   fails [8] only (1,011,393)
  m8b-halfbow   the bow at half its cadence in the window     45.9%   fails [8] only (11,946)
  m9-novakept   the cast also fires the fourteen-arrow nova   80.6%   fails [9] only (1,152)
  -- the second review's (r-double, r-half, r-beatside byte-identical to the reviewer's files) --
  r-double      tickHail twice a step (a 4.58s window)        77.5%   fails [1] only (2,345,525: two calls a step)
  r-half        tickHail on every other step (a 16s window)   50.9%   fails [1] (1,281,827: no call on a step)
                                                                      and [9] (808: a 16s window outlives the 14 charge)
  r-beatside    the fatal beat credits the loser's side       61.7%   fails [7] only (27)   (presentation)
  r-beatspot    the fatal beat at the caster's spot           61.7%   fails [7] only (27)   (presentation)
  -- the third review's (c-caster, c-chip byte-identical to the reviewer's files; c-selfsunder this build's) --
  c-caster      the hail also strikes its caster (§6.3)       57.7%   fails [4] only (3,138: a hurt on the caster; its hp)
  c-chip        a landing takes 1 more hp outside hurt()      60.8%   fails [4] only (5,767: the foe's hp, 1 under the rebuild)
  c-selfsunder  a landing also sunders the caster             43.7%   fails [5] only (5,366: every landing call's sunder list)
  -- the first review's, a mutant of sc-ironhail-b14 --
  r3-halfbow    the bow at half its cadence in the window     35.1%   fails [8] only (12,510)
  ```
  **Each fails its own check and only that one**, except `r-half`, which also fails [9]: its
  half-speed window is still open when the next cast comes, which [9] forbids (the review asked that
  both clock mutants fail [1], and `r-double` alone). Every mutant but m7, `r-beatside` and `r-beatspot` (the beat is presentation) moves the win.
  Under the second review's probe all three read 9/9: `c-caster` and `c-chip` in the reviewer's own
  runs (`runs/probe_before_review3/probe_rev3-c-*.txt`), and `c-selfsunder` rerun here under that probe
  (`runs/probe_before_review3/probe_r2probe-c-selfsunder.txt`: its sunder on the caster passed [6]'s
  "other status" filter). Now each fails its own check alone. m4 and m5 fail the same check as before with more counts, because the new
  call-level lists (and, for m4, the hp rebuild) catch the same broken landing a second and third way;
  every other count is the second review's to the digit. The counts under the second review's probe are
  in `runs/probe_before_review3/probe_mutants3.txt`, under the first review's in `runs/probe_mutants2.txt`,
  and the first draft's six controls, on sc-ironhail-b14 and under the old [8], in `runs/probe_mutants.txt`.

## 4. Stage 5: the blade — it holds at 16.23, the shipped rate

Both sides (`relic_rate.py`: each seed played from both sides; every other relic a foe, 10 seeds a foe
a side, 740 fights a block; seed0 2207 and 2317; `runs/stage5_rr_*`, the table in
`runs/ladder_final.txt`, `runs/ladder2.py`):

```
blade                        block 1   block 2   split   pooled (1480)   side A   side B   mean
16.23 SHIPPED (the nova)     61.5      62.4      0.9     62.0            62.6     61.4     51.6s   sc-tendril-t3: THE REFERENCE
15    (the brief's grid)     49.3      55.9      6.6     52.6            52.4     52.8     52.9s
15.5  (the brief's grid)     54.1      58.9      4.9     56.5            55.1     57.8     52.1s
16    (the brief's grid)     59.6      59.2      0.4     59.4            59.1     59.7     51.8s
16.23 FINAL (the link)       61.9      60.9      0.9     61.4            61.6     61.2     51.6s   sc-ironhail-sunder, no --set
16.23 --set (the proof)      61.9      60.9      0.9     61.4            61.6     61.2     51.6s   sc-ironhail-sunder --set dmg=16.23
16.5  (above the bow row)    63.4      61.6      1.8     62.5            63.2     61.8     51.1s
12                           29.7      35.0      5.3     32.4            32.4     32.3     56.1s
13                           42.7      42.6      0.1     42.6            43.6     41.6     55.1s
14    (the 50% alternative)  50.0      48.9      1.1     49.5            50.0     48.9     53.9s   = sc-ironhail-b14, no --set
14.5                         54.3      53.9      0.4     54.1            54.3     53.9     53.2s
```

- **The target is the design's own default, the shipped rate.** §5 stage 3: "the blade, wide on 151 at
  15 / 15.5 / 16 to the shipped rate"; §3 prices the blade back to SHIP ("61.5 against a shipped 55.8:
  the blade from 16.23 to about 15.3 (the bow row 9.5–16.2)"); the v87 handoff's redesign row reads
  SHIP -> new. §6.2 ("The blade target") leaves the target to Rick and names no other, so rule 0 takes
  the design's default and flags the other, as the Widowmaker and Lightkeeper redesign builders do.
  This build's first draft set 50%, the batch's standard for a new relic, and the review sent it back:
  nothing in v83, the handoff or the standing rulings puts a redesign at 50.
- **On 151 the shipped rate is 62.0%** (Ironhail as shipped, the nova at 16.23, on the base: 917 wins
  of 1480, 61.96%; one standard error 1.26 points, 18.7 wins). The brief's grid reads 15 -> 52.6,
  15.5 -> 56.5, 16 -> 59.4, all under it. The design's "about 15.3" took back a lab gap measured on 141
  (the redesign 61.5 against a SHIP of 55.8); on 151, against the engine, there is no gap to take back:
  the redesign already reads the shipped rate at the shipped blade.
- **The pick, in wins** (`runs/blade_pick.txt`, `runs/blade_pick.py`; the rounded percentages hide
  it): the shipped blade 16.23 reads 909 of 1480 (61.42%, **8 wins under**) and 16.5 reads 925
  (62.50%, **8 wins over**). The two measured points nearest the shipped rate are **an exact tie**, each
  under half a standard error away (an earlier draft of this section called 16.5 "0.1 nearer": that was
  the rounding of 61.96 to 62.0). **The tie goes to 16.23**: the blade does not move, 16.23 is the top
  of the bow row the design names (§3 "the bow row 9.5–16.2", whose top is Ironhail's own blade;
  16.5 would lift it above the row), and it is the nearer of the two to the brief's own grid (15 / 15.5
  / 16). **So the blade does not move, and stage 3's link is the final.** The brief names no knob to
  move before the blade, and none moved. 16.5 is Rick's to take if he reads the tie the other way
  (§6).
- **The final link is the measured relic:** `relic_rate --set dmg=16.23` on `sc-ironhail-sunder`
  reproduces the link with no `--set` in both blocks: 61.9% and 60.9%, side A 63.5 / 59.7, side B
  60.3 / 62.2, mean 51.4937s / 51.7166s, all 37 foes' rates and every type identical
  (`runs/stage5_rr_set16.23_*` against `runs/stage5_rr_d16.23_*`).
- **The ladder's noise** (the review's note): the 15 and 12 points split 6.6 and 5.3 points between the
  blocks (15.5 splits 4.9), wider than the handoff's ~5-point tier, and pooled, 15 (52.6) comes out under
  14.5 (54.1). The 50% line therefore crosses somewhere in 14-15 within noise, and 14 is the measured
  point nearest it; the shipped-rate points 16.23 and 16.5 split 0.9 and 1.8.
- **The ladder at the final** (40 fights a foe, `runs/ladder_final.txt`), with the shipped relic and the
  50% alternative beside it: by type flail 70% (shipped 77, alt 57), scythe 68 (66, 54), warhammer 67
  (65, 63), twinblade 60 (50, 43), bow 53 (55, 50), greatsword 49 (53, 29). Worst Farwarden and
  Lightkeeper 40, Axiom 42.5, Dawnbringer 45; best Ironwood 97.5 (shipped 42.5), Bloodmirror and
  Portcullis 82.5, Thornwake 80. The largest moves against the shipped relic: Ironwood +55, Widowmaker
  +25, Duskreave +20, Spellbreaker +15; Paradox -25, Bulwarden -22.5, Ravelbone -17.5. The shipped
  relic's worst was Farwarden 35 and its best Portcullis 87.5.

**The gates on the final, `sc-ironhail-sunder`:**
- **engine_ab sc-tendril-t3 -> sc-ironhail-sunder, the 37 others (every base id but Ironhail), n=6:
  PASS, 3996 / 3996 matches identical field for field**, no page errors, 37 / 37 distinct winners,
  3996 distinct seeds, 21.5-115.1s (`runs/engine_ab37_sunder.txt`). The redesign moves no other
  relic's fight; its own fights differ by design.
- **verify --n 40 on sc-ironhail-sunder (38 relics, 28,120 matches): 10/13, and the three reds are the
  base's own** (`runs/verify_sunder.txt`; sc-tendril-t3's is `06-docs/v101/runs/verify_t3.txt`).
  Ironhail 61.7% (60.1% in the base's verify; verify plays i < j, so Ironhail is side A to 29 foes and
  side B to 8); every relic inside 30-70% (Heartwood 30.2 .. Gloamwire 63.7). The reds: "both sides can
  win every matchup" (Heartwood v Twinshade 0/40, Heartwood v Bindweed 0/40, as on the base); the
  pairing-duration band, whose red end is Farwarden/Starwarden 100.0s as on the base (its low end is now
  Ironhail/Marrowdraw 40.2s, inside the band; the base's was Gravemourn/Ironhail 38.6s); the overall mean
  60.8s, the base's 60.8s. None is Ironhail's.
- **tip_audit on sc-ironhail-sunder: exit 0, and its body identical to sc-tendril-t3's**
  (`runs/tip_audit_sunder.txt`, `tip_audit_base.txt`; diffed, the only differing line is the first, the
  page's path; the redesign touches no status tip; Burn's `feed` line is the base's own). The second
  review found the first run's file without the `exit` line the other two carry; it was rerun with the
  exit code recorded, and the body is unchanged.
- **chain_audit** (`--relic sc-ironhail-sunder --tip sc-ironhail-sunder --builder ironhail_build.py`):
  **ALL 9 INSERTS SURVIVE** (`runs/chain_audit_sunder.txt`). The builder keeps no module-level stage-5
  table: the final carries no blade edit, and the audit reads every module-level table as an insert the
  final must hold; the 50% alternative's table is built in `main()` when `--alt50` asks for it.
- **The builder re-applies:** every link rebuilt from the final builder to a temporary path matches its
  sha (`runs/rebuild_check6.txt`, rerun for the third review's fix with the builder unchanged;
  `runs/rebuild_check5.txt`, for the second's;
  `runs/rebuild_check4.txt`, after the last comment-only edit; `runs/rebuild_check.txt` before it:
  stub, hail, sunder, and b14 through `--stage 5 --alt50`). The carry, stages 1-3, writes **the same
  105-line diff** (md5 `eb3609089944`) on the base, where it is `sc-ironhail-sunder` to the byte, and on
  eight other builds of this lineage (`runs/compose4.txt`, `runs/compose4.sh`; `runs/compose3.txt`
  before): `02-chain/sc-tendril-fx`, `02-chain/sc-onslaught-fx`, and the batch's scratch builds
  `sc-angelus-b9`, `sc-oracle-sight`, `sc-coldiron-temper-b93` and `sc-lodestone-b215` (39 relics each),
  `sc-lightkeeper-bulwark-b9.5` and `sc-widowmaker-b1075`. It refuses, by content, the Watchlight
  lineage now in `02-chain/` (`sc-watchlight`, `sc-watchlight-fx`, `sc-wardbolt`, `sc-beacon`: no
  Tendril ticker for the hail's to follow). It refuses to overwrite a link, a stage on a source that already carries it, a name that is
  not `sc-ironhail*`, and `--stage 5` without `--alt50`.

**The 50% alternative, `sc-ironhail-b14` (dadb773b6f8d4555), as gated in the first draft** (unchanged
bytes; it rebuilds from the revised builder through `--stage 5 --alt50`): `relic_rate` with no knob set
gives both blocks of `--set dmg=14` exactly (50.0% / 48.9%, every foe, both sides and the duration;
`runs/stage5_rr_built_b14_*`); engine_ab against the base on the 37 others 3996/3996 identical
(`runs/engine_ab37.txt`); verify --n 40 10/13, Ironhail 47.4%, the reds the base's own three
(`runs/verify_b14.txt`); tip_audit identical (`runs/tip_audit_b14.txt`); chain_audit whole
(`runs/chain_audit_b14.txt`, 10/10 under the first draft's module-level table); probe 9/9 under
the probe as it now stands (§3: the first review's [8], the second's [1] and [7], the third's [4] and
[5]); the ladder at 14 in `runs/ladder_b14.txt`.

## 5. Stage 6: the picture and the voice — `sc-ironhail-sunder-fx`

The brief's stage 4 ("picture, voice, carry; nova's field spec out; `engine_ab`, `shell_identity`,
`render_ab`, `chain_audit`, one fight watched"), picked on measurements under Rick's "you pick i
overrule" by two labs run in parallel on the final (the picture lab's scratch and
`tools/ironhail_voice_lab.py`), and built as **`ironhail_build.py --stage 6` on the final**
(`sc-ironhail-sunder`): **fifteen anchored edits, byte-exact to the labs' own row files** (voice 3,
picture 12; no two share an anchor, so none is merged; ten re-emit their anchor and five replace the
nova's art outright). The picture rows alone reproduce the picture lab's stamp (`f03b657a1d99d86c`);
voice and picture together are the voice lab's combined page to the byte (`b8ff2014a954be3f`), in
either order. The generator (`runs/stage6/gen_s6.py`) checks the returned rows against the files, the
stamp, that no anchor sits inside another's, and both orders, then writes `S6` into the builder with a
`--stage 6` that refuses to run twice (`'tickQuarrel' is already in this source`), refuses anything but
the final (the b14 link, stage 2, stage 1 and the bare tip all refuse), and scans every stage-6 insert:
no RNG, no `ultFx`, no call into the simulation (`apply`, `hurt`, `beat`, `resolveHit`, `tickHail`,
`spawnShot` ...), no write but to its own `quarrel*` fields, the canvas, a tag's count, a puff's own
clock, `taught` and an oscillator's pitch, no mutation of any array but its own, and the inlined
`fx.js` copy untouched. The picture sheet is `05-reference/v108/ironhail-picture-sheet.png` (sha16
`da19edc582be8e06`); the voice lab's 51 wavs are `05-reference/v108/ironhail-*.wav` (gitignored).
Readings 15-21 are in the builder's docstring and §0.

### 5a. The picture (v83 §4), as built

- **The cast: the limbs in the forge.** The bow's limbs are stroked over the shape (SHAPES.bow's own
  limb path, in the shape's own frame, so every other bow draws as before) in a forge's dull red
  `#8A2C0A` with a forge-orange edge `#F08A30` and, while hot, a pale heart `#FFE2A8`; the rivets are
  redrawn on top so the plate still reads. Up over 0.15s, held for the window, cooled over 0.5s after
  it -- off `ultHail && !over`, so they cool at the verdict too.
- **Each bolt, while it falls:** a rune on the spot it will land on (dwarven `dark`, r 14, ringed and
  crossed in the school's core -- the design's words), with a ring closing on it from the bolt's reach
  (60) as it falls: where it lands, and how soon. The bolt itself falls from the top of the LIVE hall
  (the seals walk the ceiling in) as the bow's own shot stood on end -- its gradient streak and its dart,
  pointing down -- gathering speed. All of it is drawn from `m.hail`'s own `{x, y, t}` and `t / fallT`,
  so a bolt hangs where the sim holds it through a hit stop; nothing is kept per bolt and nothing draws
  from the rng (`shellHash` on the landing's count).
- **A landing:** a splash ring out to the bolt's reach -- `tickHail`'s own test drawn, a foe whose
  shell touches it was struck -- in the school's glow, five dust blobs kicked up, **six sparks** (the
  design's number) fanned up and falling back, and **four iron-spark motes** rising for 1s (the
  design's field, drawn: §5c). The **SUNDER tag on the foe ticks up** with its count, on the foe's rim
  toward the spot; one sunder tag on the foe at a time (Tendril's and Temper's rule: a tag already up,
  the bow's own or the last bolt's, takes the new count in place). A killing landing tags nothing: the
  shatter owns that frame.
- **A miss:** a splash ring in dust brown (`#8A6A3A`, the retired nova's floor-dust colour) and fainter
  dust, and nothing else.
- **How a resolved bolt is found:** by watching `hailTally.landed / missed` rise and the bolt that left
  `m.hail` since the last tick (read, never written), so `tickHail` makes no call for the picture and
  hit-or-miss is the tally's word. The puff and the limbs live on the FIGHTER (`quarrel*`), never on the
  one ultFx slot (open item 25).
- **The nova's art is retired with the nova:** `drawUltUnder`'s floor-dust ring and `drawUltOver`'s
  release flash (fourteen arrow streaks and the mount's kick ring, keyed on the slot's `"ironhail"`);
  the charge rune's eight heads going out become three bolts dropping onto a crossed rune, lower as the
  charge fills and on it when it goes off; the banner's letters, which converged in the nova's fan, now
  fall out of the ceiling letter by letter, a streak over each (Daybreak's rising letters, the other way).
- **The resting silhouette is the shipped one, unchanged:** the six bows at the app's size, Ironhail's
  riveted dwarven siege bow reads |dL| 0.093, last of six (umbral 0.099, bloodsworn 0.122, verdant 0.186,
  vigil 0.187, sanctified 0.217): the darkest steel of the six palettes. Three brighter-edge variants
  reached 0.100-0.110 and were **not taken** (the design names no change to the resting bow; Rick's to
  overrule).
- **The picture lab's numbers** (on the final, 9 fights, 76 frames at 540x960 through the post chain):
  the picture's share of the arena's bloom lift at most **+0.0006** (gate +0.02); the foe's disc moves
  at most 0.0216 and the caster's 0.0086, and the frames past 0.90 are the same 2 with and without it.
  Three controls come back wrong, as they must: a caster halo puts the caster's disc past 0.90 on 59 of
  63 window frames; a 200-unit landing flash lifts the arena past +0.02 on 15 of 76 frames and pushes
  the foe's disc past 0.90 on 14; a 40-unit column stays inside (+0.0065) -- the size of flash the gate
  would miss. Legibility (median |dL| of each part's own pixels, out of a stop): the streak 0.215, the
  dart 0.154, the ring 0.172, the rune 0.117, the splash 0.230, the sparks 0.332, the tag 0.163, the
  limbs 0.179, the dust 0.070, the motes 0.065. **Frame cost** (Electron 44, RTX 3070, interleaved A/B
  on the same state, the PC busy): the picture's own calls +0.0 to +0.6 ms at the median (+1.2 at most at
  p90) on 6-10 ms of drawing, whole-frame medians inside the noise (-2.5 to +2.1 ms). **Sim identity:**
  14 whole fights (12 with Ironhail, 2 without), every step hashed, the final against the picture link
  undrawn and drawn: identical in all four arms; the 1e-9 sim-write control differs on all 12 Ironhail
  fights and on neither without. **Kills:** 4 hail kills drawn
  -- the puff at the spot, no tag on the kill frame, the limbs cooled 0.5s after.

### 5b. The voice (v83 §4; `tools/ironhail_voice_lab.py`)

Every render an OfflineAudioContext at 48 kHz through the game's own `Sfx.buildChain`; the lab's
controls reproduce v88's published rune-crack, BAR and hit numbers before anything new is read. Levels
are set against Ironhail's own blow (the hit at 16.23). Round 1 found no cast that passed and a landing
(DEEP, 55-73 Hz) a phone cannot hear; round 2 added the phone gates (culverin's: the top high-passed at
200 Hz; a landing's stepping partial at or above 200 Hz over the score) and new candidates.
- **The cast -- WHOOMPH, of 9** (5 more as controls): "a forge-bellows huff, 0.4s". A swell of
  lowpassed air (150 -> 300 Hz) with the huff on its top (400 -> 150 Hz): one hump, never dipping on
  the way up and never growing again after its top; its power centred at 203-272 Hz on every noise draw
  (a bellows, not a quench's hiss or a rumble); no peak more than 2.5 dB over its neighbours (air, not a
  note). Audible 350 ms; its loudest 50 ms -3.2 to -1.6 dB re the blow; register at most 0.77 against
  rune-crack, the school's and the bow's casts, the tornado's woosh, the bowstring, the blow and the
  death voice. The rejected: PUSH / ARC dip on the way up; EXHALE / ROAR / LOW regrow 11-12 dB after
  their top; all five register 0.91-0.99 against the woosh. Ironhail had no arm and fell through to
  rune-crack (as 11 other relics on this link still do): the row ADDS its arms before that shared
  fallback and re-emits the fallback line unchanged.
- **A landing -- RINGING, of 9** (5 controls): "a short iron thud (<=0.15s), pitched by sunder count".
  A sine body under a falling punch, an iron bar struck (its first mode, a triangle at 2.76x, as loud as
  the body and ringing 0.8 of its decay; its second, a sine at 5.40x, at 0.35) and a 12 ms 2.5 kHz
  contact click. **The note steps a semitone a stack: 110 / 117 / 123 / 131 / 139 / 147 Hz at counts
  1-6** (measured within 0 cents); on a phone the count is its iron, 304 / 322 / 341 / 361 / 383 /
  405 Hz, +13.3 dB or more over the score's p90. Rise under 1 ms; gone by 125 ms at every count; 0.72
  of its power under 400 Hz at the worst; the iron partial 144 cents off every harmonic; loudest 50 ms
  -2.6 to -2.3 dB re the blow; register at most 0.74 against the blow, the clank, the bowstring, the
  death voice, rune-crack and the cast. `tickHail` plays it once per landed bolt, AFTER its hurt and its
  sunder, with `n` = the foe's count then (the number its tag shows). The rejected: BOLT and BLOCK
  register 0.82-0.84 against the blow and the death voice; DEEP is inaudible on a phone (-11.8 dB);
  PLATE and PENT do not rise on a phone.
- **A miss -- SAME, of 4** (3 controls): "a quieter thud". The landing's own thud at count 0's note
  (103.8 Hz, a step under a first landing: a miss sunders nothing), -5.9 dB under the quietest landing,
  gone by 130 ms, +10.5 dB over the score where a phone hears it; register at most 0.76. DULL / DEAD /
  DUST (the thud without its iron) are not heard over the score (-3.7 to -6.1 dB) and register 0.92
  against the death voice. `tickHail` plays it once per missed bolt, on the miss line's own test read
  first (the anchor guards it: if that line changes, the row stops applying).
- **The close plays nothing** (v83 §4: "close -- nothing"); no row touches the close line.
- **Wired and checked in the lab:** through the patched `play()` every arm reproduces its candidate
  (worst 1e-07) and 125 other voices are unchanged (worst 2e-07); `ult/ironhail` is no longer rune-crack.
  148 fights with the rows beside the original: 148/148 identical and every other voice call identical
  in order and options; 403 casts -> 403 cast voices, 1906 landings -> 1906 landing voices (7 killing),
  5275 misses -> 5275 miss voices; 318 clock closes, 51 death closes and 34 windows open at the fight's
  end, none voiced. The control (the rows plus a 1e-9 nudge of the foe on a landing) is 2/148 identical.
  **In a real window** (Ironhail v Cindercleave 108601, 11 landings, 9 misses) every landing stands
  +6.4 dB or more over the fight and the score in its loudest third-octave at or above 200 Hz over its
  first 50 ms, every miss +4.4 dB or more, the cast +9.1 dB. With Bindweed's, Coldiron's and
  Portcullis's Sfx rows applied too, in either order, every arm renders alike.
- **The voice lab's flags, printed and not gated** (Rick's to hear): Coldiron's close voice (an iron
  ring on the same A2 bar partials) registers 0.91 against this miss and 0.80 against this landing --
  heard only in an Ironhail v Coldiron fight, and its 0.4s ring is not a 0.13s thud; Portcullis's cast
  registers 0.83 against this miss; and 67% of landings arrive at the sunder cap (6: 1284 of 1906 in the
  lab's fights, 4016 of 5896 in the probe's), so the step-by-step pitch is heard mostly over a fresh
  foe's first five landings -- the design's cap, not the voice. The wavs to hear first:
  `05-reference/v108/ironhail-pick-sequence.wav` (the cast, landings 1-6 each with a miss, the blow) and
  `ironhail-pick-real-window(-without).wav` (the Cindercleave window with and without the three voices).

### 5c. No new `fx.js` field -- the iron-spark motes are drawn; the nova's field spec goes out of both copies by the orchestrator

v83 §4: "Field: iron-spark motes on landings, both copies." A SPECS field fires ONCE, at the one ultFx
slot's cast edge, at the slot's spot. The picture lab measured it on real fights (96 Quarrelstorm
windows, 16 foes x 2 seeds, both sides): **the slot is Ironhail's for a median 0.62s of its 8s window**
(the cast's own record expiring in 83 windows, the opponent's cast taking it in 13); **15 of 417
landings came while it was still Ironhail's**, and a landing's spot is a median **254 units** from the
point the field would spawn at. A slot-borne field cannot fire at a landing, so the motes are drawn:
four embers rise off every landing, in the emissive pass, for 1s. **Rick's to overrule** (Zenith's,
Canopy's and Temper's precedent).

**The nova's field spec, `SPECS.ironhail` (a `beam` of 1300 -- "A VOLLEY IS MANY SHOTS"), is the brief's
"nova's field spec out"**, and it lives in BOTH copies (`src/render/fx.js` and the page's inlined copy).
`fx.js` is shared by every build in the batch, so this builder does not edit it: the removal is the
orchestrator's `sync_fx_remove` (dawn_build.py's shape: the whole inlined module compared to
`src/render/fx.js` before and after, both stamps re-cut), run at the carry. **Until then the stage-6
link still fires the nova's beam field at each cast** (the builder asserts its inlined copy untouched).
The picture lab's `ih-final-fx.html` (`4463f003dd5230b8`) is that look with the spec out of the inlined
copy, and the probe reads 9/9 on it with every number of `runs/probe_sunder.txt`.

### 5d. Stage 6's gates -- every one able to fail

Every file named here is in `runs/stage6/` (the labs' own outputs in `runs/stage6/picture_lab/` and
`runs/stage6/voice_lab/`).
- **engine_ab sc-ironhail-sunder -> sc-ironhail-sunder-fx, ALL 38 RELICS WITH Ironhail, n=6: PASS,
  4218 / 4218 matches identical field for field**, no page errors, 38 / 38 distinct winners, 4218
  distinct seeds, 22.7-114.9s (`engine_ab38.txt`). Presentation moves no fight, Ironhail's included.
  (The voice lab's own engine_ab, 7 relics x 30 seeds: 630 / 630 for the voice page and for picture +
  voice, `voice_lab/engine_ab_final.txt`.)
- **ironhail_probe: 11/11 on sc-ironhail-sunder-fx** (`probe_fx.txt`, 444 fights), and **every line
  of [1]-[9] and every mechanism number is `runs/probe_sunder.txt`'s to the digit** (diffed). The two
  new checks switch themselves on from the page -- [10] when `"ironhail-land"` is in
  `AC.SFX.play.toString()`, [11] when the Match has `tickQuarrel` -- so the same probe still reads
  nine checks on a link without stage 6: on `sc-ironhail-sunder` it reads **9/9, every line past the
  header `runs/probe_sunder.txt`'s** (`probe_sunder_newprobe.txt`; the stage-2 and 50% links, which carry
  no stage 6 either, were not rerun under it):
  - **[10] the voice:** one cast voice inside every Ironhail `fireUlt` (1266); inside every
    `tickHail` call exactly its resolved bolts' voices, in order -- a landing thud per landed bolt whose
    `n` is the foe's count after THAT landing's sunder, read in the apply and again when the voice
    plays (5896: n 1-6 = 323 / 375 / 404 / 386 / 392 / 4016; 27 of them on a killing landing, under the
    death voice), a miss thud per missed bolt (16427) -- and nothing else but a ward's own shatter
    (`shatter()` plays its crit hit voice inside `hurt()`, once a break: 96, every one accounted for);
    the closes silent (996 clock, 140 death); every Ironhail voice of the run accounted for by those
    events, in both passes and every verdict.
  - **[11] the picture:** `tickQuarrel`, the picture's one hook on the step, leaves the sim exactly as
    it found it on each of its 5,381,274 calls (both fighters' bodies, statuses, window and tally; the
    match's clock, stop, verdict, holds, beats, shots and the bolts in the air) and draws no RNG; the
    limbs are up exactly while the window is open, the match runs and the caster stands; every
    resolved bolt gets exactly one new puff at its own spot, hit or miss as `tickHail` resolved it
    (22323: 5896 landed, 16427 missed); a live landing has a sunder tag on the board reading the foe's
    count (5869) and a killing landing adds or recounts none (27); limbs up at `over` are at 0 by 0.51s
    into the verdict (269); no resolved bolt goes unshown; and on the DRAWN subset (the first seed,
    both sides, every foe, through the kill and the verdict, the post chain off) 38,520 frames drawn --
    34,632 with the picture up, 4,826 of them in a hit stop, 497 in the verdict -- none throws, draws
    the match's RNG or changes the sim.
  - **Controls, one thing each, each failing its own check alone** (`probe_mut_*.txt`; the mutants by
    `mutants6.py`; one seed, 74 fights): **mS1** the landing thud played before its sunder fails [10]
    alone (397: every thud under the cap a count short, and the run's accounting); **mS2** a thud on
    every window close, deaths included, fails [10] alone (215; the fights unchanged, 74.3%); **mS3**
    `tickQuarrel` nudging the foe it tags by 1e-9 fails [11] alone (1087; it also moves the fights,
    74.3% -> 58.1%, which engine_ab would catch too); **mS4** a drawn frame nudging the bolt it draws
    fails [11] alone (24,565 findings, each "a drawn frame changed the sim"; the fights as the clean seed's, 74.3%) --
    headless fights never draw, so only the drawn subset sees it;
    **mS5** the puff drawn at the foe instead of its bolt fails [11] alone (3942). The clean link on
    the same seed reads 11/11 (`probe_fx_s1.txt`).
- **render_ab sc-ironhail-sunder -> sc-ironhail-sunder-fx, the other relics' pairs**
  (paradox:heartwood:25064, twinshade:lastlight:991, bulwarden:vinesower:70707, axiom:grudgebearer:31337
  at 0.5 / 6 / 12 / 22 / 31 / 40s): **PASS, 24 / 24 frames pixel-identical** (`render_ab_others.txt`).
  **The control, Ironhail v Cindercleave 108238 at 15-22.5s, inside its first window: 0 / 6
  identical, exit 1**, as it must (`render_ab_control.txt`). (The picture lab's own: 54 / 54 on nine
  other pairs, 0 / 6 on each of two Ironhail pairs: `picture_lab/renderab.out`.)
- **chain_audit** (`--relic sc-ironhail-sunder-fx --tip sc-ironhail-sunder-fx --builder
  ironhail_build.py`): **ALL 24 INSERTS SURVIVE**, exit 0 (`chain_audit_fx.txt`: stages 1-3's nine and
  stage 6's fifteen). **The control** (the same relic against `sc-ironhail-sunder` as the tip): **14
  LOST, exit 1** (`chain_audit_fx_ctl.txt`). The fifteenth, the miss voice, reads "ok" in the control:
  the line chain_audit picks as its marker (the guard `if (!foe.alive || !(Math.hypot(...) < u.hitR +
  R))`) is a substring of the miss line the insert anchors on and re-emits, and the audit counts
  substrings, so it cannot see that insert go missing. The probe's [10] is its guard (every miss thud
  accounted for, and more than none); declared in §6.
- **tip_audit on sc-ironhail-sunder-fx: exit 0, its body identical to the final's**
  (`tip_audit_fx.txt` against `runs/tip_audit_sunder.txt`, diffed past the first line, the page's
  path): stage 6 touches no status tip.
- **The builder:** refuses to run twice, to overwrite, and on the 50% link, stage 2, stage 1 and the
  bare tip; and **stages 1, 2, 3 and 6 (and 5 --alt50) rebuilt from `02-chain/sc-tendril-t3` into a
  temporary folder match every link's sha** -- stub 7f99, hail d3d9, sunder 1bed, fx b8ff, b14 dadb
  (`builder_checks.txt`). **Its own guards can fail:** eight copies of the builder, each with one
  forbidden thing written into a stage-6 insert -- a sim write (`foe.x +=`), an RNG draw, the ultFx
  slot, a `beat`, a splice of the bolts in the air, a write into `m.hail[...]`, a write to the tally, a
  `Math.random` -- all REFUSE and write nothing; the unmodified builder writes `b8ff2014a954be3f`
  (`builder_controls.txt`).
- **It composes** (`compose6.txt`, `compose6.sh`): stages 1, 2, 3 and 6 chained on the real tip give
  `sc-ironhail-sunder-fx` to the byte, and on eight other builds -- `02-chain/sc-tendril-fx` and
  `sc-onslaught-fx`, and the batch's scratch links `sc-coldiron-temper-fx` (whose own stage 6 anchors
  on the same rune-crack line and the same `tickPresentation` head), `sc-angelus-b9`,
  `sc-lightkeeper-bulwark-b9.5`, `sc-lodestone-b205`, `sc-oracle-sight` and `sc-widowmaker-b1075` --
  stage 6 writes **the same 509-line diff** (md5 `1df1972410f0`) on every one. The other way round,
  angelus 1-2-3-5, coldiron 1-6, lightkeeper 1-2-3-5, lodestone 1-2-3-5, oracle 1-3, widowmaker 1-2-5,
  and bindweed's and portcullis's stage 6 all apply on `sc-ironhail-sunder-fx`.
- **Not run here:** `shell_identity` (the app's json is shared: the orchestrator's), and verify (stage
  6 moves no fight: engine_ab above, over all 38 ids).

### 5e. The clip (Rick's to overrule)

`tools/_ironhail_pick.py` (from `_ironwood_pick.py`, by way of `_coldiron_pick.py`) scores a window on
v83 §4: it must close BY ITS CLOCK with both alive (the only close that shows the limbs cooling, and
shows the close silent), land AND miss, and the fight must run on for the clip's 1.8s tail; the counts
the landings thud at score a point a count heard, so a window that climbs beats one that starts at the
ceiling (`runs/stage6/pick.txt`: 12 foes x 6 seeds and two named pairs, Ironhail side A). **The pick:
Ironhail v Cindercleave (Breach), seed 108238**, cast at 14.83: a clock window of 8.57s, 9 landings and
11 misses, **the foe's count heard at every step, 1 -> 6**, from none (score 19.70; Spellbreaker 99015,
the picture lab's own look, 19.50).

    python tools/cinema_clip.py --game <scratch>/ironhail/links/sc-ironhail-sunder-fx.html \
      --a ironhail --b cindercleave --seed 108238 --at 13.63 --window 11.57 --end-at-window \
      --fps 60 --w 540 --out 07-shorts/v108/quarrelstorm-window.mp4

**`07-shorts/v108/quarrelstorm-window.mp4`**: 11.60s, 695 frames, 540x960 at 60fps, AAC 48 kHz stereo,
2,953,333 bytes; the fight is still on at the end (473 v 257; the kill is at 43.6s, outside the clip).
**The timeline** (`clip_timeline.txt`, clip time): the cast at 1.20; landings at 1.99 (SUNDER 1), 3.27
(2), 4.07 (3), 5.27 (4), 5.67 (5), 6.07 (6) and three more at 6; eleven misses; **the clock close at
9.77**. **Five frames checked through the pipeline** (an ffmpeg tile of frames 84 / 202 / 322 / 400 /
601, and the close's own frame, 586): the banner's letters falling on their streaks, a bolt falling
from the top of the hall onto its rune and closing ring, the limbs in forge-orange; a landing's splash
ring with SUNDER 2 on the foe; SUNDER 4 on the foe; a bolt's ring on the foe with the limbs still hot
(6.67); at the close the last miss's brown dust ring; 0.25s after it the limbs cooling. The art
renders through the post chain. Cindercleave's Breach jets fill much of the second half.
**The AAC** (`clip_aac.txt`): mean -23.2 dB, max -2.5 dB; integrated -21.4 LUFS, LRA 1.9 LU, true
peak -2.5 dBFS. **The voices read off it** (`clip_audio_check.txt`: Goertzel on the decoded mono
track, the 60 ms after each event against the 60 ms before): the cast's bellows band +13.6 dB at
200 Hz; **every landing's iron partial (the count's note x 2.76, where a phone hears it) +9.9 to
+48.6 dB, stepping 304 / 322 / 341 / 361 / 383 / 405 Hz with the count**; every miss's partial at
286.6 Hz +3.8 to +35.7 dB (the first, 0.38s after the cast, sits under the cast's own huff); **the
close adds nothing** (the 100 ms after it at -28.0 dBFS against -26.7 before; the bellows band near
-54 dBFS throughout).
**One thing in the clip is not the design's: at each cast the retired nova's particle beam
(`SPECS.ironhail`) still fires** -- a white spray from the bow toward the foe over the first frames
after the cast. That is `fx.js`'s spec, which the orchestrator takes out of both copies (§5c). The
clip is of the stage-6 link as it stands; once `sync_fx_remove` has run on the carried tip, the cast
shows only the limbs, the banner and the first bolt. **Rick's to overrule, all of it.**

## 6. What is left, and whose

- **Rick:**
  1. **The blade target** (v83 §6.2). Built at the design's own default, **the shipped rate**: the
     blade holds at 16.23 (`sc-ironhail-sunder`, 909 of 1480, 61.4%, against the shipped relic's 917,
     62.0%). 16.5 is the other measured point nearest it (925, 62.5%): **an exact tie**, 8 wins either
     side, broken to the blade that does not move and stays inside the bow row; 16.5 is one number away
     if Rick reads the tie the other way. **50%** is blade 14 (732 of 1480, 49.5%, `sc-ironhail-b14`,
     `--stage 5 --alt50`, gated in §4: engine_ab identical, verify's reds the base's own, tip_audit
     identical, chain_audit whole). The design's "~15.3" was priced on Chromium 141 against a lab SHIP
     of 55.8; on 151 there is no gap to take back.
  2. **The cadence:** 0.4s as priced and as §4 states, where §1's prose says "every third of a second".
  3. **The hail on the caster's own path** (§6.3): not, the design's default (the probe's [4] holds it
     since the third review).
  4. **The card:** the design's 68-character alternate (the 74 fits in pixels but not verify's cap).
  5. **The brief's gates, and the built links miss four of them** (§2's table): stage 2
     (`sc-ironhail-hail`) reads 18.18 drops a cast against "~19" (met), but **4.76 landed against ~6,
     19.05 damage against ~24 and 46.1% against ~57: RED**; stage 3 (`sc-ironhail-sunder`) reads
     sunder = landings to the digit (met) and **59.4% against ~62: RED**. The causes are measured: the
     "~57" was an estimate with no run behind it (the lab's own arm B at the taken point reads 50.0 on
     151, so no build could meet it), and the rest -- ~21% fewer landings, so ~21% less damage and
     sunder, and the rates' ~3 points -- is the window clock (a bolt's 0.3s of fall is ~0.34s of match
     time), which two controls in §2 reproduce both ways. The build keeps the engine's convention and
     every designed number; stage 5 prices the relic as built and, at the shipped blade, it reads the
     shipped rate both sides, the design's own stage-3 target. Meeting the landing gates on the
     engine's clock would take a change to a designed number, which is Rick's call, not this build's.
  6. **The type spread** at the final (flail 70 .. greatsword 49; shipped flail 77 .. twinblade 50;
     at the 50% alternative warhammer 63 .. greatsword 29) and the largest foe moves against the
     shipped relic (Ironwood +55, Widowmaker +25; Paradox -25, Bulwarden -22.5): item 12/32.
  7. **The veto** (§6.1) is waived under the batch's no-vetoes ruling.
  8. **Stage 6, all Code's picks under "you pick i overrule" (§5):** the clip
     (`07-shorts/v108/quarrelstorm-window.mp4`, §5e); the sheet (`05-reference/v108/ironhail-picture-sheet.png`);
     the voices (the bellows WHOOMPH, the RINGING thud a semitone a stack, the miss as the same thud a
     step under and 5.9 dB down, no close voice; wavs in `05-reference/v108/`); the picture (the limbs
     in the forge, the rune and its closing ring, the falling bolt as the bow's own shot on end, the
     splash to the bolt's reach, six sparks, the SUNDER tag); **the iron-spark motes drawn in place of
     an `fx.js` field** (§5c); the resting bow left as shipped (last of the six bows by |dL|, three
     brighter variants measured and not taken); and the nova's art retired (the charge rune's three
     falling bolts, the banner's falling letters).
     The voice lab's printed flags are his to hear (§5b): Coldiron's close registers 0.91 against the
     miss and 0.80 against the landing (the same A2 iron-bar partials; only an Ironhail v Coldiron
     fight has both), Portcullis's cast 0.83 against the miss, and two landings in three arrive at the
     sunder cap, where the thud no longer climbs.
- **The orchestrator (ALL DONE at the carry, §7):**
  - carry **stages 1, 2, 3 and 6** onto the chain with `--src <tip>` (each on the one before; stage 6
    goes on the carried stage-3 link and refuses anything else) and prove each with `engine_ab` (stage
    6 over every id, Ironhail included); `--stage 5` without `--alt50` refuses by design;
    `ironhail_probe.py --game <the carried link>` is the mechanism's own gate there: 9/9 on the stage-3
    link, **11/11 on the stage-6 link** ([10] and [11] switch themselves on from the page);
  - **the nova's field spec out of BOTH copies** (§5c): `SPECS.ironhail` (the `beam` of 1300 under "A
    VOLLEY IS MANY SHOTS") from `src/render/fx.js` and the inlined copy, by `sync_fx_remove`, with the
    stamps re-cut. Until then the cast still fires the nova's beam field (and the clip shows it, §5e);
  - `shell_identity` on the carried stage-6 link (not run here: the app's json is shared), and the
    clip to Rick (one clip per ultimate).
- **Standing, not this build's:**
  - verify's three reds are the base's own (§4): the two clock bands, red on every link since the
    minute pace, and Heartwood's two 0/40 pairings (Twinshade, Bindweed);
  - chain_audit's marker for the miss-voice insert is a line the insert re-emits a prefix of (its guard
    `if (!foe.alive || !(Math.hypot(...) < u.hitR + R))` is a substring of the miss line it anchors
    on), so the audit counts that insert present on any tip that has the miss line; its control finds
    the other 14 stage-6 inserts LOST and this one "ok" (§5d). The probe's [10] -- every miss thud
    accounted for, and more than none -- is that insert's guard. A chain_audit fix (count whole lines,
    not substrings) is chain_audit's owner's.

## 7. The carry onto the chain, and the nova's field spec out

Built and gated in scratch on `sc-tendril-t3` while the batch's other builds ran on the same tip, then
carried onto the batch line after Coldiron's stage 6 with the same builder, one stage at a time
(`--src` the previous link), and one more link that takes the retired nova's particle field out:

```
sc-coldiron-temper-fx.html        the batch line's tip (Coldiron stage 6)   67cc3e6e05d5326e
  -> sc-ironhail-stub.html         stage 1                                   f16340749a2465d6
  -> sc-ironhail-hail.html         stage 2                                   4661de4efec62d74
  -> sc-ironhail-sunder.html       stage 3 (= stage 5: the blade holds)      1833597f1b08d92f
  -> sc-ironhail-sunder-fx.html    stage 6                                   b51c2539999dd272
  -> sc-ironhail-fxout.html        SPECS.ironhail out of both fx.js copies   4b3775e5900172ea
```

- **The four builder links rebuild byte for byte from the tip** (`runs/carry_links.txt`: each rebuilt
  into scratch and compared with `02-chain/`; the session that first wrote them ended during its
  engine A/B, so all of it was re-run).
- **engine_ab, the scratch stage-6 link against the carried one, all 38 ids of the scratch build
  (Ironhail included), n=6: 4218/4218 identical** (`runs/carry_engine_ab.txt`). Every number above
  carries.
- **The nova's field spec out: `tools/fx_remove.py --relic ironhail`** (new; dawn_build.py's
  `sync_fx_remove` lifted out of a builder, because a scratch build cannot edit the shared file). It
  removes the four lines under "A VOLLEY IS MANY SHOTS" from `src/render/fx.js` AND the inlined copy,
  requires the two copies equal before and after, re-cuts both stamps (**fx.js 28fc58641370a1a9 ->
  8bf7db5ceb2685a0**, the stamp stage 6 predicted), and refuses if anything but the block and the
  stamps moved; `--dry` checks without writing (`runs/fxout/fx_remove.txt`). Its controls: a relic with
  no entry and a page whose inlined copy diverged from the disk file both refuse.
- **Gates on `sc-ironhail-fxout`** (`runs/fxout/`):
  - engine_ab against `sc-ironhail-sunder-fx`, every id on the link (39, Ironhail and Coldiron
    included), n=6: **4446/4446 identical** (`engine_ab.txt`);
  - render_ab: the other relics' four pairs **24/24 identical**; Ironhail v Cindercleave 108238 before
    its first cast **4/4 identical**; **the control, the same pair through the cast (14.95-15.35s),
    0/5 identical** -- the beam spray is gone and nothing else moved;
  - `ironhail_probe.py` **11/11** (`probe_fxout.txt`, 456 fights on this tip);
  - tip_audit exit 0, its body the stage-6 link's (only the path differs);
  - **shell_identity 185/185** (app Chromium 152 vs headless 151; the pointer not moved, the json
    restored);
  - **yert's staff carry, dry run onto this link** (`staff_carry.py --src sc-ironhail-fxout`, to
    scratch): **all 35 stages hold, syntax ok** (`staff_carry_dry.txt`), so the batch line still takes
    the staves when Rick moves GAME to it.
- **The clip, re-filmed on `sc-ironhail-fxout`** (same command as §5e, `--game` the carried link):
  `07-shorts/v108/quarrelstorm-window.mp4` (sha16 b72fe463ad2063c8, 2.77 MB, 11.6s, `runs/fxout/clip.txt`).
  The cast frames (14.9-15.2s) show the falling banner letters, the first bolt and its rune, and no
  beam spray.

# v106 — WIDOWMAKER / EXSANGUINATE, BUILD. STAGES 1-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-lodestone-b205-fx`, the nova's field spec out of both `fx.js` copies: §7): stage 1 is arm A to the fight; the drain is the lab's, tick for tick; the built relic reads the lab's arm B (58.0 against 58.1), the window clock and the frozen-step drain measured and offsetting; the blade holds the SHIPPED win rate, as the design says (§3, §5): 10.75, 47.0% both sides against the shipped nova's 46.7 on the same fights. The band's 50 is 11 (49.2%): Rick's other choice (v76 §6.2), one number. Gated: the probe 10/10 on stages 2 and 5 (after a third review it rebuilds her whole blade, reads every field of both fighters at the cast and every write to her hp, and pins the charge and the window from the builder; twenty-two mutants each fail their own check alone), engine_ab on the 37 others identical (3996/3996), verify the base's own 10/13 (Widowmaker 50.0% there, the nova 49.3). Stage 6, the picture and the voice (the nova's art retired): `sc-widowmaker-b1075-fx`, twelve rows byte-exact to the labs'; engine_ab on all 38 WITH her 4218/4218; the probe 12/12 (two new checks, the voices and the picture's hook, each failed by its own mutants); render_ab 24/24; six fights drawn as the app draws them identical to undrawn (6/6); the clip is with Rick. On the batch line (§7): both carry A/Bs identical, `SPECS.widowmaker` out of both copies with the NOVAS header kept (`sc-widowmaker-fxout`), the probe 12/12 there once it learned Coldiron's clank mass, shell_identity 200/200.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`, the BUILD row under the
redesign's). Input: `06-docs/v76/widowmaker-exsanguinate-redesign-v76.md` (§5 its build brief), and
nothing else (rule 0). Builder `tools/widowmaker_build.py`, probe `tools/widowmaker_probe.py`, runs in
`runs/`. **A REDESIGN of a shipped relic**: Widowmaker keeps her row, her blade type, her channel and her
names; her nova is replaced. The roster stays at 38.

**Revised 2026-09-27 after an adversarial review.** (1) The blade moved from 11 (the 50% crossing) to
10.75, the shipped rate: the design's own stated target, which the first pass had set aside for the
batch's crossing. (2) Probe check [5] now rebuilds every factor of a blow from its definition. Before,
it read `dmgMul` and `dmgTakenMul` back from the engine, so a blade change routed through them passed
8/8. (3) The builder no longer refuses when no other relic is still a nova. (4) §6 below, "What is
left, and whose", is new. Every gate the fix can move was re-run on the new final link
(`sc-widowmaker-b1075`). The old stage-5 link, `sc-widowmaker-b11` (7438eed4e6e4ca6b), is kept in
scratch as Rick's other choice (`variants/sc-widowmaker-b11-alt.html`; the builder at
`TUNED["dmg"] = 11` rebuilds it). Its run files (`*_b11*`) stay in `runs/` as the measurements at 11.

**Revised again, 2026-09-27, after a second review.** Four findings, all taken:
1. **Probe [1] could not see the window's clock across a hit stop.** It counted `tickDrain` calls and
   never read the window on a frozen step. The review's mutant R1 (the window also ticking in the
   hit-stop branch: the lab's step clock) changed 111 of 148 fights and passed 8/8. [1] now reads the
   window on every step: a frozen step must leave it exactly as it was, and a live step must move its
   clock by exactly dt. R1 is in the mutant table and fails [1] only (§3).
2. **§6.3 was misread.** "Her own cap (Bloodletting's 8)" is the hemorrhage STACK ceiling
   (Bloodletting's `cap:8`, the bleeding fighter's `bleedCap`), not her maxHp. The code lifted nothing
   and still lifts nothing. But the probe read the foe's ceiling back from the engine, so the review's
   mutant R63 (the foe's ceiling at 8 while she drains; 141 of 148 fights changed, she wins 68.0%)
   passed 8/8. A new check, [9], rebuilds the ceiling from its definition and fails R63 alone.
   Reading 10 and the §6.3 line in §6 are rewritten. [3] (maxHp) is now tied to §2's "capped at
   `maxHp`", where it belongs.
3. **About one window in eight is still set when the match ends.** A kill landed after `tickDrain`
   in the last step ends the match, and `step` runs no ticker after `over`. Reading 5 now says so, the
   probe counts those windows, and stage 6 is told to stop its thread at `over` (§5).
4. **Readings 9-11 were not in the builder's docstring.** They are now, with reading 10 corrected.

The page comment on `tickDrain` said the same thing as the old reading 5, so it was reworded too. That
moves the bytes of links 2 and 5. Their code is unchanged: with comments stripped, both links are
identical to the ones the first review gated. They were deleted by hand, rebuilt, and every gate was
re-run on the new bytes: relic_rate reproduction, built vs lab, probe, mutants, engine_ab, verify,
tip_audit, chain_audit and the compose check. The stub's bytes did not move.

**Revised a third time, 2026-09-27, after a third review.** The review found the build correct and
every finding in the probe. Each was a sentence whose check read only part of the state it names,
the same class as rounds 1 and 2:
1. **Her own state was not read (should-fix).** [6] snapshotted the foe at the cast and only her hp;
   [7] compared her statuses only inside a drain tick. The review's LS (lifesteal 0.35 in the window,
   the lab's rejected arm D; she wins 65.3%) and BLESS (Blessing 3 on her at the cast; 63.1%) changed
   142 and 146 of 148 fights and passed 9/9. Now:
   - a new check, **[10], "the drain is her only heal"** (§3: "Lifesteal is Triplicate's (umbral) and
     is not taken"; §4: "Blessing is NOT used"). A setter on her `hp` fails any rise outside another
     fighter's status tick, where [2]-[4] already hold every change of it exactly. No Blessing and no
     lifesteal may be on her after any step or at any blow.
   - **[6] now reads every field of both fighters** at the cast: every own number, flag and string,
     and every status. Only her window, her tally and the engine's cast count may move. It also
     fails a cast that draws the RNG or adds to any array of the match but the common ult beat.
   LS and BLESS fail [10] alone (§3), at the review's own 65.3% and 63.1%.
2. **[5] rebuilt a blow's damage and onHit, not the swing (should-fix).** The review's SPIN (her
   blades 10% faster in the window) changed 148 of 148 fights and passed 9/9. [5] now rebuilds the
   whole blade from its definition, in the window and out:
   - the turn on every step;
   - the two segments (reach);
   - the hit test (width) and the cooldowns;
   - each blow's knock, the foe's hitstun and the stop;
   - her side of every clank (mass).
   SPIN and four more blade mutants (knock, reach, clank mass, a row edit) fail [5] alone. [5] also no
   longer exempts the 124 blows on a cursed foe or into Bulwarden's wall: it rebuilds them with the
   foe's own rule.
3. **The probe took the window and the charge from the row it tested (note).** They are now pinned
   from the builder's `ULT` (8 and 14), and the twinblade's profile from its `SHIP_HEAD`. [8] asserts
   the cadence: every cast comes exactly 1681 live steps (14 s) after the last. A row with `dur:9`
   fails [1] alone, and one with the lab's unconverted `charge:16` fails [8] alone.
4. **The nova's art on a stage-5 tip (note).** It stays declared (reading 8, §5), and stage 6 should
   land before any clip.

**No link moved.** The builder changed only in its docstring (readings 6 and 9 now name the probe's
[8] cadence and [10]; sha16 a3b2d26d581735c7). It rebuilds all three links byte for byte. So the
gates that read the links (relic_rate, built vs lab, engine_ab, verify, tip_audit) stand as run on
these same bytes in round 2. Re-run in round 3 were the probe (every stage and control), the mutants,
the compose check, the refusals and chain_audit. The compose check now also runs on the real chain
tip, `sc-tendril-fx`.

```
sc-tendril-t3.html              the base: the chain tip (Bindweed stage 5)                  5a6216e3b629fad4
  -> sc-widowmaker-stub.html     stage 1  the nova out, the drain's block in, stubbed (1e9)  f2de7bed898799f6
  -> sc-widowmaker-drain.html    stage 2  the drain, charge 14 (the design's stage 1)        a5b403ceeafb2efa
  -> sc-widowmaker-b1075.html    stage 5  the blade, 11.95 -> 10.75 (the design's stage 2)   a9977a757d5772b7
  -> sc-widowmaker-b1075-fx.html stage 6  the picture and the voice (the design's stage 3) a253d1d3816d0c85
     (sc-widowmaker-b11-alt.html  the same at 11, the crossing: Rick's other choice, scratch  1a805fe1de1d531b)
```

(Before the second review: drain 2a5f0e1b97159ce6, b1075 18e927591b54ebc3, b11 7438eed4e6e4ca6b. The
same code, the old comment.)

**Built in scratch, not on the chain.** Several batch builds run in parallel on `sc-tendril-t3`. The
orchestrator carries each onto the real chain one relic at a time, rebuilding it with its builder
`--src <tip>` and proving the carry with engine_ab. The links above live in the build's scratch
folder. The builder rebuilds each of them byte for byte from the base (re-checked after the third
review with the builder at a3b2d26d581735c7).

It also re-applies cleanly on later tips (`runs/compose_check_b1075.txt`):
- on a scratch tip carrying Lodestone's stages 1-2 and Ironhail's stages 1-2 (their own builders);
- on one carrying Lightkeeper's Bulwark redesign, stages 1-5, the parallel build that takes Lightkeeper
  off the nova;
- on the real chain tip as it stands now, `02-chain/sc-tendril-fx.html` (Bindweed's stage 6,
  eea0cde5536955b3). It is read only; its links are in scratch (added in round 3, after the third
  review ran the builder there).

On each, its 70 added and 2 removed lines are the same lines in the same order. On a scratch tip where
no other relic is a nova at all, it still builds and says so. There are no stages 3-4: the design has
one mechanism stage.

## 0. What this build stands on

- **The relic** is Widowmaker as shipped (the donor is herself): twinblade, reach 62, width 8, artW 30,
  spin 5.7, mass 1.1, blades [0, 0.5], onHit hemorrhage 2, blade 11.95 until stage 5. The builder
  asserts, by content and never by which relic is last:
  - that row;
  - `STATUS.hemorrhage` at dps 1.5;
  - `tickStatus`'s dps tick as written;
  - the status source contract and its fall-back attribution;
  - its four anchors.
- **The charge is 14.** The design's lab cast every 16s of its own step clock (`ult_overlay`'s default),
  converted under Rick's batch ruling. It was measured for this fighter on arm B with a census copy of
  `drain.js` (`runs/drain_freeze.js`), which counts, before each lab step, whether the step is frozen
  (`hitStop > 0 || latch || splitHold`), over 660 fights a block (`runs/s0_census_B_*`). **12.57% /
  12.45% of the lab's steps are frozen, and 13.96% / 13.96% inside windows. So the lab's 16 is the
  engine's 13.99 / 14.01, which rounds to 14.** (The nova also shipped at 14.)
- **The lab is `ult_overlay.py --mech overlays/drain.js`** (the design's own stage-0 command), with arms
  A (no ultimate), SHIP (the nova live) and B (the drain), side A. **No lab default differs from the
  settled numbers:**
  - `drainMul` defaults to the design's 1.0;
  - `steal` is read only by the rejected arms C and D;
  - charge 16, window 8 and the shipped blade are the harness's defaults, as priced.
- **What is retired, and what is not.**
  - Stage 1 deletes Widowmaker's nova block from her row: radius 240, dmg 16, apply hemorrhage 3, knock
    200 and its card (§4: "the nova's `radius` and `apply` are deleted").
  - `kind:"nova"` and its cast tail stay. Bulwark and Consecration (Lightkeeper, Censer) still use them
    on this base. The builder reads who is still a nova and never refuses on it: both relics are being
    redesigned too, and either may be carried first.
  - The new ultimate is its own kind, `"drain"`. No string `"drain"` exists on the base.
    `Match.drain()`, the lifesteal's mote stream, is a different thing and is not touched.
  - **The nova's picture, voice and field are NOT retired in stages 1-5.** These are keyed on the relic,
    not the kind: the fang burst (`drawUltOver`, `u.w === "widowmaker"`), the "wet slice" ult voice,
    `SPECS.widowmaker` (both copies), the ultFx `life` entry and the banner's letter spread. The design
    retires them at its stage 3 (our stage 6). Nothing in the simulation reads any of them.
  - **With `radius` gone from the row, the kept fang burst draws at the fallback 300 px, not 240.**
    `fireUlt`'s ultFx record takes `u.radius || 300`, and `drawUltOver`'s Widowmaker branch scales by
    it. This is presentation only, until stage 6 retires the burst.
- **Readings** (in the builder's docstring):
  1. **The window is 8s.** §1 says "for a duration" and names no number. The lab ran `ult_overlay`'s
     default window, 8, and that is what was priced.
  2. **The drainer is the bleeding fighter's opponent.** §4 reads `st.src` and says hemorrhage's source
     "is written by apply (since v66)". On this base it is not: the blade's onHit apply passes none
     (only Corona's burn and the batch's window ultimates write a source), so every hemorrhage stack
     has `src` undefined. The build takes the engine's own attribution for hemorrhage instead, from the
     fatal-tick beat: "hemorrhage and smite still fall back to the other fighter". That is also what
     the lab drained. A source, if a later build writes one, must name her.
  3. **A shade's bleed drains nothing.** The lab's `foe` is the opponent, never a Twinshade shade.
  4. **A tick on a fighter already dead drains nothing; the killing tick drains** ("every tick"). The
     lab drained neither; the fight is decided either way.
  5. **The window closes by its clock or on a death that `tickDrain` sees** (the lab's close is
     either death). A kill landed later in the same step (a blow in `tickHits`, after the window
     tickers) ends the match with the window still set: `step` runs no ticker after `over`, so that
     window never closes. It is about one window in eight (209 of 1706 in the final link's probe run).
     Nothing in the simulation reads `ultDrain` after `over`. Stage 6's thread is drawn off
     `ultDrain`, so it must stop at `over` (§5).
  6. **No wait clause.** Charge 14 against a window of 8 on the same clock cannot overlap. The probe
     asserts it ([8]), and also that every cast comes exactly 14 s of her live clock after the last.
     It pins 14 and 8 from the builder, never from the row it tests.
  7. **The card is written at stage 1** (the design lists it at its stage 2). The stub is the new
     block, and the nova's card would describe a cast that is gone. "Her foe's bleeding drains into
     her: every tick of it heals her" is **62** characters (§4 prints "(66)").
  8. **The nova's picture and voice still play at the cast in stages 2-5** (above).
  9. **hp and nothing else** (§4; §3's "Lifesteal ... is not taken"): no status on her (Blessing is
     not used), no lifesteal, no float, no beat, no stop, no knock. The cast resolves nothing. It keeps
     `fireUlt`'s common banner, 0.08 stop and ult beat. The probe holds this in three checks: [6] the
     cast, [7] the drain tick, and [10] "the drain is her only heal".
  10. **The drain lifts no cap** (§6.3, "left out"). The cap §6.3 names, "her own cap (Bloodletting's
      8)", is the hemorrhage STACK ceiling: Bloodletting's `cap:8`, the bleeding fighter's `bleedCap`,
      recomputed in `tickSpectre`. It is not her maxHp. The build lifts nothing: her foe's bleed
      ceiling stays hemorrhage's own 4, since no spectre of hers can stand to raise it. The probe's
      [9] holds that from the definition. The heal's own cap at her maxHp is a different rule, §2's
      ("heals `hp` by it, capped at `maxHp`"), held by the probe's [3]; her maxHp never moves.
  11. **The blade holds the shipped rate** (§3, §5; see §4 below).

  Readings 1-11 are all in the builder's docstring (9-11 were added after the second review; 6 and 9 were extended after the third).
  Readings 12-16, stage 6's, are in the docstring too, and in §5d below.
- **Names:** kind `"drain"`, fields `ultDrain` / `drainTally`, ticker `tickDrain`. All are free on the
  base and in every batch builder in `tools/` (grepped).
- **The clock:** the window runs on the window tickers' clock, which stops in a hit stop. So does the
  bleed it drains (`tickStatus` does not run in one). The lab's window ran 8 step-seconds, frozen ones
  included, and paid the drain on frozen steps where the engine's bleed does not tick (§2).

## 1. Stages 1, 2 and 5

Stage 1 replaces the ult line of her row with the drain's block at charge 1e9. The clock never reaches
it and `fireUlt` never runs, so it is the lab's arm A.

Stage 2 (the design's stage 1: "the nova out, `f.ultDrain` in, `tickStatus`'s branch") sets charge 14
and adds:
- **the fields** `ultDrain` / `drainTally`, after `this.vineTally = null;`;
- **the drain**, in `tickStatus`'s dps branch right after `f.hp -= d;`. It fires when `key ===
  "hemorrhage"`, the tick was on a live fighter, and that fighter's opponent is alive with her window
  open: `me.hp = min(me.maxHp, me.hp + d)`. `d` is the engine's own tick, `dps x stacks x dt x
  dmgTakenMul`, read and never changed;
- **the cast**, `kind === "drain"`, before `kind === "tendril"`. It opens `{t: 0, dur}` and returns
  before the generic tail (no damage, knock, stun or status);
- **`tickDrain`**, after `tickTendril` (before `tickWinnow`): `t += dt`, the close on the clock or on
  a death it sees (reading 5), and the probe's window-frame counts.

Stage 5 moves the blade, 11.95 -> 10.75 (§4).

Every insert is anchored exactly once. Each strips clean of the RNG, `spawnFx`, `ultFx`, any write to
the shared weapon, and any apply / beat / hitStop / float / SFX / velocity / stun / hurt. `node --check`
parses the page, and the page is written LF.

The builder refuses:
- to overwrite a link;
- a name that is not `sc-widowmaker*`;
- a stage on the wrong source (stage 2 on the base, stage 5 on stage 1, stage 1 on a built link, stage 2
  or 5 twice).

All refusals were re-checked after the third review (`runs/builder_refusals_b1075.txt`,
`refusals.py`). The compose check was re-run with the builder as it now stands
(`runs/compose_check_b1075.txt`, `compose_check.py`); that run includes the real chain tip.

## 2. Stage 0 and the stages against it — the clocks, measured and offsetting

The lab command is `ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic widowmaker --mech
overlays/drain.js --arms A,SHIP,B --seeds 20 --foes <33>`, on seed0 2207 and 2317, 660 fights an arm a
block. The foes are the design's 33 (the 34-relic roster without the donor). The built links run
`--arms SHIP` on the same foes and seeds, with the same seed formula and side. The blade-10.75 and
blade-11 lab rows are arm B with `--P blade=`.

```
                               lab on 151 (1 / 2)   published 141   BUILT (1 / 2)              pooled
A    no ultimate               40.2 / 40.9          37.1            stage 1: 40.2 / 40.9       identical, fight for fight
SHIP the nova as shipped       47.0 / 48.3          46.4
B    the drain, 11.95          57.6 / 58.6          57.1            stage 2: 57.1 / 58.8       58.0 (lab 58.1)
B    the drain, blade 10.75    47.3 / 48.3          --              stage 5: 47.1 / 45.9       46.5 (lab 47.8)
B    the drain, blade 11       52.9 / 50.6          51.5            (b11:    48.6 / 50.9       49.8 (lab 51.8))
```

- **Published vs 151.** SHIP and B reproduce (+0.6 / +0.5 on block 1). A reads 3.1 / 3.8 over the
  published 37.1. Two things moved under it: the runtime (141 -> 151), and the base (`sc-trunk` ->
  `sc-tendril-t3`, which redesigned two of the 33 foes, Axiom and Dawnbringer). The lifts over A
  shrink to match: SHIP +6.8 / +7.4 and B +17.4 / +17.7, against the published +9.2 and +20.0.
- **Stage 1 is arm A fight for fight** on both blocks:
  - every foe's rate and blow count is identical (`runs/built_stub_*`);
  - every field of `AC.simulate`'s summary is identical on all 2640 fights (33 foes x 20 seeds x 2
    blocks x both sides; `runs/stub_vs_A.txt`, `stub_vs_A.py`);
  - the control, the base with the nova live, differs on 2588 of them.
- **Lab mechanism on 151 (arm B):** 3.66 / 3.67 casts; **24.5 / 24.2 hp drained a cast, 4.0 / 3.9 of
  it paid on frozen steps**; the foe at 2.23 / 2.22 stacks on a window frame; 8.4 blows in windows
  and 11.0 outside. At blade 10.75: 24.2 / 24.3 hp a cast.
- **Built (the probe, both sides, 444 fights): 23.5 hp drained a cast.** The tally and her hp deltas
  agree to the digit; the design's gate is "~24 hp a cast, off hp deltas". Also: 3.73 casts; 2.18
  stacks; 9.8 blows in windows and 9.8 outside; a window is 960 steps of the window clock and **9.26s of
  match time**; 14.5% of window steps frozen. The round-2 and round-3 probes read the same numbers to
  the digit (`runs/probe_drain_r2.txt`, `runs/probe_drain_r3.txt`).

**The built relic reads the lab, and that is two clock effects cancelling, both measured.**
- The engine's window is 8 seconds of the window clock, about 9.3s of match time at 14% frozen. The
  lab's was 8 step-seconds.
- The engine's bleed does not tick in a hit stop, so the drain is paid only on live steps. The lab paid
  it on every step.

Controls, blocks 2207 / 2317 (`runs/ctl_*`; `runs/drain_live.js` is the census copy with one switch,
`liveOnly`):

```
                                                          block 1  block 2  pooled  drained a cast
lab B: 8 step-seconds, drain on every step                 57.6     58.6    58.1    24.5 (4.0 frozen)
lab: 8 step-seconds, drain on live steps only              54.8     55.0    54.9    20.3
BUILT, its window on MATCH time (8s, scratch variant)      53.2     56.7    55.0    20.3 (the probe)
lab on the engine's clock: 9.30 s, live steps only         55.3     56.8    56.1    23.4
BUILT stage 2: 8s of the window clock                      57.1     58.8    58.0    23.5 (the probe)
lab at 9.30 s, drain on every step                         60.2     60.2    60.2    28.0
```

1. **The drain is the lab's, tick for tick.** The scratch build variant with its window on match time
   (the lab's 8s: `Z.t = this.t - Z.t0`, two lines, `variants/` in scratch) drains 20.3 hp a cast,
   has 8.4 blows in windows and reads 55.0. That is the lab's own live-steps arm within a tenth (54.9,
   20.3, 8.4). The probe (round 2's, and round 3's at 9/10) fails it on [1] alone, and for the reason [1] exists: on the first
   live step after a hit stop, its window's clock jumps by the whole stop ("a live step moved the
   window's clock by 0.0917, want 0.0083"; `runs/ctl_probe_matchclock.txt`). Before the second
   review, [1] failed this variant only because it rewrote `Z.t` outright. A window that ticked
   through the stop with `t += dt` (the review's R1) passed. It now fails too (§3).
2. **The frozen-step drain is worth about -3.** The lab paid 16% of its drain on steps where no bleed
   ticks (58.1 -> 54.9 when it stops).
3. **The engine's window is worth about +1 to +3.** 9.26s of match time holds more live ticks and more
   blows: the lab at 9.30 live-only drains 23.4 a cast, and the built link drains 23.5.

**At stage 5 the built link sits 1.3 under the lab's blade-10.75 arm** (46.5 against 47.8, pooled
1320 fights each). The standard error of a difference of two such reads is about 1.9 points, so this
is 0.7 of one. At 11 the gap was 2.0, and at stage 2 it was 0.1. On these same side-A fights the lab's
SHIP arm (the nova as shipped) reads 47.7, so the built redesign at 10.75 lands 1.1 under the shipped
relic here, and 0.3 over it both sides (§4). The build keeps the engine's convention and every
designed number: every window runs on the window tickers' clock, and a freeze freezes the world.
Stage 5 settles the blade on the built relic, wide, both sides.

## 3. The probe (`widowmaker_probe.py`, one check per sentence, read inside the hooks)

The probe wraps:
- `step`, `fireUlt`, `tickStatus`, `tickDrain` and `tickCharge`;
- `tickWeapon`, `bladeSegments`, `tickHits`, `resolveHit`, `resolveClank` and `checkEnd`.

It also puts a setter on Widowmaker's `hp`, so every write to it is read where it happens. It REBUILDS
`tickStatus`'s loop to get each tick's `d` exactly: the keys in order, each expiry, every dps tick
before the bleed, and the blessing. It runs Widowmaker against every foe, both sides, 6 seeds.

**The build's numbers are pinned, never read from the row under test** (the third review's note):
- the window (8) and the charge (14) come from the builder's `ULT`;
- the twinblade's profile comes from its `SHIP_HEAD`: reach 62, width 8, spin 5.7, mass 1.1, blades
  [0, 0.5], mode "spin", onHit hemorrhage 2, no knockMul, no lifesteal;
- the blade is the shipped 11.95 or `TUNED`'s 10.75 (`--blade` for another, e.g. 11).

After the third review it has ten checks, one per sentence of v76 §1, §2, §3, §4, §5 and §6.3:

- [1] "for a duration", **8 s on the window tickers' clock** (reading 1; the standing ruling). The
  row's `dur` must be the build's 8. It reads the window around every step:
  - a FROZEN step (a hit stop, the latch or the split, read on entry) must leave the window exactly as
    it was: the same object, its clock not moved, nothing opened or closed;
  - a LIVE step with the window open must move its clock by exactly dt, whether it closes or not (the
    cast's own step belongs to [6] and [8]);
  - a clock close must come after exactly the 960 window steps whose dt first reach 8;
  - a death that `tickDrain` sees must close the window;
  - every cast must be accounted for as a clock close, a death close, or a window still set when the
    match ends (counted, not failed: reading 5);
  - only Widowmaker carries `ultDrain`.
- [2] "every tick of Hemorrhage on the enemy heals her by the same amount": her hp moves by exactly the
  tick as dealt (the `dmgTakenMul` each tick actually read).
- [3] "capped at `maxHp`" (**§2**; §4's `min(src.maxHp, ...)`): a tick that would pass it leaves her
  exactly at maxHp, and her maxHp never moves in a status tick.
- [4] nothing drains with the window shut, from a shade's tick or from a corpse's. The foe's own hp is
  rebuilt exactly in every status tick, **each dps tick at Sunder's definition** (`1 + taken x
  stacks`), so the tick itself is never changed.
- [5] **"her blades are unchanged": THE WHOLE BLADE, in the window and out of it** (rebuilt after the
  third review). Every factor comes from its definition, never from the engine's methods:
  - **the row** against the pinned twinblade;
  - **the turn**: every live step turns her blade exactly once and no frozen step turns it. Theta
    advances by exactly `spin x spinMul x dt x spinDir`, or not at all while she is stunned. `spinMul`
    is `max(0.15, act spin x (1 + Entangle's spin x stacks) x desperation's 1.30 at or under 25%)`.
    `spinDir` is read on entry, so a clank's reversal needs no exemption;
  - **the segments**: every `bladeSegments` of hers is the two blades at `theta + off x TAU`, from
    `ballR - 4` to `ballR + reach x act reach`;
  - **the hit test and the cooldown**: every `tickHits` of hers lands exactly the blows that the
    segments and the width give (`ballR + width / 2`, the page's own `segDist` and `clamp`). It leaves
    each blade's cooldown at `combat.hitCd` or at the old one less dt. No blow of hers lands anywhere
    else;
  - **the blow**:
    - its damage, `blade x dmgMul x jitter x dmgTaken`, rounded, crit included, from the captured
      draws. `dmgMul` comes from the act's dmg and desperation's 1.35, `dmgTaken` from Sunder's
      `1 + taken x stacks`, and the crit from its own draw against `critChance` (the engine's crit
      count must agree);
    - a cursed foe's echo is added from curse's definition, and what Bulwarden's wall ate is read off
      the wall. **No blow is exempt any more** (round 2 exempted 124 of them);
    - its onHit: +2 where the bleed ceiling cannot bind (where it binds, the stacks are [9]'s);
    - **its knock**: `combat.knock`, x1.5 on a crit, away from her;
    - **the foe's hitstun**: impact's stun off the damage as handed to `hurt()`, with its diminishing
      return, and none on a kill;
    - **the stop**: impact's, x `critStopMul`, `killStop` on a kill, plus the wall's 0.05 and a ward
      shatter's 0.10 where they happen;
  - **the clank**: her side of every bind (the spin reversal, her stun, her velocity), from the two
    rows' masses (hers 1.1) and the streak.
- [6] "no damage change, no knock, no stun" at the cast, and "no new object" (§4). **The cast may
  change no field of either fighter**: every own number, flag and string, and every status. Only her
  window (`ultDrain`), her tally (`drainTally`) and the engine's cast count (`ultsFired`) may move.
  Her Blessing and her lifesteal are [10]'s, which reads them after every step, the cast's included.
  The cast may not draw the RNG or add to any array of the match, except the common ult beat (exactly
  one) and the note. Its stop is the common 0.08, and its window is `{t 0, dur}`.
- [7] a drain tick files no beat but the engine's own fatal-tick beat (at most one, and only when the
  foe's hp crossed 0 in that tick), no stop, no float, and no status on her.
- [8] **the charge, 14 on her live clock** (the lab's 16 converted). The row's charge must be the
  build's 14. Every cast must come exactly 1681 steps after the last, counting only the steps on which
  `tickCharge` runs with her standing (14.008 s, where dt first reaches 14), or after the match's
  start. No fight may end owing a cast, and no cast may come while her window is open.
- [9] **§6.3, "left out": the drain does not also lift "her own cap (Bloodletting's 8)"**, the
  hemorrhage stack ceiling. It is rebuilt from its definition: her foe's `bleedCap` is
  `STATUS.hemorrhage.maxStacks` (4) unless a Bloodletting spectre of HERS stands, and none can. The
  foe's ceiling must be 4 after every step and at every blow of hers, window open or shut. A blow where
  the ceiling binds must leave the foe at exactly 4, or where it was if at or above 4.
- [10] **NEW: the drain is her only heal.** §3: "Lifesteal is Triplicate's (umbral) and is not taken"
  (the lab's arm D, rejected). §4: "Blessing is NOT used (this is hp, not a status)".
  - A setter on her `hp` fails any rise outside another fighter's status tick, where [2]-[4] hold
    every change of it exactly. That covers her own blows, her own status tick and any ticker.
  - The one exempt write is `checkEnd`'s clamp of a dead loser's hp up to 0 (a corpse, not a heal),
    counted.
  - No Blessing may be on her after any step, and no lifesteal (her field or her row) after any step
    or at any blow of hers.

**Results:**
- **sc-widowmaker-drain (stage 2): 10/10** (`runs/probe_drain_r3.txt`). Every mechanism number is the
  same to the digit as in round 2 (`runs/probe_drain_r2.txt`), round 1 (`runs/probe_drain_v2.txt`) and
  the first probe (`runs/probe_drain.txt`):
  - 3.73 casts; 23.46 hp a cast; 576 drain ticks a cast; 2.0% at the cap;
  - 1655 windows: 1388 closed by the clock, 65 on a death, **202 still set at `over`**;
  - 14.5% of window steps frozen.
  New in round 3:
  - all 1655 casts came exactly 1681 live steps after the last;
  - her blade turned by its definition on 2.57 million live steps and held on 457,532 frozen ones;
  - 3.18 million `tickHits` were rebuilt;
  - the damage, knock, hitstun and stop of all 8695 of her blows were rebuilt, 116 of them with a
    foe's own rule;
  - 11,414 clanks;
  - 934,049 rises of her hp, every one inside another fighter's status tick.
- **sc-widowmaker-b1075 (stage 5, the final link): 10/10** (`runs/probe_b1075.txt`):
  - 3.84 casts; 23.58 hp a cast (the tally and the hp deltas agree); 580 drain ticks a cast; 2.3% at
    the cap;
  - 9.26s of match time a window; 14.4% of window steps frozen;
  - 1706 windows: 1445 closed by the clock, 52 on a death, **209 still set at `over`**;
  - **the charge**: every one of the 1706 casts came exactly 1681 steps of her live clock after the
    last, and no fight ended owing one;
  - **her blade**:
    - it turned by its definition on 1,215,675 live steps in windows and 1,429,853 outside (578,524
      of them stunned and held), and held on 469,246 frozen steps;
    - its segments were rebuilt 9.29 million times;
    - the hit test and cooldowns were rebuilt on 1,524,015 `tickHits` in windows and 1,747,478
      outside;
    - the damage, knock, hitstun and stop of all 9075 blows were rebuilt, 124 of them with a foe's
      rule;
    - 5820 clanks in windows and 5865 outside;
  - the foe's ceiling was 4 after every step (3.69 million) and at every blow; 4237 blows met it and
    stopped there;
  - **her only heal**: 967,558 rises of her hp, all inside another fighter's status tick. No Blessing
    or lifesteal after any of 3.69 million steps. None of her 9075 blows healed her. 235 deaths were
    clamped to 0 by `checkEnd`;
  - 10.4 blows a fight in windows and 10.0 outside; she wins 47.1%.
- **The same on a fresh block** (seed0 202001, 12 seeds, 888 fights): **10/10**
  (`runs/probe_b1075_s2.txt`). The mechanism numbers are round 2's to the digit:
  - 3.79 casts; 23.70 hp a cast; 579 drain ticks a cast; 1.7% at the cap;
  - 9.28s of match time a window; 14.6% of window steps frozen;
  - 3369 windows: 2831 closed by the clock, 113 on a death, **425 still set at `over`**;
  - every one of the 3369 casts came 1681 live steps after the last;
  - the blade was rebuilt on 5.22 million live steps and 6.47 million `tickHits`;
  - all 18,007 blows were rebuilt, 242 of them with a foe's rule; 23,077 clanks;
  - 1,916,585 rises of her hp, all inside another fighter's status tick;
  - she wins 49.1%.
- **One clause of [4] never ran.** A corpse's bleed tick inside an open window came up 0 times in every
  probe run. `tickDrain` closes the window on the step of a death, and once the match is over `step`
  runs no ticker. The kill flight that keeps a corpse ticking is armed only by the Grudgebearer and
  Ravelbone ult strikes. The `hp0 > 0` guard (reading 4) is written and unexercised, and no mutant of
  it could change a fight.
- **Controls** (`runs/probe_mutants_b1075.txt`, `mutants.py`). Twenty-two mutants of the final link, each
  breaking one sentence and each changing fights (out of 148: Widowmaker v every foe, 2 seeds, both
  sides). The probe runs each at 3 seeds:

  | mutant | fails | fights changed | she wins (3 seeds) |
  |---|---|---|---|
  | the window 10% long | [1] | 102 | 53.2 |
  | the window also ticking in a hit stop: the lab's step clock (the second review's R1) | [1] | 111 | 45.9 |
  | **the row's window 9, not the build's 8** | [1] | 106 | 53.2 |
  | the drain 1% over the tick | [2] | 74 | 51.4 |
  | the heal past maxHp (§2's cap lifted) | [3] | 8 | 51.4 |
  | the drain with the window shut | [4] | 147 | 64.0 |
  | the foe's bleed 10% harder while she drains (the second review's RFT) | [4] | 131 | 53.6 |
  | her blades +5% in the window through `Fighter.dmgMul` (the first review's mutant) | [5] | 148 | 47.7 |
  | the same +5% in `resolveHit` | [5] | 148 | 47.7 |
  | her onHit bleed 3, not 2, in the window (the second review's ROH) | [5] | 148 | 58.1 |
  | **her blades spin 10% faster in the window (the third review's SPIN)** | [5] | 148 | 46.8 |
  | **her blow's knock x1.2 in the window** | [5] | 144 | 45.9 |
  | **her blades' reach +10% in the window** | [5] | 148 | 53.6 |
  | **her mass x3 in a clank in the window** | [5] | 148 | 64.0 |
  | **the row's reach 66, not the twinblade's 62** | [5] | 148 | 55.4 |
  | the nova's 3 hemorrhage kept at the cast | [6] | 148 | 61.7 |
  | **the cast stuns her for 0.3 s** | [6] | 148 | 43.7 |
  | a drain tick that stops the world | [7] | 148 | 45.9 |
  | **the lab's charge 16, unconverted** | [8] | 148 | 46.8 |
  | the foe's bleed ceiling at 8 while she drains: §6.3's option (the second review's R63) | [9] | 141 | 68.0 |
  | **lifesteal 0.35 in the window: the lab's rejected arm D (the third review's LS)** | [10] | 142 | 65.3 |
  | **Blessing 3 on her at the cast (the third review's BLESS)** | [10] | 146 | 63.1 |

  Unmutated, the same 222 fights read 50.5% (`runs/probe_b1075_3seeds.txt`). **Each mutant fails its
  own check and only that one.** Bold rows are new in round 3. How the probe catches each of them:
  - **SPIN** fails [5] on the turn itself ("her blade turned -0.05225, want -0.04750").
  - **LS** fails [10]: "she carries lifesteal 0.35 after a step", and her hp rising across her own
    blow; 913,256 failures in all.
  - **BLESS** fails [10] on "she carries Blessing x3 after a step" and on her hp rising in her own status
    tick. Neither touches [6]. [6] leaves her Blessing and lifesteal to [10] on purpose, so that one
    sentence fails one check. [10] reads them after every step, the cast's included.
  - The cast's self-stun fails [6] on "the cast moved her stun: 0 -> 0.3".
  - The row mutants fail on their pins: "the row's window is 9, the build's 8" plus "a clock close after
    1080 window steps, want 960"; "the row's charge is 16" plus "a cast after 1921 steps of her live
    clock, want 1681"; "the row's reach is 66".
  - The clank mutant fails on her side of the bind ("her stun 0 -> 0.138 (want 0.254), vx ...").

  **The probe as it stood before each review misses that review's mutants.**
  - The round-2 probe (`runs/probe_v3_control.py`, sha16 912e8e4f6bad3545 as it shipped) passes all ten
    round-3 mutants 9/9, though they change 106 to 148 of 148 fights (`runs/probe_v3_on_r3.txt`).
  - The pre-round-2 probe (`runs/probe_v2_control.py`, 960863fbcb56a4c4) passes R1 and R63 8/8
    (`runs/probe_v2_on_R1_R63.txt`).
  - The pre-round-1 probe passes the `dmgMul` mutant 8/8 (`runs/probe_v1_on_mut5d.txt`,
    `runs/probe_v1_control.py`).
- **The match-clock control** (the scratch build variant whose window runs on match time, §2) reads
  9/10 on the round-3 probe and fails [1] alone (`runs/ctl_probe_matchclock.txt`).
- **One finding of the round-3 probe's own, fixed before any gate ran on it.** The first cut rebuilt a
  blow's hitstun and stop from `dealt`'s difference. After Bulwarden's wall that can lose the last bit
  of a fraction, and 2 of 8695 blows on the stage-2 link read 0.10648499934495101 against
  0.10648499934495106. It now reads the damage exactly as it is handed to `hurt()`. The wall's bite
  and the curse echo are rebuilt too, so no blow is exempt. Every run above is on the fixed probe
  (sha16 7c1e5d1420211714).

## 4. Stage 5: the blade — 10.75, the shipped win rate

The runs are `relic_rate.py`, both sides: each seed from both sides, every other relic a foe, 10 seeds
a foe a side, 740 fights a block, seed0 2207 and 2317 (`runs/stage5_rr_*`, `runs/ship_rr_*`).

```
                                   block 1  block 2  pooled (1480)  side A  side B  mean s
SHIPPED: the nova, 11.95 (the base)   45.3     48.1     46.7          48.1    45.3    63.4
the drain, 10.5                       44.7     47.4     46.1          47.3    44.9    68.9
the drain, 10.75   <- BUILT           46.6     47.4     47.0          47.4    46.6    68.3
the drain, 11      (the crossing)     48.8     49.6     49.2          50.5    47.8    68.1
the drain, 11.25                      51.1     51.9     51.5          53.0    50.0    68.1
the drain, 11.95                      54.3     56.8     55.5          57.6    53.5    67.4
```

- **The target is the design's: the SHIPPED win rate.**
  - v76 §3: "The build settles it wide on 151 to the SHIPPED win rate, not to 50 — a redesign keeps
    the fighter where it was."
  - §5 stage 2: "the blade, wide on 151 at 10.5 / 10.75 / 11, target the SHIPPED win rate".
  - The v87 handoff says "~10.7".

  §6.2 leaves the target to Rick ("the shipped 46 or the band's 50"). The build takes the design's
  default and flags the other choice (§6).
- **The shipped relic reads 46.7% on these fights. 10.75 reads 47.0** (+0.3; 10.5 is -0.6). It is the
  measured point nearest the shipped rate, and it lies inside the brief's "10.5 / 10.75 / 11", the
  design's "~10.6–10.8" and the twinblade row (8.3-11.95).
- **The design names no knob but the blade**, and none moved.
- **The built link reproduces the measurement exactly.** `relic_rate` on `sc-widowmaker-b1075`
  (a9977a757d5772b7) with no knob set gives 46.6% on block 2207 and 47.4% on 2317. Every foe's rate,
  `byType`, both sides and the mean duration (68.23s / 68.47s) equal the `--set dmg=10.75` runs, field
  for field, on both blocks. They also equal the same runs on the link's pre-round-2 bytes
  (`runs/stage5_rr_built_b1075_*`, `runs/stage5_rr_compare_b1075.txt`).
- **The band's 50 instead is 11** (49.2%, the measured point nearest the crossing at about 11.1). It is
  one number in the builder (`TUNED["dmg"]` 10.75 -> 11). That link was built and gated before the
  first fix (`sc-widowmaker-b11`, 7438eed4e6e4ca6b; `runs/*_b11*`):
  - probe 8/8;
  - engine_ab 3996/3996 identical;
  - verify 10/13 with the base's three reds (Widowmaker 53.0% there);
  - chain_audit 8/8.

  After the second fix it was rebuilt with the reworded comment (`variants/sc-widowmaker-b11-alt.html`,
  1a805fe1de1d531b; the same code). The round-3 probe on it (`--blade 11`) reads 10/10, as round 2's
  read 9/9 (`runs/probe_b11_alt.txt`). She wins 48.0% of the probe's 444 fights and drains 22.99 hp a
  cast, and 203 of 1701 windows are still set at `over`.
- **The drain lengthens her fights** (63.4s -> 68.3s mean): a heal is time.
- **The ladder at 10.75** (40 fights a foe, `runs/ladder_b1075.txt`, printed beside the shipped relic
  and 11):

  | type | at 10.75 | shipped | at 11 |
  |---|---|---|---|
  | warhammer | 55 | 50 | 52 |
  | bow | 53 | 44 | 60 |
  | greatsword | 47 | 50 | 49 |
  | scythe | 46 | 44 | 48 |
  | flail | 42 | 48 | 45 |
  | twinblade | 36 | 44 | 39 |

  - Worst foes: Twinshade 20%, Spellbreaker 27.5, Redflail 30, then Cindercleave, Lightkeeper,
    Slagheart and Vesper at 35.
  - Best foes: Censer 77.5, Marrowdraw 67.5, then Aureole, Bloodmirror, Heartwood and Duskreave at 60.
  - The redesign gains most on the bows and the warhammers, and loses most on the twinblades and the
    flails. At 40 fights a foe, a foe's rate has a standard error of about 8 points; the type rows (140
    to 240 fights) are the readable ones.
  - **The type spread is item 12/32, Rick's.**

**The gates on the final link** (`sc-widowmaker-b1075`, a9977a757d5772b7), all run on these bytes after
the second fix. The third review moved no link, so they stand. chain_audit was re-run in round 3
with the builder's new docstring:
- **engine_ab, sc-tendril-t3 → sc-widowmaker-b1075, the 37 others (every base id but Widowmaker),
  n=6:** **PASS. All 3996 matches are identical field for field**, with no page errors and 37/37
  distinct winners (`runs/engine_ab37_b1075.txt`, ids in `runs/ids37.txt`). The redesign moves no other
  relic's fight. The design's stage-1 gate says "the 41 others"; the chain carries 38 relics. The final
  link carries every line stage 2 adds, so this gate covers the drain as well as the blade.
- **verify --n 40 on sc-widowmaker-b1075 (38 relics): 10/13, the base's own 10/13 with the same three
  reds** (`runs/verify_b1075.txt`, 28120 matches, 3177s; the base's is v101's `verify_t3`). Its json
  and every check line are identical to the run on the link's pre-round-2 bytes. None of the three
  reds is hers:
  - the two clock bands: the overall mean is 61.1s against the base's 60.8, and the pairings run from
    Gravemourn/Ironhail 38.6s to Farwarden/Starwarden 100.0s, as on the base;
  - "both sides can win every matchup": Heartwood v Twinshade 0/40 and Heartwood v Bindweed 0/40, as on
    the base.

  Every relic is inside 30-70% (Heartwood 30.3 to Gloamwire 63.7). **Widowmaker reads 50.0%, against the
  shipped nova's 49.3% in the base's verify** (53.0 at blade 11). She is side A in 36 of her 37
  pairings (she is second in the roster). No other relic moves more than 0.7 points: each meets her in
  one pairing of 37.
- **tip_audit:** identical to the base's apart from the header path (`runs/tip_audit_base.txt`,
  `tip_audit_b1075.txt`). The one field no tip mentions is Burn's `feed`, which is the base's own. The
  build touches no status tip. The ult card is the builder's check: 62 characters, under 72.
- **chain_audit** (`--relic sc-widowmaker-b1075 --tip sc-widowmaker-b1075 --builder
  widowmaker_build.py`): **8/8 inserts survive** (`runs/chain_audit_b1075.txt`). With the base as tip
  it fails, as it must (`runs/chain_audit_b1075_ctl_base.txt`).
- **Built vs lab, re-run on the new bytes:** the SHIP-arm runs of stage 2, stage 5 and the match-clock
  variant (`runs/built_drain_*`, `built_b1075_*`, `ctl_built_matchclock_*`) have json identical, field for
  field, to the runs on the pre-round-2 bytes. §2's table stands as printed.

## 5. Stage 6: the picture and the voice — `sc-widowmaker-b1075-fx`

Picked on measurements under Rick's "you pick i overrule" by two labs run in parallel: the picture lab
(in scratch) and `tools/widowmaker_voice_lab.py`. Built as `widowmaker_build.py --stage 6` on stage 5's
link: twelve anchored edits, byte-exact to the labs' own row files (voice `ff78068cbe2fa1f2`, 2 rows;
picture `42121c10265e101c`, 10 rows). No two rows share an anchor, so none were merged, and no row's
anchor sits inside another row's anchor or code. The picture rows alone reproduce the picture lab's
stamp (`518477d4537ec077`) and the voice rows alone the voice lab's page (`373f16b7e0a85770`). The two
sets give the same bytes in either order, and those bytes are the link:

```
sc-widowmaker-b1075.html       stage 5                                                     a9977a757d5772b7
  -> sc-widowmaker-b1075-fx.html stage 6  the picture and the voice (the design's stage 3)   a253d1d3816d0c85
```

That is +16068 characters, +343 and -58 lines. The builder is `bf8dff45e6870fa4`. It wrote the link as
`51c97e69a975ca92`; since then only its docstring has moved (reading 16 now names the NOVAS header,
§5b), and it rebuilds all four links byte for byte. Stage 6's readings are 12-16 in its docstring.

- **The picture sheet:** `05-reference/v106/widowmaker-picture-sheet.png` (2200x4016).
- **The voice picks:** `05-reference/v106/widowmaker-pick-sequence.wav`: the inhale, three drips at
  each count, then a blow. The wavs are gitignored.

### 5a. The picture (v76 §4)

- **The cast.** Her shell flushes dark red for 0.25s. It is a darkening: a radial from 0.55 at the
  centre to 0.82 at the rim, drawn over both fighters in the world pass. When she is `b`, the foe's
  shell is cut out of it, so it stays on her layer. Her disc only darkens (by 0.04 to 0.34) and is past
  0.90 on none of 101 frames. The banner's word FILLS: every letter is there in outline from the first
  frame, and the red rises in it from the foot, left to right, in 0.35s. That is a level coming up,
  which is what the drain does to her. The nova's fan of letters and the drops running off the word
  are retired with it.
- **The thread.** It leaves the foe's shell on the drips' own arc (`_stBleed`'s 0.44 to PI - 0.44,
  the underside), at the point of it nearest her. It curves out of the wound before it turns for her,
  so it never crosses the foe, and it ends at her rim. It reaches her in 0.12s at the cast, or when
  the foe starts to bleed, and draws back into the wound in 0.15s when the foe stops. It is drawn only
  while her window is open, both fighters stand and the match is not over. It sits in the world pass,
  under both balls, so none of it is inside a shell or reaches the bloom.
- **The beads.** Three beads run down the thread. They are placed by her drained total, so they move
  only when a tick pays her: faster with more stacks, still at her full hp, frozen in a hit stop. One
  enters her shell per whole hp, on the frame its "+1" floats.
- **The "+n".** A red (#FF4F63) "+n" floats on her once per whole hp drained, not per tick (`hurt()`'s
  rounding rule). It is the engine's own `float`, filed in `tickSiphon` on the presentation clock and
  never in `tickStatus`, because "the drain files none" (reading 12; the probe's [7] holds a drain tick
  to no float).
- **The close: the thread snaps.** It breaks at its middle. The two halves whip back, one into the
  wound and one into her, with a bead on each torn end, and the tear throws six short strands and five
  drops that fall. It lasts 0.3s. It snaps at a clock close, at a death, or at the verdict. About one
  window in eight is still set when the match ends (reading 5), so the thread snaps at the verdict
  instead of hanging on the corpse. The snap is the only thing drawn after `over`, and it is gone
  before the verdict panel.
- **What is kept.** `ULTSIG.widowmaker`, the charge sigil ("a drop, and a ring drawn INTO it"), already
  reads as a drain. The design does not name it. No weapon art is touched. The silhouette at the app's
  size is unchanged: her blade's |dL| is 0.173, 2nd of the 5 twinblades (Spellbreaker 0.289 >
  Widowmaker 0.173 > Starwarden 0.156 > Twinshade 0.151 > Thornshear 0.144).
- **What is retired.** `drawUltOver`'s fang burst, the banner's fan, drops and 52 spread entry, and
  the "wet slice" (see the voice). The ultFx `life` entry keeps its number and is annotated as the
  cast's record, as for Daybreak and Corollary.
- **Numbers from the picture lab** (Chromium 151; Electron 44 on the RTX 3070):
  - **Legibility**, median |dL| out of a hit stop / in one:
    - thread 0.142 / 0.141
    - cord 0.133 / 0.137
    - beads 0.119 / 0.121
    - flush 0.086 / 0.118
    - "+n" 0.115 / 0.108
    - snap 0.145 / 0.083
    - banner 0.157 / 0.059 (in a stop, the banner is on its first outline frame)
  - **Bloom:** the picture's share of the arena-mean lift is at most +0.0002 against a +0.02 gate
    (9 fights x 101 frames). The control, a 120-unit white beam in the thread's place, fails: it is
    over +0.02 on 6 of 101 frames and puts the foe's disc past 0.90 on 46 of 101. No foe disc moves
    more than 0.006 (sanctified, umbral, dwarven and runic foes).
  - **Frame cost:** measured in Electron at 453x805 with the chain on, A/B interleaved, over 3
    fights. The picture's own calls take 0.2-0.5 ms median (0.3-0.8 ms p90), against 0.0 / 0.1 ms
    hidden. The whole frame is equal within noise in every phase. The PC was saturated by other
    builds, so both arms ran at about 55-80 ms a frame.
  - **Watched:** one whole fight at 453x805 (Aureole 4101, her as `b`): 267 frames, 4 windows, the 4th
    still open at the kill. The thread snaps at the verdict, and nothing of it reaches the panel.
- **A window with an unbleeding foe draws nothing after the flush and the banner.** That is the design:
  the thread shows "for as long as the foe bleeds inside the window". In the drawn fights, 53 of 76
  windows snapped. The rest had drawn back first. **Rick's to overrule** against his "hard to tell
  what it does" bar.

### 5b. No field in `fx.js` — the nova's is taken out, and nothing replaces it

The design says: "field spec REMOVED (the nova's burst spec is dead) — both copies, sha re-stamped"
(v76 §5, stage 3). Nothing replaces it. The measurement (the picture lab's `fxprobe`, 123 windows, 16
foes x 2 seeds, both sides) shows a SPECS field could never carry this ultimate:
- A field lives on the one ultFx slot. The slot is hers for a median 0.58s of the 8s window (max
  0.62s): 7.1% of the window's clock. It is lost to the clock expiring (107 of 123), the opponent's
  cast (13) or the match ending (3).
- Only 6.6% of the drained hp lands while the slot is still hers.
- While the drain pays, the foe is a median 186 units from where a burst would be drawn (p10 64, p90
  383).

So a slot-borne field could show at most the first half-second of an 8-second mechanic, in the wrong
place. The picture draws off the fighter instead, which is Zenith's and Canopy's precedent.

**The removal is not in the builder.** `src/render/fx.js` is shared, and on disk it now follows the
batch line's tip, so this builder edits neither copy. Stage 6 refuses to write if its edits touched
the inlined copy. `SPECS.widowmaker` leaves BOTH copies at the carry, by the orchestrator's
`tools/fx_remove.py` (reading 16). The entry, from the base's inlined copy (line 32282, byte-equal to
`src/render/fx.js` line 120):

```
    widowmaker: { mode: 'burst', n: 1620, sp: [240, 620], grav: 90, drag: 2.6,
                  life: [0.30, 0.75], heavy: 0.05, size: [0.8, 2.2],
                  spawn: 0.05, up: 0 },
```

**One catch for the orchestrator.** `fx_remove.py` removes the entry "with the one comment directly
above it". The line above Widowmaker's is the section header `/* ---- NOVAS: a burst that does NOT fall
--- */`, and that header also heads Lightkeeper's and Censer's entries. This was read with
`fx_remove`'s own `spec_block` on the link, which returns the header and the three lines. The two
removals give different module stamps:
- the picture lab's, the three lines only: `28fc58641370a1a9` -> `f710f845485543b6`;
- `fx_remove` as written, the header included: `024d7a84c2a43f42`.

No fight reads a comment, so either way is harmless to the game. But only the first is the page the
picture lab gated (the rows plus the spec out, `93e8955ef03be732`). So either strip the three lines
only, or let the header go and know that the stamp is not the lab's. Lightkeeper and Censer are being
redesigned off the nova too, so the header goes with them in the end.
`runs/stage6/specout.txt` (`specout.py`) builds the three-line removal in scratch, without touching
`src/render/fx.js`.

### 5c. The voice (v76 §4; `tools/widowmaker_voice_lab.py`, lab sha b672b1e2a0572e3e)

**Cast: MID, of 14 candidates.** A low breath, drawn in. Two lowpassed noise sweeps: 210 to 560 Hz,
and 420 to 1120 Hz starting 318 ms in, at g 0.5386.
- It is audible for 400 ms (the design's 0.4s).
- It is drawn IN: its band rises +1011 cents. The breath rises in 80 ms, with no dips and no
  regrowth.
- Its centroid is 301-366 Hz on every draw, which is low.
- It is air, not a note: TONAL 2.4 dB, TONAL-50 3.3 dB.
- It is heard +22.8 dB over the score. Its loudest 50 ms is -3.5 to -1.4 dB relative to her blow.
- Its highest register similarity is 0.79, against Starwarden's cast and the bowstring.

It REPLACES the nova's "wet slice" arm in place. The shared rune-crack fallback is untouched, so other
relics' rows anchored on it still apply in either order. SIP-H also passed the rule. MID wins the
stated tiebreak on a later top (TOP-PLACE 0.36 against 0.35), so that is a near-tie. All 7 cast
controls fail the rule. WHISTLE misses only by 0.02 dB on the air clause, while the slice misses it by
27.2 dB, so the clause can fail by a wide margin.

**Drain: TRI, of 5 candidates.** The bleed has no drip voice anywhere in the game, so the lab made one
(a drop into a pool: a sine chirping up 1.5x over 0.12s). Only its REVERSE ships: a triangle sliding
down a fifth onto the note as it swells, and stopping, at g 0.09989, with 122 strikes at count 4.
- **Pitch:** it lands at 906 / 1081 / 1214 / 1358 Hz against the declared 880 / 1047 / 1175 / 1319
  (A minor pentatonic from A5, one step per stack). Every note is within 57 cents, and the counts are
  at least 193 cents apart.
- **Reversed:** it falls 284-290 cents and is audible for 75-80 ms. LAST5 is 0.86 and LATE 0.78.
  ENV-CORR5 is 0.95 against its own drip's samples reversed. TONAL is 23.8 dB.
- **Quiet:** its loudest 50 ms is -11.3 to -10.7 dB relative to the blow, and at least +8.3 dB over
  the wall tick. Its highest register similarity is 0.51.
- **When it plays:** once per whole hp drained, the same unit as the "+n". n is the bleeding foe's
  hemorrhage stacks.
- DROP, SLURP and LOW also pass the rule. TRI wins the stated tiebreak (fewest strikes). All 6 drain
  controls fail the rule.

**The close plays nothing** (v76 §4).

**In fights** (the voice lab's 148 fights; this build's probe, below, counts the same thing):
- Only two of the four notes are ever heard, C6 (count 2) and E6 (count 4). The blade applies
  hemorrhage two at a time.
- A window has a median of 23 drips, one every 167 ms at the cap (the closest pair 158 ms apart).
- In a real window, the median drip is +21.7 dB over the fight in its band, and the inhale +15.5 dB.

**Flagged, not gated:**
- **Cost.** A drip at count 4 is 122 synth calls and 4.7 ms of main thread (3.0 ms at count 1). That
  is about 10,700 synth calls a fight. Daybreak's step, already on the chain, is 82 calls and about
  1.4 ms. The shorts render their audio offline, so only live play in the app pays this. If the app
  stutters, the fix is its own voice round: striking every second cycle risks a subharmonic.
- **Neighbours not on this base.** Coldiron's anvil, being carried now, sits at register 0.88 with the
  drip (0.87-0.92 when both land on the same note). LOW (at most 0.31 against it, and it passes the
  rule) is the one swap if Rick wants the two apart. Ironhail's bellows cast sits at 0.93 with the
  inhale (0.93-0.99 for every cast candidate but THROAT); the bellows' pitch falls where the inhale's
  rises.

### 5d. Stage 6 on the simulation's path — declared (builder readings 12-16)

Stage 6 puts exactly one line on the step's path that is not the presentation clock: the drip VOICE,
in `tickStatus`'s drain block. It reads `me.drainTally.drained` into a local before and after the
booked gain, then calls `SFX.play` once if a whole hp was crossed, with n read from the foe's stacks.
`SFX.play` draws nothing and writes nothing the simulation reads, and headless it returns on its first
line.

The picture finds the cast and the drain by watching `drainTally` rise (`casts` and `drained`), so
neither `fireUlt` nor `tickStatus` makes a call for it. Its one hook, `tickSiphon`, runs in
`tickPresentation`. It writes its own `siphon*` fields (on the fighter, never `m.ultFx`, open item 25)
and the "+n" floats, and nothing else. It uses no rng, no spawnFx and no Math.random; the jitter is
`shellHash`.

The builder refuses to write any insert that:
- draws the RNG or takes the ultFx slot;
- calls into the simulation;
- writes anything but its own fields;
- floats outside `tickSiphon`;
- plays a voice outside the drain block;
- puts on the sim path anything but that drip line.

It also refuses if the nova's burst, slice or spread survive, or if the inhale, drip, thread or flush
is not wired exactly once.

The probe's [6], [7] and [10] stay green without moving a clause. [6] sees no field set in `fireUlt`
(the flush clock starts in `tickSiphon`, in the same step). [7] sees no float in a drain tick. [10]
sees no new route to her hp.

### 5e. Stage 6's gates — every one able to fail

- **Builder refusals, 7/7** (`runs/stage6/refusals6.txt`).
  - The real builder refuses to go on twice ("'tickSiphon' is already in this source") and refuses
    stage 2's link (wrong base).
  - Five scratch copies, each with one S6 row mutated, are each refused by the rule that names it:
    - the picture's hook writing `foe.vx`;
    - the drip floating a number;
    - the hook drawing the RNG;
    - a voice at the close;
    - the wet slice kept.
  - **Control:** the unmutated builder, copied to scratch and given the same call, writes the link
    byte for byte (`a253d1d3816d0c85`).
- **engine_ab, stage 5 -> stage 6, ALL 38 relics INCLUDING Widowmaker, n 6: 4218/4218 matches
  identical field for field.** No page errors; 38/38 distinct winners; 4218 distinct seeds
  (`runs/stage6/engine_ab38.txt`). The picture lab's own run on its page (the rows plus the spec out)
  also came back 4218/4218.
- **widowmaker_probe (`89865c3332c39ce8`): 12/12 on the stage-6 link** (444 fights, 6 seeds;
  `runs/stage6/probe_fx.txt`). Every line of checks [1]-[10] is identical to stage 5's own run
  (`runs/probe_b1075.txt`): 3.84 casts a fight, 23.58 hp a cast, 1706 windows = 1445 + 52 + 209,
  47.1%. Two new checks:
  - **[11], the voices:**
    - 1706 casts, each exactly one inhale;
    - 39,993 drain ticks crossing a whole hp, each exactly one drip, its n the foe's stacks (count 2:
      7967, count 4: 32,026; no other count occurs);
    - 927,565 drain ticks paying less than a whole hp played nothing;
    - no voice on any close: 1445 by the clock, 52 on a death;
    - none through 2s of the verdict on the 209 windows still set at `over`;
    - none anywhere else.

    Only her two `ult` arms are read. A ward's shatter plays its own crit HIT voice inside `hurt()`,
    and the drain never goes through `hurt()`.
  - **[12], the picture's hook:**
    - 7,130,470 calls of `tickSiphon`, each changing no field of either fighter or of the match
      (the shared weapon row, the statuses, the window and the tally included) and drawing no RNG;
    - 39,993 "+n" floats, exactly one per whole hp crossed;
    - 1706 flushes for 1706 casts;
    - the thread up on 2,213,806 calls, never with the window shut, a fighter down or `over` set;
    - 969 snaps at a clock close and 236 at `over`;
    - every fight ends with every whole hp floated and the thread down.

  Detected by their own presence (the drip arm in `AC.SFX.play.toString()`, `tickSiphon` on the
  Match): **on stage 5's link the same probe runs [1]-[10] only and prints 10/10**, every line
  identical to stage 5's own run (`runs/stage6/probe_b1075_newprobe.txt` against
  `runs/probe_b1075.txt`).
- **The probe's controls, each able to fail** (`runs/stage6/probe_mutants6.txt`; 2 seeds, 148
  fights):
  - the stage-6 link unmutated: 12/12, 0 fights changed;
  - **[11a]** the drip on every drain tick instead of once per whole hp: fails [11] alone, with 0
    fights changed;
  - **[11b]** a close voice, on a death only: fails [11] alone, with 0 fights changed;
  - **[12a]** the picture's hook writing the sim (`foe.vx += 1e-9` on a "+n"): fails [12] alone,
    with 141 of 148 fights changed;
  - **[12b]** the thread left up past its close (no snap): fails [12] alone, with 0 fights changed.

  The stage-5 probe (`7c1e5d1420211714`) passes all four mutants 10/10: it cannot see stage 6, so
  [11]-[12] are what catch them. Three of the mutants move no fight at all, and the probe still sees
  them. [12a] changes 141 of 148 fights, and [1]-[10] still pass it: a picture that writes the sim
  shows up only in [12] and in engine_ab.
- **Drawn sim identity on this link: 6/6 identical** (`runs/stage6/drawn_ident.txt`, `drawn_ident.py`).
  The picture lab's drawn arms ran on its own page, without the voice rows, so this was re-run on the
  stage-6 link itself. Each fight is run three times in one page:
  - undrawn (`m.step` only);
  - drawn the way the app draws it (`AC.__inject`, then `AC.__draw` every second step at 540x960);
  - drawn, with a control write.

  Every run goes through the kill and 2s of the verdict. The state at the kill must be identical: steps, t,
  the winner, both fighters' hp, x, y, vx and vy, and her drained tally. The six fights are Aureole
  106038, Gravemourn 5150 and Lightkeeper 99008 with her as `a`, and Dawnbringer 99001, Spellbreaker
  99015 and Goreshard (`oathwound`) 106112 with her as `b`. All six are identical drawn: 25,658 draws,
  0 thrown. **Control:** a 1e-9 write to the foe's vx after every draw while her thread is up differs
  on 6/6. The run was cut off by a usage limit after four fights; the last two were run on the same link
  with the script's index argument, and both sittings are in the file.
- **render_ab: the other relics' pairs 24/24 frames pixel-identical** (Paradox v Heartwood 25064,
  Twinshade v Lastlight 991, Bulwarden v Vinesower 70707, Axiom v Grudgebearer 31337).
  **Control:** Widowmaker v Goreshard (`oathwound`) 106112 inside her window (frames 46.3-55.3): 0/6
  identical, so every frame differs, as it must (`runs/stage6/render_ab_*.txt`). The picture lab's run on its page:
  54/54 on other relics (the other bloodsworn relics, twinblades, banner neighbours and the newest
  chain pictures). Its controls differed at 4/6 and 4/6 of the fixed times.
- **chain_audit** `--relic <fx> --tip <fx> --builder widowmaker_build.py`: **ALL 20 INSERTS SURVIVE**
  (S1 1, S2 6, S5 1, S6 12). **Control:** stage 5's link as the tip loses all 12 of S6, exit 1
  (`runs/stage6/chain_audit_fx*.txt`).
- **tip_audit:** identical to stage 5's (`runs/tip_audit_b1075.txt`) apart from the header path
  (`runs/stage6/tip_audit_fx.txt`).
- **The carry re-applies** (`runs/stage6/compose6.txt`). All four stages were rebuilt by the builder on:
  - `sc-tendril-t3`: each link is byte for byte the scratch link (stage 6 `a253d1d3816d0c85`);
  - the batch line's newest link, `sc-ironhail-fxout` (39 relics; Coldiron and Ironhail carried),
    giving `e1c2875e791ff02d`.

  Stage 5 -> 6 is the same +343 -58 lines on both, and the stage-6 lines are identical (same
  signature). The labs also carried their rows onto `sc-tendril-fx`, `sc-coldiron-temper-fx`,
  `sc-ironhail-sunder-fx` and `sc-ironhail-fxout`.
- **shell_identity: NOT run here.** The app's json is shared; the orchestrator runs it. The nearest
  measurement is the picture lab's: Electron (RTX 3070) against headless 151 on its page, 36/36 fights
  identical, with a control page differing on 27 of 33 Widowmaker fights.
- **The labs' own gates** (`runs/stage6/`):
  - The picture's sim identity: 15 fights undrawn and drawn with every step hashed, all identical; a
    1e-9 sim-write control differs on 13/13 of hers.
  - The rows: 62 orders byte-identical, and `node --check`.
  - The voice's tickStatus row: 148/148 fights identical and every other SFX call identical; 558
    casts, 558 inhales; 13040 whole-hp crossings, 13040 drips. Its sim-write control: 0/148
    identical.

### 5f. The clip (Rick's to overrule)

`tools/_widowmaker_pick.py` (from `_ironwood_pick.py`) scores a window on §4. Widowmaker plays side
A, as the clip does. A window qualifies only if it closes BY ITS CLOCK with the thread still up, the
shells at least 160 units apart when it snaps (the design's close, big enough to read), and shows
every picture and voice event:
- the flush;
- the thread up where it can be seen (`_siphonPath` draws no line between shells closer than 2 ballR
  + 10);
- the "+n";
- drips at both counts the blade makes, 2 and 4;
- a draw-back when the foe stops bleeding;
- a hit stop with the thread up.

It also has to be free of anything that takes the screen from those events:
- no cast of the foe's, and no other banner, from 2.4s before the clip to its end;
- not the scrunch card, which opens at the match's first clank.

The qualifying windows are ranked on:
- drained hp;
- the thread's visible share of the window;
- draw-backs and blows;
- the snap's width.

Left out of the pool: Twinshade, whose shades bleed and drip and drain nothing (reading 3), and every
foe of her own affinity (a bloodsworn foe wears the same red shell and blades).

**Five windows were filmed. Four were set aside, each for a reason the picker now enforces.** Every
one is kept in scratch with its pick table (`runs/stage6/pick_*.txt`, `clip_*.txt`):
1. **Goreshard (Oathwound) 106112.** A bloodsworn foe: two red balls with red blades, so you cannot
   see which one the blood goes to. The first table's top, Twinshade 106001, was already out for its
   shades.
2. **Aureole 106038.** Aureole's Benediction fired 0.2s after her cast, and its banner replaced hers.
   It was her first cast, so the scrunch card (the match's first clank) opened in the middle of the
   window.
3. **Slagheart 106001.** The window closed with the shells 89 units apart, so the snap was a tear too
   small to read, and they touched a frame later.
4. **Grudgebearer 106038.** Grudgebearer's Crucible raised its banner 0.85s before her cast, without
   passing the cast count the picker read. The picker now reads any banner that is not hers.

Of 248 fights (31 foes x 8 seeds), 3 have a window that shows everything (`runs/stage6/pick.txt`):

    python _widowmaker_pick.py --game <scratch>/links/sc-widowmaker-b1075-fx.html --seeds 8

It prints the `cinema_clip` command below. It was re-run on the final picker (`385c1a64c9adae1d`) and printed
the same table (`runs/stage6/pick_rerun.txt`).
The pick is **Widowmaker v Spellbreaker, seed 106223**, cast at 47.22. The window is 9.41s of match
time, the thread visible 80.9% of it:
- 29.1 hp drained, 29 "+n";
- drips 8 at count 2 and 21 at count 4;
- 1 draw-back, 4 blows;
- the snap at 255 units;
- no other banner and no card.

Spellbreaker is a runic twinblade, blue against her red.

    python cinema_clip.py --game <scratch>/links/sc-widowmaker-b1075-fx.html --a widowmaker --b spellbreaker \
      --seed 106223 --at 46.02 --window 12.41 --end-at-window --fps 60 --w 540 \
      --out ../07-shorts/v106/exsanguinate-window.mp4

The clip runs 13.4s at 60 fps, 540x960: the window and the snap, and nothing after
(`--end-at-window`). Its match state at the end is the headless fight's to the digit: hp 276.65 /
237.425 at 58.4417 (`runs/stage6/snapcheck_spellbreaker.txt`, which also puts the close at 56.633
with the shells 255 apart).

**Audio:** AAC 48 kHz stereo, mean -22.6 dB, max -2.7 dB, integrated -20.8 LUFS
(`runs/stage6/clip_levels.txt`). The drips are in the mix. In the band where count 4 lands (E6, 1358
Hz ± 25), a rough onset count (+8 dB over the band's running median, +6 dB over a reference band where
no count lands) finds none in the 1.2s before the cast, 41 in the window's 10.4s of video, and 3 in the
tail. Count-2 drips slide through that band too, so the count is not the drip count.

**Five frames**, checked by eye (`05-reference/v106/exsanguinate-window-5frames.png`); the art renders
through the pipeline:
- **frame 76 (match 47.3):** her shell flushed dark;
- **frame 112 (47.5):** the director's cast zoom, the banner's letters filled red, her first "+1";
- **frame 216 (48.7):** the thread from Spellbreaker's underside to her rim, "+1"s rising, the banner
  settling;
- **frame 432 (52.3):** the thread through a hit stop;
- **frame 696 (56.7):** THE SNAP, the break at the middle with its strands and drops. Frames 692-699
  show it tearing and the halves whipping home.

**Frames 71-100 also show the nova's particle burst** at the cast: a white flash of particles over the
foe that falls away as a red spray (re-checked by eye on frames 76, 84 and 92 of both clips). That is
`SPECS.widowmaker`, still in this link's inlined `fx.js` until the carry's `fx_remove` (§5b). A
render_ab of this link against a scratch copy with only those three lines out and the stamps re-cut
(`sc-widowmaker-b1075-fx-specout.html`, `3d16bbc543e74c18`; its module sha is the picture lab's
`f710f845485543b6`) differs at 47.3, 47.4 and 47.6 and nowhere else. Its other 7 frames are
identical, Paradox's included (`runs/stage6/render_ab_specout.txt`). **The delivered look, the same
window filmed on that copy, is `07-shorts/v106/exsanguinate-window-specout.mp4`**. That is the one to
judge the picture by. The two clips differ only in the burst.

The delivered-look clip is the same command with `--game <scratch>/links/sc-widowmaker-b1075-fx-specout.html`
and `--out ../07-shorts/v106/exsanguinate-window-specout.mp4`:
- 13.4s, 804 frames, the same end state;
- no spray at the cast (its five frames: `05-reference/v106/exsanguinate-window-specout-5frames.png`);
- AAC mean -22.6 dB, max -0.4 dB, integrated -20.8 LUFS;
- the same drip audit: 0 onsets before the cast, 38 in the window.

The two renders' peaks differ (-2.7 against -0.4 dB) because the synth's noise draws Math.random on
every render. The mean and the loudness are the same.

**Not this build's:** the cast banner is drawn at the caster, and here she casts near the arena's left
edge, so its first letter is cut ("xsanguinate") until it settles. That is the shared banner's
placement, the same for every relic.

## 6. What is left, and whose

- **Rick:**
  - **§6.1, his veto** ("this is his first relic's ultimate"). The standing ruling settles it: no
    vetoes. The build went ahead on the design as written.
  - **§6.2, the blade target.** Built to the shipped rate, 10.75 (47.0% against 46.7), as §3 and §5
    say. The band's 50 is 11 (49.2%): one number in the builder, already built in scratch
    (`variants/sc-widowmaker-b11-alt.html`, 1a805fe1de1d531b).
  - **§6.3, the drain also lifting "her own cap (Bloodletting's 8)".** That cap is the hemorrhage
    stack ceiling, not her maxHp. It is left out, as the design leaves it: not priced, and a second
    payoff on one ultimate. **Her foe's bleed ceiling stays at hemorrhage's 4 and the drain lifts
    nothing.** The probe's [9] holds that from the definition, and its mutant (the review's R63: the
    ceiling at 8 while she drains) fails [9] alone. That mutant also shows what the option would do:
    on the probe's 222 fights (3 seeds) she wins 68.0% and drains 31.4 hp a cast, against 50.5% and
    23.7 on the same fights without it (`runs/probe_mut9_R63.txt`, `runs/probe_b1075_3seeds.txt`).
    That is a second payoff worth about +18 points. If Rick wants it, it is a design question for a
    lab first.
  - **The type spread (item 12/32).** At 10.75 the types run from warhammer 55 and bow 53 down to
    twinblade 36; the shipped nova ran 44-50.
  - **Stage 6's picks, all his to overrule:**
    - the clip (one per ultimate): `07-shorts/v106/exsanguinate-window-specout.mp4`, the delivered
      look. `exsanguinate-window.mp4` is the same window on the stage-6 link as built, with the
      nova's burst still at the cast. Also the choice of foe (§5f);
    - the picture (§5a) and the sheet;
    - the thread drawn only while the foe bleeds (a window with an unbleeding foe shows only the flush
      and the banner);
    - the snap at the verdict;
    - no `fx.js` field (§5b);
    - `ULTSIG` kept;
    - the inhale (MID; SIP-H the near-tie);
    - the drip (TRI; LOW the swap if Coldiron's anvil sits too close);
    - the silent close.
- **The orchestrator (ALL DONE at the carry, §7):**
  - **The carry**, one relic at a time: `widowmaker_build.py --stage 1, 2, 5, 6 --src <tip>`, each
    proved by engine_ab on the others. Then `tools/fx_remove.py --relic widowmaker` takes the nova's
    field out of both `fx.js` copies. **Mind the NOVAS header** (§5b): `fx_remove` takes the comment
    above the entry, and that comment heads Lightkeeper's and Censer's entries too.
  - **shell_identity** on the carried stage-6 link. It was not run here, because the app's json is
    shared.
  - **The app pointer** waits for Rick. It is not this build's to move. The build of record is yert's
    staff row (`sc-nightglass-fx`).
  - **A stage-5 carry** still plays the nova's fang burst (at 300 px) and its wet slice on a cast that
    resolves nothing (reading 8). Stage 6 must follow it before any clip is cut from a carried tip.
- **Watch in the app:** the drip's cost (§5c). About 10,700 synth calls a fight, all in live play; the
  shorts render audio offline. If the app stutters in Widowmaker's windows, the fix is a voice round.
- **Standing, not this build's:** the two verify clock bands, red on every link since the minute pace;
  Heartwood's two 0/40 pairings (the base's own reds).

## 7. The carry onto the chain, and the nova's field spec out

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Lodestone with the
same builder, one stage at a time (`--src` the previous link), and one more link that takes the
retired nova's particle field out:

```
sc-lodestone-b205-fx.html          the batch line's tip (Lodestone stage 6)       4568c2995d06f696
  -> sc-widowmaker-stub.html        stage 1                                        614fea683577bbdc
  -> sc-widowmaker-drain.html       stage 2                                        13f7129b0695bb1f
  -> sc-widowmaker-b1075.html       stage 5                                        64a93517c317fe38
  -> sc-widowmaker-b1075-fx.html    stage 6                                        94875b2b314c5625
  -> sc-widowmaker-fxout.html       SPECS.widowmaker out of both fx.js copies      04fdd2e2daa17c26
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail (redesigned on the chain since), n=6: **3996/3996 identical** (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-lodestone-b205-fx` against the carried stage-6 link, every relic on the
  tip but Widowmaker (39), n=6: **4446/4446 identical** (`runs/carry_engine_ab_tip.txt`): the redesign
  moves no other relic's fight on the batch line.

**The nova's field spec out: `tools/fx_remove.py --relic widowmaker`** -- the three lines of the entry
only. The comment above it is the section header `/* ---- NOVAS: a burst that does NOT fall ---- */`,
which heads Lightkeeper's and Censer's entries too, and stays (the tool leaves a `/* --` header since
92ffe3a; in scratch its output equals this build's spec-out link 3d16bbc543e74c18 byte for byte).
**fx.js 8bf7db5ceb2685a0 -> bb57bd38ca475650** (`runs/fxout/fx_remove.txt`).

**Gates on `sc-widowmaker-fxout`** (`runs/fxout/`):
- engine_ab against `sc-widowmaker-b1075-fx`, all 40 relics, n=6: **4680/4680 identical**;
- render_ab: the other relics' four pairs **24/24 identical**; **the control, Widowmaker v Spellbreaker
  106223 through the cast (47.25-47.65s), 0/5 identical** -- the burst is gone;
- **the probe, 12/12, after one fix to its model** (below);
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold;
- **shell_identity 200/200** (app Chromium 152 vs headless 151; the json restored).

**The probe met Coldiron on the chain.** On the carried link it first read 11/12: [5]'s clank model
(her side of every bind, from the two rows' masses) failed 207 clanks, her stun and knock about 1.85x
the model's (`probe_fxout.txt`). The engine's clank mass is `w.mass * massMul`, and `massMul` is 1 on
every fighter but a Coldiron inside its Temper (v103), which the scratch base did not have. The probe
now takes the engine's rule, row mass times `massMul`, and ALSO fails if her own `massMul` is ever not 1
(the original is kept: `widowmaker_probe_before_massmul.py`). With it: **12/12 on the carried link**
(`probe_fxout_massmul.txt`: clanks 6212 in the window, 6204 out), **12/12 on the scratch link, every
line unchanged** (`probe_scratchfx_massmul.txt`), and **a mutant that multiplies her clank mass by 1.2
in the engine fails [5] alone, 11/12** (`probe_mut_clankmass.txt`). No check was loosened.

**The clip, re-filmed on `sc-widowmaker-fxout`** (the §5 command, `--game` the carried link):
`07-shorts/v106/exsanguinate-window.mp4` (sha16 141b65945310da54, 2.74 MB, 13.4s, `runs/fxout/clip.txt`),
the cast without the burst.

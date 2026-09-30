# v114 — GORESHARD / BLOODPRICE (REDESIGN), BUILD. STAGES 0-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-heartwood-fxout`, the old beam's field spec out of both `fx.js` copies: §7) (stages 0-5 fixed after the build's review, 2026-09-30): stage 1 is arm A fight for fight (2640/2640 fights, every field); the price is the design's, blow for blow, and hers alone (probe 10/10 on stages 2 and 5 and on the batch line's tip: every one of 7,580 window blows rebuilt from its own draws at x(1 + 0.3 x the stacks it found), the log at x1.00 / x1.60 / x2.20; under the new check [10], none of the other attackers' blows (about 9,700 a link) is priced or touches her window; eleven mutants, each caught by its own check alone, the review's R2 by [10]); the built relic reads 1.4 over the lab's arm B on four blocks (1.0 SE), and the two clocks account for it: on the lab's window and the lab's cast the build reads the lab (43.1 against 44.4), the engine's window is worth +4.9 and the cast's common 0.08 stop -2.2 (§2); **THE BLADE IS 10.25, THE MEASURED POINT NEAREST 50% BOTH SIDES: 50.2%** (Rick's 2026-09-29 ruling), where the design's own "confirm 9.17" reads 43.2 and the shipped beam 35.3 on the same fights. Gated: engine_ab on the 37 others 3996/3996 identical; verify 10/13, the base's own three reds (Goreshard 50.1% there, the beam 35.8%); tip_audit the base's; **chain_audit 9/9, the damage-line clause now among them** (`PRICE_CLAUSE_NEW`; the first audit read 8/8 and never saw it), with controls that lose all nine and the clause alone; the builder re-applies on six later tips. On disk `SPECS.oathwound` is the FIRST entry under "BEAMS AND BOLTS", so the header stays at the carry (§0, corrected). **Stage 6, the picture and the voice, is built (`sc-goreshard-b10.25-fx`, §5):** thirteen rows byte-exact to the two labs'; for the window the blade runs arterial red from the guard to the point in 0.3 s, its glow climbing 0.2 -> 0.8 with the foe's Hemorrhage, blood motes dripping off the barbs, a priced blow's float drawn x(1 + 0.1 n), and the red draining back in 0.35 s at the close; a wet drawn-blade hiss at the cast (a scrape rising 2.6 -> 8 kHz, drops off the blade), a priced blow's strike a semitone lower a stack, and nothing at the close; the beam's pool, seam and sigil retired, and no `fx.js` field (the motes are drawn; `SPECS.oathwound` is the orchestrator's to take out of both copies at the carry, tried in scratch). engine_ab 4218/4218 over all 38 relics with Goreshard in; the probe 12/12 on the fx link, its [1]-[10] the stage-5 link's number for number, its two new checks ([11] the voices, [12] the picture's hook, 74 fights drawn, 13,669 frames) each failed by its own mutants (7/7); render_ab 24/24 with a control at 0/6; chain_audit 22/22 with controls; stages 1-6 re-apply on seven later tips, the batch line's newest among them. The clip is with Rick (5g); the carry and shell_identity are the orchestrator's.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`, the BUILD row under the
redesign's), built 2026-09-30. Input: `06-docs/v81/goreshard-bloodprice-redesign-v81.md` (§5 its build
brief) and its runs, and nothing else (rule 0). Builder `tools/goreshard_build.py` (sha16
eddeef420792bf7f, with stage 6; 7f2f86d2a87b7aa3 before it, and b6fa8226dc291099 before the review's fix, which
names the damage-line clause; every one writes the same stage 1-5 links byte for byte), probe
`tools/goreshard_probe.py` (a9c3cf33c7b141e9, with [11]-[12]; bc2d8226432bf69c before them, 4031e3fbffd117db before
[10]), the clip's picker `tools/_goreshard_pick.py` (8714d41fb8042b52), runs in `runs/` (the scratch tools that made
them are copied there too). **A REDESIGN, not a new relic:** Goreshard ships in the base
(id `oathwound` -- the roster's id/name mismatch; every tool here reads the name from the build); its beam
is replaced, and the roster stays at 38. Chromium 151.0.7922.34, Python 3.13, playwright 1.62.

```
sc-tendril-t3.html              the base: the chain tip (Bindweed stage 5)                    5a6216e3b629fad4
  -> sc-goreshard-stub.html      stage 1  the beam out, the price's block in, stubbed (1e9)     5dac38065e1c8ac3
  -> sc-goreshard-price.html     stage 2  the price, charge 14 (the design's stage 1)          9105fa5bb4cf258c
  -> sc-goreshard-b10.25.html    stage 5  the blade, 9.17 -> 10.25 (the design's stage 2)      8eb3c1634184c1bd
  -> sc-goreshard-b10.25-fx.html stage 6  the picture and the voice (the design's stage 3)    f063e05c0f721d54   THE FINAL LINK
```

**Built in scratch, not on the chain** (`<scratchpad>/batch/goreshard/links/`). Several batch builds run in
parallel on `sc-tendril-t3`; the orchestrator carries each onto the real chain one relic at a time,
rebuilding it with its builder `--src <tip>` and proving the carry with engine_ab. The builder rebuilds all
four links byte for byte from the base, and re-applies on six later tips (§1; seven with stage 6, §5). No link name is on
`02-chain/`. The stage numbers are the builder's: its stage 2 is the brief's stage 1 ("beam out, the
multiplier in"), its stage 5 the brief's stage 2 (the blade). There are no stages 3-4: the design has one
mechanism stage. The brief's stage 3 (picture, voice, carry) is the batch's stage 6 (§5), built here too.

## 0. What this build stands on

- **The relic** is Goreshard as shipped (the donor is itself): the bloodsworn greatsword, reach 116, width
  14, artW 40, spin 3.4, mode "swing" with arc 1.5, mass 3.0, blades [0], onHit hemorrhage 2, blade 9.17
  until stage 5. The builder asserts, by content and never by which relic is last:
  - that row (and, for stage 1, the shipped beam block);
  - `STATUS.hemorrhage` at maxStacks 4 and dps 1.5, and `Fighter.stacks` as the status reader;
  - resolveHit's crit draw, jitter draw and damage line, in that order, ahead of its onHit loop;
  - its six anchors, each exactly once.
- **The charge is 14.** The design states none; its lab cast every 16 s of its own step clock
  (`ult_overlay`'s default), converted under Rick's batch ruling. Measured for this fighter on arm B with a
  census copy of `bloodprice.js` (`runs/price_freeze.js`), which counts, before each lab step, whether the
  step is frozen (`hitStop > 0 || latch || splitHold`), over 660 fights a block (`runs/s0_census_B_*`):
  **13.06% / 13.06% of the lab's steps are frozen (14.93% / 14.87% inside windows, 11.80% / 11.82%
  outside), so the lab's 16 is the engine's 13.91 / 13.91, which rounds to 14.** (The beam also shipped at
  14.) The census copy is inert: it reproduces arm B's win rate and blow counts on both blocks.
- **The lab is `ult_overlay.py --mech overlays/bloodprice.js`** (the brief's own stage-0 command, `--arms
  A,SHIP,B --P perStack=0.30`), side A, the design's 33 foes (the 34-relic roster without the donor).
  **One lab default differs from the settled number, and it is flagged:** `perStack` defaults to **0.12**
  (the design's first arm, "+12% a stack", 30.3%), not the settled **0.30** ("(taken)"). Every run here
  passes `perStack=0.30`, as the brief's command does. `extraBleed` (default 1) is read only by arm C, which
  the design rejected ("the extra bleed is +0: the cap is 4 and 2 a hit fills it"). Charge 16, window 8 and
  the shipped blade 9.17 are the harness's defaults, as priced.
- **What is retired, and what is not.**
  - Stage 1 deletes Goreshard's beam block from its row: dmg 16, apply hemorrhage 3 and its card ("beam
    out").
  - `kind:"beam"` has no cast branch of its own: it resolves in `fireUlt`'s generic tail, which every
    non-returning kind shares. Aureole's Benediction is still a beam on this base. The builder reads who is
    still a beam and never refuses on it. On the batch line Aureole's redesign has already taken her off it,
    and there (compose tips (a) and (b), §1) Goreshard was the last `kind:"beam"` row, so no ultimate of
    that kind is left after the carry. That is the kind only: the SPECS field mode `'beam'` (Farwarden's and
    Marrowdraw's entries) and the bolt's `B.phase = "beam"` are other things of the same name, and stay. The
    generic tail stays for the kinds that use it.
  - **The beam's picture, voice and field are NOT retired in stages 1-5.** They are keyed on the relic, not
    the kind: the charge sigil `ULTSIG.oathwound` ("a beam, and the toll paid under it"), `drawUltUnder`'s
    pool and `drawUltOver`'s seam (`u.w === "oathwound"`), the ultFx `life` entry (1.5), the cast voice
    (Goreshard has no `ult` arm and falls through to the shared rune-crack) and `SPECS.oathwound` in both
    `fx.js` copies. The design retires the art at its stage 3 (our stage 6): **stage 6 retires the pool,
    the seam and the sigil and gives the cast its own voice (§5); the field goes at the carry (5b).** Nothing in
    the simulation reads any of them. The beam had no `radius`, so fireUlt's ultFx record is exactly as it was.
  - **For the carry** (corrected after the build's review of 2026-09-30; this doc's first version had it wrong): on disk,
    `src/render/fx.js` (which follows the batch line; read 2026-09-30) holds `SPECS.oathwound` as the
    **FIRST** entry under the "BEAMS AND BOLTS" header (L133), straight after that section's two-line note
    "Negative gravity is what stops a beam reading as an explosion pointed sideways." (L134-135). Three
    entries follow it under the same header before the FIELDS header (L157): `'axiom-echo'` (mode
    `'burst'`), `farwarden` and `marrowdraw` (both mode `'beam'`). Aureole's and Spellbreaker's entries,
    which stood either side of it in the base's inlined copy (aureole, oathwound, spellbreaker, 'axiom-echo',
    ironhail, farwarden, marrowdraw), are already out on disk, and Ironhail's too. The entry's exact text
    (disk L136-138, the base's inlined copy L32242-32244, the final link's L32292-32294) is:
    ```
        oathwound: { mode: 'beam', n: 1250, sp: [25, 140], grav: -60, drag: 1.3,
                     life: [0.40, 1.00], heavy: 0.0, size: [0.7, 2.0],
                     spawn: 0.50, up: 0 },
    ```
    **Taking it out keeps the header**: three entries still stand under it, so the header must not go.
    Only the two-line "Negative gravity" note loses its subject: it was written for the negative-gravity
    beams (Aureole -120, Goreshard -60, Spellbreaker -40), and after Goreshard's entry goes no
    negative-gravity beam is left (Farwarden's and Marrowdraw's gravity is +120 and +150; 'axiom-echo' is a
    burst). That note may go with the entry. Both calls are the orchestrator's at the carry.
- **Readings** (all twelve in the builder's docstring; stage 6's nine more, 13-21, are in §5a):
  1. **The window is 8 s.** §1 says "for a duration" and names no number; the lab ran `ult_overlay`'s
     default window, 8, and that is what was priced.
  2. **The stacks are the struck fighter's, read at the blow, before its own onHit.** §4 is explicit:
     `foe.stacks("hemorrhage")` in `resolveHit`, "read BEFORE this blow's own application (the blow pays on
     the stacks it found, then bleeds)". The lab set `w.dmg` at the end of the previous step from the
     opponent's stacks. The two differ only where (a) the foe's bleed expires in this step's `tickStatus`
     before the blow, or (b) the blow lands on a Twinshade shade, which pays on its own stacks (the lab's
     `w.dmg` carried the opponent's): 34 of 3,907 window blows in the probe's stage-2 run.
  3. **The multiplier sits inside the product**, on the blade itself, ahead of the jitter, the crit and the
     rounding -- where the lab scaled `w.dmg` -- so a blow is bit-identical to the lab's for the same count
     (the tree's line, v99 reading 3). The curse echo and a garrote's consume are not scaled; they were not
     in the lab either.
  4. **The shared weapon is never written.** The lab wrote `w.dmg` every frame; `w` is shared by the mirror
     match. The builder refuses any insert that writes it, and the probe's [8] reads the row after every
     step and at every blow.
  5. **The window closes by its clock or on a death that `tickPrice` sees** (the lab's close is either
     death). A kill landed later in the same step (a blow in `tickHits`, after the window tickers) ends the
     match with the window still set: `step` runs no ticker after `over`, and nothing in the simulation
     reads `ultPrice` then. It is 226 of 1,489 windows in the final link's probe run. A picture drawn off
     it must stop at `over` (§5).
  6. **No wait clause.** Charge 14 against a window of 8 on one clock cannot overlap. The probe's [7]
     asserts it, and that every cast comes exactly 1681 steps (14.008 s) of the caster's live clock after
     the last. It pins 14 and 8 from the builder, never from the row it tests.
  7. **The card is written at stage 1**: the stub is the new block, and the beam's card would describe a
     cast that is gone. `Its blows hit harder the more the foe bleeds: +30% a Hemorrhage stack` is 69
     characters (§4 prints "(69)").
  8. **The beam's picture, voice and field still play at the cast in stages 2-5** (above); stage 6 retires
     the picture and the voice, and the orchestrator the field.
  9. **Every blow of the caster's takes the multiplier**: whatever reaches resolveHit's damage line with
     its window open, as every read of the lab's `w.dmg` did. Goreshard has no projectile, so these are its
     melee blows, on the opponent or on a shade (the probe fails any blow of hers with a `mul`). No other
     attacker's blow takes it, in her window or out (the probe's [10]: "every blow GORESHARD lands").
  10. **Nothing else**: no status, no stop, no beat, no float, no knock and no heal of the price's own. A
      priced blow is an ordinary blow: its knock, hitstun and stop are the engine's rules applied to its
      damage, as they were to the lab's scaled `w.dmg`. The cast keeps `fireUlt`'s common banner, 0.08 stop
      and ult beat, and resolves nothing.
  11. **The price lifts no cap.** §1 prices "cap 4 -> up to +120%"; §6.3 (whether Bloodletting's cap of 8
      applies too) is "not priced; two payoffs on one ultimate". The build takes §1's 4: hemorrhage's own
      `maxStacks`, untouched. The probe's [3] holds the struck fighter's ceiling at 4 at every blow; its
      mutant (the ceiling 8 while she prices) reads 64.0% against the build's 50.9% on the same 222 fights
      (§3). Flagged for Rick.
  12. **The blade is for balance** (Rick, 2026-09-29, after the design was written: "you pick the blades.
      do whatevers best for balance."): the measured point whose win rate both sides is nearest 50%. This
      replaces §5's "confirm 9.17 wide on 151 or nudge to the shipped rate at Rick's word" (and open
      decision 2, "42 or the shipped 38"). The design's own 9.17 and the shipped rate are measured beside
      it (§4).
- **Names:** kind `"price"`, fields `ultPrice` / `priceTally`, ticker `tickPrice`, and the local `priceN`.
  All are free on the base, on the batch line's tip and in every builder in `tools/` (grepped on identifier
  boundaries).
- **The clock:** the window runs on the window tickers' clock, which stops in a hit stop. The lab's window
  ran 8 step-seconds, frozen ones included (§2).

## 1. Stages 1, 2 and 5 (stage 6: §5)

Stage 1 replaces the ult block of Goreshard's row with the price's block at charge 1e9. The clock never
reaches it and `fireUlt` never runs, so it is the lab's arm A.

Stage 2 (the design's stage 1: "beam out, the multiplier in") sets charge 14 and adds:
- **the fields** `ultPrice` / `priceTally`, after `this.vineTally = null;`;
- **the read**, after resolveHit's jitter draw: `const priceN = self.ultPrice ? foe.stacks("hemorrhage") :
  0;` and the tally's two counts. It sits after both of the blow's draws and before its onHit loop;
- **the price**, one clause inserted in the damage line after the tree's: `self.ultPrice ? self.w.dmg * (1 +
  self.w.ult.perStack * priceN) : ...`. The Angelus build on the batch line inserts its own clause at the
  same place; the two read the same in either order (the compose check below). The clause is declared as
  the module constant `PRICE_CLAUSE_NEW` (`PRICE_LINE_ANCHOR + '''...'''`), so that `chain_audit` audits
  it. It is a partial line, and `chain_audit`'s table pass skips an insert with no newline, so the first
  build's audit never saw the one insert that IS the mechanic (the build's review found it; §4);
- **the cast**, `kind === "price"`, before `kind === "tendril"`: `{t: 0, dur}` and return, before the
  generic tail (no damage, no status);
- **`tickPrice`**, after `tickTendril` (before `tickWinnow`): `t += dt`, the close on the clock or on a death
  it sees (reading 5), and the probe's window-frame counts.

Stage 5 moves the blade, 9.17 -> 10.25 (§4). It is one field of the row.

Every insert is anchored exactly once. Each strips clean (comments out, its re-emitted anchor out) of the
RNG, `spawnFx`, `ultFx`, any write to the shared weapon, `hitStop`, a beat, a float, an SFX, a status tag,
and every call but `stacks` and the ticker's own. The only writes it may make are the window, the tally's
counters and the window's clock (`WRITE_OK`); it may not rewrite the blow's own locals (`dmg`, `crit`,
`jitter`, `stop`) or write by index. The builder also checks that the read, the damage line and the onHit
loop are in that order, and that the read and the clause are there exactly once. `node --check` parses the
page, and the page is written LF.

**The refusals** (`runs/builder_refusals.txt`, `refusals.py`), all twenty refuse:
- seven guards: stage 2 on the base, stage 1 on the stub, stage 2 twice, stage 5 on the stub, an existing
  link, a name that is not `sc-goreshard*`, the live build's name;
- **thirteen negative copies of the builder**, each with one insert made wrong:
  - a foe velocity write in `tickPrice`, a stop in `tickPrice`, a `hurt` from `tickPrice`;
  - an RNG draw, a float, a heal, a status written by index, or the jitter rewritten, in the read;
  - a shared-weapon write, the beam's bleed kept (an apply), or a stun, at the cast;
  - the read moved below the damage line (after the onHit), and the clause written twice.

**It re-applies on later tips** (`runs/compose_check.txt`, `compose_check.py`): stages 1 / 2 / 5 on six tips,
every anchor found once, every page parsing, and the same added and removed lines in the same order as on
the base:
- (a) the batch line's tip now, `02-chain/sc-spellbreaker-fxout.html` (Spellbreaker carried, 42 relics, no
  other beam), read only;
- (b) Aureole's carry `sc-aureole-fxout` (Benediction off the beam) and (c) Widowmaker's `sc-widowmaker-fxout`;
- (d) Bindweed's stage 6 `sc-tendril-fx`;
- (e) Heartwood's and (f) Thornwake's scratch links, the two redesigns in flight beside this one.

On (a) and (b) the damage line already carries Angelus's clause. The price's clause goes in after the
tree's, and the line is otherwise the tip's own; the check reads it as that one edit. **The probe reads 10/10
on the final composed onto (a)** (492 fights against 41 foes; `runs/probe_on_batch_tip.txt`): 3.43 casts,
2.42 priced blows a cast, x1.72, 15.1% of window steps frozen.

## 2. Stage 0 and the stages against it -- the two clocks, measured

The lab command is `ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic oathwound --mech
overlays/bloodprice.js --arms A,SHIP,B --P perStack=0.30 --seeds 20 --foes <33>`, on seed0 2207 and 2317,
660 fights an arm a block. The built links run `--arms SHIP` on the same foes and seeds, with the same seed
formula and side.

```
                               lab on 151 (1 / 2)   published 141   BUILT (1 / 2)              pooled
A    no ultimate               17.9 / 18.0          20.0            stage 1: 17.9 / 18.0       identical, fight for fight
SHIP the beam as shipped       39.4 / 39.8          37.6
B    the price, perStack 0.30  43.3 / 43.3          42.4            stage 2: 46.4 / 45.8       46.1 (lab 43.3)
```

- **Published vs 151.** The design's own runs replayed on 151 (10 seeds, seed0 2207, 330 fights an arm,
  `runs/pub151_*`), each against its published number:

  | arm | 151 | published 141 |
  |---|---|---|
  | A | 17.0 | 20.0 |
  | SHIP | 37.9 | 37.6 |
  | B at 0.12 | 27.0 | 30.3 |
  | C | 33.3 | 29.7 |
  | B at 0.25 | 39.1 | 35.5 |
  | **B at 0.30** | **43.6** | **42.4** |

  The runtime moved (141 -> 151), and so did the base (`sc-trunk` -> `sc-tendril-t3`, which redesigned
  Axiom and Dawnbringer among the 33 foes). At 330 fights a standard error is 2.7 points. The settled arm
  reproduces (+1.2), and the lifts keep their order: SHIP +20.9 and B +26.6 over A, against the published
  +17.6 and +22.4.
- **Stage 1 is arm A fight for fight** on both blocks:
  - every foe's rate and the blow count are identical (`runs/built_stub_*`);
  - every field of `AC.simulate`'s summary is identical on all 2640 fights (33 foes x 20 seeds x 2 blocks x
    both sides; `runs/stub_vs_A.txt`, `stub_vs_A.py`);
  - the control, the base with the beam live, differs on 2640 of 2640.
- **Lab mechanism on 151 (arm B, the census):** 3.46 casts; 7.71 blows in windows and 9.97 / 9.91 outside;
  2.15 / 2.16 blows a cast; the foe at 2.36 / 2.37 stacks on a window frame; **a window blow priced on 2.39 /
  2.37 stacks** (x1.71).
- **Built (the probe, stage 2, both sides, 444 fights):** 3.45 casts; 2.55 priced blows a cast; the foe at
  2.26 stacks on a window frame; **a window blow found 2.35 stacks (x1.70)**; 15.2% of window steps frozen;
  a window is 960 steps of the window clock and **9.34 s of match time**.

**The mechanism is the lab's; what differs is the clock.** The probe shows every window blow paying exactly
x(1 + 0.3n) on the stacks it found (§3), and a priced blow finds the same stacks as the lab's (2.35 against
2.39). Two blocks put the built relic 2.8 over arm B. Four blocks, with controls, take the gap apart. Side A,
the same 33 foes and seeds; seed0 2207 / 2317 / 2427 / 2537; 2640 fights a row (`runs/gap_table.txt`,
`gap_table.py`; the scratch variants' makers are `make_matchclock_variant.py` and `make_nostop_variant.py`):

```
                                                             2207   2317   2427   2537   pooled
lab B: 8 step-seconds, no cast stop (the design's arm)       43.3   43.3   45.6   45.5    44.4
lab B with fireUlt's 0.08 cast stop                          46.4   46.7   42.6   40.0    43.9
lab B at the engine's window: 8 / (1 - 0.149) = 9.40 s       46.4   46.7   47.4   48.3    47.2
BUILT, the lab's window AND the lab's cast (no 0.08 stop)    42.6   43.0   43.3   43.6    43.1
BUILT, its window on MATCH time (the lab's 8 s)              41.1   41.4   39.7   41.5    40.9
BUILT stage 2: 8 s of the window clock                       46.4   45.8   43.6   47.4    45.8
```

The standard error of a difference between two of these rows is 1.4 points.

1. **On the lab's window and the lab's cast, the build reads the lab**: 43.1 against 44.4 (-1.3, 0.9 SE).
   This scratch variant has its window on match time (`Z.t = this.t - Z.t0`: the lab's 8 step-seconds) and
   no 0.08 stop at Goreshard's cast. The lab's harness never froze the world at a cast. Everything else is
   the built link.
2. **The engine's window is worth +4.9** on the build (the window clock against match time: 45.8 against
   40.9, 3.6 SE) and +2.8 on the lab (lengthened to the engine's 9.40 s: 47.2 against 44.4, 2.0 SE). The
   engine's 8 s are 8 seconds of the window tickers' clock, which stops in a hit stop. At 15% of window steps
   frozen, a window is 9.34 s of match time, and it holds more blows: 2.55 priced blows a cast built,
   against 2.30 on the match-clock variant and 2.15 in the lab.
3. **The cast's common 0.08 stop is worth -2.2 on the build** (40.9 against 43.1, 1.6 SE) and -0.5 in the
   lab (0.4 SE). Every built cast carries it, `fireUlt`'s common head. It is a foe-specific effect.
   Farwarden, Nightfell and Shroudmaul fall 16-33 points with the stop in the lab too (81.2 -> 62.5,
   70.0 -> 53.8, 55.0 -> 22.5, 80 fights a foe), and other foes gain.
4. **Net: the built relic reads 1.4 over the lab (45.8 against 44.4, 1.0 SE)**, and 1.4 under the lab run
   at the engine's window (-1.0 SE). The first two blocks alone said +2.8; two more halve it.

Nothing is mis-built. The build keeps the engine's convention and every designed number: every window cadence
runs on the window tickers' clock (Corollary, Daybreak, Zenith, Canopy, Onslaught, Tendril, Exsanguinate), a
freeze freezes the world, and every cast carries `fireUlt`'s common stop. Stage 5 settles the blade on the
built relic, wide, both sides.

## 3. The probe (`goreshard_probe.py`, one check per sentence, read inside the hooks)

The probe wraps `step`, `fireUlt`, `tickPrice`, `tickCharge`, `tickWeapon`, `bladeSegments`, `tickHits`,
`resolveHit`, `resolveClank` and `checkEnd`; around each blow in her fights, hers or another attacker's, the
struck fighter's `stacks` and the attacker's `dmgMul`, which bracket the price's lines; and, for the whole
fight, her `ultPrice` and `priceTally` as watched accessors that record only inside another attacker's
blow ([10]). It runs Goreshard against every other relic, both sides, 6 seeds (444 fights). **The stage is
pinned** (`--stage 2|5`), and the build's numbers come from the builder, never from the row under test: the
window 8, the charge 14 and perStack 0.3 from `ULT`, the greatsword's profile from `SHIP_HEAD`, the blade
from the stage (9.17, or `TUNED`'s 10.25). Ten checks (the tenth added after the build's review of
2026-09-30, whose mutant R2 priced the foe's blows in her window and read 9/9 on the first nine):

- [1] "For a duration", **8 s on the window tickers' clock** (reading 1):
  - the row's `dur` is the build's 8;
  - a frozen step leaves the window exactly as it was, and a live step moves its clock by exactly dt;
  - a clock close comes after exactly the 960 window steps whose dt first reach 8, and a death `tickPrice`
    sees closes the window;
  - every cast is a clock close, a death close, or a window still set at `over` (counted, reading 5);
  - only Goreshard carries `ultPrice` (no shade, no foe).
- [2] **"every blow Goreshard lands hits harder for every stack of Hemorrhage the enemy is carrying",
  `dmg x (1 + 0.30 x stacks)`, "read BEFORE this blow's own application"** (§1, §4, and §5's gate
  "measured multiplier on every window blow = 1 + 0.3 x stacks-before-the-blow (asserted against a
  log)"):
  - every blow of hers with the window open deals exactly `round(blade x (1 + 0.3 n) x act dmg x
    desperation x jitter x Sunder [x critMul])`, plus the foe's curse echo, less what Bulwarden's wall ate,
    rebuilt from the blow's own captured crit and jitter draws;
  - n is the struck fighter's Hemorrhage as its STATUS holds it when the blow arrives (not read through
    `stacks()`), and 0.3 is the builder's; the row's perStack must be 0.3;
  - the n the price read and recorded must be that n;
  - **the log**: the measured multiplier of each window blow (its blade part over the same blow rebuilt at
    n = 0), by n.
- [3] **"then bleeds", and the cap** (§1 "cap 4"; reading 11): every blow's onHit is +2 Hemorrhage after it
  pays, stopped at hemorrhage's own 4 where the ceiling binds; the struck fighter's `bleedCap` is 4 at every
  blow of hers, window open or shut; no window blow is priced on n > 4.
- [4] **"in the window" and nowhere else**: every blow of hers with the window shut is the plain blade
  (the same rebuild at x1), and reads no stacks for a price.
- [5] **the blade is otherwise the shipped greatsword**, in the window and out, every factor rebuilt from its
  definition (readings 3 and 10):
  - the row;
  - **the swing** on every live step (`swingPhase += spin x spinMul x dt x spinDir`, `theta = aim +
    sin(swingPhase) x arc`), held while stunned, and no frozen step moves it;
  - the segment, the hit test and the cooldown;
  - for every blow, priced or plain, what the engine does with its damage: the knock, the foe's hitstun and
    the stop (the wall's 0.05 and a ward shatter's 0.10 where they happen);
  - her side of every clank, from the two rows' masses.
- [6] **the cast resolves nothing** ("beam out"):
  - it may change no field of either fighter (every own number, flag and string, and every status) but the
    window, the tally and the engine's cast count;
  - no RNG draw, and no array of the match but the common ult beat and the note;
  - the common 0.08 stop, and a window {t 0, dur};
  - the row's ultimate may carry none of the beam's `dmg`, `apply`, `radius`, `knock`, `heal`, `freeze`.
- [7] **the charge, 14 on her live clock**: the row's charge the build's 14; every cast exactly 1681 steps
  (14.008 s) of her live clock after the last or after the match's start; no fight ends owing a cast; no
  cast while her window is open (reading 6).
- [8] **the shared weapon is never written** (reading 4): every own field of Goreshard's WEAPONS row and of
  its `ult` is what it was when the fight began, after every step and at every blow.
- [9] **the price's own code writes nothing but its window and tally** (reading 10). Read across every
  `tickPrice` call while a window is open or closing (and one in 16 of the rest), and across the price's read
  inside `resolveHit` (from the struck fighter's Hemorrhage read to her `dmgMul` on the damage line):
  - every own field of both fighters, every shade and the match (numbers, flags, strings, statuses, array
    lengths), and the RNG;
  - in `tickPrice` only the window's clock, its close and the tally's frame counts may move;
  - in the read only the tally's blow counts may move.
- [10] **"every blow GORESHARD lands": the price is hers alone.** In every other attacker's blow in her
  fights (the foe's, or a Twinshade shade's; her window open or shut):
  - no read or write of HER `ultPrice` or `priceTally` anywhere inside that `resolveHit` (both are
    accessors on her that return exactly what the field holds and record only while another attacker's
    blow is resolving, so no fight moves: the stage-2 run below is the first run's, number for number);
  - no read of the struck fighter's Hemorrhage between the blow's second draw and the attacker's
    `dmgMul` on the damage line, where the price's read and clause stand. No other attacker reads
    Hemorrhage there on this engine: the garrote's consume is below the damage line;
  - coverage: other attackers' blows that reached the damage line, with her window open and with it shut.

**Results** (the probe with [10], sha16 bc2d8226432bf69c). Every number of checks [1]-[9] below is the
first run's, line for line, on every link: the watched accessors move no fight.
- **sc-goreshard-price (stage 2): 10/10** (`runs/probe_price.txt`):
  - 3.45 casts; 8.80 blows a fight in windows and 9.06 outside; she wins 50.0% of the probe's fights;
  - 2.55 priced blows a cast; the foe at 2.26 stacks on a window frame; a window blow found 2.35 (x1.70);
  - 1530 windows: 1239 closed by the clock, 58 on a death, **233 still set at `over`**; 9.34 s of match time a
    window; **15.2% of window steps frozen** (the lab's census: 14.9%);
  - every one of the 1530 casts came 1681 live steps after the last;
  - **the log**: n 0: 1200 blows at x0.9996; n 2: 830 at x1.5996; n 4: 1877 at x2.2002. That is the
    design's x1.00 / x1.60 / x2.20; the residue is the rounding.
  - 2707 blows at n > 0 dealt more than the plain blade, and 2030 would have been priced otherwise on the
    stacks the blow leaves, so the read before its onHit is load-bearing. Odd counts do not occur: the blade
    applies 2 a hit and a bleed expires whole;
  - 34 window blows landed on a Twinshade shade and paid on its own stacks (reading 2); 37 carried a foe's
    rule (a curse echo or Bulwarden's wall); 3973 shut-window blows rebuilt plain;
  - the swing rebuilt on 2.49 million live steps (413,289 stunned and held) and held on 442,849 frozen ones;
    the knock, hitstun and stop of all 7,928 of her blows rebuilt; 11,852 clanks; 462 ward shatters;
  - the shared row unmoved after 3.35 million steps; `tickPrice` clean on 1.32 million window calls and
    98,904 sampled idle ones; the read clean on all 3,907 window blows;
  - **[10], hers alone:** 5,367 of the foe's blows with her window open and 4,210 with it shut, and 51 / 106
    of a shade's, all reached the damage line unpriced, and none read or wrote her window or tally.
- **sc-goreshard-b10.25 (stage 5, the final link): 10/10** (`runs/probe_b10.25.txt`):
  - 3.35 casts; 2.47 priced blows a cast; x1.71;
  - the log: n 0 x1.0009 on 1134 blows, n 2 x1.5986 on 748, n 4 x2.2005 on 1791;
  - 15.1% of window steps frozen; 9.34 s a window;
  - 1489 windows: 1201 by the clock, 62 on a death, 226 at `over`;
  - she wins 53.6% of the probe's fights;
  - [10]: 5,271 of the foe's blows with her window open and 4,238 shut, 42 / 105 of a shade's, all unpriced.
- **The final composed onto the batch line's tip: 10/10** (§1; `runs/probe_on_batch_tip.txt`, 492 fights;
  [10] on 6,101 / 4,736 of the foe's blows).
- **The match-clock variant** (its window on match time, §2) fails [1] alone, 9/10: "a live step moved the
  window's clock by 0.0917, want 0.0083" (`runs/ctl_probe_matchclock.txt`).

**Controls** (`runs/probe_mutants_b10.25.txt`, `mutants.py`, the probe's output for each in `runs/mutants/`):
eleven mutants of the final link, each breaking one sentence, all run in one pass against the probe with
[10]. "Fights changed" is out of 148 (Goreshard v every foe, 2 seeds, both sides); the probe runs each at 3
seeds, where the unmutated link reads 10/10 and she wins 50.9% (`runs/probe_b10.25_3seeds.txt`):

| mutant | fails | fights changed | she wins (3 seeds) |
|---|---|---|---|
| the window 10% long | [1] | 54 | 53.6 |
| the price read AFTER the blow's own onHit (the stacks it leaves, not the ones it found) | [2] | 144 | 59.5 |
| the struck fighter's bleed ceiling 8 while she prices (§6.3's Bloodletting cap) | [3] | 133 | 64.0 |
| the price also with the window shut (after the first cast) | [4] | 141 | 59.9 |
| the blade's reach +10% in the window | [5] | 145 | 56.3 |
| the beam's 3 Hemorrhage kept at the cast | [6] | 144 | 63.5 |
| the lab's charge 16, unconverted | [7] | 148 | 44.1 |
| the lab's method: the shared row's `dmg` written at every blow of hers | [8] | **0** | 50.9 |
| the window's ticker stops the world a little every window frame | [9] | 148 | 59.9 |
| **the foe's blows on her priced too while her window is open, by her own Hemorrhage** (the review's R2: `(self.ultPrice \|\| foe.ultPrice)` in the read and the clause) | **[10]** | 20 | 48.6 |
| the foe's blows on her priced by her Hemorrhage, keyed on her relic (`foe.w.id === "oathwound"`), not her window: no field of hers read | [10] | 20 | 47.3 |

**Each fails its own check and only that one** (11/11). The [8] mutant is the lab's own method made
bit-identical to the build. It changes no fight the probe plays, since the probe never plays the mirror,
where the shared row is the whole of the harm. It is the control that [8] can fail, not a fight-changing
mutant; the other ten all change fights. **The review's R2 read 9/9 on the first probe** (it changes 20
fights, against Bloodmirror, Marrowdraw, Ravelbone, Threshmaw and Widowmaker, the foes that bleed her (`runs/mutants_10_changed.txt`), and
moves her from 50.9% to 48.6%); it now fails [10] alone. Its twin keyed on her relic reads no field of hers,
so the accessor arm cannot see it, and [10]'s Hemorrhage bracket fails it alone: each arm of [10] can fail
on its own. The first nine rows are the first run's, number for number. How the probe catches each:
- [2] on "the price read n 0 and recorded 2";
- [4] on a shut-window blow reading the stacks for a price;
- [6] on "the cast moved the foe's status: [] -> [hemorrhage 3]";
- [7] on "the row's charge is 16" and "a cast after 1921 steps of her live clock, want 1681";
- [9] on "tickPrice moved hitStop";
- [10] (R2) on "dawnbringer's blow on her with her window OPEN touched her read ultPrice" (4,826 fails);
- [10] (keyed on her relic) on "dawnbringer's blow on her with her window OPEN read the struck fighter's
  Hemorrhage 1x between its second draw and its dmgMul" (4,776 fails).

## 4. Stage 5: the blade -- 10.25, nearest 50% both sides

The runs are `relic_rate.py`, both sides: each seed from both sides, every other relic a foe (37), 10
seeds a foe a side, 740 fights a block, seed0 2207 and 2317 (`runs/stage5_rr_*`, `runs/ship_rr_*`;
`runs/stage5_table.txt`). The grid is on stage 2's link with `--set dmg=X`; the shipped row is the base, as
it ships.

```
                                     block 1  block 2  pooled (1480)     side A  side B  mean s
SHIPPED: the beam, 9.17 (the base)     38.2     32.3    35.3 (522)        37.3    33.2    62.5
the price, 8                           30.5     32.7    31.6 (468)        31.4    31.9    63.5
the price, 8.5   (nearest the shipped) 33.9     33.8    33.9 (501)        35.1    32.6    63.0
the price, 9.17  (the design's own)    42.7     43.8    43.2 (640)        43.9    42.6    62.4
the price, 9.5                         45.5     46.1    45.8 (678)        47.4    44.2    62.4
the price, 9.75                        45.4     48.0    46.7 (691)        47.6    45.8    62.2
the price, 10                          49.1     47.6    48.3 (715)        51.5    45.1    61.7
the price, 10.25   <- BUILT            49.7     50.7    50.2 (743)        51.2    49.2    61.3
the price, 10.5                        51.8     49.6    50.7 (750)        52.0    49.3    61.2
the price, 10.75                       55.8     51.5    53.6 (794)        53.8    53.5    61.2
the price, 11                          56.9     57.0    57.0 (843)        56.6    57.3    60.8
```

- **The target is Rick's: the measured point nearest 50% both sides** (2026-09-29, after the design was
  written: "you pick the blades. do whatevers best for balance."). **10.25 reads 50.2%** (743 of 1480; 10.5
  reads 50.7, 10 reads 48.3). It is inside the greatsword row (Axiom 7.42 .. Heartwood 12.65).
- **The design's own target, "confirm 9.17 wide on 151", reads 43.2%** both sides here. The design's side-A
  lab said 42.4; §2's side-A arm B reads 43.3 and the built side A 46.1.
- **Its alternative, "nudge to the shipped rate at Rick's word", goes the other way.** The shipped beam
  reads **35.3%** on these fights, under even the price at 9.17. The crossing of the shipped rate is about
  8.8; 8.5 (33.9) is the measured point nearest it.
- **The shipped relic, as the reference:** Goreshard with its beam at 9.17 reads 35.3% both sides (side A
  37.3, side B 33.2). The redesign at 10.25 is +14.9 over it; at the design's 9.17, +7.9.
- **The design names no knob but the blade** (§5's stage 2), and none moved. perStack stays the design's
  0.30.
- **The built link reproduces the measurement exactly.** `relic_rate` on `sc-goreshard-b10.25`
  (8eb3c1634184c1bd) with no knob set gives 49.7% on block 2207 and 50.7% on 2317. Every foe's rate,
  `byType`, both sides and the mean duration (61.55 s / 61.04 s) equal the `--set dmg=10.25` runs, key for
  key, on both blocks (`runs/stage5_rr_built_*`).
- The mean fight is 61.3 s at 10.25, against the shipped relic's 62.5.
- **The ladder at 10.25** (40 fights a foe, `runs/stage5_table.txt`), beside the design's 9.17 and the
  shipped relic:

  | type | at 10.25 | at 9.17 | shipped |
  |---|---|---|---|
  | bow | 61 | 53 | 46 |
  | scythe | 59 | 54 | 39 |
  | twinblade | 48 | 45 | 38 |
  | greatsword | 46 | 40 | 30 |
  | flail | 43 | 30 | 30 |
  | warhammer | 42 | 38 | 30 |

  - Worst foes at 10.25: Axiom 25%, Ironwood 27.5, Heartwood 30, Twinshade 32.5, then Gravemourn and
    Threshmaw (`redflail`) at 37.5.
  - Best: Marrowdraw 77.5, Lightkeeper and Starwarden 70, Aureole 65, then Lastlight, Ironhail, Farwarden,
    Cindercleave and Duskreave at 62.5.
  - At 40 fights a foe, a foe's rate has a standard error of about 8 points. The type rows (5 to 7 foes,
    200 to 280 fights) are the readable ones.
  - Over the shipped relic, the price gains +20 on the scythes, +16 on the greatswords, +15 on the bows, +13
    on the flails, +12 on the warhammers and +10 on the twinblades. The verdant pair (Heartwood, Ironwood)
    stays among its worst, as it was for the beam.
  - **The type spread is item 12/32, Rick's.**

**The gates on the final link** (`sc-goreshard-b10.25`, 8eb3c1634184c1bd):
- **engine_ab, sc-tendril-t3 → sc-goreshard-b10.25, the 37 others (every base id but `oathwound`), n=6:**
  **PASS. All 3996 matches are identical field for field**, with no page errors, 37/37 distinct winners and
  3996 distinct seeds, 20.8-111.2 s (`runs/engine_ab37_final.txt`, ids in `runs/ids37.txt`). The redesign
  moves no other relic's fight. The final link carries every line stage 2 adds, so this covers the price as
  well as the blade.
- **verify --n 40 on sc-goreshard-b10.25 (38 relics): 10/13, the base's own 10/13 with the same three reds**
  (`runs/verify_final.txt`, 28120 matches, 2739 s; the base's is v101's `verify_t3`). None of the three is
  Goreshard's:
  - the two clock bands: the overall mean is 60.8 s, the base's 60.8, and the pairings run from
    Gravemourn/Ironhail 38.6 s to Farwarden/Starwarden 100.0 s, as on the base;
  - "both sides can win every matchup": Heartwood v Twinshade 0/40 and Heartwood v Bindweed 0/40, as on the
    base.

  Every relic is inside 30-70% (Heartwood 30.9 to Gloamwire 63.1). **Goreshard reads 50.1%, against the
  shipped beam's 35.8% in the base's verify.** No other relic moves more than 1.6 points (Lightkeeper -1.55,
  Portcullis -1.01): each meets Goreshard in one pairing of 37.
- **tip_audit:** identical to the base's below the header path (`runs/tip_audit_final.txt`,
  `tip_audit_base.txt`). The one field no tip mentions is Burn's `feed`, the base's own. The build touches no
  status tip. The ult card is the builder's check: 69 characters, under 72.
- **chain_audit** (`--relic sc-goreshard-b10.25 --tip sc-goreshard-b10.25 --builder goreshard_build.py`,
  builder 7f2f86d2a87b7aa3): **9/9 inserts survive** (`runs/chain_audit_final.txt`): the eight table rows
  and `PRICE_CLAUSE_NEW`, the damage-line clause, marked by its own text `self.ultPrice ? self.w.dmg * (1 +
  self.w.ult.perStack * priceN) :`. The first build's audit read "8/8" and did not say the ninth was
  missing: its table pass skips an insert with no newline, and the clause is a partial line (the build's
  review deleted the clause from a copy of the final link and the old audit still printed "ALL 8 INSERTS
  SURVIVE"). Three controls, each able to fail:
  - the base as the tip loses all nine and exits 1 (`runs/chain_audit_ctl_base.txt`);
  - **the final link with only the clause deleted** (scratch `tmp/ctl-goreshard-noclause.html`) reports
    `LOST PRICE_CLAUSE_NEW`, the other eight surviving, and exits 1 (`runs/chain_audit_ctl_noclause.txt`);
  - the final composed onto the batch line's tip (§1's (a)) keeps all nine (`runs/chain_audit_batch_tip.txt`).
- **Rebuilt byte for byte:** the fixed builder (7f2f86d2a87b7aa3) writes all three links again from the base
  to the same sha16s (5dac38065e1c8ac3 / 9105fa5bb4cf258c / 8eb3c1634184c1bd; `runs/compose_check.txt`, "==
  the links in links/"). The fix names the clause and changes no byte of any link, so no gate that reads a
  link (engine_ab, verify, tip_audit, relic_rate, the gap table) can move, and none was re-run; the refusals
  (20/20) and the compose check (six tips) were.

## 5. Stage 6: the picture and the voice — `sc-goreshard-b10.25-fx`

The design's §4 (the picture, the sound) and its §5 brief stage 3, "picture, voice, carry; beam's field spec out;
`engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched", this build's stage 6. Picked on
measurements under Rick's "you pick i overrule" by two labs (the picture lab's scratch, `gs_rows.py`, copied as
`runs/stage6_picture/`, and `tools/goreshard_voice_lab.py`), and built as `goreshard_build.py --stage 6` on the
final stage-5 link (the b10.25): **thirteen anchored edits (voice 3, picture 10)**, byte-exact to the labs' own row
files (voice `rows_final.json` 780b26fd136cfa59, picture 1b95d5d4e1c71ed6; copied as
`runs/stage6_voice_rows.json` and `runs/stage6_picture_rows.json`).

```
sc-goreshard-b10.25.html          stage 5  the blade (the base of stage 6)                      8eb3c1634184c1bd
  -> sc-goreshard-b10.25-fx.html  stage 6  the picture and the voice (presentation)           f063e05c0f721d54
```

- **The rows, reproduced** (`runs/stage6_gen_s6.txt`; the generator is `runs/gen_s6.py`, the pattern's: rows ==
  files, the stamps, no nested anchor, merge by anchor line, a table written with triple-quoted strings, refusing
  a builder that already carries S6): the picture rows alone give the picture lab's stamp, **1f0248fee32086ba**
  (its `gs-final.html`, byte for byte); the voice rows alone the voice lab's end-to-end page,
  **8323dc9c2a8302b5**; both sets, either order and all thirteen reversed, **f063e05c0f721d54**, the fx link. No
  two rows share an anchor line, so none is merged; no row's anchor sits inside another row's anchor or code, and
  no two anchors' spans overlap. **Nine re-emit their anchor and four replace it**: three Goreshard's own
  (drawUltUnder's pool branch, drawUltOver's seam branch, the charge sigil `ULTSIG.oathwound`) and resolveHit's
  shared float-size line, replaced by its own text times `(1 + 0.1 x priceN)` -- x1 exactly wherever `priceN`
  is 0, which is every other relic's blow. Twenty new names (`tickGore`, `_goreShed`, `drawGoreWeapon`,
  `drawGoreDrops`, the `_gore*` helpers and the renderer's `_gorePals` cache, the eleven `gore*` fields), each
  free on the stage-5 link on identifier boundaries (the builder refuses otherwise) and each in the page after.
- **Composition.** The cast arm goes BEFORE the shared rune-crack fallback and the priced-blow branch BEFORE the
  plain hit arm, both re-emitting their anchor unchanged, so the eleven other relics that still fall through to
  rune-crack keep it (Lastlight, Spellbreaker, Ironhail, Lightkeeper, Farwarden, Aureole, Censer, Heartwood,
  Gloamwire, Portcullis, Bindweed, on the b10.25), and another relic's arms anchored there apply in either
  order. The picture's fields follow stage 2's own fields, `tickGore` follows `tickPrice`'s end; its call and
  methods sit beside shared lines every stage 6 of the batch uses (`tickPresentation`'s first call, drawWeapon's
  tree hook, the world pass's `drawTree`, `drawMotes`). **The compose check** (`runs/compose_check6.txt`,
  `compose_check.py 1,2,5,6`): stages 1, 2, 5 and 6 rebuild the four links from the base byte for byte, and
  re-apply on the same six later tips as §1's -- the batch line's tip `sc-spellbreaker-fxout` (42 relics),
  Aureole's and Widowmaker's carries, Bindweed's stage 6, and the Heartwood and Thornwake links in flight -- and
  on **(g) the batch line's NEWEST tip, `02-chain/sc-thornwake-fxout`** (65464e514ea28b9e; Thornwake was carried
  at 10:53 while this stage was being built), with every anchor once, every page parsing, and **the same +395 /
  -84 lines in the same order as on the base, on all seven**; the stage 1/2/5 shas on the first six are the
  earlier run's (on (g): f12e2f2b7a037a57 / fbc0e615d467750e / 189752974bf67319 / 5bdb719b3f893bc6). The picture lab also carried its rows with
  the voice rows onto 8 tips, both orders byte-identical, and ran them in 62 orders of its own
  (`runs/stage6_picture_order.txt`). **One composition note for the carry:** with Heartwood's in-flight picture
  rows the two relics insert at the same shared points (`drawMotes`, the world pass, `tickPresentation`), so
  the page's bytes depend on which is carried first -- the same lines, the two inserts in either order, both
  parsing -- and not its behaviour.
- The picture sheet is `05-reference/v114/goreshard-picture-sheet.png` (b1a2dd5650061cc2); the voice lab's wavs
  are `05-reference/v114/goreshard-*.wav` (24 files, 3.6 MB, raw level; gitignored).

### 5a. The picture

Every number here is the picture lab's: headless Chromium 151 at 540x960 with the post chain on (m2 on the final
bytes: 9 fights x 11 states, 97 frames; white, dark and ordinary foes; `runs/stage6_picture_m2_summary.txt`), on
its shipped-look page (the rows, with the beam's `SPECS.oathwound` taken out of the inlined `fx.js` as the carry
will: ef6a477f6e6c76c6, its stamp 28fc5864 -> d56fb70c, which is `fx_remove.py`'s own cut, 5b).

- **The blade, arterial red for the window** (v81: "the blade darkens to arterial red for the window"): through
  the window and its drain the blade draws itself (`drawGoreWeapon`, one hook in `drawWeapon` on a field nothing
  else writes), off the same blade set, reach and angles `bladeSegments` tests, with the school's steel swapped
  for **#D02A40** -- the blade, its barbs and its swept guard; the honed edge, grip, pommel and the fed notch
  stay the school's, so the barbed silhouette reads as it does at rest. The lightest red of three that still
  reads as blood (`gs_explore`: the weapon's |dL| 0.100 against 0.092 and 0.084 for the two darker).
- **The cast**: the red runs down the blade from the guard to the point in **0.3 s**, a bright seam at its
  front, easing OUT so it is already a third of the way down inside the cast's own 0.08 s stop (the lab's first
  version eased in and changed 0 px in the stop; the final reads |dL| 0.101 there). The cast is found by
  `priceTally.casts` rising, so `fireUlt` makes no call for the picture.
- **The glow, the stack readout** (v81: "the blade's glow SCALES with the foe's current stack count (0 -> 4
  maps alpha 0.2 -> 0.8)"): the blade's own glow sprite (`weaponGlow`'s cache: baked once a reach, never a
  frame), baked at **1.6x the blade's width, blur 18**, in the school's bright `glow` instead of its `core`, and
  ADDED (`lighter`, the world pass: nothing of it reaches the bloom) at **0.2 + 0.15 a foe stack**, read live
  through `stacks` and eased over 0.08 s. The wider sprite was picked on the ladder: 0.2 -> 0.8 moves |dL|
  0.109 over 8130 px against 0.076 over 5353 at the rest sprite's own width and blur (explore3; the weapon
  0.113 against 0.100); on the final bytes the ladder reads **0.100 over 7142 u2**, and the glow **0.048 /
  0.078 / 0.140 at the foe's 0 / 2 / 4 stacks**. The rest pose's glow crossfades out as the red runs in.
- **The motes** ("blood motes off the blade"): drops shed off the four back-edge barbs and the point in turn,
  **10 a second** while the window is open, placed by `shellHash` on their count (no RNG), carrying a third of
  the blade's sweep and a little speed out along it, then falling (560 u/s2), living **0.65 s**, at most 40;
  each drawn along its own velocity with a dark rim (#3A0610), so it reads on a white foe as well as on the
  floor; the world pass under both balls, clipped to the hall. They outlive the window by their fall.
- **The float** ("the damage float on a scaled blow is drawn larger"): **x(1 + 0.1 n)**, n the stacks the blow
  paid on -- x1.2 at 2, x1.4 at 4 (a 23 priced on n 2 prints at 43.5 px, where it printed at 36.3). resolveHit's own float
  line with the price's factor on it: every blow the price did not scale is the old size, exactly.
- **The close**: the red drains back from the point into the guard in **0.35 s** and the glow crossfades back
  to the rest pose's -- at a clock close, her fall, or `over`. The window is read off `ultPrice && !over`
  with both standing (reading 14): about one window in seven is still set when the match ends (reading 5), and
  the blade drains at the verdict instead of holding red through the panel (watched: Goreshard v Spellbreaker
  99015, her last window open at the kill drains inside the kill's own stop).
- **The beam's art is retired** ("the beam art is retired"): drawUltUnder's pool under the struck foe and its
  rivulets, drawUltOver's seam torn in the air over the quarry with its drops and the tether back to the
  caster (each branch replaced by a comment that says so), and the charge sigil `ULTSIG.oathwound`, which drew
  a beam and the pool under it: **now a greatsword laid across the rune, reddening from the guard to the point
  as the charge fills, its glow rising, blood running off its edge**. **Kept, declared:** the ultFx `life` entry
  `oathwound: 1.5` (it equals the map's default, and Heartwood's in-flight row anchors on that line); the
  engine's common Bloodprice banner.
- **The art hangs off the Fighter** (`goreFade`, `goreAge`, `goreOut`, `goreGlow`, `goreSeen`, `goreAcc`,
  `goreDropN`, `goreDrops`, and `goreTh` / `goreT` / `goreW`, the blade's sweep), never off `m.ultFx` (open item
  25); `tickGore` drives it in `tickPresentation` (half-seconds, as every `life` there: the run's 0.6 is 0.3 s),
  and `drawGoreWeapon` / `_goreGlow` / `_goreSteel` / `_goreFront` / `drawGoreDrops` draw it, one method a
  component, so each can be measured alone.
- **Bloom** (<= +0.02): the picture's share of the chain's arena lift **max +0.0000** (min -0.0003); the raw
  luma it adds (chain off) at most +0.0014. **Two controls, each failing:** a 200-unit white wash on the blade
  (4.1c) lifts +0.0854, past 0.02 on 44 of 97 frames, her disc past 0.90 on 78 of 81 window frames; the blade
  drawn as light over the balls (4.1b) pushes the foe's disc past 0.90 on 4 of 81.
- **No disc erased:** her disc moves at most 0.0013, a foe's 0.0117 (white sanctified, dark and ordinary alike),
  and no frame is newly past 0.90 (3 with, 3 without).
- **Legibility** (median |dL| of each component's own pixels, out of a hit stop / in one): **the window's blade
  0.093 / 0.110** (the resting blade 0.188: arterial red is a darkening, as v81 asks); the glow 0.048 / 0.078 /
  0.140 at 0 / 2 / 4 stacks; the cast inside its own stop 0.101; the red's front 0.128 / 0.367; the motes 0.134
  / 0.165; **the priced float 0.232 / 0.260**; the drain 0.128; at the verdict 0.109.
- **The silhouette at the app's size** (453x805, chain on; `runs/stage6_picture_sil.txt`): Goreshard at rest
  0.179, 5th of the 7 greatswords (unchanged); **in the window 0.113, dE 21.3 -- 7th of 8, above Emberedge's
  resting blade (0.107)**. Flagged: the design's "darkens" costs the window's blade about a third of its
  contrast against the floor; the glow and the motes carry the rest.
- **Whole fights** (the lab's verify, `runs/stage6_picture_verify.txt`: 14 pairs, 12 with Goreshard on either
  side and 2 without, each as the base, the rows, the shipped look, and the rows drawn through the renderer):
  **the simulation identical to the base in all 14**, every step hashed. **Control:** a copy with one 1e-9 sim
  write in the cast branch differs on all 12 Goreshard fights with a cast and on neither without her. **Drawn
  whole** (22 fights through the kill and 3 s of the verdict, the chain on and off by turns): nothing thrown;
  60/60 casts start the run on their step; the red up exactly while the window is open; the glow at 0.2 + 0.15 n
  on 54,187 checks; **97/97 priced floats exactly x(1 + 0.1 n), 672 other floats the old size**; no mote shed
  with the window shut; the shared weapon row never written.
- **The lab's own render_ab**: 54/54 frames pixel-identical on 9 pairs without Goreshard; two Goreshard pairs
  0/6 and 0/6 (`runs/stage6_picture_renderab.txt`).
- **Frame cost** (Electron 44, RTX 3070, ANGLE D3D11, interleaved A/B on three fights; a loaded PC, frames 36-61
  ms; `runs/stage6_picture_cost.txt`): the window **+0.1 / +0.2 / -0.1 ms** (noise); a blow +0.3..+1.5; **the
  cast +5.8..+6.4 ms and the close +5.6..+7.5 ms, for their 0.3 s and 0.35 s** -- while the red runs the blade
  is drawn twice (the school's and the red, each through `litWeapon`, one clipped behind the front). Alone, the
  window frame 7.7 -> 7.8 ms and a cast frame about 7 -> 12-14 ms.

**Readings declared** (the builder's docstring, 13-21; the art and the sound are Code's picks):
13. The picture hangs off the fighter (`gore*`), never `m.ultFx`; driven on the presentation clock.
14. The window is read off `ultPrice && !over` with both standing, so the blade drains at the verdict; the cast
    is found by `priceTally.casts` rising.
15. No `fx.js` field: the motes are drawn off the blade (5b); the beam's `SPECS.oathwound` is the
    orchestrator's to take out of both copies at the carry.
16. The glow is the blade's own sprite at 1.6x, in the school's glow, added at 0.2 + 0.15 n, eased.
17. The float is x(1 + 0.1 n) on a blow priced on n: resolveHit's own float line, one of the two lines stage 6
    puts on the sim path; it writes only the float.
18. The scaled blow's voice: the plain strike at the damage dealt, every frequency down a semitone a stack, for
    a blow priced on n > 0 (an x1 window blow keeps the plain call); the other line on the sim path.
19. The cast's voice is its own arm before the rune-crack fallback, re-emitted unchanged; the close plays
    nothing.
20. The beam's art is retired (the pool, the seam, the sigil redrawn); the life entry 1.5 is kept.
21. Nothing of it reaches the simulation: no RNG, spawnFx, ultFx or Math.random; no call into the simulation;
    writes only its own fields, its motes, the canvas and the synth.

### 5b. No new `fx.js` field: the motes are drawn, and the beam's spec goes out of both copies by the orchestrator

The design asks for "blood motes off the blade, both copies". A SPECS field fires once, at the cast, from the one
`m.ultFx` slot, where the cast was. The picture lab measured what that slot gives this relic over 107 Bloodprice
windows (16 foes x 2 seeds, both sides; `runs/stage6_picture_fxprobe.txt`):
- the slot is Goreshard's at the cast on 89 of 107, and then for a median **0.67 s** of the window clock (max
  0.72; the window is 8 s): a field borne on it could exist for **7.5%** of the window; the opponent's cast took
  it 18 times, it expired 88 times, and the match ended in it once;
- the motes are to come OFF THE BLADE, and the blade moves: after the slot is gone the blade's middle stands a
  median **220 units** from the cast point (p10 85, p90 403; 215 from the foe's point, where a burst is drawn),
  and it turns through a median **7.04 rad** over a window. A field spawned at the cast would shed where the
  blade no longer is, for a thirteenth of the window.

So the motes are DRAWN, off the barbs themselves, in the world pass (5a): the Zenith, Canopy, Tendril,
Exsanguinate and Unmaking precedent. **Rick's to overrule.**

The beam's own spec, `SPECS.oathwound` (mode `beam`), is the brief's "beam's field spec out". `fx.js` is shared by
every build in the batch, so this builder never edits it, and stage 6 refuses to write if its inlined copy moved
(reading 15; a negative copy of the builder that takes the entry out is refused, 5d). Its exact text (the fx
link's lines 32553-32555; `src/render/fx.js` on disk, lines 136-138, both at 7dc0123af735c83e and at
d08802c3e71e9f2b, which the orchestrator's Thornwake carry left there at 10:53, during this build):

```
    oathwound: { mode: 'beam', n: 1250, sp: [25, 140], grav: -60, drag: 1.3,
                 life: [0.40, 1.00], heavy: 0.0, size: [0.7, 2.0],
                 spawn: 0.50, up: 0 },
```

**Tried in scratch** (`runs/stage6_fx_remove_scratch.txt`, `runs/fxout_scratch.sh`; `fx_remove.py --fxjs` on
copies, the real `fx.js` untouched -- 7dc0123af735c83e before and after the first two, d08802c3e71e9f2b before and
after the third):
- on the fx link, with `fx.js` at the stamp its inlined copy carries (28fc58641370a1a9, extracted from the page,
  its sha256 checked against the stamp): the three lines come out whole, only the block and the two stamps move
  (-> **d56fb70c97b7dc93, the picture lab's cut**), the page becomes 3c1f4698a50d457b;
- **the carry, dry, on the batch line's tip:** stages 1, 2, 5 and 6 on `02-chain/sc-spellbreaker-fxout`
  (9243277a756e84b6 -> 46aca169fd7c2937 / b8b3319f11a41df1 / c3d5fc24835f91f4 / fb8d112bc1f4766a), then
  `fx_remove --relic oathwound` with a copy of today's `fx.js`: **on disk the entry is the first under the
  "BEAMS AND BOLTS" header, and the two-line "Negative gravity" note directly above it goes WITH it by
  default** (it is a comment, not a section header; the header stays, with 'axiom-echo', farwarden and marrowdraw
  under it). 7dc0123af735c83e -> 4ea79bab45f2a6d3, the page 0dfe8cc42e9931e0. That is what §0 recommended (no
  negative-gravity beam is left after it); `--keep-comment` keeps the note, if Rick wants it;
- **and again on the batch line's newest tip**, `02-chain/sc-thornwake-fxout` (65464e514ea28b9e; stages 1-6 ->
  5bdb719b3f893bc6), with a copy of `fx.js` as it stands after Thornwake's carry: the same five lines out,
  d08802c3e71e9f2b -> a778168bca1731d4, the page 02c578c378dc0afb.

The page is safe without the entry (`ULTFX.sync` returns on a missing spec, the fx link's line 32915). **Until the carry, the stage-6 link
still fires the beam's particle field at every cast (from the one slot, for its 1.5), and so does the clip (5g).**

### 5c. The voice

Every number here is `tools/goreshard_voice_lab.py`'s (dddf53194282c9a6; its final run, Chromium 151.0.7922.34;
`runs/stage6_voice_lab.txt`, its three rounds `runs/stage6_voice_r{1,2,3}.txt`; every render an OfflineAudioContext
at 48 kHz through `Sfx.buildChain`, render.py's xorshift noise, a candidate rendered from its arm's own text).
Its controls reproduce the six published numbers (rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, hit@11.6 0.443 /
80 ms), and levels are read against Goreshard's own blow at 10.25 (its loudest 50 ms 0.1124-0.1182 over 12
draws) and the wall tick (0.0105-0.0118). The design's sound is three lines: "cast -- a wet drawn-blade hiss,
0.4s; a scaled blow -- the sword's strike voice pitched DOWN by the stack count (bigger = lower); close --
nothing."

- **The cast, "a wet drawn-blade hiss, 0.4s" -- DRIP, of 4.** The draw, every candidate's: a scrape (bandpass
  noise, Q 5, narrower than air) RISING 2.6 -> 8 kHz in two overlapping strokes (2.6 -> 4.6 kHz over 0.36 s,
  and 0.16 s on, 4.1 -> 8 kHz over 0.49 s): **+997 cents from its first audible 100 ms to its last, swelling in
  194 ms (drawn, not struck), 0.96 of its power at 2 kHz and up.** Two strokes because a single `_sweep` cannot
  be audible 0.4 s at a blow's level (its ramps run to an absolute 1e-4: 0.27 s at the gain a blow needs) -- a
  toolkit finding, in the lab's docstring. The wet is the candidate; DRIP's is **three drops off the blade as it
  clears**, sines at 0.17 / 0.25 / 0.31 s, 760 / 880 / 1010 Hz, each chirping up 1.5x over 80 ms: heard **+9.0
  dB** over the score's p90 in its own band on its worst draw (level-matched there), gliding 804 cents, 0.02 of
  the power. **Audible 395-415 ms, gone by 465; its top -2.8 dB re the blow (quietest draw), +16.8 dB re the
  wall; heard +36.4 dB over the score; 5 synth calls.** Register at most **0.71** (the tornado's woosh) against
  rune-crack, the bloodsworn casts with voices of their own (Widowmaker, Threshmaw, Marrowdraw, Ravelbone,
  Bloodmirror), the greatsword casts' (Dawnbringer, Emberedge, Nightfell, Axiom), the woosh, the blow and the
  death voice, and the in-flight peers' casts (Widowmaker's inhale, Lightkeeper's, Heartwood's); on the batch
  line's tip (42 relics) against its school and type casts at most 0.44 (Emberedge). BUBBLE (0.77) and SLICK
  (0.73) pass too; the tiebreak (the most distinct register, to 0.05, then the fewest calls) picks DRIP. SQUELCH
  is out (its wet heard +3.3 dB, under the +6 gate). **Five controls each fail on the gate they are for:** DRY
  (the draw alone: no wet heard), STILL (the strokes held at 2.6 kHz: +75 c, not drawn), HUM (a held 620 Hz
  note: moving 27 c, not a liquid), FAINT (BUBBLE's wet 12 dB down: heard -1.6 dB) and RUNECRACK, today's voice
  (hiss 0.18, falling, struck).
- **The scaled blow, "the sword's strike voice pitched DOWN by the stack count (bigger = lower)" -- SEMI, of
  5.** The plain strike as the plain arm plays this blow -- at the damage DEALT, so its weight, level, jitter and
  crit are the blow's own -- with every frequency x 2^(-100 n / 1200): **a semitone a stack, a major third at
  4**, held at 4's voice above Hemorrhage's cap. Against the plain hit at the same damage it falls **-82 / -200
  / -316 / -422 cents on the crack and -102 / -204 / -307 / -409 on the body at 1-4 stacks**; at 2 and 4 (the
  counts a window has) that is 1.5 and 1.9 x what the damage roll's whole range moves the plain hit by (the
  SPREAD: 129 / 224 c on the crack, 95 / 150 on the body). **Its peak within 0.9 dB of the plain hit's; a strike
  (rise 1 ms, the peak at 8 ms); audible 1.08x the plain hit's at 4; on a phone -1.7 dB.** TONE (a whole tone a
  stack) and THIRD (a minor third) pass; the tiebreak -- the SMALLEST drop at 4 stacks that clears every gate
  (round 2: the least change heard over the dice keeps it "the sword's strike voice") -- picks SEMI. TAPE is out
  (audible 1.79x at 4: a boom), BODY out (its crack does not move). **Two controls each fail:** PLAIN, what a
  priced blow plays today, and UP (the interval upward).
  - **Flagged, for Rick's ear:** SEMI's 4-stack blow reads register **0.97 against the death voice** (the plain
    hit at the same damage 0.85, TONE 0.69). Printed, not gated since round 2: the hit and the death voice share
    the low register at this weight, so the gate failed today's own voice; "not a death" is read as NOT A BOOM
    (audible <= 1.25x the plain hit's; the death voice is 620 ms, the hit 80). The runner-up is one constant
    (`c` 100 -> 200, TONE).
  - What the weight alone already does today (the plain hit at the dealt damage, n stacks against 0): -149 /
    -356 c on the crack at 2 / 4 stacks. The pitch drop is on top of that.
- **The close: nothing** (v81). The window's ticker plays no voice at a close, by its clock or on a death, and
  nothing plays anywhere else for it (the probe's [11], 5e).
- **Wiring** (readings 18-19). The cast is `fireUlt`'s own prologue call, `SFX.play("ult", { w: f.w.id })`:
  Goreshard had no arm and fell through to rune-crack, so its arm goes BEFORE that fallback, which is re-emitted
  unchanged. The scaled blow: resolveHit's one line BEFORE its hit-voice line, `if (priceN > 0) SFX.play("hit",
  { dmg, crit, price: priceN }); else` -- the line after it, Canopy's call, follows unchanged -- and the hit arm
  grows one branch, `kind === "hit" && p.price`, BEFORE the plain arm: every call without `price` takes the arms
  below it, byte for byte. `priceN` is 0 whenever the window is shut and on every other relic.
- **The Sfx rows, applied to `Sfx.prototype.play`'s own source:** the arms equal their candidates (the cast
  4.5e-08 on two noise draws; the blow at 1-5 stacks x jitter x crit 1.2e-07; price 6 plays 4's voice, 0.0);
  **145 other voices unchanged through the patched play** (worst 2e-07: the hit at five weights x crit, a hit
  whose `price` is 0, Canopy's bough at three, the heal chime at n 0-6, 92 ult ids, every kind `play()` names);
  `ult/oathwound` is no longer rune-crack (0.608 apart) and the bare fallback still is (6e-08). Main-thread cost
  a call: the cast 0.20 ms, a priced blow 0.10 ms. **With eleven other relics' Sfx rows** (Widowmaker,
  Lightkeeper, Heartwood, Angelus, Aureole, Censer, Coldiron, Ironhail, Lodestone, Oracle, Spellbreaker): both
  orders render every arm alike (worst 1.8e-07), these arms unchanged by them.
- **The lab's wire run** (the resolveHit row applied to the prototype's own source beside the unpatched one;
  148 fights, Goreshard both sides x every foe, seeds 114601-2): **148/148 identical** (both fighters' hp,
  positions, velocities, stun, charge, Hemorrhage, both tallies, the winner, and a digest of every step), every
  other SFX call identical in order and options. **502 casts, 502 cast voices; 1224 window blows by the stacks
  they were priced on [0: 358, 2: 244, 4: 622] -> 866 priced voices for the 866 scaled blows, the 358 x1 window
  blows plain;** untouched: 1241 of her blows outside the window, 3107 of the foe's, 177 ward bursts; problems 0.
  **Control:** the row plus one sim write (the struck body nudged 1e-9 on a priced blow) leaves 4/148 identical.
- **End to end**, the three rows applied as text (8eb3c1634184c1bd -> 8323dc9c2a8302b5, +4381 chars) and loaded
  fresh: the new voices through the page's own `SFX.play` equal the candidates (worst 3.0e-08); 145 other voices
  unchanged (1.8e-07); 74/74 fights identical to the unpatched page's, cast voices = casts and every scaled blow
  voiced with its stacks in all 74; the unpatched page priced none. The same on the batch line's tip carrying
  stages 1-5 (c3d5fc24835f91f4, 42 relics): 82/82, 176 other voices unchanged.
- **A real window** (Goreshard v Bulwarden, side A, seed 114601; the cast at 31.30 s, a clock close at 40.93 s),
  over the fight's own sounds and the score: **the cast +34.7 dB in its own third-octave (5080 Hz)**; the
  window's five scaled blows each alone at the damage it dealt, their body -208 c (2 stacks, a 44 crit) and -412
  / -408 / -409 / -413 c (4 stacks) against the plain call.

### 5d. The builder's stage 6 (`--stage 6`, the S6 table and its scans)

`gen_s6.py` wrote the S6 table (13 rows, label / anchor / new, triple-quoted, byte-exact to the row files) into
`goreshard_build.py` once, and the wiring is by hand (`runs/patch_wire6.py`): the docstring's stage table and
readings 13-21, `--stage 6` on stage 5's link, `STAGE_OUT["6"]`, and two scans. The builder is now
eddeef420792bf7f (7f2f86d2a87b7aa3 before stage 6; it still writes the stub, the price and the b10.25 byte for
byte, `runs/compose_check6.txt`).

- **Stage 6 goes on stage 5, once:** the price at charge 14, Goreshard's row at the TUNED blade 10.25 (the base
  check reads the shipped head with the tuned blade for stage 6 alone), none of the twenty new names in the
  source yet, and neither voice arm.
- **`s6_static_checks`, the table's added code** (each row's re-emitted anchor out, comments out), run on every
  stage: no RNG (`rng`, `Math.random`, `spawnFx`) and never the one `ultFx` slot; no call into the simulation
  (apply, hurt, heal, resolveHit, fireUlt, knock, beat, float, note, tickPrice, tickHits ... ); no write to the
  shared weapon row, and no reference to a module table but three exact reads (`CONFIG.physics.ballR`,
  `CONFIG.arena`, `SHAPES[f.w.shape]`), none written; no write to a body, a status, the window, the tally, the
  hit stop or a beat; **writes only** its own `gore*` fields (on the fighter, or `this` in the Fighter's
  constructor), a mote's clock (`f.goreDrops[i].t`), the renderer's palette cache `_gorePals` (bound once), the
  canvas `c` (bound to the renderer's own context or a method's first parameter, never reassigned); **mutates
  only** its own motes (`f.goreDrops`) or a fresh local array; no `delete`, `defineProperty` or `Object.assign`
  into an object it did not make; `SFX`, `fsz` and `floats` only in **the two sim-path rows, each checked whole,
  line for line** (`if (priceN > 0) SFX.play("hit", { dmg, crit, price: priceN });` / `else`, and `const fsz =
  clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + 0.1 * priceN);`); the synth (`_tone`, `_burst`,
  `_sweep`, `.play(`, `frequency`) only in the two Sfx rows.
- **`s6_output_checks`, the page it would write:** the inlined `fx.js` (header to THE ULT FIELDS) untouched
  (reading 15); the rune-crack fallback there once and after Goreshard's arm; the priced-blow branch before the
  plain hit arm, which is there once; the beam's art gone (no `u.w === "oathwound"`, the old sigil and both
  branches' headers); the tick call, the world-pass call, the drawWeapon hook, the four methods, both arms and
  the new sigil each exactly once; the old float line gone and the two sim-path lines each added once, **inside
  resolveHit, after the price's read, the voice just before the hit-voice line**; `tickGore` straight after
  `tickNovaFx` in tickPresentation; fireUlt's cast voice call count unchanged; the page's `Math.random` count
  unchanged (13; the retired art drew none).
- **It refuses** (`runs/builder_refusals6.txt`, `refusals6.py`), all twenty-two:
  - five guards: stage 6 on the base, on stage 2 (no blade under it), on itself (twice), stage 5 on stage 6, and
    over an existing link (the link unmoved);
  - **seventeen negative copies of the builder, one stage-6 row made wrong each:** tickGore writing the foe's
    velocity, drawing the match's RNG, closing the window, writing a status, turning the blade, calling into the
    simulation (a note), playing a voice off its line, pushing a float, `Object.assign` into the fighter; a mote
    writing the shared weapon; the motes' draw taking the ultFx slot, using `Math.random`, writing a module
    table; the float row off its own text (x0.2); the priced voice on every window blow (`>= 0`); the cast arm
    dropping the rune-crack fallback; a row taking `SPECS.oathwound` out of the inlined `fx.js`.
  - **the harness can pass:** the builder copied unchanged writes the fx link's own bytes (f063e05c0f721d54),
    and a copy with a harmless comment in tickGore writes too (d719cfe76125eb56).
  - The twenty of stages 1-5 (`runs/builder_refusals.txt`) all refuse again on the new builder.

### 5e. The probe's stage 6: [11] the voices, [12] the picture's hook

`goreshard_probe.py` (a9c3cf33c7b141e9; bc2d8226432bf69c before stage 6) gains two checks, each run only where the
link carries it -- the voices detected by their own presence in `AC.SFX.play.toString()` (the cast arm, `w ===
"oathwound"`, and the priced-blow branch, `kind === "hit" && p.price`; one without the other fails [11]), the
picture by `tickGore` on the Match -- so the same probe still gates stages 2 and 5 at 10/10, every line as before,
and `--stage 6` requires both. Once a fight is over it steps 2 s more of the verdict (the `over` path: the
presentation clock only) for these two checks alone; [1]-[10] read none of those steps. The picture's numbers
are pinned from the builder's S6 table (the ease 0.16, the drain 0.7, the motes 5 a clock unit living 1.3,
capped at 40, the float's 0.1), and the glow's 0.2 -> 0.8 from v81 itself.

- **[11] the voices fire exactly on their events, and nowhere else.** Every `SFX.play` call in her fights is
  recorded (a no-op headless: the call is recorded before its first line returns) and tagged with where it was
  made. Evidence: a cast of hers playing anything but exactly one `ult` / `oathwound` voice, inside fireUlt, or
  that voice anywhere else; a blow of hers whose own hit voice (resolveHit's line; **a ward's shatter plays its
  own crit hit voice inside `hurt()`, told apart by its caller**, never priced) is not exactly one call --
  carrying `price` = the stacks it was priced on, with its dmg and crit, when her window is open and n > 0, and
  no `price` otherwise (x1 window blows, shut-window blows); `price` on any other call (the foe's blows, a
  shade's, a shatter); **any voice at all inside tickPrice -- "close -- nothing": a window closing by its clock
  or on a death plays nothing, and never a close voice on a death**; a voice of hers in the picture's hook, a
  drawn frame or the verdict. Coverage: casts voiced one for one, priced blows voiced at n 2 and 4 one for one
  with the log, x1 and shut-window blows plain, the foe's blows unpriced with her window open and shut, clock
  closes and death closes silent, a quiet verdict.
- **[12] the picture's hook writes nothing of the simulation's, and is the picture declared.** `tickGore` is
  wrapped: evidence is any change across it to either fighter or a shade (every own number, flag and string but
  the picture's `gore*` fields, every array's length, every status) or to the match, an RNG draw or a voice; the
  foe carrying any of the picture; the picture up before her first cast. **And the picture rebuilt, exactly, in
  the builder's own arithmetic:** the red up exactly while her window is open with the match on and both
  standing; the run clock the presentation clock since the cast (found by `casts` rising); the drain a fade to
  0 over its 0.7 at any close; the glow eased toward 0.2 + 0.15 x the foe's Hemorrhage; the motes shed 5 a clock
  unit while open and never while shut, each born within her reach, aged to 1.3, capped at 40; nothing up after
  2 s of the verdict. **The float:** every blow in her fights draws its damage float exactly clamp(22 + dmg x
  0.62, 22, 62) x (crit ? 1.3 : 1) x (1 + 0.1 n) for a blow of hers priced on n, and the old size for every
  other (hers shut or at n 0, the foe's, a shade's). `--drawn N` adds a drawn subset: the first seed's fights
  drawn through the renderer (270x480, the post chain off) every Nth step while the picture shows and every
  120th otherwise, through the kill and the verdict; [12] fails a frame that throws, draws the match's RNG,
  plays a voice, or changes the simulation or the picture's clocks.

**Results.**
- **sc-goreshard-b10.25-fx (stage 6): 12/12** (`runs/probe_fx.txt`, 444 fights):
  - [11]: **1489 casts, 1489 cast voices; priced blows voiced 748 at n 2 and 1791 at n 4 -- the log's own 748
    and 1791; 1134 x1 window blows and 3974 shut-window blows plain; 471 ward shatters' own voices unpriced**;
    the foe's blows unpriced, 5313 with her window open and 4343 shut (a shade's among them); **closes silent:
    1201 by the clock and 62 on a death**; 444 verdicts quiet (226 with the window the sim left set);
  - [12]: **tickGore clean on all 6,334,461 calls** (1,564,075 before a first cast); rebuilt exactly: 1489
    casts found, 2,803,762 open calls (the glow checked at n 0 / 2 / 4 on 892,040 / 679,204 / 1,232,518 of
    them), 1203 closes with the match on, 226 at a kill with the window set, 60 at `over` after a death's
    close, 123,587 draining calls, the red gone after all 1489; 116,600 motes shed, every one born on her blade;
    all 444 fights clean after the verdict; **floats: 2539 priced exactly x(1 + 0.1 n), 1134 x1 and 3974
    shut-window blows of hers and 9656 of other attackers' the old size**;
  - **[1]-[10] are the stage-5 link's, number for number** (`runs/stage6_probe_cmp.txt`, `probe_cmp6.py`: the
    57 counters of [1]-[10], the tally, the log and the win rate equal, and the 29 printed [1]-[10] lines
    identical but the header): the picture and the voice move no fight the probe plays.
- **sc-goreshard-b10.25 (stage 5) on the extended probe: 10/10**, every line the earlier run's, and "stage 6:
  not on this link -- [11]-[12] not run" (`runs/probe_b10.25_s6probe.txt`).
- **The drawn subset** (`--drawn 24` on the first seed, 74 fights: **12/12, 13,669 frames drawn clean** -- 11,272 with the picture up, 1797 in a hit stop, 281 in the verdict -- nothing thrown, no RNG drawn, no voice played, neither the simulation nor the picture's clocks changed (`runs/probe_fx_drawn.txt`)); **its control**, the stage-5 link drawn the same way: 4651 frames clean, [12]
  the drawn check alone, 11/11 (`runs/probe_b10.25_drawn_ctl.txt`).

**The mutants** (`runs/stage6_mutant_table.txt`, `mutants6.py`, `mutant_table6.py`; the probe's output for each in
`runs/mutants6/`): seven mutants of the fx link, each breaking one sentence of the picture or the voice, run at 1
seed (74 fights), the drawn one with `--drawn 24`. "Fights changed" is out of 148 (Goreshard v every foe, 2 seeds,
both sides, `AC.simulate`'s summary against the fx link's):

| mutant | fails | fights changed | she wins (1 seed) | caught on |
|---|---|---|---|---|
| mV1: the cast voice again at every window close, a death's included (a close voice) | [11] | 0 | 48.6 | "her cast voice played in the price's ticker" (408) |
| mV2: the priced voice on every window blow, x1 ones included (price 0) | [11] | 0 | 48.6 | "a x1 window blow of hers voiced price 0" (204) |
| mP1: tickGore nudges the foe 1e-9 at every mote it sheds (a sim write) | [12] | 143 | 43.2 | "the picture wrote the simulation: vx ..." (19,039) |
| mP2: the glow's floor 0.25, not v81's 0.2 | [12] | 0 | 48.6 | "goreGlow 0.9609375 (want 0.9583...)" (464,748) |
| mP3: the priced float x(1 + 0.2 n), not x(1 + 0.1 n) | [12] | 0 | 48.6 | "(n 2): its float 50.76, want 43.51" (416) |
| mP4: the red read off the window alone, so a kill that leaves the window set holds it red through the verdict | [12] | 0 | 48.6 | "the picture draining: goreFade 1 (want 0.988)" (23,641) |
| mD1: the blade's draw writes her velocity (only a drawn frame can see it; `--drawn 24`) | [12] | 0 undrawn; the drawn fights move | 51.4 | "a drawn frame changed the simulation: vx ..." |

**Each fails its own check and only that one (7/7).** The four that change no fight are the controls a picture or
a voice needs: engine_ab cannot see them, and [11] or [12] fails each alone. mP1's sim write is also engine_ab's
control (5f). **The first pass** (`runs/mutants6_pass1/`) caught two faults of the harness, not of the build, and
both are fixed before the numbers above: (1) mP1 failed [11] as well as [12], on "a blow of hers priced on n 4
voiced dmg 21.700000000000003, want 21.69999999999999" -- once mP1 moved the fight, a blow whose damage a foe's
rule left fractional was compared by `===` against the dealt total's difference; the voice's dmg is now held to
1e-6, and the float's text is read with `parseFloat` (the unmutated runs never met such a blow, and read the same
before and after); (2) the first mP4, `!this.over` alone taken out of the red's test, read 12/12: **an equivalent
mutant** -- on these fights `over` is only ever set with a death (no timeout), and `alive` already drains the red
-- so it was replaced by the window-alone mutant above, which reads 23,641 fails.

### 5f. Stage 6's gates -- every one able to fail

- **engine_ab, sc-goreshard-b10.25 -> sc-goreshard-b10.25-fx, all 38 relics, GORESHARD INCLUDED, n=6: PASS. All
  4218 matches identical field for field** (`runs/engine_ab38_fx.txt`, ids in `runs/ids38.txt`; no page errors,
  38/38 distinct winners, 4218 distinct seeds, 18.6-114.9 s; 368 / 374 s). The picture and the voice move no
  fight, hers included. **Control** (`runs/engine_ab_ctl_mP1.txt`): the same against the mutant whose picture
  nudges the foe 1e-9 at every mote it sheds (mP1), on Goreshard, Axiom, Aureole and Widowmaker: **FAIL, 18 of 36
  differ -- every one of the 18 matches Goreshard is in**, and none of the others.
- **The probe, 12/12 on the fx link** (5e), its [1]-[10] the stage-5 link's number for number; **the fx link composed onto the batch line's tip** (§1's (a), 42 relics, 492 fights against 41 foes; `runs/probe_fx_on_batch_tip.txt`): **12/12** -- 1689 casts, 1689 cast voices; 817 / 2032 priced blows voiced at n 2 / 4, the log's own; 1364 clock closes and 63 death closes silent; tickGore clean on 7,146,310 calls; 2849 priced floats exact and 10,984 of other attackers' the old size.
- **render_ab, sc-goreshard-b10.25 -> sc-goreshard-b10.25-fx** (540x960, frames at 0.5 / 6 / 12 / 22 / 31 / 40 s):
  on four pairs without Goreshard (Paradox v Heartwood 25064, Twinshade v Lastlight 991, Bulwarden v Vinesower
  70707, Axiom v Grudgebearer 31337), **PASS, 24/24 frames pixel-identical** (`runs/render_ab_others.txt`).
  **Control**, Goreshard v Aureole 4101 (her window up at 12-40 s): **0/6 identical** (`runs/render_ab_control.txt`)
  -- the frames at 0.5 and 6 s, before her first cast, differ by the charge sigil alone (the HUD's rune, redrawn),
  and the four in a window by the blade, its glow and the motes.
- **chain_audit** (`--relic sc-goreshard-b10.25-fx --tip sc-goreshard-b10.25-fx --builder goreshard_build.py`,
  builder eddeef420792bf7f): **ALL 22 INSERTS SURVIVE** (`runs/chain_audit_fx.txt`): stages 1-5's nine (the clause
  among them) and stage 6's thirteen. Two of stage 6's are marked by comment text -- the beam's pool and seam
  retired, whose only added text is the comment that says so (§6). **Controls:** the stage-5 link as the tip
  loses exactly stage 6's thirteen and exits 1 (`runs/chain_audit_fx_ctl_b5.txt`); the fx link composed onto the
  batch line's tip (§1's (a), `compose/a`) keeps all 22 (`runs/chain_audit_fx_batch_tip.txt`), and so does the
  fx link composed onto the NEWEST tip, `sc-thornwake-fxout` (`compose/g`, `runs/chain_audit_fx_newest_tip.txt`).
- **tip_audit** on the fx link: identical to the final link's below the header path (`runs/tip_audit_fx.txt`,
  `runs/tip_audit_final.txt`): stage 6 touches no status tip, and the card is stage 1's.
- **The refusals and the compose check** (5d, 5): twenty-two stage-6 refusals and the twenty of stages 1-5 all
  refuse; stages 1/2/5/6 rebuild all four links byte for byte and re-apply on seven later tips, the same lines.
- **verify is not re-run on the fx link**: stage 6 moves no fight (engine_ab above, with Goreshard in, and the
  probe's [1]-[10]), so §4's verify on the b10.25 (10/13, the base's three reds, Goreshard 50.1%) stands for it.
- **shell_identity is not run here** (the app's json is shared; the orchestrator runs it at the carry).
- **One fight watched** (the brief's gate): the picture lab's watch (Goreshard v Spellbreaker 99015, side A, four
  windows, the last open at the kill and drained inside the kill's own stop, nothing thrown;
  `runs/stage6_picture_watch.txt`, the sheet's last row), and the clip (5g).

### 5g. The clip (Rick's to overrule)

**`07-shorts/v114/bloodprice-window.mp4`** (0559c567566128ba; 754 frames, 12.59 s, 540x960 at 60 fps, AAC 48 kHz
stereo; 2.1 MB). RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.

- **The pick** (`tools/_goreshard_pick.py`, `_ironwood_pick.py`'s shape by way of `_spellbreaker_pick.py`): a
  window qualifies only if it shows the whole of v81 §4 as built -- one cast (its voice and the red's run), blows
  priced on 4 AND on 2 (their voices and floats), the glow at the foe's 0, 2 and 4 stacks, and a close BY ITS
  CLOCK with both alive (the drain; a death's close or a kill is the death voice's moment and the verdict's) --
  and nothing takes it over: no cast of the foe's or other banner anywhere in the clip, not the scrunch card, not
  the match's end. Left out of the pool: Twinshade (a second body) and the five bloodsworn foes (the same red,
  bleeding HER; the clip has to show whose blade the price reddens). **Four seeds found one qualifying window of
  124** (`runs/stage6_pick.txt`: Slagheart 114038, four blows); **twelve found four of 372**
  (`runs/stage6_pick_12seeds.txt`), and the best is filmed: **Goreshard v Grudgebearer, seed 114371, side A, the
  cast at 31.81 s, 9.57 s of match time to a clock close, four blows priced on 4 and one on 2, the foe at 0 / 2 / 4
  stacks on 3 / 29 / 68% of the window's steps, six blows in all**.
- **The command:**
  ```
  python cinema_clip.py --game <scratch>/batch/goreshard/links/sc-goreshard-b10.25-fx.html --a oathwound \
    --b grudgebearer --seed 114371 --at 30.61 --window 12.57 --end-at-window --fps 60 --w 540 \
    --out ../07-shorts/v114/bloodprice-window.mp4
  ```
  (lead 1.2 s before the cast, tail 1.8 s after the close; `runs/stage6_clip_log.txt`: the first frame at match
  30.617, the window ends at 43.18 s, the fight not over, hp 209 / 125.)
- **What is in it, second by second** (`runs/stage6_clip_timeline.txt`, the same fight headless; video time is
  match time less 30.62): **the cast at 31.81** (the hiss; the red runs down the blade, the Bloodprice banner);
  an x1 blow at 32.08 (the foe not bleeding yet: a 12, the plain voice, the old float); **priced blows at 34.90 (n
  2: 22, float 42.8 px), 36.09 (n 4: a 69 crit, float 112.8 px -- the size's ceiling, 62 x 1.3 x 1.4), 37.08 (n
  4: 34), 37.98 (n 4: 30) and 40.63 (n 4: 28)**, each a semitone a stack lower; **the clock close at 41.38**, no
  voice, the red drained by 41.73 (0.34 s); a plain blow at 41.93 after it. At most 7 motes in flight; 190 of the
  window's 1149 steps in a hit stop.
- **Five frames** (`05-reference/v114/bloodprice-clip-5frames.png`, 0b2be19d649e93f9, video 1.36 / 4.32 / 5.55 /
  7.90 / 10.93 s), checked by eye that the art renders through the pipeline: the cast (the banner, the blade
  reddening from the guard; **the beam's particle field still fires here, from the one slot: it goes at the carry,
  5b**); the n-2 blow (22, HEMORRHAGE, drops off the barbs); the 69 crit at 4 stacks, its float the largest on
  screen; the window at 4 stacks (the red blade, its glow, the motes, a 30); the drain, the red running back to the
  guard with the point steel again.
- **The AAC levels** (`runs/stage6_clip_levels.txt`): mean -22.4 dB, max -2.5 dB; -20.6 LUFS integrated, LRA 0.7
  LU, true peak -2.0 dBFS. The same window filmed on the stage-5 link (scratch, a1d320db3ec57252): mean -22.3,
  max -3.0; -20.4 LUFS, LRA 1.0, TP -2.4. The stage-6 voices move the clip's loudness by 0.2 LU.
- **The voices, in the mix** (`runs/stage6_clip_audio.txt`, `clip_audio6.py`: both clips decoded to mono 48 kHz,
  the same fight frame for frame, each voice read where it is):
  - **the cast rises**: its 2-12 kHz centroid **+879 cents** from its first 100 ms to its last (3283 -> 5454 Hz;
    the lab's +997 alone), where the same moment on the stage-5 link, rune-crack, **falls -640**; the scrape's
    top (4-9 kHz, 0.20-0.45 s) **+16.9 dB** over it. The drops' band reads -11.1 dB against rune-crack's own
    energy there: the drops are quiet by design (0.02 of the voice's power; the lab level-matched them +9 dB over
    the score in their own band, not over rune-crack);
  - **each priced blow's body is lower**: the FFT peak at 40-400 Hz over its first 40 ms, against the same blow
    on the stage-5 link: **-483 c at n 2; -454, -358, -189, -296 c at n 4** (the arm: -200 / -400; in the mix,
    over 40 ms of the score and the foe, a peak reading is coarse). **Control:** her two plain blows read **+0 c
    and +0 c**;
  - **the close plays nothing**: 0-0.4 s after it, with against without, +0.0 / +0.5 / +2.3 dB (40-400 Hz /
    700-1600 / 2-12 kHz) -- inside what windows with no new voice sounding read once the two soundtracks differ
    anywhere (-0.9 .. +3.2 dB, four windows 0.5 s clear of every event); before the cast, every band -0.0.
- The clip is sent to Rick; he overrules from it.

### 5h. Where each event hangs, and the simulation state stage 6 reads

**In the fx link** (`sc-goreshard-b10.25-fx.html`, f063e05c0f721d54):
- **the window and the tally the picture reads**: the cast opens `ultPrice` in fireUlt's price branch (L16814);
  `tickPrice` (L13740, called from `step()` at L9036) keeps its clock and closes it; the tally counts casts,
  window frames and priced blows;
- **the picture**: its fields at L7787 (after stage 2's); `this.tickGore(dt)` in tickPresentation (L9078);
  `tickGore` (L13768) and `_goreShed` (L13807), after tickPrice; the world pass's motes call (L19516);
  `drawGoreWeapon` (L20617) and `drawGoreDrops` (L20694), before `drawMotes`; drawWeapon (L24222) and its hook
  (L24365); the sigil `ULTSIG.oathwound` (L662); the pool's and the seam's retirement comments (L21422, L22174);
- **the voice**: the priced-blow branch (L6060) before the plain hit arm (L6084); the cast arm (L7464) before
  the rune-crack fallback (L7490); fireUlt's cast voice (L16438); in resolveHit the price's read (L14585), the
  damage line (L14595), the float (L15299) and the priced voice (L15318), the hit-voice line after it;
- the ultFx `life` entry `oathwound: 1.5` (L16467, kept) and `SPECS.oathwound` in the inlined `fx.js`
  (L32553-32555, out at the carry).

**The labs' brief** (written before stage 6; the line numbers are the stage-5 link's, `sc-goreshard-b10.25.html`):

- **The window**, `f.ultPrice = {t, dur}`, is null outside it. The cast sets it in fireUlt's price branch
  (L16630-16639; `{ t: 0, dur: u.dur }` at L16634). `tickPrice` (L13645) clears it on the clock or on a
  death it sees (L13651). It is called from `step()` at L8942, after `tickTendril` and before `tickHits`, on
  the window tickers' clock, so it stops in a hit stop. A window is 960 live steps (8.000 s), about 9.34 s of
  match time.
  **About 15% of windows are still set at `over`** (reading 5), so a picture must stop at `over`.
- **The tally**, `f.priceTally = {casts, frames, foeStk, blows, stk}`, is cumulative over a fight:
  - `casts++` at each cast (L16637);
  - `frames` / `foeStk` on each live window step (L13652-13653);
  - `blows++` and `stk += priceN` on each priced blow (L14420).

  So the picture can find a cast by `casts` rising and a priced blow, with its n, by `blows` / `stk`
  rising, with no call on the sim path (the Exsanguinate and Tendril pattern).
- **The price** (`resolveHit`, L14347):
  - the read at L14419: `priceN`, the struck body's Hemorrhage (the opponent, or a Twinshade shade);
  - the tally at L14420, and the damage line at L14429;
  - `hurt` at L14587, `self.hits++` at L14590, the stop at L14646, the hit beat at L14681, the hitstun at
    L14703;
  - the onHit loop at L14742 (`foe.apply` at L14748: the blow bleeds after it pays), the HEMORRHAGE tag at
    L14763, the knock at L14988;
  - **the damage float** at L15127-15128: `fsz = clamp(22 + dmg x 0.62, 22, 62) x (crit ? 1.3 : 1)`. A priced
    blow's number is already larger by its damage; the design asks for it "drawn larger";
  - **the hit voice** at L15136, `SFX.play("hit", self.ultTree ? {dmg, crit, bough} : {dmg, crit})`. The
    design's "the sword's strike voice pitched DOWN by the stack count" can pass one plain number more while
    `self.ultPrice && priceN > 0`, as Canopy's `bough` does.
- **The cast** (`fireUlt`, L16227):
  - the banner at L16246 (Goreshard is not in `onTarget`, so the name sits on the caster), the 0.08 stop at
    L16251, the ult beat;
  - `SFX.play("ult", { w: f.w.id })` at L16254. The ult dispatch (L6161) has no `oathwound` arm and falls
    through to the shared rune-crack at L7425. The design's cast voice ("a wet drawn-blade hiss, 0.4s")
    needs an arm BEFORE that fallback, which is re-emitted unchanged (the Bindweed / Portcullis pattern).
  - The ultFx `life` entry is `oathwound: 1.5` (L16283). The close plays nothing (the design: "close --
    nothing").
- **The beam's art to retire** (§4: "the beam art is retired"):
  - `drawUltUnder` (L20734), its branch `u.w === "oathwound"` at L21103: the pool;
  - `drawUltOver` (L21294), its branch at L21871: the seam and its drops;
  - `ULTSIG.oathwound` at L659, the charge sigil ("a beam, and the toll paid under it"). The design does not
    name it, but it draws a beam;
  - `SPECS.oathwound` in the inlined `fx.js` (L32292-32294), which goes out of both copies at the carry by
    the orchestrator. On disk it is the FIRST entry under "BEAMS AND BOLTS" (L136-138), with 'axiom-echo',
    farwarden and marrowdraw after it: the header stays, and only the "Negative gravity" note above it
    loses its subject (§0).
- **The blade** ("darkens to arterial red for the window; the blade's glow SCALES with the foe's current
  stack count (0 -> 4 maps alpha 0.2 -> 0.8)"):
  - the head and silhouette route is `SHAPES.greatsword` (L3452) -> `if (key === "bloodsworn") return
    SHAPES._gsBarbed(c, L, W, p)` (L3460) -> `_gsBarbed` (L3630). Goreshard is the only bloodsworn
    greatsword;
  - `drawWeapon(m, f)` is at L23968, and `weaponGlow(shape, L, W, pal, k, blur)` at L17930 is called from
    it at L24137. A glow that tracks the stacks should not rebake glow sprites every frame (Canopy's
    frame-cost note, v99 §6);
  - the foe's stacks are read live with `foe.stacks("hemorrhage")`. In practice they are 0 / 2 / 4:
    - on a window frame, 2.21 on average;
    - at a window blow, n 0 on 31% of blows, 2 on 20% and 4 on 49%.
- **The field** ("blood motes off the blade, both copies"): a SPECS field rides the one `m.ultFx` slot,
  which the opponent's cast takes (open item 25). The batch's precedent (Zenith, Canopy, Onslaught, Tendril,
  Exsanguinate) draws the motes instead, in the world pass, placed by `shellHash`, never the RNG.
- **Numbers for the picture:** 3.35 casts a fight, 2.47 priced blows a cast, 15% of window steps frozen.
- **Presentation hook:** `tickPresentation` is at L8982.

## 6. What is left, and whose

- **Rick:**
  - **the clip** (5g, sent): the picture and the voice are Code's picks under "you pick i overrule", one clip.
    What to overrule, each with its number:
    - **the window's blade is darker than the blade at rest** (|dL| 0.113 against 0.179 at the app's size: 7th
      of the 8 greatswords, above Emberedge's resting blade) -- v81's "darkens to arterial red", taken at its
      word; the glow's ladder (0.048 / 0.078 / 0.140 at 0 / 2 / 4 stacks) and the motes carry the window. The
      red is one constant (#D02A40; the two darker reds read 0.092 and 0.084);
    - **the scaled blow at 4 stacks reads register 0.97 against the death voice** (printed, not gated: the plain
      hit at the same damage already reads 0.85, since the hit and the death share the low register at this
      weight). "Not a death" is read as not a boom (audible 1.08x the plain hit's). TONE, a whole tone a stack
      (0.69), is the runner-up and one constant;
    - **no fx.js field**: "blood motes off the blade, both copies" is drawn off the barbs, not fired from the one
      ultFx slot (7.5% of a window, 220 units from the blade; 5b);
    - **the float's size, x(1 + 0.1 n)** (x1.4 at 4): v81 says "drawn larger" and names no factor;
    - **the frame cost**: the cast and the drain cost +5.6..+7.5 ms a frame for their 0.3 s and 0.35 s on a
      loaded PC (the blade drawn twice while the red runs); the window itself +0.1 (5a);
  - the stages 1-5 items stand as they were:
    - the blade: 10.25 by his 2026-09-29 ruling (50.2%). The design's 9.17 reads 43.2, and the shipped rate (35.3)
      would be about 8.8 (8.5 reads 33.9) (§4). It is one number in the builder;
    - reading 11: the price stops at hemorrhage's own cap of 4 (§1's "cap 4"). §6.3's Bloodletting cap of 8 is
      not priced and not built; its mutant reads 64.0% against the build's 50.9% on the same fights (§3), so it
      would need its own blade. The scaled blow's voice holds 4's voice above 4, so an 8 cap would not push the
      strike further down than was measured;
    - reading 2: a blow on a Twinshade shade pays on the shade's own stacks (§4's literal "the stacks it found"),
      where the lab's `w.dmg` paid it on the opponent's. That is 34 blows in 3,907;
    - **the window's clock** (the batch convention, not a choice of this build): the window is 8 s of UNFROZEN
      time on the window tickers' clock, about 9.34 s of match time, where the lab's window was 8 step-seconds,
      frozen ones included. It is the largest single term in §2's gap, worth about +4.9 on the build (45.8
      against the match-clock variant's 40.9, 3.6 SE). The charge was converted to the game's clock (16 -> 14)
      and the window was not, as for Corollary through Tendril. The 50% blade already absorbs it; a window on
      match time would need its own blade;
    - the type spread (item 12/32): bows 61 and scythes 59 against warhammers 42 at 10.25.
- **The orchestrator (ALL DONE at the carry, §7):**
  - **the carry** onto the batch line's tip: `goreshard_build.py` stages 1, 2, 5 and 6 with `--src <tip>`, proved
    with engine_ab. The compose check says all four apply with the base's lines on `sc-spellbreaker-fxout` and
    on the newest tip, `sc-thornwake-fxout` (5, §1), the probe reads 12/12 with stage 6 on the first (5f), and
    chain_audit keeps all 22 inserts on both (5f). Engine_ab at the carry
    excludes `oathwound` for stages 1-5 by the redesign policy (the price's own survival is chain_audit's and
    the probe's); **stage 6 itself moves no fight with Goreshard IN** (5f: engine_ab over all 38);
  - **at the carry, `fx_remove.py --relic oathwound`**, out of both `fx.js` copies. On disk the entry is the
    first under "BEAMS AND BOLTS" and the two-line "Negative gravity" note directly above it goes with it by
    default -- the header stays, with 'axiom-echo', farwarden and marrowdraw under it; `--keep-comment` keeps
    the note. Tried in scratch on the batch line's tips (5b): on `sc-spellbreaker-fxout` 7dc0123af735c83e ->
    4ea79bab45f2a6d3, and on the newest, `sc-thornwake-fxout`, d08802c3e71e9f2b -> a778168bca1731d4;
  - **shell_identity** on the carried link (not run here: the app's json is shared);
  - **carry order with Heartwood's picture**: the two relics' inserts share three anchor points, so the bytes
    depend on which is carried first (the same lines either way, both parsing; 5);
  - `src/render/fx.js` was not edited by this build.
- **Standing, not this build's:**
  - `chain_audit`'s table pass still skips an insert body with no newline (tools/chain_audit.py, the
    `"\n" not in body` test). This build works round it by naming its partial-line insert
    `PRICE_CLAUSE_NEW`; any other builder with a partial-line table row is still unaudited there (open item
    31's family);
  - **`chain_audit` audits presence, not removal**: stage 6's two retirement rows (the beam's pool and seam) add
    only a comment, and it marks them by that comment's text (it says so: "marked by COMMENT text"). A carry that
    brought a beam branch back beside the comment would still pass; the builder's output check (the beam's art
    gone, `BEAM_GONE`) is what refuses it, at build time only.

## 7. The carry onto the chain, and the old beam's field spec out

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Heartwood with the
same builder, one stage at a time (`--src` the previous link), and one more link that takes the retired
beam's particle field out:

```
sc-heartwood-fxout.html            the batch line's tip (Heartwood, fx out)   d692f6a014bf5a69
  -> sc-goreshard-stub.html         stage 1                                       ec8ad922c561f0a6
  -> sc-goreshard-price.html        stage 2                                       5999922a2462f663
  -> sc-goreshard-b10.25.html       stage 5                                       a5cda688a968522e
  -> sc-goreshard-b10.25-fx.html    stage 6                                       217e637c6df96565
  -> sc-goreshard-fxout.html        the old beam's field out of both fx.js copies a58575b8f16c3d8e
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail, Widowmaker, Lightkeeper, Censer, Aureole, Spellbreaker, Thornwake and Heartwood (redesigned on the chain since), n=6: **2610/2610 identical** (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-heartwood-fxout` against the carried stage-6 link, every relic on the tip but
  Goreshard (41), n=6: **4920/4920 identical** (`runs/carry_engine_ab_tip.txt`).

**The field spec out: `tools/fx_remove.py`** -- SPECS.oathwound (Goreshard's beam; its id is oathwound), with the 'negative gravity' note above it: no negative-gravity beam is left after it: **fx.js e07b60fee7425662 -> 7d745d39bfb9fecd**
(`runs/fxout/fx_remove.txt`).

**Gates on `sc-goreshard-fxout`** (`runs/fxout/`, full power):
- engine_ab against the carried stage-6 link, all 42 relics, n=6: **5166/5166 identical**;
- `goreshard_probe.py --stage 6` on the carried link: **12/12** -- it met every relic carried since its scratch base;
- render_ab: the other relics' four pairs **24/24 identical**; **the control, Goreshard v Grudgebearer 114371 through the cast (31.84-32.24s), 0/5
  identical** -- the old field is gone;
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold;
- **shell_identity 200/200** (app Chromium 152 vs headless 151; the json restored).

**The clip, filmed on `sc-goreshard-fxout`** (the §5 command, `--game` the carried link):
`07-shorts/v114/bloodprice-window.mp4` (2.06 MB, 12.6s; `runs/fxout/clip.txt`).

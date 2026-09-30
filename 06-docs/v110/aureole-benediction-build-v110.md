# v110 — AUREOLE / BENEDICTION (REDESIGN), BUILD. STAGES 1-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-censer-fxout`, the retired beam's field spec out of both `fx.js` copies: §7; shell_identity 200/200): stage 1 is arm A to the fight; the halo is the lab's mechanism, on the engine's window clock (measured); the blade to the design's target, the shipped rate: 12.5 (56.1% both sides, against the shipped 54.1%); the 50% alternative is 11.5 (48.8%). **Stage 6, the picture and the voice, is built (`sc-aureole-b12.5-fx`, §5):** thirteen rows byte-exact to the two labs'; a ring of light at the halo's own radius under both balls, brightening while a foe is inside, a rim on the foe, motes drifting in, SMITE and BLESSING once a stretch; a choir swell at the cast (C4 and G4, re-struck), a bright C6 note as a foe comes inside, the spark collect a blessing, the swell reversed at a clock close (none on a death); the beam's art out, and no `fx.js` field (the motes are drawn). engine_ab 4218/4218 with Aureole in; the probe 10/10, its two new checks (the voices, the picture's hook, 74 fights drawn) each failed by its own mutants; render_ab 24/24 with a control at 0/6; chain_audit 21/21 with a control; compose6 0 FAIL up to `sc-censer-fxout`. The clip is with Rick. The beam's `fx.js` spec is the orchestrator's to take out at the carry. Review round 2026-09-29: chain_audit now watches the blade (9 of 9 inserts at stage 5); every link unchanged.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`, the BUILD row under the
redesign's). Input: `06-docs/v82/aureole-benediction-redesign-v82.md` (its §5 is the build brief), its
runs `06-docs/v82/runs/halo_base.*` and its lab `tools/overlays/halo.js`, and nothing else (rule 0).
Builder `tools/aureole_build.py` (7cf0a20f6b53a2c3; stages 1-5's was c7641c026661b686), probe
`tools/aureole_probe.py` (fc096aca9624bb99; stages 1-5's was afa389b746f9c12b), runs in `runs/` (stage 6's are
`runs/stage6_*`). **A REDESIGN:**
Aureole ships in the base; its ultimate, the beam, is replaced by the halo. Built in scratch
(`<scratch>/batch/aureole/links/`) on the chain tip `sc-tendril-t3` while other builds ran on the same
tip; the orchestrator carries it onto the chain with the same builder (`--src <tip>`) and proves the
carry with engine_ab.

```
sc-tendril-t3.html          the base: the chain tip (Bindweed stage 5; 38 relics)        5a6216e3b629fad4
  -> sc-aureole-stub.html     stage 1  the halo's ult block, stubbed at 1e9; the beam out   21dc5fe5783980d1
  -> sc-aureole-halo.html     stage 2  the halo and the smite, charge 14 (arm B)            51cd039d45f40521
  -> sc-aureole-bless.html    stage 3  the blessing, bless 0 -> 1 (arm C)                   bdd954b260479136
  -> sc-aureole-b12.5.html    stage 5  the blade 16.01 -> 12.5, to the shipped rate         21ea91d0f3c14274
       -> sc-aureole-b12.5-fx.html   stage 6  the picture and the voice (presentation)   f3228d8d1509edbb   THE FINAL LINK
     sc-aureole-b11.5.html    stage 5 --alt50  blade 11.5, the 50% crossing                 5a3f9c431d30bd7e   Rick's other choice; not the carry
```

The brief's stages are one off the links': its stage 1 (the halo and the smite) is link stage 2, its
stage 2 (the blessing) is link stage 3, its stage 3 (the blade) is link stage 5, and its stage 4 (the
picture, the voice, the carry) is link stage 6. Link stage 1 is the redesign's stub, and there is no
stage 4 (v100's numbering). In §2-§4, written at stage 5, "the final link" is `sc-aureole-b12.5`; stage 6 is
presentation and moves no fight (engine_ab 4218/4218 with Aureole in, §5e), so every number there holds for the
fx link.

**Every link rebuilds byte for byte** from the builder as it stands (`aureole_build.py`
c7641c026661b686), chained from the base into a temporary folder (`runs/rebuild_check4.txt`), and the
five links were then deleted by hand and rebuilt in place with the same five hashes
(`runs/build_fixround.txt`). The builder refuses to overwrite a link, a stage on the wrong stage, a
second stage 1, a name outside `sc-aureole*`, a name 02-chain already has, and a base without
Tendril's ticker. **With stage 6** the builder is 7cf0a20f6b53a2c3: it rebuilds all six links from the base
byte for byte, the five above unchanged, and refuses stage 6 twice, on Rick's 50% link, on any stage but 5 and
on the base (`runs/stage6_builder_checks.txt`, §5e).

**Review round (2026-09-29).** An adversarial review found one should-fix: `chain_audit` never
checked the stage-5 blade, because the blade edit lived only inside a function (`s5_edits`) and
chain_audit reads only module-level insert tables and `*_NEW` constants. The builder now keeps the
carry's blade in a module-level table, `S5 = s5_edits(BLADE)`, as Portcullis's and Bindweed's do:
chain_audit reads 9 inserts, and a tip with the blade put back fails (§4). The change is module data
only, so every link is byte for byte what it was. The review's three notes are taken in §2, §4 and §6.

## 0. What this build stands on

- **The relic** is Aureole as it ships (base line 1026): the sanctified bow, blade 16.01, reach 54,
  width 9, artW 44, spin 2.8, ranged, mass 1.6, onHit smite 1, and the type's shot (cadence 0.34,
  speed 380). Every physical stat, the shot, the channel and the blurb stay; only the ult block
  changes, and at stage 5 the blade. The builder asserts all of it by content, not by which relic is
  last: the row, the shipped Benediction verbatim, the shipped blade, `Fighter.apply(key, n, src)`,
  `stacks`, `STATUS.smite` (4 stacks, 3.2s, 1.5/s) and `STATUS.blessing` (5 stacks, 6s, 1.2/s) as
  priced, tickStatus's blessing heal, and that step()'s window tickers stop in a hit stop.
- **The lab's donor is the relic itself** (`ult_overlay --relic aureole`, no cell): arm A is Aureole
  with no ultimate, SHIP is Aureole with the beam, B/C/D are the halo's arms.
- **The ultimate it replaces, found whole in the base** (`sc-tendril-t3`), and what became of each piece:
  - the ult block `kind:"beam", dmg:15, heal:28` (line 1038): **replaced** by `kind:"halo"`;
  - fireUlt's generic tail, `if (u.heal){...}` (line 17146): **retired at stage 1.** It was Aureole's
    alone: no other ult block carries `heal:` (the builder asserts it, and refuses the base otherwise).
    The tail's `inRange && u.dmg` damage clause **stays**: Goreshard's Bloodprice (`id:"oathwound"`,
    `kind:"beam"`, dmg 16) runs it. `kind:"beam"` has no cast branch of its own, so nothing else goes;
    the heal's pulse field `f.mend` stays too (four other writers and the renderer read it);
  - no ticker, no fighter field, no life-cycle: the beam was instantaneous;
  - **presentation, kept by stages 1-5 and retired by link stage 6** (§5; nothing in the simulation
    reads any of it): the ultFx record's `life` entry `aureole: 1.6` (line 16306); the
    lit ground in `drawUltUnder` (21156) and the lance with its target rings in `drawUltOver`
    (22010), both keyed `u.w === "aureole"`; the charge rune `ULTSIG.aureole` (621, "the halo, and
    the shaft through it"); the cast voice (Aureole has no arm and falls through to rune-crack); and the
    field spec, the inlined `fx.js` copy's `SPECS.aureole` (base lines 32239-32241):

        aureole: { mode: 'beam', n: 1350, sp: [20, 120], grav: -120, drag: 1.2,
                   life: [0.45, 1.10], heavy: 0.0, size: [0.7, 2.0],
                   spawn: 0.55, up: 0 },

    The brief: "Stage 4 — picture (bloom measured), voice, carry; beam's field spec out". The disk
    `src/render/fx.js` still carries the same entry (line 142 then; 136-139 today, Censer's burst out); this build
    touches neither copy, and the orchestrator's `fx_remove.py` takes it out at the carry (§5b).
- **The charge is 14:** the design names none; every arm it priced (`halo_base.json`: charge 16.0,
  dur 8.0) cast every 16 seconds of the lab's step clock, which counts hit-stop freezes. Rick's batch
  ruling converts it. **The census** (a scratch copy of `ult_overlay.py`, `labx.py`, that counts before
  each lab step whether it is frozen, `m.hitStop > 0 || m.latch || m.splitHold`, in total and inside
  windows; 660 fights an arm a block; `runs/lx_ABC_*`): on arm C **10.77% / 10.80% of the lab's steps
  are frozen** (12.32% / 12.25% inside windows, 9.77% / 9.87% outside), so the lab's 16 is the engine's
  14.28 / 14.27, and **14**. Arm B: 10.47% / 10.50% (14.32). The census copy reads ult_overlay's
  arms A, B and C exactly (the win rate, every foe's rate, casts, hits and every stat column; the stats
  differ only by one extra key). The shipped beam also charged 14.
- **Stage 0 on Chromium 151** reproduces the published mechanism (§2); the lab's defaults are the
  settled numbers (`halo.js`: haloR 150, tickCd 0.5, blessCd 0.8; `ult_overlay`: charge 16, dur 8 —
  `halo_base.json`'s own), so no lab flag differs from the design.
- **Names** are free on the base (the builder checks with word boundaries): the kind `"halo"` (no SFX
  kind, no string `"halo"` anywhere in the base's code), the ticker `tickHalo`, the fields `ultHalo`
  and `haloTally`.
- **Readings** (in the builder's docstring):
  1. **The window is 8s.** §1 says "for a duration"; every priced arm used the harness's dur 8.
  2. **The charge** is the lab's 16 converted (above).
  3. **The inside test** is the foe's centre strictly within haloR + R of the caster's centre, on the
     ticker's frame (§4 "inside = foe centre within 150 + R"; the lab's `<`).
  4. **The two cooldowns run through the whole window, inside or not,** and each fires on the first
     inside frame it is clear (the lab's `cd -= dt` every open frame: what was priced). Both start clear
     at the cast (the lab's onCast), so a foe already inside is smitten, and she blessed, on the first
     window frame. They are separate clocks.
  5. **The smite and the blessing are `apply()` and nothing else** (§4 "No damage, no knock, no
     beat"): no hurt, no float, no tag, no stop, no push.
  6. **`apply`'s source is a side letter** (Rick's ruling 4; §4 and the lab pass the Fighter). Smite's
     source is read by one thing, a fatal tick's beat in tickStatus (`st.src === "a" ? a : b`): the
     side letter credits HER side; the lab's Fighter would credit side b every time (probe [8]).
     Blessing's source has no reader.
  7. **No beat.** The halo files none (§4). A smite tick that kills files its own fatal beat inside
     tickStatus, as every smite does: ruling 5 is met by the engine's existing path, and the halo itself
     has no damage path.
  8. **The target is the opponent,** never a Twinshade shade (the lab's `foe`).
  9. **The window closes on its clock or either death** (the lab's); nothing is applied after it.
  10. **No cast waits.** The design asks none, and a cast cannot find its window open: the charge is 14
      of unfrozen time against a window of 8 on the same clock (probe [7] asserts it on every cast).
  11. **No arrows through the halo** (arm D, +1; §6.3 "no, by the numbers"): the bow's shot, its blows
      and its onHit smite 1 are untouched (probe [6]).
  12. **The card** is the design's own, 67 characters: `A halo: foes inside it are smitten, and she is
      blessed while one is`.
  13. **The beam is out** at stage 1 (brief stage 1): the block and the heal; its picture and voice are
      retired and replaced at stage 6 (§5, readings 14-20), and its field spec is the orchestrator's (§5b).
- **The clock:** the window and both cooldowns run on the window tickers' clock, which stops in a hit
  stop (Corollary's, Daybreak's, Zenith's, Canopy's, Onslaught's, Tendril's and the hail's convention).
  The lab ran all three through freezes (§2).

## 1. Stages 1-3, and how they compose

Stage 1 replaces Aureole's ult block with the halo's at charge 1e9 (the clock never reaches it, so
`fireUlt` never runs for her) and retires the heal block. Stage 2 adds `ultHalo` / `haloTally` after
`this.vineTally = null;`, the `kind === "halo"` cast branch before Tendril's, `tickHalo` after
`this.tickTendril(dt);` (so after `ballCollision` and before `tickHits`) and the method before
`tickWinnow(dt){`, and the charge 14, with the blessing written but inert (`bless:0`). Stage 3 is one
character. Stage 5 is the blade. Stage 6 is the picture and the voice (§5).

`tickHalo`, each window frame: the clock (t += dt; the close on dur or either death), then both
cooldowns down by dt, then the inside test, then on an inside frame the smite (cd clear: the foe's
`apply("smite", 1, side)`, cd = 0.5) and the blessing (bcd clear: her `apply("blessing", 1, side)`,
bcd = 0.8). `haloTally` (casts, frames, inFrames, smite, bless, foeStk) is the probe's count; nothing
in the simulation reads it.

**The anchors compose.** Every insert goes after or before a stable line (Aureole's own ult block and
heal block, `this.vineTally = null;`, `    if (u.kind === "tendril"){`, `this.tickTendril(dt);`,
`  tickWinnow(dt){`, Aureole's own blade line), each exactly once or the builder refuses. No insert
names another relic's row. **The carry, dry** (`runs/compose3.txt`, re-run 2026-09-29 with the fixed
builder): stages 1, 2, 3 and 5 apply and parse on thirteen links of the batch's lineage — the base, the
newest real tips `sc-angelus-b9-fx` (85b8af63055d1108, 42 relics) and `sc-oracle-fx` (41),
`sc-widowmaker-fxout` (40), `sc-ironhail-fxout`, `sc-ironhail-sunder-fx`, `sc-lodestone-b205-fx`, and
the scratch tips of Angelus, Censer, Coldiron, Lightkeeper, Oracle and Widowmaker — and every one
takes the same 90 changed lines (md5 5993d6de9fe4; the earlier eleven-tip run is `runs/compose2.txt`).
The builder's scans: no insert draws the RNG, takes the ultFx slot, writes the
shared weapon (`w.dmg/spin/reach/blades =`), hurts, knocks, stops, files a beat or moves a ball; one
`kind:"halo"`; no `u.heal` and no `heal:` left; the Math.random count unchanged; node --check; LF.

## 2. Stage 0 and the stages against it — the window clock, measured

`ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic aureole --mech overlays/halo.js
--arms A,SHIP,B,C,D --seeds 20 --foes <33>`, seed0 2207 and 2317, 660 fights an arm a block
(`runs/s0_*`). The foes are the design's roster: the 34-relic roster minus Aureole. The built links run
`--arms SHIP` on the same foes and seeds; a third block (2427) and a fourth (2537) were added for the
gap (`runs/s0x_BC_*`, `runs/built_*`).

```
                          lab on 151 (2207 / 2317)   published 141   BUILT (2207 / 2317)          four blocks, pooled (2640)
A   no ultimate           34.7 / 32.0                27.9            stage 1: 34.7 / 32.0         identical, fight for fight
SHIP the beam (16.01)     53.5 / 52.1                55.5
B   smite inside          55.0 / 51.5                49.7            stage 2: 53.6 / 53.2         built 51.4, lab 51.0
C   + the blessing        72.6 / 72.3                69.4            stage 3: 73.8 / 73.2         built 72.6, lab 70.9
D   + blessed arrows      72.9 / 72.0                70.6            (not taken, §6.3)
```

Blocks 2427 and 2537: lab B 48.3 / 49.1, C 69.2 / 69.4; built stage 2 49.7 / 49.2, stage 3 72.6 / 70.9.
**The brief's gates:** stage 2 (its stage 1) "foe inside ~36%, ~7.7 smite a cast, relic ~50% at 16.01" —
the relic reads 51.4 (lab 51.0); stage 3 (its stage 2) "~5.8 blessing a cast, relic ~69%" — 72.6 (lab
70.9). The mechanism columns read lower (below), for a measured reason.

**Stage 1 is arm A fight for fight** on both blocks: 660/660 fights each, every winner, duration to
the step, blow counts in and out and casts identical, and every foe's rate the same
(`runs/stage1_vs_A_perfight.txt`, the census copy's per-fight rows against the stub's).

**Published against 151** (`runs/pub_vs_151.txt`): the published run's own 330 fights (sc-trunk,
10 seeds) replayed on 151 read A 33.0, SHIP 55.8, B 53.9, C 69.1, D 69.4 against the published 27.9 /
55.5 / 49.7 / 69.4 / 70.6 — 3 to 10 of 33 foes identical, the runtime moving single fights — and the
mechanism to the digit: C smite 7.95 a cast (7.93), blessing 5.85 (5.82), the foe inside 36.6% of
window frames (36.4), 3.48 smite stacks on a window frame (3.47). On the chain tip (38 relics) the
same arms read A 33.3, SHIP 52.8, B 53.3, C 72.4 pooled.

Lab mechanism on 151 (arm C, block 1 / 2): 3.02 / 3.01 casts; smite 7.80 / 7.74 and blessing
5.74 / 5.71 a cast; the foe inside 36.0 / 35.7% of window frames; 3.47 smite stacks on a window frame.

**The built relic reads the lab's arm within noise, and the mechanism columns read lower for one
measured reason: the lab counted frozen frames.** The probe, run on the lab's own 660 fights (side A,
the same seeds), gives the same win rate as ult_overlay on the link over the same 660 fights, to every
digit: 0.536364 / 0.531818 (stage 2, 2207 / 2317) and 0.737879 / 0.731818 (stage 3). Neither run keeps
a per-fight row, so that is equality of the totals, not a fight-by-fight comparison (stage 1 against
arm A, above, is one). It reads on stage 3: 5.51 blessing and 7.23 smite a cast, the foe inside 30.5% of window frames, 12.8%
of window steps frozen, a window 9.11s of match time. The lab's window was 8 step-seconds with 12.3%
of them frozen, so ~7.0s of play; the engine's is 8s of play, ~9.1s of match time.

**Where the lab's halo ticked** (`tools/halo_split.js` in `runs/`: `halo.js` unchanged in what it does,
plus counters that split the lab's window frames by whether the step that made them was frozen; its
arms give the lab's win rates and every foe's rate exactly; `runs/lab_split_BC_*`, blocks 2207 / 2317):

```
                                         arm B           arm C
lab window frames that were frozen       12.1 / 12.1%    12.4 / 12.3%
foe inside, on the frozen frames         74.7 / 74.3%    75.2 / 75.0%
foe inside, on the unfrozen frames       29.9 / 29.6%    30.7 / 30.4%     the engine's (probe): 29.4 / 30.5%
smite a cast (of it, in a freeze)        7.59 (0.87) / 7.56 (0.84)    7.80 (0.92) / 7.74 (0.88)
blessing a cast (of it, in a freeze)          -          5.74 (0.58) / 5.71 (0.55)
```

**A freeze is a contact.** The hit stops fall where the balls meet, so the foe is inside the halo on
three frozen frames in four, against one unfrozen frame in three. The lab's "36% inside" is the
engine's 30% plus its frozen frames; about 11-12% of the lab's smites and 10% of its blessings landed
in a freeze, which the engine's halo cannot do (its window tickers stop), and its cooldowns also ran
down through freezes, so they fired sooner in play time. The engine gives it back as length: its
window is 8s of play, ~9.1s of match time, against the lab's ~7.0s of play. Per cast, the build lands
7% fewer smites and 4% fewer blessings than the lab (7.23 / 5.51 against 7.80 / 5.74) over a window
14% longer in play.

**The controls** (blocks 2207 / 2317 / 2427 / 2537, 660 fights each; `runs/lab_scaled_BC_*`,
`runs/ctl-lab-*`, `runs/built_*`, `runs/s0*`):

```
                                                    B                                  C
lab (the design's arm)                              55.0  51.5  48.3  49.1   51.0      72.6  72.3  69.2  69.4   70.9
BUILT (stage 2 / stage 3)                           53.6  53.2  49.7  49.2   51.4      73.8  73.2  72.6  70.9   72.6
the build on the lab's clock (tickHalo also runs    48.6  49.5  49.8  48.3   49.1      71.5  73.2  74.1  70.9   72.4
  on every frozen step: clock_variant.py)
the lab at the engine's window (dur 9.12, tickCd    55.6  51.7  51.5  55.6   53.6      78.0  75.9  74.1  73.5   75.4
  0.570, blessCd 0.912: x 1/(1-0.123))
```

- **The build on the lab's clock is the lab.** Its win rate sits within noise of the lab's arms (49.1
  against 51.0, 72.4 against 70.9; one standard error of a four-block arm is ~1 point), and the probe on
  it, on the lab's own 660 fights (2207), gives back the lab's mechanism columns: stage 3 the foe inside
  35.7% (lab 36.0), smite 7.68 (7.80), blessing 5.68 (5.74), a window of 7.99s of match time; stage 2
  34.5% and 7.52 (35.2, 7.59) (`runs/probe_lab_ctl-lab-*`; the probe fails [1] on it, as it must).
- **The built relic reads its lab arm within noise** (+0.4 at B, +1.7 at C). The two halves of the
  window clock pull opposite ways and nearly cancel: the longer window in match time is worth +2.3
  (B) and +0.2 (C) over the build on the lab's clock, where Canopy's and Tendril's were worth ~+9 and
  ~+11 — the halo's work is capped by its cooldowns and done only while the foe is inside, and the
  lab had spent 11-12% of it inside freezes.
- **Scaling the lab's window alone over-predicts** (+2.6 at B, +4.5 at C): it keeps the frozen-frame
  ticks and adds the length. That is why this control, which settled v101's gap, does not reproduce the
  build here; the build-on-the-lab's-clock control and the split do.
- **Nothing is mis-built:** the probe (§3) rebuilds every tick, and the only difference from the lab's
  mechanism is the clock, which is the engine's convention.

**What the build does with it.** It keeps the engine's convention (every window cadence in the batch
runs on the window tickers' clock, and a freeze freezes the world) and every designed number. The
brief's blade stage then prices the built relic.

## 3. The probe (`aureole_probe.py`, one check per sentence, read inside the hooks)

It wraps `tickHalo`, `fireUlt`, `tickWeapon`, `tickFire`, `resolveHit`, `tickStatus`, `beat` and
`step`, and plays Aureole against every other relic, both sides (6 seeds, 444 fights), or with
`--sides A --seedstep 11 --foes <33> --seeds 20` the lab's own fights.

- **[1] "For a duration a halo stands around Aureole":** the window's clock advances by exactly dt a
  call, closes on dur or either death and never outlives them; `tickHalo` is asked exactly once on every
  unfrozen step and never on a frozen one (counted by the step wrapper); only Aureole carries `ultHalo`.
- **[2] "an enemy inside the halo":** the engine's inside flag (`inFrames` rising) is the rebuilt test on
  every window frame, the foe's centre strictly within haloR + R (inside by the rim alone is exercised).
- **[3] "is smitten for as long as it stays there":** the smite's cooldown rebuilt on every window frame
  (cd - dt <= 0 on an inside frame: exactly one `apply("smite", 1, side letter)` on the foe and cd =
  0.5; otherwise none and cd - dt); the stacks and clock after it the engine's; none outside, none on
  anybody else.
- **[4] "and for as long as an enemy is inside it, Aureole is blessed":** the same for the blessing on
  its own cooldown (none at bless 0); and it is her only heal: every tickStatus of hers heals by exactly
  hps x stacks x dt, rebuilt.
- **[5] "No damage, no knock, no beat":** a tickHalo call hurts nobody, moves, turns, stuns or pins no
  ball, changes no hp, ward or ward pool, stops nothing, files no beat, draws no rng, spawns no shot and
  applies nothing else.
- **[6] no arrows through the halo** (§6.3): the bow's spin as ever, its fire asked once a step with the
  cadence rebuilt, every blow's damage rebuilt from its captured crit and jitter draws, and each blow's
  statuses exactly the channel's smite 1 — in the window and out.
- **[7] the beam is out:** a cast spawns no shot, hurts, heals or applies nothing, opens {t 0, dur, cd 0,
  bcd 0}, never lands on an open window; the ult block is the design's (no dmg, no heal).
- **[8]** a smite tick that kills her foe files its fatal beat for HER side (reading 6).

```
                              fights   casts   smite/cast  bless/cast  foe inside  frozen   window     win
sc-aureole-halo  (stage 2)     444     2.86      7.06        0.00        30.0%      12.5%    9.09s     52.7%    8/8
sc-aureole-bless (stage 3)     444     3.04      7.24        5.50        30.9%      12.9%    9.11s     72.7%    8/8
sc-aureole-b12.5 (stage 5)     444     3.34      7.50        5.66        32.4%      12.8%    9.10s     58.8%    8/8
lab's fights, stage 2 (2207)   660     2.89      7.02        0.00        29.4%      12.5%    9.07s     53.6%    8/8
lab's fights, stage 2 (2317)   660     2.87      7.01        0.00        29.3%      12.5%    9.08s     53.2%    8/8
lab's fights, stage 3 (2207)   660     3.07      7.23        5.51        30.5%      12.8%    9.11s     73.8%    8/8
lab's fights, stage 3 (2317)   660     3.04      7.22        5.49        30.4%      12.9%    9.12s     73.2%    8/8
```

On the final link: 1217 clock closes and 141 death closes; 1,291,901 open-window frames, 2,853,859
unfrozen steps each with one tickHalo call; 1,454,042 blessed tickStatus frames rebuilt exactly; 101
fatal smite ticks credited to her side; 3799 blows in windows and 4505 outside, each rebuilt.

**Mutants** (scratch copies of the final link, `mut/`, `runs/probe_mut-*.txt`; each breaks one sentence
in a way that changes fights, and must fail its own check and only that one):

```
mutant (tools: mutants.py)   the one thing broken                                   fails          Aureole (final 58.8%)
m1-frozen    3d9ef0ea4b3fc541  tickHalo also on every frozen step (the lab's clock)   [1] only, 712,886   52.5%
m2-radius    38309b3ed9cd1775  inside within haloR + 1.25 R                         [2] only, 35,572    60.6%
m3-cadence   e67a321ceb7e5f04  the smite every 0.4s, not tickCd                     [3] only, 12,594    57.7%
m4-blessout  6cdfcb18253a7e6b  blessed every blessCd whether or not a foe is inside [4] only, 18,570    66.2%
m5-hurt      8b9e709a70accf3d  each smite also hurts the foe for 1                  [5] only, 21,558    68.9%
m6-arrows    336ffa2bf1a4f5d6  a blow in the window smites +1 more (arm D)          [6] only, 3,777     59.9%
m7-beamheal  d4185a96ceaead6b  the cast still heals 28                              [7] only, 1,447     72.7%
```

Seven, one a sentence (the redesign's "the beam is out" among them); each changes fights (the same
444 fights move from 58.8% to 52.5-72.7%) and fails its own check and no other. [8] has no mutant of
its own: a Fighter as the smite's source would credit side b, and [8] is exercised on every run (101
fatal smite ticks on the final link, each credited to her side). m1 also doubles as the mechanism
control: on the final link's fights it reads the foe inside 37.1% of window frames, 7.93 smite and 5.83
blessing a cast — back at the lab's columns (36.0, 7.80, 5.74), where the engine's clock reads 32.4, 7.50
and 5.66 on the same fights.

## 4. Stage 5: the blade — 12.5, to the shipped rate

**The target is the design's own** (§5 "the blade, wide on 151 at 13.5 / 14 / 14.5 to the shipped
rate"; §3 "settled wide to the shipped rate"): Aureole as shipped (the beam at 16.01) on the base,
`relic_rate` both sides, two blocks, **801 of 1480, 54.1%** (56.8 / 51.5; `runs/rr_shipped_*`).

Both sides (`relic_rate.py --game sc-aureole-bless.html --relic aureole --n 10 --set dmg=X`, each seed
from both sides, every other relic a foe, 10 seeds a foe a side, 740 fights a block, seed0 2207 and
2317; `runs/stage5_rr_d*`, table `runs/stage5_table.txt`):

```
blade                      block 1   block 2   pooled (1480)        side A   side B   mean     against the shipped 801
16.01 SHIPPED (the beam)   56.8      51.5      54.1 (801)           53.8     54.5     56.5s    the target
16.01 the halo             74.7      71.9      73.3 (1085)          75.5     71.1     55.9s    +284
14.5  the brief's grid     69.5      67.2      68.3 (1011)          68.9     67.7     58.2s    +210
14    the brief's grid     64.9      68.2      66.6 (985)           66.5     66.6     58.9s    +184
13.5  the brief's grid     61.1      61.9      61.5 (910)           61.1     61.9     59.2s    +109
13                         57.4      58.0      57.7 (854)           58.6     56.8     60.1s    +53
12.5                       55.8      56.4      56.1 (830)           56.2     55.9     60.9s    +29     <- THE BLADE
12                         50.5      53.5      52.0 (770)           52.7     51.4     61.6s    -31
11.5                       48.2      49.3      48.8 (722)           48.1     49.5     62.1s    -79     <- the 50% alternative
11                         48.0      46.4      47.2 (698)           47.4     46.9     62.8s    -103
10                         37.0      36.5      36.8 (544)           34.6     38.9     64.2s    -257
```

- **The brief's grid is all above the target.** The design's "about 14" took back a lab gap priced on
  141, side A (C 69.4 against a SHIP of 55.5). On 151, both sides, the halo at the shipped blade reads
  73.3 against the shipped 54.1, so the crossing of the shipped rate falls at ~12.4, under 13.5.
- **The brief names no knob to move first**, so the blade moves outside the grid, inside the bow row the
  design names (§3: "the bow row 9.5-16.2"), and it is said here. The grid was extended down on the
  same blocks, and nothing else moves.
- **Blade 12.5 is the measured point nearest the shipped rate:** 56.1% (+29 wins), against 12's 52.0%
  (-31). Two wins apart, inside one standard error (~19 wins); every tiebreak points the same way (the
  nearer to the design's "about 14" and to the brief's grid). Side A 56.2, side B 55.9.
- **The 50% crossing** (the batch's standard for a new relic, Rick's other choice) is ~11.7, between 12
  (52.0, +30 wins over half) and 11.5 (48.8, -18): **11.5** is the nearer. `--stage 5 --alt50` writes it
  (`sc-aureole-b11.5`, 5a3f9c431d30bd7e); it is not the carry.
- **The built link is the measured relic:** `relic_rate` on `sc-aureole-b12.5` with no knob set gives
  both blocks exactly (55.81% / 56.35%, side A 55.95 / 56.49, side B 55.68 / 56.22, mean 60.886122s /
  60.814135s, all 37 foes and every type; `runs/stage5_rr_proof_b12.5.txt`). So does the 50%
  alternative, `sc-aureole-b11.5`, against `--set dmg=11.5` (48.24% / 49.32%, mean 62.137257s /
  61.974378s; `runs/stage5_rr_proof_b11.5.txt`).
- **Against the reference:** Aureole as shipped reads 54.1% both sides on the base (side A 53.8, side B
  54.5); the redesign at 12.5 reads 56.1% (56.2 / 55.9), at the shipped 16.01 73.3%. Her fights run
  longer: 60.9s against the beam's 56.5s (55.9s for the halo at 16.01).

**The ladder at 12.5** (40 fights a foe, both blocks, both sides; `runs/ladder_final.txt`), beside the
shipped beam's:

```
by type       halo 12.5   the beam 16.01
warhammer     65.8%       59.6%    +6.2
flail         62.1        64.6     -2.5
scythe        61.1        58.9     +2.1
twinblade     53.5        50.5     +3.0
bow           46.5        46.0     +0.5
greatsword    45.4        42.5     +2.9
```

By foe: best Bloodmirror and Bindweed 90%, Vinesower and Thornshear 80, Ironwood 77.5; worst
Lightkeeper 20%, Starwarden 25, Ironhail and Gloamwire 30, Dawnbringer and Emberedge 35. The largest
moves from the beam: Axiom +25, Bloodmirror +20; Bulwarden -17.5, Gravemourn, Cindercleave and
Gloamwire -15. The type spread is 20 points (the beam's 22). The full table is in the run file.

- **engine_ab sc-tendril-t3 → sc-aureole-b12.5, the 37 others, n=6: 3996/3996 identical** (666
  pairings, 37/37 distinct winners, 3996 distinct seeds, 20.8-111.2s; `runs/engine_ab37_final.txt`,
  ids `runs/ids37.txt`). The redesign moves no other relic's fight. **Control:** the same gate with
  Aureole among the ids (Aureole, Grudgebearer, Gravemourn, Bindweed, n=6) **fails: 18 of 36 differ**,
  exactly Aureole's 18 (`runs/engine_ab_control.txt`).
- **verify --n 40 on sc-aureole-b12.5 (38 relics): 10/13** (`runs/verify_final.txt`; 28,120 fights).
  Aureole 55.7% (the base's verify: 56.3%); every relic in 30-70% (Heartwood 30.5 .. Gloamwire 63.5,
  spread 33.0pp; the base's 30.5 .. 63.7). The three reds are the base's own, none of them Aureole's:
  the two clock bands (every link since the minute pace; mean 61.0s, the base's 60.8), and "both sides
  can win every matchup" on **Heartwood v Twinshade 0/40 and Heartwood v Bindweed 0/40** — the same two
  pairings on `sc-tendril-t3` (v101 §4), which engine_ab shows are the same fights here. Item 12/32,
  Rick's.
- **tip_audit:** identical to `sc-tendril-t3`'s below the header (the one field no tip mentions is
  still Ward's `bank`, by design; `runs/tip_audit_final.txt`, `runs/tip_audit_base.txt`). The halo adds
  no status and changes none.
- **chain_audit** `--relic sc-aureole-b12.5 --tip sc-aureole-b12.5 --builder aureole_build.py`
  (c7641c026661b686): **all 9 inserts survive**, exit 0 (`runs/chain_audit_final.txt`): S1's two, S2's
  five, S3's one and **the blade, `S5:the blade: to the shipped rate`**. The first build of this doc
  read 8 and did not say the blade was unwatched: its edit lived only inside `s5_edits()`, which
  chain_audit cannot see (the review's should-fix; the builder now keeps `S5 = s5_edits(BLADE)` at
  module level, and `--alt50` deliberately stays out of it, since the carry is 12.5). **Controls, each
  of which can come back wrong:**
  - **the blade put back.** The final link with Aureole at dmg 16.01 again (which is stage 3's bytes
    exactly, bdd954b260479136) as the tip: `LOST S5:the blade: to the shipped rate`, the other 8 ok,
    exit 1 (`runs/chain_audit_blade_control.txt`);
  - **the base.** `sc-tendril-t3` as the tip loses all 9 and exits 1 (`runs/chain_audit_control.txt`);
  - **the heal put back (what chain_audit cannot see).** Stage 1's retirement of fireUlt's
    `if (u.heal){...}` block is a deletion, so it leaves no code line and chain_audit marks it by its
    comment alone: the final link with the block restored under that comment (e2222f4b44443b83) still
    reads all 9 surviving, exit 0 (`runs/chain_audit_heal_control.txt`). What watches it instead: the
    builder refuses to write any stage while `u.heal` or an ult block's `heal:` remains, and probe [7]
    checks that a cast heals nothing. A restored block would also do nothing: no ult block carries
    `heal:`, and the halo's cast branch returns before the generic tail.

## 5. Stage 6: the picture and the voice — `sc-aureole-b12.5-fx`

Design §4 (the picture, the sound) and its §5 brief stage 4, "picture (bloom measured), voice, carry; beam's
field spec out", this build's link stage 6. Picked on measurements under Rick's "you pick i overrule" by two
labs run in parallel (the picture lab's scratch, `au_rows.py` 53b9990b537d939e, and
`tools/aureole_voice_lab.py` 98d45f69e0a1e718), and built as `aureole_build.py --stage 6` on the final
stage-5 link (the b12.5): **thirteen anchored edits (voice 4, picture 9)**, byte-exact to the labs' own row
files (voice `rows_final.json` 5a43210cd9d13019, picture ed67bd6722cbbe2b; copied as
`runs/stage6_voice_rows.json` and `runs/stage6_picture_rows.json`). The reports the two labs returned, as the
orchestrator relayed them, are the files: their first 5000 and 6996 characters are the files' own JSON,
character for character, and a one-character change fails the check (`runs/stage6_check_inline.txt`).

```
sc-aureole-b12.5.html          stage 5  the blade (the base of stage 6)                     21ea91d0f3c14274
  -> sc-aureole-b12.5-fx.html  stage 6  the picture and the voice (presentation)          f3228d8d1509edbb
```

- **The rows, reproduced** (`runs/stage6_gen_s6.txt`; the generator is `runs/stage6_gen_s6.py`, the pattern's:
  rows == files, the stamps, no nested anchor, merge by anchor, a `--stage 6` that refuses to run twice and
  scans S6 for `ultFx`): the picture rows alone give the picture lab's stamp, **b8d571f46a2681af** (its
  `au-final.html`, byte for byte); the voice rows alone the voice lab's end-to-end page,
  **50d4b2dfd385397e**; both sets, either order, **f3228d8d1509edbb**, the fx link. No two rows share an
  anchor, so none is merged; no row's anchor sits inside another row's anchor or code, and no two anchors'
  spans overlap. **Nine re-emit their anchor and four replace it**, all four Aureole's own: the beam's two
  art branches (the lit ground, the lance), `ULTSIG.aureole`, and the life map's narrowest token
  `aureole: 1.6, ` (Consecration's entry on the same line is left to its own build). Eighteen new names,
  each free on the base on identifier boundaries and each in the page after.
- **Composition.** The Sfx row goes BEFORE the shared rune-crack fallback, which it re-emits unchanged, so the
  11 other relics that still fall through keep it (Lastlight, Spellbreaker, Ironhail, Lightkeeper,
  Farwarden, Censer, Oathwound, Heartwood, Gloamwire, Portcullis, Bindweed) and another relic's arms anchored
  there apply in either order. The three voice rows on the sim path ride on stage 2's own lines inside
  `tickHalo` (the inside test, `T.bless += u.bless;`, the window's close); the picture's fields follow stage
  2's fields; its call and methods sit beside shared lines (`tickPresentation`'s first call, `tickWinnow`,
  `drawTree`, `drawMotes`) and re-emit them. **compose6** (`runs/stage6_compose6.txt`, 0 FAIL): stages 1, 2, 3,
  5 and 6 on nine real tips on `02-chain` — up to the newest, **`sc-censer-fxout`** (00a2e2e10448c492, 42
  relics: Censer carried, its field removed) — and on six scratch tips; with the two builders still in
  progress (Heartwood and Spellbreaker, at their stage 3) both ways. On every tip the change set of stages
  1-5 is t3's (a73d17141fe14b0a; sha256 of the sorted diff lines, the same set compose3's md5 5993d6de9fe4
  names), and the change set of stage 6 alone is t3's (91a52fd6cfebc2bf, 406 lines) on every tip **but the
  three that carry Censer's stage 6** (`sc-censer-fxout`, `sc-censer-consecration-b25.5-fx`, Censer's scratch
  fx link: 5d7927576f9c60e1), where only the life map's line differs: Censer has already taken its own
  `censer: 1.6,` out, so after Aureole's token goes the line is left holding its indent alone. It parses and
  nothing reads it; a cosmetic blank line the carry may tidy. The picture lab also carried its rows with the
  voice rows onto 18 tips and scratch pictures, both orders equal (`runs/stage6_picture_order2.txt`).
- The picture sheet is `05-reference/v110/aureole-picture-sheet.png` (4184dbf043667d5e, 2200x2688); the voice
  lab's wavs are `05-reference/v110/aureole-*.wav` (34 files, raw level; gitignored).

### 5a. The picture

Every number here is the picture lab's: headless Chromium 151 at 540x960 with the post chain on (m2: 10
fights, 96 frames, white, dark and ordinary foes; `runs/stage6_picture_m2_summary.txt`), on its shipped-look
page (the rows, with the beam's `SPECS.aureole` taken out of the inlined `fx.js` as the carry will:
a213880cc8e38ffe).

- **A ring, not a disc, and the ring is the simulation's halo** (reading 16): a 10-unit band at `haloR` read
  live off the relic (150), centred on Aureole, so the drawn ring is where `tickHalo` tests: a foe is inside
  (its centre within haloR + R) from the moment its shell reaches the middle of the band. In the school's glow (sanctified:
  #FFFFFF) at **0.4, and 0.7 while a foe is inside** — the tell that the blessing is running — with the hole
  cut in the path (a radial gradient with an inner radius still fills its inner circle: CLAUDE.md 4.1b), a
  drawn falloff 6 units either side in the school's core (#FFF6E2, 0.12 of the band), and **a 0.04 wash**
  inside it (the design's interior wash). The world pass, under both balls, source-over only, clipped to the
  live hall: nothing under `lighter` and nothing the bloom sees.
- **The ring grows out of the ball over 0.3s at the cast and shrinks back into it over 0.3s at the close** —
  a clock close, a death or the verdict (ease-out, from the shell's radius to 150) — on the presentation clock,
  which runs through the cast's own 0.08s hit stop. `tickHalo` never runs once `over` is set, so a halo
  standing at the kill would otherwise stand through the verdict (reading 14).
- **What the halo does, shown** (reading 15): the band brightens 0.4 → 0.7 over 0.1s as a foe comes inside
  and falls back over 0.25s after it leaves; **a foe inside wears a rim of the light**, a gradient from its
  shell out 7 units (the glow at 0.5 of the brightening), drawn under its ball with the hole cut at the shell,
  so it can only be a rim whatever the school (m1 had the hole at R - 1, and the rim showed +0.012 on a white
  foe's disc in a hit stop: it moved to R). **SMITE n on the foe at the first smite of each inside stretch,
  BLESSING n on Aureole at the first blessing of each** (the tag rule of Corona, Daybreak, Zenith and Canopy),
  both re-armed the first step the foe is out. "Inside" is `tickHalo`'s own test as it ran, found by watching
  `haloTally` rise (a step the window ticked is inside iff `inFrames` rose with it), and it holds through a
  hit stop as the halo does; so the ticker makes no call for the picture.
- **The field, drawn** (5b): 24 motes born just outside the band drift 30 units in along it and fade in and
  out, placed by `shellHash` on the match clock (the death clock after the kill): no RNG, and they keep
  moving through a hit stop.
- **The beam's art is retired** (reading 20): `drawUltUnder`'s lit ground (a 150-unit pool at the target, for
  every cast's 1.6s), `drawUltOver`'s lance along the shot line with its target rings and the heal's rings
  closing into the caster (under `lighter`), and the life map's `aureole: 1.6` (the cast's record falls to
  the map's own 1.5, and nothing draws from it). **The charge rune, `ULTSIG.aureole`, is redrawn:** the halo
  round the ball, the monstrance's six rays out of it and five motes drifting in to the ball, brightening as
  the charge fills (the beam's shaft gone).
- **The silhouette is left alone:** Aureole's resting bow reads |dL| 0.217, 1st of the 6 bows (Farwarden
  0.187, Vinesower 0.186, Marrowdraw 0.122, Gloamwire 0.099, Ironhail 0.093; `runs/stage6_picture_sil.txt`).
- **The art hangs off the Fighter** (`beneFade`, `beneAge`, `beneOut`, `beneIn`, `beneLit`, `beneSeen`,
  `beneTagS`, `beneTagB`), never off `m.ultFx` (open item 25); `tickBenediction` drives it in
  `tickPresentation`, and `drawBenediction` draws it with one method a component (`_beneGeom`, `_beneWash`,
  `_beneRing`, `_beneMotes`, `_beneRim`), so each can be measured alone.
- **Bloom** (the design's gate, ≤ +0.02): the picture's share of the chain's arena lift **max +0.0004** (min
  -0.0011; the worst a Gravemourn fight out of a hit stop); the raw luma it adds (chain off) at most +0.0223.
  **Three controls, each failing:** the halo as a filled white `lighter` disc at 0.35 lifts +0.0712 (past
  0.02 on 16/96 frames) and pushes Aureole's disc past 0.90 on 49/80 window frames; a white-hot `lighter`
  glow on her, 65/80; the rim as a filled white `lighter` disc over the foe pushes the foe's disc past 0.90 on
  22/30.
- **No disc erased:** the art lifts her disc at most +0.0021 and a foe's at most +0.0179 (white Dawnbringer,
  in a hit stop), and no frame is newly past 0.90 (hers 5 with / 6 without of 96; the foe's 4 / 4). By the
  foe's school: dwarven 0.0081, runic 0.0008, sanctified 0.0179, umbral 0.0028, verdant 0.0005 at most.
- **Legibility** (median |dL| of each component's own pixels, out of a hit stop / in one): **the ring 0.239
  with the foe out, 0.344 with it in (the tell)** — 0.236 / 0.318 in a stop; the ring growing at the cast
  0.235 (0.115 in the cast's own stop), closing 0.238; the motes 0.234 / 0.231; the tags 0.282 / 0.317; the
  foe's rim 0.096 / 0.088; the wash 0.033 / 0.032 (the design's 0.04 is a wash, and reads as one).
- **Whole fights** (the lab's verify, `runs/stage6_picture_verify.txt`: 15 fights, 13 with Aureole on both
  sides and 2 without, each as the base, the rows, the shipped look, and the shipped look drawn through the
  renderer): **the simulation identical to the base in all 15**, hash at the kill, steps and result. Drawn
  through the kill and 3s of the verdict: 19,933 frames, nothing thrown; "inside" equal to `tickHalo`'s own
  test on 40,952 ticked steps; one SMITE and one BLESSING tag per inside stretch, exactly; the ring at
  `haloR` on every fully grown frame; closes 0.29-0.38s (0.575 once, through hit stops); at the kill the ring
  contracts in 0.29s; the weapon row never written. **Control:** a copy that nudges the foe 1e-9 at a SMITE
  tag differs on all 13 Aureole fights and not on the 2 without.
- **The lab's own render_ab**: 77/77 frames pixel-identical on 11 pairs without Aureole (Censer's 1.6 kept);
  two Aureole pairs 0/7 and 0/7 (`runs/stage6_picture_renderab.txt`); and its own `engine_ab` on the shipped
  look, 38 relics, 4218/4218 (`runs/stage6_picture_engine_ab38.txt`).
- **Frame cost: not measured** (deferred by the orchestrator; no Electron was launched in the final round).
  The lab's first attempt ran one informally before that ruling; it is not quoted. §6.

**Readings declared** (the builder's docstring, 14-20; art and sound are Code's picks):
14. The picture reads the window off `ultHalo && alive && !over` and keeps its own state on the fighter; the
    ring grows out of the ball at the cast and shrinks back into it at the close, a death or the verdict.
15. Inside is `tickHalo`'s own test as it ran, read off the tally; the brightening and the foe's rim; the tag
    rule; the picture writes its `bene*` fields, the tags and `taught` only, and draws no RNG.
16. A ring, not a disc: the band at `haloR` read off the relic, a 0.04 wash, motes drifting in; world pass,
    under both balls, source-over only.
17. The voices on the sim path are three things inside `tickHalo`: the entry (the ticker's own test repeated,
    its answer kept as `voiceIn` on the window's record), the heal chime, the close voice; the cast's voice is
    `fireUlt`'s own.
18. No close voice on a death: the death voice has that moment; a halo still up at the fight's end closes in
    the picture only.
19. No `fx.js` field; the beam's `SPECS.aureole` is the orchestrator's to take out.
20. The beam's art is retired with the beam; the charge rune redrawn.

### 5b. No new `fx.js` field: the motes are drawn, and the beam's spec goes out of both copies by the orchestrator

The design asks for "motes drifting inward along the ring (both copies)". A SPECS field fires once, at the
cast, from the one `m.ultFx` slot, where the caster stood. The picture lab measured what that slot gives this
relic over 113 Benediction windows (16 foes x 2 seeds, both sides; `runs/stage6_picture_fxprobe.txt`):
- the slot is Aureole's a median **0.68s** of the window clock (max 0.72; the window is 8s): a field borne on
  it could exist for **7.9%** of the window; the opponent's cast took it in 16 windows, and it expired in 95;
- the ring rides her and she moves: her centre stands a median 203 units from the field's spawn point (p10
  65, p90 401), and **after the first second a median 214 (p90 411), more than the ring's own radius on 69%**
  of those samples — a field spawned at the cast would drift inward along a ring that is no longer there.

So the motes are DRAWN, off the ring itself, in the world pass (5a): the Zenith, Canopy, Tendril,
Quarrelstorm, Ascension, Bulwark and Consecration precedent. **Rick's to overrule.**

The beam's own spec, `SPECS.aureole`, is the brief's "beam's field spec out". `fx.js` is shared by every
build in the batch, so this builder never edits it, and stage 6 refuses to write if its inlined copy moved
(reading 19). The orchestrator takes the entry out of both copies with `fx_remove.py --relic aureole` at the
carry. Its exact text, with the comment `fx_remove` takes with it:

```
    /* Negative gravity is what stops a beam reading as an explosion pointed
       sideways. */
    aureole: { mode: 'beam', n: 1350, sp: [20, 120], grav: -120, drag: 1.2,
               life: [0.45, 1.10], heavy: 0.0, size: [0.7, 2.0],
               spawn: 0.55, up: 0 },
```

The b12.5 32307-32309 and the fx link 32557-32559 (the entry's three lines); `src/render/fx.js` on disk
today (866f45e37dc54e3f, Censer's burst already out) still carries it. **Tried in scratch twice**
(`runs/stage6_fx_remove_scratch.txt`; `fx_remove.py --fxjs` on copies, the real `fx.js` untouched):
- on the fx link, with `fx.js` at the stamp its inlined copy carries (git edd6400, 28fc58641370a1a9): the
  block comes out whole, only the block and the two stamps move (→ 813fe9b101be3878), the page becomes
  66c384110868783b;
- **the carry, dry, on the newest real tip:** stages 1, 2, 3, 5 and 6 on `02-chain/sc-censer-fxout`
  (00a2e2e10448c492) → e373cf79dc779466, then `fx_remove` with a copy of today's `fx.js`
  (866f45e37dc54e3f → fd4932c664fcbac9): the page afa83ad4a4f56ca7.

The page is safe without it (`sync` returns on a missing spec); the picture lab's `engine_ab` (4218/4218) and
whole-fight identity ran on its own spec-out page. **Until the carry, the stage-6 link still fires the beam's
particles at every cast, and so does the clip (5f).**

### 5c. The voice

Every number here is `tools/aureole_voice_lab.py`'s (98d45f69e0a1e718; its final run, round 5, Chromium
151.0.7922.34; `runs/stage6_voice_lab.txt`; every render an OfflineAudioContext at 48 kHz through
`Sfx.buildChain`, a candidate rendered from its arm's own text). Its controls reproduce the six published
numbers (rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, hit@11.6 0.443 / 80 ms), and levels are read
against Aureole's own blow at 12.5 (its loudest 50 ms 0.1176-0.1234 over 12 draws).

- **The cast, "a soft choir swell (two re-struck tones, a fifth), 0.5s" — PURE, of 5.** C4 and a just G4
  (261.63 / 392.44 Hz, the score's III), the fifth at 0.8 of the root, as two sines. A held note does not
  exist in this synth, so each tone is **re-struck in phase at its own whole cycles nearest every 11 ms**,
  each strike 0.25s, the first carrying 0.6 of its plateau (68 synth calls). It swells **+12.3 dB with no dip
  to a crest 350 ms after the cast — as the ring finishes opening** — and is audible 555 ms; both tones within
  0.3 cents and 0.7 dB of each other from the start to the crest; flutter 1.7 dB; every partial a harmonic of
  C3 (a voice, not a chime); nothing at or over 4.9x the root within 56 dB of it (soft). Its crest is -2.7 dB
  re the blow at 12.5 (quietest draw), +17.2 dB over the score at its crest; register at most **0.46**
  (Angelus's close, on the batch line) against rune-crack, the sanctified and bow casts with voices of their
  own (Dawnbringer, Morningstar; Vinesower, Marrowdraw), BAR, the seal, the blow, the death voice and
  Angelus's cast and close. All five pass (OO, VOWEL, CHORUS, BREATH: register 0.44-0.51); the tiebreak
  (the register in steps of 0.05, then the fewest synth calls) puts CHORUS (0.44) in PURE's step, and PURE
  has the fewer calls (68 against 272). **Seven controls each fail their own gate:** STEP (Zenith's figure, the root then the
  fifth), ONE (the root alone), STRUCK (struck once, ringing), OFFBEAT (re-struck out of phase, Angelus's
  way: audible 610 ms, +6.0 dB, a dip), BRIGHT (Zenith's timbre: an edge -28.0 dB), BELL (a bar's mode: 54
  cents off the harmonics), and rune-crack itself.
- **A foe entering, "a single bright note" — CHIME, of 4.** A harmonic chime struck on **C6 (1046.50 Hz, the
  halo's root two octaves up)**, its 2nd and 3rd partials at 0.5 and 0.25, each dying faster (3 calls). One
  onset; the note holds (-0.0 cents) and stands 55 dB over the noise round it; its 2.00x partial -7.5 dB re the
  note (bright); peak at 6 ms, audible 200 ms; loudest 50 ms -8.5 dB re the blow and +11.4 dB re the wall
  tick. **It shares a frame with the heal chime on most entries** (1886 of 3091 in the survey), so the rule
  put its register against the spark collect first: at most **0.17** at any count (n 1-5: 0.17 / 0.15 /
  0.09 / 0.09 / 0.11), each keeping its own band within 0.0 dB on one frame; at most 0.41 against the wall
  tick, hex-snap, the spark arm, Zenith's tick, the bowstring, the blow, the clank and the cast. BELL
  (0.17 / 0.42) and GLASS (0.18 / 0.35) pass too; the tiebreak (the register against the heal chime, then the
  register overall, each in steps of 0.05, then the fewest synth calls) puts GLASS a step behind on the heal
  chime and BELL level with CHIME on both, and CHIME has the fewer calls (3 against 4). SUNG is out (two
  onsets: not single). **Five controls each fail their own gate:** LOW (C4: not bright), DULL (a bare sine: no
  overtone), DOUBLE (a second note 120 ms later: not single, and 0.71 against the chime), TICK (dying in 30
  ms), SPARK (the heal chime's own shape: 1.00 against it).
- **The blessing — the `spark` collect voice, reused, unchanged** (§4), once per blessing with n the blessing
  Aureole carries after it (Zenith's call word for word): 1290-1730 Hz for n 1-5, audible 130-135 ms, -12.6
  dB re the blow, heard +21.0 to +23.9 dB over the score's p90; register 0.09-0.17 against the entry, 0.02-0.03
  against the cast.
- **The close, "the swell reversed" — TIGHT, of 5.** The cast run backward on the same dyad and strikes: its
  release as a 200 ms climb, then the swell unwinding 19.76 dB over 0.2s, the fall's length solved so the
  whole is as long as the cast (75 calls). Its envelope correlates **0.91** with the cast's samples literally
  reversed; LATE 0.43 (its energy in the first half of its sound, where the cast's 0.55 is in the second);
  audible 555 ms; its top +0.0 dB re the cast's (a reversal keeps its level; v82 does not say quiet); flutter
  1.3 dB. MIRROR (the plain reversal: audible 715 ms) and DEEP (700 ms) are out on length, FADE and SIGH on
  the envelope (0.49, 0.55); the LITERAL reversal, the reference that cannot ship, passes. **Three controls
  each fail:** AGAIN (the cast itself: LATE 0.55, its top at 0.62 of its sound), SHORT (half the length),
  QUIET (9 dB under).
- **The rule grew over five rounds**, each said in the lab's docstring: the strike length fixed at Zenith's
  0.25s (a solved 0.10-0.12s fluttered 4-5 dB); the crest centred as the ring opens; the close read "heard"
  at its crest, not its reversed onset; a PLACE gate added when the AGAIN control (the cast
  itself) was failing on LATE alone; and
  the real-window reading of both swells taken over the 100 ms centred on each one's top.
- **Wiring** (reading 17). The cast is `fireUlt`'s own prologue call, `SFX.play("ult", { w: f.w.id })`:
  Aureole had no arm and fell through to rune-crack, so the three arms go in BEFORE that fallback, which is
  re-emitted unchanged. **The entry** plays in `tickHalo`, just before the ticker's own inside test: the test
  repeated into a const, `SFX.play` when it is true after a false tick of the same window, and the answer kept
  on the window's record as `voiceIn` — born undefined with every cast, so **a foe already inside when the halo
  rises is no entry** (the cast's swell has that moment; 151 of 506 windows in the survey), and read by nothing
  but this row. **The chime** plays after `T.bless += u.bless;`. **The close** plays before the window's own
  close line, on a close BY ITS CLOCK with both alive; **a close by a death is silent** (reading 18: a
  caster's death ends the fight and a close after the foe's death belongs to its kill flight — Tendril's,
  Canopy's, Zenith's and Lightkeeper's rule), and a halo still up when the fight ends closes in the picture
  only. The smite has no voice (none named).
- **The Sfx row, applied to `Sfx.prototype.play`'s own source:** the arms equal their candidates (worst
  7.5e-08); 137 other voices unchanged through the patched play (worst 1e-07: every hit weight and crit, the
  heal chime at n 0-6, 91 ult ids and every kind `play()` names); `ult/aureole` is no longer rune-crack (0.629
  apart). Main-thread cost a call: the cast 1.20 ms, the entry 0.10 ms, the close 1.30 ms. With Angelus's Sfx
  row (the batch line's other choir): both orders render every arm alike (worst 1.5e-07).
- **The lab's wire run** (the rows applied to `tickHalo`'s own source beside the original; 148 fights,
  Aureole both sides x every foe, seeds 110601-2): **148/148 identical** (every field of both fighters, the
  arrows in the air, the tally and the halo's record but `voiceIn`, which differs alone in the 48 fights that
  end with the halo up), every other SFX call identical in order and options. **506 casts, 506 cast voices;
  3091 entries, 3091 entry notes** (1886 on a blessing's frame; gaps between entries min 0.05s, p5 0.35,
  median 1.03, 22 of 2591 under 0.2s); **2878 blessings, 2878 chimes** (n 1: 506, 2: 491, 3: 478, 4: 443, 5:
  960); **409 clock closes, 409 close voices, and none on the 49 closes a death made** (8 on Aureole's, 41 on
  the foe's) or the 48 halos the fight's end cut off. **Control:** the rows plus one sim write (the foe nudged
  1e-9 on an entry) leave 3/148 fights identical.
- **End to end**, the four rows applied as text (21ea91d0f3c14274 → 50d4b2dfd385397e, +6723 chars) and loaded
  fresh: the three new voices through the page's own `SFX.play` equal the candidates (worst 8.9e-08); 137
  other voices unchanged (1.2e-07); 74/74 fights identical to the unpatched page's, and in every one cast
  voices = casts, entry notes = entries, chimes = blessings (with the count), close voices = clock closes.
- **A real window** (Aureole v Axiom, side A, seed 110601; the cast at 62.87s, a clock close at 72.81s, 14
  entries and 9 blessings), each event over the fight's own sounds and the score, in the third-octave where it
  stands highest: **the cast +28.3 dB at 400 Hz** (over the 100 ms centred on its top; +7.2 over its first 100
  ms); **the entries a median +23.5 dB** (+11.6 to +45.3, 14 of 14 over +6); **the close +11.9 dB at 400 Hz**
  (+2.2 over its first 100 ms, its reversed release); the chimes a median +21.3. The AFTER control (0.8s past
  the close, no new voice) reads NOT heard for every voice; the LEVEL control (each voice 20 dB under) reads
  lower for every event heard. `05-reference/v110/aureole-pick-real-window.wav` and its `-without` twin hold
  that window with and without the new voices; `aureole-pick-sequence.wav` the picks in order for the ear (the cast,
  three entries each with its chime, a blow, a chime, the close).

### 5d. The probe's stage 6: [9] the voices, [10] the picture's hook

`aureole_probe.py` is now fc096aca9624bb99 (stages 1-5's was afa389b746f9c12b, kept in scratch; the patch is
`s6/patch_probe.py` there, copied as `runs/stage6_patch_probe.py`). Checks [1]-[8] test and print what they did
(the new code rides in the same wrappers, and on the b12.5 the new probe prints every line and counter the old
one did: §5e). Two checks are new, one for each half
of stage 6, and **the link itself switches each one on** (the entry's arm, `aureole-enter`, in
`AC.SFX.play.toString()`; `tickBenediction` on the Match), so the same probe still reads [1]-[8] alone on a link
without stage 6. Once a fight is over it steps 2s more of the verdict (the step's `over` path, the
presentation clock only) for these two checks alone.

- **[9] the voices.** `SFX.play` is wrapped for the run (put back after it) and every call recorded with
  where it was made. Aureole's three arms and the heal chime are read; **a ward's shatter plays its own crit
  HIT voice inside `hurt()`**, which is not one of them, and so it cannot pass or fail [9]; nor can another
  relic's cast. It fails:
  - an Aureole cast without exactly one cast voice (w "aureole"), inside `fireUlt`, or the cast voice
    anywhere else;
  - **a `tickHalo` call whose voices are not exactly, in order, the rebuilt ones:** the entry on an inside
    tick that follows an outside tick of the same window (the probe keeps its own memory of each window's
    last answer, from the engine's inside flag, which [2] rebuilds from the geometry) and never on a
    window's first tick; one heal chime a blessing laid (n her blessing after it); **the close voice on a
    close by the clock with both alive, and never on a close by a death**;
  - the chime anywhere but the halo and the other relics' own spark tickers (`tickSun`, `tickSparks`, and
    `tickHolyGround` on a tip that carries Censer); any of them in the picture's hook, a drawn frame or the
    verdict;
  - and every one of the run is accounted for: cast voices = casts, entry notes = entries, chimes =
    blessings, close voices = clock closes; and a window opened with the foe inside, an inside tick after
    an inside one, and a death close must each have been seen silent (NOT EXERCISED otherwise).
- **[10] the picture's hook.** `tickBenediction` (the picture's one call on the step path) is wrapped. It
  fails a call that changes either fighter (every own number, flag and string but `bene*`, every array's
  length, every status, the window **with its `voiceIn`**, the tally, the weapon row and its ult) or the match
  (every own number, flag and string, every array's length but `tags`, every shot's x, y, vx, vy and life),
  or draws the RNG, or plays a voice. And the picture as declared, **rebuilt from the tally the way [3]
  rebuilds the smite** (readings 14-15): the ring not up (`beneFade` 1) in an open window or its growth clock
  not the presentation clock since the cast, up with none, or a close that is not a fade to 0 over exactly
  0.6 of its clock (0.3s) — by the clock, on a death or at `over`; "inside" not the ticker's own answer
  (through a hit stop the last answer holds); the brightening not 0.2 / 0.5 of its clock up and down; a SMITE
  tag not exactly on the first smite of each inside stretch (at the foe, with its count), a BLESSING tag not
  exactly on the first blessing of each (on Aureole, with her count), or any other tag; the foe carrying any
  of it; the ring up or lit after 2s of the verdict.
- **The drawn subset** (`--drawn 6`, the default): the first seed's fights, both sides, every foe, drawn
  through the renderer (`AC.__draw`, the post chain off, 270x480) every 6th step while the picture shows and
  every 60th otherwise, through the kill and the verdict; [10] fails a drawn frame that throws, draws the
  match's RNG or changes the simulation. It runs on any link, so the base's draws are its control.

### 5e. Stage 6's gates — every one able to fail

- **engine_ab b12.5 → fx, ALL 38 WITH Aureole, n=6: 4218/4218 identical** (`runs/stage6_engine_ab38.txt`;
  703 pairings, 38/38 distinct winners, 4218 distinct seeds, 22.7-114.9s; the ids `runs/stage6_ids38.txt`).
  Presentation moves no fight, Aureole's own included. **Control:** the b12.5 against `mP1` (below: its picture
  nudges the foe 1e-9 at a SMITE tag) with Aureole, Farwarden, Dawnbringer and Twinshade at n=6:
  **FAIL, 18/36 differ**: Aureole's 18 (she is in 3 of the 6 pairings); the other 18 fights have no halo and are identical (`runs/stage6_engine_ab_control.txt`).
- **aureole_probe (fc096aca9624bb99): 10/10 on the fx link** (`runs/stage6_probe_fx.txt`): 444 fights,
  Aureole both sides x 37 foes x 6 seeds, and the first seed's 74 drawn. **[1]-[8] print every mechanism line
  the b12.5 prints under the stages 1-5 probe** (3.34 casts a fight; 7.50 smite and 5.66 blessing a cast; the
  foe inside 32.4% of window frames; 12.8% of window steps frozen; a window 9.10s of match time; 58.8%;
  the probe's own run on the b12.5, `runs/probe_final.txt`, line for line; all 37 of its counters and its tally equal, the fx run adding 44 of its own). **The new probe on the b12.5 itself** (`--drawn 0`) reads 8/8, every line as
  `runs/probe_final.txt` and all 37 counters and the tally equal, and says "stage 6: not on this link"
  (`runs/stage6_probe_b12.5.txt`, `runs/stage6_probe_cmp.txt`). Then:
  - **[9] the voices:** 1485 cast voices for 1485 casts, each inside `fireUlt`; **8926 entry notes, each on an
    inside tick after an outside tick of the same window**, none on the first tick of the 477 windows that opened
    with the foe inside, and 409,182 inside ticks after inside ticks and 873,316 outside ticks silent; **8406
    chimes for 8406 blessings**, each with her count; **1217 close voices for 1217 clock closes, and all 141 death
    closes silent**; silent through 2s of the verdict in all 444 fights (127 with the sim's window still open);
    245 chimes of the other relics' own spark tickers (`tickSun`, `tickSparks`), and none anywhere else;
  - **[10] the picture:** 6,275,774 `tickBenediction` calls, none of which changed the simulation, drew the RNG or
    played a voice; the ring up, its growth clock exact, on every one of the 2,773,461 calls in an open window, in
    1484 windows; **every close a 0.3s contraction**: 1217 by the clock, 1 on Aureole's death, 266 at `over`
    (the arithmetic of the one cast the picture never saw open, 1485 against 1484: [1]'s 141 death closes are
    the picture's 1 on Aureole's death, the 139 of its 266 at `over` whose window a death had already closed --
    the other 127 were open at `over` -- and that one, a window a death closed on the step it opened); inside:
    418,464 window calls that ticked inside, 556,907 held inside between ticks (the presentation clock runs twice
    a step), 1,798,090 outside, and through a hit stop 138,441 held inside and 51,470 outside; the brightening
    rising on 197,094 calls, full on 778,277, falling on 487,507; **SMITE on 8863 stretches' first smites (2273
    smites inside a tagged stretch, untagged), BLESSING on 7783 (623)**; after 2s of the verdict the picture
    gone in all 444, 272 of them lit at `over` (127 with the sim's window still open);
  - **the drawn 74:** 48,557 frames through the renderer (43,566 with the picture up, 5700 of them in a hit
    stop, 488 in the verdict), none of which threw, drew the match's RNG or changed the simulation. **The base,
    drawn** (the b12.5, the first seed, `--drawn 6`; `runs/stage6_probe_b12.5_drawn_s1.txt`): 9/9, [1]-[8] and
    the drawn check, 9050 frames through the renderer (every 60th step: nothing of stage 6's to show).
- **The probe's controls**, scratch copies of the fx link with one edit each (`runs/stage6_mutants6.py`, their
  hashes in `runs/stage6_mutants6.txt`; the first seed, both sides, every foe, 74 fights), each failing its own
  check and passing the other nine:

```
mutant          sha16             breaks  how                                                            probe   fails          fights
mV1-closevoice  50e6e1064363fa7d  [9]     the close voice on EVERY close of the window, a death's too    9/10    [9] 22x        identical
mV2-enterfirst  b52f9b96000d578d  [9]     the entry note on a window's FIRST tick too (a foe inside      9/10    [9] 76x        identical
                                          when the halo rises)
mP1-picwrite    2ecbdb82e7a8bc19  [10]    tickBenediction nudges the foe 1e-9 at a SMITE tag (sim write)  9/10    [10] 1525x     move
mT1-tagevery    9a21efee6c2b5fda  [10]    the SMITE tag on every smite, not each inside stretch's first   9/10    [10] 394x      identical
mD1-drawwrite   77e96508edea27b4  [10]    drawBenediction nudges side a 1e-9 when it draws (drawn only)   9/10    [10] 42345x   move (drawn)
```

- The clean fx link on the same 74 fights (the first seed, no drawing) reads 10/10 (`runs/stage6_probe_fx_s1.txt`),
  and mV1, mV2 and mT1 leave its tallies and win rate (55.41%) exactly as they are: a voice and a tag are
  presentation, so the three presentation-only faults are caught by the checks that read the presentation, and by
  nothing else.
- mV1 fails on the death closes ("the halo played [["ult","aureole-close"]], want []", 22 in the 74 fights): **the
  check that no close voice ever sounds on a death**.
- mV2 fails on the windows that open with the foe inside ("the halo played [entry, chime n1], want [chime n1]",
  76): the check that a window's first tick is not an entry.
- mP1 fails on every call where the picture tags a SMITE ("the picture wrote the simulation: vx ..."), read on the
  call itself; its fights move (58.11% against 55.41%; the `engine_ab` control above), and [1]-[8] still pass,
  because they rebuild every frame from its own state.
- mD1 is caught only by the drawn subset ("a drawn frame changed the simulation: vy ..."), on the frames that draw
  the ring: the check that a DRAW writes nothing, which the headless hooks cannot see. Its drawn fights move
  (56.76% against 55.41% on the 74).
- mT1 fails where the rule says a stretch's later smites go untagged ("1 SMITE tag(s) on a call with 1 smite(s),
  want 0").
- **The probe's first extension had a fault, found by its own first full run and fixed before any number here:**
  [10] counted two names [2] already counts (`inOk`, `outOk`), so on the fx link [2]'s counters read 837,049 /
  2,671,406 against the b12.5's 418,585 / 873,316 (`runs/stage6_probe_cmp_firstprobe.txt`,
  `stage6_probe_fx_firstprobe.txt`). Both checks passed either way, but a check whose counters are shared is not
  the check it says it is. [10]'s are now `picInOk`, `picInHeldOk`, `picOutOk`; `runs/stage6_counter_clash.txt`
  asserts that every name [1]-[8] counts keeps its number of `inc` sites (the first extension, put back, fails
  it), and every probe run in this section is the fixed probe's (fc096aca9624bb99).
- **render_ab:** the other relics' pairs (paradox:heartwood:25064, twinshade:lastlight:991,
  bulwarden:vinesower:70707, axiom:grudgebearer:31337, at 0.5 / 6 / 12 / 22 / 31 / 40s) are **24/24
  pixel-identical** (`runs/stage6_render_ab_others.txt`). **Control:** Aureole v Spellbreaker 110075 (the
  clip's fight) at 45.3 / 46.5 / 48 / 50 / 52 / 53.8, inside the window that runs 44.817-54.058, is **0/6
  identical** (`runs/stage6_render_ab_control.txt`; the frame's mean luma -3.8 of 255 at 45.3, the beam's lit
  ground and lance gone from the cast, then +1.6 to +4.0 as the ring stands).
- **chain_audit** `--builder aureole_build.py`, relic = tip = the fx link: **ALL 21 INSERTS SURVIVE**, stages
  1-5's nine and stage 6's twelve (`runs/stage6_chain_audit.txt`); the thirteenth row, the life token, adds no
  code and so is not an insert the tool can read. **Control:** the same relic with the b12.5 as the tip loses
  11 of stage 6's and exits 1 (`runs/stage6_chain_audit_control.txt`). **Two rows it cannot watch:** the heal
  chime's line is Zenith's and Daybreak's word for word, so its marker stands 3 times in the relic and 2 in the
  base and never reads LOST; and the life token's removal has no marker. The builder watches both on every
  stage-6 build: the chime's line must be in the page exactly once more than in its source, and `aureole: 1.6`
  and `u.w === "aureole"` must be gone. Three of the 21 are found by their comment text, the code they leave
  shorter than the tool's floor (stage 1's heal retirement, §4, and the two retired art branches).
- **tip_audit:** identical to the b12.5's, line for line, but the file name, and the b12.5's is still
  `runs/tip_audit_final.txt`'s (`runs/stage6_tip_audit_fx.txt`, `stage6_tip_audit_cmp.txt`). Stage 6 adds no
  status and changes none.
- **The builder's own guards** (`runs/stage6_builder_checks.txt`, `stage6_builder_checks6.py`; the builder
  7cf0a20f6b53a2c3):
  - **all six links rebuild byte-identical from the bare tip**, `sc-tendril-t3`, LF, no CR — the five of stages
    1-5 as they were, and the fx link;
  - **stage 6 refuses** to run twice (its names are in its own output), on Rick's 50% link (b11.5), on stages
    3, 2 and 1, on the bare tip, over an existing link, to a name not `sc-aureole*`; stage 5 refuses on the fx
    link, and `--alt50` refuses with stage 6;
  - **its scan of stage 6's ADDED code** (a re-emitted anchor aside) refuses twenty scratch copies of the
    builder, each with one forbidden thing written into a stage-6 insert: a sim write in `tickBenediction`
    (the foe nudged), the RNG in a draw method, the one `ultFx` slot, a beat, a hurt in the heal row, a status
    laid (stun), a splice of the sim's shots, an index write into them, a write to the tally, a write to the
    window's clock, `voiceIn` written outside the entry row, `Math.random`, a shared table through an alias
    (`Q_ = STATUS.smite`), the shared weapon (`w.reach`), a sim write in a draw method (the match's clock),
    **the close voice on every close** (a death's included), **the entry's memory changed** (every inside tick
    an entry), a voice in the picture's fields row, a sim write in the fields row (the charge), and the synth
    struck outside the Sfx row. **A harmless edit in the Sfx arm writes its page** (a different one,
    190dc133036ad797), and the unmutated copy writes the fx link, f3228d8d1509edbb;
  - on stage 6 it also refuses if the inlined `fx.js` moved, if the beam's art is still drawn off the ultFx
    record or its life entry is in the map, if the rune-crack fallback is not kept once after Aureole's
    three arms, if the entry's test is not the ticker's own repeated just before it, and unless each arm,
    call, pass and method is wired exactly once and `tickBenediction` follows `tickNovaFx` in
    `tickPresentation`. The generator (`runs/stage6_gen_s6.py`) was run once (it wrote 8ecab292585ae40c) and
    refuses a builder that already carries S6; it also reworded reading 13's tail (stage 6 now retires what it
    named) and added readings 14-20 and the stage table's line. One hand edit followed it, said here: two
    comments named this doc's "§5-§6" for stage 6, which is §5 (comment-only; the final builder is
    7cf0a20f6b53a2c3, and every check in this section was re-run on it or on links it writes byte for byte).
- **compose6** (above; `runs/stage6_compose6.txt`, `stage6_compose6.sh`): 0 FAIL.
- **shell_identity** is not run here: the app's json is shared, and the orchestrator runs it on the carried link.
- **The labs' own gates** (§5a, §5c): the picture — bloom share +0.0004, with three controls that fail;
  whole-fight identity on 15 fights x 3 (the rows, the shipped look, drawn), with a 1e-9 control that differs
  on all 13 Aureole fights; 77/77 other-relic render frames on 11 pairs, with Aureole controls at 0/7 and 0/7;
  `engine_ab` 4218/4218 on its shipped look. The voice — the 148/148 wire run, with a sim-write control at
  3/148; 74/74 end to end.

**What the design's stage 4 asked for, and where it went** (§5: "picture (bloom measured), voice, carry;
beam's field spec out; `engine_ab`, `shell_identity`, `render_ab`, `chain_audit`, one fight watched"): the bloom
measured, +0.0004 (§5a); the beam's field spec out of both copies — the orchestrator's at the carry, tried in
scratch (§5b); `engine_ab` 4218/4218 with Aureole in; `render_ab` 24/24 with a control; `chain_audit` 21/21 with
a control; `shell_identity` the orchestrator's; one fight watched, the clip (§5f).

### 5f. The clip (Rick's to overrule)

`tools/_aureole_pick.py` (35f9b21b11ca0b9d; from `_ironwood_pick.py`, by way of `_censer_pick.py`) scores a
window against v82 §4 as built. A window qualifies only if it shows everything: the cast voice, **a foe
entering** (an entry note) **and leaving** (the ring dimming back), a smite, a blessing with its chime, and **a
close BY ITS CLOCK with both alive**, with its close voice (the ring contracting; a death's close or a kill is
the death voice's and the verdict's); and nothing taking the screen: no cast or banner of the foe's, not the
scrunch card, and no kill inside the clip. Twinshade is left out (a second body) and so is Aureole's own school
(a sanctified foe wears the same white and gold shell). Scored on the entries, the exits, the smites, the
blessings, the share of window frames with the foe inside and the hit stops while it is.

It ran 32 foes x 4 seeds (`runs/stage6_pick.txt`: of the 128 fights' best windows, 5 show everything). The pick is **Aureole v
Spellbreaker, seed 110075**:
- the cast at 44.817; the window closes by its clock at 54.058: 8s on the window clock, 9.24s of match time;
- the foe inside at the cast (no entry: the swell has that moment), then **8 entries and 9 exits**, 13 smites
  and 8 blessings (the chime at n 1-5), the foe inside 50.4% of the window's frames, 150 hit-stop steps with it
  inside;
- no banner, card or kill in the clip; the fight runs on past the clip's end (55.875, both alive; the kill is
  at 75.23).

The runner-up, Spellbreaker 110001, scored 0.34 lower (8 entries, 11 smites).

    python cinema_clip.py --game <scratch>/batch/aureole/links/sc-aureole-b12.5-fx.html \
      --a aureole --b spellbreaker --seed 110075 --at 43.62 --window 12.24 --end-at-window --fps 60 \
      --w 540 --out ../07-shorts/v110/benediction-window.mp4

`--at` is the cast less 1.2, `--window` the window's 9.24s of match time plus 1.2 and 1.8 (the window clock
stops in the freezes, so 8 + 3 would end the clip before the close).

The clip (`runs/stage6_clip_check.txt`, `stage6_clip_log.txt`, `stage6_clip_timeline.txt`):
- **12.25s, 735 frames**, 1:1 with the match (the director's T3 cut is the kill at 75.23, outside the clip);
- 540x960 h264 at 60 fps, AAC 48 kHz stereo, 2.65 MB (f56af7299f6f5072);
- **AAC mean -22.3 dB, max -3.5 dB; -20.3 LUFS integrated, LRA 1.1 LU, true peak -3.1 dBFS;**
- the fight's state at the clip's end (t 55.875, hp 371.96 / 213.775, 12 clanks) is the headless fight's
  (`stage6_clip_timeline.py`);
- **the new voices are in the mix** (`runs/stage6_clip_audio.txt`): the same window filmed on the b12.5 (no
  stage-6 voice; its cast plays rune-crack; 93d707c1cf1198d3), both tracks decoded, each voice read in its own
  band over its own time, with minus without: the cast's swell +12.1 dB, the eight entry notes +23.3 to +86.2,
  seven heal chimes +11.7 to +42.7, the close +22.7. The chime on the cast's own frame reads -12.8, because the
  base's cast fills that band with rune-crack. **Control:** the same readings at ten times with no stage-6 voice
  come back within 3.8 dB.

Five frames, checked through the pipeline (the post chain and the director), matched to the fight's own event
times by the HUD's clock; tiled in `05-reference/v110/benediction-clip-5frames.png` (add6b9e25b0a5b10,
2700x960):
- 1.40s (HUD 45.0): the cast, 0.18s after it (44.817): the banner, the ring growing out of the ball, SMITE 2 on
  the foe (inside at the cast) and BLESSING 1 on Aureole;
- 2.80s (46.4): the first entry (46.292, its note): the ring bright, the foe on its edge with SMITE 3, and
  BLESSING 2 on Aureole (the foe's rim is not legible at this size under Spellbreaker's own blue glow);
- 6.30s (49.9): the foe inside, the ring bright (the stretch from 49.258), Spellbreaker's own HEX tag;
- 9.00s (52.6): the foe outside (since 52.008): the ring back at 0.4;
- 10.60s (54.2): 0.14s after the clock close (54.058, its close voice): the ring contracting into the ball.

**The white spray at the foe in the cast's frames (1.2-1.6s) is the beam's own `SPECS.aureole` field** (a
`beam` is drawn toward the quarry), still on this link until the carry's `fx_remove.py` (5b). The clip is
`07-shorts/v110/benediction-window.mp4` (gitignored). **Rick's to overrule.**

### 5g. Where each event hangs (the fx link)

The lines, in `sc-aureole-b12.5-fx.html` (grep the quoted text on a carried link; `runs/stage6_lines.txt` has
them on the fx link and on the b12.5):

```
the cast       fireUlt 16428: the shared prologue (banner, 0.08s hit stop, beat "ult", SFX.play("ult", { w: f.w.id }) 16455,
               this.ultFx; the life map line 16547 now "censer: 1.6," -- Aureole's 1.6 gone), then
               `if (u.kind === "halo"){` 16831: `f.ultHalo = { t: 0, dur: u.dur, cd: 0, bcd: 0 };` 16837, returns
the halo       `this.tickHalo(dt);` 9039 (after tickTendril, before tickHits); `tickHalo(dt){` 13750: the close voice 13765,
               the close 13766 (the clock or a death), the entry's test and voice 13779-13781, the inside test 13782,
               `T.inFrames++` 13783, the smite 13787, the blessing 13792, `T.bless += u.bless;` 13793, the chime 13799
the voices     Sfx arms: `} else if (w === "aureole"){` 7427, `"aureole-enter"` 7460, `"aureole-close"` 7480, before the
               shared `} else {  // rune-crack` 7501
the picture    fields after `this.haloTally = null;` 7793 (`this.beneFade = 0;` ...); `this.tickBenediction(dt);` 9081,
               right after tickNovaFx in `tickPresentation` 9079; `tickBenediction(dt){` 13822 (before tickWinnow);
               `if (__world) this.drawBenediction(m);` 19533 (the world pass, after drawTree); `drawBenediction(m){` 20622
               and its four parts (before drawMotes 20722); ULTSIG `aureole(c, t, cf, P){` 623 (redrawn)
the beam's art the two `u.w === "aureole"` branches gone: their comments at 21528 (drawUltUnder) and 22377 (drawUltOver);
  (retired)    fx SPECS.aureole still inline at 32557-32559 (the orchestrator's, 5b)
```

## 6. What is left, and whose

- **Rick:**
  - **the clip** (§5f, `07-shorts/v110/benediction-window.mp4`) and every art and sound pick in §5 — the ring
    in the school's white at 0.4, 0.7 while a foe is inside, its 0.3s growth and contraction, the 0.04 wash, the
    motes, the foe's rim, the redrawn charge rune; PURE for the cast (C4 and G4 re-struck), CHIME for a foe's
    entry (C6), TIGHT for the close (the cast reversed) — under "you pick i overrule";
  - **no `fx.js` field** (§5b): the design's "motes drifting inward along the ring (both copies)" are drawn off
    the ring instead, because the one ultFx slot is Aureole's for 7.9% of a window and she stands a median 214
    units from where a field would spawn after the first second;
  - **a foe already inside when the halo rises is no entry** (the cast's swell has that moment; 151 of 506
    windows in the voice lab's survey), and **a close by a death is silent** (the death voice has it; reading
    18). Both are readings of "a foe entering" and "close"; the design names neither case;
  - **the blade target.** The design's own is the shipped rate (54.1%): 12.5 reads 56.1%. The batch's
    new-relic standard, 50%, would be 11.5 (48.8%), built beside it as `sc-aureole-b11.5`. Both are
    under the brief's 13.5-14.5 grid, which the 151 runtime put above the target; the brief named no
    knob to move first;
  - the veto (waived for the batch) and §6.3, the arrows: not taken, as the design says;
  - the ladder at 12.5: Lightkeeper 20% and Starwarden 25% are her worst (the beam's: 32.5 and
    37.5), Bloodmirror and Bindweed 90% her best; the type spread 20 points (item 12/32);
  - verify's reds (§4) are the base's, not this relic's;
  - **the brief's mechanism gates read lower than asked, and the win-rate gates pass.** Brief stage 1
    asks for the foe inside ~36% and ~7.7 smite a cast; built stage 2 reads 29.3-30.0% and 7.01-7.06.
    Brief stage 2 asks for ~5.8 blessing a cast; stage 3 reads 5.49-5.51 (§3's table). The cause is the window
    clock (§2): the lab's halo also ticked on frozen frames, which are contact frames, and the engine's
    stops in a hit stop. The same build on the lab's clock gives back 35.7% / 7.68 / 5.68. The win rates
    are within noise of the lab's (stage 2 51.4 against 51.0, stage 3 72.6 against 70.9, four blocks).
    **The mechanism gate is the one gate of the brief this build does not meet as written, by the clock and
    by nothing else** (§2's controls, §3's m1): nothing to decide unless Rick wants the lab's clock, which
    would break the batch's convention.
- **The orchestrator (ALL DONE at the carry, §7):**
  - carry the five stages with `aureole_build.py --stage 1/2/3/5/6 --src <tip>` (the change sets are line for
    line the same on every newer tip tried, up to `sc-censer-fxout`, but for the life map's one line on a tip
    that carries Censer's stage 6: §5, compose6) and prove the carry with `engine_ab`; `chain_audit` watches
    21 inserts, including the blade, though not the heal deletion (§4) nor the heal chime's line and the life
    token (§5e), which the builder watches instead;
  - take the beam's `SPECS.aureole` out of both copies of `fx.js` with `fx_remove.py --relic aureole` at the
    carry (§5b, its exact text; tried in scratch on the fx link and, dry, on `sc-censer-fxout`). Until then an
    Aureole cast still fires the beam's particles, and the clip shows them;
  - `shell_identity` on the carried link (the app's json is shared; not run here);
  - the app pointer (`app/main.js` GAME) waits for Rick's check of the whole batch.
- **Not measured here:** the picture's frame cost in the app (deferred by the orchestrator; no Electron was
  launched in the picture lab's final round). A later session with the app, or the orchestrator.

## 7. The carry onto the chain, and the beam's field spec out

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Censer with the
same builder, one stage at a time (`--src` the previous link), and one more link that takes the retired
beam's particle field out:

```
sc-censer-fxout.html               the batch line's tip (Censer, fx out)        00a2e2e10448c492
  -> sc-aureole-stub.html           stage 1                                      f0385dde62b833b1
  -> sc-aureole-halo.html           stage 2                                      d801dc0bdd2e6a94
  -> sc-aureole-bless.html          stage 3                                      0c967b3a5113bdc6
  -> sc-aureole-b12.5.html          stage 5                                      02dfcf9b1c4d3875
  -> sc-aureole-b12.5-fx.html       stage 6                                      e373cf79dc779466
  -> sc-aureole-fxout.html          SPECS.aureole out of both fx.js copies       da5eafafcfae06c2
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail, Widowmaker, Lightkeeper and Censer (redesigned on the chain since), n=6: **3366/3366
  identical** (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-censer-fxout` against the carried stage-6 link, every relic on the tip but
  Aureole (41), n=6: **4920/4920 identical** (`runs/carry_engine_ab_tip.txt`): the redesign moves no
  other relic's fight on the batch line.

**The beam's field spec out: `tools/fx_remove.py --relic aureole --keep-comment`** -- the entry's three
lines only. The comment above it ("Negative gravity is what stops a beam reading as an explosion pointed
sideways") states a rule the beams below it (Oathwound, Spellbreaker) still follow, so it stays;
`--keep-comment` is new for this carry, and the tool's default is unchanged (Ironhail's removal still
reproduces the committed link byte for byte). **fx.js 866f45e37dc54e3f -> 487c9de9dff7f374**
(`runs/fxout/fx_remove.txt`). The stage-6 builder's removal of `aureole: 1.6, ` from the ultFx life map
leaves that line holding only whitespace on this line (Censer's token went too): it parses and nothing
reads it -- cosmetic, left.

**Gates on `sc-aureole-fxout`** (`runs/fxout/`, one at a time at idle priority: Rick was on the PC):
- engine_ab against `sc-aureole-b12.5-fx`, all 42 relics, n=6: **5166/5166 identical**;
- `aureole_probe.py` on the carried link: **10/10** -- it met every relic carried since its scratch base
  and needed no change;
- render_ab: the other relics' four pairs **24/24 identical**; **the control, Aureole v Spellbreaker
  110075 through the cast (44.85-45.25s), 0/5 identical** -- the beam's spray is gone;
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold;
- **shell_identity 200/200** (app Chromium 152 vs headless 151), run 2026-09-30 05:30 once Rick was off the PC (`runs/fxout/shell_identity.txt`; the pointer not moved, the json restored).

**The clip, re-filmed on `sc-aureole-fxout`** (the §5 command, `--game` the carried link):
`07-shorts/v110/benediction-window.mp4` (2.62 MB, 12.2s; `runs/fxout/clip.txt`), the cast without the
beam's spray.

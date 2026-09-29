# v104 — ANGELUS / ASCENSION, BUILD. STAGES 0-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-oracle-fx`, §7): stage 1 is arm A to the fight; the rise, the shafts and the heal are the lab's mechanism, proven sentence by sentence; the win rate stays within ~2.5 points of the lab arms, and controls attribute the gap (the 0.35s rise pulls it down, the window clock pushes it up); the brief names no knob for the blade, so none moved, and the blade is 9 (51.1% both sides, crossing ~8.9). Review r2 taken, and no link changed. Stage 6, the picture and the voice: `sc-angelus-b9-fx`, twelve rows byte-exact to the labs'; engine_ab on all 39 WITH Angelus 4446/4446; the probe 12/12 (two new checks, the voices and the picture's hook, each failed by its own mutants); render_ab 24/24; six fights drawn identical to undrawn (6/6); the picture closes the window the sim leaves open at `over`; no `fx.js` field (the motes are drawn). The clip is with Rick. Not yet on the chain: the orchestrator carries it (stages 1, 2, 3, 5 and 6), and there is nothing to take out of `fx.js`.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`). Input:
`06-docs/v74/ANGELUS-BUILD-BRIEF.md` + `sanctified-twinblade-design-v74.md`, and nothing else (rule 0).
Builder `tools/angelus_build.py`, probe `tools/angelus_probe.py`, runs in `runs/`.

**A NEW relic: the 39th on its base** (the brief's "41st" is the cell count). It was **built in
scratch** on the chain tip while other builds ran on the same tip. The orchestrator carries it onto the
chain one relic at a time (`angelus_build.py --stage N --src <tip>`) and proves each carry with
engine_ab.

```
sc-tendril-t3.html        the base: the chain tip (Bindweed stage 5), 38 relics      5a6216e3b629fad4
  -> sc-angelus.html       stage 1  the relic, ult stubbed (charge 1e9), blade 11.95  cb1786badd375ec3
  -> sc-angelus-rise.html  stage 2  the rise and the shafts (arm B), charge 14        9607d88c968b1aff
  -> sc-angelus-heal.html  stage 3  the heal, healPer 0 -> 1 (arm C)                  45f46064b018bb85
  -> sc-angelus-b9.html    stage 5  the blade, 11.95 -> 9                            db58100b3aa0092a
  -> sc-angelus-b9-fx.html stage 6  the picture and the voice (§5)                   6356f75eb0b328e1
```

- **Where the links are:** the batch scratch folder, `<scratchpad>/batch/angelus/links/`, not `02-chain/`.
- **No stage 4:** the brief has none. **Stage 6** goes on stage 5's link.
- **Every link rebuilds byte for byte** from the base. This was checked three times; the last time was
  2026-09-28 02:31 PDT, with the final review-r2 builder (`runs/rebuild.txt`, `runs/recheck_resume2.txt`,
  `runs/rebuild3.txt`). The stage-6 builder rebuilt all five, the stage-6 link included, byte for byte on
  2026-09-28 23:33 PDT (`runs/stage6/rebuild6.txt`).
- **Builder** `tools/angelus_build.py` **0e4e2fc3ff5813de** (stage 6 in; through review r2 it was
  e5b0d70b8555a916, and stages 1-5 still write the same bytes). **Probe** `tools/angelus_probe.py`
  **fa5ee160cbbe177c** ([11]-[12] added for stage 6; through review r2 it was 4c3ecb34775f7c65, and on
  stage 5's link it prints the same lines). **Clip picker** `tools/_angelus_pick.py` 66236cd9c5c3d61b (new).

**Review r2 (2026-09-28).** Two should-fix findings and four notes. None of them changed a link.
- **The hold's re-arm was argued, not measured.** The probe now clears the hold itself before every
  50th window tick. This is inert on the build: the fights are identical. Mutant m8-pinfree proves
  [2] can fail (§3, reading 4).
- **The window does not close on the foe's death.** This is now declared as reading 10, and measured:
  the window is still open when the match ends in 260 of 456 fights. The picture has to close it
  (§5).
- **The notes:** shade hits heal (reading 11); the spin anchor is consumed (§1); a knob move below
  `dur` would need a cast wait (reading 9); the §5 line numbers were corrected; the stage-1 verify
  band is covered by the fight-for-fight proof (§2).
- **What moved:** the builder's docstring and comments, the probe, and the doc. The links are
  byte-identical, so engine_ab, verify, relic_rate, tip_audit and the built-vs-lab runs stand as
  they were. chain_audit reads the builder, so it was re-run (§4).

**Stage 6 (2026-09-28/29): the picture and the voice.** Two labs picked them on measurements (Rick's "you
pick i overrule"), and the builder writes their twelve rows byte for byte (§5).
- **What moved:** the builder (S6, `--stage 6`, readings 12-18), the probe ([11] the voices, [12] the
  picture's hook), the new clip picker, one new link, and this doc (§1, §3, §5, §6). Stages 1-5 are
  untouched: the four earlier links rebuild byte for byte.
- **The gates** (§5e): builder refusals 10/10; engine_ab 4446/4446 on all 39 relics, Angelus
  included; the probe 12/12, and 10/10 with every line unchanged on stage 5's link; four mutants,
  each failing [11] or [12] alone; render_ab 24/24 with an in-window control at 0/6; chain_audit 20/20
  with a control; tip_audit unchanged; six fights drawn as the app draws them, identical to undrawn
  (6/6, with a control); the carry re-applies on 14 sources.
- **The clip** (§5f): `07-shorts/v104/ascension-window.mp4`, Angelus v Slagheart 104112, 14.6s.

## 0. What this build stands on

### The relic

It is Widowmaker's twinblade profile: blades [0, 0.5], reach 62, width 8, artW 30, spin 5.7, spin
mode, mass 1.1. That profile is the lab's donor and every shipped twinblade's. Until stage 5 it is at
the lab's blade, 11.95. It carries:
- aff sanctified, with onHit smite 1 (the school's channel);
- the brief's 69-character card.

The builder asserts:
- the type's profile on all five twinblades, except the donor's blade (Widowmaker's v106 redesign
  changes it);
- the channel on the five sanctified relics;
- the head's route: `SHAPES.twinblade` → `_tbRadiant`, which no shipped relic has drawn;
- the blessing heal;
- the pin's three behaviours: `move` returns for a pinned ball, `_ballPair` treats a pinned ball as
  immovable, and `tickStasis` leaves a `pinFree` ball's weapon free.

### The lab

The lab is `ult_overlay.py --mech overlays/ascend.js` (sha 1a0f1d0f18214a89), unmodified, run on
Chromium 151 on the base. The foes are the design's roster: the 34-relic roster minus the donor, which
is 33 foes.

**One lab default differs from the settled numbers.** `hangY` defaults to the CEILING (`inset + R +
6`), and the design took **300** (§3). Stage 0 ran `--P hangY=300`, the brief's own command. The
overlay's other defaults are the brief's numbers: shaft 10, spinMul 0.5, winDmg 0.4, healPer 1,
smiteExtra 1 (arm D only), charge 16 and dur 8.

### The charge: 14

The brief's 16 is on the lab's clock, and Rick's batch ruling converts it. I measured it for this
fighter with a scratch copy of `ult_overlay.py`, `runs/ascend_census.py`. Before each lab step, the
copy counts whether the step is frozen (`m.hitStop > 0 || m.latch || m.splitHold`), in total and
inside windows. The control is that its win rates equal stage 0's.

660 fights an arm (`runs/s0_census_BC_2207`):

```
arm   frozen, all lab steps   in windows   outside   the lab's 16 on the game's clock
B     14.41%                  19.12%       11.16%    13.69
C     14.78%                  19.39%       11.53%    13.64
```

Both round to **14**, matching the "lab 16 ≈ engine 14" of the batch's other builds.

### Readings

These are in the builder's docstring. Each one follows the doc's own words or the engine's rule.

1. **The shafts light when the caster arrives** (design §5 says so twice). For the 0.35s of the rise
   the blades are still the twinblade's own: reach 1, full spin, full damage, no heal. The lab
   teleported the caster and lit the whole window. The design's open item 5 prices the difference at
   "~4%" of the window.
2. **The ease is a smoothstep** (3u² − 2u³) from the cast position to the hang point, on the window
   clock. The prose says "eases it up over 0.35s"; the curve is the build's choice.
3. **The hang point is the lab's:** (W/2, max(hangY, inset + R + 6)) = (260, 300). The clamp cannot
   bind, because 140 + 34 + 6 = 180 < 300, and the probe counts 0 binds.
4. **The hold is re-armed every window frame, `pinMax` and `pinFree` as well as `pin`** (the brief:
   "pinned there (pinFree 1, re-armed)"; Canopy's reading), so the blades keep "sweeping the hall as
   they turn".
   - What can clear the hold is Ravelbone's wire, and only on a caster it caught BEFORE the cast (a
     pinned ball cannot be caught). The wire's slip, its window's end and its connect each clear
     `pin` / `pinMax` / `pinV` / `pinFree` on its quarry, and the next tick puts the hold back.
   - A connect clears it inside `resolveHit`, after the tick, so the caster would ride its knock for
     one frame before the hang write puts it back; the lab re-pinned after the step. That is
     reasoning: it was never observed.
   - **It is measured, not argued (review r2, finding 1).** The path never came up: `pinFree` was
     found cleared 0 times in every run (§3). So the probe clears the hold itself before every 50th
     window tick, which leaves this build's fights identical, and [2] fails a build that does not
     re-arm (mutant m8-pinfree).
5. **The window closes on the caster's death** ("for a duration"; Canopy's reading). A dead caster
   keeps its kill flight. This happens only when the tick comes round after the death (a kill
   flight, or a death in the fighter loop). Reading 10 covers the kill that ends the match.
6. **Every shaft hit heals, including the last window frame's.** The heal reads the `hits` delta at
   the top of the tick, before the clock can close the window. The lab closed first.
7. **`apply`'s source is a side letter** (the engine's contract; the brief wrote `f`). Nothing reads
   blessing's source.
8. **The shared weapon is never written.** The lab scaled `w.spin` and `w.dmg`. The build scales both
   at their one read site, off `f.ultRise`, in the lab's order of multiplication.
9. **No cast wait.** The design has no wither, and the charge (14) and the window (8) run on the same
   unfrozen clock. The probe asserts that no cast comes inside a window ([10]).
   - A knob move that put the charge at or under `dur` WOULD need one. A cast inside a window starts
     a new rise with `reachMul` still 10 and full damage; review r2 measured this at charge 6.
   - The wait would go on the charge gate's stable prefix,
     `if (f.charge >= f.w.ult.charge && !f.ultCorona`.
10. **The window does not close on the FOE's death, and it stays open at `over`.** This is
    Canopy's convention (v99), and it goes against the lab (review r2, finding 2).
    - **The lab** released on either death (`ult_overlay`: `!me.alive || !foe.alive` → `ascend.js`
      `release()`). It did so AFTER its step, when the match was already decided, so that close
      moved no fight, and leaving it out moves none.
    - **In the engine** a kill ends the match INSIDE the killing step. `checkEnd` sets `over` at
      once: only Ravelbone's burst and Grudgebearer's forge arm a `killFlight`, and Angelus's blows
      arm none. Then `step()` returns at `over` before any ticker.
    - **So a window open at the kill stays open** through the verdict, hung and lit at reach ×10,
      whichever ball died. The one exception is Angelus killed by Ravelbone's burst or Grudgebearer's
      forge: their flight lets the tick run, and it closes the window on the caster's death
      (reading 5).
    - **A foe that dies in the fighter loop** (Angelus's own smite, a damage-over-time status in
      `tickStatus`) is dead for one more tick, and that tick leaves the window open too.
    - The probe counts both (§3). **The picture closes it:** stage 6 draws the close at `over`
      (§5). The sim will not.
11. **A shaft hit on a shade heals.** `tickShadeHits` calls `tickHits(Angelus, shade)`, so a blow on
    Twinshade's copy is an ordinary `resolveHit` blow: × winDmg while lit, and `self.hits++`, which
    the heal reads. The lab read the same `hits` delta, and the prose says "every hit heals". The
    probe counts them (§3).

**Readings 12-18 are stage 6's** (the picture and the voice), in the builder's docstring and in §5d.

### Names and the clock

- **Names:** `ultRise`, `riseTally`, `tickRise`, kind `"rise"`, `shaftSpin`, `healPer` and `hangY`.
  I grepped each and found none in the base or in `src/render/fx.js`. Stage 6's (`tickAscend`, the
  `drawAscend*` and `_ascend*` methods, the `ascend*` fields, the `angelus-shaft` / `-close` / `-land`
  voices, `falling`) are checked free on identifier boundaries by the builder before it writes.
- **The clock:** the window, the rise and the hold run on the window tickers' clock, which stops in a
  hit stop. This is the convention of Corollary, Daybreak, Zenith, Canopy, Onslaught and Tendril.

## 1. Stages

### Stage 1

Stage 1 appends the row at the END of the WEAPONS array, with the ultimate stubbed at charge 1e9. The
anchor is the array's closing `];` plus the comment under it ("The single source of truth for"). That
anchor names no relic.

### Stage 2

- `ultRise` / `riseTally`, after `this.vineTally = null;`.
- The `kind === "rise"` cast branch, BEFORE the tendril branch. It pins the caster where it stands
  (`pin` dur, `pinFree` 1, `pinV` [0, 0]) and resolves nothing.
- `this.tickRise(dt)`, AFTER `this.tickTendril(dt);` and before `tickHits`.
- `tickRise` itself, BEFORE `tickWinnow`. It heals, re-arms the hold, eases the caster up, lights the
  shafts on arrival, holds the hang point and closes the window.
- The shafts' spin: `× shaftSpin` in tickWeapon's spin product.
- The shafts' damage: `× winDmg` in resolveHit's damage line.
- Charge 14.

### Stages 3 and 5

- Stage 3 flips `healPer` from 0 to 1.
- Stage 5 sets the blade to 9.

### Stage 6

Stage 6 goes on stage 5's link: the labs' twelve rows as twelve anchored edits, four for the voice
and eight for the picture (§5). It refuses to go on twice, or on any other stage.

### What the builder refuses and checks

- It asserts the base BY CONTENT, never by which relic is last.
- It refuses to overwrite a link, to write a name that is not `sc-angelus*`, or to apply a stage out
  of order (`runs/builder_refusals.txt`; re-run with the review-r2 builder in
  `runs/builder_refusals3.txt`, where a stage 1 on a source that already carries Angelus also refuses).
- It replaces each anchor exactly once, or refuses.
- It strips comments, then checks:
  - the ult block;
  - the Math.random count;
  - each insert for `rng()`, `spawnFx`, `ultFx`, a write to the shared weapon (`w.* =`), or a hurt,
    knock, beat or hit stop.
- It runs `node --check` on the page and writes LF.
- **Stage 6** also refuses any insert that is not presentation (§5d), checks the inlined `fx.js` is
  untouched and the shared rune-crack fallback kept, and wires every arm, call and pass exactly once.
  Its refusals, `runs/stage6/refusals6.txt`, 10/10: the real builder refuses to go on twice, on stage
  3's link and onto the existing link; six scratch copies with ONE S6 row mutated are each refused by
  the rule that names it; and the unmutated copy writes the link byte for byte (§5e).

### It composes with the other builds

I applied stages 1, 2, 3 and 5 to the base and to 9 other sources: the chain's newest link and the
newest link of every in-flight scratch build.
- **The sources:** `sc-coldiron-temper-fx` (chain, 67cc3e6e05d5326e), `sc-tendril-fx`,
  `sc-onslaught-fx`, and the coldiron, ironhail, lightkeeper, lodestone, oracle and widowmaker scratch
  links.
- **On every one of them** the stages apply, the page parses, and the same lines are added
  (added-lines hash `cac1f0175114`) in place of the same two replaced lines
  (`runs/recheck_resume2.txt`, `runs/compose_test.txt`).
- **Onto the current chain tip:** at 22:30, with Coldiron / Temper committed to the chain, a fresh
  application onto `02-chain/sc-coldiron-temper-fx.html` gave the same result: 40 relics, the same
  added lines, 2 replaced (`runs/compose_chain_tip.txt`).
- **Again with the final review-r2 builder** (2026-09-28 02:31 PDT, `runs/recheck3.txt`), onto 11 sources:
  - the batch line's newest chain links, `sc-ironhail-fxout` (4b3775e5900172ea) and
    `sc-ironhail-sunder-fx` (b51c2539999dd272), and `sc-coldiron-temper-fx`;
  - the newest link of every scratch build: bindweed, coldiron, ironhail, lightkeeper, lodestone
    (now `sc-lodestone-b205-fx`), oracle, portcullis and widowmaker (now `sc-widowmaker-b1075-fx`).
  - Every one applies and parses, with 39 or 40 relics, added-lines hash `cac1f0175114` and 2 lines
    replaced.
- **With stage 6, and the final builder** (2026-09-29, `runs/stage6/compose6.txt`), stages 1-2-3-5-6
  apply to 14 sources:
  - the base, where they rebuild the scratch link byte for byte (`6356f75eb0b328e1`);
  - the chain's `sc-ironhail-fxout` (4b3775e5900172ea), `sc-ironhail-sunder-fx` and
    `sc-coldiron-temper-fx`, and the orchestrator's newest carries in `02-chain/`,
    `sc-widowmaker-fxout` (04fdd2e2daa17c26) and `sc-lodestone-b205-fx` (4568c2995d06f696), 41 relics;
  - the newest link of all 8 scratch builds.
  - Every one parses. Stages 1-5 add `cac1f0175114` as before, and stage 5 → 6 is the same +523 / -1
    lines everywhere (added-lines hash `4b9c29685fb0`). The labs also carried their rows onto 10 tips
    each (§5c, §5a).

**The first anchor Angelus does not re-emit (stages 1-5).** The spin insert consumes
`(f.ultVine ? 0 : f.w.spin) * f.spinMul(mods.spin)` (Bindweed's line). It has to: the lab's order of
multiplication puts the shaft scale between the spin and `spinMul`.
- Once Angelus is carried, a later builder that anchors on that exact string will refuse.
- On 2026-09-28 only `bindweed_build.py`, the line's author and already on the chain, contains it.
  No in-flight builder does.
- The damage insert keeps its anchor, `self.ultTree ? self.w.dmg * self.w.ult.winDmg : `, as a
  prefix. Every other anchor of stages 1-5 is re-emitted whole.

**Stage 6 consumes a second anchor:** `    const tr = f.trail;`, in `drawFighter`. The body trail's
row replaces it with `const tr = f.ascendFade > 0 ? [] : f.trail;` (reading 16) and does not re-emit
it. On 2026-09-29 no builder in `tools/` but this one contains that line, and no scratch build's
either. A builder carried after Angelus that anchors on it will refuse. Every other stage-6 anchor is
re-emitted whole: eight rows are `before` / `after` rows, and the other three replace rows carry
their anchor (the Sfx arms re-emit the shared rune-crack fallback, last and unchanged).

## 2. Stage 0 and the stages against it

**Stage 0** ran this command, on seed0 2207 and 2317, 660 fights an arm a block:

    ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic widowmaker --cell sanctified:twinblade
      --mech overlays/ascend.js --arms A,B,C,D --P hangY=300 --seeds 20 --foes <33>

**The built links** ran `ult_overlay.py --relic angelus --arms SHIP` on the same foes, seeds and side
(A). The SHIP arm plays the relic's own ultimate, at charge 14; the "charge=16.0" in its header is the
overlay's default.

```
                     lab on 151 (2207 / 2317)  pooled  published 141  BUILT (2207 / 2317)             pooled  gap
A  no ultimate       28.9 / 29.4               29.15   28.5           stage 1: 28.9 / 29.4            29.15   0 -- fight for fight
B  rise + shafts     47.3 / 46.4               46.85   43.9           stage 2: 45.8 / 44.5            45.15   -1.7
C  + the heal        65.0 / 69.4               67.2    62.7           stage 3: 69.5 / 69.8            69.65   +2.45
D  + smite 2 a hit   72.3 / 74.4               73.35   67.7           (not taken: brief §3)
```

### Published vs 151

151 reads above the design's published arms: +0.65 on A, +2.95 on B, +4.5 on C and +5.65 on D. Two
things changed at once:
- the runtime, from 141 to 151;
- the base: the design ran on `sc-trunk`, this is `sc-tendril-t3`, and its foes' ultimates have moved
  since.

The ordering and the lifts hold: C − A is +34.2 published and +38.1 here.

### Stage 1 is arm A, fight for fight

`runs/fight_compare.py` plays each of the 1320 (foe, seed) pairs twice:
- on the base, with the donor mutated exactly as arm A does it;
- on `sc-angelus`, as `angelus`.

It compares the winner, the steps, both sides' hits, dealt, crits and clanks, and both final hp.
- **Result:** 1320/1320 records are identical (`runs/stage1_vs_A.txt`).
- **Control:** the donor UNMUTATED differs on 1319/1320, so the comparison can fail.
- **The overlay's json agrees:** byFoe is identical 33/33 on both blocks, and so are the blows outside
  windows (18.78 / 18.68) and the win.
- **The brief's stage-1 gates** ("engine_ab on 40; verify 25–35%; tip_audit") were not run on stage 1
  itself. As in v100 and v101, the proof that stage 1 IS arm A to the fight covers them. The
  lab-roster SHIP run reads 29.15%, inside 25–35. engine_ab, verify and tip_audit ran on the final
  link (§4).

### The mechanism, lab against built

Side A, the lab's fights, pooled over 1320. The built rows come from `angelus_probe.py --sides A
--seed-step 11` on the same seeds (`runs/probe_*_labfights_*`). The probe's win rates equal the built
SHIP runs to the digit, so the hooks are inert.

```
                       casts   blows in / out   shaft hits a cast   blessing a cast   foe smite stacks   healed a cast
lab B (8s)             3.56    18.30 / 11.16    5.12                --                2.91
lab B at dur 9.92      3.52    22.32 /  9.21    6.30                --                3.06
built stage 2          3.44    21.14 /  9.47    5.96                --                2.95
lab C (8s)             3.78    19.52 / 12.04    5.11                5.11              2.94               (design: ~36 hp)
lab C at dur 9.92      3.80    24.00 /  9.98    6.25                6.25              3.09
built stage 3          3.63    22.37 / 10.31    5.95                5.95              2.97               43.7 hp (tickStatus)
```

**The build hunts like the lab does at the engine's window length, minus the rise.**
- **Why the windows differ.** A built window is 8s of the window clock. The probe counts 19.2-19.5% of
  window steps frozen, so a built window is 8 / (1 − 0.194) = **9.92s** of match time. The lab's window
  was 8 step-seconds, freezes included.
- **The arithmetic.** The lab at dur 9.92 lands 6.25-6.30 shaft hits a cast. Taking off the rise's
  0.35s of dark blades (× (1 − 0.35/8)) leaves 5.98-6.02. The build lands 5.95-5.96.
- **The heal follows the hits.** Blessing equals shaft hits, which gives **43.7 hp a cast** against
  the design's ~36, because 16% more shaft hits land.

### The win rate, attributed with controls

Each built control is a scratch copy of a built link with one thing changed (`runs/make_variant.py`;
`runs/ctl_*`, blocks 2207 / 2317):

```
                                                          stage 2 (arm B)          stage 3 (arm C)
lab, as designed (8 step-seconds; teleport, lit at once)   47.3 / 46.4   46.85      65.0 / 69.4   67.2
lab at dur 8 / (1 - 0.194) = 9.92 (the engine's window)    48.3 / 47.3   47.8       72.4 / 73.3   72.85
BUILT                                                      45.8 / 44.5   45.15      69.5 / 69.8   69.65
built, rise 0 (hung and lit on the cast frame)             47.0 / 46.8   46.9       70.8 / 69.7   70.25
built, the window clock running through freezes            45.5 / 45.2   45.35      69.2 / 67.1   68.15
built, both of the lab's conventions                       47.0 / 49.1   48.05      68.6 / 71.1   69.85
```

**Stage 2's −1.7 is the rise.**
- With the rise at 0, the build reads 46.9, against the lab's 46.85.
- So the 0.35s in which the blades are still blades is worth about −1.75. The design's open item 5
  said "~4%" of the window.
- A longer window adds little when the relic has only the shafts: +0.2 on the build, +0.95 on the lab.

**Stage 3's +2.45 is the window clock, minus the rise.**
- The window clock is worth +1.5 by the build's control and +5.65 by the lab's. The two controls agree
  within ~1.6 standard errors of their difference.
- The rise is worth −0.6.
- With both of the lab's conventions, the build reads 69.85, which is +2.65 over the lab's C. That is
  inside the lab's own block-to-block spread (65.0 / 69.4) and about 1.5 standard errors of a
  1320-fight difference.

**Nothing is mis-built.**
- The probe proves the mechanism sentence by sentence (§3), and the counts line up with the lab run at
  the engine's window length.
- The build keeps the engine's convention: every window cadence in the batch runs on the window
  tickers' clock.
- It also keeps the prose's rise and every designed number.

**The brief's gates:**
- stage 2, "relic ~44% at 11.95": 45.15;
- stage 3, "relic ~63%": 69.65, over because of the window clock;
- "~36 hp a cast": 43.7, because the longer window lands more shaft hits.

**Casts** read 3.63 against the lab's 3.78. The charge was rounded from 13.64 up to 14, which makes it
2.6% slower.

## 3. The probe (`angelus_probe.py`, one check per sentence, read inside the hooks)

### How it works

The probe wraps `tickRise`, `tickWeapon`, `resolveHit`, `tickStatus`, `fireUlt`, `step` and each
fighter's `apply`. It reads every event where it happens and rebuilds the engine's arithmetic:
- the smoothstep;
- the turn, `w.spin × shaftSpin × spinMul × dt × spinDir`;
- both blade tips at `R + reach × mods.reach × reachMul`;
- every blow's damage, from the captured crit and jitter draws.

A check that never ran counts as a FAIL. Each run is 456 fights: both sides × 38 foes × 6 seeds.

### The ten checks

- **[1] the rise:** the cast's record, the ease, the arrival at `rise` on the window clock, and the
  hang point held on ≥ 99% of lit steps.
- **[2] the hold:** pinned at the cast and re-armed every frame; the hung ball never moves; foe blows
  land on it.
  - **The re-arm is exercised, not assumed (review r2, finding 1).** Nothing on the roster clears the
    hold inside a window: "pinFree found cleared" reads 0 on every run. So a build that forgot to
    re-arm `pinFree` or `pinMax` would pass on natural fights alone.
  - Before every 50th window tick (`--force 50`, the default), the probe clears the three fields the
    re-arm owns: `pin`, `pinMax` and `pinFree`. `tickStasis` has already run that step, and nothing
    reads them before the tick, so on a correct build the tick restores them and no fight changes.
  - [2] fails a frame that ends un-held. Its coverage needs at least one cleared tick re-armed.
- **[3] the close:** a live caster is released to rest, and a dead caster's kill flight is untouched.
- **[4] the shafts:** their reach and geometry.
- **[5] the turn.**
- **[6] the damage,** with no shaft hit at full damage.
- **[7] the heal:** blessing = healPer × the hits delta, applied once, by side letter, and healed by
  `tickStatus`.
- **[8] nothing else:**
  - the tick makes no hurt, beat, hit stop or shake;
  - nothing is applied to the foe;
  - the cast files its one `ult` beat.
- **[9] the window:** held through every frozen step and +dt through each live one; `dur` long; closes
  on the caster's death; only Angelus carries `ultRise`. It does NOT close on the foe's death
  (reading 10): a tick that finds the foe dead and the caster alive must leave the window open, or
  [9] fails it as "closed early".
- **[10] no cast inside a window.**
- **Counts for the readings, not checks:**
  - windows still open when the match ends, by winner and by lit (reading 10);
  - ticks that find the foe dead and the caster alive (reading 10);
  - shaft hits on Twinshade's shades (reading 11).
- **Stage 6 adds [11] (the voices) and [12] (the picture's hook).** Each runs only where the link
  carries it, detected by its own presence. On stage 5's link the probe still prints 10/10 with every
  line as before (stages 2-3 carry neither). They, their results and their four mutants are in §5e.

### The results

**sc-angelus-rise (stage 2): 10/10.**
- 3.49 casts a fight and 5.77 shaft hits a cast; blows 20.73 in windows and 9.97 outside.
- The foe carries 2.89 smite stacks.
- The caster is held at (260, 300) on **100.00% of 1,646,067 lit steps**, and the hung ball moved on 0
  of 1,339,607 frame pairs.
- Foe blows landed on the hung caster 2.33 times a cast, with 0 knock taken (it never moved).
- Shaft tips average 702 units from the centre, which reaches past the floor from y 300.
- 19.0% of window steps are frozen.

**sc-angelus-heal (stage 3): 10/10.**
- 3.64 casts; 5.81 shaft hits and 5.81 blessing a cast.
- 43.0 hp healed a cast, measured in `tickStatus`.
- Blows 21.84 / 10.75; 19.3% of window steps frozen.

**sc-angelus-b9 (stage 5): 10/10** (`runs/probe_b9.txt`).
- 3.96 casts; 5.92 shaft hits, 5.92 blessing and 42.9 hp a cast; blows 24.32 / 11.89.
- 1548 closes: 1527 by the clock and 21 on the caster's death.
- The window clock held through 380,769 frozen steps and advanced +dt through 1,587,530 live ones.

**Re-run with the review-r2 probe, every number above came back identical** (the earlier runs are in
`runs/probe_v2/`). The new counts:

```
                          rise (stage 2)   heal (stage 3)   b9 (stage 5)
pinFree found cleared     0                0                0
hold cleared by probe     28,145           29,587           31,817
  ... and re-armed        28,112           29,559           31,785   (the rest were closes)
open at the match's end   211 / 456        207 / 456        260 / 456
  Angelus won / lost      105 / 106        152 / 55         133 / 127
  lit                     192              191              243
foe dead, caster alive    35 ticks         58 ticks         47 ticks
shaft hits on shades      51               81               90
```

- **The forced clears are inert on the build.** `sc-angelus-b9` with `--force 50` and with
  `--force 0` agrees in every count but the clear's own: the win (52.0%), the tallies, the blows and
  the smite (`runs/probe_b9_force0.txt`). Both runs also equal the pre-review run
  (`runs/probe_v2/probe_b9.txt`), apart from the new counts.
- **The lab-fight runs of §2 were re-run too** (rise and heal, both blocks, 660 fights each). Every
  mechanism line came back identical, and the wins still equal the SHIP runs to the digit (45.8 / 44.5
  and 69.5 / 69.8). So the hooks, the forced clears included, are inert.
- **pinFree was never cleared naturally:** 0 in the 456 × 3 fights here, and 0 in the 4 × 660
  lab-fight fights. It was also 0 in 500 fights against Ravelbone alone, the one foe that can clear
  it (both sides, 250 seeds from 204001, `--force 0`; `runs/probe_b9_ravelbone.txt`). Review r2 read 0
  in 400 more. So reading 4's path is real but never reached, which is why the probe forces it.
- **Reading 10 is not an edge case.** The window is still open when the match ends in 57% of b9's
  fights, whichever ball won. Stage 6 has to handle it (§5).
- **The foe-dead ticks** are foes killed by Angelus's own smite. It is a damage-over-time status
  (1.5 hp/s a stack), so it kills in `tickStatus`, in the fighter loop, before the tick: hp a hair
  under 0, smite on the foe at all 47, and no kill flight (`runs/foedead_diag.txt`, scratch
  `foedead_diag.py`). The window stays open for that one tick, and then `checkEnd` ends the match.

### The mutants

The mutants are scratch copies of the final link (`runs/make_mutants.py`, `runs/probe_mut_*`). Each
breaks one sentence and changes fights: b9 reads 52.0% in the probe. Each fails its own check and no
other.

```
m1-hang      hung 10 units high                         fails [1] only   53.7%
m2-clock     the window clock runs through freezes      fails [9] only   45.8%   (the lab's clock)
m3-release   the close keeps the banked velocity        fails [3] only   49.1%   (released at thousands of px/s)
m4-reach50   the shafts at reachMul 5                   fails [4] only   45.0%
m5-spin      the shafts at full spin                    fails [5] only   74.1%
m6-dmg       the shafts at full damage                  fails [6] only   84.6%   ("FULL DAMAGE", named)
m7-heal      two blessing stacks a shaft hit            fails [7] only   55.7%
m8-pinfree   the re-arm drops pinFree (review r2's r1)  fails [2] only    0.0%   (under the probe's clears)
```

All eight were re-run with the review-r2 probe (`runs/mutants_made3.txt`, `runs/probe_mut_*`). m1-m7
are byte-identical to the earlier set and read the same win rates as before.

**m8-pinfree is review r2's finding 1, made a mutant.**
- **On natural fights it is invisible.** With `--force 0` it plays b9's 456 fights exactly: 52.0%,
  every count identical, 10/10 (`runs/probe_mut_m8-pinfree_force0.txt`). That is why the earlier
  probe could not fail it.
- **Under the probe's clears it fails [2] alone, and it changes fights.** Once a clear lands, the hold
  stays un-freed. `tickStasis` then stuns the blades for the whole `pin` (`f.stun = max(stun, pin)`,
  re-armed to 8 every frame). The shafts stop turning, and the stun outlives the window: blows fall
  to 0.08 in windows and 3.15 outside, and the win to 0.0%.

The first reach mutant used 0.95 (`runs/probe_v1/probe_mut_m4-reach`). It failed [4] but did not move
the win rate at all, because reach 9.5 still spans the hall from y 300. It is kept as the record, not
as a control.

### Two inserts chain_audit cannot watch

- **The spin product:** its marker line is shared with the base.
- **The one-line damage edit:** it is not in chain_audit's table.

The probe watches both instead: [5] and [6], with mutants m5 and m6.

## 4. Stage 5: the blade — 9

The sweep ran on `sc-angelus-heal`, both sides (`relic_rate.py --n 10`, every other relic a foe, 760
fights a block), seed0 2207 and 2317: 1520 fights a point (`runs/stage5_rr_*`).

```
blade   block 1   block 2   pooled   side A   side B   mean fight
 8.5    46.3      46.2      46.25    48.0     44.45    74.6s
 9      50.7      51.6      51.15    53.3     48.95    73.7s
 9.5    52.4      54.5      53.45    53.3     53.6     72.9s
10      58.8      56.1      57.45    60.3     54.6     71.9s
```

### The pick

- **The crossing is ~8.9**, interpolated between 8.5 and 9. That is just under the brief's "Expect
  9–9.5" and the design's "~9.3".
- **No knob moved, because the brief names none for the blade.** The only lever the design names is
  the hang height, and that is Rick's (design §7 item 1). The brief also says: "do not 'improve' the
  hang height upward".
- **Blade 9** is the measured point nearest 50% inside the band, at 51.15%.

### The link reproduces the measurement exactly

`relic_rate` on `sc-angelus-b9` with no `--set` equals the `--set dmg=9` run on `sc-angelus-heal`, key
for key in the json, on both blocks: every foe's rate, both sides, the type rates and the mean
duration (`runs/stage5_rr_built_b9_*`).

### The ladder at blade 9

40 fights a foe (`runs/ladder_b9.txt`); pooled 51.1%.
- **By type:** warhammer 78, flail 62, bow 59, scythe 48, greatsword 37, **twinblade 19**.
  - The design had 81 / 68 / 68 / 54 / 35 / 19 at blade 10.
  - The inverted counter holds: the fast blades that can reach a hanging target beat it, and the slow
    heavy ones cannot.
- **Worst:** Starwarden 2.5, Spellbreaker 5, Bloodmirror 12.5, Lightkeeper 15, Emberedge 15, Twinshade 20.
- **Best:** Bulwarden 92.5; Morningstar, Duskreave and Censer 90; Shroudmaul 87.5; Lastlight, Ravelbone
  and Marrowdraw 85.
- **The type spread is item 12/32, and Rick's.**

**Angelus lengthens its fights.** Its mean fight is 73.7s (both sides), against the roster's 61.5s.
While it hangs, the foe can reach it only by jumping.

### The gates on the final link

**engine_ab, sc-tendril-t3 → sc-angelus-b9, the 38 base relics, n=6: 4218/4218 identical.**
- 38/38 distinct winners; fights of 22.7-114.9s.
- Files: `runs/engine_ab38.txt`; the ids are in `runs/ids38.txt`.
- Adding Angelus moves no other fight.

**verify --n 40 on sc-angelus-b9 (39 relics): 11/13** (`runs/verify_b9.txt`).
- Angelus reads 47.2%. That is side B, because verify plays an appended relic as side B.
- Every relic is in 30-70%, and "both sides can win every matchup" passes.
- **The two reds are the clock bands, which have been red on every link since the minute pace:**
  - pairing means run 38.3-98.4s, and the worst pairing is Lightkeeper/Starwarden, not one of Angelus's;
  - the overall mean is 61.5s.

**tip_audit** matches the base's except for the file name. That includes the base's own MISSING entry
(burn `feed`), which is not this relic's (`runs/tip_audit_{base,b9}.txt`).

**chain_audit** `--builder angelus_build.py`, with relic = tip = sc-angelus-b9: **ALL 8 INSERTS SURVIVE**.
- **Control:** with the base as the tip, it loses 7 of 8 and exits 1.
- The eighth, the spin product, reads "ok" there because its marker line is shared (§3).
- **Re-run with the review-r2 builder,** since chain_audit reads the builder: the same result, all 8
  survive (exit 0), and the control loses 7 and exits 1 (`runs/chain_audit_b9.txt`,
  `runs/chain_audit_control.txt`).

**The gates that read the links did not move in review r2.** The four links are byte-identical
(`runs/rebuild3.txt`). engine_ab, verify, tip_audit, relic_rate and the built-vs-lab runs therefore
stand as run. The builder's refusals were re-run and are unchanged (`runs/builder_refusals3.txt`).

## 5. Stage 6: the picture and the voice — `sc-angelus-b9-fx`

Picked on measurements under Rick's "you pick i overrule", by two labs run in parallel: the picture lab
(in scratch; its row builder `ang_rows.py` 146bc1f26e29bc5e) and `tools/angelus_voice_lab.py`
(2b3b971065782bf9). Built as `angelus_build.py --stage 6` on stage 5's link: twelve anchored edits,
byte-exact to the labs' own row files (voice `70f47a5acf37e4f7`, 4 rows; picture `324d3654c51b4d04`, 8
rows).
- The rows the labs returned equal the files.
- No two rows share an anchor, so none were merged, and no row's anchor sits inside another row's
  anchor or code.
- The picture rows alone reproduce the picture lab's stamp (`32d61ac685db232f`), and the voice rows
  alone the voice lab's page (`32d55d74179c4335`).
- The two sets give the same bytes in either order (the voice lab also tried 62 interleavings), and
  those bytes are the link:

```
sc-angelus-b9.html          stage 5                                    db58100b3aa0092a
  -> sc-angelus-b9-fx.html  stage 6  the picture and the voice         6356f75eb0b328e1
```

That is +28,189 characters, +523 and -1 lines (`runs/stage6/gen_s6.txt`, `runs/stage6/built_fx.txt`).
The builder is `0e4e2fc3ff5813de`, and it rebuilds all five links byte for byte from the base
(`runs/stage6/rebuild6.txt`). Stage 6's readings are 12-18 in its docstring (§5d).

- **The picture sheet:** `05-reference/v104/angelus-picture-sheet.png` (2200x3259, 240673bf195b7c4f),
  every frame from the picture lab's stamped page. Its rows: the resting silhouette among the seven
  twinblades; the cast and the rise across the whole hall (Grudgebearer 2213); one shaft blow followed
  to its heal; the close by the clock (Dawnbringer 4242); the kill with the window open (Grudgebearer
  2213); and the window's key states against a white sanctified foe (Dawnbringer 2207), a dark foe
  (Nightfell 2211) and an ordinary one (Spellbreaker 99015, Angelus as side B).
- **The voice picks:** `05-reference/v104/angelus-pick-sequence.wav` and the real-window pair (§5c).
  The wavs are gitignored.

### 5a. The picture (v74 §6.1), as built

- **Canopy's rule.** The picture reads `ultRise && !over && alive` and keeps its own state on the
  fighter: `ascendFade`, `ascendAge`, `ascendLit`, `ascendOut`, `ascendSeen`, `ascendHeal` and
  `ascendFx` (the threads). `tickAscend` drives it from `tickPresentation`, on the presentation clock,
  which runs through hit stops and after `over`. The simulation reads none of it. Its only other
  writes are `m.tags` and `m.taught` (the tag rule). It never uses `m.ultFx`.
- **The rise.** A column of light from the ball to the floor comes up over 0.05s, and fades over
  0.4s once the ball arrives (half-width 0.8R at 0.24, the core at 0.45). The halo is a ring at r
  1.1R in the school's glow, line 2.6 at 0.85, drawn source-over and NOT `lighter` (the design's
  words). It comes up over the 0.35s rise and goes with the close.
- **The shafts.**
  - The blades are drawn at REST length. Each shaft's light runs from the shell to whichever is
    nearer: the end of the hit segment, or the edge of the live hall (inset-aware, and clipped). So
    nothing is drawn past a wall: the design's "from the ball to the floor or wall". Stages 2-5 drew
    the radiant art at reach × 10, about 620-680 units, through the walls.
  - The body is a soft bar 10 units wide at half its peak (half-width 7), at 0.55, source-over. Its
    edge is a warm #FFD98A, so it reads as light and not as a white rod.
  - The 3-unit core is the only part under `lighter`, at 0.8, with both shells cut out of it (the
    design: "Under `lighter` ONLY the core").
  - An ignition flare runs for 0.12s at the arrival, and each shaft's foot throws a pool of light (r
    18 at 0.45) where it meets the hall.
  - The motes: 8 a shaft, drifting down at 90 units/s just outside the body, where the dark floor
    shows them. This is the design's field, drawn (§5b). They are placed by `shellHash` and the
    clock, never the RNG.
  - `bladeSegments` and the hit geometry are untouched.
- **A shaft hit.** The blade's own flash is the engine's. A gold thread with a dark-rimmed bead runs
  from the blow's contact point up the nearest shaft to the ball, over 0.25s, drawn over the cores.
  The contact point is the `hit` beat `resolveHit` filed that step, read and never written. On a
  blow to one of Twinshade's shades, the thread starts at the shade (reading 11).
- **The heal.** When `riseTally.bless` rises (the next live step), the halo flares gold for 0.3s and
  BLESSING n goes up on the caster. There is one tag at a time: a tag already up takes the new count.
  The first one teaches.
- **The close.** The shafts shorten to blades over 0.3s and dim to 0.35, and the halo goes. The
  ball's drop and landing are the engine's.
  - **At `over`** (reading 10: the window the sim leaves open) it is the same close on the
    presentation clock. The blades are drawn at rest while `reachMul` stays 10 through the verdict.
  - **No presentation-only drop after the kill.** The ball stays where the frozen sim holds it, like
    every relic's ball at the verdict. **Rick's to overrule.**
  - A dead caster is drawn by `drawShatter`, which draws no weapon, so its halo and shafts go with
    the ball.
- **Added: the body trail's ghost.** `move()` feeds the body trail, and a pinned ball skips `move()`.
  So through stages 2-5 the stale trail drew a ghost of the ball at the cast point for the whole
  window. It is hidden while `ascendFade > 0`, by a replace row on `    const tr = f.trail;`. That is
  the second anchor Angelus consumes (§1).
- **The silhouette** is the shipped `_tbRadiant`, unchanged: |dL| 0.234 at 453x805, 2nd of the 7
  twinblades (Spellbreaker 0.289; then Widowmaker 0.171, Coldiron 0.159, Starwarden 0.156,
  Twinshade 0.151, Thornshear 0.144).
- **The hexagon needs nothing:** `pinFree` is 1 for the whole window, so `_drawField` draws none
  (§5h).

**Code's picks** (you pick, I overrule): the close 0.3s (the design's), the thread 0.25s, the flare
0.3s, the ignition 0.12s; the column in over 0.05s and out over 0.4s; the halo's line 2.6 at 0.85;
the pools r 18 at 0.45; 8 motes a shaft at 90 units/s; the body's edge #FFD98A and the core at 0.8;
no SPECS field (§5b).

**The picture lab's numbers** (Chromium 151, 540x960, the post chain on; Electron 44 on the RTX 3070):
- **Bloom**, 9 fights and 87 frames, against white sanctified, umbral, dwarven and runic foes.
  - Against the bare hall (every piece of window art hidden, the blades at rest), the picture's share
    of the arena-mean lift is at most **+0.0051** (min -0.0069). The lab gated it at +0.02; the
    design's gate is +0.03. The raw arena luma it adds is at most +0.0209. Against stage 5's ×10
    placeholder it is +0.0052.
  - **Controls that must fail, and do:** an r400 lighter fill at 0.35 (the Harrowing's class) gives
    +0.076 and fails on 57 of 87 frames; a lighter disc on the caster pushes its disc past 0.90 on 69
    of 72 window frames; 60-unit lighter bars lift a foe's disc by up to +0.447.
  - **The discs.** The caster's moves -0.008 to +0.007, and is past 0.90 on 1 frame both with and
    without the picture. The foes', art only: sanctified -0.067 to +0.002 (the -0.067 is Lastlight in
    a hit stop, where the chain adapts: CLAUDE.md 4.1d, not the art); umbral down to 0.000 (-0.19
    with the BLESSING teaching panel over a distant foe); dwarven -0.013 to +0.001; runic 0 to +0.004.
    No foe's disc is pushed toward white.
- **Legibility**, median |dL| of each piece's own pixels, out of a hit stop / in one:
  - halo 0.340 / 0.342, and the heal flare 0.337;
  - shaft body 0.293 / 0.293, cores 0.098 / 0.188;
  - motes 0.404 / 0.380; the thread 0.200 (in a stop);
  - pools 0.101 / 0.057; the column 0.123 / 0.037 (the in-stop frames are the cast's own 0.08s stop,
    0.05s into the column's rise);
  - the BLESSING tag 0.061 / 0.153; the close 0.225 / 0.132;
  - the blades 0.277 in the window and 0.220 at rest.
  - Everything the picture changes, by state: rise 0.13, lit 0.19, hang 0.24, hit 0.40, heal 0.22,
    close 0.23.
- **Sim identity** (15 pairs, 13 with Angelus on both sides): a per-step hash of the positions,
  velocities, hp, statuses, charge, pins, `reachMul`, hits, `ultRise`, `riseTally`, shades and beats,
  up to the kill, is identical to stage 5's on all 30 runs, undrawn and drawn. **Control:** a 1e-9
  write to the foe's vx in the heal branch differs on all 13 Angelus fights and matches on the 2
  without.
- **The same 15 fights drawn**, to 3s past the kill: 23,827 draws, 19,958 of them picture frames
  (3,827 in a hit stop), and nothing threw.
  - 293 lit shaft blows, 293 threads, each on the nearest shaft inside its drawn length.
  - 293 heals, 293 BLESSING tags with the right count within 3R of the caster.
  - 100,385 shaft ends checked, 0 past the live hall.
  - A close by the clock reaches 0 in 0.29-0.58s.
  - The window was open at the kill in 9 of 13. With the caster alive (4), the verdict was drawn
    with the blades at rest on 66-67 frames each, 0 bad, while `reachMul` stayed 10. With the caster
    dead (5), the picture went with the shatter, its fade at 0 in 0.29s.
  - The shared weapon row `w` was never written.
- **Reading 11** (12 Twinshade fights, both sides): 321 lit blows, 90 of them on a shade. 321/321
  threads start at the blow's contact point, within 1 unit, 90/90 at the shade. **Control:** a thread
  started at the foe misses 90/90.
- **Frame cost** (Electron 44, RTX 3070 ANGLE, 453x805, chain on; one process per arm, alternated
  ON/OFF/OFF/ON):
  - the picture's own passes (`drawAscend` + `drawAscendTop`): 0.05-0.15 ms a frame;
  - Angelus's `drawWeapon` in the window (bodies, motes, blades at rest): 0.20-0.35 ms, against
    0.40-0.50 at rest and 34-43 ms for stage 5's ×10 art;
  - the whole frame while lit, stage 6 against stage 5: Dawnbringer 78.6 vs 106.2 ms, Gravemourn
    63.1 vs 91.2, Spellbreaker 70.5 vs 336.9. Rest and rise frames are equal.
  - Stage 5's ×10 art was the costly one, for a reason that is not this relic's: §6, the orchestrator.

### 5b. No field in `fx.js` — the motes are drawn instead

The design says "Field: light motes drifting down the shafts, both copies" (v74 §6.1), and the brief's
stage 6 says "Field in both copies". **No SPECS entry was added: `fx_spec` is NONE, and both `fx.js`
copies are as they were.** The picture lab measured why a field cannot carry this (its `fxprobe`, on
stage 5's link, 133 Ascension windows, 16 foes × 2 seeds, both sides):
- A SPECS field rides the one `m.ultFx` slot, which has no `life` entry for Angelus, so it takes the
  default. Angelus holds it for a median **0.633s** of window clock (max 0.717): 7.4% of the window,
  and 4.36% of the lit time. The shafts only light at 0.35.
- The slot is lost to the opponent's cast in 21 of 133 windows, expires in 109, and ends with the
  match in 3.
- A field fires once, at the cast position. That is a median **226 units** (p10 79, p90 383) from the
  hang point the shafts turn about.

So a slot-borne field would be gone before the shafts light, would sit on the floor the ball has
left, and could not follow two turning shafts. The motes are drawn in the world pass instead, down
each shaft, for the whole window (§5a). That is the Zenith (v98) and Canopy (v99) precedent.
- **The builder edits neither copy** (reading 17). Stage 6 refuses to write if its edits touched the
  inlined copy (the text from the inlined fx.js header to THE ULT FIELDS must be byte-equal before
  and after).
- **So the carry has nothing to take out of `fx.js`** and nothing to stamp: `fx_remove.py` is not
  needed for Angelus.
- **Rick's to overrule.**

### 5c. The voice (v74 §6.2; `tools/angelus_voice_lab.py`, lab sha 2b3b971065782bf9)

**Reproduction control:** v88's published rune-crack (0.608 / 450 ms) and hit at 11.6 (0.443 / 80 ms)
come back on this PC. Before stage 6, Angelus's cast WAS rune-crack (it had no arm and fell through,
to 6e-8). Now its cast sits at register 0.631 against rune-crack.

**The cast — VOWEL, of 5.** D4, A4 and D5 (the score's iv: root, fifth and octave) as three sines.
Each strike carries its 2nd and 3rd partials at 0.3 / 0.12, and each tone is held by re-striking it in
phase, at its own whole cycles, about every 11 ms.
- It swells +11.9 dB to a crest at 445 ms, which is where the ball arrives (measured 0.42s after the
  cast voice, median: the 0.08s hit stop plus the 0.35s rise). The design's "0.6s" is the whole
  voice: audible 605 ms, flutter 0.3 dB, no dips.
- Every tone is within 0.1 cents. Its crest is -2.8 dB against Angelus's own blow at 9, and +16.5 dB
  over the wall tick.
- Its register is at most 0.61 against any voice in the game (Starwarden's cast), 0.46 against the
  seal and 0.54 against Zenith's cast.
- PURE, REED and STACK also pass the rule and lose on register (0.67-0.69). CHORUS is out.
- **Controls that fail, as they must:** STRUCK, DYAD, OFFBEAT and RC-NOW. RAW is a reference only:
  v97's phase finding does not bite at 294-587 Hz.

**A shaft hit — SKY, the tap.** A glass rod (partials 1 : 2.76) at C8, D8, E8, G8 and A8 (4186-7040
Hz), one step of A-minor pentatonic for each blessing count, 1 to 5. The count is the caster's after
the heal; at the cap it stays on 5.
- 70 ms (the design's), centroid 4.8 kHz, no noise.
- -9.3 dB against the shaft's own blow (the hit voice at 3.6), and +9.3 dB over the wall tick.
- Register at most 0.51 (the wall tick), 0.30 against Zenith's tick, 0.14 against the heal chime.
- Every tap below C8 sat on the spark collect or Zenith's tick (0.92-1.00). That is why it is this
  high: it is the only free register for a glass tap in this game.

**The close — STEP.** The cast's chord steps down a fourth, 0.15s in, to A3, E4 and A4 (iv → i: a
plagal "Amen"). This is "the chord resolving down".
- Audible 590 ms, -3.0 dB against the cast. The old tones are 21.8 dB down by 300 ms.
- Register at most 0.62 (the seal).
- **Controls that fail:** AGAIN, UP, OTHER and GLIDE.

**The landing — DEEP. NEW: the engine had no thud,** only its 3 kHz wall tick, which every floor
contact plays and still plays under this. A sine falling from 95 to 42 Hz, under noise low-passed at
220 Hz.
- Audible 115 ms, with all but 0.3% of its power under 250 Hz. -6.7 dB against the blow.
- Register at most 0.77 (the death voice), 0.43 against the blow.

**The SFX row:** the four arms match the lab's candidates to within 1.3e-7 (tolerance 1e-5); the
game's 127 other voices are unchanged (worst 1e-7).

**In fights** (the voice lab's 152 fights, seeds 104601-104602; the probe counts the same things on
456, §5e):
- 152/152 fights identical, and every other voice call identical. `riseTally` differs by `falling`
  only. **Control:** a sim write in the row leaves only 1 of 152 identical.
- 606 casts, 606 cast voices; 3,555 heals, 3,555 taps (counts 1-5: 585 / 563 / 544 / 508 / 1,355).
  A tap sounds a median 0.07s after its blow's hit voice.
- 512 closes by the clock with both alive, 512 chords; 470 landings, 470 thuds (42 fights ended
  before the ball landed). The fall from the close to the landing: 0.52-7.32s, median 1.17s; 96 of
  the 470 drops fall straight.
- 8 death closes, 0 clock closes on the step the foe died, and 86 windows still open at the end: none
  of them plays a chord or a thud.
- **A real window** (Starwarden, side A, seed 104602, 12 shaft hits), mixed with and without the new
  voices: the taps +6.7 to +64.5 dB over the fight in their band; the cast +12.9 / +9.9 / +20.8 dB at
  D4 / A4 / D5; the close's tonic +7.2 dB at A4; the thud +12.4 dB at 79 Hz.

**Flagged for Rick, not gated** (the lab's FOR RICK section):
1. **Cost.** The VOWEL cast is 393 synth calls, 12-18 ms of main thread a call on this busy PC, and
   the close 9-14 ms. The tap and the thud are 0.1 ms. The shorts render audio offline and do not
   feel it. The live app may drop a frame at the cast, inside the cast's own hit stop. PURE passes
   every gate at 131 calls (4.7-5.1 ms) and loses only the register tiebreak (0.67 against 0.61).
2. **The tap sits at 4.2-7 kHz,** the only free register for a glass tap in this game.
3. **The thud is 42-95 Hz,** which phone speakers will not play.
4. **The thud waits for the first floor contact.** A knocked drop lands later (a median 1.17s after
   the close; 80% of the drops were knocked). The other reading is a fixed-delay thud inside the
   close voice.
5. **No close voice at the kill.** The other reading would sound over the death voice.

The ear clips (gitignored): `05-reference/v104/angelus-pick-sequence.wav` (the cast; five blows each
followed by its tap, at counts 1-5; the close; the landing over its wall tick) and
`angelus-pick-real-window.wav` / `angelus-pick-real-window-without.wav`.

### 5d. Stage 6 on the simulation's path — declared (builder readings 12-18)

Stage 6 puts exactly three lines on the step's path that are not the presentation clock, and each is
one `SFX.play` call (reading 14). `SFX.play` draws nothing and writes nothing the simulation reads,
and headless it returns on its first line.
- **The tap,** in `tickRise`'s heal, after the blessing lands: once per tick that heals, with n the
  caster's blessing stacks. A tick healing two hits at once taps once (1 such tick in 456 probe
  fights).
- **The chord,** in `tickRise`'s close, only when the window closes BY ITS CLOCK with both fighters
  alive (reading 15). It also sets `riseTally.falling`, on the probe's tally, which nothing in the
  simulation reads.
- **The thud,** in `move`, on the caster's first floor contact after that close, the caster alive
  (reading 18). It clears the flag.

The picture finds everything by watching (reading 13): the window off `ultRise`, a shaft blow off
`hits` rising while lit (the blow's `hit` beat for its point), a heal off `riseTally.bless` rising. So
neither `fireUlt`, `tickRise` nor `resolveHit` makes a call for it. Its one hook, `tickAscend`, runs in
`tickPresentation`. It writes its own `ascend*` fields, the BLESSING tag and `taught`, and nothing
else. It draws no RNG; the jitter is `shellHash`.

The builder refuses to write any stage-6 insert that:
- draws the RNG, uses `Math.random`, `spawnFx` or the ultFx slot;
- calls into the simulation (apply, hurt, heal, resolveHit, knock, beat, float, fireUlt, a ticker...),
  or names a beat, hurt, knock, ring, shake or hit stop;
- writes the shared weapon row, or anything but what its table allows (its own `ascend*` fields, a
  thread's clock, a tag's count, `taught`, the landing flag, the canvas and the synth's nodes);
- puts on the sim path anything but those three voice calls, whole, each in its own row;
- plays a voice anywhere else, strikes the synth outside the Sfx arms, or tags outside `tickAscend`.

It also refuses if the inlined `fx.js` moved, if the shared rune-crack fallback is not kept once and
after Angelus's arms, or if any arm, call or pass is not wired exactly once. The probe's [1]-[10] see
none of it: every line of them is identical on stage 5's link and stage 6's (§5e).

### 5e. Stage 6's gates — every one able to fail

The files are in `runs/stage6/`.

- **Builder refusals, 10/10** (`refusals6.txt`, `refusals6.py`).
  - The real builder refuses to go on twice ("'tickAscend' is already in this source"), on stage 3's
    link ("stage 6 goes on stage 5"), and onto the existing link.
  - Six scratch copies of the builder, each with ONE S6 row mutated, are each refused by the rule
    that names it: the picture's heal flare writing `foe.vx`; the motes drawing the RNG;
    `tickAscend` reading the ultFx slot; the motes playing the tap; the chord on every close, a
    death's included; the rune-crack fallback dropped.
  - **Control:** the unmutated builder, copied to scratch and given the same call, writes the link
    byte for byte (`6356f75eb0b328e1`).
- **engine_ab, stage 5 → stage 6, ALL 39 relics INCLUDING Angelus, n 6: 4446/4446 matches identical
  field for field.** No page errors; 39/39 distinct winners; 4446 distinct seeds; fights of
  20.3-118.1s (`engine_ab39.txt`, the ids in `ids39.txt`). Presentation moves no fight.
- **angelus_probe (`fa5ee160cbbe177c`): 12/12 on the stage-6 link** (456 fights, 6 seeds;
  `probe_fx.txt`). Every line of checks [1]-[10] is identical to stage 5's own run
  (`../probe_b9.txt`): 3.96 casts a fight, 5.92 shaft hits and 42.9 hp a cast, 52.0%, 260 of 456
  windows still open at the end. Two new checks, each run only where the link carries it:
  - **[11], the voices** (read through `AC.SFX.play`, which is a no-op headless; only Angelus's four
    `ult` arms are read, so a ward's shatter, which plays its own crit HIT voice inside `hurt()`, is
    not one of them):
    - 1,808 casts, each exactly one cast voice; no foe's cast plays one;
    - 10,699 healing ticks, each exactly one tap, its n the caster's blessing after the heal (counts
      1-5: 1,749 / 1,683 / 1,607 / 1,500 / 4,160); 1 tick healed two hits at once and tapped once;
    - 1,527 clock closes with both alive, each exactly one chord; none on the 21 death closes, and 0
      clock closes found the foe dead;
    - 1,401 landings, each exactly one thud, in `move`, on the caster's first floor contact after
      the chord. **Every chord is accounted for:** 1,401 thuds + 67 fights that ended before the
      ball landed + 59 balls the next cast hung again in mid-air before they landed = 1,527;
    - silent through 2s of the verdict: 260 fights with the window left open, 196 with it shut;
    - none anywhere else (a foe's cast, the picture's hook, any other step).
  - **[12], the picture's hook** (`tickAscend`, wrapped):
    - 7,622,890 calls, every one changing nothing of the simulation's (both fighters' own numbers,
      flags and strings but `ascend*`, every status, the window, the tally, the pin's rest, the
      blade cooldowns, the shared weapon row and its ult; the match's own fields and every array's
      length but `tags`) and drawing no RNG;
    - up on all 3,558,925 calls in an open window;
    - 1,808 closes, each a fade to 0 over exactly 0.3s: 1,527 by the clock, **260 AT THE KILL with
      the sim's window still open** (reading 10), and 21 at `over` with the window already shut (a
      caster killed in the fighter loop: the tick closes the window, and the match is over by the
      picture's next tick);
    - 10,697 heals, each with the halo's flare and a BLESSING tag with the caster's count on the
      caster (the other 2 of the 10,699 healing ticks came in a step that ended the match, and the
      picture draws no flare at the verdict);
    - 10,700 threads for 10,700 shaft blows seen lit, none for anything else;
    - after 2s of the verdict the picture is down in all 260 fights the sim left open and the 196
      others.

  **Detected by their own presence** (the tap's arm in `AC.SFX.play.toString()`, `tickAscend` on
  the Match). **On stage 5's link the same probe runs [1]-[10] only and prints 10/10,** every line
  identical to stage 5's own run (`probe_b9_newprobe.txt` against `../probe_b9.txt`).

  **One probe edit during the gate.** The first full run (probe `1e86bf4805b46696`,
  `probe_fx_1e86.txt`) passed 12/12, but its landing counts did not add up: 1,401 thuds + 93 fights
  ended before the landing = 1,494 of 1,527 chords. The missing 33 are balls the next cast hung
  again before they touched the floor (the cast pins the ball and the flag stays up, so the thud
  waits for the landing after a later close). The probe now counts that at the cast, and [11]
  requires thuds + unlanded + re-hung = chords. Every other line of the two runs is identical.
- **The probe's controls, each able to fail** (2 seeds, 152 fights; `probe_mut6_*.txt`; made by
  `make_mutants6.py`, `mutants_made6.txt`; the fights compared record for record by `mut_fights.py`,
  `mut6_fights.txt`):

```
the stage-6 link, unmutated                                                 12/12              the reference
m9-chorddeath  the chord on every close, a death's included (reading 15)    fails [11] alone   0 of 152   5 chords on a death
m10-overopen   the picture reads the window without `over` (reading 10)     fails [12] alone   0 of 152   "the close is not a fade" at the kill (21,283)
m11-picwrite   the heal flare nudges the foe's vx by 1e-9                   fails [12] alone   148 of 152 "the picture wrote the simulation: vx" (3,595)
m12-thudall    a thud on every floor contact, no clock close needed         fails [11] alone   0 of 152   "a landing thud with no clock close" (1,088)
```

  Three of the four move no fight, and the probe still sees them. m11 changes 148 of 152 fights, and
  [1]-[10] still pass it: a picture that writes the sim shows only in [12] and in engine_ab. Under
  m10 the picture is still up after 2s of the verdict in 44 of the 83 fights the sim left open (m10
  still closes on the caster's death): the defect reading 10 warned of.
- **Drawn sim identity on this link** (`drawn_ident.py`, v106's, for Angelus):
  **6/6 identical** (`drawn_ident.txt`). The picture lab's drawn arms ran on its own page, without
  the voice rows, so this was re-run on the stage-6 link itself. Each fight is run three times in one
  page:
  - undrawn (`m.step` only);
  - drawn the way the app draws it (`AC.__inject`, then `AC.__draw` every second step at 540x960);
  - drawn, with a control write.

  Every run goes through the kill and 2s of the verdict. The state at the kill must be identical:
  steps, t, the winner, both fighters' hp, x, y, vx and vy, and Angelus's rise tally. The six are
  Grudgebearer 2213, Nightfell 2211 and Twinshade 104001 with Angelus as `a`, and Dawnbringer 4242,
  Spellbreaker 99015 and Ravelbone 5150 with it as `b`. All six are identical drawn: 27,727 draws,
  13,941 of them with the picture up, 0 thrown. The window was open at the kill in all six, so the
  close at `over` was drawn every time. **Control:** a 1e-9 write to the foe's vx after every draw
  while the picture is up differs on 6/6. The run was split across two browsers (fights 1-3, then 4-6
  with the script's index argument), and both sittings are in the file.
- **render_ab: the other relics' pairs 24/24 frames pixel-identical** (Paradox v Heartwood 25064,
  Twinshade v Lastlight 991, Bulwarden v Vinesower 70707, Axiom v Grudgebearer 31337;
  `render_ab_others.txt`). **Control:** Angelus v Slagheart 104112 at six times inside the clip's
  window (31.4-40.6): **0/6 identical**, every frame differs, as it must (`render_ab_ctl.txt`). The
  arena luma moves from the ×10 placeholder's 28.9-30.9 to 26.8-30.1: darker while lit, lighter only
  at 31.4, where the column rises. The picture lab's own run on its page: 54/54 on other relics, and
  its controls differed exactly at the window's times.
- **chain_audit** `--relic <fx> --tip <fx> --builder angelus_build.py`: **ALL 20 INSERTS SURVIVE**
  (S1 1, S2 6, S3 1, S6 12). **Control:** stage 5's link as the tip loses all 12 of S6, exit 1
  (`chain_audit_fx.txt`, `chain_audit_fx_control.txt`).
- **tip_audit:** identical to stage 5's (`../tip_audit_b9.txt`) apart from the file name
  (`tip_audit_fx.txt`), the base's own burn `feed` entry included.
- **The carry re-applies** (`compose6.txt`, `compose6.sh`): stages 1-2-3-5-6 on 14 sources, every one
  parsing, with stage 5 → 6 the same +523 / -1 lines everywhere (§1).
- **shell_identity: NOT run here.** The app's json is shared; the orchestrator runs it on the carried
  link. The nearest measurement is the picture lab's Electron frame-cost runs (§5a).
- **The labs' own gates:**
  - The picture: sim identity on 15 fights undrawn and drawn with every step hashed, and its
    control; bloom, legibility, silhouette, frame cost; the rows in 62 orders; reading 11's threads
    (§5a; `picture_*.txt`).
  - The voice: the reproduction control; every pick's rule with its failing controls; 152/152 fights
    identical, and its sim-write control identical on only 1/152; end to end on b9 (76/76) and on
    Angelus rebuilt onto `sc-lodestone-b205-fx` (80/80); the rows in every order and on 10 tips
    (§5c; `voice_*.txt`).

### 5f. The clip (Rick's to overrule)

`tools/_angelus_pick.py` (from `_ironwood_pick.py`, with `_widowmaker_pick.py`'s exclusions) scores a
window on §6. Angelus plays side A, as the clip does. A window qualifies only if it closes BY ITS CLOCK
with both alive (the only close with the chord and the drop) and the ball LANDS inside the clip's
tail (the thud), and it shows every picture and voice event:
- the cast voice, and the arrival (the shafts light);
- at least two heals, each with its tap (the pitch climbing with the count);
- the threads up the shafts;
- a hit stop while lit.

It also has to be free of anything that takes the screen from those events:
- no cast of the foe's, and no other banner, from 2.4s before the clip to its end;
- not the scrunch card, which opens at the match's first clank;
- **no kill inside the clip.**

The qualifying windows are ranked on the heals, the distinct tap counts, the threads, the lit hit
stops, the foe's blows on the hung ball and how soon the ball lands. Left out of the pool: Twinshade,
whose shades take shaft blows and heal (reading 11), which puts threads on a second body; and every
sanctified foe, which wears the same white and gold as Angelus.

**Two picker fixes, and one clip set aside.** Each fix is now enforced by the picker.
1. **The first table counted no threads,** because `tickAscend` runs about twice a step, so a new
   thread is already a tick old when the step returns. The picker now counts a thread when it first
   sees it (`pick_v1_threadbug.txt`).
2. **The fixed table's top, Angelus v Farwarden 104001** (cast at 81.88), was filmed and set aside.
   The window closed by its clock and the ball landed 0.73s later, but Angelus killed Farwarden 0.14s
   after the landing, at 92.78. The thud sat under the kill's voices, and the clip ran on through the
   kill into the verdict (20.0s). The picker now refuses a kill inside the clip. The clip and its log
   are kept in scratch (`clip_farwarden104001.txt`, `pick_v2_farwarden.txt`).

Of 128 fights (32 foes × 4 seeds), 8 have a window that shows everything (`pick.txt`):

    python _angelus_pick.py --game <scratch>/links/sc-angelus-b9-fx.html --seeds 4

The pick is **Angelus v Slagheart, seed 104112**, the second cast, at 31.18. Slagheart is a dwarven
flail, brown against Angelus's white and gold. The window is 9.85s of match time
(`clip_timeline.txt`, headless on the same link):
- the cast at (273, 357); the arrival at (260, 300) 0.425s later (the cast's 0.08s stop and the
  0.35s rise);
- 8 shaft blows, each with its tap: counts 1, 2, 3, 4, 5, 5, 5, 5;
- 1 blow of Slagheart's landing on the hung ball, and lit hit stops through the window;
- the close by the clock at 41.033 (8.000 of 8 on the window clock), with the chord;
- the landing 0.90s later, at 41.933, with the thud;
- no other banner, no card, no kill.

    python cinema_clip.py --game <scratch>/links/sc-angelus-b9-fx.html --a angelus --b slagheart \
      --seed 104112 --at 29.98 --window 12.85 --end-at-window --fps 60 --w 540 \
      --out ../07-shorts/v104/ascension-window.mp4

The clip runs **14.6s at 60 fps, 540x960** (878 frames): the window, the drop and the landing, and
nothing after (`--end-at-window`; the director's slow motion at 38.6 stretches 12.85s of match into
14.6s). Its match state at the end is the headless fight's to the digit: t 42.8417, hp 286.59 /
276.512 (`clip.txt` against `clip_timeline.txt`). `07-shorts/v104/ascension-window.mp4`,
`db54d28cf46009eb`, 3.3 MB.

**Audio:** AAC 48 kHz stereo, mean -22.9 dB, max -3.4 dB, integrated -20.8 LUFS (`clip_levels.txt`).
The voices are in the mix (`clip_audit.txt`, `clip_audit.py`: narrow-band onsets over each band's
running median and a reference band; the 85 ms analysis window puts every onset about a tenth of a
second early):
- **the cast chord** at 1.08s (the cast frame is at 1.20s). The detector also fires later on the
  score, whose key shares D and A, so only the cast's onset is claimed;
- **the taps:** onsets in the C8-A8 band at each of the 8 shaft blows (2.49 to 12.45s; most of them
  a pair 60 ms apart: the blow's own hit voice, then the tap), and none in the 1.2s lead;
- **the close:** the chord at 12.83s and its step down to A3-E4 at 13.07s;
- **the thud:** a burst in 35-110 Hz at 13.48s, +34 dB against 12 dB in the 150-240 Hz reference
  band. The ball reaches the floor in frames 818-824 (13.63-13.73s).

**Five frames**, checked by eye (`05-reference/v104/ascension-window-5frames.png`, 2700x960,
`5de25ecc944f2505`). The art renders through the pipeline:
- **frame 90 (match 31.5):** the cast. The column of light under the rising ball, the banner.
- **frame 150 (32.5):** the shafts lit (warm edges, to the wall and the floor), the halo's gold flare,
  BLESSING 1, and the gold thread with its bead running up the lower shaft from Slagheart.
- **frame 545 (38.7):** the director's zoom, inside a hit stop: BLESSING 5, the thread's bead at the
  blow, SMITE on the foe.
- **frame 770 (41.1):** the close. The shafts shortening, the ball still at the hang point.
- **frame 822 (41.9):** the landing. The ball on the floor, its blades at rest.

**Not this build's:** in the tail, Slagheart's HUD card counts down to its Ironbloom (4.0, 3.2). That
is the shared HUD's five-second preview; the cast itself falls after the clip.

### 5g. What the brief's stage 6 asked for, and where it went

The brief's stage 6: "picture, voice, carry per design §6; bloom gate ≤ +0.03 measured. Beats: the
rise files `ult`; shaft hits file as blows. Field in both copies. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder angelus_build.py`, one fight watched."
- **The picture, with the bloom gate:** §5a. The picture's share of the arena lift is at most
  +0.0051, against the brief's +0.03 (and the lab's own +0.02).
- **The voice:** §5c.
- **The field in both copies:** none; the motes are drawn down the shafts instead (§5b).
- **The beats:** nothing new in the sim. The rise files `ult` (fireUlt's own beat; the probe's [8]
  holds it to one a cast), and shaft hits file as blows (resolveHit's own). Stage 6 files no beat:
  the builder refuses one.
- **`render_ab` and `chain_audit --builder angelus_build.py`:** §5e.
- **One fight watched:** the clip (§5f), the picture lab's 15 whole fights drawn (§5a), and the drawn
  sim identity (§5e).
- **`shell_identity` and "Move `GAME`":** not this build's. The app's json is shared, and the app
  pointer waits for Rick (§6).
- **The two lines moved here from the brief's stage 2:** "FILM IT" is the clip (§5f). "Run
  `harrow_bloom_probe` on the placeholder shafts": that tool is hard-wired to the Harrowing (Lastlight's
  match and its own scratch arms), so the picture lab measured the bloom itself, against the bare
  hall and against stage 5's ×10 placeholder (§5a).

### 5h. What the sim gave the picture and voice labs (stage 5's link, as written before stage 6)

Line numbers are `sc-angelus-b9`'s. The anchors are the quoted strings.

**The fields:**
- **`f.ultRise`** = `{t, dur, x0, y0, lit, hits}` while the window is open, and null otherwise.
  - `t` runs on the window clock, which stops in every hit stop.
  - `lit` is 0 through the rise and 1 from the arrival.
  - `x0` / `y0` are the cast position.
- **`f.riseTally`** = `{casts, frames, litFrames, arrivals, shaftHits, bless}`. It is cumulative over
  the fight, and the sim never reads it. A picture can key "a shaft hit" off `shaftHits` rising.
- **`f.reachMul`** is 10 while lit.
- **The hold:** from the cast to the close, `pin` and `pinMax` equal dur, `pinFree` is 1 and `pinV` is
  [0, 0].
- **The numbers:** `u = f.w.ult` = `{name "Ascension", charge 14, kind "rise", dur 8, rise 0.35,
  hangY 300, shaft 10, shaftSpin 0.5, winDmg 0.4, healPer 1}`.

**The cast is `fireUlt` (16274).** In order:
1. The banner at the caster, shake 32, `hitStop` 0.08.
2. The `ult` beat (16299-16300).
3. `SFX.play("ult", { w: f.w.id })`, which is `w: "angelus"` (16301). Angelus has no voice arm, so
   this falls through to rune-crack (`} else {  // rune-crack`, 7435). A cast voice goes BEFORE that
   fallback, which is re-emitted unchanged.
4. `m.ultFx = { w: "angelus", kind: "rise" ... }` (16309). There is no `life` entry, so the default
   1.5s applies.
5. The `u.kind === "rise"` branch (16677), which creates `ultRise` and pins the caster.

**`tickRise` (13673)** is called once a step, at 8953 (`this.tickRise(dt);  // ASCENSION (v74)`),
after `tickTendril` and before `tickHits`. On each window frame, in order:
1. **The heal:** `T.shaftHits += n` (13681), then `f.apply("blessing", healPer × n, side)` (13683).
2. `Z.t += dt`.
3. **The close**, when `Z.t >= Z.dur || !f.alive` (13688). reachMul goes back to 1 and the hold is let
   go. A live caster gets v = 0 and then falls. The foe's death does not close it, and neither does
   the match's end (reading 10, below).
4. The hold is re-armed.
5. **The rise:** the smoothstep from (x0, y0) to (260, 300) (13700-13703).
6. **The arrival:** `lit = 1; reachMul = shaft; arrivals++` (13705). This is "the shafts light".
7. **The hang:** `f.x = tx; f.y = ty` (13706).

**A shaft hit is an ordinary blade blow in `resolveHit`.**
- The damage line is 14476 (`× winDmg`, read off `ultRise.lit`), and the ledger `self.hits++` is 14637.
- The blow's own hit stop, flash, beat and hit voice play.
- Its blessing lands on the NEXT live step's `tickRise` (the hits delta), after the blow's hit stop.
- **A blow on one of Twinshade's shades is a shaft hit too** (reading 11; `tickShadeHits`, 8960):
  90 in b9's 456 probe fights. A picture keyed off `riseTally.shaftHits` counts them, and the thread
  up the shaft should start at the shade.

**THE WINDOW IS STILL OPEN WHEN THE MATCH ENDS in 260 of b9's 456 probe fights** (57%; Angelus won
133 and lost 127; lit in 243). This is reading 10, and the sim will not close it:
- A kill sets `over` inside the killing step (`checkEnd`, 17758, called at 8969).
- `step()` then returns at `if (this.over){ this.decay(dt); return; }` (8730), before any ticker.
- So `ultRise` stays set, `reachMul` stays 10, `pin` stays 8 and the caster stays hung at (260, 300)
  through the kill, the shatter and the verdict, whichever ball died. The one exception is Angelus
  killed by Ravelbone's burst or Grudgebearer's forge, whose kill flight lets the tick close the
  window (reading 5).
- The design's close ("the shafts shorten to blades over 0.3s, the halo goes, the ball drops") never
  plays on a kill.

**So stage 6's picture must close the shafts and the halo itself** at `over`, and when the caster is
dead (done: §5a; the probe's [12] counts 260 closes AT THE KILL in b9's 456 fights):
- Canopy's picture does exactly this, reading `(this.over || !f.alive) ? null : f.ultTree` (9117).
- `drawWeapon` reads `f.reachMul` directly (24026), so at `over` the picture must also stop drawing
  reach × 10. It can shorten the shafts on the presentation clock, which keeps running under the
  verdict.
- A ball that "drops" after the kill is presentation only. The sim's ball stays where it hung.
- 47 more ticks in those 456 fights find the foe already dead, killed by Angelus's smite in
  `tickStatus`, before `checkEnd` ends the match. The window stays open through them too.

**The weapon draw is `drawWeapon` (24020):** `reach = f.w.reach * m.actMods.reach * f.reachMul`.
- On stages 2-5 the radiant twinblade art is therefore drawn at reach × 10, about 620-680 units, and
  through the wall. That is the placeholder.
- Stage 6 draws the shafts clipped at the wall and the floor. The design says "drawn to the wall/floor,
  not past".

**The head and the silhouette:** `SHAPES.twinblade` (4344) → `key === "sanctified"` →
`SHAPES._tbRadiant` (4430). That is a halo ring at L × 0.33 plus `_twinDagger`. No relic has drawn it
before; it is the design's "first cut".

**The field hexagon:** `_drawField` draws the stasis hexagon only when `f.pin > 0 && !f.pinFree`
(23180). Angelus has `pinFree` 1 for the whole window, so no hexagon is drawn. What the brief asks for
is already the engine's behaviour.

## 6. What is left, and whose

- **Rick:**
  - the veto (design §7 item 1: the hang height is the lever, and the brief says not to "improve"
    it upward). The standing ruling settles it: no vetoes, so the build went ahead as designed;
  - the blade: 9, with the crossing at ~8.9, just under the brief's 9–9.5 and the design's ~9.3. The
    brief names no knob, so nothing else moved;
  - twinblades at 19% (Starwarden 2.5, Spellbreaker 5) against warhammers at 78%. This is the
    design's inverted counter (item 12/32);
  - fights that run 12s longer than the roster's: 73.7s against 61.5s;
  - the window clock makes each built window 9.92s of match time. The heal comes out at 43.7 hp a
    cast against the design's ~36, and stage 3 reads 69.65 against the brief's ~63. The blade was
    re-priced on top of this;
  - **stage 6's picks, all his to overrule:**
    - the clip (one per ultimate): `07-shorts/v104/ascension-window.mp4`, and the choice of window
      and foe (§5f);
    - the picture (§5a) and the sheet (`05-reference/v104/angelus-picture-sheet.png`);
    - the close at `over` drawn as the clock's close, with the ball left hung (no presentation-only
      drop after the kill);
    - no `fx.js` field: the motes drawn down the shafts instead (§5b);
    - the voices (§5c): the VOWEL cast (PURE the cheaper near-tie, if the app stutters at the cast),
      the SKY tap at 4.2-7 kHz, the STEP close, the NEW landing thud (42-95 Hz: phones will not
      play it), the thud on the first floor contact rather than at a fixed delay, and no close voice
      at the kill.
- **The orchestrator (ALL DONE at the carry, §7):**
  - **the carry,** one relic at a time: `angelus_build.py --stage 1, 2, 3, 5, 6 --src <tip>`, each
    proved by engine_ab. Stages 1-6 apply today to the batch line's newest chain links
    (`sc-ironhail-fxout`, `sc-widowmaker-fxout`, `sc-lodestone-b205-fx`, …) and to every in-flight
    scratch build (§1, `runs/stage6/compose6.txt`);
  - **nothing to take out of `fx.js`:** `fx_spec` is NONE, so `fx_remove.py` does not run for
    Angelus, and neither copy is re-stamped;
  - **two anchors are consumed** (§1). A builder carried after Angelus that anchors on
    `(f.ultVine ? 0 : f.w.spin) * f.spinMul(mods.spin)` (the spin product) or on
    `    const tr = f.trail;` (drawFighter's body trail) will refuse. None does today;
  - **`shell_identity`** on the carried stage-6 link. It was not run here, because the app's json is
    shared;
  - move `app/main.js`'s `GAME` line only after Rick's check, as for the batch's others. The build of
    record is yert's staff row (`sc-nightglass-fx`); a batch GAME move goes through
    `tools/staff_carry.py` first;
  - **a finding from the picture lab, not a picture defect:** `litWeapon` draws every lit weapon
    through ONE module-level scratch canvas, `_litScratch`, which grows to the largest weapon ever
    drawn, never shrinks, and is cleared whole on every call. Stage 5's ×10 placeholder grew it to
    1463-1597 px (815-863 on the stage-6 picture), and from then on every lit weapon in that page
    paid for it: Spellbreaker's `drawWeapon` ran 290-640 ms against 90-147 ms, and the cost carried
    into the NEXT match in the same page. Stage 6 removes it for Angelus, but any future relic that
    draws a very long lit weapon will hit the same scratch. Worth an item;
  - **carry stage 6 with stage 5.** A stage-5 carry alone draws the ×10 placeholder art through the
    walls, leaves the stale body trail's ghost at the cast point, plays rune-crack at the cast, and
    grows that shared scratch. Cut no clip from a carried tip until stage 6 is on it.
- **Watch in the app:** the cast chord's cost (§5c, flag 1). The shorts render their audio offline;
  only live play pays it, and the cast sits inside its own 0.08s hit stop.
- **Standing, not this build's:**
  - verify's two clock bands, red on every link since the minute pace. Angelus's long fights push
    them further;
  - the base's own tip_audit MISSING entry (burn `feed`);
  - reading 4's Ravelbone path (a caster caught before its cast, then released mid-window). It is
    real in the engine and was never reached on this roster. If a future relic can clear a hold
    mid-window, the forced-clear check in [2] is what covers it.

## 7. The carry onto the chain

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Oracle with the
same builder, one stage at a time (`--src` the previous link):

```
sc-oracle-fx.html                  the batch line's tip (Oracle)   15cf62f96f72653a
  -> sc-angelus.html                 stage 1                                  9aac8243eecc2d71
  -> sc-angelus-rise.html            stage 2                                  42d3e551913d55bb
  -> sc-angelus-heal.html            stage 3                                  97ebdb9d239c651f
  -> sc-angelus-b9.html              stage 5                                  ea75be11ae23ba09
  -> sc-angelus-b9-fx.html           stage 6                                  85b8af63055d1108
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail and Widowmaker (both redesigned on the chain since), n=6: **3996/3996 identical**
  (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-oracle-fx` against the carried stage-6 link, every relic on the tip
  (41), n=6: **4920/4920 identical** (`runs/carry_engine_ab_tip.txt`): Angelus moves no other relic's
  fight on the batch line, the redesigns and the relics carried since included.

**Gates on the carried stage-6 link** (`runs/carry/`):
- engine_ab stage 5 -> stage 6 over all 42 relics on this tip, Angelus included, n=6: **5166/5166
  identical** (`engine_ab_s6.txt`);
- `angelus_probe.py` **12/12** on the carried link, [the stage-6 checks] on (`probe_fx.txt`) -- the
  probe met every relic carried since its scratch base (Coldiron's Temper, Ironhail's hail, Lodestone's
  walls, Widowmaker's drain, Oracle's sight) and needed no change;
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold (`staff_carry_dry.txt`);
- **shell_identity 200/200** (app Chromium 152 vs headless 151; the pointer not moved, the json
  restored).

The clip stays the scratch one (`07-shorts/v104/ascension-window.mp4`): Angelus v Slagheart 104112 is inside the scratch A/B (neither relic moved),
so the carried fight is the filmed one.

**The roster is 42 on the batch line.**

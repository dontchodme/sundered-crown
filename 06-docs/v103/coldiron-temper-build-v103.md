# v103 — COLDIRON / TEMPER, BUILD. STAGES 1-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-tendril-fx`, §9): stage 1 is arm A fight for fight (660 of 660, both blocks); the mechanism is the lab's (the probe reads every sentence on the window tickers' clock, every control failing its own check only); the brief names no knob to move, and the blade sits at 9.3 (48.4% both sides); verify 11/13 (the clock bands), Coldiron 50.5%. STAGE 6, the picture and the voice, is built from the two labs' rows byte for byte and gated: engine_ab 4446/4446 with all 39, probe 9/9 (two new checks: the voice and the picture), render_ab 24/24 (control 0/5), chain_audit 29/29. No fx.js field (the forge sparks are drawn). The clip is `07-shorts/v103/temper-window.mp4`, for Rick. Carried: engine_ab 4446/4446 against the scratch build, shell_identity 185/185. The app pointer waits for Rick.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`, the BUILD row under the
dwarven twinblade's). Input: `06-docs/v73/COLDIRON-BUILD-BRIEF.md` + `dwarven-twinblade-design-v73.md`,
and nothing else (rule 0). Builder `tools/coldiron_build.py`, probe `tools/coldiron_probe.py`, runs in
`runs/`. **A NEW relic, the dwarven twinblade** (the brief's "40th" is the cell number; on this base it
is the 39th relic in the roster, and its place on the chain is the carry order's).

**Built in scratch, in parallel with the batch's other builds** (the orchestrator carries each onto the
real chain one relic at a time, rebuilding with `coldiron_build.py --src <tip>` and proving the carry
with engine_ab). Nothing here is in `02-chain/` yet; the links below are the scratch builds. The
chain tip has moved on since the base was taken: it is now `sc-tendril-fx` (Bindweed's picture,
which moves no fight), and stages 1-6 re-apply on it cleanly (§4, §7d).

```
sc-tendril-t3.html                the base: the tip when the batch began (Bindweed stage 5)     5a6216e3b629fad4
  -> sc-coldiron.html              stage 1  the relic, ult stubbed (charge 1e9)                 d4e88ca41e384ab8
  -> sc-coldiron-mass.html         stage 2  the mass, charge 14 (arm B)                         5c0b491fa04e3040
  -> sc-coldiron-bind.html         stage 3  sunder on a won bind, bind 0 -> 2 (arm C)           5da2971c7018c7bc
  -> sc-coldiron-temper.html       stage 4  the cap, 6 -> 9 (arm D at cap 9)                    231801282154c302
  -> sc-coldiron-temper-b93.html   stage 5  the blade, 11.95 -> 9.3                             324b42d5b36fac98
  -> sc-coldiron-temper-fx.html    stage 6  the picture and the voice (moves no fight)          3693eda608b26fa8
```

Every link is rebuilt byte-identical by the builder from the base (re-checked on resume, and again
after each of the fix's builder changes: `coldiron_build.py` c5b8ecf7016fc829, then 155eec593ce9e6c2 (a
docstring sentence, §9's past-6 item), rebuilds all five to the hashes above), and the builder
refuses to overwrite a link. The stage-6 builder (1def68ac25637c8a, then f194fa06f46454c9 with the
widened weapon guard, §6) rebuilds all six to the hashes above (`runs/builder_checks_s6.txt`,
`runs/rebuild7.txt`).

**Reviewed adversarially (2026-09-27), verdict "fix"; fixed here.** One should-fix: the probe could
not tell whether the window runs on the window tickers' clock. The review's mutant r1 ticks the
window through the hit stop too, so it runs on match time as the lab's did. It still makes 960 ticks
a window, and the first probe (7ba5df7e85cf82af, kept as `runs/coldiron_probe_v1_7ba5df7e.py`) passed
it 7/7 although it changes fights. **Probe v2
(`coldiron_probe.py` bc34ecee5ad1ab30) reads the clock inside `step`.** A frozen step (a hit stop, the
latch, the split) must leave the window and its clock exactly as they were. A live step must move the
clock by exactly dt. r1 now fails [1] and only [1], 226571 times. Every stage still reads 7/7 and
every earlier control still fails its own check only (§3). The review also made five notes:
- The window is still set at `over` on an ordinary kill: reading 4, [1] and §5 are reworded, and the
  probe now counts these windows.
- The composition paragraph named stale links: §4 now cites a re-run on today's links.
- The builder's check on `apply`'s ceiling line was brittle: it now tests the sunder clause, not the
  whole line.
- The brief's `{t0, end}` sketch was not declared: now declared under "The clock".
- Stacks past the cap outlive the window on screen: now an open item for Rick (§9).
The review also remarked that the stage-1 comparison read the overlay's json, which keeps each
foe's rate and not each fight. Stage 1 is now read fight by fight: 0 of 660 fights differ on
either block (§3). This doc now closes, like v100 and v101, on what is left and whose (§9).
No link changed: the fixes are to the probe, the builder's docstring and assertions, and this doc.
The builder is now 155eec593ce9e6c2 and the probe bc34ecee5ad1ab30 (stage 6 and the second review's
notes moved them to f194fa06f46454c9 and db6a380e135e49d5: §6, §7).

## 0. What this build stands on

- **The relic** is Widowmaker's twinblade profile, the lab's donor (blades `[0, 0.5]`, reach 62, width
  8, artW 30, spin 5.7, mode spin, mass 1.1), at the lab's blade 11.95 until stage 5; aff dwarven,
  `onHit {sunder:1}`, and the brief's 69-character card. The builder asserts the donor's physical
  profile (not its blade: §4), `STATUS.sunder` {6 stacks, 5s, +11% taken}, the clank's `mass^1.7`
  shares and its 0.16 decisive line, the per-fighter bleed ceiling beside which the sunder ceiling
  goes, `apply`'s never-trim rule, the charge as pure normal-path time, and the dwarven twinblade's
  art route (`SHAPES.twinblade` → `_tbBuilt`, never drawn by a shipped relic). It asserts the base by
  these contents, never by which relic is last, and appends the row at the end of the WEAPONS array
  (the `];` that closes it and the comment after it, which names no relic), so a build carried
  before or after this one composes.
- **The charge is 14:** the brief's 16 on the lab's clock, converted (Rick's batch ruling). Measured
  for this fighter on arm D at cap 9 (`runs/anvil_census.py`, a scratch copy of `ult_overlay.py` that
  counts, before each lab step, whether it is frozen — `m.hitStop > 0 || m.latch || m.splitHold` — in
  total and inside windows; its fights equal the unmodified lab's foe for foe; `runs/s0_census_2207`):
  **12.83% of the lab's steps are frozen (15.03% inside windows, 11.34% outside), so the lab's 16 is the
  engine's 13.95, and 14.** Arms B and C read 13.91; D at blade 9 reads 13.92.
- **The lab is `tools/ult_overlay.py` + `overlays/anvil.js`** (the brief's stage-0 command). It plays
  the relic as side A against the design's 33 foes (the 34-relic roster less the donor, Widowmaker).
  **A lab default that differs from the settled numbers: `winCap` defaults to 12**, the design's first
  price (§3 arm D), rejected in §3 for 9 ("Cap 9 instead of 12"). Every arm below passes `winCap=9`
  except the one run that reproduces the published cap-12 number. `winMass` 5.0 and `bindSunder` 2
  default to the settled numbers; charge 16 and dur 8 are the harness's. The lab WRITES the donor's
  weapon (`w.mass = 5` at the cast) and the GLOBAL `STATUS.sunder.maxStacks` for the window; the build
  writes neither (the builder refuses an insert that writes `w.*` or any `maxStacks`).
- **The mass reaches every read of it** (design §5, brief §1, open item 3 — "the build lists them").
  `f.massMul` (1 on every fighter, always, but Coldiron inside its window, where it is `5.0 / 1.1` and
  `1.1 x 5.0/1.1` is 5 exactly in doubles) multiplies `w.mass` at **all five reads, at four sites**:
  `resolveClank`'s two shares; `move`'s gravity; the hit stop's gravity (the frozen path of `step`: the
  brief's "decayImpactOnly's gravity"); and the liquid's gravity (`SLOSH`: picture only, but it must
  feel the gravity the ball feels). The only other `.mass` read is the clank voice's `p.mass`, which
  receives `max(mA, mB)` and so already hears the iron. `ballCollision` reads no mass; `massRef` is a
  constant (2.68), so no derivation of it exists to carry; the burden term is untouched (the
  multiplier is on `w.mass`, which is what the lab moved). The builder refuses any `.mass` read that
  is not on this list, on the base and on the output, and any `w.mass` read without `massMul` (the
  cast's own `u.mass / f.w.mass` aside).
- **Readings** (in the builder's docstring):
  1. **The cap is the foe's own** (brief §0, design §5: "per-fighter ... on the foe BEING sundered").
     The lab lifted the status's global ceiling, which also let a dwarven foe sunder Coldiron past 6
     while Coldiron's own window was open; the build does not. Twinshade's shades keep the status's 6.
  2. **A won bind sunders the loser of that bind** (the brief's `loser.apply`). The lab sundered the
     opponent even when the bind was against one of Twinshade's shades; the two differ only while
     shades stand.
  3. **`apply`'s source is a side letter** (the engine's contract, Rick's standing ruling); the brief
     wrote the Fighter. Sunder has no reader of its source.
  4. **The window closes on either death while the match still runs** (the lab's; the docs are
     silent), and the close puts the mass back. A death with the match still running is a death in
     a kill flight (Ravelbone's wire, the Crucible's forge). Those are the only live frames after a
     death. **On an ordinary kill the window is still set at `over`**: `checkEnd` comes after
     `tickTemper` in the killing step, and nothing ticks once `over` is set. On the final link's
     probe, 245 of 1613 windows end this way; 1342 close on the clock and 26 on a death in a kill
     flight. No fight can change. A picture drawn off `f.ultTemper` has to read
     `f.ultTemper && !m.over` (§5).
  5. **The mass is set at the cast**, so a bind on the cast's own frame is already iron (the lab's
     cast came between two steps, before the whole step it opened). The cap is the brief's per-frame
     recomputation in `tickTemper`.
  6. **The mass reaches gravity too** (design §5: "the lab priced it in"): a mass-5 ball falls with
     gravity x (5 / 2.68)^0.5 = 1.366 of the config's, where the twinblade's own 1.1 gives 0.641.
  7. **The bind is the engine's own**: `aWins` and `decisive` read inside `resolveClank`. The lab
     re-derived the outcome after the step from the same rule, and counted at most one bind a frame.
- **Names:** the window is `ultTemper`, the ticker `tickTemper`, the tally `temperTally`, the kind
  `"temper"`. The brief's `ultIron` / `tickIron` are prefixes of the staff row's `ultIronfall` /
  `tickIronfall` (yert's branch), and `ironTally` is Ironfall's (the tickVine / tickVines trap). The
  brief's `massMul` and `sunderCap` are free and kept. The builder refuses if any name is already in
  the base.
- **The clock:** the window runs on the window tickers' clock, which stops in a hit stop (every window
  of the batch). The lab's 8s were 8 step-seconds, frozen ones included (§2). **The brief sketches
  the window as `f.ultIron = { t0, end }`** (brief §1), a match-time shape. The build keeps
  `{t, dur}`, where `t` advances only in `tickTemper`, on the window tickers' clock. Rick's standing
  ruling for every window cadence ("they stop in a hit stop") replaces the sketch's shape. It does not
  change its 8 seconds. Probe [1] asserts the clock: it holds on every frozen step and moves by dt on
  every live one.
- **Rick's veto:** waived for the batch (no vetoes). The cap is 9 (the brief's settled number; the
  design's §7.1 fallback, cap 6, is arm C).
- **A deliberate change to the brief's process** (v98's precedent): stage 2's "FILM a bind won" is
  folded into stage 6. The picture is presentation, it cannot move a fight or the blade, and the
  window to film is picked here (§5).

## 1. Stages 1-4

Stage 1 appends the row with the ultimate stubbed at charge 1e9 (bind 0, cap 6 written, inert).
Stage 2 adds the four fields after `this.bleedCap = ...` (`sunderCap`, `massMul`, `ultTemper`,
`temperTally`), sunder's per-fighter ceiling in `apply` (`key === "sunder" ? this.sunderCap`), `massMul`
at the five mass reads, the won-bind clause after `aWins` in `resolveClank` (at bind 0 it only
counts), the `kind === "temper"` cast branch before Tendril's, `tickTemper` after `tickTendril` (the
method before `tickWinnow`), and charge 14. Stage 3 flips bind 0 → 2; stage 4 flips cap 6 → 9. Nothing
waits (design §5); the cast gate is untouched, and a charge of 14 on the normal path cannot come round
inside an 8s window on the same clock (the probe asserts no cast under an open window).

- **The cast** (`fireUlt`, after the engine's generic head: its 0.08 stop, its `ult` beat, its voice
  and its `ultFx` record): `ultTemper = {t: 0, dur}`, `massMul = mass / w.mass`, and returns.
  Nothing resolves.
- **A won bind** (`resolveClank`, after `aWins`): when the bind is decisive and its winner's window
  is open, the loser takes `apply("sunder", bind, <the winner's side letter>)` through its own
  ceiling. Nothing else in the clank changes; the clank files its own beat and its own stop.
- **`tickTemper`**, every normal-path frame: each open window's clock advances by dt. At `dur`, or
  on a death while the match still runs (a kill flight), the window closes and `massMul` returns to 1.
  On an ordinary kill it is still set at `over` (reading 4). Then, for BOTH fighters, whether or
  not anybody has cast, `sunderCap` is the other fighter's `ult.cap` while its window is open and
  the status's 6 otherwise (Bloodletting's rule: no paired write to forget). Stacks above 6 when a
  window drops are not trimmed; `apply` adds nothing over the ceiling. They run out on sunder's own
  5s clock, as the brief says, but every sunder that lands refreshes that clock even when it adds
  nothing (the engine's whole-status expiry), so while Coldiron's blade keeps landing they mostly do
  not run out before the next window (§3, "Past the cap"; an item for Rick, §9). It moves nobody,
  draws nothing, stops nothing, files nothing.

## 2. Stage 0 and the stages against it — the window clock, measured

`ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic widowmaker --cell dwarven:twinblade
--mech overlays/anvil.js --arms A,S,B,C,D --P winCap=9 --seeds 20 --foes <33>`, seed0 2207 and 2317,
660 fights an arm a block, Chromium 151.0.7922.34 (`runs/s0_ASBCD9_*`); the brief's own command at
blade 9 (`runs/s0_AD9_b9_*`); arm D at the lab's default cap 12 (`runs/s0_D12_*`). The built links run
`ult_overlay.py --relic coldiron --arms SHIP --mech overlays/anvil.js` on the same foes and seeds (the
same seed formula and side). Arm B, the noisiest, was read on two more blocks (2427, 2537).

```
                                lab on 151            published 141     lab at dur 9.4         BUILT                        built, window clock
                                (block 1 / 2 [/3/4])                    (1 / 2 [/3/4])         (1 / 2 [/3/4])               through freezes
A   no ultimate                 35.2 / 38.9           35.2 (33.6)                              stage 1: 35.2 / 38.9         identical, fight for fight
S   sunder on a bind, no mass   35.2 / 38.9           33.6
B   the mass                    57.9/55.3/54.1/53.6   56.4 / 57.9       53.9/55.9/61.5/58.8    stage 2: 60.2/60.6/58.8/57.9  49.1/54.8/59.4/55.9
C   + sunder 2 on a won bind    60.9 / 63.5           61.7 / 60.0       62.9 / 65.3            stage 3: 63.6 / 65.0         60.6 / 61.5
D   + the cap, 9                70.9 / 70.8           —                 72.6 / 73.3            stage 4: 70.6 / 71.7         71.1 / 71.7
D   at the lab's default cap 12 75.3 / 75.6           73.9 / 73.0
D   cap 9, blade 9              51.4 / 51.5           50.2 / 48.8
A   blade 9                     14.4 / 16.8           17.1

pooled                          lab     lab at 9.4    BUILT    built on the lab's clock    BUILT - lab
B   (4 blocks, 2640 an arm)     55.2    57.5          59.4     54.8                        +4.1
C   (2 blocks, 1320)            62.2    64.1          64.3     61.1                        +2.1
D   (2 blocks, 1320)            70.8    73.0          71.1     71.4                        +0.3
```

**Stage 0 reproduces the published arms on 151** (the published runs are other seeds on `sc-trunk`
at 141; every arm lands within the noise of a 660-fight block of them, the largest gap 3.5 points,
arms A and S against the base run's 33.6; and the brief's stage-0 targets hold: A ~17% at blade 9
reads 15.6, D ~50% at blade 9 / cap 9 reads 51.4). The lab at "dur 9.4" is the lab at the engine's
window in match time: 8 / (1 - 0.150) = 9.41. **Stage 1 is arm A fight for
fight** on both blocks: every one of the 660 fights a block has the same winner, the same length
in steps and the same blows in and out (`runs/f4f.py`, below).

Lab mechanism on 151, arm D at cap 9 (block 1 / 2): 3.35 / 3.33 casts; 3.07 / 3.10 binds, 2.61 / 2.63
won and 5.22 / 5.26 sunder from binds a cast; the foe's stack peak 7.85 / 7.87; 5.94 / 5.91 stacks on
a window frame; 9.26 / 9.22 blows in windows and 9.60 outside. Arm S, the control that can fail:
2.92 binds a window and **0.00 won**; arm B: 3.20 binds, **2.73 won**.

**The built relic reads over the lab at B and C, and the whole gap is the window clock:**
1. **The engine's window is longer in match time.** The engine's 8s are 8 seconds of the window
   tickers' clock, which stops in a hit stop; 15.0% of window steps are frozen here (the census; the
   probe reads 15.5-15.9% on the built links), so a built window is ~9.4s of match time (the probe:
   9.3-9.4s a window, death closes included). A longer window holds more binds: the built stage 4
   takes 3.60 binds, wins 2.97 and sunders 5.93 a cast, where the lab's D took 3.07 / 2.61 / 5.22.
2. **The lab at the engine's window reproduces the built mechanism** (arm D at dur 9.4: 3.52 / 3.57
   binds, 2.98 / 3.03 won, 5.96 / 6.06 sunder a cast, peak 8.07) and reads over the lab by +2.3 / +1.9
   / +2.1 at B / C / D.
3. **The built relic with its window clock running through freezes, as the lab's did**
   (`runs/labclock.py`: a scratch copy of each built link where `ultTemper.t` also advances on the
   three frozen paths of `step`; nothing else changes) **reads the lab's arms**: 54.8 / 61.1 / 71.4
   against 55.2 / 62.2 / 70.8. B needed four blocks to say so (its blocks spread 49.1-59.4).

At D the four readings sit within 2.1 points of each other, inside two blocks' noise. **The
mechanism is the lab's; nothing is mis-built.** The build keeps the engine's convention (every window
cadence of the batch runs on the window tickers' clock, and a freeze freezes the world) and every
designed number; stage 5 settles the blade on the built relic.

## 3. The probe (`coldiron_probe.py`, one check per sentence, read inside the hooks)

The probe wraps `step`, `move`, `resolveClank`, `resolveHit`, `fireUlt`, `tickTemper` and the liquid's
`SLOSH.step`, plays Coldiron from both sides against every other relic (38 foes x 6 seeds x 2 sides =
456 fights), rebuilds the engine's arithmetic exactly where it can, and prints N/N; a check that
never ran fails. The checks:

- **[1] "For a duration"**: every clock-closed window is exactly `dur` on the window clock (960 ticks
  at dt 1/120). **The clock is the window tickers' (probe v2, read in the `step` hook).** Every frozen
  step (a hit stop, the latch, the split) leaves the window and its clock exactly as they were, and
  opens and closes nothing. Every live step with the window open moves the clock by exactly dt. A
  window closes on a death while the match still runs (a kill flight); a window still set at `over`
  (an ordinary kill) is counted, not failed. Only Coldiron ever carries `ultTemper`, and no cast
  comes under an open window.
- **[2] "as heavy as a warhammer, so every bind the twinblade takes, it wins"**: `massMul` is exactly
  `mass / w.mass` on the window (`w.mass x massMul` exactly 5 at the cast) and 1 on every fighter
  (shades included) outside it; every clank's four knocks and two stuns are the engine's rule rebuilt
  from `w.mass x massMul` (the `mass^1.7` shares, the streak's growth and falloff).
- **[3] "each bind it wins sunders the enemy"**: a bind won decisively by an open window (the outcome
  read off the knock the engine actually gave) carries exactly one `apply("sunder", bind, <the
  winner's side letter>)`, on the loser, landing the stacks the ceiling's rule gives; no apply on any
  other bind.
- **[4] "While the iron holds, sunder stacks past its limit"**: each fighter's `sunderCap` is `cap`
  while the other's window is open and 6 otherwise, after every step and every tick; no stack above
  `max(6, cap)` ever; no fighter rises above 6 outside a window; stacks above 6 are never trimmed
  (they only run out, on sunder's own clock).
- **[5] the blades are still the blades**: every blow of Coldiron's is its blade x `dmgMul` x the
  jitter x the foe's damage taken (sunder included), rounded, crit included — rebuilt from the
  captured draws, in the window and out (blows on an Aegis or a cursed foe are counted, not rebuilt:
  the bindweed / ironwood probes' convention).
- **[6] the declared gravity consequence**: `move`'s gravity, the hit stop's and the liquid's are
  `(w.mass x massMul + burden) / massRef` to the `massWeight`, exactly, on every fighter.
- **[7] nothing else**: the cast moves, hurts and applies nothing and stops the world only by the
  engine's generic 0.08; a `tickTemper` frame moves nobody, draws no RNG, hurts, applies, stops and
  files nothing; a clank files its own one beat and its own stop.
- **[8] the voice and [9] the picture** are stage 6's (§7d); each runs only on a link that carries its
  half, read off the page itself.

**7/7 on every stage from 2 on** with probe v2 (bc34ecee5ad1ab30; `runs/probe_{mass,bind,temper,b93}.txt`
and `.json`, one probe, the same seeds; every number but the clock's equals the first probe's):

```
link (stage)                   casts   binds / won / deadlocked   sunder from   foe stack   foe stacks on    blows a fight   Coldiron   a window,     window steps
                               a fight a cast (lost: 0)           binds a cast  peak        a window frame   in / out        win        match time    frozen
sc-coldiron-mass (2)           3.53    3.70 / 3.09 / 0.61         0             4.24        3.20             11.41 / 9.42    56.4%      9.32s         15.5%
sc-coldiron-bind (3)           3.44    3.71 / 3.08 / 0.63         6.15          5.53        4.66             10.97 / 9.12    62.9%      9.37s         15.7%
sc-coldiron-temper (4)         3.30    3.60 / 2.97 / 0.63         5.93          7.69        6.09             10.25 / 8.73    73.2%      9.34s         15.5%
sc-coldiron-temper-b93 (5)     3.54    3.76 / 3.11 / 0.65         6.22          7.99        6.44             12.15 / 9.42    52.2%      9.35s         15.9%

the window clock ([1], probe v2)   frozen steps, window held   live steps, clock +dt   casts   closed on the clock   on a death (kill flight)   still set at `over`
sc-coldiron-mass (2)               257338                      1400756                 1609    1332                  25                         252
sc-coldiron-bind (3)               254770                      1370279                 1567    1307                  13                         247
sc-coldiron-temper (4)             237807                      1301041                 1507    1218                  16                         273
sc-coldiron-temper-b93 (5)         266752                      1411474                 1613    1342                  26                         245
```

No window ever reached the 160s limit open, and no frozen step on any stage moved a window's clock,
opened a window or closed one.

- **The brief's stage-2 gate, the control that can fail:** in the window the iron wins 3.1 of 3.7
  binds a cast and **loses none** (the rest are deadlocks, and every deadlock is against a
  warhammer: "deadlocks against a non-hammer 0" on every stage); outside the window the same relic
  takes 11.5-12.3 binds a fight and **wins 0**. The lab: 2.7 of 3.2 (B), and 0 of 2.9 (S).
- **The gravity consequence, measured** (brief stage 2): the ball falls with x1.366 of the config's
  gravity in the window and x0.641 outside (x2.13 its own weight's fall); design: (5 / 2.68)^0.5 =
  1.366. `move`, the hit stop and the liquid all read it (probe [6], every frame, every fighter).
- **Stage 4's gate:** the foe's stack peak 7.69 a window at 11.95 (the lab at cap 9: 7.85 / 7.87)
  and 7.99 at 9.3 (the lab at blade 9: 7.97 / 7.99); **no stack above 9, ever** (asserted, [4]); no
  fighter rises above 6 outside a window ([4]); a stack above 6 is never trimmed ([4]).
- **Past the cap, after the window** (declared, not new): the engine expires a status whole, and
  every sunder application refreshes its 5s clock even when it adds nothing (`apply`'s never-trim
  rule; Bloodletting's cost, written on `tickSpectre`). So a foe left above 6 at the close stays
  there while Coldiron's blade keeps landing. On the final link 1103 closes left the foe above 6:
  301 ran out, 4.35s after the close on average, and 802 were still above 6 at the next cast or the
  fight's end (6.1s later on average); 5590 blows (12.3 a fight) landed on a foe above 6. The lab
  restored the global ceiling at its close and the same `apply` held its stacks the same way, so
  the lab priced this too.
- **Controls** (`runs/mutants.py`, scratch mutants of the final link, each breaking one sentence in a
  way that changes fights; re-run with probe v2, `runs/probe_mut_<name>.txt`; the first probe's runs
  are `runs/probe_mutants.txt` and `runs/probe_mutants2.txt`, with the same fail counts):

```
mutant                                              breaks                                  the probe v2                      Coldiron win (final 52.2%)
m1   the window 1% long on its clock                [1] "for a duration"                    fails [1] only (13278)            53.3
r1   the window also ticks in a hit stop (review)   [1] the window tickers' clock           fails [1] only (226571)           51.5 (a window 7.95s of match time)
m2b  the clank weighs the iron only on side A       [2] "every bind ... it wins"            fails [2] only (3055)             38.2
m3   one stack a won bind, not `bind`               [3] "each bind it wins sunders"         fails [3] only (5057)             53.5
r2   a won bind sunders the opponent (review)       [3] "... sunders" the LOSER             fails [3] only (34)               52.2 (blows differ: 12.14 / 9.39)
m4   the ceiling stays up after the first cast      [4] "while the iron holds"              fails [4] only (1943335)          52.2 (blows differ: 12.10 / 9.46)
m6   move falls at the twinblade's own weight       [6] the declared gravity                fails [6] only (1460436)          54.6
m7b  the window's close stops the world 0.1s        [7] nothing else                        fails [7] only (1361)             53.7
```

  **r1 and r2 are the review's mutants, verbatim** (`scratchpad/review_coldiron/my_mutants.py`, now in
  `runs/mutants.py`; r1 f3d3837b11c72ceb, r2 3c8fc8098e166f64). r1 makes the window run on match time
  the way the lab's did: still 960 ticks a window, so the first probe passed it 7/7. Probe v2 fails it
  on every hit-stop step inside a window (the latch and the split, which r1 leaves alone, still
  hold: 2294 steps). r2 is the lab's own reading (reading 2); it differs only while one of
  Twinshade's shades takes the bind, hence 34 fails. Two first attempts are recorded and are NOT
  controls: **m2** (the clank light on both sides) fails [2] but also leaves [3] unexercised,
  because no bind is ever won — two sentences, not one; **m7** (a 0.05 stop on the window's first
  tick) lands under the cast's own 0.08 stop and changes no fight (every number equal to the final's; probe v2 reads it 7/7 again). [5] had no mutant here (the
  blade is the donor's arithmetic, untouched); the second review's q3 is one, and its q1 exercises [1]'s death close (§6). Every mutant's hash was regenerated from the final link
  and matches (`runs/mutants.py`, session of the fix).
- **Stage 1 is arm A fight for fight** on both blocks. First read foe by foe (`runs/built_sc-coldiron_*`,
  `runs/cmp.py`): 35.15% / 38.94%, 0 of 33 foes differ, 18.684848 / 19.025758 blows a fight in both.
  The review noted that the overlay's json keeps each foe's rate, not each fight, so this is now
  read FIGHT BY FIGHT (`runs/f4f.py`: `ult_overlay.py`'s own JS, read from the file unmodified, with
  its per-fight rows kept; the lab's arm A on the base against the built stage 1's SHIP):
  **0 of 660 fights differ on either block** in winner, length in steps, blows in and blows out
  (mean 7853.87 / 7932.81 steps a fight in both). The control that can fail: the same comparison
  with the built fights paired one seed off differs on 627 of 627 (`runs/f4f_{2207,2317}.txt`).

## 4. Stage 5: the blade — 9.3

Both sides (`relic_rate.py`: each seed played from both sides; every other relic a foe, 10 seeds a foe
a side, 760 fights a block; seed0 2207 and 2317; `runs/stage5_rr_*`), `--set dmg=X` on stage 4:

```
blade   block 1   block 2   pooled (1520)   side A   side B   mean duration
8.8     49.1      48.3      48.7            50.9     46.5     65.5s
9.3     46.8      49.9      48.4            50.4     46.3     64.8s
9.8     53.8      55.9      54.9            58.7     51.1     64.2s
```

- **The crossing is inside the brief's band** ("Wide on 151 at 8.8 / 9.3 / 9.8. Expect 9-9.5"): a
  straight line through the six block readings crosses 50% at ~9.2, and between the two nearest
  points at ~9.4. **The brief names no knob for this stage, and none moves:** the charge, the window,
  the mass, the bind and the cap are all the designed numbers. **Blade 9.3 is the measured point
  inside the band** (and the design's own "crossing near 9.3"): 48.4%, about 1.3 standard errors under
  50. 8.8 reads the same within noise but lies outside the band.
- **The built link is the measured relic:** `relic_rate` on `sc-coldiron-temper-b93` with no knob set
  gives block 2207 exactly (46.8%; side A 48.7, side B 45.0; every foe's rate, every type's and the
  mean duration 64.84s the same; `runs/stage5_reproduce.txt`).
- **The ladder at 9.3** (40 fights a foe, `runs/ladder_b93.txt`), which the brief asks to print:
  greatsword 65%, bow 56, twinblade 48, scythe 45, flail 45, **warhammer 30**. Worst Ironwood 17.5%,
  Shroudmaul 20, Bloodmirror 25, Ravelbone 27.5; best Oathwound 75, Heartwood 72.5, Lightkeeper 72.5.
  The design's shape (D, blade 9: greatsword 66, bow 54, flail 48, twinblade 48, scythe 43, warhammer
  37; worst Ravelbone 15, Bloodmirror 25) holds, a little wider: the hammers are the row the iron does
  not beat (mass 5 against mass 5 is a deadlock: 0.65 of 3.76 binds a cast deadlock, every one of
  them against a hammer), and Ironwood, not in the design's roster, is a hammer. **The hammers at 30%
  are Rick's** (brief §4.4, design §7.4).

- **engine_ab sc-tendril-t3 → sc-coldiron-temper-b93, the 38 others, n=6: 4218/4218 identical**
  (`runs/engine_ab38.txt`; 38/38 distinct winners). Adding Coldiron moves no other fight.
- **engine_ab sc-tendril-t3 → sc-coldiron (stage 1; the brief's stage-1 gate "engine_ab"), the 38
  others, n=6: 4218/4218 identical** (`runs/engine_ab38_s1.txt`, run in the fix session).
- **verify --n 40 on sc-coldiron-temper-b93 (39 relics, 29640 fights): 11/13**
  (`runs/verify_b93.txt`). **Coldiron 50.5%** (side B, as verify plays an appended relic); every
  relic in 30-70% (Heartwood 31.6 .. Gloamwire 66.1, spread 34.5pp); "both sides can win every
  matchup" passes. Both reds are the two clock bands (pairing means 38.3-98.4s, overall 61.1s), red
  on every link since the minute pace and not Coldiron's.
- **verify --n 40 on sc-coldiron (stage 1; the brief's stage-1 gate "verify 30-40%"): 11/13**
  (`runs/verify_s1.txt`). **Coldiron 35.2%**, inside the gate; every relic in 30-70% (Heartwood 32.7
  .. Gloamwire 66.4); the reds are the same two clock bands.
- **tip_audit:** sc-coldiron-temper-b93 reads exactly as sc-tendril-t3 (`runs/tip_audit_{base,b93}.txt`;
  the one MISSING line, Burn's `feed`, is the base's). Coldiron teaches no new status.
- **chain_audit --builder coldiron_build.py:** 15/15 inserts survive to sc-coldiron-temper-b93
  (`runs/chain_audit_b93.txt`); its control, the same audit against the base, finds 15 of 15 missing.
  Re-run with the fix's builders (c5b8ecf7016fc829, 155eec593ce9e6c2): identical, 15/15
  (`runs/chain_audit_b93_v2.txt`, `runs/chain_audit_b93_v3.txt`).
- **The review's fixes move no gate.** Every link is byte-identical to the one gated: each was
  deleted by hand and rebuilt with the final builder (`runs/rebuild_of_record.txt`), to the same hash. So engine_ab,
  verify, tip_audit, relic_rate and the built-vs-lab runs above stand as run. The fixes are to the
  probe, the builder's docstring and assertions, and this doc.
- **The builder composes with the batch's other scratch builds** (the carry this doc is built for).
  Re-run 2026-09-27 08:28 PDT on each build's newest scratch link with `coldiron_build.py`
  c5b8ecf7016fc829 (`runs/compose.sh`, `runs/compose.txt`, no browser):
  - **The real chain tip, `02-chain/sc-tendril-fx.html`** (eea0cde5536955b3; the scratch
    `sc-tendril-fx` below is an earlier cut of it), with the final builder 155eec593ce9e6c2: stages
    1-5 re-apply cleanly, 39 relics, and the stage-5 inserts are line for line the ones
    `sc-coldiron-temper-b93` makes on `sc-tendril-t3` (`runs/carry_dry_tipfx.txt`, 2026-09-27 12:04). The carry's engine_ab is the orchestrator's.
  - **Forward:** stages 1-5 re-apply cleanly on `sc-angelus-b9` (db58100b3aa0092a),
    `sc-tendril-fx` (5e2cc29a1178bef4), `sc-ironhail-b14` (dadb773b6f8d4555),
    `sc-lightkeeper-bulwark-b9.5` (d60a5c63b785ad04), `sc-lodestone-b215` (d5df2416d9e07a37),
    `sc-oracle-aim` (8bfe5968101e10de), `sc-onslaught-fx` (ee74fe9ad67e50a6) and
    `sc-widowmaker-b1075` (18e927591b54ebc3).
  - **Reverse, on `sc-coldiron-temper-b93`:** the other builders re-apply cleanly on the final link.
    - `angelus_build.py`, `lightkeeper_build.py` and `lodestone_build.py`: stages 1, 2, 3 and 5.
    - `ironhail_build.py`: stages 1-3, plus `--stage 5 --alt50`. Its plain stage 5 writes nothing
      by design ("Stage 3's link is the final").
    - `oracle_build.py`: stages 1-3. Its stage 5 is not measured yet (`TUNED is None`).
    - `widowmaker_build.py`: stages 1, 2 and 5.
    - `bindweed_build.py` and `portcullis_build.py`: stage 6 (the Tendril and Onslaught pictures).
  - **Earlier fixes, before the review:**
    - The first try refused Widowmaker's link. The builder asserted the donor's blade, 11.95, and the
      Widowmaker redesign moves it. It now asserts the donor's physical profile, not its blade.
      Coldiron's 11.95 is the lab's number, written in the builder, and nothing reads Widowmaker's
      row.
    - It no longer asserts the other twinblades or the other dwarven relics, which are not what it
      needs.
  - **The review's change:** the post-check on `apply`'s ceiling line now asserts the clause
    `key === "sunder" ? this.sunderCap :` on the one `const cap = key === ...` line. It no longer
    asserts the whole line, so a later relic's own per-fighter ceiling clause on that line cannot
    make it refuse (`runs/captest.txt`: the old check refuses such a line, the new one accepts it).
    The five links rebuild byte-identical after every change.

## 5. Stage 6's ground: what the labs read on b93 (written before stage 6; built in §7)

Design §6.1-6.2 and brief §2 stage 6, picked on measurements under "you pick i overrule" (built in
scratch on b93 in §7; the carry is the orchestrator's). What a picture and voice lab reads, on
`sc-coldiron-temper-b93` (line numbers are that file's; the anchors are the strings):

- **Fields** (constructor, after `this.bleedCap = ...`, l.7967-7970): `f.ultTemper` — `{t, dur}` while
  the window runs (t on the window clock, 0 → 8), `null` otherwise; `f.massMul` — `5.0 / 1.1` in the
  window, 1 otherwise; `f.sunderCap` — 9 on the FOE of an open window, 6 otherwise (both fighters,
  every frame); `f.temperTally` — `null` until the first cast, then `{casts, frames, won, applied}`,
  cumulative: the probe's count, read by nothing.
- **The cast** (`fireUlt`, l.16278): the engine's generic head files everything the brief asks —
  the 0.08 stop (l.16302), `beat({kind:"ult", w:"coldiron"})` (l.16303), `SFX.play("ult", {w:
  "coldiron"})` (l.16305, the cast voice's hook: the QUENCH), and the one `ultFx` record, `kind:
  "temper"` (l.16313; Coldiron has no `life` entry, so it lives the table's default 1.5s, l.16398). Then the
  `u.kind === "temper"` branch (l.16681-16691) sets `ultTemper` and `massMul` and returns.
- **The ticker:** `this.tickTemper(dt)` (l.8966), after `tickTendril`, before `tickHits`, on the
  normal path only, so it freezes in a hit stop. `tickTemper` (l.13696-13713): the close is
  `if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultTemper = null; f.massMul = 1; ... }` — a
  CLOCK close is `Z.t >= Z.dur` with both alive (the design's cool-back-to-steel and "the ring dying"
  belong there); a death close is the other two, and it runs only in a kill flight. The ceiling
  recompute follows it.
- **The window at the end of a match:** on an ordinary kill `checkEnd` sets `m.over` in the killing
  step, after `tickTemper`, and nothing ticks again. So `ultTemper`, `massMul` 5/1.1 and the foe's
  `sunderCap` 9 are still set on the finished match (245 of 1613 windows on the final link's probe).
  **Draw the iron off `f.ultTemper && !m.over`** (or treat `m.over` as a close: cool the blades on the
  result card). Drawn off `f.ultTemper` alone, the blades stay iron on the result card after about
  nine in ten of the deaths that happen inside a window. No fight can change after `over`.
- **A won bind** (`resolveClank`, l.10788): the iron's clause at l.10825-10833 (`temperW` the winner,
  `temperL` the loser, `apply("sunder", u.bind, ...)`); the clank's own beat at l.10885
  (`{kind:"clank", x:hx, y:hy, streak, decisive, spd, close}` — the brief's "a won bind files the
  clank's own beat"; no new beat); its rings and sparks at l.10893-10898 (the winner's `aff.core`
  ring, the spray thrown along the loser's flight); **the clank voice, `SFX.play("clank", {mass:
  max(mA, mB)})` at l.10899, already hears the iron** (mass 5 in the window). The ANVIL RING (6 drawn
  sparks at hx, hy, no rng), the anvil strike stepping up with the sunder count, and "forge sparks
  off the blades at every won bind, both copies" (the field, `fx.js` and the page's copy) hang here.
  **A won bind files no status tag** today: the clause's `apply` is silent, so "the sunder tag on the
  foe ticking up" is a `statusTag` call stage 6 adds (picture only).
- **Past the cap as a colour:** the tag is `statusTag(x, y, "sunder", first, val)` (l.8592); a
  blade's own sunder tag is filed in `resolveHit` (l.14814), which prints a count (`val`) only for
  hemorrhage under a raised ceiling (Bloodletting's precedent). The shell's own sunder picture,
  `_stSunder` (l.23813, from `drawStatus` l.23511), draws `min(6, n)` flakes, so stacks 7-9 show
  nothing more today. Dwarven's palette: core #9C6326, glow #E8A34E, dark #2E1B0A, steel #6A6E74.
- **The head / silhouette:** `SHAPES.twinblade` (l.4345) routes `aff` "dwarven" to `SHAPES._tbBuilt`
  (l.4455), which no shipped relic has drawn: `_twinDagger` plus a chisel point, a collar and three
  rivets ON THE BLADE'S CENTRE LINE. The design's "two broad riveted cleavers, first cut (open item
  34's construction rule: rivets ON the outline, not on top)" is a redraw of `_tbBuilt`; only
  Coldiron reaches it. The window's "blades 1.4x thicker" and the quench (forge-orange cooling to
  black iron over 0.3s; back to steel over 0.4s at the close) are drawn off `f.ultTemper && !m.over` in
  `drawWeapon` (l.24021) — never by writing `w.artW` or `w.width` (the shared weapon).
- **A window to film** (brief stage 2, "FILM a bind won"; the picture is stage 6's, so the clip is
  too): `runs/bind_pick.txt` — **Coldiron v Spellbreaker, seed 99015**, cast at 15.83, clock close at
  25.16: five won binds, the foe 0 → 2 → 4 → 6 → 8 → 9 (past 6 at 20.72), Coldiron wins.

## 6. The review's four notes, closed at stage 6

The second review of stages 1-5 (verdict "pass", four notes) came back before stage 6 was built.
Each note is closed here; no link changed for any of them.

1. **chain_audit's control had no run file.** It is now `runs/chain_audit_ctl_base.txt` (the
   reviewer's run, copied verbatim): `chain_audit.py --relic <sc-coldiron-temper-b93> --tip
   <02-chain/sc-tendril-t3> --builder coldiron_build.py` → **15 LOST, exit 1**. The review's
   warning stands and is repeated here: `--relic <base> --tip <base>` is NOT that control (it
   prints "ALL 3 INSERTS SURVIVE", because chain_audit falls back to markers found in the base).
   Stage 6's own control is in §7d.
2. **Probe [1] could pass without its death close ever running.** [1]'s coverage now also needs
   `deathCloseOk > 0` (`coldiron_probe.py` db6a380e135e49d5; the stage-6 probe c6a76035520a0b90 is
   kept as `runs/coldiron_probe_c6a76035.py`). The reviewer's four mutants are in
   `runs/mutants_review2.py` (verbatim; 44e2f91944423d64) with their runs
   (`runs/probe_mut_q{1,2,3,4}-*.txt`), and they fill the gap the §3 table left ("[5] has no
   mutant"):

```
mutant                                              breaks                                  the probe v2                      Coldiron win (final 52.2%)
q1   the death close dropped (a kill flight         [1] "closes on a death"                 fails [1] only (29)               52.2 (29 windows never close)
     keeps the iron)
q2   the cap lifted on the CASTER, not the foe      [4] "sunder stacks past its limit"      fails [4] only (6260858)          37.7
q3   the iron blade hits x1.1 in the window         [5] the blades are still the blades     fails [5] only (5014)             58.8
q4   a deadlock sunders too                         [3] "each bind it WINS"                 fails [3] only (533)              53.7
```

   (mutant hashes q1 6a54695586c98252, q2 705628b54a762f39, q3 94b88c9c45ab0350, q4
   73c14657f0feee60). They were run with probe v2 bc34ecee5ad1ab30, whose checks db6a380e keeps
   unchanged; the one new clause can only add a fail.
3. **The builder's shared-weapon guard was narrow** (`w.(dmg|spin|reach|blades|mass) =` and
   `.w.X op=` only). It is now one test over every insert, stages 1-6:
   `\bw\.(dmg|spin|reach|blades|mass|width|artW|ult|onHit)\b[\w.]*\s*[-+*/]?=[^=]`
   (`coldiron_build.py` f194fa06f46454c9). The control (`runs/builder_guard_controls.txt`): a
   stage-2 insert carrying `f.w.artW *= 1.4;` or `f.w.ult.cap = 9;` is **refused** by the new
   builder (exit 1) and was **written** by the old one (1def68ac, exit 0). Stage 6's inserts also
   pass a stricter whitelist of their own (§7d). All six links rebuild byte-identical with the
   widened builder (`runs/rebuild7.txt`).
4. **Reading 1 (a Twinshade shade keeps the sunder ceiling of 6)** needed no change; it is now
   named beside reading 2 in §9 as a reading Rick may overrule.

## 7. Stage 6: the picture and the voice — `sc-coldiron-temper-fx`

Picked on measurements under Rick's "you pick i overrule", by two labs run in parallel on
`sc-coldiron-temper-b93` (the picture lab's scratch, `batch/coldiron/stage6-picture/`, and
`tools/coldiron_voice_lab.py` 2cb24b1439dae799), and built as `coldiron_build.py --stage 6`:
**fourteen anchored edits** (voice 3, picture 11), byte-exact to the labs' own row files. No two rows
share an anchor, so none is merged; voice-then-picture and picture-then-voice write the same bytes.
The picture rows alone reproduce the picture lab's stamp (94bb7580047f01bc). The link adds 23057
characters (picture 17587, voice 5470) and moves no fight (§7d). The sheet is
`05-reference/v103/coldiron-picture-sheet.png` (2200x2764, 42b61c1be5f52172); the voice's wavs are in
`05-reference/v103/coldiron-*.wav` (47, gitignored).

How the rows reached the builder (`runs/gen_s6.py`, `runs/gen_s6.out`, `runs/check_reports.{py,txt}`):
the rows the labs returned equal their files field for field (voice `rows_final.json`
ca982fff987f77fc, which is the lab's `rows_lab.json` plus each row's `why`, reproduced byte for byte by
its confirmation run; picture `rows_final.json` 2c035026c727a316, the file the lab recorded); every
anchor occurs once in b93 and no anchor sits inside another row's span; the S6 list in the builder is
those rows as (label, anchor, new text), in order. **Names:** every stage-6 name is checked free on
identifier boundaries, because `tickIron` is a prefix of the staff row's `tickIronfall` (the
tickVine / tickVines trap).

### 7a. The picture (v73 §6.1), as built

- **The quench (the cast).** The whole blade flashes forge-orange #F08A30, edge and bevel white-hot
  #FFF2C8, and cools on p = u² over 0.3s (it holds hot, then drops) to **black iron**: dwarven `dark`
  #2E1B0A for the flat, and "the steel edge gone matte" as the bevel and the honed line in a matte grey
  taken off the school's steel. Over the same 0.3s the blades ease from 1.0x to **1.4x wide** on a
  smoothstep. Palette and width are locals of the draw: `w` is never written (the builder refuses it,
  §6 note 3, and the lab's drawn fights checked it). The quench opens inside the cast's own 0.08s stop. The
  ball does not change.
- **The window** is drawn off `f.ultTemper && !m.over` (reading 4: on an ordinary kill the window is
  still set at `over`), so **the cool** — 0.4s back to steel and 1.0x, no debris — runs on a clock
  close and also at the verdict. There is no cool when the caster dies: the shatter owns the ball.
  Presentation clocks run at half speed in a hit stop (the engine's rule), so a cool that starts in a
  stop runs long (once 0.78s against 0.40-0.53).
- **A won bind** (found by `temperTally.won` rising; the contact read back off the clank's own beat,
  `decisive` and `b.t === m.t`): the **anvil ring**, 6 radial sparks with a white-hot core in a glow
  sheath, 0.25s, at the clank's own contact and turned by `shellHash` of the bind count (no rng); and
  the **forge sparks**, 5 per blade struck off the outer half of each edge and flung with the spin
  (0.35-0.6s). Both are drawn in the world pass, source-over. No beat, no stop.
- **The sunder tag ticking up** (reading 10). Before this, a won bind filed no tag at all. It now files
  `SUNDER n` on the foe's rim toward the bind, or updates the sunder tag already up there in place
  (Tendril's one-tag rule); while the foe's `sunderCap` is raised, the blade's own sunder tag in
  `resolveHit` carries its count too (Bloodletting's precedent, one status along; the tag's `val`
  only).
- **Past the cap is a colour — a reading the code forced.** The design says a tag past 6 "prints in
  dwarven's `core` rather than the default"; but `statusTag` colours a status by the school that owns
  it, so the SUNDER tag's default already IS dwarven's core (#9C6326), and the literal reading changes
  nothing. The build follows the stated purpose ("so 'past the cap' is a colour"): **a count above 6
  prints in dwarven's glow, #E8A34E.** One expression in the `statusTag` row; Rick's to overrule.
- **Stacks 7-9 on the ball (Code's pick; the design does not ask).** `_stSunder` draws `min(6, n)`
  flakes, so 7-9 were invisible on the shell; `_stSunderPast` draws the rest as hot flakes in the
  glow. They outlive the window, as the stacks do (§3: 802 of 1103 closes left the foe above 6 at the
  next cast or the end). Dropping them is one row.
- **The silhouette.** `_tbBuilt`, the dwarven twinblade route that no shipped relic drew before
  Coldiron, becomes **two broad cleavers**: three rivet heads stand half out of the spine, in the
  blade's own path, so they are ON the outline (open item 34's rule); the chisel end is kept (squared,
  cut back on the edge side); a bright ground bevel under the honed line; a squared iron collar; the
  flat lifted off dwarven steel (`_shade` 1.2), because plain #6A6E74 read too dark. At the app's size
  the weapon reads |dL| 0.148 over the floor, **4th of the 6 twinblades** (Spellbreaker 0.273,
  Widowmaker 0.174, Starwarden 0.158, Coldiron 0.148, Twinshade 0.146, Thornshear 0.145) with the
  largest ink area (3942 px); the old cut read 0.105, last, and overlapped Twinshade's ink at IoU 0.905
  (the new one 0.40-0.57 against every sibling). A first cut, Rick's to overrule.

**The picture lab's gates** (its `numbers`; Chromium 151 at 540x960, post chain on, shake zeroed):
- **Bloom:** the picture's share of the chain's arena-mean lift max +0.0000, min -0.0004 (gate +0.02),
  over 80 frames in 11 states (rest, quench, iron, hit stop, a won bind at +2/+14/+24 steps, past 6 in
  and after the window, the cool, the verdict) against white, dark and ordinary foes. The controls
  fail it: the quench as a disc R+18 at 0.6 puts the caster's disc above 0.90 on 53 of 64 window
  frames (1 of 64 without); a halo R+120 at 0.35 lifts +0.0771; an anvil ring as a disc r 70 at 0.9
  moves the foe's disc +0.51. (The same controls in dwarven's own glow lift only +0.0006 — under the
  bloom's knee, so they could not fail and were rebuilt white-hot.)
- **Discs:** the caster's moves at most 0.0074 and is above 0.90 on the same 1 of 80 frames with and
  without the rows (the body); no ball's disc is erased.
- **Legibility** (median |dL| of each component's own pixels, out of a stop / in one): the resting
  head 0.167; the quench 0.255 / 0.128; iron against the steel look 0.119 / 0.087; the anvil ring 0.319
  / 0.320; the forge sparks 0.402 / 0.417; the bind's SUNDER tag 0.229 / 0.257; the count and past-6
  colour 0.242 / 0.175; the hot flakes 0.191; the cool 0.107 / 0.099. **The iron weapon reads 0.079
  over the floor against the steel look's 0.109: the design's black iron is darker than steel** (the
  matte-steel edge lifted it from 0.072).
- **Sim identity:** 13 whole fights (11 with Coldiron, on both sides between them; 2 without)
  identical to the base,
  undrawn AND drawn; the control, `foe.vx += 1e-9` in `tickIron`'s won-bind branch, differs on all 9
  Coldiron fights that have a won bind and on none of the others.
- **Drawn through the kill:** 0 throws; 127 won binds, each found once, 127/127 rings at the clank's
  own contact (to 1e-9) and 127/127 with the foe's SUNDER tag showing the count the bind left; 176 tags
  past 6, all in the glow, none at or under 6 in it; at most 1 ring and 19 sparks up at once.
- **Frame cost** (Electron from `app/`, RTX 3070 through ANGLE D3D11, 453x805, interleaved A/B with
  the order flipped every frame, on a machine loaded at 40-68 ms a frame): whole-frame medians, rows
  minus base, -3.0..+1.7 ms with no sign; the picture's own calls -1.3..+0.5 ms. No `shadowBlur` is
  added; the 1.4x blades bake at most 13 glow sprites, once.

### 7b. The voice (v73 §6.2; `tools/coldiron_voice_lab.py`)

Coldiron had no voice arm: its cast fell through to **rune-crack** (as Ironhail's and Spellbreaker's
still do). The three arms are added BEFORE that shared fallback, whose line is re-emitted last and
unchanged, so another relic's voice row anchored there still applies, in either order. Controls
reproduce the published numbers (rune-crack peak 0.608 / 450 ms; hit@11.6 0.443 / 80 ms).

- **Cast — STEAM (7 of 8), "a quench hiss into a low iron ring, 0.5s":** a q 2.5 noise band falling
  7.5 → 5 kHz over 0.32s (12 ms attack), and from 80 ms under it an iron bar on A2, the score's tonic
  (sines on the free-bar modes 1 : 2.76 : 5.40 : 8.93), ringing on alone. Audible 490 ms; the hiss
  leads the first 100 ms (-1.1 dB re the whole) and is silent by the end; the ring's loudest 50 ms comes
  70 ms after the hiss's; the loudest 50 ms -2.9 dB re Coldiron's blow at 9.3. **Worst register 0.79
  (Emberedge's cast), 0.01 under the gate.** HUSH also passes (0.78) and loses on list order; BAR,
  PLATE, SPIT and IRON fail on Emberedge (0.84-0.88); TENOR (A3) and DEEP (E2) sit under the score.
- **A won bind — SEMI (3 of 4), "an anvil strike (a hard metallic hit with a 0.3s ring, peak ≤ 0.6)
  over the engine's clank voice; pitch steps up with the sunder count":** a struck steel block
  (triangle on the note, sines on 2.76 and 5.40) under a 12 ms 5 kHz contact click, **a semitone a
  stack, A5 (880 Hz) at count 1 to F6 (1397 Hz) at 9**. Audible 295-300 ms; sample peak ≤ 0.536 on
  every count and noise draw (0.861 with the clank on its frame, gated only against clipping); at
  least +10.2 dB over the clank in its own band; worst register 0.54. `resolveClank` plays it on the
  won bind's own frame, after the loser's sunder, over the clank's own voice, with `n` = the loser's
  count after the bind (reading 8). BAR (the A-minor pentatonic) passes too and loses the tiebreak
  (0.73 against rune-crack); PLATE (+9.2 dB over the clank) and LOW are out.
- **Close — BARE (3 of 3), "the ring dying, 0.4s":** the cast's own ring on A2 without its top mode,
  not struck again: it starts at its loudest, -8.2 dB under the cast, and fades over 395 ms; heard by
  its 304 Hz mode, +3.1 dB over twice the score's p90 (its 110 Hz sits under the score). Worst register
  0.76 (the death voice). FADE and DROOP tie; BARE wins on fewer calls. `tickTemper` plays it only
  when the window closes BY ITS CLOCK with both alive (reading 9): a death close (a kill flight) and a
  window still set at `over` play nothing and are left to the death voice (Zenith's, Canopy's and
  Onslaught's rule).
- **Controls, each failing at least one gate:** cast NOHISS, NORING, SAME, HIGH, HARM, RC-NOW; anvil
  FLAT, TICK, HARM, LOUD, CLANK; close STRUCK, HELD, OTHER, SHORT.
- **In a real window** (Coldiron v Spellbreaker 99015, anvils at counts 2 4 6 8 9 9): the anvils
  +24.9 / +28.5 / +23.4 / +10.1 / +10.4 / +10.1 dB over the fight, clank included; the close +3.3 dB at
  304 Hz; the cast's ring +13.6 dB at its loudest partial (982 Hz), its hiss +21.5 dB.
- **The lab's sim check:** 152 fights with the rows beside the real functions, 152/152 identical and
  every other voice call identical in order, kind and opts; 540 casts / 540 cast voices; 1629 won
  binds / 1629 anvils (counts 2:84, 3:60, 4:86, 5:75, 6:82, 7:75, 8:86, **9:1081**); 436 clock closes /
  436 close voices; the 14 death closes and 90 windows open at `over` silent. The sim-write control
  comes back 24/152 identical.
- **Code's numbers where the design gives words:** the ring 80 ms in, "low" < 262 Hz, the ring on the
  score's key, the anvil's 5 kHz click and its level matched to peak 0.54; the lab's first-cut
  corrections (the close read at its loudest partial; the cast's real-window gate likewise; an
  instrument fix for shade binds) are in its docstring.

### 7c. No `fx.js` field — the forge sparks are drawn

The brief says "Field in both copies" and the design "Field: forge sparks off the blades at every won
bind, both copies". **`fx.js` is untouched, both copies** (Zenith's, Canopy's and Bindweed's
precedent), because a field cannot be what the sentence asks. Measured on b93 over 121 Temper windows
(16 foes x 2 seeds, both sides; the picture lab's `ci_fxprobe.py`):
- a SPECS row fires ONCE, at the cast edge of the one `m.ultFx` slot, at the caster's cast point;
- Coldiron holds that slot a median 0.65s of its window clock (max 0.72), and the opponent's cast took
  it in 21 of 121 windows — a slot-borne field could exist for 7.7% of the window;
- the 427 won binds fall a median 3.58s into the window (p10 0.75s); only 31 of 427 land while the slot
  is still Coldiron's, and those after the field has already spawned at the cast;
- a bind's contact is a median 196 units from the cast point (p10 60, p90 425).

A field that spawns once, at the cast, ~200 units from the binds, cannot be sparks at every won bind.
The sparks are drawn at every won bind instead (§7a), with bloom share 0.0000 and |dL| 0.40. The
page's own per-event sparks (`spawnFx`) are no way round it: they draw the match's RNG, so they would
move fights, and the builder refuses them in any insert. **Rick's to overrule.**

### 7d. Stage 6's gates — every one able to fail

Chromium 151.0.7922.34 (playwright 1.62.0) throughout; at most two browsers of this build's at once
(one exception, declared: `tip_audit.py` opens a page, and its two ~10 s runs went up beside the two
running jobs). Run files in `runs/` (names below).

- **engine_ab sc-coldiron-temper-b93 → sc-coldiron-temper-fx, ALL 39 WITH Coldiron, n=6: 4446/4446
  identical** (741 pairings; 39/39 distinct winners, 4446 distinct seeds, 20.3-118.1s; no page errors;
  `runs/engine_ab39.txt`, ids `runs/ids39.txt`). Presentation moves no fight.
- **coldiron_probe (db6a380e135e49d5) on the fx link: 9/9** (`runs/probe_fx_final.txt` / `.json`;
  the same run with the stage-6 probe c6a76035 before the review's [1] clause, `runs/probe_fx.txt` /
  `.json`, reads the same numbers, and its json is equal). [1]-[7] read stage 5's numbers to the
  digit (52.2%, 3.54 casts a fight, 1613 casts, 1342 clock closes, 26 death closes, 245 set at
  `over`), and the two stage-6 checks, each switched on by reading the page itself (the voice when
  `"coldiron-anvil"` is in `AC.SFX.play.toString()`, the picture when the Match has `tickIron`):
  - **[8] the voice:** one `ult`/coldiron voice a cast (1613 of 1613 casts); one anvil a won bind, at the
    loser's count after the bind's sunder (**5018 of 5018**: n 2:259, 3:225, 4:253, 5:253, 6:251, 7:249,
    8:268, 9:3260), none on any other clank, and each clank its own one clank voice with nothing else
    sounding in `resolveClank` (6621 plain clanks); one close a clock close with both alive (**1342 of
    1342**), **none on the 26 death closes** and none on the 245 windows still set at `over`; nothing else
    sounds in `tickTemper`; and every Coldiron voice of the run accounted for by its event (1613 /
    5018 / 1342 — so none plays after `over`). **The ward's note:** a ward shatter plays its own crit
    hit voice inside `hurt()`; neither `resolveClank` nor `tickTemper` calls `hurt`, so "nothing else
    sounds there" cannot be tripped by a ward, and the cast check counts only Coldiron's voices
    (`fireUlt` does call `hurt` for other relics' casts).
  - **[9] the picture:** `tickIron`, the picture's one hook on the step, changed no sim field of either
    fighter, a shade or the match and drew no RNG on 6683441 calls; the iron up exactly while the window
    is open, the match not over and the caster alive (3089632 fighter-steps up, 143273 cooling); 5018 of
    5018 won binds rang one new ring at the `resolveClank` call's own contact and, the foe alive, put a
    sunder tag on the board reading the foe's count (3805 of them past 6); 14735 sunder tags coloured
    right (7015 past 6, in dwarven's glow; none at 6 or under in it); the 245 windows still set at `over`
    cooled to 0 within 0.5s of the verdict; and on the drawn subset (the first seed, both sides, every
    foe, through the kill and 0.5s of verdict) 70884 drawn frames (67706 with the picture up, 10810 of
    them in a hit stop, 701 in the verdict) that threw nothing, drew none of the match's RNG and wrote no
    sim field.
- **The probe's stage-6 controls** (`runs/mutants6.py`, one-line mutants of the fx link; runs
  `runs/probe_mut_mS*.txt`):

```
mutant (hash)                                       breaks                                   the probe (db6a380e)               Coldiron win (fx 52.2%)
mS1  the close voiced on EVERY close,               [8] "one close a clock close,            fails [8] only (27: the 26 death   52.2 (a voice: no fight moves)
     death closes included (63e533ffb9863d59)            none on a death"                    closes, and 1368 voices vs 1342)
mS2  the anvil pitched at the count BEFORE the      [8] "one anvil a won bind at the         fails [8] only (5019: every won    52.2 (a voice: no fight moves)
     bind's sunder, n - bind (da07416d964e4a95)          loser's count"                      bind, and the run's accounting)
mS3  tickIron nudges the foe's vx 1e-9 on a won     [9] "a picture hook never writes         fails [9] only (5099: every won    55.5 (fights move)
     bind (2acfd973153aabe7)                             sim state"                          bind)
mS4  a drawn frame nudges fighter a's vx 1e-9       [9] "no drawn frame writes the sim"      fails [9] only (10611, on the      52.0 (the drawn seed's
     (2b21db99dcffdcd6)                                                                      drawn subset)                      fights move)
```

  Each fails its own check and nothing else. mS3 and mS4 move fights and [1]-[7] still pass: those
  checks rebuild each sentence from the state as it is, so a stray write that breaks no sentence is
  not theirs to see; [9] and engine_ab are. mS1 also leaves [8]'s coverage short (no death close is
  silent). The first loop that ran these was stopped after mS1 to split the other three over the two
  browsers (`runs/probes6_mut.sh`, `runs/probes6_mut_split.sh`); mS1's probe ran to its end in the same
  file, so its `exit` line is written by hand.

- **render_ab b93 → fx, the other relics' pairs: 24/24 pixel-identical** (paradox v heartwood 25064,
  twinshade v lastlight 991, bulwarden v vinesower 70707, axiom v grudgebearer 31337 at 0.5, 6, 12, 22,
  31, 40s; `runs/render_ab_others.txt`). **The control, Coldiron v Vinesower 103349 inside the clip's
  window (33, 35, 37, 39, 41s): 0/5 identical**, exit 1 (`runs/render_ab_control.txt`).
- **chain_audit --builder coldiron_build.py (f194fa06): 29/29 inserts survive to sc-coldiron-temper-fx**
  (15 of stages 1-5, 14 of stage 6; exit 0, `runs/chain_audit_fx_final.txt`). **Its control**, the same
  audit with b93 as the tip, finds **the 14 stage-6 inserts LOST**, exit 1
  (`runs/chain_audit_fx_final_ctl.txt`). On the dry-run carry to the real tip, 29/29
  (`runs/chain_audit_fx_on_tipdry.txt`, builder 1def68ac).
- **tip_audit:** sc-coldiron-temper-fx reads exactly as b93 (and b93 as recorded in stage 5): the one
  MISSING line, Burn's `feed`, is the base's (`runs/tip_audit_fx.txt`). Stage 6 teaches no status.
- **The builder** (`runs/build_s6.txt`, `runs/builder_checks_s6.txt`, `runs/builder_controls_s6.txt`):
  stage 6 goes on stage 5 once (it refuses a second run — `tickIron` is already there — and refuses
  stage 4's link, and refuses to overwrite a link); every stage-6 name is free on identifier
  boundaries; every stage-6 insert, its re-emitted anchor aside and comments stripped, draws no RNG,
  never takes the one ultFx slot, calls nothing that hurts, heals, applies, resolves, shatters, knocks,
  files a beat or fires an ult, and writes only what its whitelist names (its own `iron*` fields,
  the canvas, a tag's `val` and colour, a record's clock, `taught`, an oscillator's pitch). Four
  builder mutants are refused, one per rule: a `foe.vx` write, an `rng()` draw, an `ultFx` use and a
  `beat(` call. The widened weapon guard and its control are §6 note 3. Stages 1-6 rebuild byte-identical from the base
  (`runs/rebuild7.txt`).
- **Composition** (`runs/compose6b.sh`, `runs/compose6b.txt`, the final builder, no browser): stages
  1-6 re-apply cleanly, forward, on the real tip `sc-tendril-fx` (s6 67cc3e6e05d5326e, the dry
  run's) and on the newest scratch link of every build in flight — `sc-angelus-b9`, `sc-ironhail-b14`, `sc-lightkeeper-bulwark-b9.5`, `sc-lodestone-b205`,
  `sc-oracle-aim`, `sc-oracle-sight`, `sc-widowmaker-b1075` — each +23057 characters, the same as on
  b93; and in reverse the other builders re-apply on the fx link (angelus, lightkeeper and lodestone
  stages 1 2 3 5; ironhail and oracle 1-3; widowmaker 1 2 5; bindweed's and portcullis's stage 6, the
  Tendril and Onslaught pictures). The first run (builder 1def68ac, `runs/compose6.txt`) read the same
  hashes on the links it had.
- **The carry, dry** (`runs/carry_dry_tipfx_s6.txt`): stages 1-6 on the real tip
  `02-chain/sc-tendril-fx.html` (eea0cde5536955b3) give s6 67cc3e6e05d5326e; stage 5 is the file
  `runs/carry_dry_tipfx.txt` recorded; each of stage 6's 14 edits' text is in both exactly once; the
  416 lines it adds and 17 it removes on the tip are line for line b93 → fx's (+23057 characters on
  both).
- **Not run here: `shell_identity`** (the app's json is shared; the orchestrator runs it on the carried
  link).

## 8. The clip (Rick's to overrule)

`tools/_coldiron_pick.py` (from `_ironwood_pick.py`, by way of `_bindweed_pick.py`) scores a window on
v73 §6: it must close BY ITS CLOCK with both alive (the only close that cools the blades and rings
out), with binds won in the iron — each an anvil ring, forge sparks, an anvil note and the SUNDER tag
ticking up — the count going past 6, and the fight running on for the clip's 1.8s tail; the counts
the anvils strike at score by how many different ones are heard, so a window that climbs 2-4-6-8-9
beats one that starts at the ceiling. 12 foes x 6 seeds plus §5's Spellbreaker 99015
(`runs/pick_s6.txt`). The pick: **Coldiron v Vinesower, seed 103349**, cast at 32.05, a clock close
after 9.87s of match time (8s on the window clock), 6 won binds at counts 2 4 6 8 9 9, past 6 at 36.99,
score 18.60 (Heartwood 103386 18.10, Twinshade 103312 18.00; Spellbreaker 99015 17.70).

    python cinema_clip.py --game <scratch>/batch/coldiron/links/sc-coldiron-temper-fx.html \
      --a coldiron --b vinesower --seed 103349 --at 30.85 --window 12.87 --end-at-window \
      --fps 60 --w 540 --out ../07-shorts/v103/temper-window.mp4

(`<scratch>` is this session's scratchpad,
`C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad`;
run from `tools/`.)

**`07-shorts/v103/temper-window.mp4`**: 12.87s, 772 frames, 540x960 at 60 fps (h264) with AAC 48 kHz
stereo, 2.93 MB (c26fdc94808250d7); the fight is still on at the end (43.725, hp 329 / 284;
`runs/clip_s6.log`). Filmed on the scratch link: when the carry lands, the same command on the chain
link films the same fight (engine_ab).

**What is in it** (`runs/clip_timeline.py` / `.txt`, clip time = match time - 30.858): the cast at 1.20
(the foe at 0 stacks); won binds at 1.95 (the foe to 2), 3.27 (4), 4.08 (6), 6.14 (8: past 6), 7.83 (9)
and 9.91 (9, at the ceiling); the clock close at 11.08; 1.8s of the fight after it.

**Five frames, checked through the pipeline** (ffmpeg tile of frames 78, 120, 372, 540 and 678; kept in
scratch, `batch/coldiron/s6/clip_tile.png`, with two zooms): the quench (the blades forge-orange under
the "Temper" card); the first won bind (the anvil ring at the contact and `SUNDER 2` in dwarven's core);
the bind to 8 (`SUNDER 8` in the brighter glow, a ring at the contact); the window (black iron, broad
cleavers, 1.4x); after the close (the riveted cleavers back in steel). The art renders through the
clip's own pipeline (`CINE.pump` / `CINE.drawLerped`, the draw code the live page runs).

**The sound** (`runs/clip_aac.txt`, `runs/clip_audio_check.{py,txt}`): AAC mean -21.7 dB, max -1.5 dB;
-19.5 LUFS integrated, LRA 0.8 LU, true peak -1.3 dBFS (v99's canopy clip: mean -22.7, max -1.6). Read
off the AAC: **every anvil sounds at its count's note** — the note for the loser's count rises +37.9 to
+71.1 dB in the 100 ms from its bind (932 Hz at 2 up to 1397 Hz at 9); the cast's ring rises +8.3 /
+12.0 / +31.3 / +22.9 dB at 110 / 304 / 594 / 982 Hz. **The close is soft in this clip:** its 304 Hz
mode stands +29.2 dB over its neighbours in the 250 ms after the close (+7 to +11 around it), but its
level (-47 dBFS) does not rise above what the score already plays at that partial. That is the voice
lab's pick doing what it measured (-8.2 dB under the cast, heard by that one mode, +3.1 dB over twice
the score's p90). Rick's to judge.

For Rick, with this doc. **Rick's to overrule.**

## 9. What is left, and whose

- **Rick:**
  - **the clip** (§8, `07-shorts/v103/temper-window.mp4`) and **stage 6's picks**, under "you pick i
    overrule":
    - the picture: the quench (forge-orange cooling to black iron, the blades 1.4x wide), the anvil
      ring and the forge sparks, the cool at a clock close and at the verdict, the `_tbBuilt` redraw
      as two riveted cleavers (a first cut; 4th of 6 twinblades on legibility);
    - **no `fx.js` field** — the forge sparks are drawn (§7c);
    - **the colour past 6 is dwarven's glow, not its core** (the design's literal word changes nothing,
      because the sunder tag is already in the core; §7a);
    - **the hot flakes past 6 on the ball** (Code's pick, not the design's; they outlive the window
      as the stacks do; dropping them is one row);
    - the voices: the STEAM cast (register 0.79, 0.01 under the gate); the SEMI anvil, which steps
      chromatically (A#5 at count 2 is outside the score's key; BAR, on the A-minor pentatonic, also
      passes), with **1081 of 1629 anvils ringing at count 9 (F6)** in the lab because the blade holds
      the foe at the cap; the BARE close, heard by its 304 Hz mode and **soft in the clip** (§8).
    - To hear the voices alone: `05-reference/v103/coldiron-pick-sequence.wav` (cast, anvils at
      2/4/6/8/9 over the clank, the close, a blow); the real window with and without them:
      `coldiron-pick-real-window{,-without}.wav`. The picture:
      `05-reference/v103/coldiron-picture-sheet.png`.
  - carried from stages 1-5: **the hammers at 30%** (brief §4.4, design §7.4; Ironwood, a hammer the
    design's roster did not have, is the worst foe at 17.5%); the foe spread, 57.5pp, and the type
    spread, 34pp where the design had 29 (item 12/32); **stacks past the cap outlive the window** (every
    sunder that lands refreshes the 5s clock; 802 of the 1103 closes that left the foe above 6 still
    had it above 6 at the next cast or the end) — now on screen as the flakes and the glow tag;
  - **readings 1 and 2, the shades** (the review's note 4): a Twinshade shade keeps the ceiling of 6
    (reading 1, from the brief's sketch; the lab's global lift and the design's "on the foe BEING
    sundered" would lift a sundered shade to 9), and a bind won against a shade sunders the shade
    (reading 2; the lab sundered the opponent; the two differ on 34 binds in 456 fights). Both are
    declared; either is one line.
- **The orchestrator:**
  - **carry** stages 1-6 onto the real chain one relic at a time (`coldiron_build.py --stage N --src
    <tip> --out <link>`, 1 to 6 in order; the dry run on `sc-tendril-fx` is clean, §7d) and prove it
    with engine_ab, stage 6 against stage 5 with every id, Coldiron included;
  - **`shell_identity`** on the carried stage-6 link (not run here: the app's json is shared);
  - `chain_audit --builder coldiron_build.py` on the carried link (29 inserts);
  - `CLAIMS.md` and `CLAUDE.md` §0 on the carry (this build writes neither);
  - move `app/main.js`'s `GAME` line (brief stage 6) only when Rick has nothing to overrule on the
    batch's clips.
- **Standing, not this build's:**
  - verify's two clock bands ("pairing mean duration 18-70s", "overall mean 28-54s") are red on every
    link since the minute pace;
  - tip_audit's one MISSING line, Burn's `feed`, is the base's;
  - the brief calls Coldiron "the 40th relic" (the cell's number); on this base it is the 39th in the
    roster, and its place on the chain is the carry order's.

## 9. The carry onto the chain

Built and gated in scratch on `sc-tendril-t3` while the batch's other builds ran on the same tip, then
carried onto the chain after Bindweed's stage 6 (`sc-tendril-fx`) with the same builder, one stage at
a time (`--src` the previous link):

```
sc-tendril-fx.html        the chain tip (Bindweed stage 6)
  -> sc-coldiron.html              stage 1   689a0ab8d366fd55
  -> sc-coldiron-mass.html         stage 2   8937a1f5b0ad1598
  -> sc-coldiron-bind.html         stage 3   86f36d046222f8b7
  -> sc-coldiron-temper.html       stage 4   a13d08d7162f6405
  -> sc-coldiron-temper-b93.html   stage 5   79949e14c617cd93
  -> sc-coldiron-temper-fx.html    stage 6   67cc3e6e05d5326e
```

- **engine_ab, the scratch stage-6 link against the carried one, all 39 relics WITH Coldiron, n=6:
  4446/4446 identical** (`runs/carry_engine_ab.txt`, hashes in `runs/carry_links.txt`). Every number
  above carries.
- **shell_identity on the carried `sc-coldiron-temper-fx`** (`SWB_GAME`, the pointer not moved; the
  json restored): **185/185** (`runs/carry_shell_identity.txt`).

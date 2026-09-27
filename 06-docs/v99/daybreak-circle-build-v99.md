# v99 — DAWNBRINGER / DAYBREAK, THE CIRCLE, BUILD. STAGES 1-3 BUILT AND GATED ON yert; THE CLIP IS WITH RICK (card hidden). A side branch off `sc-zenith`; the app pointer waits on him.

Claude Code on **yert**, claimed 2026-09-27 04:17 UTC (`CLAIMS.md`, the BUILD row under THE
CIRCLE). **Rick chose yert over DESKTOP-DERRAFT for this one**, asked in this session: the
design batch is otherwise built there. The input is `06-docs/v99/DAYBREAK-CIRCLE-BUILD-BRIEF.md`
and `dawnbringer-daybreak-circle-design-v99.md` (Cowork), and nothing else (rule 0). Builder
`tools/sunrise_build.py`, probe `tools/sunrise_probe.py`, the picture's gates
`tools/sunrise_sheet.py`, the voices `tools/sunrise_voice_lab.py`, the clip `tools/_sunrise_pick.py`.

```
sc-zenith.html            the base: the batch tip (sc-leaf + Corollary c14 + the line + Zenith 1-4)
  -> sc-sunrise.html        stage 1  the line out, the sun in    sunrise_build --stage 1   b84435a83eb5cce7
                            stage 2  the blade                   10.4 CONFIRMED -- no link
  -> sc-sunrise-fx.html     stage 3  picture, voice, the tick's marks   sunrise_build --stage 3
```

**A SIDE BRANCH.** DESKTOP-DERRAFT is building Ironwood on the same link (`sc-zenith`), so the
batch line is forked at `sc-zenith` until one of the two is re-applied onto the other's tip.
`sunrise_build.py --src` takes any later tip that still carries the line, and it pins every span
it cuts by sha256, so a carry onto a tip where somebody has edited the line refuses instead of
cutting something else. **The app pointer does not move** (it still reads `sc-leaf`).

## 0. What this build stands on, and the readings it had to make

**The base is asserted**: Corollary at charge 14, the line through its stage 3 (`dawnShown`, the
line's ult block as built), and Zenith.

**THE BRIEF'S NAMES COLLIDE WITH ZENITH'S, SO THEY ARE NOT THE BRIEF'S.** The brief says
`f.ultSun`, `tickSun` and a beat flag `sun: true`. All three are Morningstar / Zenith's
(`morningstar_build.py`, v98), built on this link before the brief was written against
`sc-corollary-c14`. This relic's state is `ultSunrise`, its ticker `tickSunrise`, its beat flag
`sunrise: true`, matching the block's `kind:"sunrise"`, which the brief does name. A naming
collision, not a design choice; the builder asserts Zenith's `ultSun` is untouched.

The readings (in `sunrise_build.py`'s docstring):
1. **The tick's cadence is the lab's**: a 0.5s cooldown through the sun's whole life, firing on
   the first inside frame it is clear, zeroed at the break.
2. **`apply`'s source is a side letter** (the engine's contract).
3. **No beat for a tick, except the tick that kills**, which files its own fatal `hit` beat.
4. **The anchor is the blow's own hit point**, as §4 declares (the lab used the foe's centre).
   A blow on one of Twinshade's shades is a blow that landed.
5. **The break files a beat** at the hit point: the cast beat's kind and fields, `sunrise: true`.
6. **The target is the opponent**, never a shade.
7. **Armed and up are two flags on one record**: a re-cast while a sun is up re-arms the blade
   and leaves that sun burning until the next break (what the lab does).

**The clock** is the window tickers' (it stops through a hit stop). The lab counted every step.

## 1. Stage 0: the control on 151, on sc-zenith (35 relics)

`ult_overlay.py --relic dawnbringer`, seeds 20 (680 fights an arm a block), seed0 2207 and 2317,
`runs/build/s0_*`. Chromium 151.0.7922.34; `math_fingerprint` PASS.

```
arm                              design, 141 (c14)    151 block 1   block 2   pooled (1360)
A      no ultimate               19.1                 14.9          16.2      15.6
SHIP   the sparks (on c14)       60.7                 56.7          57.4      57.1   (660 a block)
B      the line (lab)            52.6                 53.4          51.5      52.5
SHIP   the line as built         --                   52.4          50.6      51.5
C      grows the whole 8s        43.2 (r 220)         44.1          40.4      42.3
D      THE SUN r200 g2 (taken)   52.7                 52.9          47.2      50.1
E      follows the foe           63.5 (r 220)         62.8          61.9      62.4
```

**The mechanism reproduces to the digit**: arm D's foe is inside 55.4 / 55.2% of the sun's life
(design 56.0), 9.82 / 9.78 ticks and 19.6 damage a cast (9.8, 19.5), 3.17 / 3.19 suns a fight
(3.21), a mean wait of 2.92 / 3.00s (2.96). **The win rate is 2.6 under the published 52.7**, and
the line on the same seeds sits 2.4 above the sun: both inside the batch's tier (5pp at 660).
Every gate below reads against this run.

## 2. Stage 1: the line out, the sun in — `sc-sunrise.html`

`sunrise_build.py --stage 1 --src ../02-chain/sc-zenith.html --out ../02-chain/sc-sunrise.html`:
src `9be1a7ca4832c327`, out `b84435a83eb5cce7`, -10376 characters.

**The line comes out as six whole spans, each pinned by sha256** (the brief's "whole spans"):
the picture fields, the presentation clock, the draw call, `drawDawn`, the eight-step voices,
and `tickDawn` with its SMITE tag (which the sun's ticker replaces). Then eight edits: the ult
block (`kind:"sunrise"`, charge 14, dur 8, grow 2, r 200, tick 0.5, tickDmg 2, smite 1, the
brief's 71-character card), the fighter's record, the cast, the break in `resolveHit` beside
`self.hits++`, the ticker in `tickDawn`'s slot, and three comments that described the line.
The builder refuses to write if any of eleven line names or `kind:"dawn"` survives.

- **`sunrise_probe`: 12/12** (408 fights, Dawnbringer both sides; `runs/build/s1_probe.txt`).
  3.17 suns a fight, **0.966 breaks a cast** (the brief: >= 0.95), 9.11 ticks and 18.2 damage a
  cast, the arming a mean **2.80s** (median 1.77, **p90 6.93**, max 15.7). 17 killing ticks, each
  with its fatal beat; 185 wards broken by a tick; 123 re-casts with a sun up.
- **THE ANCHOR DOES NOT MATTER.** The foe is inside the sun **51.9%** of its life anchored at the
  hit point, and **51.4%** had the same sun been anchored at the foe's centre (the lab's anchor,
  tracked in the probe on the same fights). The hit point sits a median 37.7 from the struck
  body's centre (p10 32.1, p90 40.4). The design's 56% is the lab's clock: it ticks through hit
  stops, which the engine does not, and the sun is anchored where the blows land.
- **engine_ab sc-zenith → sc-sunrise, the 34 others, n=8: 4488/4488 identical**
  (`runs/build/s1_engine_ab34.txt`).
- **The relic at 10.4: 48.4 / 49.4%, pooled 48.9%** (`runs/build/s1_rate_*`), against stage 0's
  arm D at 50.1%. In tier. The rate runs replay the lab's own fights (`sunrise_probe --rate`);
  **its control reproduces `ult_overlay`'s arm SHIP to the decimal** (the line on sc-zenith,
  52.4% both ways).

### 2a. THE BRIEF'S CONTROL CANNOT PASS AS WRITTEN, AND THE ONE THAT MEANS WHAT IT MEANT DOES

The brief: *"a control: a sun of r 0 must deal 0 and price at arm A."* **It cannot**: a foe is
inside while its centre is within `r + ballR`, so a sun of radius 0 is still a disc of 34 at the
contact point, and a struck foe's centre starts ~38 from it. Measured: **r 0 deals 4.3 damage a
cast and reads 26.2%**, against arm A's 14.9 on the same seeds (`s1_rate_r0_2207`). And a sun that
deals 0 and applies 0 smite is not null either: **22.2%**, because `apply("smite", 0)` refreshes
the clock on the stacks the blade already put there (`Fighter.apply` sets `cur.t = def.dur`
before it adds anything). That is a real property of this tick, not a fault in it.

**The control that tests what the brief meant** (that nothing but the sun's feed moves the
fight) is a sun that sets the frame it comes up (`--set dur=0`): the cast, the arming, the break
and its beat all run, and nothing is ever inside. **14.1 / 15.0%, pooled 14.6%, against arm A's
15.6%** on the same seeds (`s1_rate_dur0_*`). The machinery is inert; the sun's feed is the relic.

## 3. Stage 2: the blade — 10.4 CONFIRMED

The brief: confirm 10.4 wide on 151 (10.4 / 11.2); it stays unless the stage-1 relic sits
outside the tier. **10.4 → 48.9% (1360), 11.2 → 55.4 / 52.1, pooled 53.8%**
(`runs/build/s2_blade11.2_*`). The stage-1 relic is 1.2 under stage 0's arm D, inside the tier,
so **the blade stays 10.4** and no link is written. Parity with the sparks (57.1% on 151) would
want about 12; not taken (design §3).

## 4. Stage 3: picture, voice and the tick's marks — `sc-sunrise-fx.html`

`sunrise_build.py --stage 3 --src ../02-chain/sc-sunrise.html --out ../02-chain/sc-sunrise-fx.html`:
14 anchored edits. Design §4.1 and §4.2 as written; the two picks that are Code's (the rim's
crossing flare, the arming smear) are drawn and named where they are drawn.

### 4a. The picture, as built

- **The sun**, in the WORLD pass right after the arena (where `drawDawn` sat), under every
  emissive layer and both balls, clipped to the live hall, hung off the fighter and never
  `m.ultFx`. Its own palette, `SUNLIGHT` (core `#FFF6E2`, gold `#FFD98A`, amber `#FFB347`), used
  nowhere else. Read off the live `ultSunrise` with `tickSunrise`'s own radius, so **the rim on
  screen is the boundary the tick tests** (the foe burns while its shell touches the light):
  - the **rim**: 3 units of gold at 0.8, shimmering ±0.1 at 1.2 Hz, and a 10-unit halo outward
    cut out of the path (§4.1b's hole);
  - the **core**: r 14 of core white at 0.9; **ten rays** of amber at 0.22, tapered, 110-170 long
    (never past 0.85 of the rim), turning 0.15 rad/s, their length breathing at 0.6 Hz;
  - the **wash**: gold 0.35 at the core to amber 0.20 at the rim, source-over;
  - **24 embers** drifting up through the disc (shellHash on the index, no RNG).
- **Armed**: a gold edge-light along the blade's inset edge (not the axis: the sanctified fuller
  is pierced down it), breathing 1.5 Hz between 0.45 and 0.8, and **the smear** (Code's pick):
  the blade's own sweep over its last ~0.11s, off the tip history the swing ribbons keep, gold to
  0.25. World pass, over both fighters, occluded by the foe's shell as the blade is. Nothing on
  the floor while armed.
- **The break**: the flash at the hit point, core white, r 0 → 70 in 0.2s, gone by 0.3s — the
  only `lighter` mark, drawn in the emissive pass over both balls **and cut out of both** (4c).
- **A tick** (every one): the gold number (`float(foe.x, foe.y - 50, 2, gold, 24)`), a 2-unit
  gold ring on the shell at R + 4 fading over 0.2s, and the tick's voice. SMITE on the first
  tick of each stretch inside. Between ticks the line's twelve motes rise off the foe, gold, at
  1.5x their alpha. **The foe outside gets nothing.**
- **The crossing flare** (Code's pick): where the foe's shell crosses the rim, a 60-unit arc of
  the rim flares to 1.0 over 0.15s.
- **Sunset**: the rim falls to the core over 0.5s with the wash, the core winks out 0.15s after;
  0.3s when a new dawn replaced it; the sun that is up at match end sets too.
- **Every mark that lives a set time is stamped on the MATCH clock.** The presentation clock runs
  twice a normal step and once a frozen one, and every break opens with the blow's own hit stop,
  so a flash aged on it outlived its 0.3s by half the freeze. The match clock runs through a hit
  stop; the flash is now gone at 0.300-0.308s, every break.

### 4b. The voices (`tools/sunrise_voice_lab.py`, levels solved against a blow)

Rendered through the shipped chain in an OfflineAudioContext against the `hit` voice at the
blade's own 10.4, loudest 50 ms (the line's measure), the noise seeded; **the lab renders exactly
the builder's text**, so the two cannot drift. All five bounds land: **the arming -16.0 dB**
(A3 → B3 → C4 held, the steps at 1.5s and 3s of arming, one strike a quarter second of the
arming's own clock, in phase); **the bell -4.0 dB**, modes 1 : 2.4 : 4.1 on 880 Hz with a 30 ms
mallet, peak at 6.6 ms, audible 830 ms; **the shimmer -20.0 dB** (A4 + E5 on a 1/220 s grid, a
strike every half second of the sun's clock); **the tick -10.0 dB** (1.2 kHz, 40 ms over 660 Hz,
60 ms: the shimmer's own top note); **the sunset** E5 re-struck in phase for 0.4s, -34 dB about
400 ms after. **The hum STOPS on the break: 0 strikes after it.** The line's steps are gone.

### 4c. Stage 3's gates

- **engine_ab sc-sunrise → sc-sunrise-fx, ALL 35 WITH Dawnbringer, n=6: 3570/3570 identical**
  (`runs/build/s3_engine_ab35.txt`). Picture, voice and marks move no fight.
- **sunrise_probe: 16/16** (`runs/build/s3_probe.txt`), the fight statistics identical to stage
  1's to the last digit. Counted at the call over 408 fights: **12,206 ticks, each with its
  number, its shell flash and its voice, and no frame without a tick carrying any of the
  three** (1,076,803 quiet frames); 13,313 hum strikes on their clock and step, none after a
  break; **1,294 bells for 1,294 breaks**; 17,044 shimmer strikes; **964 sunset voices for 964
  clock sunsets**, none on a death. Every voice renders audibly alone.
- **shell_identity: 194/194 identical** (app Chromium 152 against headless 151, `SWB_GAME`, the
  pointer not moved; the json restored to sc-leaf's afterwards). 194 and not 200 because the
  app's sweep skips mirror pairings, and at 35 relics six of its 200 land on one.
- **chain_audit**: sunrise_build relic and tip sc-sunrise-fx **24/24**; sc-sunrise →
  sc-sunrise-fx **10/10** (stage 1's inserts survive stage 3 -- after a fix: stage 3 first
  REWROTE stage 1's cast line and the audit, correctly, called the insert lost; the arming's
  clock is its own line now); corollary_build sc-corollary-c14 → sc-sunrise-fx **25/25**;
  morningstar_build's stages 1-4 all survive (its stage-6 rows belong to `sc-zenith-fx`, a
  sibling of this branch). **The line's own inserts are gone from this tip on purpose** —
  `dawn_build`'s audit would report them lost, and that is the retirement.
- **tip_audit**: passes, as on sc-zenith.
- **render_ab**: the other relics' pairs (paradox:heartwood, twinshade:lastlight,
  bulwarden:vinesower, axiom:grudgebearer, 6 frames each) **24/24 pixel-identical** from
  sc-sunrise AND from sc-zenith (retiring the line moved no one else's picture); **the control,
  dawnbringer v grudgebearer 4242 at four frames inside a sun, 0/4 identical**, as it must be.

### 4d. THE PICTURE'S GATES — `tools/sunrise_sheet.py`, legibility FIRST: 12 of 17, every red measured

Real fights, 540x960, the shipped renderer, shake zeroed and Math.random pinned per draw, from
two frames that differ only in the mark (v88 §6c). Dawnbringer against a runic foe
(Spellbreaker), the white Aureole and Grudgebearer; the bloom on six foes, both sides, 180 hold
frames. `runs/build/s3_sheet*.txt|json`; the filmstrip is `05-reference/v99/sunrise-states.png`.

```
                                           spellbreaker   aureole     grudgebearer
L1 the wash over the bare floor  (>= +0.15)    +0.187        +0.179       +0.182      PASS x3
L2 the rim: band luma            (>= 0.50)      0.769         0.687        0.771
   the step, worst angle, 7 frames (>= 0.12)    0.126         0.116        0.109      PASS, FAIL, FAIL
   the step, median                             0.13-0.14     0.13         0.13-0.14
L3 the rays |dL| / cover of r60-110            0.079 / 10%   0.084 / 16%  0.084 / 16%   PASS x3
L4 the tick's "2" |dL| vs the echo's "12"      0.235/0.282   0.278/0.251  0.253/0.275   FAIL, PASS, FAIL
L5 the flash gone by 0.3s of match time        0.300-0.308s, 28 breaks                   PASS
L6 the armed edge-light                        762/762 armed frames, 0/2607 others       PASS
B1 the sun's share of the bloom  (<= +0.02)    mean -0.00001, max +0.00005               PASS
B2 the sun never takes a disc over 0.90        5 of 400 flash ball-frames (see below)     FAIL
B3 the sun paints no ball, and is not bloom    disc change max 0.0018 on and off;         PASS
                                               the wash the same chain on and off
```

**L2, THE RIM'S STEP, IS THE DESIGN'S NUMBERS AGAINST THIS HALL'S FLOOR.** The step is the sun's
own light across the rim (the frame minus the same frame without the sun: a real fight puts
other light just outside the rim, and raw luma read it as the rim failing, down to -0.39). Where
the floor is the hall's near-black the step is 0.13-0.14; where the hall's own art brightens the
floor (the pentagram, its rings, the centre's glow) the design's 0.20 of amber at the rim can
only add `0.20 x (0.735 - floor)`, and the worst angles read 0.109-0.119. **The wash's alpha is
the design** (brief §2, stage 3), so it was not moved: **0.23 at the rim would clear every
measured angle** (0.109 x 1.15 = 0.125; 0.22 lands the worst one on 0.120). Rick's and Cowork's.

**L4, THE NUMBER, IS THE DESIGN'S COLOUR ON THE DESIGN'S WASH.** A tick only happens inside the
sun, so its number always sits over the amber wash, and gold on amber is lower contrast than the
echo's pale blue on the same wash. SIZE IS NOT THE LEVER: at 30 the "2" still reads 0.263
against 0.282 on the runic foe, and this engine sizes a number by its damage (the echo is
`22 + dmg / 2`), so a big "2" would read as a big hit. Kept at the design's gold and 24. The
fix is the colour (the core's white reads everywhere, but the design keeps white for the core)
or accepting it; Rick's eye on the clip decides it.

**B2, THE FLASH.** Drawn over a ball, the flash lifted a struck ball's disc by up to +0.31 and
past 0.90 on 94 ball-frames it was not already over, so **it is cut out of both balls** now (one
clip per ball: two holes in one nonzero path fill where they overlap). What is left is the
bloom's spill: 20 of 400 flash ball-frames end over 0.90, and in **15 of them the ball is over
0.90 without the flash** (the blow's own hit flash: the break IS a blow); in the other 5 the
flash tips a ball already at 0.889-0.899 over, by at most +0.020. The spill barely moves with the
flash's brightness (+0.20 max at 0.55, +0.19 at 0.22 -- the bloom adapts to the frame), so the
brightness is kept; the design's own next knob is the flash's radius (70). A strict red, reported.

**L6 AND THE HOLD'S DISCS ARE THE MEASURE'S, NOT THE BUILD'S, AND BOTH WERE FIXED IN THE TOOL
BEFORE THE READINGS ABOVE.** Three armed frames drew no tell because the blade pointed into a
wall and the tell's whole span lay past the hall's edge; they are not counted. A hold frame's
disc of 0.932 is a ball's own (over 0.90 with the sun stubbed too), and the gate charges the sun
only with what the sun did.

### 4e. THE CARRY IS READY, AND IT WAS TESTED

DESKTOP-DERRAFT has since built Zenith's stage 6 as `sc-zenith-fx` on the same link, so the
batch line is forked at `sc-zenith`. `sunrise_build.py` was first written with its cuts ending at
"whatever comes next", and Zenith's stage 6 put its own code right after three of the line's
spans: carried onto `sc-zenith-fx`, the sha pin REFUSED (the design of it) instead of cutting
Zenith's clock. The cuts now end at the line's OWN last text (the same six sha pins: the line's
spans are byte-identical on both tips), and the draw call anchors on two lines instead of
three. **From `sc-zenith` the builder reproduces `sc-sunrise` and `sc-sunrise-fx` byte for byte**
(`b84435a83eb5cce7`, `740b05d4bb6e7001`); **onto `sc-zenith-fx` both stages build and parse**
(`73e1a5f6d6ae8b14`, `2cdb93ba5baf8cc3`, scratch only -- not written to the chain and not gated).

## 5. Stage 4: the clip and the sheet — Rick's gate, the one no tool runs

`_sunrise_pick.py` scores a sun on the brief's whole sentence -- a short arming, the break in
frame, the foe crossing the rim at least twice, a clock sunset -- **and a clean opening**: the
first pick (Axiom, seed 99138) opened on the PREVIOUS sun still setting, the wrong dawn for a
viewer meant to work the mechanic out cold, so a sun whose lead-in has another sun on screen is
not picked. The pick: **dawnbringer v heartwood, seed 99138**: cast 48.28, arming 0.78s, the
break at 49.07, the set at 58.59 by its clock; 14 ticks, the foe inside 73.6% of the sun's
life and crossing the rim 18 times -- the counterplay on screen as often as the burn.

    python cinema_clip.py --game ../02-chain/sc-sunrise-fx.html --a dawnbringer --b heartwood       --seed 99138 --at 47.28 --window 12.71 --end-at-window --fps 60 --w 540 --no-card       --out ../07-shorts/v99/daybreak-sun.mp4

**Two opt-in flags were added to `cinema_clip.py` for it**, and neither changes a clip that does
not ask for it:
- **`--no-card`** sets the HUD's `ULTBAR.tip` off: the HUD fades an ultimate's own card text in
  for the five seconds before it fires, and the brief's gate is that Rick watches with the card
  hidden. The filmstrip is drawn the same way.
- **`--end-at-window`** stops the capture when the MATCH clock passes `--at + --window`. Without
  it a window is capped at 2.6x its length in VIDEO seconds, which assumes the director slows
  the window down; this one it barely touched, and the first cut ran 41s of video over 38s of
  fight, a second sun included. **v97's own clip (`--window 12.56`, 38.6s of video) very likely
  ran past its window the same way.**

**The filmstrip**: `05-reference/v99/sunrise-states.png` (`sunrise_sheet.py --only sheet`),
dawnbringer v grudgebearer seed 5500: armed / the break / +0.5s / +2s / +5s / sunset, card
hidden. Rick sees it with the clip.

## 6. Open decisions (Rick's; the build holds the design's numbers until he rules)

1. **The card** (design §6.1): the 71 as built, or one of the two alternatives.
2. **The strength** (§6.2): as priced (48.9% built at 10.4), or the tick to 3 (+10 in the lab).
3. **The colour** (§6.3): amber/gold/core as built, or the school's white.
4. **The heal** (§6.4): not taken.
5. **Code's two picks** (§6.5), on the numbers: the crossing flare and the arming smear are both
   IN. Overrule either and it is one draw call.
6. **THE THREE REDS, each one number of the design's** (§4d): the rim-side wash 0.20 → 0.23
   clears the rim's step on the hall's brighter floor; the number's gold on amber reads under the
   echo's on two foes of three (the colour or the size); the flash's radius 70 is the design's
   next knob for its bloom tipping a hit-flashed ball past 0.90. None was moved, because each is
   the design's to move -- and Rick's eye on the clip is the gate those numbers exist to serve.
7. **THE FORK**: this branch and DESKTOP-DERRAFT's (`sc-zenith-fx`, Ironwood next) meet by
   re-applying one onto the other. `sunrise_build.py --src <their tip>` is tested onto
   `sc-zenith-fx`; which way round, and when, is the carry session's call.

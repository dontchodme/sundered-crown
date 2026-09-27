# v97 — DAWNBRINGER / DAYBREAK, BUILD. STAGES 1-3 BUILT AND GATED; THE CLIP IS WITH RICK ("you pick i overrule"). The app pointer waits on him.

Claude Code on **DESKTOP-DERRAFT**, claimed 2026-09-27 01:35 UTC (`CLAIMS.md`, the BUILD row
under Daybreak's). The input is `06-docs/v86/dawnbringer-daybreak-redesign-v86.md` §5 with its
§7 rulings, and nothing else (rule 0). Builder `tools/dawn_build.py`, probe
`tools/dawn_probe.py`. (v89-v96 are the staff row's, claimed by Cowork, hence v97.)

```
sc-corollary-c14.html   the base: the chain tip (sc-leaf + Axiom / Corollary stages 1-6)
  -> sc-dawn.html          stage 1  the dawn; the sparks out     dawn_build --stage 1   fa8703a2e143f59d
                           stage 2  the blade                    10.4 CONFIRMED at charge 14 -- no link
  -> sc-daybreak-fx.html   stage 3  picture, voice, the field out   dawn_build --stage 3   1aac87b67fa2a495
```

## 0. What this build stands on

**The base is the chain tip**, asserted by the builder: the Winnowing's rung stop, Corollary's
`echoShown` and its stage-5 apply fix. (The claim said `sc-corollary-fx`; Corollary's stage 5
landed before stage 1 was built, so the tip moved to `sc-corollary-src`.) The v86 pricing was
on `sc-trunk`; since then Axiom's ultimate changed and Thornshear's kunai lost their hit stop,
which reaches 2 of Dawnbringer's 33 pairings. Stage 0 below is run on this base, and the gates
read against it.

**Rick's rulings** (v86 §7): **charge 16** (the doc did not state it; 16 is what it was priced
at, and the shipped Daybreak was 14). The heal and the line speed are built **as written**: no
heal, and the full floor-to-ceiling rise.

**The readings the build had to make** (in `dawn_build.py`'s docstring):
1. **The tick's cadence is the lab's:** a 0.5s cooldown that runs through the whole window
   and fires on the first lit frame it is clear.
2. **`apply`'s source is a side letter.** §4 and the lab pass the Fighter, but the engine's
   contract is "a"/"b", and smite ticks damage, so a fatal smite tick is attributed by it.
3. **"No beat" for a tick, except the tick that KILLS**, which files its own `fatal` hit beat.
   That is the engine's standing rule for every side-channel kill (Scour's ticks: "ticks file
   nothing, the fatal one does"), and without it a fight won on the dawn has no killing blow.
4. **H is `CONFIG.arena.h`**, the full hall, as the lab reads it. After the hall starts
   closing, the line starts below the visible floor for up to ~1.4s; the lab priced exactly
   that.

**The clock** is the window tickers' (it stops through a hit stop), as for Corollary. The lab
counted every step.

## 1. Stage 0: the control on 151, on sc-corollary-src

`ult_overlay.py --relic dawnbringer --mech overlays/dawn.js --seeds 20`, seed0 2207 and 2317,
660 fights an arm a block:

```
arm                          published 141 (330)   151: block 1   block 2   pooled (1320)   lit    ticks  dmg / cast
A     no ultimate            13.6%                  14.8           17.0      15.9
SHIP  the sparks             57.0%                  58.0           57.9      58.0
B     the dawn (the lab)     54.8%                  54.5           52.4      53.5           60.3%  9.91   19.8
```

The control reproduces within the batch's tier; the dawn's mechanism reproduces to the digit
(published: lit 61%, 10.0 ticks, 20.0 damage a cast).

## 2. Stage 1: the dawn, the sparks out — `sc-dawn.html`

`dawn_build.py --stage 1 --src ../02-chain/sc-corollary-src.html --out ../02-chain/sc-dawn.html`:
src `82433ea61c9701b6`, out `a3fde3a7869fde65`, +3261 characters. Five anchored edits:
- Dawnbringer's ult block (`kind:"dawn"`, charge 16, dur 8, tick 0.5, tickDmg 2, smite 1, the
  doc's 72-character card);
- `ultDawn`/`dawnTally` on the fighter;
- the `kind === "dawn"` cast branch, which opens the window and resolves nothing;
- `tickDawn` beside `tickEcho` among the window tickers;
- `tickDawn` itself.

**The sparks are out by construction.** No relic carries `kind:"radiant"` any more (the builder
refuses otherwise), so nothing sets `ultRadiant` and the spark spawn in `resolveHit` is
unreachable. The spark machinery stays for Lastlight's Harrowing.

**Probe, `dawn_probe.py --game ../02-chain/sc-dawn.html`: 9/9** (396 fights, Dawnbringer on both
sides). Per cast: 9.95 ticks, 19.9 damage, foe lit 59.5% of the window, 2.83 casts a fight
(the lab: 3.3, the frozen-clock effect). 14 killing ticks, each with its fatal beat; 182 wards
broken by a tick. Dawnbringer threw no spark.

### 2a. At charge 16 the dawn came in 10 under the sparks, and the reason was the clock

The first build of stage 1 (on sc-corollary-src, charge 16; `runs/charge16_*`) read **49.8 / 46.8,
pooled 48.3%** at blade 10.4. That is 5 under the lab's arm B and 10 under the sparks. The
probe showed why: **2.83 casts a fight against the lab's 3.3.** The blade curve at charge 16
(pooled 1320): 10.4 → 48.3, 11.2 → 51.0, 12.0 → 58.9, 12.8 → 63.7. Parity with the sparks
would have taken ~12.0.

Corollary had shown the same thing (v88 §4), so it was put to Rick once, for the batch: the
lab's charge counts hit-stop freezes and the engine's does not. Measured before asking, on
scratch copies at charge 14: Daybreak 52.5% at 10.4 (the lab: 53.5%), Corollary 40.0% at 7.42
(the bolt: 40.2%). **Rick, 2026-09-27: "Use the game's equivalent"** — the lab's 16 is the
engine's 14, and the weapons stay as designed. Corollary took it as its stage 6
(`sc-corollary-c14`), and this build was rebuilt on it at charge 14.

### 2b. Stage 1 at charge 14 — `sc-dawn.html` (the link of record)

`dawn_build.py --stage 1 --src ../02-chain/sc-corollary-c14.html --out ../02-chain/sc-dawn.html`:
src `3fc6ec27a5298615`, out `fa8703a2e143f59d`, +3261 characters. The same five edits at
charge 14.
- **Probe: 9/9** (`runs/dawn1_probe.txt`). 9.88 ticks, 19.8 damage a cast, foe lit 58.9%, and
  **3.30 casts a fight: the lab's exactly.**
- **engine_ab sc-corollary-c14 → sc-dawn, the 33 others, n=8: 4224/4224**; Dawnbringer + 8:
  64/288 differ (its 8 pairings × 8 seeds, the pass).
- **The relic at 10.4: 53.2 / 51.2, pooled 52.2%** (`runs/dawn1_built_*`), against the lab's
  arm B at 53.5%. In tier.

## 3. Stage 2: the blade — 10.4 CONFIRMED

v86 §5: "confirm 10.4 wide on 151". At charge 14 the built dawn reads 52.2% against the priced
arm B's 53.5%, inside the tier, so the blade stays at 10.4 and no link is written. (The design's
own "parity with SHIP ±3" does not hold even in its lab on 151: arm B 53.5 against the sparks'
58.0. Rick's ruling is to land where Cowork priced, and it does.)

**verify --n 40 on sc-dawn: 10/13** (`runs/verify_dawn.txt`). Dawnbringer 53.8% (54.2% before
the build); every relic in 30-70% (Heartwood 35.0 .. Gloamwire 63.9). The reds are the two
clock bands and sc-leaf's own Axiom vs Thornshear 0/40.

## 4. Stage 3: picture, voice, the sparks' field out — `sc-daybreak-fx.html`

Rick, 2026-09-26: **"you pick i overrule"**. Every choice v86 §4 left open was picked on a
measurement (`tools/dawn_voice_lab.py`; the picture lab's scripts are in the session scratch,
and its numbers are here). One clip goes to Rick.

`dawn_build.py --stage 3 --src ../02-chain/sc-dawn.html --out ../02-chain/sc-daybreak-fx.html`:
out `1aac87b67fa2a495`, +8474 characters, 14 anchored edits (2 voice, 12 picture). The sparks'
field spec came out of BOTH copies of `src/render/fx.js` (stamp `060d6c89f9c3451d` →
`28fc58641370a1a9`).

### 4a. The picture

- **The wash:** sanctified glow #FFFFFF at alpha 0.10, source-over, from the line to the floor,
  **drawn in the WORLD pass** right after the arena, under every emissive layer and both balls,
  and clipped to the live hall.
- **The line:** a 4-unit band at 0.6 in sanctified core, and a 12-unit linear horizon above it
  from 0.6 to 0.
- **The clocks:** the brightening is a 0.3s ease-out at the cast; the close fades over 0.5s, and
  the same fade runs at match end.
- **The foe in the dawn:** 12 faint motes drawn with shellHash (not spawnFx) rise from its upper
  disc under its shell. It gets the ordinary SMITE tag on the FIRST tick of each lit stretch (2.5
  a window, not the 10-14 ticks), and its own smite bolts carry it between tags.
- **Why world and not emissive, measured:** the line drawn in the emissive pass read stronger,
  but its bloom share was +0.018 and it whitened Dawnbringer's disc from 0.644 to 0.802 when the
  line ran behind the ball. That is §4.1b again.

The numbers (headless Chromium 151, 540x960, chain on):
- **Legibility:** band luma 0.57-0.64 over a bare floor of 0.07-0.14; the wash +0.084..0.090
  signed luma, the SAME with the chain off, so none of it is bloom.
- **THE BLOOM GATE PASSES:** 180 frames at D.t 7.90-7.92, the whole hall lit, six foes, both
  sides. Arena-mean lift +0.0012 (max +0.0034); Daybreak's own share mean -0.00001, max
  +0.00001, against the gate's +0.02. Control: the same wash in the emissive pass lifts +0.071,
  above the Harrowing's +0.0628, and FAILS as it must.
- **THE BALLS ARE NOT TOUCHED:** disc change max 0.0000 on the foe and on Dawnbringer, the white
  Aureole included. The white Aureole at 7.9s reads disc 0.819 against its surround 0.581.
- **Frame cost** (Electron 44, RTX 3070): drawDawn 0.28-0.36 ms.
- **Sim identity:** 8 fights, a per-step hash compared up to the kill, identical; a control that
  nudges one velocity fails on all 7 Dawnbringer fights.

**Retired:** the sparks-era pool (drawUltUnder), the corona (drawUltOver), and the old banner
horizon (it sat 5-170 units from the real line and read brighter than it). **The HUD sigil's
orbiting shards come out** ("a spark field IS the mechanic", and no longer). **The sparks' cast
burst comes out of both copies of fx.js, with no replacement.** Measured left in: 1350 particles
drawn AT THE FOE on the cast frames, whitening its disc to 0.87-0.91. That is §4.1b's erased
ball, on the foe. The dawn's own motes ride a moving foe for 8s, which the one-slot field cannot
carry, so they are drawn. The generic ultFx cast record stays (life 1.6) and draws nothing.
**Kept:** the spark machinery (Lastlight), and `b.w === "dawnbringer"`'s banner letters.

### 4b. The voices

- **Cast and steps: "a slow swell rising over the whole 8s (re-struck tones stepping up a scale,
  one per second)": HANDOFF** (of five). One octave of C major, C5 → C6 (diatonic to the score's
  A minor). Step 0 is the cast (fireUlt's own call). **Steps 1-7 are played from `tickDawn` as the
  WINDOW's clock crosses each second**, so a hit stop holds the note and a death stops the rise.
  Each step is re-struck in phase and handed to the next degree. The window's seconds run a median
  1.16s and p99 1.62s of match time (hit stops freeze its clock), and a note that held exactly one
  second (HELD) passed the nominal case and failed every real window. +9 dB over the eight steps.
- **Close: "the top note held and released": STOP** (of five). It picks up step 7's strikes in
  phase, holds 0.5s (the wash's own fade) and releases in 380 ms. It plays only when the window
  closes by its clock: never on a death, never after the fight is over.
- **A tick:** "nothing new (smite's)". No smite voice exists, so ticks are silent.
- **Levels:** step 0 is -16.8 dB under a blow and +3.4 dB over the wall tick; the top step is
  -8.7 dB under a blow. The cast is QUIET by the spec's own word ("a slow swell" starts low). The
  lab's level window allows +2.6 dB more if Rick wants it.
- **Checked:** on 132 real fights the voice row is identical in the sim; steps 1..7 play once
  each, in order, on their crossing frame, and there is exactly one close per clock close.

**A TOOLKIT FINDING for CLAUDE.md §4.5.** `_tone`'s re-strikes are NOT phase-coherent above
~500 Hz: it sets the frequency with an event AT the strike, and Chromium starts the oscillator's
phase from the param's 440 Hz default, up to ±177° off at 1046 Hz. Setting `.frequency.value = f`
on the returned node puts every strike within one sample. HANDOFF does this; without it (the
lab's RAW control) the top step is 10 dB down and the swell is gone. Corollary's MIRROR echo
re-strikes at 46-190 Hz and passed its own gates, but it was not re-measured for this.

### 4c. Stage 3's gates — every one able to fail

- **engine_ab sc-dawn → sc-daybreak-fx, ALL 34 WITH Dawnbringer, n=6: 3366/3366 identical**
  (`runs/stage3_engine_ab34.txt`). Picture, voice and the removed field move no fight.
- **dawn_probe: 11/11** (`runs/stage3_probe3.txt`).
  - [10] steps 1-7 on the window's clock, in order, and one close per clock close, none on a
    death (8394 step voices, 1081 clock closes).
  - [11] cast, top step and close each render audibly ALONE, and the old chord and bell is gone
    from the synth (a check that reads TRUE on sc-dawn).
- **render_ab:**
  - the other relics' pairs (paradox:heartwood, twinshade:lastlight, bulwarden:vinesower,
    axiom:grudgebearer) print **24/24 pixel-identical**;
  - the control, dawnbringer v grudgebearer 31337 inside a window, prints **0/4 identical**.
  - render_ab's own default pairs include ironhail:dawnbringer:4412, which now differs by
    construction.
- **shell_identity on sc-daybreak-fx** (`SWB_GAME`, the pointer not moved): **200/200**.
- **chain_audit:**
  - dawn_build: relic and tip sc-daybreak-fx, 17/17; sc-dawn → sc-daybreak-fx, 6/6;
  - corollary_build: sc-corollary-c14 → sc-daybreak-fx, all 25 survive.
- **tip_audit: 1**, as before.

### 4d. The clip (Rick's to overrule)

`_dawn_pick.py` scores a window on the whole of §4. It must close by its clock, which is the only
way to hear all eight steps and the close, with ticks, lit share and line crossings. The pick:
**dawnbringer v redflail (Threshmaw), seed 97138**, cast at 15.00, 14 ticks, the foe lit 77% of
the window and crossing the line 5 times.

    python cinema_clip.py --game ../02-chain/sc-daybreak-fx.html --a dawnbringer --b redflail \
      --seed 97138 --at 13.80 --window 12.56 --fps 60 --w 540 --out ../07-shorts/v97/daybreak-window.mp4

38.6s (the director's slow motion over a 12.5s window; cinema_clip's "no ending" warning is
because the fight runs on to 44.4s past the window), AAC mean -22.8 dB, max -0.6 dB. Sent to
Rick 2026-09-27. Threshmaw's own Bloodmill fills part of the window with red spikes, so the
sample is busy.

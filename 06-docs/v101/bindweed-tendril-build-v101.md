# v101 — BINDWEED / TENDRIL, BUILD. STAGES 1-6 DONE: stage 1 is arm A to the fight; the mechanism is the lab's; the win rate runs over the lab by the window clock (measured); the build's knob moved and said (turn 4 -> 3) and the blade sits at the crossing, 18 (48.5% both sides); the vine drawn and voiced, gated, and on the chain (`sc-tendril-fx`, carried onto `sc-onslaught-fx`). Clip with Rick; the app pointer waits for him.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 06:12 UTC (`CLAIMS.md`, the BUILD row under the
verdant flail's). Input: `06-docs/v68/BINDWEED-BUILD-BRIEF.md` + `verdant-flail-design-v68.md`, and
nothing else (rule 0). Builder `tools/bindweed_build.py`, probe `tools/bindweed_probe.py`, runs in
`runs/`. **A NEW relic: the 38th built** (the brief's "35th" is the cell number).

```
sc-onslaught-b23.html   the base: the chain tip (Portcullis stage 5, carried onto Canopy's stage 6)
  -> sc-bindweed.html    stage 1  the relic, ult stubbed (charge 1e9)          26f311f8c7feebb5
  -> sc-vine.html        stage 2  the seek and the growth                      ae3b70d586461897
  -> sc-bites.html       stage 3  the bites, biteDmg 0 -> 2, bitePer 0 -> 1     b5eeec40b34e943f
  -> sc-tendril.html     stage 4  the root, rootPer 0 -> 0.3                    f186dbc770ecdade
  -> sc-tendril-t3.html  stage 5  turn 4 -> 3 (the build's knob), blade 19 -> 18  5a6216e3b629fad4
sc-onslaught-fx.html   (Portcullis stage 6, landed first)
  -> sc-tendril-fx.html  stage 6  the picture and the voice                     eea0cde5536955b3
                                 (built and gated in scratch on sc-tendril-t3 as 5e2cc29a1178bef4)
```

## 0. What this build stands on

- **The relic** is Gravemourn's flail profile, the lab's donor (reach 96, width 22, artW 52, spin
  2.2, chain, mass 3.6), at the lab's blade 19 until stage 5; aff verdant, onHit entangle 2, and the
  brief's 70-character card. The builder asserts the donor's profile, the five verdant channels
  and the verdant flail head's route (`_fhGrown`, never drawn by a shipped relic).
- **The charge is 14:** the brief's 16 on the lab's clock, converted (Rick's batch ruling).
  Measured for this fighter on arm D (a scratch copy of `vine_price.py` that counts frozen steps,
  660 fights, `runs/s0_census_2207`): 11.7% of the lab's steps are frozen (16.6% inside windows), so
  the lab's 16 is the engine's 14.1, and 14.
- **The lab is `tools/vine_price.py`**, not `ult_overlay` (the brief's own stage-0 command). It
  plays the relic as side A against the 33 foes of the design's roster.
- **Readings** (in the builder's docstring):
  1. **The chain's spin is 0 for the window, not only its drive.** The lab zeroed the weapon's spin,
     which zeroes the drive and leaves the extension's normaliser at its 0.5 floor, so a small sway
     throws the head out. The brief's "drive = 0" and "the extension untouched" are both that. The
     build zeroes `spin` in tickWeapon for this fighter and never writes the shared weapon.
  2. **The vine keeps turning while stunned** (the brief leaves it to the build; the lab turned it).
     15% of window frames are stunned frames (the probe).
  3. **Reach returns to 1 at the close** (design §7 and the lab). The brief's "eased back over the
     wither" is the wither's picture, not the hit box.
  4. **No per-bite reach kick.** The lab's arms C and D add 0.05 of reach a bite; the prose has
     none. Priced below: the lab without it reads 56.5 against 53.7.
  5. **Either death ends the window and roots nobody** (the brief); the lab closed only on its clock.
  6. `apply`'s source is a side letter (the engine's contract; entangle has no reader of it).
  7. **A bite that kills files its own fatal hit beat** (Rick's standing rule for a side-channel
     kill; the brief's stage-6 sentence "bites file nothing" predates it). No other bite files one.
  8. The target is the opponent, never a Twinshade shade.
- **Names:** the ultimate's kind is `"tendril"` and its ticker `tickTendril`: `"vine"` is the
  Thicket's live SFX kind and `tickVines` its ticker.
- **The clock:** the window, the turn, the growth, the bite's cooldown and the wither run on the
  window tickers' clock, which stops in a hit stop. The lab ran all of them through freezes (§2).

## 1. Stages 1-4

Stage 1 appends the row after Portcullis with the ultimate stubbed at 1e9. Stage 2 adds
`ultVine` / `vineWither` / `vineTally`, the `kind === "tendril"` cast branch, the seek in
tickWeapon's chain branch (`spin` 0 for the window; the facing turns toward the foe at `turn`
rad/s the shortest way round), `tickTendril` after `tickRam` (the growth toward the foe's rim, the
bite machinery at biteDmg 0 / bitePer 0, the close, the wither, the root at rootPer 0), the cast's
wait on the wither, and charge 14. Stages 3 and 4 flip their numbers.

## 2. Stage 0 and the stages against it — the window clock, measured

`vine_price.py --game ../02-chain/sc-onslaught-b23.html --seek 2 --track 1 --grow-time 0.3
--grow-cap 3.0 --turn 4 --blade 19 --seeds 20 --foes <33>`, seed0 2207 and 2317, 660 fights an arm a
block. The seek+growth reference is `--arms C --bite-dmg 0 --bite-per 0` (the brief's). The built
links run `ult_overlay.py --relic bindweed --arms SHIP` on the same foes and seeds (the same seed
formula and side).

```
                               lab on 151 (1 / 2)   published 141   lab, no kick   lab at dur 9.6   BUILT (1 / 2)                pooled
A   no ultimate                1.4 / 1.1            1.5 / 1.4                                        stage 1: 1.4 / 1.1           identical, fight for fight
C0  seek + growth              40.2 / 40.6          42.6                            54.1 / 54.2      stage 2: 51.4 / 51.8         51.6
C   + the bites                48.9 / 50.0          48.8                            60.9 / 62.7      stage 3: 60.8 / 60.5         60.7
D   + the root                 53.2 / 54.2          54.4 / 55.8     55.5 / 57.4     65.5 / 67.4      stage 4: 63.9 / 65.0         64.5
```

Lab mechanism on 151 (arm D, no kick): 3.2 casts; 6.6 bites, 13.3 damage and 0.90s of root a cast;
the foe at 3.08 stacks on a window frame; touch 17.8%; 11.7 blows in windows and 5.4 outside.

**The built relic reads ~11 over every lab arm from stage 2 on, and the lab run at the engine's
window reproduces it** (the "lab at dur 9.6" column, no kick: 54.2 / 61.8 / 66.5 against the built
51.6 / 60.7 / 64.5). The engine's 8s are 8 seconds of the window tickers' clock, and 16.7% of window
steps are frozen, so a window is ~9.6s of match time where the lab's was 8 step-seconds. The design's
own prices put a second of window at ~6 points ("window 6s reads 41, 10s reads 65"). This is the
clock v99 §4 and v100 §2 measured on Canopy and Onslaught; here it pushes up, through a longer hunt
(13.6 blows in windows against the lab's 11.7). The mechanism is the lab's; nothing is mis-built.
Stage 5 prices it with the brief's knob.

## 3. The probe (`bindweed_probe.py`, one check per sentence, read inside the hooks)

- **sc-vine (stage 2): 9/9**: the seek rebuilt exactly on every window frame (15% of them stunned),
  the drive 0 (the head's tumble rebuilt with drive 0), spin as ever outside the window; the growth
  exact both ways; 13.8 blows in windows and 4.8 outside; growth peak 2.27 a fight.
- **sc-bites (stage 3): 9/9**: 6.47 bites and 13.0 damage a cast; touch 15.8%; 3.08 stacks.
- **sc-tendril (stage 4): 9/9**: 6.55 bites, 13.1 damage and 0.85s of root a cast; 96% of clock
  closes root; 21 killing bites, each with its fatal beat.
- **sc-tendril-t3 (stage 5): 9/9**: 3.28 casts; 6.06 bites, 12.1 damage and 0.85s of root a cast;
  94% of clock closes root; 16.1% of window steps frozen.
- **Controls** (`runs/probe_mutants.txt`): the seek gated on stun fails [2]; a Fighter as the
  bite's source fails [6]; the growth 1% fast fails [3]; a root at a death close fails [8]; the
  bite cooldown 10% short fails [5]. (1% short does not change a single bite at 120 frames a
  second, so it is not a control.)
- **Stage 1 is arm A fight for fight** on both blocks (every foe's rate identical).

## 4. Stage 5: the turn and the blade — turn 3, blade 18

Both sides (`relic_rate.py`, each seed from both sides; every other relic a foe, 10 seeds a foe a
side, 740 fights a block; seed0 2207 and 2317; `runs/stage5_rr_*`):

```
turn   blade   block 1   block 2   pooled (1480)   side A   side B
4      17      55.8      53.6      54.7            54.7     54.7
3      17      46.4      45.0      45.7            46.2     45.1
3      18      49.1      48.0      48.5            49.2     47.8
3      19      56.6      54.6      55.6            57.6     53.6
```

- **At the designed turn 4, blade 17 reads 54.7**, so the crossing is ~15.5, outside the brief's
  17-19.5. **The brief: "move `turn` inside 3-5 FIRST and say so."** It is said here.
- **At turn 3 the crossing is ~18.2**, inside the brief's "expect 17.5-18.5"; at 3.5 it would fall
  just under 17. Blade 18 is the measured point nearest it: 48.5%, about one standard error under
  50. The built link reproduces the measurement exactly (`relic_rate` on `sc-tendril-t3` with no
  knob set: block 2207 49.1%, every foe and the mean duration the same).
- **The ladder at turn 3 / 18** (40 fights a foe, `runs/ladder_t3.txt`): greatsword 78%, twinblade
  53, warhammer 50, scythe 45, flail 38, bow 23. Worst Aureole 12.5%, Farwarden 15, Gloamwire 17.5,
  Ironhail 20; best Heartwood 97.5, Axiom 92.5, Ironwood 90. The design's greatswords 78.6 hold; its
  bows (37.5) read lower here. **The type spread is item 12/32, Rick's.**

- **engine_ab sc-onslaught-b23 → sc-tendril-t3, the 37 others, n=6: 3996/3996 identical**
  (`runs/engine_ab37.txt`). Adding Bindweed moves no other fight.
- **verify --n 40 on sc-tendril-t3 (38 relics): 10/13** (`runs/verify_t3.txt`). Bindweed 49.7% (side B,
  as verify plays an appended relic); every relic in 30-70%. The reds: the two clock bands, and "both
  sides can win every matchup" on Heartwood v Twinshade 0/40 (not Bindweed's pairing) and Heartwood v
  Bindweed 0/40 -- Bindweed's own lopsided verdant pairing (Heartwood 97.5% in its ladder). Item 12/32,
  Rick's.

## 5. Stage 6: the picture and the voice — `sc-tendril-fx`

Picked on measurements under Rick's "you pick i overrule", by two labs run in parallel (the picture
lab's scratch, `bw_rows.py`, and `tools/bindweed_voice_lab.py`), and built as `bindweed_build.py
--stage 6`: fifteen anchored edits (voice 4, picture 11), byte-exact to the labs' own row files. No two
rows share an anchor, so none is merged; no row's anchor sits inside another's; voice-then-picture and
picture-then-voice write the same bytes. The picture rows alone reproduce the picture lab's stamp
(`ef4bd13fe968d99c`). The sheet is `05-reference/v101/bindweed-picture-sheet.png`; the wavs are
`05-reference/v101/bindweed-*.wav` (gitignored).

**Built in scratch on `sc-tendril-t3`** (38 relics) while other builds ran on the same tip, then
**carried onto the chain** with `bindweed_build.py --stage 6 --src ../02-chain/sc-onslaught-fx.html`
(Portcullis's stage 6 landed first): **engine_ab, the scratch link against the carried one, all 38
relics WITH Bindweed, n=6: 4218/4218 identical** (`runs/carry_engine_ab.txt`). The builder re-applies on a tip that carries other relics: every anchor is a line
of Bindweed's own stages or a shared line that other relics' rows only insert beside (the rune-crack
fallback is re-emitted, the draw calls are `after` rows); the picture lab applied these rows with
Onslaught's picture rows in both orders.

**The picture** (v68 §8.1; every number from the picture lab, headless Chromium 151 at 540x960 with the
post chain on, 67 frames across 10 fights and 7 states, foes white sanctified, dark umbral, ordinary):
- **The cast:** the flail greens haft to head over 0.30s on the presentation clock (so it plays through
  the cast's own hit stop). The haft's steel goes to dark bark (#0D3A1A) with a core seam and a glow
  ridge; each station sprouts its leaf pair and thorn as the green passes; the head (`_fhGrown`,
  unchanged) is wrapped in bramble. Verdant's palette exactly.
- **The vine is drawn on the line the bite tests** (pivot to head), not the chain's slack bow, with a
  2.2-unit living sway pinned at both ends. Measured over 48,592 window steps: the bow would have drawn
  it a median 0.7 units off the tested segment, but more than 8 units off on 2% of steps and 3% of bites.
- **The reach is the only thing that animates the growth.** The leaf scale puts a pair every 12 units
  from the pivot; the leaves stand ~8 units off the axis, which is `vineW`, so a leaf touching the foe is
  a bite.
- **A bite:** four glow thorns with a dark edge flash from the foe's rim at the point nearest the tested
  segment, source-over, 0.12s, no hit stop. It is read off `vineTally.bites` rising, so the sim makes no
  call. The ENTANGLE tag prints its count whenever a bite leaves a different count from the one the vine
  last printed (the first bite, then each step of the climb), one vine tag up at a time, silent at the
  cap of 4, and merged into the head blow's own ENTANGLE tag instead of printing over it (tagging every
  bite, 3.3/s, stacked three tags).
- **The window tell:** a thin core ring at R+2.2 on the caster.
- **The wither:** the chain is drawn grey at its tested rest length and the vine over it on the chain's
  own curve, brown running head to haft (at the haft by 0.3s, gone by 0.4s); the vine beyond the new
  length breaks off as falling stems, each leaf pair drops as the brown passes it. Debris is drawn:
  `shellHash`, no `spawnFx`, no RNG.
- **The root:** four shoots out of the floor (the inset floor) climb the held ball's rim and clench with
  core tips; grow 0.12s, clench 0.1s, dry through the pin's last 30%, fade 0.2s after release. Verdant
  on any ball; in mid-air they are aerial roots (Canopy's precedent). **The runic hexagon is not drawn
  on a ball the root holds** (design open decision 6), and cleanly: `tickTwine` sets a presentation
  marker, `twineHeld`, on the quarry when `vineTally.roots` rises, and `_drawField`'s guard becomes
  `f.pin > 0 && !f.pinFree && !(f.twineHeld > 0)`. `pinFree` is untouched, so `tickStasis` still locks
  the weapon. No other relic pins Bindweed's foe (self-pins set `pinFree`, which already skips the
  hexagon): measured 3,909 held steps, 0 missing, 0 stray.
- **The director:** the root files one write-only `ult` beat at the quarry (Paradox's hold's shape, no
  hit stop), anchored on `T.rootSec += hold;` because the voice row owns `T.roots++;`. The cast's `ult`
  beat is `fireUlt`'s own; bites file nothing new (a killing bite's fatal beat is stage 4's).
- **The silhouette is left as it is:** the resting `_fhGrown` head at the app's size reads |dL| 0.192
  (min 0.141), 3rd of the 7 flails (Morningstar 0.226, Paradox 0.216 above; Threshmaw 0.156,
  Portcullis 0.137, Gravemourn 0.131, Slagheart 0.130 below). The design's "redraw a separate claim"
  stands.
- **The art hangs off the Fighter** (`twine*` fields), never off `m.ultFx` (open item 25). Names are
  `twine*` because the Thicket owns `vine`/`vines`/`tickVines`/`drawVines` and the "vine" SFX kind.
- **Bloom:** the picture's share of the chain's arena lift max +0.0000 (gate +0.02); raw luma it adds
  +0.0037. No ball's disc moves more than 0.0135 (the caster; foes 0.0025-0.0086) and none is erased;
  the white sanctified foe's disc passes 0.90 on 1/33 frames with and without the rows (the body). The
  control (a glow band along the vine and a disc on the foe, lighter 0.35, emissive) lifts +0.0372 and
  FAILS the gate on 10/67 frames, and drives the white foe's disc past 0.90 on 19/20.
- **Legibility** (median |dL| of each component's own pixels, out of a hit stop / in one): vine 0.230 /
  0.252, leaf scale 0.185 / 0.197, haft bark 0.155 / 0.108, bramble head 0.159 / 0.173, rim tell 0.135 /
  0.193, bite flash 0.234 / 0.239, root shoots 0.242 / 0.238, leaf motes 0.147 / 0.165, wither debris
  0.140 / 0.147. During the greening the vine reads 0.192 while its leaves are still sprouting (0.081).
- **Frame cost, real GPU** (Electron from `app/node_modules`, RTX 3070 through ANGLE, 453x805, chain on,
  interleaved A/B; the machine was loaded by the parallel builds, frames 46-58 ms): the whole-frame
  median difference ON minus OFF is -1.2..+0.3 ms at rest (the noise floor, identical code), -0.2..+0.8
  in the greening, +0.1..+0.8 in the hunt, +0.2..+1.2 in the root and wither. The caster's weapon plus
  `drawTwine`/`drawTwineTop` alone: 8.3-9.3 ms against the base chain's 8.1-8.8. No `shadowBlur` beyond
  the base head's own, no glow-sprite bakes.
- **Whole fights drawn** through the kill plus 3s of verdict, post chain alternating: 0 throws in 12
  fights, 15,853 draws; every clock close fades in 0.40s (0.44-0.78 when a hit stop falls in the
  wither); a window cut by the match's end withers in place.

**No `fx.js` field** — the design's §8.1 asks for "an emitter along the vine (leaf motes, glow, sparse)"
in both copies of `fx.js`. The picture lab measured why a SPECS field cannot be that, on 100 Tendril
windows (16 foes x 2 seeds, both sides): a field rides the one `m.ultFx` slot, which Bindweed holds for
a median 0.67s of window clock (max 0.72; there is no `life` entry for it, so the default 1.5) — 8.0% of
the window; the opponent's cast took the slot first in 16 of 100 windows; and a field spawns at the cast
point, while the vine's midpoint sits a median 191-218 units from it at t = 1/3/5/7s (p90 335-390),
because the vine moves with the caster. So the leaf motes are DRAWN instead, in the world pass, for the
whole window: shed off the tested segment at 2 a presentation-second (~4 a second of play), placed by
`shellHash`, at most 5 on screen, |dL| median 0.147, bloom share 0. Both copies of `fx.js` are unchanged
and nothing is re-stamped. The Zenith and Canopy precedent. **Rick's to overrule.**

**The voice** (v68 §8.2; Chromium 151; the controls reproduce the six published numbers, rune-crack
0.608/450 ms, BAR 0.364/300 ms, hit@11.6 0.443/80 ms; Bindweed's own blow, hit@18, is loudest-50 ms
0.1308-0.1362 over 12 noise draws):
- **Cast — SWEEP-TRI (of 5):** one bandpass sweep climbing 400 -> 3000 Hz over 0.56s, under it a
  triangle re-struck at its own cycles gliding 70 -> 90 Hz and swelling. The rustle climbs +533 cents,
  the creak reads 71 -> 88 Hz at -6.0 dB under the rustle; BAND 0.65 (a literal 400-3k band reads 0.55),
  no peak over 2.6 dB (noise, not a chime), +12.6 dB from head to top (not a crack). Audible 510 ms,
  -2.9 dB re the blow; worst register 0.69 (Thornshear). Bindweed had no arm and fell through to
  rune-crack, which eleven other relics still use: the arms go in BEFORE that fallback, which is
  re-emitted unchanged.
- **Bite — SNAP (of 4):** a 12 ms bandpass snap at 2.4 kHz over a sine body falling A5 -> A4, every
  frequency x 2^(n/12) with n the foe's entangle stacks AFTER the bite (A#5 on a clean foe's first bite,
  C#6 at the cap). Audible 75-80 ms at every count 0-4, worst peak 0.21 (spec <= 0.45); the body falls
  518-565 cents under the snap (wet); each count +100 cents on the body; -9.0 dB re the blow, +11.9 dB
  re the wall tick; worst register 0.51. A killing bite snaps too: the number of snaps is the number of
  bites.
- **Root — DEEP (of 5):** Canopy's timber an octave and a half down (260 Hz and its 2.76 mode at 0.4)
  pulsed for 0.2s, quickening 33 -> 55 a second, then the crack: a 35 ms highpass snap over a sine
  falling 60 -> 30 Hz, under the death voice's 120 Hz start. LOW 0.50 of its power below 120 Hz at the
  worst draw (spec >= 0.4); the crack lands 206 ms in, +43.5 dB over the creak; audible 370 ms; -1.4 dB
  re the blow and +1.5 dB over the loudest of the relic's other three voices; 0.31 against the death
  voice; worst register **0.795 against Threshmaw's cast (the gate is 0.80)** — every other root
  candidate crossed it.
- **Wither — CHAIN (of 4):** three overlapping bandpass sweeps falling 7 -> 4.8, 5 -> 3.4 and 3.6 -> 2.4
  kHz, each quieter: the cast's chain run downward. Falls -807 cents; 0.01 of its power below 1.5 kHz
  (dry), 0.00 below 120 Hz; no peak over 2.2 dB; audible 355 ms; peak 0.19 (spec <= 0.3); -9.0 dB under
  the cast. On a rooting close it shares the root's frame and keeps +4.9 dB in its own band (6.4 kHz).
- **Wiring:** the cast is `fireUlt`'s own `ult`/bindweed call; a bite plays once per bite inside
  `tickTendril` after the bite's hurt and entangle; the root plays inside the pin write's own block; the
  wither plays on a clock close with both alive, rooted or not, and never on a death (a caster's death
  ends the fight; a close after the foe's death belongs to its kill flight: Canopy's, Zenith's and
  Daybreak's rule). The lab's wire run (148 fights, both sides x 37 foes): 148/148 fights identical and
  every other SFX call identical in order and options; 2,882 bite voices for 2,882 bites (the count at a
  bite: 1: 243, 2: 49, 3: 230, 4: 2,360 — 82% at the cap), 356 roots, 371 withers for 371 clock closes,
  none on the 18 closes the caster's death made or the 87 the fight's end cut off. A real window (v
  Oathwound, 101602, 14 bites): the bites stand a median +28.5 dB over the fight in their own band, the
  root +26.6, the wither **+3.6 dB** (gate 3; the spec keeps it quiet and it shares the root's frame).

**Readings declared** (the labs', written in `bw_rows.py` and `bindweed_voice_lab.py`; art and sound are
Code's picks):
1. "The entangle tag printing its count": it prints when the count a bite leaves differs from the one
   the vine last printed, one vine tag at a time, silent at the cap, merged into the head's own tag.
2. The chain's bow eases out over the greening (median 0.7 units).
3. A stunned vine dims only its haft, as the base effectively dims the chain; it still turns and bites.
4. At the match's end the vine withers in place on the frozen geometry (Revenant's behaviour).
5. The root's shoots come from the floor even when the ball is mid-air (aerial roots).
6. The cast's "re-struck _tone" is a held note re-struck at its own cycles; "rising" is band, pitch and
   level together.
7. The bite's "wet" is the house's fork body falling underneath; n is the stacks after the bite.
8. The root's "Deadfall's register" is read as its standing, not its number (Deadfall's detonation
   measures 0.05 below 120 Hz; the spec's own LOW >= 0.40 is the gate); "the biggest single thing" is at
   least 1 dB over the relic's other three voices and never over its blow.
9. The wither plays on every clock close with both alive, rooted or not; never on a death.

### 5a. Stage 6's gates — every one able to fail

- **engine_ab sc-tendril-t3 → sc-tendril-fx, ALL 38 WITH Bindweed, n=6: 4218/4218 identical**
  (`runs/stage6_engine_ab38.txt`; 38/38 distinct winners, 4218 distinct seeds, 22.7-114.9s; the ids are in
  `runs/ids38.txt`). **Control:** the same gate against a copy with ONE sim write in the picture
  (`foe.vx += 1e-9` in `tickTwine`'s bite branch), with Bindweed, Grudgebearer, Aureole and Gravemourn at
  n=6: **16/36 differ**. The write can only move Bindweed's 18 fights (`runs/stage6_engine_ab_control.txt`).
- **bindweed_probe: 11/11** on sc-tendril-fx (`runs/stage6_probe.txt`; 444 fights, Bindweed both sides x
  37 foes x 6 seeds). **Stage 5's numbers hold to the digit:** 3.28 casts a fight; 6.06 bites, 12.12 damage
  and 0.85s of root a cast; 94% of clock closes root; 17 killing bites; 16.1% of window steps frozen. There
  are two new checks, and the link itself switches each one on:
  - **[10] the voice** (on because "bindweed-bite" is in `AC.SFX.play.toString()`):
    - casts: 1455 cast voices for 1455 casts, each inside `fireUlt`;
    - bites: 8818 bite voices for 8818 bites, the 17 killing bites included, each pitched at the foe's
      stacks after the bite (1: 715, 2: 161, 3: 754, 4: 7188);
    - roots: 1074 root voices for 1074 roots;
    - closes: 1144 wither voices on 1144 clock closes, and **none on the 51 death closes**;
    - inside the vine's tick nothing else sounds except the 134 ward shatters' own crit hit voices
      (hurt() plays them);
    - every Bindweed voice of the run is accounted for by its event.
  - **[11] the picture** (on because the Match has `tickTwine`):
    - 5,940,267 `tickTwine` calls: none changed a sim field of either fighter or the match, and none drew
      the RNG;
    - 1074 root beats, one per root, each at the quarry; no beat on any other close, and the hit stop
      untouched;
    - `twineHeld` set exactly while the root's pin holds (160,896 held steps);
    - the DRAWN subset (the first seed, both sides, every foe: 74 fights): 50,536 frames through the
      renderer (46,438 with the picture up, 6,905 of them in a hit stop). None threw and none changed the
      sim. The 74 drawn fights on their own also read 11/11 (`runs/stage6_probe_seeds1_drawn.txt`).
  - **Controls** (`runs/stage6_probe_mutants.txt`). Each one fails its own check and passes the other:
    - the wither voiced on every close fails [10] 17 times: 16 death closes, plus the run total (406
      voices against 390 accounted for);
    - `foe.vx += 1e-9` in `tickTwine` fails [11] 2864 times;
    - `a.vx += 1e-9` inside `drawTwineTop` fails [11] 5453 times on the drawn subset.
- **The builder's own scan** of stage 6's added code (its re-emitted anchors aside): no RNG, no `ultFx`,
  and no call that hurts, applies, resolves or shatters. The code writes only to `twine*` fields, the canvas,
  a tag's count, a record's clock, `taught` and an oscillator's pitch. **Controls:** a copy of the builder
  whose `tickTwine` writes `foe.vx` refuses ("writes foe.vx"), and so does one whose presentation call draws
  `this.rng()`. Stage 6 also refuses to run on its own output or on stage 4.
- **render_ab:** the other relics' pairs (paradox:heartwood:25064, twinshade:lastlight:991,
  bulwarden:vinesower:70707, axiom:grudgebearer:31337) are **24/24 pixel-identical**. **Control:** Bindweed v
  Grudgebearer 31337 at t = 6/16/20/24.1/33/39.2 (its windows run 14.45-23.84, 30.06-39.02 and
  45.67-46.74) is **1/6 identical**. The identical frame is t = 6, before the first cast; all five window
  and wither frames differ (`runs/stage6_render_ab.txt`).
- **chain_audit** `--builder bindweed_build.py`, with relic = tip = sc-tendril-fx: **ALL 28 INSERTS
  SURVIVE** (`runs/stage6_chain_audit.txt`). **Control:** the same relic with sc-tendril-t3 as the tip
  loses 14 of stage 6's 15 inserts and exits 1 (`runs/stage6_chain_audit_control.txt`). The fifteenth, the
  root's beat, still reads "ok" there, because its marker is a line that every `ult` beat shares (4 on the
  relic, 3 on the tip). chain_audit cannot watch that insert; probe [11] does.
- **tip_audit:** identical to sc-tendril-t3's except for the file name (`runs/stage6_tip_audit_*.txt`).
- **shell_identity on the carried `sc-tendril-fx`** (`SWB_GAME`, the pointer not moved; the json
  restored): **200/200** (`runs/stage6_shell_identity.txt`).
- **The carry, dry:** after Portcullis's stage 6 landed on the chain (`02-chain/sc-onslaught-fx.html`,
  ee74fe9ad67e50a6; its rows share four of these anchors: the rune-crack fallback and the three draw-call
  lines), `bindweed_build.py --stage 6 --src ../02-chain/sc-onslaught-fx.html` applies all fifteen edits
  and parses (eea0cde5536955b3). This was a scratch file, not a link; the orchestrator's engine_ab
  proves the carry.
- **The labs' own gates** (§5 above):
  - picture: bloom share +0.0000, with a lighter-filled control that fails;
  - picture: 24/24 whole-fight sim hashes, with a 1e-9 control that differs on all 10 Bindweed fights;
  - picture: 32/32 other-relic render frames, with a Bindweed control at 1/4;
  - picture: 12 whole fights drawn without a throw;
  - voice: the 148/148 wire run, with a sim-write control at 4/148 identical, and 74/74 end to end.

## 6. The clip (Rick's to overrule)

`tools/_bindweed_pick.py` (from `_ironwood_pick.py`) scores a window against §8. Three things are required:
the window must close BY ITS CLOCK with both alive (the only close that roots and withers), it must root the
foe, and the fight must run on through the clip's 1.8s tail. Points then come from:
- the bites (0.35 each, up to 12);
- the entangle counts heard (1.0 per count, so a 1-2-3-4 climb, the design's "count in the ear", beats a
  window that starts at the cap);
- the touch stretches and the blows;
- the growth's peak and its drawing back.

It ran 12 foes x 6 seeds, with Bindweed as side A, the side `cinema_clip --a` films
(`runs/stage6_pick.txt`). The pick is **Bindweed v Shroudmaul (Grasp), seed 101275**:
- the cast lands at 47.12, and the 9.35s window closes by its clock and roots (1.20s, 4 stacks);
- 10 bites, climbing 1-2-3-4;
- 10 touch stretches;
- reach peaks at x1.64.

The runner-up, Lightkeeper 101201, scored 0.05 lower: it had 12 bites, but only the counts 3 and 4.

    python cinema_clip.py --game <scratch>/batch/bindweed/links/sc-tendril-fx.html --a bindweed \
      --b shroudmaul --seed 101275 --at 45.92 --window 12.35 --end-at-window --fps 60 --w 540 \
      --out ../07-shorts/v101/tendril-window.mp4

The clip:
- 13.35s: 800 frames covering the window and 1.8s past the close; the fight is still on at 58.27 (55 / 18 hp);
- 540x960 h264 at 60 fps, AAC 48 kHz stereo, 2.88 MB;
- **AAC mean -22.0 dB, max -3.1 dB** (`runs/stage6_clip_aac.txt`).

Five frames, checked through the pipeline (post chain, director):
- 1.4s: the cast card over the greening flail;
- 3.3s: the vine hunting out to the bramble head;
- 7.3s: the leafed vine down to the head, with the foe trailing its entangle vines;
- 11.3s: the ENTANGLE tag just before the close;
- 12.7s: the root's four shoots up the held ball, and the vine gone.

Shroudmaul's Grasp holds Bindweed mid-window and draws its own runic hexagon on it. That is open item 41,
not this relic's. The clip is `07-shorts/v101/tendril-window.mp4` (gitignored). **Rick's to overrule.**

## 7. What is left, and whose

- **Rick:**
  - the clip, and the picture and voice picks;
  - the drawn leaf motes in place of the design's `fx.js` field (§8.1 asks for one; §5 has the
    measurements behind the choice);
  - the aerial root shoots;
  - **the root's register: 0.795 against Threshmaw's cast**, just under the 0.80 gate, where every other
    root candidate crossed it. Worth an ear;
  - 82% of bites land at the cap, because the head's blow applies 2 stacks, so "the count in the ear" is
    heard mostly at the start of a window;
  - the wither stands only +3.6 dB over a real fight, because the spec keeps it quiet and it shares the
    root's frame;
  - the type spread (item 12/32);
  - the brief's "one whole fight watched end to end" is MEASURED here, not watched: the picture lab drew
    12 fights through the kill and the verdict, and the probe drew 74.
- **The orchestrator:**
  - move `app/main.js`'s `GAME` line (the brief asks for it) only when Rick has nothing to overrule on
    the batch's clips;
  - send the clip to Rick (one clip per ultimate).
- **Standing, not this build's:**
  - Grasp's squeeze still draws the runic hexagon on its pinned ball (open item 41);
  - the silhouette redraw is a separate claim (design §8.1);
  - `s.snap`, `maxLive` and `frame_probe` belong to the chain, not to this relic.

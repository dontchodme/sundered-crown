# v101 — BINDWEED / TENDRIL, BUILD. STAGES 1-5 DONE: stage 1 is arm A to the fight; the mechanism is the lab's; the win rate runs over the lab by the window clock (measured); the build's knob moved and said (turn 4 -> 3) and the blade sits at the crossing, 18 (48.5% both sides). Stage 6 (picture, voice) next. Claude Code has it.

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

## 5. Stage 6 (next)

The picture and the voice (design §8.1-8.2), after Portcullis's stage 6 lands under this line;
these links are carried onto it first (engine_ab against these).

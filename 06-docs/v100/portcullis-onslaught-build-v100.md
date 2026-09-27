# v100 — PORTCULLIS / ONSLAUGHT, BUILD. STAGES 1-5 DONE: stage 1 is arm A to the fight, the mechanism is the lab's, and the blade sits at the crossing, 23 (50.8% both sides). Stage 6 (picture, voice) next. Claude Code has it.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 05:22 UTC (`CLAIMS.md`, the BUILD row under the
vigil flail's). Input: `06-docs/v72/PORTCULLIS-BUILD-BRIEF.md` + `vigil-flail-design-v72.md`, and
nothing else (rule 0). Builder `tools/portcullis_build.py`, probe `tools/portcullis_probe.py`, runs
in `runs/`. **A NEW relic: the 37th built** (the brief's "39th" counts the cell grid).

```
sc-canopy-w38.html      the base: the chain tip (Ironwood stage 5)
  -> sc-portcullis.html   stage 1  the relic, ult stubbed (charge 1e9)   131b2956dbbcc3fc
  -> sc-ram.html          stage 2  the charge and the slam (arm C)       4d425f69405aa56e
  -> sc-onslaught.html    stage 3  the bank, bank 0 -> 8 (arm D)         2d84fc7090a49afa
  -> sc-onslaught-b23.html stage 5  the blade, 24.03 -> 23                2ebe6e1b8c5c9e00
```

When Ironwood's stage 6 lands on the tip, these links are rebuilt on it with the same builder
(`--src`), and engine_ab against these proves the fights carry (Ironwood's own precedent, v99 §1).

## 0. What this build stands on

- **The relic** is Gravemourn's flail profile, the lab's donor (reach 96, width 22, artW 52, spin
  2.2, chain, mass 3.6) and its blade, 24.03, until stage 5; aff vigil, onSelf ward 1, and the
  brief's 71-character card. The builder asserts the donor's profile, the four vigil melee
  channels and the vigil flail head's route (`_fhPlated`, never drawn by a shipped relic).
- **The charge is 14:** the brief's 16 on the lab's clock, converted (Rick's batch ruling).
  Measured for this fighter on arm D (660 fights, `runs/s0_freeze_2207`): 11.4% of the lab's steps
  are frozen (13.8% inside windows), so the lab's 16 is the engine's 14.2, and 14.
- **Readings** (in the builder's docstring):
  1. the slam is 0.25 x shield and nothing else (design §4); the lab's `ramDmg` defaults to the
     rejected flat 10, so every lab arm passes `ramDmg=0`, as the settled runs did;
  2. both components of the charge (the brief's "vx,vy");
  3. the target is the opponent, never a Twinshade shade;
  4. a slam at zero shield is still a slam: no damage, but the knock, the bank and the cooldown;
  5. the knock skips a dead or pinned foe (the lab's);
  6. `hurt`'s source is the Fighter (its contract); the bank's `apply("ward", 1)` passes none;
  7. every slam files a hit beat marked `ram`, fatal when it killed (design §6, brief §1).
- **The clock:** the window, the charge's acceleration and the slam's cooldown run on the window
  tickers' clock, which stops in a hit stop. The lab ran all three through freezes. On Canopy that
  difference was worth -5 through the canopy's cadence (v99 §4); here it pushes the other way (§2).

## 1. Stages 1-3

Stage 1 appends the row after Ironwood with the ultimate stubbed at 1e9. Stage 2 adds `ultRam` /
`ramTally`, the `kind === "ram"` cast branch, `tickRam` after `tickTree` (after `ballCollision`,
before `tickHits`) and charge 14, with bank 0 written but inert. Stage 3 is one character.

`tickRam`, each window frame: the charge (vx, vy += unit(foe) x 600 x dt unless pinned, clamped
at speedMax); a slam when the centres are within 2R + 3 and the cooldown is clear: hurt(foe,
0.25 x shield, f), knock 500 along caster → foe, then the bank's three writes (shield to the
cap, shieldMax, `apply("ward", 1)`), and a hit beat.

## 2. Stage 0 and the stages against it

`ult_overlay.py --game ../02-chain/sc-canopy-w38.html --relic gravemourn --cell vigil:flail
--mech overlays/ram.js --arms A,B,C,D --P ramDmg=0 --seeds 20 --foes <33>`, seed0 2207 and 2317,
660 fights an arm a block. The foes are the published 33 (every relic but the donor on the
34-relic chain). The built links run `--relic portcullis --arms SHIP` on the same foes and seeds.

```
                          lab on 151 (block 1 / 2)   published 141   BUILT (block 1 / 2)        pooled
A   no ultimate           26.8 / 25.5                28.0            stage 1: 26.8 / 25.5       identical, fight for fight
B   slam only             33.6 / 31.7                31.2
C   + the charge          35.0 / 36.1                33.9            stage 2: 35.2 / 32.9       34.1 (lab 35.6)
D   + the bank            55.2 / 52.6                54.4            stage 3: 57.9 / 58.5       58.2 (lab 53.9)
```

Lab mechanism on 151 (arm D): 3.54 casts; 3.67 slams, 16.5 damage and 28.9 ward banked a cast;
18.4 shield on an average window frame.

**Stage 3 reads 4.3 over arm D, on both blocks.** The engine's window is 8 seconds of the window
clock, ~9.3s of match time at 13.8% frozen, where the lab's was 8 step-seconds, so the built
window holds more slams and more bank (the probe: 3.82 and 29.9 a cast against 3.67 and 28.9).
The mechanism is the lab's; stage 5 settles the blade on the built relic.

## 3. The probe (`portcullis_probe.py`, one check per sentence, read inside the hooks)

- **sc-onslaught: 9/9** (432 fights, every foe, both sides): every charge rebuilt exactly (none
  while pinned), every slam inside 2R + 3 and never closer than 0.5s, never a missed clear
  contact, the damage exactly 0.25 x the shield before, the knock exact, the bank's three writes
  and the ward's clock, one `ram` beat a slam (30 killing slams, each fatal). 3.55 casts; 3.82
  slams, 17.7 damage and 29.9 banked a cast; 18.6 shield on a window frame. 37% of slams land at
  zero shield (knock and bank only); 115 wards broken by a slam, and no other stop.
- **sc-ram (stage 2): 9/9**: 3.43 casts; 3.86 slams and 11.3 damage a cast (arm C: 3.65, 10.6);
  shield 10.0 on a window frame (10.3).
- **sc-onslaught-b23 (stage 5): 9/9**: 3.64 casts; 3.84 slams, 17.6 damage and 30.2 banked a cast;
  18.4 shield.
- **Controls** (`runs/probe_mutants.txt`): the charge unclamped fails [1]; a flat 10 on the slam
  fails [3]; the bank without the ward's clock fails [5]; the knock 1% long fails [4]; a killing
  slam's beat not fatal fails [6]. Each fails its own check and only that one.
- **Stage 1 is arm A fight for fight** on both blocks: every foe's rate and every blow count
  identical (`runs/built_portcullis_*`).
- **engine_ab sc-canopy-w38 → sc-onslaught, the 36 others, n=8: 5040/5040 identical**
  (`runs/engine_ab36.txt`). Adding Portcullis moves no other fight.

## 4. Stage 5: the blade — 23

Both sides (`relic_rate.py`: each seed from both sides; every other relic a foe, 10 seeds a foe a
side, 720 fights a block; seed0 2207 and 2317; `runs/stage5_rr_*`):

```
blade   block 1   block 2   pooled (1440)   side A   side B
22      46.9      46.7      46.8            48.2     45.4
23      50.8      50.8      50.8            52.1     49.6
24      53.2      54.6      53.9            55.3     52.5
```

**The crossing is ~22.8**, inside the brief's "expect 22.5-23.5". Blade 23 is the measured point at
it; nothing else moves. The built link reproduces the measurement exactly (`relic_rate` on
`sc-onslaught-b23` with no knob set: block 2207 50.8%, every foe and the mean duration the same).

- **verify --n 40 on sc-onslaught-b23 (37 relics): 10/13** (`runs/verify_b23.txt`). Portcullis
  52.3% (side B, as verify plays an appended relic); every relic in 30-70% (Heartwood 31.7 .. Gloamwire 65.3). The reds are the two clock bands and "both sides can win every matchup" on Bloodmirror v Ironwood 40/0: not Portcullis's pairing. It is Ironwood's own counter (5% in its ladder, 0% in its design, v99 §5), and adding a relic reshuffles verify's seeds; at 5%, 0/40 turns up about one time in eight. Item 12/32, Rick's.
- **The ladder at 23** (40 fights a foe, `runs/ladder_b23.txt`): greatsword 69%, scythe 54,
  warhammer 51, twinblade 48, flail 40, bow 38. Worst Ironhail 10%, Gloamwire 12.5, Slagheart 27.5;
  best Heartwood 87.5, Oathwound 82.5, Axiom 77.5. The design's shape (greatsword 71, bow 35,
  flail 33; Ironhail and Gloamwire 20): bows, and a flail that latches. **"Bows at 35%" is item
  12/32, Rick's.**

## 5. Stage 6 (next)

The picture and the voice (design §7.1-7.2), picked on measurements under "you pick i overrule",
after Ironwood's stage 6 lands on the tip; these links are carried onto it first.

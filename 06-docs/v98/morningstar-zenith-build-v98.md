# v98 — MORNINGSTAR / ZENITH, BUILD. STAGES 1-5 DONE (every stage on its lab arm; blade 24.03 confirmed); stage 6 (picture, voice) next. Claude Code has it.

Claude Code on **DESKTOP-DERRAFT**, claimed 2026-09-27 (`CLAIMS.md`, the BUILD row under the
sanctified flail's). The input is `06-docs/v71/MORNINGSTAR-BUILD-BRIEF.md` +
`sanctified-flail-design-v71.md`, and nothing else (rule 0). Builder `tools/morningstar_build.py`,
probe `tools/morningstar_probe.py`. **A NEW relic: the 35th built** (the design's "38th" counts
the cell grid, and Bindweed, Ironwood and Lodestone are not built yet).

```
sc-daybreak-fx.html     the base: the chain tip (sc-leaf + Corollary 1-6 + Daybreak 1-3)
  -> sc-morningstar.html   stage 1  the relic, ult stubbed (charge 1e9)   ae15f5d9ff083b90
  -> sc-sun.html           stage 2  the light and the smite (arm B)      9b5e93cde1a6cfe3
  -> sc-burn.html          stage 3  the burn, tickDmg 0 -> 3 (arm C)      e4ec9fa69978b6c4
  -> sc-zenith.html        stage 4  the heal, bless 0 -> 1 (arm D)       9be1a7ca4832c327
```

## 0. What this build stands on

- **The relic** is Gravemourn's flail profile, the lab's donor: reach 96, width 22, artW 52,
  spin 2.2, chain, mass 3.6. It keeps **the type's own blade, 24.03**. aff sanctified, onHit
  smite 1, and the brief's 69-character card. The builder asserts the donor's profile. The blurb
  is taken from the brief's §0 prose; nothing reads it.
- **The charge is 14:** the brief's 16 on the lab's clock, converted (Rick's batch ruling).
  Measured for this fighter the engine's clock runs 0.897 of the lab's.
- **Readings** (in the builder's docstring):
  1. the tick order is the prose's (hurt, smite, blessing);
  2. `apply`'s source is a side letter;
  3. a killing tick files its own fatal beat;
  4. the target is the opponent only;
  5. the lab's cadence;
  6. the blessing is per tick, unconditional on damage.
- **A deliberate change to the brief's process:** stage 2's "FILM IT, bloom-measure the
  placeholder" is folded into stage 6. The picture is presentation, it cannot move a fight or the
  blade, and the real art's bloom is measured before it ships.

## 1. Stages 1-4

Stage 1 appends the row after Starwarden, with the ultimate stubbed at 1e9 (Starwarden's
pattern); every table keyed by relic id falls back. Stage 2 adds `ultSun`/`sunTally`, the
`kind === "sun"` cast branch, `tickSun` after `tickDawn`, and charge 14, with tickDmg 0 and
bless 0 written but inert. Stages 3 and 4 are one character each.

**Probe on sc-zenith: 9/9** (408 fights, Morningstar on both sides, 34 foes).
- Per cast: 5.34 ticks, 16.0 damage, 5.34 blessing.
- The foe is lit 15.6% of the window, against the lab's ~20%. The lab tests lit after the whole
  step, frozen frames included, and the engine's ticker freezes with the world and runs before
  `tickHits`. Starwarden's dwell ran short the same way (v66 §0b).
- 3.31 casts a fight (the lab's ~3.2). 19 killing ticks, each with its fatal beat.


## 2. Stage 0 and the stages against it — every stage lands on its arm

`ult_overlay.py --game ../02-chain/sc-daybreak-fx.html --relic gravemourn --cell sanctified:flail
--mech overlays/sun.js --P sunR=100 blessOnTick=1 --seeds 20` (the lab's defaults are sunR 70 and
blessOnTick 0, so both are passed), seed0 2207 and 2317, 660 fights an arm a block. The built
links run `--relic morningstar --arms SHIP --foes <the lab's 33>` on the same seeds (arm SHIP is
the built ultimate at its own charge).

```
                         lab on 151 (block 1 / 2)    published 141        BUILT (block 1 / 2)   pooled
A   no ultimate          7.9 / 8.2                   7.6                  stage 1: 7.9 / 8.2    identical, fight for fight
B   the light + smite    18.5 / 18.2                 18.5                 stage 2: 20.0 / 18.5  19.3
C   + the burn           30.5 / 27.9                 26.1                 stage 3: 28.8 / 29.4  29.1
D   + the heal           51.1 / 50.9                 50.2 / 50.6          stage 4: 50.5 / 52.3  51.4
```

The lab's mechanism reproduces too: ~5.9 ticks, 17.6 damage and 5.9 blessing a cast, the foe lit
~20%, and 3.19 casts a fight. **At charge 14 every stage lands on its lab arm**, and stage 1, with
its ultimate stubbed, is the same fights as arm A.

- **engine_ab sc-daybreak-fx → sc-zenith, the 34 existing relics, n=8: 4488/4488 identical.**
  Adding Morningstar moves no other fight.
- **Probe on sc-sun (stage 2): 9/9**; on sc-zenith: 9/9 (§1).
  On sc-zenith (408 fights, `runs/probe_zenith.txt`): 5.34 ticks, 16.0 damage and 5.34 blessing a
  cast, the foe lit 15.6%, 3.31 casts a fight; 19 killing ticks each filed its own fatal beat;
  59 wards broken by a tick, and no other stop.
- **chain_audit** (`morningstar_build.py`, sc-burn → sc-zenith): all 7 inserts survive (the
  stage-4 marker is unresolved only because sc-burn predates it). **tip_audit**: identical to
  the base's (it reads status tips; Burn's `feed` flag is the base's own).
- **verify --n 40 on sc-zenith (35 relics): 11/13.** Morningstar 47.8%; every relic in 30-70%
  (Heartwood 35.5 .. Gloamwire 65.1, spread 29.6pp); both reds are the clock bands. "Both sides
  can win every matchup" passes.

## 3. Stage 5: the blade — 24.03 CONFIRMED

Wide, both sides, two blocks of 660 on the lab's 33 foes: **22.5 → 47.0 / 49.4 (48.2)**, **24.03 →
51.4**, **25.5 → 52.7 / 50.5 (51.6)**. The type's own blade sits on the design's ~50%, so it does
not move and no link is written.

**The ladder at 24.03** (40 fights a foe), which the brief asks to print because of "Farwarden 0%
— Rick's": **Farwarden is 32%, not 0%.** The range runs from Aureole and Gloamwire at 18% to Axiom
at 85%; no pairing is a lockout. The full ladder is `runs/ladder_zenith.txt` (pooled from `built_zenith_*.json` byFoe).

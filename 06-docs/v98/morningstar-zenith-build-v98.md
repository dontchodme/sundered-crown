# v98 — MORNINGSTAR / ZENITH, BUILD. STAGES 1-6 DONE (every stage on its lab arm; blade 24.03 confirmed both sides; the sun drawn as a gold ring, voiced, gated). Clip with Rick; the app pointer waits for him.

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
  -> sc-zenith-fx.html     stage 6  the picture and the voice            5e9babefde273d37
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

## 3. Stage 5: the blade — 24.03 CONFIRMED, both sides

**A CORRECTION to the first version of this section (commit 3e2303d).** It said "wide, both
sides", but those numbers came from `ult_overlay`, which always plays the relic as side A. They
were side A only: 22.5 → 47.0 / 49.4 (48.2), 24.03 → 51.4, 25.5 → 52.7 / 50.5 (51.6), on the lab's
33 foes.

**Both sides** (`relic_rate.py`, which plays each seed from both sides; every other relic as a foe,
10 seeds a foe a side, seed0 2207 and 2317, 680 fights a block, on sc-zenith-fx, whose fights are
sc-zenith's; `runs/stage5_rr_*`):

```
blade    block 1   block 2   pooled (1360)   side A   side B
22.5     42.1      45.9      44.0            44.9     43.1
24.03    47.6      49.4      48.5            50.9     46.2
25.5     52.9      53.7      53.3            57.9     48.7
```

The crossing is ~24.4. **24.03 reads 48.5%, about one standard error under 50, and the brief says
"move only if the band misses"**, which it does not (verify: 47.8%, every relic in 30-70). The
type's own blade stays, and no link is written. Side B, the side `verify` plays an appended relic
on, runs 4.7 points under side A at 24.03.

**The ladder at 24.03** (40 fights a foe), which the brief asks to print because of "Farwarden 0%
— Rick's": **Farwarden is 32%, not 0%.** The range runs from Aureole and Gloamwire at 18% to Axiom
at 85%; no pairing is a lockout. The full ladder is `runs/ladder_zenith.txt` (pooled from `built_zenith_*.json` byFoe).

## 4. Stage 6: the picture and the voice — `sc-zenith-fx`

Picked on measurements under Rick's "you pick i overrule", by two labs run in parallel (the
picture lab's scratch and `tools/zenith_voice_lab.py`), and built as `morningstar_build.py --stage 6`:
twelve anchored edits, the thirteen rows the labs returned with the two that share the tick's
blessing line merged into one. Every row is byte-exact to the labs' own files; the picture rows
alone reproduce the picture lab's stamp (0d62ea78b4bbb510).

**The picture** (v71 §6.1; the sheet is `05-reference/v98/zenith-picture-sheet.png`):
- **The sun is a ring**, not a disc: a 10-unit gold band at radius 100 round the flail head, peak
  alpha 0.35 with a hot heart line, the hole cut, an 8-unit halo outside it, and the ground inside
  lit at most 0.05. Eight rays turn with the head's tumble. A hot core (r 12) sits on the head.
- **The cast** ignites over 0.25s (the ring grows out of the head); **the close** contracts into
  the head over 0.3s, and so does a window cut by the caster's death or the match's end.
- **A tick** drops four drawn sparks onto the foe and runs a gold thread with a bead from the foe
  back to the caster for 0.15s; the first tick of each lit stretch tags SMITE on the foe and
  BLESSING on the caster (Corona's and Daybreak's rule), and the ball draws its own smite count.
- **Twenty drawn embers** rise off the band for the whole window.
- **The head** is redrawn: faceted gold on the pale haft (`_fhRadiant`, which only a sanctified
  flail draws; this is the first).
- **Warm gold with a hot heart, not the school's white**, and every tick shows the burn landing and
  the heal running home. That is Rick's note on Daybreak ("sunlight glowing rather than the dull
  white"; "hard to tell what exactly it does"), applied here because it fits this sun.
- It hangs off the fighter (`sunFade`, `sunAge`, `sunLitFade`, `sunTagged`) and a match list
  (`sunFx`), never `m.ultFx` (open item 25). `tickSun` gains one line, `this.sunShown(f, foe)`,
  which writes presentation state only.
- **Passes:** ring, rays, lit ground, embers, rim and thread in the WORLD pass under both balls
  (bloom share 0); core and sparks in the EMISSIVE pass over them, so the head glows.

**No field in `fx.js` (a reading the brief did not expect: it asks for the field "in both
copies").** A SPECS row fires once, at the cast, from the one ultFx slot, centred where the caster
stood, while the ring rides the head a mean 128 units away for 8s. On 1 of 6 fights the opponent's
cast took the slot and there was nothing to spawn from. And a cast field on the near-white caster
pushed its disc past 0.90 (a swirl, +0.0125) or clipped 61% of it (a burst, +0.231). So the embers
are drawn, for the whole window, as Daybreak's motes are (v97 §4a). The stamp on both copies is
untouched. **Rick's to overrule.**

**The voice** (v71 §6.2; `zenith_voice_lab.py`, wavs in `05-reference/v98/`, gitignored):
- **Cast — STEP:** D5 then A5, a just fifth, re-struck in phase (`.frequency.value = f`, v97 §4b),
  swelling +11.9 dB to its top 495 ms in, -2.9 dB against Morningstar's own blow. Register 0.45
  against rune-crack, 0.09 against Daybreak's cast.
- **Tick — SOFT:** a 55 ms struck bar pitched by the foe's smite stacks after the tick (an A-minor
  pentatonic from C7), peak 0.205 against the design's 0.35.
- **The heal** is the existing spark-collect voice, unchanged (Lastlight's), pitched by the
  caster's blessing stacks.
- **Close — MIRROR:** the cast reversed, 9 dB under its top, only when the window closes by its
  clock with the caster alive.
- Morningstar had no voice arm and played the shared rune-crack. The arms are added before that
  fallback, which is left untouched.

### 4a. Stage 6's gates — every one able to fail

- **engine_ab sc-zenith → sc-zenith-fx, ALL 35 WITH Morningstar, n=8: 4760/4760 identical**
  (`runs/stage6_engine_ab35.txt`). The picture and the voice move no fight.
- **morningstar_probe: 11/11** (`runs/stage6_probe.txt`), the stage-4 numbers to the digit, plus:
  - [10] every tick plays one chime pitched by the foe's smite and one heal voice pitched by the
    caster's blessing (7222 ticks); every clock close plays one close voice (1095), none on a
    death; cast, tick and close each render alone, and the cast is no longer rune-crack;
  - [11] every tick files one picture record, and `sunShown` changes nothing the simulation reads.
  - **Controls:** a close voice that also plays on a death fails [10] (19 times); a `sunShown` that
    nudges the foe by 1e-9 fails [4] and [11] (3605 times) (`runs/stage6_probe_mutants.txt`).
- **render_ab:** the other relics' pairs (paradox:heartwood, twinshade:lastlight,
  bulwarden:vinesower, axiom:grudgebearer) print **24/24 pixel-identical**; the control,
  Morningstar v Grudgebearer 31337 inside a window, prints **0/4 identical**.
- **shell_identity on sc-zenith-fx** (`SWB_GAME`, the pointer not moved; the app's json restored):
  **194/194**.
- **chain_audit:** morningstar_build, relic and tip sc-zenith-fx, 20/20; dawn_build,
  sc-daybreak-fx → sc-zenith-fx, 17/17; corollary_build, sc-corollary-c14 → sc-zenith-fx, 25/25.
- **tip_audit:** identical to sc-zenith's.
- **The picture lab's own gates** (headless 151 at 540x960, chain on; frame cost on Electron 44 /
  RTX 3070):
  - **Bloom:** Zenith's own share of the arena lift max +0.0007 (gate +0.02) over 427 full-sun
    frames on 6 foes. The caster's disc moves at most +0.0030, and is ≤ 0.90 on 366/367 unflashed
    frames (the one reads 0.9535 with and without the picture: the body alone). The white
    sanctified foe (Aureole) is not erased: disc 0.837 against its contour 0.511.
  - **Control that must fail:** the sun as a filled lighter disc puts the caster's disc at 0.987
    and 85/367 frames past 0.90. It fails.
  - **Legibility:** the ring band |dL| 0.16-0.18 at full sun on white, dark and ordinary foes,
    0.07-0.17 inside a hit stop; tick sparks peak 0.91-0.93 at the foe; the thread 0.05-0.25.
  - **Frame cost:** drawSun + drawSunTop 0.42-0.77 ms (Daybreak's drawDawn: 0.28-0.36).
  - **Sim identity:** per-step hashes on 8 fights identical with and without the rows, and a
    1e-9 sim write in `sunShown` differs on all 7 Morningstar fights.

## 5. The clip (Rick's to overrule)

`tools/_zenith_pick.py` scores a window on §6: it must close by its clock (the only way to see
the ring contract and hear the close), with ticks, lit share and entries into the light. The pick:
**Morningstar v Shroudmaul (Grasp), seed 98286**, cast at 60.90, 14 ticks, the foe lit 56% of
the window and entering the light 8 times.

    python cinema_clip.py --game ../02-chain/sc-zenith-fx.html --a morningstar --b shroudmaul \
      --seed 98286 --at 59.70 --window 12.54 --fps 60 --w 540 --out ../07-shorts/v98/zenith-window.mp4

14.8s, AAC mean -20.8 dB, max 0.0 dB. The window closes by its clock at 70.6 and Morningstar falls
at 71.0, so the clip ends on the verdict. The late Third Seal's inset puts part of the ring outside
the hall. Sent to Rick 2026-09-27.

## 6. What is left, and whose

- **Rick:** the clip; the picture and voice picks; the drawn embers in place of an `fx.js` field.
- **The app pointer** stays on `sc-leaf` until Rick has nothing to overrule on the batch's clips
  (Corollary, Daybreak's line, Zenith). The brief's "move GAME" waits for that.
- **The chain tip is sc-zenith-fx.** Ironwood (v99) is carried onto it.

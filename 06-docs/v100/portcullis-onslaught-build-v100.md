# v100 — PORTCULLIS / ONSLAUGHT, BUILD. STAGES 1-6 DONE: stage 1 is arm A to the fight, the mechanism is the lab's, the blade sits at the crossing, 23 (50.8% both sides); the shell drawn and voiced, gated, and on the chain (`sc-onslaught-fx`, on `sc-tendril-t3`). Clip with Rick; the app pointer waits for him.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 05:22 UTC (`CLAIMS.md`, the BUILD row under the
vigil flail's). Input: `06-docs/v72/PORTCULLIS-BUILD-BRIEF.md` + `vigil-flail-design-v72.md`, and
nothing else (rule 0). Builder `tools/portcullis_build.py`, probe `tools/portcullis_probe.py`, runs
in `runs/`. **A NEW relic: the 37th built** (the brief's "39th" counts the cell grid).

```
sc-canopy-fx.html       the base: the chain tip (Ironwood stage 6)
  -> sc-portcullis.html   stage 1  the relic, ult stubbed (charge 1e9)   baa42ac9afe5509c
  -> sc-ram.html          stage 2  the charge and the slam (arm C)       26baece2e0b5f41c
  -> sc-onslaught.html    stage 3  the bank, bank 0 -> 8 (arm D)         1e35fb5045382352
  -> sc-onslaught-b23.html stage 5  the blade, 24.03 -> 23                db47cc35a1fe7e98
sc-tendril-t3.html      the chain tip now (Bindweed stage 5 over Portcullis stage 5; 38 relics)
  -> sc-onslaught-fx.html  stage 6  the picture and the voice               ee74fe9ad67e50a6
```

**Carried onto Ironwood's stage 6.** The links were first built on `sc-canopy-w38` (commit
eee7ec1: 131b2956dbbcc3fc, 4d425f69405aa56e, 2d84fc7090a49afa, 2ebe6e1b8c5c9e00). When
`sc-canopy-fx` landed they were rebuilt on it with the same builder, deleted by hand first as the
builder asks. **engine_ab, the first `sc-onslaught-b23` against the carried one, all 37 relics WITH
Portcullis, n=6: 3996/3996 identical** (`runs/carry_engine_ab37.txt`). Every number below carries.

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

## 5. Stage 6: the picture and the voice — `sc-onslaught-fx` (on `sc-tendril-t3`)

Picked on measurements under Rick's "you pick i overrule" by two labs run in parallel on the chain tip:
the picture lab (scratch, `batch/portcullis/stage6-picture/`) and `tools/portcullis_voice_lab.py`.
Built as `portcullis_build.py --stage 6 --src ../02-chain/sc-tendril-t3.html`: **thirteen anchored
edits, five voice and eight picture, byte-exact to the labs' own row files**
(`runs/stage6_gen_s6.txt`, `runs/stage6_build.txt`):

- the picture rows alone reproduce the picture lab's stamp, **de1cf49480a06745**;
- the voice rows alone reproduce the voice lab's end-to-end page, **817c69c9dfe9463b**;
- both together are the voice lab's combined page and the built link, **ee74fe9ad67e50a6**
  (+23,366 chars, 38 relics).

The chain tip is `sc-tendril-t3` (Bindweed stage 5 over Portcullis stage 5), so stage 6 goes straight
on it. It was built and gated in scratch (`batch/portcullis/links/sc-onslaught-fx.html`) and carried
onto `02-chain/` with the same builder on the same tip: **the carried link is byte-identical to the
gated one (ee74fe9ad67e50a6)**, so every gate below is the chain's.

**How the rows became the builder.** Each lab's full report carries its rows, and they equal the row
files field for field. No two anchors share a line of the base, so nothing is merged. Every replace
row re-emits its anchor, so another relic's row on the same line applies in either order. Bindweed's
voice also lands on the rune-crack fallback, and its sound is the same whichever order the rows go in.
**One anchor is widened.** The bank voice's line, `T.banked += f.shield - b0;`, appears once on this
tip, but Lightkeeper's Bulwark (in flight) writes the same line twice more. So the edit takes
Portcullis's whole bank block, from `if (u.bank > 0){`, and puts it back unchanged: the same bytes
come out. The carry was tried read-only on every link the batch has in flight: 24 links (Coldiron,
Ironhail, Lightkeeper, Lodestone, Widowmaker, and Tendril's picture page). Every edit's old text
occurs exactly once in each. **And the carry was built.** Bindweed's own `--stage 6` and this one were
run on `sc-tendril-t3` in both orders, in scratch. Both orders apply, parse and carry 38 relics.
They hold the same lines; only the order of independent blocks differs, such as the two relics' arms
before the rune-crack fallback (`runs/stage6_carry_bindweed.txt`).

`--stage 6` refuses to run twice ("stage 6 goes on stage 5, once"). It refuses any insert that draws
the rng, takes the ultFx slot or writes the shared weapon row. Before it touches the head route and
the haft, it asserts that Portcullis is the only vigil flail.

**Readings, declared in the builder's docstring (8-15):**
- **8. The bank's voice is new.** §7.2 asks for "the ward's existing bank voice, reused", and there
  is none: the synth's 17 kinds have no ward or bank voice. A ward banks in silence, and a ward that
  breaks plays an ordinary crit hit. So `ward-bank` is the ward's own new kind, as `hex-snap` is the
  runic school's. Only Onslaught plays it; the vigil blow's own bank stays silent, as it was.
- **9.** The slam's voice carries the shield the slam hit for, before the bank. A slam at no shield
  still knocks and banks, so it still thuds, at the quiet end.
- **10.** A bank at the cap still sounds: it adds nothing but restarts the ward's clock (the brief:
  "Slams = banks"). That was 23 of 2058 banks in the voice lab.
- **11. The close voice plays only on a clock close with the caster alive.** A death belongs to the
  death voice and the shatter (Zenith's, Daybreak's and Canopy's rule). The plates fall on a clock
  close, and also, silently, at the match's end with the caster alive; on the caster's death nothing
  falls.
- **12. No `fx.js` field** (§5c).
- **13. The head and the haft.** The vigil route `_fhPlated` becomes the square plated head (the gored
  sphere it drew was never on a shipped relic), and the haft's bands are gated on the vigil key.
- **14.** The ward's ring stands down while the shell stands, and is back the frame the plates crack.
- **15. The picture hangs off the fighter, never `m.ultFx`** (open item 25). It is driven in
  `tickPresentation`, which writes presentation fields, floats, tags and `taught` only. A slam is
  found by `ramTally.slams` rising, and its number is read off the slam's own `ram` beat.

### 5a. The picture (v72 §7.1; sheet `05-reference/v100/portcullis-picture-sheet.png`)

- **The cast — the shell.** The vigil ring thickens into a plated shell over 0.25s. The shell is a
  hexagon from R+2 to R+18 made of six six-sided plates, with `dark` edges and `core` seams. It
  thickens inward from the ward ring's own band (R+14..R+18). The plates' edges run lit and cool over
  0.4s, so the cast reads even on an empty pool: the pool is empty at most casts, and a 0.15 fill alone
  would not show the cast. The shell is drawn in the world pass, under both balls, so the health liquid
  is never covered and a slam never covers the foe's disc.
- **The fill is the pool: alpha 0.15 + 0.45 × shield / cap** (the design's 0 → 90 maps to 0.15 →
  0.6). On 4849 settled window frames the drawn alpha never left that line; it ran 0.150..0.581 over
  shield 0..86.2. On the pixels, the plate interior's lift against shield / cap gives r = 0.941 over
  44 frames. The probe asserts the same line on every settled frame (§5d).
- **The ward's ring stands down under the shell.** The shell is that ring, thickened. The ring comes
  back the frame the plates crack, because the bank outlives the window. This is a one-line replace
  in `_stWard`; the break, spend and expiry art are untouched.
- **The charge — the streak.** Five speed lines off the back of the ball. Their strength is the speed
  along the line to the foe (250..900 u/s), eased, so a ball knocked back by its own slam does not read
  as charging. No streak while pinned.
- **A slam.**
  - The struck plate flashes for 0.25s and its two neighbours at 0.45, because the foe's shell covers
    the struck plate.
  - A glint cross shows at the contact for 0.2s, with nine drawn sparks (shellHash, no rng).
  - The number is the slam beat's own damage, rounded, floated in vigil's glow and sized like a blow's
    float. A slam that rounds to 0 floats nothing.
  - The WARD tag ticks up to the pool the bank left: 8, 16, 24…
- **The close.** The six plates crack and fall as drawn debris and are gone in 0.3s.
- **The silhouette.**
  - The head is square and plated, in four plates, with studs and a boss: the only square head in the
    flail row. At the app's 453×805 it reads at 0.223, against 0.162 for the gored sphere it replaces.
    The flail row runs from 0.146 (Gravemourn, Slagheart) to 0.287 (Morningstar), so it sits mid-row.
  - The haft is banded: two bands in `core` over a `dark` underlay (0.158; the row runs 0.156..0.184).
- **The lab's numbers** (77 measured frames on 8 fights, 540×960, post chain on):
  - **Bloom.** The picture's share of the arena lift is at most +0.0000 (gate +0.02). The caster's
    disc peaks at 0.936 with or without the picture, and is above 0.90 on the same 4 of 77 frames
    either way. Controls: the fill drawn as a lighter glow disc takes the caster's disc to 1.000 (above
    0.90 on 35/53 frames) and fails; a lighter halo lifts the arena +0.0668 and fails.
  - **Legibility** (median |dL|): shell 0.122 (0.054..0.214), cast edges 0.219, streak 0.122 while
    charging, plate flash 0.189, sparks 0.178, number 0.215, WARD tag 0.229, falling plates 0.134,
    head 0.113, haft bands 0.163.
  - **Frame cost** (Electron 44 on the RTX 3070, interleaved A/B, machine loaded at 57-77 ms a
    frame): whole-frame medians are within the noise. The picture's own calls take 0.30 ms median
    (0.40 p90) with the shell up, and 0.40 / 0.50 ms at a slam and in the close. The square head costs
    0.10 ms against the gored head's 0.15.
  - **Drawn whole fights:** 10 fights, 0 throws, 37 windows. Each of the 151 slams was found exactly
    once. 149 WARD tags carry a number; the other 2 had the pool broken on the same step.

### 5b. The voice (v72 §7.2; `tools/portcullis_voice_lab.py`, wavs in `05-reference/v100/`, gitignored)

Each voice had 3 to 5 candidates, a written rule and tiebreak, and controls that must come back
wrong. All 14 controls did: BELL, NOHUM, CLANG, HELD, RC-NOW, PLAIN, LONG, FLAT, SPARK, LONG, TWO,
RING, TINK and LATE. Levels are solved against Portcullis's own blow (the hit @ 23).

- **The cast — BAR, of 5.** Until now `ult/portcullis` fell through to rune-crack. It is a stone
  thunk (600 Hz lowpass noise, 60 ms, dry), an iron bar struck on E4 (triangles on 1 : 2.76 : 5.40),
  and an A2-over-A1 hum that settles. It is audible for 400 ms. Its loudest 50 ms sit -2.7 dB re the
  blow; the hum is -6.2 dB under the clang, and the stone -9.0 dB. Register is at most 0.71 (against
  Paradox's cast) and 0.37 against rune-crack. GRILLE tied it and lost on calls.
- **A slam — TOM, of 4.** A held E2 sine and E3 triangle, cut together on a zero crossing at 0.194s,
  under a falling punch and a contact click.
  - **Louder with the shield:** the gain is a quadratic in the shield (clamped 0..90), solved so the
    peak is **0.350 / 0.427 / 0.500 / 0.574 / 0.650 at shield 0 / 22.5 / 45 / 67.5 / 90** (the design:
    0.35 → 0.65). The worst noise draw lands 0.011 off the line.
  - 0.84 of its power is below 120 Hz on the worst draw (the design: ≥ 0.45). It is gone by 200 ms
    (≤ 0.25s), within 6 dB of its loudest for 95% of its length, then cut in 10 ms (gated).
  - Register is at most 0.40. SINE lost the register tiebreak (0.50 against the cast); NOISE and STACK
    failed their gates.
- **A bank — LATCH, of 4, the new `ward-bank` kind.** A latch catching: C7 then E7, 35 ms apart,
  struck with a bar mode. It is audible for 65 ms. It lands on the slam's frame and stands +13.9 dB
  over the loudest (shield-90) slam in its own band. Its loudest 50 ms sit -9.3 dB re the blow.
  Register is at most 0.48, and 0.21 against the spark collect (the blessing's chime).
- **The close — FALL, of 3.** Three plate clinks, E6 / D6 / C6 at 0 / 0.10 / 0.23s, 50 ms each, all
  inside the picture's 0.3s fall. Register is at most 0.65.
- **In fights** (148, both sides × 37 foes): 148/148 identical, with every other voice call identical
  in order, kind and options.
  - 528 casts played 528 cast voices, and 2058 slams played 2058 slam voices (38% at shield 0).
  - 2058 banks played 2058 bank voices, 23 of them at the cap.
  - 439 clock closes played 439 close voices. The 16 windows closed by the caster's death and the 73
    ended by the fight played none.
  - The sim-write control came back 3/148 identical, so the check can fail.
  - In a real window (v Thornwake, 100602), each slam stands +7.5 to +57.7 dB over the fight and score
    in its band, each bank +19.7 to +48.1, and the close +31.1.

### 5c. No `fx.js` field — drawn sparks (Rick's to overrule)

The brief says "Field in both copies", and §7.1 says "spark motes off the plates on each slam, both
copies". **Both `fx.js` copies are untouched.** The picture lab measured why a SPECS field cannot be
that (`fieldprobe`, 24 fights, 12 foes, both sides: 82 windows, 324 slams):

- A SPECS row spawns once, on the cast edge of the one ultFx slot, at the caster, and lives only while
  that record lives. Portcullis's record lasts 0.75s, and less when the opponent's cast takes the slot,
  which happened in 52 of 82 windows.
- **Only 24 of 324 slams (7.4%) land while a field could be alive.** Slams land a median 4.43s after
  the cast (p10 0.98s, p90 8.18s), a median 184 units from where the field would spawn (p10 63, p90
  333). Only 28 of 324 land within 60 units of it.

So the sparks are drawn per slam instead: nine a slam, placed by shellHash, in the world pass over
both balls, as Zenith's embers and Canopy's leaves were drawn. This follows Zenith's and Canopy's
precedent, and it is Rick's to overrule.

### 5d. Stage 6's gates — every one able to fail

- **engine_ab sc-tendril-t3 → sc-onslaught-fx, ALL 38 WITH Portcullis, n=6: 4218/4218 identical**
  (703 pairings, 38/38 distinct winners; `runs/stage6_engine_ab38.txt`, ids in `runs/ids38.txt`).
- **portcullis_probe on sc-onslaught-fx: 11/11** (444 fights; `runs/stage6_probe.txt`). The probe
  reads stage 6 only when the link's own `SFX.play` carries the slam's voice.
  - **[1]-[9] match the digit** of the same probe on `sc-tendril-t3`, which scores 9/9 there with stage
    6 off (`runs/stage6_probe_base.txt`): 3.64 casts a fight; 3.85 slams, 17.38 damage and 30.28 banked
    a cast.
  - **[10] the voices.** 1616 casts played 1616 cast voices. 6226 slams played 6226 slam voices, each
    carrying the shield it hit for, then 6226 `ward-bank`s after them. 1328 clock closes were voiced,
    and 32 caster deaths stayed quiet. No Onslaught voice played anywhere else, the vigil blow's bank
    included. A ram frame's only hit voice is a ward's own shatter, a crit played inside `hurt` (110
    wards broken by a slam).
  - **[11] the picture.** 4,966,170 presentation ticks and 448,764 draws of `drawRam` / `drawRamTop`
    moved no sim state and drew no rng. The state checked is every fighter's body, ledger, statuses,
    window and tally, plus the match's clock, stop, verdict, beats and shots. Every slam was seen by
    the picture exactly once, and 2,948,822 settled shells sat exactly at fill 0.15 + 0.45 × shield /
    cap.
  - **Controls** (`runs/stage6_probe_mutants.txt`, 148 fights each):
    - a close voice on every close, deaths included, **fails [10]** 10 times and nothing else;
    - `foe.vx += 1e-9` in the picture's slam branch **fails [11]** 2070 times (every slam) and nothing
      else.
- **render_ab:** the other relics' pairs (paradox:heartwood:25064, twinshade:lastlight:991,
  bulwarden:vinesower:70707, axiom:grudgebearer:31337) are **24/24 pixel-identical**. The control,
  Portcullis v Grudgebearer 31337 at 6 / 17 / 19.5 / 33s (inside a window at 17, 19.5 and 33), is
  **0/4** (`runs/stage6_render_ab*.txt`).
- **chain_audit** `--relic sc-onslaught-fx --tip sc-onslaught-fx --builder portcullis_build.py`:
  **21/21 inserts survive**. The control against `sc-tendril-t3` finds the 13 stage-6 inserts LOST and
  exits 1 (`runs/stage6_chain_audit*.txt`).
- **tip_audit:** identical to `sc-tendril-t3`'s below the header. The Ward tip is unchanged, and the
  one field no tip mentions is still Burn's `feed` (`runs/stage6_tip_audit.txt`).
- **shell_identity on the carried `sc-onslaught-fx`** (`SWB_GAME`, the pointer not moved; the json
  restored): **200/200** (`runs/stage6_shell_identity.txt`).

## 6. The clip (Rick's to overrule)

`tools/_portcullis_pick.py` (`_ironwood_pick.py`'s shape) scores a window on §7:
- a close BY ITS CLOCK, 4 points: the only way to see the plates fall and hear the clinks;
- each slam, 0.5 (up to 8);
- each slam that floats a number, 0.4 (up to 6);
- the pool the fill reaches, 2 × shield / cap;
- the share of window frames the streak is lit, × 2.

**A clean frame comes first.** A window with the foe's own ultimate up on the clip (cast in the 8s
before it, inside it, or in the 1.8s tail) ranks below every clean one. The pick also leaves out the
vigil relics (the same pink on both balls) and the batch's redesigns still in flight (their fights
change when they are carried).

The clean-frame rule is a filter, not a weight, because the first two picks were filmed with a
1-point weight and both lost the frame:
- **Twinshade 100175**: Triplicate, cast 5s before the window, filled most of it with shades;
- **Thornshear 100212**: the Winnowing, cast on the close, took the tail and the falling plates.

Both films are kept in scratch and not in the repo; their tables are `runs/stage6_pick_first_*` and
`runs/stage6_pick_second_*`.

**The pick: Portcullis v Slagheart (Ironbloom), seed 100101.** The cast is at 31.62, and the window
runs 8.77s and closes by its clock. It holds 7 slams (4 floating a number), the pool reaching 48, the
streak lit on 9.4% of window frames, and no foe ultimate on the clip (`runs/stage6_pick.txt`).

    python cinema_clip.py --game <scratch>/batch/portcullis/links/sc-onslaught-fx.html \
      --a portcullis --b slagheart --seed 100101 --at 30.42 --window 11.77 --end-at-window \
      --fps 60 --w 540 --out ../07-shorts/v100/onslaught-window.mp4

**The film: 11.8s at 540×960, 60 fps** (yert's `--end-at-window`: the window and the fall, nothing
after; `runs/stage6_clip.txt`). The AAC's mean is -21.3 dB and its max -0.5 dB, with flat factor 0
(no clipped run). Five frames checked, all drawn through the pipeline with the post chain on:
- 31.8, the cast: the shell setting round the glass, the ONSLAUGHT banner, the first WARD 8;
- 32.9, the charge: the streak off the back of the ball, the square head and banded haft;
- 33.9, a slam: the glint, with WARD 8 over the caster;
- 38.9, a later slam: the lit shell in contact, WARD 8 again over the caster (the pool emptied and
  banked again), the exchange's numbers floating;
- 40.5, the close: the six plates cracked and falling, and the ward's ring back on the ball.

The mp4 is gitignored and sits in `07-shorts/v100/` on DESKTOP-DERRAFT; it has not been sent to Rick.

## 7. What is left, and whose

- **Rick:**
  - the clip, and the picture and voice picks (`05-reference/v100/portcullis-pick-sequence.wav` has
    the cast, three slams at shield 0 / 45 / 90 each with its bank, the close, then the flail's own
    blow for scale);
  - the drawn sparks in place of an `fx.js` field;
  - the new `ward-bank` voice: should every ward bank play it, not only Onslaught's, and should it
    stay silent at the cap?
  - the square head;
  - bows at 35% (item 12/32, from stage 5).
- **The app pointer** ("Move `GAME`", the brief's stage 6) waits for Rick, as the batch's others do.

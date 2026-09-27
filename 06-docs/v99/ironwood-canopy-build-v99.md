# v99 — IRONWOOD / CANOPY, BUILD. STAGES 1-6 DONE: the mechanism is the lab's, the gap measured to the clock, the knob moved and said (winDmg 0.38, blade 24: 50.1% both sides); the tree drawn and voiced, gated. Clip with Rick; the app pointer waits for him.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 04:07 UTC. Input: `06-docs/v69/IRONWOOD-BUILD-BRIEF.md` +
`verdant-warhammer-design-v69.md`. A NEW relic (verdant x warhammer), the 36th built. Base: the chain tip
(`sc-zenith`). Builder `tools/ironwood_build.py`, probe `tools/ironwood_probe.py`, runs in `runs/ironwood/`.
Nothing here is a design decision (CLAUDE.md §3 rule 0); where the build had to read the docs, the
reading is written down (§1).

## 0. What this build stands on

- **The relic count.** The chain carries 35 relics (Morningstar is the 35th), so Ironwood is the 36th, as
  the brief says. The brief counted Bindweed there; it is not built.
- **Rick's veto: waived for the batch** (CLAIMS.md, the batch ruling). **The charge: the game's
  equivalent** (Rick, 2026-09-27). Measured for this fighter on arm D (660 fights, `runs/ironwood/s0_freeze_2207`):
  13.0% of the lab's steps are frozen (17.0% inside windows, 10.2% outside), so the lab's 16 is the
  engine's 13.9, and 14.
- **Stage 0 on Chromium 151** (below) reproduces the published arms on 141.

## 1. Stages 1-4

```
sc-zenith-fx.html  the base: the chain tip (Zenith stage 6)
stage 1  sc-ironwood     15412f14b27734cc   the row after Morningstar: Grudgebearer's hammer profile, dmg 23.5,
                                            verdant, onHit entangle 2, the card (70), ultimate stubbed at 1e9
stage 2  sc-rooted       4c3d5bbb6f2a1980   the root, the growth, the wither; the bough and damage machinery
                                            wired at boughs 1 / winDmg 1 (inert); charge 14
stage 3  sc-boughs       3747b833fca3730a   boughs 3, winDmg 0.35
stage 4  sc-canopy       b1a5637ba066b60a   canopy 1
stage 5  sc-canopy-w38   13f8d25aa7ebe34a   winDmg 0.35 -> 0.38 (the build's knob), blade 23.5 -> 24
stage 6  sc-canopy-fx    717c7bbda9469cf6   the picture and the voice
```

**Carried onto the new tip.** Stages 1-4 were first built on `sc-zenith`; Zenith's stage 6 landed
while they were measured, so they were rebuilt on `sc-zenith-fx` with the same builder. **engine_ab,
the first `sc-canopy` against the rebuilt one, all 36 relics WITH Ironwood, n=6: 3780/3780
identical** (`runs/ironwood/carry_engine_ab36.txt`). Every number below carries over.

What stage 2 adds, all on the window tickers' clock:
- **The cast** (`kind:"tree"`, returns before the generic tail): `ultTree = {t, dur, cd, sprouted}`,
  `pinV = [0,0]`, `pin = pinMax = dur`, `pinFree = 1`.
- **`tickTree`**, after `tickSun`: re-arms `pin` and `pinFree` every frame; `reachMul += 0.35 x dt` to
  2.5; at 1.5s the blade set becomes `[0, 1/3, 2/3]` with two new ribbons and clear cooldowns; the canopy
  applies entangle every 0.5s to a foe within reach x mods.reach x reachMul + R. On close (the clock, or the
  caster's death): the blade set and the extra ribbons go, reach returns to 1, the roots let go (a live
  caster to rest; a dead one keeps its kill flight), and 0.4s of wither begins.
- **`bladeSegments` and `drawWeapon`** read `f.bladeSet || f.w.blades`: the shared weapon is never written.
- **`resolveHit`'s damage line**: `(self.ultTree ? self.w.dmg * self.w.ult.winDmg : self.w.dmg) * ...`,
  ahead of the jitter, the crit and the rounding, where the lab scaled `w.dmg`.
- **`tickCharge`**: a cast waits for `!f.ultTree && !f.treeWither`. It cannot bind at charge 14.

The readings, each in the builder's docstring:
1. **The sprout is the prose's**, at 1.5s. The lab gave all three boughs at the cast.
2. **The shared weapon is never mutated** (the brief). `w` is shared by the mirror match.
3. **The 0.35 sits inside the product**, so a blow is bit-identical to the lab's scaled `w.dmg`.
4. **The root re-arms `pinFree` as well as `pin`.** Ravelbone's wire clears `pinFree` on its quarry; with
   only the pin re-armed, `tickStasis` would lock the weapon for the rest of the window, and the prose
   says it keeps turning.
5. **The window closes on the caster's death** (the prose), not the foe's (the lab). A dying caster keeps its
   kill-flight velocity (the engine's rule).
6. **A new bough's cooldown starts clear.** The lab left the last window's value in the slot.
7. **The canopy's source is a side letter** (the engine's contract). Entangle has no reader of its source.
8. **The growth is linear**, as priced.
9. **The wither is a picture after a mechanical close.** Its wait cannot bind at 14 against 8.4.

## 2. Stage 0 and the stages against it

`ult_overlay.py --game ../02-chain/sc-zenith.html --relic grudgebearer --cell verdant:warhammer
--mech overlays/tree.js --P boughs=3 growCap=2.5 winDmg=0.35 --seeds 20 --foes <33>`, seed0 2207 and
2317, 660 fights an arm a block. The foes are the published 33 (every relic but the donor on the 34-relic
chain), so Morningstar is not one. Arm C1 is `--arms C --P boughs=1 growCap=2.5` (winDmg left at 1), the
stage-2 reference; the brief's 26% was at cap 3.0. The built links run `--relic ironwood --arms SHIP`
on the same foes and seeds.

```
                          lab on 151 (block 1 / 2)   published 141   BUILT (block 1 / 2)        pooled
A   no ultimate           16.1 / 14.8                14.5            stage 1: 16.1 / 14.8       identical, fight for fight
C1  root + growth         26.5 / 27.0                (26.1 at 3.0)   stage 2: 24.7 / 26.8       25.8 (lab 26.8)
C   + three boughs        45.3 / 45.2                48.2            stage 3: 42.6 / 42.4       42.5 (lab 45.3)
D   + the canopy          46.2 / 48.3                47.1            stage 4: 40.2 / 38.9       39.6 (lab 47.3)
```

Lab mechanism on 151 (arm D): 3.76 casts; 17.8 blows in windows and 7.8 outside a fight; the foe under
the canopy 40.4% of window frames; 3.25 entangle stacks on an average window frame; 7.8 applications a
cast; growth peak 2.46.

## 3. The probe (`ironwood_probe.py`, one check per sentence, read inside the hooks)

- **sc-rooted: 10/10** (420 fights, every foe, both sides). The rooted ball moved on 0.00% of window-frame
  pairs; released to rest every time; reach peaks 2.49 a cast; 3.39 casts a fight; every blow rebuilt
  exactly from its captured crit and jitter draws.
- **sc-canopy: 10/10.** 3.78 casts; 18.9 blows in windows and 7.0 outside; the foe under the canopy 36.4%
  of window frames; 7.44 applications a cast; 3.14 stacks on an average window frame; growth peak 2.49.
  **Freeze census (v67): 16.6% of window steps frozen** (the lab's: 17.0%).

The mechanism reproduces the lab's. The win rate at stage 4 does not, and §4 is where that is measured.

## 4. The gap at stages 3 and 4 — measured to the clock

The mechanism reproduces, the win rate does not: at stage 4 the built relic reads 7.7 points under
arm D. Four blocks (2207, 2317, 2427, 2537), side A, the lab's 33 foes, 660 fights an arm a block:

```
                     block 1   block 2   block 3   block 4   pooled   what the canopy adds
lab C                45.3      45.2      46.5      45.3      45.6
lab D                46.2      48.3      50.8      49.2      48.6     +3.0
built stage 3        42.6      42.4      44.1      43.0      43.0
built stage 4        40.2      38.9      41.2      44.8      41.3     -1.8
```

Controls, each a scratch copy of a built link with one thing changed (blocks 2207 and 2317;
`runs/ironwood/ctl_*`):

```
the boughs at the cast (sprout 0), stage 3          54.8 / 55.9   55.4   the prose's 1.5s sprout is worth -12.9
the lab's C with the engine's window (dur 9.6)      53.8 / 55.2   54.5   the engine's window is worth ~+9
the lab's D at dur 9.6                              57.3 / 57.0   57.2   the lab's canopy at 9.6: +2.7
the boughs at the cast, stage 4                     53.8 / 52.9   53.4   the build's canopy: -2.0
stage 4, the entangle's source a Fighter (the lab's) 40.2 / 38.9  39.6   the same fights: the source is inert
stage 4, the canopy's clock running through freezes  44.7 / 44.1  44.4   +4.9; the canopy then adds +1.9 (lab +2.0)
```

**The whole gap is clocks, and nothing is mis-built:**
1. **The window.** The engine's 8s are 8 seconds of the window tickers' clock, which stops in a hit
   stop; 16.6% of window steps are frozen here, so a window is ~9.6s of match time. The lab's 8s
   were 8 step-seconds, frozen ones included. With the boughs at the cast, the build reproduces the
   lab run at dur 9.6 (55.4 against 54.5). Worth about +9.
2. **The sprout.** The prose sprouts the two boughs at 1.5s; the lab gave all three at the cast.
   Worth about -13. At stage 3 these two nearly cancel (43.0 against 45.6).
3. **The canopy's cadence.** The lab's canopy cooldown ran through hit stops and could apply during
   one; the engine's runs on the window clock. Worth about -5: with the lab's clock the build's
   canopy adds +1.9, as the lab's does.

**What the build does with it.** It keeps the engine's convention: every window cadence in the batch
runs on the window tickers' clock (Corollary, Daybreak, Zenith), and a freeze freezes the world.
It keeps every designed number. Rick's batch ruling converted the charge; the weapons were kept "as
designed". The shortfall is then priced at stage 5 with the lever the brief gives the build for
exactly this: "if the pinned runtime reads out of band, move `winDmg` inside 0.30-0.40 first, and
say so." It is said here.

## 5. Stage 5: the bough scale and the blade — winDmg 0.38, blade 24

Both sides (`relic_rate.py`: each seed played from both sides; every other relic a foe, 10 seeds a
foe a side, 700 fights a block; seed0 2207 and 2317; `runs/ironwood/stage5_rr_*`):

```
winDmg   blade   block 1   block 2   pooled (1400)   side A   side B
0.35     23.5    45.1      43.7      44.4            44.1     44.7
0.35     24.5    46.1      47.0      46.6            46.7     46.4
0.35     25      50.0      49.9      49.9            52.3     47.6
0.38     23.5    48.9      49.0      48.9            49.4     48.4
0.38     24      50.3      49.9      50.1            50.0     50.1
0.38     24.5    52.3      53.4      52.9            54.1     51.6
```

- **At the designed 0.35 the crossing is blade ~25.0** (49.9% there), outside the brief's 23.5-24.5.
- **At 0.38 it is 24.0**, where design §5 puts it ("the crossing is near 24"), and the smallest
  measured move of the knob that puts it inside the band. Side A and side B agree (50.0 / 50.1).
- The side-A lab runs agree: at 0.38, 23.5 → 49.8 / 52.3, 24 → 53.2 / 50.5, 24.5 → 55.6 / 52.0; at
  0.40 the crossing falls under 23.5 (23.5 → 52.3 / 51.8). The knob is steep: about 2.5 points
  per 0.01, twice the lab's, because the engine's window holds more bough blows.
- **The built link is the measured relic:** `relic_rate` on `sc-canopy-w38` with no knob set gives
  block 2207 exactly (50.3%, every foe, the mean duration to the digit).
- **The probe on sc-canopy-w38: 10/10** (`runs/ironwood/probe_w38.txt`): 3.67 casts; 18.5 blows in windows and
  6.7 outside; the canopy 35.6%; 7.28 applications a cast; 3.10 stacks; 16.5% of window steps frozen.
- **Probe controls** (`runs/ironwood/probe_mutants.txt`): full damage in the window fails [6] (793 times);
  a close that leaves velocity fails [2]; a Fighter as the canopy's source fails [7]; a sprout 0.1s
  early fails [5]; growth 1% fast fails [4]. Each fails its own check and only that one.

- **verify --n 40 on sc-canopy-w38 (36 relics): 11/13** (`runs/ironwood/verify_w38.txt`). Ironwood
  48.7% (side B, as verify plays an appended relic); every relic in 30-70% (Heartwood 32.3 ..
  Gloamwire 64.1, spread 31.8pp); "both sides can win every matchup" passes; both reds are the
  clock bands, as on every link since the minute pace.
- **engine_ab sc-zenith-fx → sc-canopy, the 35 others, n=8: 4760/4760 identical**
  (`runs/ironwood/stage4_engine_ab35.txt`); stage 5 edits only Ironwood's own row.

**The ladder at 0.38 / 24** (40 fights a foe, `runs/ironwood/ladder_w38.txt`), which the brief asks to print:
greatsword 76%, flail 46, scythe 46, bow 45, warhammer 44, twinblade 36. Worst Bloodmirror 5%,
Twinshade 7.5, Cindercleave 25; best Axiom 97.5, Lastlight and Heartwood 90. The design predicted
this shape (greatsword 86, Bloodmirror 0, Twinshade 15): a rooted tree cannot leave a standing
hazard. **The 40-point type spread and Bloodmirror are item 12/32, Rick's**, not this build's.

## 6. Stage 6: the picture and the voice — `sc-canopy-fx`

Picked on measurements under Rick's "you pick i overrule", by two labs run in parallel (the picture
lab's scratch and `tools/ironwood_voice_lab.py`), and built as `ironwood_build.py --stage 6`: fourteen
anchored edits, byte-exact to the labs' own row files. The picture rows alone reproduce the picture
lab's stamp (65dcbc1ef80ccf97). The sheet is `05-reference/v99/ironwood-picture-sheet.png`.

**The picture** (v69 §7.1):
- **The cast:** bark plates climb the shell (#0D3A1A plates, #4FD06B seams), and three roots drop
  to the floor. The ball is in mid-air on most casts (a median 135 units up), so the roots are aerial
  roots, dropped the whole way like a banyan's: the ball stands on them. At the close they let go and
  shrink back into the shell.
- **The bark over the health:** one opaque layer hid the liquid level, so the plates are 0.86 over
  the headspace and 0.5 over the liquid. The level reads as sap glowing through the bark and keeps
  43% of its contrast.
- **The trunk and the burl:** the haft thickens into a trunk as reach grows, and the head stays a
  33.5-unit burl at every growth (the shipped `_whGrown` stretched it to 103 at full size).
- **The sprout:** the two boughs are drawn growing over 0.5s, ending in lighter burls. A bough that
  strikes or clanks while drawn short snaps whole on that frame: 246 of 246 contacts inside a sprout
  were drawn whole (218 would have been short without the snap).
- **The canopy:** the 0.06 glow disc at the canopy's own radius, with an edge of leaves; ENTANGLE
  and its count tag the foe once a stretch under it (Corona's, Daybreak's and Zenith's rule).
- **The wither:** the boughs draw back as dead, dry wood under the live hammer, which is drawn at its
  tested reach (the close restores one blade and reach 1 at once); bark falls as drawn debris.
- **The silhouette:** the resting verdant hammer, the first `_whGrown` ever drawn, reads at the app's
  size (head |dL| 0.202, mid-row among the hammers).
- **Drawn leaves, no `fx.js` field** (Zenith's precedent): a SPECS field lives on the one ultFx slot,
  is gone about 3 seconds into the window, loses the slot to the opponent's cast in 67% of windows,
  and can only spawn at the rooted ball, while the bough tips are 137-243 units away. The leaves are
  shed off the burls for the whole window, in the world pass. **Rick's to overrule.**
- **Frame cost, and the glow cache:** the tree draws its own halo and bypasses `weaponGlow`, which
  rebaked 107-112 shadow sprites a window under continuous growth. Three boughs growing: the
  caster's weapon 1.4-1.8 ms against the base's 13.9-18.7; the whole frame 30.5-36.9 ms against
  44.2-54.3 (Electron 44, RTX 3070, interleaved A/B on a machine at ~90% CPU).

**The voice** (v69 §7.2; wavs in `05-reference/v99/`, gitignored):
- **Cast — BEAM:** a ground-thud (72 → 28 Hz) and a pulsed timber creak; 0.60 of its power below
  120 Hz on every noise draw (the design's gate 0.5); -2.9 dB against the blow.
- **Sprout — BLOCK:** two woody cracks, A then E a fifth up, 90 ms apart, 80/75 ms each, on the
  frame the boughs appear.
- **A bough blow — PITCH:** the hammer's own strike, rebuilt from dmg / 0.38 and pitched down a
  fourth (-486 / -501 cents), peak 0.44 of the hammer's (0.55 at the worst draw; gate 0.6). Without
  it a bough blow played the plain hit at 9, pitched UP (+286 cents). `resolveHit` hands the hit
  voice one plain number more, `bough`, while the tree stands.
- **Wither — BEAM:** a dry creak falling -861 cents over 360 ms, only on a clock close with the
  caster alive.

### 6a. Stage 6's gates — every one able to fail

- **engine_ab sc-canopy-w38 → sc-canopy-fx, ALL 36 WITH Ironwood, n=8: 5040/5040 identical**
  (`runs/ironwood/stage6_engine_ab36.txt`).
- **ironwood_probe: 11/11** (`runs/ironwood/stage6_probe.txt`), stage 5's numbers to the digit, plus
  [11]: one sprout voice a sprout (1502), one wither voice a clock close (1313) and none on a death,
  and `bough` on the hit voice exactly while the tree stands (7777 bough blows, 2831 hammer blows; a
  blow that breaks a ward plays the ward's own shatter voice first). **Controls:** `bough` on every
  Ironwood blow fails [11] (957 times); a wither voice on every close fails [11] on the deaths
  (`runs/ironwood/stage6_probe_mutants.txt`).
- **render_ab:** the other relics' pairs **24/24 pixel-identical**; the control, Ironwood v
  Grudgebearer 31337, **0/4**.
- **shell_identity on sc-canopy-fx** (`SWB_GAME`, the pointer not moved; the json restored):
  **200/200**.
- **chain_audit:** ironwood_build 27/27 at sc-canopy-fx; morningstar_build 20/20, dawn_build
  17/17, corollary_build 25/25 → sc-canopy-fx. **tip_audit:** identical to sc-zenith-fx's.
- **The picture lab's own gates:** Canopy's share of the arena lift max +0.0000 (gate +0.02); no
  ball's disc moves more than 0.0011; the caster's disc darkens under the bark (0.469 → 0.396) and
  never passes 0.90. The control, the canopy filled at 0.35 in lighter, lifts +0.082 and puts the
  caster's disc past 0.90: it fails. Sim identity on 10 whole fights with a 1e-9 sim-write control
  that differs on all 8 Ironwood fights.

## 7. The clip (Rick's to overrule)

`tools/_ironwood_pick.py` scores a window on §7: it must close by its clock (the only way to see the
wither), with the sprout, bough blows, the foe under the canopy and its stacks. The pick:
**Ironwood v Slagheart (Ironbloom), seed 99249**, cast at 47.88: the foe under the canopy 80% of the
window and entering it 7 times, 13 entangle applications, 9 blows.

    python cinema_clip.py --game ../02-chain/sc-canopy-fx.html --a ironwood --b slagheart \
      --seed 99249 --at 46.68 --window 12.93 --end-at-window --fps 60 --w 540 \
      --out ../07-shorts/v99/canopy-window.mp4

16.0s (yert's `--end-at-window`: the window and the wither, nothing after), AAC mean -22.7 dB, max
-1.6 dB. Slagheart casts Ironbloom on the first frame. Sent to Rick 2026-09-27.

## 8. What is left, and whose

- **Rick:** the clip; the picture and voice picks; the drawn leaves in place of an `fx.js` field;
  the aerial roots; the bark over the health.
- **The app pointer** stays on `sc-leaf` until Rick has nothing to overrule on the batch's clips.
- **Portcullis (v100) is carried onto `sc-canopy-fx`**, with engine_ab against its first build.

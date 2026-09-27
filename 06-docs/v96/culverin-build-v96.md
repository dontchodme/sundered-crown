# v96 — CULVERIN / IRONFALL, BUILD. IN PROGRESS — stages 0-5 built and gated (blade 13.5, measured); stage 6 (picture, voice, field, the carry) next. Claude Code on yert, claimed 2026-09-27 03:25 UTC. Do not build this cell elsewhere.

The staff row's first build, and the type with it (`shape:"staff"`, the pole).
Input: `CULVERIN-BUILD-BRIEF.md` + `dwarven-staff-design-v96.md` (this folder),
`06-docs/v89/STAFF-ROW-v89.md` §1/§6, `06-docs/v89/staff-art-v89.md` and
`staff_spec.js`. Rick, 2026-09-27, on yert: *"staff is in the repo. lets build
it"*, read as the row accepted whole. Builder `tools/culverin_build.py`, probe
`tools/culverin_probe.py`, paint gate `tools/staff_paint_gate.py`, win rates
`tools/relic_rate.py` (both sides, live knobs; written for all seven staves).
Runs in `runs/build/`.

```
sc-leaf.html            the base: the build of record, what the row was priced on
  -> sc-culverin.html      stage 1  the relic, ult stubbed, the bow's arrow   1e0c53387b7b04b7
  -> sc-slug.html          stage 2  the spell: SLUG                            141e7ea709682074
  -> sc-ironfall.html      stage 3  the ultimate: IRONFALL, charge 14          8751e32b0956fab0
  -> sc-ironfall-blade.html stage 5 the blade: 13 -> 13.5, measured          a0e7ed9f9f853c8b
```

**A BRANCH, AND IT SAYS SO.** The design batch builds its own line off
`sc-leaf` on DESKTOP-DERRAFT (`sc-leaf` → … → `sc-dawn`). Every anchor in
`culverin_build.py` is chosen to hold on that line too, and the builder accepts
either base and names it, so the lines meet by re-running it with `--src` on the
other tip. **This line does not move `GAME`** until that carry is made.

## 0. Stage 0: the control on 151

`ult_overlay.py --relic ironhail --cell dwarven:staff --mech overlays/staff_dwarf.js
--arms A,S,U --P blade=13 every=1.0 sMul=1.3 popR=90 --seeds 20`, two blocks:

```
arm              published 141 (660)   151 block 2207   block 2427   pooled
A  bow body          22.3%                20.2             17.3        18.8
S  slug              24.1%                25.5             22.0        23.8
U  + Ironfall        47.9%                48.5             49.7        49.1
   shells/cast        7.32                 7.33             7.30
   blows/window       2.80                 2.80             2.81
   foe sunder         3.11                 3.11             3.09
```

The mechanism reproduces to the digit; the win rates within the tier.

## 1. Stage 1: the relic, the art, the glow — `sc-culverin.html`

Five anchored edits: Cowork's `STAFF` object pasted byte for byte before
`SHAPES` (all 21 heads — **Rick's letters are owed** and land by editing
`STAFF.pick`; default A); `SHAPES.staff`; `weaponGlow` sized per shape
(`GLOW_EXT.staff = 2.0`); Culverin appended, the bow's physics and arrow
asserted off Ironhail, blade 13, Ironfall stubbed at `charge:1e9` with the
design's 70-character card.

- **Reproduces the lab's arm A TO THE FIGHT**: on the lab's seeds the built relic
  wins 133/660, 17.589 blows a fight, all 33 foes identical
  (`stage1_armA_2207`). Both sides, 680 fights: 20.4% (A 19.4 / B 21.5).
- **engine_ab sc-leaf → sc-culverin, the 34, n=10: 5610/5610 identical.**
- **Paint gate 21/21**: every candidate head drawn by the build is
  pixel-identical to the spec injected over the same page.
- **THE GLOW WAS CLIPPED AND THE CONCEPT SHEET COULD NOT SHOW IT.** `drawWeapon`
  draws a pre-blurred glow sprite sized at 1.15 L; the staff draws to ~1.9 L.
  At 1.15 L a staff lost 2.0-8.3% of its glow with alpha on the sprite's far
  edge (a hard cut across the head); at 2.0 L, 0.0%. The bow loses nothing
  either way (the control). The lab draws through `litWeapon` alone, which is
  why the sheet never showed it. `05-reference/v96/staff-spin-stage1.png` is
  all seven at eight facings as `drawWeapon` draws them.
- tip_audit: nothing new. **verify --n 40: 10/13** — Culverin 19.3%, the body with
  no ultimate and the bow's arrow (the design's arm A, ~20%), plus the two known
  clock bands. "Both sides can win every matchup" passes even here.

## 2. Stage 2: the spell — `sc-slug.html`

The shot block becomes the slug (`cadence 0.55, speed 470, r 28, life 3.0,
grav 700, dmgMul 1.6`, tip "Lobs a heavy slug that falls · clankable", 40).
No engine change: every field is one `spawnShot` already copies.

- **Reproduces the lab's arm S TO THE FIGHT** on both blocks: 25.5% / 22.0%,
  14.12 / 13.99 blows a fight — the stage-0 numbers exactly. (The lab ran the
  relic as side A, where `fireCd` starts at 0 whatever the cadence; as side B
  the first slug comes at 0.275s instead of 0.17s. Nothing the lab measured.)
- **Probe 6/6** (136 fights): cadence exact on 10,471 looses; vy grows by
  exactly 700·dt on 398,222 moving slug-steps and not on 37,185 frozen ones;
  no slug bounces; 782 batted mid-hall; **13.65 blows a fight** (7.19 slugs).
- **26% of slugs are spent on the step they leave** (7,728 of 10,471 are seen
  alive after one step) — loosed into the floor or a near wall from `R + reach`
  with r 28. The design's own sentence ("a slug fired downward hits the floor
  and dies") and the lab's behaviour; worth knowing when the picture is judged.
- **engine_ab sc-culverin → sc-slug, the 34, n=10: 5610/5610 identical.**
- **verify --n 40: 10/13** — Culverin 22.4% with the spell and no ultimate (the
  design's arm S, ~24%), and the two clock bands.
- The slug is filmed in stage 3's clip (§3d), drawn as what it is from there on.

## 3. Stage 3: IRONFALL — `sc-ironfall.html`

`culverin_build.py --stage 3`: eight anchored edits, every anchor checked unique
on BOTH lines (sc-slug and the batch's sc-dawn):
- the ult block live: `charge 14, kind "ironfall", dur 8, every 1.0, T 0.85,
  g 1000, shellR 26, shellMul 1.3, popDmg 8, popR 90`, the design's card; the
  builder refuses to write unless the shipped block carries every number the
  run printed (v56);
- `f.ultIronfall` / `f.ironTally` on the fighter; the cast branch (opens the
  window, resolves nothing; `m.ultFx` carries only the cast flash);
- `tickIronfall` beside the window tickers, after `tickShots` — a shell from the
  caster's centre with the velocity solved for the foe's lead point `T` out
  under `g`, `life T`, the engine's own shard pop to burst it. Declined at
  `maxLive`, never shifted, and `next` not advanced — the lab's rule;
- **one engine line beyond the brief**: `spawnShot` copies an optional
  `shot.spell` onto the shot, because a shot carries no handle on its relic and
  the renderer has to tell a slug from an arrow. Set only when the block names
  one, so every other relic's shots are the objects they always were;
- `drawShots` first cuts: the slug as a dull iron ball with a faint shimmer (no
  streak — the streak says "straight line"), the shell as iron with a hot seam
  and a derived ember trail, and **the landing ring** at `popR`, a pure function
  of the shell's state. Without the shell branch the shell would have drawn as
  Ironbloom's shrapnel, because it carries `shard` for the pop.

### 3a. The charge, converted — measured, not assumed

The design priced charge 16 on the lab's step clock, which counts hit-stop
freezes; the engine charges in unfrozen time only. The design batch's ruling
(Rick, 2026-09-27: "use the game's equivalent") applies by the same argument,
because the staff row was priced on the same harness. **On the lab's own seeds
and field** (side A, 33 foes x 20, `culverin_probe --lab`):

```
                    casts/fight   win     shells/cast   blows/window   foe sunder
lab, 16 (its clock)    2.87       48.5%      7.33           2.80           3.11
engine 14              2.93       49.7%      7.26           3.16           2.92
engine 15              2.75       45.9%      7.28           3.07           2.87
engine 16              2.56       44.4%      7.23           3.13           2.96
```

**14 is the equivalent** — the same conversion Corollary and Daybreak found —
and on the same fights the relic reads 49.7% against the lab's 48.5%. Blows in a
window run high (3.16 against 2.80) because the window is 8s of unfrozen time,
a little longer in wall time than the lab's.

### 3b. The probe, 15/15 (`stage3_probe.txt`, 136 fights, both sides)

Every shell leaves as solved (2,784 of 2,784: life T, the shell's numbers, the
foe's lead point at that instant, the velocity for it); 7.25 shells a cast, 0
declined; 3.18 blows a window; the foe at 2.99 sunder on a window frame; the
window never outlives 8s (longest 7.992) and closes on a death; 384 ult beats
for 384 casts; **14 kills by a shell or a burst, all 14 with a fatal beat**; the
render path CALLED on 6,363 frames (slug, shell and ring, the staff).

**WHERE THE SHELLS GO**, which is the design's "the lead is kept because it is
worse" as a count: in flight onto the foe **16%**, batted or eaten **21%**,
burst at the mark **7%** (10 of 187 bursts caught anybody), and **56% on a
wall** — a lead of `v_foe x 0.85s` is often outside a hall 520 wide. And 26% of
slugs are spent on the step they leave (§2). Both are the design's behaviour
and the lab's, and both are the first things to look at when the picture is
judged: most of what this relic throws dies on stone.

### 3c. The gates, and the relic at blade 13

**engine_ab sc-slug → sc-ironfall, the 34, n=10: 5610/5610 identical** — the
`spell` line in `spawnShot`, the cast branch and `tickIronfall` move no other
relic. **verify --n 40: 11/13, both reds the known clock bands**
(Farwarden/Starwarden 99.7s; overall mean 60.4s) and **every relic in
30-70%** (Culverin 44.6% as side B in every pairing).

Both sides, all 34 foes:

47.9% (block 2207) and 47.2% (block 5003), 680 fights each — the brief's
"relic ~48%". By type: flail 65, warhammer 55, scythe 48, bow 49, twinblade 40,
greatsword 36 (the design's: 56 / 50 / 56 / 47 / 48 / 34).

### 3d. Filmed

`_culverin_pick.py` scores windows on shells landing, bursts landing and
wall-splats; the top one is **culverin vs heartwood, seed 3301, from 30.6s**.
`07-shorts/v96/ironfall-window-cut.mp4` (11.5s, trimmed from the tool's
34.6s: `cinema_clip --at` treats `--window` as a capture cap and films on to
the end or the cap). Stills: `05-reference/v96/ironfall-window-strip.png`,
`ironfall-frames-3.png`. First cuts, for Rick's eye (rule 2).

## 5. Stage 5: the blade — 13 → 13.5, `sc-ironfall-blade.html`

Wide on 151, on `sc-ironfall` at charge 14 (`relic_rate.py --set dmg=...`):
both sides of every pairing, all 34 foes, two seed blocks, 2040 fights a point,
no bisection.

```
blade   pooled (2040)   block 2207   block 5003   side A   side B
13.0       45.7%          44.8%        46.7%       47.2%    44.3%
13.25      47.9%          47.7%        48.0%       48.6%    47.2%
13.5       49.4%          48.6%        50.1%       51.5%    47.3%
13.75      51.3%          53.2%        49.3%       52.6%    49.9%
```

**13.5 ships**: the measured row nearest 50% whose blocks agree. 13.75's came
back 3.9 points apart, which is more than the difference being decided. The
honest precision is 13.5–13.75, the brief's "expect 13–13.5 on 151" holds, and
the number is **PROVISIONAL**: v89 §8.2 re-prices the row against all seven
staves before any blade is called settled. It lives in
`culverin_build.TUNED_BLADE`.

**The ladder at 13.5** (by the foe's type): flail 62, scythe 56, warhammer 53,
bow 51, twinblade 47, **greatsword 34** — against the design's 56 / 56 / 50 /
47 / 48 / 34. Worst Lightkeeper 20, Axiom 27, Spellbreaker 27; best Vinesower
73, Thornwake 70, Censer 67. Greatswords are the row's counter as the design
said (open decision 4, Rick's).

**THE SIDES DIFFER BY ABOUT FOUR POINTS**, A ahead of B at every blade (1.4 to
4.2). `verify` pairs `i < j`, so an appended relic is side B in all of its
pairings and will read this relic a little low; the lab ran side A only.

On the blade link: **probe 15/15**; **engine_ab sc-ironfall → sc-ironfall-blade, the 34:
5610/5610**; **verify --n 40: 11/13, both reds the clock bands**, every relic in
30-70% (Heartwood 36.6 .. Gloamwire 63.7, spread 27.1pp), Culverin 48.5% as
side B in every pairing.

## Open (Rick's)

1. **The seven staff letters** (`05-reference/v89/staff-sheet.png`).
2. **The sim reach**: the picture's head sits at 1.6-1.9 reaches and the hit
   segment at the bow's 54. Built at the priced 54.

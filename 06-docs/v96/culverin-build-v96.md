# v96 — CULVERIN / IRONFALL, BUILD. IN PROGRESS — stages 0-2 built and gated; stage 3 (Ironfall) next. Claude Code on yert, claimed 2026-09-27 03:25 UTC. Do not build this cell elsewhere.

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
- tip_audit: nothing new. **verify --n 40 was still running at commit** (`stage1_verify.txt`).

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
- **engine_ab sc-culverin → sc-slug was re-running at commit** (the first run
  was stopped when the link was rebuilt for a comment fix).
- **NOT FILMED YET** — the brief's stage-2 FILM (a slug arcing and dropping).

## 3. Next

Stage 3, Ironfall: `f.ultIronfall`, `tickIronfall` after `tickWinnow` (both
lines share that anchor), shells pushed as the lab pushes them, the landing
ring, and the charge converted to the game's clock per the batch ruling
(measure the built relic's casts a fight against the lab's 2.88 at 14/15/16).
Then FILM, stage 5 (blade, wide, both sides, two blocks) and stage 6.

## Open (Rick's)

1. **The seven staff letters** (`05-reference/v89/staff-sheet.png`).
2. **The sim reach**: the picture's head sits at 1.6-1.9 reaches and the hit
   segment at the bow's 54. Built at the priced 54.

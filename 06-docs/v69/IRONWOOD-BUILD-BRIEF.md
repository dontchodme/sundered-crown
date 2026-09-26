# IRONWOOD / CANOPY — BUILD BRIEF (v69). The verdant warhammer, the 36th relic.

**Cowork, 2026-09-26. DESIGNED. Build from this file and
`verdant-warhammer-design-v69.md`; do not design (CLAUDE.md §3 rule 0).**
The build owns the blade (stage 5) and may move the bough damage scale
inside 0.30–0.40 first. Claimed in `06-docs/CLAIMS.md`. **Rick's veto of
the cell comes before stage 1 — check CLAIMS.md.**

## 0. THE RELIC AND THE NUMBERS

> For a duration the hammer takes root: the ball stops where it stands and
> grows bark — it cannot be moved or knocked but it can still swing — and
> the haft grows into a bough, then two more boughs grow from the trunk, so
> three lighter heads sweep the hall at up to two and a half times the
> hammer's reach. Anyone under the canopy is entangled. When it ends the
> tree withers back to a hammer and the roots let go.

```
the cell            verdant x warhammer            Cowork (v68 table, second least-decided)
the fighter         IRONWOOD                        Cowork, from four
the ultimate        CANOPY                          Cowork, from four
the card            "Takes root and grows three sweeping boughs. Foes beneath them entangle"   70
the blade           dmg ~24 (stage 5)               Grudgebearer's hammer profile otherwise
the channel         onHit {entangle: 2}
the window          8s, cast every 16s
the self-root       f.pin on the caster, pinFree 1, re-armed each frame; released to REST on close
the growth          reachMul eased at 0.35/s to 2.5; back to 1 on close
the boughs          w.blades [0, 1/3, 2/3] for the window (tips/hitCd sized 3); blows at dmg x 0.35 while the tree stands
the canopy          foe within reach x reachMul x mods.reach + R: entangle 1 every 0.5s
```

**Priced whole (design §4.1, §5):** blade 23.5, 660 an arm, Chromium 141:
body 14.5% → whole **47.1%**; blade 25 → **54.1 / 55.2%** on two blocks.
Boughs are the payload (+33); self-root and canopy are free and kept for the
picture and the school. 3.7 casts a fight, 18 bough blows in windows, the
foe under the canopy 41% of the window at ~3.2 stacks.

## 1. IN THE ENGINE

- `f.ultTree` — `{ t0, end, sprouted }`. Null elsewhere; `engine_ab` on the
  other 35 proves it.
- **Self-root**: at cast `f.pinV = [0,0]; f.pin = f.pinMax = dur; f.pinFree
  = 1`; `tickTree` keeps `pin` topped up each frame; on close `pin = pinMax
  = 0; pinV = null; pinFree = 0; vx = vy = 0`. `move` skips a pinned ball,
  gravity skips it, `ballCollision` treats it as immovable, `resolveHit`'s
  knock is discarded by the pin — all existing behaviour.
- **Growth**: `f.reachMul` toward 2.5 at 0.35/s in `tickTree`; site 2 of 7
  recomputes the drawn haft from it. The builder refuses if any
  `f.w.reach` read lacks `reachMul`.
- **Boughs**: `bladeSegments` reads `f.w.blades`; for the window the relic
  needs three offsets. **Do not mutate the shared weapon object** (the lab
  did; a build must not — `w` is module-level and shared by the mirror
  match): give `bladeSegments` a per-fighter override (`f.bladeSet`, null
  elsewhere) and size `f.tips` / `f.hitCd` to it at cast. The two extra
  boughs sprout at 1.5s (drawn growing; live for hits from the moment they
  exist).
- **Bough damage**: in `resolveHit`, `dmg *= 0.35` when the attacker has
  `ultTree` — one line, declared, and the ONLY damage change. Knock, sunder,
  crit, hit stop and the beat are the hammer's.
- **Canopy**: `foe.apply("entangle", 1, f)` every 0.5s while the foe's
  centre is within the boughs' reach + R.
- **The wither**: 0.4s; the next cast waits for it.
- `_drawField`'s held-ball block: skip for `pinFree` (as Garrote's snag).

## 2. STAGES AND GATES

**Stage 0 — control.** `ult_overlay.py --relic grudgebearer --cell
verdant:warhammer --mech overlays/tree.js --arms A,D --P boughs=3
growCap=2.5 winDmg=0.35 --seeds 20` UNMODIFIED on the pinned 151. Arm A
~14.5%, arm D ~47%. Every later gate reads against this run.

**Stage 1 — the relic, stubbed.** Ironwood at dmg 23.5, verdant, entangle 2,
charge 1e9, names, card, a verdant warhammer silhouette (first cut).
Gate: `engine_ab` on the 35; `verify` reads 10–20%; `tip_audit` in pixels.

**Stage 2 — the root and the growth.** Pin, pinFree, growth, restore, wither.
Gate: probe over ≥96 fights — the ball moves 0 px on ≥99% of window frames,
takes 0 knock, `reachMul` peaks ~2.46; relic ~26% at 23.5 (arm C without
boughs — reproduce it with `--P boughs=1 --arms C`). **FILM IT**: a rooted
barking ball with a lengthening trunk is the picture and no probe sees it.

**Stage 3 — the boughs.** The per-fighter blade set, sprouting at 1.5s, the
0.35 scale in `resolveHit`, tips/hitCd sizing.
Gate: ~18 bough blows in windows a fight, ~7.7 hammer blows outside, no
blow inside a window at full damage (asserted), relic ~48% at 23.5 (arm C).
`engine_ab` on the 35. Freeze census per window (v67) — write it down.

**Stage 4 — the canopy.** Gate: foe under the canopy ~41% of window frames,
~7.7 stacks applied a cast, ~3.2 stacks on an average window frame; relic
~47% (arm D). Stacks = applications, asserted.

**Stage 5 — the blade.** Wide, both sides, two blocks, n ≥ 1000 a point at
23.5 / 24 / 25 on 151. Expect 23.5–24.5. If out of band move `winDmg` inside
0.30–0.40 first and say so. Gate: verify 30–70 on all 36; type ladder
printed (greatswords ~86%, Bloodmirror ~0 — item 12/32, not this build's).

**Stage 6 — picture, voice, carry.** Design §7.1–7.2. Beats: the cast files
`ult`; bough blows file as blows; the wither files nothing. Field spec in
both `fx.js` copies, sha re-stamped. Move `GAME`. `shell_identity`,
`render_ab`, `chain_audit --builder ironwood_build.py`, one whole fight
watched.

## 3. NOT TO RE-BUY

- One bough at any reach is +16 (§3); the type's revolution rate is the
  ceiling and reach does not move it.
- Three boughs at the hammer's blow is ~90% and the blade cannot fix it
  without deleting the hammer (§3); the bough scale is the lever (§4).
- Self-root and canopy are inside ±2 of free at n=660 (§4.1).
- Blade curve ~4 points a damage point, 23.5–27 (§5).

## 4. OPEN, AND WHOSE

1. Rick's veto (design §8.1); the two-bough fallback is one flag.
2. `winDmg` inside 0.30–0.40 — the build's, declared.
3. The blade — the build's, wide.
4. Bloodmirror 0% and the 50pp type spread — Rick's (item 12/32).
5. Three simultaneous binds — say so if the engine misbehaves.

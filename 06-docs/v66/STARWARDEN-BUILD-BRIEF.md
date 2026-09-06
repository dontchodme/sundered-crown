# STARWARDEN / CORONA — BUILD BRIEF (v66). The vigil twinblade, the 34th relic, second design.

**Cowork, 2026-09-03. DESIGNED. Build from this file and `vigil-twinblade-design-v66.md`; do not design (CLAUDE.md §3 rule 0).** Every number below is Rick's or is priced in the design doc; the one number the build owns is the burn's per-stack damage (stage 5). Claimed in `06-docs/CLAIMS.md`.

Arclight / Static (`06-docs/v64/`) was the first design for this cell and Rick scrapped it built — *"i dont like what ive built. lets start over."* Nothing survives it, not the names. Four of its measurements do and this brief is written against them (`v64/vigil-twinblade-CONSTRAINTS.md`): the body is strong before any ultimate exists; the blade is not the balance lever; two payoffs on one ultimate must be priced jointly; anything in the room must close with the hall.

---

## 0. THE RELIC, IN RICK'S WORDS AND HIS RULINGS

> *for a duration the fighter gets an elliptical ring of neon light with a small gap left for a large star in the middle. enemy fighters who enter the ring are burned for rapid tics of damage over time and left with a burn that deals more damage over time for a few seconds. If the enemy is hit by the star it explodes sending a shower of smaller stars bouncing around the arena. if an enemy hits one of the stars it detonates, dealing damage over time and knocking them back. after a duration the leftover stars detonate anyways, not all at once, in a chain reaction like effect from one end of the arena to the other*

> *its like the rings of saturn. a sash that floats off the body and extends beyond*

```
the cell            vigil x twinblade          Rick, 2026-09-02, reconfirmed 2026-09-03
the fighter         STARWARDEN                 Rick, from four
the ultimate        CORONA                     Rick, from four
the card            "Ring and stars deal burn damage over time. Burn is gained as shield"   67 chars, his
the blade           dmg 8.3                    Rick — the row floor, Twinshade's. Widowmaker's profile otherwise
the window          8s, cast every 15s         Rick (8 over 6)
the ring            outer 120 x 42, band 24, tilt 0.45 rad, fixed in the world, centred on the ball   Rick (120 over 100/150)
ring ticks          10/s while the foe's disc overlaps the band: 1 damage AND +1 burn stack        Rick ("each tick adds a stack")
ring crossing       +1 burn stack on each entry into the band
the star            on the body; pops on the first ball-to-ball contact of the window (d < 2R+2)
the shower          16 small stars, r 12, speed 380, random angles from the caster; bounce the CURRENT inset; never expire   Rick (16 over 10/6)
a touched star      +2 burn stacks, knock 600 along the star's travel; the star is gone            Rick (600 over 300/150)
the chain           when the window shuts, the leftovers go off top-to-bottom at 70ms a star; within 80 of the foe: +2 stacks, knock 600 away
the burn            NEW status, UNCAPPED stacks, 3.0s, refreshed whole on every application; 0.10/s a stack PLACEHOLDER for stage 5   Rick (uncapped over 4/8)
the shield          every burn tick banks 0.55 x its damage as ward on the caster, capped at STATUS.ward.cap    Rick ("the burn feeds the shield")
```

**Priced whole (design doc §10):** blade 8.3 body 17.2% → with Corona **49.1%** (10 seeds, 320 fights an arm, Chromium 141). Ring alone +12.8, shower alone +17.2, whole +31.9 — **additive**, which is the property the uncapped ruling bought. ~34 stacks a cast, peak ~49 on the foe; 26 damage and 11 shield a cast.

## 1. WHAT IT IS IN THE ENGINE — the shape, not the code

- `f.ultCorona` — the window: `{ t0, end, popped, inb, tickAcc }`. Null on every other relic and on this one outside its window; `engine_ab` over the other 33 proves it.
- **The ring test** is an elliptical annulus in the caster's frame: `u = dx·cos(tilt) + dy·sin(tilt)`, `v = -dx·sin(tilt) + dy·cos(tilt)`, `rho = hypot(u/120, v/42)`; the foe is in the band if `rho ∈ [(120-24)/120, 1]` for the foe's centre OR any of 12 points on its rim. The design's lab is the reference (`tools/ring_price.py`, `inRing`); a build that changes the test re-runs the lab against itself.
- **The burn** is a `STATUS` entry (`burn`, `maxStacks` 99 = uncapped in this engine's terms, `dur` 3.0, `dps` = the stage-5 number, `tip` ≤40 chars). It ticks in `tickStatus` like hemorrhage and smite — `hp` directly, times `dmgTakenMul`, no shield — and a fatal tick files a beat as the others do. **New in this engine: its tick banks ward on the OTHER fighter.** `tickStatus` has to know the applier; the status carries `src` (the comment on the fatal-tick beat already says the day a third party can apply a bleed the status needs a source — this is that day, from the other direction). Bank `0.55 × tick` into `src.shield` capped at `W.cap`, raise `shieldMax`, restart the ward clock — the same three writes resolveHit's vigil branch makes. **Whether every tick restarts the 5s clock or only the application does is the build's to decide and declare**; the design priced every tick.
- **Small stars** are objects with `x, y, vx, vy, r 12, born`, bouncing off `n = m.inset` (§4 of v64: the room closes). They do not expire. The foe's disc within `R + 12` after a 0.15s grace detonates one; the caster passes through. Honour `maxLive` by DECLINING to spawn, never by shifting (the Bloodhunt fork rule; the kunai design §4.1). 16 at a pop is inside 64, but a bow foe's arrows share the ceiling.
- **The chain** is a queue built when `end` passes: leftovers sorted by `y`, one every 70ms. The NEXT cast waits for the queue to drain (the lab does; a cast that starts under a running chain is two set-pieces on one screen).
- **Knock 600** is `foe.vx += kx * 600` on a live, unpinned foe — the kunai's rule for a touched star (along its travel), away from the blast for a chained one.
- The card line goes in as `ult.tip` exactly: `Ring and stars deal burn damage over time. Burn is gained as shield`.

## 2. STAGES AND GATES

Each stage is one link, one builder stage, one gate that can fail. The base is the chain tip at the time of the build — `sc-minute` per CLAUDE.md §0 as of this writing, or its successor; **the builder names it and does not guess.** Remember the chain is forked (Crossweave's stages 7-12 are in `sc-nova` only) — the builder says which branch it is on.

**Stage 1 — the relic, ultimate STUBBED.** Starwarden: Widowmaker's twinblade profile at `dmg 8.3`, `aff vigil`, `onSelf {ward:1}`, `ult.charge 1e9`, name, blurb, card line, a vigil twinblade silhouette (the type's art, the school's palette — a first cut; the redraw is a picture question for later, as the umbral scythe's was).
Gate: `engine_ab` identical on all 33 others; `verify` reads the new relic in 15-25% (the design's 17.2% at n=192; a 34-relic tip and the pinned runtime will move it — read against a local reproduction, CLAUDE.md §4.2b); `shell_identity`; the tip audit sees the 67-char line.

**Stage 2 — the ring and the burn.** The window, the annulus test, the ticks (1 dmg + 1 stack at 10/s), the crossing stack, the burn status with its ward feed. No star.
Gate: a probe over ≥96 fights reads **~0.8s of ring dwell and ~5.6 crossings a window, ~12 stacks a cast, ~6 damage and ~3.4 shield a cast** (design §10 arm B). `engine_ab` on the 33. The status-source plumbing is asserted, not commented: a probe that applies burn from A and checks B's ward never moves.

**Stage 3 — the star and the shower.** Pop on first body contact; 16 stars; bounce the inset; touched → +2 stacks, knock 600; grace; `maxLive` by refusal.
Gate: probe reads **the star pops in ~92% of casts, ~1.3s in; ~11 stars touched a cast; refusals = 0 in a hall with no bow foe.** Bookkeeping asserted per fight: spawned = touched + chained + alive. `engine_ab` on the 33.

**Stage 4 — the chain.** Queue on window close, `y`-ordered, 70ms, blast 80, +2 stacks, knock 600 away. The next cast waits.
Gate: **~3.4 chained a cast, ~0.35 landing within 80** (it is a picture and the gate says so); no star outlives its chain; no cast opens under a chain.

**Stage 5 — THE ONE KNOB.** Bisect the burn's per-stack damage on the pinned runtime, n ≥ 700 a point, target the band. **The design's ladder at n=192 has a step between 0.15 and 0.20 that the sample cannot resolve** (design §9) — size the top of the bisection to that, and confirm the answer with one wide direct measurement (the v47 lesson, §4 of CLAUDE.md). **Run the reproduction control first:** `ring_price.py` at the design's settings must read arm A ≈ 17.2% and arm D ≈ 49% on the design's runtime (Chromium 141) before any number from the build is compared to it; on 151 read the build against its own reproduction, not the published decimal (v64 §3aa moved a gate in both directions).
Gate: `verify` 30-70 on all 34; every relic in band; the type ladder printed (this relic is a contact hazard — it should be strongest against types that bump it and weakest against bows; write the spread down as Thornshear's was, do not fix it here).

**Stage 6 — the picture, the voice and the carry.** Rendered SPREADS for Rick, before he is asked anything in words (rule 2): the ring (a tilted neon band in vigil pink, the "Saturn" read, with its band and gap), the star on the body, the small stars, the burn tag and its count, the chain. Four cast voices and three burn/star voices rendered and sent. The ult FX spec goes into `src/render/fx.js` AND the inlined copy, sha re-stamped (the Thornshear lesson). Director: **a hit-heavy ultimate declares itself (§3 rule 3)** — ~34 burn applications a cast file nothing; file a beat on the pop and on the chain's first detonation; the fatal burn tick files as every dps status does; `crowdMul` wants its own measurement, not the spike storm's. Move `app/main.js`'s `GAME` line. `shell_identity`, `render_ab` where the base is untouched, and one whole fight watched end to end.

## 3. WHAT THE DESIGN MEASURED THAT THE BUILD SHOULD NOT RE-BUY

- Ring dwell is 0.6-0.9s a cast at any reach 100-150; "rapid ticks" are a brush, and the burn is the mechanic (design §5-6).
- Under a stack cap the two halves substitute and every look knob is inert; uncapped they add and the knobs are levers (§6.1, §9). Do not reintroduce a cap "for safety".
- The chain lands a blast in a third of casts at 80 and half at 130, and the win rate does not move either way — it is a picture (§6 item 3).
- Ring-tick ward feed at 1 dmg a tick is inert (+0.5pp); the BURN's feed is the payoff (§6.2). Routing ticks through `resolveHit` would add the former; declare it if so.
- Blade 7.0 / 8.3 / 9.5 bodies read 6% / 17% / 35% with no ultimate at the minute pace (§4, §9).

## 4. WHAT IS OPEN, AND WHOSE

1. **The art and the sound.** Rick's, from rendered spreads at stage 6. Not to be asked in words.
2. **The burn tip** (≤40 chars, the arena explainer's line). Rick has not written it; offer three at stage 2.
3. **The silhouette.** A vigil twinblade has no art of its own yet; the first cut ships and a redraw is a later, separate claim.
4. **The status-source plumbing** (`src` on a status) is chain-wide and touches the fatal-tick beat's attribution comment; name it in the build doc.
5. **`s.snap`, `maxLive` shifting, `frame_probe`** — the standing chain-wide items (CLAUDE.md §8) are not this brief's.

---

*Tools: `tools/sash_tracks.py` (the event rate), `tools/ring_price.py` (the live price, four arms, every knob). Runs in `06-docs/v66/runs/`.*

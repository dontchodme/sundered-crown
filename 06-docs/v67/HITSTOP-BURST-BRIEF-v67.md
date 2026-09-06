# HIT STOP IN A BURST — BUILD BRIEF (v67). Engine-wide: a flurry freezes the world once, not once per hit, and the sparks keep flying while it does.

**Cowork, 2026-09-03 09:24 UTC. RULED. Build from this file; do not design (CLAUDE.md §3 rule 0).** Rick, watching Thornshear: hit stop on loud, many-hit ultimates *"sometimes reads as lag even though its probably not."* He chose the engine-wide rule here TOGETHER WITH the one-relic patch in `WINNOWING-HITSTOP-BRIEF-v67.md`; that one lands first and this one is its own claim. Claimed in `06-docs/CLAIMS.md`.

---

## 0. THE FINDING — why a freeze reads as impact once and as lag ten times

From `02-chain/sc-minute.html` (the build of record, CLAUDE.md §0):

```
resolveHit()      stop = min(0.13, 0.045 + 0.0022 x dmg); x1.7 crit; killStop 0.55 fatal.
                  hitStop = max(hitStop, stop)  -- EVERY hit, no memory of the last one.
step()            while hitStop > 0: t advances, decayImpactOnly(dt), return.
decayImpactOnly   rings, shake, finisher, tickPresentation. THAT IS ALL.
decay()           fx particles, floats, motes, banner -- NORMAL PATH ONLY (and `over`).
```

Two things follow, and both are the finding:

1. **A hit stop has no memory.** One heavy swing: one hold of 70-130ms with a windup before it, a flash, a shake and a ring running through it. That reads as weight. A many-hit ultimate: the same hold again every time a hit lands — `stopBase` 0.045 is a floor a 2-damage chip clears — at whatever rhythm the hits happen to arrive. Regular (Scour's 7/s, before it got `stop: 0`: ~45% of every second frozen) or irregular (the Winnowing's ricochets), a run of 50ms holds with no per-hit cue is what a frame drop looks like.
2. **During the hold, the picture holds.** Particles and damage numbers are advanced in `decay()`, which the freeze path never reaches. Only rings and shake move. A stylised freeze-frame in any fighting game keeps its sparks flying and its number rising; a dropped frame has neither. The engine is on the wrong side of that line for everything but two things.

The repo has been fixing (1) one ultimate at a time — Scour `stop: 0`, Bloodletting 0.02, Breach 0.04, Deadfall 0.05, each with a comment saying a full stop apiece "would freeze the hall solid" — and each new many-hit ultimate re-creates it until someone watches (Crossweave's arrows carry the default; so will Corona's ring ticks and stars). A rule in the engine is what stops the next one.

## 1. THE RULING — two parts, both Rick's, 2026-09-03

**Part A. Diminishing returns on hit stop inside a burst**, the shape `takeHitstun` already has for hitstun (`stunDR 0.55`, decaying 0.75/s, `dur = raw / (1 + stunDR x acc)`). The first hit of any flurry lands at exactly today's weight; each hit arriving within a short window of the last freeze is scaled down, harder each time; the accumulator recovers when the hits stop.

```
CONFIG.impact.stopDR        0.55     the divisor's slope, hitstun's number to start
CONFIG.impact.stopDRDecay   4.0      per second -- one hit's memory is gone in 250ms.
                                     NOT hitstun's 0.75: that window is a second and a half
                                     and would grind ordinary exchanges, which are 0.3-0.6s
                                     apart. The burst this rule is for is inside 250ms.
match.stopDR                0        the accumulator, ON THE MATCH -- hit stop is global.
```

`stop = raw / (1 + I.stopDR * this.stopDR); this.stopDR += 1;` — and the accumulator decays in `decayImpactOnly`, which runs on BOTH paths (via `decay()` on the normal one), so the clock is wall-time, the same time the viewer's eye is keeping. **`killStop` bypasses the divisor entirely** — the kill is the shot. **Clank's 0.15 is left alone** (it is already gated by `clank.cd` 0.22s and it is not a hit). The ~30 direct `this.hitStop = Math.max(...)` writes outside `resolveHit` (Grasp 0.09, Garrote 0.14, the Crucible's `stopBase + stopPer x n`, the vigil shatter 0.10, ult casts 0.08…) are set-piece ACCENTS, one per event, not per-hit ticks: **stage 1 routes `resolveHit` only**, and stage 2 decides the rest site by site with a probe in hand, not by find-and-replace.

**Part B. The effects layer keeps moving through a freeze.** `fx` particles and `floats` advance during hit stop at a reduced rate, so the freeze still reads as a freeze but not as a stall.

```
CONFIG.impact.fxDuringStop  0.35     particles and numbers run at a third speed while
                                     the world holds. 0 is today. 1 is no freeze on the
                                     effects at all. A picture number; Rick's to move
                                     from a rendered pair if 0.35 is wrong.
```

Move the two loops out of `decay()` into `decayImpactOnly()` with `const k = this.hitStop > 0 ? I.fxDuringStop : 1` on `dt`. **NOT the motes** — `motes` call `this.rng()` when they wrap, and advancing them on the freeze path would draw from the match RNG during a freeze and change every fight. **NOT the shots** — a kunai is a sim object and where it is decides what it hits. (A render-side extrapolation of shots during a freeze — draw them at `x + vx x frozen x k` without moving them — is possible, deterministic, and NOT in this brief; it draws kunai through walls unless clipped, and it is a picture Rick has not been shown.)

## 2. WHAT MOVES IN THE SIM, AND WHAT MUST NOT

Part B touches nothing the sim reads: `fx` and `floats` are presentation lists, and the gate is `engine_ab` IDENTICAL on every pairing of every relic — a single DIFFER fails the stage.

Part A changes how much frozen time is inserted into `t`, and `t` fires the seals and the timeout. So fights with a burst in them WILL differ — that is the pass — and the control that can come back wrong is the knob at zero:

- **`stopDR = 0` must be byte-identical to today on all 528 pairings.** The divisor is `1 + 0 x acc = 1`; the accumulator is written and never read. If that is not identical, the plumbing leaked into the sim somewhere (the decay is on the wrong path, or the accumulator got into a probe's hash) and the build stops.
- **The first hit after ≥250ms of quiet gets EXACTLY today's stop**, asserted by a probe on a heavy single-hit relic (Marrowdraw, Sentinel's caster, any clank-and-swing pair) — not "about", exactly, to the double.
- **The pace.** The Minute (v65) put the mean fight at 60.2s on all 528 pairings and every relic in 30-70%. Less frozen time per burst means slightly more sim progress per second of `t`; re-read the mean and the per-relic band on the pinned runtime after stage 1 and publish the delta. Expected: small, inside verify's band, largest on the many-hit ultimates. If a relic crosses out of band, that is a finding for Rick, not a number to fix here.

## 3. STAGES AND GATES

Base is the chain tip at build time and the builder names it (the chain is forked; say which branch). The Winnowing patch lands before this and its rung numbers are then ALSO divided by the burst rule — declared, and fine: a rung-3 kunai arriving alone still carries its 0.060.

**Stage 1 — Part A in `resolveHit`.** `stopDR` / `stopDRDecay` in `CONFIG.impact`, the accumulator on the match, reset with the rest of the match state, decayed in `decayImpactOnly`, divisor applied to `stop` after `critStopMul` and before the `over.stop` override (an override is a call site's own number and is divided too; `stop: 0` stays 0; fatal keeps `killStop`).
Gate: (a) knob-at-zero identical, 528/528; (b) first-hit-exact probe; (c) **the freeze census** — a probe that sums `hitStop` wall-time inside each ultimate window for the Winnowing, Crossweave, Bloodletting, Breach and Deadfall, BEFORE and AFTER, per cast and as a share of the window: publish the before numbers first, and the after must show every many-hit window under a stated ceiling (propose 15% of the window frozen; the number is Rick's to move from the clips) with single-hit relics' freezes unchanged to the double; (d) pace re-read, delta published.

**Stage 2 — the direct writes.** With the census in hand, walk the ~30 `this.hitStop = Math.max(...)` sites outside `resolveHit`. A once-per-event accent (a cast, a grab closing, the Crucible strike) is left alone. A site that can fire several times inside 250ms (the Breach vents at 0.04, Deadfall mines at 0.05, Bloodletting copies at 0.02, Garrote's ring, anything in a tick function) is routed through the same helper. Each site's decision is one line in the build doc with the census number that made it.
Gate: census re-run; knob-at-zero identical again; the count of routed sites stated.

**Stage 3 — Part B.** The two loops move; `fxDuringStop` in `CONFIG.impact`; motes and banner stay in `decay()`.
Gate: `engine_ab` IDENTICAL 528/528 and on every relic's own pairings; `render_ab` DIFFERS only on frames inside a freeze (a frame probe on one seed: pick a freeze, assert particle displacement between its first and last frame is > 0 and is `fxDuringStop` x the unfrozen displacement to the pixel); `shell_identity`.

**Stage 4 — the clips.** The same seed, three ways, filmed: today's tip, stage 1, stage 3 — for the Winnowing and for Crossweave (the two loudest many-hit ultimates in the chain). Rick said "reads as lag"; whether it still does is his to say from the clips, and `stopDR`, `stopDRDecay` and `fxDuringStop` are his three numbers to move from them, not to be asked about in words.

## 4. WHAT IS OPEN, AND WHOSE

1. **The three picture numbers** (`stopDR` 0.55, `stopDRDecay` 4.0, `fxDuringStop` 0.35) — Rick's, from stage 4's clips. The build ships the proposals.
2. **The ceiling on frozen share of an ultimate window** (proposed 15%) — a design check the census enforces from now on; the number is Rick's.
3. **Whether the per-ultimate `stop:` overrides stay** once the rule exists. They are correct as accents and harmless under the divisor; the brief leaves them and stage 2 says so per site.
4. **Shot extrapolation during a freeze** — not in this brief; a separate picture question if the Winnowing's spray still looks stopped after stage 3.
5. **The audio gate after a freeze** (the 70ms near-silence, CINE) is untouched and unmeasured here; if the effects moving through a freeze change what the mix wants, that is CINE's claim.

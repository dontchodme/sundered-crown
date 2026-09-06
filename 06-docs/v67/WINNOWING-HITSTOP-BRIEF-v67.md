# THE WINNOWING'S HIT STOP — BUILD BRIEF (v67). Thornshear's kunai carry a freeze that grows with the rung.

**Cowork, 2026-09-03 09:24 UTC. RULED. Build from this file; do not design (CLAUDE.md §3 rule 0).** Rick watched Thornshear and said the hit stop *"reads as lag even though its probably not."* He chose this patch AND the engine-wide rule in `HITSTOP-BURST-BRIEF-v67.md`, over a kunai-with-no-freeze patch alone and over the engine rule alone. This file is the small one and it lands first. Claimed in `06-docs/CLAIMS.md`.

---

## 0. WHAT HE SAW, AND WHY IT IS THIS RELIC

Read out of `02-chain/sc-minute.html` (the build of record, CLAUDE.md §0), not from memory:

```
CONFIG.impact         stopBase 0.045   stopPerDmg 0.0022   stopMax 0.13   critStopMul 1.7   killStop 0.55
step()                while hitStop > 0: t advances, decayImpactOnly(dt), return.
                      Fighters, shots, fx particles and floats HOLD. Rings, shake and
                      the presentation clocks keep running. Nothing else does.
resolveHit()          stop = min(stopMax, stopBase + dmg x stopPerDmg); x1.7 on a crit;
                      killStop on a fatal; `over.stop` replaces it when a call site says
                      so (Scour passes 0). hitStop = max(hitStop, stop).
the Winnowing         dur 4, cadence 0.6, fan 5 x 2 bearings = 10 kunai a volley,
                      dmgMul 0.15 on dmg 11.83 = 1.77 a kunai, x1.25 a rung, 3 bounces.
spawnKunai()          NO `over`. Its own comment: hit stop "comes free from resolveHit".
```

So every landed kunai buys the DEFAULT freeze for 1.8-3.5 damage:

```
rung 0   1.77 dmg   stop 0.049s        crit 0.083s
rung 1   2.22       0.050              0.085
rung 2   2.77       0.051              0.087
rung 3   3.47       0.053              0.090
```

`stopBase` is a floor and it does not scale down for a chip: a 3-damage leaf holds the whole picture for about half of what a 30-damage swing holds (0.053 against 0.111). Six or seven volleys, sixty-odd kunai, leave over four seconds, 69.8% of the landed ones arrive off a wall (`kunai_probe [4]`), so the hits come at IRREGULAR moments spread over five or six seconds — an irregular series of ~50ms full-picture stalls, each caused by a hit too small to see, with the whole spray halting on every one. That is what a dropped frame looks like. Scour got `stop: 0` for exactly this reason ("a grind is the one thing in this game that must not stutter"); the Winnowing shipped a version earlier and never got a ruling.

## 1. THE RULING — the freeze is the size of the rung

Rick chose the rung-scaled patch over "no freeze at all":

```
rung 0   a fresh kunai        stop 0      no freeze. The loose is the picture; the hit is a leaf.
rung 1   off one wall         0.020
rung 2   off two              0.040
rung 3   off three            0.060      about a rung-0 kunai's freeze today, on a kunai
                                          twice its size -- the growth becomes legible with
                                          no number on screen (the Crucible's rule: "the
                                          freeze is the size of the meal").
a kill   any rung             killStop    unchanged. resolveHit guards `!fatal` before it
                                          honours `over.stop`; nothing here touches that.
a crit   any rung             the rung's number, NOT x1.7 -- the override replaces the
                                          whole formula, critStopMul included. Declared, and
                                          fine: a crit kunai is still a 4-damage leaf.
```

The numbers are Rick's shape ("nothing fresh, a little off a wall") with Bloodletting's 0.02 as the unit; they are picture numbers, not balance numbers, and the build does not bisect them.

## 2. WHAT IT IS IN THE ENGINE

Two edits, one relic, no new field on any other projectile.

- `spawnKunai(f, a)`: the shot gains `over: { stop: 0 }`. `over.onHit` and `over.knock` stay undefined, so entangle and the kunai's own `knock` (260, applied on the shot path) are untouched — `resolveHit` reads `(over && over.onHit) || self.w.onHit` and `over.knock !== undefined ? over.knock : 1`, both checked.
- `kunaiRung(s, src)`: after `s.rung++`, `s.over.stop = 0.02 * s.rung`. One definition, both reflection paths (wall and parry), the same place the growth already lives.

`resolveHit` already does the rest: `if (over && over.stop !== undefined && !fatal) stop = over.stop;` and `if (stop > 0) hitStop = max(hitStop, stop)` — a zero override does not write the clock (the negative-residue invariant, §12318 of the build of record). Nothing in the sim reads `hitStop` except `step()`'s gate and gravity-through-freeze, so damage, entangle, knock and the rung schedule are byte-identical; what moves is the match clock `t`, which advances through every freeze — so fights WITH a Winnowing cast will differ (seals fire on `t`), and fights without one must not.

## 3. STAGE AND GATE — one link, one gate that can fail

**Stage 1 — the two edits.** Base is the chain tip at build time; the builder names it (CLAUDE.md §0 says `sc-minute`, and the chain is forked — say which branch).

Gate, in this order:

1. **The control that can come back wrong.** `engine_ab` over all 33 other relics: IDENTICAL, every pairing. Thornshear's own pairings DIFFER, and the builder says how many (the pass is that they differ — a Winnowing cast now inserts less frozen time into `t`).
2. **The freeze census, before and after.** A probe over ≥96 Thornshear fights sums `hitStop` wall-time inside each Winnowing window (cast → last kunai gone) and prints: frozen seconds a cast, frozen share of the window, and the count of freezes by rung. Publish the BEFORE number from the unpatched tip first — if it is not several hundred ms a cast the diagnosis above is wrong and the build stops. After: rung-0 freezes = 0 exactly; rung-3 freezes = 0.060 exactly; a kill inside the window = 0.55.
3. **`verify` on Thornshear.** It was in band before (§0: every relic in 30-70%); a change to the match clock alone should not move it by more than the n≈700 noise. If it moves further, that is a finding, not a fix — write it down and stop.
4. **One fight watched.** A Winnowing cast, filmed, next to the same seed on the unpatched tip. Rick said "reads as lag"; the gate is that it no longer does, and that is his to say — send both clips.

## 4. WHAT IS OPEN, AND WHOSE

1. **Whether 0.06 at rung 3 is enough to read as "bigger".** A picture question; if it is not, the number is Rick's to move, from a rendered pair, not in words.
2. **Every other many-hit ultimate** with the default weight on each hit — Crossweave's arrows (`s.over` undefined on the shot path), Corona's ring ticks and stars once they land — are NOT this brief's. They are the engine rule's (`HITSTOP-BURST-BRIEF-v67.md`), which is why Rick took both.

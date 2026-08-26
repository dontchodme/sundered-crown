# SLAGBURST — Emberedge's ult redesign. Patch for the live session.

Applies on top of chain tip `sc-daybreak.html` `c25a90cc0ca82f68`.
Produces `sc-ember.html` **`b3d8adf2e86baf44`** — the new chain tip.

**NOT SHIPPED.** `01-live/sundered-crown.html` is still v21's `ba423d8e…`.
Ship is now three cp's behind Rick's word (Crucible, Daybreak, Slagburst — all
in the one chain tip).

## Apply it

Canonical — the builder is the patch, a generated file is not a place to
store a number:

```
cd tools
python3 ultember_build.py --src ../02-chain/sc-daybreak.html \
                          --out sc-ember.html
# -> sc-daybreak.html -> 02-chain/sc-ember.html  sha256 b3d8adf2e86baf44
```

`sc-daybreak-to-sc-ember.diff` is the same change as a unified diff (451
lines) if you want to read it or apply it directly. `02-chain/sc-ember.html`
is the built artifact if you just want to run it.

Chain, updated:

```
  ultforge_build   THE CRUCIBLE     bd28056762e1fe34   sc-crucible
  ultdawn_build    DAYBREAK         c25a90cc0ca82f68   sc-daybreak
  ultember_build   SLAGBURST        b3d8adf2e86baf44   sc-ember   <-- tip
```

## What it is, in one paragraph

`kind:"detonate"` — a THIRD state shape, neither the forge's gated promise nor
Daybreak's window, but a fuse. Cast (in range only, radius 230): splits the
foe's shell for 3 Sunder, resolves no damage, banners on the TARGET, and lights
a 0.55s fuse ticked on fighter time. During the fuse the foe keeps moving and
keeps swinging — nothing is stunned, because the Crucible owns freeze. The
detonation reads `n = banked + split` uncapped (range 3..9), CLEARS every
Sunder stack, then prices `6 + 5.5n` damage and `110 + 34n` knockback, and
throws **one shard per consumed stack**. Foe dead, wielder dead, or match over
during the fuse -> the state drops and nothing resolves.

Interview answers this implements: fantasy "The Detonation — set off Sunder",
budget "strictly sideways", Sunder role "detonator, consume stacks for burst".

## The measurement that shaped it

`sunder_probe.py`, 1893 Emberedge casts across the field — Sunder on the foe
at cast time:

```
0 stacks 26.3%   1: 17.4%   2: 13.2%   3: 10.9%   4: 10.9%   5: 6.6%   6: 14.7%
mean 2.42   median 2
```

**A quarter of casts find zero stacks.** A literal detonation is a dud one time
in four. The split fixes it, and the relic's own blurb had already written the
fix: *"It does not cut so much as split."*

## Balance — sideways, and the blade is NOT repaid

Paired test, 260 shared seeds x Emberedge's 15 pairings = 3900 games, the same
seed list the old build was measured on:

```
Forgefall  48.46%      Slagburst  48.08%      delta -0.38pp
discordant 519 lost / 504 won        McNemar z = -0.47
```

Sideways to within half a point of noise **at the blade it already had**
(12.32, unchanged). Repaying it would be tuning against noise. Per-opponent
texture moved a lot while the aggregate did not — Goreshard -6.9pp, Farwarden
+4.6pp — which is the good version of this outcome.

## Checks, all at `b3d8adf2e86baf44`

```
ultember_check.py   23/23 — mech, phases, art samples, 16-relic set-piece
                    regression. Includes the traps: cap-swallowed split,
                    damage double-dip, stale overflow on a dropped fuse.
engine_ab           3150/3150 bit-identical on the other 15 relics vs
                    sc-daybreak. Zero rng added anywhere.
verify.py --n 60    13/13.   verify.py --n 40  13/13.
ember_filmstrip.py  eyes pass, including a 390px phone-width row.
```

## Why this is not the Crucible

Rick picked the detonation over my flagged objection that it is Grudgebearer's
move pointed outward. Every axis is inverted, which is what makes it hold:

```
Crucible    18s · a PROMISE · needs a melee connect · stacks become crit
            chance and crit multiplier on ONE strike · rewards patience ·
            a whiff keeps the stacks and wastes the cast
Slagburst   14s · a COMMITMENT · needs no connect · manufactures its own fuel
            then spends it instantly for flat burst and knockback · rewards
            pressure · cannot whiff, but dying cancels it
```

Grudgebearer hoards Sunder and spends it on a promise. Emberedge makes Sunder
and spends it on the spot.

## Ways a check lied, this session — read these

* **`verify.py --n 60` cannot rank a flat field, and does not say so.** Its
  bar chart is ordered and looks decisive; its standard error is 1.7pp and the
  field is 1.6pp wide. **The v23 note's floor — "Farwarden ~46 / Gravemourn ~47
  / Spellbreaker ~47.5" — is noise.** Two disjoint seed sets at 4500-6000 games
  per relic put Farwarden 13th/14th of 16, near the TOP of the field. Only
  Lightkeeper and Nightfell are bottom-three in both. Full table:
  `sundered-crown-weakest-probe.md`.
* **THE FX CLOCK RUNS AT 2x SIM TIME.** `ultFx.t` is advanced by BOTH decay
  paths, so every `life` number in the engine is in half-seconds — the
  1.3-2.6 table reads as 0.65-1.3s on screen. A fuse tell given `life = fuse +
  0.35` died 0.18s BEFORE its own detonation and left a dead frame. This is
  not documented anywhere else; anything timing a set-piece against a sim
  duration has to double it.
* **A fuse ticked on fighter time is frozen by hit-stop; `m.t` is not.** The
  0.55s fuse resolves 0.633s after the cast because the cast's own 0.08
  hit-stop pauses the fighter tick. Correct and consistent — the Crucible's
  cap and Daybreak's window live on the same clock — but a harness measuring
  `m.t` reads it as a slow fuse.
* **The Daybreak spark lesson repeated, exactly.** v1 shards were 7-14px with
  a 2.4px stroke. Every assert passed, `[17] set-piece is not thin` passed, and
  on the 390px filmstrip a nine-stack burst and a three-stack burst were the
  same picture — the central design claim was false while the tests were
  green. They are now ~ball-radius long, born slower, dark-body-with-hot-core
  so they have an edge against both the flash and the hall. **A new sim-visible
  object needs a MODEL and a phone-width look, from the start.**
* A harness that asserts internal tidiness instead of the contract pushes
  changes into shared code to satisfy itself. `tickCharge`'s pre-existing
  `if (!f.alive || this.over) return;` leaves a dead wielder's fuse lit on the
  corpse; it is unreachable and the match is over. The assert now tests that
  the detonation never resolves, which is the thing that matters.

## Open

1. **Rick's eyes on the clip, with sound.** The filmstrip is stills; the LAW is
   watch it at phone size WITH SOUND. No mp4 was cut this session.
2. **The name.** "Slagburst" was my pick, not an interview answer — flag it if
   it's wrong, it is one constant in the builder.
3. **The out-of-range cast plays the split SFX and splits nothing.** Reads as
   the blade flaring and finding nothing; a dedicated fizzle sound would be
   more honest.
4. **Phone perf, unmeasured** — now three ults deep in debt (v21 §3 + the
   Crucible + Daybreak's spark field + Slagburst's ≤9 shards, each a fill +
   a core fill + a streak stroke with shadowBlur ≤16). One paired QUICK run.
5. `tune.py` must still NOT be run blind — it would flatten both deliberate
   towers.
6. The next ult after this one: **Lightkeeper**. Bottom of the field in both
   seed sets AND `Bulwark` is the only ultimate in the game whose contribution
   a 2250-game paired test cannot separate from zero (+2.0pp, McNemar z=1.54).
   It is also one of the five remaining novas.

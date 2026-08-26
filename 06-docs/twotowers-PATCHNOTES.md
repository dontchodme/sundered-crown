# The Sundered Crown — Patch: THE TWO TOWERS
2026-08-15 · replaces build `ba423d8e6453592d` (v21)

```
sundered-crown.html   sha256 51c9bf566f9eb679   the game
sc-playable.html      sha256 710b5fd95d877e61   the public/share page, rebuilt from it
```

Drop both files over the live copies. `sc-playable.html` is regenerated from
the new game file by `share_build.py` (engine slice byte-identical, shell
patches unchanged) — do not ship the new game with the old share page, or
strangers get the old roster.

---

## For the players

**GRUDGEBEARER — Mountainfall is gone. THE CRUCIBLE is here.**
The ult no longer slams — it *lights*. The ball ignites with the fires the
hammer was forged in, the hammer spins up into a wheel of heat, and a black
hole forms that drags the opponent in. The first blow that connects consumes
every Sunder stack on the foe — each one adds +15% crit chance and +0.4x
crit damage (six stacks: a certain crit at 4.5x) — freezes the hall in
proportion to the meal, and sends the victim flying into high-speed bounces
off the arena. If the blow kills, the match holds its breath while the ball
flies — and shatters against the wall it meets, which stays cracked.
Whiffs fizzle at 4s: stacks kept, 18s cooldown restarts. Hex and hitstun
cannot stop the wheel while the forge is lit.

**DAWNBRINGER — Judgement is gone. DAYBREAK is here.**
No more pillar, no more free 34-point heal. For 5 seconds the relic radiates
white-hot fire, and every blow it lands throws six sun-shard sparks that
comet out of the impact, arm with a pop, and stand drifting in the hall.
They are a contested resource: an opponent touching one burns for 5 and is
shoved off it; Dawnbringer collecting one banks a stack of **Blessing**
(new status: heals 1.2 hp per second per stack, up to 5). The cast itself
does nothing — everything is earned by fighting during the window.
Dawnbringer's blade is repaid for losing its subsidy: damage up ~17%.

## Balance (7200-match sweep, 60 seeds x 120 pairings, 13/13 checks)

```
Grudgebearer   62.9%   the strongest ball, by design
Dawnbringer    53.0%   was the weakest at ~46; now the clear runner-up
the field      47.4 - 52.3, all sixteen inside the health bands
duration       39.0s mean, 0 timeouts
```

The other fourteen relics are PROVEN untouched: 6300 matches replayed on
both builds, identical field-for-field (engine A/B, both new ults keyed on
state only they set, zero stray rng).

## Technical notes

* Build chain: v21 ship + `ultforge_build.py` (Crucible) + `ultdawn_build.py`
  (Daybreak). Every tuned number lives in the builders, not the artifact.
* `CHANGES.diff` in this package is the full unified diff against the v21
  live file (1,031 lines), for audit.
* New SFX: forge ignition / implosion / fizzle (Crucible); spark arm chirp,
  burn sizzle, collect chime that climbs with the stack (Daybreak).
* Known debt, carried deliberately: nothing in this patch has been measured
  on phone hardware (Adreno 660). The new art is small-stroke by design
  (no full-canvas blur; spark field ≤48 small gradients) but that is an
  in-container proxy. If the live build feels heavy, `CINE.on` still
  toggles the cinema director live, and the spark cap is `sparks.length`.

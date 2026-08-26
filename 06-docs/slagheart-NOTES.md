# SLAGHEART and IRONBLOOM — the seventeenth relic

**2026-08-15.** `slagheart_build.py --src sc-introfit.html --out
sc-slagheart.html`, applied to the card-v3 tip `71c0a0c0c1ea6996`; result
**`f4d8aa660fe0ee0f`**, the new chain tip. `01-live` is untouched — still
v21's `ba423d8e…`.

Rick picked the cell off the shape × school grid (`05-reference/roster-grid.png`):
greatsword is the only complete row at 7/7, and **`mode:"chain"` had exactly
one relic**, so a second flail is the addition that says whether the chain
model generalises at all. Ult pattern: "pitch me options" → Rick designed it
himself. Power target: in the field, 46–52.

---

# 1. The relic

Flail archetype — reach 96, spin 2.2, mass 3.6 — carrying dwarven Sunder at
**+2 a hit** instead of the usual +1. It lands few, enormous blows, so three
connects cap the stack and it becomes its own damage amplifier.

That is the characterisation, and it is a *relationship* rather than a skin:
**Grudgebearer spends Sunder, Slagheart builds it, and they are the same
school.** The intro card puts them side by side and says so without a word of
explanation — `+1 SUNDER` / "consumes Sunder" against `+2 SUNDER` / "shrapnel
bounces the hall, sundering".

# 2. Ironbloom, in Rick's words

> "the flail head burns with the forges heat and if it connects within a time
> window it latches to the target causing massive hitstop and exploding
> sending its opponent flying. the explosion sends out shards of shrapnel
> that bounce around the arena and cause further damage and apply sunder if
> they connect. if they dont hit anything after a duration they explode"

`kind:"latch"`. Four beats:

```
LIT     the head goes orange. No banner, no damage, no assist. A 6.0s window
        opens and the charge does not rebuild while it burns — the 17s is
        owed from the RESOLUTION, bite or fizzle.
HELD    the first melee connect inside the window deals NO DAMAGE: the head
        bites. The chain snaps taut and the hall freezes for 0.8s — the
        longest freeze in the game, longer than a six-stack Crucible.
BLAST   26 damage, the foe shoved at 1800 over a raised speed ceiling, and
        nine splinters thrown into the hall. The name lands here.
SHARDS  each bounces up to 3 times, deals 7.5 and +1 Sunder on a connect,
        and pops where it dies if it never found anything.
```

Rick asked mid-build for "some screenshake and a special animation to the
latch hit stop too". The hold is a **frozen world**, so everything in it is a
pure function of the presentation clock: a standing wave on the tether rising
in frequency and amplitude, the head going orange to white, fissures of light
opening across the foe's shell, three charge rings collapsing inward each
faster than the last — and a camera shake that **ramps on t^2.2 instead of
decaying**, so the beat reads as pressure building rather than as a stall.
`05-reference/ironbloom-beat.png` is the hold in seven frames;
`ironbloom.mp4` is a real cast in a real fight at 24fps.

# 3. Why it is not the Crucible

A second dwarven light-it-and-connect ultimate is the real risk in this
build, and the answer had to be structural rather than cosmetic:

* **The Crucible pulls.** Ironbloom has no pull, no capture term, no assist.
* **The Crucible consumes Sunder** for one enormous strike. Ironbloom's
  strike is modest and it *sprays* Sunder — the payoff is the twenty seconds
  after the blast, not the blast.
* **The Crucible suppresses hits below a legibility floor.** Ironbloom has no
  floor; the flail's own 0.45 hit cooldown means the earliest bite is several
  tenths away anyway, so a floor would only waste the window.
* **The Crucible zeroes stun** while it burns, because it promises contact.
  Ironbloom promises nothing, so a hex still locks it. Probe [7] asserts the
  *opposite* of what the Crucible asserts, because copying that block would
  have been the easy mistake.

# 4. THE FINDING: the bite rate is a Poisson trial, and no weapon knob moves it

Ironbloom bites on **~61%** of its casts. The Crucible strikes on **85%**.
That gap cost two deleted mechanics before it was understood, and both
deletions are recorded in the builder because the measurements are worth more
than the code was:

```
1. A SPIN-UP — the bow's mechanic, "massive weapon rotation speed until the
   bow is pointed at the enemy":
     spinMul 1.0, window 4.5    bite 52% ±5    hits/s 0.210
     spinMul 2.6, window 4.5    bite 55% ±5    hits/s 0.208
     spinMul 3.4, window 5.0    bite 62% ±5
     spinMul 2.6, window 6.0    bite 69% ±4
   2.6x the swing rate bought THREE POINTS, inside the error bar, and moved
   hits/s not at all.

2. A CHAIN PAYOUT — the lit head swings on a longer chain, which does
   address distance:
     reachMul 1.0    bite 61% ±3   (155/256 casts)
     reachMul 1.5    bite 63% ±3   (163/260 casts)
   Two points. Also inside the error bar.
```

**The reason both failed:** the bite rate is not a weapon property. Slagheart's
natural connect gap is 5.7–6.2s, the window is 6.0s, and
`1 - exp(-6.0/6.2) = 62%` — which is the measurement, to within a point. It is
a Poisson trial on *the foe's position*, and no knob on the **weapon** moves
the **foe**. The Crucible gets 85% because it drags the foe onto the hammer:
it promises contact, so it was given a mechanism for contact. Ironbloom
promises nothing and is deliberately not given one — that is the entire
distinction between the two dwarven ultimates, and closing the gap would have
erased it.

So probe [10] asserts the **prediction** rather than a threshold. If the
observed rate ever drifts off `1 - exp(-window/gap)`, something is eating
casts, and that is a bug rather than a balance question.

The first version of that check demanded Ironbloom come within 20pp of the
Crucible. It failed — correctly — and the fix was to realise the check was
asking the wrong question.

# 5. massRef: closed, and it moves every fight in the game

Rick chose to fix it in this build. `physics.massRef` is the roster mass mean
and the config comment always said "if the roster grows, re-derive it or every
existing relic's fall rate shifts underneath you". It had been stale since the
six-relic roster: shipped **2.509**, neutral wanted **2.628**, and the whole
roster was falling **+2.3%** too fast. A seventeenth relic at mass 3.6 pushed
neutral to **2.680**.

Shipped at 2.680. Mean fall multiplier is now exactly **1.000**, drift +0.0%,
and backlog item 7 is closed.

**Both changes ship together and neither hides the other**, because they were
built and measured separately:

```
sc-slagheart-norm.html   the relic, OLD massRef
    engine_ab vs sc-introfit, 16 ids, 55 seeds x 120 pairings
    6600/6600 IDENTICAL field for field   <-- the relic is inert
sc-slagheart.html        the relic, NEW massRef
    engine_ab vs sc-slagheart-norm, same 16 ids
    4800/4800 DIFFER                      <-- the constant is not subtle
    Slagheart at dmg 41: 53.0% on the old constant, 45.9% on the new.
    massRef alone cost the heaviest new relic 7.1pp.
```

`massref_probe.py` also had an inverted verdict — it printed *"an assertion
would want 2.68 and would FAIL at 2.68"* on the day the drift was finally
closed. Fixed to state the verdict rather than the ask. A check that says FAIL
when the constant is right is worse than no check.

# 6. Tuning, by measurement

```
verify.py --n 60, all 136 pairings, massRef 2.680:
   dmg 38.5                   Slagheart 42.4%
   dmg 40.0                   Slagheart 45.3%
   dmg 41.0                   Slagheart 45.9%
   dmg 42.5 + shardDmg 7.5    Slagheart 51.5%   <-- SHIPPED
   dmg 44.0 + shardDmg 7.5    Slagheart 54.0%   (over the field)
```

Both knobs moved together on purpose: the design says the weight lives in the
aftermath, so the melee stays under Gravemourn's 44.1 and the splinters carry
the difference.

**Final field, 17 relics, verify 13/13:** Grudgebearer 62.9 · Dawnbringer 55.1
· **Slagheart 51.5** · Lightkeeper/Farwarden/Emberedge 50.2 · Aureole 50.1 ·
Censer 50.0 · Widowmaker 49.8 · Nightfell 49.0 · Heartwood/Gravemourn/
Goreshard 48.0–48.1 · Axiom 47.2 · Ironhail 47.0 · Spellbreaker 46.9 ·
Thornwake 45.8. **Both deliberate towers intact; the field is tighter than it
was at 16 relics** (45.8–51.5 against 45.9–54.2).

# 7. Every check

```
slagheart_probe   [0]  the head bites at all
                  [1]  the bite deals NO damage of its own (0.000 hp)
                  [2]  the hold is 97 frames vs 96 stated; the world is
                       frozen solid across it — positions, velocities, hp
                       and the shot list all unchanged
                  [3]  the shake RAMPS: 18 -> 58, 0 frames of decay
                  [4]  blast pays 26; shoves +1800 on the away-axis with the
                       vmax clamp lifted past 1300; 9 of 9 splinters spawn
                  [5]  a splinter sunders ONCE where the head sunders twice
                  [6]  splinters bounce ≤3, none outlives 2.6s, none ever
                       touches its own caster
                  [7]  the lit head buys NO stun immunity — the opposite of
                       the Crucible's assertion
                  [8]  deterministic: the blast spawns off shellHash, not rng
                  [9]  64 matches, 0 NaN, 0 unresolved, 39 bites -> 39 blasts
                  [10] the bite rate IS the Poisson prediction              16/16
engine_ab         6600/6600 identical on the 16 (relic alone, old massRef)   PASS
verify.py --n 60  13/13 over 136 pairings, Slagheart 51.5%                   PASS
introfit_probe    17/17 relics fit the card, 34/34 overflow bands clean      PASS
intro_probe       [1]-[6]                                                    PASS
tip_audit         0 gaps; ult tip 71 chars of 72                             PASS
massref_probe     mean fall multiplier 1.000, drift +0.0%                    PASS
anchors           15 edits, each hitting exactly once
```

# 8. Bugs this build caught in itself

* **The splinters spawned inside the hitbox.** `R + 6` is inside `R + s.r`, so
  all nine resolved on the foe on the frame they were born — ~50 damage and
  six Sunder in one instant, a burst and the exact opposite of the design.
  Fixed with an arming fuse (`arm: 0.12`) and a spawn clear of the shell, so
  what catches the foe afterwards is a *ricochet*. Caught by probe [5]
  reporting "+6 per shard".
* **Two probe checks that measured the wrong thing.** "No splinter touches its
  caster" was watching hp while the opponent was still swinging; "a splinter
  sunders once" was counting Slagheart's own +2 melee hits during the shard
  window. Both fixed by isolating (stun the other party). A failing check is
  not automatically a failing build — but you have to go and look.
* **`introfit_probe` printed a hardcoded "16/16"** while iterating 17 relics.
  The checks were right and the report was a lie. Now it prints what it
  counted.

# 9. What is owed

1. **WATCH IT, with sound.** `ironbloom.mp4` is silent and 24fps.
   Slagheart's four SFX voices (light, bite, blast, fizzle) have never been
   heard — and the bite's rising whine under an 0.8s freeze is the one cue
   that has to land or the hold reads as a hitch.
2. **The 0.8s freeze on a phone, at 4x speed.** It is the longest hold in the
   game by some way and nobody has watched it on a handset.
3. **Phone frame cost of the blast**: nine additive-gradient splinters plus a
   150px radial, on top of the standing phone debt.
4. **Same-type tape ties.** Slagheart vs Gravemourn is now a mirror on three
   of four tape rows — both sides light and the card says "everything is
   equal". Already on the backlog; the flail row makes it visible.
5. **Twenty-one free cells left** on the grid. Chain generalised without a
   single change to the chain model, which is the question this relic was
   picked to answer: the answer is yes.

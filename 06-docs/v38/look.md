# v38 — THE LOOK AT THE BLOODSWORN FLAIL, and a published number that was wrong

**2026-08-20.** Rick: *"lets build the next one"* → the axe and the staff are
held back until the current six types are filled → **the bloodsworn × flail
cell.**

No design work has been done and none should be until §1 exists in Rick's
words. What follows is the look-first probe, run before any of it, and the
correction it turned up in a number three documents already reason from.

```
tools/flail_probe.py          NEW   14/14
tools/contact_rate_probe.py   RESTORED from the Project + --noult   (v36 tool,
                                    never checked into the tree; its OUTPUT was)
05-reference/v38/flail-heads-6x.png
05-reference/v38/flail-arena-1to1.png
NOTHING WAS BUILT. Injection is runtime-only; no build was written to.
```

---

# 1. THE CELL HAS FINISHED ART AND NOBODY HAS EVER SEEN IT

`SHAPES.flailHead` dispatches on `p.key` and carries a branch for all seven
schools. The bloodsworn one — `_fhBarbed`, seven hooked barbs curving off the
ball with core-coloured beads at their tips — has been in the build unreachable.
Same situation `purpledagger_probe` and `whitescythe_probe` were written for.

**It is not the flat cell the matrix doc says it is.** §3 of the weapon matrix
called `flailHead` "genuinely school-neutral, so the palette swap carries it",
scored IoU 1.000, "the flattest cell in the game". The build's own comment
already records that this "turned out to mean nobody had tried". At 6x the
three chains are three different weapons: bloodsworn's barbs all sweep one way
so the head reads as *rotating* while standing still, umbral's `_fhEaten` has
half its spikes missing and a crescent bitten out of one side, dwarven's
`_fhBuilt` is eight riveted plates in an asterisk. **The bloodsworn flail
arrives with real art. That is unusual and it is worth knowing before pricing
the session.**

One thing to watch, and it is v37 §3.2 recurring: the barbs are drawn from
`_shade(p.steel, …)`, and bloodsworn's `steel` is `#EBD3D3` — near-white. **At
1:1 the only red on the head is the ball and the bead tips; the barbs carry no
school colour at all.** The palette does less work here than the sheet at 6x
suggests.

# 2. THE CHAIN IS REAL, AND THAT WAS CHECKED RATHER THAN ASSUMED

`_initChain` reads `f.w.mode` at MATCH CONSTRUCTION, and injection rewrites the
weapon before the Match exists, so it should hold. "Should" is how the Harrowing
shipped as twelve small arrows. Asserted directly, with a negative control:

```
headAng 4.8054 finite · headR 51.84 == reach*(1-hilt) 51.84
head lags the arm: max 0.695 rad, mean 0.314 rad over 120 steps
control: the spin-mode foe has no headAng at all
```

# 3. THE HAZARD IS THE OPPOSITE OF THE ONE THIS CELL LOOKS LIKE IT HAS

The obvious worry about giving bloodsworn a heavy is that it stacks too hard.
The measurement says look the other way.

Hemorrhage is bloodsworn's only channel and it **decays**: `maxStacks 4,
dur 3.2`. It has to be refreshed to mean anything. The flail is the
lowest-contact type in the game (§4). One contact every ~6.2 seconds against a
3.2-second window is a foe that is clean more often than it is bleeding.

Damage pinned at 14.0 across every relic and every foe, ultimates suppressed,
6 foes × 8 seeds:

```
                                  hits/s   mean    >=2    >=4   appl  refr%
THIS CELL  bloodsworn flail        0.147   1.15    41%    17%    6.0    43%
           bloodsworn twinblade    0.230   1.62    53%    28%    9.6    57%
           bloodsworn greatsword   0.235   1.72    55%    30%    9.6    58%
CONTROL    umbral flail (curse)    0.146   2.76    62%    34%    6.2    84%
CONTROL    dwarven flail (sunder)  0.148   1.85    52%    27%    6.2    55%
```

**Hemorrhage survives, at 71% of the twinblade's mean.** Not dead — 41% of the
fight at two stacks or more. Thinner, and specifically thinner.

**And the control says it is the CLOCK, not the chain.** All three flails share
reach, spin, mass and mode and their contact rates agree to 1.6%. The only thing
that differs is how long their status lives:

```
hemorrhage  dur 3.2   ->  mean 1.15,  >=2 for 41%
sunder      dur 5.0   ->  mean 1.85,  >=2 for 52%
curse       dur 99    ->  mean 2.76,  >=2 for 62%
```

So: **bloodsworn's status is a sustain status, and this is the type least able
to sustain.** That is a design constraint, not a defect, and it is the sharpest
thing this probe has to hand to whoever designs the ultimate. A weapon that
finds two stacks on the board 41% of the time cannot have an ultimate that
merely *spends* them — it would be a coin flip whether there is anything to
spend. Applying and spending in one motion is what Slagburst does with Sunder.

One reporting note: `>=1` and `>=2` are the same number, because `onHit`
applies 2 at a time and the foe is never at exactly 1. **Bloodsworn's ladder is
2 and 4, never 1 and 3.** Worth knowing before anyone writes a tip.

# 4. THE PUBLISHED CONTACT-RATE TABLE COUNTS ULTIMATES AS CONTACT

This is the part that outlives the relic.

`flail_probe` measured the two shipped flails — identical physics, damage
pinned — at **0.141 and 0.196 hits/s**, a 39% gap on a number that cannot vary.
With ultimates suppressed the gap is **1.6%**. Slagheart's Ironbloom sprays nine
shards and each one resolves a hit.

`contact_rate_probe.py` is v36's tool. It pins damage, and it explicitly checks
"spread within type" as its own guard — *"if two relics of one type disagree,
the type is not what is being measured"* — but **it never suppressed the
ultimate**, so the guard was reading the ult and the finding was never drawn.
Restored here with `--noult`, on `sc-twinshade-scrunch`:

```
type          relics  ULTS ON  spread   ULTS OFF  spread   ult share
bow                3    0.360   0.081      0.351   0.011         3%
twinblade          3    0.302   0.097      0.295   0.030         2%
greatsword         7    0.283   0.035      0.302   0.027        -6%
scythe             2    0.228   0.084      0.194   0.008        15%
flail              2    0.205   0.073      0.161   0.019        22%
warhammer          2    0.183   0.013      0.190   0.005        -4%
```

**Within-type spread collapses on every single type.** That is decision 1 —
type owns the physics — showing up as a measurement for the first time at this
resolution, and it was invisible while the ultimate was in the number.

Four relics carry almost all of it, and they are the four "many small objects"
ultimates:

```
lastlight  +0.080   the Harrowing's 12 scythes
slagheart  +0.072   Ironbloom's 9 shards
twinshade  +0.063   Triplicate's two copies
ironhail   +0.057   Quarrelstorm's 14 arrows
```

Everything else is inside ±0.04 and mostly slightly **negative** — removing an
ult lengthens the fight more than it removes contact.

## Two corrections to things already written down

**(a) The flail is LAST, not fifth.** The published table reads
`flail 0.205 · warhammer 0.183`. The weapon-only numbers are
`warhammer 0.190 · flail 0.161`. The flail is the lowest-contact type in the
game. This session used the wrong one of those two facts in its own §3 until
the correction landed, and the corrected number makes the hemorrhage finding
sharper rather than softer.

**(b) v36 §2's reach dominance is now a tie.** Greatsword over twinblade was
`0.283 vs 0.271`, +4.4%. Corrected: `0.302 vs 0.295`, +2.4% — inside the
twinblade's own 0.030 within-type spread. The greatsword does not out-contact
the twinblade; they are level. `purpledagger_probe`'s header quotes the old
ordering and should be footnoted.

**What the residual spread is, stated honestly:** with the ultimate gone, relics
of one type still differ by their STATUS — entangle slows the foe's swing, hex
stuns its weapon, sunder multiplies what it takes. The right column is not
instrument noise and the tool no longer calls it that. What the collapse shows
is only that the ultimate was the dominant term.

---

# Open decisions

1. **THE DESIGN, IN RICK'S WORDS — §1, and nothing starts without it.** Twice
   this order was skipped and twice the work was scrapped. The probe deliberately
   ships a placeholder nova and a placeholder name so that nothing here reads as
   a proposal.
2. **How many stacks a hit?** Both shipped bloodsworn relics apply 2. On a type
   that contacts once every 6.2s, 2 is what produced the 41% above. 3 or 4 would
   put the foe at the cap on a single contact and make the ladder 4-or-nothing.
3. **Does the ultimate spend hemorrhage, and can it?** §3 says a pure spender
   finds nothing to spend 59% of the time. Apply-then-spend in one motion is the
   shape that works, and Slagburst already owns it for Sunder.
4. **`p.steel` does no work on this head.** The barbs read grey at 1:1. Either
   bloodsworn's `steel` moves toward the core, or `_fhBarbed` takes its barb
   colour from somewhere other than `steel`. This is v37 §3.2 for the third time.
5. **Re-run every type-level measurement in the project with `--noult`.** §4 is
   almost certainly not the only place the ultimate was inside a number that was
   called a property of the weapon.
6. **`contact_rate_probe.py` is now in the tree and its old output is quoted in
   three documents.** Footnote them, or leave the corrected table as the single
   source and let the quotes rot.
7. **Still open from v37:** `01-live` is on sixteen relics against nineteen.

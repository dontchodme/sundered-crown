# THE BUILD OF RECORD NEVER HAD THE DRAIN IN IT

**2026-08-19/20, v37 round 6.** Rick, after four rounds of art revision:
*"i am still seeing nothing on the lifesteal animation"*.

He was right every time. **The effect was not in the file.**

# THE BUG

`liquid_build.py` does this:

```python
replace_span(s, "      if (f.hp >= f.hpGhost) f.hpGhost = f.hp;",
                "  }\n\n  decayImpactOnly(dt){",
                SLOSH_HOOK + "\n  }\n\n  decayImpactOnly(dt){", "slosh hook")
```

It replaces the **entire tail of `tickPresentation`** — from the health ghost to
the end of the method — with its own slosh hook. The drain's clock was inserted
in that span:

```js
for (let i = this.drains.length - 1; i >= 0; i--){
  const d = this.drains[i];
  d.t += dt;                                    // <- swallowed
  if (d.t >= d.delay + d.life) this.drains.splice(i, 1);
}
```

So on the build of record `d.t` never advanced. `drawDrains` skips anything
with `u = (d.t - d.delay) / d.life <= 0`. **Every strand sat at u <= 0 for
ever and not one of them was ever drawn.** No error, no warning, no failing
check. The relic build was correct. The file being watched was not.

Fixed by anchoring the drain clock on the **status-tag loop**, above the span.

# WHY FOUR ROUNDS OF CHECKS DID NOT CATCH IT

**Every check asked whether motes were SPAWNED.** Spawning was never what broke.
`m.drains.length` was the wrong quantity and it was the only one anybody
measured. The diagnostics agreed with themselves for the same reason: "frames
with a mote in flight, 48%" counted a list that never emptied because nothing
ever aged out of it.

**And every picture was taken of the wrong build.** `drain_iso.py` and
`drain_shot.py` defaulted to the RELIC build, where the drain works perfectly.
The video and the delivered file are the SCRUNCH build.

# THE TWO CHECKS THAT NOW EXIST

## `twinshade_probe` [12e] — does it reach the canvas

```
  14 strands born · clock reached 1.283s · peak 20 live at once
  deleting m.drains changes  AC.__draw: 167504 px of bbox
                             CINE.drawLerped: 167504 px of bbox
```

`CINE.drawLerped` is the path the **mp4** is rendered through — different code
from `AC.__draw`, and until this round only one of the two had been looked at.

**The shake had to be pinned first.** `draw()` offsets the hall by
`(Math.random()-0.5) * m.shake` on every call, so two renders of one state
differ across the whole frame; the first version of this check measured that
and reported a million differing pixels. v26 §4's standing "seeded RNG for
shake" decision arriving as a concrete obstacle, exactly as that note predicted.

## `chain_audit.py` — did every edit survive the chain

Reads the markers **out of the relic builder's own `*_NEW` constants** rather
than a hand-kept list, which would rot the first time the builder changed.
Negative control against a build with none of them: **18 LOST**, by name, with
the swallowed line printed. An untested failure path is worth nothing.

# WHAT THIS COST, HONESTLY

Rick said it three times. Each time the response was to make the effect louder.
**The first response should have been to prove the effect reached the file, and
it took until the third complaint to ask that question.** The tell was there the
whole time: the shipped build and the photographed build were different files,
and nothing in the workflow said so.

# Open decisions

1. **`liquid_build.py` replaces spans silently.** `replace_span` should hash
   what it is about to discard and refuse, the way `one()` does in the relic
   builders. The drain is simply the first insert that ever landed in that span.
2. Every measurement in the drain documents was taken on the relic build and is
   right about the code, wrong about the artefact.
3. Nine strokes per strand across up to 69 strands, unbenchmarked on phone.

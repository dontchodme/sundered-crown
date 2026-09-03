# VIGIL × TWINBLADE — WHAT ANY DESIGN FOR THIS CELL HAS TO CLEAR. Measured on the built-and-scrapped 34th relic.

**Claude Code, 2026-09-02. FOR WHOEVER DESIGNS THIS CELL NEXT.** Arclight and
Static were built to `ARCLIGHT-BUILD-BRIEF.md`, gated green, and scrapped by
Rick — *"i dont like what ive built. lets start over."* He has asked for a new
design for the same cell.

**Nothing in this file is a design and nothing in it proposes a mechanic**
(CLAUDE.md §3 rule 0). It is the set of numbers the last attempt produced, in
the order a designer would hit them. The full record is
`arclight-build-v64.md`; this is the part that is about the CELL rather than
about Arclight.

---

## 1. THE BUDGET IS SMALL, AND IT IS SMALL BEFORE ANY ULTIMATE EXISTS

`budget-v59.md` §3: ward is the most weapon-speed-sensitive status in the game
and the twinblade is the fastest weapon. Measured on the built relic:

```
   blade      win, ward on, NO ultimate at all       (330 fights a point)
   11.95                       54.2%                 the design's donor body
    8.30                       21.8%                 Twinshade's blade, the row floor
    4.00                        0.0%
    1.00                        0.0%
```

**At the twinblade row's own floor this body already wins one fight in five with
no ultimate, and at the donor body it wins more than half.** An ultimate for
this cell is being fitted into whatever is left under 50%, and that space is
much smaller than it is anywhere else on the board.

## 2. THE BLADE IS NOT A BALANCE LEVER HERE — IT IS BARELY A LEVER AT ALL

The same blades with a strong ultimate on top:

```
   blade    no ultimate        with STATIC        the blade is worth
   8.30          21.8%              93.9%
   4.00           0.0%              88.2%              -5.7 for -4.3 of blade
   1.00           0.0%              81.8%
   0.50           0.0%              80.6%              -13.3 over the whole range
```

**A relic winning nine fights in ten off its ultimate cannot be brought to the
band by a weapon that lands 26 scratches.** Taking the blade from 8.3 to 0.5
bought back 13 points where 31 were needed, and below `dmg 4` the body cannot
win a single fight in 330 — so there is no blade left to spend.

**The consequence for a design: this cell cannot promise "the blade gives it
back".** v64 §6 did (*"has to give back ~40 points at the blade"*) and it was
wrong for the built relic AND for the design's own model (D = 90.7% when
`storm_price` is re-run on the pinned runtime). **Whatever the ultimate is, it
has to be priced to land near the band on its own.**

## 3. TWO PAYOFFS ON ONE ULTIMATE CAN BE SUBSTITUTES, AND THEN NEITHER PRICES

Static had two halves — a ward feed and a detonation. Measured at the shipped
blade:

```
   delete the ward feed entirely          -3.6pp
   the ward feed ALONE, detonation off   +29.2pp over the no-ultimate floor
```

Both are correct. **Either half won the fight on its own, so the marginal value
of the second was almost nothing** — and every one-knob curve therefore
understated its own knob. Any tune that took one down looked nearly free and
changed nearly nothing, and the two had to come down together.

**For a design: if an ultimate here has two payoffs, price them jointly and not
one at a time**, or the sweep that chooses their numbers will read as flat when
it is not. `tools/arclight_sweep.py --combos blade:a:b` prices whole settings
side by side and exists for exactly this.

## 4. A LAB THAT BOUNCES THINGS OFF THE ARENA IS NOT MEASURING THIS HALL

`storm_price.py` clamps at the arena bounds (`x < P.rb`). The engine's own
projectiles use `n = this.inset`, and the seals walk that **0 → 140** across a
fight. Anything that flies, bounces or is placed in the room is running in a
room that gets smaller.

The built swarm reproduced the priced one on all five counts **while the hall
was open** and was five times the size once it had closed — which took a
60-object cap the brief called *"a safety, not a knob"* and made it a knob in 98
of 241 casts. **Any overlay written for this cell has to close the room.**

## 5. AND EVERY DECIMAL IN `06-docs/v64/` IS ON THE OTHER RUNTIME

`storm_price.py`, unmodified, on its own build, on the repo's pinned Chromium
151 rather than a Cowork container's 141:

```
   arm            here      published      delta
   A no ult      53.2%          56.9%       -3.7
   D - A         +37.5          +33.1       +4.4
```

A gate read against the published decimal called the build 7.8pp hot; read
against this reproduction it was 3.4pp and in band. **Run the reproduction
control before quoting a tier** — CLAUDE.md §4.2b, and it has now moved a gate
in both directions on two consecutive relics.

---

## What already exists, and rebuilds

- `tools/arclight_build.py --stage 1|2|3` rebuilds the three scrapped links
  byte-identically from `sc-lastthree`. The relic itself is in git at `4f022f4`.
- `tools/arclight_probe.py` — a swarm census that reads its own stage off the
  page, plus the render path CALLED against a real 2D context.
- `tools/arclight_price.py` — the four-arm budget shape on a BUILT relic, with
  a `--blade` override so it can be read against a design's donor body.
- `tools/arclight_sweep.py` — curves for the blade, for one number inside an
  `ult` block, and for whole candidate settings.
- `tools/_storm_pick.py` — a cast worth filming.

All five take `--relic`, so they are not Arclight-only. The measurements above
cost about 12,000 fights; a new design for this cell does not have to buy them
again.

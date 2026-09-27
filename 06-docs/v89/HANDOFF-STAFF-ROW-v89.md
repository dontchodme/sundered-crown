# THE STAFF ROW — seven relics designed by Cowork on 2026-09-27, handed off whole. READ `STAFF-ROW-v89.md` BEFORE BUILDING ANY OF THEM.

**Rick, 2026-09-27:** *"id like to get started building the staff weapon type.
id like you to design all of them at once and then we can hand off to code to
build them all. you design ill reject/accept."*

**Nothing is built.** Every cell is claimed in `06-docs/CLAIMS.md` as
`DESIGNED — RICK'S ACCEPT/REJECT OWED — THEN CODE'S`. Rick has read none of
them; the first thing that happens after this lands is his pass, cell by
cell, and only the survivors are Code's to build (rule 0: Code builds from
the doc and designs nothing; a rejected cell goes back to Cowork).

```
#   cell                    fighter / spell / ultimate            the sentence                                                                   bow → spell → whole (141)   blade   doc
43  bloodsworn x staff      BLOODWICK / Bloodseeker / GYRE        blood that bends toward the foe; it orbits the caster, then lunges as one      5 → 16 → 50.5% at 8.5     ~8.5    06-docs/v90/
44  umbral x staff          NIGHTGLASS / Shadebolt / BACKLASH     a bolt that ricochets twice; shrouded, half of every blow taken is thrown back  0 → 18 → 45.5% at 7.3     ~7.6    06-docs/v91/
45  vigil x staff           WATCHLIGHT / Wardbolt / BEACON        a bolt of light that shoves; a lantern set down fires at the foe, banking ward  6 → 21 → 49.7% at 9.3     ~9.3    06-docs/v92/
46  verdant x staff         BRIARWAND / Thornburst / BLOOM        a fan of three thorns; a pollen cloud drifts after the foe, entangling         22 → 23 → 53.8% at 17     ~16.5   06-docs/v93/
47  runic x staff           CIPHER / Glyph / CONVERGENCE          a bolt that hangs on the wall as a rune; every rune leaves its wall and hunts   10 → 31 → 50.5% at 11     ~11     06-docs/v94/
48  sanctified x staff      CROZIER / Lance / RADIANCE            a needle no blade can parry; every lance grows as it flies                     28 → 18 → 52.1% at 14.5   ~14.3   06-docs/v95/
49  dwarven x staff         CULVERIN / Slug / IRONFALL            an iron slug that falls; shells lobbed onto where the foe will be              22 → 24 → 47.9% at 13     ~13.2   06-docs/v96/
```

- **The type** (physics = the bow's; the shot block = the school's) and
  what the engine needs once are `STAFF-ROW-v89.md` §1 and §6.
- **How they were priced** and what to trust: `STAFF-ROW-v89.md` §4. Chromium
  141 in a Cowork container; every brief's stage 0 reproduces on 151 first.
  The control that can fail (v75's arm A on `sc-trunk`) passed to the fight:
  `06-docs/v89/runs/control_v75_trunk.txt`.
- **The order to build**, if the vetoes leave it alone: Culverin, Briarwand,
  Cipher, Watchlight, Crozier, Bloodwick, Nightglass (`STAFF-ROW-v89.md` §7).
  One at a time; each row goes to `BUILDING` when its build starts.
- **After the seventh lands, re-price the row against 41** before any blade
  is called settled — every one was priced alone against 34.
- **Names are Cowork's.** Every doc has the spread of four they came from.
- **Art and sound are specced, not rendered.** Rule 2's spreads happen at each
  build's last stage.

## What this batch did NOT do

- It did not touch the build (`sc-leaf` is the build of record; Axiom /
  Corollary is at stage 4 on the tip).
- It did not settle a blade. Every blade above is a bracket.
- It did not render a frame or a voice.
- It did not draw the staff. `shape:"staff"` is seven heads on one rod, and
  the rod is the first build's.
- It did not decide whether a staff should clank differently from a bow
  (`STAFF-ROW-v89.md` §8.3). Identical on purpose; Rick's to change once.

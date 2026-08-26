# v39 — THE RUNIC SCYTHE, AND THE CONVERSE. §1 FIRST.

**2026-08-20.** The cell was chosen from `cell_survey.py`'s measurement of all
twenty-two open ones and is written up separately (`-cell-survey-v39`). The
deep look at it, run before any of this, is in the same document at §5. What
those found that bears on the design:

- runic and the scythe both have **two relics**; the greatsword is full at
  seven, so the roster wants a scythe or a warhammer.
- hex holds ≥2 stacks for **18%** of a fight on this type and reaches its cap
  **1%** of the time — the shortest clock in the game on the second
  lowest-contact weapon.
- but **hex is a RATE, not a quantity.** One stack already shuts the foe's
  weapon every 1.15s; the ladder multiplies the rate. So 18%-at-two-stacks
  still delivers a weapon locked for 24.8% of the fight, +10.1pp of it hex's
  own. **An ultimate that reaches the CAP is worth far more here than one that
  merely applies.**
- runic has never had an ultimate that was not a `bolt`. Unmaking and Corollary
  are the same ultimate twice, differing by two damage.

---

# 1. THE DESIGN, IN RICK'S WORDS

    "when the ult procs the ball begins to leave behind small orbs. the orbs
     pulse a blue electric ring of damage while they presist. a line draws the
     orbs together. then at the end of the ult the artifact quickly reverses
     through the line, retracing its path. every time it makes it back to an
     orb it pulses again, this time larger, applying the status effect and
     dealing extra damage."

Four interview answers, and every one is load-bearing:

    the BALL ITSELF retraces, on rails, and is left at the OLDEST orb
    an orb is dropped every N units TRAVELLED, not every N seconds
    the line is PRESENTATION — it deals nothing
    NOTHING interrupts it once it procs. Not hitstun, not a true stun

## Four readings of the prose that are load-bearing

- **"leave behind"** — the trail is a record of where the caster HAS BEEN, and
  nothing in this engine has ever recorded that. `f.trail` is eighteen points
  of rolling art, overwritten four times a second. **This is a path memory, and
  it is new.**

- **"the artifact quickly reverses through the line"** — the caster comes off
  its own steering. Also new: the Crucible pulls the FOE, Dirge pulls the FOE,
  Ironbloom latches the FOE. Fourteen ult kinds and not one of them moves the
  ball that cast it. It is also the ultimate's price — the caster ends at the
  oldest sigil, which may be the far corner of the hall.

- **"every N units travelled"** — the failure modes decide it. Time-gated, a
  ball pinned in a corner drops every sigil on top of itself and the line
  collapses to a dot with nothing to retrace. Distance-gated, that same ball
  lays almost nothing — a **smaller** ultimate rather than an incoherent one.
  The trail becomes a record of where the fight actually went.

- **"nothing stops it"** — this is the one that breaks with v38, and
  deliberately. Bloodmill's counter is nameable: five relics of twenty carry a
  true stun and a viewer can learn who shuts it down. The Converse has none,
  and **the trade is paid in the telegraph instead**: the sigils are on the
  floor and drawn together by the line for four seconds before the reversal
  starts. What is coming is legible long before it arrives. An ultimate whose
  outcome is settled before it lands is *a foregone conclusion*, which is where
  the relic's name comes from.

---

# 2. WHAT IT IS, MECHANICALLY

```
id foregone · Foregone · runic · scythe · reach 104 width 11 spin 3.2
mass 2.4 · mode spin · onHit {hex:1} · dmg 22.0

ult CONVERSE · kind "retrace" · charge 15
    PHASE 1  THE LAYING, 4.0s. A sigil is dropped at the cast site and then
             every 130 units TRAVELLED, to a ceiling of 12. Each sigil pulses
             a ring every 0.62s: 2.0 damage inside radius 88, and NO status.
             The caster fights normally throughout. A line is drawn through
             the sigils in the order laid, and on to the ball — presentation.
    PHASE 2  THE REVERSAL, ~1.1s. The caster leaves its own steering and
             travels the polyline backward at 1600 u/s against a cruise of
             405. Reaching a sigil blooms it: 9.0 damage inside radius 130,
             and 2 stacks of hex. The sigil is spent. It ends at the oldest.
    NOTHING BREAKS IT. Not hitstun, not a true stun, not a hex.
tip "Leaves sigils as it moves, then rewinds its path through them"  60 of 72
```

## What was free

The pulses are `ring` + `hurt` + `apply` — the nova's own resolution with an
(x, y) that is not the caster's. `ballCollision` runs AFTER the reversal, so
the reversing ball shoulders the foe out of its way and the foe can crowd the
line; neither needed writing.

## What was new

A path memory, and a caster on rails. Both had teeth — see README §2 and §3.

## The zero-burden argument, kept structurally

    ALL STATE LIVES IN `f.ultTrace`, WHICH IS null ON EVERY OTHER RELIC.

`tickRetrace` returns on its first line when neither fighter has one. Unlike
the spike storm there is **no edit anywhere else in the tick** — the storm had
to touch the chain drive multiplier and argue an identity at rest; this one
does not. The only other guarded edit is one null check per beat in the
director's crowd condition. `engine_ab` 1710/1710 on the other twenty is the
proof, and the probe asserts it directly as well: `ultTrace` non-null on 0 of
1,447,981 frames across 342 matches without it.

---

# 3. WHAT IS NOT DECIDED BY THE PROSE, AND WAS DECIDED HERE

Recorded because they are the sentences a future session will want to argue
with, not because they are settled.

- **The weapon keeps swinging during the reversal.** Bloodmill's rule — the
  relic does not stop being a scythe because it is travelling. Consequence:
  the reversal connects on contact as well as on a bloom, at four times the
  usual closing speed. That consequence turned out to be most of the
  director's problem with it (README §5).
- **A sigil is dropped AT the cast site.** Without it a caster killed,
  cornered or pinned before it travels 130 units holds an ultimate made of
  nothing, and the reversal has no destination. It also makes the last thing
  the reversal reaches the place the ultimate was called from.
- **The small pulses apply no status.** Rick's sentence attaches the status to
  the bloom only. It also concentrates the whole hex payload into one second,
  which is what the cell needed.
- **Control returns at the pre-cast speed, not at 1600.** `move()`'s relax term
  takes 1/0.62 of a second to pay back an overspeed, so handing the ball back
  at reversal speed would fire it across the hall as a parting gift the design
  does not describe.

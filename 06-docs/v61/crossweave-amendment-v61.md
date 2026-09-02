# v61 — AMENDMENT TO CROSSWEAVE: THE TRIO IS HELD, AND THE VOLLEY ENDS IN A NOVA. Rick's design, taken in conversation on 2026-09-01 after watching the built relic, and written down here before a line of it is built.

**THIS IS RICK'S DESIGN, NOT THIS SESSION'S.** CLAUDE.md §3 rule 0. It is
recorded here because the standing lesson of v59-v62 is that a deliverable
living in a chat message does not exist, and because `gloamwire-design-v61.md`
is Cowork's and must not be edited by a builder.

**Amends `06-docs/v61/gloamwire-design-v61.md`.** Everything not named here is
unchanged.

---

# 1. WHAT PROMPTED IT

Rick, watching the shipped build in the app: *"seeing some of the arrows fire
without their lightning chains."*

Measured, and it is not a drawing fault — `drawStrands` failed to draw a strand
on a full volley **0 times in 495,566 arrow-frames**. It is the design's own
pairing rule, which the brief states: *a strand joins ADJACENT live arrows, and
a dead arrow breaks its links and does not re-form them.*

```
arrow-frames with a volley alive        495,566
naked — no live adjacent neighbour        31.5%
  a lone survivor, two siblings dead      28.2%
  two left, the MIDDLE one dead            3.3%
  all three alive and no strand             0.0%
```

**Only 51% of volleys still have all three arrows by the first frame they can be
drawn.** The bow looses from 88 units out along a facing sweeping at 2.8 rad/s
with the fan spread ±26°, so an outer arrow frequently meets stone inside a
tenth of a second. Of every Crossweave arrow: **85.7% wall, 7.5% parried, 6.9%
landed** — so it is overwhelmingly the wall, and an arrow that LANDS also breaks
the chain.

---

# 2. THE AMENDMENT, IN RICK'S WORDS

> *"what if the arrows stuck until all 3 had a chance to collide? that way their
> trio is always alive together"*

> *"the stuck arrow is inert, and the strand still shoves."*

> *"how about when all 3 connect the arrows explode in a nova for more damage and
> knockback?"*

> *"by all 3 connect i mean once all 3 arrows expire. so either by the wall or by
> hitting an enemy. should mean all of them explode"*

## 2.1 Settled by those four sentences

1. **AN ARROW THAT RESOLVES DOES NOT LEAVE.** It sticks where it expired —
   whether on the wall, on a parry or on the quarry — and stays as a strand
   anchor until every arrow of its volley has resolved.
2. **A STUCK ARROW IS INERT.** It has already had its effect. It cannot hit, be
   hit, be parried, or move.
3. **THE STRAND STILL SHOVES.** A strand anchored to a stuck arrow is a live
   strand and keeps its one-shove latch.
4. **WHEN THE LAST ARROW OF A VOLLEY RESOLVES, ALL THREE EXPLODE** — a nova
   each, carrying damage and knockback. The trigger is the volley COMPLETING,
   not a rare alignment.

## 2.2 What that costs, measured before it is built

**IT IS FEASIBLE AND THE TWO THINGS THAT COULD HAVE KILLED IT DO NOT.**

```
how long a stuck arrow sits    p50 0.37s · p90 0.92s · p99 1.38s · max 1.84s
first arrow of a volley dies   0.18s after it is loosed (p90 0.50s)
live net arrows now, peak      15
live if the trio is HELD, peak 23        against CONFIG.shot.maxLive = 64
```

**The cap does not bite.** `spawnShot` SHIFTS the oldest off the front at 64,
silently, which would have deleted the very arrows this mechanic exists to keep;
at a peak of 23 there is 2.8x of headroom. **And the hold is short** — half a
second at the median — so a wall does not grow a hedge of arrows.

**THE NOVA FIRES ON EVERY VOLLEY, AND THAT IS THE POINT AND THE RISK.** 24
volleys a cast at 5.9 a second, three detonations each — **72 novas in 4.1
seconds.** The strict reading of "all 3 connect" (all three landing on the
quarry) was measured first and is dead: **3 volleys in 8,315, 0.04%**, about one
per fifty fights. Rick's clarification replaces it.

> **THE FAILURE MODE TO WATCH IS DEADFALL'S, AND IT IS NAMED HERE SO IT CANNOT
> BE DISCOVERED LATE.** v54 shipped a pentagram that paid in five charges of
> `stamp/5`, putting five damage numbers over the ball across 42 milliseconds;
> every number was right and it read as noise. Rick's own fix was to make it ONE
> large mine. Seventy-two novas in four seconds is that shape again, and the
> question it has to answer is whether three detonations at three points read as
> one event.

---

# 3. WHAT IS NOT SETTLED, AND IS RICK'S

1. **THE NOVA'S RADIUS, DAMAGE AND KNOCKBACK.** Placeholders in the builder and
   swept, in this project's sense (CLAUDE.md §4.9) — but their SCALE is a design
   question, because 72 novas a cast at any meaningful damage is an enormous
   channel and the blade cannot absorb an arbitrary amount of it.
2. **DOES A NOVA FIRE FROM AN ARROW STUCK IN A WALL?** By §2.1.4 yes — all
   three explode. Named because it means most novas happen ON the wall rather
   than in the room, which is a different picture from three detonations around
   the quarry.
3. **THE SOUND AND THE BEAT.** Unchanged from the design's own open decisions,
   and now harder: the sound budget was already ~120 events in four seconds
   before this added 72 more.

---

# 4. WHAT THIS VOIDS

**THE BLADE, AGAIN.** `dmg` 9.5 was measured over 12,240 fights at `speedMul`
1.35 with no hold and no nova. Both halves of this amendment change the contact
rate, and the nova adds a damage channel outright. `gloamwire_sweep.py --only 0`
then `--only 1` re-runs it; the curve is four minutes and the wide pass about
six.

**AND THE STRAND'S PRICE.** Holding the trio means both strands survive the
whole volley rather than dying with their shortest-lived arrow, so there are
materially more frames in which a strand can reach the quarry. The shove is
already measured as a cost (design §6.2, −9pp across knock 0 → 400); more
shoves is not obviously more of the same and wants re-measuring rather than
assuming.

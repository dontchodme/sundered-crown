# STOP — THERE ARE TWO v60 DESIGNS FOR THE SAME CELL, AND THEY WERE WRITTEN IN PARALLEL BY TWO SESSIONS THAT COULD NOT SEE EACH OTHER

**2026-09-01 ~08:50 UTC.** Written by the Cowork session on discovering
`redhammer-design-v60.md` already in this folder. **Rick has not yet chosen
between them. Do not build from either until he has.**

```
06-docs/v60/redhammer-design-v60.md      Claude Code, 08:35 UTC
                                         bloodsworn x warhammer
                                         ULTIMATE: the hammer throws the quarry
                                         into a WALL and the wall pays, scaled by
                                         arrival speed. Direction taken from four.
                                         Not named, not built, §1 "not yet sentences"

06-docs/v60/wirering-design-v60.md       Cowork, 07:4x UTC
06-docs/v60/ravelbone-build-brief-v60.md bloodsworn x warhammer
                                         ULTIMATE: RAVELBONE / GARROTE — the hammer
                                         winds up, a barbed wire ring at its hit
                                         range SNAGS the foe (ball held, weapon
                                         free), the head comes around, hits, throws,
                                         and the ring explodes consuming Hemorrhage.
                                         Named, priced over 26 arms, staged brief
```

**Same cell. Same session version. Different ultimates.** Rick answered design
questions in both conversations. Neither session was told about the other.

---

# THEY ARE NOT ACTUALLY RIVALS, AND THE OVERLAP IS THE INTERESTING PART

GARROTE's payoff is *"the connection deals massive knockback"* — priced at
**+4.9pp for the first doubling and nothing beyond it** (`wirering-design-v60.md`
§5b). It was measured for VALUE and never for whether it READS.

**`redhammer-design-v60.md` §3 answers exactly that question, and the answer is
no:**

- The impulse is real and exactly `knock x knockMul` — 379.5 — but *"most of the
  impulse is spent cancelling the incoming velocity rather than adding to it"*,
  because the quarry was moving toward the attacker, which is why they touched.
- And *"speed is governed, not conserved"* — `move()` clamps to [250, 1300] and
  relaxes toward an energy-derived target at 0.62, so whatever survives washes
  out inside the 0.41s median flight to a wall.
- Its repair, Rick's from four: `launch` (a permission to exceed the ceiling,
  which adds nothing on its own) **plus a separate impulse**. Measured optimum
  **kick 800**, and the Crucible's own 2400 is *the single worst value in the
  sweep for a mechanic that pays per blow rather than once*.

> **So Garrote's headline effect is weaker on screen than its lab number
> implies, and the red hammer document already contains the fix.**

## AND THE SNAG MAKES THE WALL-SLAM WORK BETTER, NOT WORSE

`redhammer` §3's whole problem is that the impulse is spent reversing a quarry
that was moving toward the hammer. **A snagged ball has no incoming velocity to
cancel** — `f.pin` holds it still. So a connect delivered to a pinned foe is the
one case in the game where the full impulse goes into departure.

**With one condition, and it is `ravelbone-build-brief-v60.md` §4:** `move()`
discards every impulse a ball took while pinned. Release the pin, clear `pinV`,
*then* kick. In the wrong order the ball does not move at all.

---

# THE THREE WAYS OUT, FOR RICK

1. **MERGE.** The wire ring is the delivery, the wall-slam is what the connect
   does: the ring holds you, the head comes around, and it throws you into a
   wall hard enough that the wall pays. Both documents' measurements survive;
   Garrote's knockback stops being a number and becomes the loudest event in the
   game. This is the recommendation.
2. **RAVELBONE ALONE**, and the red hammer's `launch`/kick finding is folded in
   as the connect's impulse (kick 800, launch 1.2s) rather than a bare 2x.
3. **THE RED HAMMER ALONE**, and Ravelbone's ring is retired — in which case
   `wire_lab.py` and the snag result still stand as the answer to
   "is `f.pin` without `f.stun` worth anything", which is +4.4pp and unused.

**Whichever is chosen, one of these two documents should be renamed to
`-SUPERSEDED` rather than deleted.** Both contain measurements the other does
not, and both registered predictions that were tested.

---

# WHAT IS TRUE IN BOTH, AND IS NOT IN DISPUTE

- The cell is **bloodsworn x warhammer**, bloodsworn's last open cell, and both
  sessions priced it as the warhammer row leader (+22.1% at 280 fights on the
  Breach tip; +16.3% at 270 on the Shroudmaul tip).
- The art is `_whBarbed` and Rick has already ruled *"leave it, it's fine"*
  against its 50.8% ink diff. **Do not re-raise it** — `redhammer-design-v60.md`
  §0.1, and the Cowork session independently rendered it in colour and agreed it
  is the best-looking candidate on the board (`cell-error-v60.md` §5).
- **BLOODMIRROR (the 30th) IS STILL AHEAD OF THIS IN THE QUEUE** and its brief
  is not in this repo. It lives in the Cowork project as
  `claude/sundered-crown-bloodmirror-build-brief-v59.md`, with
  `spectre-design-v59.md`, `budget-v59.md`, `tip-surface-v59.md` and
  `sc_spectre_lab.py`.

---

# RESOLVED, 2026-09-01. RICK TOOK ROUTE 2 — RAVELBONE ALONE

> *"Ravelbone alone"* — with the red hammer's finding folded in as the
> connect's impulse rather than a bare 2x knock.

`redhammer-design-v60.md` is renamed `redhammer-design-v60-SUPERSEDED.md` and
NOT deleted, because two things in it are load-bearing for the build that won:

- **§3, which refutes Garrote's own headline effect.** `|dv|` is exactly
  `knock x knockMul` and the departure speed barely moves, because the impulse
  is spent reversing a quarry that was travelling toward the hammer and because
  `move()` governs speed rather than conserving it.
- **§4.1, the kick sweep, and the finding that the shipped build was already
  clipping at `speedMax` 1300 while P1 read a healthy 2.96.** Copying the
  Crucible's `launch: 2400` would have reproduced that defect one ceiling
  higher; **kick 800 with `launch` 1.2s** is the measured optimum for a
  mechanic that pays per event.

So GARROTE's connect is **not** the brief's bare `knock x2`. It is the normal
blow's knock plus a **separate impulse of 800 under `launch` 1.2s** — which
`wirering-design-v60.md` §5b says costs nothing (flat past 2x) and
`redhammer-design-v60-SUPERSEDED.md` §4 says is the difference between a throw
that reads and one that washes out inside its own 0.41s flight to the wall.

**This changes the conditions of the registered prediction in
`ravelbone-build-brief-v60.md` §11**, which names "knock 2x". The VALUE should
be unchanged — §5b measured x2 and x5 within 0.3pp — so the +30 claim still
stands as a test. It is no longer a clean test of the connect as specified, and
this paragraph is here so nobody reads a pass as confirming a number nobody
shipped.

`wire_lab.py`'s snag result stands and is now used rather than stranded.

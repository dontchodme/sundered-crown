# THE WINNOWING'S HIT STOP — THE BUILD (v67). The freeze is the size of the rung.

**Claude Code, 2026-09-06. Built from `WINNOWING-HITSTOP-BRIEF-v67.md` and from
nothing else — CLAUDE.md §3 rule 0.** Rick watched Thornshear: the hit stop
*"reads as lag even though its probably not."*

```
stage 1   the two edits    sc-trunk.html -> sc-leaf.html    GREEN
```

`tools/winnow_hitstop_build.py`, `tools/winnow_hitstop_probe.py`.

---

## 0. THE DIAGNOSIS WAS A STOP CONDITION, AND IT HELD BY A FACTOR OF FIVE

The brief makes gate 2 a gate on the BUILD HAPPENING AT ALL: *"publish the
BEFORE number from the unpatched tip first — if it is not several hundred ms a
cast the diagnosis above is wrong and the build stops."*

`winnow_hitstop_probe.py` on `sc-trunk`, 96 fights, 279 windows (a window being
the cast until the last kunai is gone, which outlives `ult.dur` 4):

```
FROZEN SECONDS A CAST      1.825s   median 1.792   max 3.192
FROZEN SHARE OF THE WINDOW  22.9%
freezes this relic caused    7304    6002 kunai · 1302 blade · 45 kills
writes at or under 0.060s    5433 of 7304
```

**Nearly a quarter of every Winnowing window was a frozen frame**, and three
quarters of the freezes were chip hits. The brief predicted "several hundred
ms"; it is nearly two seconds.

The cause is exactly as the brief read it: `stopBase` is a FLOOR —
`min(stopMax, 0.045 + dmg × 0.0022)` — so it does not scale down for a chip,
and a 1.8-damage leaf was holding the whole picture for about half of what a
30-damage swing holds. Sixty-odd of them, at irregular moments, over five or
six seconds. **That is what a dropped frame looks like.**

---

## 1. WHAT WAS BUILT

Two edits, one relic, and no new field on any other projectile.

- **`spawnKunai`** — the shot gains `over: { stop: 0 }`. `over.onHit` and
  `over.knock` stay undefined, so entangle and the kunai's own 260 knock are
  untouched.
- **`kunaiRung`** — after `s.rung++`, `s.over.stop = 0.02 * s.rung`, written
  with the other growth, which is **one definition for both reflection paths**
  (wall and parry both come through here).

`resolveHit` already does the rest, and it is Scour's code: `if (over &&
over.stop !== undefined && !fatal) stop = over.stop;` then `if (stop > 0)`.
**The builder refuses to write if either of those has moved**, because two
fields are worth nothing without the rule that reads them.

**SCOUR IS THE PRECEDENT AND IT IS EXACT.** `over.stop` exists because a grind
at 7 ticks a second would have frozen the world for 45% of every second it held
someone — *"a grind is the one thing in this game that must not stutter."* A
ten-kunai fan is the same sentence with a different noun; the Winnowing simply
shipped a version earlier and never got the ruling.

---

## 2. THE GATE

### 1. The roster did not move, and Thornshear did

```
engine_ab  sc-trunk -> sc-leaf, the 33 OTHERS   4224/4224 IDENTICAL
engine_ab  with Thornshear in (9 relics, 8 seeds, 36 pairings)
                                                64 of 288 DIFFER
```

**64 is exactly 8 Thornshear pairings × 8 seeds.** Every other pairing is
identical. `engine_ab` prints FAIL because it is built to demand identity;
differing on precisely those and nothing else is the pass, and it is what the
brief predicted — a Winnowing cast now inserts less frozen time into `t`, and
the seals fire on `t`.

### 2. The freeze census, before and after

```
                              BEFORE     AFTER
frozen seconds a cast         1.825s    1.142s
frozen share of the window     22.9%     16.4%
freezes caused                  7304      5992
  kunai                         6002      4687
  blade                         1305      1305
  kills                           45        40
hits that wrote NOTHING            0      1201
```

The brief's three exact conditions, met exactly:

```
rung 0 ordinary freezes    0            (and 1201 hits now write nothing at all)
rung 1 / 2 / 3             0.020 ×1841 · 0.040 ×1797 · 0.060 ×1035
a kill                     0.550 ×40    unchanged
```

**And the rung buckets equal the size buckets, 4673 = 4673**, which is the
invariant that says nothing is mis-attributed.

**BLADE FREEZES ARE UNCHANGED AT 1305 EITHER SIDE**, which is the control this
table needed: the patch reaches the kunai and nothing else the relic does.

### 3. verify, and the one number that had to be checked properly

The brief says a change to the match clock alone should not move Thornshear
beyond the n≈700 noise, and that anything more is *"a finding, not a fix"*.

`verify --n 40` reads Thornshear **40.3% → 43.6%**, which looks like 3.3pp. It
is not: at n=40 a pairing that figure is one fight per pairing wide. Measured
directly, **both sides, two seed blocks, n=1320 each**:

```
sc-trunk   42.3%   43.0%        block spread 0.7pp
sc-leaf    44.4%   43.2%        block spread 1.2pp
```

**+1.15pp against a within-build spread of 0.7–1.2pp — inside the instrument.**
No finding, and no number moves.

### 4. AND A THIRD verify RED THAT IS NOT THIS PATCH

`sc-leaf` is **10/13** against `sc-trunk`'s 11/13. The new one is *"both sides
can win every matchup — Axiom vs Thornshear 0/40"*. Measured on the same
pairing, same seeds, both builds:

```
              n=40              n=300
sc-trunk      39/40  (97.5%)    289/300  (96.3%)
sc-leaf       40/40 (100.0%)    291/300  (97.0%)
```

**Thornshear already beat Axiom 96.3% of the time before the patch.** The
pairing sat one fight from the boundary of a ZERO-TOLERANCE check at a sample
of forty, and a 0.7pp nudge tipped it. It is not a balance change and it was
not caused here.

**It is worth writing down as its own thing, though**, because it is open item
12 pointing the other way: that item records Thornshear losing four fights in
five to every bow, and this is the same concentration at the top — a 96%
pairing that no per-relic band can see. Rick's, and unchanged by this build.

### 5. One fight, filmed, on both builds

`07-shorts/v67/winnow-before-cut.mp4` and `winnow-after-cut.mp4` — Thornshear
vs Lastlight, **seed 8986**, the Winnowing at 17.1s, chosen as the worst-freezing
cast of 48 examined (**2.07s frozen of an 8.68s window**). Same seed, same cast,
one number different. **Rick said it reads as lag; whether it still does is his,
and that is gate 4.**

---

## 3. OPEN, AND WHOSE

1. **Whether 0.06 at rung 3 reads as "bigger".** The brief's own open item 1, a
   picture question, and it is Rick's from the pair above rather than in words.
2. **THE APP POINTER HAS NOT MOVED.** `app/main.js` still reads `sc-trunk.html`.
   This is one link cleanly on top of it — not a fork — and moving it is one
   line the moment the clip reads right. **It is deliberately not moved before
   gate 4**, because the pointer is what the app and every future short read.
3. **Every other many-hit ultimate still carries the default weight on each
   hit** — Crossweave's arrows, Corona's ring ticks and its stars. Those are
   `HITSTOP-BURST-BRIEF-v67.md`'s, which is why Rick took both, and it is the
   next job.

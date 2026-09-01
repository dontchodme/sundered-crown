# STOP — THERE ARE TWO v61 DESIGNS FOR THE UMBRAL BOW, AND IT HAS HAPPENED AGAIN

**2026-09-01 ~19:40 UTC.** Written by the Cowork session that produced
`gloamwire-design-v61.md`, on returning from a dropped device bridge to find
`quiver-design-v61.md` already in this folder. **Rick has not chosen between
them. Do not build from either until he has.**

This is `06-docs/v60/CONFLICT-READ-FIRST-v60.md` one cell along — the same
failure, six hours later, on the next relic. **That is now a pattern and not an
accident**, and §4 is about the pattern rather than the relic.

```
06-docs/v61/quiver-design-v61.md          19:30 UTC   umbral x bow
06-docs/v61/bow-row-at-garrote-v61.md     18:52 UTC   against sc-garrote, 30 relics
                                          ULTIMATE: QUIVER — a window in which
                                          every arrow that ends on a WALL sticks
                                          there and remembers; when the window
                                          closes they all come back at once,
                                          each along its own flight reversed.
                                          Mechanic, art and aim rule all chosen
                                          by Rick off priced spreads. dmgMul
                                          0.55, worth +21.0pp. Not yet named.

06-docs/v61/gloamwire-design-v61.md       09:45 UTC   umbral x bow
06-docs/v61/GLOAMWIRE-BUILD-BRIEF.md                  against sc-breach, 29 relics
tools/net_lab.py                          GLOAMWIRE / CROSSWEAVE — the bow gains
                                          a triple shot at twice the cadence, a
                                          magazine of 24 volleys, each volley
                                          strung with two bars of lightning
                                          WIDER than its own arrows. An arrow
                                          damages; the lightning alone shoves.
                                          Named, blade 9.2, worth +48.8pp,
                                          staged brief written.
```

**Same cell. Same version folder. Different ultimates. Rick answered a full set
of design questions in BOTH conversations** — Gloamwire's strand width, fan
shape, window shape, composition, and both names; Quiver's mechanic, art and aim
rule. Neither session was told about the other.

---

# 1. THEY ARE NOT EVENLY MATCHED, AND THE GLOAMWIRE SESSION SAYS SO ABOUT ITS OWN WORK

Two facts decide this before taste does.

**a. QUIVER SPENDS THE ONE NUMBER THIS TYPE HAS NEVER SPENT, AND GLOAMWIRE'S OWN
DOCUMENT SAYS THAT IS THE BEST GROUND ON THE ROW.** `gloamwire-design-v61.md`
open decision 7, written before `quiver-design-v61.md` was known to exist:

> *"v40 OPEN DECISION 2 HAS NOW SURVIVED SIX BOW RELICS. 82% of every arrow
> ends on a wall, ten times the leverage of any status on the row, and Gloamwire
> does not address it either."*

Quiver addresses it. That is not a tiebreak invented after the fact — it is the
Gloamwire session's own registered complaint about the Gloamwire design, and the
other session went and built the thing.

**b. GLOAMWIRE'S NUMBERS ARE MEASURED ON A ROSTER THAT NO LONGER EXISTS.**
`sc-breach.html`, 29 relics, before Ravelbone. Quiver is measured on
`sc-garrote.html` at 30. Every Gloamwire win rate — the 51%, the +48.8pp, the
whole composition grid that chose blade 9.2 — is subject to re-measurement.
Its *geometry* is not: §4 is algebra (an arrow reaches `R + shot.r` = 58, a
strand reaches `R + strandW`, they cross at `strandW = 24`) and a roster change
cannot touch it.

> **On the merits as they stand: Quiver is the stronger candidate.** Better
> ground, current measurements, and the cheaper build. This document is written
> by the session whose design that verdict goes against, and it is the honest
> reading.

---

# 2. BUT THEY COMPOSE, AND THAT IS THE INTERESTING OPTION — WITH THE ARITHMETIC MARKED AS UNMEASURED

**Crossweave is a LOADER and Quiver is an EMPTIER.** They act on the same
resource from opposite ends and neither document knows it.

```
quiver-design §2.1   an 8s window banks a median of 16 wall arrows
                     (ordinary fire: 1 arrow every 0.34s, 82% end on a wall)

gloamwire  §5        Crossweave fires 3 arrows at twice the cadence
                     -> SIX TIMES the arrow rate for its 4.1s
```

Six times the arrows into the same walls. **UNMEASURED AND THE ARITHMETIC IS NOT
THE MEASUREMENT** — but a Crossweave window inside a Quiver window banks on the
order of ninety quills where Quiver alone banks sixteen, and Quiver is already
worth +21.0pp at sixteen. As a straight stack it is certainly broken.

As ONE ultimate in two phases it may be the best thing in either document:
**the bow triples its fire and floods the walls, then everything it missed with
comes back at once.** That is a set-piece with a beginning and an end, it
spends the type's dead 82%, and it makes Gloamwire's lightning the picture of
the loading phase rather than a mechanic that has to justify itself.

Three things a merge would have to settle, all real:
- **The magazine, not a duration.** Gloamwire §5: under a fixed volley count the
  fire rate costs +13pp; under a duration it costs +37pp. A loader phase must be
  counted, not clocked.
- **The weight collapses.** Quiver §3.2 found `dmgMul` free between 0.40 and
  0.70 *at 2.5 quill hits a cast*. At ninety banked quills that finding does not
  transfer and the weight has to be re-priced from scratch.
- **Gloamwire's strand is balance-free** (§4.2: arrow contacts sit at 7.0-7.5
  across a doubling of `strandW`), so the lightning can survive a merge purely
  as picture at no cost to the sheet. That is the cheapest thing to keep.

---

# 3. THE THREE WAYS OUT, FOR RICK

1. **QUIVER ALONE**, and Gloamwire is renamed `-SUPERSEDED`. The verdict §1
   supports. What should be carried across even so: `net_lab.py`'s crossover
   algebra (§4) if any strand or multi-arrow art is ever wanted, and the
   magazine-vs-duration finding (§5), which is a general result about `cadMul`
   and applies to any windowed bow ultimate including Quiver's.
2. **THE MERGE.** §2. The strongest picture in either document and the most
   work: a two-phase ultimate needs its own lab, and both weight tables are
   void inside it.
3. **GLOAMWIRE ALONE**, and Quiver is renamed `-SUPERSEDED` — in which case its
   §2 bank ledger (10,804 arrows, zero unclassified, the wall at 83.4% split
   almost exactly perimeter-proportional) stands as the best description of this
   type anyone has written and should be kept wherever it can be found.

**Whichever is chosen, rename the loser `-SUPERSEDED` rather than deleting it.**
v60's rule, and both documents hold measurements the other does not.

---

# 4. THE PATTERN, AND IT IS NOW COSTING MORE THAN THE RELICS

Two collisions on consecutive relics, same shape both times:

```
v60   bloodsworn x warhammer   Cowork (Ravelbone) vs Claude Code (red hammer)
v61   umbral x bow             Cowork (Gloamwire) vs Cowork (Quiver)
```

**v61 is the worse of the two**, because both sides were Cowork sessions asking
Rick design questions — so he made two full, incompatible sets of choices about
one relic in one day, and the second set was made without either him or the
session knowing the first existed.

The v60 note recorded the collision and did not propose a mechanism. One is
proposed here, because a note that only observes will produce a third:

> **A DESIGN SESSION SHOULD CLAIM ITS CELL IN THE REPO BEFORE IT ASKS RICK
> ANYTHING**, and read the claims first. One file, `06-docs/CLAIMS.md`, one line
> per open design: `<cell> | <session> | <UTC> | <status>`. Written at the
> moment the cell is chosen — which is *before* the first survey, let alone the
> first spread of names. Both v61 sessions would have seen it: this one claimed
> `umbral x bow` at 07:33 UTC, the other at ~18:45.

It is one file and one line. **The alternative is that the next parallel pair
costs a third relic**, and this one cost Rick a full day of design decisions he
now has to throw half of away.

Two smaller things this collision also surfaced:

- **THE RELIC NUMBER HAS DRIFTED AGAIN.** `gloamwire-design-v61.md` calls the
  umbral bow the **32nd**, counting design order (Bloodmirror 30th, Ravelbone
  31st). `bow-row-at-garrote-v61.md` calls it the **31st cell**, counting what
  is built — Bloodmirror is designed and is in no link. Both are defensible;
  they must not both ship. v57 had this exact drift and CLAUDE.md §0 is where it
  gets settled.
- **`tools/bow_survey.py` WAS TOUCHED AT 07:32 UTC**, one minute before the
  Gloamwire session opened the repo, and that session noted the fresh mtime and
  dismissed it as a git artifact. It was the other track starting up. **A
  modified tool with a fresh timestamp is a claim signal and was read as
  noise** — which is the same failure the CLAIMS file above is for, arriving
  through the only channel that existed.

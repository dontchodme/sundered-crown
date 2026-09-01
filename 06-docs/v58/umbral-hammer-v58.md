# v58 — THE UMBRAL WARHAMMER, REDRAWN. Rick rejected `_whEaten`; this is what replaces it, why the grammar and not the function was at fault, and what Claude Code has to do with it.

**Read `06-docs/v56/SHROUDMAUL-BUILD-BRIEF.md` §3.2 first**, because it says
*"`_whEaten` ALREADY EXISTS ... THE SILHOUETTE IS NOT NEW WORK"* — and that
sentence is now the wrong call. Nothing else in v56 moves: the relic, GRASP,
every number in §3.3 and every gate in §6 stand. **This is art only. `SHAPES`
is render-only and `engine_ab` must be bit-identical on all 28 after it.**

```
IN    02-chain/sc-grasp.html          the build of record
OUT   02-chain/sc-gnawed.html         one function replaced, one dispatch line
```

---

# 0. WHAT RICK SAID

> *"umbral hammers silhouette looks pretty bad. can we take another stab at its
> design? the hammer with blocks attached to it idea just isnt working for me"*

and on the first cut of the replacement:

> *"upclose the spikes just look like triangles layered behind the hammer. can
> we make them look truly attached?"*

He also sent three references, unprompted, and they agree with each other more
than any three references usually do:

```
1  a bone-and-iron warhammer: a long curved horn off the top of the head, a fan
   of spurs off the back, a skull set in the cheek, a clawed pommel
2  a chunky rectangular head with triangular teeth right round its perimeter,
   violet, on a dark wrapped haft
3  a NEAR-BLACK block head with long glowing violet spikes off the top, front,
   bottom and back, and lit inset panels in the cheek
```

**What all three share: spikes that break the outline, and a dark body with the
colour glowing INSIDE it.** Neither of those is what umbral's hammer was doing.

---

# 1. THE DIAGNOSIS, AND IT IS ABOUT THE GRAMMAR

`_whEaten` was **purely subtractive** — call `_whBase`, then punch two blobs and
a haft slot out of it with `destination-out`.

**Subtracting from a shape that is already rectilinear does not produce an
absence. It produces smaller rectangles.** The haft came apart into two bars
with a gap between them; the head became a lump with corners bitten off; the two
`p.core` wisps drawn afterwards read as detached shards. A stick, a gap, a
stick, and some blocks — which is, precisely and fairly, *"the hammer with
blocks attached to it."*

The silhouette doc's §3.1 table is the reason it is only umbral that has this
problem on this row:

```
runic       a floating cluster            ADDS a contour
verdant     a burl and three thorns       ADDS a contour
bloodsworn  six hooks and a return spur   ADDS a contour
sanctified  a halo standing off behind    ADDS a contour
dwarven     langets and proud bolt bosses ADDS a contour
vigil       four stacked stepped plates   ADDS a contour
umbral      two bites and a slot          REMOVES one          <--
```

**Removal is the weakest silhouette operation there is**: it takes area without
giving the outline a new event, and at phone size the holes close up under the
bloom and the mask reverts toward the base hammer. Worse, on THIS type it eats
the wrong thing — a hammer's whole argument is that the mass is at the end, and
`_whEaten` bites the mass.

## 1.1 AND THE NUMBER NEVER SAW ANY OF IT

Measured on a faithful rebuild of the shipped shapes (see §5 for why that
caveat matters), `_whEaten` scores **0.382 against its nearest sibling** — inside
the 0.32–0.45 band the silhouette doc calls *"distinct, and still recognisably
one weapon type"*. **By the metric it was fine. It was not fine.**

> This is silhouette doc §4.3 for the second time — the runic scythe scored 0.20
> either way while the crescent was not being drawn at all. **A number that is
> easy to compute is not thereby the number you want.** The instrument to trust
> on this row is `--sheet`, and the reviewer is Rick.

**`06-docs/v57/cindercleave-design-v57.md` §6 already wrote this down** — that
the 78.6% in v56 §3.2 measures separation from the other six schools and says
nothing about whether the shape is any good, and that both briefs leaned on it.
That was written before Rick saw the hammer. This document is the same finding
with a picture attached, and it should settle it.

**AND THE TWO NUMBERS ARE NOT THE SAME INSTRUMENT.** v56 §3.2's *78.6% distinct*
comes from `cell_survey`, on an INK mask, against the fifteen open cells. §5
below is `silhouette_probe`'s IoU, on a SILHOUETTE mask, against the six
warhammer siblings only. They disagree — 78.6% distinct would be an IoU of
0.214, under the 0.30 floor, where §5 measures 0.382 — and this session cannot
reconcile them from the docs alone. **Do not quote one as if it were the other,
and do not treat that gap as settled until somebody runs both against the same
build.** It may be nothing more than two masks and two comparison sets; it may
also mean one of the two instruments is being read wrong somewhere in the
chain, which would matter well beyond this cell.

## 1.2 ONE THING TO CHECK THAT IS NOT A DESIGN QUESTION

`_whEaten`'s bites are the only `destination-out` in the warhammer row that
**extends past the head's own outline** — `bite(L*0.99, hh*0.52, hh*0.50)` runs
off the striking face and below the lower chamfer, and the haft slot is a bare
`fillRect`. Sanctified's rosette, by contrast, is five circles entirely inside
the head.

In a standalone harness that paints a background first, those bites **erase the
background**, not the weapon. Whether that happens in the shipped build depends
on whether weapons are drawn to an offscreen buffer or straight onto the arena
canvas, and that is not visible from the docs. **Check it, and check `_gsEaten`
and `_tbEaten` for the same exposure while you are in there.** If it is real it
is a live rendering bug in three shipped cells and it is worth its own finding.
The replacement below contains no `destination-out` at all.

---

# 2. WHAT REPLACES IT — `_whGnawed`

Five candidates were drawn and photographed (`umbral-hammer-candidates.png`):
H1 a horned maul with a clawed pommel, H2 a head gnawed down to fangs, H3 a
near-black block with lit spikes, H4 the head as a skull, H5 the head held in a
skeletal hand. **Rick took H3** and then made three rulings on it.

```
THE SHAPE     a near-black head, LONGER than `_whBase`'s (0.585L, not 0.64L),
              carrying three bone spikes above and three below, a beak forward
              and a spur back. In all three references the head is the mass and
              everything else is trim, so the head got bigger, not smaller
THE MATERIAL  bone spikes, not violet          Rick's, from two colourways
THE LENGTH    the shorter of two               Rick's, from a ladder of four
                                               tips at hy + hh*(0.28+0.50*0.64)
THE PALETTE   the dark head stays on THIS      Rick's. The other five umbral
              hammer only, for now             cells keep their pale `steel`
```

## 2.1 THE RULE THAT MADE IT WORK, AND IT IS REUSABLE

The first cut drew each spike as its own filled, stroked shape and then drew the
head on top. Every spike therefore carried its own outline and the head carried
another one behind it — up close, triangles layered behind a block. Rick saw it
immediately.

> **A grammar that adds a limb to a type must add it to the type's OUTLINE, not
> behind it.** Head, spikes, beak and spur are now ONE closed path: one fill,
> one stroke, no internal edges anywhere on the weapon. A spike that shares the
> head's outline cannot come apart from it at any zoom.

The light follows the same logic: each spike's gradient starts **transparent
just inside the iron** (`rootY = ±hy*0.86`) rather than at the head's edge, so
the bone reads as *seated in* the head instead of *glued to* it.

**This generalises.** Bloodsworn's six hooks and dwarven's four bolt bosses are
built the old way on this row, and both are candidates for the same failure at
close range. Nothing needs doing about it today; it is worth knowing before the
next grammar is drawn, and before the 8th type arrives needing seven of them.

## 2.2 WHAT HAPPENS TO THE SCHOOL'S THESIS

Umbral's grammar is *"eaten — the weapon is incomplete and the absence is the
point."* `_whGnawed` is not subtractive, so either the thesis moved or this cell
is an exception. **The honest reading is that it moved, one word:** what is
missing is the smooth block, and what the eating exposed is the bone underneath.
That is still absence, and it points outward instead of inward.

Rick has NOT signed off on extending that to the other five umbral cells — he
explicitly kept the change to this hammer for now (§6.2). Until he does, umbral
means *eaten* on five types and *gnawed to the bone* on one, and that
inconsistency is a known, chosen state rather than a drift.

---

# 3. THE CODE

`06-docs/v58/sc_wh_gnawed.js` is the whole function, drop-in, signature
`(c, L, W, p)` exactly as `_whEaten`'s. Three things about it:

- **It leaks no canvas state.** `shadowBlur`, `globalAlpha` and
  `globalCompositeOperation` are all unchanged on return — asserted, not
  assumed. `depth_build.py`'s CHECK_JS is the harness that cares.
- **It depends on `SHAPES._shade` and nothing else.** No `_facet`, no `_ink`,
  no `_whBase`.
- **Nothing is drawn past `x = L`.** The beak tip lands exactly on `L`. The
  silhouette doc's *"do not let a grammar contradict the hitbox"* holds: the
  weapon does not lie about `reach`. Vertical excursion to `1.20 * hh` is well
  inside bloodsworn's shipped `1.62 * hh`.

```js
if (key === "umbral")     return SHAPES._whGnawed(c, L, W, p);   // was _whEaten
```

`_whEaten` is then dead code on this row and should be **deleted in the same
commit**, not left behind a flag — git has it, and a second umbral hammer in the
file is how a dispatcher gets repointed by accident later.

---

# 4. WHAT CLAUDE CODE DOES

```
 #   IN                  OUT                 WHAT CHANGES
 1   sc-grasp.html       sc-gnawed.html      _whEaten -> _whGnawed, dispatch
                                             line repointed, old fn deleted
 F   --                  --                  FILM IT. Before anything else
```

**GREEN BEFORE IT IS CALLED DONE**

```
engine_ab          IDENTICAL on all 28, every match. SHAPES is render-only and
                   this is the cheapest possible proof of it. If a single bit
                   moves, THAT is the finding and it stops the stage
shape check        depth_build.py CHECK_JS over all seven schools x six shapes:
                   no leaked shadowBlur / globalAlpha / composite, no throw
silhouette_probe   --sheet, warhammer row, all seven. THE SHEET, not the table.
                   Report the real IoU row; §5 says why the numbers here are not
                   it, and expect the WORST case to be against runic
frame_probe        the new head is bigger; confirm nothing clips at 1080x1920
                   or at the phone resolution
chain_audit        --builder <the builder you write>. It DEFAULTS to
                   twinshade_build.py and will happily audit the wrong inserts
```

**FILM IT BEFORE YOU TUNE.** v43 §13, and v54 §2c is the reason it is not
optional. Everything above is a still at a fixed facing. Rick's own standing
note on this row — *"nothing has been judged in motion"* — is still open, and a
hammer spends most of a fight rotating.

---

# 5. THE NUMBERS, AND WHY THEY ARE SOFT

Every figure below comes from a **standalone rebuild** of `_whBase` and the
seven grammars from `sc_wh_patch.py` plus the `--steel` and depth edits — not
from the shipped build, which this session cannot reach. `_whConjured` is worse
than that: `_conjure` is not in the project docs at all, so runic's mask is
reconstructed from its spec, and runic is the worst-case column in every row.
**Re-run `silhouette_probe.py` against the real build before quoting any of
this.**

```
IoU vs the six siblings          runic*  verdnt  bldswn  sanct   dwarvn  vigil    worst   mean
umbral, SHIPPED  `_whEaten`       0.382   0.542   0.583   0.389   0.535   0.600    0.382  0.505
umbral, NEW      `_whGnawed`      0.335   0.558   0.690   0.441   0.741   0.646    0.335  0.569
```

**Read that honestly: the metric says this is a lateral move.** The worst case
improves by 0.047 and the mean gets worse by 0.064. The change is justified by
the sheet and by Rick, not by the number — which is exactly what §1.1 says the
number is good for.

**And there is one figure in that row worth watching: 0.741 against dwarven.**
That is Grudgebearer — the other hammer in the game, and the relic Shroudmaul's
blade was priced off. Three quarters of their footprints coincide. Colour
separates them (violet against gold-orange) and `night-plan.md` §1.2 found that
the glow is what actually survives motion and phone size, so this is probably
fine. **It is fine as an assumption, not as a measurement.** If those two ever
share a card or a thumbnail, check it there.

---

# 6. WHAT NOT TO DO

- **Do not draw a spike, a hook or a boss as its own stroked shape behind a
  head.** §2.1. It is the whole reason the first cut came back.
- **Do not reintroduce `destination-out` on this cell.** §1.2.
- **Do not push the beak past `x = L`** to make the weapon look longer.
- **Do not spread the dark head to the other five umbral cells** without asking
  — Rick scoped it deliberately. §6.2 of his rulings, and open decision 2.
- **Do not touch anything in v56.** The relic and GRASP are unaffected; this
  commit should not appear in a win-rate diff at all.
- **Do not trust §5's table.** §5.

---

# Open decisions — Rick's, and stage 1 can start without any of them

1. **THE SPIKE COUNT.** Three a side, from the references. Four reads busier and
   would shorten each one; two stops reading as a spiked maul at phone size.
   Not measured, not cheap to measure, and a picture decision either way.

2. **THE OTHER FIVE UMBRAL CELLS.** Rick kept the near-black head to this hammer
   *for now*, so umbral is currently two materials across six types. The
   greatsword, twinblade, scythe, bow and flail head can be drawn both ways on
   one sheet whenever he wants to settle it — `night-plan.md` §1.4 already
   wanted umbral *"genuinely dark"* in August and it never got done.

3. **BLOODSWORN AND DWARVEN, SAME CLOSE-RANGE PROBLEM.** §2.1. Their added parts
   are separate stroked shapes on top of `_whBase`, which is the construction
   Rick rejected here. Nobody has complained about them. Worth a look the next
   time anything brings you back to that file, not a job of its own.

4. **THE `destination-out` EXPOSURE.** §1.2 — a question for Code, not for Rick,
   but if it turns out to be real then `_gsEaten` and `_tbEaten` are shipped
   bugs and that outranks this whole document.

5. **NOTHING HERE HAS BEEN SEEN IN MOTION.** Standing open item on this row
   since v13, and this cell now has six spikes rotating through every frame of
   a swing. Film before tuning.

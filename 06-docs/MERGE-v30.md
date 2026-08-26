# MERGE v30 — three siblings into one chain

**2026-08-18.** Rick: *"2 patches. apply them and then zip up for handoff."*

Three proposals existed, **all three authored against `sc-cardspin.html`
`ec9b8d753235385d`**, none of them built on any other. They were siblings, not
a chain, and applying them meant composing them rather than stacking files.

```
sc-cardspin.html                                      ec9b8d753235385d
  shatter_build.py    Axiom v3 — 2-D fracture         98965a7f49ac32d7
  lastlight_build.py  Lastlight + the Harrowing       445a5241d9dbf0c4
  health_build.py     gauge / lifeline / stages / ult b57041681d7ee45b   <-- TIP
```

---

# 1. Reproduce before compose

Both incoming builders were re-run against **plain cardspin** first and had to
land on their patches' own stated hashes before anything was merged:

```
shatter_build.py --src sc-cardspin.html   ->  98965a7f49ac32d7   README says 98965a7f49ac32d7
health_build.py  --src sc-cardspin.html   ->  d0bb4890b19edc47   APPLY-ME says d0bb4890b19edc47
```

Every control HTML in the shatter patch also hash-matched its README
(`sc-glass` `b3342dafc360d57c`, `sc-sh-none` `868364c2246abfdf`, `sc-glass-nb`
`60eed45d59cd22f4`, `sc-glass-np` `7371c5a5b3e31bd0`, `sc-glass30`
`79b1e4418a98392f`). So the packages are intact and the builders are the ones
that made them. Only then was the order chosen.

# 2. The order, and why it is forced

Anchors do not collide. Shatter edits two spots inside `_gsConjured`.
Lastlight edits the roster, `moveMul`, `move`'s fall term, `tickCharge`,
`fireUlt`, `tickShots`, and inserts into `drawShots` / before `drawSparks` /
into the two ult set-piece heads. Health replaces the span
`drawHud .. drawClock` and the health ring, and rewrites 48 font stacks.
`drawHud` is at source line 9301 and `drawSparks` at 9467, so health's span
replacement and lastlight's inserts are in disjoint regions.

**What forces the order is `health_build.py`'s own rule 9: it exits if any
relic has no ult sigil.** Run health first and Lastlight ships with a blank
ult block; run it last and it refuses to build until the eighteenth relic has
a glyph. The second failure is the good one — it is the builder declining to
produce a file that is missing one of its own declared features, which is
exactly what that post-check is for.

So health runs last, and this merge had to write a sigil.

## `ULTSIG.lastlight` — the Harrowing, as a glyph

The sigil table is keyed on **weapon id, not `ult.kind`** — the patch's own
note records that one generic thing for N relics is a mistake this project has
already made three times. So the Harrowing needed its own.

It is the cast frozen one instant before it happens: twelve little scythes on
a ring, hafts pointing back at the centre they came from, sliding OUT and
brightening as the charge fills, and the core emptying as they go. Charge is
pure wall time, so `cf` is a clock and the glyph assembles toward the moment it
fires — the anticipation beat the rest of the table is built around.

**The count is the count.** `ult.scythes` is 12 and so is the glyph. A viewer
who counts the sigil and then counts the spray gets the same number — the same
discipline as Slagburst's cracks equalling its shards.

# 3. What the composed build was made to prove

```
engine_ab --n 18    2448/2448 IDENTICAL vs sc-cardspin on the 17 pre-existing
                    ids.  This is the load-bearing one: all three proposals
                    claim to be presentation-only for the existing roster, and
                    this is the claim measured COMPOSED rather than one at a
                    time.  Lastlight's two physics edits are exact identities
                    at zero burden, which is what makes it possible.
verify.py --n 60    13/13.  Lastlight 49.3%, Grudgebearer 59.5, spread 12.7pp,
                    0/9180 timeouts, no pairing under six hits.
harrow_probe        22/22 on the composed tip
introfit_probe      18/18 fit the card, 36/36 overflow bands clean
tip_audit           0 gaps
silhouette_probe    greatsword min IoU 0.330 — the shatter patch's own number,
                    so the fracture survived composition unchanged
twin_identity       _twinConjured 0px · _whConjured 0px · _gsConjured 122473px
health_build        18/18 relics have their own sigil
```

`twin_identity` reports **NOT IDENTICAL** overall and is right to: the runic
greatsword moved and nothing else did, which is the entire point of the
shatter patch. Read the rows, not the verdict — the README says so too.

# 4. THE ONE CLAIM THAT DID NOT SURVIVE: glass_probe

`README-SHATTER-PATCH.md` documents:

```
glass_probe.py --a sc-cardspin.html --b sc-sh-none.html --n 10     5/5
```

Run exactly as written it gives **2 FAILED**. Neither artifact is wrong; the
check line is, and it fails for a reason worth keeping:

* **The tool says so itself.** It requires `bind:0.000` *and* `pool:0.000` in
  the candidate and prints *"does not look like a --bind 0 --pool 0 build.
  Numbers below may be meaningless."* `sc-sh-none.html` has `bind:0.000` and no
  `pool` token at all — `shatter_build.py` has no `pool` parameter. `pool` is a
  `glass_build.py` (v2) concept.
* **`--dump` shows the gaps as NEGATIVE** — -5.4, -20.4, -18.0, -13.5. Those
  are not gaps, they are overlaps. glass_probe measures **1-D daylight along
  the blade axis**; v3 is a **2-D fracture**, so its pieces overlap when
  projected onto one axis. [1] counting 10 runs at some `_t` and 11 at others
  is the same fact.

Pointed at the build it was written for, with that build's own shard count:

```
glass_probe.py --a sc-cardspin.html --b sc-glass-nb.html --n 6     ALL PASS
```

(`--n` describes the CANDIDATE. The v2 control has 6 shards.)

**A 2-D fracture has no instrument of its own.** That is the real gap this
found, and it is left open rather than papered over by loosening `--min-gap`
until the number went green.

# 5. v3 was composed, v2 was kept

The shatter patch offers two alternatives for Axiom and says *"pick one"*. v3
was composed because the zip, the README title and the whole check list lead
with it. **This was a choice made without asking and it is one rebuild to
reverse** — v2's four HTMLs are all still present with their hashes intact:

```
python3 glass_build.py     --src ../02-chain/sc-cardspin.html --out ../02-chain/sc-glass.html --open -0.15
python3 lastlight_build.py --src ../02-chain/sc-glass.html    --out sc-glass-lastlight.html
python3 health_build.py    --src ../02-chain/sc-glass-lastlight.html --out ../02-chain/sc-health18.html
```

# 6. Housekeeping

* `tools/scpage.py` is the **health patch's** version and must stay: the
  artifact embeds Atkinson as base64 WOFF2, and Canvas silently draws the
  fallback face *with the fallback's metrics* for anything measured before
  those faces parse. `game()` now waits on `window.__fontsReady`. Every capture
  in the repo goes through that one function. The change is
  backward-compatible (`!== false`), so it is safe on older builds.
* `02-chain/sc-lastlight.html` (lastlight on plain cardspin) was **deleted**.
  It is superseded by `sc-shatter-lastlight.html` and regenerates in one
  command; a generated file is not a place to store anything.
* Reference images from this session are in `05-reference/v30/`.

# 7. Open decisions

1. **v3 shatter or v2 glass for Axiom?** Composed v3; reversing is §5.
2. **Promote `sc-health18.html` `b57041681d7ee45b` to chain tip of record?**
   `sc-cardspin.html` is still nominally it, and has been through three
   sessions of open decisions asking the same question.
3. **Ship to 01-live?** The tip dominates live by seven builds.
4. **`BAND.pos`** defaults to top. Bottom composes better standing alone but
   lands the B fighter's block under Shorts chrome. Unchanged from the health
   patch's own note — nobody has watched either on a handset.
5. **Perf has never been measured on real hardware** — the HUD's +2.2% and the
   shatter art's ~2.5x are both ratios from a GPU-less box, and the standing
   budget is ~6 ms at 165 Hz. This merge adds both at once.
6. **Sanctified is now four relics and the HUD made it worse** — health's own
   open decision 1 flags Dawnbringer/Censer as one cream object across names,
   chunks and charge bars. Lastlight is a fifth cream row.
7. **A 2-D fracture still has no probe.** §4.

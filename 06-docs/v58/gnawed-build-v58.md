# v58 — THE UMBRAL WARHAMMER IS REDRAWN, AND THE `destination-out` QUESTION IS SETTLED: the erase is real in three shipped cells and reaches nothing, because a buffer happens to be in the way.

**2026-08-31, Claude Code.** Built to `06-docs/v58/umbral-hammer-v58.md`.

```
IN    02-chain/sc-grasp.html      28 relics
OUT   02-chain/sc-gnawed.html     BUILD OF RECORD. One function replaced, one
                                  dispatch line, two comments, and the old
                                  function deleted
```

`tools/gnawed_build.py`. The shape itself is read from
`06-docs/v58/sc_wh_gnawed.js` and not pasted into the builder — one copy, the
way `fx_build.py` inlines `src/render/fx.js`.

---

# 1. THE GATE, AND IT IS THE WHOLE ARGUMENT THAT THIS IS ART

```
engine_ab   3024/3024 IDENTICAL field for field, ALL 28 RELICS
```

`SHAPES` is render-only — nothing in `Fighter`, `Match` or `Sfx` reads it — so
a silhouette change must not move a single bit. It did not. This is the same
proof stage 1 of v56 made for a name, one layer down, and it is the cheapest
one this project has.

**And `app/main.js`'s `GAME` line moved with it.** CLAUDE.md §0 names that as
the carry step nothing checks, and v48 shipped with it stale.

---

# 2. WHAT CHANGED

Rick: *"umbral hammers silhouette looks pretty bad. can we take another stab at
its design? the hammer with blocks attached to it idea just isnt working for
me."*

`_whEaten` was purely SUBTRACTIVE — call `_whBase`, punch two blobs and a haft
slot out of it with `destination-out`. **Subtracting from a shape that is
already rectilinear does not produce an absence, it produces smaller
rectangles.** Every other grammar on this row ADDS a contour; umbral was the
only one that removed one, and removal is the weakest silhouette operation
there is.

`_whGnawed` is a near-black head — LONGER than `_whBase`'s, because in all
three of Rick's references the head is the mass and everything else is trim —
carrying three bone spikes above and three below, a beak forward and a spur
back, with the school's light banked inside it.

## 2.1 The rule the builder asserts

> **A grammar that adds a limb to a type must add it to the type's OUTLINE,
> not behind it.**

Head, spikes, beak and spur are ONE closed path: one fill, one clip, one
stroke, no internal edges. Rick rejected the first cut because each spike
carried its own outline — *"upclose the spikes just look like triangles layered
behind the hammer."* `gnawed_build.check_shape()` refuses to write unless
`path(c)` is called exactly three times and `c.stroke()` exactly once, and it
refuses on any `destination-out`, any `_whBase` call, and a beak that does not
land on `L`.

---

# 3. THE SILHOUETTE NUMBERS, MEASURED ON THE REAL BUILD

`silhouette_probe.py --types warhammer --footprint`, which is the flag this
build needs: `_whGnawed`'s head is `_shade(p.dark, 0.92, 0.04)` — a near-black
literal — and without `--footprint` the mask would miss the head entirely.

```
                    min IoU   mean IoU
the v58 doc's        0.335      0.569     from a standalone rebuild, and it
standalone rebuild                        warned "do not quote any of this"
MEASURED HERE        0.325      0.563     on the shipped build
```

**The doc's soft table was accurate to 0.01 and 0.006.** It said not to trust
it; it was right anyway, and that is worth recording because the next
standalone reconstruction will be judged against this.

**AND IT IS STILL A LATERAL MOVE ON THE METRIC**, exactly as the doc said: the
old cell scored 0.382 worst / 0.505 mean, so the worst case improves and the
mean gets worse. **The change is justified by the sheet and by Rick, not by the
number.** `05-reference/v58/warhammer-row.png`.

---

# 4. AND THE `destination-out` QUESTION IS SETTLED — IT IS LATENT, NOT LIVE

v58 §1.2 raised this as *"a question for Code, not for Rick"* and said that if
it were real, `_gsEaten` and `_tbEaten` are shipped bugs that **outrank the
whole document**. Measured on the build, painting each shape onto an OPAQUE
background and counting pixels punched through it:

```
warhammer x umbral   `_whEaten`     1378        ->  `_whGnawed`  0
greatsword x umbral  `_gsEaten`     4132            unchanged
twinblade x umbral   `_tbEaten`     4877            unchanged
warhammer x sanctified              560             unchanged
warhammer x vigil                     0             control
```

**The erase is real.** It is also unreachable:

> `litWeapon()` bakes every weapon onto its own **transparent scratch canvas**
> before blitting it, and on a transparent buffer `destination-out` can reach
> nothing but the weapon. That is the correct behaviour and it is what ships.

The one path that skips the buffer is `drawWeapon`'s fallback,
`if (!litWeapon(...)) fn(c, ...)`, which draws straight onto the arena.
Measured across every shape × school × drawK: **`litWeapon` declines 21 of 126,
and every single one of them is the FLAIL** — the one shape with a detached
head. **No flail school is eaten.** So the fallback never carries a
`destination-out` shape.

**That is an accident of which shapes need a buffer, not a design**, and it is
worth knowing before somebody adds an eaten flail or changes what `litWeapon`
declines. Sanctified's rosette punches 560 as well, which v58 §1.2 predicted
would be safe because its circles sit inside the head — they do not, quite.

**Nothing needs fixing today.** `_whGnawed` removes the technique from this
cell; the other three cells are unchanged, unreachable and uncomplained-about.

---

# 5. THE OTHER CHECKS

```
canvas state    shadowBlur, globalAlpha and globalCompositeOperation all
                restored across all seven warhammer grammars, no throw.
                depth_build.py's CHECK_JS contract, asserted directly
the row sheet   05-reference/v58/umbral-hammer-row.png — the new hammer beside
                Grudgebearer, Censer and Bulwarden, which is the comparison
                that matters because three quarters of its footprint coincides
                with the dwarven one (v58 §5)
chain_audit     nothing downstream of this build exists to clobber an insert
frame_probe     STILL CRASHES on every build, old tips included. CLAUDE.md §5
                and open item 14; it did not run here either
```

## 5.1 And two comments moved with the function

`_whEaten` is deleted, not left behind a flag — a second umbral hammer in the
file is how a dispatcher gets repointed by accident later. Two sentences named
it and both moved in the same commit:

- **Shroudmaul's own relic comment** said *"`SHAPES.warhammer` already routes
  `umbral` to `_whEaten`, so the silhouette is not new work: it exists, it is
  78.6% distinct."* **That is the paragraph that sent v56 the wrong way**, so it
  is corrected rather than repointed, and it carries why.
- **`_scEaten`'s shared-path note** pointed at `_whEaten` for the technique. It
  points at `_gsEaten` and `_tbEaten` now, and carries §4's measurement.

> **AND THE BUILDER REFUSED TO WRITE ON ITS OWN EXPLANATION TWICE.**
> `sc_wh_gnawed.js`'s header says *"there is no `destination-out` in this
> function at all"*, and the corrected relic comment quoted the old name. Both
> are fixed the way `revenant_rename.py` fixed it — strip block comments as a
> BLOCK, and excise the one authored paragraph by identity. **CLAUDE.md has now
> recorded this failure five times in two sessions.** It is not a recurring
> mistake so much as a permanent property of a codebase that explains itself in
> the file, and every new grep-the-source check will hit it.

---

# Open decisions

1. **NOTHING HAS BEEN SEEN IN MOTION.** v58 §5, a standing open item on this
   row since v13, and this cell now has six spikes rotating through every frame
   of a swing. `07-shorts/v56/grasp-gnawed.mp4` is the first one.

2. **THE SPIKE COUNT.** Three a side, from Rick's references. Untouched.

3. **THE OTHER FIVE UMBRAL CELLS.** Rick kept the near-black head to this
   hammer *for now*, so umbral is currently two materials across six types.
   Deliberate and scoped, not drift.

4. **BLOODSWORN AND DWARVEN HAVE THE CLOSE-RANGE CONSTRUCTION RICK REJECTED.**
   v58 §2.1: their added parts are separate stroked shapes on top of
   `_whBase`. Nobody has complained. Worth a look next time anything brings
   somebody back to that file.

5. **THE TWO SILHOUETTE INSTRUMENTS STILL DISAGREE AND THIS BUILD DID NOT
   RECONCILE THEM.** v58 §1.1: `cell_survey`'s *78.6% distinct* on an INK mask
   against fifteen open cells, against `silhouette_probe`'s IoU on a
   SILHOUETTE mask against six siblings. 78.6% distinct would be an IoU of
   0.214; the measurement is 0.325. **Do not quote one as if it were the
   other.** It is probably two masks and two comparison sets; it may also mean
   one instrument is being read wrong somewhere, which would matter well beyond
   this cell. Running both against this build is the way to settle it and
   nobody has.

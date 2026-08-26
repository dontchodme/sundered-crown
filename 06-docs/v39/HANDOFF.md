# v39 — HANDOFF. Where this is and what to pick up.

**2026-08-20.** One relic added; the twenty-first was surveyed, chosen,
designed, built and tuned in one sitting. **No posting cut was made.**

```
02-chain/sc-foregone.html   b1a58c5a3982a8cf   <-- THE BUILD OF RECORD CANDIDATE
built off 02-chain/sc-redflail.html            07d4c845732cfe72
01-live UNTOUCHED, still on sixteen

cell_survey          7/7
runic_scythe_probe   8/8
foregone_probe      16/16
engine_ab           1710/1710 IDENTICAL on the other twenty
verify.py --n 40    13/13 . 0/7600 timeouts . spread 14.1pp . mean 37.8s
director_diag       Converse 15.61x -> 1.83x ex-kill
foregone_sweep's runtime override vs a real rebuild: 400/400 identical
```

## Read in this order

| doc | the headline |
|---|---|
| `look.md` | All 22 open cells measured BEFORE the choice. Art is settled everywhere — 22/22 — so it cannot discriminate a cell; v38's "that is unusual" was too generous. And **hex is a RATE, not a quantity**, which is what made this cell buildable. |
| `design.md` | §1 in Rick's words, and nothing started before it existed. |
| **`README.md`** | **The build. §2 and §5 are the ones to read: the reversal ran 65% too fast because two integrations added, and the director's 15.61x came from an ultimate that puts nothing extra on the floor.** |

## Four things that outlive the relic

1. **An alpha mask cannot see interior ornament.** The dwarven bow's rivets are
   drawn on top of the riser: 0.12% of coverage, unmistakable to the eye. The
   instrument reported "no art" and was flatly wrong — the same class of error
   v38 caught the weapon matrix making one layer out. **Hold the palette and
   vary only `p.key`**, then a differing pixel is the dispatch.
2. **`hitStop` freezes the hex clock.** `step()` returns before `tickStatus`,
   so 9.4% of a scythe fight buys no hex. Almost certainly true of every clock
   in `tickStatus` and nothing else has been checked.
3. **`tickFire` gates on `f.w.shot`, not on mode.** `relicShot()` gates on mode
   and `tickFire` does not call it. A `shot` left on a melee weapon fires a bow
   at cadence forever — it inflated five rows of a probe by 1.9x before it was
   caught by disagreeing with two other measurements.
4. **`director_diag`'s window predicate has been generalised three times** and
   there is still no shared field an ultimate's duration hangs on. A fourth
   crowding ultimate will silently measure a zero-length window.

## What is NOT in this repo

`.gitignore` at the root explains each. In short: the mp4s and wavs (the seed
IS the fight — commands in `sc/WHATS-NOT-IN-THIS-ZIP.md`),
`05-reference/**/*.png` (every one is a probe's output), the 338 MB kokoro
models (`FETCH-KOKORO.md`, two curls), and frame caches.

## The first four things to pick up

1. **THERE IS NO POSTING CUT.** No seed picked, no VO, no clip. Every prior
   relic shipped with one and this one did not, so the pipeline is untested
   against it — and `cinema_vo.SPOKEN` has no entry for either "Foregone" or
   "Converse". Both are compounds Kokoro will run into one cluster.
2. **`01-live` is FIVE relics behind** — Lastlight, Slagheart, Triplicate,
   Threshmaw and now Foregone all exist and nobody outside this tree can play
   them. v27 open decision 1, and by a distance the oldest open thing in the
   project.
3. **The reversal's contact damage has never been isolated.** README open
   decision 3. The caster crossing the hall at four times cruise lands ordinary
   blows at four times the closing speed, which is where the director's 15.61x
   came from — and no `decomp` run exists for this relic. v38 found a third of
   Bloodmill was a mechanic nobody designed; **this one has not been looked
   for.**
4. **The pulse economy is unswept and it is quadratic in `lay`.** README open
   decision 1. Only 11% of rings reach the foe, and `orbDmg`, `orbR`, `pulse`
   and `lay` were all held constant through the entire blade sweep.

## Still open from v38, unmoved

The card-removal analytics pull (v38 §10, the registered prediction:
r(6) ~0.28 → ~0.45+ with the post-0:05 tail unchanged at 0.43); Bloodmill's
missing set-piece art; and `stormMul` at 6.9, worth 7.6pp of a mechanic nobody
designed.

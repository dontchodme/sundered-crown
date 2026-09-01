# v60 — THE CELL COLUMN IS ONLY GOOD TO A TIER, AND THIS SESSION MEASURED THE ERROR BAR INSTEAD OF ASSUMING IT. Every open cell reproduced v57 within 1.3pp on a newer build — and then one of them moved 10.3 points on a different block of seeds. Two of this session's own readings were refuted by their own checks, including one that had already been written into a draft.

**2026-09-01, Cowork.** `row_price.py` at `--pin 0` on all five rows with open
cells, `cell_survey.py --skip-clock`, and three new runtime-only tools —
`cell_ults_on.py`, `cell_se.py`, `curse_pool_probe.py` — against
`02-chain/sc-shroudmaul.html`, the pushed tip, **28 relics**, neither
Cindercleave nor Bloodmirror in it. ~25,000 fights. Nothing written to any build.

**HARNESS CONTROL, run first.** Chromium **141.0.7390.37**, byte-identical to
v57 and v59. The warhammer row at `--pin 14` against `sc-nightfell.html` returns
bloodsworn **+15.0**, umbral **+7.3**, runic **+1.9**, verdant **−0.8** —
`cell-repricing-v57.md`'s header table to the decimal, all four cells.

---

# 1. THE WHOLE OPEN GRID, REPRICED ON THE CURRENT TIP

Fourteen open cells at shipped weights, 270 fights an arm, against all 27 other
relics. `bloodsworn x scythe` and `dwarven x scythe` are Bloodmirror's and
Cindercleave's and are listed only because this build predates them.

```
cell                      v60      v57    move      art (diff from nearest sibling)
vigil x twinblade       +49.3    +50.0    -0.7      73.2%
vigil x flail           +31.1    +30.8    +0.3      71.3%
sanctified x twinblade  +28.1    +27.3    +0.8      32.6%   closest pair on the board
dwarven x twinblade     +25.9    +25.8    +0.1      32.7%
bloodsworn x warhammer  +16.3    +15.4    +0.9      50.8%
umbral x bow            +15.6    +14.6    +1.0      54.5%
bloodsworn x scythe     +14.1    +14.2    -0.1      59.0%   <- Bloodmirror
runic x bow             +13.0    +11.9    +1.1      41.4%
dwarven x scythe        +10.0    +11.2    -1.2      71.5%   <- Cindercleave
sanctified x flail       +9.6    +10.4    -0.8      64.9%
umbral x scythe          +8.1     +7.3    +0.8      65.6%   retires the scythe row
verdant x flail          +8.1     +7.7    +0.4      49.1%
runic x warhammer        +6.7     +6.2    +0.5      98.0%
verdant x warhammer      +4.4     +4.2    +0.2      99.3%
```

**Every cell within 1.3pp on a build with one more relic in it.** That looks
like a precise instrument. §2 is why it is not.

---

# 2. THE ERROR BAR, MEASURED TWICE, AND THE SECOND WAY IS THE ONE THAT MATTERS

`cell_ults_on.py` was re-run on two cells with a different seed block
(`91001 + 11i` against the standard `2207 + 11i`):

```
cell                      block A    block B    move
umbral x bow               +15.6      +25.9    +10.3
bloodsworn x warhammer     +16.3      +10.7     -5.6
```

**A cell moved ten points between two draws of the same measurement.** So
`cell_se.py` was written to ask what the error bar actually is. The suspicion
going in was that the docs' quoted ~4pp is too small because a cell is 27 foes x
10 SEEDS and a seed sets the whole match, so the 27 fights sharing a seed are
correlated and the independent unit is the seed.

**That suspicion is refuted.** At 20 seeds x 27 foes = 540 fights an arm:

```
                                       umbral x bow   bloodsworn x warhammer
naive binomial SE (what the docs quote)      3.0pp                    3.0pp
clustered on SEED   (20 clusters)            2.5pp                    2.8pp
clustered on FOE    (27 clusters)            2.8pp                    2.9pp
```

Clustering does not inflate the error at all. **The SE is ~3pp at 540 fights and
~4.3pp at the 270 the survey column uses**, exactly as advertised — and a
difference of two lifts carries ~6pp, so the 10.3-point move is a 1.7σ draw, not
a broken tool. The 540-fight run puts umbral x bow at **+16.3**, in line with
block A.

> **The consequence is what matters. A cell price at 270 fights has a 95%
> interval about ±8pp wide, and a DIFFERENCE between two cells needs ~12pp to be
> real.** The fourteen open cells are four tiers and inside a tier the decimal
> means nothing:
>
> ```
> +49   vigil x twinblade
> +31   vigil x flail · sanctified x twinblade · dwarven x twinblade
> +16   bloodsworn x warhammer · umbral x bow · runic x bow
> +10   sanctified x flail · umbral x scythe · verdant x flail · runic x warhammer · verdant x warhammer
> ```
>
> This does not contradict v57 §2 — it sharpens it. v57 said cross-row
> comparison is indicative; this says **within-row is also only good to a tier.**

---

# 3. PRICING CELLS WITH THE FIELD'S ULTIMATES ON — budget-v59 OPEN DECISION 2, ANSWERED

`row_price` passes `noult` true for every pinned id, which is every weapon, so
every cell in this project's history was priced in a world with no ultimates.
`cell_ults_on.py` prices both worlds. Six cells, 4 arms each, 270 fights an arm:

```
cell                     FIELD ULTS OFF        FIELD ULTS ON        logit gap
                        floor    lift        floor    lift
umbral x scythe         52.6%   +8.1pp       39.3%   +4.8pp           -0.13
umbral x bow            40.0%  +15.6pp       17.8%  +23.3pp           +0.54
runic x warhammer       37.4%   +6.7pp       17.0%   +5.2pp           +0.05
sanctified x twinblade  31.1%  +28.1pp       10.7%  +24.1pp           +0.33
vigil x twinblade       31.1%  +49.3pp       10.7%  +45.6pp           +0.17
bloodsworn x warhammer  37.4%  +16.3pp       17.0%  +18.9pp           +0.34
```

**The answer is: the arm moves the floors and not the order.** Every donor body
loses 13 to 22 points when the field gets its ultimates back — a body with no
ultimate against a field that all have theirs is simply losing — and on the
log-odds scale, which removes the floor, every channel is worth slightly *more*
in the real world.

**The one apparent ranking change did not replicate.** umbral x bow's +7.8pp gap
came back at −15.2pp on the second seed block (§2). It is not a finding.

> So `row_price`'s world is a defensible choice and the honest fix is small:
> **print `noult` in the tool's own header.** Running both arms costs 2x for a
> re-ordering that does not happen.

---

# 4. THE CURSE POOL — A DESIGN READ, PROPOSED AND THEN REFUTED BY ITS OWN PROBE

The read, written before the measurement: *the reworked curse is a memory of
three blows, so on a spin weapon whose blows are all the same size it fills in
three hits and freezes — a constant with extra steps. That makes* `umbral x
scythe` *the weakest expression of the school.*

`curse_pool_probe.py` grafts curse onto every type's donor and traces the foe's
pool every 0.25s. **The read is wrong:**

```
type         final pool   blade dmg   t to 90% of final   share of fight AT final
greatsword         80.0        10.4         46.9s                    6%
twinblade          89.0        11.9         47.4s                    6%
bow                98.9        16.2         35.0s                   12%
flail             134.9        24.0         38.9s                   13%
warhammer         135.2        23.5         38.6s                   10%
scythe            161.7        31.4         34.4s                   12%
```

**Nothing fills fast.** Every type takes 34 to 47 seconds to reach 90% of its
final pool, because per-blow damage varies far more (crits at 2.1x, 30% jitter,
`dmgTakenMul`) than the flat-blade reasoning assumed. The scythe has the
*highest* pool and the *fastest* convergence, the opposite of the prediction.

**And the useful thing came out of the refutation.** Total echo delivered over a
fight is pool x 0.08 x blows landed:

```
greatsword 111    twinblade 117    warhammer  99
bow        114    scythe    101    flail       82
```

**82 to 117 across every weapon in the game — the flattest channel there is.**
That is `v49 §1` working exactly as written: *"a small cap is what narrows the
gap between the 5.6-blow flail and the 25.7-blow twinblade."* It also means
**an umbral cell cannot be argued for or against on which weapon it lands on.**

---

# 5. THE ART COLUMN AND THE EYE DISAGREE, AND v58 PREDICTED THAT THEY WOULD

`cell_survey [3]` measures the ink mask at 6x with **one palette held for every
school** — the right way to ask "is this outline its own shape", and, v58
established, no answer at all to "does this read as a different weapon on
screen." Four candidate cells were rendered in their own school's palette beside
the sibling the column calls nearest:

```
cell                     ink-mask diff   what it looks like in colour
bloodsworn x warhammer          50.8%    near-worst on the board and the best
                                         object in the set — a red-and-bone head,
                                         three claw slashes across the face
runic x warhammer               98.0%    second-most distinct by the column and
                                         genuinely distinct by eye: a fanned blue
                                         head with a lit rune ring at the pommel
umbral x bow                    54.5%    clearly its own object beside the
                                         dwarven bow
dwarven x twinblade             32.7%    the column is right — it is Twinshade's
                                         outline in a different colour
```

**The column inverts against the eye on the top of this list.** Use it to catch
the 32% cases and never to rank the 50-98% ones.

---

# 6. THE FOUR THAT WERE OFFERED, AND THE ONE TAKEN

`dwarven x twinblade` (+25.9), `bloodsworn x warhammer` (+16.3), `umbral x bow`
(+15.6) and `runic x warhammer` (+6.7). **Rick took bloodsworn x warhammer**,
and gave it as a §1 rather than as a pick. It is bloodsworn's last open cell.
Priced in `wirering-design-v60.md`.

`umbral x scythe` remains the only cell that retires a row, and the two vigil
cells remain open for the reason `budget-v59.md` §3 gave.

---

# Open decisions

1. **QUOTE CELL PRICES AS TIERS, NOT DECIMALS.** §2. A difference under ~12pp
   at 270 fights is not a difference. Every survey in this project prints three
   significant figures and none of them prints an interval.

2. **`row_price` SHOULD PRINT `noult` IN ITS HEADER.** §3. One line. Running
   both arms is not worth 2x for a re-ordering that does not happen.

3. **`row_price --pin` SHOULD DEFAULT TO 0.** Still open from v57, still one
   line.

4. **THE INK-MASK COLUMN NEEDS A COLOUR COMPANION.** §5. `cand_art.py` is
   fifty lines and it caught an inversion on the first four cells it was pointed
   at.

5. **THE SESSION'S OWN ERROR RATE IS THE ARGUMENT FOR THE CHECKS.** Two
   readings were published to Rick and then withdrawn — the ultimates-on gap
   (§3) and the curse-pool read (§4) — both killed by a check that cost a few
   minutes. Neither would have been caught by any test in `tools/`.

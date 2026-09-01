# v57 — THE CELL TABLE WAS NEVER A CELL TABLE. v55's open decision 2, closed, and the answer is not the one it expected: the pin never reordered a single row. What it was distorting is the cross-row list every survey in this project has quoted, and the cause is not weight — it is that the six rows are measured against six donors whose floors are 36 points apart.

**2026-09-01, Cowork.** `tools/row_price.py` at `--pin 0` and `--pin 14`, five
rows, and `tools/cell_survey.py --skip-clock`, all against
`02-chain/sc-nightfell.html` — the build of record, 27 relics, Shroudmaul not
yet in it. Runtime only. Nothing is written to any build.

**THE HARNESS IS NOT THE PINNED ONE AND THAT IS DECLARED UP FRONT.** This
session runs Chromium **141.0.7390.37**; the repo pins playwright 1.62.0 ->
Chromium 151.0.7922.34 and `cdn.playwright.dev` is blocked from here, so exact
V8 parity was not available. `docs/RUNTIME-DRIFT.md` says a one-ULP difference
in `Math.pow` alone leaves 68/192 fights identical, so the individual fights
below are NOT the same fights the repo would run.

The control that makes the tables usable anyway, and it was run first:

```
warhammer row, pin 14        v55 (Chromium 151)   here (Chromium 141)   delta
bloodsworn x warhammer              +17.3                +15.0          -2.3
umbral x warhammer                   +7.7                 +7.3          -0.4
runic x warhammer                    +1.4                 +1.9          +0.5
verdant x warhammer                  -1.0                 -0.8          +0.2
```

Same order, largest disagreement 2.3pp against a per-cell SE of ~4pp. **The
fights differ and the aggregate does not.** Every number below is a win rate
over 260 fights and none of them is a claim about a single fight.

---

# 1. WHAT THE PIN ACTUALLY DID

`row_price --pin` sets EVERY relic's `dmg` to one value so a harder-hitting arm
cannot win by ending the fight sooner. It has defaulted to 14 since it was
written and v55 §1 found the warhammer row reordering across a pin sweep, which
put every cell ranking in the project's history in doubt.

Re-run at shipped weights, within each row:

```
TWINBLADE   donor widowmaker      no-channel floor 30.8%
  vigil x twinblade       ward         +50.0%   (pin 14: +24.2%)   +25.8pp
  sanctified x twinblade  smite        +27.3%   (pin 14: +10.4%)   +16.9pp
  dwarven x twinblade     sunder       +25.8%   (pin 14: +13.5%)   +12.3pp

WARHAMMER   donor grudgebearer    no-channel floor 37.7%
  bloodsworn x warhammer  hemorrhage   +15.4%   (pin 14: +15.0%)    +0.4pp
  umbral x warhammer      curse         +9.2%   (pin 14:  +7.3%)    +1.9pp
  runic x warhammer       hex           +6.2%   (pin 14:  +1.9%)    +4.2pp
  verdant x warhammer     entangle      +4.2%   (pin 14:  -0.8%)    +5.0pp

SCYTHE      donor thornwake       no-channel floor 52.7%
  bloodsworn x scythe     hemorrhage   +14.2%   (pin 14: +16.9%)    -2.7pp
  dwarven x scythe        sunder       +11.2%   (pin 14: +13.8%)    -2.7pp
  umbral x scythe         curse         +7.3%   (pin 14:  +9.2%)    -1.9pp

FLAIL       donor gravemourn      no-channel floor 16.5%
  vigil x flail           ward         +30.8%   (pin 14: +19.2%)   +11.5pp
  sanctified x flail      smite        +10.4%   (pin 14:  +0.0%)   +10.4pp
  verdant x flail         entangle      +7.7%   (pin 14:  -2.3%)   +10.0pp

BOW         donor ironhail        no-channel floor 40.0%
  umbral x bow            curse        +14.6%   (pin 14: +13.1%)    +1.5pp
  runic x bow             hex          +11.9%   (pin 14: +18.8%)    -6.9pp
```

**Four of five rows keep their exact order.** Only the bow row swaps, and its
two cells are 2.7pp apart at shipped weight — inside noise — where they were
5.7pp apart at pin 14. So the honest statement is that the pin has never
reordered a row it could be trusted on, and the bow row is a coin flip either
way.

---

# 2. THE REAL DEFECT IS OLDER THAN THE PIN AND IT IS IN THE FLAT LIST

The list of open cells that v40, v43, v47, v48 and v55 all quote reads as a
ranking of the grid. It is not one. Every row is A/B'd against ITS OWN donor
with the channel deleted, and at shipped weights those donors are not
comparable:

```
donor        no-channel floor
gravemourn              16.5%
widowmaker              30.8%
grudgebearer            37.7%
ironhail                40.0%
thornwake               52.7%
```

Thirty-six points. A cell on the flail row is being asked to lift a body that
loses five fights in six; a cell on the scythe row is being asked to lift one
that already wins. **`vigil x flail +30.8%` and `bloodsworn x scythe +14.2%`
are not two numbers on one scale**, and the cross-row list has been read as if
they were for five surveys.

The obvious repair does not work either. Log-odds lift removes the floor
algebraically and is LESS stable across the pin, not more:

```
Spearman rho between the two pins    raw lift 0.779    log-odds 0.593
```

Because the pin does not rescale the world, it CHANGES it — different fights,
different lengths, different foes winning. There is no transform of these two
tables into each other.

**Within a row the column is clean and always was. Across rows it is
indicative and nothing better is currently available.** That is the finding,
and cross-row cells should be separated on grid coverage, art and design space
rather than on a decimal.

---

# 3. THE TWO CELLS THE PIN WAS HIDING, AND WHY THEY STILL LOSE

```
sanctified x twinblade   +10.4 -> +27.3   rank 9 -> 3
dwarven x twinblade      +13.5 -> +25.8   rank 7 -> 4
```

Both are real. Both also carry the worst art on the grid — `cell_survey [3]`,
ink mask at 6x, palette held:

```
cell                    nearest sibling   diff   inkIoU   closest pair on its type
sanctified x twinblade  umbral            32.6%   0.761   #1 of 21
dwarven x twinblade     umbral            32.7%   0.907   #2 of 21
runic x bow             dwarven           41.7%   0.723   #4 of 21
verdant x flail         umbral            49.1%   0.639   #1 of 21
bloodsworn x warhammer  dwarven           50.8%   0.762   #1 of 21
umbral x bow            dwarven           54.5%   0.537   #10 of 21
bloodsworn x scythe     sanctified        59.0%   0.648   #1 of 21
sanctified x flail      verdant           64.9%   0.481   #4 of 21
umbral x scythe         sanctified        65.6%   0.528   #2 of 21
vigil x flail           umbral            71.3%   0.692   #7 of 21
dwarven x scythe        sanctified        71.5%   0.578   #3 of 21
vigil x twinblade       umbral            73.2%   0.794   #7 of 21
umbral x warhammer      bloodsworn        78.6%   0.525   #4 of 21
runic x warhammer       vigil             98.3%   0.456   #11 of 21
verdant x warhammer     umbral            99.3%   0.492   #13 of 21
```

Note what this column does to the three row LEADERS: bloodsworn tops both the
warhammer and the scythe row and holds the most confusable art on each. A row
leader is not a cell recommendation on its own.

---

# 4. THE FOUR THAT WERE OFFERED, AND THE ONE TAKEN

```
vigil x twinblade    +50.0pp   art 73.2%   strongest open cell at BOTH pins
vigil x flail        +30.8pp   art 71.3%   the weakest body in the game, lifted
umbral x bow         +14.6pp   art 54.5%   retires a row; cheapest cell to MINT in
dwarven x scythe     +11.2pp   art 71.5%   <- RICK'S
```

Rick took **dwarven x scythe**, over the two vigil cells and the umbral bow.
The grid after Shroudmaul is nearly symmetric — every school on 4 of 6, every
type on 4 of 7 but greatsword (7) and bow (5) — so coverage separates almost
nothing now, and it will separate less with every build.

**Registered for the next survey, and it is not this relic's problem:** both
vigil cells sit at the top of the table on both pins and have now been passed
over three times. If the two strongest open cells in the game keep being
declined on grounds the table cannot see, the table is measuring the wrong
thing and should be told what the actual criterion is.

---

# Open decisions

1. **THE VIGIL PAIR.** `vigil x twinblade` (+50.0pp) and `vigil x flail`
   (+30.8pp) are the two strongest open cells in the game and have been passed
   over three surveys running. Either they are next, or the ranking column
   needs a second axis that explains why they are not.

2. **THE BOW ROW IS A COIN FLIP.** umbral +14.6 against runic +11.9 at 260
   fights an arm, and the two swap across the pin. Whichever is taken, it is
   not being taken on this number.

3. **`row_price --pin` SHOULD DEFAULT TO 0.** The flag stays — pinning is the
   right way to ask "is this channel worth anything at equal weight" — but the
   default is a claim about the game and 14 is not a weight anything in the
   game fights at. One line.

4. **THE HARNESS PIN IS NOT AVAILABLE TO COWORK.** `cdn.playwright.dev` is
   blocked from this environment, so every Cowork survey from here runs a
   different Chromium from the one the repo pins and the mp4s are rendered on.
   The reproduction control in the header is the mitigation and it should be
   run at the top of every Cowork survey from now on, not just this one.

5. **`STATUS.curse.tip` STILL SHIPS THE PRE-REWORK WORDING** — *"Hits reflect
   8% of the damage that cursed"*. Open since v55, still 40 characters, still
   one line.

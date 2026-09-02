# v62 HANDOFF — DUSKREAVE AND SCOUR, THE UMBRAL SCYTHE. THE MECHANIC AND THE NAMES ARE SETTLED AND THE RELIC MEASURES +55.8pp, WHICH WOULD MAKE IT THE STRONGEST ULTIMATE IN THE GAME. THREE READINGS IN THIS SESSION WERE PUBLISHED AND THEN WITHDRAWN AND THEY ARE ALL LISTED BELOW.

**CHECKED 2026-09-02 — READ `../v63/duskreave-check-v63.md` BEFORE THIS FILE.**
The v63 check found: (1) the curse reading in §1–§2 holds against the engine,
line for line; (2) §1's +55.8pp reproduces exactly on the same Chromium; (3) but
every v62 arm ran with the scythe donor's own ultimate, Bramblesnare, still
firing — stub it the way every other lab does and **Scour is +59.2pp**, hotter,
with no v62 ruling flipping; (4) §3.1's trim arithmetic was wrong — the base
tick barely moves the number, the tick rate and width do, and a priced ladder
is in v63 §4; (5) §2's `resolveHit` note is necessary and not sufficient —
`resolveHit` also knocks back, hit-stops, hit-stuns and files a beat on every
call, and the brief must exclude those (v63 §5); (6) nine of the ten tools in
§7 hardcoded a container path and would not have run on Rick's machine — fixed.
The numbers below are left as v62 wrote them.

---

**Cowork, 2026-09-01.** Written for the session that checks this work. Read this
file before `duskreave-design-v62.md` — that document is 57KB across seventeen
sections and it is **not a linear read**, because three of its sections were
withdrawn by later ones.

**NOT A BUILD BRIEF. DO NOT BUILD FROM THIS.** Four decisions are open (§3) and
one of them changes the relic's numbers.

---

# 0. THE ONE-PARAGRAPH STATE

Rick took `umbral × scythe` — the last open scythe, the cell that retires the
row — from four priced candidates. He gave the §1 himself: a purple electric
tornado that paths the arena floor, eats projectiles, and drags the enemy down
into rapid ticks of damage that apply curse. Four rounds of this session
measured whether those ticks FEED the curse pool, concluded no, and were
measuring the wrong direction. **Rick corrected it: the ticks CASH the pool, on
every tick, and a school that pays per hit is a multiplier for an ultimate that
hits twenty times.** That is the relic. It is named **Duskreave**, its ultimate
**Scour**, and at the settings Rick chose it measures **+55.8pp**.

---

# 1. THE RELIC AS SETTLED

```
cell            umbral × scythe        the last open scythe; retires the row
relic           DUSKREAVE              from four: Barrowgale, Wraithcoil,
                                       Duskreave, Hollowgyre
ultimate        SCOUR                  from four: Undertow, Scour, Squall,
                                       Attrition
blade           21                     Bloodmirror's weight; scythe row runs
                                       17.25 (Vesper) to 31.35 (Thornwake)
body            reach 104, spin, mass 2.4   — fixed for every scythe in the game

THE TORNADO
  height        top at y = 600         a third of the arena; contact 26%
  width         160                    31% of the arena's 520
  sweep         200 px/s               MEASURED FREE — contact is 17.3% at
                                       120 px/s and 17.4% at 300. Looks only.
  cast          10 seconds             a DURATION, not a count of passes —
                                       Rick chose this over the fixed-count
                                       shape he took for Breach and Crossweave
  casts/fight   ~2                     at charge ~15
  tick rate     7 a second             ~23 ticks a fight
  tick damage   5 base                 plus the target's curse echo
  projectiles   the tornado eats them  KEPT AS FLAVOUR AND NEVER PRICED —
                                       fires in 9 matchups of 29
  curse         ticks are HITS: they COLLECT the echo and they APPLY curse,
                both, exactly as the §1 says
```

**MEASURED, 986 fights an arm against all 29 other relics:**

```
    no ultimate                  26.6% win
    SCOUR                        82.4% win      226 dmg a fight, 113 a cast
    SCOUR IS WORTH              +55.8pp         of which the apply clause is +0.6
```

---

# 2. THE BUILD NOTE THAT DECIDES WHETHER THIS SHIPS AS DESIGNED

**There are two damage paths in this engine and they are twelve win points
apart.**

- **`resolveHit`** — crit, jitter, `dmgTakenMul` (Sunder), **the curse echo**,
  Aegis, hit-stop, knockback, `onHit` status.
- **`hurt(foe, dmg, src)`** — shield absorption, then `foe.hp -= dmg`. Nothing
  else. **No echo.**

**Sentinel's beam, the nearest precedent for a ticking ultimate, uses `hurt`.**
`beamHit` calls `this.hurt(foe, dmg, f)` and collects nothing. A builder
following the nearest precedent will build a +17.8 relic and never notice there
was a choice. **Scour's ticks must go through `resolveHit`.**

---

# 3. WHAT IS OPEN — ALL OF IT RICK'S

1. **+55.8pp IS ABOVE THE FIELD. TRIM OR ACCEPT?** Crossweave measured +48.8
   and was second only to Harrowing; Scour clears both. The cast delivers 113
   against a 100 budget, twice. **The trim is one number:** 7 ticks at base 4 is
   90 a cast, or 4.5 ticks at base 5 is 87. Either lands beside Crossweave.
   Rick has been shown this and has not ruled.

2. **THE ROLLING WINDOW.** Rick proposed replacing curse's top-3-by-size rule
   with a rolling window of the last 3 hits. Measured in §13, §14, §16. It is
   nearly a no-op for the shipped game and it costs Duskreave 55 echo at 4.5
   ticks a second and 82 at 10. **He has not ruled.** `CLAIMS.md` shows
   `umbral × bow` BUILDING with Claude Code right now; a curse rule change
   under a live build is the third collision waiting to happen.

3. **THE SCRUNCH CARD COPY.** Not drafted. Rick's, per `CLAUDE.md` §3 rule 2.
   The card is the only surface the game teaches on.

4. **THE ANIMATION AND THE SOUND.** Not drafted. Rick's, both.

---

# 4. WHAT THIS SESSION GOT WRONG. CHECK THESE FIRST.

**Three readings were published to Rick and then withdrawn.** Two of the three
were caught by Rick, not by this session.

- **§7 — "the curse memory grows tick by tick."** Inferred from two of Rick's
  answers, offered as settled, and **rejected by him.** Withdrawn in §9b.
- **§9a — "tick rate is pure feel, no balance."** Wrong. On the `resolveHit`
  path every tick collects an echo, so **tick rate is a direct damage
  multiplier** — worth 22 win points across its range. **Rick caught this.**
  Withdrawn in §15.
- **§11c — "a heavier blade makes every tick hit harder."** The pool does rise
  (90 to 136) and the echo with it (80 to 100), but a heavier blade kills
  faster, so there are fewer ticks. **Tornado damage is flat at 176-177 across
  the whole blade range.** Withdrawn in §12.

**And one measurement was reported and then refuted by its own re-run.** §10's
tick A/B at 120 fights an arm showed the tick-curse arm at **+5.0% win rate**.
At 320 it reads **−0.9%**. The first number was noise. **Outcome columns in
this engine need n≥300 where state columns are stable at 100.**

---

# 5. CONTROLS THAT FAILED, AND WHAT WAS DONE

Every table in the design doc carries a control that could come back wrong.
**Two did.**

- **`tornado_lab.py`, first version.** Compared an edge-rule sweep (ball caught
  when its RIM crosses y=600) against §1's centre-rule histogram (ball counted
  when its CENTRE crosses). Ball radius is 34, so the rules differ by 34px and
  the sweep read 51.5% against the histogram's 37.8%. **Both numbers were
  right; the comparison was not.** Fixed to compare like with like: 51.5% vs
  51.5%, PASS. The failure and its cause are in the tool's docstring.
- **`rate_ladder.py`, ladder [B].** Meant to hold total base damage constant
  and vary only the number of hits. **The base drifted 95 to 134** because the
  expected-tick estimate that sets `base = total / expected` is approximate.
  **The absolute numbers are not quotable.** Salvaged by ratio — echo per unit
  of base damage is immune to the drift — and that ratio (0.25 → 1.67, a 6.6x
  rise) is what the claim was about.

**One control passed in a way worth trusting:** contact measured **26.2%** in
`tornado_full.py` against the **26.0%** `tornado_lab.py` predicted from
position tracks alone — different code, different fights, two tenths of a point
apart.

---

# 6. THE LIMITATION THAT MATTERS MOST TO A CHECKING SESSION

**No lab in this session built the ultimate. Every tick was simulated.**

The tornado's ticks are modelled as `m.hurt(foe, base + Math.round(foe.curseEcho()), me)`
— that is, `hurt` plus a hand-computed echo. **A real `resolveHit` tick would
additionally get crit, damage jitter, `dmgTakenMul` (Sunder), Aegis reflection,
hit-stop and knockback.** None of those are in these numbers.

**So +55.8pp is not a prediction of the built relic.** Sunder and crits would
push it up; Aegis and shields would pull it down; hit-stop changes the fight's
pacing in ways nothing here models. **The first thing to do after a build is
re-run `ult_price.py` against the real thing and compare.** Treat +55.8 as
"this design is in the top tier and needs a real price", not as a number.

Two smaller modelling notes:
- The two 10-second cast windows are pinned at t=12–22 and t=30–40 rather than
  fired by the real charge system. Real cast timing will differ.
- The tornado's drag does not move the fighter it catches. A real drag holds
  the ball, which would raise contact above the measured 26%.

---

# 7. THE TOOLS THIS SESSION WROTE — ALL IN `tools/`, ALL RUNTIME-ONLY

```
tornado_lab.py       sweeps a band through real position tracks; contact by width
tornado_full.py      the tornado at real geometry, hurt-path vs resolveHit-path
tornado_fifo.py      the same, under both curse rules, push and no-push
echo_collect.py      does a tick collect the echo? the first version of the above
tick_ab.py           does a tick-sized curse do anything? 3 arms, 320 fights
tick_trace.py        ONE cast tick by tick under both rules — the most legible
curse_fifo.py        the rolling window: unit check, flatness, the 4 built relics
push_monotone.py     is pushing curse ever a loss? four lines, answers §16
blade_sweep.py       blade x ultimate across the scythe row
rate_ladder.py       tick rate as a damage knob (ladder [B] control FAILED)
duskreave_config.py  the shipping configuration, measured whole
```

**Run them with `python` or `py` on Windows, never `python3`.** All take
`--game` and default to `02-chain/sc-garrote.html`.

**RUNTIME DECLARATION.** Every number in v62 was measured against
`02-chain/sc-garrote.html` — the build of record, 30 relics — on **Chromium
141.0.7390.37**, byte-identical to the runtime v57, v59 and v60 quote. A
reproduction control was run first: ten open cells repriced, largest move 4.0pp
against a 270-fight SE of ~4.3pp.

---

# 8. READING ORDER FOR `duskreave-design-v62.md`

It is not linear. If you read it top to bottom you will read three arguments
that were later withdrawn.

```
  START HERE   §11   the ticks CASH the pool — the finding the relic rests on
               §16   why that is monotone under the shipped rule and not under
                     a window — the clearest four lines in the document
               §17   the shipping configuration, measured whole
               §14   one cast tick by tick, both rules — the most legible table
               §15   tick rate is a damage knob (withdraws §9a)
               §13   the rolling window priced across the whole school
               §12   the blade (withdraws §11c)
               §1-2  the floor and the projectiles — both still stand
  SKIP         §3-§10  the four rounds that measured the wrong direction. They
                       are correct about what they measured and they are not
                       the reason the relic works. §10 is worth reading only
                       for the n=120 vs n=320 lesson.
  WITHDRAWN    §7 (by §9b) · §9a (by §15) · §11c's blade claim (by §12)
```

---

# 9. WHAT I THINK NEEDS DOING, IN ORDER

1. **RICK RULES ON THE TRIM (§3.1) AND THE WINDOW (§3.2).** Nothing else can be
   written down until the first one lands, because it sets the numbers the
   brief carries.
2. **RICK GIVES THE CARD COPY, THE ANIMATION AND THE SOUND** — three of his
   seven, and all three are still blank. The card matters most: it is the only
   place the game explains itself now the fight card is gone.
3. **THEN THE BUILD BRIEF** — `06-docs/v62/DUSKREAVE-BUILD-BRIEF.md`, staged in
   separable commits with gates, the way Rick asked for the umbral package on
   2026-08-31. The natural stages are: the tornado exists and sweeps · it
   catches and ticks on the `resolveHit` path · it eats projectiles · art,
   sound and beat.
4. **AFTER THE BUILD, RE-PRICE IT FOR REAL** with `ult_price.py` and compare
   against +55.8 (§6). If the built relic comes in far from it, the gap is the
   modelling limitation and it should be written down, not smoothed over.
5. **AND SOMEBODY SHOULD DELETE `umbral-scythe-design-v62.md`** — it is a
   491-byte pointer stub left behind by a rename this session could not perform
   properly, because the device bridge it was working through cannot delete
   files.

---

# Open decisions

1. **THE TRIM.** §3.1. +55.8pp is above the field. One number fixes it and
   Rick has not ruled.
2. **THE ROLLING WINDOW.** §3.2. Not ruled. Should not land under Code's live
   Gloamwire build in any case.
3. **CARD COPY, ANIMATION, SOUND.** §3.3, §3.4. All Rick's, all blank.
4. **IS THE `hurt`-VS-`resolveHit` NOTE LOUD ENOUGH?** §2. It is the one place
   this relic can be built wrong while looking right, and it will not throw an
   error — it will just be twelve points weaker.
5. **`ult_price.py` AND `cell_ults_on.py` SHOULD PRINT THEIR BUILD AND THEIR
   CHROMIUM.** This session had to read both out of a separate document to know
   its numbers were comparable to v60's.

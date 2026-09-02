# v63 — THE v62 WORK CHECKED. THE CURSE READING HOLDS AGAINST THE ENGINE AND THE HEADLINE NUMBER REPRODUCES TO THE DECIMAL — BUT EVERY v62 ARM RAN WITH THORNWAKE'S OWN ULTIMATE STILL LIVE, AND WITH IT STUBBED THE WAY EVERY OTHER LAB IN THE REPO STUBS IT, SCOUR IS +59.2pp, NOT +55.8.

**Cowork, 2026-09-02.** A checking session, asked for by Rick: *"weve had some
trouble getting aligned on how curse would affect the ult. please double check
the last sessions work."* Nothing here is a design change. Every ruling Rick
made in v62 stands; two numbers move and one build note is added.

Against `02-chain/sc-garrote.html`, the build of record, 30 relics, Chromium
**141.0.7390.37** — the same runtime v62 quoted, confirmed by `navigator.userAgent`
inside the harness. ~21,000 fights. Nothing written to any build.

---

# 0. THE ANSWER TO THE QUESTION RICK ASKED, IN PLAIN WORDS

**How curse affects the ultimate — checked against the code, not the doc:**

Curse on a fighter is a list of the **three biggest single blows** ever landed
on them, kept for the whole fight. Every hit that lands on that fighter, from
anyone, is enlarged by **8% of the sum of those three**. That is the "echo".

The tornado's ticks are hits. So **every tick is enlarged by the echo.** With
the scythe's three memories sitting around 100 total, that is roughly +8 on
top of a 5-damage tick — and it happens ~23 times a fight. Measured, the echo
is **half the tornado's damage**: 113 of 226 a fight.

Each tick also *applies* curse — pushes its own ~5 into the list. Under the
shipped rule the list only keeps the three biggest, so the 5 is looked at and
thrown away. **That costs nothing and changes nothing** (+0.6pp, inside the
noise). It stays in because Rick's §1 says it and because it is free.

**Both halves of "rapid ticks of damage that apply curse" are therefore true
in the engine as written.** The collecting half is where the value is. The
applying half is the picture. Nothing about this needs a rule change.

---

# 1. WHAT WAS CHECKED AGAINST THE ENGINE — ALL FIVE HOLD

Read directly from `sc-garrote.html` (line numbers are that file's):

| v62 claim | where | holds? |
|---|---|---|
| `pushCurse` pushes, sorts descending, truncates to `maxStacks` 3 | 6696–6701 | yes |
| `curseEcho()` = `curseSum() * 0.08` | 6705, 731 | yes |
| `resolveHit` reads `foe.curseEcho()` off the TARGET, no owner guard, folds it into `dmg` above the Aegis block | 10812–10814 | yes |
| `hurt()` is shield-then-hp and nothing else — no echo | 10592–10603 | yes |
| Sentinel's `beamHit` uses `hurt`, so the nearest ticking precedent collects nothing | 8956–8961 | yes |
| `apply("curse")` without a memory refreshes the clock and derives stacks from the pool | 6707–6720 | yes |
| curse `dur` 99 — lasts the fight | 731 | yes |

**The reading v62 §11 rests on is the engine's.** There is no interpretation
left in it.

---

# 2. THE HEADLINE NUMBER REPRODUCES EXACTLY

`tools/duskreave_config.py`, v62's own tool, unmodified, 986 fights an arm, in
this container:

```
    no ultimate                  26.6%
    SCOUR, ticks apply curse     82.4%     226.0 a fight, 113.0 a cast
    SCOUR, ticks do not apply    81.7%
    SCOUR IS WORTH              +55.8pp    apply clause +0.6pp
```

**Identical to v62 §17 to every decimal.** Same build, same Chromium, same
seeds, deterministic engine. The runtime is declared as an input and it is the
same input.

---

# 3. THE FLAW: THORNWAKE'S BRAMBLESNARE WAS LIVE IN EVERY v62 ARM

Every v62 lab grafts umbral curse and the test blade onto the scythe donor,
`thornwake`. The graft rewrites `aff`, `dmg`, `onHit` — **and leaves `w.ult`
alone.** Thornwake's ultimate is **Bramblesnare**: a 1.6-second root at radius
260, 10 damage, 3 Entangle, charge 15. It fired **2.34 times a fight** in v62's
"no ultimate" arm and **1.72** in its Scour arm (counted off `me.ultsFired`).

So v62's "no ultimate" was *Bramblesnare*, and its "Scour" was *Bramblesnare
and Scour together*.

**Every other design lab in the repo stubs the donor's ultimate** —
`spectre_lab`, `wire_lab`, `quiver_lab`, `row_price` and `cell_ults_on` all set
`w.ult.charge = 1e9` so the cell has no ultimate but the one being designed.
The ten v62 tools are the only ones that do not.

`tools/duskreave_price.py` is `duskreave_config.py` with that one line added
and a `--donor-ult live` switch to reproduce v62. Same seeds, same model, same
runtime:

```
                                  BRAMBLESNARE LIVE (v62)      BRAMBLESNARE OFF (v63)
    no ultimate                        26.6%                        17.6%
    SCOUR, ticks apply curse           82.4%                        76.9%
    SCOUR, ticks do not apply          81.7%                        77.5%
    SCOUR IS WORTH                    +55.8pp                      +59.2pp
    apply clause                       +0.6pp                       -0.6pp
    paired flips                      594/986                      610/986
    donor casts a fight (no-ult arm)     2.34                         0.00
```

**CONTROL 1 — the `live` switch must reproduce v62 exactly: 26.6 / 82.4 / +55.8.
PASS.**

**CONTROL 2 — with the donor's ultimate off, the no-ult floor must sit below
`cell_ults_on`'s 39.0% for a 31.35 blade with no ultimate, because this is a
21 blade: 17.6%. PASS.** (And it must sit below the live floor, because a root
is worth something: 17.6 < 26.6.)

> **THE FINDING.** Bramblesnare was worth **9 points to the no-ult floor and
> 5.5 to the Scour arm.** Take it out of both and Scour is worth **+59.2pp**,
> three and a half points MORE than v62 said. The correction makes the relic
> hotter, not cooler.
>
> **NO v62 RULING FLIPS.** Every table in v62 compared arms that both had
> Bramblesnare live, so the *differences* it reported — tick rate is a knob,
> the blade coupling cancels, the window costs a quarter of the damage, the
> apply clause is free — were measured on a consistent baseline and stand. Only
> the *absolute* headline, the one the trim decision hangs on and the one
> compared against Crossweave's +48.8, was off — and it was off in the
> conservative direction.

---

# 4. THE TRIM, PRICED PROPERLY — AND v62's ARITHMETIC FOR IT WAS WRONG

v62 §17 offered the trim as *"7 ticks at base 4 is 90 a cast, or 4.5 ticks at
base 5 is 87."* The first of those assumed the whole cast scales with the base
tick. **It does not — the echo is independent of the base tick,** and the echo
is the bigger half. Cutting the base from 5 to 4 cuts ~19 of a 114-damage cast.

The ladder, `duskreave_price.py --donor-ult off`, 986 fights an arm, blade 21,
160 wide, 10-second casts, ticks apply curse:

```
    ticks/s   base   ticks/fight   base dmg   echo dmg   total   per cast   SCOUR IS WORTH
        7       5        22.9        114.4      113.3    227.8     113.9        +59.2pp   <- as settled
        7       4        23.8         95.4      118.6    214.0     107.0        +56.6pp
        7       3        24.8         74.3      124.8    199.1      99.6        +51.8pp
        5       5        19.0         94.8       97.8    192.6      96.3        +50.1pp
        4.5     5        17.4         86.8       90.6    177.4      88.7        +47.1pp   <- beside Crossweave
        3       5        12.7         63.3       68.5    131.8      65.9        +31.5pp
    7 / 5, 120 wide      20.0        100.2      102.1    202.2     101.1        +52.8pp
```

**CONTROL — the no-ult arm is the same 986 fights in every row and must read
17.6% in every row. PASS, every row.**

> **THE BASE TICK IS THE WEAK KNOB AND THE TICK RATE IS THE STRONG ONE**, which
> is v62 §15's finding arriving from the other side. Notice the echo column
> *rises* as the base falls (113 → 125): a weaker tornado kills slower, the
> fight runs longer, and the tornado collects the echo more times. The relic
> resists a base-damage trim because its damage is mostly not its own.
>
> **WHAT ACTUALLY LANDS BESIDE CROSSWEAVE (+48.8):** 4.5 ticks a second at
> base 5 (+47.1), or 5 a second (+50.1). Both keep the blur Rick asked for and
> both keep every one of his other rulings. **Both also give back the one thing
> he raised on purpose** — he moved the rate from 4.5 to 7 after being shown
> tick rate was a knob — so this is his to weigh, not a recommendation.
>
> **A width trim** — 160 to 120 at Rick's 7/5 is +52.8 — moves contact rather
> than payload and is the one trim that leaves the tick rate alone. It is also
> the one a viewer sees: a narrower tornado.

---

# 5. THE BUILD NOTE v62 §11c DID NOT FINISH — `resolveHit` DOES FOUR OTHER THINGS ON EVERY CALL

§11c is right that the ticks must go through `resolveHit`, or the echo is never
collected and the relic ships twelve points weaker. **It is not enough to say
so, because `resolveHit` is a whole blow, and a whole blow seven times a second
is not a drag.** Read from the build:

| on every `resolveHit` | line | at 7 ticks/s, ~10 dmg a tick |
|---|---|---|
| **knockback** `combat.knock` (165) × the weapon's `knockMul`, **away from the caster's ball** | 11219–11222 | seven shoves a second, in a direction that has nothing to do with the tornado — it throws the foe OUT of the thing that is supposed to be holding them |
| **hit-stop** `max(hitStop, 0.045 + dmg × 0.0022)`, capped 0.13 | 10907–10910 | ~0.067s a tick; the world freezes (`step` 7184–7187) for ~45% of every second the tornado holds someone |
| **hit-stun** `takeHitstun(dmg)` — with diminishing returns | 10955 | a foe locked 7 times a second; the DR will grind it down but the first second is a stagger-lock |
| **a director beat** of kind `hit` | 10936–10954 | 23 beats a fight from one ultimate; `cinePlan` cuts to them |
| crit (9%, ×2.1), jitter (±15%), `dmgTakenMul` (Sunder), Aegis absorption + reflect | 10742–10897 | these are fine and arguably wanted — they are what makes a tick "a hit" |

**No relic in the game ticks through `resolveHit` today.** Harrowing's stuck
scythes and sparks use `hurt` plus their own `stopBase`/`stopPer` knobs
(11320, 13371); Sentinel's beam uses `hurt`; the Thicket's lashes go through
`resolveHit` but at blade cadence, and they needed `_cineVine` (10924–10936)
to keep the beats off the director. Scour would be the first per-tick
`resolveHit` consumer.

> **WHAT THE BRIEF HAS TO SAY.** A Scour tick takes from the pipeline: the
> damage roll (jitter, crit, Sunder), **the echo**, the Aegis check, `hurt`,
> and the `onHit` curse push-and-apply. **It does not take: the knockback, the
> ordinary hit-stop, the hit-stun, or the beat.** The cleanest shape is an
> `over` extension — `over` already carries `onHit` (10990–10995) — with
> something like `{ knock: 0, stop: 0, stun: false, beat: false }`, so the
> tick is a `resolveHit` call and not a fork of it. Whether the tornado wants
> its OWN small stop or stun, the way Harrowing carries its own, is a feel
> question for the film-before-you-tune pass (CLAUDE.md §4.0), not a
> simulation one.
>
> This is the second place the relic can be built wrong while looking right.
> The first (§11c) ships a weak Scour. This one ships a Scour that flings the
> foe out of its own tornado and freezes the clip half the time it is on.

---

# 6. THE v62 DOCUMENT CONTRADICTED ITSELF ON THE ONE THING RICK ASKED ABOUT — FIXED

Three places in `duskreave-design-v62.md` said the ticks should **not** apply
curse, and all three were written before §14–§17 settled that they do:

- the **title** — "the tornado's third clause is the dead clause";
- the **header block** — "IN PROGRESS … blade, names … do not exist yet";
- **Open decisions item 2** — "DO THE TORNADO'S TICKS APPLY CURSE AT ALL? …
  the answer that measures best is **no** … the ticks should COLLECT and not
  APPLY."

A builder who reads the foot of a document first — which is where the open
decisions are — would read that item as the current state. **It was the exact
reading Rick had rejected four times** (*"why do you continue to keep
suggesting the ult to not apply curse"*). All three are rewritten in place,
dated and attributed, with the v62 body left intact as the record. The HANDOFF
carries a banner pointing here.

---

# 7. THE TOOLS DID NOT RUN ANYWHERE BUT THE CONTAINER THEY WERE WRITTEN IN — FIXED

Nine of the ten v62 tools hardcoded `/mnt/user-data/uploads/sundered-crown/…`
for both the `scpage` import and the default `--game`. The HANDOFF said *"all
take `--game` and default to `02-chain/sc-garrote.html`"*; that was the
intent and not the file. On Rick's machine every one of them would have died
on the import line.

All nine now resolve `HERE` from `__file__` and route `--game` through
`scpage.resolve_game`, which is the convention every older tool follows.
Verified by running `push_monotone.py` from outside `tools/` and getting v62
§16's table back. `duskreave_price.py` is written the same way. **Numbers
printed by the nine are unchanged** — only the paths moved — so they still
reproduce v62's tables, Bramblesnare and all; the docstring of each does not
yet say so, and a reader should carry §3 of this file with them.

---

# 8. WHAT THIS CHECK DID NOT DO

- **It did not build the ultimate.** The model is still v62's: `hurt` plus a
  hand-computed echo, windows pinned at t=12 and t=30, no crit or Sunder in the
  ticks, and a drag that does not move the ball. Every number above inherits
  those limits (HANDOFF §6). The +59.2 is "top tier, needs a real price after
  the build", exactly as v62 said of +55.8.
- **It did not re-run the eight other v62 tables with Bramblesnare off.** Their
  findings are differences between arms on a shared baseline (§3) and the
  check does not expect them to move in sign. If any is quoted as an absolute
  in a brief, re-run it with `charge = 1e9` first.
- **The rolling window — RULED IN after this section was written.** Priced
  first with `duskreave_price.py --curse-rule fifo --donor-ult off`, same 986
  fights: no-ult 18.2%, Scour 58.6%, **+40.5pp**, echo 49 a fight (113 under
  the shipped rule). Rick: "last-3 goes in; Scour lands at ~+40." Its own
  claim and note: `curse-window-v63.md`. It still does not land under
  Gloamwire's build.

---

# Open decisions

1. **THE TRIM.** §4. Rick's. The honest options are the tick rate (4.5–5 a
   second lands beside Crossweave) or the width; the base tick barely moves it.
   Or accept +59 and let it be the strongest ultimate in the game.
2. **THE ROLLING WINDOW.** v62 §13–§16. Not ruled. Costs this relic a quarter
   of its damage, gains the rest of the game almost nothing, and should not
   land under a live build.
3. **THE CARD, THE ANIMATION, THE SOUND.** Rick's. Blank.
4. **THE TICK'S OWN STOP AND STUN.** §5. Whether a tick should carry a small
   hit-stop or stagger of its own, Harrowing-style, or none. Feel; film first.
5. **THE NINE TOOLS' DOCSTRINGS** still describe arms that had Bramblesnare
   live without saying so. One line each. Not done here because it changes no
   number and the check was the point.

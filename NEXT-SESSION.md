# v43 — HANDOFF. The twenty-fifth relic, and the first thing in this game that stops a ball.

**2026-08-21.** Runic × flail built, priced before it was built, refuted three
times by its own probes, rebuilt, tuned, filmed.

```
02-chain/sc-paradox.html            <- THE RELIC
02-chain/sc-paradox-frame.html      <- THE BUILD OF RECORD
built off 02-chain/sc-marrowdraw.html
01-live UNTOUCHED, still on sixteen

cell_survey             7/7      the grid on the v42 tip — 18 cells open
verify --n 40 (v42 tip)13/13     11040 fights, so the cell was priced at 40 seeds
flail_survey           26/26     the flail row, before the design existed
runic_flail_probe      12/12     §1 PRICED BEFORE A BUILDER WAS OPENED
paradox_relic_probe    31/31     one check per sentence of §1, against the build
paradox_sweep            —       need x bleed x blow, dmg bisected in every cell
engine_ab          2760/2760     IDENTICAL on the other twenty-four
chain_audit            12/12     every insert survives to the tip
frame_probe            11/11
verify.py --n 40       13/13     Paradox 47.7%, 0/12000 timeouts
SEED 25064 NO LONGER LANDS A KILL. On the pinned runtime it is a 40.12s
timeout finish, so the clip below cannot be rebuilt from its own seed -- 4.2b,
working exactly as documented, and this is the first time anyone has hit it.
paradox_pick.py on the current tip offers seed 55957: 41.1s, 2 casts, 3 holds,
two blows landed on a held quarry for 282, and the hold lands the last blow.
That is the paradox clip to film now.

07-shorts/v43/stasis-v-heartwood.mp4   seed 25064, 23.0s, three holds and the
                                       window lands the last blow
```

Read `06-docs/v43/` in this order:

| doc | the headline |
|---|---|
| `sundered-crown-flail-survey-v43.md` | The type, before anything was designed. **The flail's live blade is 13.2 units where a greatsword's is 128, and its own contact interval is longer than its own status.** |
| `sundered-crown-hexring-design-v43.md` | §1 in Rick's words and §1 PRICED. **Two of its four sentences could not be built as written, one is a free look knob, and the fourth is the best thing in it.** |
| **`README.md`** | The build. §4 is the pricing, §5 is the one line that had to be invented, §8 is a sound that landed first time because it was offered as a spread, §10 is what the probes caught. |

---

# RICK'S THREE RULES STILL STAND, AND HERE IS WHERE THEY LANDED

## 1. THE FIGHT CARD IS DEAD

Nothing shipped with one. Still IN the build — `introcard_build.py` writes it,
`m.introT` is on every Match, the guard in `cinema_clip` is what stops it.
**Unmoved for a fourth session.** v40's sentence is unchanged: *"die completely"
means removing it, and that is a chain-wide change that wants its own session
and its own probe.*

## 2. RICK GIVES INPUT ON SEVEN THINGS — AND ALL SEVEN WERE ASKED

```
  the CELL               four candidates, priced at 40 seeds first. He took
                         runic x flail, and the sentence it was sold on turned
                         out to be half wrong — see rule 4.
  the ult MECHANICS      §1 in his words, then THREE FORKS priced from
                         measurement before they were put to him: how "too
                         long" is counted (a continuous 2s stay happens ZERO
                         times a minute), what the inert "extra hit stun"
                         sentence should do instead, and how big "medium sized"
                         is. And a fourth he answered unprompted: what a held
                         ball does with the knockback it eats.
  the ult NAME           Stasis Field, and HIS OWN WORDS. Twelve were offered
                         across three spreads and he rejected two spreads
                         outright — which is the "offer a spread" lesson from
                         the other end: being wrong about the REGISTER is what
                         costs. `hex-*` was ruled out BEFORE the first spread
                         because the school's status is called Hex and the hold
                         OVERWRITES 61% of its fires.
  the FIGHTER name       Paradox, from four offered. The id matches.
  the SCRUNCH CARD       STILL OPEN. The placeholder is 67 of the 72 characters
                         `verify` allows — a limit nothing in this project had
                         ever hit.
  the ult ANIMATIONS     two cuts, and the second one was HIS IDEA: "how about
                         we add lightning lines that connect from the hexagons
                         edges to the center?" A ring with nothing joining it
                         to the relic reads as a thing the HALL is doing.
  the ult SOUND          ONE PASS. Six casts and four holds rendered into two
                         files before he was asked anything; "first option on
                         both". Against v42's four serial failures.
```

**Two of his answers were refutations of measurements I had put in front of
him** — the pin's banked knockback, and the second cut of the art — one was a
mechanic I would not have thought of, and **one was a bug nothing in this repo
could have found.**

> *"9 seconds into that video. really weird physics on paradox colliding with
> the stunned opponent."*

A held ball keeps the vector it was captured with, and `_ballPair` was feeding
that straight into the relative-velocity term — but **a held ball's velocity is
a MEMORY, not a motion.** With the stored vector pointing away, the exchange
came out near zero and the caster did not bounce off: it STUCK to the thing it
had frozen and slid along it, for as long as **2.067 seconds, which is the
whole hold.** Now 0.142s.

**It moved no win rate worth seeing, filed no error, broke no invariant, and
the relic probe was 30/30 with it live.** It is a PICTURE fault — the second
one this project has had that only a person watching could catch, after v42's
silent ultimate. README §7.

## 3. A HIT-HEAVY ULT MUST DECLARE ITSELF TO THE DIRECTOR

**This relic is the sharpest case yet, because it deals no damage at all.**
Nothing about a hold is a hit, so nothing else in the frame files anything and
`cinePlan` would score the most legible moment of the ultimate as empty air. A
hold files a beat now — fifth relic running.

**And then the pick tool returned ONE candidate out of 340**, which produced the
first measurement of this in the project:

```
relic          any cut   FATAL cut   mean cuts   best beat
axiom              62%         23%        1.06        2.04
gravemourn         56%         23%        0.62        2.00
redflail           46%         19%        0.48        2.23
PARADOX            38%         12%        0.52        1.82
thornwake          38%         10%        0.44        1.77
foregone           23%          8%        0.27        2.17
```

**A fatal cut is rare for every melee relic in this game.** `cineScore`'s big
multipliers are closing speed and flight distance, and a melee relic that lands
one blow every six seconds has neither. Paradox is on the low side of an 8–23%
band, not outside it. Chain-wide, named, not fixed.

**The shared `cineFloor` is STILL not built.** v40's first pickup item, still
first, six relics deep.

---

# WHAT v43 ADDS TO THE RULES

## 4. `cell_survey`'s OCCUPANCY COLUMN HAS NOW MISPRICED TWO CELLS

The cell was taken on *"the thinnest cell ever measured here — 15% at two or
more stacks and 0% at cap"*, and by delivered effect it is **the second-
strongest channel on its own row (+12.1%) and the only one of four that cuts
damage TAKEN.**

Occupancy is a proxy twice removed for a status that is a RATE (v39 5.2), and
the tool does not say so in its own output. The umbral row has been suspect
since v40 §4.1 for a related reason. **A survey that answers "which type"
correctly can still answer "which school on this type" wrongly, and the fix is
that the type gets its own probe — which is v40's rule, doing exactly its job.**

## 5. A CHECK CAN BE UNDERPOWERED, THEN CHAOTIC, THEN RIGHT

`flail_survey` §3 asked one question three ways before the answer meant
anything, and every step is a different failure:

1. **Contacts in a 2s window.** The flail expects 0.15 of one. Two types came
   back with the STUNNED arm ahead. That is not a wrong instrument, it is an
   underpowered one, and the tell is a sign flip in a control.
2. **The arc, over the same 2s.** Smooth quantity, usable variance — and the
   calibration row stopped holding, because the two arms are identical up to
   the stun and chaotic after it. **A long window measures divergence.**
3. **The arc over 1.0s, with the recovery horizon left long** because recovery
   is slower than the thing that caused it and is read off one arm, where
   divergence cannot reach it.

Four rigid types then come back at 0.92–1.07x of a 0.20s stun, **and that is the
control the flail's number lives or dies by.**

## 6. AND THE HYPOTHESIS WAS REFUTED ANYWAY, WHICH IS THE POINT

A stun costs the flail the same SWING it costs everything else. The head coasts
through it and the coast pays for the respin. **What it costs is REACH** — the
head pulls in to 0.58 extension and takes 1.08s to climb back, so a 0.20s stun
is a ~1.28s event of shortened reach. Six times the stun, in a column nobody
was looking at.

## 7. AN INSTRUMENT THAT FIRES WHERE THE MECHANIC DOES NOT, MEASURES SOMETHING ELSE

The pin was first priced by freezing the quarry at a fixed clock time and read
**−12% damage.** True of a pin; false of THIS pin. A foe frozen at the 259 units
this game averages is a foe a 115-unit head cannot reach — and this pin only
ever triggers on a foe already inside the hexagon, at a measured 136. Firing it
where the mechanic would fire it flips the sign to **+42%.**

## 8. OFFER THE SPREAD FIRST, NOT AFTER FOUR FAILURES

v42 learned to spread after four serial round trips had already failed. This
session spread FIRST: six cast candidates and four holds rendered into two files
before Rick was asked anything. **"First option on both."**

That is not evidence the first guess was good. It is evidence that a spread is
how you find out cheaply — and the same lesson arrived from the other end on the
NAME, where two spreads of four were rejected outright because both were in the
wrong REGISTER. Runic's three ultimates are abstract nouns; the roster's other
twenty-one are concrete, and I had generalised from three.

## 9. A METRIC NORMALISED BY PEAK REWARDS A QUIET ATTACK

"Is this sound a state or an event" was first measured as late-window level
divided by the sound's own peak, and the cast scored **worse than the control
for having a louder attack.** v42 §3c from the other side: when a brief becomes
a number, ask what the worst thing that scores well on it looks like.

## 10. A HELD OBJECT'S STORED STATE IS NOT ITS CURRENT STATE

The general form of the bug above, and it is worth having in these words
because `pin` will not be the last suspended state anybody adds here. **When a
thing is frozen and something about it is kept so it can resume, every OTHER
system that reads that field is now reading a lie.** `pinV` exists so the ball
can resume on exactly what it was doing; `_ballPair` read it as what the ball
was doing NOW.

The fix is not "clear the field" — the field is load-bearing. It is that every
reader has to ask whether it wants the memory or the motion, and there is no
type-system answer to that. Grep the field, read every site.

## 11. A BUILDER SHOULD SYNTAX-CHECK ITS OWN OUTPUT

This build wrote an unbalanced `*/` once — a comment paragraph appended after
the block it belonged inside — and the only signal was a twenty-second
Playwright timeout with a stack trace. `one()` counts `/*` against `*/` now.

**And `chain_audit` could not see this builder's inserts at all**, because its
regex did not allow a raw-string prefix and every `*_NEW` here is `r'''`. It
reported *"no *_NEW inserts found — nothing to audit, which is itself a
failure"*: the right message for the wrong reason, and one anybody in a hurry
reads as a pass. Fixed, one character.

---

## 12. A PICTURE FAULT IS A DEFECT CLASS, AND THIS PROJECT NOW HAS TWO OF THEM

v42's ultimate shipped **silent** through a 14-check probe, a 29-check probe, a
full sweep, a 13/13 verify and a rendered clip. v43's hold **stuck to the ball
it had just frozen for a full two seconds** through a 30/30 relic probe, a
2760/2760 engine A/B and a 13/13 verify. Both were caught by Rick watching.

They are the same class and it is worth naming: **a defect where "wrong" and
"right" produce identical numbers.** Sound and physics are both places where
the simulation is correct, no invariant breaks, no error is filed, and the only
difference is what a person sees or hears.

**The fix is never only the bug. It is the instrument.** v42 answered its
silence by RENDERING the sound in an OfflineAudioContext and measuring it, and
that check is now the reason a sound cannot ship quiet again. v43 answered its
sticking the same way, by measuring the quantity the eye was actually seeing:

```
                 hold frames in contact   contacts   mean     longest
first build                        6.9%         89   0.097s     2.067s
ships                              0.8%         88   0.014s     0.142s
```

**When a person catches something no tool could, the deliverable is a
measurement of the thing they saw** — not a fix and an apology.

## 13. FILM BEFORE YOU TUNE, WHEN THE ULTIMATE IS A PICTURE

**This is the single most expensive mistake in the session and it cost about
thirty thousand fights.**

The Stasis Field deals no damage. Its entire effect is a thing you watch
happen — a ball that stops. So the clip is not a deliverable that comes after
the numbers are settled; **it is a TEST, and it is the only test that can see
the class of fault §12 describes.** I filmed after tuning, because that is the
order every previous session used — and every previous session's ultimate could
be counted rather than watched.

The re-work: a second `verify --n 40` (12,000 fights), a second `engine_ab`
(5,520), a whole final bisection at 40 seeds (6,720), three pick runs and a
render, plus rewriting every document that quoted the old damage.

**Thirty seconds of clip on placeholder numbers, before the sweep, costs four
minutes.** Do that for anything whose ultimate is watched rather than counted.

## 14. WHAT A HUNDRED THOUSAND FIGHTS ACTUALLY BOUGHT

This session ran **~102,000 simulated matches, about 43 minutes of pure
simulation** at a measured ~40 matches a second in one headless V8 thread.
Reconstructed from the logs, ±10%:

```
discovery     changed what got built                   ~6,100    6%
verification  proved it changed nothing else          ~17,600   17%
tuning        found one number                        ~24,700   24%
selection     which fight to film                      ~1,100    1%
VOID          re-runs my own bugs invalidated         ~46,600   45%
```

**Six percent of the fights changed a decision.** The two surveys and the
pre-build probe are under 5,000 fights between them and they produced nearly
every finding that shaped the relic — `runic_flail_probe` refuted two of §1's
four sentences and set three of its numbers in **840 fights.**

**That ratio is not the failure.** Discovery is a SEARCH: a few well-aimed
fights kill a sentence. Verification is a COVERAGE ARGUMENT, and there is no
cheap version of *"all 2,760 are identical"* — the count IS the claim, and a
300-match engine A/B would be nine times weaker evidence for the zero-burden
argument the whole build rests on.

**The 45% is the failure**, and §13 is most of it.

### 14.1 Two cheap things, for whoever budgets the next one

- **A BISECTION SHOULD ESCALATE ITS SAMPLE.** `paradox_sweep.bisect` spends the
  same 960 fights on step one, where the interval is 12 damage wide and the
  answer is obvious, as on step seven, where it is 0.1 and the answer is the
  whole point. A schedule that starts at ~100 and ends at ~960 halves the cost
  of every bisection in this repo for no loss of precision.
- **THE GRID DOES NOT NEED A PRECISE BISECTION.** Phase 2 bisected nine cells to
  five steps purely to normalise telemetry that is not sensitive to ±1 damage.
  Three steps would have done, which is 4,300 fights.
- **AND NOTHING HERE IS PARALLEL.** One browser, one thread, start to finish.
  Four or eight worker processes over the seed range would be straightforward
  and roughly that much faster; every tool in `tools/` already takes its seeds
  as a list.

## 15. IF YOU GENERALISE FROM A SUBSET, GO AND LOOK AT THE SUPERSET FIRST

The ult name took **three spreads and twelve rejected candidates.** I inferred
runic's naming register from runic's own three ultimates — Corollary, Converse,
Unmaking, all abstract nouns — and never looked at the other twenty-one, which
are almost all concrete: Crucible, Thicket, Ironbloom, Bloodmill, Quarrelstorm,
Slagburst. Two spreads of four were rejected outright before I checked.

**Reading the whole roster was free and would have cost thirty seconds.** The
same shape as §4: a tool that answers one question correctly can answer the
neighbouring question wrongly, and the cheap defence is to look at the larger
set before trusting the smaller one.

# THE FIRST FOUR THINGS TO PICK UP

1. **THE CARD.** Rick's wording for Paradox's tip has not arrived and the
   placeholder is in the build. 72 characters, including the numbers.
2. **THE TWO REMAINING BEATLESS DEATHS.** v42 §9, unmoved. Daybreak's spark
   burn and `_traceHit` both take hp through `hurt()` and file nothing, and
   Dawnbringer is still 22.1% blind. The general fix is one backstop — *if a
   fighter died this step and no beat was filed, file one* — which is
   chain-wide and therefore Rick's call.
3. **RULE 3, BUILT PROPERLY.** A measured `cineFloor` and a windowed beat in
   `cinema_build.py`. v40's item 1, unmoved, six relics deep — and §3 above is
   the first measurement of how rare a fatal cut is for a MELEE relic, which is
   the number that rule would be set against.
4. **`01-live` IS NINE RELICS BEHIND.** v27 open decision 1, still the oldest
   open thing in the project.

## Still open, unmoved

- **`tip_audit.py` does not check ult tips.** v40's item 3, v41's, v42's. This
  relic's card carries `9s` and `2s` and `paradox_relic_probe [1]` asserts both
  against the weapon's fields — but that guard lives in one relic's probe and
  not in the shared tool, for the third session running. **And `verify.py`'s
  72-character limit on an ult tip was hit for the first time this session**,
  which is the same gap from the other side.
- **`_burst` DOES NOT LOOP ITS 0.6s NOISE BUFFER** and `_tone`'s frequency
  automation is un-anchored. Both live, both measured, both chain-wide changes
  to twenty-four shipped voices. v43 wrote its voice inside the safe envelope
  rather than fixing either.
- **A HELD WEAPON IS STILL A LEGAL THING TO BIND AGAINST.** 22 binds over 27
  holds. Priced into the +42% and named rather than fixed.
- **EVERY OTHER READER OF `pinV` IS A BUG WAITING.** §10. `_ballPair` was the
  one that existed; the next suspended-state field anybody adds will have its
  own.
- **A kill by ward SHATTER files no beat.** v41's, unmoved.
- **`STATUS.ward.bank 0.55 / cap 90` have never been swept.** Vigil od 4 — now
  with three points on the type axis: the flail banks fine at 1.0, like the
  warhammer and unlike the bow, so Farwarden's 2.5 was a patch for a BOW and
  not for weight.
- **`shot.life: 3.4` is dead config on all five bows** (v40). This session
  refused to add a sixth dead knob — "extra hit stun" was measured inert and
  converted rather than shipped — and that decision is only defensible while
  the existing one is being chased.
- **`cell_survey`'s umbral row is suspect on all six types** (v40 §4.1), and §4
  above is a second cell it has now mispriced.
- **`tickFire` gates on `f.w.shot`, not on mode** (v39 od 4). Still inert; no
  flail carries a `shot`.
- **THE GREATSWORD DEADLOCK IS SIX THOUSANDTHS FROM BEING A WIN.** New. The
  flail is heavier than the greatsword and cannot cash it — 0.1537 against a
  0.16 threshold, 100% deadlocks over 112 binds.
- **A STUNNED GREATSWORD'S BLADE KEEPS TURNING.** New. `mode:"swing"`
  recomputes theta from the AIM every frame, so it is the only type in the game
  whose facing is not an integral of its own spin. Inert for damage, live for
  the picture and for anything measured off `theta`.
- **Every type-level measurement still wants a `--noult` pass** (v38 od 5, v39
  od 5, v40 od 6, v41, v42).

# v42 — HANDOFF. The twenty-fourth relic, and a hole in the director that belonged to seven.

**2026-08-21.** Bloodsworn × bow built, priced before it was built, refuted
once by its own sweep, rebuilt, tuned, filmed.

```
02-chain/sc-marrowdraw.html         <- THE RELIC
02-chain/sc-marrowdraw-frame.html   <- THE BUILD OF RECORD
built off 02-chain/sc-bulwarden.html
01-live UNTOUCHED, still on sixteen

cell_survey            7/7      the grid on the v41 tip — 19 cells open
bow_survey            25/25     the bow row, re-run on 23 relics
marrowdraw_probe      14/14     §1 PRICED BEFORE A BUILDER WAS OPENED
marrowdraw_relic_probe 29/29    one check per sentence of §1, against the build
marrowdraw_sweep        —       cadMul x dmgMul, dmg bisected in every cell
engine_ab         2530/2530     IDENTICAL on the other twenty-three
verify.py --n 40      13/13     Marrowdraw 50.0%, spread 12.2pp, 0/11040 timeouts
chain_audit           15/15     every insert survives to the tip
07-shorts/v42/bloodhunt-v-heartwood.mp4   seed 10158, 25.6s, the window lands
                                          the last blow
```

Read `06-docs/v42/` in this order:

| doc | the headline |
|---|---|
| `sundered-crown-redbow-design-v42.md` | §1 in Rick's words, and **§1 priced before a builder was opened** — homing takes the wall from 82.9% to 21.3%, "larger" is a look knob, and the teeth are in the SPEED. |
| **`README.md`** | The build. **§8 is a sentence of §1 that could not be built as written, §9 is the director being blind to a fifth to a half of seven relics' wins, §10 is three cuts of art and the reference that ended it.** |

---

# RICK'S THREE RULES STILL STAND, AND HERE IS WHERE THEY LANDED

## 1. THE FIGHT CARD IS DEAD

Nothing shipped with one. Still IN the build — `introcard_build.py` writes it,
`m.introT` is on every Match, the guard in `cinema_clip` is what stops it.
**Unmoved for a third session.** v40's sentence is unchanged: *"die completely"
means removing it, and that is a chain-wide change that wants its own session
and its own probe.*

## 2. RICK GIVES INPUT ON SIX THINGS — AND ALL SIX WERE ASKED AGAIN

```
  the ult MECHANICS      §1 in his words, and then THREE FORKS priced from
                         measurement before they were put to him: how hard the
                         bolt hunts (he took "it hunts", 3-4 rad/s), which half
                         carries the bleed, and whether a fork can be batted.
  the ult NAME           Bloodhunt. `quarrel` was ruled out BEFORE the four
                         were offered because Quarrelstorm owns it — the
                         Bulwark trap, caught a step earlier.
  the FIGHTER name       Marrowdraw, from four offered. The id matches.
  the SCRUNCH CARD       "For 8s, fires homing bolts that pierce and fork" —
                         his wording, not one of the four offered.
  the ult ANIMATIONS     three cuts. "cartooney" killed the first, "cartoony
                         ROCKETS" killed the second, and the third was drawn
                         from a reference image he supplied.
  the ult SOUND          FOUR passes, and every one of them moved it.
                         "a sound effect to signify it triggering" FOUND A BUG
                         -- the ult voice called helpers that do not exist and
                         the ultimate had shipped SILENT through every probe in
                         the repo. "a bang followed by a low gutteral growl"
                         set the shape. "the growl frankly sounds like a fart"
                         was correct and mechanical: sawtooths gliding DOWN at
                         a 4.5 Hz beat is the recipe for exactly that. "give
                         the fork its own sound" closed that half. AND THEN
                         "bloodhunt made no sound in that video" FOUND A SECOND
                         ONE -- the rebuilt growl was 97.7% sub-60Hz and
                         inaudible on any real device, certified correct by a
                         check a sine wave could pass. README §12.
                         AND THEN "it sounds like rolling thunder. want me to
                         get you inspiration?" -- which ended it. The reference
                         RECORDING is what fixed the sound, exactly as the
                         reference IMAGE fixed the bolt. FIVE passes, and his
                         ear beat every instrument in the repo three times.
  the BALL's animation   a seventh thing, and his: "piercing red hunters eyes
                         floating above it". README §13.
```

**One of the six answers was refuted by a measurement after he gave it** (the
extra fork bleed, README §8) and **one of them found a bug nothing in the repo
could have found** (the silent ultimate, README §12). Both directions are why
this rule exists.

**And he asked for a seventh thing this session** — an animation on the BALL —
which is not on the list and probably should be. Every window ultimate needs
one; Bloodhunt was the first whose expression lived entirely off the caster,
and it took him watching a clip to notice.

## 3. A HIT-HEAVY ULT MUST DECLARE ITSELF TO THE DIRECTOR

**This session found the biggest instance of it in the game and it is not this
relic's.** `tickStatus` files no beat, so a fight that ends on a bleed tick
carries no fatal beat at all:

```
Dawnbringer  44.1% of its wins invisible     Ironhail    0.0%
Widowmaker   31.1%                           Axiom       0.0%
Threshmaw    26.2%                           Nightfell   0.0%
Lastlight    25.7%                           Bulwarden   0.0%
Marrowdraw   23.8%
Goreshard    20.9%
Aureole      19.4%
```

Every school with a `dps` status is between a fifth and nearly half; every
school without one is exactly zero. **A fatal tick files a beat now; an
ordinary one does not** — the fourth relic to need that exact distinction and
the first time it was chain-wide. Dawnbringer drops to 22.1%, and the residue
is Daybreak's spark burn calling `hurt()` directly.

**The shared `cineFloor` is STILL not built.** v40's first pickup item, still
first, five relics deep.

---

# WHAT v42 ADDS TO THE RULES

## 3f. OFFER A SPREAD, NOT A GUESS — AND KNOW WHICH SOUNDS ARE ATTEMPTABLE

The cast voice took **four** serial round trips as a creature growl and **two**
as a spread. `cast_lab.py` renders N candidate sounds into one file through the
shipping chain; Rick picked a character from six, then a depth from three, and
both landed. When the judge is a person and the author cannot hear, **the cost
of a candidate is nearly zero and the cost of a round trip is enormous** —
render six.

And the class matters more than the effort:

```
  landed on the FIRST attempt   the lock, the fork's split, the ballista
                                string, the ratchet, the iron clamp
  failed FOUR times             one sustained biological voice
```

A percussive sound is an envelope plus a rough band; approximately right still
sounds right. A voice is carried by fine structure over time, its average
spectrum barely constrains it, and approximately right is the uncanny valley.
**Do not attempt voices, breathing or creature vocalisations with this
toolkit.** Impacts, latches, ratchets, springs, whooshes, fire, stone and metal
resonance are all fair game and have a 5-for-5 record.

## 3e. ASK FOR A REFERENCE THREE CUTS EARLIER

The bolt art took three cuts and a reference IMAGE ended it in one. The cast
sound took three cuts and a reference RECORDING ended it in one. Both times the
failing loop was the same: translate an adjective into parameters, render,
guess again. **Rule 2 should say that when a look or a sound misses twice, the
next move is to ask for a reference rather than to try a third adjective.**

A reference is also a SPEC. `growl_lab` measured four growls in Rick's file and
turned "lower rumblier and much longer" into six band shares and a modulation
rate; the fit went from 65.9 points of band error to 6.4.

**AND IT WAS STILL WRONG, WHICH IS THE HARDER HALF OF THE LESSON.** A spectrum
match that close, still rejected, is what finally showed the problem was the
CLASS of sound rather than the parameters -- the missing thing is cycle-to-cycle
jitter and subharmonic chaos, which no band-share metric can see. A reference
narrows a search; it does not make an unattemptable sound attemptable.

## 3d. A BENCH THAT RENDERS AT TIME ZERO IS NOT THE GAME

The growl was fitted on a bench to 19/49/25 and shipped at 12/68/15 -- same
code, same chain. **An AudioParam whose first automation event is at t > 0
holds its constructor default until then** (440 Hz for an oscillator), and
`currentTime` is never 0 in a live match, so the bench was fitting a case that
cannot occur. One line -- `.value = f` before the automation -- makes it stable
across start times, and the probe now renders through a proxy whose
`currentTime` is 1.0 for the same reason.

`_tone` has the identical un-anchored pattern. Measured at 0.4-3.4 points of
band shift across four shipped relic voices: real, immaterial for short sounds,
**and a trap for the next long sustained one anybody writes.**

## 3c. A METRIC A BROKEN OUTPUT SCORES PERFECTLY ON IS NOT A CHECK

The growl passed a check that said *"98.2% of its energy is below 180 Hz —
lower than anything in the game"* while being **97.7% between 20 and 60 Hz in
the finished clip**: as loud as the entire mix and inaudible on any laptop,
phone or earbud. Rick heard nothing and was right.

"Lower" had been encoded as a metric **a 30 Hz sine wave maxes out**, so the
test was passed most convincingly by the exact degenerate answer it existed to
prevent. It is replaced by what a small speaker actually gets — the share of
level surviving a 300 Hz high-pass — where the reference itself reads 44%. **That threshold was
then found to be wrong too** -- 40% would have failed the real growl -- so the
check is now the six-band PROFILE against the reference, which no single
degenerate answer can win.

The general form: when a brief becomes a number, ask what the WORST thing that
scores well on it looks like. If that thing is the failure you are guarding
against, the number is wrong.

## 3b. A SUBSYSTEM THAT IS INERT HEADLESS IS A PLACE BROKEN CODE SHIPS

`SFX.play` wraps its body in a try/catch AND returns on its first line when
there is no audio context, which is every automated run here. A call to a
helper that does not exist therefore looks exactly like a sound that is quiet,
and it passed a 14-check probe, a 29-check probe, a full sweep, a 13/13 verify
and a rendered clip. **The check now RENDERS the sound in an
OfflineAudioContext and measures it**, which catches silence whatever caused it
and turns Rick's brief -- "lower rumblier and much longer" -- into three
numbers with the other relics' voices as controls. Sound is the instance this
project has; it should not be assumed to be the only one.

## 4. A CONTROL THAT SEPARATES CLEANLY IS WORTH MORE THAN A BIG NUMBER

The bleed-out finding took THREE instruments and the first two were both wrong
in ways that looked completely plausible:

1. *"the match ended more than two steps after the last blow"* — measures the
   KILL FLIGHT, which is true of every death in the game.
2. the same idea against the hp crossing, with an off-by-one — **100% for every
   relic including the controls**, which is what exposed it.
3. *"was any beat filed on the step hp crossed zero"* — and four schools came
   back at exactly 0.0%.

**The third one is trustworthy because of the zeros, not because of the 44%.**
Instrument two would have shipped a headline number that was pure artefact.

## 5. A PICK TOOL MUST ASK THE DIRECTOR WHAT IT INTENDS TO DO

v41 open decision 6, **closed**. `marrowdraw_pick.py` runs every candidate
through `window.cinePlan` and rejects any seed whose plan carries no FATAL cut.
Measured on this relic: **24 of the 30 fights that cleared the relic bar had no
KILL cut** and would have rendered as clips with no ending. v41 lost two
renders to exactly that.

## 6. A RENAME CAN EAT AN EDIT, SILENTLY

`dmgMul` was set to 1.6 and stayed 2.2, because the anchor text mentioned a
tool that had been renamed since. **A whole 4600-fight bisection ran at the
wrong value** and was caught only because the builder echoes its settings and
somebody read them. Builders echo what they are about to write; read it.

## 7. A CELL CHOICE PRICED ON FEWER THAN 40 SEEDS IS PRICED ON NOISE

The candidate set was priced on `verify --n 12` and five relics moved by more
than five points at `--n 40`. Spellbreaker went 39.8% → 45.8%, so "the weakest
relic in the game" was an artefact of 264 fights.

---

# THE FIRST FOUR THINGS TO PICK UP

1. **THE TWO REMAINING BEATLESS DEATHS.** §9 of the README. Daybreak's spark
   burn and `_traceHit` both take hp through `hurt()` and file nothing, and
   Dawnbringer is still 22.1% blind. The general fix is one backstop — *if a
   fighter died this step and no beat was filed, file one* — which is a
   CHAIN-WIDE change to how every clip in the game is cut and is therefore
   Rick's call, not a slip-in. It is named here rather than taken.
2. **RULE 3, BUILT PROPERLY.** A measured `cineFloor` and a windowed beat in
   `cinema_build.py`, for every crowding mechanic. v40's item 1, unmoved, five
   relics deep.
3. **KILL THE FIGHT CARD OUT OF THE BUILD.** Rule 1. Chain-wide, wants a probe.
4. **`01-live` IS EIGHT RELICS BEHIND.** v27 open decision 1, still the oldest
   open thing in the project, and now one relic worse.

## Still open, unmoved

- **`tip_audit.py` does not check ult tips.** v40's item 3, v41's. This relic's
  card carries `8s` and `marrowdraw_relic_probe [1]` asserts it against `dur` —
  but that guard lives in one relic's probe and not in the shared tool, for the
  second session running.
- **`chain_audit` cannot resolve a marker whose template carries a `%SUB%`.**
  `SFX_ULT_VOICE_NEW` reports as unresolved on this build and the insert is
  present; the tool says "the marker is wrong, not the chain", which is the
  right behaviour and still a gap.
- **A kill by ward SHATTER files no beat.** v41's, unmoved. Zero occurrences
  measured on this relic.
- **`STATUS.ward.bank 0.55 / cap 90` have never been swept.** Vigil od 4.
- **`shot.life: 3.4` is dead config on all five bows** (v40). This session
  refused to add a sixth dead knob — `forkBleed` was measured inert and left
  out — and that decision is only defensible while the existing one is being
  chased rather than accepted.
- **`cell_survey`'s umbral row is suspect on all six types** (v40 §4.1).
- **`tickFire` gates on `f.w.shot`, not on mode** (v39 od 4). Inert today, and
  this relic came closer to it than anything yet: Bloodhunt rewrites a shot
  after `spawnShot` has made it rather than swapping the block, specifically so
  the trap stays inert.
- **Every type-level measurement still wants a `--noult` pass** (v38 od 5, v39
  od 5, v40 od 6, v41).

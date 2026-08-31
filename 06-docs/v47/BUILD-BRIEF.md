# v47 — BUILD BRIEF FOR CLAUDE CODE. THORNSHEAR and the WINNOWING, priced and ready to build.

**Read `06-docs/v47/twinblade-survey-v47.md` and then
`06-docs/v47/kunai-design-v47.md` before this file.** They carry the
measurements; this one carries only what to do with them.

**The split, in Rick's words on 2026-08-30:** *"lets design and plan here and
let code build it."* Cowork surveyed the type, priced every sentence of §1 and
put four forks to Rick. **You build.** Two instruments are already in `tools/`
and both are runtime-only:

```
tools/twinblade_survey.py    the type, 20/20     — re-run it, do not trust this doc
tools/kunai_probe.py         §1 priced, 11/11    — likewise
```

---

# 0. THE ORDER, AND ITEM 1 IS NOT NEGOTIABLE

**1. FILM IT ON PLACEHOLDER NUMBERS BEFORE YOU TUNE ANYTHING.**

v43 §13 is the most expensive mistake that session made and it cost about
thirty thousand fights. Its rule: *film before you tune, when the ultimate is
a picture.* **This ultimate is more of a picture than the Stasis Field was.**
Nothing about it can be counted into correctness — a kunai that vanishes at the
`maxLive` ceiling, a growth step that does not read on screen, a fan so dense
the hall turns to soup, a ricochet that looks like a teleport at 60fps
interpolation — every one of those passes every probe in this repo and is
visible in half a second of clip.

**Thirty seconds of clip on placeholder numbers costs four minutes.** Do it
before the sweep, not after.

**2.** Re-run both instruments at the tip. If any number in the design doc has
moved, the design doc is wrong and it is yours to say so.
**3.** Build. **4.** Probe. **5.** Sweep and bisect. **6.** Film properly.
**7.** Rick's four remaining inputs — name, ult name, card, art and sound
spreads.

---

# 1. THE CHAIN

```
built off   02-chain/sc-paradox-ignition.html      <- the build of record, 25 relics
builder     tools/thornshear_build.py              <- new
produces    02-chain/sc-thornshear.html            the relic alone
            02-chain/sc-thornshear-frame.html      the tip
probe       tools/thornshear_relic_probe.py        <- new, one check per sentence of §1
sweep       tools/thornshear_sweep.py              <- new
id          thornshear   —  the id matches the name, as it does on all 25
01-live     UNTOUCHED. Still on sixteen. Not a target.
```

`chain_audit.py --builder thornshear_build.py` after every carry. **It defaults to
`twinshade_build.py` and will happily audit the wrong inserts and pass** — and
in v43 its regex could not see `r'''`-prefixed inserts at all and printed *"no
*_NEW inserts found"*, which reads like a pass in a hurry.

---

# 2. WHAT IS SETTLED

**The cell:** verdant x twinblade. Rick's, from four priced candidates.

**The names:** the fighter is **THORNSHEAR**, the ultimate is **THE
WINNOWING**, both Rick's from four offered each. The id is `thornshear`.
Lastlight's ult is the Harrowing and the -ing collision was flagged to him
before he chose; it is settled, not open.

**The block** is the type's, byte for byte, like every other relic in its row:

```
reach 62   width 8   spin 5.7   mass 1.1   blades [0, 0.5]   mode spin
onHit entangle:2                            (the school's, byte for byte)
dmg <BISECTED — see §5>
```

**The ultimate**, with the settled numbers and the ones the sweep decides:

```
kind        winnow       a firing window, blades suppressed
charge      15-17        the roster band; sweep it with dur
dur         ~4.0s        SWEEP — the window
cadence     SWEEP        see §5.1: the fan is a look knob, the cadence is not
fan         LOOK KNOB    §5 of the design doc — Rick picks it from a render
spread      LOOK KNOB    likewise
speed       ~420         sweep lightly; 260 cost 4% of connections
life        3.0 or 6.0   THE REAL CONSTRAINT — see §3.2
bounce      3            above 3 is INERT at life 3.0
r           ~10 base     grows per rung
knock       260          RICK'S, from a priced spread of five
dmgMul      1.0 base     grows per rung
```

**Rick's two decided forks:**

- **A parry deflects AND empowers.** A blade that bats a kunai must ricochet it
  and advance its rung, not kill it. This is a change to the parry branch of
  `tickShots`, which today sets `dead = true`.
- **Knockback 260**, flat, from a spread of 0 / 120 / 260 / 420 / 700.

---

# 3. THE FOUR THINGS THAT WILL BITE

## 3.1 `spawnShot` DELETES A LIVE KUNAI AT THE CEILING

```js
if (this.shots.length >= CONFIG.shot.maxLive) this.shots.shift();
```

`maxLive` is 64. On a bow this is invisible. **On a bouncing kunai it is one
vanishing in mid-air** — no error, no invariant broken, no win rate moved, and
only a person watching can see it. That is v42's silent ultimate and v43's
stuck hold for a third time, and unlike both of those it is *foreseen*.

**DECLINE, do not shift.** The Bloodhunt fork branch already does exactly this
and says why. And **file the refusal count** — the probe should assert the
shipping fan never saturates in normal play, because a design that is
permanently at the ceiling is a design whose cadence is decided by a constant
in `CONFIG`.

## 3.2 THE THIRD RUNG IS THE LAST ONE, AND `life` IS WHY

Each bounce costs 12% of speed (`s.vx *= 0.88`), so at life 3.0 **nothing
reaches a fourth bounce** — `bounce 6` and `bounce 3` return identical numbers,
digit for digit. If the growth schedule wants four rungs, `life` goes up; that
is a picture decision (kunai stay in the hall visibly longer) as much as a
balance one, and it belongs in the sweep with both arms rendered.

## 3.3 `shot.life` AND THE `w.shot` MODE GATE ARE BOTH WAKING UP HERE

`tickFire` gates on `f.w.shot` and not on mode (v39 od 4, inert six sessions).
`shot.life: 3.4` has been dead config on all five bows since v40 — *"a shot
travels 1292 units in its life and the longest wall is 800, so `life` has never
once expired in this game."* **A bouncing kunai's modal death is expiry, at
34.3%.** Both knobs become load-bearing in this one ultimate. Treat anything
either of them touches as untested code, because it is.

## 3.4 A RICOCHET MUST NOT TWEEN THROUGH A WALL

`s.snap = true` exists on the wall-bounce branch for exactly this — *"the
interpolator must not tween through a wall."* Every new reflection path this
build adds (the parry ricochet above all) must set it, and the probe must
assert it, or a kunai at 60fps will cut the corner it just bounced off.

---

# 4. THE PROBE — ONE CHECK PER SENTENCE OF §1, AGAINST THE BUILD

`tools/thornshear_relic_probe.py`. `kunai_probe.py` priced the sentences before the
build; this one asserts them against it. At minimum:

1. **The blades really are gone during the window** — `bladeSegments` returns
   empty, `tickHits` lands nothing, `_clankPair` files no bind, and all three
   come back the frame the window ends.
2. **The fan looses from both bearings**, and the two bearings are the two
   entries of `w.blades` rather than a second copy of them.
3. **The ceiling is never reached in normal play**, and if it is, the loose is
   DECLINED and counted — never shifted. Assert `m.shots` never loses an
   element that was not resolved.
4. **A kunai's rung advances on a wall AND on a parry**, and on nothing else.
5. **The growth reaches the numbers**: radius, damage and knockback at each
   rung read what the config says, measured off landed hits rather than
   computed.
6. **A parried kunai survives** and its rung went up — Rick's fork, quoted in
   the check.
7. **`s.snap` is set on every reflection**, both kinds.
8. **A lethal kunai does not keep bouncing.** `foe.alive` is tested after
   `resolveHit` in the fork branch for the neighbouring reason; a corpse should
   not be a wall.
9. **A hold/hit on a Twinshade COPY must not advance a rung** — v43 §11 caught
   exactly this one frame in six thousand. `!foe.shade`.
10. **THE SOUND IS RENDERED AND MEASURED IN AN OfflineAudioContext.** `SFX.play`
    returns on its first line headless and swallows its own exceptions; v42
    shipped a silent ultimate through every green check in the repo. A growth
    ultimate needs a per-rung sound, so there are three or four voices here and
    every one of them must be rendered and measured, not played.
11. **The ult files a BEAT for the director.** Rule 3, sixth relic running. The
    kunai land through `resolveHit`, so ordinary hits file themselves — but the
    RUNG-UP is the legible moment of this ultimate and nothing else in the frame
    knows it happened.

**And `_burst` still does not loop its 0.6s noise buffer, and `_tone` is still
un-anchored.** Both live, both chain-wide, both Rick's call. Write this relic's
voice inside the safe envelope like v43 did: every burst under 0.6s, sustain
carried by `_tone`.

---

# 5. THE SWEEP, AND WHAT IT IS ACTUALLY CHOOSING

`thornshear_sweep.py`. **Bisect `dmg` against all 25 opponents in every cell before
reading that cell's telemetry** — otherwise the grid compares relics of
different strength and reports it as a mechanic (v43 §6).

**Do not sweep the fan.** Design doc §5: a nine-fold range of fan width lands
within x1.17 of itself, because the coverage comes from the weapon's own 6.47
rad/s. The fan is a look knob and it is Rick's, from a render.

**Sweep, in order of measured leverage:** `bounce` x `life` (the +78% and the
three-rung ceiling), the growth schedule (how much per rung), then `dur` x
`charge`.

**Two cheap wins nobody has taken yet** (v43 §14.1, unmoved):

- **A bisection should ESCALATE its sample.** Spending 960 fights on step one,
  where the interval is 12 damage wide and the answer is obvious, is the same
  cost as step seven where it is 0.1 and the answer is the point. ~100 rising
  to ~960 halves the cost of every bisection in this repo for no loss of
  precision.
- **Nothing in `tools/` is parallel.** One browser, one thread. Every tool
  already takes its seeds as a list.

**The framing that should make the sweep decidable**, the way v43's did: the
bisection compensates, so the pair does not choose how hard this relic hits.
**It chooses how much of the relic IS the growth** — what share of a cast's
damage is carried by kunai on their second and third rungs, against the share
carried by fresh ones. That is the number to put to Rick, not a win rate.

---

# 6. THE GATES

```
engine_ab       IDENTICAL on the other 25 in any match with no cast in it
chain_audit     --builder kunai_build.py, every insert survives to the tip
verify --n 40   12000 fights; the thirteenth check (duration band) is KNOWN
                to fail at the tip — do not credit this relic with it and do
                not credit yourself with fixing it by accident
tip_audit       and verify's 72-character ult-tip limit, hit for the first
                time in the project in v43
frame_probe
post_identity   the picture is unchanged where the ult is not running
```

**And the registered prediction from the design doc §9, which is this build's
job to falsify:** *this relic's win-rate spread across the roster will be the
widest of any relic in the game, strongest against the seven greatswords and
weakest against the five bows* — because entangle is worth -33.1% against a
swinging foe and +3.3% against a bow, and now a parry (swing 28.7%, ranged
14.1%) empowers the ultimate as well. **If the finished spread sits inside the
existing band, the prediction was wrong; say so and strike the concentration
argument rather than explaining it away.**

---

# 7. WHAT NOT TO DO

- **Do not add homing.** Rick amended §1 specifically: *"the kunai ricochet
  shouldnt be steering. natural and predictable ricochet physics."* `s.home`
  exists and works; leaving it at zero is the design.
- **Do not build the fan as new machinery.** `spawnShot(f, angle)` already
  takes the angle.
- **Do not fix `spawnShot`'s shift for everyone.** Quarrelstorm looses 14 at
  once and Ironbloom 9; both still shift. Chain-wide, and Rick's.
- **Do not touch `01-live`.** Nine relics behind and not a target.
- **Do not fix `_burst` or `_tone`.** Twenty-five shipped voices.
- **Do not let the fight card back in.** Nothing ships with one, four sessions
  running.

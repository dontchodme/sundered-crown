# v40 — HANDOFF. Three standing rules from Rick, and where this is.

**2026-08-20.** Twenty-second relic built, tuned, filmed. **A posting cut
exists**, which v39 did not have.

```
02-chain/sc-vinesower.html         <- THE RELIC
02-chain/sc-vinesower-frame.html   <- THE BUILD OF RECORD
built off 02-chain/sc-foregone.html
01-live UNTOUCHED, still on sixteen

bow_survey          25/25    the four open bow cells, before the choice
verdant_bow_probe    7/7     the chosen cell, deep
vinesower_probe     38/38    one check per sentence of §1, plus the camera
vinesower_sweep      4/4     staged; the runtime override proved against a rebuild
engine_ab       2100/2100    IDENTICAL on the other twenty-one
verify.py --n 30    13/13    Vinesower 50.3%, spread 15.9pp, 0/6930 timeouts
chain_audit         18/18    every insert survives to the tip
07-shorts/v40/vinesower-v-grudgebearer.mp4   seed 3928777967, 45.0s, won on 3%
```

---

# THE THREE RULES. These are Rick's, verbatim, and they outlive this relic.

## 1. THE FIGHT CARD IS DEAD

> *"the videos keep coming through with the old fight cards and cold open. id
> like the fight cards to die completely. they have been replaced with the
> scrunch and thats the only thing id like to see going forward."*

**Done, and enforced rather than remembered.** `cinema_clip.py --intro` and
`--cold-open` now **refuse to run** without `--legacy-card`. That guard exists
because the card came back three separate times in this session alone, every
time from a command copied out of a doc — a flag that merely defaults off is a
flag that returns.

**WHAT IS NOT DONE.** The card is still IN the build. `introcard_build.py`
still writes it, `intro_probe.py` still tests it, `newrelic_sheet.py` still
renders it, and `m.introT` still exists on every Match. It is opt-in and
nothing ships with it, so nothing is broken — but "die completely" means
removing it, and that is a chain-wide change touching every relic and the live
build. **It wants its own session and its own probe.** Do not bolt it onto a
relic build.

## 2. RICK GIVES INPUT ON SIX THINGS. IF HE HASN'T, ASK — WITH OPTIONS.

> *"i would always like to give input on the following things when we build:
> the ult mechanics, the ult name, the fighter name, the wording on the scrunch
> card, the ult animations, the ult sound effects. if i dont offer them that
> means i want you to give me options to choose from."*

```
  the ult MECHANICS        §1 in his words. Already the rule since v38.
  the ult NAME
  the FIGHTER name
  the wording on the SCRUNCH CARD    <- never been asked about. It is
                                        `ult.tip` and `onHit` tips today, and
                                        both have been written unilaterally on
                                        all twenty-two relics.
  the ult ANIMATIONS       the set-piece AND the mechanic's own art
  the ult SOUND EFFECTS    the `SFX.play("ult", {w: id})` voice and any
                           per-mechanic voice the relic adds
```

**"Options" means real ones with the trade named** — the naming ask in this
session offered four candidates each with the register it borrowed from and
what it cost, and Rick took none of them and gave a better word (Vinesower,
which names both the act and what grows; every one of mine named only one).
That is the point of offering rather than deciding.

**This was under-served in v40.** Six things on that list, and he was only
asked about two of them (the mechanic, then the names) — the tip wording, both
sound designs and all the animation went in without a question. Do better.

## 3. A HIT-HEAVY ULT MUST DECLARE ITSELF TO THE DIRECTOR

> *"when we build ults that produce lots of hits we need to tell the director
> not to register those as cinematic moments. the director should be forewarned
> that this ult should only trigger a cinematic if it produces significantly
> more hits than it normally would"*

He caught this off a clip. The measurement, once it was looked for:

```
                  beats  hit beats  lashes   cuts  volley cuts
guard live          451        274     436     12            6
guard defeated      884        707     436     27           24
```

**61% of the hit beats this relic handed the director were its own vines, and
24 of its 27 cuts were volleys they had manufactured.** The camera was filming
the garden instead of the fight.

### What v40 shipped, and why it is only half the ask

`_cineVine` is a **blanket** suppression: a lash files no beat at all, except a
fatal one. It is set around the vine's own `resolveHit` exactly the way
`_cineShot` is set around a projectile's. It works and it is measured.

**But Rick asked for a THRESHOLD, not a mute.** *"only trigger a cinematic if
it produces significantly more hits than it normally would."* A vine flurry
that is genuinely four times the usual is a cinematic moment and this build
throws it away.

### The generalisation, for whoever picks this up

Every hit-heavy mechanic should declare a floor, and **the floor should be
MEASURED, not chosen**:

1. The relic's probe already counts hits-per-window for its own mechanic.
   Have it write the **distribution**, not just the mean.
2. The ult block carries `cineFloor` = a high percentile of that distribution
   (85th is a reasonable first guess and should itself be swept).
3. `beat()` takes an optional `src` tag. Beats carrying a tag are held in a
   rolling window rather than filed; when the count in the window crosses
   `cineFloor`, the whole burst is filed **as one beat** with `n` set — which
   is what `kind:"volley"` already is, and the director already prices `n`.
4. Below the floor: nothing. Above it: one cut, correctly sized.

**This is a `cinema_build.py` change, not a relic change**, and it should land
with `director_diag` numbers on Bloodmill and the Thicket both — v39's handoff
already warned that `director_diag`'s window predicate has been generalised
three times and still has no shared field to hang on. This is the fourth
crowding mechanic. **It is time to build the shared thing.**

---

# WHERE THE RELIC IS

**VINESOWER**, verdant × bow, the twenty-second relic. Rick's name, against
four of mine, and better than all of them: it names the ACT (sowing, which no
other relic does) and what GROWS (the vine, which is the part that fights).
The id matches the name — `oathwound`/Goreshard and `redflail`/Threshmaw are
the two existing drifts and a third was not worth saving twenty minutes on.

```
dmg 15.6   reach 54   spin 2.8   mass 1.6   mode ranged   onHit entangle:2
THICKET  charge 15   seeds 8   sprout 1.0   vineLife 9.2   maxVines 10
         reach 205   turn 5.2rad/s   aware x1.7   windup 0.20s
         whipDmg 2   whipCd 1.4   whipKnock 260   lash 0.30s
```

Read `06-docs/v40/` in this order:

| doc | the headline |
|---|---|
| `sundered-crown-bow-survey-v40.md` | **82% of every arrow this game has ever fired ends on a wall**, the type's own thesis is true and had never been tested, and curse delivers ZERO on this type while `cell_survey` ranks umbral best-in-game everywhere. |
| `sundered-crown-quickset-design-v40.md` | §1 in Rick's words. Nothing started before it existed. (Filename still says quickset; the relic was renamed after it was written.) |
| **`README.md`** | The build. **§4b is the camera, §4c is the three notes off the second clip** — and both are things Rick caught that no probe here was looking for. |

---

# THE FIRST FOUR THINGS TO PICK UP

1. **RULE 3, BUILT PROPERLY.** A measured `cineFloor` and a windowed beat, in
   `cinema_build.py`, for every crowding mechanic — not one `_cineVine` per
   relic. Four relics now need it.
2. **KILL THE FIGHT CARD OUT OF THE BUILD.** Rule 1. Guarded in the clip tool,
   still present in the engine. Chain-wide, wants a probe.
3. **`tip_audit.py` DOES NOT CHECK ULT TIPS.** v40 shipped a card reading
   "5s" after a sweep moved the number to 8.1, and nothing caught it —
   `verify.py` only asks that a tip EXISTS. One relic is fixed by hand;
   **twenty-one are unaudited.** And per rule 2 the tip wording is Rick's call
   and has never once been put to him.
4. **`01-live` IS SIX RELICS BEHIND.** v27 open decision 1, still the oldest
   open thing in the project.

## Still open, unmoved

- **The garden reaches 67% of the hall** (README §4c). "Good but limited range"
  is the clause of §1 most under strain; 130 reach / 12 seeds held the read at
  51% if the count is allowed back up.
- **Entangle on the whip is mine, not Rick's** — a consequence of routing
  through `resolveHit`, and the largest thing in the relic §1 did not ask for.
- **A fatal lash still files a beat**, which is a deviation from rule 3 as
  stated. 30% of this relic's kills are landed by a vine and they would
  otherwise carry no KILL cut.
- **No VO.** `cinema_vo.SPOKEN` has no entry for "Vinesower" or "Thicket",
  both compounds Kokoro runs into one cluster, and the 338 MB models are not in
  the tree (`FETCH-KOKORO.md`, two curls).
- **`shot.life: 3.4` is dead config on all four bows.** A seed uses 11% of it.
- **`cell_survey`'s umbral row is suspect on all six types.**
- Every type-level measurement still wants a `--noult` pass (v38 od 5, v39 od
  5, v40 od 6).

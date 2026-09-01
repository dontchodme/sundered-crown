# v56 — BUILD BRIEF FOR CLAUDE CODE. SHROUDMAUL, the 28th relic, and its ultimate GRASP. Four separable stages, and the first one is a one-string rename that has to land before anything else is named.

**Read `06-docs/v55/warhammer-curse-v55.md` (the cell), then
`06-docs/v56/grab-v56.md` (the ultimate, priced), then `06-docs/v55/charge-v55.md`
(why charge is 15 and not derived) before this file.** They carry the
measurements; this one carries only what to do with them.

**The split, Rick's:** Cowork designs and prices, Code builds. Two instruments
are already in `tools/`, both runtime-only, neither writes to a build:

```
tools/wh_curse_survey.py   the pool at weight, six types      5/6 — one is a recorded refutation
tools/grab_lab.py          the ultimate, 14 arms at n=702     the whole design
```

```
SHROUDMAUL   umbral x warhammer. The two thinnest lines in the grid crossed
             here; filling it puts umbral on 4 of 6 types and the warhammer on
             4 of 7 schools.
GRASP        a window; the artifact grows ONE large skeletal hand, tethered,
             that reaches out and closes on the foe every 0.6s inside 200
             units. A grab deals nothing, applies nothing, and locks the
             weapon for 0.5s. The FIFTH grab is a true stun of 2.0s — and the
             hand dissipates on it.
```

---

# 0. THE STAGES — WHERE TO START, WHERE TO STOP, AND WHAT MUST BE GREEN BETWEEN

```
 #    IN                        OUT                      WHAT CHANGES
 1    sc-nightfell.html         sc-revenant.html         Gravemourn's ultimate is
                                                          renamed Grasp -> Revenant.
                                                          ONE STRING. Nothing else
 2    sc-revenant.html          sc-shroudmaul.html       the 28th relic exists, its
                                                          ultimate STUBBED at
                                                          charge 1e9. Blade 23.5
 3    sc-shroudmaul.html        sc-grasp.html            GRASP — the hand, the window,
                                                          the grabs, the true stun
 F    --                        --                       FILM. Before you tune
 3b   sc-grasp.html             sc-grasp.html            blade bisected — AND SEE §3.4,
                                                          it may not need to move
STOP
```

**GREEN BEFORE THE NEXT STAGE STARTS**

```
after 1   engine_ab IDENTICAL on all 27 — a name is not read by the sim, and if
          this moves a single bit, THAT is the finding and it stops the stage
          tip_audit passes; every doc, VO script and tool string that says
          "Grasp" about Gravemourn is found and changed in the same commit
after 2   engine_ab IDENTICAL on the 27 in every match not containing Shroudmaul
          verify --n 40 completes with 28 relics
          the roster sheet, the picker and the intro card all FIT 28 — nothing in
          the game hardcodes a count, but three tools lay out grids
          Shroudmaul with no ultimate lands near 27% (grab_lab's floor)
after 3   grasp_relic_probe 12/12 (§5)
          engine_ab IDENTICAL on the 27 in any match containing no cast
          held seconds a fight is 6.5-7.0 — the scalar the whole design is on
after 3b  Shroudmaul inside the field band; umbral's four re-swept
```

**IF A GATE IS RED, STOP AND REPORT.** Stage 1 is thirty seconds of work and it
exists as its own commit for one reason: it is the only stage in this build
that can be proven inert, so if `engine_ab` is not bit-identical after it, the
problem is in the harness and not in the relic — and you want to know that
before three stages of new objects are in the world.

**FILM BEFORE YOU TUNE.** v43 §13, and v54 §2c is the reason it is not
optional: Deadfall's arming state was invisible at alpha 0.16 and no probe in
this repo could have said so. This ultimate has THREE states that must read
apart — reaching, holding, and the crush — and it does no damage, so **the art
is the only evidence on screen that the ultimate is happening at all.**

**STOP AFTER 3b.** Naming is done (§7). The intro-card copy is Rick's.

---

# 1. THE CHAIN

```
built off   02-chain/sc-nightfell.html            <- the build of record, 27 relics
builders    tools/revenant_rename.py              <- new, STAGE 1
            tools/shroudmaul_build.py             <- new, STAGES 2 and 3
produces    02-chain/sc-revenant.html             stage 1 alone
            02-chain/sc-shroudmaul.html           stage 2 on top
            02-chain/sc-grasp.html                stage 3 on top
probes      tools/grasp_relic_probe.py            <- new
sweep       tools/shroudmaul_sweep.py             <- new
            tools/umbral_sweep.py                 <- EXISTS, extend to four relics
01-live     UNTOUCHED. Not a target.
```

`chain_audit.py --builder shroudmaul_build.py` after every carry. **It defaults
to `twinshade_build.py` and will happily audit the wrong inserts and pass.**

---

# 2. STAGE 1 — GIVE GRAVEMOURN BACK REVENANT

Rick named it Grasp at build time over the v51 brief's REVENANT, then gave it
back so the grabbing word is free for the relic that grabs. Gravemourn's hands
fly and punch; they do not grab. Revenant — *that which comes back* — is what a
hand that takes a memory, deals it and re-parks it actually does.

```js
ult: { name: "Revenant", ... }        // was "Grasp"
```

The tip is unchanged: `"Lengthens the chain; every hit throws a cursed hand"`
says nothing about grasping and stays at 51/72.

**GREP WIDER THAN THE BUILD.** `grasp_price.py`, `06-docs/v53/grasp-build-v53.md`
and any VO or hook script that names the ultimate. Docs are history and stay as
written — but anything a RUNNING TOOL reads, or that a viewer could hear, moves.
`cinema_vo.py` and `hook_vo.py` both pull ult names.

---

# 3. STAGES 2 AND 3 — SHROUDMAUL, AND GRASP

## 3.1 Rick's §1, verbatim

> *for a duration the artifact grows an etherial skeletal hand that reaches out
> and grabs nearby enemies. the grab does no damage and doesn't apply curse but
> it does apply massive hit stun. if it grabs several times in one trigger (2-6
> depending on balance) it true stuns for extra duration and then dissipates.*

## 3.2 The relic

```
id          shroudmaul       Rick's, from a spread of four
aff         umbral           onHit { curse: 1 }, like the school's other three
shape       warhammer        `_whEaten` ALREADY EXISTS and is already the umbral
                             branch — 78.6% distinct from its nearest sibling,
                             3rd most distinct of the fifteen open cells. THE
                             SILHOUETTE IS NOT NEW WORK
dmg         23.5             Grudgebearer's, as a start. See §3.4
reach/mass  the warhammer's. Do not invent a fourth set
```

## 3.3 The ultimate

```
name        GRASP        Rick's. Freed by stage 1 and unusable before it
kind        "grip" (new). NOT `freeze` — freeze is the Crucible's and Rootfast's,
                         and the engine already says a second hold would make two
                         relics the same one. This is not a freeze: it is a
                         repeated, zero-damage, EARNED hold
charge      15           v55b: charge was never derived for anybody and 15 is the
                         roster's mode. Unlike every other relic in the chain a
                         longer charge does NOT make this ultimate stronger — the
                         hold does not scale with anything that accumulates
dur         8.0s         the window
radius      200          MEASURED OPTIMUM, and the one number that is not free:
                         140 costs 2.7 points and 300 costs 4.0 AT THE SAME HELD
                         SECONDS. A hold is only worth what the hammer can reach
cadence     0.6s         FREE. 0.3 to 1.3 all inside noise
grabStun    0.5s         per grab. Writes `f.stun`. NOT `takeHitstun` — §4.1
n           5            grabs to the true stun. +24.9%; n=4 is +20.4% and the two
                         are inside one SE, so 3b settles which
trueStun    2.0s         AND IT IS A REGISTERED TRUE-STUN SITE — §4.2
endOnTrue   true         "then dissipates". Worth -10.8 points and it is the
                         balance clause, not a cost — §3.5
ult.dmg     0            the cast opens the window and resolves nothing
apply       NONE         no damage, no curse. Rick's, and measured: the ultimate
                         has no relationship to the pool and that is deliberate
pin         NEVER        `f.pin` is the Stasis Field's only exclusive verb and it
                         is worth -3.3 points here at identical hold — §4.5
blade       23.5 -> BISECT, and see §3.4
tip         "Grabs repeatedly; the fifth grab is a true stun, then it fades"  (62/72)
```

## 3.4 THE BLADE MAY NOT NEED TO MOVE, WHICH HAS NOT HAPPENED IN THIS CHAIN BEFORE

```
Shroudmaul with no ultimate, blade 23.5      27.1%
Shroudmaul with GRASP at n=5                 52.0%        field 50.0%
```

The §1 arrived correctly sized. **Sweep the blade anyway and plot it** — the
lab is Grudgebearer standing in, with Grudgebearer removed from the foe field
and its own Crucible suppressed, and the real relic is a 28th body in a field
that still contains Grudgebearer. But start the bisection at 23.5 and expect a
small move, not the 44 -> 24 of stage 2 last time.

**And unlike the last three builds the bisection surface here is SIMPLE.** `dmg`
moves the blade and the pool; it does NOT move the ultimate, because the
ultimate carries no damage and reads nothing. v51 §4.5's superlinear warning
does not apply. The one knob that moves the ultimate is `n`.

## 3.5 THE WHOLE ULTIMATE IS ONE SCALAR, AND THIS IS THE MOST USEFUL THING IN THE BRIEF

Fourteen arms at 702 fights each, regressed on total seconds the foe is held:

```
lift = +3.1 + 2.62 x held seconds     r2 = 0.79
residual sd 2.7pp against a per-arm SE of 5.3pp
```

**The residuals are smaller than the measurement error.** Window length, grab
cadence, grab hold, true-stun length, grab count and whether the window
survives its own payoff are six ways of writing one number. So:

- **Tune on `held`, not on win rate.** It is 30x cheaper to measure and it is
  what the win rate is made of. `grasp_relic_probe [11]` reports it.
- **The arrangement is free.** Any shape delivering 6.5-7.0 held seconds is
  worth the same, so every remaining choice can be made for the picture.
- **Do not try to buy value by lengthening the true stun.** It is on the line
  like everything else: "grabs only, no true stun at all" is +22.9% at 6.2s and
  n=6 is +26.2% at 7.0s. The escalation earns its place as a rhythm and as a
  picture, not as a payload.

---

# 4. THE SEVEN THINGS THAT WILL BITE

## 4.1 `stunDR` MUST NOT BE IN THIS PATH — AND IT IS THE EASIEST WAY TO BUILD THIS WRONG

`takeHitstun` caps at `stunMax` 0.26s and each application divides the next by
`1 + 0.55 x stunDR`. **Route the grabs through it and the second grab onward is
eaten**: five grabs become one grab and a rumour, the mechanic still "works" by
every invariant, no probe fails, and the symptom is a `held` column that does
not move when the knobs do.

The grabs write `f.stun = Math.max(f.stun, 0.5)` directly, exactly as
`u.freeze` does. That is also why "massive hit stun" in the §1 is not
`takeHitstun`: nothing routed through that function can be massive.

## 4.2 THE TRUE STUN IS AN APPLICATION SITE, NOT A DURATION

Rick's own rule, already in the engine: *"Hitstun shouldnt stop the windup. but
true stuns from ults/abilities should."* There is no flag — every source writes
the same `f.stun` — so the distinction is drawn at the **application sites**,
and there are exactly three: hex, `u.freeze`, and the Harrowing's burst.

**This build makes it four, and only the FIFTH grab joins the list.** The four
ordinary grabs delay a wind-up and do not cancel it; the true stun cancels.
Add the site to the same list the engine comments enumerate, in the same
comment, so the count stays nameable — a viewer can learn who shuts a wind-up
down, and that is a property the project deliberately kept.

**The lab never measured this half.** Every arm above writes `f.stun` from an
unregistered site, so the whole table is hold duration only. The wind-up-cancel
half touches the Crucible, Bloodmill and Reprisal and is worth an unknown
amount. Expect the built relic to read slightly stronger than the doc and
re-bisect rather than arguing with it.

## 4.3 A ZERO-DAMAGE ULTIMATE CANNOT FILE A FATAL BEAT — AND MIGHT FILE NONE

v53 §4: 30 of 58 Gravemourn kills rendered a clip with no killing blow, because
a hand filed `kind:"ult"` and `cinema_clip` finds the finish with
`plan.find(c => c.fatal)`. **This relic is worse placed.** It does no damage
ever, so nothing about it can be fatal — and if the grabs file no beat, the
director cannot see the most visually distinctive thing in the fight happen.

Rule 3, ninth relic running: **the cast files a beat, and the true stun files
its own.** The ordinary grabs should not — "do not let small hits drive the
camera" — which is the Thicket's `_cineVine` rule exactly.

## 4.4 THE HAND HANGS OFF THE FIGHTER. NOT OFF `m.ultFx`.

v54 §2a, now a chain-wide open item: `m.ultFx` is a single field on the match
and the opponent casting **anything** overwrites it, after which that cast's
own shorter `life` nulls it. Ironhail's 1.3s Quarrelstorm leaves an
eight-second window with no art for 100% of its frames.

Deadfall survived only by being rebuilt onto `f.ultDeadfall`. **This one has to
start there**: `f.ultGrasp` and `f.graspFade`, drawn by one function called
twice, the shape of `drawVines(m, false/true)`. And set `atSelf` on the fx spec
(v54 §2b) — `drawUltOver` puts a `burst` field at the QUARRY, which is right
for a nova and wrong for a thing that grows out of the caster.

## 4.5 DO NOT WRITE `f.pin`

Measured: stun+pin is **-3.3 points against stun alone at identical held
seconds**, consistent with the reach result — a pinned ball cannot be knocked
toward the wielder, and this relic needs the foe to arrive. `f.pin` is also
written by exactly one relic in the game and that exclusivity is worth more
than nothing.

The picture follows the mechanic here rather than fighting it: **the hand grips
the WEAPON, not the ball.** That is what `f.stun` models and it is what the
frame should show.

## 4.6 FOE ONLY, AND TWINSHADE IS THE TEST

"grabs nearby enemies" is plural in a 1v1 game — except against Triplicate,
where there are three bodies for six seconds. A hand that grabs a shade spends
a grab on a copy that is about to expire, and `tickShadeHits` is where v51
§4.3's bug lived. **Decide the rule, write it in the comment, and assert it.**

## 4.7 PER-FIGHTER STATE, AND NOTHING IN FLIGHT AT THE END

One hand, tethered, owned by a fighter — so not `shots` (`spawnShot` shifts the
oldest live entry out at `maxLive` 64) and not the match. It must be discarded
on death, on `m.over`, and when the window closes, and no grab may resolve on a
corpse. And the window logic must not run while `m.hitStop > 0`: the sim is
frozen and so is the hand.

---

# 5. THE PROBE — ONE CHECK PER SENTENCE

`tools/grasp_relic_probe.py`:

1. **The window opens on the charge and closes on `dur` or on the nth grab**,
   never otherwise, and never twice at once.
2. **Exactly `n` grabs to a true stun**, counted off the engine's own events
   rather than recomputed from the config.
3. **A grab does not touch `stunDR`.** Read it before and after. §4.1.
4. **The true stun cancels a wind-up and an ordinary grab does not** — run it
   against the Crucible's forge, Bloodmill's spin-up and Reprisal, which are
   the three wind-ups in the game.
5. **No grab deals damage and none applies curse.** `foe.hp` unchanged across a
   grab, and the curse pool identical in length and entries before the cast and
   after the window closes.
6. **Foe only** — asserted in a Twinshade match, §4.6.
7. **No grab resolves after `m.over` or on a corpse.**
8. **The hand is per-fighter** — cast Shroudmaul, then run six other-relic
   matches AFTER it in the same page session and assert nothing of theirs
   moved. This is `gravemourn_relic_probe [9d]`'s pattern and it is the check
   that would have caught the `w.reach` hazard.
9. **`f.pin` is never written by this relic**, in any match. §4.5.
10. **The ult files a BEAT and the true stun files its own**; the four ordinary
    grabs file none. §4.3.
11. **`held` seconds a fight is 6.5-7.0**, which is the scalar the entire design
    is priced on and the number to tune against. Report it every run.
12. **THE SOUND IS RENDERED AND MEASURED IN AN `OfflineAudioContext`.**
    `SFX.play` returns on its first line headless and swallows its exceptions;
    v42 shipped a silent ultimate through every green check in the repo. Three
    voices here — the hand growing, a grab closing, the crush. Render all three.

---

# 6. THE GATES

```
engine_ab      IDENTICAL on the 27 at stage 1 (all matches) and at stages 2-3
               (matches containing no Shroudmaul cast)
chain_audit    --builder revenant_rename.py / shroudmaul_build.py
verify --n 40  completes with 28; the duration-band check is KNOWN to fail at
               the tip — do not credit this build with it either way
tip_audit      Grasp's tip 62/72; Revenant's name changed and its tip unchanged
row_price      umbral x warhammer now filled; re-run the row
frame_probe / post_identity
roster fit     28 relics through the roster sheet, the picker and the intro card
```

**Registered prediction, this build's job to falsify:** *at `n` 5, radius 200,
window 8.0, grab 0.5 and true 2.0, the built relic delivers 6.5-7.0 held
seconds a fight and lands within one SE of +24.9% over its own no-ultimate
floor; and the blade bisects to somewhere in 21-23.5 rather than moving far.*
If `held` comes out in band but the win rate does not, the held-seconds law is
an artefact of one relic and every knob has to be re-priced separately.

---

# 7. THE ART — AND IT IS THE ONLY EVIDENCE THE ULTIMATE HAPPENED

Rick, unprompted, in the §1: *"this ult will need a unique animation for the
hand, the reaching and grabbing, as well as a unique animation for the true
stun grab."* He is right and it is stronger than that: **this ultimate deals no
damage, so there is no number on screen, no hit-stop scaled to it, no health
bar moving. If the hand does not read, nothing happened.**

## 7a. THE COLLISION, NAMED BEFORE ANYTHING IS DRAWN

Gravemourn's Revenant is **already made of ethereal purple hands in this
school**, and they are not placeholder art — Rick rejected the first cut
(*"the hands dont read as hands. not detailed enough"*) and the shipped version
was measured at 37px on a 540 frame and 75px on a phone, deliberately legible
as a hand.

```
REVENANT     MANY hands, SMALL, AIRBORNE, thrown off blows, converging on the
             quarry at 2500px/s and closing into fists. Smoke and afterimage.
             On screen 1.8s per hand
GRASP        ONE hand, LARGE, TETHERED — it grows FROM the artifact and stays
             attached to it for the whole window. Bone. It reaches, opens,
             closes, HOLDS
```

One versus many, tethered versus airborne, bone versus smoke, reaching versus
striking. **The tether is the strongest of the four and it is free:** nothing
else in the game connects the wielder to the quarry with a limb, and it is on
screen for eight seconds rather than 1.8. This is v52 §4's problem — Converse
and Deadfall both mark the floor — and it gets the same treatment: an art
constraint written down before either is drawn again.

## 7b. THREE STATES, AND TWO OF THEM ARE ONE FRAME APART

```
REACHING   the hand is open and extending. The window is live and the foe is
           not yet caught. This is most of the eight seconds
HOLDING    closed on the weapon, taut, the tether drawn tight. 0.5s at a time,
           five times
THE CRUSH  the fifth. 2.0s, and the hand is gone after it
```

v54 §2c is the precedent and it nearly shipped broken: Deadfall's ARMING and
ARMED states were drawn at alpha 0.16 against a hall that already had a gold
pentagram on the floor, and photographed off a real match they did not separate
at all. **Photograph these three off a real match before tuning anything**
(`deadfall_sheet.py` is the pattern), and separate them more ways than one —
alpha alone is lost to a phone screen, to the bloom, or to a dark frame.

The count matters too: a viewer should be able to tell the fourth grab from the
fifth **before** the fifth lands, or the payoff arrives without having been
promised. Four knuckles closing, or four marks on the tether — a decision, not
an accident.

## 7c. AND THE GESTURE, NOT THE SILHOUETTE, IS WHAT IS CROWDED

`_whEaten` already exists and is 78.6% distinct from its nearest sibling. But
the other two warhammers in the game — Censer and Bulwarden — both cast novas,
and a nova is *raised overhead and brought down*. So is any hammer. **The
weapon's own animation is free; the ULTIMATE's gesture is the crowded one**,
and this ultimate's answer is that the hammer does nothing at all during it.
The arm does the work and the hammer keeps swinging its ordinary swing.

---

# 8. WHAT NOT TO DO

- **Do not route a grab through `takeHitstun`.** §4.1.
- **Do not write `f.pin`.** §4.5.
- **Do not make the ordinary grabs cancel wind-ups.** Only the fifth. §4.2.
- **Do not give the ultimate damage or a curse application to "make it feel
  worth it."** Both were considered and Rick ruled them out, and the pool is
  measured to be unmoved by the whole ultimate: +1.2 blows and +5.4% of pool.
- **Do not hang the window's art on `m.ultFx`.** §4.4.
- **Do not lengthen the true stun to buy value.** §3.5.
- **Do not touch `01-live`.** Ten relics behind.
- **Do not fix `_burst` or `_tone`.** Twenty-seven shipped voices.
- **Do not let the fight card back in.**

---

# Open decisions — Rick's, and the build can start without any of them

1. **`n` — 4 OR 5.** +20.4% against +24.9%, inside one SE at n=702, so 3b's
   bisection decides it on evidence the lab could not produce. Build 5.

2. **DOES IT GRAB SHADES?** §4.6. A rule, not a knob, and the build needs an
   answer in a comment either way. Placeholder: foe only, shades excluded.

3. **THE FOUR-VERSUS-FIVE TELL.** §7b — whether a viewer can see the crush
   coming. A picture decision with no measured cost and a real effect on
   whether the escalation reads as earned.

4. **CHARGE.** 15, from the roster mode, because v55b established that nobody's
   was ever derived. This relic is the one place where the usual argument for a
   longer charge does not apply — the hold scales with nothing that accumulates
   — so 15 is a positive choice here rather than a default.

5. **SLAGHEART, STILL OPEN FROM v55b.** Ironbloom is the only ultimate in the
   game worth less than nothing (-1.9%) and carries the second-longest charge.
   Not this relic's problem; it has been open for one build now.

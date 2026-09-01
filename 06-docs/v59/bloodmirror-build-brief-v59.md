# v59 — BUILD BRIEF FOR CLAUDE CODE. BLOODMIRROR, the 30th relic, and its ultimate BLOODLETTING. Three separable stages, and the second one changes a number the whole school reads — so the scoping of that change is the single thing most likely to go wrong.

**Read `sundered-crown-spectre-design-v59.md` first** (the §1, priced), and
`sundered-crown-budget-v59.md` §4 (why this cell, and why `row_price`'s numbers
are measured in a world with no ultimates). This file carries only what to do
with them.

**The split, Rick's:** Cowork designs and prices, Code builds. One instrument is
already written — `tools/spectre_lab.py`, runtime-only, 25 arms, and every
paired result in the design doc came out of it.

```
BLOODMIRROR   bloodsworn x scythe, the 30th relic. Bleed is the strongest foe
              channel available on this weapon: +10.0pp against curse's +3.9
              and sunder's +4.7, beaten only by a shield that is already Vesper's
BLOODLETTING  the scythe throws a bloody spectral copy of itself. It flies 0.55s,
              sticks, and mills a 138 disc for 4.5s — and WHILE IT STANDS,
              Hemorrhage stacks to 8 instead of 4, for the blade too
```

---

# 0. THE STAGES

```
 #    IN                          OUT                       WHAT CHANGES
 T    <the tip of the chain>      sc-tipfix.html            the four changes in
                                                            tip-surface-v59.md.
                                                            Provably inert; do it
                                                            first for that reason
 1    sc-tipfix.html              sc-bloodmirror.html       the 30th relic exists,
                                                            its ultimate STUBBED at
                                                            charge 1e9. Blade 21
 2    sc-bloodmirror.html         sc-bloodletting.html      BLOODLETTING — the throw,
                                                            the stick, the mill, the
                                                            ceiling
 F    --                          --                        FILM IT. Before you tune
 3b   sc-bloodletting.html        sc-bloodletting.html      blade bisected from 21
STOP
```

**THE CHAIN'S TIP IS NOT `sc-nightfell.html`.** Everything in the design doc was
measured against it because it is the newest build in the pushed repo, but
Shroudmaul (28) and Cindercleave (29) are yours and are ahead of it. **Build off
the Cindercleave tip and expect every absolute number here to move**; the
DIFFERENCES are what were measured and those travel.

**GREEN BEFORE THE NEXT STAGE STARTS**

```
after T   engine_ab IDENTICAL on all 29, every match. None of the four changes is
          read by the sim and this is the cheapest possible proof of it. If a bit
          moves, THAT is the finding and it stops the stage
          tip_audit re-run: expect §1.1 of tip-surface-v59, not what it prints today
after 1   engine_ab IDENTICAL on the 29 in every match not containing Bloodmirror
          verify --n 40 completes with 30 relics
          the roster sheet, the picker and the intro card all FIT 30
          Bloodmirror with no ultimate lands near 23% at blade 21 (§2)
after 2   bloodletting_relic_probe 13/13 (§4)
          engine_ab IDENTICAL on the 29 in any match containing no cast
          TICKS A FIGHT IS 10.5-11.0 — the scalar the whole design is priced on
after 3b  Bloodmirror inside the field band
          bloodsworn's OTHER FOUR re-swept. §3.2 — the ceiling is scoped, but a
          scoped change to a shared status is exactly the claim to check
```

---

# 1. THE RELIC

```
id          bloodmirror      Rick's, from four
name        Bloodmirror
aff         bloodsworn       onHit { hemorrhage: 2 }, like the school's other four
shape       scythe           reach 104, width 11, artW 46, spin 3.2, mass 2.4,
                             blades [0], mode "spin" — the type owns these and
                             there is no fifth set to invent
dmg         21               -> BISECT. §5
```

**The art is new work and it is not free.** `budget-v59.md` §4.2: `smite` and
`hemorrhage` are byte-identical statuses, and Lastlight is already
sanctified x scythe. v57's repricing puts bloodsworn x scythe at **59.0% from
its nearest sibling — the closest pair on the row**, and v58 is the standing
warning that this number measures separation from the other schools on the same
shape and says NOTHING about whether the shape is any good. **Look at the
bloodsworn branch of the scythe on a real frame before stage 1, not after 3b.**

---

# 2. THE ULTIMATE

```
name        BLOODLETTING     Rick's, from four
kind        "effigy" (new)   NOT "harrow" — Harrowing is Lastlight's, on this same
                             row, and §3.4 of the design doc is why the two must
                             not share a verb
charge      15               the roster mode. AND SEE OPEN DECISION 3: unlike Grasp,
                             this ultimate DOES scale with cast count and charge has
                             never been swept for it
flight      0.55s at 420     thrown at where the quarry is NOW. NO HOMING
life        4.5s             it stands, then it is gone
disc        138              NOT A KNOB. ball 34 + reach 104 — it is a copy of
                             itself, and 138 is what that means
tick        0.22s            FREE at a fixed total (§1 of the design). The rate is
                             the picture
dmg         3 a tick         through `hurt` scaled by the quarry's own dmgTakenMul
bleed       2 a tick         the school's own rate. Worth +4.0pp over 1 a tick ONCE
                             THE CAP MOVES (z +2.53) and nothing at all before it
CEILING     4 -> 8 while the spectre stands, AND THE BLADE FEEDS IT     §3
knock       120              Rick's. +7.9pp, z +2.98, and flat from 60 to 240
who         THE FOE ONLY. -16.5pp at z -6.02 otherwise, which is BELOW the
            no-ultimate floor. Not a balance term — a different relic
hitFly      true             free; +12.7 against +11.2. Do whichever looks better
tip         "Stands a spectral scythe that mills — bleed stacks to 8"   (54/72)
```

## 2.1 THE WHOLE ULTIMATE IS ONE SCALAR, AND THAT IS THE MOST USEFUL LINE HERE

23 arms, regressed on the damage the spectre delivers in a fight:

```
lift = +5.6 + 0.245 x spectreDamage      r2 = 0.80
residual sd 2.9pp against a per-arm SE of 3.1pp
```

**The residuals are smaller than the measurement error.** So:

- **Tune on ticks landed, not on win rate.** It is far cheaper to measure and it
  is what the win rate is made of. The probe reports it every run.
- **The arrangement is free.** Tick rate, damage a tick, life and flight are four
  ways of writing one number; any shape delivering ~32 spectre damage a fight is
  worth the same. Make the remaining choices for the picture.
- **The disc is the exception and so is the ceiling.** Radius is the strongest
  lever in the lab (104 → +10.0, 206 → +28.8) and the first thing that breaks the
  fiction. The ceiling is §3 and it is not on the line at all.

---

# 3. THE CEILING — THE ONE THING THAT IS NOT LIKE ANY PREVIOUS RELIC

## 3.1 WHY IT EXISTS

```
having bleed at all, against none, at cap 4       -2.5pp        z -0.93
having bleed at all, against none, at cap 8       +6.9pp        z +2.67
and once the ceiling is up it keeps paying:
  2 a tick against 1, at cap 8                    +4.0pp        z +2.53
  3 a tick against 1, at cap 8                    +5.2pp        z +3.08
```

Hemorrhage is `{ maxStacks: 4, dur: 3.2, dps: 1.5 }` — a hard ceiling of 6
damage a second. A spectre ticking every 0.22s reaches four stacks in under a
second and everything after is a clock refresh. **Rick's sentence — "hits
rapidly applying bleed" — describes a mechanic the game currently forbids**, and
lifting the ceiling is what makes it true. It is also what makes this relic do
something different to the status than Harrowing does.

## 3.2 AND `maxStacks` IS GLOBAL, WHICH IS THE HAZARD

`AC.STATUS.hemorrhage.maxStacks` is **one number shared by every fighter in the
match and by the four other bloodsworn relics in the field.** The lab moves it
and restores it per match and asserts it is 4 on the way out; that is fine for a
lab and it is NOT fine for a build.

**Scope it per-fighter**, the way v53 scoped the curse pool — a fighter carries
its own cap, defaulting to the status's, raised while a Bloodmirror spectre it
does not own is standing. Precedent and reasoning are in `curse-build-v53.md`
§2.1: *"a convention that two call sites must both fire is not agreement, it is
a promise."*

**The three failure modes, all silent:**

```
a Marrowdraw in the same fight inherits the window and nothing errors
the cap is left at 8 after a match and the NEXT match starts wrong
the cap is restored on m.over but not on the window merely expiring
```

Assert all three. The third is the one a probe usually misses.

## 3.3 WHAT HAPPENS TO STACKS ABOVE 4 WHEN THE WINDOW CLOSES

Open decision 4 in the design doc, and the build needs an answer in a comment
either way. **Placeholder: leave them and let them decay on their own 3.2s
clock.** A window that reaches into the seconds after it closes is what a bleed
should do, and trimming instantly is the version that looks like a bug.

---

# 4. THE PROBE — ONE CHECK PER SENTENCE

`tools/bloodletting_relic_probe.py`:

1. **The spectre is thrown on the cast and on nothing else**, never two at once
   from one cast, and its flight is 0.55s at 420 with no homing — assert the
   bearing is fixed at spawn.
2. **It stops where it stops.** After `flight`, position is constant for `life`
   and then the object is gone. Assert it never leaves the hall.
3. **The disc is 138** and a tick lands if and only if the quarry's centre is
   inside it.
4. **A tick deals 3 through `hurt` scaled by `dmgTakenMul`, applies 2
   Hemorrhage, and knocks 120** — read off the engine's own events, not
   recomputed from the config.
5. **THE CEILING IS SCOPED.** §3.2. Run a Bloodmirror match and a Marrowdraw
   match in the same page session and assert Marrowdraw's cap never moved; then
   assert the cap is 4 after the window expires WITHOUT the match ending.
6. **The blade feeds the raised ceiling too** — Rick's ruling. Assert a blade hit
   during the window can carry the quarry past 4.
7. **The caster is never ticked**, in any match, by its own spectre or anyone
   else's. §2, and it is worth -16.5pp.
8. **No tick on a corpse, none after `m.over`, none while `m.hitStop > 0`.**
   The sim is frozen during hit-stop and so is the hall.
9. **The spectre is per-fighter.** Cast Bloodmirror, then run six other-relic
   matches after it in the same page session and assert nothing of theirs moved.
   `gravemourn_relic_probe [9d]`'s pattern.
10. **It is not built on `shots`.** Assert `bladeSegments` cannot parry it —
    v57 §4.6, and `spawnShot` shifts the oldest live entry out at `maxLive` 64.
11. **THE BEAT.** The cast files one, the landing files its own, the individual
    ticks file none. **And the spectre CAN kill**, so a tick that lands the
    killing blow must file a FATAL beat — v53 §4, where 30 of 58 Gravemourn
    kills rendered with no killing blow because a hand filed `kind:"ult"`.
12. **TICKS A FIGHT IS 10.5-11.0.** The scalar the whole design is priced on
    (§2.1). Report it every run.
13. **THE SOUND IS RENDERED AND MEASURED IN AN `OfflineAudioContext`.**
    `SFX.play` returns on its first line headless and swallows its exceptions;
    v42 shipped a silent ultimate through every green check in the repo. **Four
    voices, and the third is the hard one:** the throw, the landing, the mill
    while it stands, and the window closing. The mill has to survive being heard
    for four and a half seconds without becoming a wash — the Winnowing's rung
    problem, held rather than repeated.

---

# 5. THE BLADE

`final_blade.py`, the exact ruled build, 416 fights an arm:

```
blade      24.0    22.0    20.0    18.0    16.0
with it   59.1%   56.2%   46.6%   46.6%   37.7%
without   29.8%   28.8%   17.8%   12.5%    7.5%
```

**Start the bisection at 21 and expect the answer in 20-22.** The curve is flat
between 18 and 20 and steep either side of that, which is its own finding: two
points of blade are worth ten points of win rate around 21 and nothing at all
around 19.

At 21 the ultimate is worth roughly **28 points** — just above the roster mean
of +20.1, and exactly the composition Rick chose from three.

**And the surface is NOT simple.** `dmg` moves the blade AND the pool AND — via
the raised ceiling — how much the pool is worth during the window. v51 §4.5's
superlinear warning applies here where it did not to Shroudmaul.

---

# 6. THE TRAPS

**6.1 `m.ultFx` IS ONE SLOT.** v54 §2a, chain-wide: the opponent casting anything
overwrites it. Deadfall survived only by being rebuilt onto `f.ultDeadfall` and
Breach was told to start on `f.ultBreach`. **Start on `f.ultSpectre`.** And set
`atSelf` on the fx spec (v54 §2b) — `drawUltOver` puts a `burst` at the QUARRY,
which is right for a nova and wrong for a thing thrown from the caster.

**6.2 DO NOT BUILD IT ON `shots`.** §4 check 10.

**6.3 SHADES.** `tickShadeHits` is where v51 §4.3's bug lived and Twinshade puts
three bodies in the hall for six seconds. A disc that mills everything inside it
will sweep all three. Decide the rule, write it in the comment, assert it.
Placeholder: a shade is caught like any other body.

**6.4 THE CAP.** §3.2. The most likely silent failure in this build.

**6.5 THE COLLAPSE.** `CONFIG.collapse` walks the inset 0 → 140 from t=21s. A
spectre anchored early can end up outside the hall — v40 §3.3 is the precedent
and Breach was told the same thing. **Either clamp it to the current inset every
frame, or let it die when the wall reaches it, but decide which and say so.**
The lab clamps to the arena at throw time only and does not model the collapse
at all, so this is unmeasured.

---

# 7. THE ART, AND ONE LINE OF IT IS THE MECHANIC

## 7a. THE ADJACENCY IS ON THIS RELIC'S OWN ROW

```
HARROWING    Lastlight, sanctified x scythe. TWELVE small white scythes that
             stick to the BODY, burden it, and burst ONCE
BLOODLETTING ONE large red scythe that anchors in the HALL and mills
BLOODMILL    Redflail already throws bleeding things — but they FLY AWAY.
             This one STOPS
```

## 7b. NOTHING IN THIS GAME HAS EVER OCCUPIED OPEN SPACE

Thicket's vines root to walls, Breach's vents are torn in walls, Deadfall's
sigils are stamped where a blow landed, the Stasis Field rings its own caster.
**The spectre is the first object the two balls have to navigate around**, and
that is the strongest thing in the §1. It is free and a viewer will notice it.

It also sets a camera problem: `cinema_clip` has to be able to frame the spectre
and both fighters at once, and nothing in this game has needed that before.

## 7c. FOUR STATES, AND THE LAST ONE IS THE MECHANIC

```
THE THROW    the copy leaves the weapon. 0.55s, and it is a COPY — the same
             silhouette, red and ghosted
THE STICK    it stops. The frame that tells a viewer it is STAYING, and if it
             does not read, the ultimate looks like a missed shot
THE MILL     4.5 seconds of rotation. Most of the ultimate, and the state that
             has to hold up without becoming wallpaper
THE CEILING  while it stands, the quarry can carry more bleed than anything else
             in the game can put on it. §3 says this is the mechanic — SO IT HAS
             TO BE VISIBLE. The stack readout going past four is the only
             evidence on screen that the ceiling moved
```

**7c's last line is the one to get right**, and v54 §2c is the precedent that
cost a build: Deadfall's arming state was invisible at alpha 0.16 and no probe
in this repo could have said so. A viewer cannot see a constant. **Photograph
the stack readout at 5, 6, 7 and 8 off a real match before tuning anything.**

## 7d. FILM BEFORE YOU TUNE

v43 §13, and this ultimate is a thing you watch stand there for four and a half
seconds. The clip is a test, not a deliverable that comes after the numbers.

---

# 8. WHAT NOT TO DO

- **Do not let the spectre cut the caster.** §2. Six standard errors.
- **Do not move `STATUS.hemorrhage.maxStacks` globally.** §3.2.
- **Do not give BLOODLETTING the `harrow` kind**, or Harrowing's spray, or its
  white. Same row, same status, and §3 is the only thing that separates them.
- **Do not tune on win rate** when ticks landed is 30x cheaper and is what the
  win rate is made of. §2.1.
- **Do not widen the disc past 138** to buy strength. It stops being a copy.
- **Do not touch `01-live`.** Twelve relics behind.
- **Do not fix `_burst` or `_tone`.** Twenty-nine shipped voices.
- **Do not let the fight card back in.**

---

# 9. THE REGISTERED PREDICTION, AND IT IS THIS BUILD'S JOB TO FALSIFY IT

> *At disc 138, tick 0.22, 3 damage and 2 Hemorrhage a tick, life 4.5, flight
> 0.55 at 420, knockback 120, cap 8 while it stands and blade 21, the built
> relic delivers **10.5-11.0 ticks a fight** and lands within one SE of
> **+28 points over its own no-ultimate floor**; and the blade bisects into
> 20-22 rather than moving far.*

**If ticks come out in band but the win rate does not**, the one-scalar law in
§2.1 is an artefact of the lab's injection and every knob has to be re-priced
against the built relic. **If the ceiling's +7.9pp does not reproduce**, the
scoping in §3.2 is doing something the lab's global version was not — and that
is a finding about the engine, not about this relic.

---

# Open decisions — Rick's, and stage T can start without any of them

1. **THE NAMES SHARE A WORD.** No relic in the game shares its first word with
   its own ultimate — Redflail casts Bloodmill, Marrowdraw casts Bloodhunt,
   Oathwound casts Bloodprice, Widowmaker casts Exsanguinate. Bloodmirror
   casting Bloodletting would be the first. Rick has seen this and has not
   changed either; it ships as picked unless he says otherwise.

2. **STACKS ABOVE 4 WHEN THE WINDOW CLOSES.** §3.3. A rule, not a knob.
   Placeholder: they decay on their own clock.

3. **CHARGE.** 15, the roster mode, and v55b established nobody's was ever
   derived. **Unlike Grasp this ultimate DOES scale with cast count** — more
   spectres is strictly more damage — so charge is a real knob here and it has
   never been swept. One lab, and it belongs before the bisection rather than
   after.

4. **SHADES.** §6.3. Same shape as every previous relic's version of this.

5. **THE COLLAPSE.** §6.5, and it is the one thing in this brief that is
   completely unmeasured.

6. **THE SCYTHE'S BLOODSWORN ART IS THE CLOSEST PAIR ON ITS ROW** at 59.0%, and
   v58 established that number does not measure whether a shape is any good.
   Look at it early.

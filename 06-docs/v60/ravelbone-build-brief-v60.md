# v60 — BUILD BRIEF FOR CLAUDE CODE. RAVELBONE, the 31st relic, and its ultimate GARROTE. Four stages. The single most likely failure in this build is silent, it is in the engine's own `move()`, and it would delete the ultimate's headline effect while every probe in the repo stayed green.

**Read `sundered-crown-wirering-design-v60.md` first** (the §1, priced, 26 arms
at 702 fights each) and `sundered-crown-cell-error-v60.md` §6 for the cell. This
file carries only what to do with them.

**The split, Rick's:** Cowork designs and prices, Code builds. One instrument is
already written — `tools/wire_lab.py`, runtime-only, 26 arms, and every paired
number in the design doc came out of it.

```
RAVELBONE   bloodsworn x warhammer, the 31st relic and bloodsworn's LAST open
            cell. Rick's name, from four
GARROTE     the hammer winds up; a ring of barbed wire at its hit range SNAGS
            the foe — the ball is held, the weapon keeps swinging — and when the
            head comes around it hits, throws, and blows the ring apart,
            consuming the foe's Hemorrhage for damage.  Rick's name, from four
```

**THE CHAIN'S TIP IS NOT `sc-shroudmaul.html`.** Everything above was measured
against it because it is the newest build in the pushed repo, but Cindercleave
(29) is yours and is ahead of it, and **Bloodmirror (30) is neither built nor in
the repo** — its brief is `sundered-crown-bloodmirror-build-brief-v59.md` and it
is ahead of this one in the queue. **Build off whatever the real tip is when you
start, and expect every absolute number here to move**; the DIFFERENCES are what
were measured and those travel.

---

# 0. THE STAGES

```
 #    IN                       OUT                     WHAT CHANGES
 1    <the tip of the chain>   sc-ravelbone.html       the 31st relic exists, its
                                                       ultimate STUBBED at charge
                                                       1e9. Blade 23.5
 2    sc-ravelbone.html        sc-wire.html            the wind-up and the RING:
                                                       snag, hold, connect,
                                                       knockback. NO consume yet
 3    sc-wire.html             sc-garrote.html         the explosion CONSUMES
                                                       Hemorrhage. §5
 F    --                       --                      FILM IT. Before you tune
 4    sc-garrote.html          sc-garrote.html         blade bisected from 23.5
STOP
```

**Stage 2 stops before the consume on purpose.** The consume is a clean linear
knob (+0.73 win points per point of per-stack damage, §5) and it is the last
thing that should move. A stage-2 build that lands near **+24%** over its own
no-ultimate floor is the gate; if it does not, the consume will paper over
whatever is wrong with the ring and nobody will find it until the bisection
misbehaves.

**GREEN BEFORE THE NEXT STAGE STARTS**

```
after 1   engine_ab IDENTICAL on the existing roster in every match not
          containing Ravelbone
          verify --n 40 completes with the full roster
          the roster sheet, the picker and the intro card all FIT the new count
          Ravelbone with no ultimate lands near 37% at blade 23.5 (§7)
after 2   garrote_relic_probe 1-11 (§6)
          engine_ab IDENTICAL on the others in any match containing no cast
          THE RING LANDS +24% +/- 3 over the stage-1 floor
          CONNECTS PER CAST IS 0.8-0.9 — the scalar the picture depends on (§3)
after 3   garrote_relic_probe 12-14
          bloodsworn's OTHER FIVE re-swept. The consume DELETES a status the
          whole school shares and that is exactly the claim to check
after 4   Ravelbone inside the field band
```

---

# 1. THE RELIC

```
id          ravelbone        Rick's, from four
name        Ravelbone
aff         bloodsworn       onHit { hemorrhage: 2 }, like the school's other five
shape       warhammer        reach 76, width 26, artW 54, spin 1.6, mass 5.0,
                             knockMul 2.3, blades [0], mode "spin" — the type owns
                             these and there is no fifth set to invent
dmg         23.5             -> BISECT. §7
```

**The art is the best thing in the candidate set and the ink-mask column says the
opposite.** `cell_survey [3]` puts bloodsworn x warhammer at **50.8% from
dwarven, the closest pair on its type** — and rendered in its own palette beside
Grudgebearer it is unmistakably a different object: a red-and-bone head with
three claw slashes across the face. `cell-error-v60.md` §5 and `tools/cand_art.py`.
**v58's warning stands in both directions** — that number does not say a shape is
bad any more than it says one is good. Look at it on a real frame before stage 1.

---

# 2. THE ULTIMATE

```
name        GARROTE          Rick's, from four
kind        "wire" (new)     NOT "forge" — see §8.1, and Crucible is the dwarven
                             warhammer
charge      16               the roster mode. AND SEE OPEN DECISION 4: never swept,
                             and this ultimate DOES scale with cast count
dur         8.0s             the window, if nothing is ever caught. 4s is +19.1
                             and 12s is +30.9, so this is a real knob and 8 is
                             where the §1 sits
spinMul     6.0 to 9.0       FLAT TO NOISE across x2 -> x12 (8.1pp spread against
                             a 2.7pp SE). PICK IT FOR THE PICTURE. Do NOT pick 3.4
                             — that is Crucible's exact number on this same type
radius      110              Rick's, from two. reach 76 + ballR 34 = where a blow
                             actually lands, and where 3 catches in 4 pay off.
                             76 is +6.7 stronger and fewer than HALF its catches
                             ever get the hammer (§3 of the design doc)
snag        f.pin, NOT f.stun            §3. The whole separation
connect     w.dmg x1 + the consume, knock x2, and the ring expires
knock       2x a normal blow = CONFIG.combat.knock 165 x knockMul 2.3 x 2 = 759.
            +4.9pp for the first doubling and NOTHING after it: x5 is +29.8
            against x2's +30.1. Do not buy strength here
consume     8 damage a stack, and see §5
tip         mechanic-first, <=72 chars. Not written — open decision 3
```

---

# 3. THE SNAG — THE ONE VERB NOTHING ELSE IN THE GAME USES

Rick ruled the wire **snags** rather than stuns, and separately that the ball is
**frozen**. Together those are one design and it is new:

```
                     ball        weapon      can the foe act?
CRUCIBLE             pulled      LOCKED      no
GRASP                free        LOCKED      no
STASIS FIELD         HELD        LOCKED      no      ("unable to move (ball and weapon)")
GARROTE              HELD        free        YES — it just cannot leave
```

**Write `f.pin`. Do NOT write `f.stun`.** The engine's own comment at `this.pin`
confirms Stasis writes both; writing only the ball half is unused, and it is the
entire answer to *"this is the third warhammer that stops the other fighter."*

Measured, at 702 fights an arm:

```
ring that only cuts, no hold at all            +19.6%    the field median exactly
SNAG — ball held, weapon free                  +24.0%    the hold is worth +4.4
the stun version, for comparison               +27.8%    snagging costs 3.8
```

**The snag costs 3.8 points and buys the whole identity.** It also raises
connects from 1.17 to 1.38 a fight, because a pinned ball cannot drift out of the
head's path — so the promised payoff lands more often as well.

**`ballCollision` is deliberately NOT gated on `pin`** (engine comment at
`this.pinV`): a held ball can still be shouldered. That is correct here and worth
knowing — the hammer's own body can shove its catch, and that is a picture, not a
bug.

---

# 4. THE TRAP THAT WILL EAT THE KNOCKBACK, SILENTLY

**`move()` DISCARDS every impulse a ball took while it was pinned.** The engine
says so in its own voice, and it was a measured, named fix:

> *"everything that happened to its velocity while it could not use it is
> discarded HERE, on the first frame it is allowed to move again, and the vector
> it resumes with is byte-for-byte the one it was captured with. [...] The
> discard is untouched: this still ASSIGNS, so knockback banked during the hold
> is still thrown away. v43's rule."*

**GARROTE'S HEADLINE EFFECT IS A MASSIVE KNOCKBACK DELIVERED TO A BALL THAT IS
PINNED AT THAT INSTANT.** Apply the impulse before clearing the pin and `move()`
overwrites it with `f.pinV` on the very next frame. The hit lands, the damage
lands, the beat files, the probe passes — **and the ball does not move.**

```
THE ORDER, AND IT IS NOT NEGOTIABLE
  1.  f.pin = 0;  f.pinMax = 0;  f.pinV = null;      release FIRST
  2.  then the impulse
  3.  then the consume, the damage, the beat
```

**Assert it as a displacement, not as a velocity write.** The probe must read the
ball's position two frames after the connect and see it *somewhere else*, because
a test that checks `vx` immediately after the write passes in the broken build.
This is §6 check 8 and it is the most important check in this document.

---

# 5. THE CONSUME

Rick's ruling, over leaving the bleed as picture only. **The reason it is needed
is that the §1's bleed did nothing at all:** `hemorrhage` caps at 4, the hammer's
own `onHit` puts on 2 a blow, and the bar is full before the ultimate casts —
applying 1 stack on the explosion and applying 4 returned **64.5% and 64.5%,
identical to the decimal**.

```
consume per stack      0        8       14       20
lift                +24.0%  +30.3%   +35.3%   +38.4%
burst on the connect    24      56       80      104     (on top of a 23.5 blade)
```

**Linear at +0.73 win points per point of per-stack damage.** Start at **8** —
~56 damage on the connect, the hardest single blow in the game and still not a
quarter of a fighter's health. **Settle it AFTER the bisection**, because it and
the blade trade directly and the blade is the coarser instrument.

```
read  th.stacks("hemorrhage")  BEFORE any of the connect's own damage
then  delete th.status.hemorrhage
```

**And it is a status the whole school shares.** Five other bloodsworn relics put
Hemorrhage on, and Bloodmirror — if it lands first — raises its ceiling to 8
while its spectre stands, which would make a Garrote connect worth up to double.
**Re-sweep bloodsworn after stage 3**, and if both relics exist, decide whether
Garrote consuming an 8-stack pool is a feature or a number nobody chose.

---

# 6. THE PROBE — ONE CHECK PER SENTENCE

`tools/garrote_relic_probe.py`:

1. **The ring exists only inside the window**, is centred on the wielder every
   frame, and its radius is 110. Assert it is gone the frame the window ends.
2. **The wind-up multiplies rotation and nothing else.** Assert `f.theta`
   advances at `spin x spinMul` and that reach, damage and `hitCd` are untouched.
3. **NOT `f.ultSpin`.** §8.1. Assert Twinshade's field is null on Ravelbone in
   every frame of a cast.
4. **The snag writes `f.pin` and NEVER `f.stun`.** Assert the caught foe's
   weapon still turns and still lands blows while held. This is the relic.
5. **One catch per window.** The ring does not re-snag after a connect, because
   the connect expires it.
6. **The connect fires when the head comes around** — `|theta - bearing|` inside
   the head's own arc — and not on a timer.
7. **The hold ends when the window ends**, even with no connect, and `pin`,
   `pinMax` and `pinV` are all clear afterwards. Assert on a fight where the foe
   is caught and the window expires.
8. **THE KNOCKBACK ACTUALLY MOVES THE BALL.** §4. Read POSITION two frames after
   the connect, not velocity at the write. **The single most important check
   here.**
9. **The caster is never snagged**, by its own ring or anyone else's.
10. **No catch on a corpse, none after `m.over`, none while `m.hitStop > 0`.**
11. **THE BEAT.** The cast files one, the connect files its own, and **the
    connect CAN kill** — so a killing connect must file a FATAL beat. v53 §4,
    where 30 of 58 Gravemourn kills rendered with no killing blow because a hand
    filed `kind:"ult"`. Tenth relic running.
12. **The consume reads the stacks BEFORE the connect's damage and clears them.**
13. **It clears only the QUARRY's.** Run a Ravelbone match and another
    bloodsworn match in the same page session and assert nothing of theirs moved.
14. **CONNECTS PER CAST IS 0.8-0.9.** The scalar the picture depends on. Report
    it every run.
15. **THE SOUND, rendered and measured in an `OfflineAudioContext`.** `SFX.play`
    returns on its first line headless and swallows its exceptions; v42 shipped a
    silent ultimate through every green check in the repo. **Four voices:** the
    wind-up, the snag, the wire under tension while it holds, and the burst. The
    third is the hard one — it has to hold for seconds without becoming a wash,
    which is the Winnowing's rung problem again.

---

# 7. THE BLADE

`§1 as ruled` lands at **+30.3%** over its own no-ultimate floor against a field
whose 27 built ultimates run **mean +20.1, median +19.7, Q3 +25.5**. That is
sixth or seventh of thirty-one, so **the blade pays**, and by more than
Shroudmaul's did.

Start the bisection at **23.5** (the type's own) and expect the answer **below**
it. The lab's floor arm — Grudgebearer as a bloodsworn warhammer with no
ultimate — sits at **36.8%**, so there is room to give back.

**The surface is not simple.** `dmg` moves the blade AND the Hemorrhage the
consume later eats, so lowering the blade lowers the burst twice. Sweep the
consume again after the blade lands, not before.

---

# 8. THE TRAPS

**8.1 `f.ultSpin` IS TWINSHADE'S AND IT ALSO CHANGES CLANKS.** The field is
declared *"{t, dur} while the shades walk"*, `tickSpinStorm` drives it, and
`resolveClank` reads `spinLockA = !!A.ultSpin` to grant **immunity from having
your spin direction reversed by a lost bind**. Reusing it would collide with
Twinshade and would silently hand Ravelbone that immunity.

> **But Ravelbone probably WANTS that immunity, and for a stated reason:** a
> hammer at 6-9x whose direction flips on a lost clank stops coming around, and
> the snag never pays off. **Grant it deliberately from Ravelbone's own field,
> with a comment**, rather than inheriting it by accident. Open decision 2.

**Start on `f.ultWire`.** Add its own term to the spin expression in
`tickWeapon` alongside `ultDraw || ultForge` and `ultSpin`.

**8.2 `m.ultFx` IS ONE SLOT.** v54 §2a, chain-wide: the opponent casting anything
overwrites it. Deadfall survived only by moving to `f.ultDeadfall`, Breach was
told to start on `f.ultBreach`, Bloodletting on `f.ultSpectre`. A ring that is on
screen for eight seconds cannot live in a slot the other fighter can clear.

**8.3 DO NOT BUILD THE RING ON `shots`.** `spawnShot` shifts the oldest live
entry out at `maxLive` 64, and a parryable ring is not a ring.

**8.4 SHADES.** Triplicate puts three bodies in the hall and a ring at hit range
will reach whichever is nearest. `tickShadeHits` is where v51 §4.3's bug lived.
Decide the rule, comment it, assert it. **Placeholder: the ring snags the real
quarry only** — pinning a copy that is about to expire is a wasted window, and
unlike Grasp this ultimate gets exactly one catch.

**8.5 THE COLLAPSE.** `CONFIG.collapse` walks the inset 0 -> 140 from t=21s. The
ring is centred on the wielder so it travels with it, but a ball pinned near a
wall can end up outside the hall as the wall arrives. **Decide: does the collapse
break the snag, or does the wall push a held ball?** Unmeasured, and v40 §3.3 is
the precedent.

**8.6 DESPERATION AND ENTANGLE BOTH MULTIPLY SPIN.** `spinMul(actSpin)` already
folds in `entangle.spin` and `CONFIG.desperation.spin` 1.30. A desperate,
un-entangled Ravelbone at x9 is turning at 1.6 x 1.3 x 9 = 18.7 rad/s, about
three revolutions a second. Check it does not read as a strobe.

---

# 9. THE ART

```
THE WIND-UP    the head starts turning faster. The telegraph, and the only
               warning the other fighter gets
THE RING       barbed wire at exactly the reach of the head. FIRST object in this
               game whose area IS the weapon's own hit range, drawn — a viewer
               who sees the ring knows precisely where it is unsafe to be
THE SNAG       the foe stops moving AND KEEPS SWINGING. If this does not read,
               the ultimate looks like a stun and the whole separation in §3 is
               invisible. The wire has to be seen holding the ball
THE CONNECT    the head arrives, the foe goes across the hall, the ring blows
               apart. One frame, and it is the payoff for eight seconds
```

**9c's third line is the one to get right**, and v54 §2c is the precedent that
cost a build: Deadfall's arming state was invisible at alpha 0.16 and no probe in
this repo could have said so. **Photograph a snagged foe mid-swing before tuning
anything** — a held ball with a moving weapon is a picture this game has never
drawn, and if it reads as a frozen one the design is not on screen.

**FILM BEFORE YOU TUNE.** v43 §13. The wind-up, the catch and the arrival are
three beats in eight seconds and no number above says whether they read.

---

# 10. WHAT NOT TO DO

- **Do not apply the connect's knockback before releasing the pin.** §4.
- **Do not write `f.stun` on the snag.** §3. It is the relic.
- **Do not use `f.ultSpin`.** §8.1.
- **Do not use `spinMul` 3.4.** Crucible's, on this type.
- **Do not widen the ring past 110** to buy strength. It stops being the hammer's
  reach, which is the only thing it means.
- **Do not tune the consume before the blade.** §7.
- **Do not touch `01-live`.** Twelve relics behind.
- **Do not fix `_burst` or `_tone`.** Twenty-nine shipped voices.
- **Do not let the fight card back in.**

---

# 11. THE REGISTERED PREDICTION, AND IT IS THIS BUILD'S JOB TO FALSIFY IT

> *At radius 110, spin x6, window 8s, snag by `pin` and never `stun`, knock 2x,
> consume 8 a stack and blade 23.5, the built relic delivers **0.8-0.9 connects
> a cast** and lands within one SE of **+30 points over its own no-ultimate
> floor**; the blade bisects DOWNWARD from 23.5; and the ultimate's value tracks
> **blows the opponent does not land** at roughly +8 win points per blow denied,
> as it did across all 26 lab arms.*

**If connects come out in band but the lift does not**, the lab's ring is not the
built ring and every knob has to be re-priced. **If the snag's +4.4 over a
cutting-only ring does not reproduce**, then `pin` is doing something in the
build that it did not do in the lab — and §4 is the first place to look, because
a discarded knockback would show up exactly that way.

---

# Open decisions — Rick's, and stage 1 can start without any of them

1. **THE CONSUME'S PER-STACK NUMBER.** 8 is the recommendation and it is a clean
   linear knob at +0.73 a point. Settle it after the bisection.

2. **DOES RAVELBONE KEEP ITS SPIN DIRECTION THROUGH A LOST CLANK?** §8.1.
   Recommended yes, from its own field and with a comment — a hammer that
   reverses mid-window never comes around, and the snag it is holding pays off
   nothing. Rick already ruled the same way for Twinshade: *"grant immunity to
   losing clanks so it never reverses direction while its casting."*

3. **THE TIP.** 72 characters, mechanic-first (Rick's standing rule), and the
   thing to get in is that the wire holds you where you stand and the hammer is
   coming. Not written.

4. **CHARGE.** 16 by default, never derived for anybody (v55b), and unlike Grasp
   this ultimate scales with cast count. One lab, before the bisection.

5. **SHADES.** §8.4. A rule, not a knob.

6. **THE COLLAPSE AGAINST A HELD BALL.** §8.5. The one thing in this brief that
   is completely unmeasured.

7. **BLOODMIRROR IS AHEAD OF THIS IN THE QUEUE AND ITS BRIEF IS NOT IN THE REPO.**
   Neither is this one. Both live in the Cowork project only.

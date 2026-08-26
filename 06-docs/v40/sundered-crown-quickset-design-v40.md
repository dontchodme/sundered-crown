# v40 — §1. THE DESIGN, IN RICK'S WORDS.

**2026-08-20.** Verbatim, unedited, before anything was written. v38 §1 and
v39 §1, held to a third time.

---

> heres the ult
>
> for a duration the bow fires out seeds instead of arrows.
>
> the seeds deal normal damage if they hit another ball. or disappear if
> clanked
>
> however if they stick to the wall they take root. after a short time the
> bloom into a flowering plant with a vine whip that reaches out and strikes
> at the enemy if they come close enough.
>
> vine whips should have good but limited range so several can swipe at the
> enemy at the same time
>
> the vines cannot be damaged or removed by the enemy
>
> the vines stay for a duration and then wither and die.
>
> the vines should have knockback
>
> the vines should have their own unique whipping sound effect

---

# 2. WHY THIS IS THE RIGHT ANSWER TO WHAT THE SURVEY FOUND

The survey's headline was that **82% of every arrow this game has ever fired
ends on a wall**, that the wall is worth ten times what any status is on this
type, and that nothing in the roster addresses it. Rick's ultimate does not
mitigate that number. **It spends it.** The waste channel becomes the payload:
the arrows that miss are the ones that do the work, and the 82% stops being a
loss and becomes a rate.

Three measurements from `bow_survey.py` and `verdant_bow_probe.py` are load-
bearing on the numbers below and each of them was taken before this design
existed:

* **~82% of seeds will reach a wall.** At `cadence 0.34` that is 2.9 seeds a
  second fired and roughly 2.4 rooting. A five-second window is about twelve
  plants, which is why "several can swipe at the same time" is achievable at
  all and why a cap is needed rather than optional.
* **Two thirds of wall deaths are on the SIDE walls**, which are 520 apart —
  not the floor and ceiling, which are 800 apart. The garden grows down the
  long sides of the hall by itself.
* **`shot.life` is 3.4 seconds and an arrow uses 11% of it.** The seed
  inherits a life nine times longer than it can ever need, so nothing about
  the window has to be paid for twice.

And one from the arc: the hall collapses from 15s and separation halves.
**The vines ride the wall inward** rather than being left outside it — see §4.3.
That is not decoration. It means the ultimate gets stronger exactly as the
fight compresses, which is the type's own measured arc.

---

# 3. THE FOUR INTERVIEW ANSWERS I DO NOT HAVE

These are decisions §1 does not settle and that I have made explicitly, so
each is visible and vetoable rather than buried in a constant:

1. **A vine's strike goes through `resolveHit`.** So it crits, jitters, is
   multiplied by Sunder, causes hit stop and hitstun, draws a damage float —
   and **applies the wielder's own `onHit`, which is Entangle 2.** Rick did
   not ask for that; it is what the house rule ("a shot is a hit in every
   sense the rest of the game already understands") produces. The alternative
   is a second damage path, which this codebase has refused four times.
2. **The knock is the vine's own and goes vine → foe**, i.e. off the wall and
   into the hall. `resolveHit`'s built-in knock still fires away from the
   CASTER, exactly as it does for every arrow. Double knock on a projectile is
   the established pattern, not a new one.
3. **A vine does not care whether its caster is alive.** It withers on its own
   clock. It will not strike a dead foe.
4. **The seed keeps the arrow's speed, cadence and radius.** The type owns
   those and all three bows share one `shot` block byte for byte.

---

# 4. WHAT IS NEW IN THE ENGINE, AND WHAT IS FREE

## 4.1 Free

The seed is a `shot`. It is clankable, travelling, missable, drawn by the same
loop, and resolved by `resolveHit` — "disappear if clanked" is already what
the parry does to any projectile, and "normal damage if they hit another ball"
is already what the hit branch does. **No code was written for two of the
seven sentences in §1.**

"The vines cannot be damaged or removed by the enemy" is free in the strongest
possible sense: a vine is not in `a` or `b`, so `tickHits`, `tickClank` and
`tickShots` cannot see it. There is nothing to exempt.

## 4.2 New

`m.vines` — a match-level list in the same family as `m.sparks`, `m.shades`
and `m.drains`. **It is empty in every match without this relic**, and
`tickVines` returns on its first line when it is. `engine_ab` over the other
twenty-one ids is the proof of that, not this paragraph.

`f.ultBloom = {t, dur}` — the seed window, and it is `f.ultRadiant`'s exact
shape. Daybreak already established "for a duration this weapon's hits are
different"; this is "for a duration this weapon's SHOTS are different", one
field and one branch in `spawnShot`.

## 4.3 The one thing that had to be invented

**A vine is stored as a wall and a position ALONG that wall, not as an (x, y).**
`CONFIG.collapse` moves `m.inset` from 0 to 140 over the fight, so an absolute
position planted at 10s is outside the hall by 40s — the plant would be buried
in the closing wall and lashing from off-screen. Storing `{wall, u}` and
recomputing the perpendicular coordinate from the current inset every frame
costs two lines and makes the collapse work for the mechanic.

---

# 5. EVERY NUMBER IS A PLACEHOLDER AND MUST BE SWEPT

`sprout`, `vineLife`, `reach`, `whipDmg`, `whipCd`, `whipKnock`, `maxVines`
and `dur` are all unset in §1 and none of them can be guessed. The economy is
worse than Foregone's was: the vine count is linear in `dur`, the number that
can reach the foe at once is quadratic-ish in `reach`, and the damage is the
product of both against a cooldown. A foe that happens to sit in a corner is
inside three plants' arcs at once.

`quickset_sweep.py` is the instrument and it is the next thing after the probe.

---

# 6. THE NAME

Not Rick's, and vetoable.

**QUICKSET.** A quickset hedge is a real thing and it is made by driving
living cuttings into the ground and letting them root where they land. The
word is the mechanic — "quick" in its old sense of *living*, "set" a cutting
planted to grow — and it sits in the verdant register beside Heartwood,
Thornwake, Rootfast and Bramblesnare without borrowing from any of them.

**THICKET**, for the ultimate. It names the RESULT, which is how the school's
other two ultimates are named, and a viewer who watches a wall sprout six
flowering plants has been told what a thicket is without a caption.

---

# Open decisions

1. **The name.** §6. Mine, not Rick's.
2. **Entangle on the whip.** §3.1. A consequence of the house rule rather than
   a design choice, and the largest single thing in here that Rick did not ask
   for.
3. **Every number.** §5. Nothing below `charge` has been swept.
4. **What happens to a plant the closing wall reaches.** §4.3 moves it inward
   with the wall. The alternative — it is crushed and withers early — is also
   defensible and is not what is built.

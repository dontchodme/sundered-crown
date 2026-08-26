# v41 — BULWARDEN / AEGIS. §1 in Rick's words, and the three forks he settled.

**2026-08-20.** Vigil × warhammer, the twenty-third relic. The cell is the
double gap: thinnest school (2 of 6) and thinnest type (2 of 6), chosen against
`wh_survey.py`'s 23/23 rather than against a hunch.

---

# 1. THE DESIGN, IN RICK'S WORDS

> *"Bulwark: The ult conjures a shield in front of the ball. the shield rotates
> with the weapon and blocks incoming damage. it also reflects a portion of the
> damage it blocked back to its attacker"*

Four sentences. Nothing was started before this existed.

---

# 2. WHY IT IS THE ANSWER TO WHAT THE SURVEY MEASURED

`wh_survey` §3 found the type's own thesis and it is a problem, not a strength:
**the hammer's 2.3× knockback throws its quarry +22 units off a 76 reach**,
costing 12% of its contacts and 16 points of win rate — *unless the ultimate
takes the shove back.* Grudgebearer's Crucible pulls and is paid **+7%** for
carrying the shove; Censer's Consecration knocks and is still down **−17%**.
Same type, same shove, opposite ultimates, opposite sign.

Aegis is a third answer to that brief and it is neither of the two:
**it does not fix the reach, it stops needing it.** A relic that is only
dangerous when the foe is inside 76 units has, for the duration, a damage
channel that pays out *when the foe comes to it* — a blow arriving on the arc
is damage the hammer never had to reach for.

That is also why the reflection is the sentence that matters. `wh_survey` §5
measured the vigil channel as the strongest on the row (77% at bank 1.0 against
a 52% control) and it is **entirely defensive** — the plate eats 2.46 dmg/s and
returns nothing. This ultimate is the first thing in the school that converts
the bank into damage without spending it as a number on a hit, which is
Reprisal's job and already taken.

**And it is honest about the cell's cost.** The same survey found the vigil
warhammer doubles down on the type's weakness: a plate BREAKING throws the
attacker at `210 × 2.3 = 483`, more than the hammer's own 379, measured at +44
units. Aegis does not remove that. The relic will shove its quarry away with
its blow, again when its plate breaks, and stand behind a wall in between.
Whether that reads as a fortress or as a relic that cannot close is what the
sweep has to answer.

---

# 3. THE THREE FORKS §1 LEFT OPEN, AND RICK'S CALLS

### 3.1 The name — **AEGIS**, because Bulwark was already taken

§1 called it Bulwark. **Bulwark is Lightkeeper's ultimate** — the vigil
greatsword, "Nova: deals 12 damage — extra knockback". Offered: take the name
here and rename Lightkeeper's (a one-string change, but chain-wide, present in
`01-live`'s sixteen, and in every fight card and posted short), or leave
Lightkeeper alone. Rick left it alone. **Aegis.**

The fighter is **BULWARDEN** — Rick's, from four offered. Bulwark and warden:
the wall, and the one who keeps it. It also keeps the word he reached for first
without taking it off a shipped relic. `id` matches `name`; the two existing
drifts (`oathwound`/Goreshard, `redflail`/Threshmaw) are two traps and a third
was not worth the twenty minutes.

### 3.2 The shield's hp — **THE BANKED POOL, PLUS A FLOOR**

`onSelf.ward`'s value is already a per-relic bank multiplier and `spendWard()`
already exists — Reprisal spends the pool as damage on one shot. Aegis spends
the same pool as a **wall**, and adds a floor so a cast is never dead.

This is the fork that makes the relic a vigil relic rather than a warhammer
that happens to be pink. Today the bank does exactly one thing, and a third
vigil relic that did not give it a second thing would leave the school where it
found it. The survey's numbers set the scale: the plate banks 3.94/s at
multiplier 1.0, sits at a mean of 14.3, and **reaches its 90 cap 0.6% of the
time** — so the bank multiplier is not a balance knob today and becomes one the
moment the ult drinks the pool.

Rejected: *purely what you banked* (a losing relic cannot defend itself — a
downward spiral no other relic has) and *its own fixed pool* (two unrelated
defences on one relic, bank unchanged).

### 3.3 The arc — **ON THE HEAD'S SIDE**, the literal reading

§1 says *in front of the ball* and *rotates with the weapon*. The shield rides
the weapon's own angle, sweeping ahead of the hammer. At `spin 1.6` that is
**3.9 seconds per revolution, the slowest in the game** — so wherever the arc
is pointing, it points there for a long time, and the viewer can read it.

The consequence is the design: **attacking and defending become the same act.**
The side you are swinging is the side you are covered on, and your back is open
for most of a revolution. Rejected: opposite the head (sword-and-board, always
one safe side — too forgiving on a channel already measuring 77%) and a
quarter-turn ahead (unreadable at 1:1 without art explaining the offset).

---

# 4. WHAT THE ENGINE GIVES FREE

- **The pool, the spend and the three endings.** `spendWard()` exists, returns
  what it consumed, and is deliberately *not* `shatter()` with a flag — it does
  not burst at the holder or fling anybody. Aegis calls it and gets a number.
- **"Blocks incoming damage" covers arrows for free.** Every projectile resolves
  through `resolveHit`, so a test placed there catches a bow's shot and a
  hammer's swing with one branch and no special case. Four bow relics exist.
- **The art vocabulary.** `_stWard` already draws the bank as **five countable
  plates** with a near-black value break (a self-buff cannot separate by hue on
  its own school's ball) and a hot rim for time. Aegis is those plates, off the
  shell and out in front. The viewer sees where the wall came from.
- **DoT stays under it, by design.** Hemorrhage and smite do not route through
  the shield gate. A hammer facing bloodsworn or sanctified cannot hide.

# 5. WHAT HAS TO BE INVENTED

**One thing, and it is the arc test.** Every existing defence in this game is a
POOL — ward, and nothing else. Aegis is the first defence with a *direction*,
and direction means the block has to be decided at the CONTACT POINT rather
than at the victim. `resolveHit` already carries `(hx, hy)` for its own
effects; the test is the angle from the victim's centre to that point against
the victim's own `theta`, which is the same quantity `bladeSegments` builds its
segments from. Nothing else in the engine knows where a blow landed.

Everything downstream of the test is arithmetic: eat what the arc can eat, pass
the overflow through to `hurt()` exactly the way the plate does, and hand back
`reflect` of what was eaten through `hurt()` again so the return respects
whatever the attacker is standing behind.

**The zero-burden argument, kept structurally:** all state is `f.ultAegis`,
`null` on every other relic; `tickAegis` returns on its first line; the branch
in `resolveHit` is one `if (foe.ultAegis)`. `engine_ab` over the twenty-two
pre-existing ids is the proof, not this paragraph.

---

# 6. EVERY NUMBER IS A PLACEHOLDER AND IS MARKED AS ONE

```
dmg      the type's, minus what a 77%-win channel is worth. BISECTED, not chosen.
ward     the bank multiplier — and now the ult's magazine as well as the plate
charge   Grudgebearer 18, Censer 15
dur      how long the wall stands
floor    the guaranteed hp so a cast is never dead
bankMul  what a banked point is worth as wall
arc      the angular width. The whole feel of the relic is in this number
r        how far in front of the shell it rides
reflect  the share handed back
```

`arc` and `reflect` are not independent: a wide arc that reflects hard is a
relic that wins by being hit, and the survey says being hit is the one thing
this type does easily. The sweep solves them jointly, the way v40's had to.

---

# Open decisions

1. **The tip wording is Rick's and has not been asked.** Rule 2 of the v40
   handoff, and the thing v40 shipped wrong: `tip_audit.py` does not check ult
   tips at all, and twenty-two relics are unaudited.
2. **The animations and the sound are Rick's and have not been asked.** The
   conjure, the block, the break, and the ult voice.
3. **Does a blocked blow file a CINEMA beat?** Rule 3 says a hit-heavy mechanic
   must declare itself; Aegis blocks a handful of times a cast, not a flurry.
   The current intent is: file the beat with the damage that actually reached
   health, so a fully blocked blow scores itself as the nothing it was.
4. **Does the reflection carry status, crit or knockback?** Intent: none of the
   three. It is a return, not a blow.
5. **What happens to the arc while the wielder is stunned?** `tickHits` empties
   `segs` on a stunned fighter, so its weapon stops — and Aegis rides the
   weapon. Intent: the wall stands still and keeps blocking where it stopped.

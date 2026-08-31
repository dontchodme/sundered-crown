# v51/52 — BUILD BRIEF FOR CLAUDE CODE. The Curse rework and both umbral ultimates, in three separable stages.

**Read `06-docs/v49/curse-rework-v49.md`, then `06-docs/v50/umbral-ults-v50.md`,
then `06-docs/v51/hands-v51.md`, then `06-docs/v52/echoes-v52.md` before this
file.** They carry the measurements; this one carries only what to do with
them.

**The split, Rick's:** Cowork designs and prices, Code builds. Five instruments
are already in `tools/`, all runtime-only, none writes to a build:

```
tools/echo_probe2.py       the curse arms, corrected      — re-run, do not trust this doc
tools/field_and_ult.py     the field, and the ult audit
tools/ultstack_probe.py    what an ult-applied stack remembers
tools/ult_price.py         every ultimate, A/B against its own deletion
tools/umbral_ult_lab.py    nine payloads, both umbral relics
tools/hand_lab.py          §1 priced — chain, hands, knock, blade, window
```

**Nightfell IS now designed** (`06-docs/v52/echoes-v52.md`) and is STAGE 3
below. Stage 1 strips its dead `apply` field and nothing else; do not start
rebuilding it during stage 1.

---

# 0. THE STAGES — WHERE TO START, WHERE TO STOP, AND WHAT MUST BE GREEN BETWEEN

**Each stage is its own commit and its own build file.** Stage 1 moves every
win rate in `verify.py`; stages 2 and 3 each add a set-piece with new objects
in the world. If they arrive as one diff and a gate goes red, nothing tells you
which one did it — and `engine_ab`'s bit-identical check is only meaningful
stage by stage.

```
 #   IN                     OUT                     WHAT CHANGES
 1   sc-thornshear.html     sc-curse.html           the Curse rework (§2). Dirge and
                                                    Eclipse lose `apply:{curse:3}`
                                                    and nothing else
 1b  sc-curse.html          sc-curse.html           three umbral blades re-swept (§2.8)
 F1  --                     --                      FILM: 30s on the new motes + tag
 2   sc-curse.html          sc-gravemourn.html      Gravemourn's ultimate (§3)
 2b  ...                    ...                     blade bisected to ~22-23
 F2  --                     --                      FILM: the window, the hands, the dive
 3   sc-gravemourn.html     sc-nightfell.html       Nightfell's ultimate (§8)
 3b  ...                    ...                     blade to ~13, stamp bisected
 F3  --                     --                      FILM: crackle, ARMED, the chain
STOP
```

**GREEN BEFORE THE NEXT STAGE STARTS**

```
after 1    engine_ab IDENTICAL on the 23 non-umbral relics
           curse_check.py 8/8 (§5)
           verify --n 40 completes; every umbral win rate has MOVED
           row_price shows curse delivering effect, not occupancy
           tip_audit passes with curse's new tip and the two edited ult tips
after 1b   three blades bisected; umbral's three inside the field band (§6)
after 2    gravemourn_relic_probe 9-14 (§5); engine_ab IDENTICAL on the 23 in
           any match containing no cast
after 3    nightfell_relic_probe (§8.4); engine_ab IDENTICAL on the 23 likewise
```

**IF A GATE IS RED, STOP AND REPORT. Do not carry a red gate into the next
stage** — that is the entire reason the work is staged, and a stage-2 failure
diagnosed against a stage-1 regression costs more than the stage did.

**FILM BEFORE YOU TUNE, when the ultimate is a picture** — v43 §13. Both of
these are: a flock of objects converging on a ball at 2500px/s, and a floor
covered in sigils that must read as ARMED or NOT ARMED. Thirty seconds of clip
on placeholder numbers costs four minutes.

**STOP AFTER STAGE 3.** Naming, tips and the intro-card copy are Rick's and are
not blockers — placeholders are in §7 and §8.

---

# 1. THE CHAIN

```
built off   02-chain/sc-thornshear.html          <- the build of record, 26 relics
builders    tools/curse_build.py                 <- new, STAGE 1
            tools/gravemourn_build.py            <- new, STAGE 2
            tools/nightfell_build.py             <- new, STAGE 3
produces    02-chain/sc-curse.html               stage 1 alone
            02-chain/sc-gravemourn.html          stage 2 on top
            02-chain/sc-nightfell.html           stage 3 on top
probes      tools/curse_check.py                 <- new
            tools/gravemourn_relic_probe.py      <- new
            tools/nightfell_relic_probe.py       <- new
sweep       tools/umbral_sweep.py                <- new, three blades
01-live     UNTOUCHED. Not a target.
```

`chain_audit.py --builder curse_build.py` after every carry. **It defaults to
`twinshade_build.py` and will happily audit the wrong inserts and pass.**

---

# 2. STAGE 1 — THE CURSE REWORK

## 2.1 The data

```js
curse: { name:"Curse", maxStacks:3, dur:99, echo:0.08,
         tip:"Adds 8% of a remembered blow per stack" },   // 38 chars, limit 40
```

`maxHpLoss` is **deleted**, not zeroed. `maxStacks` 8 -> **3**: Gravemourn
lands 5.6 blows a fight and cannot fill more (v49 §1), and a small cap is what
narrows the gap between the two archetypes the mechanic serves (v49 §4).

## 2.2 The pool lives on the Fighter

```js
this.cursePool = [];                       // descending, length <= maxStacks
pushCurse(v, n){ ... }                     // push n copies of v, sort desc, trim
curseEcho(){ return sum(this.cursePool) * STATUS.curse.echo; }
```

**Displacement is Rick's rule and it is the good one:** a new stack drops the
WEAKEST, so the pool converges on the wielder's biggest blows. That is the only
term in the design that scales with hit size (v49 §4).

`stacks("curse")` and `cursePool.length` must agree. Assert it.

## 2.3 The three edits in `resolveHit`, in this order

```
a.  dmg computed and rounded                          UNCHANGED
b.  const echo = foe.curseEcho();                     the stacks that ALREADY exist
c.  const dmgBase = dmg;                              <- THE MEMORY. Post-crit,
                                                         post-jitter, POST-sunder,
                                                         PRE-echo
d.  dmg += echo;                                      folded in BEFORE the Aegis
                                                         block, so a wall eats it,
                                                         hit-stop scales with it and
                                                         knockback carries it
e.  ...Aegis block, this.hurt, self.dealt += dmg...   UNCHANGED
f.  onHit loop: if (k === "curse") foe.pushCurse(dmgBase, n);
```

**Every number in `hands-v51.md` is a FLOOR because the lab could not do (d)** —
it paid the echo as a separate `hurt()` after the blow, so it scaled no
hit-stop, carried no knockback and no Aegis wall stopped it. Expect the built
version to read slightly stronger than the doc and re-bisect rather than
arguing with it.

## 2.4 THE MEMORY IS `dmgBase`. NEVER `dmg`.

If the stack remembers the blow's total including the echo it just paid, curse
compounds and goes exponential inside one fight. This is Slagburst's rule —
*consumed then priced* — and it is one line. Put the reason in the comment, not
just the code.

## 2.5 `apply` loses its maximum-life line

```js
if (key === "curse") this.maxHp = Math.max(60, this.maxHp - def.maxHpLoss * n);
```

Gone. `tickStatus`'s closing `f.hp = Math.min(f.hp, f.maxHp);` **stays** — it is
generic and other things could still lower a ceiling.

**Two readers go inert and must not be left claiming they show Curse:**
`maxFrac` in the health-bar draw and `maxFrac` in the relic's own fill. Both
become 1 forever. Delete them or comment them honestly; do not leave a
"maximum life, gone for good" comment next to a constant.

## 2.6 The picture, and there is no HUD chip to put the number on

`v49 §7` said "the chip prints the number." **There is no persistent status
chip in this build** — statuses are on-ball art plus a transient `statusTag` at
the point of contact. So:

- **`statusTag` prints the REMEMBERED TOTAL — the pool sum — not the pending
  echo.** *(v49 §7 first said the echo; measured, the echo peaks at 5-8 across
  the whole school and is not a number worth watching. The pool holds 42-60 and
  peaks at 66-106, fills in three blows, and is what BOTH ultimates read.)*
  `CURSE 96` at the impact, then a detonation for 96, is a story a viewer can
  follow.
- **`_stCurse` is re-cut, because the shipped art is now a lie.** Motes that
  leave and never return said *maximum life, gone for good*. Nothing leaves any
  more. **One mote per remembered blow**, sized by that memory's share of the
  pool, arriving and orbiting rather than escaping. Three motes, countable at
  phone size, and the count IS the stack count.
- Everything stays a pure function of `(side, index, m.t)` through `shellHash`.
  Never `this.rng()`.

## 2.7 Dirge and Eclipse lose one field each

```js
apply:{curse:3}      // Gravemourn's Dirge, Nightfell's Eclipse — DELETE
```

They are worth **-3.2** and **+7.2** against a field median of **+20.4**
(`ult_price.py`). Nothing of value goes. Their tips must lose the "3 Curse
stacks" clause in the same commit or `tip_audit` is lying.

## 2.8 Then re-sweep THREE blades, not two

```
gravemourn  44.10      nightfell  15.83      twinshade  8.30
```

**Twinshade is the one that gets forgotten in a package named after the other
two.** Nobody is touching Triplicate, but it is the ultimate the rework helps
most in the game (+36.0 worth, `ult_price.py`) — three bodies feeding and
cashing one shared pool — and its 8.30 was tuned under the dead curse.

---

# 3. STAGE 2 — GRAVEMOURN'S ULTIMATE

## 3.1 Rick's §1, verbatim

> *when the ult fires for a duration the flails chain gains length and then each
> time it lands a hit an etheral purple hand flys off the hit. the hand soars
> around the arena briefly and then clenches into a fist as it dive bombs into
> the enemy fighter. on contact it applies curse and deals massive knockback.*

## 3.2 The numbers

```
name        REVENANT     Rick's, from a spread of four. That which comes back
kind        "sling" (new). NOT `pull` — pull-and-cash is the Crucible's verb
charge      16          unchanged. Charge is NOT a balance lever here: at 42
                        the ult fires in a quarter of fights and the relic
                        still wins 61.5%
dur         8.0s        NOT free. 4s->16s is 19 points, and it trades against
                        the blade (v51 §2, §8). This is what the blade below
                        is priced against
reachMul    1.35        PER-FIGHTER, for the window. 1.30-1.45 is the plateau;
                        past 1.6 it gets WORSE. Nearly free at the tuned blade
handFly     1.2s        flight, staggered ~0.45s apart
handMul     1.0         NEVER above 1.0. See 4.2
knock       RICK'S      150 / 400 / 700 — ~6 points for the dive-bomb landing
                        like one. Does NOT eat its own window (v51 §4)
ult.dmg     0           the cast opens the window and does nothing else
blade       ~22-23      BISECTED, down from 44.10. Not optional
tip         "Pays out the chain; every blow throws its memory back"   (53/72)
```

## 3.3 What the hand is

On each blow the wielder lands inside the window: **one hand per entry in the
foe's curse pool.** Each hand **takes** its entry as it peels off, so the pool
empties on the blow. On landing, the hand:

1. **deals** exactly the memory it carries (`handMul` 1.0),
2. **applies curse remembering what it just dealt** — a hand that lands is a
   hit, so the memory is passed along rather than grown,
3. **knocks back** hard.

**All four of Rick's clauses are true in this reading and it is the strongest
arm measured** (79.5% against 77.0% for spend-and-empty and 74.5% for
flat-damage hands). It also throws half a hand a fight more, because the pool
is re-parked instead of emptied.

The chain buff is **75% of the ultimate's value and it is defensive** — the foe
lands 10% fewer blows and deals 10% less damage (v51 §1). A viewer who reads
the hands as the whole ultimate has misread which half is winning; that is an
art problem worth solving, not a bug.

---

# 4. THE FIVE THINGS THAT WILL BITE

## 4.1 `w.reach` IS MODULE-LEVEL AND WILL DISARM THE RELIC FOREVER

**The single most likely way this build gets wasted.** `w` is shared by every
match in a page session — the live page runs hundreds against one roster. A
window that writes `w.reach` and misses one restore path does not lengthen one
flail; it **permanently rewrites the relic for every fight afterwards**, and
the symptom shows up in a match that never cast anything.

**Build a per-fighter `f.reachMul`, default 1, and multiply at every read
site.** There are eight, all of the form `f.w.reach * mods.reach` — five in the sim
(chain physics and the hit tests) and three in the renderer. Miss a renderer
one and the picture disagrees with the hit box, which is the hardest class of
bug in this repo to see. `hand_lab.py` swaps `w.reach`
because it is a throwaway page; **the build must not.** Same shape as
Nevermend's `blades` hazard, one field along.

## 4.2 `handMul > 1.0` COMPOUNDS WITHOUT BOUND

The hand deals `mem x M` and re-parks `mem x M`, so at M > 1 every memory grows
by M each time it is thrown. An 8-second window and 1.7 casts a fight hide it —
two or three cycles is not enough for the exponent to show, and it reads as a
merely strong 86.0%. A third cast, a longer window or a future duration buff
uncovers it. **M = 1.0 is a conservation law. Clamp it and say why.**

## 4.3 THE ECHO IS PRICED ON THE TARGET, NOT ON AN ASSUMED ATTACKER

Any blow landing on a cursed fighter pays the echo and remembers its own
damage. **Do not guard on `self === owner`.** Twinshade's shades are real
`Fighter` objects carrying `onHit:{curse:1}`, resolved on the shade and
credited to the caster afterwards in `tickShadeHits` — a guard on the caster
makes 9.3 blows a fight invisible. That exact bug produced a confidently
formatted, entirely wrong finding in this session's first pass (v51 §3), and it
is also PoE's own rule: *hit by any source*.

## 4.4 HANDS IN FLIGHT WHEN THE FIGHT ENDS

A hand must not resolve on a corpse or after `m.over`. `hand_lab` models this
and it is 20-30% of hands spawned. Also: if hands are routed through `shots`,
`spawnShot` **shifts a live one at `maxLive` 64** — decline and count the
refusal, never shift. Bloodhunt's fork branch is the precedent.

## 4.5 THE BISECTION SURFACE IS NOT THE USUAL ONE

`dmg` now moves three channels at once: blade damage, the pool (which is made
of blade damage), and hand damage (which is a memory). **The response is
superlinear and a single-pass bisection assuming monotonic linear response will
land in the wrong place.** Sweep wide and plot it. v50 §6 registered this
before it was seen; v51 §8 is what it looks like.

---

# 5. THE PROBES — ONE CHECK PER SENTENCE

`tools/curse_check.py` (layer 1):

1. **A stack remembers the blow that applied it**, post-crit and post-sunder,
   and **never** the echo — assert a pool entry never exceeds the largest
   `dmgBase` the wielder has dealt.
2. **The pool is the top K**, and a new stack drops the weakest.
3. **`stacks("curse")` equals `cursePool.length`**, always.
4. **A fresh stack does not pay on its own blow.**
5. **The echo is stopped by an Aegis wall and absorbed by a Ward**, because it
   is folded into the hit rather than dealt beside it.
6. **A shade's blow feeds and cashes the pool** — the §4.3 check, written as a
   Twinshade match.
7. **`maxHp` never moves in any match**, for any relic. The old channel is gone
   and nothing may quietly re-open it.
8. **Delivered against nominal.** The general form of v47's defect: for every
   status, damage delivered with the channel minus damage delivered with it
   deleted. Curse's ratio goes from 3% to ~100%; **the other seven have never
   been measured and this is where that check belongs.**

`tools/gravemourn_relic_probe.py` (layer 2):

9. **The chain really lengthens, and only for the window, and only for this
   fighter** — assert the other 25 relics' reach is untouched during and after,
   in the same page session. §4.1.
10. **One hand per pool entry**, and the pool is empty the instant they leave.
11. **A hand deals exactly what it carries** and re-parks exactly that.
12. **No hand resolves after the fight ends or on a corpse.**
13. **The ult files a BEAT** for the director — rule 3, seventh relic running.
    The hands land through their own path, so nothing else in the frame knows
    the dive happened.
14. **THE SOUND IS RENDERED AND MEASURED IN AN `OfflineAudioContext`.**
    `SFX.play` returns on its first line headless and swallows its exceptions;
    v42 shipped a silent ultimate through every green check in the repo. There
    are three voices here — the chain paying out, the hand peeling off, the
    fist landing. Render all three.

---

# 6. THE GATES

```
engine_ab       IDENTICAL on the 23 non-umbral relics, layer 1 AND layer 2
chain_audit     --builder curse_build.py / gravemourn_build.py
verify --n 40   every win rate moves; the duration-band check is KNOWN to fail
                at the tip -- do not credit this build with it either way
tip_audit       curse's tip loses maxHpLoss and gains echo; Dirge and Eclipse
                lose their "3 Curse stacks" clause. 40 for status, 72 for ult
row_price       curse must now show delivered effect, not occupancy
frame_probe / post_identity
```

**Registered prediction, this build's job to falsify:** *after layer 1 the
three umbral relics land inside the field band (50.0% mean, 6.4% sd) with no
ultimate changes beyond the two stripped `apply` fields; and through layer 2's
bisection Gravemourn's hand damage stays in the 120-140 band while its hand
COUNT rises as the blade falls.* If hand damage tracks the blade instead of
staying flat, the self-stabilising claim in v51 §8 is wrong and the window and
blade have to be re-priced together.

---

# 7. WHAT NOT TO DO

- **Do not keep `kind:"pull"`.** Pull-and-cash is the Crucible's verb and
  Gravemourn is not allowed to be a second Crucible. The `pull` branch in
  `fireUlt` has exactly one user; leave the branch, change the relic.
- **Do not touch Triplicate.** It is the ultimate the rework helps most and it
  needs no code at all — only a blade re-sweep.
- **Do not build Nightfell during stage 1 or 2.** It is stage 3, §8, and it
  is built on top of Gravemourn's file, not beside it.
- **Do not give an ult-applied stack something better to remember.** Measured
  at two caps and three rules; worth 0.7 to 2.7 points, all inside the noise
  (v49 §5b). A full pool has no room. Do not re-litigate it in code.
- **Do not write `w.reach`.** §4.1.
- **Do not touch `01-live`.** Ten relics behind.
- **Do not fix `_burst` or `_tone`.** Twenty-six shipped voices.
- **Do not let the fight card back in.**

---

# 8. STAGE 3 — NIGHTFELL'S ULTIMATE

Built on `sc-gravemourn.html`, not beside it. Design and every number:
`06-docs/v52/echoes-v52.md`.

## 8.1 Rick's §1, and the two clauses that changed

> *nightfell crackles with purple electricity. for the duration of the ult when
> it lands a hit the hit leaves behind an echo bomb (thinking a pentagram
> imprinted on the battlefield) the echos slowly begin to crackle with the same
> purple electricity and then explode. dealing damage, applying curse and
> knocking back enemy fighters in its area.*

**"then explode" became "then ARM"** — Rick's call once the catch rates were on
the table. A timer catches 8-38% of its bombs; a landmine catches 69-86% and
lets the figure be small. **"applying curse" is gone** — measured at exactly
+0.0% in the shipped arrangement (v52 §3e). The figure READS the memory; it
does not write to it.

## 8.2 The numbers

```
name        DEADFALL   Rick's, from a second spread after the first was
                       rejected whole. A trap rigged to drop on whatever
                       disturbs it — it springs, it does not fire
kind        "sigil" (new). NOT `nova` — it does not nova any more
charge      15         unchanged
dur         8.0s       window. 4s to 16s is 16.4 points; 8s is what the blade
                       below is priced against
figure      ONE per blow landed inside the window: five charges evenly spaced
                       on a 60-unit ring centred on the contact point
arm         ~1.6s      of crackle, then live
life        NONE       a live charge waits until something walks into it.
                       Permanent is worth +6.4 over a 2s life AND is one
                       sentence instead of a number and a fade
trigger     FOE ONLY   §8.3
radius      70         per charge
payload     each charge deals `stamp / 5 * M`, where `stamp` is the SUM of the
                       foe's curse pool at the moment the blow landed.
                       M ~= 0.3, BISECT. No curse application
push        250        per charge, radially outward. Rick's call on legibility;
                       it costs ~23% of the chain and 800 costs half
blade       ~13        BISECTED, down from 15.83
tip         "Stamps sigils that arm, then take whatever walks in"  (51/72)
result      5 figures a fight, ~25 charges, ~18 walked into, chains of 4.9
            of 5, and 50.4% against a 50.0% field
```

## 8.3 The four things that will bite, and two are new

**a. THE CHAIN MUST SPAN FRAMES.** When a charge fires it shoves the ball, and
the shove is what carries it into the next charge. If the detonation handler
loops over every remaining charge in the same frame, the whole figure goes off
at once and **there is no chain to see** — the mechanic still "works" by every
number and is invisible. Detonate on a per-frame proximity test, exactly as
`bomb_lab.py` does, and have the probe assert consecutive detonations are at
least one frame apart.

**b. THE FIGURE IS READ-ONLY ON THE POOL.** It copies the sum at spawn. It must
not push to the pool and must not spend it — Gravemourn's hand takes and
returns; this one only reads. A build that re-applies curse from a charge
recreates the +0.0 clause the design deleted.

**c. FOE ONLY, and the caster is standing in exactly the same place.** The
charges are planted where blows land, so a caster-triggering figure eats 48% of
its own charges (v52 §3c). This is not a tuning knob, it is a bug if it
happens.

**d. LIVE CHARGES ARE PER-MATCH STATE.** They never expire, so they must live on
the match and be discarded with it. Anything hung off `w` is the §4.1 hazard
again. And if they are routed through a pooled array with a `maxLive` ceiling,
**decline and count the refusal, never shift a live one out.**

## 8.4 The probe — `tools/nightfell_relic_probe.py`

1. **One figure per blow inside the window**, five charges, on a ring of the
   stated radius — measured off positions, not recomputed from the config.
2. **A charge does not exist before its arming time** and cannot be triggered
   during the crackle.
3. **No charge ever fires on the caster**, in any match, at any separation.
4. **No charge expires.** Count planted, walked-into and still-standing at the
   end; the three must add up with nothing lost.
5. **The pool is unchanged by the whole ultimate** — same length and same
   entries before and after a figure detonates.
6. **The stamp equals the pool sum at the moment the blow landed**, not at the
   moment the charge fires.
7. **The chain spans frames** — §8.3a, asserted on the timestamps.
8. **THE SOUND IS RENDERED AND MEASURED IN AN `OfflineAudioContext`.** Three
   voices: the stamp, the arming, the detonation. v42 shipped a silent
   ultimate through every green check in the repo.
9. **The ult files a BEAT**, and so does a chain of four — the director cannot
   see a floor charge going off.
10. **ARMED READS DIFFERENTLY FROM ARMING.** Not a probe check — a filmstrip
    check, and the one thing that decides whether any of this is visible. With
    a fuse the crackle was a countdown; with a mine it is an arming animation,
    and a viewer who cannot tell a live sigil from a crackling one cannot see
    the mechanic at all.

---

# Open decisions — Rick's, and the build can start without them

1. **KNOCKBACK.** 150 / 400 / 700. ~6 points for the dive-bomb landing like a
   dive-bomb; the warhammer pays the same tax on purpose. Placeholder 400.
2. **THE WINDOW, which is now coupled to the blade.** 8s is what blade 22-23 is
   priced against. 16s is ~19 points more and needs a smaller blade again; 4s
   buys blade back. One decision, not two. Placeholder 8s.
3. ~~**BOTH ULT NAMES.**~~ **SETTLED.** Gravemourn's ultimate is **REVENANT**,
   Nightfell's is **DEADFALL**, both Rick's from offered spreads — Nightfell's
   from a second spread after the first, entirely ecclesiastical-Latinate, was
   rejected whole. Tips are mechanic-first, both in §3.2 and §8.2 and both
   inside 72. `STATUS.curse.tip` is `"Adds 8% of a remembered blow per stack"`
   (38/40).

   **`blurb` is NOT copy anyone sees** — nothing in the game or the shorts
   pipeline reads it (v52 open decision 5). The copy that ships is
   `w.ult.name`, `w.ult.tip` (<=72) and `STATUS.curse.tip` (<=40), and all
   three are now written.
4. **HOW THE CHAIN BUFF READS.** It is 75% of the ultimate's value and it is
   currently visible only as a longer chain. Art problem, not a build blocker.

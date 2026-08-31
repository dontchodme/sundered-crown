# v47 — THORNSHEAR / THE WINNOWING, BUILT. Twenty-six relics, one new mechanic, and one bug that made 89% of the ultimate disappear on the wall it had just bounced off.

**2026-08-30, Claude Code.** The split was Rick's: *"lets design and plan here
and let code build it."* Cowork surveyed the type, priced every sentence of §1
and put four forks to him; this document is the other half. Read
`twinblade-survey-v47.md`, then `kunai-design-v47.md`, then `BUILD-BRIEF.md`,
then this.

```
02-chain/sc-thornshear.html      THE RELIC — 26 relics, built off the tip
tools/thornshear_build.py        17 inserts, all of them audited
tools/thornshear_relic_probe.py  31/31
tools/thornshear_sweep.py        the bisection, and the share
tools/kunai_art_lab.py           four kunai, rendered before he was asked
```

**IT IS NOT THE BUILD OF RECORD YET.** `app/main.js` and CLAUDE.md §0 still
point at `sc-paradox-ignition.html`, and they should until the growth schedule
is settled and `verify` has run at the tuned number. Everything else is done.

---

# 0. THE TWO INSTRUMENTS, RE-RUN AT THE TIP — AND THE DESIGN DOC MOVED IN TWO PLACES

The brief's item 2: *"Re-run both instruments at the tip. If any number in the
design doc has moved, the design doc is wrong and it is yours to say so."*

```
tools/kunai_probe.py        12/12    every load-bearing number reproduced
tools/twinblade_survey.py   20/21    one FAIL, and it is the sample, not the finding
```

**THE CENSUS HELD.** 69.8% of every landed kunai has bounced at least once;
the same fan with no bounce budget lands 1359 against 2479; a nine-fold range
of fan width lands within x1.13 of itself; 0.1% of kunai are spent on a wall
against a bow's 82%. Every sentence the design rests on is still true.

**WHAT MOVED, ONE: VERDANT'S CHANNEL IS NOT THE WEAKEST OF THE THREE.** The
design doc §5 prices entangle on this type at **+7.6% delivered, 68.8% win**
and concludes *"the school's channel will not carry this relic, so the ultimate
has to."* Re-run at the tip, against the same 24-relic field:

```
school      status      dealt/s   taken/s     win   vs no channel at all
dwarven     sunder         7.89      4.69   76.0%          +20.3%
verdant     entangle       7.00      4.56   75.5%          +19.8%      (doc: +7.6%)
sanctified  smite          5.87      4.86   69.3%          +13.5%
```

Verdant is second by half a point, which at n=192 is a tie with dwarven — not
the weakest of three. **The conclusion it was used to support is weaker than
the doc states**: the ultimate does not have to carry the whole relic. It is
still true that the ultimate is what makes this cell interesting, and §5 below
prices it at 4.5 points of blade.

**WHAT MOVED, TWO: THE LIVE ENTANGLE LADDER IS UNSTABLE AT n=4 PER MODE.** The
survey's own check *"entangle cuts a melee foe's blows harder than a ranged
foe's"* FAILED on the re-run: spin −2.6% against ranged −11.0%, where the doc
reports ranged +1.2% and spin −8.3%. **The CAP table — the one the design
actually argues from — reproduced cleanly**, and it is the one that matters
because an ultimate that pinned the status is buying the ceiling:

```
foe mode     doc (off -> cap)    re-run (off -> cap)
ranged             +3.3%               -3.3%
swing             -33.1%              -36.2%
spin              -16.0%              -21.0%
chain              -9.9%               -6.8%
```

Swing worst, ranged least, by a factor of ten. **The concentration argument
stands and the registered prediction stays registered.** Four foes a mode is
too thin for the uncapped ladder; do not read that row from either run.

---

# 1. THE FIVE DECISIONS THIS BUILD MADE THAT THE BRIEF DID NOT

## 1.1 `spawnKunai`, NOT `spawnShot` — and the brief says otherwise

The brief's §7: *"Do not build the fan as new machinery. `spawnShot(f, angle)`
already takes the angle."* It is right that the fan is a loop, and wrong that
`spawnShot` is the place to run it.

**`spawnShot` READS `f.w.shot`, AND A `shot` BLOCK ON THIS RELIC IS A TWINBLADE
THAT FIRES ALL FIGHT.** `tickFire` gates on `f.w.shot` and on nothing else —
that is the design doc's own §4 finding — so reusing `spawnShot` means adding a
guard inside a function all five bows live in, in order to borrow twelve lines.

`spawnSpike` is the precedent and the argument is already written in the
engine: *"Deliberately NOT `spawnShot`: that function needs `f.w.shot`, and
this relic has none."* So:

> **THE ENGINE'S SHARED RANGED PATH IS UNTOUCHED BY THIS RELIC.** `tickFire`,
> `spawnShot`, `relicShot`, `fireCd` — not one character. The kunai fly, parry,
> bounce and land through `tickShots`, which is the part that had to be shared
> and is shared.

**AND THE SPAWN GEOMETRY IS THE MEASUREMENT'S.** `kunai_probe` looses from the
shell edge (`R + 6`); `spawnShot` looses from the blade tip (`R + reach`), 62
units further out. Every number in the design doc is the first geometry. Using
the second would have made this build a different experiment from the one that
priced it — and it is also the wrong picture: the blades are GONE, so there is
no tip for anything to leave from.

## 1.2 §3.3 OF THE BRIEF IS HALF WRONG, AND THE HALF THAT IS RIGHT IS WORSE THAN IT SAYS

> *"`shot.life` and the `w.shot` mode gate are both waking up here."*

**The mode gate does not wake up.** This relic has no `shot`, so v39 open
decision 4 is exactly as inert as it was for the last six sessions.
**`shot.life: 3.4` also stays dead config on all five bows** — the kunai carry
`ult.life`, not `shot.life`.

What DOES wake up is the branch those knobs were pointing at, and it is worth
more attention than the config was. `tickShots`' `s.life <= 0` arm has never
fired in the history of this game (`bow_survey` §4: *"a shot travels 1292 units
in its life and the longest wall is 800"*), and it is now **the modal death of
a kunai at 33.3%.** A third of this ultimate's population dies down a code path
with no shipping history at all. It got its own picture (§3.3 below) for that
reason.

## 1.3 THE BOUNCE BUDGET IS SHARED BETWEEN THE WALL AND THE PARRY

Rick's fork — *"deflect AND empower"* — says a blade must not kill a kunai. It
does not say a blade must never kill one. One budget for "how many times can
this come off something" means a kunai that has spent it dies on the next blade
exactly as an arrow does: **the counterplay is delayed by three, not removed.**
Measured over 44 real casts, **16% of all growth is the foe's own defence.**

## 1.4 `parryArm`, WHICH IS NOT A DESIGN KNOB

A kunai batted by a blade is still inside that blade's radius on the next
frame. Without a hold-off it racks a rung every frame against a blade it is
merely passing. `arm` is the field `tickShots` already gates both hit branches
on, so this costs no new state and no new branch. 0.06s.

## 1.5 THE SOUND AND THE BEAT SHARE ONE 0.4s GATE, AND THE NUMBER BEHIND IT MOVED

The brief expected the top rung to be rare — `kunai_probe` measured 19.1% of
kunai reaching a third bounce. **It flew CONSTANT kunai.** A growing one is
fatter every time it comes off something and is parried more, and on this build
**55% arrive fully grown — 38 a cast, not 13.**

A chime ten times a second is a wash, and a beat that often would evict the
fight's own: `m.beats` is capped at 600 and SHIFTS. So the top rung still
flashes every time, and the SOUND and the BEAT share one rate limit. 6.4 ult
beats a cast, measured.

**AND THE WINDOW DECLARES ITS DENSITY.** Not in the brief, and it should have
been: `beat()`'s own comment says *"anything that puts extra CUTS on the floor
belongs in this loop"*, and this window puts ~24 landed projectile hits on the
floor in four seconds — more than the spike storm, which is the relic that
forced `crowdMul` to exist. `crowdMul: 10` is a placeholder at the storm's own
value and wants the storm's own measurement (`beat_dist.py`, cut preference
inside the window against outside).

---

# 2. WHAT THE ULTIMATE IS, IN THE ENGINE

```
bladeSegments   `if (f.ultWinnow) return [];`   — §1's first sentence, and ONE
                mutation reaching all four consumers: tickHits lands nothing,
                _clankPair finds no crossing, tickShots' parry has no segment
                to bat with, tickWeapon has no tip to record.
tickWinnow      the window, the cadence, the fan, and the REFUSAL.
spawnKunai      twelve lines beside spawnSpike.
kunaiRung       what a ricochet does. ONE definition, both reflection paths.
tickShots       two branches, both `if (s.kunai)`: the parry deflects and
                empowers instead of killing; the wall advances a rung.
beat()          crowd + crowdMul while the window is open.
```

All state is `f.ultWinnow` and `f.winnowFade`, and both are null/0 on every
other relic and on this one outside its own window. `engine_ab` over the
twenty-five pre-existing relics is the proof of that, not this paragraph —
**1800/1800 matches identical, field for field.**

---

# 3. THE BUG, AND IT IS THE FINDING OF THE SESSION

## 3.1 A PROJECTILE THAT GROWS IS THE FIRST THING IN THIS GAME WHOSE RADIUS CHANGES AFTER IT IS PLACED

`tickShots`' wall branch clamps the shot to the boundary and then reflects:

```js
if (s.x < n + s.r){ s.x = n + s.r; s.vx = Math.abs(s.vx); hitWall = true; }
```

and the `spent` branch, four blocks later, asks the same question:

```js
if (!dead && (s.life <= 0 || s.x < n + s.r || ...))
```

**Both are written against `s.r` at the moment they run, and the rung-up
between them multiplies `s.r` by 1.25.** So a kunai that grew on the wall it
had just bounced off was one pixel outside itself, and was spent on the same
frame it ricocheted.

**IT WAS NOT SUBTLE ONCE IT WAS MEASURED, AND IT WAS INVISIBLE BEFORE:**

```
                        with the bug        after the clamp
kunai dying on a wall          89%                     13%
median age                   0.33s                   2.56s
rungs 0/1/2/3          40/500/55/33            19/47/107/242
peak in flight                  20                      55   (predicted 50)
landed per cast                ~8                      ~24
```

Every one of those numbers is the same missing clamp. The fix is two lines in
`kunaiRung` — grow, then give back the space the growth took:

```js
const AR = CONFIG.arena, ins = this.inset;
s.x = clamp(s.x, ins + s.r, AR.w - ins - s.r);
s.y = clamp(s.y, ins + s.r, AR.h - ins - s.r);
```

**AND IT BELONGS IN `kunaiRung`, NOT IN THE BRANCH THAT FOUND IT.** A parry
inside `s.r * growR` of a wall puts a grown kunai outside the hall with nothing
having touched it. One function owns the growth, so one function owns its
consequences.

> **THE GENERAL FORM, for the next relic that changes a live object's size:**
> every geometric test already written against that object was written against
> the size it had. This is CLAUDE.md §4.2 (`f.pinV` — "a held object's stored
> state is not its current state") with the tense reversed: **a mutated object's
> NEW state invalidates every clamp computed from its old one.** Grep the field
> and read every site.

## 3.2 THE THREE PICTURE FAULTS THAT WERE BUILT AGAINST RATHER THAN FOUND

**THE CEILING.** `spawnShot` honours `maxLive` by deleting the oldest live
shot — on a bouncing kunai, one vanishing in mid-air. `tickWinnow` DECLINES, by
whole volleys, and counts the refusals. Half a fan is its own picture fault: an
asymmetric spray with no cause a viewer can see.

**AND THE COUNT IS A DESIGN CHECK, NOT A LOG.** At fan 5 / cadence 0.25 the
probe refused 9090 of 11050 looses — a design permanently at the ceiling is a
design whose cadence is set by a constant in `CONFIG`. The shipping pair is the
one arm on the board that refused nothing. **The builder now refuses to write a
saturating configuration at all**, arithmetically, before any fight runs:
`fan x 2 x life / cadence` against 64.

**THE STALE RIBBON.** `f.tips` is fed from `bladeSegments`, which is empty for
the whole window — so two swing-arc ribbons would have hung motionless in the
hall for four seconds. Cleared at the cast; they grow back from empty when the
blades do.

**THE GHOST BLADE.** A blade drawn where no blade is live is the same fault
pointing the other way, and it is exactly v42's silent ultimate and v43's stuck
hold: a picture and a simulation disagreeing with no number between them.
`winnowFade` SNAPS to 1 at the cast and eases back over 0.25s AFTER the window,
so the disagreement can only ever run the safe way round — never a blade drawn
that cannot hit, only a blade drawn small that can. Measured: `winnowFade === 1`
on 1265 of 1265 in-window steps.

## 3.3 AND EXPIRY GOT A PICTURE, BECAUSE IT IS A THIRD OF THE POPULATION

See §1.2. A grown kunai reaching the end of its life and simply blinking out is
the same silent fault as one deleted at the ceiling. It comes apart into leaf
instead, larger the more it grew.

---

# 4. `s.snap` IS SET ON EVERY REFLECTION — AND NOTHING READS IT

The brief's §3.4: *"Every new reflection path this build adds must set it, and
the probe must assert it, or a kunai at 60fps will cut the corner it just
bounced off."* Both paths set it and the probe asserts it. **But the flag is
inert, and that is worth knowing rather than discovering:**

```
LERP_FIELDS.shot is ["x","y"], and CINE.snapObj copies only NUMBERS
```

so a boolean is invisible to the interpolator. Nothing in the engine reads
`s.snap` — grep it: one write in the shipped wall branch, one in `kunaiRung`,
zero reads. What actually saves the picture is structural: **both reflections
change VELOCITY and leave POSITION where the step put it**, so the previous and
current positions are both on the legal side of the surface and there is
nothing to tween through.

The flag is kept because it is the convention and because the day something
does read it, this build will already be correct. `thornshear_relic_probe [7]`
asserts both halves — that it is set, and that it is decorative.

---

# 5. THE NUMBERS

## 5.1 THE BISECTION, WITH AN ESCALATING SAMPLE

v43 §14.1's cheap win, unclaimed for four sessions and taken here: a bisection
spends the same number of fights on step one — where the interval is twelve
damage wide and the answer is obvious — as on step seven, where it is 0.1 and
the answer is the point. The sample now rises geometrically with the step.

**1050 fights a bisection instead of 2400, at the same precision**, and the
last step is a 300-fight sample where the flat version's was 150.

```
                       dmg at 50% against all 25
the blade alone (charge 1e9)        14.45
the blade, shipping ultimate         9.95
```

> **THE WINNOWING IS WORTH 4.5 POINTS OF BLADE — 31% of the weapon.** The
> Stasis Field was worth about nine points of a flail's 35. This is a smaller
> relic paying a larger share.

## 5.2 THE COLUMN THAT IS ACTUALLY BEING CHOSEN

The bisection compensates, so no arm is stronger than another. What the arms
choose is **what share of a cast is carried by kunai that have grown**:

```
at dmg 9.95:  53.6s mean, 2.4 casts, 59% of all damage from kunai (85 a cast)

  rung    hits   damage   of the ult   of the fight
     0     9.1     19.2           9%             6%
     1    13.9     43.9          21%            13%
     2    14.8     75.4          36%            22%
     3     8.7     68.9          33%            20%

  GROWN KUNAI CARRY 91% OF THE ULTIMATE AND 54% OF THE FIGHT.
```

**That is the number to put to Rick, and it is not a win rate.** Nine percent
of this ultimate is the thing that was fired; ninety-one percent is what the
hall did to it afterwards. §1's fourth sentence is not decoration on the
ultimate — it is very nearly all of it.

## 5.3 THE CEILING, IN A REAL FIGHT

```
predicted steady state  50 = fan 5 x 2 bearings x life 3.0 / cadence 0.6
measured peak            55-58 objects in flight, of a shared ceiling of 64
volleys refused           0, over 44 casts and 6 foes
```

**Nine of sixty-four is not a lot of headroom**, and the ceiling is shared with
the foe's own arrows. It has never been touched in measurement, but a bow with
a faster cadence than Ironhail's would eat into it. If the growth sweep raises
`life`, the cadence must move with it — the builder enforces that arithmetic
and will refuse to write the combination.

---

# 6. THE GATES

```
thornshear_relic_probe   31/31   one check per sentence of §1, against the build
engine_ab (6 relics)     150/150 identical
engine_ab (all 25)      1800/1800 identical, field for field
chain_audit             17/17 inserts survive  --builder thornshear_build.py
kunai_probe (tip)        12/12
twinblade_survey (tip)   20/21   §0 above
verify --n 40            NOT YET RUN at the tuned dmg — see §8
```

**THE CHAIN TABLE IN THE BRIEF ASSUMES A CARRY THAT DOES NOT EXIST.** It names
`sc-thornshear-frame.html` as a separate tip, the way `sc-vinesower.html` and
`sc-vinesower-frame.html` are two links. This relic was built **off the tip
itself** — `sc-paradox-ignition.html` already carries the frame, the post
chain, the fields, the pace, the hit-stop fix and the ignition open — so the
relic build IS the tip and there is nothing above it to carry into.
`chain_audit --relic X --tip X` is therefore trivially green, and its real
value here was proving its regex can see all seventeen `r'''`-prefixed inserts,
which in v43 it could not.

---

# 7. RICK'S SEVEN, AND WHERE THEY STAND

```
the cell            SETTLED   verdant x twinblade, from four priced candidates
the ult mechanics   SETTLED   §1, plus two forks (deflect-and-empower, knock 260)
the ult name        SETTLED   THE WINNOWING, from four
the fighter name    SETTLED   THORNSHEAR, from four
the scrunch card    SETTLED   2026-08-30, his own wording, off the first-look clip
the ult animations  PART      the kunai is his pick from four rendered candidates
the ult sound       OPEN      written, rendered and measured — but not yet chosen
                              from a spread
```

**THE CARD IS HIS OWN WORDING**, unprompted, off the first-look clip:

> *"fires a fan of kunai that ricochet. ricochets deal bonus damage"*

63 of 72 characters, verbatim except for the two capitals every other tip in
the roster carries. It is also the better line: the first cut spent a third of
the budget on the duration — a number the viewer cannot act on and can watch
for themselves — and never said what the mechanic was. His says the mechanic
twice.

**THE KUNAI IS HIS PICK FROM FOUR, AND THE BRIEF FOR IT WAS FIVE WORDS.**
Watching the first look: *"the blades dont look like kunai"*, then *"kunai
first, leaf second."* What shipped was a pointed ellipse with a midrib — the
verdant flavour carrying the whole silhouette and the weapon carrying none of
it. `kunai_art_lab.py` rendered four, all kunai in silhouette, differing in how
the leaf gets in; he took **B, the leaf-bladed kunai** — kunai furniture, and
the blade itself is the leaf.

> **THREE THINGS SAY KUNAI AT THIRTY-SEVEN PIXELS**, and the shipped shape had
> none of them: a TANG (the object is longer than its blade and the back half
> is dark), a RING (the only hole on screen, and it reads at four pixels), and
> a SHOULDER (a kunai's blade widens abruptly and then tapers dead straight —
> a leaf's widest point is halfway and its edges are convex).

**AND THE SHEET WITH FOURTEEN ON IT IS WHY IT WAS A SPREAD.** A silhouette that
reads alone can still turn to soup in a crowd of fifty, and the shape sheet
cannot see that. Both are in `05-reference/v47/`.

---

# 8. WHAT IS LEFT

1. **THE GROWTH SCHEDULE IS UNMEASURED.** `growR 1.25 / growDmg 1.5 /
   growKnock 1.3` are the only numbers in the block nothing has measured —
   `kunai_probe` flew CONSTANT kunai, so every census number in the design doc
   is this schedule at 1.0/1.0/1.0. `thornshear_sweep.py [3]` sweeps `growDmg`
   against `life` with the blade re-bisected per cell and reports the share
   table from §5.2 for each. **That table is the thing to put to Rick.**
2. **`bounce` x `life`, AND IT IS A PICTURE DECISION.** Above 3 is inert at
   life 3.0 — bounce 6 and bounce 3 return identical numbers, digit for digit.
   A fourth rung means `life` goes up and kunai visibly stay in the hall
   longer. Both arms are in the sweep and both want a rendered clip, not a
   number.
3. **THE SOUND HAS NOT BEEN OFFERED AS A SPREAD.** The cast, the volley and the
   rung are written, rendered in an `OfflineAudioContext` and measured (peak
   0.72 / 0.08 / 0.10, and the cast hands over rather than ending — late rms
   0.027 against the Stasis Field's 0.048). v43's rule is that a spread lands
   the voice in one round trip where four serial guesses did not. Three casts
   and three rungs, rendered, is the next ask.
4. **`crowdMul: 10` IS THE SPIKE STORM'S NUMBER, NOT THIS RELIC'S.** §1.5.
5. **THEN: `verify --n 40` AT THE TUNED NUMBER, AND THE FLIP.** `app/main.js`
   and CLAUDE.md §0 point at `sc-paradox-ignition.html` and should move only
   after that. Expect 12/13 — the duration-band check is KNOWN to fail at the
   tip and this relic must not be credited with it either way.
6. **THE REGISTERED PREDICTION IS STILL OPEN.** The design doc §9 predicts this
   relic's win-rate spread across the roster will be the widest in the game,
   strongest against the seven greatswords and weakest against the five bows.
   The bisection's per-foe column has the data; nobody has read it out yet. If
   the spread is inside the existing band, **say so and strike the
   concentration argument** rather than explaining it away.

---

# Open decisions

1. **THE THREE-RUNG CEILING.** Carried from the design doc, still open, and now
   priced on both sides: at life 3.0 nothing reaches a fourth bounce, and 55%
   of kunai already arrive fully grown — so a fourth rung is a longer,
   slower-emptying hall as much as it is more damage. Sweep arms exist; the
   choice wants a clip.
2. **NINE OF SIXTY-FOUR IS THE WHOLE HEADROOM.** §5.3. The population is
   arithmetic and the builder enforces it, but `CONFIG.shot.maxLive` is shared
   with the foe and is a chain-wide constant. Raising it is Rick's.
3. **`spawnShot` STILL SHIFTS FOR EVERY OTHER CALLER.** Quarrelstorm looses 14
   at once and Ironbloom 9. Chain-wide, and unchanged here — the third session
   this has been named.
4. **`s.snap` IS A DEAD FLAG IN THE SHIPPED ENGINE.** §4. Three writes, zero
   reads. Either something should read it or it should go; leaving a
   defensive flag that defends nothing is how the next person believes they
   are protected.
5. **`cell_survey`'s OCCUPANCY COLUMN, and now the SURVEY's own delivered-effect
   column.** The design doc's +7.6% for verdant did not reproduce (§0). Two
   different tools have now mispriced this cell in two different directions
   within one session.

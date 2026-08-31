# v54 — DEADFALL IS BUILT. Stage 3 of three, and the umbral school is finished. **Five things nearly shipped broken and all five were pictures. Three were caught by rendering, and the two that were not were caught by Rick watching — including one the engine had already written a warning about, for a different object, three lines from where it went wrong.**

**2026-08-31.** `tools/nightfell_build.py`, `02-chain/sc-gravemourn.html` →
`02-chain/sc-nightfell.html`. Design: `06-docs/v52/echoes-v52.md`. Plan:
`06-docs/v51/umbral-build-brief-v51.md` §8. What stage 2 left it:
`06-docs/v53/grasp-build-v53.md` §9.

```
DEADFALL   a window; every blow inside it stamps ONE PENTAGRAM where the blow
           landed, carrying what Curse remembers about the quarry at that
           instant. It crackles for 1.6s, goes live, and then WAITS —
           permanently — for the foe to walk within 110 of its centre. Then it
           deals the whole of what it remembers, in one number, and shoves at
           250. FOE ONLY. Blade 15.83 -> 12.27.
```

**THE FIGURE IS ONE MINE, AND THAT IS RICK OFF THE FIRST BUILD.** It shipped
first as five charges on a ring, because v52 §3b measured that ring as the
only arrangement that chains. He watched it:

> *"i can tell the difference between armed and arming pretty easily. but what
> isnt legible is the explosion itself. currently each pentagram spawns a
> bunch of mini bombs. not opposed to this direction but my vision was the
> pentagram was 1 large mine not a cluster of small ones."*

Five charges at `stamp/5` put five 3-damage numbers over the ball across 42
milliseconds. **Every number was right** — the damage, the win rate, the chain
counters, the beats, sixteen green probe checks — and it read as noise. §7
below is what it cost and what it bought.

---

# 1. WHAT WAS BUILT, AND WHAT IT COST

| | |
|---|---|
| `kind` | `"sigil"` — new. NOT `nova`; Eclipse is gone, art included |
| `dmg` at the cast | **0**. Nothing resolves; the cast opens a window |
| `dur` | 8.0s |
| `points` / `ring` | 5 points on a 60-unit ring — **a drawing.** One figure per blow, one mine per figure |
| `rad` | **110**, on the figure's centre. The whole pentagram is the hit box |
| `arm` | 1.6s of crackle, then live |
| `stampMul` | 0.3 of the pool sum at the blow, **undivided** — one blast, one number |
| `push` | 250, radially outward |
| `apply` | **gone, and it stays gone** — v52 §3e, +0.0% |
| blade | 15.83 → **12.27** (stage 3b, re-swept after the mine changed) |

Sixteen probe checks pass (`tools/nightfell_relic_probe.py`), `engine_ab` is
bit-identical over the other 26 relics at 2600 matches, `verify --n 40` is
12/13 on the known Lightkeeper/Farwarden 77.3s and nothing else, and every
number in §4 below is off the built relic rather than off the lab.

**The umbral three, off `verify`'s 14,040 fights: Gravemourn 56.0, Nightfell
49.8, Twinshade 49.0**, in a roster spanning Goreshard 40.5 to Slagheart 58.7.

---

# 2. THE FIVE THINGS THAT NEARLY SHIPPED, AND ALL FIVE ARE PICTURES

None of them moves a win rate. None of them fails a probe. All five are
CLAUDE.md §4.1's defect class; the first is not this relic's problem alone,
and the last two needed a person.

## 2a. `ultFx` IS ONE SLOT, SO A WINDOW ULTIMATE'S ART IS ERASED BY THE OPPONENT'S CAST

The crackle is §1's first sentence — *"nightfell crackles with purple
electricity ... for the duration of the ult"* — and it is the only thing on
screen that says the window is open, which is the only thing that says the
next blow will leave a figure behind. It was built on `m.ultFx`, the way every
other set-piece is.

**Counting frames in which Nightfell's window was open, four seeds an
opponent:**

```
                  ultFx still shows THIS relic
vs ironhail                  0.0%
vs bulwarden                20.8%
vs twinshade                47.6%
vs grudgebearer             57.5%
vs axiom                    97.9%
vs emberedge                99.1%
```

`m.ultFx` is a single field on the match. The opponent casting **anything**
overwrites it, and then that cast's own shorter `life` expires and nulls it —
which is why Ironhail, whose Quarrelstorm is 1.3s long, leaves this relic's
eight-second window with **no art at all for the whole of it**.

The fix is that the crackle hangs off `f.ultDeadfall` and `f.deadfallFade`,
which belong to the fighter and cannot be taken away by somebody else's cast.
`drawCrackle(m, over)` is one function drawn twice, the same shape as
`drawVines(m, false/true)`.

> **THIS IS A GENERAL PROPERTY AND IT IS NOW AN OPEN ITEM.** Every window
> ultimate in the game sets `ultFx.life` from `ult.dur` — Aegis, the Thicket,
> the ballista, the Stasis Field, the Winnowing, the Sentinel, Grasp — and
> every one of them is erased on the same rule. Most survive it because what
> the viewer actually reads is a SIM OBJECT (kunai in the air, vines on the
> wall, hands diving, and the Sentinel's beam, which is already drawn off
> `f.ultBeam`). DEADFALL was the one whose window had no object of its own
> until the first figure lands. **Nobody has looked at what the other six lose
> when their fx is taken.**

## 2b. A `burst` PARTICLE FIELD IS DRAWN AT THE FOE

`drawUltOver` ends with `const at = F.spec.mode === "burst" ? [u.tx, u.ty] :
[u.x, u.y]` — right for the four novas the rule was written for, because a
nova is cast AT somebody. DEADFALL resolves nothing at the cast, so it put
**1400 purple particles over the quarry on a cast that touched nobody.** The
picture said the ultimate landed on them.

Caught on the first rendered frame and by nothing else. The flag goes on the
SPEC (`atSelf: 1` in `src/render/fx.js`) rather than on a relic name in the
glue, because "this field belongs to its caster" is a property of the field.
The spec is also retuned from Eclipse's slow dark nova to sparks coming off
the ball: faster, shorter-lived, no gravity to speak of, gone before the first
figure has finished arming.

## 2c. THE ARMING STATE WAS NOT DIM, IT WAS INVISIBLE

§8.4's tenth check is the one no tool in this repo can run: *can a viewer tell
an ARMED sigil from a crackling one?* With a fuse the crackle was a COUNTDOWN
and the tension was time; with a mine it is an ARMING animation and the
tension is space, and a viewer who cannot separate the two states cannot see
the mechanic at all.

The first cut drew arming at alpha 0.16 against a hall that **already has a
gold pentagram on its floor**. Photographed off a real match
(`tools/deadfall_sheet.py`, `05-reference/v54/deadfall-states-*.png`) it did
not read at all — so sigils appeared already live and the arming beat, which
is the whole tension of a mine, did not exist on screen.

The two states are now separated four ways at once, because any one of them
can be lost to a phone screen, to the bloom, or to a dark frame:

```
ARMING   incomplete   the ring and the star are DRAWN IN over `arm` seconds
         flickering   every stroke jitters off `shellHash`, per frame
         loose        the crackle jumps BETWEEN points, unattached
         thin         1.5px, no lamps

ARMED    complete     the figure closes, and it closes with a SNAP
         still        the jitter stops dead. Stillness is the tell.
         bound        solid star lines
         lit          ONE core at the centre, and the ground it covers
```

**Darkness was doing none of that work and was hiding one of the states.** The
figure is also now drawn in `A.core` rather than `A.glow`: #DDB8FF over a
bright ball reads as WHITE, and v52 §4 says these must not read like
Foregone's Converse, which is the other floor-marking ultimate in the game.

Rick, off that build: *"i can tell the difference between armed and arming
pretty easily."* **Settled, and nothing in the rework below is allowed to
weaken it.**

## 2d. AND THE EXPLOSION WAS FIVE THINGS, WHICH IS NO THING

The one a rendered frame could not catch, because every frame of it was
correct. Five charges each dealt `stamp/5` — about three damage — and a figure
came apart across 42 milliseconds as five small numbers. The mechanic was
right, the chain counters were right, sixteen probe checks were green, and
what a viewer saw was noise.

**One figure is one mine now.** The drawn pentagram is the hit box: one
trigger at its centre, out to `rad` 110; one blast; one number. The five
points are a drawing. §7 is what that cost.

## 2e. AND THE BLAST FROZE ON THE FLOOR — 96.2% OF THEM

Rick, on the one-mine build: *"ive also seen some mines explode and then
disappear and some explode and stick around."*

**Measured before it was touched, 36 fights: 178 of 185 detonations left a
figure frozen mid-expansion, and the worst stood for 31.67 SECONDS against a
0.42s life.**

Two causes, one on top of the other. The ageing loop sat below
`if (!this.sigils.length) return;`, and a mine is spliced out of `sigils` the
instant it fires — so when it was the last one on the floor, which it very
nearly always is, the next frame returned before reaching it. Moving it above
that guard took the worst case from 31.67s to 1.72s and **left 128 of 132
still frozen**, because the real home was somewhere else: a detonation is an
IMPACT, it sets `hitStop`, and `step()` returns through `decayImpactOnly` for
as long as that runs.

> **THE ENGINE HAD ALREADY WRITTEN THE WARNING, THREE LINES FROM WHERE THE
> BUG WENT.** `tickPresentation`, about status tags: *"a status tag is spawned
> by a hit, and every hit begins with a hit stop that runs decayImpactOnly.
> Tick it on the normal path only and the tag freezes for exactly the frames
> the viewer is staring hardest at."* Same sentence, one object along. The
> blast now lives in that function, with `life` in half-seconds like every
> other `life` in the engine, because that clock runs at 2x.

**Nothing here could see it.** The simulation is untouched, `engine_ab` is
bit-identical, no win rate moves by a thousandth — and the relic probe's own
flash check asked whether more than EIGHT were held at the end of a fight. One
frozen figure sails through a hoarding check.

> **AND THE CHECK THAT REPLACED IT GOT IT WRONG THE FIRST TIME TOO.** A
> held-time threshold fired on 128 detonations that were fine, because the
> blast runs at 2x on a normal step and 1x through a hit stop, so no duration
> bound is both loose enough to survive an ordinary hit stop and tight enough
> to catch a freeze. The invariant is exact and rate-free: **`b.t` must
> strictly increase on every step the blast is alive for.** 132 detonations,
> 0 frozen frames.

---

# 3. THE ONE MECHANISM DECISION THIS BUILD MADE ON ITS OWN

**AT MOST ONE MINE FALLS PER FRAME, and it is the nearest one.** §8.3a asked
for the chain to span frames and pointed at `bomb_lab.py`, which loops over
everything in range each step. Those two are not the same thing: a loop fires
every mine at once, every number stays right, and **there is no chain to
see.**

So `tickDeadfall` scans, fires the nearest triggering mine, and returns. The
shove has therefore landed before the next test runs, which means the ball is
genuinely carried from mine to mine rather than a loop being unrolled.
Asserted: **84 detonations, 0 steps took more than one.**

---

# 4. WHAT IT DOES, MEASURED ON THE BUILD

16 fights, four opponents:

```
40 casts   92 mines planted   84 walked into   8 still standing
most live at once 3       chained 4       longest run 2
```

`planted = walked-into + still-standing` exactly, which is check [4]: nothing
expires and nothing is lost. **Every blow inside a window stamped exactly one
figure and every figure is exactly one mine** — 92 blows, 92 figures, 0
refused at the ceiling, 0 with a payload anywhere but the centre.

**A mine is walked into 91% of the time.** That is the landmine reading paying
off exactly as v52 §2 said it would: the timer needed a blast covering half
the hall to catch 59%, and this catches nine in ten with a figure 220 units
across. It is also why a live mine now waits a fraction of a second rather
than most of a fight — `deadfall_sheet.py`'s "armed" panel could not find a
figure that had been live for a whole second anywhere in a 120-second match,
and had to ask for 0.35s instead.

Stage 3b telemetry at the shipped blade: **the echo is 14.3% of everything
Nightfell delivers**, the pool means 48 and peaks at 130, and it is up 90% of
the fight and full 68%. 477 of 915 blows land on a pool with something in it —
which is the number DEADFALL actually spends, because a figure stamped on an
empty pool is a decoration.

## 4b. THE BLADE, AND THIS CURVE DOES NOT BEND

`umbral_sweep.py --relics nightfell --lo 8 --hi 22`, 9750 fights, **run twice
— once on the five-charge figure and again on the single mine.** On the mine:

```
 8.00  14.1%      14.00  61.1%      20.00  84.1%
10.00  33.9%      16.00  71.7%      22.00  89.0%
12.00  48.4%      18.00  76.9%
```

Monotone and steep over the whole range. **Gravemourn's bends downward** —
67.3% at 47.2 and 60.6% at 52.0, because a bigger blow throws the quarry out
of reach of a weapon that lands 5.6 times a fight. A greatsword is reach-poor
and contact-rich, so its knockback never gets far enough ahead of its own
swing to cost it a blow. The sweep was run wide first anyway, because a
bisection cannot tell you which of those two shapes you are standing on.

```
15.83   what it shipped with, under the dead curse and a dead Eclipse
12.79   five charges on a ring, each dealing a fifth of the stamp
12.27   ONE MINE at radius 110 rather than five at 70
```

> **THE BRIEF PREDICTED "~13" BEFORE ANY OF THIS EXISTED** (v51 §8.2), and
> both cuts landed inside half a point of it. Second registered prediction in
> two stages to come in — Gravemourn's "~22-23" measured 24.03.

> **AND THE ONE-MINE CONFIRMATION IS MONOTONIC WHERE THE FIVE-CHARGE ONE WAS
> NOT.** Pass 3, n=1040 a point: the mine reads 11.64 → 44.3%, 12.14 → 48.9%,
> 12.64 → 53.1%; the five-charge build read 50.1 / 49.7 / 57.0 and the tool
> said out loud that it had landed in its own sampling noise. **One number a
> figure is a quieter instrument than five**, and that is worth knowing beyond
> this relic: an ultimate that pays in many small pieces is harder to measure
> as well as harder to watch.

# 5. WHAT THE PROBE ASSERTS

`tools/nightfell_relic_probe.py`, 16 checks. The two that exist for this
relic in particular:

- **[3] NO MINE EVER FIRES ON THE CASTER**, measured with the caster
  *standing inside its own armed figures* for 3,654 frames — which it does
  constantly, because they are planted where its own blows land. A
  self-triggering figure eats 48% of its own charges (v52 §3c) and **the cost
  tunes straight out of the blade**, so no sweep and no `verify` could ever
  see it.
- **[7] THE CHAIN SPANS FRAMES.** §3 above.

And two the last stage taught it:

- **[5] the pool is measured across `tickDeadfall` and nothing else.** The
  first cut compared it across a whole `m.step` and reported 2 moves in 336 —
  both of them a blade blow landing on the same frame as a detonation, which
  is the pool doing exactly what it is for. **A check that photographs a wider
  span than the claim it is making measures the rest of the engine and calls
  it a defect**; three checks in `gravemourn_relic_probe` did this in one
  session.
- **[9] a charge that KILLS files a FATAL beat** — open item 20, registered
  in advance off Grasp's hands. It is **weakly exercised**: a charge deals
  about a fifth of a stamped pool, so it lands the killing blow far less often
  than a hand does (1 in 16 fights here against Grasp's 51.7%), and the probe
  now says so in its own output rather than reporting a green it has not
  earned.
- **and a static check fired on its own new feature.** `noExpiry` was a regex
  for `/life|expire/` over `tickDeadfall`, and the blast added `sigilFlash`,
  which is presentation and is *supposed* to have a lifetime. It reported a
  defect that was not there — the fourth time in two stages that a check
  encoding its own model of a rule has failed on a legitimate change to it.
  The claim is about the MINE, so it is now asserted on the mine, at runtime,
  where it can only mean one thing.

`[10]` was never in the probe and **Rick answered both halves of it off the
first build**: *"i can tell the difference between armed and arming pretty
easily"* — so the four separations stay exactly as they are — and *"what isnt
legible is the explosion itself"*, which is §7. Neither half was ever
checkable here. `deadfall_sheet.py` is the instrument and a person is the
gate.

---

# 6. WHAT DID NOT CHANGE, ON PURPOSE

- **The figure is READ-ONLY on the pool.** `curseSum()` and nothing else: no
  push, no spend, no `apply`. Gravemourn MOVES a memory; this COPIES one, and
  that is the whole of what keeps the two umbral ultimates off each other's
  verb. The builder refuses to write if `tickDeadfall` mentions `pushCurse`,
  `apply("curse")` or `cursePool`, with comments stripped first — because
  `curse_check` fired on its own explanation once and `curse_build` refused to
  write on its.
- **Nothing expires.** *The sigil stays until something sets it off.* One
  sentence, worth +6.4 points over a 2s life, and the hall accumulates as the
  fight runs.
- **The shove is 250 and outward.** Rick's, on legibility, and it costs 23% of
  the chain.

---

# 7. WHAT THE SINGLE MINE COST, AND IT IS THE CHAIN

This is the one place where what Rick asked for and what the design measured
pull against each other, so the number goes here rather than in a footnote.

```
                              live at once   chained   longest run
five charges on a 60u ring            18        193             9
ONE mine per figure                    3          4             2
```

Same 16 fights. **The chain is gone.** v52 §3b predicted exactly this — *"at
one bomb a blow there is nothing to chain into; 1.55 live at once, 0.25 chain
hits, longest run 1.23, which is not a chain at all"* — and the build agrees
with it to within the difference the bigger radius makes.

What is left is figure-to-figure: a shove out of one blast carrying the ball
into another mine standing on the floor, which happens about four times in
sixteen fights. It is real and it is rare.

**That is the trade, stated plainly.** The five-point ring bought a chain
reaction that could not be read as one, because each link was a fifth of an
explosion. One mine buys an explosion that can, and pays for it with the
chain. Rick has the picture; the numbers had the chain; **he is the one who
has to watch it**, and the ultimate's job is to be watched.

> **AND IT DID NOT COST BALANCE.** The blade moved 12.79 → 12.27 — half a
> damage point — because one mine at radius 110 catches 91% of what is planted
> against the five-charge figure's 89%. The delivered damage is nearly
> identical; only its shape moved.

---

# Open decisions

1. ~~**THE ART**~~ **— armed against arming is SETTLED**, Rick off the first
   build: *"i can tell the difference between armed and arming pretty easily."*
   The explosion is rebuilt to his sentence and **has not been watched yet.**
   `05-reference/v54/deadfall-states-*.png`,
   `07-shorts/v54/deadfall-one-mine.mp4`.
2. ~~**THE SOUND**~~ **— THE DETONATION IS REBUILT**, Rick: *"lets make the
   explosion sound effect bigger."* It was a short bright crack on purpose,
   because five charges could land inside 42ms and five thuds would have been
   mud; that reason went with the five charges. Now a real blast in four
   parts — a sub that drops away under everything, a body of low noise, a
   crack on top so it cuts through the hit-stop, and three short debris hits
   under the tail. Rendered in an `OfflineAudioContext`: peak 0.4876 → 0.605,
   audible 1.15s → 1.35s, and the share below 120 Hz 0.224 → 0.553. **No
   burst is longer than 0.6s** — CLAUDE.md §4.5, `_burst` does not loop its
   noise buffer, and this is exactly the voice that would have wanted one.
   The other three voices are unchanged.
3. ~~**A FIGURE ARMING AND FIRING ON THE SAME FRAME**~~ **— SETTLED: that is
   how it works.** Rick. No protection window, no cost to catch rate.
4. **`crowdMul` IS UNSET FOR THIS ULTIMATE**, as it was for Grasp and the
   Winnowing. Much less pressing now — three live mines at once rather than
   eighteen live charges — but open item 15 is the same question three times.
5. **THE OTHER SIX WINDOW ULTIMATES HAVE §2a's HOLE** and nobody has looked at
   what they lose when their fx is taken. Open item 25.
6. **THE CHAIN IS GONE AND THAT WAS A TRADE, NOT AN ACCIDENT** (§7). If it is
   wanted back without the mini-bombs, the measured routes are a bigger `rad`
   (a mine that covers more floor is a mine the shove is more likely to throw
   you into) or more figures per window (a shorter `arm`, a longer `dur`, or a
   cheaper `charge`). Both are sweeps, neither has been run, and both would
   move the blade again.

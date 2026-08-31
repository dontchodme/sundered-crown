# v54 — DEADFALL IS BUILT. Stage 3 of three, and the umbral school is finished. The mechanic landed on the numbers the design predicted; **the three things that nearly shipped broken were all pictures, and one of them is chain-wide.**

**2026-08-31.** `tools/nightfell_build.py`, `02-chain/sc-gravemourn.html` →
`02-chain/sc-nightfell.html`. Design: `06-docs/v52/echoes-v52.md`. Plan:
`06-docs/v51/umbral-build-brief-v51.md` §8. What stage 2 left it:
`06-docs/v53/grasp-build-v53.md` §9.

```
DEADFALL   a window; every blow inside it stamps ONE PENTAGRAM of five
           charges on a 60-unit ring where the blow landed, each carrying a
           fifth of what Curse remembers about the quarry at that instant.
           They crackle for 1.6s, go live, and then WAIT — permanently — for
           the foe to walk within 70 of one. It deals its share, shoves at
           250, and takes its point off the figure. FOE ONLY.
           Blade 15.83 -> 12.79.
```

---

# 1. WHAT WAS BUILT, AND WHAT IT COST

| | |
|---|---|
| `kind` | `"sigil"` — new. NOT `nova`; Eclipse is gone, art included |
| `dmg` at the cast | **0**. Nothing resolves; the cast opens a window |
| `dur` | 8.0s |
| `points` / `ring` | 5 on a 60-unit ring — one figure per blow |
| `rad` | 70 per charge |
| `arm` | 1.6s of crackle, then live |
| `stampMul` | 0.3 of the pool sum at the blow, split five ways |
| `push` | 250, radially outward |
| `apply` | **gone, and it stays gone** — v52 §3e, +0.0% |
| blade | 15.83 → **12.79** (stage 3b) |

Fifteen probe checks pass (`tools/nightfell_relic_probe.py`), `engine_ab` is
bit-identical over the other 26 relics at 2600 matches, and every number in
§4 below is off the built relic rather than off the lab.

---

# 2. THE THREE THINGS THAT NEARLY SHIPPED, AND ALL THREE ARE PICTURES

None of them moves a win rate. None of them fails a probe. All three are
CLAUDE.md §4.1's defect class, and the first one is not this relic's problem
alone.

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
         lit          a lamp per live charge, at its own trigger radius
```

**Darkness was doing none of that work and was hiding one of the states.** The
figure is also now drawn in `A.core` rather than `A.glow`: #DDB8FF over a
bright ball reads as WHITE, and v52 §4 says these must not read like
Foregone's Converse, which is the other floor-marking ultimate in the game.

---

# 3. THE ONE MECHANISM DECISION THIS BUILD MADE ON ITS OWN

**AT MOST ONE CHARGE FALLS PER FRAME, and it is the nearest one.** §8.3a asked
for the chain to span frames and pointed at `bomb_lab.py`, which loops over
every charge in range each step. Those two are not the same thing: a loop
fires a whole figure in one frame, every number stays right, and **there is no
chain to see.**

So `tickDeadfall` scans, fires the nearest triggering charge, and returns. The
shove has therefore landed before the next test runs, which means the ball is
genuinely carried from charge to charge rather than a loop being unrolled. At
dt = 1/120 a five-charge figure takes 42ms to come apart. Asserted:
**337 detonations, 0 steps took more than one.**

---

# 4. WHAT IT DOES, MEASURED ON THE BUILD

16 fights, four opponents, blade 15.83 (pre-tune):

```
38 casts   76 figures   380 charges planted   337 walked into   43 standing
most live at once 18       chained 193       longest run 9
```

`planted = walked-into + still-standing` exactly, which is check [4]: nothing
expires and nothing is lost. **Every blow inside a window stamped exactly one
figure** — 76 blows, 76 figures, 0 refused at the ceiling.

Stage 3b telemetry at the shipped blade: **the echo is 14.7% of everything
Nightfell delivers**, the pool means 50 and peaks at 144, and it is up 90% of
the fight and full 69%. 474 of 893 blows land on a pool with something in it —
which is the number DEADFALL actually spends, because a figure stamped on an
empty pool is a decoration.

## 4b. THE BLADE, AND THIS CURVE DOES NOT BEND

`umbral_sweep.py --relics nightfell --lo 8 --hi 22`, 9750 fights:

```
 8.00  16.9%      14.00  61.7%      20.00  84.3%
10.00  30.9%      16.00  68.4%      22.00  85.9%
12.00  46.6%      18.00  79.0%
```

Monotone and steep over the whole range. **Gravemourn's bends downward** —
67.3% at 47.2 and 60.6% at 52.0, because a bigger blow throws the quarry out
of reach of a weapon that lands 5.6 times a fight. A greatsword is reach-poor
and contact-rich, so its knockback never gets far enough ahead of its own
swing to cost it a blow. The sweep was run wide first anyway, because a
bisection cannot tell you which of those two shapes you are on.

> **THE BRIEF PREDICTED "~13" BEFORE ANY OF THIS EXISTED** (v51 §8.2).
> Measured 12.79. That is the second registered prediction in two stages to
> land — Gravemourn's "~22-23" came in at 24.03.

> **AND THE CONFIRMATION IS NOT MONOTONIC, WHICH THE TOOL SAID OUT LOUD.**
> Pass 3 at n=1040 a point: 12.27 → 50.1%, 12.77 → 49.7%, 13.27 → **57.0%**.
> The first two are one reading of the same thing; the third is 7.3pp away
> over half a damage point. **12.79 is the middle of a flat region, not a
> crossing measured to two decimals** — the honest precision is the
> half-point interval. CLAUDE.md §0's "nothing below n≈700 ranks anything"
> is a floor, not a comfort: n=1040 is only just above it.

---

# 5. WHAT THE PROBE ASSERTS

`tools/nightfell_relic_probe.py`, 15 checks. The two that exist for this
relic in particular:

- **[3] NO CHARGE EVER FIRES ON THE CASTER**, measured with the caster
  *standing inside its own armed figures* for 11,789 frames — which it does
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

`[10]` is not in the probe and saying so is the point: it is a filmstrip
question, and the sheet in `05-reference/v54/` is the first half of the answer.
The second half — whether the difference survives motion at phone size, with
two balls moving over it — is the video's and Rick's.

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

# Open decisions

1. **THE ART IS A FIRST CUT AND IT IS RICK'S** (rule 2). The sheet is
   `05-reference/v54/deadfall-states-{arming,snap,armed,both,chain}.png` and
   the clip is `07-shorts/v53/deadfall-first-cut.mp4` (rendered against the
   pre-tune build; a fresh one is 6 minutes). The specific questions:
   **is ARMING distinguishable from ARMED at phone size and in motion**, and
   **does a purple pentagram on a floor that already carries a gold one
   read as a second thing or as part of the first?**
2. **THE SOUND IS A FIRST CUT AND IT IS RICK'S.** Four voices — the cast
   (a rising electrical whine), the stamp (short, low, under the blow), the
   ARM (a bright upward snap, one per figure), and the detonation (a crack,
   not a thud, because five can land inside 42ms). All four render audible in
   an `OfflineAudioContext`. A spread was NOT offered before building, which
   is rule 2's letter; v43's lesson says the register is what costs, so if any
   of these is wrong it wants a spread rather than a guess.
3. **A FIGURE ARMS AND FIRES ON THE SAME FRAME when the foe is standing in
   it** — three times in the seed filmed. Mechanically correct, and it means
   the arm-snap and the first detonation collide. Whether the arming beat
   should be protected (a charge cannot fire for N ms after going live) is a
   design question and Rick's; it would cost catch rate.
4. **`crowdMul` IS UNSET FOR THIS ULTIMATE**, as it was for Grasp and the
   Winnowing. DEADFALL puts up to 18 live contacts on the floor at once; open
   item 15 already flags the same question twice over.
5. **THE OTHER SIX WINDOW ULTIMATES HAVE 2a's HOLE** and nobody has looked at
   what they lose when their fx is taken. It is now an open item.

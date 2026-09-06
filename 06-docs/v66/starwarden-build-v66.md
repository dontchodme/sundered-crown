# STARWARDEN / CORONA — THE BUILD (v66). The vigil twinblade, the 34th relic.

**Claude Code, 2026-09-03. Built from `STARWARDEN-BUILD-BRIEF.md` and
`vigil-twinblade-design-v66.md` and from nothing else — CLAUDE.md §3 rule 0.**
Written as it goes (§7 rule 3), so what is below is the record and not a
summary written at the close.

```
stage 1   the relic, ultimate STUBBED    sc-minute      -> sc-starwarden.html   GREEN
stage 2   the ring and the burn          sc-starwarden  -> sc-ring.html         GREEN
stage 3   the star and the shower        sc-ring        -> sc-shower.html       GREEN
stage 4   the chain -- THE RELIC         sc-shower      -> sc-corona.html       GREEN
stage 5   the one knob, MEASURED      STATUS.burn.dps 0.10 -> 0.14            GREEN
stage 6   the particle field          sc-corona     -> sc-corona-fx.html      PART
          art, sound, the carry                                               OPEN
```

`tools/starwarden_build.py`, `tools/corona_relic_probe.py`,
`tools/corona_sweep.py`.

---

## 0. THE BASE, NAMED AND NOT GUESSED — AND THE CHAIN IS STILL FORKED

The brief says the builder names its base. It is **`02-chain/sc-minute.html`**:
33 relics, the Duskreave tip, the LAST-3 curse window, and **the minute pace**
(baseHP 520, seals 27/64, timeout 156). That last one is asserted by the
builder and not assumed, because every decimal in `06-docs/v66/` — the 17.2%
body, the 49.1% whole, the dwell, the crossing rate — was priced on it. On the
old 48-second clock this would be a different relic measured against a table
that cannot judge it.

**AND THE FORK IS SETTLED — `02-chain/sc-trunk.html`.** Rick, 2026-09-03:
*"lets get it in the app."*

For most of this build the pointer could not move: `sc-minute` does not carry
Crossweave's stages 7-12, so shipping this relic would have silently un-shipped
a finished ultimate. The fix is the cheap direction CLAUDE.md named — re-apply
Crossweave's six missing stages onto THIS tip rather than re-applying the pace
and four relics onto `sc-nova`:

```
gloamwire_build.py --stage 7..12  --src sc-corona-fx.html -> sc-trunk.html
```

All six applied with **every anchor holding on the first attempt**, which is
worth stating: they were written against a different branch of the fork and
nothing they anchor on had moved.

```
engine_ab   sc-corona-fx -> sc-trunk   3168/3168 IDENTICAL on the 33
                                       (Gloamwire excluded -- its ultimate is
                                        the thing being carried, so it MUST
                                        differ, and a run that included it
                                        would be a check that cannot fail)
chain_audit gloamwire_build.py         ALL 21 INSERTS SURVIVE
chain_audit starwarden_build.py        ALL 35 INSERTS SURVIVE
                                       (the carry did not clobber this relic)
shell_identity                          PASS 200/200 -- and the app is on
                                        Chromium 152 against headless 151,
                                        agreeing to the last bit, which is the
                                        property §4.2b cares about rather than
                                        version equality
```

**AND THE POINTER WAS NOT WHERE THIS FILE SAID IT WAS.** CLAUDE.md §0 says in
two places that the app loads `sc-nova.html`. It has loaded
**`sc-lastthree.html`** since `6117924` — so the app has been showing 33
relics with **neither** Crossweave's stages 7-12 **nor** the minute pace, and
the note in §0 has been describing a pointer that moved out from under it.
`sc-trunk` gains all three and loses nothing.


### 0a. AND THE CARRY PUT GLOAMWIRE AT THE TOP OF THE ROSTER

`verify --n 40` on `sc-trunk`: **11/13, every one of the 34 relics inside
30-70%**, and both reds are the known clock bands — the pairing ceiling
(`Farwarden/Starwarden` 98.4s, the same four relics for the sixth time, ruled
accept) and the overall mean of 60.9s against a 28-54s band that cannot contain
a minute since `pace60_build` landed.

**BUT THE SPREAD WENT 24.0pp -> 29.3pp AND IT IS NOT THIS RELIC.**

```
  Gloamwire   64.1%   <- top of the roster
  Ironhail    59.2%
  Starwarden  46.4%
  Heartwood   34.8%
```

Gloamwire is the relic whose ultimate the carry just restored: the held trio,
72 novas a cast, the drawn explosion. **Its blade was measured at 7.25 in
`sc-nova` — 32 relics, on the 48-second clock.** It is now in a 34-relic field
on the minute pace, and it reads 64.1%. Nothing about that is a defect in the
carry — the carry is exactly what Rick asked for and `engine_ab` says it moved
nobody else — but **Crossweave's blade is now priced against a field that no
longer exists**, and that is a tune somebody has to decide on. Not this
build's: it is Gloamwire's blade, on a relic this session did not design, build
or measure.

**AND IT MOVES STARWARDEN'S OWN NUMBER, WHICH IS WORTH SAYING PLAINLY.**
`corona_sweep` settled `dps` at 0.14 reading **50.9%** pooled, both sides, two
blocks — on a field WITHOUT Crossweave's finished ultimate in it. On the trunk
Starwarden reads **46.4%**. Two things account for the gap and neither is a
surprise: `verify` pairs `i < j`, so a newly appended relic is side B in all 34
of its pairings (worth about -1.9pp on the three relics where it has been
measured), and the field itself got harder when Gloamwire gained thirteen
points. **46.4% is comfortably in band and the number is explained**, but the
sweep's 50.9% and this 46.4% are not the same measurement and should not be
quoted as if they were.


### 0b. ONE COLUMN OF THE DESIGN'S TABLE DOES NOT REPRODUCE, AND IT IS THE DWELL

`corona_relic_probe [2]` is red on the build of record and it is **not** the
merge and **not** the foe sample. Measured at the full 33-foe roster:

```
                    built      lab (ring_price, UNMODIFIED, same runtime)
  crossings a cast   6.20       5.68        ok
  stacks a cast     34.4        33.97       ok
  stars touched     10.9        10.90       ok
  chained            2.6         3.29       ok
  burn damage       26.2        20.8        ok (scales with the shipped dps)
  shield            14.4        11.4        ok (same)
  peak stacks       57         49.2         ok
  DWELL              0.56s      0.82s       <- 32% SHORT
  ring damage        2.97       5.8         <- and this follows from it
```

**Eight columns of nine reproduce and one misses by a third.** The same number
of crossings, each one SHORTER — so the foe enters the band as often as the
design says and leaves it sooner. `coronaRing` is a line-for-line port of the
lab's `inRing`, so the geometry is not the difference; the likeliest remaining
candidates are WHERE IN THE FRAME the test is sampled (the lab tests after the
whole `m.step`, the build inside `tickCorona`, which runs before `tickHits`)
and what the shower's 600-knock does to a foe that is being thrown around the
band for the six seconds after the pop. **Neither has been measured and this
build is not guessing between them.**

**WHAT IT COSTS IS THE SMALLEST CHANNEL IN THE RELIC.** Dwell buys ring ticks,
and ring ticks are ~3 damage a cast against the relic's ~26 — the design's own
§6 says 94% of the damage is the burn and calls the ring the fuse. The stack
count, which is what the burn is made of, reproduces exactly. **And the balance
is unaffected either way**, because `corona_sweep` measured the BUILT relic
directly rather than trusting the overlay: 0.14 was chosen against fights this
build actually played.

**THE BAND WAS NOT WIDENED.** A gate moved by the build it is judging is not a
gate. It stays red and it is written down here.

**AND THE CHECK WAS WRONG ABOUT SOMETHING ELSE ON THE WAY.** It gated at any
`--foes` count, and the dwell is a property of WHO this relic fights — the
8-foe stride reads 0.51s, the 11-foe 0.61s, the full 33 reads 0.56s. So it
FAILED on the build of record for no reason but a flag, on a build
byte-identical in every line it touches. It is a gate only at the full roster
now and reports a shape otherwise.

---

## 1. WHAT WAS BUILT, IN THE ORDER IT WAS BUILT

### Stage 1 — the relic, stubbed

Starwarden: the twinblade's own physical stats (`blades:[0,0.5], reach:62,
width:8, artW:30, spin:5.7, mass:1.1, mode:"spin"` — **asserted against all
four shipped twinblades before writing**, because the design's numbers were
measured on one twinblade body and are only transferable to a fifth if the four
really do agree), `aff:"vigil"`, `onSelf:{ward:1}`, `dmg 8.3`, `charge:1e9`.

**RICK'S CARD LINE IS IN AT STAGE 1**, which is where this build differs from
every other stubbed one in the chain. He wrote it, trimmed it twice himself,
and it is 67 characters against `verify`'s 72 — there was nothing left to
settle, so there was no reason to ship a stub.

> *"Ring and stars deal burn damage over time. Burn is gained as shield"*

**And `tip_audit` cannot see it.** The brief's gate 1 asks the tip audit to read
that line; the tool reads STATUS tips and not ult tips, which is **open item 4**
and has been open since v40. What actually gates the card line is the builder
(it refuses to write a tip over 72 or one the run did not print) and `verify`.
Said plainly rather than reported as a pass.

### Stage 2 — the ring and the burn

The window (`f.ultCorona`), the elliptical annulus test, the ticks, the
crossing stack, the burn status and its ward feed.

**`coronaRing` is a port of `ring_price.py`'s `inRing`, line for line and
deliberately not a rewrite.** Every decimal in the design was measured through
that function, so a test that is merely equivalent would silently re-price the
relic and the design's table would no longer be judging this build.

### Stage 3 — the star and the shower

The pop on the first body contact of a window, sixteen stars, the bounce off
the **current inset**, the touch, +2 stacks and knock 600.

### Stage 4 — the chain

The queue built when the window's clock passes `dur`, top of the hall first,
one every 70ms, blast 80; the window object outliving its own window until the
queue drains; and the next cast waiting for it.

---

## 2. THE THREE THINGS THIS BUILD ADDED TO THE ENGINE ITSELF

Everything else is one relic's own tick and one relic's own art. These three
are on paths every relic runs down, and all three are asserted rather than
commented.

### 2a. A STATUS CAN NOW SAY WHO APPLIED IT

`apply(key, n, src)` — a third argument, optional, undefined at all forty-odd
existing call sites. `src` is **"a" or "b"** and not a Fighter: a reference
would put a live object graph inside a status the renderer snapshots every
frame.

`tickStatus`'s fatal-tick beat has carried this note for four versions — *"the
day a third party can apply a bleed, this needs a source on the status"* — and
Corona is that day **from the other direction**. The burn does not need to know
who to blame. It needs to know who to pay.

### 2b. A STATUS TICK CAN NOW PAY SOMEBODY

Rick's third ruling: *the burn feeds the shield*, at the blade's rate. So the
share is **`STATUS.ward.bank`** and not a second copy of 0.55 — "the blade's
rate" is his sentence, and two copies of a number are two numbers waiting to
drift. Same three writes, same order, as `resolveHit`'s vigil branch makes: the
pool, its high-water mark, and the clock.

**DECLARED, because the brief leaves it to the build: every banked tick
restarts the 5s ward clock.** That is what the design priced
(`ring_price --feed-burn`), and it means a burning enemy keeps the caster's
plate lit on its own. **No float and no tag on a banked tick** — a tick banks a
fraction of a point and `resolveHit`'s "+n" would print zeroes a hundred times a
second; what a viewer reads is the plate filling.

### 2c. A CAST CAN NOW WAIT

One clause on `tickCharge`'s fire line, against `f.ultCorona`, which is null on
every other relic. **It cannot bind at the shipped numbers** — the window is 8s
and the charge is 15 — and the probe reports it as zero. It is there for the
state the design names (a cast starting under a running chain is two set-pieces
on one screen) if any of those three numbers ever moves. The charge is **not
spent** while it waits.

---

## 2d. THE ONE KNOB, AND IT IS 0.14

`corona_sweep.py`, on the pinned runtime, **both sides of every pairing, two
seed blocks, 2112 fights a point**:

```
   dps   block 1   block 2   pooled    +/-     A-B
 0.120     45.8%     45.5%    45.7%   1.1%    2.6%
 0.130     47.8%     50.9%    49.4%   1.1%    2.0%
 0.140     50.8%     51.0%    50.9%   1.1%   -1.0%     <- SHIPPED
 0.145     51.5%     51.5%    51.5%   1.1%    1.5%
 0.170     55.6%     57.4%    56.5%   1.1%    3.9%
```

Monotonic, and the curve was found first rather than guessed — pass 0 ran
0.04 to 0.32 wide before anything was bisected, which is v53's lesson (a curve
can bend and a bisection started from a guessed bracket converges happily
inside the wrong one).

**0.14 is a MEASURED ROW and not an interpolation** — Cindercleave's rule. It
is not the row nearest 50%; **0.130 is**, by 0.6pp against 0.9pp. It is taken
over that one because **0.130's two blocks came back 47.8% and 50.9% — a 3.1pp
swing, larger than the difference being decided** — while 0.140 reproduces to
two tenths of a point on the same seeds. **The honest precision is the interval
0.130-0.145**, every row of which is inside 1.5pp of even.

**NO BISECTION WAS RUN.** v48 and v56, twice each: a bisection converges on the
noise in its tail and a three-point confirmation is only as good as the one
block it is drawn on.

## 2e. THE REPRODUCTION CONTROL, AND IT SEPARATES CLEANLY

The brief requires this before any number from the build is compared to the
design's (CLAUDE.md §4.2b). `ring_price.py` **unmodified**, at the design's own
settled settings, on `sc-minute`, on **the pinned 151**:

```
                     design (Chromium 141)      here (pinned 151)
  arm A, the body            17.2%                    19.4%
  arm D, the whole           49.1%                    45.3%
  D - A                     +31.9pp                  +25.9pp
```

**And every mechanical number in it reproduces to a decimal:**

```
                design    here          design    here
  casts a fight   4.6     4.56    dwell   0.82s   0.82s
  pops a cast    0.92     0.92    entries   5.6    5.68
  stacks a cast  33.9    33.97    touched  10.9   10.90
  chained         3.4     3.29    in blast 0.35    0.36
  ring damage     5.8      5.8    burn     20.5    20.8
  shield         11.2     11.4    peak       49    49.2
```

**The MECHANISM crosses runtimes and the WIN RATE does not.** That is the
cleanest demonstration of §4.2b this project has: nothing about the ring, the
shower or the burn is different on the two Chromiums, and the same arm is
6.0pp weaker on ours. **Read the design's 0.20 against 45.3%, not against
49.1%** — it is not refuted by this build needing 0.14, it was measured
somewhere else.

**AND THE BUILT RELIC AGREES WITH THE OVERLAY THAT PRICED IT.** The lab's arm D
at `dps` 0.10 reads 45.3%; the built relic's curve reads 43.2% at 0.096 (n=264,
SE 3.0pp). The control that could have failed did not: **what was built is what
was priced.**

## 3. THE GATES

### Stage 1

```
engine_ab  sc-minute -> sc-starwarden   5280/5280 IDENTICAL on all 33
tip_audit                               0 effect fields the tips never mention
verify --n 40                           (below)
```

Gate 1's number is the one that matters and it lands: **Starwarden 19.5%**
against a brief band of 15-25% and a design figure of 17.2% — the ward body at
the row's floor blade with no ultimate at all. Near 10% would have meant the
ward channel was not wired; near 50% would have meant something was firing.

The other four `verify` reds at stage 1 are the stub and the two known clock
bands: two relics beat a body with no ultimate 40/0, the 30-70% band cannot
hold a stubbed relic, `Farwarden/Starwarden` runs 108s (the known pairing
ceiling, Rick ruled accept), and the overall-mean band is 28-54s and **cannot
contain a minute** (CLAUDE.md §0 — that band is stale, not this build).

### Stage 2-4

```
engine_ab  sc-starwarden -> sc-corona   5280/5280 IDENTICAL on all 33
corona_relic_probe (sc-corona-fx)       20/20
```

The three intermediate A/Bs were collapsed into one across the whole ultimate:
if `sc-starwarden` and `sc-corona` are identical on the other 33 relics, every
stage between them is inert on them too, and it is the cumulative claim that
matters. **What that proves is the three engine changes in §2** — `apply`'s
third argument, `tickStatus`'s new branch and `tickCharge`'s new clause — since
those are the only lines outside this relic's own methods.

**And the probe's per-cast table is the design's arm D on the pinned runtime:**
33.51 stacks a cast against 33.9, the star popping in every cast that reached a
body contact, 11.6 stars touched against 10.9, 2.4 chained against 3.4, peak 59
against 49 — at `dps` 0.14 rather than the design's 0.10, which is why the
damage and shield rows are higher.

### THREE OF THE PROBE'S OWN CHECKS WERE WRONG BEFORE THE BUILD WAS

The repo's standing failure mode, three more times in one file:

1. **"a window outlived its caster"** — 4 of 173. `tickCorona` runs before
   `tickHits` and `checkEnd`, so a caster killed later in the same step leaves
   a window standing on a frame the ticker never saw. Asked in the ticker's own
   wrapper instead: **0**.
2. **"the caster is hurt inside its own tick"** — 1 frame. The ring's tick goes
   through `hurt`, which empties the quarry's plate and calls `shatter`, and a
   shatter is a BLAST that catches whoever is next to it. This relic is a
   contact hazard, so the caster is next to it by construction. Counted
   separately rather than asserted away.
3. **"stage 3 is not in this build"** — on a build that has it. The capability
   check grepped `tickCorona` for `stars.push`, which lives in `coronaPop`, so
   **the design's own bookkeeping invariant was silently SKIPPED** rather than
   failing. It runs now: spawned = touched + chained + still alive, every cast.

A CHECK THAT COUNTS FRAMES IN WHICH AN EVENT IS POSSIBLE IS NOT COUNTING THE
EVENT — and a capability check that looks in the wrong place does not fail, it
goes quiet.

---

### Stage 5, on the finished relic

```
verify --n 40 (sc-corona)   11/13   Starwarden 47.0%
                                    every relic in 30-70% (Heartwood 35.5 ..
                                      Ironhail 59.5, spread 24.0pp)
                                    BOTH SIDES CAN WIN EVERY MATCHUP -- the
                                      stage-1 red cleared when the ultimate
                                      went live
```

**Both reds are the clock and neither is this build's.** `Farwarden/Starwarden`
at 98.4s is the known pairing ceiling — the same four relics that have been the
answer four times running, ruled ACCEPT — and the overall mean of 61.1s fails a
band of 28-54s that **cannot contain a minute** and has contradicted a ruling
since `pace60_build` landed. Read `11/13` as two stale bands, exactly as §0 of
CLAUDE.md says to.

The roster spread is **24.0pp**, against 25.4pp on this branch before this
relic existed. A thirty-fourth relic went in and the spread came DOWN.

## 3b. AND THEN RICK WATCHED IT, WHICH IS THE ONLY TEST THAT COULD SEE THIS

> *"looking good. i cant see the large star in the ring though."*

§4.1: when a person catches something no tool could, **the deliverable is a
MEASUREMENT of the thing they saw.** `tools/corona_star_probe.py` is that
measurement and it is a permanent check.

```
                            first cut     redrawn
  the star stands            2.72s a cast, 29% of its own window   (unchanged)
  ball radius                34px          34px
  drawn radius               17px          1.02 x ballR
  mean |dL| over its box     0.0168        0.0781
  peak |dL|                  0.1670        0.8081
  pixels it moves            12.0%         23.1%
```

**IT WAS NEVER A DURATION PROBLEM.** The star is up for 29% of the window and 3
casts in 74 never popped at all. What was wrong was legibility, and it was
**three faults at once, each of which this repo already had a rule for**:

1. **It was drawn inside `drawCorona`'s `lighter` block**, so it ADDED pink
   light to an already-bright pink shell. §4.1b, third time in this project:
   the ball is not lit, the mark is erased.
2. **Radius 17 against `ballR` 34** — the whole star fitted inside the disc it
   was supposed to be sitting on.
3. **`P.core` is the ball's own hue.** `_stWard`'s docstring has said it in
   capitals since the ward shipped: **A SELF-BUFF MUST SEPARATE BY VALUE, NOT
   BY HUE** — every ward plate gets a near-black outline first. This is the
   second self-coloured mark on a vigil ball in the game and it made the same
   mistake.

The fix is `source-over`, `1.02 × ballR`, and a 7px outline in the school's
dark before the fill. **`engine_ab` 3366/3366 identical WITH STARWARDEN ITSELF
IN THE ROSTER** — the picture moved and no fight did, which is the cheapest
proof this project has and the reason art can still be changed after stage 5.

`07-shorts/v66/corona-window.mp4` is the first cut and
`corona-window2.mp4` the redraw, same seed, same window.

### 3c. AND THEN IT MOVED OFF THE BALL ALTOGETHER

> *"the star should live within the ring. not the ball."*

**His own §1 had said it and two cuts of this build missed it** — *"an
elliptical ring of neon light **with a small gap left for** a large star in the
middle."* The band is BROKEN and the star is what the break is for. Drawn on
the shell, the gap was decorative and the star was a marking on a relic.

The band is drawn in 64 segments now, accumulated into ONE path and filled
once, so the gap costs the same two fills and two strokes a pass it cost
before — Breach's constraint. **The gap is sized from the star rather than
typed in**: `|dP/dt|` on an ellipse is `hypot(A sin t, B cos t)`, so dividing
the star's own radius by it gives a break of constant ARC LENGTH wherever the
seat is put. A fixed angle would leave the star swimming in one seat and jammed
in another, and the seat is Rick's.

`corona_star_sheet.py` photographs four seats off one real frame
(`05-reference/v66/corona-star-seats.png`). **The control worked**: seat D
(`-π/2`) draws the star behind the ball and it is completely invisible, which
is what says the sheet is measuring something. Seat B (`π/2`) is 42 units out
against a ball radius of 34 and lands back on the shell — the thing he
rejected. **Seat A (`starAt` 0, the end of the major axis, 108 units out) is
the default.**

Re-measured at the star's own seat: **mean |dL| 0.107, peak 0.932, 31% of the
box**. `engine_ab` identical with Starwarden in the roster — `starAt` and
`starR` are read by `drawCorona` and by nothing else.

**AND THE PROBE WENT STALE WITH THE BUILD, WHICH IS THE INTERESTING PART.**
`corona_star_probe`'s contrast box was centred on the CASTER, because that is
where the star used to be. With the star seated 108 units out the same box
measured empty hall and reported **|dL| 0.0000 — a false red on a picture the
contact sheet shows perfectly clearly.** A PROBE THAT HARDCODES WHERE A THING
USED TO BE MEASURES SOMEWHERE ELSE AND CALLS IT A DEFECT. The box follows the
seat now.

### 3d. AND THE TRIGGER IS NOW A QUESTION, PRICED

The star is on the band; **the pop still fires on a body-to-body contact**,
because that is what the design settled when the star was on the body. Over 74
casts:

```
  body contact     fires in 85% of casts, median 1.31s into the window
  the star's seat  fires in 78% of casts, median 2.61s
  and the seat is touched FIRST in 30% of casts
```

Only the "which is first" column is clean — after the body trigger fires the
fight has spent its shower, so a later seat touch is a moment in a fight that
would have gone differently (§7). **Moving the trigger to the star's own seat
would cost about seven points of pop rate and delay the pop by ~1.3s**, which
shortens the shower's uptime inside the window — and the shower is ~60% of the
fire, so it re-prices the relic and `dps` would have to be re-measured. **It is
a mechanic, so it is Rick's and Cowork's, not this session's** (rule 0). Named,
priced, and left alone.

### 3e. AND THE BURN IS EMBERS, WITH NO RING

> *"the burn stacks need a different animation. they look like worms."*
> *"b looks best but the full ring of red is really confusing."*

**The worms were a constant-width curved stroke.** The first cut stroked a
quadratic three times at 5.4 / 3.0 / 1.3px; nothing in fire is a line of even
thickness that bends, so twelve of them crawling round a shell read as
something animal. `corona_burn_sheet.py` put four vocabularies in front of him
at two stack counts — TONGUES (tapered filled flames), EMBERS (motes, no
licks), CROWN (one jagged silhouette) and CHAR (the shell blackens and cracks).

**He took EMBERS and killed its rim, and the rim was a fault this engine had
already written down.** Variant B carried a stroked circle at `R × 0.99` to
say heat — and a continuous ring around a ball in this game is a GAUGE.
`_stWard`'s own docstring records the ward arc being moved out to R+17 because
*"at R+9 it was fighting the health ring for the same annulus"*; a red ring at
0.99R sits inside both of them. The heat is a DISC now: a surface, not a
readout.

**AND THE FIRST CUT OF HIS PICK SATURATED BY TWENTY STACKS**, which the range
sheet caught and the two-count spread could not. `heat` divided by 24 and the
mote count capped at 22, so **a quarry on sixty looked exactly like one on
twenty** — on the one status in this game with no ceiling. That is `_stBleed`'s
bug in a second costume: it is not enough to draw more than four marks, **the
SCALE has to reach where the status actually goes.** The probe measures the
peak at 59, so the scale runs to 48; the mote count runs to 34; and the plume
gets TALLER with the count, because height is legible at arena scale where a
brighter ball is not. The additive heat was also cut back hard — the first cut
washed the shell toward white at 40 stacks, which is §4.1b again: a bright
thing added to a bright thing is erased. The relic keeps its colour and its
health ring at every count.

`05-reference/v66/corona-burn-shapes.png` is the four-way spread and
`corona-burn-shipped.png` the shipped one at 6 / 20 / 40 / 60.

### 3f. THE CAST HAS A VOICE, AND IT WAS PICKED IN A FIGHT

> *"i cant judge the sound like this."* — then, from four heard in a real
> window — *"3 sounds the best."*

**SWEEP.** `_sweep` rising into a lock: two re-struck triangles a fifth apart
at 0.50 and 0.86, which is the ring taking its shape. It is a SWEEP and not a
strike, and that is why it fits this cast — **nothing has been hit when it
plays.** For a median 1.31s afterwards the ultimate has touched nobody, so an
impact voice would promise a contact that has not happened; every other ult
voice in this game is a thing landing.

**FOUR BARE RENDERS WERE THE WRONG INSTRUMENT AND HE SAID SO IN FOUR WORDS.**
`sentinel_hum_lab`'s own docstring had already written it down — a candidate
has to be heard ARRIVING the way it will in the fight, *"a hum judged cold is
judged in a context the game never produces"* — and this build handed him four
files in silence anyway. `corona_voice_audition.py` is the fix and it is a
permanent tool: it records the engine's own `SFX.play` call list across one
real window (**134 sounds in fourteen seconds** — 102 wall bounces, 16 hits, 11
ult calls, 5 clanks), replays it with exactly ONE call substituted, and muxes
each render onto the SAME picture. Four files differing by one sound at 1.20s.

**GAIN-MATCHED TO A CONTROL, because a spread that is not is a loudness test.**
Every candidate is normalised against the same window rendered with the build's
own voice, so the comparison is register.

**AND WHAT SHIPPED IS PROVED TO BE WHAT WAS AUDITIONED.** `voice_matches`
refuses to write unless the shipped branch carries every number of the lab's
candidate 3 — and the shipped path was then rendered ALONE against the lab's
own function: **1.14s against 1.15s, 0.6% against 0.6% under 120 Hz, 352 Hz
against 350 Hz.** A voice that had drifted from the file Rick approved would be
INAUDIBLE as an error; nothing else in this repo would have said so.

**A FINDING ON THE WAY: `_noiseBuffer` FILLS WITH `Math.random()`**, so any
voice with noise in it renders differently every time — the same candidate
measured peak 0.269 and 0.486 across three runs. It cannot reach the
simulation (audio is downstream of everything and `SFX.play` returns on its
first line headless), but **no rendered voice in this project is reproducible**,
and every measured decimal in its sound work has that wobble under it. It also
means a peak taken over a whole window is dominated by wall bursts and cannot
be used to compare two voices — which is why the check above renders the cast
ALONE. Not this build's to fix; `_burst` and `_tone` are already open item 6.

### 3g. AND THE STAR POP HAS A VOICE — CHIMES, CHOSEN TWICE

Four candidates — SHATTER (glass and its pieces), FLARE (a low thump under a
bright bloom), CHIMES (a struck cluster spraying small bells) and SCATTER (a
dry crack and then sixteen ticks, one per star). Rick took **CHIMES**: the only
one that says STAR rather than BOMB.

**IT WAS AUDITIONED TWICE AND THE SECOND ONE IS WHY THE PICK IS TRUSTWORTHY.**
The pop lands a **median 1.31s after the cast** and SWEEP runs **1.15s**, so in
the ordinary window the two OVERLAP — and the first window offered had a
**3.35s** gap, which hears them as separate events *by construction*. A voice
chosen there could have fused into the cast on every ordinary cast and nothing
in this repo would have said so. `_corona_tight.py` hunts the hard case; the
second audition ran at a **1.28s** gap, in a busier fight (114 sounds, against
Lastlight, with the Harrowing's own set-piece in it). **CHIMES was picked from
the tight one.** That is `sentinel_hum_audition`'s lesson taken seriously: a
spread cannot answer a timing question.

**AND THE BUILD WAS SILENT THERE.** `coronaPop` filed a beat, a ring and a
shake and made no sound at all — v42's defect sitting in the open — which is
why the audition had to INJECT the candidate rather than substitute it. Stage 6
adds the CALL as well as the voice, and `voice_matches` refuses to write if the
voice is defined and nothing plays it.

Proved, as the cast was: the shipped path rendered ALONE against the lab's own
function — **0.60s against 0.60s, 4.1% against 4.1% under 120 Hz, 800 Hz
against 796 Hz.** `engine_ab` **3366/3366 identical across all 34** with the
`SFX.play` call on Starwarden's own sim path, which is the check that matters
for a sound added inside a ticker.

**A CHECK THAT ONLY LOOKED LIKE IT COVERED BOTH.** `voice_matches` searched
from the cast's branch to the next `} else {` — and the fallback is the LAST
arm, so that search ran straight past the pop's branch and read two voices as
one. It asserted nothing about the pop while reporting a pass. It searches to
`} else ` now and checks both, plus the call site.

## 4. OPEN, AND WHOSE

1. **The art and the sound — Rick's, from rendered spreads at stage 6.** The CAST voice is settled (SWEEP, §3f) and the ring, the star and the burn are settled (§3b-3e). The CAST (SWEEP, §3f) and the STAR POP (CHIMES, §3g) are settled. **What is still unheard is the BURN and the CHAIN** — two voices. The chain has a window waiting for it: the tight audition's own fight leaves 5 stars over.
   One window has now been watched **four times** and every round of it moved
   something no probe had a number for: the star's legibility, then its seat in
   the ring, then the burn's whole vocabulary, then the cast's voice. That is
   CLAUDE.md §4.0 earning its place four times in one build. The shower and the
   chain are still first cuts and have never been commented on. Rule 2.
2. **The burn's own tip.** ≤40 characters, and Rick has not written it. The
   placeholder is in the house form and its number is **substituted from the
   shipped `dps`**, so a bisection cannot leave the card describing the old
   relic (v40 shipped "5s" after a sweep moved it to 8.1).
3. **The silhouette.** `_tbPlated` has existed since before this cell had
   anything in it and **this is the first relic that will ever draw it.**
   Nobody has looked at it. A redraw is a later, separate claim.
4. **The particle field.** `SPECS` has no entry for `starwarden` — and none for
   `ravelbone` or `gloamwire` either, which is **open item 46**. `ULTFX.sync`
   returns on a missing spec rather than erroring, which is exactly why it
   ships.
5. **`crowdMul` is unset**, as it is for Deadfall, Grasp and the Winnowing. It
   wants its own measurement and not the spike storm's — **open item 15**, now
   four relics old.
6. **The fork, and therefore the carry.** §0.

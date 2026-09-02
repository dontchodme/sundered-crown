# v63 — DUSKREAVE AND SCOUR, BEING BUILT. THE UMBRAL SCYTHE, THE 33RD RELIC, THE LAST SCYTHE.

**IN PROGRESS — Claude Code, 2026-09-02. Do not build this cell; it is claimed
in `06-docs/CLAIMS.md`.**

Built from `06-docs/v63/DUSKREAVE-BUILD-BRIEF.md` (Cowork), on the chain tip
`02-chain/sc-bloodletting.html` (32 relics), by `tools/duskreave_build.py`.

| stage | what | state |
|---|---|---|
| 1 | the relic, ult stubbed | **BUILT**, gate 1 GREEN |
| 2 | the tornado exists and sweeps, no damage | **BUILT**, `sc-scour.html`, probe 7/7 |
| 3 | it catches, drags and ticks — the relic | **BUILT**, `sc-grind.html`, probe 13/13 |
| 4 | it eats projectiles | **BUILT**, `sc-scourwind.html` |
| 5 | art, sound, beat | **SILHOUETTE + FUNNEL + VOICE BUILT**. The voice is a SPREAD awaiting Rick |
| 6 | the real price | **THE BALANCE PASS**: tick damage 5 -> 1, and the curse window landed under it |

---

# 0. THE CURSE RULE IN THE LINK IS THE SHIPPED ONE, AND THE BUILDER ASSERTS IT

Brief §1 says to build against whichever rule is in the build of record and to
never write a tick that behaves differently under the two. `curse_rule()` reads
`pushCurse` out of the source, with comments stripped, and classifies it:

```
  curse BIGGEST-3  keep the 3 BIGGEST -- the shipped rule.
                   Scour prices in the +59.2pp tier.
```

`pushCurse` sorts descending and truncates to `STATUS.curse.maxStacks`, so the
last-3 window (`curse-window-v63.md`, Rick's ruling of 2026-09-02) has not
landed and is not this build's. **The classification is printed on every run**,
so gate 6's price can never be read against the wrong rule — which is the one
way this build could produce a number that looks fine and means something else.

---

# 1. STAGE 1 — THE RELIC, ULT STUBBED

`02-chain/sc-duskreave.html`, 33 relics.

```
  src sc-bloodletting.html  dc5ddaec21e20590
  out sc-duskreave.html     547ae9776677c094   1532319 bytes
  relic dmg 21, onHit curse 1, ult Scour STUBBED (charge 1e9, kind scour)
```

Everything in the entry is the brief's §0 table. `dmg` 21 is Rick's and is not a
bisection start — there is no blade stage in this brief and no `TUNED_DR` in the
builder, deliberately. `kind:"scour"` shares with nothing: the scythe row already
carries `harrow`, `converse`, `sentinel`, `breach` and `effigy`, and a sixth
set-piece on one weapon type has to be separable by sigil, voice and picture.

**THE BUILDER REFUSES BEFORE IT WRITES, ON FOUR THINGS.** Each can fail:

1. the source is the Bloodmirror tip (`tickSpectre` present) and does not
   already carry Duskreave;
2. the curse rule is one of the two recognised ones — not "assume the shipped
   one";
3. **the six shipped scythes agree on the type's own body.** Every number in the
   design was measured on Thornwake's body, and they are only transferable to a
   seventh scythe if the six really do agree. Measured: `reach:104, width:11,
   artW:46, spin:3.2, mass:2.4, mode:"spin"` across lastlight, thornwake,
   foregone, vesper, cindercleave and bloodmirror;
4. `SHAPES.scythe` still routes `umbral` to `_scEaten`. This relic is the first
   ever to draw it, so if the routing had moved, the silhouette that shipped
   would be the generic crescent and **no measurement in this repo would say
   so.**

---

# 2. TWO FINDINGS OFF STAGE 1, AND NEITHER IS A DEFECT IN THIS RELIC

## 2a. RICK'S CARD LINE IS 83 CHARACTERS AND `verify` CAPS AN ULT TIP AT 72

```
    "Conjures a tornado that absorbs projectiles. Enemies caught in it take rapid damage"
     83 characters, over by 11
```

It is his own wording, given 2026-09-02, so it is not this session's to cut
(CLAUDE.md §3 rule 2 — the card wording is one of the seven). And the brief
records it as **measured to fit**: two lines in the ult-bar reminder at 390px,
two on the scrunch panel at 21px, nothing dropped.

**Both can be true at once**, and that is the whole of the finding:

- the 72 is a CHARACTER count, and v53 settled that characters are the wrong
  unit for this box — `"Each hit reflects 8% of remembered cursed damage"` is 48
  characters and 583px, so it passes `verify` and overflows the card;
- `tip_audit`, the gate CLAUDE.md calls the one that actually protects the
  layout, **does not look at ult tips at all** — open item 4, five versions old.
  So the pixel gate that would settle this does not exist;
- the cap has been raised once before, from 44 to 72, for exactly this reason.

**Rick's, and it is one of two:** the cap moves on a pixel measurement taken on
this machine, or the line comes down to 72 characters in his words. Stage 1 does
not need it — the tip is stubbed at `"-"`. **Stage 3 does.**

## 2b. `silhouette_probe` CANNOT SEE AN EATEN GRAMMAR

The scythe row, silhouettes only, on the built link:

```
type          variants   min IoU  mean IoU   the split
scythe               7     0.443     0.566   sanc | bloo | dwar | verd | umbr | runi | vigi
```

`05-reference/v63/duskreave-scythe-row.png`. **The umbral panel is a plain
crescent with no bites in it.** They are there in colour and they are gone in
the mask, because the probe forces every colour the shape asks for to white so
it can compare outlines — and `_scEaten` takes each bite with `destination-out`
and then strokes a RIM around it. Flatten the palette and the rim is white, the
weapon is white, and the bite is a white hole in a white shape.

So that 0.443 describes a weapon without its grammar. **`_gsEaten` and
`_tbEaten` have the same problem and have been shipping far longer**, which
means the IoU numbers quoted for those two cells are also numbers about a shape
they do not draw. This is open item 35's two-instruments problem with a
mechanism attached: not a defect in this relic, and worth knowing before anyone
quotes an eaten cell's separation again.

**So the review sheet is drawn in COLOUR**, through `litWeapon` — the path the
game uses, and the only reason an eaten grammar is safe at all.
`tools/duskreave_sheet.py`.

---

# 3. WHAT RICK HAS TO LOOK AT BEFORE STAGE 2

Brief stage 1: *"Film it and show Rick a strip before stage 2"* — v58's
`_whEaten` was rejected on sight after it had been built and tuned.

- `05-reference/v63/duskreave-scythe-row-colour.png` — all seven scythes at
  zoom, in their own palettes. Umbral is the fifth.
- `05-reference/v63/duskreave-arena.png` and `-arena-zoom.png` — the relic in a
  real fight against Lastlight at the delivery resolution, 540×960, seed 33581.

**RICK RULED ON IT, 2026-09-02:** *"this one is rough and should be redone."*
Three reference images with it. `_scEaten` is out; the redraw is §5 below.

**What this session saw in them, and it is the same fault he named:** the bites are
bright-rimmed cutouts, and at both sizes they read closer to *studs set into the
blade* than to *something bitten out of it* — the rim is the brightest thing on
the weapon, so the eye takes it as an added object rather than as a missing one.
That is the shape of the v58 complaint (*"the hammer with blocks attached to it
idea just isnt working for me"*), arriving on a different row. It is also the
first time anyone has looked at this grammar, and it may read fine in motion.
**Rick's call, and the strip is the point of asking.**

---

# 4. GATE 1

## 4a. `engine_ab` — PASS, 4960/4960

All 32 existing relics, 496 pairings, 10 seeds each, against the parent link:

```
  sc-bloodletting.html            4960 matches  221.1s
  sc-duskreave.html               4960 matches  322.5s

  PASS  no page errors on either build
  PASS  same number of matches            4960
  PASS  every match identical field for field   4960/4960
  PASS  the sweep is real   32/32 distinct winners, 4960 distinct seeds, 13.6-90.2s
```

**Adding Duskreave does not move the 32-relic roster.** The "sweep is real"
line is the control that could have failed: an A/B over a roster that all drew
or all timed out would pass identity trivially.

## 4b. `verify --n 40` — 11/13, and BOTH failures were predicted before it ran

528 pairings, 21,120 fights, 33 relics.

```
  PASS  no JS errors or page exceptions
  PASS  every status and ultimate has viewer-facing text
  PASS  all 528 pairings ran
  PASS  every match resolved
  PASS  both sides can win every matchup
  PASS  timeout rate <= 10%            0/21120 = 0.0%
  FAIL  every relic winrate in 30%-70%   Duskreave 15.3% .. Ironhail 59.8%
  FAIL  every pairing mean duration in 18-70s
                                         Lightkeeper/Farwarden 75.7s
  PASS  overall mean duration in 28-54s  47.6s
  PASS  every pairing clanks at least once
  PASS  no pairing resolves on fewer than 6 hits
  PASS  capture path pins the canvas to 1080x1920
  PASS  renderer draws a non-blank frame
```

**The duration failure is the KNOWN thirteenth check** — Lightkeeper/Farwarden,
vigil against vigil, no umbral relic in it, and it has failed on every build
since the long-fight pace at 74.6s, 75.7s and 76.9s. Not this build's, in either
direction.

**The winrate failure is the stubbed ultimate, and it is the gate passing rather
than failing.** Excluding Duskreave the roster runs Heartwood 39.8% to Ironhail
59.8% — a **20.0pp spread**, in line with the 20.3pp Gloamwire shipped at. The
44.5pp the check prints is one relic with its ultimate switched off.

## 4c. THE NO-ULT FLOOR — 15.3% AGAINST A REGISTERED 17.6%

This is gate 1's real reading and it is a registered prediction landing.
Duskreave is a 21 blade carrying curse with `charge:1e9`, so `fireUlt` can never
run and what `verify` measured IS the no-ultimate floor.

```
    registered (v63 §3, control 2, a MODEL)          17.6%
    measured (the built relic, verify --n 40)        15.3%
    side-B asymmetry, measured elsewhere            ~+1.3pp
    ------------------------------------------------------
    like for like                                   ~16.6% against 17.6%
```

Roughly a point apart, on two different rosters and two different instruments —
the model was a donor with its own ultimate stubbed on a 30-relic roster,
measured as side A; this is the real relic on a 33-relic roster, run as side B
in all 32 of its pairings because `verify` pairs `i < j`.

**And the number that would have been the finding is 26%.** The brief says a
floor landing there means something is firing that should not — a stub that is
not stubbing, a channel applying twice, an inherited window. It is nowhere near
it. **GATE 1 PASSES.**


---

# 5. THE REDRAW — FIVE CANDIDATES AS A SPREAD, AND THE SHIPPED ONE AS THE CONTROL

`tools/umbral_scythe_lab.py`, `05-reference/v63/umbral-scythe-candidates.png`.
Every arm is injected over `SHAPES._scEaten` at runtime and the page is thrown
away; **nothing is written to any build.**

**WHAT THE THREE REFERENCES SHARE, read as silhouette rather than as colour:**
a thin deeply-curved blade with a hot edge on a near-black body (all three); a
secondary fang hooking under the head (1 and 2); spines along the blade's back
(3); a jointed shaft with knuckles and a finned pommel (all three, and the one
feature nothing else on this row uses). Ref 3's chain and refs 1–2's gem
sockets are surface, not outline, and can go onto whichever shape wins.

```
    A  FANG     the crescent plus one recurved fang under the head
    B  SPINED   the back edge IS six swept spines, growing toward the tip
    C  SHAFT    clean blade; the grammar moves to the snath — four knuckles
                and a finned pommel
    D  REAVER   fang and spines and the hot edge together
    F  THIN     a narrowed, deeply hooked blade — the references' single most
                consistent feature, and the one none of A–D answers
    E  SHIPPED  `_scEaten`, the control
```

**EVERY ARM OBEYS v58'S RULE**, which is the rule that fixed the umbral
warhammer: a grammar that adds a limb to a type must add it to the type's
OUTLINE, not behind it. Fangs and spines are emitted into the SAME closed path
as the crescent — one path, one fill, one stroke — so nothing can come apart
from the blade at any zoom.

> **AND THE FIRST CUT OF THE FANG REPRODUCED v58'S REJECTION EXACTLY.** It left
> the outline at the crescent's root and returned to the point it had left
> from, so the lobe hung off the blade by a single vertex and rendered as a
> dark shape laid behind it — *"triangles layered behind the hammer"*, in a new
> place. Caught in the lab, before Rick had to see it a second time, and the
> fix is that both ends of a limb must land on the outline.

> **AND THE SHEET'S SECOND COLUMN WAS CUT FOR BEING UNTRUSTWORTHY.** It was
> meant to show the delivery register beside the zoom — v56's hand was approved
> at zoom and shipped at ~40px as a white scribble. Three attempts: cropped at
> the zoom radius it overflowed the cell and painted over the sheet; cropped at
> its own it framed the handle and cut the blade off; sized off the renderer's
> scale it came out LARGER than the zoom panel beside it. **A column that
> cannot be trusted is worse than no column**, so the spread is a shape
> question at zoom (v53's rule) and the scale question is answered separately,
> by a real 540-wide arena frame off `duskreave_sheet.py --arena`, once an arm
> is chosen.

**THE REFERENCES ARE NOT IN THE REPO AND SHOULD BE.** They arrived as chat
attachments and Code cannot read a transcript — `CLAIMS.md`'s standing lesson.
The paragraph above is written so the redraw survives without them, the way the
brief wrote down what is inside `ref-vortex.mp4`. If Rick drops the three files
into `06-docs/v63/`, name them `ref-scythe-1/2/3` and this section should say so.


---

# 6. STAGE 2 — THE TORNADO EXISTS AND SWEEPS

`02-chain/sc-scour.html`, ten inserts, `7aa6239f22bcb186`.

```
  tornado dur 10s, w 160, top y=600, sweep 200 px/s, charge 15
  starts UNDER THE CASTER heading toward the foe
```

Every number is the brief's §0 table. `tick` and `dmg` are written now and are
inert until stage 3 — Bloodmirror's `strandW` precedent, and the reason is v56:
a stage-2 insert wrote a whole `ult` block, stage 3 rewrote one line of it, and
the run logged numbers the shipped relic did not carry.

**START AND DIRECTION ARE CODE'S CALL (open decision 2) AND THIS IS THE ONE THE
BRIEF POINTS AT:** under the caster, heading toward the foe. The labs started it
at the left wall and bounced it — a lab's convenience, since it makes every run
comparable — and on screen that would open a set-piece where nobody is looking.
The sweep SPEED is measured free (v62 §8b: contact 17.3/17.3/17.4% across
120/200/300), so the start almost certainly is too. Filmed, not tuned.

**`dir` IS SNAPSHOTTED AT THE CAST.** Read live off the foe's position, the band
would turn round every time the quarry crossed it — a hazard that chases is a
different mechanic and it is not this one.

**THE BAND IS DRAWN OFF ITSELF, NOT OFF `m.ultFx`** — Deadfall's fix rather than
a taste. `ultFx` is one slot; the opponent casting anything overwrites it and
that cast's shorter `life` then nulls it, measured at 0.0% survival against
Ironhail (open item 25). A ten-second window whose picture can be erased by
somebody else's nova is a window nobody sees.

## 6a. `scour_probe.py` — 7/7, AND IT WAS WRONG TWICE FIRST

```
  PASS  the ultimate casts at all            52 casts / 24 fights = 2.17 (charge 15 predicts ~2)
  PASS  the band carries the brief's numbers w [160], top [600], one value each
  PASS  sweeps live, frozen by hit stop      51426 live frames moved, 0 frozen
  PASS  it bounces off the walls             325 direction changes
  PASS  the EDGE never leaves the hall       0 frames, cx ran 80..440
  PASS  no band outlives its match           0
  PASS  the window runs its stated 10s       33 windows, 9.99s..9.99s
```

**BOTH OF ITS FIRST TWO FAILURES WERE THE PROBE**, which is this repo's
documented default. One compared a JS object's keys — which are STRINGS — against
integers, so a build carrying exactly the right numbers could not pass. The other
**measured the window's duration against `m.t`** and read a 10.00s window as
12.38s. That is Bloodmirror's probe fault verbatim: the window's own clock only
advances on live steps, because `step()` returns through `decayImpactOnly` while
`hitStop` runs, so wall-clock is always longer.

> **AND THE GAP BETWEEN THOSE CLOCKS IS A NUMBER STAGE 3 NEEDS.** A 10.00s
> window occupies up to **12.38s** of the fight. 7 ticks a second is 70 ticks a
> window in WINDOW time, and the quarry is inside the band for rather longer
> than that in wall time.

## 6b. TWO BUGS IN THE BUILD, AND ONE OF THEM CLOSED AN OPEN ITEM

**A COMMA BETWEEN CLASS METHODS**, because `Match` and `Renderer` are classes
and both new methods were inserted with an object-literal separator. The symptom
was CLAUDE.md §4.11 exactly: **a twenty-second Playwright timeout naming no file
and no line**, indistinguishable from a slow machine.

> **SO THE BUILDER NOW SYNTAX-CHECKS ITS OWN OUTPUT** — §4.11 has asked for this
> since v40. `node --check` on every inline `<script>` block before the write,
> and node is already a dependency of this repo (the app pins electron). The
> comment-balance test in `one()` catches one specific cause; this catches the
> whole class, **including the one that actually happened, which balance could
> never have seen.** A machine without node gets a warning rather than a refusal.

**AND `this.c` INSTEAD OF `this.ctx`** in `drawScour`. Green across the probe,
the syntax check and `engine_ab` — none of which draws — and it threw on the
**first rendered frame**. That is v48's fault exactly, where `_drawBeam` reached
for a Match method from the Renderer and `drawUltUnder` handed a NaN to
`createRadialGradient`, both green across 27 probe checks and a 280-match A/B.
§4.0 is not advice.

## 6c. GATE 2 — FILMED, AND THE BAND IS A QUARTER OF THE HALL

`05-reference/v63/scour-gate2.png`, three casts on three seeds, each sampled at
a different point in its own window (12%, 50%, 86%) — one instant repeated three
times says nothing about a thing whose whole job is to move.

```
  seed 33581  window 1.21s  cx 354  dir +1   band 31% of the width, 25% of the height
  seed 11961  window 5.00s  cx 360  dir +1   31% / 25%
  seed 55196  window 8.60s  cx 117  dir +1   33% / 24%   (foe INSIDE)
```

**THE WIDTH AGREES WITH RICK'S WORDS AND THE HEIGHT DOES NOT.** `CONFIG.arena` is
520 × 800; `w` 160 is 31% of the width, which is "a third" as the brief's own
gloss says. `top` y=600 leaves 200 of 800 — **25%, a quarter, not a third.** A
third would be y=533 and would make the band 267 tall.

**THE NUMBER IS WHAT SHIPS, because the number is what v62 measured** — every
arm in the design ran `top` 600 and the catch rule is written against it. But
the number and the sentence do not agree, gate 2 asks in as many words whether
the band "reads as a third of the arena", and moving it would change the catch
area by a third and therefore the price. **Rick's.**

> **AND THE HALL CLOSES ON IT, WHICH THE FILM SHOWS.** `m.inset` walks 0 → 140,
> so the floor rises while `top` stays where it is: the band is 200 tall at the
> start of a fight and **60 at full collapse**. Seed 55196 catches it mid-way at
> 181. The labs pinned their windows at t=12 and t=30, so partial collapse is
> inside what was priced — but a Scour cast late in a long fight is a materially
> smaller hazard than one cast early, and nobody has measured that. It is the
> same class as Breach's vents, whose comment says an absolute (x, y) torn early
> is outside the room later.


---

# 7. STAGE 3 — IT CATCHES, DRAGS AND TICKS. THIS IS THE RELIC.

`02-chain/sc-grind.html`, `9b8effdcc917c2a8`.

```
  tick 7/s at base 5, drag 6, EDGE catch rule (|x-cx| <= w/2 + R, y + R >= top)
```

**THE ECHO IS THE RELIC AND IT MEASURES.** 465 ticks over 24 fights:

```
    mean damage a tick          12.53      against a stated base of 5
    the echo's share            60%
    peak tick                   28
    ticks on an empty pool      0 of 465
```

v63 §0 predicted the echo would be about half the tornado's damage, measured on
a model before anything was built (113 of 226 a fight). Built, it is **60%** —
and the relic is on the `resolveHit` path, which is the whole difference between
a +17.8 ultimate and a +59 one. Sentinel's `beamHit` uses `hurt` and collects
nothing; that is the precedent this build was warned not to follow.

## 7a. `over` LEARNED FOUR SWITCHES, AND `resolveHit` WAS NOT FORKED

The brief is explicit — *"Extend it — do not fork `resolveHit`."* A second copy
of a 500-line function read by thirty tools is how two damage paths drift apart.

| switch | why | measured |
|---|---|---|
| `knock: 0` | the ordinary knock fires AWAY FROM THE CASTER at 165×`knockMul`; seven a second throws the quarry out of the thing holding it | 0 of 465 ticks moved the foe inside `resolveHit` |
| `stop: 0` | `0.045 + 0.0022×dmg` ≈ 0.067s a tick, and 7 a second freezes ~45% of every second | 0 non-fatal ticks raised hit stop |
| `stun: false` | 7 stagger-locks a second is a weapon lock, not a grind; the DRAG is this design's control | 0 raised stun |
| `beat: false` | ~23 `hit` beats a fight from one ultimate, and `cinePlan` would cut to every one | 0 ordinary ticks filed; **14 fatal ticks, 0 of them silent** |

**THE FATAL TICK FILES REGARDLESS, AND THAT IS NOT NEGOTIABLE.** A kill the
director cannot see is Gravemourn's 30-of-58 all over again — 30 kills landed by
a hand, all thirty producing a clip with no killing blow. `over.beat` silences
an ordinary tick and cannot silence a kill.

> **AND A ZERO OVERRIDE NOW SKIPS THE WRITE RATHER THAN CLAMPING.** The first
> cut left `this.hitStop = Math.max(this.hitStop, stop)` with `stop` 0, and the
> probe reported **155 ticks raising hit stop to 0.000** — the clock carries a
> small NEGATIVE residue between freezes and `Math.max(…, 0)` clamps it up,
> which is a write. Nothing reads the difference (`step()` tests `> 0`), so it
> was inert — but **an invariant that is "nearly true" cannot be asserted, and
> a check that has to allow 155 exceptions will not notice the 156th.**

## 7b. THE BRIEF'S OWN SNIPPET PASSES A `seg` THAT THROWS

Brief stage 3 gives the call as `this.resolveHit(f, foe, foe.x, foe.y, null, …)`.
**`resolveHit` reads `seg.bx - seg.ax` unconditionally** — impact sparks fly
ALONG the blade rather than outward from the point — so `null` throws on the
first tick that ever lands, and it throws *inside the step*, which kills the
match rather than the frame. Every projectile call site synthesises one;
`tickShots` builds a 20-unit segment along the shot's own velocity.

The tornado's is **horizontal, along the sweep** — the bearing the thing is
actually travelling on, which is the same reasoning that gave Breach's jets
their own bearing instead of the caster's.

## 7c. THE DRAG IS CODE'S, AND IT IS `drag` 6.0 UNTIL SOMEONE WATCHES IT

Open decision 1, and the labs never modelled it (v62 HANDOFF §6). An
**acceleration toward the band's floor centre, proportional to how far out the
quarry is** — so a ball at the edge is pulled hardest and one already in the
throat is barely touched, which is what makes it read as a vortex rather than a
magnet. At the band's edge, 80 units out, 6.0 buys about 480 px/s² inward, which
meets the brief's own test: a ball entering from the side is still inside a
second later.

**IT IS NOT A PIN, AND THAT IS LOAD-BEARING THREE TIMES OVER.** `foe.pin` stays
0 because `tickStasis` carries `f.stun = Math.max(f.stun, f.pin)` for both
fighters on every frame outside any guard (v60's finding — any relic that writes
`pin` is handed a weapon lock from a file nowhere near it); because `_drawField`
would draw PARADOX'S HEXAGON on the caught ball (open item 41, live on Shroudmaul
today); and because `ballCollision` treats a held ball as immovable (open item
42). **A pull is a pull.**

Measured: the quarry is inside the band on **22.9%** of band-frames.

## 7d. THE PROBE MEASURES THE TICK, NOT THE FRAME IT LANDED ON

`scour_probe` wraps `resolveHit` and takes its before/after either side of the
tick's own call. A frame can carry a tick AND a blade blow, and a blade blow
legitimately raises hit stop, stun and the beat count — so a frame-level check
would have reported **the blade** as a defect in the tick. That is CLAUDE.md's
most repeated probe fault in a new costume.

**AND ONE CHECK COULD NOT FAIL, WHICH IS WORTH MORE THAN THE CHECK.** The
headline test was written as "ticks on a non-empty pool must out-damage ticks on
an empty one" — and the empty-pool population is **0 of 465**. The blade applies
curse on every blow, so a tornado never catches a quarry whose pool is clean.
The comparison is against the tick's stated base instead, and the absence is
itself the finding: **there is no such thing as a Scour tick without an echo.**

## 7e. GATE 3

`05-reference/v63/scour-gate3.png` — the catch, on two seeds. Tick damage of
**10 and 12** floating over the quarry against a base of 5, with `CURSE 66` and
`CURSE 77` on the shell: the echo is legible on screen without a caption, which
is the higher form of rule 1.

*(One of the three seeds produced no cast in 60s. That is a finding about the
seed, not the band — it is printed rather than silently replaced.)*


---

# 8. STAGE 4 — IT EATS PROJECTILES

`02-chain/sc-scourwind.html`. Measured over 20 fights a side:

```
    the five bows        127 arrows eaten
    greatswords + warhammers    0, exactly
```

**THE ORDER IS THE GUARANTEE.** `tickShots` both MOVES an arrow and RESOLVES it
in the same pass, so an eat placed with the other window tickers — after it,
where `tickScour` lives — would let an arrow already standing in the band travel
and connect on the frame before it was removed. `scourEat()` runs immediately
**before** `tickShots`: anything inside the band at the top of the frame is gone
before it can do anything at all. The brief's *"do not let the eaten shot deal
damage"* is an ordering requirement, not a flag.

**THE MARK IS A RING, NOT A SPARK FIELD**, and that is determinism rather than
taste — `spawnFx` draws twice from `this.rng()` per particle. `Match.ring` is a
pure push.

---

# 9. STAGE 5a — THE SILHOUETTE, AND IT IS NOT THIS SESSION'S

`02-chain/sc-duskmoon.html`. Rick, shown `_scEaten` on screen for the first time
in the game's history: *"this one is rough and should be redone."* Cowork owns
the redraw (CLAIMS.md 03:58 UTC), Rick chose **arm A, THE MOON** from a spread
of four, and the spec is `06-docs/v63/scmoon_spec.js` — **checked at 0 pixels
differing** against the arm he actually picked.

**THE SPEC IS PASTED VERBATIM.** Retyping any of it would be re-deciding a
settled picture and would make that 0-pixel check meaningless.
`tools/umbral_scythe_lab.py`'s candidates — this session's A–F and G–J — are
**superseded**, and `_scEaten` is **deleted** (v58's precedent: `_whEaten` was
deleted when `_whGnawed` replaced it, because a dead grammar that still parses
is one the next dispatch edit can route back to by accident).

> **AND THE CUT TOOK THE WRONG SPAN FIRST, WHICH THE SYNTAX GATE CAUGHT.** The
> deleter walked back from the header to the nearest `/* -` to take the doc
> comment with it — and found one **inside the function pasted just above**, so
> it cut from the middle of `_scMoon` and took that function's tail with it.
> `node --check` named the line. It now finds the comment by its `*/` being
> separated from the header by whitespace and nothing else. **This is the
> second bug the stage-2 syntax gate has caught in one build**, and neither
> would have surfaced as anything but a twenty-second timeout.

---

# 10. STAGE 5b — THE FUNNEL

`02-chain/sc-vortex.html`. Rick, on the placeholder band: *"the tornado is just
a purple box."* Built against `ref-vortex.mp4` as the brief describes it: eleven
stacked bands narrowing to the floor, each leaning on its own phase so the stack
shears as it turns; a halo ring above; near-black debris orbiting between the
bands; a hard floor line and pool; and the lightning.

**THE LIGHTNING JUMPS INTO THE QUARRY WHILE IT IS CAUGHT, AND THAT IS THE ONLY
ELEMENT THAT CHANGES WHEN THE MECHANIC FIRES.** The tick deals no knock, no hit
stop and no stagger by design — so without it the most violent thing this relic
does has **no representation on the target at all**. That is v59's bleed drips
and v54's arming sigil, one relic along.

## 10a. THE REFERENCE AND THE HIT BOX DISAGREE, AND THE POOL IS THE ANSWER

The reference funnel is **narrow at the floor**; the catch is full width at
every height (`|x − cx| <= w/2 + R`). Drawn literally, the picture says the
floor is safe exactly where the hazard is widest — and CLAUDE.md is explicit
that **a picture claiming a smaller hazard than the one that exists is the
hardest kind of bug in this repo to see.**

So the taper is the reference's and the floor carries the reference's own
answer: the hard glow line and the pool span the **full band width**, so the
footprint is stated by the brightest thing in the picture. **Whether that lands
is a question only a person can answer**, and it is on Rick's list.

## 10b. TWO CONSTRAINTS IT IS BUILT UNDER

**NOT ONE `this.rng()` CALL.** Every phase is derived from `T.t` and an index.
`spawnFx` takes two draws per particle, so a debris field here would have moved
every Duskreave fight and put gate 6's price on a different sim — the hazard
that forced Breach's sparks to be drawn rather than spawned, twice.

**NO PER-FRAME GRADIENTS IN A LOOP.** Flat fills and strokes under `lighter`.
`GRAIN_CACHE`'s comment names nine `createRadialGradient` calls a frame as *"the
single cause of the stutter Rick reported"*, and Breach's billow put one inside
a lobe loop for seventy-two a frame at 14× the render time.

---

# 11. SCOUR HAS NO VOICE, AND IT IS PLAYING SOMEBODY ELSE'S

**Not silent — worse in one way, because silence is easier to notice.**
`SFX.play("ult", { w: f.w.id })` falls through the whole relic dispatch to the
final `else`, which is the **rune-crack**: a 0.5-second high burst written for
runic. So a ten-second grinding tornado is announced by a short crack and then
makes no sound for the rest of its window, and **the ticks are silent** — 7 a
second, ~23 a fight, the loudest thing the relic does.

That is v42's defect class in a milder costume (*a silent ultimate shipped
through a 14-check probe, a 29-check probe, a full sweep and a 13/13 verify*),
and it is why the brief asks for **a rendered spread — three casts × three holds
× two tick voices — before anything is chosen.** Sound is Rick's (rule 2) and he
has said he has no preference, which means he has to hear options.

**It is also part of why both clips fail the loudness gate** at −17.0 LUFS
against a −16..−13 target, with the mixer's three limiter settings all landing
short. Not diagnosed further; the biggest set-piece in the fight currently
contributes almost nothing to the mix.

**THE COUNT: 22 relics have an ult voice and 11 fall through to the rune-crack**
(`aureole, axiom, censer, duskreave, farwarden, gloamwire, heartwood, ironhail,
lightkeeper, oathwound, spellbreaker`). Ten of those are not this build's and
nobody has written it down before. Worth its own open item.


---

# 12. THE EASTER EGG — A COW, ON 13.3% OF SEEDS

Rick, 2026-09-02: *"lets also make our first easter egg! lets have a small
amount of seeds 10-15% show a cow flying around the tornado"* and *"lets also
make sure our cow gets a good moo."*

**SHE IS CHOSEN FROM `m.seed`, AND THAT IS THE WHOLE ENGINEERING PROBLEM IN ONE
LINE.** The seed IS the fight: every recorded number, every clip, `engine_ab`
and the entire history of this project rest on `(build, relics, seed)` naming
exactly one fight. A draw from `this.rng()` would have moved the sim, so **the
cow would change the fight she appears in** — an easter egg that alters the
balance is a bug wearing a joke. Hashing the seed costs nothing, is stable
per-fight, and makes the seed quotable, which is what an easter egg is *for*.

```
    h1(seed * 0.61803398875) < 0.125      12.5% by construction
    measured over 4,000 seeds             13.3%        (Rick asked for 10-15%)
```

The scaled hash is not decoration: seeds are dense in the low integers and a
raw `sin(n)` bands badly on consecutive inputs.

**AND THE MOO USES THE SAME TEST, SO A MOO WITH NO COW CANNOT HAPPEN.** Twice a
window — once as she first comes round, once late. Two falling tones a fifth
apart with a sagging tail: **a moo is a pitch that sags**, which is what
separates it from a horn. Quiet on purpose; an easter egg that shouts stops
being one the second time you hear it.

> **AND THE RNG GUARD REFUSED THE BUILD, ON ITS OWN EXPLANATION.** `duskreave_
> build.py` will not write stage 5b if the funnel's source contains
> `this.rng()` — and the cow's comment has to say those words to explain why it
> does not call it. That is `curse_check` and `curse_build`'s failure from v53,
> twice in one day, arriving a third time: **a check that cannot tell code from
> the comment explaining it fires on its own explanation.** The fix was already
> in the file — `strip_comments()` — and CLAUDE.md's note says this will keep
> happening to anything that greps shipped source in a codebase that explains
> itself in the file.

---

# 13. THE VOICE — A SPREAD, AND THEN THE SAME WINDOW THREE TIMES

`tools/scour_sound_lab.py`, `05-reference/v63/scour-voices.wav`. Eight
candidates in 44s: three casts, three holds, two ticks.

**WHAT SCOUR NEEDS THAT NO OTHER RELIC HAS NEEDED.** Every other ultimate's
voice is an EVENT — a strike, a nova, a shatter. This one holds for **ten
seconds** and carries **seven ticks a second** under it, 70 a window. So the
three questions are separable and the sheet asks them separately: does the
window OPEN, does ten seconds of it WEAR OUT, and at seven a second is the tick
a grind or a BUZZ.

**AND THE HOLD HAS TO BE RE-STRUCK, WHICH IS NOT A STYLE CHOICE.** CLAUDE.md
§4.5: `_burst` does not loop its 0.6s noise buffer so anything longer plays
silence for its tail, and `_tone` ends on an exponential ramp over its whole
length — **a held note does not exist in this toolkit.** Ten seconds of standing
tornado is 38 strikes at 0.26s and there is no other way to do it. The cadence
is therefore the character: Wind 0.26s, Turbine 0.16s, Hollow 0.44s.

`T.hum` counts down in **window time**, inside `tickScour`, so the cadence stops
with the window through a hit stop. A cadence on a frame counter would drift
against the thing it is describing every time somebody landed a blow.

## 13a. THE PER-SECTION PEAK WAS MEASURING THE WRONG SOUND

The first run reported holds B1 and B3 at **0.434 — which is A1's cast peak**,
bleeding into a section that opens with the neutral cast so the hold can be
heard being arrived at. Two different candidates cannot have identical peaks to
three decimals; that is the tell. Measured after the cast decays:

```
    B1 WIND      0.109
    B2 TURBINE   0.486        four times louder than Wind
    B3 HOLLOW    0.232
```

Every section is asserted audible at peak >= 0.005, because `SFX.play` returns
on its first line headless and wraps its body in try/catch — **v42 shipped a
silent ultimate through a 14-check probe, a 29-check probe, a full sweep and a
13/13 verify.**

## 13b. AND A SPREAD CANNOT ANSWER IT — RICK ASKED FOR CLIPS

*"ill need to hear them in a clip."* That is `sentinel_hum_audition`'s finding
one relic along: a spread is heard cold, and the question is whether the voice
survives a real fight's clanks and hits and hit stops. So the three HOLDS are
built into `04-experiments/_scour-voice-B1/B2/B3.html` and the **same window on
the same cow seed** is filmed three times, varying one thing.

**THE SIM CALLS THE VOICE AND THAT IS PROVABLY FREE.** `SFX.play` returns on its
first line when `!this.on` — every headless run — and nothing in the audio path
draws from `this.rng()`, so a sound in a tick loop reaches no fight.
`engine_ab` over the roster is the proof, and it is the proof v42 never had.


---

# 14. RICK'S PICK, AND THE WOOSH

**B1 WIND**, 2026-09-02, off the three clips: *"first one."* Landed in the chain
at `02-chain/sc-scourvoice.html` with cast **A1 UPDRAFT** and tick **C1 ZAP**,
which were held constant while he judged the hold. Those two axes have not been
spread against him and can be, the same way, if he wants them.

**AND A WOOSH OVER THE TOP** — *"can we also give the tornado a wooshing
sound."* It is a SEPARATE LAYER and that is the design, not an implementation
detail: B1's job is to say the tornado EXISTS, which is why it is a flat floor
struck four times a second and deliberately even, so ten seconds of it does not
wear out. A woosh says the tornado is MOVING — and this one is, at 200 px/s
across the hall, bouncing off the walls. Folding the movement into the bed would
give a floor that swells and fades, which is the one thing a ten-second bed must
not do.

**A WOOSH IS A MOVING FILTER, NOT A MOVING PITCH.** A rising pitch is a whistle;
a cutoff climbing through a noise band and falling back is air going past. Five
overlapping bursts up and down, because one long burst plays silence past 0.6s
(§4.5) — the same constraint that gives the cast six bursts and the hold its
re-striking.

**ITS CLOCK IS 1.15s AGAINST THE BED'S 0.26s, DELIBERATELY NOT A MULTIPLE.** A
woosh landing on every fourth wind strike would lock the two layers into a
repeating bar and turn a floor into a rhythm. Drifting is what makes it read as
weather.

## 14a. GATE 5c — 4224/4224, AND THE FIRST RUN MEASURED THE WRONG BUILD

`engine_ab` over all 33 relics, Duskreave's own pairings included: **every match
identical field for field.** `SFX.play` returns on its first line when
`!this.on` — every headless run — and nothing in the audio path draws from
`this.rng()`, so seventy sound calls a window reach no fight. **That is the
proof v42's silent ultimate never had.**

> **AND THE FIRST RUN OF IT WAS AGAINST `_scour-voice-B1.html`, WHICH IS NOT
> WHAT SHIPS.** The woosh was added after, and it puts another `SFX.play` on
> another clock inside `tickScour`. Same class of change — but "same class" is
> not "measured", and the chain tip is the thing that ships. Re-run against
> `sc-scourvoice.html` rather than reasoned about.


---

# 15. THE BALANCE PASS — AND THE CURSE WINDOW LANDED FIRST

Rick, 2026-09-02: *"lets do a balance pass"*, and then, asked which curse rule
to balance against: **"add the last 3 window now and balance around that."**

## 15a. THE WINDOW — `02-chain/sc-lastthree.html`

`tools/curse_window_build.py`, and it is nothing but §1 of
`06-docs/v63/curse-window-v63.md` applied: push `n` copies, then **drop the
OLDEST** until the length is 3, instead of sorting descending and truncating.

**IT IS COWORK'S CLAIM AND NOT THIS SESSION'S.** `CLAIMS.md` has it as
DESIGNED, NOT TO LAND YET, gated on re-pricing the four built umbral relics.
Rick asked for it now so the blade could be balanced against the rule the game
will actually have. **The re-pricing that gate asks for is still owed** — the
numbers it was ruled on (−2.6 / −4.6 / −4.0 / +0.0) are 320–350 fights an arm,
well under the n≈700 floor, so they are a direction and not a measurement. The
builder prints that on every run.

**THE GATE HAS TO FAIL IN ONE DIRECTION AND PASS IN THE OTHER**, and it does:

```
    the 27 relics that cannot apply curse    2808/2808 IDENTICAL
    the 6 that can                           DIFFER, as they must
```

An A/B that came back green on the umbral six would mean the rule did not land.
One that came back red on the other 27 would mean it reached something it should
not — `pushCurse` is only ever called from an `onHit:{curse:n}` or from
Revenant's hands.

## 15b. DUSKREAVE MEASURED 96.2%, AND THIRTEEN RELICS WENT 0/40

`verify --n 40` on the window build, before any tuning:

```
    FAIL  every relic winrate in 30%-70%   Heartwood 37.8% .. Duskreave 96.2%
                                           (spread 58.4pp)
    FAIL  both sides can win every matchup 13 pairings at 0/40 against Duskreave
    FAIL  pairing duration                 Censer/Duskreave 26.1s
```

Three failures, all one relic. Against a model that said **+40.5pp over a 17.6%
floor — about 58%.**

> **AND THE LARGEST SINGLE CAUSE WAS AN ART DECISION TAKEN WHILE BALANCE WAS
> DEFERRED.** Rick: *"the tornado is too short. lets double its height"* —
> a LOOK call, made explicitly before the balance pass. But `top` 600 → 400
> doubles the catch area, and the catch is the entire mechanic:
>
> ```
>     top 600 (what v62 priced)     quarry inside the band 22.9% of band-frames
>     top 400 (what shipped)                               40.8%
> ```
>
> A 78% increase in time-under-grind on a relic whose damage is ticks × echo.
> **The height is currently carrying a balance decision that was made for the
> picture**, and that is worth knowing rather than quietly compensating for.
> Two other unpriced multipliers sit under it: the DRAG, which no lab modelled
> (v62 HANDOFF §6) and which exists specifically to keep a caught ball caught,
> and the tick count per window that both of them raise.

## 15c. THE TICK'S DAMAGE IS 1, AND THE CURVE IS A CLIFF

Rick: *"lets drop the damage… i ment drop the ults damage to 1 per tick if you
have to."* Swept as a CURVE and not a bisection (v48, v56, v59, and v53's
downward-bending blade), 896 fights a point, both sides, two seed blocks:

```
    tick   block 0   block 1
    1.00     51.5%     55.0%      pooled ~53%, IN BAND
    1.50        -      72.4%
    2.00     82.8%     83.7%      reproduces across blocks
    3.00     90.6%         -
    5.00     96.8%         -      the brief's value
```

**THIRTY POINTS FOR ONE POINT OF TICK DAMAGE, and no crossing above 1.** There
is no fine tuning available on this axis: 1 is the only value in band, and it is
also the lowest the engine can express — `resolveHit` rounds, so a base below 1
would round to 0 on some rolls and 1 on others. The 3.5pp gap between blocks at
tick 1 is the n≈700 floor showing up exactly as documented; tick 2 reproducing
to within a point is the control that says the instrument is sound.

## 15d. AND THE WINDOW INVERTED WHAT THE RELIC IS MADE OF

This is the finding of the pass and it is a design consequence, not a tuning
one. Under the three-biggest rule the echo was **60% of every tick** — measured
at stage 3, and it is the design's own headline: *"the echo is the relic."*

Under the last-3 window, **every tick pushes its own small `dmgBase` into the
pool and displaces the scythe's 35-damage memories**, so the pool fills with the
tick's own damage and the echo collapses. What is left is raw output: 70 ticks a
window, linear in the tick's damage, and very nearly lethal at 5 — 350 against a
400 hp fighter. That is why the curve is a cliff and why the relic is now
balanced by the GRIND rather than by the MEMORY.

**Scour under the window is not the ultimate that was designed.** The design's
central claim — that the ticks are hits *because* they collect the echo — is
worth much less than the raw grind now. Nothing here is wrong; the rule was
ruled, the relic is in band, and Rick accepted the tier in advance. But the
sentence in `duskreave-design-v62.md` that the whole cell was chosen for is no
longer the sentence that is true, and that belongs in writing rather than in
somebody's head.

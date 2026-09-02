# v63 — DUSKREAVE AND SCOUR, BEING BUILT. THE UMBRAL SCYTHE, THE 33RD RELIC, THE LAST SCYTHE.

**IN PROGRESS — Claude Code, 2026-09-02. Do not build this cell; it is claimed
in `06-docs/CLAIMS.md`.**

Built from `06-docs/v63/DUSKREAVE-BUILD-BRIEF.md` (Cowork), on the chain tip
`02-chain/sc-bloodletting.html` (32 relics), by `tools/duskreave_build.py`.

| stage | what | state |
|---|---|---|
| 1 | the relic, ult stubbed | **BUILT**, gate 1 GREEN |
| 2 | the tornado exists and sweeps, no damage | **BUILT**, `sc-scour.html`, probe 7/7 |
| 3 | it catches, drags and ticks — the relic | not started |
| 4 | it eats projectiles | not started |
| 5 | art, sound, beat | not started |
| 6 | the real price | not started |

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

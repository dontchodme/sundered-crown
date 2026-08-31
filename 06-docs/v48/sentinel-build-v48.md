# v48 — VESPER and SENTINEL, built. The first thing in this game that persists, turns, and is paid for with the armour it is wearing — and a picture fault that every headless check in the repo called green.

**2026-08-30, Claude Code.** Built off `02-chain/sc-thornshear.html`, which is
the build of record and is what the brief's §0 item 1 means by "Thornshear
lands first". The brief names `sc-thornshear-frame.html`; there is no such
file and there never was — the twenty-sixth relic shipped as
`sc-thornshear.html`, and `vesper_build.py` refuses to run against a source
with no `"winnow"` in it, which is the same guarantee with the real name on
it.

```
02-chain/sc-vesper.html            THE NEW TIP     27 relics · SENTINEL
tools/vesper_build.py              the builder,    14 inserts
tools/vesper_relic_probe.py        27/27
tools/vesper_sweep.py              the grid
07-shorts/v48/vesper-first-look.mp4   filmed on placeholder numbers, brief §0.3
```

---

# 0. THE BRIEF'S FIRST INSTRUCTION, DONE FIRST

> *"RE-RUN THE PROBES AT THAT TIP BEFORE YOU BELIEVE ANY NUMBER IN THESE
> DOCS. If a number has moved, the design doc is wrong and it is yours to say
> so."*

All three re-ran against `sc-thornshear.html`. **Nothing load-bearing moved,
and two things did.**

| probe | result | what moved |
|---|---|---|
| `beam_probe.py` | **14/14** | pool at the cast: empty 57% → **59%**, mean 12.3 → 11.9, **median still 0.0**. Every geometry number identical to the digit. |
| `row_price.py` | 2/3 | **vigil x scythe +19.2% → +15.2%** — still the strongest cell on the row, now by 7.2 points instead of 7.5. |
| `scythe_survey.py` | 15/16 | one check's ordering, inside sampling noise — see below. |

**THE CELL SURVIVES ITS OWN RE-PRICING, AND SO DOES EVERY GEOMETRIC SENTENCE.**
The design was priced on a twenty-five relic roster and fights twenty-six; the
answer is that one relic does not move a survey.

## 0.1 THE ONE FAIL IS AN ORDERING OF TWO ARMS INSIDE THE NOISE

`scythe_survey [4.3]` asserts *"the arm that throws away least is the WORST
arm in the sweep"*. At the previous tip `dur 9.0` was worst (38.3%); at this
one it is 43.0% and `dur 5.0` is worst at 41.5%. The design doc's stronger
claim — **"`dur` HAS NO FIXED SIGN: at bank 0.55 lengthening it *costs* 1.2
points"** — reads the other way here: 41.5% → 43.5%.

**Do not re-plan anything on that.** Those cells are 200 fights each; two arms
two points apart are indistinguishable. What is stable across both runs is the
finding the section exists for: `cap` does nothing (41.5% → 41.5% at 140),
`bank` is the live knob (0.35 → 33.0%, 0.55 → 41.5%, 0.85 → 46.5%), and the
best cell measured is now **+12.0 points** over shipped rather than +13.4.

`STATUS.ward` is not this relic's to move (brief §7) and is untouched.

## 0.2 AND ONE NEW NUMBER, WHICH IS THE SHAPE OF THIS RELIC

`row_price`'s lift split by the FOE'S MODE, which the previous run did not
print for this cell:

```
cell                     ranged     swing      spin     chain
vigil x scythe           +34.0%     +2.9%    +13.3%    +17.5%
```

**The ward is worth most against the thing that lands little blows from across
the hall** — the exact opposite shape to the relic built immediately before
it, which loses four fights in five to every bow (v47, open item 12). Worth
having in front of anyone reading the two relics together.

---

# 1. WHAT WAS BUILT, AND WHERE IT DIFFERS FROM §1

Four of §1's sentences are built as written. Two are not, and both were
already decided by measurement before this session opened.

| §1 says | what shipped | why |
|---|---|---|
| "charges up (with a loud glowing animation)" | `wind: 0.85s`, a gathering ring on the blade tip and a rising four-part voice | as written |
| "thick, at least half the thickness of an artifact" | `half: 28` → a beam **56 wide** against a 68-wide artifact | as written, and the builder **refuses to write under 17** |
| (not in §1) | **the shaft GROWS out and retracts back** | **RICK ASKED FOR THIS**, 2026-08-30, against a reference frame — see §1.3 |
| (not in §1) | **it ends in a blunt point** | **RICK ASKED FOR THIS**, 2026-08-30, off the v2 clip — see §1.6 |
| "a loud glowing animation" | six voices, and the hum's **dynamo swells once per payment** | **RICK PICKED IT** off a rendered spread — see §4e |
| "limited range and points at the tip" | `range: 300`, origin = **the ball's own centre** | **RICK CHANGED THIS ONE**, 2026-08-30 — see §1.3 |
| "slowly rotates to track" | `turn: 1.6 rad/s`, rate limited | **Rick's**, from four arms |
| "rapid ticks of damage while it persists" | **PER PASS, not per tick** | at 1.6 the beam holds for 0.28s and breaks 3.5 times a window. It does not persist. Rick took the lighthouse. |
| "push enemies towards its tip" | **CUT** | six times the force moves the quarry 0.56 → 0.59 of the way down. Named, not dropped — open decision 1. |
| "uses the banked shield to increase its duration" | **DRUNK CONTINUOUSLY**, not read at the cast | the pool at the cast is a median of ZERO over 290 casts |

## 1.1 THE UNIT IS A PASS

A pass BEGINS when the ball enters the volume, ENDS when it leaves, PAYS ONCE
on entry, and pays a second time — `passDmg * (tipMul - 1)`, its own hit with
its own float, ring and voice — the instant it first reaches the far quarter.
**At any point during the pass, not where it happened to be on the last
frame.**

Measured in the build, 32 matches, 57 windows:

```
passes                 268 over 7955 frames of contact
a pass is              30 frames long and pays on ONE of them
passes a window        4.7
mean pass              0.25s        longest 2.61s
passes reaching 0.75   172 of 268   (64%)
tip bonuses paid       171          (the 172nd killed the quarry with the base hit)
mean ENTRY point       0.69 of the length
mean FURTHEST reach    0.77
```

**Entry 0.69 against furthest reach 0.77 is why the latch has to exist.** A
bonus read off the entry point, or off the last frame, would fire on a
different set of passes — and nothing in this repo would have said so.

## 1.3 RICK MOVED THE ORIGIN OFF THE BLADE, AND IT MOVED THE MECHANIC WITH IT

Off the first-look clip: *"first lets have it center from the ball, not the
scythe"*, and *"it also needs an animation showing it grow"*, with a reference
frame attached and the bar set at *"this quality or better to pass"*.

**The origin was on the blade because the measurement said the mount was
nearly free, not because it was better.** `beam_probe [2]` had the centre at
28.3% time-on-target against the tip's 23.4% — the centre was already the
stronger arm by 4.9 points, and §1's "points at the tip" was being honoured
because it cost almost nothing. It also produced a fault the film found and no
probe could: a beam fired from a tip that orbits at 3.2 rad/s is laid straight
ACROSS its own caster every time the blade swings to the far side, and for
that moment the ball reads as the thing being shot.

**AND IT MOVED THE TIP RATE BY THIRTEEN POINTS, WHICH NOTHING PREDICTED.**

```
                                    tip-mounted     ball-centred
mean ENTRY point along the shaft         0.69            0.79
passes reaching the far quarter           64%             77%
```

Firing from the centre puts the near end of the beam inside the caster, so the
quarry can only ever enter further out. **The tip bonus now fires on three
passes in four.** That is the exact axis `vesper_sweep [3]` exists to put to
Rick — and an art note moved it before the sweep did.

**AND IT MADE THE RELIC WEAKER, WHICH IS THE OPPOSITE OF WHAT [2] SAID.**
`range 300` measured from the centre is a shorter reach than 300 measured from
a tip 138 units out: the far end used to be able to sit 438 units from the
ball and now sits at 300. Re-bisected, the blade goes UP to compensate — see
§4b.

> `beam_probe`'s time-on-target number was right and incomplete. It swept the
> origin with `range` HELD, so it priced "where does the shaft start" and
> never "how far does the shaft now reach". **A knob that moves the origin of
> a fixed-length object also moves its reach, and a sweep that holds the
> length cannot see that.** Same shape as §4.6 of CLAUDE.md, one level up.

## 1.4 THE GROWTH IS IN THE GEOMETRY, NOT PAINTED OVER IT

`beamLen(B, u)` is one function — eased-cubic out over `open: 0.30`, linear
back over `close: 0.22` — and **`inBeam` measures against it.** A shaft 24
units long has a 24-unit hit volume.

```
frames with the shaft still opening or closing   3267 of 30972
shortest length a contact was tested against     24.3 of 300
```

A growth animation drawn over a volume that was full-length from the first
frame is v43's hexagon with a clock on it: the drawn boundary and the tested
boundary would be two objects again, and the disagreement would last exactly
as long as the animation. `vesper_relic_probe [4]` asserts it.

**And `tipFrom` is measured against the CURRENT length**, so the lit band the
viewer can see is the band that pays at every instant of the growth, not only
when the beam is full.

## 1.5 THE ART, AGAINST THE REFERENCE FRAME

What the reference actually contains, read off it rather than paraphrased, and
every one of these is a thing the first cut did not have:

```
A MUZZLE COLLAR       a flared ring AT THE SOURCE, wider than the shaft, with
                      the beam emerging from inside it. The first cut had a
                      small white dot. Drawn on the RIM (0.72 R) rather than
                      at the origin, because at the origin the ball covers it.
BANDED STRIATION      not one gradient. A white core carrying the MASS, with
                      discrete bright bands above and below and dark between
                      them. The first cut put five bands in the outer third
                      and they fused into one pink smear at render scale —
                      the arena is 520 wide and ships at 540, so a band under
                      about 1.5 device pixels is not a band.
A SPLASH AT THE END    the far end is not a cap, it is 22 jagged rays thrown
                      outward across a 2.3-radian spread. The beam is HITTING
                      something, and this is the single biggest difference
                      between the reference and a bar with rounded ends.
                      Deterministic off `shellHash`, so the app and the
                      capture agree.
ORBIT MARKS           dashed arcs at the muzzle, turning opposite ways, on
                      `m.t` so the post chain's four draws cannot advance them.
```

**`half` went 22 → 28 and that is a LOOK call inside a measured band.** At 22
the beam rendered as a bright line. `beam_probe [4]` prices the whole 17 → 26
range at +0.02s of mean pass and +0.2 passes a window, so thickness is very
nearly free in the mechanic and not free at all in the picture. 56 wide against
a 68-wide artifact — clearly past §1's "at least half" floor of 34, and still
narrower than a relic.

**And the halo reaches past `half` on purpose.** The tested volume is
`ballR + half`, because `inBeam` compares against the quarry's own radius — so
a shaft drawn at exactly `half` UNDER-draws the thing that hits by 34 units.
The hard banding still marks `half` exactly; the halo is the soft part of a
volume that really is softer at its edge.

## 1.6 AND IT ENDS IN A BLUNT POINT

Rick, off the v2 clip: *"the beam looks better now but it needs to end in a
point. like the tip of a dull pencil."*

`beamHalfAt(u, t)` is the profile — full `half` out to `taper: 0.62`, then a
straight cone down to `tipW: 0.26` — and **`inBeam` reads it.** The volume
comes to the same point the picture does; every band, the halo, the core and
the far-quarter wash are all filled against the same function sampled at 20
steps, so nothing in the silhouette disagrees with anything else in it.

**A drawn taper over a rectangular volume would put the disagreement exactly
where the tip bonus fires**, which is the worst place in this relic to put
one. v43's hexagon, aimed at the mechanic.

**THE 22-RAY SPLASH IS GONE RATHER THAN SHRUNK.** v2's far end was a spray
across 2.3 radians, which reads as an impact and is the exact opposite of a
point. What replaces it is the blunt end the taper already makes, a hot nub so
the point reads as lit rather than as a shaft that stopped, and four short
glints inside a 0.30-radian cone ALONG the bearing — so the point has a
direction instead of a spray. Nothing at the end is wider than the profile's
own end.

**AND THE TAPER COST ALMOST NOTHING ON THE BONUS**, which was not obvious
going in:

```
                                    v2 (rectangular)    with the point
passes reaching the far quarter            73%                72%
mean entry point along the shaft           0.79               0.77
passes over the same seeds                 192                178
```

The quarry mostly enters at 0.77 — just past the 0.75 line — so narrowing the
last stretch removes volume the ball was rarely in. Total contact does fall
7%, so the relic is weaker overall; the tip's SHARE of it barely moves.

> `tipW` and `taper` are read with `=== undefined` and not `||`. A `tipW` of 0
> is a legitimate thing for a sweep to ask for — a beam that comes to a true
> needle — and `|| 0.26` would silently refuse it. CLAUDE.md §4.3, and v41's
> `feed` is the time this project paid for that.

## 1.2 THE DRINK IS THE WARD'S FOURTH ENDING

`drinkWard(f, want)` sits beside `spendWard` and is deliberately neither it
nor `shatter`: it takes a sip, it repeats every frame, nothing is burst and
nobody is flung — **because nobody broke the plate, the relic drank it.**
`shieldMax` is left alone while the pool falls, so the gauge drains rather
than shrinking.

`scythe_survey §4.2` is the standing warning: a shatter and an expiry already
write the same three fields, so nothing outside the engine can tell a broken
plate from a lapsed one. A drink written as either would be a third
indistinguishable ending.

**The loop closes, measured from both ends:**

```
ward drunk over all windows          483.8
ward banked DURING those windows     910.0   (2.93 a second, against beam_probe's 2.0)
base duration                        4.0s
mean window                          4.58s   longest 8.03s   cap 9.0s

STARVED (the plate emptied inside the drink)   n=60  mean 3.63s  max 4.008s
FED     (the shipped path)                     n=57  mean 4.58s  max 8.03s
```

**A beam given nothing runs 4.008s against a base of 4.0.** That is the floor
asserted rather than assumed, and it is `vesper_relic_probe [5]`.

---

# 2. THE THREE THINGS THE BUILD DOES THAT THE BRIEF DID NOT ASK FOR

## 2.1 A TRUE STUN TAKES THE WIND-UP AND NOTHING TAKES THE BEAM

`breakSpin` grew a second clause, above the early return, exactly where the
Crucible's hold sits and for the same reason: this relic carries no `ultSpin`
at all. It is gated on `phase === "wind"`.

**Once the beam is lit it stands.** A light that could be switched off by a
blow is a light nobody would build a set-piece around — and what a stun does
to a standing beam is stop the blade turning, which stops the ORIGIN moving
and not the bearing. The weapon is locked; the watch is not.

## 2.2 THE BEAM CANNOT OUTLIVE THE MATCH, AND THAT IS A FOURTH ENTRY IN AN EXISTING BLOCK

`decay()` already clears the shades, the spike storm and the Converse on
`over`, and says why each time: `step()` returns from the `over` branch ABOVE
their ticks, so a set-piece left running sits frozen through the whole verdict
beat. Sentinel is exactly that shape — a shaft drawn from live state,
across the hall — so it is a fourth entry rather than a new rule.

**The tick's own guards cannot reach this.** They end the window when the
quarry dies, and they do cover the case where a `killFlight` defers
`checkEnd`; a kill with no flight sets `over` in the same step, one function
below `tickSentinel`, and the tick never runs again. Measured before it was
written: **7 steps of standing beam over a dead quarry across 57 windows**,
and a frozen pink shaft across a 2.4s verdict panel.

## 2.3 THE FIELD IS A SWIRL AND NOT A BEAM

`mode: 'beam'` spawns along the cast-time axis and FREEZES there — right for
the seven instantaneous shafts that carry it, wrong for the one beam in the
game that turns, because the motes would sit on a bearing the beam left two
seconds ago. A swirl holds them tangentially at a radius, which is what a
turning thing looks like. Written into `src/render/fx.js` AND the inlined
copy in the same commit; the builder refuses to write unless the two are
byte-identical and then re-stamps the sha.

---

# 3. THE PICTURE FAULT, AND EVERY HEADLESS CHECK IN THE REPO CALLED IT GREEN

`_drawBeam` is on the **Renderer**. `beamTip` is on **Match**. The first cut
wrote `this.beamTip(f)`.

```
27 checks in vesper_relic_probe        PASS
engine_ab, 280 matches                 IDENTICAL
chain_audit, 14 inserts                ok
post_identity                          PASS
the first rendered frame               TypeError: this.beamTip is not a function
```

**The probe's own [1] passed on it**, because it was regexing `_drawBeam`'s
source for `beamTip(` — and a string does not resolve a reference.

This is CLAUDE.md §4.0 and §4.1 arriving on schedule and being caught by the
thing that is supposed to catch them: the build brief's §0 item 3 says film it
before you tune it, and filming it is what found this in the first thirty
seconds of capture.

**The permanent check is a live call.** `vesper_relic_probe [1]` now drives a
real match to a standing beam and invokes `AC.renderer._drawBeam` against a
real 2D context — 273 wind-up frames and 1250 standing-beam frames — instead
of reading its source. When a render catches something a probe could not, the
deliverable is a MEASUREMENT of the thing it saw.

> A second, smaller version of the same lesson is in `vesper_relic_probe`'s
> own docstring: the first cut of the ledger re-derived `inBeam` from OUTSIDE
> the tick and disagreed with the build on five counts. **All five were the
> instrument** — the release frame, a lethal pass, hit stop returning above
> `tickSentinel`, a match ending mid-window, and a "starved" arm that was
> being fed by `tickShots` one function above the drink. The ledger now wraps
> `inBeam` itself and every clock it reports is `B.t`.

---

# 4. THE GATES

```
vesper_relic_probe   27/27
engine_ab            280/280 IDENTICAL over 8 relics x 10 seeds x 28 pairings
chain_audit          ALL 14 INSERTS SURVIVE   --builder vesper_build.py
post_identity        325,708 px identical, max delta 0
verify --n 40        see below
frame_probe          NOT RUN — it crashes on every build in this repo,
                     old tip included (open item 14)
```

---

# 4b. THE BISECTION, AND A METHOD NOTE THAT IS NOT ABOUT THIS RELIC

`vesper_sweep [1]` and `[2]`, escalating sample, 1092 fights each:

```
THE BLADE ALONE, window suppressed (charge 1e9)     dmg 23.95
THE BLADE, at the shipped ultimate                  dmg 17.50
```

**So Sentinel is worth 27% of this weapon.** The builder's own comment
predicted "near Lastlight rather than near Thornwake"; it landed exactly on
Lastlight.

## AN ESCALATING BISECTION CONVERGES ON NOISE IN ITS TAIL, AND THIS ONE DID

v43 §14.1's cheap win is real and this file claims it — but the escalation has
a failure mode nobody has written down. Look at `[2]`'s last three steps:

```
   15.44   42.9%   n=182
   15.78   45.3%   n=234
   15.95   44.6%   n=312
```

**The ordering across those three is noise.** n=312 is ±2.8pp, the interval
being resolved is 0.5 damage wide, and 0.5 damage does not move the win rate
by 2.8 points. The bisection is choosing between arms it cannot tell apart,
and it lands wherever the last coin came down.

Confirmed the answer directly instead, n=1040 (40 per opponent) a point:

```
   dmg  15.50    45.5%
   dmg  16.04    47.8%     <- what the bisection returned
   dmg  16.60    49.2%
   dmg  17.20    54.1%
```

Monotone, and the 50% crossing is between 16.60 and 17.20 — so the bisection
came back **about 0.6 damage low.**

**THEN THE ORIGIN MOVED AND ALL OF IT WAS RE-MEASURED.** Rick's ball-centred
beam is a different relic, so the number above is history. Re-measured at the
shipped geometry, two independent seed streams:

```
   dmg  13.00    28.3%                dmg  17.20    50.9%
   dmg  14.50    39.1%                dmg  17.50    50.1% / 50.3%   <- SHIPS
   dmg  16.00    44.2%                dmg  17.90    52.4%
   dmg  17.50    50.1%
```

**`dmg` = 17.50, which is Lastlight's number to the digit** — so Vesper sits
exactly ON the scythe floor rather than under it. That is a coincidence and is
recorded as one. Against the blade-alone 23.95, Sentinel is worth **6.45
damage a blow: 27% of the weapon.**

> **THE RULE: SIZE THE BISECTION'S TOP TO THE INTERVAL IT ENDS ON, OR CONFIRM
> THE ANSWER WITH ONE WIDE DIRECT MEASUREMENT.** The confirmation cost 4160
> fights against the bisection's own 1092 and is the only reason the number
> shipped is not the noisy one. That belongs in CLAUDE.md §6 beside the three
> cheap wins, because every relic since v40 has been tuned this way.

---

# 4e. THE SOUND, AND THE AUDITION THAT REFUTED THE FIRST CUT

Sentinel ships **six** voices. Five are events; the sixth is the reason the
beam is not silent for most of its own duration.

```
vesper           the cast, routed to the wind-up
vesper-wind      the charge-up — a RISE, which almost nothing here is
vesper-open      the beam standing up — a thump with a long ring that does NOT rise
vesper-hum       THE BEAM, STANDING. a bed, plus DYNAMO on top when it pays
vesper-pass      a pass landing
vesper-tip       the far end connecting
```

**THE HUM IS A RE-STRIKE, NOT A HELD NOTE**, at 0.24s against 0.42s decays so
they overlap into a floor. `_tone` ends on an exponential ramp over its whole
length and `_burst` does not loop its 0.6s buffer — both chain-wide (open item
6), neither a relic build's to fix, so this is written inside their envelope
the way v43's was.

**RICK PICKED DYNAMO OFF A SPREAD OF FOUR, IN ONE ROUND TRIP.**
`sentinel_hum_lab.py` rendered each candidate as a full 3.6-second RUN with
passes and a tip over the top — a single strike would have been the wrong
question, because what has to be judged is whether four seconds of it is a
presence or a nuisance. Rule 2, working exactly as written.

## AND THEN THE AUDITION REFUTED THE FIRST CUT OF THE CUE

Rick: *"we need the sound effect to reflect weather or not the beam is
connecting. the audio should be our cue that its doing damage"*, then *"a
static hum and then the sawtooth of dynamo is the damage connecting."*

Built first as CONTACT-driven — the dynamo swelling for as long as the beam
touched the quarry. `sentinel_hum_audition.py` renders one REAL window off the
engine's own `SFX.play` call list, and it says:

```
contact-driven   ..##########::...    12 loaded strikes, 2.4s of dynamo
payment-driven   ..##....##:......     5 loaded strikes, two clean swells
and it paid:     pTpT                  TWO passes, two tips
```

**The beam pays ONCE PER PASS, ON ENTRY.** A long contact is not more damage,
so a cue that swells for the whole of it says *lots of damage* while one hit
lands. The load is now raised in `beamHit` — where the damage actually is —
and nowhere else, decaying at 3.4/s. **The number of swells in a window is the
number of times the relic was paid.**

> **A SPREAD CANNOT ANSWER A TIMING QUESTION AND NEITHER CAN A SYNTHETIC RUN.**
> Whether a cue reads depends on the rhythm of the thing it cues, and this
> beam's rhythm is a ballistic ball blundering through a turning line at
> intervals nothing in the design sets. `sentinel_hum_audition.py` exists
> because the only honest audition is the engine's own call list, in order,
> with nothing invented.

---

# 4f. THE WIND-UP: SPEED DOES NOT FIX IT, AND RICK TOOK THE COUNTER

`vesper_relic_probe [8]` measured the charge-up losing 51.2% of its casts to
Axiom, Spellbreaker, Foregone and Paradox, against **0.0%** to a control of
four that cannot apply a true stun. v44 measured the Crucible at 14.77%
through the same `breakSpin` hook.

Rick: *"if the wind up loses to stun that often we need to make it wind up
faster. its fine for it to lose sometimes but not that often."* Measured, 8
seeds an arm:

```
wind   lost to the 4 hex appliers    control of 4
0.85          51.2%                      0.0%
0.60          48.8%                      0.0%
0.45          41.5%                      0.0%
0.32          40.2%   <- ships           0.0%
0.22          34.5%                      0.0%
0.14          21.0%                      0.0%
```

**A SIX-FOLD CUT IN LENGTH BUYS A HALVING OF THE LOSS RATE.** The curve is
shallow because hex is not a point event: `stunEvery: 1.15` is advanced by
`dt * stacks`, so at five stacks a stun is APPLIED every 0.23s and `breakSpin`
fires on every application. A window of any length lands inside that comb, and
0.14s is seventeen frames — not a telegraph, and the telegraph is the only
reason the wind-up exists.

So `wind` went 0.85 → **0.32**, which is Rick's instruction honoured as far as
it goes, and the remaining 40% was put to him as a structural question with
three answers: pause instead of cancel (→ ~0%), pause with a cap (a number he
picks), or leave it.

> **HE TOOK THE THIRD, AND IT IS SETTLED RATHER THAN OPEN.** 40% against four
> of twenty-seven relics is Sentinel's hard counter, deliberately. That makes
> it the ONLY relic in the game whose cast a true stun destroys outright —
> where the Crucible, offered the same three strengths in v44, was given the
> mildest. The asymmetry is intentional and this paragraph is why it should
> not be "fixed" by a later session reading it as an oversight.

---

# 4d. "CAN YOU FIX THIS BY JUST MAKING THE BEAM LONGER?" — NO, AND IT COST HALF THE DESIGN'S MAIN AXIS

Rick asked the obvious question after the origin move made the relic weaker.
Measured, `dmg` PINNED at 17.50 in every arm so the win-rate column reads as
"did this arm get stronger" rather than being flattened by a bisection:

```
   range    win%  pass/win  tip rate  TIP SHARE  ult share  mean dur
     300   50.1%       4.3       73%        38%        42%     47.5s
     360   50.8%       4.6       67%        35%        43%     47.5s
     420   48.6%       4.6       58%        33%        43%     48.3s
     480   49.2%       4.4       53%        29%        39%     48.5s
```

**Every win rate is inside ±1.2pp.** Length buys nothing in strength, so it
cannot substitute for the damage change — and it spends the bonus: 73% → 53%
of passes reach the far quarter, and the tip's share of the cast falls from
38% to 29%.

The reason is the origin move again. Centred on the ball, extra length is
added to the NEAR part of the shaft — where the quarry can never be, because
ball collision keeps it 68 units off — while the tip zone slides outward past
where the ball actually is. Mean entry is already 0.79 of the length.

## AND THIS REFUTES THE BRIEF'S §3.3

The build brief called `range` **"the sweep's main axis"** and **"nothing else
in the design has a trade this clean"**, on `beam_probe`'s overlay numbers:

```
                  OVERLAY (tip-mounted)        BUILT (ball-centred)
range 180  ->  2.8 passes,  73% reach       (not measured)
range 300  ->  3.5 passes,  60% reach       4.3 passes,  73% reach
range 420  ->  3.8 passes,  45% reach       4.6 passes,  58% reach
range 480  ->  (not measured)               4.4 passes,  53% reach
```

**The tip rate still falls. The pass count no longer rises.** 4.3 → 4.6 → 4.6
→ 4.4 is flat inside noise, so the axis is not a trade any more — it is just a
cost. Half of the design's cleanest mechanism went away when the origin moved
thirty units, and the brief's own instruction ("if a number has moved, the
design doc is wrong and it is yours to say so") is why this section exists.

> **A KNOB'S TRADE CAN BE A PROPERTY OF SOMETHING ELSE'S SETTING.** `range`
> traded pass count against tip rate because the shaft started 138 units out;
> from the centre, added length lands in a dead zone. Nothing about `range`
> changed. This is the same class as v43 §4.2 and §4.1c — a measurement that
> is right about the thing it swept and silent about the thing it held.

**RECOMMENDATION, AND IT IS A PICTURE CALL NOT A BALANCE ONE:** keep 300. It
is the best arm on tip share and equal-best on win rate. If a longer shaft is
wanted for the look, 360 costs 3 points of tip share and nothing else; past
420 it starts spending the mechanic.

---

# 4c. THE NAME IS *SENTINEL*, WITH NO ARTICLE

Rick, 2026-08-30: *"the ult is called sentinel. not the sentinel."* The design
doc and the build brief both wrote it with the article; he did not.

**The bare noun is also the register the roster already uses.** Reprisal,
Aegis, Bulwark, Retrace, Daybreak, Slagburst, Goreshard, Converse — none carry
an article. The two that do, Winnowing and Harrowing, are gerunds, where the
article is doing grammatical work rather than decorative work. So this is the
same class of error as v43 §15 and the design doc's own §7: **generalising
from the two nearest examples instead of reading the roster.** Third time this
project has paid for that, and the first two are both written down.

He then made it a standing rule for everything, not just this relic: names,
brands and items are written bare.

---

# 5. WHAT IS STILL RICK'S

Five of the seven are answered — the cell, the ult mechanics, both forks, and
both names. **Two are open and neither can be answered by measurement:**

1. **THE SCRUNCH CARD.** The placeholder is `"Sweeps a beam from the blade
   tip. Its far end hits hardest"` — 58 of the 72 characters `verify` allows,
   carrying no number (Bulwarden's precedent).
2. **THE ART AND SOUND SPREADS.** Four voices ship (`vesper-wind`,
   `-open`, `-pass`, `-tip`, plus the bare id routed to the wind-up) and all
   five are rendered and measured in an `OfflineAudioContext`. They are a
   first cut, not a spread — rule 2 says offer him one.

---

# Open decisions

1. **THE PUSH IS CUT, AND THAT IS A DECISION RATHER THAN A MEASUREMENT.**
   `beam_probe [3]` moved the quarry from 0.56 to 0.59 of the way down the
   beam at six times the force, so a push that pushes is not available at this
   tracking rate. The brief said build it as a token shove for the picture or
   not at all, and that if it ships it must not be a dead knob — this project
   already carries two (`shot.life`, `s.snap`) and both are in the open items
   list because a knob that does nothing teaches the next person they are
   protected. **The honest alternatives are a shove at the TIP on the bonus —
   a different sentence from the one Rick wrote — or nothing.** Currently
   nothing.

2. **THE WIND-UP IS FIVE TIMES MORE FRAGILE THAN THE CRUCIBLE'S, AND THAT IS
   DESIGN od 1 ANSWERED.** `vesper_relic_probe [8]`: **71.4% of casts lost**
   against Axiom, Spellbreaker, Foregone and Paradox, against **0.0%** against
   a control of four that cannot apply a true stun. v44 measured the Crucible
   at 14.77% through the same hook. A 0.85s charge-up on a 16s bar, and this
   ultimate has no fallback — a broken cast gets nothing. Shorten `wind`, give
   it partial credit, or accept it as the counterplay. **Rick's.**

3. **`drink 6.0 / durPer 0.12 / durCap 9.0` ARE THREE PLACEHOLDERS THAT ONLY
   MEAN ANYTHING TOGETHER.** No window reached the cap in 57 casts (longest
   8.03s), so `durCap` is currently a guarantee rather than a constraint —
   which is what it is for, but it means the sweep has not yet been asked
   whether it should bite. `vesper_sweep [4]` is the table.

4. **`passDmg 9.0` AND `tipMul 1.8` HAVE NOT BEEN SWEPT AND `dmg 22.0` HAS NOT
   BEEN BISECTED.** Everything above is measured against placeholders, per the
   brief's own order: film before you tune. `vesper_sweep [3]` puts
   `range x tipMul` to Rick as a SHARE TABLE — what fraction of the cast is
   paid at the far end — rather than as a win rate, which is v43's framing and
   the one Thornshear's growth schedule was chosen on.

5. **`crowdMul` IS NOT SET ON THIS RELIC AND PROBABLY SHOULD NOT BE.** The
   Sentinel puts no extra bodies and no extra projectiles on the floor — one
   beam, ~4.7 passes a window. It is the first ultimate since v37 that does
   not obviously belong in `beat()`'s crowding loop, and saying so is cheaper
   than the storm's measurement. If a filmed clip shows the director cutting
   away from the beam, that is the evidence to change it.

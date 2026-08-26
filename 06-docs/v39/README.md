# v39 — FOREGONE and THE CONVERSE. The twenty-first relic.

**2026-08-20.** The runic × scythe cell, chosen against a measurement of all
twenty-two open ones and built the same session. The design capture is
`design.md`; the survey and the look-first probe that ran before any of it are
`look.md`. This is what shipped and what it cost.

```
02-chain/sc-foregone.html   b1a58c5a3982a8cf   <-- BUILD OF RECORD CANDIDATE
built off 02-chain/sc-redflail.html            07d4c845732cfe72
01-live UNTOUCHED, still on sixteen

cell_survey          7/7    all 22 open cells, before the choice
runic_scythe_probe   8/8    the chosen cell, before the design
foregone_probe      16/16   on the tuned build
engine_ab           1710/1710 IDENTICAL field for field on the other twenty
verify.py --n 40    13/13 . 0/8400 timeouts . spread 14.1pp . mean 37.8s
                          Foregone 50.2%
director_diag       Converse 15.61x -> 1.83x ex-kill; Triplicate & Bloodmill
                          untouched (neither declares ultTrace)
foregone_sweep override checked against a real rebuild: 400/400 identical
```

Tools written: `cell_survey.py`, `runic_scythe_probe.py`, `foregone_build.py`,
`foregone_probe.py`, `foregone_sweep.py`, `foregone_strip.py`. Generalised:
`director_diag.py` (its window predicate, for the third time).

---

# 1. WHAT IT IS

```
id foregone · Foregone · runic · scythe · reach 104 width 11 spin 3.2
mass 2.4 · mode spin · onHit {hex:1} · dmg 22.0

ult CONVERSE · kind "retrace" · charge 15
    PHASE 1  THE LAYING, 4.0s. A sigil at the cast site, then one every 130
             units TRAVELLED, ceiling 12. Each pulses every 0.62s for 2.0
             damage inside radius 88, no status. The caster fights normally.
             A line is drawn through them in the order laid — presentation.
    PHASE 2  THE REVERSAL, ~1.1s. The caster leaves its own steering and
             runs the polyline backward at 1600 u/s against a cruise of 405.
             Each sigil blooms as it is reached: 9.0 damage inside radius
             130, and 2 stacks of hex. It ends at the oldest sigil.
    NOTHING BREAKS IT.
tip "Leaves sigils as it moves, then rewinds its path through them"  60 of 72
```

**The name.** Runic's register is logic — Axiom, Corollary, Unmaking.
*Foregone* does two jobs no other candidate did: "fore-gone" is literally
*already travelled*, which is what the trail is, and a foregone conclusion is
one whose end is settled before it arrives, **which is Rick's fourth interview
answer stated as a name.** *Converse* is the logical operation that reverses a
statement, sitting beside Corollary in the same vocabulary.

---

# 2. THE REVERSAL WAS 65% TOO FAST AND THE `speed` KNOB DID NOT MEAN WHAT IT SAID

First build: the retrace advanced `f.x` from wherever it found it, and set
`f.vx` so the trail, the blur and the weapon's lean would read right.

`move()` runs before `tickRetrace` and has **already integrated `f.vx` into
`f.x`** by then. So the two integrations ADD. Measured: **2645 u/s against a
`speed` of 1600.**

The fix is not a scale factor. The rail carries its own position — `S.px, S.py`
— which is advanced by the budget and then ASSIGNED to `f.x, f.y`, so move()'s
contribution is overwritten rather than compounded. Measured after:
**1577 u/s against 1600**, on position, over unfrozen frames.

**And the check that caught it had to be rewritten to catch it.** The first
version read `Math.hypot(f.vx, f.vy)` and got 1297 — which looked like
`CONFIG.physics.speedMax` (1300) and invited exactly the wrong diagnosis. The
build sets vx/vy for the ART; the position is the motion. **An instrument that
reads the decoration measures the decoration.**

---

# 3. THE PROBE REPORTED 11 BLOOMS OF 12 AND CALLED IT A BUILD FAILURE

It was not. `f.ultTrace` is nulled in the same frame the final sigil is
reached, so anything reading the counters after `step()` is **permanently one
bloom short**.

Counted at the firing site now — `_traceBurst` is wrapped, the same technique
v38 used on `fireUlt` — and the check is stronger for it. It no longer asserts
a count at all:

**the bloom POSITIONS are asserted to be the laid positions reversed, one for
one.** A reversal that fired every bloom in the wrong order passes a count and
fails this.

---

# 4. WHAT THE CELL WAS FOR, AND THIS TIME THE RATIONALE HOLDS

v38 §4b found the hemorrhage uptime that justified building Threshmaw was worth
−0.5pp. That is the mistake this section exists to check for.

The ultimate ON and OFF, on **identical seeds**, damage untouched:

```
              mean    >=2   at cap  fires/s   lock
  ult OFF     0.62    14%     1.2%    0.448  22.8%
  ult ON      0.91    21%     5.7%    0.663  26.6%
  delta      +0.29   +7.3%   +4.5%   +0.215  +3.8%
```

**Hex at its cap goes 1.2% → 5.7%, and the delivered lock 22.8% → 26.6%.**

The rationale holds, and it holds *because* the design was aimed at the right
quantity. The look-first probe found that hex is a RATE — `hexClock += dt *
stacks`, fire at 1.15 — so the cap is a 5× lock rate rather than a bigger
number. An ultimate that applies hex would have bought occupancy; one that
drives twelve applications into a single second buys the **cap**, which is the
only place the rate multiplier pays.

That is the difference from v38, stated plainly: **the design named a mechanism
and the mechanism is what moved.**

---

# 5. THE DIRECTOR, AND A CROWDING ULTIMATE THAT PUTS NOTHING EXTRA ON THE FLOOR

`director_diag` measured **15.61x** preference for the inside of a Converse
window, ex-kill. Triplicate was 4.59x when Rick called it distracting;
Bloodmill was 14.08x.

## Why, and the answer was not the one the code comment predicted

The comment v38 left at the crowd condition reads *"ANYTHING THAT PUTS EXTRA
HITS ON THE FLOOR BELONGS IN THIS LOOP."* This relic **puts nothing extra on
the floor.** Its pulses are deliberately outside `resolveHit` and emit no beat
— §6 — precisely so they could not do this.

Broken down by cut KIND, 50 matches:

```
  kind     inside  outside   in/min  out/min    pref   median score in/out
  ult           0        0     0.00     0.00       —   the ult beats never cut
  hit          22        4     3.39     0.19   18.0x   2.51 / 2.11
  volley        8        4     1.23     0.19    6.6x   3.15 / 2.26
```

**Not one `ult` cut in fifty matches.** Every cut inside the window is an
ORDINARY BLOW, landing more often and scoring higher — because the ball
throwing it crosses the hall at four times cruise, through twelve sigil
positions in about a second, and `tickHits` resolves every pass at that closing
speed.

So the comment is right and not quite general enough. What belongs in that loop
is **anything that puts extra CUTS on the floor, however it does it.**

## The value, swept

160 pinned matches, with the fights simulated ONCE and only the plan recomputed
per value — `crowdMul` does not touch the sim, so a row that re-simulated would
be buying the same fights twice at the cost of the sweep's resolution:

```
  crowdMul    0     3     4    4.5    5     6     7     8     9    10+
  ex-kill  15.61 10.17  4.32  3.82  2.66  2.49  1.83  1.33  1.16  1.00
```

**7 taken — and NOT by v38's rule.** Bloodmill's curve fell off a cliff and
"the last value above parity" picked itself. This one **flattens at exactly
1.00x from 10 onward**, because the cuts that survive are single hits and a
grouping rule cannot touch a single hit — the same floor v38 hit at 11.90x
before it changed instrument. So the choice is between parity and a value above
it, and v37's argument decides it: 1.00x would be wrong, because the ultimate
does put more real spectacle on the floor. **7 lands the third crowding
ultimate in the band the first two were tuned into — Triplicate 1.69x,
Bloodmill 2.16x, the Converse 1.83x.**

`director_diag`'s window predicate has now been generalised three times
(Triplicate → the spike storm → the Converse) and each time it was the thing
that had to change, because an ultimate's "window" is whatever state object it
hangs its duration on. **There is no shared field to read**, and that is worth
fixing before a fourth.

---

# 6. A PULSE IS NOT A SWING

v38 §7 found the published contact-rate table counting ultimates as contact,
and four relics carrying almost all of the error — the four "many small
objects" ultimates.

This relic fires up to **seventy-four rings a cast**. If any of them
incremented `f.hits` it would be the largest such error in the game by a factor
of four. They do not: damage goes through `hurt`, so a ward eats it exactly
like anything else, but nothing routes through `resolveHit` and `f.hits` is
never touched. Asserted: **+0 across a cast that fired 74 rings.**

---

# 7. THE BLADE — 22 AGAINST THE TYPE'S 24.4, AND IT IS THE OPPOSITE SHAPE TO LASTLIGHT

Swept on pinned seeds, 20 foes × 24 seeds = 480 matches a candidate, SE 2.3pp:

```
   dmg   31.35   26     22     18    17.5    15     14     12
   win    67.5  59.0   50.8   40.0   38.1   32.5   27.1   27.5
```

**22 taken.** The type's own damage is Thornwake's 31.35 against Lastlight's
17.5, mean 24.4 — so this relic pays **10%** in the blade. **Lastlight pays 44%
and IS an ultimate with a scythe attached. This is a scythe that has one.** Two
relics of one type arriving at opposite shapes, independently, is the type
doing its job.

`foregone_sweep`'s runtime override was checked against a real rebuild at
dmg 18: **400 matches, identical field for field.** An instrument standing in
for another instrument is a guess with a table around it until it is compared.

`verify.py --n 40`: **13/13**, 0/8400 timeouts, every relic in band
(Axiom 45.2% .. Grudgebearer 59.4%), **spread 14.1pp — tighter than the 16.1pp
the twenty-relic roster carried**, every pairing 18–70s, overall mean 37.8s.
Foregone lands at **50.2%**.

---

# 8. THE ART, AND THE SOUND

## The trail

Drawn from `f.ultTrace` and **not** from `m.ultFx`. ultFx is a fire-and-forget
record with a clock of its own that expires; these are live simulation objects
whose positions the sim keeps updating. `_retraceField` is called ABOVE the
`_ult` guard in `drawUltUnder`, because that guard returns when ultFx has
expired and the trail outlives it.

The sigil ring **breathes on its own pulse clock**, so the ring the viewer
watches expand is the same clock the damage fires on. Ward's plate brightness
IS its timer; this is that rule again, and it is why this ultimate needs no
second HUD element either.

**`core` and NOT `glow`, and this is v37 §3.2 for the fourth time.** Runic's
glow is `#BCDDFF` — near-white — and under `lighter` at the alpha the reversal
needs it blows out to pure white, so the one element that is supposed to say
RUNIC on a floor full of it said nothing at all. **The trap is that the LAYING
phase looked correct**: at alpha 0.30 it still read blue and at 0.58 it did
not. Caught off the filmstrip, not off the palette sheet. Rick's word for the
rings is ELECTRIC, and electric is saturated, not bright.

## The Converse's voice — five branches

Runic is the only school whose default ult sound is a rune-crack rather than a
body blow. **Electric is not low and it is not wet**: it is a fast transient
over a narrow resonance — a bandpass burst at high Q — and a pitch that is a
clean interval rather than a beat. Bloodmill was two detuned sawtooths BEATING
against each other on purpose; this is the opposite instrument and shares
nothing with it.

**`foregone-orb` makes the trail count itself.** `p.n` is the real sigil index
out of the sim, so the pitch climbs a step per orb and the ear can hear how
long the line is getting without looking at it — and because it is a sim number
rather than `Math.random()`, a render reproduces.

**`foregone-reverse` is the one sound that has to state the mechanic.**
Everything in the laying phase rises — the cast, and the twelve orbs stepping
up a tone at a time. This falls, through the same interval, at speed. The sound
of the ultimate is the sound of that climb played backwards.

---

# Open decisions

1. **The pulse economy is unswept and it is quadratic.** A sigil laid at t=0
   pulses seven times and one laid at t=3.6 pulses once, so the payload goes as
   `lay`² and `lay` has never been moved. Only **11%** of rings reach the foe;
   `orbDmg` 2.0 and `orbR` 88 were held constant through the whole blade sweep.
2. **`bloomHex` is 2 and unswept.** It is the knob the entire cell rationale
   runs through — §4 — and it was set before that measurement existed.
3. **The reversal's contact damage is a mechanic nobody designed.** §5. The
   caster crossing the hall at 1600 lands ordinary blows at four times the
   usual closing speed, and that is where the director's 15.61x came from. It
   has never been isolated: no `decomp` run exists for this relic. v38 found a
   third of Bloodmill was an undesigned mechanic; **this one has not been
   looked for.**
4. **`speed` 1600 is untested against the picture.** It was chosen to make
   "quickly" true and then a bug made it 2645 for the whole first build. What
   the reversal should FEEL like at 1200, or at 2200, has not been looked at.
5. **No custom set-piece.** The trail and the sigils are drawn, but there is no
   `drawUltUnder`/`drawUltOver` branch keyed to `foregone` and the banner
   treatment is the generic one. Same open decision v38 left for Bloodmill,
   now two relics deep.
6. **The runic mirror reads as one smudge.** look.md §5.1. It rules out the
   marquee fight against Spellbreaker or Axiom.
7. **`director_diag`'s window predicate has been generalised three times.**
   §5. There is no shared field an ultimate's duration hangs on, so a fourth
   crowding ultimate will silently measure zero window until someone edits the
   tool. That is the same class of failure as v38's inert `crowdVolleyMin`.
8. **`tickFire` gates on `f.w.shot`, not on mode.** look.md §5.4. Inert today
   because no melee weapon carries a `shot` field — which is exactly the
   condition that stops holding the first time one wants one.
9. **`hitStop` freezes the hex clock.** look.md §5.3, 9.4% of a scythe fight.
   Almost certainly true of every clock in `tickStatus`, and nothing else has
   been checked.
10. **No posting cut exists.** No seed has been picked, no VO written, no clip
   rendered. `cinema_vo.SPOKEN` has no entry for Foregone or Converse.
11. **Promote to the chain tip and to live?** `01-live` is on sixteen against
   **twenty-one** here. v27 open decision 1, now five relics wide and by a
   distance the oldest open thing in the project.

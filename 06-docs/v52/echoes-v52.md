# v52 — NIGHTFELL'S NEW ULTIMATE, PRICED. It is not Gravemourn's ultimate — the position costs 12 to 19 points, and that gap is the mechanic. The timer wastes three bombs in four, "applies curse" is dead again, and the chain reaction is built by density rather than by knockback.

**2026-08-31, Cowork.** Rick's §1, verbatim:

> *nightfell crackles with purple electricity. for the duration of the ult when
> it lands a hit the hit leaves behind an echo bomb (thinking a pentagram
> imprinted on the battlefield but open to ideas here) the echos slowly begin
> to crackle with the same purple electricity and then explode. dealing damage,
> applying curse and knocking back enemy fighters in its area.*

`tools/bomb_lab.py`. Base curse is v49's: K=3, echo 8%, permanent, displacement
kept, priced on the target. Eclipse's `apply:{curse:3}` and its 11 damage are
stripped in every arm. Arena is **520x800**, `ballR` **34**, and the roster's
novas run **240-320 radius** — which is most of the floor. Runtime only.

---

# 1. THE COLLISION, AND IT SURVIVES THE TEST

Both umbral ultimates are now: *a window; each blow inside it spawns a delayed
explosive; the explosive deals damage, applies Curse and knocks back.* The only
structural difference is that Gravemourn's hand **flies to** the foe and
Nightfell's imprint **stays where the blow landed.**

That is either a sprite change or a mechanic. Measured, 200 fights an arm:

```
                    r=90              r=160             r=240
fuse        catch     win      catch     win      catch     win
0.8s          12%   58.0%        35%   70.5%        58%   74.0%
1.6s          15%   58.5%        38%   60.0%        59%   65.0%
2.6s          12%   57.5%        31%   64.5%        55%   72.0%

the same bomb, HOMING onto the foe (= Gravemourn's design):
radius 90    58.5% stays put   vs   77.5% homing    position costs -19.0%
radius 160   60.0%             vs   77.5%                          -17.5%
radius 240   65.0%             vs   77.5%                          -12.5%
```

**It is a mechanic.** Even at a nova-sized 240 radius the foe is gone 41% of
the time, and standing still costs **12.5 to 19.0 points** against seeking.
Nightfell's ultimate is a bet on where the fight will be; Gravemourn's is a
certainty. That is a real second verb and the §1 earns it.

**The fuse is free, and for a reason worth knowing.** Catch rate is flat across
0.8s, 1.6s and 2.6s at every radius — the foe escapes within the shortest fuse
tested or not at all. At `cruise` 405 a ball crosses 324 units in 0.8s and the
hall is 520 wide. **So the crackle can be as long as it looks good.** (The win
column across fuse is scattered rather than flat; the catch rate is the clean
signal and it is the one that carries the mechanism.)

---

# 2. THE TIMER WASTES THREE BOMBS IN FOUR

His §1 says *"then explode"* — a timer. The fork is a mine: the imprint **arms**
after the fuse and then **waits** for the foe to walk into it.

```
radius   timed catch   timed win    mine catch   mine win   bombs a fight
    60            8%       54.5%           69%      73.5%            4.11
    90           15%       58.5%           78%      74.0%            4.14
   130           26%       59.5%           83%      77.5%            4.19
   160           38%       60.0%           86%      74.0%            4.15
   240           59%       65.0%           85%      72.5%            4.14
```

**A mine at radius 60 catches 69%; the timer needs radius 240 to reach 59%.**
Sixty units is less than two ball diameters — a small dense mark on the floor.
The timer's version of this ultimate needs a blast covering half the hall to
land at all, which is a worse picture for a worse result.

The mine also makes the win column flat across radius (72.5-77.5%), because the
foe walks in eventually whatever the size. **So on the mine reading, radius is a
picture knob and not a balance one** — the opposite of the timed reading, where
it is the only knob that matters.

**This is a change to the §1 and it is Rick's call.** What it costs: the
imprint no longer goes off on its own schedule, so the beat is triggered by the
foe rather than by the caster. What it buys: three bombs in four stop being
wasted, and the pentagram gets to be small and dense instead of arena-wide.

---

# 3. "APPLIES CURSE" IS DEAD AGAIN, AND THE FIX IS IN RICK'S OWN WORD

```
bomb dmg   no curse   + curse   the curse clause adds
      10      56.0%     56.0%                   +0.0%
      20      57.5%     58.0%                   +0.5%
      30      60.0%     60.0%                   +0.0%
      45      69.0%     72.0%                   +3.0%
      60      74.5%     78.5%                   +4.0%
```

Same structural fact as v49 §5b and v51 §3: **the pool holds the three biggest
blows**, so a stack only matters if the thing applying it out-hits the blade.
Nightfell's blows land at ~26, so unlike the flail's hand a bomb *can* clear
that bar — the clause starts paying at 45 — but at ~1 SE it is not established
and it is not what the ultimate is about.

**He already named the fix: "echo bomb."** Stamp the imprint with what Curse
remembers at the moment the blow lands. Mine, radius 90, blade 15.83:

```
stamp        no curse   + curse    adds   bombs   caught   bomb dmg   echo dmg
pool x0.5       75.0%     77.0%   +2.0%    3.94     3.06        117         53
pool x0.75      78.5%     88.0%   +9.5%    3.52     2.66        164         53
pool x1.0       87.5%     93.5%   +6.0%    3.15     2.43        211         52
```

Now the curse clause is worth **6 to 9.5 points** instead of nothing, because a
bomb stamped with a 61-point pool parks a memory the blade cannot displace.

## And it is a COPY, which is what keeps it off Gravemourn's verb

```
GRAVEMOURN   the hands CARRY the memory away, one each, and the pool empties
NIGHTFELL    the imprint COPIES the memory onto the floor, and the pool stays
```

Spend and echo — the two halves of the mechanic, one per relic, on the two
relics measured to want exactly those halves (v50 §4: the flail can only spend;
Nightfell is the one with the contacts to use a rate). The pictures are a fist
diving out of the air and a sigil waiting on the ground. They are not the same
ultimate.

**The multiple is nowhere near 1.0.** At `pool x1.0` the bombs deal 211 damage
a fight into a 400 pool. Nightfell's floor with no ultimate is 54.0% at blade
15.83 and ~31% at blade 13, and a median ultimate is +20.4 — so the stamp wants
to be around **0.3**, bisected. `x1.0` is in the doc to show the shape, not the
setting.

**And the same self-stabilising property the flail has:** bomb damage sits at
211-214 across blade 12 to 15.83, because a lighter blade lands more blows and
plants more imprints. Cutting the blade does not cut the set-piece.

---

# 3b. THE CHAIN REACTION — RIGHT IDEA, WRONG ENGINE

Rick: *"cant we increase the amount of bombs the enemy gets hit by with
knockback? ... getting hit by 1 is almost a chain reaction that will increase
the likelihood they will be sent into another."*

**Knockback is not the engine. It is the brake.** Mine, radius 110, stamp pool
x0.3, blade 13; a chain hit is a detonation within 0.45s of the previous one:

```
bombs a blow   knock   planted   caught   live at once   chained   longest
           1       0      5.09     4.21           1.55      0.25      1.23
           1     850      4.92     4.06           1.57      0.23      1.21
           2       0     10.16     8.35           3.10      3.77      2.44
           2     500      9.94     7.79           3.31      2.60      2.21
           3       0     15.15    12.35           4.64      7.16      3.69
           3     250     15.42    12.04           4.87      5.99      3.46
           3     500     15.03    11.19           5.01      4.58      3.07
           3     850     15.04    10.78           5.21      4.04      3.08
```

**Chains fall monotonically as the shove rises, at every density and every
radius** — 7.16 to 4.04 at three bombs a blow. The reason is geometric and it
is v41's warhammer finding wearing a different hat: **bombs are planted where
blows land, which is a CLUSTER**, so a push ejects the ball out of the field it
is standing in rather than sweeping it through more of it.

**Density is the engine.** At one bomb a blow there is nothing to chain into —
1.55 live at once, 0.25 chain hits, longest run 1.23, which is not a chain at
all. Nightfell lands ~2 blows inside an 8-second window; the ultimate cannot
produce its own chain reaction one bomb at a time.

**Reversing the sign helps, and less than it should.** A blast that DRAGS the
foe inward instead of shoving it out lifts chains from 7.16 to 8.01 at three a
blow, and does not move the longest run at all (3.69 either way) — because
pulling toward the charge that just fired does not move the ball toward its
neighbours. Real, consistent across every row, and small.

## The pentagram is the cluster, and that is his own picture solving it

A pentagram has five points. **One blow stamps ONE figure — five charges evenly
spaced on a ring** — so the density that makes it chain comes from inside the
sigil rather than from carpeting the hall.

```
points   ring r   knock       figures   charges   caught   chained   longest    win
     5       60    none          5.25     26.23    18.41     12.30      5.71  52.5%
     5       60    pull 350      5.06     25.32    18.93     13.24      5.84  48.5%
     5      110    none          5.20     26.00    16.29      9.02      4.51  47.0%
     3       70    none          5.23     15.69    10.88      5.05      3.24  54.5%
```

**Five points on a 60-unit ring: a trigger sets off 5.7 charges on average.**
A chain reaction, and the floor still reads — **five figures a fight, not
twenty-six scattered dots.** The chain is the sigil discharging around itself,
which is a picture; a minefield is not.

It also lands close to tuned already: **47.0% to 54.5% at blade 13 with the
stamp at pool x0.3**, against a 50.0% field.

**The tension to hold onto:** density is what makes it chain and density is
also what kills the property that made this ultimate different from
Gravemourn's. At one bomb a blow the foe genuinely dodges; at twenty-six loose
charges the hall has no safe ground and the bet on position is gone. Binding
the charges into one figure per blow is what buys the chain without buying the
minefield — and it is the only arrangement measured that does.

---

## Rick's call: PUSH, on legibility — and it costs 23% of the chain, not the chain

*"i think the only thing that passes the legibility requirement is push."*

He is right, and the project already wrote the rule down. `CONFIG.arena`'s
no-seek comment: *an invisible steering force on a ball makes it look like it
is breaking its own rules; the viewer cannot see it, so it reads as the physics
lying.* A blast that sucks is that class of thing. A blast that shoves is the
only one a viewer can read off the frame.

The hypothesis that a shove inside a RING throws the ball across the figure
rather than out of it — **refuted.** 5 points, per-charge radius 70, mine,
stamp pool x0.3, blade 13:

```
ring r   push   charges   caught   catch%   chained   longest   bomb dmg     win
    60      0      26.2     18.4      70%     12.30      5.71         67   52.5%
    60    250      25.6     16.4      64%      9.51      4.67         59   47.5%
    60    500      26.1     15.8      60%      7.91      4.18         58   50.5%
    60    800      26.1     14.8      57%      6.29      3.81         55   50.0%
    90      0      26.1     17.6      67%     10.62      5.12         64   45.5%
    90    250      25.9     16.2      63%      8.75      4.41         58   50.5%
   120      0      26.5     15.9      60%      8.47      4.25         58   49.5%
   120    250      25.8     14.6      57%      6.84      3.77         53   47.5%
```

A 60-unit ring is small against a 34-unit ball at 405 cruise; the shove is
radial and the ball leaves rather than crossing. **But the chain survives it.**
At push 250 the figure still fires 9.51 chained hits a fight with a longest run
of **4.67 of 5 charges** — a trigger still takes most of a pentagram with it.

```
                    chained   longest   caught      what it is
no shove              12.30      5.71     18.4      best chain, unreadable blast
push 250               9.51      4.67     16.4      77% of the chain, legible    <- take this
push 800               6.29      3.81     14.8      51% of the chain
```

**And the ring wants to be TIGHT at every shove.** 60 beats 90 beats 120 on
chain length, on catch rate and on damage. A compact pentagram about 120 units
across — three and a half ball radii — not a wide one.

---

# 3c. THE MINE IS SETTLED, AND THE CASTER MUST NOT SET THEM OFF

Rick, on being told what a mine meant: *"thats not what i was picturing but now
that youve mentioned it thats a much better idea."* **Settled: the charges arm
and wait.** Every number in this doc assumes it.

**One art consequence, and it is load-bearing.** With a fuse the crackle is a
COUNTDOWN and the tension is time. With a mine the crackle is ARMING and the
tension is space. **An armed pentagram must look different from a crackling
one**, or a viewer cannot tell which patches of floor are live, and the whole
mechanic is invisible. That is a filmstrip requirement, not a nice-to-have.

**And the landmine framing makes "can the caster set one off" a live question.
Measured, it must not.** 5 points, ring 60, push 250, stamp pool x0.3:

```
arm                   win   charges   foe hits   SELF hits   self dmg   chained   longest
foe only            47.5%      25.6       16.4        0.00          0      9.51      4.67
both balls          32.5%      24.6       10.3        9.54         36      5.50      3.61
both, blade 15.83   47.5%      22.3        9.4        8.37         37      5.12      3.54
both, blade 18      59.5%      19.9        8.2        7.46         36      4.43      3.34
```

**The caster eats 48% of its own charges.** Not a tuning problem — blade 15.83
with self-triggering lands on exactly the same 47.5% as blade 13 without it, so
the cost tunes straight out. It is a DESIGN problem, and the reason is this
game's geometry: **the charges are planted where blows land, which is precisely
where the caster is standing.** The two balls are never apart.

It also fails the rule the shove decision was made on. `CONFIG.arena`'s no-seek
comment exists because these balls do not steer — so "do not walk into your own
minefield" is not a thing a fighter can do. A self-triggering hazard is not a
gamble the wielder took; it is noise, and on screen it reads as the ultimate
malfunctioning. **Foe only.**

---

# 3d. THE TWO KNOBS THIS DOC WAS QUOTING WITHOUT MEASURING

Both were placeholders typed into a probe and then read back as if they were
settings. Third time this session, so it is a pattern: **a number that enters a
lab as a default leaves it as a claim unless somebody sweeps it.**

Settled config, 250 fights an arm: mine, 5 charges on a 60u ring, per-charge
radius 70, push 250, stamp pool x0.3, blade 13, foe-only.

```
HOW LONG A LIVE PENTAGRAM WAITS          (window 8s)
life    charges   caught   catch%   expired   chained   longest   bomb dmg     win
   2       25.6     11.5      45%      10.4      6.81      4.16         43   44.0%
   4       25.2     14.6      58%       6.0      8.61      4.44         54   46.0%
   6       25.1     16.1      64%       3.9      9.43      4.66         59   46.8%
  10       24.5     17.4      71%       1.6     10.01      4.71         63   48.4%
  99       24.6     18.4      75%       0.0     10.59      4.87         66   50.4%

HOW LONG THE WINDOW STAYS OPEN           (life 6s)
window   figures   charges   caught   chained   longest   bomb dmg     win
    4s      2.71      13.6      8.9      5.07      3.63         33   44.4%
    6s      3.81      19.0     12.6      7.35      4.25         46   40.4%
    8s      5.02      25.1     16.1      9.43      4.66         59   46.8%
   12s      7.07      35.4     23.0     13.86      5.43         84   58.0%
   16s      8.58      42.9     27.9     17.21      5.88        101   60.8%
```

**Neither is free.** Lifetime is worth 6.4 points across its range and window
16.4 — and at life 2 **forty percent of every charge planted expires unspent**,
which is the timer's waste problem coming back in a different costume.

## The recommendation: an 8-second window, and the pentagrams DO NOT EXPIRE

**Window 8s with permanent charges lands at 50.4%** — the field mean, with no
further tuning — and it is the simplest rule the ultimate can have:

- **Nothing is ever wasted.** A charge that is not walked into is not a miss,
  it is a charge still waiting. That removes the last of the timer's problem.
- **The hall accumulates.** Figures from an earlier cast are still live when the
  next one lands, so the floor gets more dangerous as the fight goes on. That is
  free tension and it costs nothing to draw.
- **It is one sentence.** *The sigil stays until something sets it off.* An
  expiry needs a second number, a fade, and a viewer who understands it.

Live charges do not run away: 24.6 planted against 18.4 walked into leaves ~6
standing at the end of a 50-second fight. **Untested at the tail** — a 100-second
fight has never been looked at, and saturation is the failure mode to watch.

---

# 3e. AND IN THE SETTLED CONFIG THE CURSE CLAUSE IS WORTH ZERO AFTER ALL

§3 priced the stamp on ONE bomb carrying the whole pool and found the curse
re-application worth +6.0 to +9.5. §3b then split the figure into five charges
for the chain. **Together, the second cancels the first**, and this doc had
both numbers in it without noticing. 250 fights an arm:

```
config                          no curse   + curse    adds   damage a charge
5 charges, stamp x0.3              50.4%     50.4%   +0.0%               3.6
5 charges, stamp x0.6              63.2%     63.2%   +0.0%               6.9
1 charge,  stamp x0.3              46.8%     47.2%   +0.4%              18.4
1 charge,  stamp x1.0              76.4%     85.6%   +9.2%              75.4
```

A charge deals `pool x0.3 / 5` — about **3.6 damage**, against pool entries of
~20 each. Its memory is displaced the instant it lands. **Drop the clause: the
charges do not apply Curse.**

## The general law, now confirmed on three separate designs

Dirge and Eclipse's `apply` field, the flail's hand, and now these charges:

> **An ultimate cannot MINT a memory. The pool holds the blade's biggest blows,
> so anything an ultimate applies is smaller than what is already in there —
> unless it out-hits the blade, and a thing that out-hits the blade is the
> relic.**

What an ultimate CAN do is take one and give it back. That is exactly why
Gravemourn's hand works and these charges do not:

```
GRAVEMOURN   MOVES the memory   takes one entry, deals it, re-parks it. Conserved.
NIGHTFELL    READS the memory   copies the pool's value onto the floor and spends
                                nothing. The pool is never written to at all.
```

Both relics are still built on Curse; neither adds to it. **Twinshade remains
the only relic in the school that fills the pool**, which is the third
relationship and the reason the school has three relics.

---

# 4. THE ADJACENCY THAT HAS TO BE NAMED

**Foregone's Converse already puts sigils on the floor and blooms them.** This
doc is not going to repeat the session's Crucible mistake by not saying so.

```
CONVERSE    sigils laid by the caster's own MOVEMENT, detonated by the caster
            retracing its path at speed 1600. A route.
NIGHTFELL   imprints laid by BLOWS, detonated by the FOE arriving. A trap.
```

Different author, different trigger, different geometry — but they are the two
floor-marking ultimates in the game and they must not read alike. **This is an
art constraint before it is a design one**, and it belongs in the filmstrip
brief: runic blue lines traced along a path against umbral purple pentagrams
stamped where blood was drawn.

---

# 5. THE SCHOOL-LEVEL RISK, STATED ONCE

Both umbral ultimates now route through the pool. That is coherent — it is a
school whose identity is Curse — but it has a cost: **umbral becomes a school
where nothing works until Curse is stacked.** Gravemourn's first cast has 1.9
blows behind it and Nightfell's has ~4. A relic that loses its first exchange
loses its ultimate as well, and that compounding is the thing to watch in the
sweep, not the mean win rate.

Twinshade is the counterweight and needs no changes: Triplicate multiplies the
applier rather than spending or copying, so the school's third relic is the one
that FILLS the pool. Three relics, three relationships to one mechanic.

---

# 6. WHAT THIS INSTRUMENT CANNOT TELL YOU

- The mine has no arming tell, no overlap rule and no cap. Four imprints a
  fight at radius 90 in a 520x800 hall is a lot of floor; whether two can
  overlap, and whether a viewer can tell an armed one from a crackling one, are
  picture questions a filmstrip answers and this does not.
- The armed/arming distinction is asserted as an art requirement in §3c and
  is not measured by anything. Nothing in `tools/` can tell you whether a
  viewer can read a live pentagram from a crackling one at phone size.
- Bomb damage is dealt as a bare `hurt()`, so it scales no hit-stop and no
  Aegis wall stops it. As in v51, every number here is a floor.
- SE is ~3.5pp at 200 fights. The curse clause at bomb damage 45-60 is ~1 SE
  and is a trend, not a result.

---

# Open decisions

1. ~~**TIMER OR MINE.**~~ **SETTLED: MINE** (§3c). Rick's, on being shown the
   catch rates. The crackle is now an arming animation and the armed state
   needs its own read.
2. ~~**DOES THE BOMB CARRY THE MEMORY?**~~ **SETTLED: it carries it and does
   not write it back** (§3e). The figure is stamped with what Curse remembers;
   the charges deal a share of it and apply nothing.
3. **WINDOW AND LIFETIME.** §3d. 8s and permanent lands on 50.4% with nothing
   else moved; 12s and 16s are +11 and +14 and want the stamp brought down.
   The recommendation is the pair, not either alone.
7. **RADIUS, AND THE SHAPE OF THE FIGURE.** On the mine reading the per-charge
   radius is a picture knob — 60 to 240 all land within noise. The RING radius
   is not: 60 chains 5.7 deep and 110 chains 4.5. Five points or three is a
   drawing decision with a measured cost.
6. **THE SHOVE IS SETTLED: PUSH, and small.** Rick's call, on legibility, and
   the project's own no-seek rule backs it. 250 keeps 77% of the chain; 800
   keeps 51%. What is still open is only the exact figure — 250 is the
   recommendation and the sweep can move it.
4. ~~**CAN THE CASTER SET ONE OFF?**~~ **SETTLED: NO** (§3c). It costs 48% of
   the charges and reads as a malfunction, because these balls cannot steer
   around anything.
5. **SETTLED: DEADFALL**, Rick's, from a second spread — the first was four
   ecclesiastical-Latinate names (Interdict, Anathema, Fulmination, Malefice)
   and he rejected the register whole, as he did for Vesper. A deadfall is a
   trap rigged to drop on whatever disturbs it: it springs rather than fires,
   which is the timer-to-mine decision in one word. Gravemourn's is REVENANT,
   and the two being Anglo-Saxon and Latinate keeps the school's two ultimates
   from reading as a matched pair. Tip: `"Stamps sigils that arm, then take
   whatever walks in"` (51/72).

   The copy that ships is `w.ult.name`, `w.ult.tip` and `STATUS.curse.tip`.
   The copy that a viewer actually reads is `w.ult.name`, `w.ult.tip` (<=72)
   and `STATUS.curse.tip` (<=40) — the intro card and the point-of-contact
   panel pull those, `relicStatus()` and `_introFacts`, and nothing else.

   **`blurb` is NOT on that list and this doc was wrong to say it was.** Rick:
   *"where do users ever even see that blurb?"* Nowhere. `grep` finds it in
   the 26 `WEAPONS` entries and in three code comments — no reader in the
   game, in `shorts_build.py`, in `cinema_vo.py` or in `hook_vo.py`. It is
   write-only data, the same class as `blessing` in `STATUS`, which
   `statuses.md` already called out as "defined in STATUS and applied by
   nothing."

   **Chain-wide and worth a decision of its own:** 26 relics carry a sentence
   of authored flavour that has never been shown to anyone, while v46's hook
   work is about giving a first-time watcher a reason to care inside two
   seconds. Either strip it or wire it in; it is the cheapest copy in the
   project and it is already written.

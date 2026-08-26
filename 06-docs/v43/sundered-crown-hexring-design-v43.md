# v43 — §1 IN RICK'S WORDS, AND §1 PRICED BEFORE A BUILDER WAS OPENED

**2026-08-21.** Runic × flail. `runic_flail_probe.py`, **12/12**, runtime-only
on the v42 tip. Nothing has been written to any build.

```
tools/runic_flail_probe.py   NEW   12/12
out/runic_flail_probe_v43.json     the numbers, machine-readable
out/runic_flail_probe_v43.txt      the run
```

---

# 1. §1, VERBATIM

> *"blue flail gains a medium sized hexagonal shaped chain of lightning
> surrounding the flails ball. the flail gains extra hit stun. enemies that
> stay inside the hexagon (that is inside the beams of lightning with the flail
> head) for too long are true stunned. unable to move (ball and weapon) for
> 2ish seconds."*

Four sentences. Each one is a question with a number behind it, and **v41 built
§1 literally and had it refuted inside an hour at the cost of a build**, so
every one of them was measured on the previous tip first.

**The headline: two of the four sentences cannot be built as written, one of
them is a free look knob, and the fourth is the best thing in the design.**

---

# 2. WHAT THE ENGINE ALREADY HAS, AND WHAT §1 ASKS FOR THAT IT DOES NOT

```
ball speed          min 250   cruise 405   max 1300     a ball is never still
moveMul floor       0.45      the only movement knob bottoms out at 45%
hitstun             0.10 + 0.0035/dmg, capped 0.26, DR 0.55 decaying 0.75
hex                 0.20s every 1.15s per stack, cap 5, dur 2.6s
the shipped "root"  Bramblesnare freeze 1.6s r260 · Rootfast freeze 1.3s r230
window ultimates    Daybreak 14/5s · Triplicate 18/6s · Bloodmill 16/5s
                    Aegis 16/9s · Bloodhunt 15/8s
arena               520 x 800
```

`PASS` **`"Roots for 1.6 seconds"` locks a WEAPON and does not touch the ball.**
`fireUlt` writes `foe.stun = Math.max(foe.stun, u.freeze)` and nothing else.
Bramblesnare and Rootfast both say *roots* in a viewer-facing tip and mean
*weapon locked*. **§1's "unable to move (ball and weapon)" is a state this
engine has never had**, and §4 below is what it turns out to be worth.

**And nothing in this game steers.** A ball is ballistic — gravity, wall
bounces, and a speed that relaxes toward a cruise it never falls below. There
is no seeking, no avoidance, and no decision. So *"enemies that stay inside the
hexagon"* is not a thing a foe does; it is a thing that happens to it.

---

# 3. WHERE THE FOE ACTUALLY IS — "MEDIUM SIZED" IS BOUNDED AT BOTH ENDS

48 fights, 1500s, six foes, ultimates suppressed. Centre to centre.

```
mean 259    closest 68    furthest 781    and the head reaches 115 from the shell

   0- 49    0.0%     0.0%
  50- 99    7.8%     7.8%  ################
 100-149   15.4%    23.2%  ###############################
 150-199   15.0%    38.2%  ##############################
 200-249   14.4%    52.6%  #############################
 250-299   13.2%    65.7%  ##########################
 300-349   11.6%    77.4%  #######################
 350-399    8.4%    85.7%  #################
 400-449    5.4%    91.1%  ###########
 450+       9.0%   100.0%
```

**§1's own parenthesis puts a floor under the size.** *"inside the beams of
lightning with the flail head"* — the head reaches **115 units** from the shell,
so a hexagon that contains it has a circumradius of at least 115. `medium` was
bounded below before anybody picked a number.

The ceiling is the hall: 520 wide, so a circumradius of 260 is a zone that
touches both walls.

---

# 4. THE SENTENCE THAT CANNOT BE BUILT AS WRITTEN — "FOR TOO LONG" CANNOT BE TWO SECONDS

Continuous residence. An episode is a run of frames the foe's centre is inside;
it ends the frame it leaves. **Episodes still open when the fight ended are
dropped**, because a censored episode is not evidence about how long a
residence lasts.

```
shape  radius   share  episodes/min   mean    p50    p90    max   >=1.0s  >=2.0s
circ      100    7.8%          31.3   0.15   0.11   0.29   0.68     0.0%    0.0%
circ      160   25.8%          41.6   0.37   0.32   0.67   1.78     2.3%    0.0%
circ      250   52.4%          42.5   0.71   0.53   1.39   4.56    20.8%    4.0%
circ      320   70.7%          34.0   1.15   0.82   2.38   6.92    40.9%   16.0%
hexT      100    5.5%          30.4   0.11   0.07   0.23   0.65     0.0%    0.0%
hexT      130   12.8%          37.8   0.20   0.16   0.41   1.00     0.1%    0.0%
hexT      160   21.5%          42.3   0.30   0.26   0.56   1.73     0.9%    0.0%
hexT      200   32.3%          46.2   0.41   0.34   0.79   1.95     4.5%    0.0%
hexT      250   45.9%          46.7   0.57   0.45   1.16   3.58    14.0%    2.3%
hexT      320   63.2%          42.4   0.85   0.61   1.87   5.71    28.3%    8.7%
```

**At a circumradius of 160 the median residence is 0.26 seconds. The longest of
1058 episodes is 1.73. Not one of them reaches two.** Even at 320 — a hexagon
640 across, in a hall 520 wide — only 8.7% do.

The foe enters and leaves **42 times a minute**. It is not loitering; it is
passing through, because nothing in this game steers and nothing travels slower
than 250 units a second.

So *"for too long"* has to be priced in **tenths**:

```
at circumradius 160, continuous:
  0.4s -> 10.6 /min    0.8s -> 0.9 /min    1.5s -> 0.1 /min
  0.6s ->  3.7 /min    1.0s -> 0.4 /min    2.0s -> 0.0 /min
```

## 4.1 THE FORK THAT MAKES THE SENTENCE TRUE AGAIN

A **charge** that fills while the foe is inside and bleeds while it is out,
instead of a residence that has to survive unbroken. On screen it says the same
thing §1 says — *stay in it and you get caught* — and unlike the continuous
rule, it fires.

Circumradius 160, 2s of pin per trigger, the pin locking out its own accrual:

```
pins/min        bleed 0/s   0.5/s   1.0/s   2.0/s        per 8-SECOND WINDOW
need 0.6s           11.1     5.4     4.6     4.0          1.48  0.73  0.61  0.53
need 0.9s            8.7     2.2     1.2     0.8          1.16  0.30  0.15  0.10
need 1.2s            6.9     1.2     0.4     0.3          0.92  0.16  0.05  0.04
need 1.6s            5.5     0.4     0.1     0.1          0.74  0.05  0.01  0.01
```

**The bleed rate is the counterplay knob, and it is the only one there is** —
a foe cannot choose to leave, so the design's only lever on how forgiving this
is, is how fast the charge drains when it does leave by luck. At 0/s the zone
is a stopwatch that never resets; at 2/s it is a trap that has to be sprung
almost in one go.

`PASS` the cumulative reading fires and the continuous one does not — same
words, same zone, and the difference between an ultimate that does something
and one that never triggers.

---

# 5. THE HEXAGON IS A LOOK KNOB, WHICH IS A LICENCE

```
radius    circle R   hex static   hex turning   circle 0.866R   hex vs circle
   100        7.8%         5.5%          5.5%            4.5%          -29.8%
   160       25.8%        21.5%         21.5%           19.4%          -16.5%
   250       52.4%        46.0%         45.9%           42.9%          -12.3%
   320       70.7%        63.5%         63.2%           59.7%          -10.6%
```

A hexagon covers **83% of its own circumcircle by area, and it collects 81% of
what the circumcircle collects.** Whether it turns with the weapon changes the
share of the fight by at most **0.06%** — six hundredths of one per cent.

**So the shape is a picture and the radius is the mechanic.** Draw it at
whatever size and rotation read in the hall; nothing downstream is balanced on
the corners. This is v42's "larger ballista shots" finding again, and it was a
licence there too.

---

# 6. THE BEST SENTENCE IN §1 — PINNING THE BALL IS WHAT MAKES THIS TYPE CONNECT

Three arms on identical seeds, 179 pins, read over the 3 seconds from the
moment the pin lands. **Arm 1 is exactly what `u.freeze` already does.** Arm 2
is what §1 asks for.

```
arm                my blows  foe blows   dealt   taken   hex fires  wasted   sep at trigger
control               0.532      0.713   29.92   19.37        1.33    0.00              136
weapon only           0.605      0.356   34.97   10.26        1.35    0.83              136
weapon AND ball       0.676      0.318   42.35    8.11        1.41    0.80              136
```

- **A locked weapon is defensive**, and the engine already has it: the foe's
  blows halve and damage taken drops 47%.
- **Pinning the ball as well is offensive, and it is the half this cell needs.**
  +21% damage on top of the lock, **+42% on nothing** — because a 13-unit head
  (flail_survey §2) against a target that has stopped moving is a different
  weapon.

## 6.1 AND THE FIRST CUT OF THIS SECTION SAID THE OPPOSITE

It pinned at a fixed clock time, wherever the foe happened to be, and read
**−12%**. That is a true fact about a pin and a false one about *this* pin: a
foe frozen at the 259 units this game averages is a foe a 115-unit head cannot
reach. **This pin only ever triggers on a foe already inside the hexagon** —
measured separation at the trigger is **136** — and firing it where the mechanic
would fire it flips the sign.

Kept as a check, because it is the same class of error as v42's fork-turn
measurement: an instrument that answers a question next to the one being asked.

## 6.2 THE PIN EATS THIS CELL'S OWN CHANNEL

`f.stun` is a `Math.max`, so two overlapping locks are one lock — v39 §5.2, from
a third direction. **0.80 hex fires land inside every pin**, against 1.33 in the
same three seconds of the control: the pin covers 67% of the window and
swallows **61% of its fires**. At this cell's measured 0.29 fires a second,
that is roughly **2.8 seconds of the school's entire channel output, per pin,
silently.**

It is not a bug and it is not free. It is an argument that the ultimate should
not *also* be about stacking hex.

---

# 7. "THE FLAIL GAINS EXTRA HIT STUN" IS NEARLY INERT ON THIS TYPE

A multiplier on this relic's own hitstun only — applied at `resolveHit`'s call
site, not by moving a CONFIG constant every relic in the game reads.

```
x hitstun  stun/blow  foe locked  my blows/s  foe blows/s   hp/s  taken/s   win
      1.0      0.240       20.6%       0.151        0.261   8.14     6.49   67%
      1.5      0.353       21.9%       0.170        0.238   9.15     5.88   71%
      2.0      0.469       21.8%       0.143        0.253   8.16     6.57   56%
      3.0      0.702       23.1%       0.141        0.244   7.91     6.55   65%
```

`PASS` the multiplier reaches the weapon — mean hitstun per blow goes 0.240s →
0.702s, and `stunMax` caps the raw value *before* diminishing returns, so the
cap does not eat the knob.

**And it buys 2.5 points of lock.** Damage taken does not move. **The reason is
the type**: this weapon lands a blow every six seconds (flail_survey §6), and
tripling the stun on a blow that rare is tripling almost nothing. For contrast,
holding hex at its cap takes the same lock from 29% to 86%.

**As written it is a dead knob** — and `shot.life: 3.4` has been dead config on
five bows since v40 and is still an open decision. A second one should not be
added without a reason.

---

# 8. WHAT IS ACTUALLY BUILDABLE, IN §1'S OWN SHAPE

Nothing here is a proposal about what the relic should be. It is the same four
sentences with the numbers filled in:

```
1. a hexagon of lightning on the caster       circumradius >= 115 so the head
                                              is inside it; 160 puts the foe
                                              in it 21.5% of the time. The
                                              SHAPE is free.
2. the flail gains extra hit stun             worth 2.5 points of lock at 3x.
                                              Inert as written.
3. enemies that stay inside for too long      not as a continuous 2s -- that
                                              happens 0.0 times a minute. As a
                                              charge with a bleed it fires
                                              0.5-1.5 times per 8s window,
                                              and the bleed is the counterplay.
4. true stunned, ball and weapon, ~2s         +42% damage over nothing and
                                              +21% over a weapon-only lock.
                                              New engine state. The best half
                                              of the design.
```

---

# WHAT RICK TOOK, AND WHAT IT COST

Every fork below was put to him with the measurement attached. Recorded here
because this document is where they were priced; the build is `README.md` §4.

```
HOW "TOO LONG" IS COUNTED   a CHARGE that fills inside and bleeds outside,
                            at need 0.6s and a 0.5/s bleed. The continuous
                            reading fires 0.0 times a minute.
WHAT SENTENCE 2 DOES        a landed blow feeds the CHARGE, 0.5s of it. The
                            hitstun multiplier it replaces is worth two and a
                            half points of lock at 3x and moves damage taken
                            by nothing.
HOW BIG "MEDIUM" IS         circumradius 200, from four priced options. The
                            floor was 115 — §1's own parenthesis — and the
                            hall is 520 across.
WHAT A HELD BALL BANKS      NOTHING. He answered this one unprompted after
                            the first build let knockback accumulate and the
                            ball launched on release: "ball should just resume
                            when the stun ends. no banked knockback and no loss
                            of momentum after the stun."
HOW OFTEN IT FIRES          1.54 holds a cast, which is 24.7% of the relic's
                            damage. The blade bisects to 33.75 to pay for it,
                            against the 42.4 the same relic needs with no
                            ultimate at all.
```

---

# Open decisions

1. **CLOSED — the four forks above.**
2. **THE PIN AND THE CHANNEL COLLIDE.** §6.2. 61% of the hex fires inside a pin
   buy nothing, and it was accepted rather than converted: the hold is strictly
   better than the fire it eats, and a mechanic that also converted them would
   be an ultimate about hex on top of an ultimate about position.
3. **THERE IS NO COUNTERPLAY BY MOVEMENT, BECAUSE NOTHING MOVES ON PURPOSE.**
   §2. Every other relic's counterplay is a thing the foe's weapon does — a
   bolt can be clanked, a wall can be gone round. This one's is luck, modulated
   by the bleed rate. Naming it rather than solving it.
4. **THE PIN IS A NEW ENGINE STATE.** `move` not being called for a fighter is
   the cheapest thing that could work and it is not obviously the right thing:
   gravity does not accrue, velocity resumes exactly, and no other system knows
   about it. Whatever ships wants its own probe.

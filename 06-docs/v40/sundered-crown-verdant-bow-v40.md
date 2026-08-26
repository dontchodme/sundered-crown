# v40 — THE VERDANT BOW, LOOKED AT. Everything §1 has to be written against.

**2026-08-20.** Rick's call out of four measured candidates. Verdant is 2/6,
the thinnest school in the game that has a channel at all, and the only one of
the four with two same-school relics instead of three.

```
tools/verdant_bow_probe.py   NEW   7/7
05-reference/v40/verdant-bow-cards.png
05-reference/v40/verdant-bow-arena.png
05-reference/v40/verdant-bow-probe.json
NOTHING WAS BUILT. Donor `axiom` overwritten in place at runtime, page thrown away.
```

**No design is proposed here.** The provisional ultimate is the literal string
PLACEHOLDER and a bare nova, so nothing in the probe or in this document can be
read as one. v38 §1, v39 §1, held to again.

---

# 1. THE ART IS GOOD AND THE MIRROR IS REAL

The verdant branch fires — 32.7% of the inked pixels differ from a nonsense
key, palette held, render deterministic to zero. On the fight card it is the
best-looking bow in the set: a bent living branch, three leaves off each limb,
a tendril off each tip, a vine for a string.

**In the arena, against its own school, it is two green balls.** v28's
same-affinity smudge, and the probe renders it rather than arguing about it.
Palette separation between two verdant relics is zero by construction; the
bow's 179px art against Thornwake's 348px scythe and Heartwood's 268px
greatsword is the only thing carrying the read. Against Widowmaker it is
perfect.

Verdant has **two** mirror pairs where runic, umbral and bloodsworn each have
three — which is why this cell can carry a marquee fight at all (v39 od 3 ruled
runic out of its own). It still should not be shown against Thornwake.

---

# 2. IT FIGHTS

Provisional damage, provisional ultimate, real everything else. Four foes
spanning the parry column, four seeds:

```
foe                  dur   over   dealt    win   hits   shots
thornwake          35.0s   100%     252    50%   10.0      80
heartwood          35.4s   100%     248    50%   11.5      80
widowmaker         36.8s   100%     211     0%    7.5      90
grudgebearer       27.9s   100%     223    50%   10.8      67
```

Widowmaker at 0% is the parry column doing exactly what v40 §2.2 said it would:
the twinblade eats 12.0% of everything thrown at it.

---

# 3. VERDANT'S OWN GRAMMAR IS WORTH +2.6% HERE

Both verdant ultimates are `kind:"freeze"` — Bramblesnare 1.6s, Rootfast 1.3s —
and `freeze` is one line: `foe.stun = Math.max(foe.stun, u.freeze)`. That is the
same field hex writes, and `tickShots` builds the foe's blade list as
`stun > 0 ? [] : segments`. **A rooted foe cannot parry at all.** So the school
already owns the strongest thing a status can do to the ranged path.

Held open permanently — far more than any ultimate could ever buy:

```
the foe is     fired  landed  parried   wall  melee/s  arrow dmg    sep
free            3129    8.2%     9.1%  82.4%    0.123        59%    194
ROOTED          3132   10.8%     0.0%  88.8%    0.137        66%    198
planted*        3940    5.0%     7.1%  87.7%    0.095        56%    194
```

`planted` is not a mechanic. It zeroes the foe's velocity and leaves its weapon
running, and it is in the table as the control that separates *cannot parry*
from *is standing still*.

**A permanent root buys +2.6% landed. Standing the foe still buys -3.2%.**

The wall keeps 89% of the arrows either way. Both halves of a root — the
disarm and the immobilise — are priced now, and one of them is negative.

---

# 4. THE WALL, AND THE ONE NUMBER THAT IS NINE TIMES TOO BIG

```
arena 520x800.  2579 arrows died on a wall.
  N (ceiling) 17.1%    S (floor) 18.1%    E 32.5%    W 32.3%
  travelled 234 on average (median 192), and used 11% OF A 3.4s LIFE
  an arrow that LANDS travelled 187
```

**`shot.life` is 3.4 seconds and no arrow has ever used more than a ninth of
it.** The life cap has never fired once in this game — a shot travels
380 × 3.4 = 1292 units and the longest wall is 800. Every arrow in the game
dies with 89% of its life left, on a wall, an average of 234 units from where
it was loosed.

Two thirds of them die on the SIDE walls, which are 520 apart, not the floor
and ceiling 800 apart.

How close a wasted arrow ever came to the shell, over its whole flight:

```
     0-40    4.2%    #####
    40-80    6.3%    ########
   80-120    8.7%    ###########
  120-160    8.5%    ##########
  160-200    8.5%    ##########
  200-240    9.3%    ###########
  240-280    6.7%    ########
  280-320    5.0%    ######
  320-360    5.3%    #######
  360-400    4.0%    #####
  400-440    2.8%    ###
     440+   30.8%    ######################################
```

**10.5% of wasted arrows passed within 80 units of the shell** — a near-miss
population that is real and countable. **30.8% never came within 440** and were
never going to hit anything.

---

# 5. EVERY ENTANGLE KNOB, PRICED. ONE OF THEM IS NEGATIVE.

Farwarden carries `ward: 2.5` because the constant was authored on a greatsword
and a bow deals a third as much a blow. That is the precedent for a per-relic
value on a channel the type does not suit. One knob at a time, everything else
stock, hp removed in a fixed 20s window against the same weapon with no channel:

```
knob                    per  stk   dur   spin   move   mean   hp@20s    net    ttk
none (control)            0    4   2.8  -0.13  -0.06   0.00       94     +0    39s
stock verdant             2    4   2.8  -0.13  -0.06   1.66      103     +9    41s
per-relic 4               4    4   2.8  -0.13  -0.06   2.08      102     +8    38s
maxStacks 8               2    8   2.8  -0.13  -0.06   2.28       98     +4    41s
dur 2.8 -> 6.0            2    4   6.0  -0.13  -0.06   2.78      108    +14    42s
spin -13% -> -26%         2    4   2.8  -0.26  -0.06   1.79       96     +2    41s
move -6% -> -20%          2    4   2.8  -0.13  -0.20   1.61       83    -11    42s
everything at once        4    8   6.0  -0.26  -0.20   5.57      114    +20    38s
```

**Doubling the per-hit value, the cap, the duration and both slows all at once
buys +20 hp over twenty seconds.** Tripling the move slow on its own costs 11.
`STATUS.entangle` is restored afterwards and that is a check.

The channel will not carry this relic. Whatever is built has to.

---

# Open decisions

1. **§1, IN RICK'S WORDS.** Nothing starts without it. Four things above are
   the constraints it will be built against: the wall keeps 82-89% of arrows
   whatever happens, `shot.life` is nine times bigger than any arrow uses,
   immobilising the foe makes the archer worse, and entangle at any setting is
   worth under +20 hp in twenty seconds.
2. **The marquee fight cannot be against Thornwake or Heartwood.** §1. Two
   green balls. Widowmaker or Grudgebearer are the extremes of the parry column
   and either would read.
3. **`shot.life: 3.4` is dead config on every bow in the game.** §4. It has
   never once fired. Anything that lets an arrow survive a wall inherits nine
   ninths of a life that is already paid for.
4. **The provisional relic's damage is Ironhail's 16.23 and is a placeholder.**
   No tuner pass has been run on this cell.
5. Everything still open from v40's survey doc, in particular that
   `cell_survey`'s umbral row is suspect on all six types.

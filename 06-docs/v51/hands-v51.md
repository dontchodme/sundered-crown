# v51 — THE PURPLE FLAIL'S NEW ULTIMATE, PRICED. The chain is the ultimate and the hand is the payload, which is the opposite of how it reads — and every clause of the §1 survives once the hand carries a memory instead of a fresh curse.

**2026-08-31, Cowork.** Rick's §1, verbatim:

> *when the ult fires for a duration the flails chain gains length and then each
> time it lands a hit an etheral purple hand flys off the hit. the hand soars
> around the arena briefly and then clenches into a fist as it dive bombs into
> the enemy fighter. on contact it applies curse and deals massive knockback.*

`tools/hand_lab.py`. Base curse in every arm is v49's recommendation — K=3,
echo 8%, permanent, displacement kept, priced on the target. Dirge's
`apply:{curse:3}` is stripped everywhere; it is what this replaces. Runtime
injection only, nothing written to any build.

---

# 1. THE CHAIN IS THE ULTIMATE

The worry going in was arithmetic: this is a WINDOW mechanic on the relic with
the fewest blows in the game — 5.6 a fight, one every 7.5 seconds — and v50 §4
priced every window shape on this relic in the dead band at +3%. An 8-second
window contains ONE blow.

**No payload at all, no knockback, 250 fights an arm:**

```
chain  reach   blows   in window   dealt   TAKEN   foe blows   fight len    win
 1.00     96     5.3        1.60     353     303        15.5       39.2s  54.0%
 1.15    110     5.5        1.80     373     284        14.8       38.6s  60.8%
 1.30    125     5.6        1.90     376     281        14.4       37.9s  66.0%
 1.45    139     5.6        1.88     379     273        14.0       37.1s  66.8%
 1.60    154     5.6        1.94     371     278        14.3       37.5s  62.8%
 2.00    192     5.5        1.88     375     289        15.1       38.7s  63.6%
```

**Lengthening the chain is worth +12.8 points before a single hand exists.**
That is two thirds of a median ultimate (+20.4) from the half of the §1 that
reads as staging.

**And the mechanism is not the one either of us assumed.** The chain does not
buy contact: Gravemourn's own blows move 5.3 → 5.6, six percent, nothing.
**It buys DEFENCE.** The foe lands 15.5 → 14.0 blows and deals 303 → 273
damage — ten percent off both. A flail on a longer chain sweeps a wider circle
and holds the quarry outside its own reach. Roughly three quarters of the
+12.8 is damage NOT taken.

*(This refutes the reason I expected it to work. `wh_survey`'s "contact rate is
reach-dominated" is a BETWEEN-TYPE finding — it ranks twinblades against
flails. It does not transfer to a within-relic knob, and this table is what
that looks like when you check.)*

**It has an optimum and it is not "longer is better."** 1.30 and 1.45 are the
same within noise; 1.60 and 2.00 fall BACK, and at 2.00 the foe's blows climb
to 15.1. Past about 1.45 the head orbits so wide that the shell it is
protecting stops being covered. **Reach 192 is worse than reach 125.**

---

# 2. DURATION IS ONE OF THE BIGGEST KNOBS ON IT — AND THE FIRST PASS SAID THE OPPOSITE

**CORRECTION, and Rick caught it.** The first pass swept duration with the
HANDS TURNED OFF and reported the win column flat, so it called duration a
spectacle knob. With no payload a longer window only extends the chain buff,
which saturates — of course it looked flat. With the payload on:

```
window   chain only   + hands   the hands buy   hands   landed   hand dmg
    4s        55.5%     70.5%          +15.0%    2.22     1.58         84
    6s        59.0%     76.5%          +17.5%    2.79     1.93        102
    8s        59.0%     79.5%          +20.5%    3.46     2.40        129
   12s        60.5%     80.0%          +19.5%    4.25     2.70        146
   16s        61.5%     89.5%          +28.0%    4.86     3.09        168
```

**Nineteen points across the range.** Duration is coupled to the blade (§8) and
neither can be chosen without the other.

This is the same failure as §3's: measure a stripped arm, generalise to the
real one. Twice in one session, so it is a pattern and not an accident — **an
arm with the payload removed cannot price a knob that only acts through the
payload.**

---

# 3. WHAT THE HAND CARRIES — AND THE FIRST PASS OF THIS SECTION TESTED A DESIGN RICK DID NOT DESCRIBE

**CORRECTION.** The first pass ran an `apply` arm at **+0.5%** and called the
§1's "applies curse" clause dead. That arm gave the hand **zero damage** and
had it re-park a value the blade had already put in the pool. Rick's
clarification — *"it deals damage and applies curse"* — is a different design,
and a hand that lands a real blow parks a real memory. Measured properly:

```
THE HAND AS A BLOW — chain 1.35, 8s, one hand a blow, knock 400, 200 fights an arm
hand dmg   no curse   + curse   the curse clause adds   hands   dmg a fight
       0      59.0%     59.0%                   +0.0%    1.90             0
      15      62.5%     63.0%                   +0.5%    1.84            23
      30      66.0%     65.5%                   -0.5%    1.79            44
      45      69.5%     70.0%                   +0.5%    1.72            63
      60      73.0%     74.5%                   +1.5%    1.66            78
```

**The hand as a damaging blow works — 60 damage is +23.8 against no ultimate,
right on the field median.** The §1 is a functioning ultimate exactly as
written.

**But the curse clause is worth +0.4pp averaged across the sweep, inside the
noise at every level, and that holds even when the hand hits as hard as the
flail does.** The reason is the same structural fact as v49 §5b, now measured
on a hand that genuinely lands: **the pool already holds the three biggest
blows.** A hand can only add to it by hitting harder than the flail — and a
hand that hits harder than the flail is the relic, with the flail as its
delivery system.

## The reading where all four clauses are true, and it is the best arm

Give the hand a memory to carry and let its damage BE that memory. Then it
flies, it dives, it **deals damage** (what it remembers), it **applies curse**
(because a hand that lands is a hit, and it remembers what it just dealt), and
it shoves.

```
variant                                  win   hands   landed   hand dmg   echo
carries a memory, SPENDS it            77.0%    2.97     2.29        125     19
carries it, deals it, RE-APPLIES it    79.5%    3.46     2.40        129     24
same, x0.7                             80.0%    3.70     2.75        101     24
same, x1.4                             86.0%    3.25     2.08        159     23
```

**Every clause of the §1 survives, and it beats both the spend-and-empty
version and the flat-damage version.** More hands, too — 3.46 against 2.97 —
because the pool is re-parked instead of emptied, so the next blow in the
window still has something to throw.

## THE MULTIPLE MUST NOT EXCEED 1.0

`x1.4` is 86.0% and that is **not a balance point, it is a feedback loop.**
The hand deals `mem x M` and re-parks `mem x M`, so at M > 1 every memory
grows by M each time it is thrown and curse compounds without bound. An
8-second window and 1.7 casts a fight hide it — two or three cycles is not
enough for the exponent to show — and a longer fight, a third cast or a future
duration buff uncovers it.

**M = 1.0 is the design point and it is a conservation law: the hand deals
exactly what it remembers and hands exactly that back.** The memory is passed
along, never grown. This is Slagburst's rule — *consumed then priced* — reached
from the other direction, and it is one line in a build brief that will
otherwise be found by a tuner six sessions from now.

---

# 4. MASSIVE KNOCKBACK COSTS ABOUT SIX POINTS AND DOES NOT EAT ITS OWN WINDOW

The worry was v41's: Grudgebearer's `knockMul 2.3` throws its quarry out of its
own reach and costs 12% of its contacts and 16 points of win rate. A hand that
flings the foe away mid-window should spawn fewer hands.

```
knock   blows in window   hands   hand dmg   blows a fight     win
    0              1.65    4.95         69             5.0   78.0%
  200              1.62    4.88         69             5.0   73.5%
  400              1.60    4.80         68             4.9   70.0%
  700              1.58    4.74         67             5.0   72.5%
 1000              1.64    4.92         69             5.0   71.5%
```

**It does not.** Blows inside the window are flat across a knockback range of
zero to a thousand, and so are blows per fight. The loop the design looked like
it had, it does not have — the hands arrive over 1.2 to 2.3 seconds and the
flail is back on the foe before the next one is due.

**It still costs about six points**, and not through contact. Knockback here is
the same trade the warhammer makes: it is bought with win rate and paid for in
picture. `u.knock` on the roster runs 150 to 460; 400 is already above
Mountainfall.

---

# 5. WHAT THE PICTURE CANNOT HAVE

**About 2 hands a cast, 3.5 a fight, 2.4 of them landing.** The §1 says *each
time it lands a hit* a hand flies off, and the honest count is that Gravemourn
lands 1.3 blows inside an 8-second window. Re-parking the memory (§3) is what
keeps the second blow in a window from throwing nothing; spend-and-empty
costs half a hand a fight.

Three ways out, in order of preference:

1. **Accept it.** Two or three dive-bombs a fight, each carrying a real number,
   is punctuation rather than a swarm — and it is what makes each one land.
2. **The cast throws a hand too**, off the pool as it stands at the moment of
   the cast. Guarantees the set-piece fires even in a window that lands no
   blows, which is 20-40% of casts.
3. **A longer window.** §2 says it is free in balance terms. 16 seconds gives
   3.2 hands a fight and costs nothing but screen time.

---

# 6. THE RECOMMENDATION, WRITTEN OUT

```
kind        new -- "sling" or similar; NOT `pull`, which is the Crucible's verb
charge      16, unchanged
duration    8s   NOT free -- 4s to 16s is 19 points (§2), and it trades
            against the blade. 8s is the point the blade below is priced at
chain       x1.35 on `reach` for the window. 1.30-1.45 is the plateau;
            past 1.6 it gets worse. Nearly free at the tuned blade -- pick it
            for the picture
hands       one per remembered blow, spawned on each blow landed in the window,
            staggered ~0.5s apart, flight ~1.2s. The hand TAKES its memory as
            it peels off, so the pool empties on the blow
payload     the hand deals exactly the memory it carries (M = 1.0), and applies
            curse remembering what it just dealt -- so the memory is passed
            along, not grown. M > 1.0 COMPOUNDS AND MUST NOT SHIP
knock       Rick's call. 400 costs ~6 points and is above Mountainfall.
blade       ~22-23, DOWN FROM 44.1 (§8). Not optional -- 44.1 was paying
            for a dead status and a negative ultimate, and both are fixed
worth       +20.4 against no ultimate -- exactly the field median
name        REVENANT — Rick's, from four
tip         "Pays out the chain; every blow throws its memory back"   (53)
hands seen  3.5 a fight, 2.4 landing -- 2 more than the spend-and-empty read
```

---

# 7. WHAT THIS INSTRUMENT CANNOT TELL YOU

- **The hand always finds the foe.** Flight is modelled as a delay, not a
  trajectory. A real hand can miss, be eaten by an Aegis wall, or be in the air
  when the fight ends — only the last is modelled. A hand that can miss is
  worth less than every number here.
- **The chain buff is a `w.reach` swap**, restored at the window's end. A real
  build wants a per-fighter `reachMul`, because `w` is module-level and shared
  by every match in a page session — Nevermend's `blades` hazard, one field
  along. **A build that swaps `w.reach` and misses a restore path disarms the
  relic for every fight after it, in a match that never cast anything.**
- SE is ~3.2pp at 250 fights and ~3.5pp at 200. `poolhands x1.0` vs `spend x1`
  is about 1 SE apart and is chosen on the picture, not the column.
- Nothing here draws anything. The hand, the clench and the dive need a
  filmstrip before anyone says this reads at phone size.

---

# 8. THE BALANCE POINT, AND WHY 44.1 WAS NEVER AN IDENTITY

Rick: *"this is also looking like its shaping up to be too strong. how can we
get it closer to the 50% winrate?"* Three knobs were tried and two of them do
not work.

```
blade 44.1, no curse at all, no ultimate         46.8%
blade 44.1, echo curse, no ultimate              60.0%
blade 44.1, echo curse, ult as designed          80.4%      ult worth +20.4
```

**The ultimate is correctly sized. +20.4 is exactly the field median.** What is
over is the relic underneath it.

**Charge is not a lever.** At charge 42 the ultimate fires in a quarter of
fights and Gravemourn still wins 61.5%. **The echo rate is not a lever
either** — 8% to 0% moves the full design 80.4% to 79.6%, because this relic
lands 5 blows a fight and its echo is 25 damage. Both of those are levers on
*other* relics; on this one they are rounding.

**The blade is the lever, and it is a correction that was already owed.**

```
blade   chain 1.00   chain 1.20   chain 1.35
   22        41.0%        49.5%        48.5%
   24        52.0%        53.5%        58.5%
   30        62.0%        67.5%        65.5%
```

**Blade ~22-23**, from 44.1. That is a 48% cut to the biggest blade in the
game, and the argument for it is v50 §6 arriving on schedule: **44.1 is not an
identity, it is compensation.** It is the largest number on the roster
*because* curse delivered 3% and Dirge was worth -3.2. Repair both channels and
the number has nothing left to pay for.

## The cut does not cost the set-piece — it pays for it

```
blade    hand damage   hands a fight   blade damage
   20            139            5.68            165
   26            140            5.12            191
   44.1          129            3.46            251
```

**The hand channel is self-stabilising.** Hand damage is flat from blade 20 to
44.1, and the hand COUNT rises as the blade falls — a lighter flail lands more
blows, and every blow in the window throws a hand. Cutting the blade buys
**two more hands a fight**. Gravemourn stops being the biggest number on the
screen and becomes the number that comes back for you, which is closer to what
Curse now is.

Chain is nearly free at that blade — 1.00 to 1.35 is inside the noise at blade
22-24 — so chain length can be chosen for how the arena looks. **The two live
knobs are blade and window.**

## The pull is worth about -3, and it goes for a different reason

Every arm above still fires the old `kind:"pull"` inside the cast. Deleting it
and the cast's own 14 damage, 250 fights a cell:

```
blade    pull kept    pull deleted    delta
   18        36.0%           32.4%    -3.6%
   20        50.4%           39.6%   -10.8%
   22        50.8%           50.8%    +0.0%
   24        58.4%           50.8%    -7.6%
   44.1      80.4%           78.4%    -2.0%
```

Scattered around a small negative, and **the blade lands at 22-24 either way**,
so the recommendation does not move. *(An earlier read of "+9 for deleting the
pull" was taken across two incompatible arms — 150 fights against 250, one with
the window and one without. It was the same error this doc warns about twice
already, and this table is the clean version.)*

The pull goes anyway, and for a reason the win column cannot see: **pulling the
foe in and cashing a status is the Crucible's verb**, and Gravemourn is not
allowed to be a second Crucible.

---

# Open decisions

1. **KNOCKBACK.** ~6 points for the dive-bomb landing like a dive-bomb. The
   warhammer pays the same tax on purpose. 150 / 400 / 700.
2. **THE WINDOW, WHICH IS NOW COUPLED TO THE BLADE.** 8s is what blade 22-23
   is priced against (§2, §8). A 16-second window is worth ~19 points more and
   needs a smaller blade again; a 4-second one buys back blade. This is one
   decision, not two.
3. **THE MULTIPLE.** x1.0 conserves the memory and is the recommendation;
   x0.7 measures the same and winds the pool down over a long fight, which is
   a feel decision rather than a balance one. **Anything above 1.0 compounds
   and is not a candidate** (§3).
4. ~~**THE NAME.**~~ **SETTLED: REVENANT** — Rick's, from a spread of four.
   That which comes back. (The -ing options were withdrawn before he chose:
   Harrowing, Unmaking and The Winnowing already end that way, and a fourth
   would be a collision, not a register.)
5. **DOES THE CHAIN BUFF SHOW ON THE HUD?** It is 75% of the ultimate's value
   and it is currently invisible except as a longer chain. A viewer who reads
   the hands as the whole ultimate has misunderstood which half is winning.

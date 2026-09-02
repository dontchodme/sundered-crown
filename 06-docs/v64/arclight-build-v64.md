# v64 — ARCLIGHT AND STATIC, BUILT. The vigil twinblade, the 34th relic — and the design's overlay was measuring a room that does not close.

**Claude Code, 2026-09-02. Stages 1-3 are built and gated. STAGE 4 IS STOPPED
AND WAITING ON A RULING: there is no blade that balances this relic, measured —
at `dmg 0.5` it still wins 80.6% while the body alone wins 0.0%.** The art and
the sound (stage 5) are first cuts nobody has chosen, and the real price
(stage 6) is stage 4's to follow. Built from `ARCLIGHT-BUILD-BRIEF.md` (Cowork, 2026-09-02), which is the
input and the only input — CLAUDE.md §3 rule 0. Builder: `tools/arclight_build.py`.
Probe: `tools/arclight_probe.py`. Price: `tools/arclight_price.py`. Run outputs
in `06-docs/v64/runs/`.

```
02-chain/sc-arclight.html   stage 1   the relic, ultimate STUBBED (charge 1e9)
02-chain/sc-storm.html      stage 2   the swarm exists. No ward, no damage
02-chain/sc-static.html     stage 3   the ward and the detonation — THE RELIC
```

The base is `02-chain/sc-lastthree.html` — the chain tip, 33 relics, Duskreave
and Scour, and the LAST-3 curse window. **Not the build of record**, which is
still `sc-nova.html` at 32; CLAUDE.md §0.

---

## 0. THE ONE FINDING SO FAR, AND IT IS ABOUT THE ROOM

**`storm_price.py` BOUNCES ITS BOLTS OFF THE ARENA. THE BUILD BOUNCES THEM OFF
`m.inset`, AND THE SEALS WALK THAT 0 → 140.** The model's walls are
`x < P.rb`/`x > W - P.rb`; the engine's own projectiles use `n = this.inset`,
and a bolt that ignored it would fly into the stone the balls cannot reach. The
build is right. The consequence is that after the Second and Third Seals the
swarm is running in a much smaller room, comes back to the quarry far more
often, and grows.

Measured over 241 casts (33 foes × 3 seeds), bucketed by how closed the hall was
at the cast:

```
   inset   casts   spawn    fork   eaten   alive    peak  refused
   1-40       99    15.2    33.4    21.1    26.6    28.4      1.6
  40-90       94    20.1    69.9    48.4    38.9    41.3     11.1
  90+         48    31.9   186.3   160.8    52.0    55.5     55.5

  the design's live model:  spawn 17-20  fork ~30  eaten ~21  alive ~24  peak ~30
```

**In the open hall the build reproduces the priced swarm to within noise.** In
the closed hall it is five times the swarm — and the 60-bolt cap, which brief §0
calls *"a safety, not a knob"*, refuses **3,867 spawns across 98 of 241 casts**
(11 of 99 while the hall was open). So on the shipped numbers the cap IS a knob,
and it is doing its shaping in exactly the part of the fight the design never
modelled.

**That is Rick's and Cowork's to rule on, not this session's** (rule 0). The
probe's cap check is left FAILING rather than widened, because it is the only
measurement that says so. Three obvious answers, none of them taken here: leave
it (the cap becomes the late-fight shape), raise it, or scale the swarm to the
hall.

> **AND A SECOND, SMALLER DIFFERENCE FROM THE MODEL IS DECLARED HERE RATHER
> THAN FOUND LATER.** `storm_price` resolves the EAT first and the fork second,
> so a bolt inside both shells is consumed. `tickStatic` tests the FOE first, so
> the same bolt forks and lives. In melee the two shells are often inside one
> bolt's 50 units, so this is not a rare case — and both readings are
> defensible: a contact is one thing, and which thing it is was not written down
> anywhere. The build's choice is stated in its own comment. It is small where
> the hall is open (the open-hall census matches the model on all five counts)
> and it compounds with §0 where the hall is closed.

---

## 1. STAGE 1 — THE RELIC, ULTIMATE STUBBED

`dmg` 8.3 (Twinshade's, a bisection START — brief stage 4 says go DOWN from it),
`onSelf { ward: 1 }`, `ult { name:"Static", charge:1e9, kind:"static" }`.

Three things the builder asserts against the shipped file rather than trusting
its own comment:

- **The twinblade's body is one set across all four shipped twinblades** —
  `blades:[0,0.5], reach:62, width:8, artW:30, spin:5.7, mass:1.1, mode:"spin"`.
  Every number in the design was measured on one twinblade body; they are only
  transferable to a fifth if the four agree, and they do.
- **`SHAPES.twinblade` routes `vigil` to `_tbPlated`**, which exists and has
  never been drawn — this relic is the first vigil twinblade in the game.
- **The school's channel** — and here the brief is not quite right.

> **BRIEF §0 SAYS `onSelf { ward: 1 }` IS CARRIED "EXACTLY AS THE OTHER FOUR
> VIGIL CARRY IT". THREE OF THEM DO.** Farwarden carries **2.5**, and its own
> comment says why: `onSelf`'s value is a per-relic bank multiplier
> (`resolveHit` banks `dmg * W.bank * n`), ward was designed on a greatsword
> landing 30-point blows, and a bow deals ~11 a hit three times inside a
> 5-second window — so at n=1 its pool topped out near 20 of a 90 cap. The
> NUMBER the brief gives is still right for this relic (the twinblade is the
> fastest weapon in the game and every price in `06-docs/v64/` is on `ward:1`),
> so what changed is the check: the builder asserts the three MELEE vigil relics
> and names the bow as the deliberate exception.

**GATE 1: `engine_ab` 5280/5280 identical** over the 33-relic roster at 10 seeds
a pairing — adding the relic moves no fight that does not contain it.

**AND `verify --n 40` READS THE STUBBED RELIC AT 18.0%, WHICH IS NOT THE ALARM
THE BRIEF NAMES.** Gate 1 says *"if it lands near 10% the ward channel is not
wired"*, and 18 is much nearer 10 than the 57-60 it predicts. The channel is
wired, and two independent measurements say so:

- **At the body the prediction was written for — dmg 11.95 — the floor is
  54.2%** (`arclight_price.py` arm A, 264 fights), against the design's 56.9%.
  The brief's own note says the body with NO channel is `cell_ults_on`'s 10.7%.
- The stage-3 probe watches the pool rise on the caster: **42.7 ward banked a
  cast** in the open hall.

What the 18.0% is, is the BLADE. The brief expected "a few points under" 57 at
8.3; it is thirty points under, because a twinblade lands ~26 blows a fight and
3.65 points of blade is ~95 damage a fight against a 400hp fighter. That number
is the first sign of what §4 then measured properly.

`verify` is **11/13** on this link: Arclight 18.0% (outside the 30-70% band) and
Farwarden/Arclight at 83.0s (outside the 18-70s pairing band). **Neither is a
finding.** Both are what a stage-1 link with a stubbed ultimate and an
un-bisected blade always looks like, and both are stage 4's to clear.

## 2. STAGE 2 — THE STORM EXISTS

`Match.storm`, a sim object drawn off itself for v54 §2a's reason (`ultFx` is one
slot and an opponent's cast erases it). Eight bolts a blade hit, born at the
foe; r 16, 600 px/s, 6 ricochets and the 7th wall kills; a bolt that touches the
foe forks into two MORE and refreshes its ricochets; a bolt that touches the
caster is consumed. Directions from the match's own seeded stream. Cap 60,
declining rather than shifting.

**GATE 2 — `arclight_probe.py`, 99 fights, 241 casts: 12 of 13 checks pass.**

```
  the books balance -- spawned + forked = eaten + died + alive     241/241
  eight bolts a blade hit, and none from anywhere else             689 blows -> 4927
  IN THE OPEN HALL the swarm is the one the design priced          within 25% on all five
  a storm needs a spark                                            20 of 241 casts grew nothing (8%)
  both sinks are real                                              14361 eaten, 605 on a 7th wall
  no bolt is ever outside the hall                                 0
  the bolts freeze with everything else                            0 of 35476 frozen steps moved one
  no damage, no ward, no beat, no hit stop, no stun, no knock       0 of everything
  no storm outlives its match                                      0
  nothing calls `Math.random`                                      0 over 262,724 ticker frames
  THE CAP IS A SAFETY AND NEVER BINDS                              FAIL -- §0 above
```

**And `engine_ab` 4224/4224 identical** over the 33-relic roster at 8 seeds a
pairing: the storm does not touch a fight it is not in.

> **THE FROZEN CHECK WAS WRONG FIRST, IN THE FAMILIAR WAY.** Its first cut read
> `hitStop > 0` *inside* the ticker and reported 148 defects. Inside the ticker
> that flag means "something earlier in this step raised a hit stop" —
> `tickShots` and six window tickers run before this one — and that step is
> still a LIVE step whose bolts are supposed to move. Sampled at the TOP of the
> step it means what it says, and the count is 0 of 35,476. CLAUDE.md's most
> repeated probe fault, in a new costume.

## 3. STAGE 3 — THE WARD AND THE DETONATION

The eat banks 2 under the 90 cap through the school's own fields in the school's
own order (`resolveHit`'s vigil branch is the reference), re-applies the status
so the 5s clock restarts, and prints the same float the blade's bank prints. At
`t >= 8` every bolt pops, the ones within `ballR + 80` of the quarry are one hit
of 15 each **through `resolveHit`** — crit, jitter, Sunder, the quarry's own
ward, and the vigil bank of 0.55 all read — with `stop:0, stun:false,
beat:false`, and then ONE hit stop, ONE ring and ONE beat for the whole
detonation.

**GATE 3, part one — `arclight_probe.py` against `sc-static.html`, 33 casts on
five foes: 19 of 20** (the cap again).

```
  the eaten bolts feed the ward           42.7 banked a cast in the open hall (design ~35)
  the 90 cap is never exceeded            0 frames over
  the finale is a lottery                 18% of live casts caught NOTHING (design 18%)
                                          5.00 bolts in the blast, open hall (design ~4)
  it pays through the ordinary path       110.4 damage a cast, open hall (design ~60)
  ONE beat, and one more only on a kill   37 beats over 33 casts, 10 fatal
  no hitstun and no knockback             0, 0
  nothing fires over a corpse             0
```

**The damage a cast is ~1.8× the design's**, which is the declared gap of design
open decision 3 arriving: the model dealt through `m.hurt` and skipped crit and
jitter, and the built one also catches more bolts in the blast late in a fight
for §0's reason.

**And `engine_ab` 4224/4224 identical** on the 33 other relics: the ward and the
detonation reach nothing outside their own fights.

### 3a. THE FOUR-ARM PRICE — THE BODY REPRODUCES AND THE ULTIMATE IS BIGGER

`arclight_price.py`, the built relic with the brief's own toggles (`ward` → 0
and `dmg` → 0), paired on (foe, seed), 33 foes × 8 seeds = **264 fights an arm**,
**at the design's own body (dmg 11.95)** so it is like-for-like:

```
  arm                          win     vs A      the design's model
  A  the body, no ultimate   54.2%       --      56.9%
  B  ward only               83.3%    +29.2      +16.1
  C  detonation only         90.9%    +36.7      +25.0
  D  the whole of STATIC     95.1%    +40.9      +33.1
```

**Arm A reproduces the design's floor** — 54.2% against 56.9%, inside the noise
of a roster win rate — so the BODY is the body the design priced. Every other
arm is bigger, and the whole is **+7.8pp over the +33 tier** but under the +45
that brief gate 3 calls "a different relic".

### 3aa. AND THEN THE MODEL WAS RE-RUN ON THIS MACHINE, AND MOST OF THE GAP WAS THE RUNTIME

**`storm_price.py`, unmodified, on `sc-bloodletting.html` — the design's own
tool on the design's own build, on the repo's pinned Chromium 151 rather than
the Cowork container's 141:**

```
  arm                    here    as published    delta
  A  no ultimate        53.2%           56.9%     -3.7
  B - A                 +21.8           +16.1     +5.7
  C - A                 +23.8           +25.0     -1.2
  D - A                 +37.5           +33.1     +4.4
```

**The published +33.1 reads +37.5 here.** So the built relic's +40.9 is
**+3.4pp above the model as this machine measures it — inside gate 3's ±6
tier.** Read against the published number the build looks 7.8pp hot; read
against a reproduction control it is in band, and the difference between those
two readings is entirely the instrument.

This is the skill's own standing instruction working: *the runtime is an input;
run a reproduction control against a published number before quoting anything
new.* Everything in `06-docs/v64/` that is a decimal is on the other runtime.
**Gate 3 passes.** What remains of the gap has two measured causes, and they are
worth keeping because they are real even if they are small:

1. **The detonation goes through `resolveHit`, not `m.hurt`.** Crit, jitter and
   the Sunder multiplier all read, which the design declared it was skipping
   (design open decision 3). 110 damage a cast against ~60.
2. **§0's closing hall** — more bolts alive, so more eats (the feed) and more
   bolts inside the blast (the finale).

> **AND THE PUBLISHED PRICE WAS TAKEN AT `ric: 99`, NOT AT THE 6 THE BRIEF
> SHIPS.** `runs/storm_price_loud8.json` carries its own parameters and its
> `P.ric` is 99 — bolts that never die on a wall. Design §3 measured 6 as
> *"within a bolt of unlimited"* and Rick ruled 6, so the gap is small and it
> points the other way (6 is the weaker arm), which is why it is a note and not
> a finding. It is written down because the +33.1 tier every gate is read
> against is the ric-99 number.

At the SHIPPED blade of 8.3 the same four arms read A 27.3% → D 95.5%, D − A
**+68.2** (n=66, tiers not decimals). That is not a second finding: the arm
gaps are not blade-invariant, and a lower floor leaves more room above it.

### 3b. AND THE BLADE MOVES THE FINISHED RELIC BY 0.4 POINTS

The one number that matters for stage 4 is in the two runs above. Cutting the
blade from 11.95 to 8.3 is worth **27 points of win rate to the body with no
ultimate** (54.2% → 27.3%) and **0.4 points to the finished relic** (95.1% →
95.5%). The ultimate is so far above the ceiling that the blade is very nearly
decorative up there — which is Rick's *"the storm is the fighter"* arriving as
arithmetic, and it is the reason stage 4 sweeps a CURVE before it bisects
anything.

## 4. STAGE 4 — THE BLADE, AND THERE IS NOT ONE

**STOPPED AT THIS GATE, AND THE MEASUREMENT IS WHY.** Brief stage 4 says to
bisect DOWN from 8.3, not to stop at the row's floor, and to expect the lightest
blade in the game. Swept as a curve first — `arclight_sweep.py`, 33 foes × 10
seeds = **330 fights a point**, side A, the whole of STATIC live:

```
    dmg      win    +/- SE   ults/fight
   8.30    93.9%       1.3         2.25
   6.00    91.5%       1.5         2.35
   4.00    88.2%       1.8         2.45
   2.00    83.3%       2.1         2.43
   1.00    81.8%       2.1         2.48
   0.50    80.6%       2.2         2.56
```

**There is no crossing.** At `dmg 0.5` — a blade that deals 13 damage across a
whole fight against a 400hp fighter, an order of magnitude below anything in
the roster — the relic still wins **80.6%**. Taking the blade from 8.3 to 0.5
costs it 13 points and it needs to give back 31.

**AND THE CONTROL COULD HAVE COME BACK WRONG.** The same curve with the
ultimate stubbed — the body, the ward channel and the blade, and nothing else:

```
    dmg      win     with the storm      the storm is worth
   8.30    21.8%              93.9%                  +72.1
   4.00     0.0%              88.2%                  +88.2
   1.00     0.0%              81.8%                  +81.8
   0.50     0.0%              80.6%                  +80.6
```

**Below `dmg 4` the body cannot win a single fight in 330** — and it still wins
four in five with the storm on. If the blade had been carrying any of this, this
table is where it would have shown; it carries none of it.

**So the blade cannot balance this relic, and what comes down next is a number
inside the ultimate. That is a design decision and this session does not make
it** (CLAUDE.md §3 rule 0). The design named its own knob before the build
existed — open decision 3, *"the 15-a-bolt is the knob, not the radius (Rick
ruled the radius)"* — and §3a says the ward feed is worth **+29.2pp on its own**
with the detonation switched off, so the bolt damage alone may not be enough to
reach the band either. Both knobs are priced in §4a so the ruling can be made
off numbers rather than off a guess.

Rick's ruling *"the storm is the fighter"* — that he accepts the lightest blade
in the game rather than toning the storm down — was made against a design that
predicted the blade WOULD land it. It does not, and that is what he should be
shown.

**AND THIS IS NOT A PROPERTY OF THE BUILD. IT IS A PROPERTY OF THE DESIGN AS
PRICED.** §3aa's reproduction puts the design's own model at D = 90.7% on this
machine; the built relic is at 95.1% on the same body. A relic winning nine
fights in ten off its ultimate cannot be brought to the band by a weapon that
lands 26 scratches — whichever of the two you measure. Design §6's *"has to give
back ~40 points at the blade"* is the assumption that fails, and it fails for
the model too.

### 4a. THE TWO KNOBS, PRICED — AND THEY ARE SUBSTITUTES, NOT ADDENDS

`arclight_sweep.py --knob`, 330 fights a point, blade held at 8.3:

```
   ult.dmg (15 a bolt)              ult.ward (2 a bolt)
     15   93.9%                       2.0   93.9%
     10   91.5%                       1.0   91.8%
      6   88.2%                       0.5   90.9%
      3   80.0%                       0.0   90.3%
      0   64.8%
```

**Deleting the ward feed entirely costs 3.6 points. Deleting the detonation
entirely costs 29.1.** And yet §3a measured the ward feed ALONE, with the
detonation switched off, at **+29.2pp over the floor**. Both readings are
correct and together they are the whole problem:

> **THE TWO HALVES OF THIS ULTIMATE ARE SUBSTITUTES.** Either one on its own
> wins the fight, so the marginal value of the second one is small — which means
> **every one-knob curve understates what that knob is worth**, and a tune that
> takes one of them down will look almost free and change almost nothing. They
> have to come down TOGETHER. That is why what follows is whole candidate
> settings and not a knob table.

### 4b. SIX WHOLE SETTINGS, PRICED SIDE BY SIDE — AND NONE OF THEM CHOSEN

Each row is a thing somebody could ship. 330 fights a point, side A.
**`blade / ward-a-bolt / damage-a-bolt`**, against the shipped `8.3 / 2 / 15`
at 93.9%:

```
    8.3 / 1   / 6      82.1%
    8.3 / 1   / 3      74.5%
    8.3 / 0.5 / 3      70.6%
    4   / 1   / 6      72.7%
    4   / 1   / 3      57.6%    IN BAND
    4   / 0.5 / 3      46.4%    IN BAND
```

**Which one ships is Rick's and Cowork's** (rule 0, and rule 2 — this is the
spread, priced, with the trade named). What each row costs the relic, in
plain terms:

- **the blade at 4** is half the twinblade row's floor and a third of
  Twinshade's. The blows read as scratches, which is what Rick already accepted.
- **the ward at 1 a bolt** halves the harvest — ~21 a cast rather than ~43 —
  and the harvest is the half of this fighter that is otherwise invisible.
- **the bolt at 3** takes the finale from ~60 a cast to ~12. 18% of casts
  already pay nothing; at 3 a bolt the ones that DO pay pay a quarter as much,
  which is the number most likely to make the detonation stop reading as the
  payoff of an eight-second window.

**Two caveats on these numbers.** They are side A at n=330; `verify` runs an
appended relic as side B in all of its pairings, and on this relic that read
**nine points lower** at stage 1 (27.3% side A against 18.0% on `verify`), so a
row at 57.6% here is not safely in band. And a roster win rate is 33 pairings of
correlated fights, not 330 flips. **Whatever is chosen wants the wide direct
measurement — n ≥ 1000 a point, both sides, a second seed block — before it
ships.**

---

## Open decisions

0. **WHICH SETTING SHIPS.** §4b. The blade alone cannot land this relic and the
   two halves of the ultimate are substitutes, so the tune is a whole setting
   and not a knob. Two of the six priced rows are in band. **Rick's and
   Cowork's** — and the design's own open decision 3 already ruled that the
   bolt damage is the knob to reach for before the radius, which both in-band
   rows honour.
1. **THE CAP.** §0. It binds in 98 of 241 casts, and brief §0 says it should
   never bind. Leave it, raise it, or scale the swarm to the hall — all three
   are design changes and none is this session's.
2. **THE BOLT ART AND THE SOUND.** Rick's, from rendered spreads at stage 5
   (brief §4). What is in `sc-storm.html` today is a first cut of the bolt — a
   jagged three-segment streak at the hit radius, drawn deterministically — and
   it exists so stage 2 could be FILMED, not because anyone chose it.
3. **NO PARTICLE FIELD.** `SPECS` in `src/render/fx.js` and the build's inlined
   copy have no `arclight` entry, so this ultimate emits no field and
   `ULTFX.sync` returns silently rather than erroring. That is CLAUDE.md open
   item 46 for the third and fourth relic running (Ravelbone and Gloamwire have
   the same hole). A field is art and therefore Rick's.
4. **THE BLADE.** Not bisected. `TUNED_AL` is `None` and stage 4 has not run.

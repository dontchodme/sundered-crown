# Vigil × twinblade — the replacement for Arclight — v66

**DESIGNED — Cowork, 2026-09-03. Claimed 06:25 UTC, designed by ~08:10 UTC. Build from `STARWARDEN-BUILD-BRIEF.md`; do not design this cell in another session.** Rick: "lets redesign vigil twinblades."

Arclight / Static (`06-docs/v64/`) was built, gated and scrapped by Rick on 2026-09-02. This is the new design for the same cell, written against `06-docs/v64/vigil-twinblade-CONSTRAINTS.md`, and written as it goes — if it ends here, the design is not finished.

## 0. Status

| Rick's seven | state |
|---|---|
| the cell | vigil × twinblade — settled (his, 2026-09-02; reconfirmed 2026-09-03) |
| the ult mechanics | **SETTLED** — §3 verbatim, priced §4-10, eight rulings §8 and §10 |
| the ult name | **CORONA** — his, from four (§11) |
| the fighter name | **STARWARDEN** — his, from four (§11). Arclight is retired with the old design |
| the card | **his own line**, 67 chars (§11) |
| the animations | open — rendered spread at build stage 6 |
| the sound | open — rendered spread at build stage 6 |

## 1. Rulings so far (2026-09-03)

- **Nothing from Arclight survives** — not the name, not the storm/ward/detonation idea. New fighter, new ultimate. (Rick, from three offered: names only / the idea too / nothing.)
- He will write the ultimate in his own words; Cowork prices each sentence before asking anything else.

## 2. What the cell already knows (from v64, not re-measured)

- The body with the ward and no ultimate wins ~54% at Widowmaker's blade (11.95) and ~22% at the row floor (8.3). The ultimate is fitted into what is left under 50%.
- The blade is worth ~13 points across its whole usable range once an ultimate carries the relic — it is not a balance lever here.
- Two payoffs on one ultimate can be substitutes; price them jointly.
- Anything that flies or is placed in the room has to close with the hall (inset 0 → 140).
- Every v64 decimal is on Chromium 141; the pinned runtime is 151. Run the reproduction control first.

## 3. Rick's §1, verbatim (2026-09-03)

> for a duration the fighter gets an elliptical ring of neon light with a small
> gap left for a large star in the middle. enemy fighters who enter the ring are
> burned for rapid tics of damage over time and left with a burn that deals more
> damage over time for a few seconds. If the enemy is hit by the star it explodes
> sending a shower of smaller stars bouncing around the arena. if an enemy hits
> one of the stars it detonates, dealing damage over time and knocking them back.
> after a duration the leftover stars detonate anyways, not all at once, in a
> chain reaction like effect from one end of the arena to the other

Amended within the half hour, unprompted:

> *"id also like the ring to read like a bandolier on the fighter. so not
> around it and the weapon. sort of an over the shoulder type effect"*
> *"tell me if that doesnt make sense. this is a little hard to describe"*

Cowork's reading, put back to him: a tilted sash across the ball, over one shoulder and past the opposite hip, hugging the body with the two ends poking a little past the rim; the star on the chest where the sash would cross; turns with the fighter, not the weapon; well inside the twinblade's reach. **Consequence named to him: worn on the body, "enters the ring" means "touches you" — the ring becomes a contact hazard rather than an aura, and "hit by the star" a body-to-body collision.** Awaiting his yes/no; pricing proceeds on the contact-hazard reading.

Read as written, six clauses:

1. **A window.** The caster wears an elliptical ring of light; a large star sits in the middle. ("a small gap" — between ring and star, or an opening in the ring; to be asked, it is a picture question unless the gap is a door.)
2. **The ring burns.** A foe inside it takes rapid ticks; leaving it, they keep a burn for a few seconds that ticks harder.
3. **The star bursts on contact.** A foe touching the big star pops it into a shower of small stars that bounce the hall.
4. **Small stars are mines.** A foe touching one detonates it: damage over time and knockback.
5. **The leftovers go off on a clock**, not together — a chain from one end of the arena to the other.
6. **Nothing in §1 touches the ward.** Vigil is in the cell by the blade alone, as Shroudmaul is umbral by its blade alone. To be confirmed with Rick, not assumed.

Amended again, ~06:55 UTC, on Cowork's contact-hazard reading:

> *"youre close. its like the rings of saturn. a sash that floats off the body
> and extends beyond"*

**Settled reading: Saturn's rings.** A flat tilted band around the ball, floating clear of it and reaching well past it on both sides; the star on the body at the centre. An enemy enters the ring by passing through the band. Priced below at three reaches.

Open readings to price both ways before he is asked: whether the ring moves with the caster (it is "the fighter's" ring, so yes unless he says otherwise); whether the big star is centred on the caster (then touching it means touching the caster's ball — a melee foe does that constantly) or set beside them in the gap; whether the ring's burn and the lingering burn stack with bleed-style rules or are a new status; whether a small star's detonation is instant damage plus a burn, or burn only.

## 4. The harness, and the control

Chromium **141.0.7390.37** in the Cowork container — the runtime v59, v60, v62 and v64 priced on, not the repo's pinned 151. **Reproduction control, run first:** `cell_ults_on.py --cells vigil:twinblade` against `sc-ravelbone.html` returns **33.1% / +47.9pp / 10.7% / +45.5pp** — v62's table to the decimal.

Everything below is measured on **`02-chain/sc-minute.html`, 33 relics, the minute pace** (baseHP 520, seals 27/64, timeout 156) — the newest link and the pace Rick ruled for. The caster is the cell as `cell_ults_on` builds it: Widowmaker's twinblade profile, aff vigil, `onSelf {ward:1}`, its own ultimate suppressed, everyone else's live.

```
the body, ward on, no ultimate, at the minute pace          (cell_ults_on, 10 seeds, 320 fights an arm)
  field ults off   floor 35.9%   ward +50.6pp
  field ults on    floor  9.7%   ward +47.8pp   -> 57.5% at the donor blade 11.95

  blade 11.95   69.8%  (seed block 4401+17i, 3 seeds — this block runs hot; v64 saw the same, 60.2 vs 56.9)
  blade  9.5    34.9%  (6 seeds, 192 fights)
  blade  8.3    17.2%  (6 seeds) — Twinshade's blade, the row floor
```

The cell has moved by nothing that matters since v64: the body is ~57% at the donor blade and ~17-22% at the row floor. **The ultimate is being fitted under 50% starting from 17%, on the lightest blade in the row.**

## 5. The ring's event rate — measured before anything was designed on it

`tools/sash_tracks.py`, observing only, 96 fights, 403 six-second windows every 15s:

```
ring outer axes (reach x edge-on)   band    seconds in the ring per window   entries   windows with none
  100 x 35                           20            0.47                        4.3           3%
  120 x 42                           24            0.69                        4.5           1%
  150 x 52                           30            1.00                        4.7           0%

body-to-body contacts per window 2.45 (median 2, none in 10%) · seconds touching 0.06
first body contact at median 1.32s after the cast, in 90% of windows   <- the star pops in 9 casts of 10
blade hits per window 2.0 · mean separation 248 · caster stunned 1.66s of every 6
```

**An enemy spends about two thirds of a second per cast inside the band, in four or five crossings.** "Rapid ticks while inside" is therefore a brush, not a roast: at 10 ticks a second that is six or seven ticks a cast. The lingering burn — applied on each crossing — is where the ring's damage has to live, and the star pops early in nearly every cast.

## 6. §1 priced live — `tools/ring_price.py`

The whole §1 run inside `m.step`: ring ticks and mine damage through `m.hurt`; the burn ticking `hp` directly like every `dps` status in the game; small stars bouncing off the CURRENT inset (the hall closes); the chain top-to-bottom at 70ms a star when the window shuts. Control: arm A reproduces sash_tracks' 69.8% on the same seeds. Bookkeeping asserted per fight: spawned = touched + chained + alive.

As written (blade 8.3, 6 seeds = 192 fights an arm, SE ~3.5pp; burn +1 a crossing, +2 a star, **cap 4**, 3.0/s a stack for 3s; 10 stars; mine knock 300; chain blast 80):

```
arm                  win     per cast: ring s  crossings  burn stacks applied  stars touched  chained  chain hits   dmg ring  burn  total
A  no ultimate      17.2%
B  ring only        55.7%              0.61       4.1            4.1                 —          —         —            4.3   44.1   48.4
C  shower only      65.1%              0.62       4.0           11.0                5.2        3.2       0.33           —    53.7   53.7
D  the whole §1     71.4%              0.59       3.8           14.4                4.9        3.2       0.33          4.2   63.6   67.8

B - A  +38.5    C - A  +47.9    D - A  +54.2      (B-A) + (C-A) = 86 > 54: THE HALVES ARE SUBSTITUTES UNDER A CAP OF 4
```

Six things, in order of weight:

1. **The burn IS the ultimate.** 94% of its damage. The ring's own ticks are 4 damage a cast at 1/tick; at 3/tick they are 12 and the win rate does not move (+54.7).
2. **The burn's ceiling is the whole price.** cap 1 → +17.7 · cap 4 → +54.2 · cap 8 → +72.9, at 3.0/s a stack. Fourteen stacks a cast are applied and ten are thrown away at cap 4 — which is also why the halves substitute: ring crossings and touched stars fight over the same four slots.
3. **The enemy walks into HALF the shower.** 5 of 10 stars are touched, 3 are left for the chain, and 10% of chained stars go off within 80 of the enemy (20% at 130 — win rate unchanged, +52.6). **The chain is a picture; it costs nothing and pays nothing.**
4. **Star count is a look knob under a cap** — 16 stars: +53.6 against 10 stars' +54.2 (8 touched instead of 5, all wasted on the ceiling).
5. **Ring reach is nearly a look knob** — 150 x 52: +58.9, mostly from the ticks (6.7 vs 4.2).
6. **Mine knockback: 0 → +49.0 · 300 → +54.2 · 600 → +54.7.** Within a paired-difference SE of each other; a look choice.

### 6.1 Uncapped: every stack counts, and the halves stop substituting

```
burn UNCAPPED, 1.0/s a stack, 3s        win     peak stacks   burn dmg/cast
  B ring only                          32.3%        7.1            19.3        +15.1
  C shower only                        56.8%       17.4            49.0        +39.6
  D the whole                          71.4%       22.3            66.6        +54.2      (B-A)+(C-A) = 54.7 ≈ D-A: ADDITIVE

the ladder, uncapped, whole §1, blade 8.3:
  0.3/s a stack                        (with the ward feed, below)             +35.4
  0.5/s                                53.1%       23.8            37.1        +35.9   <- near the band on its own
  0.7/s                                64.6%       23.3            50.3        +47.4
  0.7/s, burn lasts 2s not 3           53.1%                       40.1        +35.9
  1.0/s                                71.4%       22.3            66.6        +54.2
  0.5/s + every ring TICK adds a stack 60.9%       30.5            46.9        +43.8   (dwell feeds the burn: +8pp)
```

**Uncapped, an enemy that blunders through the shower burns three times as hard as one that only crosses the ring (17 stacks against 7), the two halves add instead of competing, and star count and ring reach become real levers rather than pictures.** Per-stack damage falls to ~0.5/s to pay for it, which lands the whole §1 at +36pp on the row's lightest blade — inside the band with no blade to spend.

### 6.2 The ward

§1 does not mention the shield. Priced anyway, because every other vigil ultimate touches it:

```
                                             ward banked/cast     win (blade 8.3)
  cap 4, 3.0/s, burn feeds ward at 0.55            34.3              91.1%   +74.0
  uncapped 1.0/s, feed 0.55                        35.6              93.2%   +76.0
  uncapped 0.5/s, feed 0.55                        20.4              73.4%   +56.2   (+20pp for the feed alone)
  uncapped 0.3/s, feed 0.55                        13.1              52.6%   +35.4   (the feed priced in: 40% less burn)
  ring TICKS feed ward at 0.55 (cap 4, tick 1)      2.3              71.9%   +54.7   inert — the ticks are too small to bank anything
```

A burn that banks shield at the blade's rate is worth about +20pp on its own and is a second payoff in a different currency; it is NOT a substitute for the burn (both are needed to reach the tier). It is also a fifth clause on a card that already has to say ring, burn, stars and chain in 72 characters.

## 7. What is put to Rick (2026-09-03 ~07:30 UTC), and why

Four questions, each priced above. Recommendation and reasoning on record before he answers:

1. **The burn's ceiling — uncapped, recommended.** Under a cap the halves substitute and star count, ring reach and the shower's aim are all pictures; uncapped they add and become levers, and 0.5/s a stack lands +36 at the row floor.
2. **What the ring's own ticks are** — the picture (a sizzle), a stack per tick (dwell feeds the burn, +8pp), or a real bite (still ~20 dmg a cast; there is 0.6s of dwell to bite).
3. **The ward** — blade only (recommended: the card cannot hold a fifth clause, and Shroudmaul set the precedent for a school relic whose ultimate is pool-independent), or the burn banks shield at the blade's rate (+20pp, paid for by 40% less burn).
4. **Mine knockback** — a look choice; 0 / 300 / 600 measured within noise.

Told to him as inert, not asked: chain blast radius (a picture), star count under a cap, ring reach.

## 8. Rick's four rulings (2026-09-03 ~07:40 UTC)

1. **Burn stacks UNCAPPED** — the recommendation.
2. **Every ring tick adds a burn stack** — the recommendation. Dwell feeds the burn.
3. **The burn FEEDS THE SHIELD at the blade's rate (55% of burn damage banked)** — over blade-only, which was the recommendation. His call; the card will have to carry it.
4. **Touched-star knockback HEAVY, 600** — over 300 (recommended) and 150. "Stars read as bombs."

## 9. The ruled shape, laddered — `ring_price.py --burn-cap 99 --tick-stacks 1 --feed-burn 0.55 --mine-knock 600`

Blade 8.3, 6 seeds, 192 fights an arm, body 17.2%:

```
burn /s a stack     win      D-A     burn dmg/cast   shield/cast   peak stacks
  0.10             34.9%   +17.7        10.7             5.8           33
  0.15             37.5%   +20.3        15.9             8.7           33
  0.20             52.1%   +34.9        20.9            11.5           33     <- the band
  0.25             58.3%   +41.1        25.8            14.1           33
  0.30             68.2%   +51.0        30.8            16.8           32
  0.35             71.4%   +54.2        35.3            19.2           32

  blade 9.5, 0.20  63.0%   +28.1  (body 34.9)          blade 7.0, 0.25  41.1%  +33.3
```

**The curve has a step between 0.15 and 0.20** (+15pp for 0.05) that n=192 cannot resolve — Scour's tick damage had the same shape. The build bisects it at n≈700+; the design number is **0.20 a stack**, and it is a placeholder for the bisection, not a ruling.

**Uncapped, the look knobs became levers — as §6.1 said they would** (blade 8.3, 0.20 a stack):

```
                        D-A     stacks applied/cast   share of the burn from the shower
stars  6               +23.4          16.0                    ~35%
stars 10               +34.9          20.7                    ~50%
stars 16               +44.3          27.5                    ~60%

ring reach 100 x 35    +25.0          18.8      (0.43s dwell)
ring reach 120 x 42    +34.9          20.7      (0.63s)
ring reach 150 x 52    +38.0          23.1      (0.92s)

window 6s              +34.9                    window 8s   +45.8
cast every 15s         +34.9                    every 12s   +43.2
```

Each of these is priced so that the bisection compensates: whichever Rick picks, per-stack damage moves to land the relic in band, and what the pick decides is **what the relic is made of** — how much of the fire is the ring and how much is the shower.

## 10. Rick's composition rulings (2026-09-03 ~07:50 UTC), and the settled design

1. **16 small stars** — the dense shower — over 10 (recommended) and 6. The shower is ~60% of the fire; the ring is the fuse.
2. **Ring reach 120 x 42, band 24** — the recommendation.
3. **An 8-second window** over 6. Cast every 15s: the ring is up more than half the fight.
4. **Blade 8.3, the row floor** — the recommendation. Twinshade's weight; not under the row.

### The settled design, priced (10 seeds, 320 fights an arm, blade 8.3, body 17.2%)

```
cast every 15s · window 8s · ring 120x42 band 24, tilt 0.45 · ring tick 10/s: 1 dmg AND +1 burn stack · +1 stack on each crossing
16 stars at 380, r 12, bounce the CURRENT inset forever · touched: +2 stacks, knock 600 along the star's travel
window shuts: leftovers chain top-to-bottom at 70ms, blast 80: +2 stacks, knock 600 away from the blast
burn: UNCAPPED, 0.10/s a stack, 3.0s, refreshed on every application · burn damage banks ward at 0.55

arm                  win     per cast: ring s  crossings  stacks   stars touched  chained  chain hits   dmg ring  burn  shield   peak stacks
A  no ultimate      17.2%
B  ring only        30.0%              0.87       5.7       12.0         —          —         —            6.3    6.3    3.4       20
C  shower only      34.4%              0.84       5.7       22.6       11.0        3.3       0.34           —    12.4    6.8       31
D  the whole        49.1%              0.82       5.6       33.9       10.9        3.4       0.35          5.8   20.5   11.2       49

B - A  +12.8    C - A  +17.2    D - A  +31.9      (B-A)+(C-A) = 30.0 ≈ D-A: THE HALVES ADD
```

**What the relic is made of:** a ward body at 17% that the fire lifts to the band. ~34 burn stacks a cast — 12 from the ring (crossings and dwell), 22 from the shower (11 touched stars at +2) — peaking around 49 on the enemy; 26 damage a cast plus 11 shield. The chain lands a blast on the enemy in a third of casts and is the finale picture.

**The per-stack number is 0.10 as a placeholder for the build's bisection** (§9's step at n=192 is not resolved), against a target of the band on the pinned runtime. Per-stack damage is the ONE knob; everything else above is Rick's and does not move.

### Declared for the build

- The burn is a NEW status. It ticks `hp` directly like hemorrhage and smite (skips the shield), scales by `dmgTakenMul`, and is refreshed as a whole on each application — the engine expires a status whole, not a stack at a time (Bloodmirror §6.4). UNCAPPED means `maxStacks` large (99), not absent; the tag prints the count.
- **It banks ward at 0.55 of each burn tick** — that is Rick's ruling 3 and it is the first status in the game whose ticks feed the applier's shield. It routes through the same `self.shield` / `shieldMax` / `apply("ward",1)` path resolveHit uses, capped at `STATUS.ward.cap`. Priced with `me.apply("ward",1)` on every banked tick; the build should decide whether every tick restarts the 5s clock (priced) or only the application does.
- Ring ticks and star damage were priced through `m.hurt` (no crit/sunder/jitter, the foe's ward absorbs first, no beat). A build that routes them through resolveHit banks ward on the tick too (`--feed 0.55` priced that at +0.5pp — inert at 1 dmg a tick) and re-prices at its gate.
- Small stars are `shots`-like objects with `r 12` that bounce off `m.inset` (the hall closes — v64 §0) and NEVER expire on their own; only a touch or the chain removes them. `maxLive` (64, shared with the foe's arrows) is honoured by DECLINING to spawn, as the Bloodhunt fork branch does — 16 at a pop is inside the ceiling but a bow foe's volley is not accounted for.
- A touched star pays on the FOE only; the caster passes through its own stars. A 0.15s spawn grace stops a star from detonating on the foe it was born next to.
- Knock 600 is applied as `foe.vx += kx * 600` on a live, unpinned foe — the kunai's rule for a touched star (along its travel), away from the blast for a chained one.
- The chain is ordered by `y` (top of the hall first) at 70ms a star; with 16 stars and ~3-5 left, it lasts 0.2-0.35s. It runs AFTER the window shuts and the next cast waits for it.
- **The card has to say ring, burn, stars and shield in 72 characters.** Rick writes it; the ruling that the burn feeds the shield is what makes it hard.
- A hit-heavy ult must declare itself to the director (§3 rule 3): ~34 burn applications a cast file nothing. The star pop and the chain want a beat each; a fatal burn tick files one as every dps status does.

## 11. The names and the card (2026-09-03 ~08:05 UTC)

**STARWARDEN.** Rick's, from four (Sundog, Lodestar, Starwarden, Pyrelight). The school's third -warden after Farwarden and Bulwarden — the vigil compound register, and the star is in the name.

**CORONA.** Rick's, from four (Starfall, Corona, Cascade, Perihelion). The ring of light itself — the thing on screen for eight seconds; the stars are what falls out of it. Sits beside Sentinel, Aegis, Grasp, Breach, Scour.

**THE CARD IS HIS OWN LINE**, trimmed twice with him to the 72 cap `verify.py` enforces:

> *"Ring and stars deal burn damage over time. Burn is gained as shield"* — 67 characters

His original was *"Ring and stars deal burning damage over time. Burn damage is gained as shield."* (78); he cut "burning" to "burn" (74) and then took the drop of the second "damage" from three offered. Every word that ships is his.

Of the seven: **five settled** — the cell, the mechanics (with eight rulings), both names, the card. **Two open, as rendered spreads at build time, not in words:** the animations (the ring, the star, the small stars, the burn tag, the chain) and the sound.

**Build brief: `06-docs/v66/STARWARDEN-BUILD-BRIEF.md`.**

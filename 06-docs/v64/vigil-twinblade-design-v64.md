# v64 — THE VIGIL TWINBLADE, THE 34TH RELIC

**IN PROGRESS — Cowork, claimed 2026-09-02 02:40 UTC. Do not build. Do not
design this cell in another session; it is claimed in `06-docs/CLAIMS.md`.**

Cell chosen by Rick from four priced candidates (v62 table, measured at
`sc-ravelbone.html`): vigil × twinblade, ~+47pp headroom, passed over four
times before. No name and no ultimate yet. This file is written as the design
goes, not at the close.

## Why this cell

The v62 table (10 cells, 4 arms, 270 fights an arm, `cell_ults_on.py` at the
30-relic tip) put vigil × twinblade at **+47.9pp ults-off / +45.5pp ults-on**,
the most headroom of any open cell by a tier — the next is vigil × flail at
+32.8. v60 §2's caveat governs: under ~12pp is not a difference; this one is
15pp clear of second. **Not re-measured this session** — the tip has moved
three relics since (Gloamwire, Bloodmirror, Duskreave in build) and the
v60 → v62 moves were all under 4pp.

After it the twinblade row has two open cells (dwarven, sanctified) and vigil
has one (flail).

## What the cell is made of — from the repo, not re-measured

**The twinblade** (v47 survey, `sc-paradox-ignition.html`): the lightest
(mass 1.1), fastest (spin 5.7), shortest melee (reach 62) type with the lowest
damage ceiling in the game (8.3–11.9). Two opposed 70-unit blades, each with
its own 0.45s hit cooldown — 139.6 units of live edge, more than a greatsword,
on a fraction of the ground. **It loses every bind it takes** — 100% against
every other type at mass 1.1, deadlock only against the mirror. A stunned
twinblade lands nothing. Row so far: Widowmaker (bloodsworn), Spellbreaker
(runic), Twinshade (umbral), Thornshear / the Winnowing (verdant, the 26th).

**Vigil** — the ward: the blade's hits bank a shield that absorbs damage.
School so far: Farwarden (bow, Reprisal), Lightkeeper (greatsword, Bulwark),
Bulwarden (warhammer, Aegis), Vesper (scythe, Sentinel). Two things the school
has already learned the hard way, both of which any §1 here will meet:

- **The pool at the cast is a median of zero** (v41, reproduced v48: 55–57% of
  casts find an empty shell). A cast is a metronome and the ward is up ~42% of
  the fight; they are uncorrelated. Anything that reads the bank at the instant
  of the cast is inert more often than not. Aegis and Sentinel both moved to
  *feed the pool while the ultimate stands* for exactly this reason.
- **The ward channel does not carry a relic on its own** — v47 §5 measured it
  as a bank readout, not a delivered effect. The ultimate has to.

## Rick's §1, verbatim (2026-09-02)

> for a duration. when the artifact lands a hit several lightning bolts arch
> off the enemy fighter and begin to bounce around the arena. the lightning
> bolts ricochet off the walls several times before disappearing. when they
> hit an enemy they fork into two more and refresh their ricochets. when they
> hit the artifact they are consumed and apply vigil. the lightning bolts
> should fill the arena in a big loud show. after the ult begins there should
> be another timer. when the timer ends all the lightning bolts explode in a
> small area for damage and expire.

Seven clauses. Read as written:

1. **A window.** While it runs, every blade hit on the foe spawns several bolts
   AT THE FOE, which fly off and bounce.
2. **Bolts ricochet off walls, N times, then vanish.**
3. **Bolt touches the FOE → forks into two, ricochet count refreshed.** No
   damage is named for this contact — the only damage in §1 is clause 7.
4. **Bolt touches the CASTER → consumed, banks ward.** So the caster's own
   ball is a sink on the swarm, and the ward is what the swarm pays out along
   the way.
5. **The arena should fill** — the swarm is the show.
6. **A second timer, started at the cast.**
7. **When it ends, every bolt explodes in a small radius for damage, and the
   swarm is gone.**

Clause 3 is exponential by construction — every foe contact doubles a bolt —
so clause 5 is the mechanic's natural state and the real question is the cap.
Clause 4 and clause 7 pull against each other: a bolt eaten by the caster is
ward now and no explosion later. Clause 7's payoff is not the bolt COUNT, it is
the count of bolts within the small radius of the foe at the instant the timer
ends — the whole cast is priced by one frame.

Two readings §1 leaves open, to be priced both ways before Rick is asked:

- **Does a fork contact deal damage?** §1 says fork + refresh, nothing else.
- **Are the two timers one moment or two?** Either the second timer ends the
  window and detonates the swarm together, or spawning stops first and the
  swarm flies on until the detonation.

---

# 1. THE HARNESS, AND THE CONTROL

Chromium **141.0.7390.37** in a Cowork container — the same runtime v59, v60
and v62 measured on, not the repo's pinned 151. **Reproduction control, run
first:** `cell_ults_on.py --cells vigil:twinblade` against `sc-ravelbone.html`
returns **33.1% / +47.9pp / 10.7% / +45.5pp** — v62's table to the decimal.

Everything below is measured on `02-chain/sc-bloodletting.html`, **32 relics**,
the chain tip Code is building Duskreave on. The caster is the cell exactly as
`cell_ults_on` builds it — Widowmaker's twinblade profile (dmg 11.95), aff
vigil, `onSelf {ward:1}`, its own ultimate suppressed — against all 31 other
relics with THEIR ultimates live.

**The body with the ward and no ultimate wins 60.2% (3 seeds) / 56.9% (8
seeds) of fights.** That is where this relic starts before anyone designs it,
and it is why budget-v59 §3 called the two vigil cells the most spoken-for on
the board. The blade will be bisected a long way down.

# 2. THE SWARM AS WRITTEN DOES NOT FILL THE ARENA, AND THE REASON IS STRUCTURAL

`tools/storm_tracks.py` records both fighters and every blade hit at 60Hz over
93 real fights; `tools/storm_lab.py` runs the swarm OFFLINE over those tracks
(bolts do nothing to the fight until the detonation, so an overlay is honest
for everything but the ward). Bookkeeping asserted per cast: spawned + forked
= eaten + died + alive. Fork-off control asserted.

Read literally — 4 bolts a hit, thin bolts (r 8), 4 wall bounces then gone,
a 6s window, detonation at 8s, blast radius 50 — a cast looks like this:

```
                              hits  spawn  fork  peak  eaten  walls  alive  in blast  casts with none
as written                     1.8    7.4   3.3   6.9    4.9    2.4    3.4     0.21        85%
  fork OFF (control)           1.8    7.4   0.0   5.5    3.7    2.5    1.1     0.05        95%
```

Three facts, in order of weight:

1. **The twinblade lands 1.8 blade hits in a 6-second window.** It is the
   shortest weapon in the game and the foe is often away. "Several bolts" per
   hit at 4 is seven bolts a cast. There is no storm to grow from.
2. **The caster stands where the bolts are born.** A blade hit means the caster
   is ~100 units from the foe, and bolts spawn AT the foe at 600 px/s. **A
   third of all bolts are eaten within half a second of birth.** The caster is
   a sink the same size as the foe is a source, so fork (+1) and eat (−1) run
   at about the same rate and the swarm sits at equilibrium: **peak 6.9**.
3. **At the detonation 3.4 bolts are alive and 0.21 are inside a 50-radius of
   the foe.** 85% of casts detonate on nothing.

**Priced live** (`tools/storm_price.py` — the same swarm run INSIDE `m.step`,
eaten bolts banking real ward through the engine's own shield and clock, the
detonation dealing real damage through `m.hurt`, 8 seeds × 31 foes = 248
fights an arm, control arm A reproduces the no-ult body to the decimal):

```
as written, whole §1          +7.3pp        11.5 damage a cast, 8 ward a cast
```

A whisper. Not a big loud show.

# 3. WHAT MAKES IT A STORM — HIS OWN NUMBERS TURNED UP, NOT A DIFFERENT DESIGN

The growth engine is his own clause read literally: **"fork into two MORE"**
— three bolts leave the foe where one arrived. Then the swarm has to survive
the caster eating it, which means more bolts per hit and bolts that last.

```
                                          spawn  fork  peak  eaten  alive  in blast  none
as written (fork +1)                        7.4   3.3   6.9    4.9    3.4    0.21     85%
fork +2 ("two more", literal)               7.4  10.7  11.0    7.4    7.5    0.60     71%
fork +2, bolts never die on walls           7.4  13.5  14.0    8.5   12.4    1.09     59%
  + fat bolts (r 16)                        7.3  17.8  15.2   11.9   13.3    1.32     60%
  + 8 bolts a hit                          14.7  33.3  27.5   22.6   25.4    2.73     39%
  + 8s window = 8s detonation   THE STORM  19.6  34.5  31.7   24.3   29.8    2.97     30%
```

**Peak ~30 bolts, ~30 alive at the detonation, the caster has eaten ~24.** That
is the picture §1 describes. The cap (60) never binds.

**"Ricochet several times before disappearing" survives** — on the storm arm,
6 bounces is within a bolt of unlimited:

```
ric 3   peak 23.6  alive 18.5  none 49%
ric 6   peak 29.3  alive 26.9  none 36%     <- "several", and it is enough
ric 12  peak 31.7  alive 29.8  none 30%
```

**The caster as sink is the mechanic, not a bug.** With eating switched off the
swarm reaches 44 and pays no ward; with it on, ~24 bolts a cast come home. The
twinblade harvests its own storm because it fights inside it.

**Speed is not a lever** (350–800 all within noise on the finale; slower is
slightly denser). **One timer, not two**: spawning stops when the storm ends
and every bolt detonates in the same instant. Stopping the spawns early and
letting the swarm fly on only thins the finale (w6/det8: 2.73 vs w8/det8: 2.97).

# 4. THE BLAST RADIUS IS THE LEGIBILITY KNOB, AND "SMALL" MISSES A THIRD OF THE TIME

On the storm arm, bolts inside the foe's blast at the detonation:

```
radius   mean in blast   casts with NONE
  40         2.45            37%
  50         2.45–3.0        30–37%      "small"
  60         3.52            23%
  80         4.58            18%         about the twinblade's reach
 100         5.91            16%
 130         7.87            13%
```

Distribution at 80 (281 casts): median 4, quartiles 1–7, p90 10, **18% zero.**
The finale is a lottery at any radius — it is priced by where thirty
ricocheting bolts happen to be on one frame — and the radius sets how often
the lottery pays nothing.

# 5. THE PRICE, LIVE — AND WHAT THE RELIC IS MADE OF

`storm_price.py`, storm arm (8 bolts a hit, r 16, fork +2, 8s = 8s, cap 60),
blast 80, **15 damage a bolt, 2 ward a bolt**, cast every 15s. Four arms
paired on (foe, seed), 248 fights each, v59's budget shape:

```
arm                        win     casts  spawn  fork  eaten  alive  in blast  dmg/cast  ward/cast
A  no ultimate            56.9%
B  ward only              73.0%    3.60   19.1  30.7   22.4   24.6    4.12        —        37.3
C  detonation only        81.9%    2.75   16.8  29.6   20.6   23.5    4.03      60.5         —
D  the whole §1           89.9%    2.85   16.9  29.2   20.4   23.2    3.93      58.9        35.2

B − A  +16.1pp    the feed: ~35 ward a cast, on a 90 cap
C − A  +25.0pp    the finale: ~60 damage a cast, 18% of casts nothing
D − A  +33.1pp    the whole, on a body already at 57% — the ceiling is close
```

**The live swarm agrees with the overlay** (eaten 20–22 vs 24, in-blast 3.9–4.3
vs 4.6), which is the overlay's own control passing.

Variants, 3 seeds (93 fights an arm, SE ~5pp — read as tiers, not decimals):

```
                           D − A     dmg/cast   ward/cast
blast 50 ("small")         +25.8       41.5       37
blast 80                   +29.0       60.9       36
blast 100                  +33.3       73.6       35
10 a bolt                  +23.7       39         36
20 a bolt                  +34.4       79         37
1 ward a bolt              +23.7       60         20
6 bolts a hit              +22.6       44         27
```

**On v59's feed axis this ultimate is a feeder** — the ward-only arm is +16 on
its own — and it is the first vigil ultimate that PAYS INTO the shield rather
than spending it (Aegis reflects it, Reprisal fires it, Sentinel drinks it).
That is the separation from the rest of the school, and it was in Rick's
fourth sentence before anything was measured.

**DECLARED:** the live detonation goes through `m.hurt` and skips
`resolveHit`'s multipliers (sunder, crit, jitter) and the cinema beat; a build
routes it properly and re-prices at its gate. The foe's own ward absorbs it
first, as it would a blade.

# 6. WHAT THE BLADE WILL BE

A body at 57% with no ultimate, 73% with the feed alone and ~90% with the
whole storm has to give back ~40 points at the blade. Gloamwire (bow, 9.0)
and Bloodmirror gave back less. **This will be the lightest twinblade in the
game and probably the lightest blade in the game** — Twinshade's 8.3 is the
row's floor today and this one will land under it. Its blows will read as
scratches; the storm and the shield are the fighter. That is the cost of the
cell, not of the §1, and budget-v59 §3 named it before this cell was chosen.

*(Rick's rulings on §3, §4 and §6 pending)*

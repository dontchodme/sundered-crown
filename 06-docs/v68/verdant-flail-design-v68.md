# v68 — BINDWEED / TENDRIL. THE VERDANT FLAIL, THE 35TH CELL. The chain becomes a vine that hunts the foe — and the §1 as first written could not reach it, so the vine learned to.

**DESIGNED — Cowork, 2026-09-26. Claimed 06:17 UTC, designed by ~09:30 UTC.
Build from `BINDWEED-BUILD-BRIEF.md`; do not design this cell in another
session; it is claimed in `06-docs/CLAIMS.md`.**

**This one is Cowork's end to end.** Rick, 2026-09-25: *"how do you feel
about designing the rest of the fighters yourself? i think by now you should
have an idea of the standard for ults/animations that im looking for."* Asked
which of his seven inputs he wanted to keep a hand in: *"Nothing — you run it
all."* So the cell, the §1, every ruling, both names, the card, the animation
and the sound are Cowork's here, and Rick vetoes the cell after reading this
file. Written as the design went, not at the close. The lab is
`tools/vine_price.py`; every run is in `06-docs/v68/runs/`.

**And the ordering:** open cells first, then the old fighters brought up to
the standard — Rick, 2026-09-25, when he asked whether that could be done.
§9 has the list.

---

## Why this cell

Eight cells were open at `sc-trunk` (34 relics, the minute pace) and all
eight were re-priced with `cell_ults_on.py` — 4 arms, 33 foes × 10 seeds =
330 fights an arm, Chromium **141.0.7390.37** in a Cowork container, the
runtime v59–v66 priced on and not the repo's pinned 151.
**The reproduction control ran first and could have failed**: the same tool
on `sc-ravelbone.html` for vigil × twinblade returns **33.1% / +47.9pp /
10.7% / +45.5pp**, v62's table to the decimal. `runs/open8_trunk.txt`.

```
cell                      FIELD ULTS OFF          FIELD ULTS ON        body, ults on
                         floor     lift          floor     lift        (floor + lift)
dwarven x twinblade      36.1%   +40.3pp          9.7%   +23.9pp         33.6%
sanctified x twinblade   36.1%   +33.3pp          9.7%   +20.6pp         30.3%
runic x bow              35.8%   +24.5pp         13.0%   +20.6pp         33.6%
vigil x flail            16.7%   +36.1pp          3.6%   +23.6pp         27.2%
runic x warhammer        36.7%   +13.6pp         13.6%    +9.1pp         22.7%
verdant x warhammer      36.7%    +7.3pp         13.6%    +2.1pp         15.7%
sanctified x flail       16.7%   +12.7pp          3.6%    +3.3pp          6.9%
VERDANT x FLAIL          16.7%    +7.3pp          3.6%    +3.3pp          6.9%
```

1. **A flail with no ultimate wins 3.6% of fights in this field.** The minute
   pace and 33 live ultimates have moved every floor a long way from v62's
   table (the flail was 7.2% at 30 relics on the 48s clock) — which is why
   this was re-measured rather than read off v62.
2. **Entangle on a flail is worth +3.3pp with the field's ultimates on.** v59
   §3.1's contact-rate law again: the flail lands a blow every ~6.6s and
   entangle is gone in 2.8. The channel does nothing on this weapon unless
   something else applies it.
3. So here **the ultimate is the entire fighter** — ~43 points to carry from a
   body at 7%, the opposite of the Arclight trap (a body already at 57%). It is
   the type with three empty cells, so what is learned is reused twice, and the
   school with the weakest set of ultimates on v59's feed table (Rootfast +3.4,
   The Winnowing +4.8, Bramblesnare +7.2).

The two twinblade cells and the runic bow start at 30–34% with no ultimate and
would repeat v64. The vigil flail is v59 §3's most spoken-for cell on a fourth
vigil ultimate. The warhammer cells are next, on this cell's reasoning.

## What the cell is made of — from the repo

**The flail** (v43 survey; `sc-trunk`'s chain tick read directly): a haft
`reach × 0.46` turning with the weapon and a chain hung off its tip whose head
has its own angle and angular velocity — `follow` toward the driven spin,
`spring` toward the facing, a pendulum under gravity divided by the live chain
length, centrifugal extension. **The head is the weapon and it is 13.2 units
long** (`bladeSegments` returns one stub `width × 0.6` around it), so the type
covers the most ground and is live in the least of it. Contacts/s 0.152, the
lowest; 24–42.5 a blow, the highest; mass 3.6. Row: Threshmaw / Bloodmill,
Slagheart / Ironbloom, Paradox / Stasis Field, Gravemourn / Revenant.
**`f.reachMul` already grows the chain live at seven read sites** — Revenant's
line, and *"the mechanic and the animation are the same line"* is that code's
own comment.

**Verdant** — entangle `{maxStacks 4, dur 2.8, spin −0.13, move −0.06}`, 2 a
blow. Bramblesnare and Rootfast root (a true stun; one ultimate, two names),
Thicket's seeds root at a wall and lash, The Winnowing's kunai grow on every
bounce. The school's verbs are **root** and **grow**.

---

# 1. §1 — THE MECHANIC, AS FIRST WRITTEN (Cowork, 06:40 UTC)

> For a duration the whole chain becomes a living thorned vine. Anywhere the
> vine touches the enemy it bites — a small hit that leaves entangle — and it
> keeps biting for as long as it stays on them. Every bite makes the vine grow
> longer, so the more it catches the further it reaches, until it is whipping
> across half the hall. The head is still a flail head and still hits like
> one. When the duration ends the vine withers, and the thorns it left in the
> enemy take root: the enemy is held where it stands for a moment for every
> entangle stack it is carrying.

Four clauses: the chain is live; a touch is a bite (small damage + 1
entangle, its own cooldown — a hazard tick, Bloodletting's and Corona's
shape, and **the feed** v59 §2 says is what separates the ultimates that pay
from the ones that ignore their school); each bite lengthens the chain (The
Winnowing's rule on the weapon itself); the window closes on a root sized by
the stacks.

# 2. THE HARNESS, AND THE CONTROL

`tools/vine_price.py` — ring_price's shape: the §1 run INSIDE `m.step` against
all 33 other relics with THEIR ultimates live, paired on (foe, seed), the cell
exactly as `cell_ults_on` builds it (Gravemourn's flail profile, `aff
verdant`, `onHit {entangle:2}`, its own ultimate suppressed). The vine reads
the engine's own `pivX/Y` and `headX/Y` each frame; bites pay through
`m.hurt` (the foe's ward absorbs first — DECLARED, §7) and apply the REAL
entangle through `foe.apply`, so the slow is the engine's; growth writes
`f.reachMul`; the root writes `f.pin` the way Grasp's squeeze does.
Bookkeeping asserted per fight: stacks = bites × per.

**CONTROL THAT COULD HAVE FAILED, and passed:** arm A (no ultimate) on the
same seeds returns **6.97% = 23/330**, `cell_ults_on`'s ults-on body for this
cell to the fight. `runs/vine_asWritten.txt`.

# 3. THE §1 AS WRITTEN IS A WHISPER, AND THE REASON IS THE TYPE

```
arm                      win    casts  bites  stacks  dmg   touch%   foe stk   head blows in/out window
A  no ultimate           7.0%                                                        —  / 9.08
B  bites only            8.2%   3.23   1.67    1.7    3.3    3.6%     1.52      3.85 / 5.25
C  bites + growth        7.9%   3.20   1.75    1.8    3.5    3.8%     1.57      3.87 / 5.16
D  the whole §1          7.9%   3.24   1.75    1.7    3.5    3.9%     1.57      3.89 / 5.25
R  root only             7.6%
```

**+1pp.** The vine touches the foe on **3.6% of window frames** and bites 1.7
times a cast. Arclight's first table, one type along: the flail's blow comes
every 6.6 seconds not because the head is small but because **the two balls
are apart**, and a 52-unit segment hung off a haft is apart with them.

And the growth clause is wrong the other way round. Turning it up (`runs/
vine_grow*`, `vine_time*`): a chain grown to 2.5× or 3× reads **3.3–6.7%**,
BELOW the body, with the head landing FEWER blows in the window (3.2 against
3.9). A longer chain swings a bigger circle and the head is on the foe's
spot less often, not more. Width ×3 and the haft live buy +1 to +2. **No
number in the sentence as written turns it into a fighter.**

# 4. THE VINE REACHES, AND THAT IS THE FIGHTER

A vine is not a chain: it grows toward what it wants. So the §1's third clause
changed — not "every bite makes it longer" but **"it turns toward the enemy
and grows until it reaches"** — and the price moved by fifty points.

In the lab: while the window is open the facing is driven toward the foe
(`me.theta` turned at `turn` rad/s; the drive spin is zero so the head hangs
off the haft's tip on its spring and its pendulum, swaying) and `reachMul`
eases at 0.3/s toward the distance to the foe's rim, capped at 3.0, drawing
back in when the foe comes closer. **The head's own blade stays live** — a
flail head at the tip of a vine that is already on the foe.

Blade 20 (from 24 — §6), 330 fights an arm, `runs/vine_b20_*`, `vine_seek*`:

```
                                                   win     bites/cast  touch%  head blows in/out
the sentence as written (no seek)                  7.9%       1.8        4%       3.9 / 5.2
seek, no growth, no bites, no root                48.8%        —        14%      11.3 / 5.5
seek + bites, no growth                     (B)   58.2%       5.4       14%      11.0 / 5.4
seek + bites + growth to 3.0 blind          (C)   47.9%      11.2       35%      10.3 / 5.2
seek + bites + growth to 2.0 blind                62.7%       9.2       29%      11.5 / 5.1
seek + bites + GROWS UNTIL IT REACHES       (C)   62.7%       9.5       30%      11.3 / 4.9
  ... and draws back in                     (C)   67.0%       7.8       23%      12.0 / 5.0
  ... + the root                            (D)   67.3%       7.8       23%      11.9 / 5.1
```

Three facts:

1. **The reach is the fighter.** Seeking alone, with nothing else in the
   sentence, is +42 on a body at 7%: the head lands **11 blows in its windows
   against 5 outside**, one every two seconds while the vine is on the foe,
   at the flail's own blow. This is `mode:"swing"` measured on the greatsword
   in August (+50pp from one field) arriving on the flail, and it is what a
   vine IS.
2. **Blind growth costs ten points; growth that stops at the foe pays.** A
   vine grown to 3× overshoots — the SEGMENT still bites but the HEAD is past
   the foe. Grown to the foe's rim and held there, the head sits where it
   hits. "Grows until it reaches you" is the sentence, and the number agrees.
3. **The bites and the root are the school, not the payload** — each is worth
   about six points on top of the reach (§5). That is the right shape: the
   type does the hitting, verdant does the entangling and the rooting.

# 5. THE TURN RATE IS THE FEEL KNOB, AND IT IS TAKEN AT 4 RAD/S

A facing that SNAPS to the foe is a turret. A vine turns. Priced at blade 20:

```
turn        snap    4 rad/s    2 rad/s
win        67.3%     55.5%      34.5%
```

**Twelve points for a vine that takes 0.8s to come round a half-turn, and
another twenty-one for one that takes 1.6s.** Taken at **4 rad/s** — alive,
not aimed — and it is the second-strongest knob in the design after the
blade, which the build can use if the pinned runtime reads hot.

## 5.1 THE WHOLE, DECOMPOSED — blade 19, turn 4, 20 seeds = 660 fights an arm

`runs/vine_t4_b19_full.txt`, `vine_t4_b19_seekgrow.txt`:

```
arm                                       win     casts  bites  stacks  dmg    touch%  foe stk  root s   head blows in/out
A  no ultimate                            1.5%                                                              —  / 9.1
   seek + growth, no bites, no root      42.6%    3.25    —       —      —      19%     2.67       —      11.9 / 5.4
B  seek + bites, no growth               40.8%    3.32   5.0     5.0    10.1    12%     2.82       —      10.3 / 5.7
R  seek + root, no growth, no bites      40.5%    3.43    —       —      —      12%     2.35     0.71     10.9 / 5.9
C  seek + growth + bites                 48.8%    3.15   7.0     7.0    14.1    19%     3.08       —      11.4 / 5.2
D  THE WHOLE                             54.4%    3.20   7.1     7.1    14.2    20%     3.07     0.90     11.6 / 5.3

D − A   +52.9      the reach ~+41 of it, growth-to-reach ~+6, bites ~+6, root ~+6
```

**Second seed block** (`seed0 9001`, 660 fights): D at 19 reads **55.8%**
against 54.4; at 18, **48.3%** against 51.7. The whole reproduces to within
1.4 points on one block and 3.4 on the other — read as tiers, v60 §2.

The foe carries **~3.1 entangle stacks** on an average window frame — its
swing at −40%, its move at −18% — which is what makes the head's one-blow-
per-two-seconds land: a vine slows what it is holding. The bites deal 14 a
cast; the root holds the ball and the weapon 0.9s a cast. Neither is the
fighter and both are the school.

## 5.2 WHAT SUBSTITUTES AND WHAT ADDS (v64's lesson 2, checked)

seek+growth 42.6 → +bites 48.8 → +root 54.4: each half adds on top of the
other. B and R (no growth) both read ~40.7 — without the growth the vine is
short and the bites and the root have less to work with, so growth is the
half that makes the other two pay. **Keep all three; the growth is not
optional and the cap is not "for safety".**

# 6. THE BLADE

The type's own 24 (Gravemourn's profile, `cell_ults_on`'s donor) reads
**67.9%** with the whole at snap seek. The curve at turn 4:

```
blade    body (A)    whole (D)      n
  20       2.1%       55.5%        330
  19       1.5%       54.4 / 55.8  660 × 2
  18       1.4%       51.7 / 48.3  660 × 2
  17       0.9%       52.1%        330   (snap seek — reads high)
  14       0.3%       38.5%        330   (snap seek)
```

**About 2.7 points a damage point and the crossing is near 18.** That makes
this the lightest flail in the game — Threshmaw's 25 is the row's floor
today — and the body with no ultimate is ~1%: **the vine is the fighter**,
Starwarden's shape, and this time the blade IS the balance lever, because the
payload is the head's own blow and scales with `dmg` (the Arclight failure
was a payload that did not). The build settles it wide on the pinned runtime
(brief stage 5); expect **17.5–18.5** and do not bisect.

**The type spread is wide and it is the vine's nature** (D, blade 19):

```
greatsword 78.6%   twinblade 66.0%   flail 46.7%   scythe 46.4%   warhammer 45.0%   bow 37.5%
worst: Ironhail 25, Farwarden 25, Gloamwire 30   ·   best: Axiom 100, Heartwood 95, Lightkeeper 90
```

41pp, Thornshear's and Shroudmaul's tier — a vine hunts what comes close and
bows stay away. Open item 12/32 for a third time; written down, not fixed.

# 7. DECLARED — what the lab pays through, and what the build must route

- **Bites go through `m.hurt`**: the foe's ward absorbs first; no crit, no
  sunder multiplier, no jitter, **no knock, no hit stop, no stagger, no beat**
  — Scour's tick rule, on purpose: a knock on a bite would push the foe off
  the vine (Cindercleave's shove cost 2.3 points for that reason). The build
  routes bites as a hazard tick and NOT through `resolveHit`; if it must use
  `resolveHit`, it strips knock/stop and re-prices at gate 3.
- **The head's blow is untouched** — `resolveHit`, `hitCd` 0.45, the flail's
  knock, the beat. A head sitting on a pinned foe: `ballCollision` treats a
  pinned ball as immovable (open item 42) and the knock is discarded by the
  pin; measured in the lab as part of the whole.
- **Seek** in the lab is `me.theta` turned toward the foe at 4 rad/s with the
  drive spin zero (`w.spin = 0` for the window). The build implements it in
  `tickWeapon`'s chain branch: while `f.ultVine`, theta turns toward the foe
  at `u.turn` instead of advancing by spin, and `drive = 0`. The spring, the
  sag and the extension are untouched — that is the sway.
- **Growth** is `f.reachMul` eased toward `(d − R) / (reach × mods.reach)`
  at 0.3/s in both directions, clamped [1, 3.0]; restored to 1 on close
  (Revenant restores it the same way). All seven read sites already multiply
  by it; the builder refuses to write if any does not (the v53 rule).
- **The root** is `f.pin = max(pin, 0.3 × stacks)`, `pinMax`, `pinV` the way
  the squeeze writes it; `tickStasis` hands it the weapon lock, so ball AND
  weapon are held (Rick, 2026-08-31: hitstun should freeze the ball). Fires
  only when the window closes on its own clock with both alive — a stun owed
  to a corpse is not owed (Grasp), and a window the caster's death ends
  roots nobody.
- **Not a `pinFree` hold**: the vine's root holds everything. `_drawField`'s
  held-ball block draws Paradox's hexagon on any `pin > 0` without `pinFree`
  (open item 41) — the build gives the root its own picture (§8.3) and skips
  that block for it.
- **Blade blows inside the window count as ordinary blows** for curse pools,
  hemorrhage, sunder and the director; nothing here writes `f.stun`.

# 8. THE NAMES, THE CARD, THE PICTURE AND THE SOUND — Cowork's rulings

**BINDWEED.** The fighter. A real creeper that strangles what it climbs — one
word, a plant, and it says what the relic does. From: Bindweed, Bracken,
Strangler, Witherlash. Sits beside Heartwood, Thornwake, Vinesower.

**TENDRIL.** The ultimate. The thing on screen — a vine reaching. Single
concrete noun, the register Rick set with Garrote, Breach, Grasp, Scour,
Corona. From: Tendril, Overgrowth, The Reaching, Stranglehold.

**The card (70):** `The chain becomes a vine that hunts the foe. Bites entangle, then root`
— measured in pixels by `tip_audit` at the build, not counted (the v53 rule).

## 8.1 The picture — the vine, and it is the same line as the mechanic

- **The cast**: the chain greens from haft to head over 0.30s — each link
  sprouts a leaf pair and a thorn as the green passes it. The head is wrapped
  in bramble. Verdant's palette exactly: `core #4FD06B`, `glow #BCF7C7`,
  `dark #0D3A1A`; the steel goes to `dark`, not to white (§4.1b: a self-buff
  separates by VALUE — this one is a colour change on a chain that was grey).
- **The reach IS the animation.** `reachMul` moves the drawn chain and the
  hit segment together (Revenant's comment); the vine visibly lengthens
  toward the foe at 0.3 of its own length a second and shortens as the foe
  closes. Nothing else animates the growth. A LEAF SCALE along the vine — one
  leaf pair per 12 units — makes the length countable as it grows.
- **The turn**: the haft turns at 4 rad/s; the head lags on its spring and
  sags — the sway is real physics and needs no art.
- **A bite**: a thorn flash at the contact point on the foe's rim (source-
  over, 0.12s, `glow`), the entangle tag on the foe printing its count.
  **No freeze** (v67: bites are a flurry and would freeze the world at 3/s).
- **The window tell**: the vine stays green and leafed for the whole window;
  the shell carries a thin green rim. Nothing in the hall says "window open"
  except the vine itself, and the vine is the biggest object in the hall.
- **The wither**: on close, brown runs head-to-haft over 0.4s, leaves drop as
  drawn (not spawned — `spawnFx` draws the match RNG) debris, the chain is
  grey again.
- **The root**: at the wither, vines sprout from the floor around the foe's
  ball — four shoots up the rim, `dark` with `core` tips, clenched for the
  pin's length, then wilting on the `pinMax` fade. **This replaces the runic
  hexagon** the held-ball block would draw (§7).
- **The silhouette**: a verdant flail has no art yet — the head as a bramble
  knot on a green-barked haft, first cut at stage 1, redraw a separate claim
  (the umbral scythe's precedent).
- **The particle field**: an emitter along the vine (leaf motes, `glow`,
  sparse) in `src/render/fx.js` AND the inlined copy, sha re-stamped
  (Thornshear's lesson; open item 46 is two relics without one).

## 8.2 The sound — registers, rendered as a spread and picked on measurement

Code renders a spread of four per voice in an `OfflineAudioContext` and
measures it (CLAUDE.md §4.4; every burst under 0.6s, §4.5); the pick is on
the numbers below, not on a word, and Rick can overrule any of them from the
clips.

- **Cast** — a rising rustle-and-creak, 0.5s, noise band-passed 400–3k with
  a low creak under it (a re-struck `_tone` at 70–90 Hz, since a held note
  does not exist here). Not a chime, not a crack: this is growth.
- **Bite** — a short wet snap, 60–90ms, peak ≤0.45, pitched up a semitone per
  entangle stack on the foe (the count in the ear — Sentinel's hum rule: the
  number of snaps is the number of bites).
- **Root** — a low creak into a crack, 0.35s, share below 120 Hz ≥ 0.4
  (Deadfall's detonation register: this is the biggest single thing the
  relic does).
- **Wither** — a dry falling rustle, 0.4s, high-passed 1.5k, quiet (peak
  ≤0.3): the tell that the window is over.

# 9. THE REDESIGN LIST — after the open cells, Rick's order

From v59 §2's feed column and the v5-era `kind`s still on the roster. Each
is its own claim when its turn comes; nothing here is started.

```
Exsanguinate   Widowmaker    nova + 3 hemorrhage       worst feed in the game (−6.7)
Bulwark        Lightkeeper   nova, extra knock         +1.4
Consecration   Censer        nova + 3 smite            +5.3
Unmaking       Spellbreaker  bolt + 3 hex              +7.7, the same bolt as
Corollary      Axiom         bolt + 3 hex              +14.9  ... this one
Bloodprice     Goreshard     beam + 3 hemorrhage       a beam
Benediction    Aureole       beam, heals 28            a beam
Quarrelstorm   Ironhail      arrow nova                +5.3
Bramblesnare   Thornwake     root 1.6s                 one ultimate with
Rootfast       Heartwood     root 1.3s                 ... two names
Daybreak       Dawnbringer   sparks, healing           −4.8, and the bloom fight
```

The seven cells still open after this one: sanctified × flail, vigil × flail,
verdant × warhammer, runic × warhammer, dwarven × twinblade, sanctified ×
twinblade, runic × bow. The two warhammer cells are next on §"Why this
cell"'s reasoning.

---

# Open decisions

1. **RICK'S VETO.** This is the first cell designed without his §1. The
   mechanic that survived pricing is not the one first written (§3–4): the
   vine REACHES. If that is not the fighter he wants, it is one sentence to
   say so before a builder is opened.
2. **THE TURN RATE** is 4 rad/s on feel, priced at 12 points against a snap.
   The build may move it inside 3–5 to land the band before it moves the
   blade, and says so in the build doc if it does.
3. **THE BLADE** — 17.5–18.5 expected; the build settles it wide, both sides,
   two blocks, on the pinned runtime, after reproducing this document's arm A
   (~1.5%) and arm D (~55% at 19) with `vine_price.py` unmodified on 151.
   Every decimal here is on Chromium 141 (v64's §3aa moved a gate 7.8pp
   between the two).
4. **THE TYPE SPREAD** (41pp, bows at 37%) is open item 12/32's question for
   the third time and is Rick's, not this build's.
5. **THE BITE'S DAMAGE PATH.** Priced through `m.hurt`. If the build routes it
   otherwise, gate 3 writes the gap.
6. **THE HELD-BALL PICTURE.** The root gets its own (§8.1); the runic hexagon
   must not be drawn on it. If the build finds `_drawField`'s block cannot be
   skipped cleanly, `pinFree` is NOT the answer here (the weapon must be held
   too) — say so and Rick rules.

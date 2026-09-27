# v89 — THE STAFF ROW. The seventh type: seven ranged relics whose basic attack is a SPELL, one per school, each with its own ultimate. Designed at once, handed off at once.

**DESIGNED — Cowork, 2026-09-27 (~03:30 UTC). Seven cells, `06-docs/v90/`
through `06-docs/v96/`, one design doc and one BUILD-BRIEF each. Rick accepts
or rejects per cell from those docs; Code builds the survivors from the briefs
and designs nothing (rule 0). Claimed in `06-docs/CLAIMS.md`.**

**Rick, 2026-09-27:** *"id like to get started building the staff weapon type.
id like you to design all of them at once and then we can hand off to code to
build them all. you design ill reject/accept. id like each staff to use a
ranged attack like bows do but each attack is a unique spell. id like each one
to also have its own unique ult. everything up to the new standards."*

The axe and the staff were held back on 2026-08-20 (v38) *"until the current
six types are filled."* The grid filled on 2026-09-26 (v75: 42 of 42). This is
the staff.

## 1. What a staff IS — the type

**A staff is a bow that casts.** Type owns the physics (weapon-matrix decision
1), and the staff's physics are the bow's exactly, so that the ONE thing that
differs between the bow row and the staff row is the projectile:

```
reach 54   width 9   artW 44   spin 2.8   mode "ranged"   mass 1.6   blades [0]
```

It keeps the bow's short blade segment and therefore the bow's whole shape:
*hits from anywhere, dies up close*. Its `shape` is `"staff"` — new art (a
rod with a head; each school's head is its own — §6 of each cell doc).

**What the bow row shares and the staff row does not: the `shot` block.**
Every bow fires the same arrow (`cadence 0.34, speed 380, r 24, life 3.4, grav
0`) — "the shot is a property of the TYPE" (Aureole's comment). On a staff
the shot IS the school: seven `shot` blocks, seven behaviours. The spell still
leaves along the facing on a cadence as the staff sweeps, is still clankable
(all but one), still resolves through `resolveHit` with the school's channel
on it. Nothing about how a shot is spawned, moved or landed changes; what
changes is what the shot IS.

## 2. The seven, in one table

```
#   cell                  fighter      spell (the basic attack)                                     ultimate       what it does                                                        bow body → spell body → whole    blade   doc
43  bloodsworn x staff    BLOODWICK    BLOODSEEKER  a globule that bends toward the foe (home 1.0)     GYRE           the seekers orbit the caster, then lunge as one when the foe closes  5.0 → 15.9 → 50.5%   at 8.5    ~8.5    v90
44  umbral x staff        NIGHTGLASS   SHADEBOLT    a bolt that ricochets off two walls                BACKLASH       shrouded: half of every blow it takes is thrown back, cursing         0.3 → 18.0 → 45.5%   at 7.3    ~7.6    v91
45  vigil x staff         WATCHLIGHT   WARDBOLT     a heavy bolt of light that shoves (knock 420)      BEACON         sets down a lantern that fires at the foe; each hit banks ward       5.6 → 20.5 → 49.7%   at 9.3    ~9.3    v92
46  verdant x staff       BRIARWAND    THORNBURST   a fan of three short thorns                        BLOOM          a pollen cloud drifts after the foe: inside, entangle and bites      21.5 → 23.3 → 53.8%  at 17     ~16.5   v93
47  runic x staff         CIPHER       GLYPH        a bolt that stops on the wall and hangs as a rune  CONVERGENCE    every rune leaves its wall and hunts the foe, hexing                 9.5 → 31.2 → 50.5%   at 11     ~11     v94
48  sanctified x staff    CROZIER      LANCE        a needle of light no blade can parry               RADIANCE       every lance grows as it flies: farther is bigger, hits harder        28.2 → 18.2 → 52.1%  at 14.5   ~14.5   v95
49  dwarven x staff       CULVERIN     SLUG         a lobbed iron slug that falls                      IRONFALL       lobs shells onto where the foe will be; they burst and sunder        22.3 → 24.1 → 47.9%  at 13     ~13     v96
```

"bow body" is arm A: the bow with the school's channel and no ultimate, at
the staff's blade. "spell body" is arm S: the staff with its spell and no
ultimate. "whole" is the staff with both. All at 660 fights an arm (33 foes x
20 seeds), `sc-leaf`, Chromium 141.0.7390.37 — see §4.

## 3. What held across the seven (write it down once)

- **A spell can be the whole fighter, and then the ultimate is nothing.**
  The first seeker (home 2.2) read **96.4%** at blade 14 with no ultimate, and
  Gyre on top of it was +1. The first ricochet read 88% at 14. A basic attack
  is fired ~100 times a fight; an ultimate runs 8s in 16. So the spells were
  priced FIRST and turned down until the ultimate had room: the seeker's turn
  went 2.2 → 1.0 rad/s (a bend, not a hunt), and the whole row's blades sit
  7–17 against the bow row's 12.7–16.2. **Seeking is still the strongest
  property in the game** (v87) — it is now also the strongest BASIC ATTACK.
- **A fast shot lands LESS.** The lance (560 px/s, r 16) lands 7.6 a fight
  where the arrow (380, r 24) lands 17: at the same blade the sanctified
  staff body is 10 points UNDER the sanctified bow body. A slow shot is
  walked into; a fast one is not. Every speed in the row is a hit-rate knob
  and none of them was free.
- **Aiming is the monster, again.** Beacon aimed direct read 97% and lead-aimed
  92% at blade 13 until its cadence was cut 0.5 → 1.2s; Ironfall aimed at where
  the foe IS read 89% against 72% with the lead. Every aimed thing in this row
  is deliberately worse than it could be (v75 §3, the prophecy kept because it
  is worse).
- **Bursts on the floor do not land; continuous status does (v87, seven more
  times).** Sequence (runes detonating in order) was +0 at 14 and was
  replaced; Ironfall's burst is +0 and is kept for the picture; Bloom's
  entangle (3.7 stacks on a window frame) and Convergence's hex are the
  payloads. Sanctum — a smiting, healing ring on the caster — priced +54 and
  was REJECTED for being Benediction (v82) with a staff in it.
- **Things hung on the caster's ball pay off the type's weakness.** A staff
  dies up close; Gyre (orbit and lunge, +35 over the spell) and Backlash
  (+28) both turn the close range into the window's strength. That is a
  design choice, priced, and it is why those two cells' bodies are the
  lowest in the row (16–18%).
- **The bow bodies of four schools are nearly nothing at these blades**
  (bloodsworn 5%, umbral 0.3%, vigil 5.6%, runic 9.5%): a blade of 7–11 on
  a bow is a blade the bow cannot use. The spell is what makes those cells
  relics at all.

## 4. How they were priced, and what to trust

- **The harness is `tools/ult_overlay.py`** (v69) with one module per cell
  in `tools/overlays/staff_*.js`. Donor `ironhail`, `--cell <aff>:staff`; the
  module rewrites the donor's `shot` block for the spell (restored at the end
  of every fight) and tags every shot the engine spawns with the spell's
  extra fields (`home`, `bounce`, `knock`, a fan, a wall-stop, a pierce); the
  ultimate runs in the module on the harness's 8s-in-16 clock. Every run is in
  `06-docs/vNN/runs/`.
- **Runtime: Chromium 141.0.7390.37 in a Cowork container — NOT the pinned
  151.** The batch's runtime (v87). **The control that can fail passed:**
  v75's arm A (`ironhail` as `runic:bow`, `sc-trunk`, 10 seeds) reproduced
  **33.64% = 111/330 to the fight** before any staff number was taken
  (`06-docs/v89/runs/control_v75_trunk.txt`). Every brief's stage 0 is its own
  reproduction on 151.
- **The build is `sc-leaf`** (34 relics, the build of record). Each staff was
  priced ALONE as a 35th relic against the 34. **Seven staves in one field
  will move each other** — the bow row is the row every staff beats or loses
  to most (§5) — so the blades here are brackets for a 41-relic field, not
  numbers.
- **n = 330 an arm for the sweeps, 660 for the settled row.** Tiers, not
  decimals (v60 §2). Blades are from two or three points each and every
  build settles its own wide, both sides, two blocks, on 151, never by
  bisection (v48/v56/v66).
- **One instrument caveat:** the harness's `hits in/out` column counts blows
  the ENGINE lands. The lance (v95) lands through the module, after the
  harness has read the counter, so for Crozier read `lanceHits`, not
  `hits in/out`. Every other cell's column is honest.

## 5. Type spread of the whole, at the settled blade (arm U/Y/Z, 660)

```
               greatsword  twinblade  warhammer  scythe  flail  bow     worst three
Bloodwick          29         50         59        54     70    51     Dawnbringer 5, Lightkeeper 5, Axiom 10
Nightglass         26         27         56        61     51    54     Starwarden 0, Dawnbringer 5, Spellbreaker 5
Watchlight         40         35         58        53     48    67     Starwarden 0, Lightkeeper 5, Dawnbringer 15
Briarwand          79         46         45        51     68    27     Aureole 15, Farwarden 20, Marrowdraw 25
Cipher             39         42         62        41     69    61     Spellbreaker 20, Duskreave 20, Dawnbringer 25
Crozier            46         70         49        46     56    51     Duskreave 10, Lightkeeper 25, Farwarden 25
Culverin           34         48         50        56     56    47     Lightkeeper 15, Nightfell 25, Duskreave 25
```

The greatswords (Dawnbringer's aimed swing, Lightkeeper's bank) are the row's
counter, as they are the bow row's; **Briarwand is the exception** (79 against
greatswords, 27 against bows — the fan is short and a bow outranges it) and
Crozier's counters are inverted the way Angelus's are (twinblades 70). Item
12/32 gets seven more points.

## 6. What the build needs that the engine does not have

Shared, once, in the first staff built:

- `shape: "staff"` and its art (a rod; the head per school). `artW 44` as the bow.
- `mode: "ranged"` already fires `f.w.shot` along the facing. **No change.**
- Per-shot fields already read by `tickShots`: `home` (Bloodhunt), `bounce`
  (the kunai), `knock` (Reprisal), `grav` (Reprisal), `shard/pop/popR`
  (Slagburst), `over.onHit`. **Five of the seven spells are these fields set
  at spawn.** Two need a line each: the fan (spawn N at `theta ± k·spread`,
  v93) and the wall-stop (a bounced bolt with `bounce 0` becomes `sigil`,
  v94); one needs a flag on the blade test (`pierce`, v95).
- Seven ultimate `kind`s, each its own (`gyre`, `backlash`, `beacon`, `bloom`,
  `converge`, `radiance`, `ironfall`), each with a window of 8 on a charge of
  16. Each brief says what state it keeps and where its hooks are.
- Every one of these declares itself to the director (rule 3): a cast files
  `ult`; shots file as ever; Backlash's reflected blow, Bloom's bites and
  Beacon's lantern shots need a beat of their own.

## 7. The order to build, if the vetoes leave the order alone

1. **Culverin** and **Briarwand** — the two whose spell is nearly the bow
   (+2 each over the bow body) and whose blades stay in the bow row's range
   (13, 16.5). The cheapest way to see whether a staff READS.
2. **Cipher** and **Watchlight** — one new shot behaviour each (the wall-stop,
   the lantern), blades 11 and 9.3.
3. **Crozier** — the pierce flag and the grow-in-flight.
4. **Bloodwick** and **Nightglass** — the two low-body cells whose ultimates
   are the fighter; build them last so the row's first four have settled the
   field they land in.

One at a time; the chain is one chain. Each has its own claim row, its own
brief, its own stage 0.

## 8. Open decisions (the row's; each cell has its own)

1. **Rick's accept/reject, cell by cell.** Seven docs.
2. **The seven together.** Priced alone against 34; land them and re-price
   the row against 41 before any blade is called settled.
3. **The physics.** Identical to the bow on purpose (§1). If a staff should
   FEEL different in the clank (heavier, a longer reach), that is a type
   decision Rick makes once, and it re-prices all seven.
4. **The names are Cowork's** (each doc has the spread of four). Any of them
   is Rick's to change; the fighter names and the spell names are the two he
   is likeliest to want.
5. **Art and sound are specced, not rendered** — each build's last stage
   spreads them (rule 2).

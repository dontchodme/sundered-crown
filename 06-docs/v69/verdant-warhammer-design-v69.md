# v69 — IRONWOOD / CANOPY. THE VERDANT WARHAMMER, THE 36TH CELL. The hammer takes root and grows into a tree — and one bough was a mid-sized ultimate until it grew two more.

**DESIGNED — Cowork, 2026-09-26 (~11:30 UTC). Build from `IRONWOOD-BUILD-BRIEF.md`;
do not design this cell in another session; it is claimed in
`06-docs/CLAIMS.md`.** Cowork's end to end (Rick, 2026-09-25: *"you run it
all"*; 2026-09-26: *"do it all. we will hand off the whole thing at once"*).
Rick vetoes the cell from this file. Lab: `tools/ult_overlay.py` +
`tools/overlays/tree.js`; runs in `06-docs/v69/runs/`.

## Why this cell

Second on the v68 table's reasoning: with the field's ultimates live the
warhammer body wins **13.6%** and entangle adds **+2.1pp** on it (the hammer's
blow comes every ~5.5s, entangle is gone in 2.8) — **15.8% before anyone
designs it**, the second least-decided cell after the flail's. Fills verdant
to 6 of 6 types (the first school finished) and the warhammer to 6 of 7.

## What the cell is made of — from the repo

**The warhammer** (v41 survey): reach 76, width 26, spin 1.6 (the slowest),
**mass 5.0** (wins every bind), **knockMul 2.3** (throws what it hits across
the hall), 20–29 a blow, `mode:"spin"`, one blade. Row: Grudgebearer /
Crucible (pulls in, consumes Sunder), Censer / Consecration (nova), Bulwarden
/ Aegis (a shield that reflects), Shroudmaul / Grasp (a hand), Ravelbone /
Garrote (a wire ring that holds the ball and leaves the weapon free).
`f.reachMul` at seven sites; `w.blades` is an array of angular offsets read
by `bladeSegments` every frame — the twinblade is `[0, 0.5]`.

**Verdant** — entangle `{4, 2.8s, spin −0.13, move −0.06}`, 2 a blow. Roots
(Bramblesnare, Rootfast), seeds (Thicket), growth (The Winnowing), and now a
vine that hunts (Tendril). Its verbs are ROOT and GROW, and the one thing the
school has never done is root ITSELF.

---

# 1. §1 — THE MECHANIC, IN PLAIN WORDS (Cowork, 10:10 UTC)

> For a duration the hammer takes root. The ball stops dead where it stands
> and grows bark — it can't be moved or knocked, though it can still swing —
> and the haft grows into a bough, longer and longer, until the hammer is a
> tree sweeping most of the hall. Then two more boughs grow out of the trunk,
> so there are three heads turning. The blows of the boughs are lighter than
> the hammer's, but there are three of them and they reach across the room.
> Anyone standing under the canopy is caught in the brambles and entangled.
> When the duration ends the tree withers back to a hammer and the roots let
> go.

Four clauses: the self-root (Garrote's verb — ball held, weapon free — on the
caster, which nothing in the game has done); growth of reach (Revenant's
line); **three boughs** (`w.blades` → `[0, ⅓, ⅔]`, lighter blows); a canopy
that entangles (the feed, the school's status applied continuously to anyone
inside the reach).

# 2. THE HARNESS, AND THE CONTROL

`tools/ult_overlay.py` — the v68 lab lifted into one harness with the
mechanic in a JS module (`overlays/tree.js`), so every design from here runs
on the same code and the same control. Chromium 141, `sc-trunk`, 33 foes ×
10 seeds = 330 fights an arm (660 for the settled runs), the cell exactly as
`cell_ults_on` builds it (Grudgebearer's hammer profile, `aff verdant`,
`onHit {entangle:2}`, own ultimate off).

**Two controls, both passed.** The harness itself: Tendril re-run as an
overlay module reads **56.5%** at blade 19 against `vine_price.py`'s
54.4 / 55.8 on two blocks (`v68/runs/overlay_control.txt`) — the two tools
close a window one frame apart, so the fights are not identical, and the
number is inside the block spread. And arm A here reproduces
`cell_ults_on`'s ults-on body for this cell **to the fight: 15.76% = 52/330**.

# 3. ONE BOUGH IS A MID-SIZED ULTIMATE; THREE ARE A FIGHTER

`runs/tree_base.txt` (blade 23.5, cap 3.0, 330 an arm):

```
arm                                         win    casts  hits in/out  canopy%  foe stk
A  no ultimate                             15.8%            —  / 11.3
G  growth only                             28.2%   3.27   6.6 / 6.7      —       1.75
B  self-root + canopy, no growth           17.0%   3.48   4.1 / 7.1     15%      2.40
C  self-root + growth                      26.1%   3.36   5.8 / 6.9      —       1.53
D  the whole (one bough)                   31.8%   3.46   6.1 / 6.9     48%      3.06
T  growth + canopy, no self-root           35.2%   3.29   7.0 / 6.7     49%      3.33
```

**+16.** A hammer grown to 3× reach lands no more blows in its window than
out of it (6.1 against 6.9 a fight): at 1.6 rad/s the head comes round once
every 3.9s, and reach does not change that. The foe is under the canopy 48%
of the window and gets hit twice. The type's own rhythm is the ceiling.

So the tree grows more heads. `w.blades = [0, ⅓, ⅔]` — three boughs, each
with its own `hitCd` — and the ceiling triples (`runs/tree_boughs*`):

```
boughs   cap    win at blade 23.5    hits in/out
  1      3.0        31.8%              6.1 / 6.9
  2      3.0        78.5%             10.2 / 6.4
  2      2.0        74.2%              9.3 / 6.7
  3      3.0        91.8%             11.9 / 5.7
  3      2.0        88.5%             11.1 / 6.0
  4      3.0        96.1%             12.6 / 5.3
```

Far too much — at the hammer's own blow and 2.3× knock, three heads at
2–3× reach is a wall of hammers. **The blade is the wrong lever for it**: at
blade 16 three boughs still read 67.9% and the body falls to 1.8%, a hammer
that is nothing outside its windows (`runs/tree_boughs3_b16`). The design
wants the hammer to stay a hammer.

# 4. THE BOUGHS ARE LIGHTER THAN THE HAMMER, AND THAT IS THE KNOB

A bough is a branch, not a maul: while the tree stands, `w.dmg` is scaled by
`winDmg` (the head's blow OUTSIDE the window is untouched). Three boughs,
cap 2.5 (`runs/tree_b3c25_w*`, blade 23.5):

```
winDmg    win     hits in/out
 1.00    ~90%
 0.50    66.4%    16.2 / 7.3
 0.35    47.3%    17.9 / 7.8
 0.25    33.3%    19.2 / 8.1
```

**0.35 — a bough hits for a third of the hammer, 18 times a fight in
windows, and the hammer outside is still a 23.5 hammer landing 7.8.** That is
the shape: a real warhammer for 36 seconds of the minute, a whirling tree for
24. Taken.

## 4.1 THE WHOLE, DECOMPOSED — blade 23.5, 660 fights an arm (`runs/tree_w35_full`)

```
arm                                         win    casts  hits in/out  canopy%  foe stk  growth peak
A  no ultimate                             14.5%            —  / 11.4
G  growth + boughs only                    47.7%   3.63  20.0 / 7.5      —       3.15     2.46
B  self-root + canopy, no growth           18.2%   3.44   4.1 / 7.2     16%      2.45      —
C  self-root + growth + boughs             48.2%   3.76  17.9 / 7.8      —       2.84     2.46
T  growth + boughs + canopy, no root       49.5%   3.64  20.2 / 7.4     41%      3.50     2.46
D  THE WHOLE                               47.1%   3.75  18.0 / 7.7     41%      3.24     2.46

D − A  +32.6    the boughs are all of it; the self-root and the canopy each read inside ±2
```

**The self-root is free and the canopy is free** (G, C, T and D are one
tier at n=660). Both are kept, and the reason is Grasp's rule: *any
arrangement delivering the same number is worth the same, so every remaining
choice is made for the picture.* The self-root is the tell — the ball stops
dead and barks over, and nothing else in the game does that — and it is what
makes "takes root" true rather than a name. The canopy is the school: the foe
under the tree carries **3.2 entangle stacks** on an average window frame,
visibly caught, and a tree that does not entangle is a windmill. A rooted
caster is also the tree's one honest weakness (§6: Bloodletting mills it).

## 4.2 The picture measured before it was drawn

The foe is under the canopy **41%** of the window; the three boughs land a
blow every **1.3s** of window on average; growth peaks at **2.46×** (reach
187 at act 1, 224 at act 3) — the hall is 520 wide and 240 at full inset, so
by the Third Seal the canopy is most of the room.

# 5. THE BLADE, AND IT STAYS A HAMMER'S

```
blade     body (A)     whole (D)              n
 23.5      14.5%        47.1%               660
 25.0      18.9%        54.1 / 55.2%        660 × 2
 27.0      24.7%        62.0%               660
```

**~4 points a damage point; the crossing is near 24** — Grudgebearer's own
23.5, mid-row, and the body is a real 15–19%. The first cell in this batch
whose fighter is a weapon with a set-piece rather than a set-piece with a
weapon. The build settles it wide on the pinned runtime; expect 23.5–24.5.

**The type spread** (D, blade 25): greatsword **86%**, bow 52, warhammer 46,
twinblade 45, scythe 44, flail 36. Worst: **Bloodmirror 0%**, Twinshade 15,
Duskreave 25 — a rooted caster cannot leave a standing hazard, and
Bloodletting's discs mill it where it stands. Best: Axiom and Lightkeeper
100, Heartwood 95. 50pp, open item 12/32 again; and the Bloodmirror pairing
is a **counter a viewer can learn** (the tree cannot walk away from the
scythes), which is what item 12 is asking whether we want.

# 6. DECLARED

- **Self-root** is `f.pin` on the CASTER with `pinFree = 1` for the window
  (the weapon keeps turning; `tickStasis` skips the weapon lock), `pinV =
  [0,0]`, re-armed every frame so nothing shortens it; released on close to
  REST (`vx = vy = 0`, the Stasis clamp's spirit — no stale vector). While
  rooted the ball is an immovable object in `ballCollision` (the foe bounces
  off the trunk at 2×), takes no knock, and gravity is skipped by `move`.
  A rooted caster that DIES ends the window (the harness's death close).
- **Growth** is `f.reachMul` eased at 0.35/s to 2.5, restored to 1 on close
  (Revenant). The seven read sites already carry it.
- **Three boughs** is `w.blades = [0, 1/3, 2/3]` for the window, restored
  after; `f.tips` and `f.hitCd` sized to three (the lab had to — the engine
  indexes both by blade). Each bough has its own 0.45s `hitCd`, its own
  ribbon, and hits through `resolveHit` exactly as the hammer does — knock
  2.3×, sunder, crit, the beat — at **`w.dmg × 0.35` while the tree stands**
  (a per-window `dmg` scale: the lab wrote `w.dmg`; the build should scale
  in `resolveHit`'s damage line off `f.ultTree` rather than mutate the
  weapon). Bough blows count as blows for every pool and status.
- **The canopy** applies `entangle 1` every 0.5s to a foe within `reach ×
  reachMul × mods.reach + R` of the caster — the real status through
  `foe.apply`, no damage, no knock, no beat.
- Hit stop: bough blows are ordinary blows and carry the ordinary freeze —
  **eighteen a fight in windows is a flurry** and v67's burst rule
  (`stopDR`) is what keeps the world from freezing every 1.3s; the build
  measures the freeze census per window as the Winnowing's did.
- Charge 16, window 8 (the row's).

# 7. THE NAMES, THE CARD, THE PICTURE, THE SOUND

**IRONWOOD.** The fighter — a real tree so hard it sinks, and a hammer's
word. From: Ironwood, Oakheart, Rootmaul, Boughbreaker.
**CANOPY.** The ultimate — the thing overhead. From: Canopy, Arbor, Bough,
Greenwood.
**Card (70):** `Takes root and grows three sweeping boughs. Foes beneath them entangle`
— pixels at the build.

## 7.1 The picture

- **The cast**: the ball stops dead (the pin) and BARK grows up its shell from
  the floor over 0.4s — `dark #0D3A1A` plates with `core #4FD06B` seams — so
  the tell is the ball itself changing material. Roots (three, drawn) grip
  the floor under it. This replaces the runic hexagon `_drawField` would
  draw on any pin (the build skips that block for `pinFree` casters, as
  Garrote's snag does).
- **The growth is the animation** (`reachMul` moves the drawn haft and the
  hit segment together): the haft thickens into a trunk and lengthens at
  0.35 of its own length a second; the hammer head becomes a burl at the
  end of it. At 1.5s the two other boughs SPROUT from the trunk — drawn
  growing out over 0.5s to full length, each ending in a lighter burl (the
  0.35 says so visually: a smaller head).
- **The canopy**: a faint leaf-lit disc at the boughs' reach, `glow #BCF7C7`
  at alpha 0.06 — a range read the viewer needs, because the entangle lands
  on anyone inside it. The foe inside carries the entangle tag and its count.
- **A bough blow** is an ordinary hit (the hammer's own flash and knock).
- **The wither**: on close the boughs draw back into the trunk over 0.4s,
  the trunk shortens to a haft, the bark cracks and falls as drawn debris,
  the roots let go and the ball drops (it was at rest; gravity resumes).
- **The silhouette**: a verdant warhammer has no art — a knotted burl head on
  a barked haft, first cut at stage 1.
- **Particle field**: leaf motes shed from the three boughs' tips while the
  tree stands, in both `fx.js` copies, sha re-stamped.

## 7.2 The sound — registers; Code renders a spread and picks on measurement

- **Cast (the rooting)**: a deep creak and a ground-thud, 0.5s, share below
  120 Hz ≥ 0.5 — the heaviest thing in the hall is putting down roots.
- **The sprout** (at 1.5s): two quick woody cracks, 80ms each, a fifth apart.
- **A bough blow**: the hammer's own strike voice, pitched down a fourth and
  quieter (peak ≤ 0.6 of the hammer's) — a lighter head on a longer arm.
- **The wither**: a dry creak falling in pitch, 0.4s, quiet.

# 8. Open decisions

1. **Rick's veto.** A hammer that roots itself and grows into a three-headed
   tree is the most visually aggressive thing in the batch; if it is too
   much, the two-bough tree at cap 2.0 reads 74% at blade 23.5 and is one
   flag.
2. **The bough damage scale (0.35)** is the build's ONE knob if the pinned
   runtime reads out of band — before the blade, which stays a hammer's.
3. **The blade** — expect 23.5–24.5, settled wide on 151 after reproducing
   arm A (~14.5%) and arm D (~47% at 23.5).
4. **Bloodmirror 0%** — a counter, and Rick's question (item 12/32).
5. **Whether the trunk parries** — three blades clank and bind like any
   blades; the tree at mass 5 wins every bind it takes, which the lab priced
   as part of the whole. If the build finds three simultaneous binds do
   something the engine did not expect, it says so.

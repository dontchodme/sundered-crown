# v72 — PORTCULLIS / ONSLAUGHT. THE VIGIL FLAIL, THE 39TH CELL. The ball is the weapon: it charges, every slam hits for the shield it carries, and every slam banks more — and two shield-on-a-chain ideas were priced first and lost.

**DESIGNED — Cowork, 2026-09-26 (~16:00 UTC). Build from
`PORTCULLIS-BUILD-BRIEF.md`; do not design this cell elsewhere; claimed in
`06-docs/CLAIMS.md`.** Cowork's end to end; Rick vetoes from this file. Labs:
`overlays/bastion.js`, `overlays/rampart.js` (rejected), `overlays/ram.js`
(taken); runs in `06-docs/v72/runs/`.

## Why this cell, and what it is

v59 §3's "most spoken-for" cell: the flail body wins **3.6%** with the
field's ultimates live and **ward adds +23.6** on it — a 27% relic before
anyone designs it, because ward banks 55% of every blow and the flail's
blows are the biggest in the game. So the ultimate here needs +23, not +43,
and it needs to be something a school whose four ultimates are *reflect,
fire, drink, feed* has not done. Closes the flail row to 7 of 7 (the third
type finished) and puts vigil on 6 of 6 — **the second school finished**.

**Ward** `{bank 0.55 of damage dealt, cap 90, 40% blast on a break, knock
210}`. **The flail's problem is contact** — three cells in this batch have
now measured it (v68 §3, v69 §3, v71 §3): a thing hung off the head meets
the foe 4–20% of a window.

---

# 1. §1 (Cowork, 15:10 UTC)

> For a duration the ward hardens the shell and the ball itself becomes the
> weapon. It charges at the enemy. Every time the two balls slam together,
> the enemy takes a hit worth a share of the shield the ball is carrying,
> is knocked back, and the slam banks more shield. The flail head keeps
> swinging.

Three clauses: the charge (the ball accelerates at the foe); the slam (a
ball-to-ball contact pays `0.25 × shield`, knock 500); **the bank** (+8 ward
a slam — the feed, and the thing that makes the slams grow).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141, `sc-trunk`, Gravemourn's flail as `vigil ×
flail` (`onSelf {ward:1}`, own ultimate off). **Arm A reproduces
`cell_ults_on` to the fight: 27.27% = 90/330.**

# 3. TWO SHIELDS ON A CHAIN, PRICED AND REJECTED

**The bastion** (`bastion.js`): the head becomes a ward disc (r 40 + 0.5 ×
shield) that parries any blade that strikes it (0.25s weapon stun, shove
250), kills arrows, and banks 8 ward a parry.

```
A 27.3%   B parry only 28.2%   C bank only 39.7%   D whole 37.3%     parries 3.3 a cast
```

+10. The foe's blade strikes the head 3.3 times in eight seconds. A
defensive head is only struck when the foe comes to it, and the foe does
not.

**The rampart** (`rampart.js`): every blow banks its FULL damage for the
window with the cap lifted to 200, and the pool DETONATES on close (0.6 ×
pool within 150, knock 500) — Slagburst's shape in ward.

```
A 27.3%   B swell only 36.4%   C burst only 22.4%   D whole 32.7%     pool peak 45, the burst lands 19% of casts
```

+5, and the burst is NEGATIVE — it spends 24 points of shield on a blast
that finds the foe one time in five. The flail lands 4.7 blows in a window;
there is not enough to bank.

# 4. THE BALL IS THE WEAPON

`ram.js` — the caster's ball charges (600 px/s² toward the foe, capped at
`speedMax`) and a ball-to-ball contact (d < 2R + 3, once per 0.5s) is a
slam. Blade 24.03, 330 an arm (`runs/ram_base`):

```
arm                                            win     rams/cast  dmg/cast  banked/cast  shield on a window frame
A  no ultimate                                27.3%
B  slam (10 + 0.25 x shield), no charge       45.2%     3.0        38          —              9.5
C  charge + slam                              51.5%     3.5        45          —              9.5
D  charge + slam + bank 8                     70.3%     3.5        50         28             17.9
```

**Balls meet three times in a window whether or not anyone charges** — the
hall is 520 wide and two balls at cruise cross it in a second — which is why
the ram works where the head-shield did not: the CONTACT IS ALREADY THERE.
The charge adds half a slam and +6; the bank adds +19 and doubles the
shield the ball carries.

70% wants a smaller slam. The flat 10 is dropped — **a slam hits for the
shield and nothing else**, so a ball with no ward slams for nothing and a
full one for 22:

```
slam = 10 + 0.25 x shield     70.3%
slam =  5 + 0.25 x shield     65.5%
slam =      0.25 x shield     57.3%     <- taken: the rule is the picture
slam =      0.40 x shield     61.8%
```

## 4.1 The whole, decomposed — blade 24.03, 660 an arm (`runs/ram_settled_full`)

```
arm                                  win     casts  hits in/out  rams  dmg/cast  banked/cast  shield
A  no ultimate                      28.0%              —  / 10.5
B  slam only (0.25 x shield)        31.2%    3.52   4.4 / 5.7     3.2     9.3        —          10.1
C  charge + slam                    33.9%    3.41   4.8 / 5.6     3.6    10.9        —          10.5
D  THE WHOLE                        54.4%    3.52   5.1 / 5.8     3.7    16.7      29.1         18.4

D − A  +26.4     the bank is +20 of it; slam and charge +3 and +3
```

**The bank is the fighter, again** (v70 §3, v71 §3.1): 29 ward banked a
cast, the ball carrying 18 on an average window frame against 10 without —
and a slam that hits for the shield grows with it. Slam and charge are
small and kept because they ARE the mechanic; without the ram there is
nothing for the bank to hang on.

# 5. THE BLADE — near the type's own

```
blade    body (A)    whole (D)
 24.03    28.0%       54.4%
 22.0     22.7%       47.6%
 20.0     10.6%       37.7%
```

**~3.4 points a damage point; crossing near 23.** A flail's blade
(Threshmaw 25, Gravemourn 24), and a real body. Expect 22.5–23.5.

**Type spread** (D): greatsword 71, warhammer 64, twinblade 58, scythe 54,
bow 35, **flail 33**. Worst Ironhail 20, Gloamwire 20, Slagheart 25 — bows
and a flail that latches. Best Axiom 90, Lightkeeper 80. 38pp; item 12/32.

# 6. DECLARED

- **The charge**: `f.vx += ux × 600 × dt` toward the foe each frame of the
  window (a pinned caster does not charge), speed clamped at `speedMax`
  1300. It is an acceleration on top of the engine's own motion, not a
  replacement — the ball still bounces, still falls.
- **A slam**: `d < 2R + 3`, once per 0.5s: `hurt(foe, 0.25 × shield, f)`
  (ward first; no crit/sunder/jitter, no hit stop, no beat from the
  overlay — the build files a beat on a slam: a ball-to-ball hit is a
  moment), `knock 500` away from the caster, and the bank: `shield =
  min(cap, shield + 8)`, `shieldMax`, `apply("ward", 1)` — the three writes
  resolveHit's vigil branch makes.
- The head's blow is untouched. Charge 16, window 8.
- The ram is NOT `ballCollision` — that runs as ever (the shoulder); the
  slam is an extra payment on the same contact, so a slam and a shoulder
  happen together.

# 7. NAMES, CARD, PICTURE, SOUND

**PORTCULLIS** — the gate that comes down on you; a fortress word for a
fortress school. From: Portcullis, Siegeward, Keepwarden, Buttress.
**ONSLAUGHT** — the charge. From: Onslaught, Battery, Sally, Breakwater.
**Card (71):** `The shell charges the foe. Each slam hits for the shield and banks more`

## 7.1 The picture

- **Cast**: the ward's plate hardens — vigil's pink shield ring on the ball
  thickens to a plated shell (six hex plates, `dark` edges, `core` seams)
  over 0.25s; the plates stay for the window and their FILL brightens with
  the shield (0 → 90 maps to alpha 0.15 → 0.6), so the bank is readable on
  the ball.
- **The charge**: a short speed-streak behind the ball while it accelerates
  (drawn from velocity, no rng).
- **A slam**: a plate flash at the contact point, the number (0.25 × shield,
  rounded) floated in vigil's `glow`, the foe knocked, and the ward tag on
  the caster ticking up — the bank is the read.
- **Close**: the plates crack and fall as drawn debris, 0.3s.
- Silhouette: a vigil flail — a plated square head on a banded haft, first
  cut. Field: spark motes off the plates on each slam, both copies.

## 7.2 The sound

- **Cast**: a metal-on-stone clang and a low hum settling, 0.4s.
- **A slam**: a heavy gated thud (share below 120 Hz ≥ 0.45, ≤ 0.25s), louder
  with the shield (peak 0.35 → 0.65 across 0 → 90).
- **A bank**: the ward's existing bank voice, reused.
- **Close**: plates falling — three short clinks.

# 8. Open decisions

1. Rick's veto. Two shield-head ideas were priced and lost (§3) — if a ram
   is not what he wants from a vigil flail, the bastion (+10) is the
   picture-first fallback and needs a different payoff.
2. The blade — 22.5–23.5, wide on 151 after reproducing A (~28%) and D
   (~54%).
3. Whether a slam should file a beat (the design says yes) — the director
   sees a ball-to-ball hit today as nothing.
4. Ironhail/Gloamwire 20% — item 12/32.

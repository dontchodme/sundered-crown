# v94 — CIPHER / CONVERGENCE. THE RUNIC STAFF, the 47th cell. Its spell is a bolt that stops on the wall and hangs there as a rune; its ultimate calls every rune off the walls at once to hunt the foe.

**DESIGNED — Cowork, 2026-09-27. Build from `CIPHER-BUILD-BRIEF.md`; do not
design this cell elsewhere; claimed in `06-docs/CLAIMS.md`.** Rick accepts or
rejects from this file. Lab: `tools/overlays/staff_runic.js`; runs in
`06-docs/v94/runs/`. The row: `06-docs/v89/STAFF-ROW-v89.md`.

## Why this cell

Runic's status is a stun on the foe's weapon (hex: 0.2s every 1.15s a
stack, 5 stacks) — a bow that lands 20 arrows stacks it well (Oracle's cell
was the bow row's strongest body). The runic bow body at blade 11 is 9.5%.
Runic knows things in advance and writes them down (Foregone, Corollary,
Deadfall's sigils, Rebuttal's runed walls); a staff that writes runes on the
walls and then reads them back is the school's sentence.

---

# 1. §1 (Cowork)

> **GLYPH (the spell).** The staff throws a rune bolt every 0.34s along its
> facing, at an arrow's speed. A bolt that lands hexes. A bolt that reaches
> a wall does not die: it STOPS there and hangs as a sigil for 4s, and a foe
> that touches a sigil takes the blow and is hexed twice.
>
> **CONVERGENCE (the ultimate).** For 8s the runes come off the walls: every
> sigil that is hanging when the window opens leaves its wall and flies at
> the foe (380, homing 3 rad/s), and every new sigil laid inside the window
> does the same half a second after it is laid.

Two clauses: the wall-stop (the spell — the misses are not lost, they wait);
the convergence (the ultimate — the waiting runes are spent, all at once,
as seekers).

# 2. THE HARNESS, AND THE CONTROL

`ult_overlay.py`, Chromium 141.0.7390.37, `sc-leaf`, Ironhail's bow as
`runic × staff` (`onHit {hex:1}`, own ultimate off), the spell as
`shot {cadence 0.34, speed 380, r 22, life 3.4, grav 0}` with `bounce 1` on
every shot: the engine's wall bounce fires once, and the module turns the
bounced bolt into a sigil (`vx = vy = 0, life 4.0, over.onHit {hex:2}`). The
row's control (v89 §4) reproduced v75 to the fight. Arm A is the runic BOW
body at the staff's blade.

# 3. THE FIRST ULTIMATE WAS A DETONATION, AND IT WAS WORTH NOTHING

Blade 14, 330 an arm (`runs/runic_14b`, `runs/runic_14_converge`):

```
arm                                                          win     hits in/out   sigils laid/cast   hanging at cast
A  bow body                                                 23.3%       — / 20.6
S  glyph                                                    47.9%    10.7 / 17.5        26                1.9
U  glyph + SEQUENCE: the sigils detonate in order (r 150)   47.9%     8.8 / 17.4        26                1.9     5.7 pops, 0.57 land
X  the same at r 220                                        53.6%     8.8 / 17.5        26                1.9     1.2 land
Y  glyph + CONVERGENCE (home 3)                             74.2%    15.8 / 16.4        28                2.4     6.9 launched, 6.2 blows a window
Z  the same at home 6                                       (a hopping bug — re-run below)
```

**The wall-stop alone is +25**: a bolt that misses hangs where the foe will
bump into it, and 26 sigils a cast-equivalent (≈ 90 a fight) is a hall
full of them. A sigil hangs only 4s and the foe touches ~2 in that time.
**Detonating them is +0** — a rune on a wall is far from a foe in the
middle, and blowing it up spends the one that would have been touched. (v87:
bursts on the floor do not land.) **Sending them at the foe is +26**: they
are seekers, the strongest property in the game, and they are made of
misses. Home 3 at 380 is a turn radius of 127; home 6 was tried, hopped
(a launched rune re-read as a sigil and stopped in mid-air — the module was
fixed and home 3 kept, the picture of a rune that has to come round).

## 3.1 Settled — blade 11, 660 an arm (`runs/settle_runic`)

```
A  bow body                9.5%
S  Glyph                  31.2%     +22 — 25.5 sigils a cast-equivalent, 1.75 hanging when a window opens, 31 blows a fight (12.3/18.6 in/out)
Y  + Convergence          50.5%     +19 — 5.4 launched a cast, 5.7 blows a window, foe at 2.6 hex on a window frame
```

# 4. THE BLADE

```
blade    spell (S)    whole (Y)
10       24.8%        39.7%
11       31.2%        50.5%
14       47.9%        74.2%
```

**Crossing near 11.** Body ~31% — the row's strongest body: this is a relic
whose spell is half the fighter (Coldiron's shape, v73). Expect 10.8–11.2
on 151.

**Type spread** (Y, 660): flail 69, warhammer 62, bow 61, twinblade 42,
scythe 41, greatsword 39. Worst Spellbreaker 20, Duskreave 20, Dawnbringer
25; best Gravemourn 85, Lightkeeper 80, Marrowdraw 80.

# 5. DECLARED

- **The spell** — `shot: { cadence 0.34, speed 380, r 22, life 3.4, grav 0,
  dmgMul 1.0, sigil: { life 4.0, hex 2 } }`. `spawnShot` sets `bounce 1` when
  the profile has `sigil`. In the wall branch of `tickShots`, a shot whose
  bounce has just been spent and whose profile has `sigil` becomes one:
  `vx = vy = 0, life 4.0, r 22 (unchanged — a bigger r puts it inside the
  wall and the wall kills it: measured), sigil: true, over: { onHit: { hex:
  2 } }`. A sigil is a stationary shot: the foe's ball landing on it resolves
  the blow (`resolveHit` with the caster as self, hex 2 through `over`), the
  foe's blade sweeping it clanks it away (the counterplay, and it reads),
  its life runs out and it fades.
- **The ultimate** — `f.ultConverge = { t0, end, fuse }`. At cast every
  hanging sigil of the caster's is given `fuse = t + 0.25·k` in the order it
  was laid; inside the window a sigil that becomes one is given `fuse = t +
  0.5`. When `t ≥ fuse`: `home 3`, velocity 380 at `atan2(foe − sigil)`,
  `life 3.0`, `sigil: false`, `flown: true` (a flown rune is never re-read as
  a sigil: the wall kills it as it kills any shot). Its blow is the sigil's
  (hex 2).
- Charge 16, window 8. Nothing waits.

# 6. NAMES, CARD, PICTURE, SOUND

**CIPHER** — a thing written that means something else. From: Cipher,
Glyphwright, Runecaller, Sigilstaff.
**GLYPH** (the spell). From: Glyph, Rune, Sigilbolt, Inscription.
**CONVERGENCE** — the runes come together on one point. From: Convergence,
Recall, Reckoning, Sequence.
**Card (59):** `Every rune on the walls leaves it and hunts the foe, hexing`
**Shot tip (40):** `Bolts stop on walls as runes · clankable`

## 6.1 The picture

- **The staff**: a slate rod inscribed root to head with runes in runic
  `core`; the head is an open ring; the bolt leaves through the ring.
- **The spell**: a bolt drawn as a rune glyph with a short trail; on the
  wall it STOPS with a small flash and sits as a sigil (r 22, the glyph,
  `glow` at alpha 0.6, breathing over its 4s). Walls with five runes hanging
  on them is the tell.
- **Cast**: the ring at the head lights; every hanging rune flares in
  sequence (0.25s apart — the order they were laid) and leaves its wall, and
  each one draws a thin sight-line from itself to the foe for its first
  0.2s of flight.
- **In-window**: a rune that lands on a wall flares and leaves it 0.5s
  later.
- **A hit**: the hex tag ticks by two; a rune flare on the foe.
- **Close**: the ring dims.
- Field: rune motes drifting off the walls toward the centre, both copies.

## 6.2 The sound

- **The wall-stop**: a short stone tap (the bolt has stopped) — quiet,
  pitched by how many are hanging.
- **Cast**: a rune-ring "open" (v75's register, the same school) — an
  inhale into a chime, 0.4s — then one soft tap per rune as it leaves, in
  sequence.
- **A hit**: the bow's own arrow voice plus a hex snap.
- **Close**: the chime reversed.

# 7. Open decisions

1. Rick's accept/reject. Sequence (detonation) is priced +0 at r 150 and +6
   at r 220 and not taken.
2. The blade — 10.8–11.2, wide on 151.
3. home 3 is the taste number; 6 is unpriced (the module bug ate the run).
4. `sigil.life` 4.0 is a picture number: longer walls-full-of-runes is
   unpriced and would move the spell body.

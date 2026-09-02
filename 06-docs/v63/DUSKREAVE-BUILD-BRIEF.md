# DUSKREAVE / SCOUR — BUILD BRIEF. THE UMBRAL SCYTHE, THE 33RD RELIC, THE LAST SCYTHE. A PURPLE TORNADO THAT SWEEPS THE FLOOR, EATS SHOTS, AND GRINDS WHOEVER IT CATCHES WITH TICKS THAT ARE REAL HITS.

**Cowork, 2026-09-02. FOR CLAUDE CODE. Every decision below is Rick's or is
measured; the measured ones say so and name the tool.** Design record:
`duskreave-design-v62.md` (not a linear read — HANDOFF-v62 §8 has the order),
checked in `duskreave-check-v63.md`. **Read the check first; it is short.**

This brief is written in stages with a gate after each, the way Rick asked for
the umbral package on 2026-08-31. **Stop at a gate that fails.** If anything in
here cannot be built as written, say so and stop — do not redesign around it
(CLAUDE.md §3 rule 0).

---

# 0. THE RELIC IN ONE TABLE

```
id                duskreave
name              DUSKREAVE            Rick, from four
aff               umbral
shape             scythe               body IDENTICAL to the row: blades:[0], reach 104,
                                       width 11, artW 46, spin 3.2, mode "spin", mass 2.4
dmg               21                   Rick: Bloodmirror's weight (v62 §12/§17)
onHit             { curse: 1 }         the school's channel, exactly as the other four umbral carry it

ult.name          SCOUR                Rick, from four
ult.charge        15
ult.tip           "Conjures a tornado that absorbs projectiles. Enemies caught in it take rapid damage"
                                       RICK'S OWN LINE, 2026-09-02. One string, both surfaces.
                                       Measured: 2 lines in the ult-bar reminder (390px at 18px
                                       Atkinson Next), 2 lines on the scrunch panel at 21px. Nothing dropped.
ult.kind          "scour"              new kind; nothing shares it (RULE 9 — one sigil, one sound, one picture)

THE TORNADO
  duration        10.0 s               Rick: a duration, not a count
  width           160                  Rick (31% of the 520 arena)
  top             y = 600              Rick: "a third of the arena"; the band runs from 600 to the floor
  sweep           200 px/s             MEASURED FREE (v62 §8b: contact 17.3/17.3/17.4% at 120/200/300).
                                       Looks only. See §2 for start point and direction.
  tick rate       7.0 / s              Rick, 2026-09-02, after being shown +59 and offered trims: KEEP
  base tick       5                    Rick: "lots of ticks for less damage"
  catch rule      foe.y + R >= 600  &&  |foe.x - cx| <= 80 + R     (R = ballR 34; the EDGE rule the labs used)
  drag            pulls the caught ball toward (cx, floor)          strength is Code's knob — v62 never modelled it
  projectiles     any ENEMY shot inside the band is removed         flavour, never priced (v62 §2)

THE TICK IS A HIT.  It goes through `resolveHit`. It collects the foe's curse echo.
It pushes its own dmgBase into the foe's curse pool and calls apply("curse", 1).
It does NOT knock back, does NOT hit-stop, does NOT hit-stun, does NOT file a beat.  (§3)
```

**Priced (v63 §3–§4, `tools/duskreave_price.py`, 986 fights an arm, donor's own
ultimate stubbed, Chromium 141.0.7390.37):**

```
    today's curse rule (keep the 3 BIGGEST)      +59.2pp     the strongest ultimate in the game. Rick: accepted.
    the last-3 window (ruled, lands later)       +40.5pp     below Crossweave. Rick: accepted — "last-3 goes in; Scour lands at ~+40"
```

**Both numbers are of a MODEL** (`hurt` + a hand-computed echo, windows pinned at
t=12/t=30, no drag). The built relic will price differently. Gate 6 re-prices it
for real and writes the gap down.

---

# 1. THE CURSE RULE THIS RELIC IS BUILT AGAINST — READ THIS BEFORE STAGE 3

Rick ruled 2026-09-02 that curse changes school-wide from "keep the three
biggest blows" to "keep the last three", **and that the change lands only after
Gloamwire ships, as its own commit** — `06-docs/v63/curse-window-v63.md`,
claimed in CLAIMS.md. It is NOT part of this brief.

**Build Duskreave against whichever rule is in the build of record when you
start.** The tick's behaviour is identical under both — it collects the echo,
it pushes its dmgBase, it applies. Only the price changes (+59 vs +40), and
Rick has accepted both. What you must NOT do is build the window here, or build
a tick that behaves differently under the two rules. One tick, one rule at a
time, and gate 6 prices whatever pair is in the link.

---

# 2. STAGES AND GATES

## STAGE 1 — THE RELIC, ULT STUBBED. `02-chain/sc-duskreave.html`

Add the weapon with `ult` present and `kind: "scour"` wired to a no-op cast (a
banner and nothing else), so the charge clock and the ult bar behave and the
fight is otherwise the row's. Art: **the umbral scythe silhouette** — the row's
outline in umbral's `core #A45CF0 / glow #DDB8FF / dark #280A44 / steel
#B6A5C9`. **Film it and show Rick a strip before stage 2** — v58's `_whEaten`
was rejected on sight after it was built and tuned, and CLAUDE.md §4.0 exists
because of it.

**GATE 1.** `engine_ab` byte-identical on every existing pairing (31 relics
→ 3720/3720 or whatever the count is at that build); `verify` unchanged;
`row_price`-style no-ult floor for the new relic near **17.6%** (v63 §3,
control 2) — it is a 21 scythe with curse and no ultimate, and if it lands
near 26% something is firing that should not be.

## STAGE 2 — THE TORNADO EXISTS AND SWEEPS. NO DAMAGE.

On cast: a `Match.tornado` object `{ src, cx, dir, t, dur: 10, w: 160, top: 600 }`.
It is a vertical band from `top` to the floor, `w` wide, centred on `cx`.

- **Start and direction — Code's call, filmed:** the labs started it at the
  left wall and bounced it wall-to-wall at 200 px/s; sweep speed is measured
  free so start point almost certainly is too. Starting under the caster and
  heading toward the foe will read better. Pick, film, keep.
- Bounces off the walls (the band's edge, not its centre, reaches the wall).
- Advanced by the ordinary step, frozen by hit-stop like everything else.
- Expires at `t >= dur`. Two casts a fight at charge 15 is the expectation.
- `ultFx` for the set-piece; `ULTSIG.duskreave` for the sigil; a banner as
  every other cast gets. Nothing else yet.

**GATE 2.** Film 3 casts on 3 seeds, before any tuning. The band's width and
height must read as "a third of the arena" and "a third of the width" in the
frame. `engine_ab` on every OTHER pairing still identical (the tornado must
not touch fights it is not in).

## STAGE 3 — IT CATCHES, DRAGS, AND TICKS. THIS IS THE RELIC.

**The catch.** Each step, the foe is `caught` when `foe.y + R >= top` and
`|foe.x - cx| <= w/2 + R` — the EDGE rule, which is what every v62 number was
measured with (v62 §8a is the control that failed when the two rules were
mixed; do not mix them).

**The drag.** While caught, a pull on the foe toward `(cx, floor - R)`. Rick's
§1: *"dragged down into it."* The labs did not model this — v62 HANDOFF §6 —
so its strength is unmeasured. Guidance: strong enough that a ball that enters
the band from the side is still in it a second later; not a pin (`foe.pin`
stays 0 — a pin is what the Sentinel and Garrote use and it changes how every
other system reads the ball). Do not knock; pull. Film it.

**The tick.** Every `1/7 s` while caught and `foe.alive` and `!m.over`, **ONE
call into `resolveHit`**, with `mul` defined (it is a projectile-class hit, not
a melee connect — that is what keeps Ironbloom's latch, the Crucible's strike,
Garrote's connect, Deadfall's stamp and Revenant's hands from firing off a
tornado tick; every one of them tests `mul === undefined`) and with an `over`
that switches off the four things a tick must not do:

```js
this.resolveHit(f, foe, foe.x, foe.y, null, u.tick / f.w.dmg,
                { onHit: { curse: 1 }, knock: 0, stop: 0, stun: false, beat: false });
```

`over` today carries only `onHit` (10990–10995). **Extend it** — do not fork
`resolveHit`. The four exclusions, and where each lands in the pipeline
(line numbers are `sc-garrote.html`):

| exclusion | where | why it must be off |
|---|---|---|
| `knock: 0` | 11219–11222, `foe.vx += (kx/kl) * power` | the ordinary knock is AWAY FROM THE CASTER'S BALL, 165 × knockMul, and 7 of them a second throw the foe out of the thing that is supposed to hold them |
| `stop: 0` | 10907–10910 | `stopBase 0.045 + 0.0022 × dmg` ≈ 0.067s a tick; 7 a second freezes the world ~45% of every second the tornado holds someone (step 7184–7187 freezes position) |
| `stun: false` | 10955 `foe.takeHitstun(dmg)` | 7 stagger-locks a second; the DR grinds it down but the first second is a lock, and the drag is the control here, not the stun |
| `beat: false` | 10936–10954 | 23 `hit` beats a fight from one ultimate; `cinePlan` would cut to every one. `_cineVine` (10924–10936) is the precedent for a hit that is real but not a shot |

**What the tick KEEPS, and must:** the roll (jitter ±15%, crit 9% × 2.1),
`foe.dmgTakenMul()` (Sunder), **`Math.round(foe.curseEcho())` folded into
`dmg` above the Aegis block (10812–10814)**, the Aegis check and reflect,
`hurt`, `self.hits++ / self.dealt += dmg`, the float over the ball, and the
`onHit` loop: `foe.pushCurse(dmgBase, 1)` then `foe.apply("curse", 1)`, with
the status tag printing `curseSum()`. **The echo is the relic.** v62 §11b: on
the `hurt` path this is a +17.8 ultimate; on the `resolveHit` path it is +29.7
at 4.5 ticks and +59 at 7. Sentinel's `beamHit` uses `hurt` and is the
precedent you will be tempted by. **Do not follow it.**

**The tornado's own weight (Code's call, filmed):** with the ordinary stop
and stun off, the tick may want a SMALL stop of its own the way Harrowing's
scythes carry `stopBase 0.05 / stopPer 0.014` (11320, 13371) — or none. Feel.
Film both; do not tune before filming.

**The director (CLAUDE.md §3 rule 3):** one `ult` beat at the cast (fireUlt
files it), and **one `hit`-class beat the first time each cast catches
someone**, filed by hand with `dmg` = the cast's running total so far and
`fatal` honest. A hit-heavy ult that files nothing is scored as empty air.
The fatal tick must file a beat regardless — the Thicket's rule (10930–10935).

**GATE 3 — the checks, and each can fail:**
1. `duskreave_relic_probe.py` (write it on `garrote_relic_probe`'s pattern):
   over 300 fights, the tornado's ticks must average **well above base** when
   the foe's pool is non-empty — a tick whose damage equals `round(5 × jitter)`
   every time is collecting no echo and is on the wrong path.
2. Across one tick: `foe.vx, foe.vy` change ONLY by the drag, `m.hitStop` does
   not rise, `foe.stun` (what `takeHitstun` writes, 6731) does not rise,
   `m.beats.length` does not rise except on the first catch and the fatal.
3. `foe.stacks("curse") === foe.cursePool.length` after every tick (the
   invariant `apply` derives).
4. Every other `mul === undefined` mechanic must be unreachable from a tick:
   a Duskreave vs Slagheart / Grudgebearer / Ravelbone / Nightfell /
   Gravemourn fight must never latch, forge-strike, wire-connect, stamp or
   sling off a tornado tick. Count them; the count is zero.
5. `engine_ab` on every pairing that does not include duskreave: identical.

## STAGE 4 — IT EATS PROJECTILES.

Each step, every entry in `m.shots` whose owner is the foe (`shot.own` is the
side string `"a"`/`"b"`) and whose position is inside the band is removed, with
a small fx at the point it vanished. Fires in 9–10 matchups of 30 and is busy
only against the bows (v62 §2). **Nothing else changes.** Do not let the eaten
shot deal damage, feed the pool, or count as a hit.

**GATE 4.** Duskreave vs each bow, 20 seeds: shots eaten > 0; Duskreave vs
each greatsword and warhammer: shots eaten === 0 exactly. `engine_ab` on
every other pairing identical.

## STAGE 5 — ART, SOUND, BEAT.

**Art — RICK SENT A REFERENCE, 2026-09-02:** `06-docs/v63/ref-vortex.mp4`
(0.8s, 1280×720) and `ref-vortex-frame.png`. What is in it, so it can be
built without the video: a **neon-purple cel-shaded funnel**, narrow at the
floor and widening upward, made of **stacked glowing bands** — magenta cores
with lilac-white rims — that tilt and slide against each other as it turns;
**a large bright ring** floating around the top like a halo, wider than the
funnel; **ragged dark debris** (near-black shards) orbiting between the
bands; and at the floor a **hard horizontal glow line** with a bright
magenta pool where the funnel touches down. Starfield behind it. **Hard
edges, high contrast, no soft particle smoke** — it is drawn, not simulated.
Arcs of electricity (Rick's §1: "crackling with electricity") between the
bands and jumping to a caught ball on every tick.

Build it in `drawUltUnder` (the pool and the funnel behind the balls) and
`drawUltOver` (the halo ring, the front bands, the arcs). Film before tuning.

**Sound — Rick has no preference (2026-09-02). Render a spread, as v43 did:**
three casts × three holds × two tick voices, in one sheet, and ask him. A
starting register: cast = rising wind into a peak; hold = continuous wind with
crackle; tick = a short dry zap. Do not ship the first one built.

**GATE 5.** Rick has seen the strip and the sound sheet. `ult_camera_probe` /
`ult_bloom_probe` pass as for every relic.

## STAGE 6 — THE REAL PRICE.

`ult_price.py` on the built relic against every other, ≥ 34 seeds. Compare to
the model: **+59.2 under today's rule, +40.5 under the window** (v63). Write
the gap into `duskreave-build-v63.md` with its cause — crit and Sunder push
it up; Aegis, the drag, real cast timing and hit-stop pacing all move it in
ways the model did not. **Do not smooth it over and do not retune to hit the
model's number** — the number was a tier, not a target, and Rick accepted the
tier.

---

# 3. WHAT IS RICK'S AND ALREADY GIVEN — DO NOT RE-ASK

The cell, the mechanic, the names, the card line, the blade, the tick rate,
the base tick, the width, the height, the duration, ticks-apply-curse,
keep-at-+59, and the curse-rule ruling. **Sound is open and he has asked to see
a spread; the silhouette and the tornado's look are Code's to draft against
the reference and film for him.**

---

# 4. WHAT TO WRITE

`06-docs/v63/duskreave-build-v63.md` as you go — the gates, the numbers, the
films. Update `CLAIMS.md` to BUILDING when you start and SHIPPED when it is in
a link. Update CLAUDE.md §0.

---

# Open decisions

1. **THE DRAG'S STRENGTH AND THE TICK'S OWN STOP** — Code's, filmed, then
   Rick's eye. §2 stage 3.
2. **START POINT AND DIRECTION OF THE SWEEP** — Code's, filmed. §2 stage 2.
3. **THE SOUND** — a rendered spread, then Rick. §2 stage 5.
4. **WHICH CURSE RULE IS IN THE LINK WHEN THIS SHIPS** — depends on Gloamwire's
   timing; §1. Either is accepted; gate 6 prices the one that is there.

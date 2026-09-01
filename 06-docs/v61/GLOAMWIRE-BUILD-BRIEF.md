# GLOAMWIRE / CROSSWEAVE — BUILD BRIEF, v61

**Design: `06-docs/v61/gloamwire-design-v61.md`. Lab: `tools/net_lab.py`.**
Read the design doc first — every number here was measured there and this
document does not re-argue any of them.

**FOUR STAGES, WITH A GATE BETWEEN EACH.** Stop at a gate that fails and say so;
do not carry a broken stage forward. Each stage is a separable commit and a
separate `02-chain/` link.

```
stage 1   sc-gloamwire.html    the relic. blade + curse. ULT STUBBED at 1e9
stage 2   sc-volley.html       the triple shot and the fan. NO STRAND
stage 3   sc-crossweave.html   the strand, the shove, the magazine
stage 4   sc-gloam-art.html    art, sound, the director's beat
```

---

# STAGE 0 — BEFORE YOU START

- **The base is `02-chain/sc-breach.html`** — 29 relics, and the last link.
  If Bloodmirror or Ravelbone have landed since, chain from the newest link and
  say which in the header. `chain_audit.py --builder gloamwire_build.py`
  after every carry (CLAUDE.md §4.10 — it defaults to `twinshade_build.py`).
- **On Windows the interpreter is `python` or `py`.** Every `python3` in
  `06-docs/` is a record of a Linux container, not an instruction.
- **The runtime is pinned** (`playwright==1.62.0` -> Chromium 151). The design
  doc was measured on Chromium 141 from Cowork and says so. **Every number in it
  is subject to re-measurement on the pin**, and stage 1's gate is where that
  happens.

---

# STAGE 1 — THE RELIC, WITH NO ULTIMATE

Add Gloamwire to `WEAPONS`. Physical stats are the bow's, copied off Ironhail,
Farwarden, Aureole, Vinesower and Marrowdraw — **all five carry the `shot` block
byte for byte and the TYPE owns it** (asserted in `net_lab` [0]). The school owns
Curse and the violet.

```js
{ id:"gloamwire", name:"Gloamwire", aff:"umbral", shape:"bow",
  blades:[0], reach:54, width:9, artW:44, dmg:9.2, spin:2.8,
  mode:"ranged", mass:1.6,
  shot:{ cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0,
         tip:"Fires along its facing · shots can be clanked" },
  onHit:{ curse:1 },
  /* STUBBED. `charge:1e9` and not an omitted `ult`: the object is read by
     verify, tip_audit, the scrunch panel and half of tools/, and a relic with
     no `ult` at all is a shape none of them have ever been handed. Same "OFF"
     shroudmaul_build used in its stage 2. */
  ult:{ name:"Crossweave", charge:1e9, kind:"net", tip:"—" },
  blurb:"<placeholder — Rick's>" },
```

`dmg 9.2` is a **PLACEHOLDER** (CLAUDE.md §4.9 — tuned numbers live in the
builder, never in the HTML). It is the design's prediction, not its answer.

### GATE 1 — and it is the one that ports the whole design onto the pin

1. `engine_ab.py` — must be clean at the new relic count (29 -> 30 relics is
   3480 pairings if the chain is at 29; report the count you actually get).
2. `verify.py` — Gloamwire inside the 30-70% band **with its ultimate stubbed**.
   Expect it very low: the design measured **2%** without Crossweave. **A relic
   that fails the band with its ult off is NOT a stage-1 failure** — say the
   number and carry on. This gate is about the engine, not the balance.
3. **THE PORTED CONTROL.** Run `net_lab.py --stage 1` on the pin. It reproduces
   the design doc's §2 pool table on Chromium 151. **Gate: the umbral-bow row
   comes back within 6 of pool 54.2 and within 2s of a 13.1s third stack.** If
   it does not, the design's central claim — that a bow fills the curse memory
   fastest in the school — did not survive the runtime, and **stop here**: what
   would be refuted is the cell's identity, not a tuning number.

---

# STAGE 2 — THE VOLLEY AND THE FAN. NO LIGHTNING YET.

Rick, §1: *"purple bow gains a triple shot"* … *"can we also give the ult
increased fire rate?"*

### 2a. `fireUlt` gains `kind:"net"`

```js
if (u.kind === "net"){
  f.ultNet = { t: 0, left: u.volleys };
  this.ultFx.life = u.volleys * f.w.shot.cadence * u.cadMul + 0.6;
}
```

**A MAGAZINE AND NOT A CLOCK.** `left` counts down per VOLLEY and the window
ends when it reaches zero. This is the decision that makes the fire rate
affordable (design §5): the payload is invariant across cadence and only the
delivery compresses. **Do not add a `dur`** — a duration and a count together is
two ways to end one window and the second one to fire is a silent behaviour
nobody wrote down. It still needs the two guards every other window has: end it
if `!f.alive || !foe.alive || this.over`.

### 2b. `spawnShot` fires three, and only on the ordinary path

`spawnShot(f, angle)` **already takes an angle** — the volley is three calls,
no new projectile path, and every existing call site is byte-identical.

```js
const n = u.n;                                  // 3
for (let k = 0; k < n; k++){
  const off = k - (n - 1) / 2;                  // -1, 0, +1
  spawnShot(f, f.theta + off * u.spread);       // spread 0.90 rad, 52 deg
  // then on the shot just pushed: dmgMul = u.dmgMul, volley = id, idx = k
}
```

**`angle !== undefined` MUST fall through to the ordinary single shot.** An
explicit angle is some other mechanic asking for one shot and must stay one
shot. This is `_gs_patch`'s lesson one object class along.

### 2c. `tickFire`'s cadence gate

The multiplier is already there and it is gated on **`f.ultBal`**, which is the
BALLISTA window:

```js
const cm = f.ultBal && f.w.ult.cadMul !== undefined ? f.w.ult.cadMul : 1;
```

Widen the gate to `(f.ultBal || f.ultNet)`. **Do not fake `ultBal`** — it starts
`tickBallista`'s clock and Marrowdraw's bolt upgrades.

Keep `=== undefined` and never `|| 1` (CLAUDE.md §4.3): a sweep must be able to
set `cadMul` to 0.

### GATE 2

1. `engine_ab` clean; `chain_audit --builder gloamwire_build.py` clean.
2. **THE CAP, ASSERTED AND NOT ASSUMED.** `CONFIG.shot.maxLive` is 64 and
   `spawnShot` SHIFTS the oldest off the front at the cap. Nine times an
   ordinary bow's load goes past it in principle. **The lab measured 0.0
   evictions at up to 205 arrows a fight — assert it stays 0** and print the
   count. A nonzero eviction count means the cap is deleting shots this build
   thinks it bought, and every number after it is a number about the cap.
3. Volleys a fight ~36.6 at `cadMul 0.5`, magazine 24 (design §5).
4. **A FILMSTRIP BEFORE ANY TUNING** (CLAUDE.md §4.0 — the most expensive
   mistake v43 made). Crossweave is entirely a picture. Thirty seconds of clip
   on placeholder numbers costs four minutes; thirty thousand fights do not
   answer whether a fan of three reads as a fan of three at phone size.

---

# STAGE 3 — THE STRAND, THE SHOVE, AND THE MAGAZINE

Rick, §1: *"each arrow connected by a string of purple lightning. Enemies hit by
an arrow take extra damage. enemies hit by only the lightning take no damage but
take extra knockback. Enemies hit by both take both"*

### 3a. `tickNet`, and WHERE IT GOES IS LOAD-BEARING

**The strand test runs BEFORE `tickShots` moves and resolves the arrows.**

If it runs after, an arrow that connected this frame has already been spliced
out of `this.shots`, its strands are gone with it, and **"hit by both" is
unreachable** — the third of Rick's three cases would silently never fire and
nothing in any probe would show it. Running first costs one step of lag
(1/120 s) and makes both outcomes reachable on the same frame.

Put it beside the other window tickers, before `tickShots`:

```
this.tickWinnow(dt); this.tickSling(dt); this.tickDeadfall(dt);
this.tickGrasp(dt);  this.tickBreach(dt); this.tickBallista(dt);
this.tickNet(dt);        // <- here
...
this.tickShots(dt);
```

### 3b. The strand itself

- A strand exists **between ADJACENT live arrows of one volley** — `idx` and
  `idx + 1`. Two strands on a volley of three. A dead arrow breaks its links and
  does not re-form them.
- Hit test: point-to-segment distance from the foe's centre to the segment,
  against `R + u.strandW`. `strandW 90`, so reach 124 against the arrow's 58.
- **ONE HIT PER STRAND PER VOLLEY.** A line sweeping across a ball overlaps for
  many frames; without a latch the strand is a blender. Latch per strand, not
  per volley — the two strands of one volley are two separate events.
- **NO DAMAGE, NO `onHit`, NO `pushCurse`, NO `apply`.** Rick's rule, verbatim:
  the lightning alone is knockback and nothing else. This is Grasp's precedent —
  a payload that deliberately touches nothing but position.
- The shove is along **the volley's travel**, not away from the archer:
  `foe.v += (arrow.v / |arrow.v|) * u.strandKnock`, `strandKnock 260`.

### 3c. The magazine decrements per volley

`u.volleys` = 24. One decrement per VOLLEY, in `spawnShot`, not per arrow.
At `cadMul 0.5` that is 24 x 0.34 x 0.5 = **4.1 seconds**.

### 3d. NOTHING CHANGES IN `resolveHit`, AND THAT IS THE INTERESTING PART

Crossweave's arrows carry `dmgMul 1.4` — real blows at 1.4x the blade — and
`resolveHit` already does the rest: `foe.pushCurse(dmgBase, n)` where `dmgBase`
is post-crit, post-jitter, pre-echo. So the ultimate raises the curse pool
**40.8 against 33.8 stubbed**, with no new code.

> **This amends v49 §5b rather than breaking it.** That section proved an umbral
> ultimate cannot ADD to a top-K pool — measured on Dirge and Eclipse, which
> applied Curse from an `apply` field with no blow behind it. Crossweave adds to
> the pool by *landing a bigger blow than the blade*, which is the one route
> v49 never tested. **Do not "fix" this. It is the design.** And do not add an
> `apply:{curse:n}` to the ult — that is exactly the dead clause v49 measured at
> +0.0, and `Fighter.apply` already refuses it (a curse stack with no memory
> behind it refreshes the clock and adds nothing).

### GATE 3

1. `engine_ab` clean. `verify.py` — Gloamwire inside 30-70%.
2. **THE FOUR OUTCOMES MUST SUM TO THE VOLLEY COUNT.** both + arrow-only +
   lightning-only + miss == volleys, to the unit. The lab leaked ~4% here on its
   first pass — volleys still in the air when the match ended were never
   retired. Retire them at the end rather than dropping them.
3. **THE GEOMETRY CONTROLS, both of which must come back at a KNOWN value:**
   - at `strandW 0`, lightning-only < 3% (a strand thinner than its arrows is
     inside them — algebra, not balance)
   - at a reach past the arena diagonal (520x800 -> 953), miss == 0%
   - **at `strandKnock 0` the win rate must be IDENTICAL to the no-strand arm to
     the digit.** A strand that records a classification and shoves nothing
     cannot change a fight. If it does, the strand test is touching state it
     should not.
4. **ARROW-ONLY WILL BE 1-6% AND THAT IS CORRECT.** At `strandW > shot.r` a ball
   an arrow touches is necessarily inside the segment's reach, so arrow-only is
   zero by construction; what survives is entirely volleys whose other arrow
   died first. **Do not tune it up.** Rick chose this regime knowing it.
5. Expect, at the shipped sheet: ~9.9 arrow hits and ~22.3 shoves a fight,
   pool 40.8, and Gloamwire at ~51%.
6. **SWEEP `dmg`.** 9.2 is the placeholder. `gloamwire_sweep.py`, on the pin.

---

# STAGE 4 — ART, SOUND, AND THE DIRECTOR

**None of this is specified and all of it is Rick's** (CLAUDE.md §3 rule 2 — the
ult animations and the ult sound are two of his seven). Do not invent it; offer
a spread. What the measurement can say:

- **The strand's thickness is balance-free.** Arrow contacts sit at 7.0-7.5 a
  fight across a doubling of `strandW` (design §4.2). So the bar can be drawn at
  whatever width reads on a phone and the sweep will not care. **This is the
  rare case where the artist has a free hand and should be told so.**
- **The bloom.** Read CLAUDE.md §4.1b-1d before drawing a bright violet bar 24
  times in 4.1 seconds. `adapt: 50` normalises the bloom against the frame's own
  mean, so a pass that raises the mean DAMPS the bloom; alpha is invisible to it
  and AREA is not. Measure the art and the post chain separately —
  `ult_bloom_probe.py` for the caster's disc, `harrow_bloom_probe.py` for a
  full-frame wash. Crossweave is a full-frame candidate: 72 arrows and 48 strand
  segments inside four seconds.
- **The sound is a real problem and it needs a decision.** ~120 events in a
  four-second window at 5.9 volleys a second. `_burst` does not loop its 0.6s
  noise buffer, and `_tone` ends on an exponential ramp over its whole length so
  **a held note does not exist in this toolkit** (CLAUDE.md §4.5) — anything that
  must last is re-struck. A per-arrow voice will be mud. Render in an
  `OfflineAudioContext` and measure it; a broken sound is invisible to every
  other tool here (§4.4).
- **THE BEAT.** CLAUDE.md §3 rule 3. Crossweave's best moment is a volley that
  lands both — an arrow number and a ball thrown sideways on the same frame —
  and `cinePlan` has no idea what a strand is. **File the beat by hand** or the
  director will score four seconds of the loudest thing in the game as empty air.
  Five relics have already had to.

---

# WHAT NOT TO DO

1. **Do not give Crossweave an `apply:{curse:n}`.** v49 measured that clause at
   +0.0 and `Fighter.apply` derives curse's stack count from the pool, so it
   refreshes a clock and adds nothing. The ultimate feeds the pool through its
   arrows or not at all.
2. **Do not run the strand test after `tickShots`.** §3a. It silently deletes
   one of Rick's three cases.
3. **Do not use `f.ultBal` as the cadence gate.** §2c.
4. **Do not tune arrow-only upward.** Gate 3 item 4.
5. **Do not read the design doc's win rates as shipped numbers.** Chromium 141,
   not the pin. The levels ported once (the 40.5% floor against v57's 40.0%) and
   that is evidence, not a guarantee.
6. **Do not write tuned numbers into the HTML.** CLAUDE.md §4.9.

---

# Open decisions — for Rick, not for the builder

1. **THE CARD COPY.** The tip budget is 40 characters (`verify.py`).
   *"24 volleys of 3 strung arrows; the strand shoves"* is 48 and does not fit.
   Rick writes this line; he has not been offered a spread.
2. **THE BLURB.** Not written. Every other relic has one in his register.
3. **THE ART, THE ANIMATION AND THE SOUND.** Stage 4. Three of his seven things,
   none of them asked yet.
4. **`dmg 9.2` ON THE PIN.** It is a prediction from Chromium 141 and the
   sweep may move it. If it moves far, §6 of the design doc is the table that
   says what else could give instead — the magazine size or the fire rate.
5. **THE 2% FLOOR.** Gloamwire wins 2% of its fights with Crossweave stubbed —
   the sharpest ultimate-dependence on the roster. Rick chose it deliberately
   (design §6) and it is worth one line on the card rather than a discovery in
   six versions' time.

# DAWNBRINGER / DAYBREAK, THE CIRCLE — BUILD BRIEF (v99). Rick's redesign of the sanctified greatsword's ultimate.

**Cowork, 2026-09-27. DESIGNED. Build from this and
`dawnbringer-daybreak-circle-design-v99.md`; do not design (rule 0). Rick's
open decisions are design §6 — the card, the strength, the colour; the build
starts on the numbers as priced and his rulings swap in as one number each.
Check CLAIMS.md first.**

## 0. THE RELIC

> The cast puts the sun in the blade. The next blow that lands breaks the
> dawn where it lands: a circle of sunlight spreads from that point and stays
> for eight seconds. A foe in the sunlight is smitten and burns.

```
the cell     sanctified x greatsword     DAWNBRINGER / DAYBREAK (names kept)
the card     "The next blow breaks the dawn where it lands; foes in the sunlight burn"   71
the blade    10.4, unchanged (design §3: the circle prices where the line priced)
the charge   16 on the lab's clock -> the engine's equivalent, 14 as measured for this fighter (the batch ruling)
the arming   cast -> the first blow Dawnbringer LANDS; no time limit; the charge is spent at the cast
the sun      anchored at the blow's hit point (hx, hy); r = 200 * min(1, t/2); life 8s from the contact
the feed     a foe inside (dist < r + ballR): smite +1 and hurt 2, every 0.5s, on the window tickers' clock
the caster   nothing (the heal is Rick's flag, +17, not taken)
re-cast      a cast while the sun is up re-arms; the next landed blow breaks a NEW dawn, the old sets in 0.3s
the end      t >= 8, or Dawnbringer's death; a foe's death leaves the sun up until its clock
```

Priced (design §3, Chromium 141, `sc-corollary-c14`, 1320 fights pooled):
A 19.1% → SHIP (the sparks) 60.7% → the line 52.6% → **the sun 52.7%** at
10.4; 9.8 ticks, 19.5 damage a cast, the foe inside 56% of the sun's life,
3.2 suns a fight, the blade waiting a mean 3.0s for its blow. Slope ~2.9 a
blade unit; tick 3 is +10.

## 1. IN THE ENGINE

- **Retire the line.** `kind:"dawn"`, `f.ultDawn`, `dawnTally`, `tickDawn`,
  `drawDawn` and the eight-step voices (v97 stages 1 and 3) come out as whole
  spans; the builder asserts no `ultDawn` and no `kind:"dawn"` survive.
  `sc-daybreak-fx` stays in the chain as a link that does not ship (v97 §5).
- **The block:** `ult:{ name:"Daybreak", charge:<engine>, kind:"sunrise",
  dur:8, grow:2, r:200, tick:0.5, tickDmg:2, smite:1, card:<71> }`. Tuned
  numbers live in `sunrise_build.py`, never in the HTML (§4.9).
- **Cast** (`fireUlt`): `f.ultSun = { armed:true, x:0, y:0, t:0, cd:0 }`;
  nothing resolves; the generic ultFx cast record as before (draws nothing).
- **The break** (`resolveHit`, the landed-blow path, after `self.hits++`):
  if `self.ultSun && self.ultSun.armed` → `armed=false, x=hx, y=hy, t=0,
  cd=0`, the break beat and voice (§3). The lab anchored at the FOE'S CENTRE;
  the hit point sits on the rim (median 39 from centre, v88 §6c). The probe
  reports the inside share both ways so the difference is a number, not a
  guess; if it moves the relic more than a point the design is told.
- **`tickSun`** beside the window tickers, on their clock (frozen through a
  hit stop): advance `t`; set at `t >= dur` or the caster's death; inside test
  against `r(t) + ballR`; the 0.5s cooldown runs through the whole life and
  fires on the first inside frame it is clear (the lab's cadence, v97's
  reading 1). `apply`'s source is the side letter (reading 2). A tick files
  no beat except the tick that KILLS, which files its own fatal `hit` beat
  with `sun:true` (reading 3; what `tickDawn` did).
- **Beats (rule 3):** the BREAK files one beat at the hit point so the
  director can cut to it — the same kind and fields the cast beat carries,
  `sun:true`; whether the director films it is the director's tuning.
- **Presentation state** (write-only, nothing the sim reads): `f.sunFade`,
  `f.sunLitFade`, the last tick's time per fighter for the shell flash, the
  rim-cross time. Hung off the FIGHTER, never `m.ultFx` (open item 25).

## 2. STAGES

**0 — control on 151.** `ult_overlay.py --game <tip> --relic dawnbringer
--mech overlays/daybreak_circle.js --arms C,D,E --P rMax=200 growT=2
--seeds 20` and `--mech overlays/dawn.js --arms A,SHIP,B`, both blocks
(seed0 2207, 2317), on the chain tip — with the tip's Dawnbringer being the
LINE, arm SHIP there is the line and not the sparks: run SHIP on
`sc-corollary-c14` for the sparks, as v97 did. Every gate below reads
against this run, never against §3's 141 decimals.

**1 — the mechanic** (`sunrise_build.py --stage 1`): the line out, the sun
in. Gate (`sunrise_probe.py`, Dawnbringer on both sides, ≥ 396 fights):
~3.2 suns a fight and ≥ 0.95 breaks a cast; ~9.8 ticks and ~19.5 damage a
cast; the foe inside ~56% (centre-anchored) with the hit-point figure beside
it; the arming wait ~3.0s mean, its p90 printed; every tick's damage went
through `hurt` (ward first); the killing tick has its fatal beat and no other
tick has one; one break beat per break; **a control: a sun of r 0 must deal
0 and price at arm A.** `engine_ab` tip → stage 1, the 33 others, n 8, all
identical. Relic at 10.4 within the batch's tier of stage 0's arm D.
Grow 2s → the rim's speed 100 px/s asserted from the block.

**2 — the blade.** Confirm 10.4 wide on 151 (10.4 / 11.2). It stays unless
the stage-1 relic sits outside the tier; then the design is told, not the
number moved.

**3 — picture, voice, beat** (`--stage 3`), design §4.1 and §4.2 as written;
the two picks that are Code's are named there. Gates, in this order:

*Legibility first — each able to fail, measured as v88 §6c did (mean |dL|
over the mark's own footprint from two frames differing only in the mark;
540x960, chain on AND off; a runic foe, the white Aureole, Grudgebearer):*
- the wash: mean luma inside the sun minus the bare floor **≥ +0.15** at the
  hold (the line measured +0.085 and failed Rick's eye);
- the rim: band luma ≥ 0.50 and the inside/outside step across it ≥ 0.12 at
  every angle not clipped by a wall;
- the rays: visible as marks (footprint |dL| ≥ 0.05) and not as a disc;
- the tick: floats pushed == ticks and tick voices called == ticks, on the
  tick's own frame, counted at the call (v88 [12]'s shape); a foe outside
  gets no float, no voice, no flash (a control that fails if a tick leaks);
- the number's footprint legibility ≥ the echo's number on the same three
  foes;
- the break flash gone by 0.3s (frames counted);
- the armed edge-light present on every armed frame and on no other;
- **and the filmstrip** (`ult_filmstrip.py` or its dawn-shaped sibling):
  armed / the break / +0.5s / +2s / +5s / sunset, one sheet, in
  `05-reference/v99/`. Rick sees the sheet with the clip.

*Then the bloom, the old gates:* arena-mean lift ≤ +0.02 with the sun fully
up (180 frames, six foes, both sides, the v97 method); any ball's disc
≤ 0.90 on every frame including the white Aureole standing ON the core,
and unchanged by the wash (max disc change 0.00, as the line achieved);
wash and rim luma equal with the chain off. The break flash is the one mark
allowed to raise a disc, to 0.90, for 0.3s. Fails → the core's area first
(r 14 → 10), then the flash's radius; the wash and rim alphas are the design.

*Then the usual:* `engine_ab` ALL 34 WITH Dawnbringer, n 6, identical
(picture, voice, beat move no fight); the probe's stage-3 checks (voices
render audibly ALONE through the shipped chain, the armed hum stops on the
break frame, one bell per break, one sunset per clock end and none on a
death); `render_ab` — the default pairs identical, and a control inside a
sun that prints 0/N identical; `shell_identity` 200/200; `chain_audit
--builder sunrise_build.py` relic and tip, and `corollary_build.py` /
`morningstar`'s inserts surviving on the tip; `tip_audit` 1; `verify --n 40`
with Dawnbringer in band.

**4 — the clip, and the sheet.** A `_sun_pick.py` on the whole sentence: a
short arming, the break in frame, the foe crossing the rim at least twice,
a clock sunset. Filmed with the director on, 540 wide, to
`07-shorts/v99/daybreak-sun.mp4`. **The clip is watched with the card
hidden** — that is Rick's gate, the one no tool runs: pass = he can say what
it does. The pointer moves when he has nothing to overrule.

## 3. NOT TO RE-BUY (measured; the design's §3 has the table)
- A sun that grows for the whole window is the line again (43%). 2s, then up.
- A sun that follows the foe is +8.5 and removes the counterplay. Anchored.
- r 300 is the sparks' parity and does not read as a circle in a 520 hall.
- tick 3 at r 200 is 62.7%: Rick's one-number lift if he wants it.
- White is what Rick called dull. Amber wash, gold rim, core white at the
  centre only.
- A wash at alpha 0.10 in the world pass passed every bloom gate and failed
  the only gate that mattered. Legibility numbers are gated BEFORE the bloom's.

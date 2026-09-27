# v93 — BRIARWAND / BLOOM, BUILD. IN PROGRESS — stages 0-3 built and gated; the blade (stage 5) is being measured and is LOWER than priced (the lab under-fired the fan). Claude Code on yert.

Input: `BRIARWAND-BUILD-BRIEF.md` + `verdant-staff-design-v93.md`. Builder `tools/briarwand_build.py` (on `tools/staffkit.py`), probe `tools/briarwand_probe.py`, picker `tools/_briarwand_pick.py`. Runs in `runs/build/`. Rick, 2026-09-27: "go ahead with the rest" / "build them all"; the staff reach stays 54 ("staff reach is fine").

```
sc-ironfall-fx.html    the base: the staff branch's tip (sc-leaf + Culverin 1-6)
  -> sc-briarwand.html     stage 1  the relic, ult stubbed, the bow's arrow     37e9cf2d015f241f
  -> sc-thornburst.html    stage 2  the spell: the fan of three thorns          dec672796c6d1c95
  -> sc-bloom.html         stage 3  the ultimate: the drifting cloud, charge 14  c8401c682d0dc0d9
```

**Two engine names differ from the brief, neither a design choice**: `f.ultBloom` is the Thicket's (Vinesower), so the cloud lives in `f.ultPollen` (the lab's name); `kind:"bloom"` is free and used. The shot block carries `spell:"thornburst"` for the renderer.

## Stage 0 on 151 (`stage0_*`)
arm A 22.0 / S 25.3 / U 54.7% (block 2207; 2427: U 55.8) against the published 21.5 / 23.3 / 53.8 — the mechanism to the digit: 12.47 bites a cast (12.43), foe at 3.66 entangle (3.67), inside 57% (57%).

## Stage 1 — reproduces the lab's arm A TO THE FIGHT (21.97%, all 33 foes identical). engine_ab on the 35: 5950/5950.

## Stage 2 — the fan. **THE LAB UNDER-FIRED IT, AND THE BUILD IS STRONGER THAN PRICED.**
Probe [1]-[5] 5/5: every loose exactly three thorns at θ, θ−0.28, θ+0.28, the cadence exact, 27.2 blows a fight. engine_ab 5950/5950. But on the lab's own seeds the built spell reads **35.5%** against the lab's **25.3%** (29.4 blows a fight against 27.3). The cause is the LAB: `overlays/staff_verdant.js` added the two side thorns only after finding the middle one still alive after its first step (`fresh()`), so every fan whose middle thorn died at a wall on the step it left was ONE thorn. `overlays/staff_verdant_fullfan.js` (the lab with the full fan, a measurement, not a design) reads **35.8%**, 29.5 blows — the build to within noise. So the design's "the fan is the bow's equal" was priced on a fan missing ~22% of its side thorns; the build is §1 as written ("not one thorn but a FAN of three") and the blade pays for the difference at stage 5. **Worth checking in Cipher and Nightglass**, whose spells also change what happens at a wall and were tagged by the same `fresh()`.

## Stage 3 — Bloom. Probe 12/12 (`stage3_probe.txt`, 140 fights, both sides)
The cloud moves by exactly min(dist, 90·dt) a step, inside the inset (349,634 steps, 0 outside); the foe inside 53% of the window; 11.7 bites a cast, never under 0.4s apart; the foe at 3.63 entangle on a window frame; 409 ult beats for 409 casts, a hit beat at every bitten cast's first bite, 16 killing bites with 16 fatal beats; the render path called (thorns, cloud). engine_ab 5950/5950. **80% of thorns end on a wall**, not at their range — the design pictures them simply falling.
**Charge 14 is the lab's 16** on its seeds: 3.06 casts a fight against 3.10 (15: 2.81, 16: 2.62); the relic reads 63.0% there against the lab's 54.7% — the full fan.
Filmed (first cut): `07-shorts/v93/bloom-first-cut.mp4` (briarwand vs ravelbone, seed 4469, from 30.7s); strip `05-reference/v93/bloom-first-cut-strip.png`.

## Stage 5 — the blade, being measured
Coarse, both sides, 700 fights a point: 14 → 40.7%, 15 → 50.7%, 16 → 54.7%, 17 → 60.7%. The wide measurement (14.75-15.5, two blocks, 1050 a point) was running when this was written: `stage5_d*`. Expect ~15, against the design's 16.5.

## Next
Stage 5's link (the blade), stage 6 (picture, voices — Rick's "you pick i overrule"), then Cipher, Watchlight, Crozier, Bloodwick, Nightglass.

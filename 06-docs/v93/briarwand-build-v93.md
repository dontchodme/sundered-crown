# v93 — BRIARWAND / BLOOM, BUILD. STAGES 0-6 BUILT AND GATED on the staff branch (`sc-bloom-fx`); blade 15.25, measured; the clip is with Rick. Claude Code on yert.

Input: `BRIARWAND-BUILD-BRIEF.md` + `verdant-staff-design-v93.md`. Builder `tools/briarwand_build.py` (on `tools/staffkit.py`), probe `tools/briarwand_probe.py`, picker `tools/_briarwand_pick.py`. Runs in `runs/build/`. Rick, 2026-09-27: "go ahead with the rest" / "build them all"; the staff reach stays 54 ("staff reach is fine").

```
sc-ironfall-fx.html    the base: the staff branch's tip (sc-leaf + Culverin 1-6)
  -> sc-briarwand.html     stage 1  the relic, ult stubbed, the bow's arrow     37e9cf2d015f241f
  -> sc-thornburst.html    stage 2  the spell: the fan of three thorns          dec672796c6d1c95
  -> sc-bloom.html         stage 3  the ultimate: the drifting cloud, charge 14  c8401c682d0dc0d9
  -> sc-bloom-blade.html   stage 5  the blade, 17 -> 15.25                      1aba6df7ffb187f0
  -> sc-bloom-fx.html      stage 6  picture, voices                             e233738512c800aa
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

## Stage 5 — the blade, 15.25, MEASURED (`stage5_d*`)
Both sides, two seed blocks, 2100 fights a point, no bisection: 14.75 → 45.7% (44.2/47.2), 15.0 → 48.5% (48.6/48.4), **15.25 → 50.1% (51.1/49.0)**, 15.5 → 51.8% (51.0/52.7). 1.25 under the design's 16.5 because the lab under-fired the fan (stage 2). engine_ab on the 35 others 5950/5950. **verify --n 40 at the tip (`sc-bloom-fx`, engine-identical): 11/13, both reds the clock bands** (Lightkeeper/Farwarden 101.8s, the known four; overall mean 60.1s against the stale 28-54 band); Briarwand **48.7%**, every relic 30-70% (Heartwood 33.1 .. Gloamwire 64.0, spread 30.9pp — Gloamwire's carry, §0, not this build); "both sides can win every matchup" passes.

## Stage 6 — picture and voices (Rick's "you pick i overrule")
Voices off `tools/briarwand_voice_lab.py`, two rounds (`stage6_voice_lab*.txt`): cast EXHALE, the cloud's rustle LEAVES2 re-struck every 0.10s (round 1's 0.25s strikes all pulsed by 33 dB+ — nothing here holds, so a sustain is overlapping strikes), bite SNAP pitched +5.8 semitones over four stacks, close FADE. The verdant staff head is "C" (the open flower — BLOOM comes off a flower). The cloud is DRAWN (no fx.js field: the one `ultFx` slot is erased by the opponent's cast): it thins over 0.5s where it stood, pollen rises off it, the head glows, petals open for 0.4s. **Gates:** engine_ab 6300/6300 over all 36 WITH Briarwand; render_ab 24/24 others identical + Briarwand's control differs; shipped voices 4/4 inside the renderer's floor; probe 12/12; insert audit 26/26; shell_identity 200/200. **Clip:** `07-shorts/v93/bloom-fx.mp4` (briarwand vs ravelbone, seed 4469, the window) — **nobody has watched it.**

## Next
Rick's eye on the clip. The staff branch still waits on the carry onto the batch line before `GAME` moves.

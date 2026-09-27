# v95 — CROZIER / RADIANCE, BUILD. STAGES 1-6 BUILT AND GATED on the staff branch (`sc-crozier-fx`); blade 14.5 → 12.75, measured; the clip is with Rick. Claude Code on yert.

Input: `CROZIER-BUILD-BRIEF.md` + `sanctified-staff-design-v95.md` (Cowork). Builder `tools/crozier_build.py` (on `tools/staffkit.py`, whose `fnum` now writes a JS boolean for `pierce:true`), probe `tools/crozier_probe.py`, voices `tools/crozier_voice_lab.py`, picker `tools/_crozier_pick.py`. Runs in `runs/build/`. Rick: "build them all".

```
sc-watchlight-fx.html        the base: the staff branch's tip (Culverin, Briarwand, Cipher, Watchlight)
  -> sc-crozier.html           stage 1  the relic, ult stubbed, the bow's arrow, smite 1   879a921a136b7513
  -> sc-lance.html             stage 2  LANCE: the pierce                               ec101f4238af499d
  -> sc-radiance.html          stage 3  RADIANCE: the growth, charge 14                 de6acf841ccf3bff
  -> sc-radiance-blade.html    stage 5  the blade, 14.5 -> 12.75                        df225eea20509dfd
  -> sc-crozier-fx.html        stage 6  picture, voices                                 c0a79c415d28f973
```

Engine names are free: `f.ultRadiance`, `kind:"radiance"`, the shot's `pierce` and `grow`.

## Stage 0 on 151 — the lab reproduces (`stage0_*`)
A 25.8 / S 18.5 / Z 57.4% (block 2207; 2427: 23.3 / 19.4 / 53.5) against the design's 28.2 / 18.2 / 52.1: 2.47 lance hits a cast (2.46) on the spell, 11.9 grown and 3.2 lance hits a cast (11.8, 3.2) on the whole relic.

## Stage 1 — arm A to the decimal (25.8%, 17.3 blows a fight). engine_ab 7030/7030 on the 38.

## Stage 2 — the pierce is the engine's, and the lab's was a fake
§5: "the blade-segment loop is skipped for a shot with `pierce` ... the ball test is unchanged". The lab could not change the engine, so it showed it a shot of r 1, armed so no engine test reached it, and ran its own ball test after the step — and it tagged the lance one step late (`fresh()`), so on its first step a lance was an ordinary arrow. **A lance loosed point-blank into a blade was batted down in the lab and goes through in the build.** On the lab's field the built spell reads **24.4%** against arm S's 18.5%; **`crozier_probe --labtag` emulates the lab's lance on the build — one step late, r 1 to the engine, its own ball test — and reads 18.5%: arm S exactly.** engine_ab 7030/7030.

## Stage 3 — Radiance. Probe 10/10, both sides, every foe (`stage3_probe.txt`)
**No lance is ever clanked** — and the check could fail: 6,867 lance-frames stood inside a foe blade's parry reach. A grown lance is **exactly** on the ramp at every step it runs (177,147 lance-steps, worst deviation 0); a lance grows iff loosed in the window; every grown landing of 20+ files a crit beat (785 of 785); an ult beat a cast. On the lab's field: **64.5%** against arm Z's 57.4%, and the lab emulated reads 59.4% — the rest is the engine's longer window (13.5 lances grown a cast against 11.9). **Charge 14 is the lab's 16** for this fighter: 2.72 casts a fight against 2.77. engine_ab 7030/7030.
**The probe was wrong three times before the build was**: it compared the ramp on FROZEN steps (the match clock runs through a hit stop, `tickShots` does not, so the lance catches up the step after — the same rule the design writes); it called 19 lances "clanked" that **Duskreave's Scour ate** (`scourEat`, the tornado's own count moved on the same step); and it counted a crit-less beat that was **Bulwarden's reflect** landing the killing blow on Crozier from inside the lance's own `resolveHit`.

## Stage 5 — the blade, 12.75, MEASURED (`stage5_*`)
The coarse pass (304 a point) read 11 39.5, 12 40.1, 13 48.0, 14 60.9 — six points low at 13 against the wide row. Wide, both sides, 1520 fights a seed block: 12.0 43.2%, 12.25 46.1%, 12.5 47.5% (three blocks), **12.75 50.3% (three blocks: 46.7 / 54.1 / 50.0 — the third settled a swing larger than the step)**, 13.0 54.3%, 13.25 54.5%, 13.5 55.7%. The honest precision is 12.5-13.0. **The control**: the stage-5 link with no `--set` reads 50.0% on block 8111 — the measured row to the decimal. Probe 10/10.

## Stage 6 — picture and voices (Rick's "you pick i overrule")
Voices (`stage6_voice_lab*.txt`, four rounds: round 1 picked a 12.5 kHz hiss for "pitched high"; round 2's chord gains were written as `k * [...]`, which the level match cannot see, so it rescaled only a breath layer; round 3's pierce rule compared whole-sound spectra, which a 0.2s ring owns): the lance's release **NEEDLE** (a 5.2 kHz tick and a 3.1 kHz sine, 30 ms), the pierce **RING** (the tick and two glassy sines), cast **CHOIR** (a C-major chord of noise bands swelling into pitch), a grown landing's **WARM** bloom (12.9 dB quieter at k 0.2 than at 1), close **FALL** (the chord falling away). The sanctified head stays **A** (the crook with its bead). A lance passing through a blade flicks white where it crossed and rings; **the shaft is drawn at its own hit radius, in the crook's gilt under `source-over`**, because sanctified's `glow` is #FFFFFF and layers under `lighter` add toward it — **§4.1b/c's gates are asserted by the builder on the drawing: peak alpha 0.55, bloom 1.3 r, no white**; a thin halo on the crook through the window and the bead's flare at the cast; motes stream off a grown shaft.
**Gates:** probe 10/10; shipped voices 5/5 inside the renderer's floor; render_ab 24/24 others identical + Crozier's control differs 7/10; shell_identity 185/185; insert audit 26/26. **Clip:** `07-shorts/v95/radiance-window.mp4` (crozier vs widowmaker, seed 4435 — a greatsword, as the brief asks: 4 grown landings and 4 lances through its blade) — nobody has watched it.

## Still running when this was written
`runs/build/stage5_engine_ab38.txt`, `runs/build/stage6_engine_ab39.txt` (all 39 WITH Crozier), `runs/build/stage5_verify.txt`.

## Open
Rick's eye on the clip. Then Bloodwick and Nightglass — check each lab for the one-step-late `fresh()` tagging.

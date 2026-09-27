# v94 — CIPHER / CONVERGENCE, BUILD. STAGES 1-6 BUILT on the staff branch (`sc-cipher-fx`); blade 8.875, measured; THREE GATES STILL RUNNING when this was written (below). Claude Code on yert.

Input: `CIPHER-BUILD-BRIEF.md` + `runic-staff-design-v94.md` (Cowork). Builder `tools/cipher_build.py` (on `tools/staffkit.py`), probe `tools/cipher_probe.py`, voices `tools/cipher_voice_lab.py`, picker `tools/_cipher_pick.py`. Runs in `runs/build/`. Rick: "build them all".

```
sc-bloom-fx.html          the base: the staff branch's tip (Culverin 1-6, Briarwand 1-6)
  -> sc-cipher.html          stage 1  the relic, ult stubbed, the bow's arrow   fe264f85368ff051
  -> sc-glyph.html           stage 2  GLYPH: the wall-stop                      46209ad84caa4fe4
  -> sc-converge.html        stage 3  CONVERGENCE: the recall, charge 14        e2a20d3193becca7
  -> sc-converge-blade.html  stage 5  the blade, 11 -> 8.875                    0a998604c54bc7bd
  -> sc-cipher-fx.html       stage 6  picture, voices                           7cf7d7330f7b1128
```

## Stage 0 on 151 — the lab reproduces: A 9.8 / S 30.5 / Y 51.5% (block 2207; 2427: 10.2 / 28.3 / 50.3).

## Stage 1 — arm A to the fight on the lab's field (9.8%, 21.9 blows). engine_ab 6300/6300 on the 36.

## Stage 2 — THE BUILD IS THE DESIGN AS DECLARED, AND THE LAB LOST A QUARTER OF ITS SIGILS
§5 and brief §1: "`spawnShot` sets `bounce 1`". The lab set it from `fresh()`, AFTER the step a bolt was loosed on — and `tickFire` runs before `tickShots`, so a bolt loosed INTO a wall met it untagged and died. The build tags at spawn: 7.3 of 29.9 sigils a cast-equivalent are born that way, and the spell reads **45.0%** on the lab's field against arm S's 30.5%. **Put the lab's tagging back (`cipher_probe --labtag`) and the build IS the lab: 30.5% and 25.47 sigils a lab cast against 30.5% and 25.50.** engine_ab 6300/6300.

## Stage 3 — Convergence. Probe 12/12 (the build), both sides
Hanging sigils leave in laid order 0.25s apart; in-window sigils 0.5s after they land; no flown rune re-forms; an ult beat a cast; no cast ever lands on a live window. On the lab's field the build reads 69.4% against arm Y's 51.5%, and BOTH halves are measured: **the lab at the engine's window** (8s on a clock that stops through hit stop = 9.78 lab-seconds, 18% of a window's steps frozen) reads 56.8%, 6.45 launched, 6.82 blows, 1.96 hanging — and the build with the lab's tagging reads **55.5%, 6.43, 6.77, 1.96**. The rest is the spawn tag. **Charge 14 measured for this fighter**: 12.7% of its steps frozen, 16 × 0.873 = 13.97; casts 3.14 a fight against the lab's 3.11-3.20. The window keeps 8s on the engine clock, as the four batch builds did.

## Stage 5 — the blade, 8.875, MEASURED (`stage5_*`)
Coarse (288 a point) 7 → 36.5, 8 → 47.9, 9 → 55.6, 10 → 63.5, 11 → 74.3% — and the coarse pass was ~6 points high at 8. Wide, both sides, two blocks, 1440 a row: 8.0 41.5, 8.25 43.2, 8.5 47.2, 8.75 47.1, **8.875 49.2 (46.9/51.4)**, 9.0 52.0, 9.25 53.3, 9.5 57.3, 9.75 61.2%. The honest precision is 8.75-9.0. **The control:** the stage-5 link with no `--set` reads 46.9% on block 2207 — the measured row to the decimal. engine_ab 6300/6300 on the 36. Probe 12/12.

## Stage 6 — picture and voices (Rick's "you pick i overrule")
Voices (`stage6_voice_lab*.txt`, two rounds): cast INHALE (an inhale into an E6 chime, v75's register), wall-stop STONE (replaces the shared "wall" for a glyph the wall STOPS; +5.2 semitones over six hanging), leave PLUCK (least like the tap), hex snap GLINT (pitched by count), close STAGGER — the chime reversed as three narrow-band swells, because one swell from −80 dB is heard for only 0.2s. The runic head stays "A" (the open ring, Rick's ref 3) and lights through the window; a stopping bolt flashes; each rune FLARES off its own fuse against the window clock; flown runes trail with a 0.2s sight-line; a rune's blow flares on the foe and the hex tag prints the count; rune motes drift off the walls (drawn, no fx.js field). **Gates in:** probe 12/12; shipped voices 5/5 inside the renderer's floor; render_ab 24/24 others identical + Cipher's control differs 9/10; shell_identity 195/195; insert audit 27/27; stage 6 rebuilds byte-identical. **Clip:** `07-shorts/v94/convergence-window.mp4` (cipher vs farwarden, seed 4452, 8 hanging at the cast) — nobody has watched it.

## STILL RUNNING when this was committed — read the files before quoting a green
`runs/build/stage3_engine_ab36.txt` (sc-glyph -> sc-converge, the 36 others), `runs/build/stage6_engine_ab37.txt` (all 37 WITH Cipher — the proof stage 6 is presentation), `runs/build/stage5_verify.txt` (verify --n 40).

## Open
CLAIMS row and CLAUDE.md §0 not yet updated for this relic. Rick's eye on the clip. Then Watchlight, Crozier, Bloodwick, Nightglass — **check each lab for the same `fresh()` tagging artifact** (Briarwand's fan and Cipher's wall-stop both had it).

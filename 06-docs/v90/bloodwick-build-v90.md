# v90 — BLOODWICK / GYRE, BUILD. STAGES 1-6 BUILT AND GATED on the staff branch (`sc-bloodwick-fx`); blade 8.5 → 7.75, measured; the clip is with Rick. Claude Code on yert.

Input: `BLOODWICK-BUILD-BRIEF.md` + `bloodsworn-staff-design-v90.md` (Cowork). Builder `tools/bloodwick_build.py`, probe `tools/bloodwick_probe.py`, voices `tools/bloodwick_voice_lab.py`, picker `tools/_bloodwick_pick.py`. Runs in `runs/build/`. Rick: "build them all".

```
sc-crozier-fx.html          the base: the staff branch's tip (Culverin, Briarwand, Cipher, Watchlight, Crozier)
  -> sc-bloodwick.html        stage 1  the relic, ult stubbed, the bow's arrow, hemorrhage 2   b76b5d375b3fd9de
  -> sc-seeker.html           stage 2  BLOODSEEKER: the bend                                 fc7c3b177f922b6c
  -> sc-orbit.html            stage 3  the orbit alone (arm V), charge 14                    92abe347a8d40613
  -> sc-gyre.html             stage 4  the lunge: GYRE whole (arm U)                         9482a033f4806c20
  -> sc-gyre-blade.html       stage 5  the blade, 8.5 -> 7.75                                7b60c0c677b54f1f
  -> sc-bloodwick-fx.html     stage 6  picture, voices                                       69b76d868126982a
```

Engine names are free: `f.ultGyre`, `kind:"gyre"`, an orbiter's `orb`.

## Stage 0 on 151 — the lab reproduces (`stage0_*`)
A 4.1 / S 15.5 / V 15.6 / U 45.2% (block 2207; 2427: 3.2 / 15.6 / 13.5 / 48.3) against the design's 5.0 / 15.9 / — / 50.5: U lunges 7.0 a cast, lands 5.3 blows a window, the foe at 3.2 hemorrhage — the mechanism to the decimal.

## Stages 1-4 on the lab's field (block 2207)
Stage 1 **4.1% = arm A** (18.0 blows). Stage 2 16.8% against arm S's 15.5%, and **with the lab's one-step-late bend put back (`--labtag`) 15.5% — arm S exactly**. Stage 3 (the orbit alone) 14.5% against arm V's 15.6% — the moat is worth nothing, as the design said. Stage 4 **58.0%** against arm U's 45.2% (53.9% with the lab's tagging; the rest is the engine's longer window and the lab testing "fewer than six in orbit" before dropping globules that had just died, so it refused joins the build allows: 17.3 orbited a cast against 11.4). engine_ab 7410/7410 at every stage.

## Stage 4 — probe 12/12, both sides, every foe (`stage4_probe.txt`)
The bend never exceeds home·dt (821,802 shot-steps); every orbiter within 1 px of the lane on every window step (126,369 orbiter-steps); orbiters are clanked (the counterplay) and land; the close looses every orbiter at the spell's speed and bend; a lunge sends every orbiter at 520, homing 8, and never fires with the foe outside 230; an ult beat a cast and one a lunge. The probe was wrong once: a globule loosed with the foe already close joins the orbit and is LUNGED on its first step, so it arrives with the lunge's numbers.

## FOR RICK — THE LUNGE IS NOT THE PICTURE THE DESIGN DRAWS
**91% of lunges carry ONE globule** (1134 of 1247 over 60 fights; two: 88, three: 20, four: 4, five: 1, six: never). §5's rule fires whenever the foe is inside 230 and any orbiter exists, and the foe almost always is — so the orbit fills only when the foe stays out for about two seconds, and "they all lunge at once" / "six of them at 4 rad/s is the tell" happen rarely. The lab's rule is the same, so the BALANCE is as priced. Built as written (rule 0): a minimum count before a lunge, or firing on the foe ENTERING 230, would be a design decision. The clip below is one of the rare windows where the orbit fills (a four-globule lunge, 1.9s with three or more circling).

## Stage 5 — the blade, 7.75, MEASURED (`stage5_*`)
Coarse (312 a point) 7.0 39.7, 7.5 52.2, 8.0 55.1, 8.5 61.9 — high again. Wide, both sides, 1560 fights a seed block: 7.0 39.6%, 7.25 44.9%, 7.5 48.8%, **7.75 50.3% (three blocks: 47.6 / 51.5 / 51.8)**, 8.0 52.1% (three blocks), 8.25 56.0%. The honest precision is 7.5-8.0. **The control**: the stage-5 link with no `--set` reads 51.8% on block 8111 — the measured row. Ladder at 7.75 (block 2207): flail 60, scythe 57, warhammer 54, staff 52, bow 48, twinblade 44, **greatsword 26** (the design's ~29).

## Stage 6 — picture and voices (Rick's "you pick i overrule")
Voices (`stage6_voice_lab*.txt`, two rounds; round 1's hisses ran 0.22-0.25s against the design's 0.35): cast **FLARE** (a lowpass whump into a highpassed hiss, 0.31s), a drop taking its slot **TICK**, the lunge **CRACK** (pitched a semitone a globule lunged, the least like the hit voice that follows it), close **SHORT** (the cast's hiss stopped at 0.14s). The bloodsworn head stays **A** (the claw and blood-glass orb with its flame). The globule is a fat drop with a dark rim and its tail (the bend's own positions; an orbiter's along its lane); the lane, the flame at twice its size through the window, and red motes drifting in along the lane are drawn off the fighter. **The lunge's shake and ring SCALE with how many lunged** — 3 for one globule up to the design's 8 for a full orbit — because 91% are one globule and eight of shake each would be a quake seven times a window: Code's reading, Rick's to overrule.
**Gates:** probe 12/12; shipped voices 4/4 inside the renderer's floor; render_ab 24/24 others identical + Bloodwick's control differs 9/10; shell_identity 200/200; insert audit 28/28. **Clip:** `07-shorts/v90/gyre-window.mp4` (bloodwick vs emberedge, seed 4486: a four-globule lunge and a full six-drop orbit) — nobody has watched it.

## Still running when this was written
`runs/build/stage5_verify.txt`, `runs/build/stage5_engine_ab39.txt`, `runs/build/stage6_engine_ab40.txt` (all 40 WITH Bloodwick).

## Open
Rick's eye on the clip, and on the lunge (above). Then Nightglass, the row's last.

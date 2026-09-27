# v90 — BLOODWICK / GYRE, BUILD. IN PROGRESS — stages 1-4 built and gated (`sc-gyre`); the blade measured, not yet written; stage 6 not started. Claude Code on yert.

Input: `BLOODWICK-BUILD-BRIEF.md` + `bloodsworn-staff-design-v90.md` (Cowork). Builder `tools/bloodwick_build.py`, probe `tools/bloodwick_probe.py`. Runs in `runs/build/`.

```
sc-crozier-fx -> sc-bloodwick (1) -> sc-seeker (2, the bend) -> sc-orbit (3, the orbit alone) -> sc-gyre (4, the lunge)
```

- **Stage 0 on 151:** A 4.1 / S 15.5 / V 15.6 / U 45.2% (block 2207; 2427: 3.2 / 15.6 / 13.5 / 48.3); U lunges 7.0 a cast, 5.3 blows a window, hemorrhage 3.2 — the design's mechanism to the decimal.
- **On the lab's field:** stage 1 4.1% = arm A; stage 2 16.8% against S 15.5%, and with the lab's one-step-late bend put back (`--labtag`) 15.5% exactly; stage 3 14.5% against V 15.6%; stage 4 58.0% against U 45.2% (53.9% with the lab's tagging; the rest the engine's longer window and the lab testing "fewer than six in orbit" before dropping globules that had just died, so it refused joins the build allows — 17.3 orbited a cast against 11.4).
- **Probe 12/12 at stage 4** (both sides, every foe): the bend never exceeds home·dt (821,802 shot-steps); every orbiter within 1 px of the lane (126,369 orbiter-steps); orbiters clanked and landing; the close and the lunge exact; an ult beat a cast and one a lunge.
- **FOR RICK — THE LUNGE IS NOT THE PICTURE THE DESIGN DRAWS.** 91% of lunges carry ONE globule (1134 of 1247 over 60 fights; 2: 88, 3: 20, 4: 4, 5: 1, six: never). The rule fires whenever the foe is inside 230 and any orbiter exists, and the foe almost always is, so the orbit only fills when the foe stays out for ~2s. The lab's rule is the same, so the balance is as priced; "they all lunge at once" and "six of them ... is the tell" rarely happen on screen. Built as written (rule 0) — a change (a minimum count, or firing on the foe ENTERING 230) is a design decision.
- **Stage 5, measured wide (both sides, two blocks, 1560 a row), not yet written into a link:** 7.0 39.6%, 7.25 44.9%, 7.5 48.8%, **7.75 49.6%**, 8.0 52.0%, 8.25 56.0% — the crossing is 7.75-8.0 against the design's 8.5.
- **Still running at this commit:** engine_ab at stages 1-4 over the 39 others (`runs/build/stage*_engine_ab39.txt`).
- **Left:** stage 5's link, stage 6 (picture, voices), verify, the clip.

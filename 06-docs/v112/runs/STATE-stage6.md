# HEARTWOOD / ROOTFAST -- STAGE 6 (picture + voice) INTEGRATION -- STATE
2026-09-30 start: no STATE-stage6.md existed; stage 0-5 STATE.md says fix round DONE (builder 4550a53a2b5ac4bf, probe 9634f7a6c2d42cb1, doc 03a17a4e4769251d).
Base for stage 6 = links/sc-heartwood-b11.html (aff84a04b303a402 expected).
## steps
- 1. read: labs' rows (voice 4c38682da549a943 2 rows, picture 184f5cb47c0bb5e7 9 rows), voice report, picture STATE; precedents ironwood gen_s6, thornwake S6 scans, bindweed probe [10]/[11], _spellbreaker_pick.
- 2. s6/gen_s6.py: anchors once, none nested, none share a line (no merge); picture alone = 4ce2e98655411557 (lab stamp), voice alone = 6a19b58add3cf38e (voice lab e2e), both orders ceba5e801f4cf91b.
  backups: s6/heartwood_build_4550a53a.py, s6/heartwood_probe_9634f7a6.py. S6 WRITTEN into tools/heartwood_build.py (--write).
- DECISION: film the fx link (precedent v111: the fx link filmed, orchestrator re-films after carry). On b11 the root's shoots are inert (Tendril's picture not on tendril-t3: hexagon shows) and SPECS.heartwood still fires at the cast until fx_remove: DECLARE.
- 3. BUILDER wired (tools/heartwood_build.py): docstring readings 14-22, S6 table, stage-6 scan (s6_static_checks: call allowlist
  S6_CALL_ANY + S6_CALL_ROW, write allowlist, declared locals, no index/destructuring writes, 2 CONFIG reads; s6_output_checks:
  fx.js untouched, arms before rune-crack, freeze art gone, voice in rootBlow after the return, each call/method once), STAGE_OUT 6
  sc-heartwood-b11-fx, --stage 6 (goes on stage 5 once). builder sha 4896a2dac7af7acb (may move with docstring edits: re-run rebuild6 + negatives at the end).
- 4. tools/builder_negatives6.py: 49/49 refuse for reason + control ceba5e80 (runs/builder_negatives6.txt); old negatives 26/26 (anchor now first of 2).
  tools/rebuild6.sh -> runs/rebuild6.txt: all 5 links identical from bare base + 7 refusals.
  LINK: links/sc-heartwood-b11-fx.html ceba5e801f4cf91b (runs/build_stage6.txt).
  tools/carry_compose6.py -> runs/carry_compose6.txt: carry on tendril-fx (c4aacc10, shoots drawn), spellbreaker-fxout (fc6895cc), aureole-fxout (b7071c0a);
  compose with thornwake 1-6 and goreshard 1,2,5,6 both orders: same lines.
- NEXT: probe [9] voice [10] picture + mutants; then gates (engine_ab 38, probe, render_ab, chain_audit, tip_audit), pick, clip, doc.
- 5. mutants (tools/mutants6.py -> mut/mut-s6-*.html, runs/mutants6_shas.txt): close-voice d198e081, kill-voice ea92e645, grove-sim 823be275, grove-rng 16def6eb.
  probe patched (s6/patch_probe6.py): [9] voice, [10] picture (+ drawn subset), --stage 6. backup of the fix round's probe: s6/heartwood_probe_9634f7a6.py
- 6. GATE engine_ab b11 -> fx, 38 ids n6: 4218/4218 identical (runs/stage6_engine_ab38.txt); control mut-s6-grove-sim 4 ids: 13/36 differ, FAIL as it must (runs/stage6_engine_ab_control.txt)
- running: probe smoke --stage 6 --seeds 1 on fx (tmp/smoke6_fx.txt) -- slow (>600 s; the drawn subset is every fight at seeds 1)
- 7. tools/_heartwood_pick.py written (repo). pick (runs/stage6_pick.txt): 31 foes x 4 seeds, 3 windows show everything; best Heartwood v Lightkeeper 112312,
  cast 76.46, window 10.28 match-s, 10 roots (4 holds, 6 re-roots), 10 voiced, 10 tags, held 88.7%, clock close, no foe cast/card/kill.
  CLIP RUNNING (runs/clip6.sh, bg bq9sfrccv): --at 75.26 --window 13.28 --end-at-window -> 07-shorts/v112/rootfast-window.mp4 (gitignored), log runs/stage6_clip_log.txt
- 8. chain_audit fx/fx: ALL 20 SURVIVE rc0 (runs/stage6_chain_audit.txt); control tip=b11: 11 LOST (the S6 rows) rc1; control tip=base: all 20 LOST rc1.
- 9. CLIP DONE: 07-shorts/v112/rootfast-window.mp4 3.24 MB, 894 frames 14.9s 540x960 60fps, AAC 48k stereo, mean -21.1 dB max -1.2 dB
  (runs/stage6_clip_log.txt, stage6_clip_probe.txt, stage6_clip_aac.txt); tile clip/tile5.png (frames 84/240/420/600/828): banner+greening+old SPECS
  leaf-fall at the cast, green leaf blade + held foe with HEXAGON (base) + ENTANGLE 4 tag, resting pale leaf sword after the close.
- doc draft s6/sec6.md (§6 stage 6, §6a gates @@GATES6@@, §7 clip @@CLIP6@@); plan: old §6 What is left -> §8 (refs updated).
- builder/probe/pick §7 refs renamed -> §6 (sed). builder sha to re-check at the end.
- 10. render_ab b11->fx 4 other pairs: 24/24 identical (runs/stage6_render_ab.txt); control heartwood:spellbreaker:2207 + paradox:heartwood:25064: 4/12 differ (t=22,31), rc1.
  tip_audit fx == b11 but the file name; b11 == the stage-5 run (runs/stage6_tip_audit_{fx,b11}.txt).
- probe smoke still running (drawn subset slow: ~20+ min for 74 drawn fights).
- 11. probe smoke (seeds 1, drawn, the probe BEFORE the docstring-only §7->§6 rename): 10/10, 67,136 drawn frames (62,605 picture up, 9,510 in a stop)
  -> runs/stage6_probe/probe_fx_drawn_smoke_prefinal.txt. Final probe sha 2269d88a1c668b32.
  RUNNING: q12 (bg bu6asgiy3; log runs/q12.log): probe fx stage 6 --no-draw 444, b11 stage 5, 4 s6 mutants (--no-draw), 16 old controls stage 5.
  RUNNING: drawn subset again with the final probe (bg) -> runs/stage6_probe/probe_fx_drawn.txt
  mutants6.py fixed: s6-kill-voice now MOVES the voice (d9474157ea33675a); first version (added) failed [9] only too.
- doc: s6/sec6.md, gates6.md, clip6.md, sec8.md, doc6_apply.py (needs s6/fill.json with HEAD_PROBE, BUILDER, PROBE, PROBE_* keys)
- 12. FINAL BUILDER 04e7ce55b18a1102: rebuild6 all 5 identical + 7 refusals; negatives 26/26 and 49/49 + controls; chain_audit 20/20 rc0,
  controls 11 LOST / 20 LOST rc1 (re-run on the final builder). carry_compose6 (final builder): carries on tendril-fx, spellbreaker-fxout,
  aureole-fxout AND sc-thornwake-b26.5-fx (Thornwake CARRIED onto 02-chain at 10:23; 42 relics; 5abbc99c -> 54ad747c; shoots drawn);
  goreshard compose both orders same lines; thornwake compose now impossible in scratch (its names on 02-chain) -> earlier result recorded.
- 13. probe fx --stage 6 --no-draw 444: 10/10 (runs/stage6_probe/probe_fx.txt), [1]-[8] numbers = b11's; probe b11 --stage 5 8/8, output byte-identical to the fix round's.
  builder final 04e7ce55b18a1102 (rebuild6/negatives/chain_audit re-run on it; the reading-22 docstring edit was NOT made: builder unchanged).
  tools/mutant_table6.py -> runs/stage6_probe_mutants.txt (after q12). tools/copy_runs6.py written. waiting: q12 mutants, drawn run.
- 14. s6 mutants: close-voice [9] only (1703), kill-voice [9] only (143), grove-sim [10] only (fights change); grove-rng pending; then 16 old controls.
  s6/fill6.py -> s6/fill.json (after mutant_table6 + drawn run); then s6/doc6_apply.py; then tools/copy_runs6.py; then SendUserFile clip; StructuredOutput.
- 15. q12 STOPPED by PID (taskkill /T 22788: its own bash + python 10668 on m1; the orchestrator's engine_ab 17888 untouched) after the 4 s6 mutants,
  to split the 16 old controls: runs/q13.sh lane 1 (m1-m8, now) and lane 2 (m9-m11, x1-x5, after the drawn run). Log in runs/q12.log.
- 16. drawn subset with the FINAL probe 2269d88a: 10/10, 67,136 frames drawn (62,605 picture up, 9,510 in a stop), same numbers as the smoke
  (runs/stage6_probe/probe_fx_drawn.txt). s6 grove-rng [10] only. Waiting: q13 lanes (16 old controls) -> mutant_table6 -> fill6 -> doc6_apply -> copy_runs6.
- 17. mutant_table6: 4/4 stage-6 controls own-check only (voice ones move no fight; picture ones do); 16/16 old controls AS BEFORE (runs/stage6_probe_mutants.txt).
  fill6 -> doc6_apply -> doc written; patch_doc6b (window's hit stops; clip SENT to Rick via SendUserFile), patch_doc6c (carry also on sc-thornwake-fxout:
  5841a505 -> 5cc32354, shoots drawn). copy_runs6 -> 06-docs/v112/runs (450 files, ~1.17 MB of small text/json).
- DONE except the final report. Final: link ceba5e801f4cf91b, builder 04e7ce55b18a1102, probe 2269d88a1c668b32, pick 22a68fef97b35a62.

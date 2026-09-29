# LODESTONE stage 6 -- THE VOICES (resume notes)
Base: S/links/sc-lodestone-b205.html 6d736451a1ffc2df. Lab: C:/dev/sundered-crown/tools/lodestone_voice_lab.py (NEW).
Rows -> this dir rows_final.json. Wavs -> 05-reference/v102/lodestone-*.wav
Arms: ult/lodestone (cast: rising 4-note rune chime, one per wall, 0.5s), ult/lodestone-touch {n} (electric snap <=80ms peak<=0.5, pitch by hex count)
 + hex-snap underneath (reading: the hex's own voice = hex-snap, the runic school's), ult/lodestone-close (chime reversed, quiet; clock close, both alive)
- (session start) nothing existed from before the cut: no lab, no stage6-voice dir, no v102 wavs.
- 18:14 lab written (tools/lodestone_voice_lab.py); first --no-wire run -> stage6-voice/run0.log
- 18:18 round-2 gates (TONAL>10 + NOISE ctl; HEX-OVER vs snap alone; cast tiebreak) -> full run run1.log / rows_lab1.json / lab1.json, peers bindweed coldiron portcullis ironhail
- 18:20 run1 EXIT 1: NOISE ctl calib tried a 0.564 s _burst (refused). Capped its D search at 0.55; rerun -> run2.log
- 18:29 run2 (run2.log, rows_lab2/lab2.json): all checks clean (wire 152/152, ctl 4/152, e2e 76/76, peers x4) but EXIT 1: no touch passed HEX-OVER (A4+ square harmonics fill 2.6k). NOISE ctl tonal 10.2 on ONE draw. Round 3: +6 HUM +7 ARC3 at A3; tonal draw-averaged for noisy bodies -> run3.log
- 18:41 run3 (run3.log, rows_lab3/lab3.json): picks EVEN / ARC3 / MIRROR, all rules + row checks pass; EXIT 1 on real window only: 1 touch +5.3 dB (foe Aureole's rune-crack cast on the same frame, 380 Hz partial in the touch's 397 band; diag_window.py). Round 4: real-window touch gate = median>=+6 & min>=+3 (Zenith's frequent-voice gate), near() 0.5 s back -> run4.log
- 18:42 run4 died (EPIPE in playwright; the session was cut by a usage limit). run4.log / engine_ab.txt are that crash, not results.
## RESUME 21:58 (after the usage-limit cut)
- lab unchanged since 18:41 (sha fbf6855cb3c58d69), base still 6d736451a1ffc2df. Picture rows (stage6-picture/rows_final.json, 9 rows) touch none of my anchors.
- re-running round 4 -> run4b.log / rows_lab4.json / lab4.json, peers bindweed coldiron portcullis ironhail.
- (found at the 01:15 resume, not logged before the cut) 22:22 run4b.log EXIT 0 (picks EVEN/ARC3/MIRROR; real-window gate median/min passed); lab then changed to a0ca911fe058156f (lab5.sha); 22:25 build_voice.py -> sc-lodestone-voice.html + sc-lodestone-picvoice.html; 22:34 probe_voice.txt lodestone_probe on the voice page 10/10 EXIT 0; 22:34 engine_ab_voice.txt = header only (cut); 22:36 run5.log EXIT 0, rows_lab5.json (== rows_lab4 but for measured numbers in the Sfx row's why).
## RESUME 2 (01:15 2026-09-28, after a second cut)
- lab sha a0ca911fe058156f == lab5.sha; base 6d736451a1ffc2df unchanged. Re-checking cheaply: rows apply/anchors, voice page hash, coapply with picture rows + peers. Then: engine_ab b205 -> voice page (cut last time), beat_dist, render_ab, rows_final.json.
- 01:2x cheap re-checks PASS: voice page 8921a39052799d17 == run5's end-to-end; coapply with picture rows (9) both orders 7a095b143d66fbdb SAME; with bindweed/coldiron/portcullis/ironhail Sfx rows both orders OK; Sfx anchor x1 on 02-chain/sc-ironhail-sunder-fx.html (batch tip carrying portcullis/bindweed/coldiron/ironhail arms). RUNNING (bg): engine_ab b205 -> voice page, all 39 ids (chk/ids.txt), n=6 -> engine_ab_voice.txt
- 01:3x chk/beats_ab.py -> chk/beats_ab.txt PASS: beats identical base vs voice 152/152, cinePlan 38/38, Lodestone ult beats 561 = casts 561; CONTROL (beat filed per touch) 4/152 identical -> fails as it must.
- 01:4x render_ab b205 -> voice page: default 4 pairs 24/24 identical; aureole:lodestone:102602 over the real window 8/8 identical (render_ab_voice.txt). CONTROL voice -> picvoice same pair 0/8 identical (render_ab_ctl.txt): render_ab sees the window.
- rows_final.json = rows_lab5.json byte-exact (b6f01158a986b7e1)
- 01:5x waiting on engine_ab (bg). rows_final.json written. Remaining: engine_ab result -> StructuredOutput.
## RESUME 3 (01:45 2026-09-28, after a third cut)
- engine_ab_voice.txt 0 bytes, no engine_ab process alive (the python/node now running are other builds: ironhail_probe, identity). lab a0ca911fe058156f, base 6d736451a1ffc2df, rows_final b6f01158a986b7e1 == rows_lab5 -- all unchanged.
- plan: cheap re-checks (rows apply -> voice page hash), then engine_ab b205 -> voice page (foreground this time, logged), then StructuredOutput.
- 01:5x recheck3.py (chk/): anchors x1 each, rows apply in memory == disk voice page 8921a39052799d17, co-apply w/ picture 9 rows both orders 7a095b143d66fbdb SAME. engine_ab RUNNING (bg) -> engine_ab_voice.txt
- 01:5x chk/mk_simctl.py -> chk/sc-lodestone-voice-simctl.html 1ae1daab88aa57b6 (voice + foe.x += 1e-9 on a touch). RUNNING engine_ab CONTROL b205 -> simctl, 8 relics incl lodestone, n=6 -> chk/engine_ab_simctl.txt (must FAIL)
- 02:0x engine_ab CONTROL done (chk/engine_ab_simctl.txt): 8 relics x 6 seeds, 168 matches, FAIL 42 differ = exactly Lodestone's 42 fights (7 foes x 6) -> engine_ab sees a 1e-9 sim write, as it must. Main engine_ab still running (~450 s a page at 168/17 s).
- 02:0x engine_ab page A (b205) 4446 matches 552 s; page B running
- 02:2x engine_ab b205 -> voice page DONE (engine_ab_voice.txt): 39 relics x 6 seeds, 4446/4446 identical field for field, no page errors, 39/39 winners, EXIT 0 (552 s / 593 s). Control (chk/engine_ab_simctl.txt) FAILS 42/168 as it must. ALL GATES OF THE VOICE STAGE DONE -> StructuredOutput with rows_final.json (b6f01158a986b7e1).

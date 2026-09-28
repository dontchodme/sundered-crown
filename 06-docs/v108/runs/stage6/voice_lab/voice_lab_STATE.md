# IRONHAIL stage 6 -- THE VOICES (resume notes)
Base: S/links/sc-ironhail-sunder.html 1bedab05b9803465. Lab: C:/dev/sundered-crown/tools/ironhail_voice_lab.py (NEW).
Output rows: S/stage6-voice/rows_final.json (label, anchor, mode, code, why). Wavs -> 05-reference/v108/ironhail-*.wav
Arms: ult/ironhail (cast, bellows huff 0.4s), ult/ironhail-land {n} (thud <=0.15s pitched by sunder), ult/ironhail-miss (quieter thud). Close: none.
- (start, session 1) nothing existed from before the cut: no lab, no stage6-voice dir, no v108 wavs.
- (session 2, 16:55) found: tools/ironhail_voice_lab.py 1645 lines, written 14:12 in session 1, NEVER RUN (no 05-reference/v108).
  Read in full: complete (cast 5 cands + 4 ctl + WOOSH/RC-NOW; land 5 + 5 ctl; miss 4 + 3 ctl; sfx row check; wire +
  sim-write control; real window; e2e in a 2nd browser after the 1st closes; peers optional). Anchors each 1x in base.
  NEXT: run it -> run1.log, rows_lab.json, lab.json; fix what breaks; review picks; rows_final.json.
- 17:05 ROUND 1 RUN (round1.log, round1_rows/lab.json, round1_wavs/): fixed a false "already voiced" check (renderer's
  u.w === "ironhail" matched) -> ran. Controls reproduce (v88). WIRE: 148/148 identical, control 2/148, e2e 74/74. EXIT 1:
  CAST: no candidate passes -- every breath registers 0.91-0.99 vs the tornado woosh and 0.82-0.94 vs the loose; two
  overlapping exp-tent sweeps make 2 humps (dips / regrow 11-12 dB). Real window: cast +4.9 dB (< 6).
  LANDING: only 4 DEEP (A1 55-73 Hz) passes (A2 ones 0.82 vs hit, 0.84 vs death). MISS pick 3 DEAD at 51.9 Hz.
  PROBLEM: DEEP/DEAD are inaudible on a phone (culverin v96 round 3 lesson; coldiron v103). -> ROUND 2: PHONE gates
  (culverin's PHONE = TOP high-passed at 200 Hz; HEARD read >= 200 Hz; landing's stepping partial >= 200 Hz over the
  score) + new cast candidates (one-breath M+T geometry, register off the woosh) + A2/A3 landing candidates.
- 17:30 EXPLORED (scratch explore_cast.py / explore_land.py, c1-c4 / l1-l2 json): the cast needs the M+T geometry (swell
  atk .34 + co-peaked short-atk long-decay huff, dur .58 both) = one hump, aud 340-400; lowpass whoomph (150-300 / 400-150)
  + a thin nozzle band (3 kHz q 2, 0.3) -> regs <= .78-.80 (cindercleave nearest), woosh .6. Landing: A2 with the iron
  bar mode at 1.0-1.5 (+5.40 mode) -> hit .68-.76, death .71-.78, phone note +11..+13 dB; DEEP phone note -11.7 (fails).
  PLAN ROUND 2 in the lab: cast 6 WHOOMPH 7 BELLOWS 8 NOZZLE 9 FORGE + ctl 0 RUMBLE; land 6 RING 7 RINGING 8 HEAVY 9 BAR;
  rules: PHONE (culverin), HEARD >= 200 Hz, landing PHONE-PITCH rising + PHONE-NOTE >= +6; cast PHONE >= blow -6; miss
  PHONE >= loose; real-window bands >= 200 Hz.
- 17:50 lab edited for ROUND 2 (docstring THE ROUNDS; cands cast 6-9 + RUMBLE; land 6-9; phone(), phone_note(), heard>=200; gates). Running round2.log with --peer-rows bindweed/coldiron/portcullis.
- 18:20 round 2 first run (round2_full.log): picks WHOOMPH / RINGING / SAME; EXIT 1 only on the real window (one landing +4.9 over 100 ms: Cindercleave's jet 58 ms after). Lab: real window read over 50 ms (TOP window) + 100 ms printed + maskers; peer names fixed. Rerun -> round2b.log / rows_lab3.json.
- 18:45 ROUND 2b (round2b.log, lab3.json, rows_lab3.json) EXIT 0. lab sha16 dea8ca3c48b47807. PICKS cast 6 WHOOMPH, landing
  7 RINGING, miss 1 SAME. rows_final.json = rows_lab3.json byte-exact (sha16 156bffc31af9234a). Real window 50 ms: landings
  min +6.4, misses min +4.4, cast +9.1. coapply_text: voice+picture both orders SAME text (acc953f4bd7bf6b5); peers OK.
  build_combined -> sc-ironhail-voice.html (e0f218411e1cf374 = lab e2e sha), sc-ironhail-picvoice.html. RUNNING engine_ab
  (7 ids, n 30) base vs each -> engine_ab.txt. Then StructuredOutput.
- 18:55 engine_ab 630/630 x2 PASS (engine_ab.txt). Text-only lab edits (fallback count 'on its stage-5 link', 'Rise under 1 ms', why wording) -> final rerun round2c.log / rows_lab4.json -> rows_final.json.
- 19:20 FINAL: round2c.log EXIT 0 (measurements = round2b; text-only comment changes). rows_final.json = rows_lab4.json
  byte-exact (sha16 5d2a679a52632527), lab sha16 c8fc473f2d44444f. voice page a9f7c759c6bcce02 (= lab e2e), picture+voice
  b8ff2014a954be3f (either order). engine_ab_final.txt 630/630 x2 PASS. coapply_text.txt OK. ONLY StructuredOutput remains.

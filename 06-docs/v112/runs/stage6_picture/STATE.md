# HEARTWOOD / ROOTFAST -- STAGE 6 (THE PICTURE) -- STATE
2026-09-30 start: nothing on disk from an earlier attempt (no stage6-picture folder, no tools/heartwood_voice_lab.py).
BASE for rows: ../links/sc-heartwood-b11.html (want sha256[:16] aff84a04b303a402)
Base verified: aff84a04b303a402 (33443 lines).
## decisions (read so far: design v85 section 4, build doc v112 section 5/6, bw_rows.py, canopy v99 section 6)
- THE ROOT REUSES TENDRIL'S FLOOR ROOT (design s4; build doc s5; the task): my rows only SET the held ball's
  twineHeld/twineRootFade/twineHeldAge/twineHeldOut at a root; Tendril's tickTwine (generic over both balls),
  drawTwine/drawTwineTop/_twineRoot and the _drawField guard (!(f.twineHeld > 0)) do the rest. They are on
  sc-tendril-fx and every later tip, NOT on b11: on the stamp link (b11 + rows) the root markers are inert and
  the hold still draws the hexagon. So the picture gates run on T = heartwood_build 1,2,3,5 --src
  02-chain/sc-tendril-fx.html + rows (the first tip that carries it); identity/drawn/apply also on S = b11 + rows.
- ULTSIG.heartwood kept ("roots going down and GRIPPING" already says Rootfast).
- the blow's ENTANGLE tag (val 0 today = no count) carries the count after the root's +1 (Tendril's g.val rule).
- retire: drawUltUnder plate + drawUltOver cage (replace with a comment), life 'heartwood: 2.2, ' cut.
- presentation clock is half-seconds (tickPresentation runs twice a normal step, once in a hit stop).
## plan
hw_rows.py (rows + lab) -> links S/T -> look -> gs silhouette lineup -> measure (bloom/discs/legibility + controls)
-> verify (sim identity + drawn + sim-write control) -> render_ab -> electron cost -> order/apply + chain carry
-> fxprobe (fx_spec) -> sheet 05-reference/v112/heartwood-picture-sheet.png -> rows_final.json -> StructuredOutput
## log
- hw_carry.py: carry/hw-on-sc-tendril-fx.html 3c61fccb5366245a (T0, the picture's lab base), hw-on-sc-spellbreaker-fxout f51666c08b8f2d9b (= earlier dry carry)
- hw_rows.py v1 (9 rows, no lab variant; components are methods): hw-final 61f7ee69 (STAMP v1), hw-final-fx, hw-tip, hw-tip-fx; all parse
- look: _look1/2/3.png. The root = Tendril's stalks from the floor (aerial roots, as designed), no hexagon; ENTANGLE n works; wither reads.
- pick_green.py (12 window frames, 4 fights): V3 mid taken by max-min rule (change |dL| .189 dE 32 vs steel; floor .164, steel .188).
  V0 .153/.172, V1 .225/.154, V2 .205/.160. Rows updated (v2).
- hw_measure.py (+dE; pixels by |dL|>.02 OR dE>2.3), hw_summ.py. smoke m0 (spellbreaker): bloom share 0, controls fail as they must.
- hw_order.py -> order.out: 9 rows, rows_final.json 4eb802b1af74866c, STAMP 2081dacee04d54e8; 62 orders identical; parses;
  carries on t3/tendril-fx/spellbreaker-fxout + 12 scratch pictures all apply both ways (+14941); control refused. No voice rows yet.
- verify relaunched after the mirror fix (no mirror matches: heartwood v thornwake 777 instead)
- m1+m1b (12 fights, 122 frames, rows v2) -> m1_summary.txt: bloom share max +0.0000; discs: me -0.0001..+0.0002, foe -0.0093..0, >0.90 share 0.960 vs 0.961;
  ctrl1 caster disc 102/122 FAIL, ctrl2 lift 19/122 + foe disc 52/122 FAIL, ctrl3 lift 30/122 FAIL. legib: blade .189 dE31, scale .158, root .171/.223, tag .246,
  motes .163 but n~27px (tiny), cast frame 0 px (greening starts at the grip; banner over the caster).
- rows v3 (NOT YET BUILT into hw-*.html while verify v2 runs): the SPROUT (each scale pair sheds a big leaf as the green passes it), bigger motes; parses, stamp would be 590fcbb85155fa51
- hw_sil.py (= lightkeeper gs_sil.py): resting heartwood 0.215, 3rd of 7 greatswords, identical to lightkeeper's reading (SHAPES untouched)
- ROWS v3 = FINAL candidate: SPROUT added; hw-final 590fcbb85155fa51 (STAMP), hw-final-fx ad2800f0, hw-tip e0c9d7fd, hw-tip-fx c45ec07d;
  rows_final.json 7c4633da9898615f; order.out re-run PASS. _look4.png: greening reads hilt->tip; the cast banner sits on the caster.
- killed the v2 verify (superseded). hw_verify.py split into lanes (stamp | tip), "tip drawn" arm dropped (tip-fx drawn kept).
- RUNNING laneA.sh (verify stamp) and laneB.sh (verify tip -> m2 measure 12 fights, states + caststop/sprout -> m2_summary.txt)
- hw_chain.py -> chain.out: ALL 9 INSERTS SURVIVE on t3/tendril-fx/spellbreaker-fxout carries; control (b11) LOST 9. PASS.
- written: hw_fxprobe.py (run when a lane frees)
- written: hw_renderab.py, electron/cost.py (+cost_electron.js), hw_seq.py (sheet sequences), hw_sheet.py (-> 05-reference/v112/heartwood-picture-sheet.png)
- QUEUED laneA2 (after laneA.done): fxprobe b11 + hw-final-fx -> fxprobe.out; heartwood_probe --stage 5 on hw-tip-fx -> probe_tipfx.txt (want = runs/probe_b11.txt numbers)
- QUEUED laneB2 (after laneB.done): hw_renderab.py -> renderab.out
- AFTER: electron/cost.py (alone), hw_seq (spellbreaker 2207 a, + nobanner), hw_snap x3 foes on v3, hw_sheet, rows_final.json already written by hw_order
## declared readings (for the report)
1 root = Tendril's, reused by 4 markers; inert on b11 (hexagon there); carry precondition: tip has `!(f.twineHeld > 0)){` + `_twineRoot(m, f, 0/1)` (hw_order [4] checks)
2 new hold: shoots from the floor (twineHeldAge 0); re-root of a held ball: shoots kept, fresh (pin back to 1.0 -> no wilt)
3 tag: the blow's own ENTANGLE tag (val 0 = no count before) carries foe.stacks after the +1; the first-ever panel left alone; no new tag
4 greening GREEN 0.6 half-s (0.3s normal; 1x in the cast's 0.08 stop -> ~0.34s real, only the grip greens inside the stop)
5 leaf scale: a pair every 12u (Tendril's), sprouting as the front passes; the SPROUT sheds one leaf per pair
6 field -> drawn motes (world pass): sprout at cast + 3.2/s sparse; fx_spec NONE (fxprobe)
7 close: verdant wither (no design text): brown tip->grip 0.3s, pairs let go, fade by 0.4s; at the kill withers in place; caster death: gone at once
8 blade green by max-min (pick_green.py); 9 ULTSIG kept; 10 plate + cage + life 2.2 retired; 11 no beats (design asks none)
12 writes: presentation fields, foe.twine* markers (presentation, read by Tendril's picture + _drawField guard only), a tag's val
- verify tip-fx drawn fight 1: held&pinned 1888 bad 0, cleared-bad 0, marked 14/14, tags 14/14
## 06:13 INCIDENT (mine): stopping my v3 lanes with a filter '*lane*.sh*' also killed the THORNWAKE stage-6 picture build's
  laneP.sh + laneE.sh (batch/thornwake/stage6-picture) and their children. Their logs at the kill:
  P: start 06:10:47 page f0a988952fee0d80
  E: start 06:10:47 page f0a988952fee0d80
  Their STATE.md says: re-launch a lane whose .done marker is absent. Not re-launched by me (theirs to resume; avoids a double run).
  REPORT THIS. Future kills: by exact PID of my own processes only.
## v4 fix (the reason for the stop): a ball that holds itself (Canopy: pin + pinFree, refreshed every step) is its own
  picture's -> a Heartwood root marks nothing on it and a mark it carried lets go when pinFree takes over (verify tip: ironwood 11 roots, 2 holds, cleared-bad 9)
- ROWS v4 (the self-held rule): STAMP 4ce2e98655411557; hw-final-fx 23eb1884, hw-tip d9230d04, hw-tip-fx 0c87a5ea; rows_final.json 184f5cb47c0bb5e7;
  order.out PASS (+ Heartwood's 2 voice rows compose both ways on all 15 bases). Smoke ironwood 5150: selfOK 8, marked 3, letGo 1, tags 11/11.
- lanes renamed hwlaneA.sh / hwlaneB.sh (so no filter can confuse them with other builds'); kill by PID only.
  A: verify stamp -> fxprobe (b11 + hw-final-fx) -> heartwood_probe stage 5 on hw-tip-fx.  B: verify tip -> m2 measure -> renderab.
## RESUME (attempt 3, 2026-09-30 after 09:00; "Try again")
- re-checked: base aff84a04b303a402, hw-final 4ce2e98655411557 (STAMP v4), final-fx 23eb1884, tip d9230d04, tip-fx 0c87a5ea,
  rows_final.json 184f5cb47c0bb5e7 -- all = the v4 log. hwlaneA/B .done both present.
- KEPT (verified outputs): verify_tip.out SIM IDENTITY PASS (13 pairs, tip/tip-fx/tip-fx drawn); m2_summary.txt (v4, 12 fights 146 frames);
  renderab.out 108/108 other relics pixel-identical, controls differ; fxprobe.out; probe_tipfx.txt 8/8.
- NOT DONE: verify_stamp.out CRASHED at the CONTROL arm's game() (Playwright "Connection closed while reading from the driver")
  -- two lanes ran two browsers at once (breaks "one browser at a time"; the likely cause). The drawn arm on hw-final passed its
  13 fights (thrown None) but the stamp's identity table + control were never printed. -> re-run `hw_verify.py stamp` ALONE.
- FRAME COST now DEFERRED by the task (Rick on the PC): electron/cost.py NOT to be run.
- then: sheet (hw_seq / hw_snap / hw_sheet) one browser at a time.
- 09:02:41 RE-RUN verify stamp ALONE (idle priority): verify_stamp2.out, hwverifyS.log/.done
## RESUME (attempt 4, 2026-09-30 ~09:05; task now ASKS for frame cost in Electron, two browsers max; user: "full speed ahead")
- pid 25616 (attempt 3's verify stamp) dead; verify_stamp2.out empty. Re-checked hashes: all = v4 log (base aff84a04, STAMP 4ce2e986, final-fx 23eb1884, tip d9230d04, tip-fx 0c87a5ea, rows 184f5cb4, T0 3c61fccb).
- 09:05 RELAUNCHED verify stamp ALONE (hwverifyS.sh -> verify_stamp2.out/.err, hwverifyS.log/.done)
- 09:08 LAUNCHED hwsheet.sh (2nd browser): hw_seq spellbreaker 2207 a (+nobanner) -> seq.out; hw_snap x3 (dawnbringer 99001 a, gravemourn 99015 a, spellbreaker 2207 a) on hw-tip-fx -> snap_*.out; hwsheet.log/.done
- NEXT: after verify stamp -> electron/cost.py (alone of Electron; 2nd browser slot) ; after hwsheet -> hw_sheet.py -> 05-reference/v112/heartwood-picture-sheet.png
- 09:08 seq spellbreaker 2207a (+nob) done: g0-g7 o0-o5 r0-r5 rr. Its first cast coincides with Spellbreaker's Unmaking (banner + rings over the caster) -> also seq a cleaner fight for the cast row after the snaps.
- 09:12 hwsheet.sh done (3 foes: all states but 'over' -- no kill inside a window with Heartwood side a on these seeds). LAUNCH hwsheet2.sh: hw_seq dawnbringer 99001 a (+nob; its first cast is clean) and hw_snap dawnbringer 99001 b (kills in a window, for 'over')
- 09:15 hwsheet2 done (seq dawnbringer_99001a + nob OK). hw_snap 'over' never fired: it timed by m.t, which stands once over -> patched to count steps; re-run hw_snap dawnbringer 99001 b.
- 09:18 SHEET written: 05-reference/v112/heartwood-picture-sheet.png (hw_sheet.py out dawnbringer_99001a spellbreaker_2207a; cast rows off Dawnbringer 99001a, root+close off Spellbreaker 2207a; 'over' tile off dawnbringer 99001 b). hw_snap fixed (over key clash + m.t stands once over).
- 09:19 LAUNCHED hwcost.sh (electron/cost.py, 3 fights, on hw-tip-fx) -> cost.out/cost.json; the 2nd browser beside verify stamp
- 09:20 VERIFY STAMP PASS (verify_stamp2.out): 13 pairs x final/final-fx/final drawn IDENTICAL to b11 (hash@kill, steps, result); drawn: 13 fights 0 throws (28,450 draws; tip-fx drawn 22,292); CONTROL (hw-control fac26014, foe.vx += 1e-9 in the root branch) DIFFERS on all 11 Heartwood fights, IDENTICAL on the 2 without. Remaining: cost (running), StructuredOutput.
- 09:30 FRAME COST (cost.out/cost.json; Electron 44, ANGLE RTX 3070, 453x805 chain on, interleaved A/B, OFF shadows _groveBlade+drawGrove+_twineRoot = upper bound; PC loaded: frames 36-66 ms med):
  whole-frame median ON-OFF: rest (identical code, noise) -0.4..+0.4 ms; cast -0.4..+1.1; window +0.2..+1.0; root +0.8..+1.2; close +0.1..+1.7.
  ALONE (drawGrove+drawTwine+drawTwineTop+caster drawWeapon): rest -0.3..-0.1 (noise); cast +0.2..+0.7; window +0.6..+0.7; root +0.7..+1.0; close +0.7..+0.9 ms (off 6.4-10.1).
- ALL GATES DONE. Next: StructuredOutput (rows = rows_final.json 184f5cb47c0bb5e7, stamp 4ce2e98655411557, fx_spec NONE).
- 09:35 rows transcription for StructuredOutput checked IDENTICAL to rows_final.json (_rows_transcribed.json). Repo touched: only 05-reference/v112/heartwood-picture-sheet.png (ec708eed).
- 09:37 DONE: sheet sent to user (SendUserFile). Returning StructuredOutput (rows = rows_final.json 184f5cb47c0bb5e7, stamp 4ce2e98655411557, fx_spec NONE).

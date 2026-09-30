# THORNWAKE stage 6 PICTURE state (scratch)
Started 2026-09-30. No earlier attempt on disk (stage6-picture/ absent, no tools/thornwake_voice_lab.py).
Base links/sc-thornwake-b26.5.html (fd5031063ecb6807).
## Done
- (nothing yet) reading design + precedents
## 1 read (no browser yet)
- base sha re-checked fd5031063ecb6807. Read design v84 §4/§5, v113 build doc §0/§5/§6, v99 §6, CLAUDE.md §4.1b-d.
- TEMPLATES: ../../censer/stage6-picture (ce_rows/measure/summ/verify/order/renderab/fxprobe/chain/hammer_sil/snap/look/sheet, idle.py),
  ../../lightkeeper/stage6-picture/electron (cost.py + cost_electron.js frame cost; ident.sh + ident_electron.js shell identity),
  ../../bindweed/stage6-picture/bw_rows.py (Tendril's root shoots: twineHeld / drawTwineTop / guard).
- Tendril's picture is NOT on this base -> the snare shoots are PORTED into my own method (same picture), and the hexagon
  is kept off by an early return inserted BEFORE the guard line (touches no existing line: composes with Tendril's guard on
  the real tip and any other row anchored on it).
- Voice is a separate job (../stage6-voice): not mine. Only the sheet goes into the repo.
## 2 rows v1 (tw_rows.py, 12 rows) built
- names brier* (free on base, tip, staff line). tw-final.html f43871ac81f0c613 (+22012), tw-final-fx.html 6041fa86bbc4269d
  (inlined fx 28fc58641370a1a9 -> 753521f4d9c676d9). node --check ok.
- FINDING for the orchestrator (fx_diag.out): tools/fx_remove.py --relic thornwake REFUSES on the base link itself
  (no rows): difflib aligns the 5-line removal one line early (Vinesower's last line `spawn: 0.85, up: 0 },` == Thornwake's)
  and compares a rotation of the block. --keep-comment passes (leaves the stale FREEZE comment). tw_rows.fx_out computes the
  page fx_remove would write (its spec_block imported read-only == my 331-byte block; multiset-of-lines check).
- NEXT: quick look (snap) on real fights, then measure (bloom/legib), verify, order, fxprobe, renderab, chain, sil, cost.
## 3 look + v2 tangle
- tw_snap.py (states rest/cast/green/plant/bramble/snare/bite/stop/close1/close2/after/brown/over), quickscan.py (per-cast action).
- v1 tangle read as a spoked wheel -> v2: 7 arching canes + offshoots, growth by a clip circle (tw-final dec7e85d657b412a,
  tw-final-fx 656c6ffc232d1f5e). Looked (snaps/_look2.png, _look3.png): tangle reads, shoots clench on the white foe's rim,
  bite thorns flash, blade greens, banner on the caster. Good fights: aureole 4101a c1, gravemourn 99015a c1, grudgebearer 31337b c2.
- NEXT: tw_measure.py (bloom/legib/controls) + tw_summ.py
## 4 m1 (tw_measure on tw-final-fx 656c6ffc, 10 fights, 139 frames; m1_summary.txt)
- bloom share +0.0000 (gate .02); art on discs: foe <= 0.0047 (sanctified .0047, umbral .0036, dwarven .0030, runic .0031), caster .0016
- controls: ctrl2 caster>0.90 92/104 FAIL ok; ctrl3 foe>0.90 35/54 FAIL ok; ctrl1 (0.35, r80) lift only +0.0138 -> did NOT fail the
  lift gate -> ctrl1 now 0.9 at r patchR+R (re-measure in m2).
- legib: tangle .133/.114(stop), plant .095, brown .141, motes .152/.107, root(snare) .192, top .235, bite .257, blade .142/.079(stop), tag .238
  shade .026 -> DROPPED. tw-final a36ab9291af1b552, tw-final-fx 0d801d86ea2cc21f.
- order.out (v2 rows): 12 rows, 62 orders identical, 18 carries clean (t3, tendril-fx, spellbreaker-fxout, aureole-fxout, ... + 9 scratch pictures),
  with Heartwood's 9 picture rows both orders apply+parse but bytes differ (shared anchors, insertion order) -> add multiset check.
- tw_verify.py written (not run). NEXT: look at dark/ordinary foes (TW_HALF=120), then order again, verify, m2, fxprobe, renderab, sil, cost, chain.
## 5 rows v3 (FINAL candidate): canes arch (turn 0.07-0.17/step) instead of looping; shade dropped
- tw-final 65a84cedda239548 (+21259), tw-final-fx f0a988952fee0d80. Looked (_look4/_look5): arching thorned canes, snare shoots
  clench a dark foe, ENTANGLE n counts, blade greens.
- the v2 verify was STOPPED (I rebuilt the pages under it); its partial (aureole, drawn): pic==sim, held==model, hexagon off 19/19,
  control drew 19/19, 43 bites / 1 new tag (the rule updates the blow's own ENTANGLE tag's count instead) -> verify_v2_partial.out
- NEXT: lane A verify on v3; lane B m2 on v3; then order, fxprobe, renderab, sil, cost, ident, engine_ab, chain, sheet.
## 6 m2 on v3 (tw-final-fx f0a988952fee0d80; m2_summary.txt) + control probe
- bloom share +0.0000/-0.0000; floor +0.0000; art on discs foe <= .0047 (sanctified), caster .0014; legib unchanged (tangle .138/.112,
  plant .092, brown .139, motes .158/.120, root .198, top .235, bite .252, blade .142/.079, tag .245).
- ctrl1 as a white disc at 0.9 r114 lifted only +0.012 (the bloom adapts); probe (c1_*.json, 12 frames): the canes stroked WHITE in the
  emissive pass lift +0.0007..+0.0036 (thin); a white lighter WASH r300 at each bramble lifts +0.019..+0.042 (11/12 > .02) -> ctrl1 = wash.
- order.out v3: STAMP 65a84cedda239548, rows_final.json f80fbfe244abacde, 18 carries clean, HW rows both orders (same multiset of lines).
- chain.out: ALL 10 INSERTS SURVIVE on t3 / tendril-fx / spellbreaker-fxout carries; cut tokens gone; spec out; control 10 LOST exit 1.
- written: tw_fxprobe.py, tw_renderab.py, scythe_sil.py, electron/{cost_electron.js, ident_electron.js, ident.sh}. RUNNING lane A verify.
## 7 lanes
- RUNNING: lane A verify (verify.out) and lane B m3 (ctrl1 = wash; m3.json/m3_summary.txt), both on v3 (65a84ced / f0a98895).
- READY: laneP.sh (looks gravemourn c1 + grudgebearer c2, snaps dawn/grave/grudge c2, scythe_sil, fxprobe final+base, renderab)
  and laneE.sh (electron cost, electron ident + control, engine_ab 38 ids n6 + control). Launch each when a lane frees
  (max 2 browsers). Then tw_sheet.py -> 05-reference/v113/thornwake-picture-sheet.png, then StructuredOutput.
  If resumed: re-launch a lane whose .done marker is absent (each step overwrites its own output).
## 8 verify + m3 DONE on v3
- verify.out (verify.sha 65a84ced / f0a98895): SIM IDENTITY PASS 15 fights x (final, final-fx, final-fx drawn) vs base; CONTROL
  (tw-control: foe.vx += 1e-9 in the tag branch) DIFFERS on all 13 Thornwake fights, identical on the 2 without. DRAWN PASS: 22510 draws,
  none thrown, pic==sim, held==model 12726 frames, hexagon off on 147/147 snares (control drew it 147/147), 367 bites 18 tags, invariants
  clean, green cools 0.29-0.575s after a close, brambles gone <=0.29s after the verdict, row unwritten.
- m3 (ctrl1 = wash): share +0.0000; ctrl1 lifts max +0.047, >0.02 on 103/139 -> FAILS as it must. Everything else = m2.
- RUNNING laneP.sh and laneE.sh (launched after verify+m3 ended).
(lanes P and E died silently at 06:10-06:20, bash terminated before the first step finished; free RAM 0.68 GB of 16.7; relaunched)
- fx_diag.out now also: fx_remove --dry REFUSES on sc-spellbreaker-fxout + thornwake 1-5 (the real batch tip) too; the line above the
  block there is Vinesower's `spawn: 0.85, up: 0 },` (and Heartwood's entry below ends with the same line: its own removal will meet it).
## 9 RESUMED 2026-09-30 09:04 (the earlier process exited after lanes P and E finished)
- hashes re-checked: base fd503106, tw-final 65a84ced, tw-final-fx f0a98895, control 79e5f9c2, rows_final.json f80fbfe2.
- lane P done: looks grave/grudge, snaps dawn/grave/grudge c2, sil (thornwake scythe |dL| .164, 4th of 7 scythes), fxprobe
  (slot Thornwake's a median 0.65s of the 8s window, 7.4%; 85% of brambles >80 from the cast point; 35.6% of bramble life after
  the close), renderab (84/84 other-relic frames pixel-identical; controls differ).
- lane E done: electron ident PASS 274/274 (control FAIL 268/274); engine_ab 38 ids n6 PASS 4218/4218; control FAIL 1 differs.
  cost: aureole + gravemourn measured; lastlight 4242 b FAILED silently (empty stderr) -> re-ran alone: OK (electron/cost_ll.out).
- NEXT: re-read rows + docs for the report, run the sheet (tw_sheet.py), final re-checks (order/apply-once/node --check), StructuredOutput.
## 10 sheet built (the only repo write): C:/dev/sundered-crown/05-reference/v113/thornwake-picture-sheet.png (2200x3255),
  from snaps/look_gravemourn*, the three trio fights, sil_final, sheet_header.txt (gate numbers). Looked: reads.
- re-checked: rows() == rows_final.json (12), stamp 65a84cedda239548 in 6 random orders, node --check parses.
- NEXT: StructuredOutput (rows from rows_final.json, fx_spec NONE + retire SPECS.thornwake at the carry).
- 09:15 all gates in hand; writing StructuredOutput from rows_final.json (f80fbfe2), stamp 65a84cedda239548, fx_spec NONE.

# LODESTONE / REBUTTAL stage 6 PICTURE -- state (resume here)
Base: ../links/sc-lodestone-b205.html (6d736451a1ffc2df). Job fresh (nothing on disk before, 18:0x).
Templates: ../../ironhail/stage6-picture (ih_*.py, electron/), ../../coldiron/stage6-picture (ci_*.py).
Plan: ld_rows.py (rows) -> look/snaps -> silhouette lineup (7 hammers) -> measure (bloom/discs/legibility + controls)
-> verify (sim identity + drawn + sim-write control + touch spot/tag/bolt-one-frame) -> verdict frame probe (+ungated control)
-> render_ab -> electron cost -> order/apply/carry test -> fxprobe (fx_spec) -> lodestone_probe on final -> sheet
05-reference/v102/lodestone-picture-sheet.png -> rows_final.json -> StructuredOutput.
Names: lode* (free on base, tendril-fx, watchlight-fx, ci-final, ih-final-fx): tickLode, drawLode, drawLodeTop, _lode*.
Touch found by watching runeTally.touches rise in tickPresentation (no sim write; probe needs no skip).
## Log
- 18:40 ld_rows.py v1 (8 rows + silhouette row). look.py/crop.py/cropfix.py/mont.py snaps. ham_sil.py lineup (453x805, 7 hammers):
  conjured weapon 0.243 head 0.352 (area 2850); SQUARE 0.239/0.317 (area 4361, 1st of row); stone 0.185/0.225; row grudge .126 censer .163 bulw .219 shroud .140 ravel .186 ironwood .211
  -> PICK SIL square (design's first cut). streak lengthened to 0.2s (TRAIL 0.4, TLIFE 0.8), width 20.
- ld_measure.py + ld_summ.py written; m0 (1 fight) bloom share 0.0000; ctrl2 widened to 100u. m1 running (9 fights) on ld-final (402a5a8c9fb58245)
- 19:1x m1 DONE (m1.json; ld_summ): bloom share max +0.0000; ctrl1 caster disc 70/72 FAIL; ctrl2 (100u band) dLift>0.02 11/88 FAIL; ctrl3 (200u flash) 5/88 + foe disc 28/88 FAIL.
  foe disc max |d| 0.096 = the HEX tag text; art only -0.014..+0.017. legib walls .197/.164 motes .258 head .390/.148 flare .161/.078 bolt .297 streak .219/.150 tag .216/.231
- ld_order.py DONE: 9 rows, stamp 402a5a8c9fb58245, rows_final.json 96c55ef0913aa366; carries on tendril-fx, ci-final, ih-final-fx, pc-final + 8 compose205 links. (voice rows not yet on disk)
- renderab DONE: other relics 54/54 identical; controls 0/6 both.
- RUNNING: ld_verify.py (verify.out), ld_fxprobe.py (fxprobe.out). NEXT: ld_verdict.py, electron cost, lodestone_probe on final, sheet.
- 19:5x verify r1 (on 402a..., bar on the presentation clock) PASS 14/14 + control bit; saved verify_r1.out. Bar showed 2 frames on a few touches (a hit stop under it)
  -> BAR MOVED TO THE MATCH CLOCK (q.t0 = this.t; visible while m.t - t0 < 0.0125 && !over: the touch's step + the next).
  fxprobe DONE (fxprobe.out): slot median 0.66s (7.9%), 17/118 opp's cast same step, 36% of walls within 300u, 1034 touches median 263u away, 103 in slot.
  snaps sp/dawn/grave (snap.py), ld_sheet.py written. SILWHY comment filled.
- REBUILT ld-final: stamp b40d52b7561c45f2 (+22788). order.out OK (+ voice rows_lab3.json both orders).
- RUNNING: verify (final bytes) + verdict (ld-final vs ld-ungated). NEXT: measure m2, renderab, lodestone_probe, electron cost, ham_sil -> .out files, snaps, sheet.
## RESUME (21:57, after a usage-limit cut; verify/verdict outputs were empty)
- ld_rows.py rebuilds ld-final == b40d52b7561c45f2; rows_final.json == rows() (9 rows)
- re-running: verify (final bytes) + verdict. Then m2, renderab, probe, electron, ham_sil out, sheet.
- 22:2x verify on final bytes (b40d52b7561c45f2): SIM IDENTITY PASS 14/14 (undrawn + drawn, 28 compares); control bit 11/11 Lodestone fights w/ touch, identical on 3 without; bar exactly 1 frame on every touch both phases (362 touches); spot/walls/tag 0 bad; w never written; nothing thrown.
- verdict: final 24 fights, 12 end lit, panel frames w/ rune 0 of 2352, pix diff 0; last rune 0.375s after kill, panel first 1.075s. CONTROL ld-ungated: 1176 rune frames under the panel (all 12 lit fights, 98 each) -> FAILS as it must.
- RUNNING: qA.sh (renderab, probe_final, sil square/conjured), qB.sh (m2, snaps sp/dawn/grave). NEXT: electron cost, sheet, numbers.
## RESUME 2 (2026-09-28, new process): on disk: verify/verdict/renderab/probe_final(10/10)/m2/snaps/sil/sheet_draft DONE; electron/cost.out FAILED after 1 pairing. Re-checking hashes, then electron cost, engine_ab, watched fight, sheet -> repo, StructuredOutput.
- R2 re-checked: base 6d736451a1ffc2df; ld_rows.rows() rebuilds ld-final == b40d52b7561c45f2 == disk; rows_final.json == rows() (9 rows, file sha16 1ab82ea2383e20de).
- R2 prof/prof.py (Electron, full-lit walls): _lodeWalls 1.1-1.2 ms med, motes 0.1, drawWeapon 8.2-8.4; a per-wall BATCHED rune candidate 1.1 ms (no gain; 462 px differ max 44) -> rows KEPT as they are (stroke count is not the cost).
- R2 RUNNING (bg): engine_ab39.out (b205 -> ld-final, 39 relics, n=6) + electron/cost.out (cost.py re-run; r1 partial kept as cost_r1_partial.out). watch.py written (one fight watched: lodestone v widowmaker 102007 a, 30fps mp4 + grids) -- run it after one of the two finishes (2-browser cap).
## RESUME 3 (2026-09-28 01:45, new process): engine_ab39 and cost r2 were cut off with the process (engine_ab39.out header only; cost.out "FAILED").
- R3 re-checked: base 6d736451a1ffc2df; rows() rebuilds b40d52b7561c45f2 == ld-final on disk; rows_final.json == rows() (9 rows, sha16 1ab82ea2383e20de). verify/verdict/renderab/probe_final(10/10)/m2/order/fxprobe/sil outputs on disk read and OK.
- R3 cost r2 failure = two Electrons on the default userData (another build's Electron was up). cost_electron.js now takes a private userData (mkdtemp sc-ld-el-*) + --outfile (widowmaker's attempt-3 fix); cost.py retries 3x off the outfile. Old output kept as electron/cost_r2_failed.out.
- R3 RUNNING (bg, 01:47): engine_ab39.out (b205 -> ld-final, 39 ids, n 6) + electron/cost.out. NEXT: watch.py after one finishes; sheet review -> 05-reference/v102/lodestone-picture-sheet.png; beat_dist; StructuredOutput.
- R3 sheet draft reviewed: row-1 labels truncated -> ld_sheet.py labels on two lines (ld_sheet_r2.py kept); the DARK row's touch sat under Gravemourn's "Revenant" banner -> snap.py skips touches under an ult banner (snap_r2.py kept); re-snap grave when a browser slot frees.
- R3 ld_beats.py written (wraps beat/fireUlt/tickRunes from outside; final vs base) -- run when a slot frees.
- R3 ld_carry3.py DONE (carry3.out): rows + voice rows apply on sc-coldiron-temper-fx, sc-ironhail-sunder-fx, sc-ironhail-fxout (+ lodestone 1,2,3,5 by the builder): once, fwd==rev, parse, +22788 each. PASS.
- R3 02:07 engine_ab39 DONE (engine_ab39.out): 39 relics x 6 seeds x 741 pairings, 4446/4446 identical b205 -> ld-final, 0 page errors, 39/39 winners. PASS.
- R3 02:07 electron/cost.out DONE (3 fights, RTX 3070, Electron, interleaved, PC ~96% CPU): whole-frame median rows-off lit +1.8/+1.8/+1.7 ms, touch +3.1/+2.1/+2.8, cast +1.7/+1.7/+2.0, close +0.7/+0.3/+1.4, rest +1.3/+0.1/-0.7 (noise); ALONE (drawLode+Top+caster weapon) +1.2..+2.1 ms in the window, 0 at rest.
- R3 RUNNING: qC.sh (snap grave r3 -> ld_beats -> watch W1 widowmaker 102007 a) + electron/cost_sil.py (square vs conjured head, interleaved in one page). NEXT: sheet -> repo, StructuredOutput.
- R3 02:09 snap grave r3 DONE (touch at 20.35s, no banner; old grave snaps in snaps_r2/). beats.out: 32 fights, 125 casts -> 125 'ult' beats from fireUlt; 0 beats / 0 hit-stop raises inside tickRunes over 1083 touches; beat lists identical to b205. PASS.
- R3 electron/cost_sil.out (spellbreaker): drawWeapon square 11.16 vs conjured 12.66 ms rest, 8.76 vs 9.96 lit (interleaved, one page): the square head is cheaper.
- R3 sheet_draft3.png -> C:/dev/sundered-crown/05-reference/v102/lodestone-picture-sheet.png (sha16 2d2c10a5d6d9f297). RUNNING: watch W1. NEXT: StructuredOutput.
- R3 02:12 watch W1 DONE (watch/W1.mp4 + 7 grids): lodestone v widowmaker 102007 a, Lodestone wins, 73.2s, 4 windows, 36 touches, 0 errors; ends LIT (ultRunes set 77 verdict frames), the picture dark 12 frames (0.4s) after the kill, no rune on a panel frame; runes walk in with the THIRD SEAL. Looked at grids 01 and 06.
- R3 ALL GATES DONE. Calling StructuredOutput (rows = rows_final.json 1ab82ea2383e20de, stamp b40d52b7561c45f2, fx_spec NONE).

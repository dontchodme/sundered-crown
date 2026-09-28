# IRONHAIL / QUARRELSTORM stage 6 PICTURE -- state (resume here)
Base: ../links/sc-ironhail-sunder.html (1bedab05b9803465). Job fresh at 14:05 (nothing on disk before).
Templates: ../../coldiron/stage6-picture (ci_*.py), ../../bindweed/stage6-picture.
Plan: ih_rows.py (rows + lab) -> look (snaps) -> silhouette lineup (6 bows) -> measure (bloom/discs/legibility + controls)
-> verify (sim identity + drawn + sim-write control) -> render_ab -> electron cost -> order/apply test -> fxprobe (fx_spec)
-> sheet 05-reference/v108/ironhail-picture-sheet.png -> rows_final.json -> StructuredOutput.
Names: quarrel* (tickQuarrel, drawQuarrel, drawQuarrelTop?, drawQuarrelGlow, _quarrelLimbs, fields quarrelFade/Age/Out/Seen/Air/Fx/End).
## Log
- (resume after usage cut, 16:55) rows unchanged: ih-final f03b657a1d99d86c. look checked on dawnbringer/gravemourn (snaps/g_dawn.png, g_grave_frames.png).
- bow_sil.py (6 bows, 453x805): ironhail 0.093 last (gloamwire 0.099, marrowdraw 0.122, vinesower .186, farwarden .187, aureole .217).
  variants silv/ (lit edge, rivets, plate): 0.100/0.106/0.110/0.106 -> NOT taken (reads; dark-value design; shipped look). 
- ih_measure.py (method shadowing, controls ctrl1 caster halo / ctrl2 200u landing flash / ctrl3 40u column) + ih_summ.py. m2 running (9 fights).
- 17:10 m2 DONE (m2_summary.txt): bloom share max +0.0006; ctrl1 caster disc 59/63 FAIL, ctrl2 dLift>0.02 15/76 + foe disc 14/76 FAIL, ctrl3 (40u column) inside (+0.0065).
  discs: foe art max +0.0216 (umbral), me -0.0086; >0.90 with 2 = without 2. legib: streak .215 dart .154 ring .172 rune .117 splash .230 sparks .332 tag .163 limbs .179 dust .070 motes .065
- ih_order.py DONE (order.out): 12 rows, stamp f03b657a1d99d86c, rows_final.json f97048b0e0bf1d99; carries on tip, ci-final, bw-final, pc-final; + voice rows_lab both orders.
- RUNNING: ih_verify.py (verify.out), electron/cost.py (cost.out). NEXT: ih_renderab.py, ih_fxprobe.py, look.py spellbreaker 99015 a, snap.py spellbreaker, ih_sheet.py -> 05-reference/v108/ironhail-picture-sheet.png, probe on ih-final-fx.
- 17:40 verify DONE: SIM IDENTITY PASS 14 pairs x (final, final-fx, both drawn); control DIFFERS on all 12 Ironhail fights, identical on 2 without. drawn: found/spot/hit all resolutions (636), tag on every live landing, no throw
- 17:45 kill.out: 4 hail kills drawn OK (puff hit at spot, no tag on the kill frame, cool 0.5s). electron cost DONE (electron/cost.out): ALONE +0.2..+0.6 ms med. RUNNING renderab + fxprobe
- 17:30 renderab: OTHER RELICS 54/54 identical; controls 0/6 both. fxprobe: slot Ironhail's median 0.62s of 8s (7.0%), 15/417 landings in slot, landing 254u median from spawn.
  look.py + snap spellbreaker done; SHEET written C:/dev/sundered-crown/05-reference/v108/ironhail-picture-sheet.png (sha16 da19edc582be8e06, 2200x2942).
  RUNNING: ironhail_probe on ih-final-fx -> probe_final_fx.txt. Then StructuredOutput.
- 17:50 probe on ih-final-fx 9/9, body identical to 06-docs/v108/runs/probe_sunder.txt. ALL GATES DONE. NEXT: StructuredOutput.
- 17:58 sheet sent to user. StructuredOutput next (stamp f03b657a1d99d86c, rows f97048b0e0bf1d99).

#!/bin/bash
# stage 6's small run files -> 06-docs/v107/runs (text/json/py/sh only), named stage6_*
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper
I=$S/s6int; R=$I/runs; D=C:/dev/sundered-crown/06-docs/v107/runs
cp_(){ if [ -f "$1" ]; then cp "$1" "$D/$2"; else echo "MISSING $1"; fi; }
cp_ $I/build_s6.txt stage6_build.txt
cp_ $I/gen_s6.py stage6_gen_s6.py
cp_ $I/s6_rows_recheck.py stage6_rows_recheck.py
cp_ $R/s6_rows_recheck.txt stage6_rows_recheck.txt
cp_ $S/stage6-voice/rows_final.json stage6_voice_rows.json
cp_ $S/stage6-picture/rows_final.json stage6_picture_rows.json
cp_ $S/stage6-voice-report.json stage6_voice_report.json
cp_ $S/stage6-picture-report.json stage6_picture_report.json
cp_ $I/builder_checks6b.sh stage6_builder_checks.sh
cp_ $I/lane_eab.sh stage6_lane_eab.sh
cp_ $I/lane_render.sh stage6_lane_render.sh
cp_ $I/lane2C.sh stage6_lane2C.sh
cp_ $I/compose12.sh compose12.sh
cp_ $R/builder_checks6.txt stage6_builder_checks_3b41.txt
cp_ $R/builder_checks6b.txt stage6_builder_checks.txt
cp_ $I/neg_test6.py stage6_builder_negtest.py
cp_ $R/builder_negtest6.txt stage6_builder_negtest_3b41.txt
cp_ $R/builder_negtest6b.txt stage6_builder_negtest.txt
cp_ $R/builder_negtest3_rerun6.txt builder_negtest3_rerun6_3b41.txt
cp_ $R/builder_negtest3_rerun6b.txt builder_negtest3_rerun6.txt
cp_ $I/ids38.txt stage6_ids38.txt
cp_ $R/engine_ab38.txt stage6_engine_ab38.txt
cp_ $R/engine_ab_control.txt stage6_engine_ab_control.txt
cp_ $I/lane2A.sh stage6_lane2A.sh
cp_ $I/lane2B.sh stage6_lane2B.sh
cp_ $I/mutants6.py stage6_mutants.py
cp_ $R/probe_fx.txt stage6_probe.txt
cp_ $R/probe_fx.json stage6_probe.json
cp_ $R/probe_b9.5_v6.txt probe_b9.5_v6.txt
cp_ $R/probe_mut6_mV1.txt stage6_probe_mut_mV1.txt
cp_ $R/probe_mut6_mP1.txt stage6_probe_mut_mP1.txt
cp_ $R/probe_mut6_mD1.txt stage6_probe_mut_mD1.txt
cp_ $R/probe_fx_twin_mD1.txt stage6_probe_seeds1_drawn30.txt
cp_ $R/render_ab_others.txt stage6_render_ab.txt
cp_ $R/render_ab_control.txt stage6_render_ab_control.txt
cp_ $R/chain_audit_fx_final.txt stage6_chain_audit.txt
cp_ $R/chain_audit_fx_ctl_final.txt stage6_chain_audit_control.txt
cp_ $R/tip_audit_fx.txt stage6_tip_audit_fx.txt
cp_ $R/fx_remove_scratch.txt stage6_fx_remove_scratch.txt
cp_ $R/pick.txt stage6_pick.txt
cp_ $R/clip_log_trim.txt stage6_clip_log.txt
cp_ $R/clip_check.txt stage6_clip_check.txt
cp_ $R/clip_timeline.txt stage6_clip_timeline.txt
cp_ $I/clip_timeline.py stage6_clip_timeline.py
cp_ $I/compose12.sh compose12.sh; cp_ $R/compose12.txt compose12.txt; cp_ $R/compose12.err compose12.err
cp_ $I/compose13.sh compose13.sh; cp_ $R/compose13.txt compose13.txt; cp_ $R/compose13.err compose13.err
cp_ $I/compose14.sh compose14.sh; cp_ $R/compose14.txt compose14.txt; cp_ $R/compose14.err compose14.err
cp_ $I/shapes_draw.py stage6_shapes_draw.py
ls $D | wc -l; du -sh $D
# the probe's first v6 form and its fix (§5d)
cp_ $R/probe_fx_v6first.txt stage6_probe_v6first.txt
cp_ $R/probe_mut6_mV1_v6first.txt stage6_probe_mut_mV1_v6first.txt
cp_ $R/probe_mut6_mP1_v6first.txt stage6_probe_mut_mP1_v6first.txt
cp_ $R/shapes_draw.txt stage6_shapes_draw.txt
cp_ $R/shapes_draw_all.txt stage6_shapes_draw_all.txt
cp_ $I/shapes_draw_all.py stage6_shapes_draw_all.py
cp_ $R/smoke61_fx.txt stage6_probe_smoke_fx.txt
cp_ $R/smoke61_mS1.txt stage6_probe_smoke_mS1.txt
cp_ $R/smoke61_mS2.txt stage6_probe_smoke_mS2.txt
cp_ $R/smoke61_mS1_fxcMap.txt stage6_probe_smoke_mS1_fxcMap.txt
cp_ $I/lane3A.sh stage6_lane3A.sh
cp_ $I/lane3B.sh stage6_lane3B.sh
cp_ $I/copy_runs.sh stage6_copy_runs.sh
ls $D | wc -l; du -sh $D
# the resume of 2026-09-29 08:05: compose15, the rows re-checked on the final builder, the probe on the line's tip
cp_ $I/compose15.sh compose15.sh; cp_ $R/compose15.txt compose15.txt; cp_ $R/compose15.err compose15.err
cp_ $R/s6_rows_recheck_final.txt stage6_rows_recheck.txt
cp_ $R/s6_rows_recheck.txt stage6_rows_recheck_3b41.txt
cp_ $I/lane4P.sh stage6_lane4P.sh
cp_ $R/probe_fx_on_angelus_s1.txt stage6_probe_on_angelus_tip_s1.txt
cp_ $I/lanes.log stage6_lanes_log.txt
cp_ $I/merge_doc.py stage6_merge_doc.py
cp_ $I/copy_runs.sh stage6_copy_runs.sh
ls $D | wc -l; du -sh $D

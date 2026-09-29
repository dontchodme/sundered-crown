#!/bin/bash
# Copy stage 6's small run files into 06-docs/v102/runs/stage6/ (text / json / small scripts only).
L=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone
D=C:/dev/sundered-crown/06-docs/v102/runs/stage6
mkdir -p $D/picture_lab $D/voice_lab $D/mut
cd $L/s6
for f in gen_s6.py gen_s6.out build6.txt expected_fx_sha.txt ids39.txt builder_checks.sh builder_checks.txt \
         builder_controls.py builder_controls.txt compose6.sh compose6.txt patch_probe6.py patch_probe6.out \
         mutants6.py mutants6.txt engine_ab39.txt probe_fx.txt probe_fx.json probe_b205_newprobe.txt \
         probe_b205_newprobe.json probe_fx_s1.txt render_ab_others.txt render_ab_control.txt \
         chain_audit_fx.txt chain_audit_fx_ctl.txt tip_audit_fx.txt tip_audit_diff.txt pick.txt pick.json \
         clip.log clip_timeline.py clip_timeline.txt clip_timeline.json clip_audio_check.py \
         clip_audio_check.txt clip_aac.txt probe_b205_newprobe_diff.txt probe_fx_vs_b205.txt tip_audit_b205_utf8.txt \
         qM.sh qM2.sh qM3.sh qM4.sh stop_qM2.ps1 qM3_killed.txt qM4_stopped.txt report_rows_check.txt builder_checks_recheck.txt splice_doc.py copy_runs6.sh; do
  [ -f "$f" ] && cp "$f" $D/ || echo "missing s6/$f"
done
for f in probe_mut_*.txt; do [ -f "$f" ] && cp "$f" $D/mut/; done
cp lodestone_build.orig.py $D/lodestone_build_before_s6.py; cp lodestone_probe.orig.py $D/lodestone_probe_before_s6.py
cd $L/stage6-picture
for f in STATE.md rows_final.json ld_rows.py ld_order.py ld_carry3.py ld_verify.py ld_verdict.py ld_measure.py ld_summ.py \
         ld_renderab.py ld_beats.py ld_fxprobe.py ham_sil.py order.out carry3.out verify.out verdict.out renderab.out \
         m2_summ.out m2.log probe_final.out engine_ab39.out beats.out fxprobe.out sil_square.out sil_conjured.out \
         sil_stone.json watch.out watch.py electron/cost.out electron/cost_sil.out electron/cost.py \
         electron/cost_sil.py electron/cost_electron.js; do
  [ -f "$f" ] && cp "$f" $D/picture_lab/ || echo "missing picture/$f"
done
cp $L/stage6-picture-report.json $D/picture_lab/report.json
cd $L/stage6-voice
for f in STATE.md rows_final.json run5.log engine_ab_voice.txt chk/engine_ab_simctl.txt chk/beats_ab.txt chk/beats_ab.py \
         render_ab_voice.txt render_ab_ctl.txt probe_voice.txt; do
  [ -f "$f" ] && cp "$f" $D/voice_lab/ || echo "missing voice/$f"
done
cp $L/stage6-voice-report.json $D/voice_lab/report.json
du -sh $D

#!/bin/bash
# Copy v111's run files (txt + json, not the lane logs or the job files) and the scratch tools the doc
# cites into 06-docs/v111/runs/ (the folder is rebuilt from scratch: it is this build's own, untracked).
# The pre-review runs go to runs/prev/. The scratch folder's path is replaced by <scratch> in the text
# files, so nothing machine-specific beyond it is written; json content is copied as it is.
SB=<scratch>
D=C:/dev/sundered-crown/06-docs/v111/runs
rm -rf $D; mkdir -p $D/prev
n=0
for f in $SB/runs/*.txt $SB/runs/*.json; do
  b=$(basename $f)
  case "$b" in jobs*.txt) continue;; esac
  sed "s#$SB#<scratch>#g" $f > $D/$b; n=$((n+1))
done
for f in $SB/runs/prev/*.txt $SB/runs/prev/*.json; do
  sed "s#$SB#<scratch>#g" $f > $D/prev/$(basename $f); n=$((n+1))
done
for t in labx.py make_labx.py unmaking_x.js clock_variant.py mutants.py mutant_table.py stage1_vs_A.py stage5_table.py \
         rr_proof.py ladder.py compose.sh rebuild_check.sh neg_builder.sh lane.sh after.sh n1_inert.py built_same.py \
         review_stage2.py plain_digest.py probe_table.py commands_fix.sh copy_runs.sh \
         gen_s6.py rebuild_check6.sh neg_builder6.sh compose6.sh mutants6.py mutant_table6.py counter_clash.py \
         probe_cmp6.py check_inline.py fxout_scratch.sh clip_timeline6.py clip_audio6.py idle_exec.py lane_r.sh \
         lane_s1.sh lane_s2.sh lane_q2.sh stage6_picture_sb_rows.py stage6_picture_measure.py stage6_picture_verify.py \
         stage6_picture_greycmp.py stage6_picture_fxprobe.py stage6_picture_order.py stage6_picture_tb_sil.py \
         stage6_picture_tagdbg.py; do
  sed "s#$SB#<scratch>#g" $SB/tools/$t > $D/$t; n=$((n+1))
done
echo "$n files -> $D ($(du -sh $D | cut -f1))"

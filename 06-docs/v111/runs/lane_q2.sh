#!/bin/bash
# lane Q, final: the builder's gates re-run on the final builder, one at a time, idle priority
SB=<scratch>
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
I="$PY $SB/s6/idle_exec.py"
$I bash $SB/tools/rebuild_check6.sh > $SB/runs/stage6_rebuild.txt 2>&1
$I bash $SB/tools/neg_builder6.sh > $SB/runs/stage6_builder_negtest.txt 2>&1
$I bash $SB/tools/neg_builder.sh > $SB/runs/stage6_builder_negtest_s1to5.txt 2>&1
$I bash $SB/tools/compose6.sh > $SB/runs/stage6_compose6.txt 2>&1
echo done > $SB/s6/laneQ2.done

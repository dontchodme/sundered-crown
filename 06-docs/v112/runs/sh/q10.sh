#!/bin/bash
# STAGE 6 GATES, lane 1 (Idle priority): engine_ab b11 -> b11-fx over ALL 38 ids (Heartwood included), n=6; then its control
# (the picture's hook writing the sim, mut-s6-grove-sim) on four ids, Heartwood among them.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
R=$S/runs; L=$S/links
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) lane1 $1" >> $R/q10.log; }
powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass = 'Idle'" && log "Idle"
IDS=$(paste -sd, $R/ids38.txt)
$PY engine_ab.py --a $L/sc-heartwood-b11.html --b $L/sc-heartwood-b11-fx.html --ids $IDS --n 6 > $R/stage6_engine_ab38.txt 2>&1; log "engine_ab38 rc=$?"
$PY engine_ab.py --a $L/sc-heartwood-b11.html --b $S/mut/mut-s6-grove-sim.html --ids heartwood,grudgebearer,aureole,gravemourn --n 6 > $R/stage6_engine_ab_control.txt 2>&1; log "engine_ab control rc=$?"
log end

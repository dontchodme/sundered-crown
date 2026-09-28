#!/bin/bash
# v108 stage 6, resumed: the two runs slotB never reached (cut off at mS4). Two browsers (the task's cap).
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
echo "start $(date +%H:%M:%S)" > "$S/s6/slotC.log"
( { $PY ironhail_probe.py --game "$S/s6/mut/sc-ironhail-mS4-draw-writes.html" --seeds 1; echo "exit $?"; } > "$S/s6/probe_mut_mS4-draw-writes.txt" 2>&1; echo "mut mS4 $(date +%H:%M:%S)" >> "$S/s6/slotC.log" ) &
( { $PY ironhail_probe.py --game "$S/links/sc-ironhail-sunder.html" --json "$S/s6/probe_sunder_newprobe.json"; echo "exit $?"; } > "$S/s6/probe_sunder_newprobe.txt" 2>&1; echo "probe sunder $(date +%H:%M:%S)" >> "$S/s6/slotC.log" ) &
wait
echo done > "$S/s6/slotC.done"

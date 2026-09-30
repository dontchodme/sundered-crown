#!/bin/bash
# RESUME 3 (2026-09-30): LANE 1 -- verify on the final (stage 5, sc-heartwood-b11), n 40. The earlier run (q4's last job) was cut.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
R=$S/runs; F=$S/links/sc-heartwood-b11.html
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date '+%m-%d %H:%M:%S') $*" >> $R/q7.log; }
log start; powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass = 'Idle'" && log "Idle; final $(sha256sum $F | cut -c1-16)"
$PY verify.py --game $F --n 40 > $R/verify_final.txt 2>&1; log "verify final n40 rc=$?"
log end

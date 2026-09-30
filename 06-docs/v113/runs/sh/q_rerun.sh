#!/bin/bash
# THE FINAL PROBE on the runs made before its last (coverage-only) edit: the final, m1-m5. Then the mutant table.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/q_rerun.log; }
while ! grep -q "end" $S/runs/q_final_probe.log 2>/dev/null; do sleep 10; done
log start
$PY thornwake_probe.py --game $S/links/sc-thornwake-b26.5.html --stage 5 --json $S/runs/probe_final.json > $S/runs/probe_final.txt 2>&1; log "probe final rc=$?"
for m in m1-window-labclock m2-every-other-blow m3-cleared-at-close m3b-radius-plus10 m4-weapon-free m5-entangle-2; do
  $PY thornwake_probe.py --game $S/mut/mut-$m.html --stage 5 --json $S/runs/probe_mut-$m.json > $S/runs/probe_mut-$m.txt 2>&1; log "probe mut-$m rc=$?"
done
$PY $S/tools/mutant_table.py $S > /dev/null 2>&1; log "mutant table rc=$?"
log end

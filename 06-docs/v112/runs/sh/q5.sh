#!/bin/bash
# THE FINAL (stage 5, blade 11) AGAINST ITS LAB ARM: the lab's arm C at the final's numbers (charge 15 on the lab's clock,
# rootFor 1.0, --P blade=11) and at the engine's window (dur 9.42), and the built link's own ultimate (arm SHIP), side A,
# the design's 33 foes x 20 seeds, both blocks. ONE JOB AT A TIME. Log q5.log.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
R=$S/runs
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
log(){ echo "$(date +%H:%M:%S) $*" >> $R/q5.log; }
log start; powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass = 'Idle'" && log "this shell at Idle priority (winpid $(cat /proc/$$/winpid)); every child inherits it"
for B in 2207 2317; do
  $PY $S/tools/rf_lab.py --game C:/dev/sundered-crown/02-chain/sc-tendril-t3.html --relic heartwood --mech C:/dev/sundered-crown/tools/overlays/rootfast.js --arms C --P rootFor=1.0 charge=15 blade=11 --seeds 20 --seed0 $B --foes $(cat $R/foes33.txt) --label "lab C at the final's blade 11, charge 15, block $B" --out $R/lab_c15_b11_$B.json > $R/lab_c15_b11_$B.txt 2>&1; log "lab C c15 blade 11 $B rc=$?"
  $PY $S/tools/rf_lab.py --game C:/dev/sundered-crown/02-chain/sc-tendril-t3.html --relic heartwood --mech C:/dev/sundered-crown/tools/overlays/rootfast.js --arms C --P rootFor=1.0 charge=15 blade=11 dur=9.42 --seeds 20 --seed0 $B --foes $(cat $R/foes33.txt) --label "lab C at the final's blade 11, charge 15, the engine's window 9.42, block $B" --out $R/lab_c15_b11_dur942_$B.json > $R/lab_c15_b11_dur942_$B.txt 2>&1; log "lab C c15 blade 11 dur 9.42 $B rc=$?"
  bash $R/built.sh sc-heartwood-b11 b11 $B; log "built b11 $B rc=$?"
done
log end

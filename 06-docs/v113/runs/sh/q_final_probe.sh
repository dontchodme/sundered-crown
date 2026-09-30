#!/bin/bash
# LANE A: the probe on the final (stage 5), the mutants of the final, the probe re-run on stages 3 and 2. $1 = BLADE
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
F=$S/links/sc-thornwake-b$1.html
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/q_final_probe.log; }
log start
$PY thornwake_probe.py --game $F --stage 5 --json $S/runs/probe_final.json > $S/runs/probe_final.txt 2>&1; log "probe final (stage 5) rc=$?"
rm -rf $S/mut; $PY $S/tools/mutants.py $F $S/mut $1 > $S/runs/mutants_shas.txt 2>&1; log "mutants written rc=$?"
for m in $(sed -n 's/^\(m[0-9a-z-]*\) .*/\1/p' $S/runs/mutants_shas.txt); do
  $PY thornwake_probe.py --game $S/mut/mut-$m.html --stage 5 --json $S/runs/probe_mut-$m.json > $S/runs/probe_mut-$m.txt 2>&1; log "probe mut-$m rc=$?"
done
$PY $S/tools/mutant_table.py $S > /dev/null 2>&1; log "mutant table rc=$?"
$PY thornwake_probe.py --game $S/links/sc-thornwake-snare.html --stage 3 --json $S/runs/probe_snare.json > $S/runs/probe_snare.txt 2>&1; log "probe snare (stage 3) rc=$?"
$PY thornwake_probe.py --game $S/links/sc-thornwake-bramble.html --stage 2 --json $S/runs/probe_bramble.json > $S/runs/probe_bramble.txt 2>&1; log "probe bramble (stage 2) rc=$?"
log end

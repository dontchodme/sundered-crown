#!/bin/bash
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/q_probe23.log; }
$PY thornwake_probe.py --game $S/links/sc-thornwake-bramble.html --stage 2 --json $S/runs/probe_bramble.json > $S/runs/probe_bramble.txt 2>&1; log "probe bramble (stage 2) rc=$?"
$PY thornwake_probe.py --game $S/links/sc-thornwake-snare.html --stage 3 --json $S/runs/probe_snare.json > $S/runs/probe_snare.txt 2>&1; log "probe snare (stage 3) rc=$?"

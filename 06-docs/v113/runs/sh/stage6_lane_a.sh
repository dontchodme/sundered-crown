#!/bin/bash
# lane A: stage 6's probe runs and mutants -- one browser, idle priority
T=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
I="$PY $T/s6/idle_exec.py $PY"
cd C:/dev/sundered-crown/tools
L=$T/links; R=$T/runs; M=$T/mut6
log(){ echo "$(date +%H:%M:%S) $*" >> $T/s6/laneA.log; }
log start
$I thornwake_probe.py --game $L/sc-thornwake-b26.5-fx.html --stage 6 --json $R/stage6_probe_fx.json > $R/stage6_probe_fx.txt 2>&1; log "probe fx rc $?"
$I thornwake_probe.py --game $L/sc-thornwake-b26.5.html --stage 5 --json $R/stage6_probe_b26.5.json > $R/stage6_probe_b26.5.txt 2>&1; log "probe b26.5 (new probe) rc $?"
$I thornwake_probe.py --game $L/sc-thornwake-b26.5-fx.html --stage 6 --seeds 1 --json $R/stage6_probe_fx_s1.json > $R/stage6_probe_fx_s1.txt 2>&1; log "probe fx s1 rc $?"
for m in mV1-closevoice mP1-picwrite mP2-invisible; do
  $I thornwake_probe.py --game $M/$m.html --stage 6 --seeds 1 --json $R/stage6_probe_mut_$m.json > $R/stage6_probe_mut_$m.txt 2>&1; log "probe $m rc $?"
done
$I thornwake_probe.py --game $L/sc-thornwake-b26.5-fx.html --stage 6 --seeds 1 --drawn 24 --json $R/stage6_probe_fx_drawn.json > $R/stage6_probe_fx_drawn.txt 2>&1; log "probe fx drawn rc $?"
log done
echo done > $T/s6/laneA.done

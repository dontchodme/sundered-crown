#!/bin/bash
# THE PROBE AFTER THE m2 FINDING ([3] and [5] read the blows that rooted; [2] whether a blow rooted): every stage
# from 2 and all eleven mutants again, then the mutant table. ONE JOB AT A TIME, Idle priority. Log q6.log.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
R=$S/runs; L=$S/links
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) $*" >> $R/q6.log; }
log start; powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass = 'Idle'" && log "Idle; probe $(sha256sum heartwood_probe.py | cut -c1-16)"
mkdir -p $R/probe_first; mv $R/probe_*.txt $R/probe_*.json $R/probe_first/ 2>/dev/null
$PY heartwood_probe.py --game $L/sc-heartwood-b11.html --stage 5 --json $R/probe_b11.json > $R/probe_b11.txt 2>&1; log "probe b11 (stage 5, the final) rc=$?"
$PY heartwood_probe.py --game $L/sc-heartwood-rootfast.html --stage 3 --json $R/probe_rootfast.json > $R/probe_rootfast.txt 2>&1; log "probe rootfast (stage 3) rc=$?"
$PY heartwood_probe.py --game $L/sc-heartwood-root.html --stage 2 --json $R/probe_root.json > $R/probe_root.txt 2>&1; log "probe root (stage 2) rc=$?"
for n in m1-window-labclock m2-every-other-blow m3-pin-before-knock m4-weapon-free m5-entangle-2 m6-root-hitstop m7-charge16 m8-row-no-entangle m9-root-stundr m10-ticker-stundr m11-blade-shipped; do
  $PY heartwood_probe.py --game $S/mut/mut-$n.html --stage 5 --json $R/probe_mut-$n.json > $R/probe_mut-$n.txt 2>&1; log "probe mut-$n rc=$?"
done
$PY $S/tools/mutant_table.py $S > /dev/null 2>&1; log "mutant table rc=$?"
log end

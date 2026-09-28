#!/bin/bash
# v103 review fix: the probe v2 (window-clock check in [1]) on stages 2-5 and on every scratch mutant.
# two slots (one browser each): ./probes_v2.sh A | ./probes_v2.sh B
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
cd C:/dev/sundered-crown/tools
mut(){ $PY coldiron_probe.py --game "$S/mutants_v2/mut-$1.html" > "$S/runs/probe_mut_$1.txt" 2>&1; echo "exit $?" >> "$S/runs/probe_mut_$1.txt"; }
if [ "$1" = A ]; then
  $PY coldiron_probe.py --game "$S/links/sc-coldiron-temper-b93.html" --json "$S/runs/probe_b93.json" > "$S/runs/probe_b93.txt" 2>&1
  for L in mass bind temper; do
    $PY coldiron_probe.py --game "$S/links/sc-coldiron-$L.html" --json "$S/runs/probe_$L.json" > "$S/runs/probe_$L.txt" 2>&1
  done
  for m in m1-window-long m2b-clank-sideA m2-clank-light; do mut $m; done
else
  for m in r1-window-through-hitstop r2-sunder-opponent m3-bind-one m4-cap-stays m6-move-light m7b-close-stop m7-open-stop; do mut $m; done
fi
echo "slot $1 done"

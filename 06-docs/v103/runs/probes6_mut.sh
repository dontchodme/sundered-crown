#!/bin/bash
# stage 6: the probe (db6a380e) on the four stage-6 mutants, one browser, in turn
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
cd C:/dev/sundered-crown/tools
for m in mS1-close-on-death mS3-iron-writes mS2-anvil-count-before mS4-draw-writes; do
  echo "coldiron_probe.py --game s6/mut/mut-$m.html   $(date '+%F %T')" > "$S/s6/probe_mut_$m.txt"
  $PY -u coldiron_probe.py --game "$S/s6/mut/mut-$m.html" >> "$S/s6/probe_mut_$m.txt" 2>&1
  echo "exit $?" >> "$S/s6/probe_mut_$m.txt"
done
echo done > "$S/s6/probes6_mut.done"

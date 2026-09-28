#!/bin/bash
# the probe on each scratch mutant of the final link (each must fail its own check and only it),
# then the probe re-run on stages 2-4 with the probe's final wording. sequential: one browser.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
cd C:/dev/sundered-crown/tools
: > "$S/runs/probe_mutants.txt"
for m in m1-window-long m2-clank-light m3-bind-one m4-cap-stays m6-move-light m7-open-stop; do
  echo "=== mut-$m" >> "$S/runs/probe_mutants.txt"
  $PY coldiron_probe.py --game "$S/mutants/mut-$m.html" >> "$S/runs/probe_mutants.txt" 2>&1
  echo "exit $?" >> "$S/runs/probe_mutants.txt"
done
for L in mass bind temper; do
  $PY coldiron_probe.py --game "$S/links/sc-coldiron-$L.html" --json "$S/runs/probe_$L.json" > "$S/runs/probe_$L.txt" 2>&1
done
echo done

#!/bin/bash
# slot 2 after the stage probes: the two replacement mutants, the bind pick, then verify --n 40 on stage 1.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
cd C:/dev/sundered-crown/tools
until [ "$S/runs/probe_temper.txt" -nt "$S/runs/probe_mutants.txt" ] && grep -q -E "/7$|Traceback" "$S/runs/probe_temper.txt"; do sleep 5; done
: > "$S/runs/probe_mutants2.txt"
for m in m2b-clank-sideA m7b-close-stop; do
  echo "=== mut-$m" >> "$S/runs/probe_mutants2.txt"
  $PY coldiron_probe.py --game "$S/mutants/mut-$m.html" >> "$S/runs/probe_mutants2.txt" 2>&1
  echo "exit $?" >> "$S/runs/probe_mutants2.txt"
done
$PY "$S/runs/bind_pick.py" "$S/links/sc-coldiron-temper-b93.html" 3 > "$S/runs/bind_pick.txt" 2>&1
$PY verify.py --game "$S/links/sc-coldiron.html" --n 40 > "$S/runs/verify_s1.txt" 2>&1
echo slot2 done

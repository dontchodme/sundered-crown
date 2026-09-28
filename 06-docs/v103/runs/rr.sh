#!/bin/bash
# stage 5: relic_rate, both sides, every other relic a foe, 10 seeds a foe a side. usage: rr.sh <link> <tag> <seed0> [--set ...]
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
L=$1; T=$2; B=$3; shift 3
cd C:/dev/sundered-crown/tools
$PY relic_rate.py --game "$S/links/$L.html" --relic coldiron --n 10 --seed0 $B --label "$T" --json "$S/runs/stage5_rr_${T}_$B.json" "$@" > "$S/runs/stage5_rr_${T}_$B.txt" 2>&1
cat "$S/runs/stage5_rr_${T}_$B.txt"
